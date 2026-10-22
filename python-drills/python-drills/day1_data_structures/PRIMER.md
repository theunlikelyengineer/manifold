# Day 1: Data structures and comprehensions

**Why this matters for Manifold.** Every source does the same three things: it reads nested JSON, reshapes it into flat rows, and counts or dedupes along the way. That's lists, dicts and sets, used well.

## Pick the right container

| Type | Use it for | Is `x in it` fast? | Worth knowing |
|---|---|---|---|
| list | ordered items, duplicates allowed | no, it checks every item | the default |
| tuple | a fixed record you won't change | no | can't be changed; unpacks neatly |
| dict | looking things up by key | yes | keeps insertion order (Python 3.7+) |
| set | unique items, "have I seen this?" | yes | no order, no duplicates |

Rule of thumb: if you write `if x in some_list` inside a loop, you probably want a set.

## Reading nested JSON safely

```python
event["properties"]["plan"]  # KeyError if either key is missing
event.get("properties", {}).get("plan")  # breaks when properties is None
(event.get("properties") or {}).get("plan")  # copes with missing and None
```

APIs send `null` about as often as they leave a key out. `or {}` covers both, because `None or {}` gives `{}`.

## Comprehensions

```python
[e["uuid"] for e in events]  # list
{e["distinct_id"] for e in events}  # set
{e["uuid"]: e for e in events}  # dict
[e for e in events if e["event"] == "$pageview"]  # with a filter
```

Read them as "give me *this*, for each `e` in `events`, if *that*". If one needs two `if`s or a nested loop before it reads clearly, write a normal `for` loop instead. Clarity beats cleverness.

## Two tools from `collections`

```python
from collections import Counter, defaultdict

Counter(e["event"] for e in events)  # Counter({'$pageview': 3, 'signed_up': 1})

groups: defaultdict[str, list[dict]] = defaultdict(list)
for e in events:
    groups[e["distinct_id"]].append(e)  # no "if key not in groups" needed
```

A `Counter` is a dict, so it compares equal to a plain dict with the same counts. `defaultdict(list)` creates an empty list the first time you touch a key; `defaultdict(set)` creates an empty set.

## Slicing and unpacking

```python
items[0:2]  # first two
items[2:]  # everything after the first two
first, *rest = items  # unpacking
merged = defaults | overrides  # dict merge, Python 3.9+
```

Chunking is slicing in a loop: `range(0, len(items), size)` gives the starting index of each chunk.

## Newer syntax you'll meet

- **Built-in generics in type hints** (3.9+): `list[str]`, `dict[str, int]`. No need for `typing.List`.
- **Generic functions** (3.12+): `def chunk[T](items: list[T], size: int) -> list[list[T]]`. `T` means "whatever type the list holds", so mypy knows `chunk([1, 2], 1)` returns `list[list[int]]`.
- **Debug f-strings** (3.8+): `f"{len(rows)=}"` prints `len(rows)=5`.

## Gotchas

- Adding or removing dict keys while looping over the dict raises `RuntimeError`. Loop over `list(d)` instead, or build a new dict.
- Assigning to a key that already exists keeps its original position. `dedupe_latest` relies on that.
- ISO timestamps such as `2026-10-01T09:00:00Z` sort correctly as plain strings only when they all share the same format and time zone. They do here. In the real build you'll parse them into datetimes.

## Today's drills

Six functions in `exercises.py`. Aim for 45 minutes.
