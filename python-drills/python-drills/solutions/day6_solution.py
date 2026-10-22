"""Day 6 solutions. Read one function at a time, only when you're stuck."""

import heapq
from bisect import bisect_left
from collections import Counter


def has_pair_with_sum(nums: list[int], target: int) -> bool:
    seen: set[int] = set()
    for n in nums:
        if target - n in seen:
            return True
        seen.add(n)
    return False


def first_duplicate(ids: list[str]) -> str | None:
    seen: set[str] = set()
    for item in ids:
        if item in seen:
            return item
        seen.add(item)
    return None


def top_k(names: list[str], k: int) -> list[tuple[str, int]]:
    counts = Counter(names)
    # nsmallest keeps only k items at a time; the key puts big counts first.
    return heapq.nsmallest(k, counts.items(), key=lambda kv: (-kv[1], kv[0]))


def merge_sorted(a: list[int], b: list[int]) -> list[int]:
    i = j = 0
    merged: list[int] = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            merged.append(a[i])
            i += 1
        else:
            merged.append(b[j])
            j += 1
    merged.extend(a[i:])
    merged.extend(b[j:])
    return merged


def sessionize(timestamps: list[int], gap: int) -> list[list[int]]:
    sessions: list[list[int]] = []
    for ts in timestamps:
        if sessions and ts - sessions[-1][-1] <= gap:
            sessions[-1].append(ts)
        else:
            sessions.append([ts])
    return sessions


def count_in_range(sorted_ts: list[int], start: int, end: int) -> int:
    return bisect_left(sorted_ts, end) - bisect_left(sorted_ts, start)
