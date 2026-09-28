"""The sample frame folds its columns into `…` wherever the box is too narrow, never running past it."""

from __future__ import annotations

import pytest

from gridflow_front_end import build
from gridflow_front_end.paths import DEFAULT_VAULT


def _frame(vendor: str, slug: str) -> dict:
    doc = build.parse_vault_file(
        DEFAULT_VAULT / vendor / f"{slug}.md", vendor, build.REAL_VENDORS[vendor]["label"]
    )
    arts, errors = build.check_artefacts(doc)
    assert errors == []
    view, errors = build._frame_view(doc, arts.sample)
    assert errors == []
    return view


@pytest.mark.parametrize(
    ("vendor", "slug"),
    [
        ("elexon", "system_prices"),
        ("elexon", "fuelhh"),
        ("elexon", "bmunits_reference"),
        ("entsog", "physical_flows"),
    ],
)
def test_every_column_but_the_first_folds_below_the_width_it_needs(vendor: str, slug: str) -> None:
    view = _frame(vendor, slug)
    cols = view["columns"]
    assert cols[0]["tier"] is None and not cols[0]["folded"]  # the first column always shows
    tiers = [c["tier"] for c in cols if not c["folded"]][1:]
    assert all(t is not None for t in tiers)
    assert tiers == sorted(tiers)  # a column never shows where the one before it has folded
    for t in set(tiers):
        assert f'@container fr (max-width: {t - 0.02:.2f}px)' in view["fold_css"]
    # with no pipeline columns folded for good, `…` shows only where the last column folds
    assert view["el_tier"] == (None if view["n_folded"] else tiers[-1])
