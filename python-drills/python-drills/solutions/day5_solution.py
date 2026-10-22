"""Day 5 solutions. Read one function at a time, only when you're stuck."""

import json
import time
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from itertools import batched, chain, islice
from typing import Any


class BadRecord(Exception):
    def __init__(self, line_no: int) -> None:
        super().__init__(f"line {line_no} is not valid JSON")
        self.line_no = line_no


def read_json_lines(lines: Iterable[str]) -> Iterator[dict[str, Any]]:
    for line_no, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError as exc:
            raise BadRecord(line_no) from exc


def paginate(fetch: Callable[[str | None], dict[str, Any]]) -> Iterator[list[dict[str, Any]]]:
    cursor: str | None = None
    while True:
        payload = fetch(cursor)
        yield payload["results"]
        cursor = payload.get("next")
        if cursor is None:
            return


def rebatch[T](pages: Iterable[list[T]], size: int) -> Iterator[list[T]]:
    # A plain function, so the check runs as soon as rebatch() is called.
    if size < 1:
        raise ValueError("size must be at least 1")
    return _rebatch(pages, size)


def _rebatch[T](pages: Iterable[list[T]], size: int) -> Iterator[list[T]]:
    buffer: list[T] = []
    for page in pages:
        buffer.extend(page)
        while len(buffer) >= size:
            yield buffer[:size]
            buffer = buffer[size:]
    if buffer:
        yield buffer


def flat_batches[T](pages: Iterable[list[T]], size: int) -> list[tuple[T, ...]]:
    return list(batched(chain.from_iterable(pages), size))


def take[T](n: int, items: Iterable[T]) -> list[T]:
    return list(islice(items, n))


@contextmanager
def timed(stats: dict[str, float]) -> Iterator[None]:
    start = time.perf_counter()
    try:
        yield
    finally:
        stats["elapsed"] = time.perf_counter() - start
