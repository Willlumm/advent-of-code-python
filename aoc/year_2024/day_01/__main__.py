from aoc.utils import calculate_similarity, calculate_total_distance, read_input_file

INPUT_FILEPATH = "aoc/year_2024/day_01/input"


def _prepare_lists(filepath: str) -> tuple[list[int], list[int]]:
    table = read_input_file(filepath)
    table.cast_column(0, int)
    table.cast_column(1, int)
    return table.get_column(0), table.get_column(1)


def part1(filepath: str) -> int:
    list1, list2 = _prepare_lists(filepath)
    return calculate_total_distance(list1, list2)


def part2(filepath: str) -> int:
    list1, list2 = _prepare_lists(filepath)
    return calculate_similarity(list1, list2)


if __name__ == "__main__":
    print(f"Part 1: {part1(INPUT_FILEPATH):>20}")
    print(f"Part 2: {part2(INPUT_FILEPATH):>20}")
