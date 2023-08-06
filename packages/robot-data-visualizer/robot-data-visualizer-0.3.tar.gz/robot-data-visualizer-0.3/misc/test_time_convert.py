import sys
import unittest
from time_convert import epoch_to_date_time

class BasicTest(unittest.TestCase):
    """setup for unittests."""
    def setUp(self):
        time0 = 1347517370
        time1 = 1347517370111111
        time2 = 12
        self.convert_time0 = epoch_to_date_time(time0)
        self.convert_time1 = epoch_to_date_time(time1)
        self.convert_time2 = epoch_to_date_time(time2)
    def test_specific_value(self):
        """Checks for correct output of 10 digit epoch  (no slicing by function needed)."""
        self.assertEqual(self.convert_time0, 'Wed Sep 12 23:22:50 2012')

    def test_specific_value_plus_subseconds(self):
        """Checks for correct output of 10+ digit epoch  (slicing by function needed)."""
        self.assertEqual(self.convert_time1, 'Wed Sep 12 23:22:50 2012')
    def test_short_time(self):
        """Checks for correct output of <10 digit epoch  (no slicing by function needed)."""
        self.assertEqual(self.convert_time2, 'Wed Dec 31 16:00:12 1969')


if __name__ == '__main__':
    unittest.main()