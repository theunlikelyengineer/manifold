# Day 1 walkthrough

**How to use this.** Each section matches one exercise. It explains the task, then solves a similar problem for a café's orders: first with a plain loop, then the shorter Python way. Then it hands over to you. The café problems use the same moves as yours with different names, so you see the pattern without being handed the answer.

Both ways pass the tests. If the short version doesn't make sense yet, write the loop version; that's still good Python. Come back and try the short one later.

## What "event data" is

An event is a record of something a user did:

```python
{
    "uuid": "e1",  # a unique id for this event
    "event": "$pageview",  # what happened
    "distinct_id": "ana",  # who did it
    "timestamp": "2026-10-01T09:00:00Z",  # when
    "properties": {"$browser": "Chrome"},  # extra details, which vary from event to event
}
```

APIs send data as JSON. Python turns a JSON object into a dict and a JSON array into a list, so "a list of events" is just a list of dicts. Everything today is list and dict handling.

These are the café orders used below. Paste them into `uv run python` and try each example as you go:

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

## 1. `flatten_event` (done)

You've done this one. For reference, the café version:

```python
def flatten_order(order):
    extras = order.get("extras") or {}
    return {
        "order_id": order["order_id"],
        "drink": order["drink"],
        "milk": extras.get("milk"),
        "size": extras.get("size"),
    }


flatten_order(orders[0])  # {'order_id': 1, 'drink': 'latte', 'milk': 'oat', 'size': 'large'}
flatten_order(orders[2])  # {'order_id': 3, 'drink': 'latte', 'milk': None, 'size': None}
```

## 2. `event_counts`: how many of each

**Task.** Given a list of events, return a dict of event name to how many times it appears.

```python
events = [{"event": "$pageview"}, {"event": "signed_up"}, {"event": "$pageview"}]
event_counts(events)  # should return {"$pageview": 2, "signed_up": 1}
```

**Solved for the café: how many of each drink?**

The loop way. Keep a dict of running totals. For each order, add 1 to that drink's total, starting it at 1 the first time you see the drink:

```python
def drink_counts(orders):
    counts = {}
    for order in orders:
        drink = order["drink"]
        if drink in counts:
            counts[drink] = counts[drink] + 1
        else:
            counts[drink] = 1
    return counts


drink_counts(orders)  # {'latte': 3, 'mocha': 1}
```

A shorter loop uses `.get()` with a default of 0, which removes the `if`:

```python
counts[drink] = counts.get(drink, 0) + 1
```

The Python way. Counting is so common that the standard library has a tool for it, `Counter`. Hand it the things to count and it does the totals:

```python
from collections import Counter


def drink_counts(orders):
    return dict(Counter(order["drink"] for order in orders))
```

- `order["drink"] for order in orders` means "the drink of each order, one at a time".
- `Counter(...)` tallies them.
- `dict(...)` turns the result into a plain dict. A Counter is already a kind of dict, so this is tidiness rather than necessity.

**Your turn.** Same idea; the name you're counting lives under the `"event"` key. Write the loop version first if the short one feels opaque.

## 3. `unique_users`: each one once

**Task.** Return the set of distinct_ids, with no repeats.

```python
events = [{"distinct_id": "ana"}, {"distinct_id": "ben"}, {"distinct_id": "ana"}]
unique_users(events)  # should return {"ana", "ben"}
```

**Solved for the café: who ordered?**

A set keeps only one copy of each item, so adding `"ana"` twice still leaves one `"ana"`:

```python
def unique_customers(orders):
    customers = set()  # an empty set. Careful: {} on its own is an empty dict
    for order in orders:
        customers.add(order["customer"])
    return customers


unique_customers(orders)  # {'ana', 'ben'}
```

The Python way is a set comprehension, the curly-bracket cousin of a list comprehension:

```python
def unique_customers(orders):
    return {order["customer"] for order in orders}
```

Read it as "the customer of each order, collected into a set". Sets have no order, so `{'ben', 'ana'}` is the same answer.

**Your turn.** The user is under `"distinct_id"`.

## 4. `users_by_event`: group, then tidy

**Task.** For each event name, a sorted list of the users who did it, each user once.

```python
events = [
    {"event": "$pageview", "distinct_id": "ben"},
    {"event": "$pageview", "distinct_id": "ana"},
    {"event": "$pageview", "distinct_id": "ben"},
    {"event": "signed_up", "distinct_id": "ben"},
]
users_by_event(events)  # should return {"$pageview": ["ana", "ben"], "signed_up": ["ben"]}
```

