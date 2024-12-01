from aoc.utils import calculate_total_distance, read_input_file


def test_read_input_file() -> None:
    input_filepath = "tests/data/2024_01"
    expected = [["3", "4"], ["4", "3"], ["2", "5"], ["1", "3"], ["3", "9"], ["3", "3"]]
    actual = read_input_file(input_filepath)
    assert actual == expected


def test_calculate_total_distance() -> None:
    input_list1 = [3, 4, 2, 1, 3, 3]
    input_list2 = [4, 3, 5, 3, 9, 3]
    expected = 11
    actual = calculate_total_distance(input_list1, input_list2)
    assert actual == expected
