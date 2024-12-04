from pathlib import Path

INPUT_FILEPATH = "data/2024_04"


def _read_input(filepath: str) -> list[str]:
    with Path(filepath).open() as file:
        return file.read().split("\n")


def _search_grid(data: list[str]) -> int:
    total = 0
    x_max = len(data)
    dxys = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    for x, row in enumerate(data):
        y_max = len(row)
        for y, _ in enumerate(row):
            for dx, dy in dxys:
                for i, char in enumerate("XMAS"):
                    xi = x + i * dx
                    yi = y + i * dy
                    if not (x_max > xi >= 0 and y_max > yi >= 0):
                        break
                    if data[xi][yi] != char:
                        break
                else:
                    total += 1
    return total


def part1(filepath: str) -> int:
    return _search_grid(_read_input(filepath))


if __name__ == "__main__":
    print(f"Part 1: {part1(INPUT_FILEPATH):>20}")
