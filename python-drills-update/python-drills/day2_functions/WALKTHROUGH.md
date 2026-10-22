# Day 2 walkthrough

Same format as day 1: each section explains the task, solves a café problem with the same moves, then hands over to you. Paste the orders into `uv run python` first:

```python
orders = [
    {
        "order_id": 1,
        "drink": "latte",
        "customer": "ana",
        "time": "09:00",
        "extras": {"milk": "oat", "size": "large"},
    },
    {
        "order_id": 2,
        "drink": "mocha",
        "customer": "ben",
        "time": "09:05",
        "extras": {"size": "small"},
    },
    {"order_id": 3, "drink": "latte", "customer": "ben", "time": "09:10"},
    {"order_id": 4, "drink": "latte", "customer": "ana", "time": "09:20", "extras": None},
]
```

## 1. `sort_events`: two sort rules

**Task.** Newest timestamp first; when two have the same timestamp, uuid A to Z. Don't change the list passed in.

**The tool: `sorted` with a `key`.** `sorted()` returns a new sorted list and leaves the original alone. `key=` is a function that tells it what to sort by:

```python
sorted(orders, key=lambda order: order["time"])  # oldest first
sorted(orders, key=lambda order: order["time"], reverse=True)  # newest first
```

`lambda order: order["time"]` is a tiny function with no name: "given an order, give back its time". It does the same as this:

```python
def get_time(order):
    return order["time"]


sorted(orders, key=get_time)  # pass the function itself: no brackets after get_time
```

**Solved for the café: customers A to Z, and each customer's orders newest first.**

That's two sort rules pointing in different directions. The trick is that Python's sort is *stable*: items that tie keep the order they already had. So sort by the **tiebreaker first**, then by the **main rule**:

```python
def by_customer_then_newest(orders):
    newest_first = sorted(orders, key=lambda order: order["time"], reverse=True)
    return sorted(newest_first, key=lambda order: order["customer"])


[o["order_id"] for o in by_customer_then_newest(orders)]  # [4, 1, 3, 2]
```

The second sort puts ana before ben. Ana's two orders tie on that sort, so they keep the newest-first order the first sort gave them: 4, then 1.

**Your turn.** Your main rule is timestamp, newest first, and your tiebreaker is uuid, A to Z. Which do you sort by first? `reverse=True` keeps ties in their existing order too.

## 2. `most_active_user`: the most, with a tiebreak

**Task.** The user with the most events; on a tie, the name first A to Z. An empty list raises `ValueError`.

**Solved for the café: the best customer (most orders), ties A to Z.**

The loop way: count, then walk the names A to Z keeping the best so far. Because you walk A to Z and only replace on a *strictly* bigger count, a tie goes to the earlier name:

```python
def best_customer(orders):
    counts = {}
    for order in orders:
        customer = order["customer"]
        counts[customer] = counts.get(customer, 0) + 1

    if not counts:
        raise ValueError("no orders")

    best = None
    for customer in sorted(counts):  # sorted() of a dict gives its keys, A to Z
        if best is None or counts[customer] > counts[best]:
            best = customer
    return best


best_customer(orders)  # 'ana'   (ana and ben both have 2; ana is first A to Z)
```

The Python way uses `Counter` for the counts, and `min` with a key that applies both rules at once:

```python
from collections import Counter


def best_customer(orders):
    counts = Counter(order["customer"] for order in orders)
    return min(counts, key=lambda customer: (-counts[customer], customer))
```

How that key works:

- A tuple key compares the first item, and only looks at the second when the first ties.
- `min` picks the smallest. Making the count negative turns "most" into "smallest", because -3 is smaller than -2.
- The name as the second item breaks ties A to Z, because `"ana"` is smaller than `"ben"`.
- `min()` of an empty Counter raises `ValueError` by itself.

In your typed version, write `counts: Counter[str] = Counter(...)`, or strict mypy complains that you're returning `Any`.

**Your turn.** Count `"distinct_id"`.

## 3. `make_filter`: a function that builds functions

**Task.** `make_filter(event="$pageview", plan="pro")` returns a function. That function takes a row and returns True if every one of those key and value pairs matches.

**Solved for the café, starting with one rule: a drink filter.**

A function can define another function inside itself and return it. The inner function remembers the variables around it, even after the outer one has finished. That's called a *closure*:

```python
def make_drink_filter(drink):
    def check(order):
        return order.get("drink") == drink  # `drink` is remembered from outside

    return check  # return the function itself; don't call it


is_latte = make_drink_filter("latte")
is_latte(orders[0])  # True
[o["order_id"] for o in orders if is_latte(o)]  # [1, 3, 4]
```

**Then any number of rules.** `**criteria` collects keyword arguments into a dict, so `make_order_filter(drink="latte", customer="ana")` gives `criteria = {"drink": "latte", "customer": "ana"}`. The inner function checks every pair:

```python
def make_order_filter(**criteria):
    def check(order):
        for key, value in criteria.items():
            if order.get(key) != value:
                return False  # one mismatch is enough
        return True  # nothing failed (also true when there are no rules)

    return check


anas_lattes = make_order_filter(drink="latte", customer="ana")
[o["order_id"] for o in orders if anas_lattes(o)]  # [1, 4]
```

The Python way replaces the inner loop with `all(...)`, which is True when every item is true, and True when there's nothing to check:

```python
def check(order):
    return all(order.get(key) == value for key, value in criteria.items())
```

**Your turn.** This is close to your answer on purpose, because closures are the new idea here. Write it from memory rather than copying.