**Solved for the café: which customers ordered each drink?**

Two stages. First, group the customers into a set per drink, which drops the repeats. Second, turn each set into a sorted list.

```python
def customers_by_drink(orders):
    groups = {}
    for order in orders:
        drink = order["drink"]
        if drink not in groups:
            groups[drink] = set()  # first time we've seen this drink
        groups[drink].add(order["customer"])

    result = {}
    for drink, customers in groups.items():
        result[drink] = sorted(customers)  # sorted() always gives back a list
    return result


customers_by_drink(orders)  # {'latte': ['ana', 'ben'], 'mocha': ['ben']}
```

`groups.items()` gives each key and its value together, as pairs, so the loop can unpack them into `drink` and `customers`.

The Python way uses `defaultdict`, which creates the empty set for you the first time a key is used, and a dict comprehension for the second stage:

```python
from collections import defaultdict


def customers_by_drink(orders):
    groups = defaultdict(set)
    for order in orders:
        groups[order["drink"]].add(order["customer"])
    return {drink: sorted(customers) for drink, customers in groups.items()}
```

In your typed version, mypy will want the type spelled out: `groups: defaultdict[str, set[str]] = defaultdict(set)`.

**Your turn.** Group by `"event"` and collect `"distinct_id"`.

## 5. `chunk`: slice a list into pieces

**Task.** Split a list into lists of `size` items; the last can be shorter. Raise `ValueError` if size is below 1.

```python
chunk([1, 2, 3, 4, 5], 2)  # should return [[1, 2], [3, 4], [5]]
chunk([1, 2], 0)  # should raise ValueError
```

**Solved: trays of three.**

`range(start, stop, step)` counts in steps, so `range(0, 7, 3)` gives 0, 3 and 6: the first index of each tray. The slice `items[start:start + size]` takes `size` items from there, and a slice that runs past the end just stops short:

```python
def trays(items, size):
    result = []
    for start in range(0, len(items), size):
        result.append(items[start : start + size])
    return result


trays([1, 2, 3, 4, 5, 6, 7], 3)  # [[1, 2, 3], [4, 5, 6], [7]]
```

The same thing as a list comprehension:

```python
def trays(items, size):
    return [items[start : start + size] for start in range(0, len(items), size)]
```

**Your turn.** This one really is the same shape as yours, so type it out rather than copying it, and say to yourself what each part does. Yours also needs a guard at the top, because a size of 0 makes no sense:

```python
if size < 1:
    raise ValueError("size must be at least 1")
```

`raise` stops the function and hands the error to whoever called it.

## 6. `dedupe_latest`: keep the newest of each

**Task.** One event per uuid, keeping the one with the latest timestamp, in the order each uuid was first seen.

```python
events = [
    {"uuid": "a", "timestamp": "09:00", "v": 1},
    {"uuid": "b", "timestamp": "09:30", "v": 1},
    {"uuid": "a", "timestamp": "10:00", "v": 2},
]
dedupe_latest(events)
# should return [{"uuid": "a", "timestamp": "10:00", "v": 2},
#                {"uuid": "b", "timestamp": "09:30", "v": 1}]
```

**Solved for the café: each customer's latest order.**

Use a dict as a "best so far" table, keyed by customer. For each order, keep it if it's the first for that customer, or newer than the one you're holding:

```python
def latest_order_per_customer(orders):
    latest = {}
    for order in orders:
        customer = order["customer"]
        if customer not in latest or order["time"] > latest[customer]["time"]:
            latest[customer] = order
    return list(latest.values())


[o["order_id"] for o in latest_order_per_customer(orders)]  # [4, 3]
```

Two dict facts make this work:

- Replacing the value of a key that already exists keeps the key in its original position. Ana was seen first, so she stays first even though her order was replaced by a later one.
- `latest.values()` gives the values (the orders) in that order, and `list(...)` makes them a list.

The times compare correctly as text (`"09:20" > "09:00"`) because they're all written the same way.

**Your turn.** Key by `"uuid"` and compare `"timestamp"`.

## When you're done

Run `uv run pytest day1_data_structures` and `uv run mypy day1_data_structures`. Then, without looking back, write `drink_counts` both ways in `uv run python`. If you can, day 1 has stuck.
