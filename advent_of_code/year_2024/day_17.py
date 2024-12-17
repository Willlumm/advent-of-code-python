import re
from pathlib import Path
from time import perf_counter
from typing import Self

INPUT_FILEPATH = "data/2024_17"


def read_input(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


class Computer:
    def __init__(self) -> None:
        self.a = 0
        self.b = 0
        self.c = 0
        self.program: list[int] = []
        self.i = 0
        self.output: list[int] = []

    def parse_input(self, data: str) -> Self:
        self.a, self.b, self.c = [
            int(match.group(1))
            for match in (
                re.search(f"Register {register}: ([0-9]+)", data)
                for register in ("A", "B", "C")
            )
            if match is not None
        ]
        program_match = re.search(r"Program: ([0-9,]+)", data)
        if program_match is None:
            raise ValueError
        self.program = [int(n) for n in program_match.group(1).split(",")]
        return self

    def combo(self, operand: int) -> int:
        return (0, 1, 2, 3, self.a, self.b, self.c)[operand]

    def adv(self, operand: int) -> None:
        self.a = self.a // 2 ** self.combo(operand)

    def bxl(self, operand: int) -> None:
        self.b = self.b ^ operand

    def bst(self, operand: int) -> None:
        self.b = self.combo(operand) % 8

    def jnz(self, operand: int) -> None:
        if self.a:
            self.i = operand - 2

    def bxc(self, _: int) -> None:
        self.b = self.b ^ self.c

    def out(self, operand: int) -> None:
        self.output.append(self.combo(operand) % 8)

    def bdv(self, operand: int) -> None:
        self.b = self.a // 2 ** self.combo(operand)

    def cdv(self, operand: int) -> None:
        self.c = self.a // 2 ** self.combo(operand)

    def execute_instruction(self, opcode: int, operand: int) -> None:
        (
            self.adv,
            self.bxl,
            self.bst,
            self.jnz,
            self.bxc,
            self.out,
            self.bdv,
            self.cdv,
        )[opcode](operand)

    def run_program(self) -> str:
        print(self)
        while self.i < len(self.program):
            opcode, operand = self.program[self.i : self.i + 2]
            self.execute_instruction(opcode, operand)
            # print(self)
            # input()
            self.i += 2
        return ",".join(str(n) for n in self.output)

    def __str__(self) -> str:
        return (
            f"\nA: {self.a:>10,}"
            f"\nB: {self.b:>10,}"
            f"\nC: {self.c:>10,}"
            f"\n{self.program[self.i: self.i + 2]}"
            f"\n{self.i}"
            f"\n{self.output}"
        )

def part1(filepath: str) -> str:
    data = read_input(filepath)
    return Computer().parse_input(data).run_program()


# def part2(filepath: str) -> int:
#     data = read_input(filepath)
#     manager = MazeStateManager.from_str(data)
#     manager.find_lowest_score()
#     return manager.count_best_tiles_to_sit()


if __name__ == "__main__":
    start = perf_counter()
    result = part1(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 1: {result:>20} {seconds:>20.1f}s")
    # start = perf_counter()
    # result = part2(INPUT_FILEPATH)
    # seconds = perf_counter() - start
    # print(f"Part 2: {result:>20} {seconds:>20.1f}s")
