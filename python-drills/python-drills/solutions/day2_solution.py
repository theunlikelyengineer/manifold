"""Day 2 solutions. Read one function at a time, only when you're stuck."""

from collections import Counter
from collections.abc import Callable
from typing import Any

Row = dict[str, Any]


def sort_events(events: list[Row]) -> list[Row]:
    # Python's sort is stable, so sort by the tiebreaker first, then the main key.
    by_uuid = sorted(events, key=lambda e: e["uuid"])
    return sorted(by_uuid, key=lambda e: e["timestamp"], reverse=True)


def most_active_user(events: list[Row]) -> str:
    counts: Counter[str] = Counter(e["distinct_id"] for e in events)
    # Negate the count so "most" becomes "smallest"; the name breaks ties A to Z.
    return min(counts, key=lambda user: (-counts[user], user))


def make_filter(**criteria: Any) -> Callable[[Row], bool]:
    def predicate(row: Row) -> bool:
        return all(row.get(key) == value for key, value in criteria.items())

    return predicate


def apply_mappers(row: Row, mappers: dict[str, Callable[[Any], Any]]) -> Row:
    return {key: mappers[key](value) if key in mappers else value for key, value in row.items()}


def append_label(label: str, labels: list[str] | None = None) -> list[str]:
    # The bug: a default `[]` is created once and shared by every call.
    return [*(labels or []), label]


def build_url(base: str, path: str, *, page: int = 1, per_page: int = 100) -> str:
    return f"{base.rstrip('/')}/{path.lstrip('/')}?page={page}&per_page={per_page}"


def describe(event: Row) -> str:
    match event:
        case {"event": "$pageview", "properties": {"$current_url": str() as url}}:
            return f"viewed {url}"
        case {"event": "$pageview"}:
            return "viewed a page"
        case {"event": "signed_up", "properties": {"plan": str() as plan}}:
            return f"signed up to {plan}"
        case {"event": str() as name} if name.startswith("$"):
            return "system event"
        case {"event": str() as name}:
            return f"custom event: {name}"
        case _:
            return "unknown"
