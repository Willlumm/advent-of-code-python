from functools import cache
from pathlib import Path
from time import perf_counter

INPUT_FILEPATH = "data/2024_19"


def read_input(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


def is_possible(design: str, patterns: set[str], max_pattern_len: int) -> bool:
    design_len = len(design)
    max_i = min(max_pattern_len, design_len)
    for i in range(max_i, 0, -1):
        if design[:i] not in patterns:
            continue
        if i == design_len or is_possible(design[i:], patterns, max_pattern_len):
            return True
    return False


def simplify_patterns(patterns: set[str], max_pattern_len: int) -> set[str]:
    return {
        pattern
        for pattern in patterns
        if not is_possible(pattern, patterns - {pattern}, max_pattern_len)
    }


def count_combinations(design: str, patterns: set[str], max_pattern_len: int) -> int:
    @cache
    def _count_combinations(design: str) -> int:
        design_len = len(design)
        max_i = min(max_pattern_len, len(design))
        combos = 0
        for i in range(max_i, 0, -1):
            if design[:i] not in patterns:
                continue
            if i == design_len:
                combos += 1
            else:
                combos += _count_combinations(design[i:])
        return combos

    return _count_combinations(design)


def part1(filepath: str) -> int:
    data = read_input(filepath)
    pattern_data, design_data = data.split("\n\n")
    patterns = set(pattern_data.split(", "))
    max_pattern_len = max(len(pattern) for pattern in patterns)
    simplified_patterns = simplify_patterns(patterns, max_pattern_len)
    return sum(
        is_possible(design, simplified_patterns, max_pattern_len)
        for design in design_data.split("\n")
    )


def part2(filepath: str) -> int:
    data = read_input(filepath)
    pattern_data, design_data = data.split("\n\n")
    patterns = set(pattern_data.split(", "))
    max_pattern_len = max(len(pattern) for pattern in patterns)
    return sum(
        count_combinations(design, patterns, max_pattern_len)
        for design in design_data.split("\n")
    )


if __name__ == "__main__":
    start = perf_counter()
    result1 = part1(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 1: {result1:>20} {seconds:>20.1f}s")

    start = perf_counter()
    result2 = part2(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 2: {result2:>20} {seconds:>20.1f}s")
