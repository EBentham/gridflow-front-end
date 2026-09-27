"""The dataset page template: the locked anatomy, its committed artefacts and its content rules."""

from __future__ import annotations

import dataclasses
import re
from pathlib import Path

import pytest

from gridflow_front_end import artefacts, build, chart_svg
from gridflow_front_end.page_fields import ChartView, KeyEntry, parse_page_fields
from gridflow_front_end.paths import DEFAULT_VAULT

# Phrases that describe our local copy instead of the vendor's data (DESIGN.md: no local-data
# references anywhere on a dataset page).
LOCAL_DATA = re.compile(
    r"\blocally\b|our copy|local (silver|history|rows|copy|store)|rows held", re.IGNORECASE
)


def _doc(vendor: str, slug: str) -> build.DatasetDoc:
    cfg = build.REAL_VENDORS[vendor]
    return build.parse_vault_file(DEFAULT_VAULT / vendor / f"{slug}.md", vendor, cfg["label"])


def _new_template_docs() -> list[build.DatasetDoc]:
    return [_doc(v, s) for v, s in sorted(build.new_template_pages(DEFAULT_VAULT))]


def _render(doc: build.DatasetDoc) -> str:
    arts, errors = build.check_artefacts(doc)
    assert errors == []
    chart, chart_errors, _ = build.resolve_chart(doc)
    assert chart_errors == []
    arts.chart = chart
    members = []
    if doc.page.family is not None:
        members = [_doc(doc.vendor_id, m.dataset) for m in doc.page.family.members]
    view, view_errors = build.page_view(doc, arts, members)
    assert view_errors == []
    return build.render_page(build.make_env(), view)


def test_fuelhh_descends_through_the_strata_in_the_locked_order() -> None:
    html = _render(_doc("elexon", "fuelhh"))
    strata = re.findall(r'<section class="stratum stratum--(\w+)', html)
    assert strata == ["sky", "topsoil", "bronze", "silver", "gold", "deep"]
    heads = re.findall(r'id="(what-h|chart-h|raw-h|sv-h|gd-h|rel-h)"', html)
    assert heads == ["what-h", "chart-h", "raw-h", "sv-h", "gd-h", "rel-h"]
    assert html.count('class="chart chart--') == 2  # wide and narrow drawings
    assert "Open the demo notebook" in html and "Copy notebook" in html
    assert "caveats" not in html.lower()
    assert "MIT" not in html  # no licence line in the foot
    assert not LOCAL_DATA.search(html)


def test_fuelhh_notebook_copy_is_the_executed_code() -> None:
    doc = _doc("elexon", "fuelhh")
    html = _render(doc)
    src = re.search(r'<textarea class="ds-nb-src"[^>]*>(.*?)</textarea>', html, re.DOTALL)
    assert src
    code = src.group(1).replace("&#34;", '"').replace("&quot;", '"')
    assert code.startswith(artefacts.SETUP_CELL)
    for cell in doc.page.notebook.cells:
        assert cell in code


def test_fuelhh_frame_keys_its_columns_and_folds_the_pipeline() -> None:
    html = _render(_doc("elexon", "fuelhh"))
    silver = html.split('<section class="stratum stratum--silver"', 1)[1].split("</section>", 1)[0]
    head = silver.split("<thead>", 1)[1].split("</thead>", 1)[0]
    assert head.count('<span class="k"') == 3  # settlement_date, settlement_period, fuel_type
    assert "shape: (8, 12)" in silver
    assert (
        '<input type="checkbox" class="fx sr-only" id="fx">' in silver
    )  # `…` opens the folded columns
    folded = re.findall(r'<th scope="col" id="c-(\w+)" class="fc">', head)
    assert folded[0] == "ingested_at"
    assert set(build.PIPELINE_COLUMNS) >= set(folded)
    guide = re.findall(r'<dt><a href="#c-(\w+)">', silver)
    assert guide[:3] == ["settlement_date", "settlement_period", "fuel_type"]
    assert not set(guide) & build.PIPELINE_COLUMNS
    assert "Relation" not in silver and "One row" not in silver and "Eight rows" not in silver
    assert "&#34;BIOMASS&#34;" in silver and "datetime[μs, UTC]" in silver  # Polars' own printing


