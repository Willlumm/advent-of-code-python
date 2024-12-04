import pytest

from advent_of_code.year_2024.day_04 import _read_input, _search_grid, part1

TEST_DATA_FILEPATH = "tests/data/2024_04"


@pytest.fixture
def data() -> list[str]:
    return [
        "MMMSXXMASM",
        "MSAMXMSMSA",
        "AMXSXMAAMM",
        "MSAMASMSMX",
        "XMASAMXAMM",
        "XXAMMXXAMA",
        "SMSMSASXSS",
        "SAXAMASAAA",
        "MAMMMXMMMM",
        "MXMXAXMASX",
    ]


def test__read_input(data: list[str]) -> None:
    assert _read_input(TEST_DATA_FILEPATH) == data


def test__search_grid(data: list[str]) -> None:
    expected = 18
    assert _search_grid(data) == expected


def test_part1() -> None:
    expected = 18
    assert part1(TEST_DATA_FILEPATH) == expected
