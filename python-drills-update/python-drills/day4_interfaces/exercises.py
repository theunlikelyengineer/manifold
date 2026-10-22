"""Day 4: composition, interfaces, custom exceptions and Pydantic.

This is build steps 1 and 2 in miniature. Fill in each class, then run:

    uv run pytest day4_interfaces
    uv run mypy day4_interfaces

mypy will complain about the tests until your classes have the right shape.
"""

from typing import Any


class NotFound(Exception):
    """Raised by FakeFetcher when it has no response for a URL.

    - NotFound(url) keeps the URL as an attribute: exc.url
    - str(exc) is "no response for {url}"

    Example:
        exc = NotFound("https://api.example.com/x")

        exc.url   -> "https://api.example.com/x"
        str(exc)  -> "no response for https://api.example.com/x"
    """


class Fetcher:
    """Make this a Protocol (from typing) with one method:

        def get_json(self, url: str) -> dict[str, Any]: ...

    Nothing inherits from it. Any class with a matching get_json counts.

    Example (what it lets you write, checked by mypy):
        fetcher: Fetcher = FakeFetcher({})
    """


class FakeFetcher:
    """A test double that satisfies Fetcher without inheriting from it.

    - FakeFetcher(responses) takes a dict of {url: response_dict}.
    - get_json(url) records the URL in self.calls (a list, oldest first) and
      returns the matching response.
    - An unknown URL raises NotFound(url), not KeyError. Hide the KeyError
      from the traceback.

    Example:
        fetcher = FakeFetcher({"https://api.example.com/a": {"ok": 1}})

        fetcher.get_json("https://api.example.com/a")   -> {"ok": 1}
        fetcher.calls                                   -> ["https://api.example.com/a"]
        fetcher.get_json("https://api.example.com/zzz") raises NotFound
    """

    def __init__(self, responses: dict[str, dict[str, Any]]) -> None:
        raise NotImplementedError


class EventsClient:
    """Composition: it's handed a Fetcher instead of creating one.

    - EventsClient(fetcher, base_url). A trailing slash on base_url is removed.
    - fetch_page(cursor=None) fetches "{base_url}/events", or
      "{base_url}/events?cursor={cursor}" when a cursor is given, and returns
      the response dict.

    Example:
        client = EventsClient(fetcher, "https://api.example.com/")

        client.fetch_page()       fetches "https://api.example.com/events"
        client.fetch_page("abc")  fetches "https://api.example.com/events?cursor=abc"
    """

    def __init__(self, fetcher: Any, base_url: str) -> None:
        raise NotImplementedError


class BaseSource:
    """Make this an abstract base class (from abc):

    - read() is abstract and returns an Iterator[dict[str, Any]].
    - read_all() is a normal method that returns list(self.read()), so every
      subclass gets it for free.
    - BaseSource() itself, or a subclass without read(), can't be created.

    Example:
        BaseSource()   raises TypeError
    """


class ListSource(BaseSource):
    """A BaseSource over a list of rows: ListSource(rows).read() iterates them.

    Example:
        source = ListSource([{"n": 1}, {"n": 2}])

        next(source.read())  -> {"n": 1}
        source.read_all()    -> [{"n": 1}, {"n": 2}]
    """


class EventsSourceConfig:
    """Make this a frozen Pydantic model with:

    - base_url: str. Must start with "https://" (raise ValueError otherwise)
      and has any trailing slash removed. Use a field_validator.
    - api_key: SecretStr, so it never shows up in repr or logs.
    - page_size: int, default 100, between 1 and 500 inclusive.
    - event_names: list[str], default an empty list.

    Example:
        config = EventsSourceConfig(base_url="https://api.example.com/",
                                    api_key="s3cret", page_size="250")

        config.base_url                    -> "https://api.example.com"
        config.page_size                   -> 250   (converted from the string)
        config.api_key                     -> SecretStr('**********')
        config.api_key.get_secret_value()  -> "s3cret"
        EventsSourceConfig(base_url="http://x", api_key="k")  raises ValidationError
        EventsSourceConfig(base_url="https://x", api_key="k", page_size=501)
                                           raises ValidationError
    """
