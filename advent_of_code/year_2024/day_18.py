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
        self.bytes: list[tuple[int, int]] = []
        self.corrupted_bytes: set[tuple[int, int]] = set()
        self.path: set[tuple[int, int]] = set()

    def parse_input(self, data: str) -> Self:
        self.bytes = [
            (int(x), int(y)) for x, y in (line.split(",") for line in data.split("\n"))
        ]
        self.corrupted_bytes = set(self.bytes[: self.byte_count])
        return self

    def get_shortest_path(self) -> int | None:
        paths = [[(0, 0)]]
        visited = {(0, 0)}
        while paths:
            new_paths = []
            for path in paths:
                x, y = path[-1]
                for x_new, y_new in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if (
                        not self.width > x_new >= 0
                        or not self.height > y_new >= 0
                        or (x_new, y_new) in visited | self.corrupted_bytes
                    ):
                        continue
                    if (x_new, y_new) == self.exit:
                        self.path = {*path, (x_new, y_new)}
                        return len(self.path) - 1
                    new_paths.append([*path, (x_new, y_new)])
                    visited.add((x_new, y_new))
            paths = new_paths
        return None

    def get_blocking_byte(self) -> tuple[int, int] | None:
        self.get_shortest_path()
        for xy in self.bytes[self.byte_count :]:
            self.corrupted_bytes.add(xy)
            if xy in self.path:
                shortest_path_len = self.get_shortest_path()
                if shortest_path_len is None:
                    return xy
        return None


def part1(filepath: str, width: int, height: int, byte_count: int) -> int:
    data = read_input(filepath)
    shortest_path = (
        MemorySpace(width, height, byte_count).parse_input(data).get_shortest_path()
    )
    if shortest_path is None:
        raise ValueError
    return shortest_path


def part2(filepath: str, width: int, height: int, byte_count: int) -> str:
    data = read_input(filepath)
    blocking_byte = (
        MemorySpace(width, height, byte_count).parse_input(data).get_blocking_byte()
    )
    if blocking_byte is None:
        raise ValueError
    return ",".join(str(n) for n in blocking_byte)


if __name__ == "__main__":
    start = perf_counter()
    result1 = part1(INPUT_FILEPATH, 71, 71, 1024)
    seconds = perf_counter() - start
    print(f"Part 1: {result1:>20} {seconds:>20.1f}s")

    start = perf_counter()
    result2 = part2(INPUT_FILEPATH, 71, 71, 1024)
    seconds = perf_counter() - start
    print(f"Part 2: {result2:>20} {seconds:>20.1f}s")
