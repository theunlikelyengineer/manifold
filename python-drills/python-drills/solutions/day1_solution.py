"""Day 1 solutions. Read one function at a time, only when you're stuck."""

from collections import Counter, defaultdict
from typing import Any

Event = dict[str, Any]


def flatten_event(event: Event) -> dict[str, Any]:
    props = event.get("properties") or {}
    return {
        "uuid": event["uuid"],
        "event": event["event"],
        "distinct_id": event["distinct_id"],
        "timestamp": event["timestamp"],
        "browser": props.get("$browser"),
        "plan": props.get("plan"),
    }


def event_counts(events: list[Event]) -> dict[str, int]:
    return dict(Counter(e["event"] for e in events))


def unique_users(events: list[Event]) -> set[str]:
    return {e["distinct_id"] for e in events}


def users_by_event(events: list[Event]) -> dict[str, list[str]]:
    seen: defaultdict[str, set[str]] = defaultdict(set)
    for e in events:
        seen[e["event"]].add(e["distinct_id"])
    return {name: sorted(users) for name, users in seen.items()}


def chunk[T](items: list[T], size: int) -> list[list[T]]:
    if size < 1:
        raise ValueError("size must be at least 1")
    return [items[i : i + size] for i in range(0, len(items), size)]


def dedupe_latest(events: list[Event]) -> list[Event]:
    latest: dict[str, Event] = {}
    for e in events:
        current = latest.get(e["uuid"])
        if current is None or e["timestamp"] > current["timestamp"]:
            latest[e["uuid"]] = e
    return list(latest.values())
