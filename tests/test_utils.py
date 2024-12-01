from aoc.utils import calculate_similarity, calculate_total_distance, read_input_file


def test_read_input_file() -> None:
    expected = [["3", "4"], ["4", "3"], ["2", "5"], ["1", "3"], ["3", "9"], ["3", "3"]]
    assert read_input_file("tests/data/2024_01") == expected


def test_calculate_total_distance() -> None:
    input_list1 = [3, 4, 2, 1, 3, 3]
    input_list2 = [4, 3, 5, 3, 9, 3]
    expected = 11
    assert calculate_total_distance(input_list1, input_list2) == expected


def test_calculate_similarity() -> None:
    expected = 31
    assert calculate_similarity([3, 4, 2, 1, 3, 3], [4, 3, 5, 3, 9, 3]) == expected
