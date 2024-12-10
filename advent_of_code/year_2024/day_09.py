from itertools import chain
from pathlib import Path
from time import perf_counter
from typing import Self

INPUT_FILEPATH = "data/2024_09"


def read_input(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


class FileSystem(list[int | None]):
    def trim(self) -> Self:
        for n in self[::-1]:
            if n is None:
                self.pop()
            else:
                return self
        return self

    @classmethod
    def from_str(cls, data: str) -> Self:
        return cls(
            chain.from_iterable(
                [None if i % 2 else i // 2] * int(size) for i, size in enumerate(data)
            )
        ).trim()

    def compact(self) -> Self:
        for i, n in enumerate(self):
            if n is None:
                self[i] = self.pop()
                self.trim()
        return self

    @property
    def checksum(self) -> int:
        return sum(0 if n is None else i * n for i, n in enumerate(self))


class DiskMap:
    def __init__(self, files: list[tuple[int, int]], free: set[int]) -> None:
        self.files = files
        self.free = free

    @classmethod
    def from_str(cls, data: str) -> Self:
        files = []
        free: set[int] = set()
        block_i = 0
        for data_i, size_ in enumerate(data):
            size = int(size_)
            if data_i % 2:
                free.update(range(block_i, block_i + size))
            else:
                files.append((block_i, size))
            block_i += size
        return cls(files, free)

    def find_space(self, required_size: int) -> int | None:
        for n in range(min(self.free), max(self.free) + 1 - required_size):
            blocks = set(range(n, n + required_size))
            if blocks <= self.free:
                self.free -= blocks
                return n
        return None

    def compact(self) -> Self:
        for file_id, (file_i, size) in list(enumerate(self.files))[::-1]:
            free_i = self.find_space(size)
            if free_i is not None and free_i < file_i:
                self.files[file_id] = (free_i, size)
        return self

    @property
    def checksum(self) -> int:
        return int(
            sum(
                (file_id * size / 2) * (2 * i + size - 1)
                for file_id, (i, size) in enumerate(self.files)
            )
        )


def part1(filepath: str) -> int:
    data = read_input(filepath)
    return FileSystem.from_str(data).compact().checksum


def part2(filepath: str) -> int:
    data = read_input(filepath)
    return DiskMap.from_str(data).compact().checksum


if __name__ == "__main__":
    # 8.7s
    start = perf_counter()
    result = part1(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 1: {result:>20} {seconds:>20.1f}s")

    # 68.8s
    start = perf_counter()
    result = part2(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 2: {result:>20} {seconds:>20.1f}s")
