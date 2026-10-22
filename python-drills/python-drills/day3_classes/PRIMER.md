# Day 3: Classes and dataclasses

**Why this matters for Manifold.** Your config, a page of API results and your run statistics are all small objects. Today you write one by hand, so you know exactly what a dataclass does for you, and then you let the dataclass do it.

## The parts of a class

```python
class Page:
    source = "events"  # class attribute: one value shared by every Page

    def __init__(self, items: list[dict], next_cursor: str | None = None) -> None:
        self.items = items  # instance attributes: each Page has its own
        self.next_cursor = next_cursor

    def is_empty(self) -> bool:  # a method: a function that receives the object as `self`
        return not self.items
```

`self` is simply the object the method was called on. `page.is_empty()` is shorthand for `Page.is_empty(page)`. `__init__` doesn't create the object; it fills in an object Python has just created.

## Dunder methods: hooks Python calls for you

"Dunder" means double underscore. You never call these yourself; Python calls them when you use ordinary syntax.

| You write | Python calls |
|---|---|
| `repr(page)`, or the REPL displays it | `page.__repr__()` |
| `page == other` | `page.__eq__(other)` |
| `len(page)` | `page.__len__()` |
| `for x in page` | `page.__iter__()` |

Without `__eq__`, two pages with identical contents are *not* equal, because the default asks "is this the very same object?". When you write `__eq__`:

- mypy expects the signature `def __eq__(self, other: object) -> bool`.
- Return `NotImplemented` (not `False`) for types you don't handle, so Python can ask the other object instead. If neither side knows, `==` gives `False`.
- Defining `__eq__` makes objects unhashable (unusable as dict keys or in sets) unless you also define `__hash__`.

In an f-string, `{value!r}` uses the value's repr, so strings get their quotes: `next_cursor='abc'`.

## `@property`: a computed attribute

```python
@property
def is_last(self) -> bool:
    return self.next_cursor is None


page.is_last  # no brackets: reads like an attribute
```

Use a property when the value is cheap and derived from other attributes. If it does real work, such as a network call, make it a normal method so the cost is visible.

## `@classmethod`: another way to build the object

```python
from typing import Self


@classmethod
def from_payload(cls, payload: dict[str, Any]) -> Self:
    return cls(items=list(payload.get("results", [])), next_cursor=payload.get("next"))
```

`cls` is the class itself, so a subclass calling it gets an instance of the subclass. `Self` (3.11+) says "an instance of whichever class this was called on". Reach for a classmethod when there's more than one sensible way to create the object, such as from an API response or from a file.

## Dataclasses (chapter 5, in practice)

```python
from dataclasses import dataclass, field


@dataclass(frozen=True)
class PageDC:
    items: list[dict[str, Any]] = field(default_factory=list)
    next_cursor: str | None = None
```

You get `__init__`, `__repr__` and `__eq__` written for you, and you can still add your own methods, properties and classmethods underneath.

- `frozen=True` blocks `page.next_cursor = "x"` with `FrozenInstanceError`. It does not stop `page.items.append(...)`: it freezes the attributes, not the objects inside them.
- `dataclasses.replace(page, next_cursor=None)` returns a changed copy.
- `field(default_factory=list)` gives each instance its own new list.
- `__post_init__` runs straight after the generated `__init__`. Use it for checks:

```python
def __post_init__(self) -> None:
    if self.pages < 0:
        raise ValueError("pages cannot be negative")
```

## Gotcha

A mutable class attribute, such as `errors = []` written at class level rather than inside `__init__`, is shared by every instance. It's the same trap as yesterday's default argument, which is why dataclasses refuse a plain `[]` default.

## Today's drills

Three classes in `exercises.py`: one by hand, then the same as a dataclass, then a stats object. Aim for 45 to 60 minutes.
