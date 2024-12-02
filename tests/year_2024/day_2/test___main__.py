import pytest

from aoc.year_2024.day_02.__main__ import _is_safe, _prepare_data, part1


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


@pytest.mark.parametrize(
    argnames=("row"),
    argvalues=(pytest.param([7, 6, 4, 2, 1]), pytest.param([1, 3, 6, 7, 9])),
)
def test__is_safe_pass(row: list[int]) -> None:
    assert _is_safe(row) is True


@pytest.mark.parametrize(
    argnames=("row"),
    argvalues=(
        pytest.param([1, 2, 7, 8, 9]),
        pytest.param([9, 7, 6, 2, 1]),
        pytest.param([1, 3, 2, 4, 5]),
        pytest.param([8, 6, 4, 4, 1]),
    ),
)
def test__is_safe_fail(row: list[int]) -> None:
    assert _is_safe(row) is False


def test_part1() -> None:
    expected = 2
    assert part1("tests/data/2024_02") == expected
