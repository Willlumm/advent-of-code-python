from collections import defaultdict
from pathlib import Path
from typing import Self

INPUT_FILEPATH = "data/2024_05"

type PagesDict = defaultdict[int, set[int]]


class Update(list[int]):
    @property
    def middle(self) -> int:
        return self[len(self) // 2]

    @classmethod
    def from_str(cls, data: str) -> Self:
        return cls(int(n) for n in data.split(","))

    def is_valid(self, pages: PagesDict) -> bool:
        illegal_pages = set()
        for page_number in self:
            if page_number in illegal_pages:
                return False
            illegal_pages |= pages[page_number]
        return True


def _read_input(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


def _split_input(data: str) -> list[str]:
    return data.split("\n\n")


def _parse_page_data(data: str) -> PagesDict:
    pages = defaultdict(set)
    for row in data.split("\n"):
        required_page_number, page_number = (int(n) for n in row.split("|"))
        pages[page_number].add(required_page_number)
    return pages


def _parse_update_data(data: str) -> list[Update]:
    return [Update.from_str(row) for row in data.split("\n")]


def _sum_valid_middles(updates: list[Update], pages: PagesDict) -> int:
    return sum(update.middle for update in updates if update.is_valid(pages))


def part1(filepath: str) -> int:
    data = _read_input(filepath)
    page_order_data, update_data = _split_input(data)
    pages = _parse_page_data(page_order_data)
    updates = _parse_update_data(update_data)
    return _sum_valid_middles(updates, pages)


if __name__ == "__main__":
    print(f"Part 1: {part1(INPUT_FILEPATH):>20}")
