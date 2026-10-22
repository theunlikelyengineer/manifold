import time

import pytest

from day6_dsa.exercises import (
    count_in_range,
    first_duplicate,
    has_pair_with_sum,
    merge_sorted,
    sessionize,
    top_k,
)


@pytest.mark.parametrize(
    ("nums", "target", "expected"),
    [
        ([3, 9, 4, 1], 13, True),
        ([3, 9, 4, 1], 6, False),
        ([5, 5], 10, True),
        ([5], 10, False),
        ([], 0, False),
        ([-2, 7, 11], 5, True),
    ],
)
def test_has_pair_with_sum(nums: list[int], target: int, expected: bool) -> None:
    assert has_pair_with_sum(nums, target) is expected


def test_has_pair_with_sum_is_fast_on_a_bigger_input() -> None:
    nums = list(range(0, 12_000, 2))
    start = time.perf_counter()
    assert has_pair_with_sum(nums, 23_994)
    assert not has_pair_with_sum(nums, 1)
    elapsed = time.perf_counter() - start
    assert elapsed < 0.5, f"took {elapsed:.1f}s: is there a loop inside a loop?"


@pytest.mark.parametrize(
    ("ids", "expected"),
    [(["a", "b", "b", "a"], "b"), (["a", "b", "a", "b"], "a"), (["a", "b"], None), ([], None)],
)
def test_first_duplicate(ids: list[str], expected: str | None) -> None:
    assert first_duplicate(ids) == expected


def test_top_k() -> None:
    assert top_k(["b", "a", "b", "c", "a", "b"], 2) == [("b", 3), ("a", 2)]


def test_top_k_breaks_ties_alphabetically() -> None:
    assert top_k(["c", "b", "a", "c", "b", "a"], 2) == [("a", 2), ("b", 2)]


def test_top_k_when_k_is_bigger_than_the_number_of_names() -> None:
    assert top_k(["a"], 5) == [("a", 1)]


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ([1, 4, 9], [2, 3, 10, 11], [1, 2, 3, 4, 9, 10, 11]),
        ([], [1, 2], [1, 2]),
        ([1, 1], [1], [1, 1, 1]),
        ([], [], []),
    ],
)
def test_merge_sorted(a: list[int], b: list[int], expected: list[int]) -> None:
    assert merge_sorted(a, b) == expected


def test_sessionize() -> None:
    assert sessionize([0, 100, 2000, 2100, 5000], 1800) == [[0, 100], [2000, 2100], [5000]]


def test_sessionize_gap_exactly_equal_stays_in_session() -> None:
    assert sessionize([0, 1800, 3601], 1800) == [[0, 1800], [3601]]


def test_sessionize_nothing() -> None:
    assert sessionize([], 1800) == []


@pytest.mark.parametrize(
    ("start", "end", "expected"),
    [(2, 5, 3), (0, 100, 6), (4, 5, 0), (8, 9, 1), (9, 20, 0)],
)
def test_count_in_range(start: int, end: int, expected: int) -> None:
    assert count_in_range([1, 2, 2, 3, 5, 8], start, end) == expected
