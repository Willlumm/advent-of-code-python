from pathlib import Path

INPUT_FILEPATH = "data/2024_02"


def _prepare_data(filepath: str) -> list[list[int]]:
    with Path(filepath).open() as file:
        return [[int(x) for x in line.split()] for line in file]


def _is_safe(row: list[int]) -> bool:
    max_dx, min_dx = (3, 1) if row[1] > row[0] else (-1, -3)
    x0 = row[0]
    for x1 in row[1:]:
        if not max_dx >= x1 - x0 >= min_dx:
            return False
        x0 = x1
    return True


def part1(filepath: str) -> int:
    return sum(_is_safe(row) for row in _prepare_data(filepath))


if __name__ == "__main__":
    print(f"Part 1: {part1(INPUT_FILEPATH):>20}")
