"""Day 7 solution. Compare with yours after the 90 minutes, not during."""

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, Field, field_validator

Row = dict[str, Any]


class Fetcher(Protocol):
    def get_json(self, url: str) -> dict[str, Any]: ...


class MiniConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    base_url: str
    batch_size: int = Field(default=100, ge=1)
    max_pages: int | None = Field(default=None, ge=1)

    @field_validator("base_url")
    @classmethod
    def _https_without_trailing_slash(cls, value: str) -> str:
        if not value.startswith("https://"):
            raise ValueError("base_url must start with https://")
        return value.rstrip("/")


@dataclass
class SourceStats:
    pages: int = 0
    rows: int = 0


def flatten(event: Row) -> Row:
    props = event.get("properties") or {}
    return {
        "uuid": event["uuid"],
        "event": event["event"],
        "distinct_id": event["distinct_id"],
        "timestamp": event["timestamp"],
        "browser": props.get("$browser"),
        "plan": props.get("plan"),
    }


class EventsSource:
    def __init__(self, config: MiniConfig, fetcher: Fetcher) -> None:
        self._config = config
        self._fetcher = fetcher
        self.stats = SourceStats()

    @property
    def name(self) -> str:
        return f"events:{self._config.base_url}"

    def _pages(self) -> Iterator[list[Row]]:
        url: str | None = f"{self._config.base_url}/events"
        while url is not None:
            payload = self._fetcher.get_json(url)
            self.stats.pages += 1
            yield payload["results"]
            if self._config.max_pages is not None and self.stats.pages >= self._config.max_pages:
                return
            url = payload.get("next")

    def read(self) -> Iterator[list[Row]]:
        size = self._config.batch_size
        buffer: list[Row] = []
        for page in self._pages():
            buffer.extend(flatten(event) for event in page)
            while len(buffer) >= size:
                batch, buffer = buffer[:size], buffer[size:]
                self.stats.rows += len(batch)
                yield batch
        if buffer:
            self.stats.rows += len(buffer)
            yield buffer
