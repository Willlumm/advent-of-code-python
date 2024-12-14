import re
from pathlib import Path
from time import perf_counter
from typing import Self

INPUT_FILEPATH = "data/2024_14"


def read_input(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


class Map:
    def __init__(self, robots: list[tuple[int, int, int, int]], **kwargs: int) -> None:
        self.robots = robots
        self.width = kwargs.get("width", 101)
        self.height = kwargs.get("height", 103)

    @classmethod
    def from_str(cls, data: str, **kwargs: int) -> Self:
        return cls(
            [
                (
                    int(match.group(1)),
                    int(match.group(2)),
                    int(match.group(3)),
                    int(match.group(4)),
                )
                for match in re.finditer(
                    r"p=(-?[0-9]+),(-?[0-9]+) v=(-?[0-9]+),(-?[0-9]+)", data
                )
            ],
            **kwargs,
        )

    def simulate(self, i: int) -> Self:
        cls = type(self)
        return cls(
            [
                ((x + i * dx) % self.width, (y + i * dy) % self.height, dx, dy)
                for x, y, dx, dy in self.robots
            ],
            width=self.width,
            height=self.height,
        )

    @property
    def safety_factor(self) -> int:
        quadrants = [0] * 4
        for x, y, _, _ in self.robots:
            if x < self.width // 2 and y < self.height // 2:
                quadrants[0] += 1
            elif x > self.width // 2 and y < self.height // 2:
                quadrants[1] += 1
            elif x < self.width // 2 and y > self.height // 2:
                quadrants[2] += 1
            elif x > self.width // 2 and y > self.height // 2:
                quadrants[3] += 1
        return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]

    def __str__(self) -> str:
        grid = [[0] * self.width for _ in range(self.height)]
        for x, y, _, _ in self.robots:
            grid[y][x] += 1
        return "\n".join("".join("#" if n else " " for n in row) for row in grid)


def part1(filepath: str, **kwargs: int) -> int:
    data = read_input(filepath)
    return Map.from_str(data, **kwargs).simulate(100).safety_factor


def part2(filepath: str, **kwargs: int) -> int:
    data = read_input(filepath)
    robot_map = Map.from_str(data, **kwargs)
    safety_factor = robot_map.safety_factor
    safety_factor_threshold = 120_000_000
    i = 0
    while safety_factor > safety_factor_threshold:
        robot_map = robot_map.simulate(1)
        i += 1
        safety_factor = robot_map.safety_factor
    print(robot_map)
    print(f"{safety_factor:,}")
    return i


if __name__ == "__main__":
    start = perf_counter()
    result = part1(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 1: {result:>20} {seconds:>20.1f}s")

    start = perf_counter()
    result = part2(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 2: {result:>20} {seconds:>20.1f}s")
