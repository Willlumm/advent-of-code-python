from pathlib import Path
from typing import Self

INPUT_FILEPATH = "data/2024_05"


class PageDict(dict[int, set[int]]):
    @classmethod
    def from_str(cls, data: str) -> Self:
        pages = cls()
        for row in data.split("\n"):
            required_number, number = (int(n) for n in row.split("|"))
            if required_number not in pages:
                pages[required_number] = set()
            if number not in pages:
                pages[number] = set()
            pages[number].add(required_number)
        return pages

    def simplify(self, numbers: list[int]) -> Self:
        return type(self)(
            {
                number: required_numbers & set(numbers)
                for number, required_numbers in self.items()
                if number in numbers
            }
        )

    def get_free_page_number(self) -> int:
        for number, required_numbers in self.items():
            if not required_numbers:
                return number
        raise IndexError


class Update(list[int]):
    @property
    def middle(self) -> int:
        return self[len(self) // 2]

    @classmethod
    def from_str(cls, data: str) -> Self:
        return cls(int(n) for n in data.split(","))

    def is_ordered(self, pages: PageDict) -> bool:
        illegal_numbers = set()
        for number in self:
            if number in illegal_numbers:
                return False
            illegal_numbers |= pages[number]
        return True

    def order(self, pages: PageDict) -> Self:
        new_order = type(self)()
        remaining_numbers = list(self)
        for _ in range(len(self)):
            pages = pages.simplify(remaining_numbers)
            free_number = pages.get_free_page_number()
            new_order.append(free_number)
            remaining_numbers.remove(free_number)
        return new_order


class UpdateList(list[Update]):
    @property
    def sum_of_middles(self) -> int:
        return sum(update.middle for update in self)

    @classmethod
    def from_str(cls, data: str) -> Self:
        return cls(Update.from_str(row) for row in data.split("\n"))

    def filter(self, pages: PageDict, *, ordered: bool = True) -> Self:
        return type(self)(
            update for update in self if update.is_ordered(pages) is ordered
        )

    def order_all(self, pages: PageDict) -> Self:
        return type(self)(update.order(pages) for update in self)


def _read_input(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


def _split_input(data: str) -> list[str]:
    return data.split("\n\n")


def part1(filepath: str) -> int:
    data = _read_input(filepath)
    page_order_data, update_data = _split_input(data)
    pages = PageDict.from_str(page_order_data)
    updates = UpdateList.from_str(update_data)
    return updates.filter(pages, ordered=True).sum_of_middles


def part2(filepath: str) -> int:
    data = _read_input(filepath)
    page_order_data, update_data = _split_input(data)
    pages = PageDict.from_str(page_order_data)
    updates = UpdateList.from_str(update_data)
    return updates.filter(pages, ordered=False).order_all(pages).sum_of_middles


if __name__ == "__main__":
    print(f"Part 1: {part1(INPUT_FILEPATH):>20}")
    print(f"Part 2: {part2(INPUT_FILEPATH):>20}")
