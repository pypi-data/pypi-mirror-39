from abc import ABC, abstractmethod

from aoc.helpers import output, read_input_from_file


class Puzzle(ABC):
    def __init__(self, part: int, day: int, year: int,
                 input_file: str = None,
                 output_dir: str = None) -> None:
        self.part = part
        self.day = day
        self.year = year
        self.input_file = input_file
        self.output_dir = output_dir
        super().__init__()

    def input(self):
        if self.input_file:
            return read_input_from_file(self.input_file)
        else:
            raise Exception('No input file provided.')

    @abstractmethod
    def solve(self):
        pass

    def output(self):
        result = self.solve()
        output(result, self.part, self.day, self.year, self.output_dir)
        return result


class Part1(Puzzle):
    def __init__(self, day: int, year: int,
                 input_file: str = None,
                 output_dir: str = None) -> None:
        super().__init__(1, day, year, input_file, output_dir)

    @abstractmethod
    def solve(self):
        pass


class Part2(Puzzle):
    def __init__(self, day: int, year: int,
                 input_file: str = None,
                 output_dir: str = None) -> None:
        super().__init__(2, day, year, input_file, output_dir)

    @abstractmethod
    def solve(self):
        pass
