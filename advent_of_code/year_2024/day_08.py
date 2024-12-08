from collections import defaultdict
from collections.abc import Iterable
from itertools import chain, combinations
from pathlib import Path
from time import perf_counter
from typing import Self

INPUT_FILEPATH = "data/2024_08"


def _read_input(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


class XY:
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            raise NotImplementedError
        return self.__hash__() == other.__hash__()

    def __add__(self, other: Self) -> Self:
        cls = type(self)
        if not isinstance(other, cls):
            raise NotImplementedError
        return cls(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        cls = type(self)
        if not isinstance(other, cls):
            raise NotImplementedError
        return cls(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int) -> Self:
        if not isinstance(other, int):
            raise NotImplementedError
        cls = type(self)
        return cls(other * self.x, other * self.y)

    def is_within(self, x_max: int, y_max: int, x_min: int, y_min: int) -> bool:
        return x_max > self.x >= x_min and y_max > self.y >= y_min


class XYSet(set[XY]):
    @classmethod
    def _get_antinodes(cls, xy1: XY, xy2: XY) -> Self:
        dxy = xy1 - xy2
        return cls((xy1 + dxy, xy2 - dxy))

    @classmethod
    def combine(cls, sets: Iterable[Self]) -> Self:
        return cls(chain(*sets))

    def get_antinodes(self) -> Self:
        cls = type(self)
        return cls.combine(
            cls._get_antinodes(a1, a2) for a1, a2 in combinations(self, 2)
        )

    def filter_within(
        self, x_max: int, y_max: int, x_min: int = 0, y_min: int = 0
    ) -> Self:
        cls = type(self)
        return cls(xy for xy in self if xy.is_within(x_max, y_max, x_min, y_min))


class Map:
    def __init__(self, width: int, height: int, antennas: dict[str, XYSet]) -> None:
        self.width = width
        self.height = height
        self.antennas = antennas

    @classmethod
    def from_str(cls, data: str) -> Self:
        rows = data.split("\n")[::-1]
        height = len(rows)
        width = len(rows[0])
        antennas: dict[str, XYSet] = defaultdict(XYSet)
        for y, row in enumerate(rows):
            for x, value in enumerate(row):
                if value != ".":
                    antennas[value].add(XY(x, y))
        return cls(width, height, antennas)

    @property
    def antinodes(self) -> XYSet:
        return XYSet.combine(
            antennas.get_antinodes() for antennas in self.antennas.values()
        ).filter_within(self.width, self.height)


def part1(filepath: str) -> int:
    data = _read_input(filepath)
    map_ = Map.from_str(data)
    return len(map_.antinodes)


if __name__ == "__main__":
    # 0.0s
    start = perf_counter()
    part1_result = part1(INPUT_FILEPATH)
    part1_time = perf_counter() - start
    print(f"Part 1: {part1_result:>20,} {part1_time:>20.1f}s")
