from typing import Any

import pytest

from advent_of_code.table import Table


def test_cast_column() -> None:
    table = Table([["1"], ["2"], ["3"]])
    expected = Table([[1], [2], [3]])
    table.cast_column(0, int)
    assert table == expected


@pytest.mark.parametrize(
    argnames=("column_index", "expected"),
    argvalues=(
        pytest.param(0, ["foo", "bar", "baz"], id="column 0"),
        pytest.param(1, [1, 2, 3], id="column 1"),
    ),
)
def test_get_column(column_index: int, expected: list[Any]) -> None:
    table = Table([["foo", 1], ["bar", 2], ["baz", 3]])
    assert table.get_column(column_index) == expected
