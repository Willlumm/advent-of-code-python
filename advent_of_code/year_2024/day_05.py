from collections import defaultdict
from pathlib import Path
from typing import Any, Self

INPUT_FILEPATH = "data/2024_05"


class PagesDict(defaultdict[int, set[int]]):
    def __init__(self, *args: dict[Any, Any]) -> None:
        super().__init__(set, *args)

    @classmethod
    def from_str(cls, data: str) -> Self:
        pages = cls()
        for row in data.split("\n"):
            required_page_number, page_number = (int(n) for n in row.split("|"))
            pages[page_number].add(required_page_number)
        return pages


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


class UpdateList(list[Update]):
    @property
    def sum_middles(self) -> int:
        return sum(update.middle for update in self)

    @classmethod
    def from_str(cls, data: str) -> Self:
        return cls(Update.from_str(row) for row in data.split("\n"))

    def filter(self, pages: PagesDict, *, valid: bool = True) -> Self:
        return type(self)(update for update in self if update.is_valid(pages) is valid)


def _read_input(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


def _split_input(data: str) -> list[str]:
    return data.split("\n\n")


def part1(filepath: str) -> int:
    data = _read_input(filepath)
    page_order_data, update_data = _split_input(data)
    pages = PagesDict.from_str(page_order_data)
    updates = UpdateList.from_str(update_data)
    valid_updates = updates.filter(pages, valid=True)
    return valid_updates.sum_middles


if __name__ == "__main__":
    print(f"Part 1: {part1(INPUT_FILEPATH):>20}")
