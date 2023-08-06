"""lidar_viewer visualizes lidar data by ploting it in matplotlib window."""

import sys

from tools.data_manager import DataManager
from time_convert import epoch_to_date_time
from plot_lidar import hokuyo_plot
from threshold_lidar import threshold_lidar_pts
sys.path.append('..')
def lidar_viewer(date, num_samples, step_size=40, pickled=False, delete_pickle=False):
    """
    lidar_viewer visualizes lidar data by ploting it in matplotlib window.

    :param date: A 'Session' date from http://robots.engin.umich.edu/nclt/ (string)
    :param num_samples: The number of lidar frames to view (int)
    :param step_size: The amount of frames to skip between plots (data recorded at 40Hz)
    :param pickled: Set to True if you want to save a pickle imported lidar data.
    :param delete_pickle: Set to True if you want to delete any existing pickles of data.
    """
    # initialize datamanager
    data_manager = DataManager(date)
    print('DataManager initialized')
    # Download and extract sensor data
    data_manager.setup_data_files('sensor_data')
    print('sensor data downloaded')
    # Download and extract data for the hokuyo lidar scanner
    data_manager.setup_data_files('hokuyo')

    # load scans of lidar

    print('hokuyo data loading...')
    data_manager.load_lidar(num_samples, pickled, delete_pickle)
    lidar = data_manager.data_dict['lidar']
    print('plotting lidar')
    for i in range(0, int(num_samples/step_size)*step_size, step_size):
        lidar_i = lidar[i]
        x_lidar, y_lidar, time = threshold_lidar_pts(lidar_i)
        x_not_equal_time = str(x_lidar) != str(time)
        if x_not_equal_time:
            time = epoch_to_date_time(time)
            hokuyo_plot(x_lidar, y_lidar, time)
