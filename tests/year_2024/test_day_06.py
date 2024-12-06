from textwrap import dedent

import pytest

from advent_of_code.year_2024.day_06 import Coords, Map, part1

TEST_DATA_FILEPATH = "tests/data/2024_06"


@pytest.fixture
def data() -> str:
    return dedent("""
        ....#.....
        .........#
        ..........
        ..#.......
        .......#..
        ..........
        .#..^.....
        ........#.
        #.........
        ......#...
    """).strip()


@pytest.fixture
def map_() -> Map:
    return Map(
        10,
        10,
        Coords(4, 3),
        {
            Coords(2, 6),
            Coords(4, 9),
            Coords(6, 0),
            Coords(8, 2),
            Coords(7, 5),
            Coords(1, 3),
            Coords(0, 1),
            Coords(9, 8),
        },
    )


class TestMap:
    def test_from_str(self, data: str, map_: Map) -> None:
        actual = Map.from_str(data)
        assert actual.width == map_.width
        assert actual.height == map_.height
        assert actual.position == map_.position
        assert actual.obstacles == map_.obstacles
        assert actual.visited == map_.visited


def test_part1() -> None:
    assert part1(TEST_DATA_FILEPATH) == 41
