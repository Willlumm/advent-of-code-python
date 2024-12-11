from functools import cache
from pathlib import Path
from time import perf_counter
from typing import Self

INPUT_FILEPATH = "data/2024_11"


def read_input(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


# @cache
def get_next(number: int) -> list[int]:
    if number == 0:
        return [1]
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
    return next_numbers


# @cache

sim_cache = {}
def _simulate(number: int, i_max: int, i: int = 0) -> int:
    input_args = (number, i_max, i)
    if input_args in sim_cache:
        return sim_cache[input_args]
    next_numbers = get_next(number)
    if i + 1 >= i_max:
        result = len(next_numbers)
    else:
        result = sum(_simulate(next_number, i_max, i + 1) for next_number in next_numbers)
    sim_cache[input_args] = result
    return result


class Stones:
    def __init__(self, numbers: list[int]) -> None:
        self.numbers = numbers

    @classmethod
    def from_str(cls, data: str) -> Self:
        return cls([int(n) for n in data.split()])

    def simulate(self, i_max: int) -> int:
        return sum(_simulate(number, i_max) for number in self.numbers)


def part1(filepath: str) -> int:
    data = read_input(filepath)
    return Stones.from_str(data).simulate(25)


def part2(filepath: str) -> int:
    data = read_input(filepath)
    return Stones.from_str(data).simulate(75)


if __name__ == "__main__":
    start = perf_counter()
    result = part1(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 1: {result:>20} {seconds:>20.1f}s")

    start = perf_counter()
    result = part2(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 1: {result:>20} {seconds:>20.1f}s")
