import pytest

from advent_of_code.year_2024.day_17 import part1, part2


@pytest.mark.parametrize(
    argnames=("file_suffix", "expected"),
    argvalues=[
        pytest.param(1, "4,6,3,5,6,3,5,2,1,0"),
        pytest.param(2, "0,1,2"),
        pytest.param(3, "4,2,5,6,7,7,7,7,3,1,0"),
    ],
)
def test_part1(file_suffix: int, expected: str) -> None:
    assert part1(f"tests/data/2024_17_{file_suffix}") == expected


def test_part2() -> None:
    assert part2("tests/data/2024_17_4") == 117_440
