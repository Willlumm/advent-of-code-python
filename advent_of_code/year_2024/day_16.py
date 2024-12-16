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
        width: int,
        height: int,
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
    def footprint(self) -> tuple[tuple[int, int], tuple[int, int]]:
        return (self.xy, self.direction)

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
        self.finished_states: list[MazeState] = []
        self.footprints = {states[0].footprint: states[0].score}

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

    def find_lowest_score(self) -> int:
        while self.states:
            lowest_scoring_state = self.lowest_scoring_state
            if (
                self.finished_states
                and lowest_scoring_state.score > self.finished_states[0].score
            ):
                break
            self.states.remove(lowest_scoring_state)
            for state in lowest_scoring_state.get_next_states():
                score = self.footprints.get(state.footprint, None)
                if score is not None and score < state.score:
                    continue
                if state.is_finished:
                    self.finished_states.append(state)
                else:
                    self.footprints[state.footprint] = state.score
                    self.states.append(state)
        return self.finished_states[0].score

    def count_best_tiles_to_sit(self) -> int:
        return len({xy for state in self.finished_states for xy in state.visited})


def part1(filepath: str) -> int:
    data = read_input(filepath)
    return MazeStateManager.from_str(data).find_lowest_score()


def part2(filepath: str) -> int:
    data = read_input(filepath)
    manager = MazeStateManager.from_str(data)
    manager.find_lowest_score()
    return manager.count_best_tiles_to_sit()


if __name__ == "__main__":
    start = perf_counter()
    result = part1(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 1: {result:>20} {seconds:>20.1f}s")
    start = perf_counter()
    result = part2(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 2: {result:>20} {seconds:>20.1f}s")
