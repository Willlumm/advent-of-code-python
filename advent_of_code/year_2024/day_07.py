from collections.abc import Callable
from itertools import product
from pathlib import Path
from time import perf_counter
from typing import Self

INPUT_FILEPATH = "data/2024_07"


def _read_input(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


class Operators:
    @staticmethod
    def add(x: int, y: int) -> int:
        return x + y

    @staticmethod
    def multiply(x: int, y: int) -> int:
        return x * y

    @staticmethod
    def concatenate(x: int, y: int) -> int:
        return int(str(x) + str(y))


class Equation:
    def __init__(self, total: int, numbers: list[int]) -> None:
        self.total = total
        self.numbers = numbers

    @property
    def required_operators(self) -> int:
        return len(self.numbers) - 1

    def is_solvable(self, operators: tuple[Callable[[int, int], int], ...]) -> bool:
        return any(
            self._check_operator_combination(combination)
            for combination in product(operators, repeat=self.required_operators)
        )

    @classmethod
    def from_str(cls, data: str) -> Self:
        total_str, numbers_str = data.split(": ")
        return cls(int(total_str), [int(n) for n in numbers_str.split()])

    def _check_operator_combination(
        self, operators: tuple[Callable[[int, int], int], ...]
    ) -> bool:
        total = self.numbers[0]
        for number, operator in zip(self.numbers[1:], operators, strict=True):
            total = operator(total, number)
        return total == self.total


class EquationList(list[Equation]):
    def total_calibration_result(self, *operators: Callable[[int, int], int]) -> int:
        return sum(
            equation.total for equation in self if equation.is_solvable(operators)
        )

    @classmethod
    def from_str(cls, data: str) -> Self:
        return cls(Equation.from_str(row) for row in data.split("\n"))


def part1(filepath: str) -> int:
    return EquationList.from_str(_read_input(filepath)).total_calibration_result(
        Operators.add, Operators.multiply
    )


def part2(filepath: str) -> int:
    return EquationList.from_str(_read_input(filepath)).total_calibration_result(
        Operators.add, Operators.multiply, Operators.concatenate
    )


if __name__ == "__main__":
    start = perf_counter()
    part1_result = part1(INPUT_FILEPATH)
    part1_time = perf_counter() - start
    print(f"Part 1: {part1_result:>20} {part1_time:>20.1f}s")

    start = perf_counter()
    part2_result = part2(INPUT_FILEPATH)
    part2_time = perf_counter() - start
    print(f"Part 2: {part2_result:>20} {part2_time:>20.1f}s")
