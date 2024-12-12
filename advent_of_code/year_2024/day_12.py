from itertools import chain
from pathlib import Path
from time import perf_counter
from typing import Self

INPUT_FILEPATH = "data/2024_12"


type Plot = tuple[int, int, str]


def read_input(filepath: str) -> str:
    with Path(filepath).open() as file:
        return file.read()


class Region:
    ADJACENT_OFFSETS = (1, 0), (-1, 0), (0, 1), (0, -1)

    def __init__(
        self, plots: list[Plot] | None = None, plant_type: str | None = None
    ) -> None:
        self.plots = plots if plots else []
        self.plant_type = plant_type

    @classmethod
    def from_str(cls, data: str) -> Self:
        return cls(
            [
                (x, y, plant_type)
                for y, line in enumerate(data.split("\n"))
                for x, plant_type in enumerate(line)
            ]
        )

    def take_connected_plots_of_same_type(self, plot: Plot) -> list[Plot]:
        x, y, plant_type = plot
        adjacent_plots = []
        for dx, dy in self.ADJACENT_OFFSETS:
            adjacent_plot = (x + dx, y + dy, plant_type)
            if adjacent_plot in self.plots:
                adjacent_plots.append(adjacent_plot)
                self.plots.remove(adjacent_plot)
        return adjacent_plots + list(
            chain.from_iterable(
                self.take_connected_plots_of_same_type(plot) for plot in adjacent_plots
            )
        )

    def split(self) -> list[Self]:
        cls = type(self)
        regions = []
        while len(self.plots) > 0:
            plot = self.plots.pop()
            _, _, plant_type = plot
            regions.append(
                cls([plot, *self.take_connected_plots_of_same_type(plot)], plant_type)
            )
        return regions

    def get_corners(self, point: tuple[int, int]) -> list[tuple[int, int, bool]]:
        x, y = point
        upper_left = (x - 1, y - 1, self.plant_type)
        upper_right = (x, y - 1, self.plant_type)
        lower_left = (x - 1, y, self.plant_type)
        lower_right = (x, y, self.plant_type)
        adjacent_plots = tuple(
            plot
            for plot in (upper_left, upper_right, lower_left, lower_right)
            if plot in self.plots
        )
        adjacent_plot_count = len(adjacent_plots)
        if adjacent_plot_count in {0, 4}:
            return []
        if adjacent_plot_count in {1, 3}:
            return [(x, y, False)]
        if adjacent_plots not in {(upper_left, lower_right), (upper_right, lower_left)}:
            return [(x, y, False), (x, y, True)]
        return []

    @property
    def perimeter(self) -> int:
        return sum(
            True
            for x, y, plant_type in self.plots
            for dx, dy in self.ADJACENT_OFFSETS
            if (x + dx, y + dy, plant_type) not in self.plots
        )

    @property
    def area(self) -> int:
        return len(self.plots)

    @property
    def price_to_fence(self) -> int:
        return self.perimeter * self.area

    @property
    def corners(self) -> int:
        return len(
            set(
                chain.from_iterable(
                    self.get_corners(point)
                    for x, y, _ in self.plots
                    for point in ((x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1))
                )
            )
        )

    @property
    def discounted_price_to_fence(self) -> int:
        return self.corners * self.area


class RegionList(list[Region]):
    @classmethod
    def from_str(cls, data: str) -> Self:
        return cls(Region.from_str(data).split())

    @property
    def price_to_fence(self) -> int:
        return sum(region.price_to_fence for region in self)

    @property
    def discounted_price_to_fence(self) -> int:
        return sum(region.discounted_price_to_fence for region in self)


def part1(filepath: str) -> int:
    data = read_input(filepath)
    return RegionList.from_str(data).price_to_fence


def part2(filepath: str) -> int:
    data = read_input(filepath)
    return RegionList.from_str(data).discounted_price_to_fence


if __name__ == "__main__":
    start = perf_counter()
    result = part1(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 1: {result:>20} {seconds:>20.1f}s")

    start = perf_counter()
    result = part2(INPUT_FILEPATH)
    seconds = perf_counter() - start
    print(f"Part 2: {result:>20} {seconds:>20.1f}s")
