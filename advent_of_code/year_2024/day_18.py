from pathlib import Path
from time import perf_counter
from typing import Self

INPUT_FILEPATH = "data/2024_18"


def read_input(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


class MemorySpace:
    def __init__(self, width: int, height: int, byte_count: int) -> None:
        self.width = width
        self.height = height
        self.byte_count = byte_count
        self.xy = 0, 0
        self.exit = width - 1, height - 1
        self.corrupted: set[tuple[int, int]] = set()

    def parse_input(self, data: str) -> Self:
        self.corrupted = set(
            [
                (int(x), int(y))
                for x, y in (line.split(",") for line in data.split("\n"))
            ][: self.byte_count]
        )
        return self

    def get_shortest_path(self) -> int | None:
        xys = [(0, 0)]
        visited = {(0, 0)}
        steps = 0
        while xys:
            new_xys = []
            steps += 1
            for x, y in xys:
                for x_new, y_new in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if (
                        not self.width > x_new >= 0
                        or not self.height > y_new >= 0
                        or (x_new, y_new) in visited | self.corrupted
                    ):
                        continue
                    if (x_new, y_new) == self.exit:
                        return steps
                    new_xys.append((x_new, y_new))
                    visited.add((x_new, y_new))
            xys = new_xys
        return None


def part1(filepath: str, width: int, height: int, byte_count: int) -> int:
    data = read_input(filepath)
    shortest_path = (
        MemorySpace(width, height, byte_count).parse_input(data).get_shortest_path()
    )
    if shortest_path is None:
        raise ValueError
    return shortest_path


if __name__ == "__main__":
    start = perf_counter()
    result = part1(INPUT_FILEPATH, 71, 71, 1024)
    seconds = perf_counter() - start
    print(f"Part 1: {result:>20} {seconds:>20.1f}s")
