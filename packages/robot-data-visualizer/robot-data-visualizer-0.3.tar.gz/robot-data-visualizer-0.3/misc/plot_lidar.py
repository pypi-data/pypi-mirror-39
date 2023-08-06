"""Plots hokuyo lidar data."""
from matplotlib.patches import Arc
import matplotlib.pyplot as plt
def hokuyo_plot(x_lidar, y_lidar, time):
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

    # Figure setup
    fig, axes = plt.subplots()
    # delete unused argument 'fig'
    del fig
    #plot inner arc
    axes.add_patch(Arc((center, center), diameter[0], diameter[0],
                       theta1=-45, theta2=225, edgecolor='b', linewidth=1.5))
    #plot outer arc
    axes.add_patch(Arc((center, center), diameter[1], diameter[1],
                       theta1=-45, theta2=225, edgecolor='b', linewidth=1.5))
    # start and end points for lidar boundary lines
    line_start_end = [0.8, 21.21]
    # x & y coordinates for line 1
    line_start_x, line_end_x = line_start_end[0], line_start_end[1]
    line_start_y, line_end_y = -line_start_end[0], -line_start_end[1]
    # plot line 1
    plt.plot([line_start_x, line_end_x], [line_start_y, line_end_y], 'b')
    # x & y coordinates for line 2
    line_start_x, line_end_x = -line_start_end[0], -line_start_end[1]
    line_start_y, line_end_y = -line_start_end[0], -line_start_end[1]
    # plot line 2
    plt.plot([line_start_x, line_end_x], [line_start_y, line_end_y], 'b')
    # plot lidar points
    plt.plot(x_lidar, y_lidar, '.')
    # plot title of time in datetime format
    plt.title(time)
    # label x axis
    plt.xlabel('Distance (meters)')
    # set axis limits
    axes = plt.gca()
    xlimits, ylimits = [-32, 32], [-32, 32]
    axes.set_xlim(xlimits)
    axes.set_ylim(ylimits)
    # wait to close plot for 'delay' seconds
    plt.pause(delay)
    # close plot
    plt.close()
