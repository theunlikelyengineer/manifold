# Manifold week 2 build: a Source interface and a GitHub issues source

Come back to this once the drills are done. Day 4 is steps 1 and 2 in miniature, day 5 is step 3, and day 7 is a dress rehearsal for all of it. The real build swaps in three things: `httpx.Client` instead of a fake fetcher, GitHub's `Link` header instead of a `next` field, and Arrow record batches instead of lists of dicts.

## The data source

GitHub's issues API, pointed at `PostHog/posthog`:

- It paginates for real: each response carries the next page's URL in a `Link` header.
- It returns nested JSON, and pull requests come back mixed in with issues, which is a real data quirk to handle.
- Its `since` parameter gives you incremental extraction almost for free later on.
- "I ingested PostHog's own issue tracker" is a decent post.

Without a token you get 60 requests an hour; with one you get 5,000. Create a fine-grained token with read-only access to public repositories.

**Read first:** Cosmic Python chapter 2, the repository pattern. It's the same idea as your Source: hide where the data comes from behind an interface. Chapter 3 is short and explains why the HTTP client is passed in rather than created inside.

## Step 0: dependencies and files

In the `manifold` folder:

```powershell
uv add httpx pydantic pyarrow
uv add --dev pyarrow-stubs
```

Create:

```
src/manifold/sources/__init__.py
src/manifold/sources/base.py
src/manifold/sources/github_issues.py
tests/test_github_issues.py
```

## Step 1: the interface (`base.py`)

```python
from collections.abc import Iterator
from typing import Protocol

import pyarrow as pa


class Source(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def schema(self) -> pa.Schema: ...

    def read(self) -> Iterator[pa.RecordBatch]: ...
```

A Protocol rather than an abstract base class: sources don't inherit anything, mypy checks each one has the right shape, and test fakes stay trivial. `schema` is declared up front on purpose. It's your data contract, and the schema-drift work later builds on it.

## Step 2: the config

A frozen Pydantic model with:

- `owner` and `repo`
- `state`: `"open"`, `"closed"` or `"all"` (a `Literal`)
- `per_page`: capped at 100, GitHub's maximum
- `batch_size`
- an optional `max_pages`, to keep development runs small
- `token` as a `SecretStr`, so it never appears in printouts or logs

**Checkpoint:** `per_page=500` raises a validation error.

## Step 3: the source

Two generators:

- `_pages()` makes a request and yields one page of JSON, then follows `response.links["next"]["url"]` until there's no next link.
- `read()` turns each item into a row and yields a `pa.RecordBatch` every `batch_size` rows, then whatever is left at the end.

Memory never grows past one batch, however big the repository.

Pass the `httpx.Client` in through the constructor rather than creating it inside. That's what makes step 4 possible.

For each item, keep:

- `id` and `number`
- `title` and `state`
- `author`, from `user.login`
- `labels`, as a list of label names
- `is_pull_request`, true when the item has a `pull_request` key
- `created_at` and `updated_at`

## Step 4: tests, with no network

httpx ships with a fake transport:

```python
def handler(request: httpx.Request) -> httpx.Response:
    page = int(request.url.params.get("page", "1"))
    headers: dict[str, str] = {}
    if page < len(pages):
        headers["Link"] = f'<https://api.github.com/repos/o/r/issues?page={page + 1}>; rel="next"'
    return httpx.Response(200, headers=headers, json=pages[page - 1])


client = httpx.Client(base_url="https://api.github.com", transport=httpx.MockTransport(handler))
```

Test:

- **Batch sizes:** two pages of five items with `batch_size=2` give batches of 2, 2 and 1 rows.
- **Schema:** every batch's schema equals `SCHEMA`.
- **Stopping:** it stops when there's no `next` link.
- **Pull requests:** a pull request is flagged.
- **The Protocol:** assigning your source to a variable typed `Source` passes mypy.
- **Config:** the validation from step 2.

## Step 5: one real run

```powershell
$env:GITHUB_TOKEN = "github_pat_..."
```

Build the client with `Authorization: Bearer <token>` and `Accept: application/vnd.github+json` headers. With `max_pages=3` you should get 300 rows. Combine them with `pa.Table.from_batches(...)` and look at them. Never commit the token.

## Three snags, so you don't lose an evening to them

1. **Timestamps.** GitHub sends them as text, and Arrow won't put text into a timestamp column (`ArrowTypeError: object of type <class 'str'> cannot be converted to int`). Convert them with `datetime.fromisoformat`, which accepts the trailing `Z` on Python 3.11 and later.
2. **mypy and the schema.** A list of `pa.field(...)` calls with different types comes out as `list[object]`, and mypy rejects `pa.schema(...)`. Annotate the list as `"list[pa.Field[Any]]"`, in quotes. The type stubs say `Field` takes a type parameter but the real class doesn't, so without quotes the module crashes on import with `TypeError: type 'pyarrow.lib.Field' is not subscriptable`.
3. **Repeated parameters.** The `next` link already includes your query string, so only send `params` on the first request.

## Done when

- the new tests pass offline
- mypy strict is clean
- the real run returns 300 rows
- it's committed, with the pre-commit hooks passing

Then write the pattern page (the adapter interface, and chunked processing with generators) while it's fresh, and paste your code to Claude for a review.
