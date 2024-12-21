from advent_of_code.year_2024.day_20 import (
    Map,
    get_delta_path_len_counts,
    read_input,
)


def test_get_delta_path_len_counts() -> None:
    expected = {
        2: 14,
        4: 14,
        6: 2,
        8: 4,
        10: 2,
        12: 3,
        20: 1,
        36: 1,
        38: 1,
        40: 1,
        64: 1,
    }
    data = read_input("tests/data/2024_20")
    maze = Map.from_str(data)
    delta_path_len_counts = get_delta_path_len_counts(maze)
    assert delta_path_len_counts == expected
