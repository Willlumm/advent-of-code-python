from enum import Enum
from pathlib import Path
from time import perf_counter
from typing import Self

INPUT_FILEPATH = "data/2024_06"


def _read_input(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


class XY(tuple[int, int]):
    __slots__ = ()

    def __new__(cls, x: int, y: int) -> Self:
        return super().__new__(cls, (x, y))

    @property
    def x(self) -> int:
        return self[0]

    @property
    def y(self) -> int:
        return self[1]


class Direction(XY, Enum):
    UP = (0, 1)
    RIGHT = (1, 0)
    DOWN = (0, -1)
    LEFT = (-1, 0)

    def rotate_clockwise(self) -> Self:
        return type(self)(self.y, -self.x)


class Coords(XY):
    def move(self, direction: Direction) -> Self:
        return type(self)(self.x + direction.x, self.y + direction.y)


class State(tuple[Coords, Direction]):
    __slots__ = ()


class Map:
    def __init__(
        self, width: int, height: int, start: Coords, obstacles: set[Coords]
    ) -> None:
        self.width = width
        self.height = height
        self.start = start
        self.position = start
        self.direction = Direction.UP
        self.obstacles = obstacles
        self.previous_states: list[State] = []

    @property
    def is_in_area(self) -> bool:
        return self.width > self.position.x >= 0 and self.height > self.position.y >= 0

    @property
    def is_stuck(self) -> bool:
        return (self.position, self.direction) in self.previous_states

    @property
    def visited(self) -> set[Coords]:
        return {coords for coords, _ in self.previous_states}

    @property
    def total_visited(self) -> int:
        return len(self.visited)

    @classmethod
    def from_str(cls, data: str) -> Self:
        rows = data.split("\n")[::-1]
        height = len(rows)
        width = len(rows[0])
        obstacles = set()
        for y, row in enumerate(rows):
            for x, value in enumerate(row):
                if value == "#":
                    obstacles.add(Coords(x, y))
                elif value == "^":
                    start = Coords(x, y)
        return cls(height, width, start, obstacles)

    def simulate(self) -> None:
        while self.is_in_area and not self.is_stuck:
            self.previous_states.append(State((self.position, self.direction)))
            next_position = self.position.move(self.direction)
            if next_position in self.obstacles:
                self.direction = self.direction.rotate_clockwise()
            else:
                self.position = next_position

    def reset(
        self, start: Coords | None = None, direction: Direction = Direction.UP
    ) -> None:
        self.position = start if start else self.start
        self.direction = direction
        self.previous_states.clear()


def part1(filepath: str) -> int:
    data = _read_input(filepath)
    map_ = Map.from_str(data)
    map_.simulate()
    return map_.total_visited


def part2(filepath: str) -> int:
    data = _read_input(filepath)
    map_ = Map.from_str(data)
    map_.simulate()
    states = map_.previous_states.copy()
    map_.reset()
    total = 0
    tried_coords: set[Coords] = set()
    for coords, direction in states:
        if coords in tried_coords:
            continue
        map_.obstacles.add(coords)
        tried_coords.add(coords)
        map_.simulate()
        total += map_.is_stuck
        map_.obstacles.remove(coords)
        map_.reset(start=coords, direction=direction)

    return total


if __name__ == "__main__":
    # 0.1s
    start = perf_counter()
    part1_result = part1(INPUT_FILEPATH)
    part1_time = perf_counter() - start
    print(f"Part 1: {part1_result:>20,} {part1_time:>20.1f}s")

    # 50.5s
    start = perf_counter()
    part2_result = part2(INPUT_FILEPATH)
    part2_time = perf_counter() - start
    print(f"Part 1: {part1_result:>20,} {part1_time:>20.1f}s")
    print(f"Part 2: {part2_result:>20,} {part2_time:>20.1f}s")
