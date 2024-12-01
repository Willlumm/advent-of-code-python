from typing import Any

import pytest

from aoc.table import Table


def test_cast_column() -> None:
    input_table = Table([["1"], ["2"], ["3"]])
    expected = Table([[1], [2], [3]])
    input_table.cast_column(0, int)
    assert input_table == expected


@pytest.mark.parametrize(
    argnames=("input_column_index", "expected"),
    argvalues=(
        pytest.param(0, ["foo", "bar", "baz"], id="column 0"),
        pytest.param(1, [1, 2, 3], id="column 1"),
    ),
)
def test_get_column(input_column_index: int, expected: list[Any]) -> None:
    input_table = Table([["foo", 1], ["bar", 2], ["baz", 3]])
    actual = input_table.get_column(input_column_index)
    assert actual == expected
