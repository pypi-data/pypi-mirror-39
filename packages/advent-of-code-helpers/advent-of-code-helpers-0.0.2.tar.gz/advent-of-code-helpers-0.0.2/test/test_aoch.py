import os
import unittest

from aoch import read_file


class TestHelpers(unittest.TestCase):
    def test_read_file(self):
        expected_data = '-1\n-19\n-7'
        file_path = os.path.join(os.path.dirname(__file__), 'resources/input.txt')
        data = read_file(file_path)
        self.assertEqual(expected_data, data, 'Data should match expected data.')
