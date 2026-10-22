# Day 2: Functions, lambda and pattern matching

**Why this matters for Manifold.** Sorting, filtering and transforming rows mostly means handing small functions to other functions. And `match` reads the shape of JSON more clearly than a stack of `if` statements.

## Functions are values

A function is an object like any other. You can store it in a dict, pass it in, or return it:

```python
def shout(s: str) -> str:
    return s.upper()


mappers = {"event": shout, "plan": lambda p: p or "free"}
mappers["event"]("$pageview")  # '$PAGEVIEW'
```

A `lambda` is a one-line function without a name. `lambda p: p or "free"` does the same as `def f(p): return p or "free"`. Use it for tiny throwaway functions, mostly as a `key=`. If it needs a name or a second line, write a `def`.

## Key functions: `sorted`, `min`, `max`

```python
sorted(events, key=lambda e: e["timestamp"])  # oldest first
sorted(events, key=lambda e: e["timestamp"], reverse=True)  # newest first
max(events, key=lambda e: e["timestamp"])  # the newest one
min(users, key=lambda u: (-counts[u], u))  # most events, then A to Z
```

A tuple key sorts by its first item, then by the second where the first ties. To reverse just one part, negate it. That works for numbers but not strings.

For strings, use the fact that Python's sort is **stable**: items that compare equal keep the order they already had. So sort by the tiebreaker first, then by the main key:

```python
by_uuid = sorted(events, key=lambda e: e["uuid"])
newest_first = sorted(by_uuid, key=lambda e: e["timestamp"], reverse=True)
```

`sorted()` returns a new list. `list.sort()` changes the list in place and returns `None`, which is a common source of `None` bugs.

## Closures: functions that make functions

```python
from collections.abc import Callable


def make_min_length(n: int) -> Callable[[str], bool]:
    def check(s: str) -> bool:
        return len(s) >= n  # still remembers n after make_min_length returns

    return check


at_least_3 = make_min_length(3)
at_least_3("abc")  # True
```

`Callable[[str], bool]` reads "a function that takes a str and returns a bool".

## Arguments

```python
def f(a, b=2, *args, c, d=4, **kwargs): ...
```

- `*args` gathers extra positional arguments into a tuple; `**kwargs` gathers extra keyword arguments into a dict.
- Anything after `*` or `*args` is **keyword-only**: callers must write `page=2`, not just `2`. Use it for options, so `build_url(base, path, 2, 50)` can't quietly swap page and page size. A bare `*` on its own does this without collecting anything.

**The mutable default trap.** Default values are created once, when Python reads the `def`, not each time the function is called. A default list is therefore one list, shared by every call that relies on it. The fix:

```python
def f(items: list[str] | None = None) -> list[str]:
    items = [] if items is None else items
    ...
```

Today's `append_label` has this bug on purpose. Run the tests before you touch it and read the failure.

## Pattern matching (3.10+)

`match` checks a value against shapes, top to bottom, and runs the first case that fits. Dict patterns only check the keys you list, so extra keys are fine:

```python
match event:
    case {"event": "$pageview", "properties": {"$current_url": str() as url}}:
        return f"viewed {url}"
    case {"event": str() as name} if name.startswith("$"):
        return "system event"
    case _:
        return "unknown"
```

- `str() as url` means "this must be a string; call it `url`".
- `if ...` after a pattern is a guard: the case only matches when it's true.
- `case _:` matches anything.
- Put specific cases before general ones, or the general one wins first.

## Newer syntax

- `str | None` instead of `Optional[str]` (3.10+).
- `Callable` now comes from `collections.abc`, not `typing`.

## A mypy note you'll probably hit

Anything pulled out of a `dict[str, Any]` is typed `Any`. So `Counter(e["distinct_id"] for e in events)` is a `Counter[Any]`, and returning `min(counts, ...)` from a function declared `-> str` makes strict mypy say "Returning Any from function declared to return str". Tell it what you know: `counts: Counter[str] = Counter(...)`.

## Today's drills

Seven functions in `exercises.py`. Aim for 45 to 60 minutes.
