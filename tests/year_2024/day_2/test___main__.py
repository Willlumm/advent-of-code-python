import pytest

from aoc.year_2024.day_02.__main__ import _is_safe, _prepare_data, part1, part2


def test__prepare_data() -> None:
    expected = [
        [7, 6, 4, 2, 1],
        [1, 2, 7, 8, 9],
        [9, 7, 6, 2, 1],
        [1, 3, 2, 4, 5],
        [8, 6, 4, 4, 1],
        [1, 3, 6, 7, 9],
    ]
    assert _prepare_data("tests/data/2024_02") == expected


class TestIsSafe:
    @pytest.mark.parametrize(
        argnames=("row", "expected"),
        argvalues=(
            pytest.param([7, 6, 4, 2, 1], False),
            pytest.param([1, 2, 7, 8, 9], False),
            pytest.param([9, 7, 6, 2, 1], False),
            pytest.param([1, 3, 2, 4, 5], False),
            pytest.param([8, 6, 4, 4, 1], False),
            pytest.param([1, 3, 6, 7, 9], True),
            pytest.param([2, 1, 2, 3, 4], False),
            pytest.param([3, 4, 3, 2, 1], False),
        ),
    )
    def test_increasing_0_tolerance(self, row: list[int], expected: bool) -> None:
        assert _is_safe(row, increasing=True, tolerance=0) is expected

    @pytest.mark.parametrize(
        argnames=("row", "expected"),
        argvalues=(
            pytest.param([7, 6, 4, 2, 1], True),
            pytest.param([1, 2, 7, 8, 9], False),
            pytest.param([9, 7, 6, 2, 1], False),
            pytest.param([1, 3, 2, 4, 5], False),
            pytest.param([8, 6, 4, 4, 1], False),
            pytest.param([1, 3, 6, 7, 9], False),
            pytest.param([2, 1, 2, 3, 4], False),
            pytest.param([3, 4, 3, 2, 1], False),
        ),
    )
    def test_decreasing_0_tolerance(self, row: list[int], expected: bool) -> None:
        assert _is_safe(row, increasing=False, tolerance=0) is expected

    @pytest.mark.parametrize(
        argnames=("row", "expected"),
        argvalues=(
            pytest.param([7, 6, 4, 2, 1], False),
            pytest.param([1, 2, 7, 8, 9], False),
            pytest.param([9, 7, 6, 2, 1], False),
            pytest.param([1, 3, 2, 4, 5], True),
            pytest.param([8, 6, 4, 4, 1], False),
            pytest.param([1, 3, 6, 7, 9], True),
            pytest.param([2, 1, 2, 3, 4], True),
            pytest.param([3, 4, 3, 2, 1], False),
        ),
    )
    def test_increasing_1_tolerance(self, row: list[int], expected: bool) -> None:
        assert _is_safe(row, increasing=True, tolerance=1) is expected

    @pytest.mark.parametrize(
        argnames=("row", "expected"),
        argvalues=(
            pytest.param([7, 6, 4, 2, 1], True),
            pytest.param([1, 2, 7, 8, 9], False),
            pytest.param([9, 7, 6, 2, 1], False),
            pytest.param([1, 3, 2, 4, 5], False),
            pytest.param([8, 6, 4, 4, 1], True),
            pytest.param([1, 3, 6, 7, 9], False),
            pytest.param([2, 1, 2, 3, 4], False),
            pytest.param([3, 4, 3, 2, 1], True),
        ),
    )
    def test_decreasing_1_tolerance(self, row: list[int], expected: bool) -> None:
        assert _is_safe(row, increasing=False, tolerance=1) is expected


def test_part1() -> None:
    expected = 2
    assert part1("tests/data/2024_02") == expected


def test_part2() -> None:
    expected = 4
    assert part2("tests/data/2024_02") == expected
