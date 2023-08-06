import sys
import unittest
import numpy as np
from threshold_lidar import threshold_lidar_pts
sys.path.append('..')
from tools.data_manager import DataManager

class BasicTest(unittest.TestCase):
    """setup for unittests."""
    def setUp(self):
        date = '2013-04-05'
        num_samples = 3
        dm = DataManager(date)
        dm.setup_data_files('hokuyo')
        dm.load_lidar(num_samples)
        lidar = dm.data_dict['lidar']
        self.thresh0_x, self.thresh0_y, self.thresh0_time = threshold_lidar_pts(lidar[0])
        #self.thresh1 = epoch_to_date_time(lidar[1])
        #self.thresh2 = epoch_to_date_time(lidar[2])
    def test_length(self):
        """Verifies lengths of outputs."""
        self.assertEqual(len(self.thresh0_x), 37)
        self.assertEqual(len(self.thresh0_y), 37)
    def test_type(self):
        """Verifies types of outputs."""
        self.assertIsInstance(self.thresh0_time, int)