## 4. `apply_mappers`: functions stored in a dict

**Task.** Given a row and a dict of column name to function, return a new row with those columns transformed.

**Solved for the café: tidying an order.**

Functions are values: you can store them in a dict and call them later. `str.title` capitalises each word; written without brackets, it's the function itself rather than a call to it:

```python
fixes = {"drink": str.title, "customer": str.upper}
order = {"drink": "latte", "customer": "ana", "time": "09:00"}

fixes["drink"]  # the function str.title
fixes["drink"]("latte")  # 'Latte': look the function up, then call it
```

The loop way:

```python
def apply_fixes(order, fixes):
    result = {}
    for key, value in order.items():
        if key in fixes:
            result[key] = fixes[key](value)
        else:
            result[key] = value
    return result


apply_fixes(order, fixes)  # {'drink': 'Latte', 'customer': 'ANA', 'time': '09:00'}
```

The Python way fits the `if` into the value using a conditional expression, `A if condition else B`, inside a dict comprehension:

```python
def apply_fixes(order, fixes):
    return {key: fixes[key](value) if key in fixes else value for key, value in order.items()}
```

Both build a new dict, so the original order is untouched. A fix for a column the order doesn't have is simply never used.

**Your turn.** Same shape.

## 5. `append_label`: the bug hunt

**Task.** The code works once and then goes wrong. Run the tests first and read the failure, then fix it.

**The same bug at the café:**

```python
def add_to_basket(item, basket=[]):
    basket.append(item)
    return basket


add_to_basket("latte")  # ['latte']
add_to_basket("mocha")  # ['latte', 'mocha']   <- the latte is still there!
```

The default `[]` is created **once**, when Python first reads the `def`, not each time the function runs. Every call that relies on the default gets that same list, so it keeps growing.

The fix is to default to `None` and make a new list inside:

```python
def add_to_basket(item, basket=None):
    if basket is None:
        basket = []
    return basket + [item]  # `+` builds a new list; .append() would change basket itself


add_to_basket("latte")  # ['latte']
add_to_basket("mocha")  # ['mocha']
```

`basket + [item]`, or `[*basket, item]`, which unpacks the old items into a new list, leaves any list the caller passed in untouched. `basket.append(item)` would change it.

With type hints, an argument that's either a list of strings or None is written `list[str] | None`.

**Your turn.** Fix `append_label` the same way, including its signature.

## 6. `build_url`: strings and keyword-only arguments

**Task.** Join base and path with exactly one slash, add the query string, and make `page` and `per_page` keyword-only.

**The string tools:**

```python
"https://api.example.com/".rstrip("/")  # 'https://api.example.com'  (strip from the right)
"/orders".lstrip("/")  # 'orders'                   (strip from the left)

base, page = "https://api.example.com/", 2
f"{base.rstrip('/')}/orders?page={page}"  # 'https://api.example.com/orders?page=2'
```

An f-string runs the code inside each `{...}` and drops the result into the text. Inside a double-quoted f-string, use single quotes for strings, as in `rstrip('/')`.

**Keyword-only arguments.** Everything after a bare `*` in a signature has to be passed by name:

```python
def order_url(base, *, page=1):
    return f"{base.rstrip('/')}/orders?page={page}"


order_url("https://api.example.com", page=2)  # fine
order_url(
    "https://api.example.com", 2
)  # TypeError: order_url() takes 1 positional argument but 2 were given
```

Why bother? With several number options, `build_url(base, path, 2, 50)` is easy to get backwards. Forcing `page=2, per_page=50` makes every call say what it means.

**Your turn.** Add the `*` to the signature, then build the URL.

## 7. `describe`: pattern matching

**Task.** Describe an event by checking its shape against a list of cases, in order.

**Solved for the café: describing an order.**

```python
def describe_order(order):
    match order:
        case {"drink": "latte", "extras": {"milk": str() as milk}}:
            return f"{milk} latte"
        case {"drink": "latte"}:
            return "a plain latte"
        case {"drink": str() as drink} if drink.startswith("iced"):
            return f"a cold drink: {drink}"
        case {"drink": str() as drink}:
            return f"a {drink}"
        case _:
            return "not an order"


describe_order(orders[0])  # 'oat latte'
describe_order(orders[2])  # 'a plain latte'   (no extras)
describe_order({"drink": "iced tea"})  # 'a cold drink: iced tea'
describe_order(orders[1])  # 'a mocha'
describe_order({})  # 'not an order'
```

How to read it:

- `match order:` is followed by cases, each describing a shape. Python tries them top to bottom and runs the first one that fits.
- A dict pattern such as `{"drink": "latte"}` matches any dict that has that key with that value. Extra keys don't matter.
- `str() as milk` means "any string here; call it `milk`".
- `if ...` after a pattern is a guard: the case only counts if that's true as well.
- `case _:` matches anything, so it goes last.
- Order matters. If `{"drink": "latte"}` came first, the oat latte would match it and never reach the more specific case.

For comparison, here's the first case written with `if`, which is why `match` exists:

```python
extras = order.get("extras") or {}
if order.get("drink") == "latte" and isinstance(extras.get("milk"), str):
    return f"{extras['milk']} latte"
```

**Your turn.** Your cases are listed in the docstring, in order. `properties` plays the part of `extras`.

## When you're done

Run `uv run pytest day2_functions` and `uv run mypy day2_functions`. Then, without looking, write `make_drink_filter` and the fixed `add_to_basket` from memory in `uv run python`.
