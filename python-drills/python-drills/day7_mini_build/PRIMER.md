# Day 7: Mini-build (timed)

A dress rehearsal for Manifold's build steps 1 to 3. It uses a fake API and plain lists instead of GitHub and Arrow, so everything you need was covered on days 1 to 5.

**Rules:** 90 minutes on a timer. No solutions folder, no AI, no copying from earlier days' solutions. Your own earlier exercise files are fair game, as are the Python and Pydantic docs.

## The spec

The API returns pages shaped like PostHog's own API:

```json
{"results": [{"uuid": "e1", "event": "$pageview", "...": "..."}], "next": "https://api.example.com/events?cursor=2"}
```

The last page has `"next": null`.

Write four things in `exercises.py`:

1. **`MiniConfig`**, a frozen Pydantic model:
    - `base_url`: must start with `https://`; any trailing slash is removed.
    - `batch_size`: default 100, at least 1.
    - `max_pages`: `None` by default; if set, at least 1.
2. **`SourceStats`**, a dataclass with `pages` and `rows`, both starting at 0.
3. **`flatten(event)`**, the same as day 1's `flatten_event`.
4. **`EventsSource(config, fetcher)`**:
    - `stats` attribute holding a `SourceStats`.
    - `name` property: `"events:"` followed by the base URL.
    - `read()`: fetch `{base_url}/events`, follow each page's `next` URL until it's `None` or `max_pages` pages have been fetched, flatten every event, and yield lists of `batch_size` rows, then any remainder.
    - Lazy: fetch a page only when more rows are needed.
    - `stats.pages` counts pages fetched; `stats.rows` counts rows yielded so far.

`test_day7.py` is the acceptance test. All green plus a clean `uv run mypy day7_mini_build` is done.

## A suggested order

1. `MiniConfig` and `SourceStats`, and get their tests passing. (About 15 minutes.)
2. `flatten`. (5 minutes; you've done it before.)
3. `EventsSource`, using two generators: one that yields pages, one that re-batches rows. (The rest.)

## Afterwards

Write down what slowed you down. That list is what to revise before the real build, and "what a 90-minute dress rehearsal taught me" is a ready-made post.

Then open `WEEK2_BUILD.md` in the folder above. The real thing is this, with three swaps: `httpx.Client` instead of a fake fetcher, GitHub's `Link` header instead of a `next` field, and Arrow record batches instead of lists of dicts.
