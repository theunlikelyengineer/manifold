"""Day 1: data structures and comprehensions.

Replace each `raise NotImplementedError` with your own code, then run:

    uv run pytest day1_data_structures
    uv run mypy day1_data_structures

The events look like the ones PostHog stores: an event name, who did it,
when, and a dict of properties that may be missing or null.
"""

from typing import Any

Event = dict[str, Any]


def flatten_event(event: Event) -> dict[str, Any]:
    """Return a flat row with exactly these keys:

        uuid, event, distinct_id, timestamp, browser, plan

    `browser` comes from properties["$browser"] and `plan` from
    properties["plan"]. Either can be missing, and `properties` itself can be
    missing or None. Use None for anything that isn't there.
    """
    raise NotImplementedError


def event_counts(events: list[Event]) -> dict[str, int]:
    """Count events by name: {"$pageview": 3, "signed_up": 1}."""
    raise NotImplementedError


def unique_users(events: list[Event]) -> set[str]:
    """Return the set of distinct_ids in `events`."""
    raise NotImplementedError


def users_by_event(events: list[Event]) -> dict[str, list[str]]:
    """Map each event name to a sorted list of the users who did it.

    Each user appears once per event name, however many times they did it.
    """
    raise NotImplementedError


def chunk[T](items: list[T], size: int) -> list[list[T]]:
    """Split `items` into lists of `size` items; the last can be shorter.

    chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]

    Raise ValueError if size is less than 1.
    """
    raise NotImplementedError


def dedupe_latest(events: list[Event]) -> list[Event]:
    """Keep one event per uuid: the one with the latest timestamp.

    Return them in the order each uuid was first seen.
    """
    raise NotImplementedError
