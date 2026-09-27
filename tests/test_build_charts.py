"""Dataset pages render a distilled chart or no chart at all."""

from __future__ import annotations

import json
import re

import pytest

from gridflow_front_end import build, chart_spec
from gridflow_front_end.paths import DEFAULT_VAULT, SITE_DIR

SEEDED_MARKERS = ("Illustrative snapshot", "seeded", '"seed"', "stackedArea")

SPECIMENS = [
    ("elexon", "fuelhh"),
    ("elexon", "system_prices"),
    ("elexon", "bmunits_reference"),
    ("entsog", "physical_flows"),
]


def _render(vendor: str, slug: str, *, with_chart: bool) -> str:
    cfg = build.REAL_VENDORS[vendor]
    doc = build.parse_vault_file(DEFAULT_VAULT / vendor / f"{slug}.md", vendor, cfg["label"])
    chart = None
    if with_chart:
        chart, errors, _ = build.resolve_chart(doc)
        assert errors == []
        assert chart is not None
    return build.render_dataset(build.make_env(), doc, build.load_manifest(vendor), chart=chart)


@pytest.mark.parametrize(("vendor", "slug"), SPECIMENS)
def test_specimen_renders_its_distilled_chart(vendor: str, slug: str) -> None:
    html = _render(vendor, slug, with_chart=True)
    series = chart_spec.load_series(SITE_DIR, vendor, slug)
    assert series is not None
    kind = "bars" if series["x_kind"] == "category" else "series"
    match = re.search(rf"data-chart=\"{kind}\" data-opts='([^']*)'", html)
    assert match, "chart element missing"
    opts = json.loads(
        match.group(1).replace("&#34;", '"').replace("&#39;", "'").replace("&amp;", "&")
    )
    assert opts["x"] == series["x"]
    assert [s["key"] for s in opts["series"]] == [s["key"] for s in series["series"]]
    assert series["caption"] in html.replace("&#39;", "'")
    for marker in SEEDED_MARKERS:
        assert marker not in html


def test_page_without_series_has_no_chart_section() -> None:
    html = _render("elexon", "agpt", with_chart=False)
    assert "data-chart" not in html
    assert 'id="snapshot-chart"' not in html
    for marker in SEEDED_MARKERS:
        assert marker not in html


def test_stale_series_fails_the_chart_check(tmp_path, monkeypatch) -> None:
    site = tmp_path / "site"
    spec = chart_spec.load_staged_spec(SITE_DIR, "elexon", "fuelhh")
    assert spec is not None
    staged = chart_spec.staged_spec_path(site, "elexon", "fuelhh")
    staged.parent.mkdir(parents=True)
    staged.write_text(json.dumps(dict(spec, unit="GW")), encoding="utf-8")
    series_file = chart_spec.series_path(site, "elexon", "fuelhh")
    series_file.parent.mkdir(parents=True)
    series_file.write_text(
        chart_spec.series_path(SITE_DIR, "elexon", "fuelhh").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    monkeypatch.setattr(build, "SITE_DIR", site)
    doc = build.parse_vault_file(DEFAULT_VAULT / "elexon" / "fuelhh.md", "elexon", "Elexon BMRS")
    chart, errors, _ = build.resolve_chart(doc)
    assert chart is None
    assert any("different spec" in e for e in errors)


def test_no_stub_generator_remains() -> None:
    for name in (
        "build_dataset_stubs_from_landings",
        "build_coming_soon_stubs",
        "COMING_SOON_VENDORS",
        "refresh_chart_data",
    ):
        assert not hasattr(build, name), name
    assert not (build.TEMPLATES_DIR / "dataset-coming-soon.html.j2").exists()
