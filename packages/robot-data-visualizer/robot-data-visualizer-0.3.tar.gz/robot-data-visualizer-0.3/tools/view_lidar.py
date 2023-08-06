"""lidar_viewer visualizes lidar data by ploting it in matplotlib window."""

import datetime
from matplotlib.patches import Arc
import matplotlib.pyplot as plt
import numpy as np


def hokuyo_plot(axis):
    """
    Creates plot of xy lidar data with lidar
    range arc plotted in blue line.

    Keyword arguments:
    x_lidar -- x components of lidar scan
    y_lidar -- y components of lidar scan
    time    -- time stamp of lidar scan
    """

    # copied and modified from:
    # https://github.com/matplotlib/matplotlib/issues/8046/#issuecomment-278312361
    # Circle parameters
    # set arc diameters
    diameter = [2, 60]
    #arc center
    center = 0
    #time to wait between plots
    delay = 0.1
    #convert epoch time to datetime format

    #plot inner arc
    axis.add_patch(Arc((center, center), diameter[0], diameter[0],
                       theta1=-45, theta2=225, edgecolor='b', linewidth=1.5))
    #plot outer arc
    axis.add_patch(Arc((center, center), diameter[1], diameter[1],
                       theta1=-45, theta2=225, edgecolor='b', linewidth=1.5))
    # start and end points for lidar boundary lines
    line_start_end = [0.8, 21.21]
    # x & y coordinates for line 1
    line_start_x, line_end_x = line_start_end[0], line_start_end[1]
    line_start_y, line_end_y = -line_start_end[0], -line_start_end[1]
    # plot line 1
    axis.plot([line_start_x, line_end_x], [line_start_y, line_end_y], 'b')
    # x & y coordinates for line 2
    line_start_x, line_end_x = -line_start_end[0], -line_start_end[1]
    line_start_y, line_end_y = -line_start_end[0], -line_start_end[1]
    # plot line 2
    axis.plot([line_start_x, line_end_x], [line_start_y, line_end_y], 'b')


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