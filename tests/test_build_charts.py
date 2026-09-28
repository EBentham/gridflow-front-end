"""Dataset pages render a distilled chart or no chart at all."""

from __future__ import annotations

import dataclasses
import json

from gridflow_front_end import build, chart_spec
from gridflow_front_end.paths import DEFAULT_VAULT, SITE_DIR

SEEDED_MARKERS = ("Illustrative snapshot", "seeded", '"seed"', "stackedArea")


def _doc(vendor: str, slug: str) -> build.DatasetDoc:
    cfg = build.REAL_VENDORS[vendor]
    return build.parse_vault_file(DEFAULT_VAULT / vendor / f"{slug}.md", vendor, cfg["label"])


def test_stale_series_fails_the_chart_check(tmp_path, monkeypatch) -> None:
    site = tmp_path / "site"
    series_file = chart_spec.series_path(site, "elexon", "fuelhh")
    series_file.parent.mkdir(parents=True)
    series_file.write_text(
        chart_spec.series_path(SITE_DIR, "elexon", "fuelhh").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    monkeypatch.setattr(build, "SITE_DIR", site)
    doc = _doc("elexon", "fuelhh")
    assert doc.page.chart is not None
    changed = dict(doc.page.chart, unit="GW")
    doc.page = dataclasses.replace(doc.page, chart=changed)
    chart, errors, _ = build.resolve_chart(doc)
    assert chart is None
    assert any("different spec" in e for e in errors)


def test_committed_series_matches_its_vault_spec() -> None:
    doc = _doc("elexon", "fuelhh")
    chart, errors, _ = build.resolve_chart(doc)
    assert errors == []
    assert chart is not None
    assert chart["spec_origin"] == "vault"
    assert json.dumps(chart["series"])  # plain JSON, no NaN


def test_no_stub_generator_remains() -> None:
    for name in (
        "build_dataset_stubs_from_landings",
        "build_coming_soon_stubs",
        "COMING_SOON_VENDORS",
        "refresh_chart_data",
    ):
        assert not hasattr(build, name), name
    assert not (build.TEMPLATES_DIR / "dataset-coming-soon.html.j2").exists()
