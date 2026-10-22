# Day 5: Generators, laziness and context managers

**Why this matters for Manifold.** A source that reads 300 pages mustn't hold 300 pages in memory. Generators produce one item at a time, only when asked, so memory stays flat however big the data gets. Build step 3 is two generators stacked together, and today's drills are that, in miniature.

## Iterables, iterators and generators

- An **iterable** is anything you can loop over: a list, a dict, a file.
- An **iterator** hands out items one at a time through `next()`, and is used up once it's finished.
- A **generator** is the easiest way to write an iterator: a function with `yield` in it.

```python
def numbers():
    print("starting")
    yield 1
    yield 2


gen = numbers()  # nothing printed: the body hasn't started
next(gen)  # prints "starting", returns 1
next(gen)  # returns 2
next(gen)  # raises StopIteration: it's finished
```

Calling a generator function runs none of its body; it just gives you the generator. Each `next()` runs the body up to the next `yield`, hands out that value, and pauses, keeping all its local variables. A `for` loop calls `next()` for you and stops quietly at `StopIteration`. A `return` inside a generator ends it.

## The laziness gotcha

Because nothing runs until the first `next()`, a check at the top of a generator doesn't fire when you call it:

```python
def rebatch(pages, size):
    if size < 1:
        raise ValueError(...)  # NOT raised by rebatch(pages, 0) ...
    ...
    yield batch  # ... only when someone first asks for a batch
```

That can make errors appear far away from the mistake. To fail immediately, do the check in a normal function and return a generator from a helper:

```python
def rebatch(pages, size):
    if size < 1:
        raise ValueError("size must be at least 1")
    return _rebatch(pages, size)  # _rebatch is the generator, with the yields
```

## Stacking generators into a pipeline

```python
pages = paginate(fetch)  # fetches one page at a time
batches = rebatch(pages, 1000)  # pulls another page only when it needs more rows
for batch in batches:
    write(batch)
```

Each stage pulls from the one before it, only as far as needed. If the loop stops early, the later pages are never fetched. That's the whole design of your Source's `read()`.

Two related bits of syntax:

- A **generator expression** is a comprehension in round brackets, and it's lazy: `sum(len(page) for page in pages)`.
- `yield from other` yields everything `other` produces.

## itertools: the ones you'll actually use

```python
from itertools import batched, chain, count, islice

list(islice(count(), 5))  # [0, 1, 2, 3, 4]: take 5 from an endless iterator
list(chain.from_iterable([[1, 2], [3]]))  # [1, 2, 3]: flatten one level
list(batched([1, 2, 3, 4, 5], 2))  # [(1, 2), (3, 4), (5,)]: 3.12+, gives tuples
```

## Exceptions

```python
try:
    record = json.loads(line)
except json.JSONDecodeError as exc:
    raise BadRecord(line_no) from exc  # keep the original as the cause
finally:
    ...  # runs whether or not anything failed
```

Catch the narrowest exception you can. A bare `except Exception:` hides real bugs. `enumerate(lines, start=1)` gives you line numbers counting from 1 as you loop.

## Context managers

`with` guarantees clean-up, even when something goes wrong inside the block:

```python
with httpx.Client() as client:  # opens connections
    ...
# connections are closed here, error or not
```

The easiest way to write your own is a generator with exactly one `yield`:

```python
import time
from collections.abc import Iterator
from contextlib import contextmanager


@contextmanager
def timed(stats: dict[str, float]) -> Iterator[None]:
    start = time.perf_counter()
    try:
        yield  # the body of the with-block runs here
    finally:
        stats["elapsed"] = time.perf_counter() - start
```

Without the `try`/`finally`, an error inside the block would skip the timing. `time.perf_counter()` is the right clock for measuring durations; `time.time()` can jump if the system clock changes.

## Today's drills

Six functions and one exception class. Aim for about an hour. The laziness tests are the important ones: if they fail, your code is reading everything up front.
