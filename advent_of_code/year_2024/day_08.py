from collections import defaultdict
from itertools import combinations
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

    def __len__(self) -> int:
        return 2

    def _check_comparable(self, other: object) -> None:
        if isinstance(other, type(self)):
            return
        if not isinstance(other, tuple):
            raise NotImplementedError
        if len(other) != len(self):
            raise NotImplementedError
        x, y = other
        if not (isinstance(x, int) and isinstance(y, int)):
            raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        self._check_comparable(other)
        return self.__hash__() == other.__hash__()

    def __gt__(self, other: tuple[int, int]) -> bool:
        self._check_comparable(other)
        return self.x > other[0] and self.y > other[1]

    def __ge__(self, other: tuple[int, int]) -> bool:
        self._check_comparable(other)
        return self.x >= other[0] and self.y >= other[1]

    def __lt__(self, other: tuple[int, int]) -> bool:
        self._check_comparable(other)
        return self.x < other[0] and self.y < other[1]

    def __le__(self, other: tuple[int, int]) -> bool:
        self._check_comparable(other)
        return self.x <= other[0] and self.y <= other[1]

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
    pass


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

    def _get_new_antinodes(self, antenna1: XY, antenna2: XY) -> XYSet:
        dxy = antenna1 - antenna2
        return XYSet(
            node
            for node in (antenna1 + dxy, antenna2 - dxy)
            if node.is_within(self.width, self.height, 0, 0)
        )

    def _get_new_antinodes_with_resonant_harmonics(
        self, antenna1: XY, antenna2: XY
    ) -> XYSet:
        antinodes = XYSet()
        dxy = antenna1 - antenna2
        while (self.height, self.width) > antenna1 >= (0, 0):
            antinodes.add(antenna1)
            antenna1 += dxy
        while (self.height, self.width) > antenna2 >= (0, 0):
            antinodes.add(antenna2)
            antenna2 -= dxy
        return antinodes

    def get_antinodes(self, *, resonant_harmonics: bool = False) -> XYSet:
        antinodes = XYSet()
        for antennas in self.antennas.values():
            for a1, a2 in combinations(antennas, 2):
                antinodes |= (
                    self._get_new_antinodes_with_resonant_harmonics(a1, a2)
                    if resonant_harmonics
                    else self._get_new_antinodes(a1, a2)
                )
        return antinodes


def part1(filepath: str) -> int:
    data = _read_input(filepath)
    map_ = Map.from_str(data)
    return len(map_.get_antinodes())


def part2(filepath: str) -> int:
    data = _read_input(filepath)
    map_ = Map.from_str(data)
    return len(map_.get_antinodes(resonant_harmonics=True))


if __name__ == "__main__":
    # 0.0s
    start = perf_counter()
    result = part1(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 1: {result:>20,} {seconds:>20.1f}s")

    # 0.0s
    start = perf_counter()
    result = part2(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 1: {result:>20,} {seconds:>20.1f}s")
