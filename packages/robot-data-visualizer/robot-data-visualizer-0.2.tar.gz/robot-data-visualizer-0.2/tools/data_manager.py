import os
import pickle
from tools.data_loader import DataLoader
from tools.read_hokuyo_30m import read_hokuyo
from tools.tar_extract import tar_extract
from tools.download_tar import download_tar


class DataManager:
    '''
    This class handles downloading, extracting and storing data to be used by the main application.
    '''

    def __init__(self, date):
        self.owd = os.path.abspath('.')
        self.data_dir_name = 'data'
        self.base_name = 'http://robots.engin.umich.edu/nclt'
        self.date = date
        self.data_dir = os.path.join(self.owd, os.path.join(self.data_dir_name, self.date))
        self.data_dict = {}

    def setup_data_files(self, data_type):
        '''
        This function sets up data files by downloading and extracting them into the *data* directory.

        :param data_type: Selects lidar or GPS data.
        :type data_type: str.
        :return: None
        '''
        filename = download_tar(self.base_name, self.date, data_type)
        tar_extract(filename)
        os.chdir(self.owd)

    def load_gps(self):
        '''
        This function loads data into the data manager's data dictionary.

        :return: None
        '''
        os.chdir(self.owd)
        gps_file_path = os.path.join(self.data_dir_name, os.path.join(self.date, 'gps.csv'))
        data_loader = DataLoader(gps_file_path)
        self.data_dict['gps'] = data_loader.get_gps_dictionary()
        self.data_dict['gps_range'] = data_loader.get_gps_range()

    def load_lidar(self, num_samples, pickled=None, delete_pickle=None):
        '''
        This function loads lidar, with the option to use a pickled file.

        :param num_samples: Number of samples to load
        :type num_samples: int.
        :param pickled: If *pickled='pickled'*, load from existing pickle of lidar, otherwise use existing
            and save a pickle of the data.
        :type pickled: str.
        :param delete_pickle: If *delete_pickle='delete'*, delete any existing pickle of lidar.
        :type delete_pickle: str.
        '''
        os.chdir(self.owd)
        lidar_file_path = os.path.join(self.data_dir_name,
                                       os.path.join(self.date, 'hokuyo_30m.bin'))
        if delete_pickle == 'delete':
            if os.path.exists("lidar.pickle"):
                os.remove("lidar.pickle")
                print("there is no pickle to delete")
        if pickled == 'pickled':
            try:
                pickled_lidar = pickle.load(open("lidar.pickle", "rb"))
                self.data_dict['lidar'] = pickled_lidar
            except (OSError, IOError) as e:
                self.data_dict['lidar'] = read_hokuyo(lidar_file_path, num_samples)
                pickled_lidar = self.data_dict['lidar']
                pickle.dump(pickled_lidar, open("lidar.pickle", "wb"))
        else:
            self.data_dict['lidar'] = read_hokuyo(lidar_file_path, num_samples)

    def load_all(self):
        '''
        This function loads both the GPS and lidar data.

        :return: None
        '''
        self.load_gps()
        self.load_lidar(100)    # Note this could take a while - loads a lot of samples

    def get_data(self, key=None):
        '''
        This function gets data from the data manager's data dictionary.

        :return: value of data at *key*
        '''
        if key is None:
            return self.data_dict
        return self.data_dict[key]
