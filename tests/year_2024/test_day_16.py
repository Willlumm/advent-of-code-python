import pytest

from advent_of_code.year_2024.day_16 import part1

TEST_DATA_FILEPATH = "tests/data/2024_16"


@pytest.mark.parametrize(
    argnames=("file_suffix", "expected"),
    argvalues=[pytest.param(1, 7036), pytest.param(2, 11048)],
)
def test_part1(file_suffix: int, expected: int) -> None:
    assert part1(f"tests/data/2024_16_{file_suffix}") == expected