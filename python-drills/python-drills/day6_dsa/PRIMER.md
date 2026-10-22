# Day 6: Data structures and algorithms for data engineers

**Why this matters.** PostHog's interviews don't use puzzles, but plenty of other companies' do. More usefully, the same ideas decide whether a pipeline step takes seconds or hours. Today's drills are the patterns that come up most often for data engineers.

## How long things take

"O(n)" means the time grows in step with the size of the input; "O(1)" means it doesn't grow at all; "O(n²)" means doubling the input quadruples the time.

| Operation | Cost |
|---|---|
| `x in some_list` | O(n): checks every item |
| `x in some_set`, `some_dict[key]` | O(1) on average |
| `list.append(x)` | O(1) |
| `list.insert(0, x)`, `list.pop(0)` | O(n): shifts everything along. Use `collections.deque` |
| `sorted(items)` | O(n log n) |
| `heapq.heappush`, `heapq.heappop` | O(log n) |
| `bisect.bisect_left` on a sorted list | O(log n) |

The single most common fix, in interviews and in real pipelines: replace a loop inside a loop with a set or dict lookup. That turns O(n²) into O(n).

## The patterns

**Hash lookup.** "Have I seen this before?" and "is there a partner for this?" are set questions. For a pair that sums to a target, remember each number you've passed; for each new number, check whether `target - n` is already in the set. One pass.

**Count, then rank.** `Counter` counts in one pass. For the top k of n items, sorting everything costs O(n log n). `heapq.nsmallest(k, items, key=...)` (or `nlargest`) only ever keeps k items, which matters when n is huge and k is small. A key of `(-count, name)` puts big counts first and breaks ties A to Z.

**Two pointers.** To merge two sorted lists, keep an index into each and always take the smaller of the two current items. One pass, O(n + m). It's the idea behind a sort-merge join, and how `heapq.merge` combines already-sorted files without loading them all.

**Sessions (gaps and islands).** Walk the sorted timestamps and start a new group whenever the gap since the previous one is bigger than a threshold. It's the Python version of the gaps-and-islands SQL you did in M1, and the same idea analytics tools use for sessions: a new session after 30 minutes (1,800 seconds) of inactivity.

**Binary search.** On sorted data, `bisect_left(xs, v)` finds where `v` would be inserted, in O(log n). So the count of values in the half-open range `[start, end)` is `bisect_left(xs, end) - bisect_left(xs, start)`. It's how you'd find which files or partitions cover a time range without scanning them all.

## How to practise

Before you run the tests for each drill, say its time complexity out loud. If it's O(n²), look for the set or dict that removes the inner loop. One test times `has_pair_with_sum` on a few thousand numbers and fails if it's slow.

## Today's drills

Six functions in `exercises.py`. Aim for 45 to 60 minutes.
