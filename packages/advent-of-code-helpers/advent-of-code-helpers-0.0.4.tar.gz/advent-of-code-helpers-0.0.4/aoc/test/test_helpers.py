import os
import unittest

from aoc.helpers import read_input_from_file, output


class TestHelpers(unittest.TestCase):
    def test_read_file(self):
        expected_data = '-1\n-19\n-7'
        file_path = os.path.join(os.path.dirname(__file__),
                                 'resources/input.txt')
        data = read_input_from_file(file_path)
        self.assertEqual(expected_data, data,
                         'Data should match expected data.')

    def test(self):
        output('test', 1, 3, 2018, '.')