def test_a_changed_row_selection_needs_a_new_sample() -> None:
    doc = _doc("elexon", "fuelhh")
    record = dataclasses.replace(doc.page.record, select={**doc.page.record.select, "order_by": []})
    doc.page = dataclasses.replace(doc.page, record=record)
    _, errors = build.check_artefacts(doc)
    assert any("different page.record.select" in e for e in errors)


def test_changed_cells_need_a_new_notebook_run() -> None:
    doc = _doc("elexon", "fuelhh")
    nb = dataclasses.replace(doc.page.notebook, cells=(*doc.page.notebook.cells, "df.tail()"))
    doc.page = dataclasses.replace(doc.page, notebook=nb)
    _, errors = build.check_artefacts(doc)
    assert any("different cells" in e for e in errors)


def test_every_schema_column_needs_a_meaning() -> None:
    doc = _doc("elexon", "fuelhh")
    fields = {k: v for k, v in doc.page.record.fields.items() if k != "published_at"}
    doc.page = dataclasses.replace(
        doc.page, record=dataclasses.replace(doc.page.record, fields=fields)
    )
    arts, _ = build.check_artefacts(doc)
    assert arts.sample is not None
    _, errors = build._frame_view(doc, arts.sample)
    assert any("no meaning for ['published_at']" in e for e in errors)


def test_every_series_needs_a_key_entry() -> None:
    chart = {"type": "line", "series": [{"key": "a", "values": [1]}, {"key": "b", "values": [2]}]}
    view = ChartView(key=(KeyEntry(series="a", label="A", paint="petrol"),))
    assert any("no entry for series ['b']" in e for e in chart_svg.check_view(chart, view))


def test_signed_series_hang_below_zero() -> None:
    chart = {
        "type": "stacked-area",
        "unit": "MW",
        "x": ["2026-09-20T00:00:00Z", "2026-09-20T00:30:00Z", "2026-09-20T01:00:00Z"],
        "series": [
            {"key": "wind", "values": [10.0, 12.0, 11.0]},
            {"key": "imports", "values": [5.0, -4.0, -6.0]},
        ],
    }
    view = ChartView(alt="x", key=(KeyEntry("wind", "Wind"), KeyEntry("imports", "Imports")))
    wide, _narrow = chart_svg.render(chart, view, "t")
    # the axis reaches below zero: a negative part was stacked, not clipped
    assert "−2" in wide or "−5" in wide or "−10" in wide


@pytest.mark.parametrize(("lo", "hi"), [(0, 16073), (-6314, 34000), (0.2, 0.9)])
def test_nice_ticks_cover_the_range(lo: float, hi: float) -> None:
    ticks = chart_svg.nice_ticks(lo, hi, 5)
    assert ticks[0] <= lo and ticks[-1] >= hi and 3 <= len(ticks) <= 9


def test_a_family_renders_one_page_and_points_its_members_at_it(tmp_path: Path) -> None:
    build.build(DEFAULT_VAULT, tmp_path, frozenset({"elexon/indo"}))
    out = tmp_path / "data-sources" / "elexon"
    page = (out / "demand-outturn.html").read_text(encoding="utf-8")
    for member in ("indo", "itsdo", "indod"):
        assert f'id="{member}"' in page
        pointer = (out / f"{member}.html").read_text(encoding="utf-8")
        assert f'href="demand-outturn.html#{member}"' in pointer
        assert "<main" in pointer


@pytest.mark.parametrize("kind", ["power", "market", "gas", "units", "sources", "elexon"])
def test_landscape_scenery_is_never_cropped(kind: str) -> None:
    """Each hero drawing letterboxes (meet) instead of cropping, and its viewBox clears every rotor tip."""
    partial = (build.TEMPLATES_DIR / "_partials" / "landscape" / f"{kind}.svg.j2").read_text(
        encoding="utf-8"
    )
    svgs = re.findall(
        r'<svg class="land land--(wide|narrow)" viewBox="([-\d.]+) ([-\d.]+) [\d.]+ [\d.]+" '
        r'preserveAspectRatio="xMidYMax meet"',
        partial,
    )
    assert [v for v, _, _ in svgs] == ["wide", "narrow"]
    wide_top = float(svgs[0][2])
    # a rotor is drawn as an invisible circle of blade radius around its hub: cy is 0 in the rotor's frame,
    # so the hub height comes from the translate that places it
    for hub_y, radius in re.findall(
        r'translate\([-\d.]+,([-\d.]+)\)"><g class="rot [^"]+"><circle r="([\d.]+)"', partial
    ):
        assert float(hub_y) - float(radius) > wide_top + 8, (
            f"{kind}: a rotor tip reaches the top edge"
        )


