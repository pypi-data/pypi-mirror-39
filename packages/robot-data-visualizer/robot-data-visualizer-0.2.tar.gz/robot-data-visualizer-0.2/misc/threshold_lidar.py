import numpy as np

def threshold_lidar_pts(data_i):
    """
    Set points in lidar frame with values less than one
    to zero and remove all zeros from lidar frame.
    Keyword arguments:
    data_i -- lidar frame (x points, y points, timestamp)
    """
    # value below which to threshold data
    thresh = 1
    x_lidar, y_lidar, time = data_i
    # index x and y values below threshold
    index_x = np.where(np.logical_and(abs(x_lidar) > 0, abs(x_lidar) < thresh))
    index_y = np.where(np.logical_and(abs(y_lidar) > 0, abs(y_lidar) < thresh))
    x_lidar[index_x] = 0
    y_lidar[index_y] = 0

    x_index = np.nonzero(x_lidar)
    y_index = np.nonzero(y_lidar)
    # convert index list to string for comparison
    # and check equality
    x_index_str = str(x_index)
    y_index_str = str(y_index)
    is_equal = x_index_str == y_index_str
    # if indexes match, remove 0 points all at once
    if is_equal:
        x_lidar = x_lidar[np.nonzero(x_lidar)]
        y_lidar = y_lidar[np.nonzero(y_lidar)]
    #else, remove 0 points one by one
    else:
        index = []
        count = 0
        while count < len(x_lidar):
            if x_lidar[count] == 0 and x_lidar[count] == y_lidar[count]:
                index = np.append(index, count)
            count = count + 1
        x_lidar = np.delete(x_lidar, index)
        y_lidar = np.delete(y_lidar, index)
    # return filtered data
    return (x_lidar, y_lidar, time)