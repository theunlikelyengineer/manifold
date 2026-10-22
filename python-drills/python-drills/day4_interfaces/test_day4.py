from typing import Any, cast

import pytest
from pydantic import ValidationError

from day4_interfaces.exercises import (
    BaseSource,
    EventsClient,
    EventsSourceConfig,
    FakeFetcher,
    Fetcher,
    ListSource,
    NotFound,
)

BASE = "https://api.example.com"


def test_fake_fetcher_returns_responses_and_records_calls() -> None:
    fetcher = FakeFetcher({f"{BASE}/a": {"ok": 1}, f"{BASE}/b": {"ok": 2}})
    assert fetcher.get_json(f"{BASE}/b") == {"ok": 2}
    assert fetcher.get_json(f"{BASE}/a") == {"ok": 1}
    assert fetcher.calls == [f"{BASE}/b", f"{BASE}/a"]


def test_fake_fetcher_raises_not_found_with_the_url() -> None:
    fetcher = FakeFetcher({})
    with pytest.raises(NotFound) as caught:
        fetcher.get_json(f"{BASE}/missing")
    assert caught.value.url == f"{BASE}/missing"
    assert str(caught.value) == f"no response for {BASE}/missing"
    assert caught.value.__suppress_context__


def test_fake_fetcher_satisfies_the_protocol() -> None:
    fetcher: Fetcher = FakeFetcher({})  # mypy checks this line
    assert fetcher is not None


def test_events_client_builds_urls() -> None:
    fetcher = FakeFetcher({f"{BASE}/events": {"page": 1}, f"{BASE}/events?cursor=abc": {"page": 2}})
    client = EventsClient(fetcher, BASE + "/")
    assert client.fetch_page() == {"page": 1}
    assert client.fetch_page("abc") == {"page": 2}
    assert fetcher.calls == [f"{BASE}/events", f"{BASE}/events?cursor=abc"]


def test_base_source_cannot_be_created() -> None:
    with pytest.raises(TypeError):
        cast(Any, BaseSource)()


def test_a_subclass_without_read_cannot_be_created() -> None:
    class Incomplete(BaseSource):
        pass

    with pytest.raises(TypeError):
        cast(Any, Incomplete)()


def test_list_source_reads_and_shares_read_all() -> None:
    rows = [{"n": 1}, {"n": 2}]
    source = ListSource(rows)
    assert next(source.read()) == {"n": 1}
    assert source.read_all() == rows


def _config(**overrides: Any) -> EventsSourceConfig:
    raw: dict[str, Any] = {"base_url": BASE, "api_key": "secret-key", **overrides}
    return EventsSourceConfig.model_validate(raw)


def test_config_defaults_and_conversion() -> None:
    config = _config(page_size="250")
    assert config.page_size == 250
    assert config.event_names == []
    assert _config().page_size == 100


@pytest.mark.parametrize("bad", [0, 501, "lots"])
def test_config_rejects_bad_page_sizes(bad: Any) -> None:
    with pytest.raises(ValidationError):
        _config(page_size=bad)


def test_config_requires_https_and_strips_the_trailing_slash() -> None:
    assert _config(base_url=BASE + "/").base_url == BASE
    with pytest.raises(ValidationError, match="https"):
        _config(base_url="http://api.example.com")


def test_config_hides_the_api_key() -> None:
    config = _config()
    assert "secret-key" not in repr(config)
    assert "secret-key" not in str(config)
    assert config.api_key.get_secret_value() == "secret-key"


def test_config_is_frozen() -> None:
    config = _config()
    with pytest.raises(ValidationError):
        config.page_size = 5


def test_config_event_names_are_not_shared() -> None:
    assert _config().event_names is not _config().event_names
