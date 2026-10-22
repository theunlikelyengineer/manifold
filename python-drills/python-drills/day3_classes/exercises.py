"""Day 3: classes and dataclasses.

Fill in each class, then run:

    uv run pytest day3_classes
    uv run mypy day3_classes

mypy will complain about the tests until your classes have the right shape.
That's expected; it should be clean by the end.
"""

from typing import Any


class Page:
    """A page of API results, written by hand. No dataclass.

    - Page(items, next_cursor=None) keeps both as attributes.
    - repr(page) looks like: Page(items=2, next_cursor='abc')
      (items shows how many there are, next_cursor shows its repr).
    - page == other compares items and next_cursor. Comparing with something
      that isn't a Page is simply "not equal".
    - len(page) is the number of items.
    - page.is_last is a property: True when next_cursor is None.
    """

    def __init__(self, items: list[dict[str, Any]], next_cursor: str | None = None) -> None:
        raise NotImplementedError


class PageDC:
    """The same page as a frozen dataclass.

    - Fields: items (defaults to an empty list) and next_cursor (defaults to None).
    - Frozen: assigning to a field raises dataclasses.FrozenInstanceError.
    - Keep len(page) and the is_last property.
    - Add a classmethod, PageDC.from_payload(payload), for API responses shaped
      like {"results": [...], "next": "abc" or None}. Either key can be missing.
    """


class RunStats:
    """A mutable dataclass that tracks a run.

    - Fields: pages (default 0), rows (default 0), errors (default empty list).
      Two RunStats must never share an errors list.
    - Raise ValueError when created with negative pages or rows.
    - record_page(page: PageDC) adds 1 to pages and len(page) to rows.
    - rows_per_page is a property: rows / pages, or 0.0 when pages is 0.
    """
