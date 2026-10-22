# Python drills

Seven sessions of practice to get you from "rusty" to ready for Manifold's build steps 2 and 3. Each has a short primer, a file of exercises with a worked example in every one, and tests that tell you when you've got it right. Days 1 and 2 also have a walkthrough that solves a similar problem for each exercise before you try yours. Everything is set in a world of PostHog-style product events, so it stays close to the real build.

## The week

| Day | Folder | Topic | Feeds into |
|---|---|---|---|
| 1 | `day1_data_structures` | lists, dicts, sets, tuples, comprehensions, `Counter`, `defaultdict` | turning nested JSON into rows |
| 2 | `day2_functions` | lambda, key functions, closures, keyword-only arguments, `match` | sorting, mapping, building URLs |
| 3 | `day3_classes` | classes, dunder methods, `@property`, `@classmethod`, dataclasses | config and stats objects |
| 4 | `day4_interfaces` | composition, Protocol versus abstract base class, custom exceptions, Pydantic | build steps 1 and 2 |
| 5 | `day5_iteration` | generators, laziness, itertools, context managers | build step 3 |
| 6 | `day6_dsa` | hash lookups, heaps, two pointers, sessions, binary search | interviews |
| 7 | `day7_mini_build` | a timed 90-minute dress rehearsal | the whole build |

Take each day at the pace it needs. Some will take one sitting and some will take two or three, and that's fine: getting them right matters more than getting them done this week. Day 7 is the exception: it's a timed 90 minutes.

## Setup, once

Unzip this folder next to `manifold` (not inside it), then:

```powershell
cd C:\dev\python-drills
uv sync
uv run pytest day1_data_structures
```

Every test fails at first. That's correct: there's nothing written yet.

## Each day

1. Read the day's `PRIMER.md` (about 10 minutes). Try the snippets in `uv run python`.
2. If the day has a `WALKTHROUGH.md`, read each exercise's section just before you do that exercise.
3. Open `exercises.py` and replace each `raise NotImplementedError` with your own code. Every docstring has an example of what goes in and what should come out; the test file at the bottom of each folder has more.
4. Run the tests until they're green, then mypy until it's clean:

    ```powershell
    uv run pytest day1_data_structures
    uv run mypy day1_data_structures
    ```

5. Tick the day off in your tracker.

## Rules

- **Turn off AI autocomplete** (Copilot and the like) while you drill. The point is recall, and autocomplete does the recalling for you. The Python docs are fine.
- **Stuck for more than 10 minutes on one drill?** Read only that function in `solutions/`, close it, and write it again from a blank function. Tomorrow, do that drill again before starting the new day.
- **One test at a time** if a day feels big: `uv run pytest day1_data_structures -k chunk`.
- **Read the failure message before the code.** Most of the learning is in working out why a test failed.
- Paste any finished `exercises.py` to Claude for a review if you want a second pair of eyes.

## Solutions

`solutions/` has a worked answer for every day. They pass every test, plus mypy in strict mode and ruff. Treat them as an answer key, not a textbook: yours can be different and still be right.

## After the week

Open `WEEK2_BUILD.md`. It's the Manifold build guide for the Source interface and the GitHub issues source, waiting for you.
