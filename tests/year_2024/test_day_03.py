from aoc.year_2024.day_03 import _prepare_data, part1


def test__prepare_data() -> None:
    expected = (
        r"xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    )
    assert _prepare_data("tests/data/2024_03") == expected


def test_part1() -> None:
    expected = 161
    assert part1("tests/data/2024_03") == expected
