from pathlib import Path
from time import perf_counter
from typing import Self

INPUT_FILEPATH = "data/2024_11"


def read_input(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


class Stones:
    def __init__(self, stones: list[int]) -> None:
        self.stones = stones
        self.cache = {0: [1]}

    @classmethod
    def from_str(cls, data: str) -> Self:
        return cls([int(n) for n in data.split()])

    def get_next(self, number: int) -> list[int]:
        if number in self.cache:
            return self.cache[number]
        number_str = str(number)
        digit_count = len(number_str)
        if digit_count % 2:
            next_numbers = [number * 2024]
        else:
            half_length = digit_count // 2
            next_numbers = [
                int(number_str[:half_length]),
                int(number_str[half_length:]),
            ]
        self.cache[number] = next_numbers
        return next_numbers

    def simulate(self, iterations: int) -> Self:
        for _ in range(iterations):
            self.stones = [
                next_numbers
                for number in self.stones
                for next_numbers in self.get_next(number)
            ]
        return self

    @property
    def stone_count(self) -> int:
        return len(self.stones)


def part1(filepath: str) -> int:
    data = read_input(filepath)
    return Stones.from_str(data).simulate(25).stone_count


def part2(filepath: str) -> int:
    data = read_input(filepath)
    return Stones.from_str(data).simulate(75).stone_count


if __name__ == "__main__":
    start = perf_counter()
    result = part1(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 1: {result:>20} {seconds:>20.1f}s")

    start = perf_counter()
    result = part2(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 1: {result:>20} {seconds:>20.1f}s")
