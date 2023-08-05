import unittest

from aoc.template import Puzzle


class TestTemplate(unittest.TestCase):
    def test_template(self):
        day = Part1(3, 2018)
        self.assertEqual(Part1.expected_result, day.output(),
                         'Should return expected result')


class Part1(Puzzle):
    expected_result = 'Solved Part 1!'

    def __init__(self, day: int, year: int) -> None:
        super().__init__(1, day, year)

    def solve(self):
        return Part1.expected_result
