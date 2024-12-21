from collections import defaultdict
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

    def get_shortest_path(self) -> list[tuple[int, int]]:
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

    def get_skippable_walls(self) -> list[tuple[int, int]]:
        return [
            (x, y)
            for x, y in self.walls
            if sum(
                True
                for adj_x, adj_y in get_adjacent((x, y))
                if (adj_x, adj_y) not in self.walls
                and self.width > adj_x >= 0
                and self.height > adj_y >= 0
            )
            > 1
        ]

    def __str__(self) -> str:
        grid = [[" "] * self.width for _ in range(self.height)]
        for x, y in self.walls:
            grid[y][x] = "#"
        grid[self.start[1]][self.start[0]] = "S"
        grid[self.end[1]][self.end[0]] = "E"
        return "\n".join("".join(row) for row in grid)


def get_delta_path_len_counts(maze: Map) -> defaultdict[int, int]:
    shortest_path_len = len(maze.get_shortest_path())
    delta_path_len_counts: defaultdict[int, int] = defaultdict(int)
    for xy in maze.get_skippable_walls():
        maze.walls.remove(xy)
        # print(maze)
        delta_path_len = shortest_path_len - len(maze.get_shortest_path())
        if delta_path_len > 0:
            delta_path_len_counts[delta_path_len] += 1
        maze.walls.add(xy)
    return delta_path_len_counts


def part1(filepath: str) -> int:
    min_delta_path_len = 100
    data = read_input(filepath)
    maze = Map.from_str(data)
    delta_path_len_counts = get_delta_path_len_counts(maze)
    # print(delta_path_len_counts)
    return sum(
        True
        for delta_path_len in delta_path_len_counts
        if delta_path_len >= min_delta_path_len
    )


if __name__ == "__main__":
    start = perf_counter()
    result1 = part1(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 1: {result1:>20} {seconds:>20.1f}s")
