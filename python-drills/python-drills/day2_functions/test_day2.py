from typing import Any, cast

import pytest

from day2_functions.exercises import (
    append_label,
    apply_mappers,
    build_url,
    describe,
    make_filter,
    most_active_user,
    sort_events,
)


def test_sort_events_newest_first_with_uuid_tiebreak() -> None:
    events: list[dict[str, Any]] = [
        {"uuid": "c", "timestamp": "2026-10-01T10:00:00Z"},
        {"uuid": "a", "timestamp": "2026-10-01T09:00:00Z"},
        {"uuid": "b", "timestamp": "2026-10-01T10:00:00Z"},
    ]
    assert [e["uuid"] for e in sort_events(events)] == ["b", "c", "a"]


def test_sort_events_leaves_the_input_alone() -> None:
    events: list[dict[str, Any]] = [
        {"uuid": "a", "timestamp": "2026-10-01T09:00:00Z"},
        {"uuid": "b", "timestamp": "2026-10-01T10:00:00Z"},
    ]
    sort_events(events)
    assert [e["uuid"] for e in events] == ["a", "b"]


def test_most_active_user() -> None:
    events = [{"distinct_id": u} for u in ["ben", "ana", "ben", "cara", "ana", "ben"]]
    assert most_active_user(events) == "ben"


def test_most_active_user_breaks_ties_alphabetically() -> None:
    events = [{"distinct_id": u} for u in ["cara", "ben", "cara", "ben"]]
    assert most_active_user(events) == "ben"


def test_most_active_user_of_nothing_raises() -> None:
    with pytest.raises(ValueError):
        most_active_user([])


def test_make_filter_matches_every_criterion() -> None:
    is_pro_pageview = make_filter(event="$pageview", plan="pro")
    assert is_pro_pageview({"event": "$pageview", "plan": "pro", "other": 1})
    assert not is_pro_pageview({"event": "$pageview", "plan": "free"})
    assert not is_pro_pageview({"event": "$pageview"})


def test_make_filter_with_no_criteria_matches_everything() -> None:
    assert make_filter()({"anything": 1})


def test_apply_mappers() -> None:
    row = {"event": "$pageview", "plan": None, "n": 1}
    result = apply_mappers(row, {"event": str.upper, "plan": lambda p: p or "free", "x": str})
    assert result == {"event": "$PAGEVIEW", "plan": "free", "n": 1}
    assert row == {"event": "$pageview", "plan": None, "n": 1}


def test_append_label_calls_do_not_share_a_list() -> None:
    assert append_label("a") == ["a"]
    assert append_label("b") == ["b"]


def test_append_label_leaves_the_list_passed_in_alone() -> None:
    existing = ["x"]
    assert append_label("y", existing) == ["x", "y"]
    assert existing == ["x"]


def test_build_url_joins_with_one_slash() -> None:
    assert (
        build_url("https://api.example.com/", "/events", page=2)
        == "https://api.example.com/events?page=2&per_page=100"
    )
    assert (
        build_url("https://api.example.com", "events", per_page=50)
        == "https://api.example.com/events?page=1&per_page=50"
    )


def test_build_url_page_is_keyword_only() -> None:
    with pytest.raises(TypeError):
        cast(Any, build_url)("https://api.example.com", "events", 2)


@pytest.mark.parametrize(
    ("event", "expected"),
    [
        ({"event": "$pageview", "properties": {"$current_url": "/pricing"}}, "viewed /pricing"),
        ({"event": "$pageview", "properties": {}}, "viewed a page"),
        ({"event": "$pageview"}, "viewed a page"),
        ({"event": "signed_up", "properties": {"plan": "pro"}}, "signed up to pro"),
        ({"event": "signed_up"}, "custom event: signed_up"),
        ({"event": "$autocapture"}, "system event"),
        ({"event": "invoice_paid", "properties": {"amount": 10}}, "custom event: invoice_paid"),
        ({"event": 42}, "unknown"),
        ({}, "unknown"),
    ],
)
def test_describe(event: dict[str, Any], expected: str) -> None:
    assert describe(event) == expected
