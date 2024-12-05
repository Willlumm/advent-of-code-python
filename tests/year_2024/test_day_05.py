from textwrap import dedent

import pytest

from advent_of_code.year_2024.day_05 import (
    PageDict,
    Update,
    UpdateList,
    _read_input,
    _split_input,
    part2,
)

TEST_DATA_FILEPATH = "tests/data/2024_05"


@pytest.fixture
def data() -> str:
    return dedent("""
        47|53
        97|13
        97|61
        97|47
        75|29
        61|13
        75|53
        29|13
        97|29
        53|29
        61|53
        97|53
        61|29
        47|13
        75|47
        97|75
        47|61
        75|61
        47|29
        75|13
        53|13

        75,47,61,53,29
        97,61,53,29,13
        75,29,13
        75,97,47,61,53
        61,13,29
        97,13,75,29,47
    """).strip()


@pytest.fixture
def page_order_data() -> str:
    return dedent("""
        47|53
        97|13
        97|61
        97|47
        75|29
        61|13
        75|53
        29|13
        97|29
        53|29
        61|53
        97|53
        61|29
        47|13
        75|47
        97|75
        47|61
        75|61
        47|29
        75|13
        53|13
    """).strip()


@pytest.fixture
def update_data() -> str:
    return dedent("""
        75,47,61,53,29
        97,61,53,29,13
        75,29,13
        75,97,47,61,53
        61,13,29
        97,13,75,29,47
    """).strip()


@pytest.fixture
def pages() -> PageDict:
    return PageDict(
        {
            47: {97, 75},
            53: {97, 75, 61, 47},
            97: set(),
            13: {97, 75, 47, 61, 53, 29},
            61: {97, 75, 47},
            75: {97},
            29: {97, 75, 47, 53, 61},
        }
    )


@pytest.fixture
def updates() -> UpdateList:
    return UpdateList(
        [
            Update([75, 47, 61, 53, 29]),
            Update([97, 61, 53, 29, 13]),
            Update([75, 29, 13]),
            Update([75, 97, 47, 61, 53]),
            Update([61, 13, 29]),
            Update([97, 13, 75, 29, 47]),
        ]
    )


@pytest.fixture
def unordered_updates() -> UpdateList:
    return UpdateList(
        [
            Update([75, 97, 47, 61, 53]),
            Update([61, 13, 29]),
            Update([97, 13, 75, 29, 47]),
        ]
    )


def test__read_input(data: str) -> None:
    assert _read_input(TEST_DATA_FILEPATH) == data


def test__split_input(data: str, page_order_data: str, update_data: str) -> None:
    assert _split_input(data) == [page_order_data, update_data]


class TestPageDict:
    def test_from_str(self, page_order_data: str, pages: PageDict) -> None:
        print(PageDict.from_str(page_order_data))
        assert PageDict.from_str(page_order_data) == pages

    def test_get_free_number(self, pages: PageDict) -> None:
        assert pages.get_free_page_number() == 97

    def test_simplify(self, pages: PageDict) -> None:
        expected = PageDict(
            {
                47: {75},
                53: {75, 61, 47},
                61: {75, 47},
                75: set(),
                29: {75, 47, 53, 61},
            }
        )
        assert pages.simplify([75, 47, 61, 53, 29]) == expected


class TestUpdateList:
    def test_from_str(self, update_data: str, updates: UpdateList) -> None:
        assert UpdateList.from_str(update_data) == updates

    def test_filter(
        self, updates: UpdateList, unordered_updates: UpdateList, pages: PageDict
    ) -> None:
        assert updates.filter(pages, ordered=False) == unordered_updates

    def test_order_all(self, unordered_updates: UpdateList, pages: PageDict) -> None:
        expected = UpdateList(
            [
                Update([97, 75, 47, 61, 53]),
                Update([61, 29, 13]),
                Update([97, 75, 47, 29, 13]),
            ]
        )
        assert unordered_updates.order_all(pages) == expected

    def test_sum_of_middles(self) -> None:
        updates = UpdateList(
            [
                Update([75, 47, 61, 53, 29]),
                Update([97, 61, 53, 29, 13]),
                Update([75, 29, 13]),
            ]
        )
        assert updates.sum_of_middles == 143


def test_part2() -> None:
    assert part2(TEST_DATA_FILEPATH) == 123
