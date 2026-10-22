from typing import Any

import pytest

from day1_data_structures.exercises import (
    chunk,
    dedupe_latest,
    event_counts,
    flatten_event,
    unique_users,
    users_by_event,
)

EVENTS: list[dict[str, Any]] = [
    {
        "uuid": "e1",
        "event": "$pageview",
        "distinct_id": "ana",
        "timestamp": "2026-10-01T09:00:00Z",
        "properties": {"$browser": "Chrome", "plan": "pro"},
    },
    {
        "uuid": "e2",
        "event": "$pageview",
        "distinct_id": "ben",
        "timestamp": "2026-10-01T09:05:00Z",
        "properties": {"$browser": "Firefox"},
    },
    {
        "uuid": "e3",
        "event": "signed_up",
        "distinct_id": "ben",
        "timestamp": "2026-10-01T09:06:00Z",
        "properties": {"plan": "free"},
    },
    {
        "uuid": "e4",
        "event": "$pageview",
        "distinct_id": "ana",
        "timestamp": "2026-10-01T09:10:00Z",
    },
]


def test_flatten_event_reads_nested_properties() -> None:
    assert flatten_event(EVENTS[0]) == {
        "uuid": "e1",
        "event": "$pageview",
        "distinct_id": "ana",
        "timestamp": "2026-10-01T09:00:00Z",
        "browser": "Chrome",
        "plan": "pro",
    }


def test_flatten_event_uses_none_for_a_missing_property() -> None:
    row = flatten_event(EVENTS[1])
    assert row["browser"] == "Firefox"
    assert row["plan"] is None


def test_flatten_event_copes_with_no_properties_key() -> None:
    row = flatten_event(EVENTS[3])
    assert row["browser"] is None
    assert row["plan"] is None


def test_flatten_event_copes_with_properties_set_to_none() -> None:
    row = flatten_event({**EVENTS[0], "properties": None})
    assert row["browser"] is None
    assert row["plan"] is None


def test_event_counts() -> None:
    assert event_counts(EVENTS) == {"$pageview": 3, "signed_up": 1}


def test_event_counts_of_nothing_is_empty() -> None:
    assert event_counts([]) == {}


def test_unique_users() -> None:
    assert unique_users(EVENTS) == {"ana", "ben"}


def test_users_by_event_is_sorted_with_no_repeats() -> None:
    assert users_by_event(EVENTS) == {"$pageview": ["ana", "ben"], "signed_up": ["ben"]}


@pytest.mark.parametrize(
    ("items", "size", "expected"),
    [
        ([1, 2, 3, 4, 5], 2, [[1, 2], [3, 4], [5]]),
        ([1, 2, 3, 4], 2, [[1, 2], [3, 4]]),
        ([1, 2], 5, [[1, 2]]),
        ([], 3, []),
    ],
)
def test_chunk(items: list[int], size: int, expected: list[list[int]]) -> None:
    assert chunk(items, size) == expected


def test_chunk_rejects_a_size_below_one() -> None:
    with pytest.raises(ValueError):
        chunk([1, 2], 0)


def test_dedupe_latest_keeps_the_newest_in_first_seen_order() -> None:
    events: list[dict[str, Any]] = [
        {"uuid": "a", "timestamp": "2026-10-01T09:00:00Z", "v": 1},
        {"uuid": "b", "timestamp": "2026-10-01T09:30:00Z", "v": 1},
        {"uuid": "a", "timestamp": "2026-10-01T10:00:00Z", "v": 2},
        {"uuid": "b", "timestamp": "2026-10-01T08:00:00Z", "v": 2},
    ]
    assert dedupe_latest(events) == [events[2], events[1]]
