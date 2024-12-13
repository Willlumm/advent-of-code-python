from random import randint

from advent_of_code.year_2024.day_13 import ClawMachine, part1, part2

TEST_DATA_FILEPATH = "tests/data/2024_13"


def test_part1() -> None:
    assert part1(TEST_DATA_FILEPATH) == 480


def test_part2() -> None:
    assert part2(TEST_DATA_FILEPATH) == 875_318_608_908


def test_procedually() -> None:
    while True:
        a_dxy = (randint(1, 100), randint(1, 100))
        b_dxy = (randint(1, 100), randint(1, 100))
        if a_dxy == b_dxy:
            continue
        prize_xy = (randint(5000, 20_000), randint(5000, 20_000))
        claw_machine = ClawMachine(
            a_dxy, b_dxy, prize_xy, prize_offset=10_000_000_000_000
        )
        a_presses = claw_machine.a_presses
        b_presses = claw_machine.b_presses
        if a_presses is not None and b_presses is not None:
            try:
                assert (
                    a_presses * a_dxy[0] + b_presses * b_dxy[0]
                    == claw_machine.prize_xy[0]
                )
                assert (
                    a_presses * a_dxy[1] + b_presses * b_dxy[1]
                    == claw_machine.prize_xy[1]
                )
            except AssertionError:
                print(a_dxy, b_dxy, prize_xy, a_presses, b_presses)
                raise
