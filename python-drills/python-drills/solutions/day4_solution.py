"""Day 4 solutions. Read one class at a time, only when you're stuck."""

from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator


class NotFound(Exception):
    def __init__(self, url: str) -> None:
        super().__init__(f"no response for {url}")
        self.url = url


class Fetcher(Protocol):
    def get_json(self, url: str) -> dict[str, Any]: ...


class FakeFetcher:
    def __init__(self, responses: dict[str, dict[str, Any]]) -> None:
        self.responses = responses
        self.calls: list[str] = []

    def get_json(self, url: str) -> dict[str, Any]:
        self.calls.append(url)
        try:
            return self.responses[url]
        except KeyError:
            raise NotFound(url) from None


class EventsClient:
    def __init__(self, fetcher: Fetcher, base_url: str) -> None:
        self._fetcher = fetcher
        self._base_url = base_url.rstrip("/")

    def fetch_page(self, cursor: str | None = None) -> dict[str, Any]:
        url = f"{self._base_url}/events"
        if cursor is not None:
            url = f"{url}?cursor={cursor}"
        return self._fetcher.get_json(url)


class BaseSource(ABC):
    @abstractmethod
    def read(self) -> Iterator[dict[str, Any]]: ...

    def read_all(self) -> list[dict[str, Any]]:
        return list(self.read())


class ListSource(BaseSource):
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self._rows = rows

    def read(self) -> Iterator[dict[str, Any]]:
        return iter(self._rows)


class EventsSourceConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    base_url: str
    api_key: SecretStr
    page_size: int = Field(default=100, ge=1, le=500)
    event_names: list[str] = Field(default_factory=list)

    @field_validator("base_url")
    @classmethod
    def _https_without_trailing_slash(cls, value: str) -> str:
        if not value.startswith("https://"):
            raise ValueError("base_url must start with https://")
        return value.rstrip("/")
