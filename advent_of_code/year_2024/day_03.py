import re
from itertools import pairwise
from pathlib import Path

INPUT_FILEPATH = "data/2024_03"


def _prepare_data(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


def _filter_data(data: str) -> str:
    return "".join(
        data_section
        for instruction, data_section in pairwise(
            re.split(r"(do(?:n't)?\(\))", "do()" + data)
        )
        if instruction == "do()"
    )


def _sum_muls(data: str) -> int:
    return sum(
        int(match[1]) * int(match[2])
        for match in re.finditer(r"mul\(([0-9]+),([0-9]+)\)", data)
    )


def part1(filepath: str) -> int:
    return _sum_muls(_prepare_data(filepath))


def part2(filepath: str) -> int:
    return _sum_muls(_filter_data(_prepare_data(filepath)))


if __name__ == "__main__":
    print(f"Part 1: {part1(INPUT_FILEPATH):>20}")
    print(f"Part 2: {part2(INPUT_FILEPATH):>20}")
