import unittest
import numpy as np
import sys
sys.path.append('.')
sys.path.append('..')
import tools.data_manager as DM

class BasicTest(unittest.TestCase):
    def setUp(self):
        self.Datamanager = DM.DataManager('2013-01-10')
        self.Datamanager.setup_data_files('sensor_data')
        self.Datamanager.load_gps()

    def test_length(self):
        self.assertEqual(len(self.Datamanager.data_dict['gps']['lat']), 7186)
        self.assertEqual(len(self.Datamanager.data_dict['gps']['lng']), 7186)
        self.assertEqual(len(self.Datamanager.data_dict['gps']['alt']), 7186)

    def test_specific_value(self):
        self.assertEqual(self.Datamanager.data_dict['gps']['lat'][6552], 0.738168689900502 * 180 / np.pi)
        self.assertEqual(self.Datamanager.data_dict['gps']['lng'][6552], -1.4610748478234 * 180 / np.pi)
        self.assertEqual(self.Datamanager.data_dict['gps']['alt'][6552], 284.2)

if __name__ == '__main__':
    unittest.main()

