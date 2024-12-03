from advent_of_code.year_2024.day_01 import _prepare_lists, part1, part2


def test__prepare_lists() -> None:
    expected = ([3, 4, 2, 1, 3, 3], [4, 3, 5, 3, 9, 3])
    assert _prepare_lists("tests/data/2024_01") == expected


def test_part1() -> None:
    expected = 11
    assert part1("tests/data/2024_01") == expected


def test_part2() -> None:
    expected = 31
    assert part2("tests/data/2024_01") == expected
