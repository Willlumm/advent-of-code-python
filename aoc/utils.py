from pathlib import Path

from aoc.table import Table


def read_input_file(filepath: str) -> Table:
    with Path(filepath).open() as file:
        return Table(line.split() for line in file)


def calculate_total_distance(list1: list[int], list2: list[int]) -> int:
    return sum(
        abs(item1 - item2)
        for item1, item2 in zip(sorted(list1), sorted(list2), strict=False)
    )
