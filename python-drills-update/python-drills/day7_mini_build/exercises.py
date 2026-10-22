"""Day 7: mini-build. A timed dress rehearsal for build steps 1 to 3.

Timebox: 90 minutes. No solutions, no AI. The spec is in PRIMER.md and the
docstrings below; the tests in test_day7.py are the acceptance criteria.

    uv run pytest day7_mini_build
    uv run mypy day7_mini_build
"""

from collections.abc import Iterator
from typing import Any, Protocol

Row = dict[str, Any]


class Fetcher(Protocol):
    """Given to you. Anything with this method can be a fetcher."""

    def get_json(self, url: str) -> dict[str, Any]: ...


class MiniConfig:
    """A frozen Pydantic model.

    - base_url: str. Must start with "https://"; any trailing slash is removed.
    - batch_size: int, default 100, at least 1.
    - max_pages: int or None, default None. If set, at least 1.
    """


class SourceStats:
    """A dataclass with pages and rows, both starting at 0."""


def flatten(event: Row) -> Row:
    """The same as day 1's flatten_event."""
    raise NotImplementedError


class EventsSource:
    """Reads events from a paginated API in fixed-size batches of flat rows.

    - EventsSource(config, fetcher). Keep a SourceStats in self.stats.
    - name is a property: "events:" followed by the config's base_url.
    - read() fetches "{base_url}/events", then follows each response's "next"
      URL until it's None, or until max_pages pages have been fetched.
      Responses look like {"results": [event, ...], "next": "https://..." or None}.
    - It flattens every event and yields lists of batch_size rows, then a
      shorter list for any remainder.
    - It's lazy: a page is fetched only when more rows are needed.
    - stats.pages counts pages fetched; stats.rows counts rows yielded so far.

    Example, with batch_size=2 and an API whose first page has 3 events and
    whose second (last) page has 2:

        source = EventsSource(MiniConfig(base_url="https://api.example.com", batch_size=2),
                              fetcher)
        source.name                                -> "events:https://api.example.com"
        [len(batch) for batch in source.read()]    -> [2, 2, 1]
        source.stats                               -> SourceStats(pages=2, rows=5)
    """

    def __init__(self, config: MiniConfig, fetcher: Fetcher) -> None:
        raise NotImplementedError

    @property
    def name(self) -> str:
        raise NotImplementedError

    def read(self) -> Iterator[list[Row]]:
        raise NotImplementedError
