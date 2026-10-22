import dataclasses

import pytest

from day3_classes.exercises import Page, PageDC, RunStats

ITEMS = [{"uuid": "e1"}, {"uuid": "e2"}]


def test_page_keeps_its_attributes() -> None:
    page = Page(ITEMS, "abc")
    assert page.items == ITEMS
    assert page.next_cursor == "abc"
    assert Page(ITEMS).next_cursor is None


def test_page_repr() -> None:
    assert repr(Page(ITEMS, "abc")) == "Page(items=2, next_cursor='abc')"
    assert repr(Page([])) == "Page(items=0, next_cursor=None)"


def test_page_equality_compares_contents() -> None:
    assert Page(ITEMS, "abc") == Page(list(ITEMS), "abc")
    assert Page(ITEMS, "abc") != Page(ITEMS, "xyz")
    assert Page(ITEMS) != "not a page"


def test_page_len_and_is_last() -> None:
    assert len(Page(ITEMS)) == 2
    assert Page(ITEMS).is_last
    assert not Page(ITEMS, "abc").is_last


def test_pagedc_equality_and_repr_come_free() -> None:
    assert PageDC(ITEMS, "abc") == PageDC(list(ITEMS), "abc")
    assert repr(PageDC([], None)) == "PageDC(items=[], next_cursor=None)"


def test_pagedc_defaults_do_not_share_a_list() -> None:
    first, second = PageDC(), PageDC()
    assert first.items == []
    assert first.items is not second.items


def test_pagedc_is_frozen() -> None:
    page = PageDC(ITEMS, "abc")
    with pytest.raises(dataclasses.FrozenInstanceError):
        page.next_cursor = "xyz"  # type: ignore[misc]


def test_pagedc_replace_makes_a_changed_copy() -> None:
    page = PageDC(ITEMS, "abc")
    last = dataclasses.replace(page, next_cursor=None)
    assert last.is_last
    assert page.next_cursor == "abc"


def test_pagedc_len_and_is_last() -> None:
    assert len(PageDC(ITEMS)) == 2
    assert PageDC(ITEMS).is_last
    assert not PageDC(ITEMS, "abc").is_last


def test_pagedc_from_payload() -> None:
    page = PageDC.from_payload({"results": ITEMS, "next": "abc"})
    assert page == PageDC(ITEMS, "abc")


def test_pagedc_from_payload_with_missing_keys() -> None:
    assert PageDC.from_payload({}) == PageDC([], None)


def test_runstats_records_pages() -> None:
    stats = RunStats()
    stats.record_page(PageDC(ITEMS, "abc"))
    stats.record_page(PageDC([{"uuid": "e3"}]))
    assert (stats.pages, stats.rows) == (2, 3)
    assert stats.rows_per_page == 1.5


def test_runstats_rows_per_page_with_no_pages() -> None:
    assert RunStats().rows_per_page == 0.0


def test_runstats_instances_do_not_share_errors() -> None:
    first, second = RunStats(), RunStats()
    first.errors.append("boom")
    assert second.errors == []


def test_runstats_rejects_negative_counts() -> None:
    with pytest.raises(ValueError):
        RunStats(pages=-1)
    with pytest.raises(ValueError):
        RunStats(rows=-5)
