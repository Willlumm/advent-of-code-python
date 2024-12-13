import re
from pathlib import Path
from time import perf_counter
from typing import Self

INPUT_FILEPATH = "data/2024_13"


def read_input(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


class ClawMachine:
    A_COST = 3
    B_COST = 1

    def __init__(
        self,
        a_dxy: tuple[int, int],
        b_dxy: tuple[int, int],
        prize_xy: tuple[int, int],
        max_presses: int | None = None,
        prize_offset: int = 0,
    ) -> None:
        self.a_dxy = a_dxy
        self.b_dxy = b_dxy
        self.prize_xy = prize_xy[0] + prize_offset, prize_xy[1] + prize_offset
        self.max_presses = max_presses

    @classmethod
    def from_str(
        cls, data: str, max_presses: int | None = None, prize_offset: int = 0
    ) -> Self:
        a_dxy, b_dxy, prize_xy = (
            (int(match.group(1)), int(match.group(2)))
            for match in re.finditer(r"X.([0-9]+), Y.([0-9]+)", data)
        )
        return cls(
            a_dxy, b_dxy, prize_xy, max_presses=max_presses, prize_offset=prize_offset
        )

    @classmethod
    def list_from_input(
        cls,
        data: str,
        max_presses: int | None = None,
        prize_offset: int = 0,
    ) -> list[Self]:
        return [
            cls.from_str(
                claw_machine_data, max_presses=max_presses, prize_offset=prize_offset
            )
            for claw_machine_data in data.split("\n\n")
        ]

    def calculate_presses(
        self, a_dxy: tuple[int, int], b_dxy: tuple[int, int], prize_xy: tuple[int, int]
    ) -> int | None:
        a_dx, a_dy = a_dxy
        b_dx, b_dy = b_dxy
        prize_x, prize_y = prize_xy
        numerator = prize_y * b_dx - prize_x * b_dy
        denominator = a_dy * b_dx - a_dx * b_dy
        if numerator % denominator != 0:
            return None
        presses = numerator // denominator
        is_within_limit = (
            self.max_presses >= presses >= 0 if self.max_presses else presses >= 0
        )
        if not is_within_limit:
            return None
        return presses

    @property
    def a_presses(self) -> int | None:
        return self.calculate_presses(self.a_dxy, self.b_dxy, self.prize_xy)

    @property
    def b_presses(self) -> int | None:
        return self.calculate_presses(self.b_dxy, self.a_dxy, self.prize_xy)

    @property
    def min_cost(self) -> int:
        if self.a_presses is None or self.b_presses is None:
            return 0
        return self.a_presses * self.A_COST + self.b_presses * self.B_COST


def part1(filepath: str) -> int:
    data = read_input(filepath)
    return sum(
        claw_machine.min_cost
        for claw_machine in ClawMachine.list_from_input(data, max_presses=100)
    )


def part2(filepath: str) -> int:
    data = read_input(filepath)
    return sum(
        claw_machine.min_cost
        for claw_machine in ClawMachine.list_from_input(
            data, prize_offset=10_000_000_000_000
        )
    )


if __name__ == "__main__":
    start = perf_counter()
    result = part1(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 1: {result:>20} {seconds:>20.1f}s")

    start = perf_counter()
    result = part2(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 2: {result:>20} {seconds:>20.1f}s")
