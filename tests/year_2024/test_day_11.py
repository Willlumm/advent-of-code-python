from collections.abc import Callable
from typing import Any

from advent_of_code.year_2024.day_11 import Stones, part1, part2

TEST_DATA_FILEPATH = "tests/data/2024_11"


def test_part1() -> None:
    assert part1(TEST_DATA_FILEPATH) == 55312


def test_part2() -> None:
    assert part2(TEST_DATA_FILEPATH) == 65601038650482


def test_performance_25(benchmark: Callable[..., Any]) -> None:
    benchmark(Stones([125, 17]).simulate, 25)


def test_performance_75(benchmark: Callable[..., Any]) -> None:
    benchmark(Stones([125, 17]).simulate, 75)
