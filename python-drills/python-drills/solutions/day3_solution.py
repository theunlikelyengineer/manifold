"""Day 3 solutions. Read one class at a time, only when you're stuck."""

from dataclasses import dataclass, field
from typing import Any, Self


class Page:
    def __init__(self, items: list[dict[str, Any]], next_cursor: str | None = None) -> None:
        self.items = items
        self.next_cursor = next_cursor

    def __repr__(self) -> str:
        return f"Page(items={len(self.items)}, next_cursor={self.next_cursor!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Page):
            return NotImplemented
        return self.items == other.items and self.next_cursor == other.next_cursor

    def __len__(self) -> int:
        return len(self.items)

    @property
    def is_last(self) -> bool:
        return self.next_cursor is None


@dataclass(frozen=True)
class PageDC:
    items: list[dict[str, Any]] = field(default_factory=list)
    next_cursor: str | None = None

    def __len__(self) -> int:
        return len(self.items)

    @property
    def is_last(self) -> bool:
        return self.next_cursor is None

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> Self:
        return cls(items=list(payload.get("results", [])), next_cursor=payload.get("next"))


@dataclass
class RunStats:
    pages: int = 0
    rows: int = 0
    errors: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.pages < 0 or self.rows < 0:
            raise ValueError("pages and rows cannot be negative")

    def record_page(self, page: PageDC) -> None:
        self.pages += 1
        self.rows += len(page)

    @property
    def rows_per_page(self) -> float:
        return self.rows / self.pages if self.pages else 0.0
