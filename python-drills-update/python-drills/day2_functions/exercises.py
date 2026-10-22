"""Day 2: functions, lambda, closures and pattern matching.

Read WALKTHROUGH.md first: it solves a similar problem for each exercise.
Then replace each `raise NotImplementedError` with your own code and run:

    uv run pytest day2_functions
    uv run mypy day2_functions

Two drills are different: `append_label` already has code with a bug in it,
and `build_url` needs a change to its signature as well as a body.
"""

from collections.abc import Callable
from typing import Any

Row = dict[str, Any]


def sort_events(events: list[Row]) -> list[Row]:
    """Newest timestamp first. Where timestamps tie, uuid A to Z.

    Return a new list; don't change the one passed in.

    Example:
        events = [{"uuid": "c", "timestamp": "10:00"},
                  {"uuid": "a", "timestamp": "09:00"},
                  {"uuid": "b", "timestamp": "10:00"}]

        sort_events(events) returns
        [{"uuid": "b", "timestamp": "10:00"},
         {"uuid": "c", "timestamp": "10:00"},
         {"uuid": "a", "timestamp": "09:00"}]
    """
    raise NotImplementedError


def most_active_user(events: list[Row]) -> str:
    """The distinct_id with the most events. On a tie, the name first A to Z.

    An empty list should raise ValueError (min and max do that for you).

    Example:
        events = [{"distinct_id": "cara"}, {"distinct_id": "ben"},
                  {"distinct_id": "cara"}, {"distinct_id": "ben"}]

        most_active_user(events) returns "ben"   (both have 2; ben is first A to Z)
    """
    raise NotImplementedError


def make_filter(**criteria: Any) -> Callable[[Row], bool]:
    """Return a function that is True for rows matching every criterion.

    A row without one of the keys doesn't match. No criteria matches everything.

    Example:
        is_pro_pageview = make_filter(event="$pageview", plan="pro")

        is_pro_pageview({"event": "$pageview", "plan": "pro", "n": 1}) returns True
        is_pro_pageview({"event": "$pageview", "plan": "free"}) returns False
        is_pro_pageview({"event": "$pageview"}) returns False
    """
    raise NotImplementedError


def apply_mappers(row: Row, mappers: dict[str, Callable[[Any], Any]]) -> Row:
    """Return a new row where each column named in `mappers` has been passed
    through its function. Other columns are copied as they are, mappers for
    columns the row doesn't have are ignored, and the input row is unchanged.

    Example:
        row = {"event": "$pageview", "plan": None}
        mappers = {"event": str.upper, "plan": lambda p: p or "free"}

        apply_mappers(row, mappers) returns {"event": "$PAGEVIEW", "plan": "free"}
    """
    raise NotImplementedError


def append_label(label: str, labels: list[str] = []) -> list[str]:  # noqa: B006
    """BUG HUNT. This passes the first time and goes wrong after that.

    Run the tests, work out why, then fix it. It should return a new list with
    `label` on the end, never share a list between calls, and never change a
    list passed in.

    Example (what it should do):
        append_label("a") returns ["a"]
        append_label("b") returns ["b"]          (the buggy version gives ["a", "b"])

        existing = ["x"]
        append_label("y", existing) returns ["x", "y"], and existing is still ["x"]
    """
    labels.append(label)
    return labels


def build_url(base: str, path: str, page: int = 1, per_page: int = 100) -> str:
    """Return "{base}/{path}?page={page}&per_page={per_page}", with exactly one
    slash between base and path, whatever the caller passes.

    Also change the signature so `page` and `per_page` are keyword-only.

    Example:
        build_url("https://api.example.com/", "/events", page=2)
        returns "https://api.example.com/events?page=2&per_page=100"

        build_url("https://api.example.com", "events", 2) raises TypeError
    """
    raise NotImplementedError


def describe(event: Row) -> str:
    """Describe an event using `match`, checking these in order:

    - a $pageview with properties.$current_url  -> "viewed {url}"
    - any other $pageview                        -> "viewed a page"
    - signed_up with a string properties.plan    -> "signed up to {plan}"
    - any other event name starting with "$"     -> "system event"
    - any other event name that's a string       -> "custom event: {name}"
    - anything else                              -> "unknown"

    Example:
        describe({"event": "$pageview", "properties": {"$current_url": "/pricing"}})
        returns "viewed /pricing"

        describe({"event": "signed_up"}) returns "custom event: signed_up"   (no plan)
        describe({"event": "$autocapture"}) returns "system event"
        describe({}) returns "unknown"
    """
    raise NotImplementedError
