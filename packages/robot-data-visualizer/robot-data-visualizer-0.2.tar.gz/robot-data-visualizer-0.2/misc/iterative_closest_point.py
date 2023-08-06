"""

Iterative Closest Point (ICP) SLAM example

author: Atsushi Sakai (@Atsushi_twi)

"""

import math
import numpy as np
import matplotlib.pyplot as plt
import datetime
import sys
sys.path.append('..')

import traceback
from tools.data_manager import DataManager

#  ICP parameters
EPS = 0.0001
MAXITER = 100

show_animation = True


def ICP_matching(ppoints, cpoints,time):
    """
    Iterative Closest Point matching

    - input
    ppoints: 2D points in the previous frame
    cpoints: 2D points in the current frame

    - output
    R: Rotation matrix
    T: Translation vector

    """
    H = None  # homogeneraous transformation matrix

    dError = 1000.0
    preError = 1000.0
    count = 0
    LOWERBOUND = 0
    UPPERBOUND = 2
    DIMENSION = 3
    while dError >= EPS:
        count += 1
        '''
        if show_animation:
            plt.cla()
            plt.plot(ppoints[0, :], ppoints[1, :], ".r")
            plt.plot(cpoints[0, :], cpoints[1, :], ".b")
            plt.plot(0.0, 0.0, "xr")
            plt.axis("equal")
            plt.title(time)
            plt.pause(0.1)
        '''
        inds, error = nearest_neighbor_assosiation(ppoints, cpoints)
        Rt, Tt = SVD_motion_estimation(ppoints[:, inds], cpoints)

        # update current points
        cpoints = (Rt * cpoints) + Tt

        H = update_homogeneous_matrix(H, Rt, Tt)

        dError = abs(preError - error)
        preError = error
        #print("Residual:", error)

        if dError <= EPS:
            #print("Converge", error, dError, count)
            break
        elif MAXITER <= count:
            print("Not Converge...", error, dError, count)
            break

    R = np.matrix(H[LOWERBOUND:UPPERBOUND, LOWERBOUND:UPPERBOUND])
    T = np.matrix(H[LOWERBOUND:UPPERBOUND, UPPERBOUND])

    return R, T


def update_homogeneous_matrix(Hin, R, T):
    """
    Update the homogeneous matrix (translation and rotation matrices combined)

    - input
    Hin: initial/previous homogeneous matrix
    R: rotation matrix
    T: Translation matrix

    - output
    H: updated homogeneous matrix

    Parameters
    ----------
    H
        The updated homogeneous matrix.
    Hin
        The initial/previous homogeneous matrix.
    R
        The rotation matrix.
    T
        The translation matrix.

    """
    H = np.matrix(np.zeros((3, 3)))

    H[0, 0] = R[0, 0]
    H[1, 0] = R[1, 0]
    H[0, 1] = R[0, 1]
    H[1, 1] = R[1, 1]
    H[2, 2] = 1.0

    H[0, 2] = T[0, 0]
    H[1, 2] = T[1, 0]

    if Hin is not None:
        H = Hin * H
    return H

def nearest_neighbor_assosiation(ppoints, cpoints):
    """
    Associates new LIDAR points with previous LIDAR points

    - input
    ppoints: 2D points in the previous frame
    cpoints: 2D points in the current frame

    - output
    inds: indices
    error: normalized difference in
    current and previous 2D points

    """
    # calculate the sum of residual errors
    dcpoints = ppoints - cpoints
    d = np.linalg.norm(dcpoints, axis=0)
    error = sum(d)

    # calc index with nearest neighbor association
    inds = []
    for i in range(cpoints.shape[1]):
        minid = -1
        mind = float("inf")
        for ii in range(ppoints.shape[1]):
            d = np.linalg.norm(ppoints[:, ii] - cpoints[:, i])

            if mind >= d:
                mind = d
                minid = ii

        inds.append(minid)

    return inds, error


