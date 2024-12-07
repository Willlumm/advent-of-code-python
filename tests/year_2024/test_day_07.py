from advent_of_code.year_2024.day_07 import part1, part2

TEST_DATA_FILEPATH = "tests/data/2024_07"


def test_part1() -> None:
    assert part1(TEST_DATA_FILEPATH) == 3749


def test_part2() -> None:
    assert part2(TEST_DATA_FILEPATH) == 11387
