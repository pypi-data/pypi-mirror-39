"""
This class is responsible for precessing data correctly corresponding to the user's choice.
"""
import numpy as np
import os
# __all__=['DataLoader']
DEGREE = 180

class DataLoader:
    """
    A class to load data according to user's choose, and do some preprocess to data.
    It can be usedin this way:

    dataloader = Dataloader(choose)
    dataloader.get_gps_dictionary()
    dataloader.get_gps_range()

    """
    def __init__(self, choose):
        # self.data_dir = '/data'
        self.chosen_data = choose
        self.gps_dictionary = self.load_data()

    # def choose_dataset(self):
    #     """
    #     Get user's choose and then return a correct file name
    #     :param choose: User's choose of which dataset to use
    #     :return: The corresponding file name
    #     """
    #     if self.chosen_data == 'Dataset1':
    #         return 'gps1.csv'
    #     elif self.chosen_data == 'Dataset2':
    #         return 'gps2.csv'
    #     elif self.chosen_data == 'Dataset3':
    #         return 'gps3.csv'

    # def choose_path(self):
    #     """
    #     To the directory fot the data, get the path.
    #     :return: The path of the data files
    #     """
    #     path = os.path.abspath(os.path.dirname(os.getcwd()))
    #     path += self.data_dir
    #     return path

    def load_data(self):
        """
        Load the data chosen by user, and get the gps's three coordinate from data file.
        :return: A dictionary contains three gps coordinate.
        """
        # path = self.choose_path()
        # os.chdir(path)
        file_name = self.chosen_data
        path = os.path.join(os.path.abspath('.'), file_name)
        gps = np.loadtxt(path, delimiter=",")

        # Get three coordinates of GPS and timestamp
        tstamp = gps[:, 0]
        lat = gps[:, 3]
        lng = gps[:, 4]
        alt = gps[:, 5]
        # Store three coordinates into a dictionary
        # Transform radius to angle
        gps_dictionary = {}
        gps_dictionary['tstamp'] = tstamp
        gps_dictionary['lat'] = lat * 180 / np.pi
        gps_dictionary['lng'] = lng * 180 / np.pi
        gps_dictionary['alt'] = alt

        return gps_dictionary

    def get_gps_dictionary(self):
        """
        :return: A dictionary contains three gps coordinate.
        """
        return self.gps_dictionary

    def get_gps_range(self):
        """
        This function return a tuple contains three tuples like(tuple1, tuple2, tuple3)
        tuple1 is a tuple contains range of latitude(min, max)
        tuple2 is a tuple contains range of longitude(min, max)
        tuple3 is a tuple contains range of altitude(min, max)
        :return: A tuple contains three tuples contains range of three GPS coordinate
        """
        lat = self.gps_dictionary['lat']
        lat_range = (min(lat), max(lat))

        lng = self.gps_dictionary['lng']
        lng_range = (min(lng), max(lng))

        alt = self.gps_dictionary['alt']
        alt_range = (min(alt), max(alt))

        return (lat_range, lng_range, alt_range)
