from typing import Any

import pytest
from pydantic import ValidationError

from day7_mini_build.exercises import EventsSource, Fetcher, MiniConfig

BASE = "https://api.example.com"


def _event(n: int) -> dict[str, Any]:
    return {
        "uuid": f"e{n}",
        "event": "$pageview",
        "distinct_id": "ana",
        "timestamp": f"2026-10-01T09:0{n}:00Z",
        "properties": {"$browser": "Chrome"},
    }


class FakeFetcher:
    def __init__(self) -> None:
        self.responses: dict[str, dict[str, Any]] = {
            f"{BASE}/events": {
                "results": [_event(1), _event(2), _event(3)],
                "next": f"{BASE}/events?cursor=2",
            },
            f"{BASE}/events?cursor=2": {"results": [_event(4), _event(5)], "next": None},
        }
        self.calls: list[str] = []

    def get_json(self, url: str) -> dict[str, Any]:
        self.calls.append(url)
        return self.responses[url]


def _source(**config: Any) -> tuple[EventsSource, FakeFetcher]:
    fetcher = FakeFetcher()
    raw: dict[str, Any] = {"base_url": BASE, **config}
    return EventsSource(MiniConfig.model_validate(raw), fetcher), fetcher


def test_fake_fetcher_fits_the_protocol() -> None:
    fetcher: Fetcher = FakeFetcher()
    assert fetcher is not None


def test_reads_every_page_in_fixed_batches() -> None:
    source, fetcher = _source(batch_size=2)
    batches = list(source.read())
    assert [len(b) for b in batches] == [2, 2, 1]
    assert [row["uuid"] for b in batches for row in b] == ["e1", "e2", "e3", "e4", "e5"]
    assert fetcher.calls == [f"{BASE}/events", f"{BASE}/events?cursor=2"]


def test_rows_are_flat() -> None:
    source, _ = _source()
    row = next(source.read())[0]
    assert row == {
        "uuid": "e1",
        "event": "$pageview",
        "distinct_id": "ana",
        "timestamp": "2026-10-01T09:01:00Z",
        "browser": "Chrome",
        "plan": None,
    }


def test_stats_after_a_full_read() -> None:
    source, _ = _source(batch_size=2)
    list(source.read())
    assert (source.stats.pages, source.stats.rows) == (2, 5)


def test_fetches_lazily_and_counts_only_rows_yielded() -> None:
    source, fetcher = _source(batch_size=2)
    batches = source.read()
    assert fetcher.calls == []
    next(batches)
    assert fetcher.calls == [f"{BASE}/events"]
    assert (source.stats.pages, source.stats.rows) == (1, 2)


def test_max_pages_stops_early() -> None:
    source, fetcher = _source(batch_size=2, max_pages=1)
    assert [len(b) for b in source.read()] == [2, 1]
    assert len(fetcher.calls) == 1
    assert source.stats.pages == 1


def test_name_and_trailing_slash() -> None:
    source, fetcher = _source(base_url=BASE + "/")
    assert source.name == f"events:{BASE}"
    next(source.read())
    assert fetcher.calls[0] == f"{BASE}/events"


@pytest.mark.parametrize(
    "bad",
    [
        {"base_url": "http://api.example.com"},
        {"batch_size": 0},
        {"max_pages": 0},
    ],
)
def test_config_rejects_bad_values(bad: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        MiniConfig.model_validate({"base_url": BASE, **bad})


def test_config_is_frozen() -> None:
    config = MiniConfig.model_validate({"base_url": BASE})
    with pytest.raises(ValidationError):
        config.batch_size = 5
