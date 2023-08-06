import unittest
import sys
import os
sys.path.append('.')
sys.path.append('..')
from tools.data_manager import DataManager

class TestDataManager(unittest.TestCase):

    def setUp(self):
        self.date = '2013-01-10'
        self.dm = DataManager(self.date)
        self.root_path = os.path.abspath('.')
        self.data_dir_root = os.path.join(self.root_path, self.dm.data_dir_name)
        self.curr_data_dir = os.path.join(self.data_dir_root, self.date)

    def test_setup_sensor_data(self):
        self.dm.setup_data_files('sensor_data')
        self.assertTrue(os.path.exists(self.curr_data_dir))

    def test_setup_lidar_data(self):
        self.dm.setup_data_files('hokuyo')
        file_name = self.date + '_hokuyo.tar.gz'
        self.assertTrue(os.path.isfile(os.path.join(self.data_dir_root, file_name)))

    def test_load_gps(self):
        self.dm.setup_data_files('sensor_data')
        self.dm.load_gps()
        self.assertTrue('gps' in self.dm.data_dict.keys())
        self.assertTrue('gps_range' in self.dm.data_dict.keys())

    def test_load_lidar(self):
        self.dm.setup_data_files('hokuyo')
        self.dm.load_lidar(100)
        self.assertTrue('lidar' in self.dm.data_dict.keys())

if __name__ == '__main__':
    unittest.main()