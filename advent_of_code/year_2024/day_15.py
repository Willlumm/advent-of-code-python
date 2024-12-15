from enum import Enum, StrEnum
from pathlib import Path
from time import perf_counter
from typing import Self

INPUT_FILEPATH = "data/2024_15"


class Entity(StrEnum):
    BOX = "O"
    BOX_LEFT = "["
    BOX_RIGHT = "]"
    NOTHING = "."
    ROBOT = "@"
    WALL = "#"

    @property
    def is_box(self) -> bool:
        return self in {Entity.BOX, Entity.BOX_LEFT, Entity.BOX_RIGHT}

    def get_other_half(self, xy: tuple[int, int]) -> tuple[int, int]:
        x, y = xy
        return {Entity.BOX_LEFT: (x + 1, y), Entity.BOX_RIGHT: (x - 1, y)}[self]


class Direction(tuple[int, int], Enum):
    __slots__ = ()
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @classmethod
    def from_char(cls, char: str) -> Self:
        return cls({"^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)}[char])


class InvalidMoveError(Exception):
    pass


def read_input(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


class Map:
    def __init__(
        self,
        width: int,
        height: int,
        robot: tuple[int, int],
        entities: dict[tuple[int, int], Entity],
        instructions: list[Direction],
    ) -> None:
        self.height = height
        self.width = width
        self.robot = robot
        self.entities = entities
        self.instructions = instructions

    @classmethod
    def from_str(cls, data: str) -> Self:
        entity_data, instruction_data = data.split("\n\n")
        entities = {}
        for y, row in enumerate(entity_data.split("\n")):
            for x, value in enumerate(row):
                entity = Entity(value)
                if entity == Entity.NOTHING:
                    continue
                if entity == Entity.ROBOT:
                    robot = (x, y)
                entities[(x, y)] = Entity(value)
        instructions = [
            Direction.from_char(char) for char in instruction_data if char != "\n"
        ]
        return cls(x + 1, y + 1, robot, entities, instructions)

    @classmethod
    def from_str_wide(cls, data: str) -> Self:
        entity_data, instruction_data = data.split("\n\n")
        entities = {}
        for y, row in enumerate(entity_data.split("\n")):
            for x, value in enumerate(row):
                entity = Entity(value)
                if entity == Entity.NOTHING:
                    continue
                if entity == Entity.BOX:
                    entities[(2 * x, y)] = Entity.BOX_LEFT
                    entities[(2 * x + 1, y)] = Entity.BOX_RIGHT
                elif entity == Entity.ROBOT:
                    robot = (2 * x, y)
                    entities[(2 * x, y)] = Entity.ROBOT
                elif entity == Entity.WALL:
                    entities[(2 * x, y)] = Entity.WALL
                    entities[(2 * x + 1, y)] = Entity.WALL
        instructions = [
            Direction.from_char(char) for char in instruction_data if char != "\n"
        ]
        return cls(2 * x + 2, y + 1, robot, entities, instructions)

    def check_move(self, xy: tuple[int, int], direction: Direction) -> bool:
        new_xy = xy[0] + direction[0], xy[1] + direction[1]
        entity = self.entities.get(new_xy, Entity.NOTHING)
        if entity == Entity.WALL:
            return False
        if entity in {Entity.BOX_LEFT, Entity.BOX_RIGHT} and direction in {
            Direction.UP,
            Direction.DOWN,
        }:
            return all(
                [
                    self.check_move(new_xy, direction),
                    self.check_move(entity.get_other_half(new_xy), direction),
                ]
            )
        if entity.is_box:
            return self.check_move(new_xy, direction)
        return True

    def make_move(self, xy: tuple[int, int], direction: Direction) -> None:
        new_xy = xy[0] + direction[0], xy[1] + direction[1]
        entity = self.entities.get(new_xy, Entity.NOTHING)
        if entity == Entity.WALL:
            raise InvalidMoveError
        if entity in {Entity.BOX_LEFT, Entity.BOX_RIGHT} and direction in {
            Direction.UP,
            Direction.DOWN,
        }:
            self.make_move(new_xy, direction)
            self.make_move(entity.get_other_half(new_xy), direction)
        elif entity.is_box:
            self.make_move(new_xy, direction)
        if xy == self.robot:
            self.robot = new_xy
        self.entities[new_xy] = self.entities[xy]
        del self.entities[xy]

    def process_instructions(self) -> Self:
        for instruction in self.instructions:
            if self.check_move(self.robot, instruction):
                self.make_move(self.robot, instruction)
        return self

    def sum_box_gps(self) -> int:
        return sum(
            xy[0] + 100 * xy[1]
            for xy, entity in self.entities.items()
            if entity in {Entity.BOX, Entity.BOX_LEFT}
        )

    def __str__(self) -> str:
        grid = [["."] * self.width for _ in range(self.height)]
        for (x, y), entity in self.entities.items():
            grid[y][x] = entity
        return "\n".join("".join(row) for row in grid)


def part1(filepath: str) -> int:
    data = read_input(filepath)
    return Map.from_str(data).process_instructions().sum_box_gps()


def part2(filepath: str) -> int:
    data = read_input(filepath)
    return Map.from_str_wide(data).process_instructions().sum_box_gps()


if __name__ == "__main__":
    start = perf_counter()
    result = part1(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 1: {result:>20} {seconds:>20.1f}s")

    start = perf_counter()
    result = part2(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 2: {result:>20} {seconds:>20.1f}s")
