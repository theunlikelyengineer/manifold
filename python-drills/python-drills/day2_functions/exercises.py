"""Day 2: functions, lambda, closures and pattern matching.

Replace each `raise NotImplementedError` with your own code, then run:

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
    Hint: you can't negate a string, but sorting is stable.
    """
    raise NotImplementedError


def most_active_user(events: list[Row]) -> str:
    """The distinct_id with the most events. On a tie, the name first A to Z.

    Use min() or max() with a key. An empty list should raise ValueError
    (min and max do that for you).
    """
    raise NotImplementedError


def make_filter(**criteria: Any) -> Callable[[Row], bool]:
    """Return a function that is True for rows matching every criterion.

        is_pro_pageview = make_filter(event="$pageview", plan="pro")
        is_pro_pageview(row)   # True only if row["event"] and row["plan"] match

    A row without one of the keys doesn't match. No criteria matches everything.
    """
    raise NotImplementedError


def apply_mappers(row: Row, mappers: dict[str, Callable[[Any], Any]]) -> Row:
    """Return a new row where each column named in `mappers` has been passed
    through its function. Other columns are copied as they are, mappers for
    columns the row doesn't have are ignored, and the input row is unchanged.

        apply_mappers({"event": "a", "plan": None}, {"plan": lambda p: p or "free"})
        == {"event": "a", "plan": "free"}
    """
    raise NotImplementedError


def append_label(label: str, labels: list[str] = []) -> list[str]:  # noqa: B006
    """BUG HUNT. This passes the first time and goes wrong after that.

    Run the tests, work out why, then fix it. It should return a new list with
    `label` on the end, never share a list between calls, and never change a
    list passed in.
    """
    labels.append(label)
    return labels


def build_url(base: str, path: str, page: int = 1, per_page: int = 100) -> str:
    """Return "{base}/{path}?page={page}&per_page={per_page}".

    Exactly one slash between base and path, whatever the caller passes:
    build_url("https://api.example.com/", "/events") gives
    "https://api.example.com/events?page=1&per_page=100".

    Also change the signature so `page` and `per_page` are keyword-only:
    build_url(base, path, 2) must raise TypeError, build_url(base, path, page=2)
    must work.
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
    """
    raise NotImplementedError
