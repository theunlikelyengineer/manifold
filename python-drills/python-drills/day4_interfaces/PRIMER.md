# Day 4: Composition, interfaces and Pydantic

**Why this matters for Manifold.** This is build steps 1 and 2 in miniature: an interface every source meets, a client that's handed its fetcher rather than creating one, and a config that checks what comes in.

## Composition over inheritance

Inheritance says "a `ListSource` **is a** `BaseSource`". Composition says "an `EventsClient` **has a** fetcher". When one object uses another, prefer composition:

```python
class EventsClient:
    def __init__(self, fetcher: Fetcher, base_url: str) -> None:
        self._fetcher = fetcher  # handed in, not created here
```

Handing the object in is called **dependency injection**. It's what makes testing easy: a test passes in a fake fetcher that returns canned responses and records every call. No network and no mocking library.

The leading underscore in `self._fetcher` is a convention meaning "internal; don't use this from outside". Python doesn't enforce it.

## Two ways to define an interface

**Abstract base class (ABC).** Subclasses must inherit from it and implement its abstract methods. It's checked at **runtime**: creating an incomplete subclass raises `TypeError`. It can also share code with every subclass:

```python
from abc import ABC, abstractmethod


class BaseSource(ABC):
    @abstractmethod
    def read(self) -> Iterator[dict[str, Any]]: ...

    def read_all(self) -> list[dict[str, Any]]:  # every subclass gets this
        return list(self.read())
```

**Protocol.** Any class with matching methods counts, with no inheritance. It's checked by **mypy**, before anything runs:

```python
from typing import Protocol


class Fetcher(Protocol):
    def get_json(self, url: str) -> dict[str, Any]: ...
```

`FakeFetcher` never mentions `Fetcher`, yet `fetcher: Fetcher = FakeFetcher({})` type-checks, because it has a `get_json` with the right signature. This is sometimes called duck typing with a type checker: if it has the right methods, it fits.

| | Abstract base class | Protocol |
|---|---|---|
| Must inherit from it | yes | no |
| A missing method is caught | when the object is created | when mypy runs |
| Can share code | yes | no |
| Works with classes you didn't write | no | yes |

Manifold uses a Protocol for `Source`, because sources share no code and test fakes stay trivial. mypy also catches an incomplete ABC subclass ("Cannot instantiate abstract class"), which is why the tests use `cast(Any, ...)` to get past it and check the runtime behaviour.

## Custom exceptions

```python
class NotFound(Exception):
    def __init__(self, url: str) -> None:
        super().__init__(f"no response for {url}")  # sets what str(exc) shows
        self.url = url  # lets callers react without parsing text
```

When you catch one error and raise another:

- `raise NotFound(url) from exc` keeps the original error as the cause, shown in the traceback.
- `raise NotFound(url) from None` hides it. Use that when the original adds nothing, like a `KeyError` from a dict lookup.

`super()` calls the parent class's version of a method. Here it lets `Exception` set up the message.

## Pydantic: checking data at the boundary

```python
from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator


class EventsSourceConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    base_url: str
    api_key: SecretStr
    page_size: int = Field(default=100, ge=1, le=500)
    event_names: list[str] = Field(default_factory=list)

    @field_validator("base_url")
    @classmethod
    def _https_only(cls, value: str) -> str:
        if not value.startswith("https://"):
            raise ValueError("base_url must start with https://")
        return value.rstrip("/")  # a validator can clean the value as well as check it
```

- Values are checked **and converted**: `"250"` becomes `250`; `"lots"` and `600` fail.
- Problems raise `pydantic.ValidationError` (a kind of `ValueError`), listing every bad field at once.
- `SecretStr` shows as `**********` in repr and logs. `.get_secret_value()` gives you the real value.
- With `frozen=True`, assigning to a field raises `ValidationError`.
- `EventsSourceConfig.model_validate(raw_dict)` builds one from a plain dict, as you would after reading YAML or environment variables.
- A `field_validator` is a classmethod that receives the value and returns the value to keep. Raising `ValueError` inside it turns into a `ValidationError` with your message.

## Today's drills

Six classes in `exercises.py`. Aim for about an hour. When you're done, compare `EventsSourceConfig` with build step 2: it's nearly the same shape.
