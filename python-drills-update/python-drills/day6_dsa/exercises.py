"""Day 6: data structures and algorithms for data engineers.

Before you run the tests for each one, say its time complexity out loud.
Replace each `raise NotImplementedError`, then run:

    uv run pytest day6_dsa
    uv run mypy day6_dsa
"""


def has_pair_with_sum(nums: list[int], target: int) -> bool:
    """True if two different positions in `nums` add up to `target`.

    One pass, no nested loop.

    Example:
        has_pair_with_sum([3, 9, 4, 1], 13)  -> True    (9 + 4)
        has_pair_with_sum([3, 9, 4, 1], 6)   -> False
    """
    raise NotImplementedError


def first_duplicate(ids: list[str]) -> str | None:
    """The first id to appear for a second time, or None if all are unique.

    Example:
        first_duplicate(["a", "b", "b", "a"])  -> "b"    (b repeats before a does)
        first_duplicate(["a", "b"])            -> None
    """
    raise NotImplementedError


def top_k(names: list[str], k: int) -> list[tuple[str, int]]:
    """The k most common names with their counts, most common first.

    Ties go A to Z. Try heapq.nsmallest or nlargest rather than sorting everything.

    Example:
        top_k(["b", "a", "b", "c", "a", "b"], 2)  -> [("b", 3), ("a", 2)]
        top_k(["c", "b", "a", "c", "b", "a"], 2)  -> [("a", 2), ("b", 2)]   (a tie)
    """
    raise NotImplementedError


def merge_sorted(a: list[int], b: list[int]) -> list[int]:
    """Merge two sorted lists into one sorted list in a single pass.

    Don't use sorted(), list.sort() or heapq.merge. Walk both lists with two indexes.

    Example:
        merge_sorted([1, 4, 9], [2, 3, 10])  -> [1, 2, 3, 4, 9, 10]
    """
    raise NotImplementedError


def sessionize(timestamps: list[int], gap: int) -> list[list[int]]:
    """Split one user's sorted timestamps (in seconds) into sessions.

    A new session starts when more than `gap` seconds have passed since the
    previous timestamp. Exactly `gap` seconds stays in the same session.

    Example:
        sessionize([0, 100, 2000, 2100, 5000], 1800)  -> [[0, 100], [2000, 2100], [5000]]
        (2000 - 100 = 1900 seconds, more than 1800, so a new session starts at 2000)
    """
    raise NotImplementedError


def count_in_range(sorted_ts: list[int], start: int, end: int) -> int:
    """How many values t in the sorted list satisfy start <= t < end.

    Use bisect, not a loop: O(log n).

    Example:
        count_in_range([1, 2, 2, 3, 5, 8], 2, 5)  -> 3    (the 2, 2 and 3)
    """
    raise NotImplementedError
