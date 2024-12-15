from advent_of_code.year_2024.day_15 import part1, part2

TEST_DATA_FILEPATH = "tests/data/2024_15"


def test_part1() -> None:
    assert part1(TEST_DATA_FILEPATH) == 10_092


def test_part2() -> None:
    assert part2(TEST_DATA_FILEPATH) == 9_021
