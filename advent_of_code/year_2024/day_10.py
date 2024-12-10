from pathlib import Path
from time import perf_counter
from typing import Self

INPUT_FILEPATH = "data/2024_10"


def read_input(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


class Map(dict[tuple[int, int], int]):
    MAX_HEIGHT = 9
    MIN_HEIGHT = 0

    @classmethod
    def from_str(cls, data: str) -> Self:
        return cls(
            ((x, y), int(height))
            for y, row in enumerate(data.split("\n"))
            for x, height in enumerate(row)
        )

    def get_trailtails(self, coords: tuple[int, int]) -> list[tuple[int, int]]:
        trailtails = []
        x, y = coords
        for new_coords in (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1):
            if new_coords not in self or self[new_coords] != self[coords] + 1:
                continue
            if self[new_coords] == self.MAX_HEIGHT:
                trailtails.append(new_coords)
            else:
                trailtails += self.get_trailtails(new_coords)
        return trailtails

    def sum_trailheads(self) -> int:
        return sum(
            len(set(self.get_trailtails(coords)))
            for coords, height in self.items()
            if height == self.MIN_HEIGHT
        )

    def rate_trailheads(self) -> int:
        return sum(
            len(self.get_trailtails(coords))
            for coords, height in self.items()
            if height == self.MIN_HEIGHT
        )


def part1(filepath: str) -> int:
    data = read_input(filepath)
    return Map.from_str(data).sum_trailheads()


def part2(filepath: str) -> int:
    data = read_input(filepath)
    return Map.from_str(data).rate_trailheads()


if __name__ == "__main__":
    start = perf_counter()
    result = part1(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 1: {result:>20} {seconds:>20.1f}s")

    start = perf_counter()
    result = part2(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 2: {result:>20} {seconds:>20.1f}s")
