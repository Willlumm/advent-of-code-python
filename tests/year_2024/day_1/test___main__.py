from aoc.year_2024.day_01.__main__ import main


def test_main() -> None:
    expected = 11
    assert main("tests/data/2024_01") == expected
