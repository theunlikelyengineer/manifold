"""Day 6: data structures and algorithms for data engineers.

Before you run the tests for each one, say its time complexity out loud.
Replace each `raise NotImplementedError`, then run:

    uv run pytest day6_dsa
    uv run mypy day6_dsa
"""


def has_pair_with_sum(nums: list[int], target: int) -> bool:
    """True if two different positions in `nums` add up to `target`.

    One pass, no nested loop.
    """
    raise NotImplementedError


def first_duplicate(ids: list[str]) -> str | None:
    """The first id to appear for a second time, or None if all are unique.

    first_duplicate(["a", "b", "b", "a"]) == "b"
    """
    raise NotImplementedError


def top_k(names: list[str], k: int) -> list[tuple[str, int]]:
    """The k most common names with their counts, most common first.

    Ties go A to Z. Try heapq.nsmallest or nlargest rather than sorting everything.
    top_k(["b", "a", "b", "c", "a", "b"], 2) == [("b", 3), ("a", 2)]
    """
    raise NotImplementedError


def merge_sorted(a: list[int], b: list[int]) -> list[int]:
    """Merge two sorted lists into one sorted list in a single pass.

    Don't use sorted(), list.sort() or heapq.merge. Walk both lists with two indexes.
    """
    raise NotImplementedError


def sessionize(timestamps: list[int], gap: int) -> list[list[int]]:
    """Split one user's sorted timestamps (in seconds) into sessions.

    A new session starts when more than `gap` seconds have passed since the
    previous timestamp. Exactly `gap` seconds stays in the same session.

    sessionize([0, 100, 2000, 2100, 5000], 1800) == [[0, 100], [2000, 2100], [5000]]
    """
    raise NotImplementedError


def count_in_range(sorted_ts: list[int], start: int, end: int) -> int:
    """How many values t in the sorted list satisfy start <= t < end.

    Use bisect, not a loop: O(log n).
    """
    raise NotImplementedError
