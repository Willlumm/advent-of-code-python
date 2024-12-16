from enum import Enum
from pathlib import Path
from time import perf_counter
from typing import Self

INPUT_FILEPATH = "data/2024_16"


def read_input(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


class Direction(tuple[int, int], Enum):
    __slots__ = ()
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def get_orthogonal_directions(self) -> list[Self]:
        cls = type(self)
        x, y = self
        return [cls((-y, x)), cls((y, -x))]

    @property
    def char(self) -> str:
        cls = type(self)
        return {cls.UP: "^", cls.DOWN: "v", cls.LEFT: "<", cls.RIGHT: ">"}[self]


type Move = tuple[Direction, int]


class Maze:
    def __init__(
        self,
        height: int,
        width: int,
        end: tuple[int, int],
        walls: set[tuple[int, int]],
    ) -> None:
        self.width = width
        self.height = height
        self.end = end
        self.walls = walls


class MazeState:
    def __init__(
        self,
        score: int,
        xy: tuple[int, int],
        direction: Direction,
        visited: set[tuple[int, int]],
        maze: Maze,
    ) -> None:
        self.score = score
        self.xy = xy
        self.direction = direction
        self.visited = visited | {xy}
        self.maze = maze

    def new_state(self, score: int, xy: tuple[int, int], direction: Direction) -> Self:
        cls = type(self)
        return cls(self.score + score, xy, direction, self.visited, self.maze)

    def get_next_states(self) -> list[Self]:
        states = []
        for direction in [self.direction, *self.direction.get_orthogonal_directions()]:
            dx, dy = direction
            xy = self.xy[0] + dx, self.xy[1] + dy
            if xy not in self.maze.walls and xy not in self.visited:
                score = 1 if (dx, dy) == self.direction else 1001
                states.append(self.new_state(score, xy, direction))
        return states

    @property
    def is_finished(self) -> bool:
        return self.xy == self.maze.end

    def __str__(self) -> str:
        grid = [[" "] * self.maze.width for _ in range(self.maze.height)]
        for x, y in self.maze.walls:
            grid[y][x] = "#"
        for x, y in self.visited:
            grid[y][x] = "."
        grid[self.maze.end[1]][self.maze.end[0]] = "E"
        grid[self.xy[1]][self.xy[0]] = self.direction.char
        return "\n".join("".join(row) for row in grid)


class MazeStateManager:
    def __init__(self, states: list[MazeState]) -> None:
        self.states = states

    @classmethod
    def from_str(cls, data: str) -> Self:
        walls = set()
        for y, line in enumerate(data.split("\n")):
            for x, value in enumerate(line):
                if value == "#":
                    walls.add((x, y))
                elif value == "S":
                    start = (x, y)
                elif value == "E":
                    end = (x, y)
        maze = Maze(x + 1, y + 1, end, walls)
        maze_state = MazeState(0, start, Direction.RIGHT, set(), maze)
        return cls([maze_state])

    @property
    def lowest_scoring_state(self) -> MazeState:
        lowest_scoring_state = self.states[0]
        for state in self.states[1:]:
            if state.score < lowest_scoring_state.score:
                lowest_scoring_state = state
        return lowest_scoring_state

    def get_state_that_visited(self, xy: tuple[int, int]) -> MazeState | None:
        for state in self.states:
            if xy in state.visited:
                return state
        return None

    def resolve_overlap(self, state: MazeState) -> bool:
        overlapping_state = self.get_state_that_visited(state.xy)
        if overlapping_state is None:
            return True
        if overlapping_state.score < state.score:
            return False
        if overlapping_state.score > state.score:
            self.states.remove(overlapping_state)
        return True

    def find_lowest_score(self) -> int:
        while self.states:
            lowest_scoring_state = self.lowest_scoring_state
            self.states.remove(lowest_scoring_state)
            for state in lowest_scoring_state.get_next_states():
                if not self.resolve_overlap(state):
                    continue
                if state.is_finished:
                    return state.score
                self.states.append(state)
        raise IndexError


def part1(filepath: str) -> int:
    data = read_input(filepath)
    return MazeStateManager.from_str(data).find_lowest_score()


if __name__ == "__main__":
    start = perf_counter()
    result = part1(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 1: {result:>20} {seconds:>20.1f}s")
