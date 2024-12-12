import pytest

from advent_of_code.year_2024.day_12 import part1, part2


@pytest.mark.parametrize(
    argnames=("file_suffix", "expected"),
    argvalues=[pytest.param(1, 140), pytest.param(3, 1930)],
)
def test_part1(file_suffix: int, expected: int) -> None:
    assert part1(f"tests/data/2024_12_{file_suffix}") == expected


@pytest.mark.parametrize(
    argnames=("file_suffix", "expected"),
    argvalues=[pytest.param(1, 80), pytest.param(3, 1206), pytest.param(5, 368)],
)
def test_part2(file_suffix: int, expected: int) -> None:
    assert part2(f"tests/data/2024_12_{file_suffix}") == expected
