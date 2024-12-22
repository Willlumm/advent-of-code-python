from pathlib import Path
from time import perf_counter
from typing import Self

INPUT_FILEPATH = "data/2024_20"


def read_input(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


def get_adjacent(xy: tuple[int, int]) -> list[tuple[int, int]]:
    x, y = xy
    return [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]


class Map:
    def __init__(
        self,
        width: int,
        height: int,
        start: tuple[int, int],
        end: tuple[int, int],
        walls: set[tuple[int, int]],
    ) -> None:
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.walls = walls

    @classmethod
    def from_str(cls, string: str) -> Self:
        walls = set()
        for y, line in enumerate(string.split("\n")):
            for x, char in enumerate(line):
                if char == "#":
                    walls.add((x, y))
                elif char == "S":
                    start = (x, y)
                elif char == "E":
                    end = (x, y)
        return cls(x + 1, y + 1, start, end, walls)

    def get_path(self) -> list[tuple[int, int]]:
        xys = [self.start]
        visited: dict[tuple[int, int], tuple[int, int] | None] = {self.start: None}
        while xys:
            new_xys = []
            for xy in xys:
                for new_xy in get_adjacent(xy):
                    if new_xy in visited or new_xy in self.walls:
                        continue
                    new_xys.append(new_xy)
                    visited[new_xy] = xy
                    if new_xy == self.end:
                        break
            xys = new_xys
        xy_: tuple[int, int] | None = self.end
        path = []
        while xy_ is not None:
            path.append(xy_)
            xy_ = visited[xy_]
        return path


def count_cheats(
    path: list[tuple[int, int]], cheat_duration: int, min_steps_saved: int
) -> int:
    total = 0
    for i, (x1, y1) in enumerate(path):
        for steps_cut, (x2, y2) in enumerate(path[i + min_steps_saved :]):
            cheat_steps = abs(x2 - x1) + abs(y2 - y1)
            if cheat_steps <= cheat_duration and steps_cut >= cheat_steps:
                total += 1
    return total


def part1(filepath: str) -> int:
    data = read_input(filepath)
    path = Map.from_str(data).get_path()
    return count_cheats(path, 2, 100)


def part2(filepath: str) -> int:
    data = read_input(filepath)
    path = Map.from_str(data).get_path()
    return count_cheats(path, 20, 100)


if __name__ == "__main__":
    start = perf_counter()
    result = part1(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 1: {result:>20} {seconds:>20.1f}s")
    start = perf_counter()
    result = part2(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 2: {result:>20} {seconds:>20.1f}s")
