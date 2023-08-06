import unittest


class BasicTest(unittest.TestCase):

    def setUp(self):
        self.list = []
        self.list.append('a')
        self.list.append('b')
        self.list.append('c')

    def test_setup_is_correct(self):
        self.assertEqual(['a', 'b', 'c'], self.list)
        self.assertGreater(len(self.list), 0)
        self.assertEqual(len(self.list), 3)

    def test_add_item(self):
        self.list.append('d')
        self.assertEqual(['a', 'b', 'c', 'd'], self.list)

    def test_remove_item(self):
        self.list.remove('b')
        self.assertEqual(['a', 'c'], self.list)


if __name__ == '__main__':
    unittest.main()