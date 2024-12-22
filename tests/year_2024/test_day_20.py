import pytest

from advent_of_code.year_2024.day_20 import Map, count_cheats, read_input


class TestCountCheats:
    @pytest.mark.parametrize(
        ("steps_saved", "expected"),
        [
            (2, 44),
            (4, 30),
            (6, 16),
            (8, 14),
            (10, 10),
            (12, 8),
            (20, 5),
            (36, 4),
            (38, 3),
            (40, 2),
            (64, 1),
            (65, 0),
        ],
    )
    def test_cheat_duration_2(self, steps_saved: int, expected: int) -> None:
        data = read_input("tests/data/2024_20")
        path = Map.from_str(data).get_path()
        assert count_cheats(path, 2, steps_saved) == expected

    @pytest.mark.parametrize(
        ("steps_saved", "expected"),
        [
            (50, 285),
            (52, 253),
            (54, 222),
            (56, 193),
            (58, 154),
            (60, 129),
            (62, 106),
            (64, 86),
            (66, 67),
            (68, 55),
            (70, 41),
            (72, 29),
            (74, 7),
            (76, 3),
            (77, 0),
        ],
    )
    def test_cheat_duration_20(self, steps_saved: int, expected: int) -> None:
        data = read_input("tests/data/2024_20")
        path = Map.from_str(data).get_path()
        assert count_cheats(path, 20, steps_saved) == expected
