import re
from pathlib import Path

INPUT_FILEPATH = "data/2024_03"


def _prepare_data(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


def part1(filepath: str) -> int:
    return sum(
        int(match[1]) * int(match[2])
        for match in re.finditer(r"mul\(([0-9]+),([0-9]+)\)", _prepare_data(filepath))
    )


if __name__ == "__main__":
    print(f"Part 1: {part1(INPUT_FILEPATH):>20}")