def SVD_motion_estimation(ppoints, cpoints):
    """
    performs single value decomposition
    to determine rotation and translation

    - input
    ppoints: 2D points in the previous frame
    cpoints: 2D points in the current frame

    - output
    R: rotation angle
    t: translation

    """
    pm = np.matrix(np.mean(ppoints, axis=1))
    cm = np.matrix(np.mean(cpoints, axis=1))

    pshift = np.matrix(ppoints - pm)
    cshift = np.matrix(cpoints - cm)

    W = cshift * pshift.T
    u, s, vh = np.linalg.svd(W)

    R = (u * vh).T
    t = pm - R * cm

    return R, t

def choose_lidar_pts(i, data_i):
    min_lidar_pts = 100
    x, y, time = data_i
    #print(x)
    x_index = np.nonzero(x)
    x_index_str = str(x_index)
    #print(x_index)
    y_index = np.nonzero(y)
    #print(y_index)
    y_index_str = str(y_index)
    #print(y_index)
    is_equal = x_index_str == y_index_str
    enough_lidar = len(x) > min_lidar_pts
    x = x[np.nonzero(x)]
    y = y[np.nonzero(y)]

    if is_equal == True & enough_lidar == True:
        return (x, y , time)
    else:
        x = i
        y = i
        time = i
        return (x, y, time)


def main():
    print(__file__ + " start!!")

    # simulation parameters

    #specify date
    dm = DataManager('2012-04-29')
    print('DataManager initialized')
    # Download and extract sensor data
    dm.setup_data_files('sensor_data')
    print('sensor data downloaded')
    # Download and extract data for the hokuyo lidar scanner
    dm.setup_data_files('hokuyo')

    # load scans of lidar
    num_samples = 10000
    step_size = 10
    delay = 0.1
    print('hokuyo data loading...')
    dm.load_lidar(num_samples, 'pickled', 'delete')
    lidar = dm.data_dict['lidar']
    print('running SLAM')
    for i in range(0,int(num_samples/step_size),step_size):
        #get previous and current points
        k = i
        k_next = k + 1
        j = -1
        lidar_i = lidar[i]
        x, y, time = choose_lidar_pts(i, lidar_i)
        x_not_equal_time = str(x) != str(time)
        if x_not_equal_time == True:
            #previous points
            px, py, time = x, y, time
            check_length = len(x) == len(y)
            ppoints = np.matrix(np.vstack((px, py)))
            #current points
            lidar_k = lidar[k]
            x2,y2, time2 = choose_lidar_pts(k,lidar_k)
            x2_not_equal_time2 = str(x2) != str(time2)
            if x2_not_equal_time2:
                cx, cy, time = choose_lidar_pts(k,lidar_k)
                cpoints = np.matrix(np.vstack((cx, cy)))
            else:
                while k != j:
                    k = k_next
                    x2, y2, time2 = choose_lidar_pts(k, lidar_k)
                    x2_not_equal_time2 = str(x2) != str(time2)
                    if x2_not_equal_time2:
                        cx, cy, time2 = choose_lidar_pts(k, lidar_k)
                        cpoints = np.matrix(np.vstack((cx, cy)))
                        j = k
                        i = k


        R, T = ICP_matching(ppoints, cpoints,time2)
        #print('R =', R)
        #print('T =', T)

        if i == 0:
            pose_xy = np.array([[0],[0]])
            pose_uv = np.array([[0],[1]])
            '''
            X = 0
            Y = 0
            THETA = 0
            U = np.cos(THETA)
            V = np.sin(THETA)
            '''
        else:

            pose_xy = np.array([X, Y])
            pose_uv = np.array([U, V])

        new_pose_xy= pose_xy + np.array(T)
        a = np.array(R)
        new_pose_uv= a.dot(pose_uv)
        X = new_pose_xy[0]
        Y = new_pose_xy[1]
        U = new_pose_uv[0]
        V = new_pose_uv[1]

        plt.quiver(X, Y, U, V)
        plt.axis("equal")
        plt.title(time)
        plt.pause(delay)
        plt.cla()

if __name__ == '__main__':
    main()
