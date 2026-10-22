import itertools
import json
from collections.abc import Iterator
from typing import Any

import pytest

from day5_iteration.exercises import (
    BadRecord,
    flat_batches,
    paginate,
    read_json_lines,
    rebatch,
    take,
    timed,
)


def test_read_json_lines_parses_and_skips_blanks() -> None:
    lines = ['{"n": 1}', "", "   ", '{"n": 2}']
    assert list(read_json_lines(lines)) == [{"n": 1}, {"n": 2}]


def test_read_json_lines_is_lazy() -> None:
    def lines() -> Iterator[str]:
        yield '{"n": 1}'
        raise AssertionError("read too far")

    assert next(read_json_lines(lines())) == {"n": 1}


def test_read_json_lines_reports_the_bad_line() -> None:
    records = read_json_lines(['{"n": 1}', "", "{not json"])
    with pytest.raises(BadRecord) as caught:
        list(records)
    assert caught.value.line_no == 3
    assert str(caught.value) == "line 3 is not valid JSON"
    assert isinstance(caught.value.__cause__, json.JSONDecodeError)


class FakeApi:
    def __init__(self) -> None:
        self.pages: dict[str | None, dict[str, Any]] = {
            None: {"results": [{"n": 1}, {"n": 2}, {"n": 3}], "next": "p2"},
            "p2": {"results": [{"n": 4}, {"n": 5}], "next": "p3"},
            "p3": {"results": [], "next": None},
        }
        self.calls: list[str | None] = []

    def fetch(self, cursor: str | None) -> dict[str, Any]:
        self.calls.append(cursor)
        return self.pages[cursor]


def test_paginate_follows_cursors_to_the_end() -> None:
    api = FakeApi()
    assert [len(page) for page in paginate(api.fetch)] == [3, 2, 0]
    assert api.calls == [None, "p2", "p3"]


def test_paginate_fetches_only_when_asked() -> None:
    api = FakeApi()
    pages = paginate(api.fetch)
    assert api.calls == []
    next(pages)
    assert api.calls == [None]


def test_rebatch_makes_fixed_size_batches() -> None:
    assert list(rebatch([[1, 2, 3], [4, 5]], 2)) == [[1, 2], [3, 4], [5]]
    assert list(rebatch([[1, 2], [3, 4]], 2)) == [[1, 2], [3, 4]]
    assert list(rebatch([[], [1]], 5)) == [[1]]
    assert list(rebatch([], 5)) == []


def test_rebatch_reads_pages_only_as_needed() -> None:
    read: list[int] = []

    def pages() -> Iterator[list[int]]:
        for i, page in enumerate([[1, 2, 3], [4, 5], [6]]):
            read.append(i)
            yield page

    batches = rebatch(pages(), 2)
    assert next(batches) == [1, 2]
    assert read == [0]


def test_rebatch_rejects_a_bad_size_straight_away() -> None:
    with pytest.raises(ValueError):
        rebatch([[1]], 0)


def test_flat_batches() -> None:
    assert flat_batches([[1, 2, 3], [4, 5]], 2) == [(1, 2), (3, 4), (5,)]


def test_take_works_on_an_endless_iterator() -> None:
    assert take(3, itertools.count(10)) == [10, 11, 12]
    assert take(5, [1, 2]) == [1, 2]


def test_timed_records_elapsed_seconds() -> None:
    stats: dict[str, float] = {}
    with timed(stats):
        sum(range(1000))
    assert stats["elapsed"] >= 0


def test_timed_records_even_when_the_block_fails() -> None:
    stats: dict[str, float] = {}
    with pytest.raises(RuntimeError), timed(stats):
        raise RuntimeError("boom")
    assert "elapsed" in stats
