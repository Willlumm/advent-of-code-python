from enum import Enum
from pathlib import Path
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


class Map:
    def __init__(
        self, width: int, height: int, start: Coords, obstacles: set[Coords]
    ) -> None:
        self.width = width
        self.height = height
        self.position = start
        self.direction = Direction.UP
        self.obstacles = obstacles
        self.visited: set[Coords] = set()

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
        while self.width > self.position.x >= 0 and self.height > self.position.y >= 0:
            self.visited.add(self.position)
            next_position = self.position.move(self.direction)
            if next_position in self.obstacles:
                self.direction = self.direction.rotate_clockwise()
            else:
                self.position = next_position


def part1(filepath: str) -> int:
    data = _read_input(filepath)
    map_ = Map.from_str(data)
    map_.simulate()
    return map_.total_visited


if __name__ == "__main__":
    print(f"Part 1: {part1(INPUT_FILEPATH):>20}")
