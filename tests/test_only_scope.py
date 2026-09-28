"""A single-page build fails only on the pages it renders."""

from __future__ import annotations

from gridflow_front_end import build


def test_only_keeps_the_errors_that_name_its_pages() -> None:
    errors = [
        "elexon/atl: page.what_it_is is 61 words, over 60",
        "temp: vault file declares no API endpoint",
        "elexon/tsdf: related x has no page",
    ]
    kept = build._scoped(errors, "elexon", frozenset({"elexon/temp"}))
    assert kept == ["temp: vault file declares no API endpoint"]


def test_a_full_build_keeps_every_error() -> None:
    errors = ["elexon/atl: over budget"]
    assert build._scoped(errors, "elexon", frozenset()) == errors


def test_a_slug_inside_another_slug_does_not_match() -> None:
    kept = build._scoped(["elexon/ndfd: bad"], "elexon", frozenset({"elexon/ndf"}))
    assert kept == []
