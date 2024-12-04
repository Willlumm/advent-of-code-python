from pathlib import Path

INPUT_FILEPATH = "data/2024_04"

type Coord = tuple[int, int]
type Pattern = tuple[Coord, ...]


def _read_input(filepath: str) -> list[str]:
    with Path(filepath).open() as file:
        return file.read().split("\n")


def _generate_ray_patterns() -> list[Pattern]:
    """
    S  S  S
     A A A
      MMM
    SAMXMAS
      MMM
     A A A
    S  S  S
    """
    dxys = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    return [tuple((i * dx, i * dy) for i in range(4)) for dx, dy in dxys]


def _generate_x_patterns() -> list[Pattern]:
    """
    M M     S M     S S     M S
     A       A       A       A
    S S     S M     M M     M S
    """
    dxys = ((-1, -1), (-1, 1), (1, 1), (1, -1))
    return [((0, 0), *(dxys[(i + j) % 4] for i in range(4))) for j in range(4)]


def _search_grid(data: list[str], chars: str, patterns: list[Pattern]) -> int:
    total = 0
    x_max = len(data)
    for x, row in enumerate(data):
        y_max = len(row)
        for y, _ in enumerate(row):
            for pattern in patterns:
                for char, (dx, dy) in zip(chars, pattern, strict=False):
                    if not (x_max > x + dx >= 0 and y_max > y + dy >= 0):
                        break
                    if data[x + dx][y + dy] != char:
                        break
                else:
                    total += 1
    return total


def part1(filepath: str) -> int:
    return _search_grid(_read_input(filepath), "XMAS", _generate_ray_patterns())


def part2(filepath: str) -> int:
    return _search_grid(_read_input(filepath), "AMMSS", _generate_x_patterns())


if __name__ == "__main__":
    print(f"Part 1: {part1(INPUT_FILEPATH):>20}")
    print(f"Part 2: {part2(INPUT_FILEPATH):>20}")
