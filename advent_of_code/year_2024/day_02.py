from itertools import combinations
from pathlib import Path

INPUT_FILEPATH = "data/2024_02"


def _prepare_data(filepath: str) -> list[list[int]]:
    with Path(filepath).open() as file:
        return [[int(x) for x in line.split()] for line in file]


def _is_safe(row: list[int], *, increasing: bool = True, tolerance: int = 0) -> bool:
    max_dx, min_dx = (3, 1) if increasing else (-1, -3)
    for row_subset in combinations(row, len(row) - tolerance):
        x0 = row_subset[0]
        for x1 in row_subset[1:]:
            if not max_dx >= x1 - x0 >= min_dx:
                break
            x0 = x1
        else:
            return True
    return False


def part1(filepath: str) -> int:
    return sum(
        _is_safe(row, increasing=True) or _is_safe(row, increasing=False)
        for row in _prepare_data(filepath)
    )


def part2(filepath: str) -> int:
    return sum(
        _is_safe(row, increasing=True, tolerance=1)
        or _is_safe(row, increasing=False, tolerance=1)
        for row in _prepare_data(filepath)
    )


if __name__ == "__main__":
    print(f"Part 1: {part1(INPUT_FILEPATH):>20}")
    print(f"Part 2: {part2(INPUT_FILEPATH):>20}")
