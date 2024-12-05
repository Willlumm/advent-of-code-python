from textwrap import dedent

import pytest

from advent_of_code.year_2024.day_05 import (
    PagesDict,
    Update,
    UpdateList,
    _read_input,
    _split_input,
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
def pages() -> PagesDict:
    return PagesDict(
        {
            53: {97, 75, 61, 47},
            13: {97, 75, 47, 61, 53, 29},
            61: {97, 75, 47},
            47: {97, 75},
            29: {97, 75, 47, 53, 61},
            75: {97},
        },
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


def test__read_input(data: str) -> None:
    assert _read_input(TEST_DATA_FILEPATH) == data


def test__split_input(data: str, page_order_data: str, update_data: str) -> None:
    assert _split_input(data) == [page_order_data, update_data]


def test__parse_page_data(page_order_data: str, pages: PagesDict) -> None:
    assert PagesDict.from_str(page_order_data) == pages


def test__parse_update_data(update_data: str, updates: UpdateList) -> None:
    assert UpdateList.from_str(update_data) == updates


def test__sum_valid_middles() -> None:
    updates = UpdateList(
        [
            Update([75, 47, 61, 53, 29]),
            Update([97, 61, 53, 29, 13]),
            Update([75, 29, 13]),
        ]
    )
    assert updates.sum_middles == 143
