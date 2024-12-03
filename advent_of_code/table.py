from typing import Any


class Table(list[list[Any]]):
    def cast_column(self, i: int, type_: type) -> None:
        for row in self:
            row[i] = type_(row[i])

    def get_column(self, i: int) -> list[Any]:
        return [row[i] for row in self]
