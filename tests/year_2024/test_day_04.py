import pytest

from advent_of_code.year_2024.day_04 import (
    _generate_ray_patterns,
    _generate_x_patterns,
    _read_input,
    _search_grid,
    part1,
    part2,
)

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


def test__generate_ray_patterns() -> None:
    expected = [
        ((0, 0), (-1, -1), (-2, -2), (-3, -3)),
        ((0, 0), (-1, 0), (-2, 0), (-3, 0)),
        ((0, 0), (-1, 1), (-2, 2), (-3, 3)),
        ((0, 0), (0, -1), (0, -2), (0, -3)),
        ((0, 0), (0, 1), (0, 2), (0, 3)),
        ((0, 0), (1, -1), (2, -2), (3, -3)),
        ((0, 0), (1, 0), (2, 0), (3, 0)),
        ((0, 0), (1, 1), (2, 2), (3, 3)),
    ]
    assert _generate_ray_patterns() == expected


def test__generate_x_patterns() -> None:
    expected = [
        ((0, 0), (-1, -1), (-1, 1), (1, 1), (1, -1)),
        ((0, 0), (-1, 1), (1, 1), (1, -1), (-1, -1)),
        ((0, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)),
        ((0, 0), (1, -1), (-1, -1), (-1, 1), (1, 1)),
    ]
    assert _generate_x_patterns() == expected


def test__search_grid(data: list[str]) -> None:
    expected = 18
    assert _search_grid(data, "XMAS", _generate_ray_patterns()) == expected


def test_part1() -> None:
    expected = 18
    assert part1(TEST_DATA_FILEPATH) == expected


def test_part2() -> None:
    expected = 9
    assert part2(TEST_DATA_FILEPATH) == expected
