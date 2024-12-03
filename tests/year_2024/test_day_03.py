from aoc.year_2024.day_03 import _filter_data, _prepare_data, _sum_muls, part1, part2


def test__prepare_data() -> None:
    expected = (
        r"xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    )
    assert _prepare_data("tests/data/2024_03_1") == expected


def test__filter_data() -> None:
    data = r"xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    assert _filter_data(data) == r"xmul(2,4)&mul[3,7]!^?mul(8,5))"


def test__sum_muls() -> None:
    data = r"xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    expected = 161
    assert _sum_muls(data) == expected


def test_part1() -> None:
    expected = 161
    assert part1("tests/data/2024_03_1") == expected


def test_part2() -> None:
    expected = 48
    assert part2("tests/data/2024_03_2") == expected
