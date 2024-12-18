from advent_of_code.year_2024.day_18 import part1, part2


def test_part1() -> None:
    assert part1("tests/data/2024_18", 7, 7, 12) == 22


def test_part2() -> None:
    assert part2("tests/data/2024_18", 7, 7, 12) == "6,1"
