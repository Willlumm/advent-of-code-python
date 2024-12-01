from aoc.utils import calculate_total_distance, read_input_file

INPUT_FILEPATH = "aoc/year_2024/day_01/input"


def main(filepath: str) -> int:
    table = read_input_file(filepath)
    table.cast_column(0, int)
    table.cast_column(1, int)
    column0 = table.get_column(0)
    column1 = table.get_column(1)
    return calculate_total_distance(column0, column1)


if __name__ == "__main__":
    print(main(INPUT_FILEPATH))
