from advent_of_code.year_2024.day_14 import part1

TEST_DATA_FILEPATH = "tests/data/2024_14"


def test_part1() -> None:
    assert part1(TEST_DATA_FILEPATH, width=11, height=7) == 12
