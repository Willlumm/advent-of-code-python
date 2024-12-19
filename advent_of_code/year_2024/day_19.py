from pathlib import Path
from time import perf_counter
from functools import cache

INPUT_FILEPATH = "data/2024_19"


def read_input(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


def check_design(design: str, patterns: set[str], i_max: int, depth: int = 0) -> bool:
    if design in patterns:
        return True
    design_len = len(design)
    for i in range(min(i_max, design_len), 0, -1):
        # print(depth, design[:i])
        # input()
        if design[:i] in patterns and check_design(
            design[i:], patterns, i_max, depth + 1
        ):
            return True
    return False

def number_of_combos(design: str, patterns: set[str], i_max: int, depth = 0) -> int:
    combos = 0
    design_len = len(design)
    for i in range(min(i_max, design_len), 0, -1):
        # print(depth, design[:i], design[:i] in patterns)
        # input()
        if design[:i] in patterns:
            if design[i:]:
                combos += number_of_combos(design[i:], patterns, i_max, depth + 1)
            else:
                # print(design)
                combos += 1
                # print("WOMBO COMBO")

    return combos


def part1(filepath: str) -> int:
    data = read_input(filepath)
    pattern_data, design_data = data.split("\n\n")
    patterns = set(pattern_data.split(", "))
    # print(len(patterns))
    max_len = max(len(pattern) for pattern in patterns)
    patterns_to_keep = set()
    for pattern in patterns:
        if not check_design(pattern, patterns - {pattern}, max_len):
            patterns_to_keep.add(pattern)
    # print(len(patterns_to_keep))
    for pattern in sorted(patterns_to_keep):
        pass
        # print(pattern)
    # input()
    # singleton_patterns = "|".join(pattern for pattern in patterns if len(pattern) == 1)

    total = 0
    for design in design_data.split("\n"):
        result = check_design(design, patterns_to_keep, max_len)
        total += result
        # print(design, result)
    return total
    # return sum(check_design(design, patterns) for design in design_data.split("\n"))


def part2(filepath: str) -> int:
    data = read_input(filepath)
    pattern_data, design_data = data.split("\n\n")
    patterns = set(pattern_data.split(", "))
    # print(len(patterns))
    max_len = max(len(pattern) for pattern in patterns)
    patterns_to_keep = set()
    for pattern in patterns:
        if not check_design(pattern, patterns - {pattern}, max_len):
            patterns_to_keep.add(pattern)
    # print(len(patterns_to_keep))
    for pattern in sorted(patterns_to_keep):
        # print(pattern)
        pass
    # input()
    # singleton_patterns = "|".join(pattern for pattern in patterns if len(pattern) == 1)

    @cache
    def number_of_combos_(design: str) -> int:
        combos = 0
        design_len = len(design)
        for i in range(min(max_len, design_len), 0, -1):
            # print(depth, design[:i], design[:i] in patterns)
            # input()
            if design[:i] in patterns:
                if design[i:]:
                    combos += number_of_combos_(design[i:])
                else:
                    # print(design)
                    combos += 1
                    # print("WOMBO COMBO")

        return combos

    total = 0
    for design in design_data.split("\n"):
        if check_design(design, patterns_to_keep, max_len):
            result = number_of_combos_(design)
            total += result
            print(design, result)
    return total
    # return sum(check_design(design, patterns) for design in design_data.split("\n"))


if __name__ == "__main__":
    start = perf_counter()
    result1 = part1(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 1: {result1:>20} {seconds:>20.1f}s")
    start = perf_counter()
    result2 = part2(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 1: {result2:>20} {seconds:>20.1f}s")
