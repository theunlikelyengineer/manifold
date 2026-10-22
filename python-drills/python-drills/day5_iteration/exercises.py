"""Day 5: generators, laziness, itertools and context managers.

This is build step 3 in miniature. Replace each `raise NotImplementedError`,
then run:

    uv run pytest day5_iteration
    uv run mypy day5_iteration
"""

from collections.abc import Callable, Iterable, Iterator
from typing import Any


class BadRecord(Exception):
    """Raised by read_json_lines for a line that isn't valid JSON.

    - BadRecord(line_no) keeps the line number as exc.line_no (counting from 1).
    - str(exc) is "line {line_no} is not valid JSON".
    """


def read_json_lines(lines: Iterable[str]) -> Iterator[dict[str, Any]]:
    """Yield one dict per line of JSON, lazily. Skip blank lines.

    A line that isn't valid JSON raises BadRecord with its line number, keeping
    the original json.JSONDecodeError as the cause.
    """
    raise NotImplementedError


def paginate(fetch: Callable[[str | None], dict[str, Any]]) -> Iterator[list[dict[str, Any]]]:
    """Yield each page's "results" list, one page at a time.

    `fetch(cursor)` returns {"results": [...], "next": "cursor" or None}.
    Call it with None first, then with each "next" cursor, and stop after a
    page whose "next" is None. Don't fetch a page until it's asked for.
    """
    raise NotImplementedError


def rebatch[T](pages: Iterable[list[T]], size: int) -> Iterator[list[T]]:
    """Turn pages of any length into lists of exactly `size` items, plus a
    shorter final list for any remainder. Read pages only as needed.

        list(rebatch([[1, 2, 3], [4, 5]], 2)) == [[1, 2], [3, 4], [5]]

    Raise ValueError for a size below 1 as soon as rebatch() is called, not
    when the first batch is asked for. (Read the laziness section of the primer.)
    """
    raise NotImplementedError


def flat_batches[T](pages: Iterable[list[T]], size: int) -> list[tuple[T, ...]]:
    """The same idea using itertools: flatten the pages with chain.from_iterable,
    then group with batched. Return a list of tuples.

        flat_batches([[1, 2, 3], [4, 5]], 2) == [(1, 2), (3, 4), (5,)]
    """
    raise NotImplementedError


def take[T](n: int, items: Iterable[T]) -> list[T]:
    """The first n items as a list. Must work on endless iterators."""
    raise NotImplementedError


def timed(stats: dict[str, float]) -> Any:
    """A context manager that stores the seconds the block took in stats["elapsed"],
    even if the block raises. Write it with contextlib.contextmanager and replace
    the `Any` return type with the right one.

        stats: dict[str, float] = {}
        with timed(stats):
            do_work()
        stats["elapsed"]   # e.g. 0.42
    """
    raise NotImplementedError