def test_no_page_block_describes_local_data() -> None:
    for doc in _new_template_docs():
        text = (DEFAULT_VAULT / doc.vendor_id / f"{doc.slug}.md").read_text(encoding="utf-8")
        block = text.split("\npage:", 1)[1].split("\n---", 1)[0]
        assert not LOCAL_DATA.search(block), doc.slug
        assert "—" not in block, f"{doc.slug}: em dash in the page block"


def test_every_new_template_page_renders() -> None:
    docs = _new_template_docs()
    assert docs
    for doc in docs:
        assert (
            parse_page_fields(
                (DEFAULT_VAULT / doc.vendor_id / f"{doc.slug}.md").read_text(encoding="utf-8")
            )[1]
            == []
        )
        _render(doc)


def test_a_page_without_a_page_block_is_blank(tmp_path: Path) -> None:
    """Ruling 30: the hero's breadcrumb, name and id, nothing else, and no planning words."""
    build.build(DEFAULT_VAULT, tmp_path, frozenset({"elexon/agpt", "neso/carbon_intensity"}))
    page = (tmp_path / "data-sources" / "elexon" / "agpt.html").read_text(encoding="utf-8")
    assert re.findall(r'<section class="stratum stratum--(\w+)', page) == ["sky"]
    assert '<h1 class="h-hero ds-hero__h" id="ds-h">Actual generation per type</h1>' in page
    assert '<code class="ds-chip">elexon/agpt</code>' in page
    assert 'href="../elexon.html"' in page and "ds-facts" not in page and "data-chart" not in page
    assert not re.search(r"soon|planned|coming|placeholder|not yet", page, re.IGNORECASE)
    family = (tmp_path / "data-sources" / "neso" / "national-carbon-intensity.html").read_text(
        encoding="utf-8"
    )
    assert '<code class="ds-chip" id="intensity_fw48h">neso/intensity_fw48h</code>' in family
    pointer = (tmp_path / "data-sources" / "neso" / "intensity_fw48h.html").read_text(
        encoding="utf-8"
    )
    assert 'href="national-carbon-intensity.html#intensity_fw48h"' in pointer


def test_the_page_set_is_149_datasets_on_73_pages() -> None:
    """Rulings 12 to 14: families are one page each; the headline count is computed."""
    manifests = [build.load_manifest(v) for v in build.REAL_VENDORS]
    for vendor_id, m in zip(build.REAL_VENDORS, manifests, strict=True):
        assert build.manifest_errors(vendor_id, m) == []
    assert sum(build.manifest_total_count(m) for m in manifests) == 149
    assert sum(len(g["pages"]) for m in manifests for g in m["groups"]) == 73


def test_hubs_and_landing_link_every_page(tmp_path: Path) -> None:
    build.build(DEFAULT_VAULT, tmp_path)
    landing = (tmp_path / "data-sources.html").read_text(encoding="utf-8")
    assert '<span class="hub-n">149 datasets</span>' in landing
    for vendor_id in build.REAL_VENDORS:
        assert f'href="data-sources/{vendor_id}.html"' in landing
        hub = (tmp_path / "data-sources" / f"{vendor_id}.html").read_text(encoding="utf-8")
        m = build.load_manifest(vendor_id)
        for g in m["groups"]:
            for page in g["pages"]:
                assert f'href="{vendor_id}/{page}.html"' in hub
                assert (tmp_path / "data-sources" / vendor_id / f"{page}.html").is_file()
        assert f"<dt>Datasets</dt><dd>{build.manifest_total_count(m)}</dd>" in hub
        assert "—" not in hub and not LOCAL_DATA.search(hub)
    assert "—" not in landing and not LOCAL_DATA.search(landing)
