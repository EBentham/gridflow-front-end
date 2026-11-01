"""The homepage is rendered by gridflow-build from the manifests and the committed series.

Its vendor strip states each vendor's name, count and fact from ``site/hifi/data/<vendor>.json``,
and each sparkline draws one series of a dataset page's chart from that page's own committed file,
so the homepage cannot show a window or a range the dataset page does not.
"""

from __future__ import annotations

import datetime as dt
import html
import re
from pathlib import Path

import pytest
from markupsafe import escape

from gridflow_front_end import build, chart_svg
from gridflow_front_end.paths import DEFAULT_VAULT

VEND = re.compile(
    r'<article class="vend vend--(\w+)">.*?<a href="data-sources/\1\.html">(.*?)</a>.*?'
    r'<p class="vend__m">(.*?)</p>\s*<svg[^>]*>(.*?)</svg>\s*'
    r'<p class="vend__cap"><code>(\w+)</code><br>(.*?)</p>',
    re.S,
)
NUM = r"(−?[\d,]+(?:\.\d+)?)"


@pytest.fixture(scope="module")
def site(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("site")
    build.build(DEFAULT_VAULT, out)
    return out


@pytest.fixture(scope="module")
def strip(site: Path) -> list[tuple[str, ...]]:
    return VEND.findall((site / "index.html").read_text(encoding="utf-8"))


def _num(text: str) -> tuple[float, float]:
    """A stated number and half its last shown place: how far from the value it may round."""
    places = len(text.partition(".")[2])
    return float(text.replace("−", "-").replace(",", "")), 0.5 * 10**-places


def test_home_states_every_vendor_and_the_total_from_the_manifests(
    site: Path, strip: list[tuple[str, ...]]
) -> None:
    manifests = {v: build.load_manifest(v) for v in build.REAL_VENDORS}
    rows = {vid: (html.unescape(name), html.unescape(fact)) for vid, name, fact, *_ in strip}
    assert set(rows) == set(manifests)
    for vid, m in manifests.items():
        assert rows[vid] == (m["name"], f"{build.manifest_count_line(m)}, {m['landing']['fact']}")
    home = (site / "index.html").read_text(encoding="utf-8")
    total = sum(build.manifest_total_count(m) for m in manifests.values())
    assert f"Seven vendors, {total} datasets," in home
    assert (
        f"Seven vendors across UK and EU power, gas, carbon and weather: {total} datasets" in home
    )


def test_each_sparkline_states_its_dataset_pages_window_and_range(
    site: Path, strip: list[tuple[str, ...]]
) -> None:
    assert len(strip) == len(build.REAL_VENDORS)
    for vid, _name, _fact, _svg, slug, caption in strip:
        doc = build.read_note(build.note_path(DEFAULT_VAULT, vid, slug), slug, vid, "")
        chart, errors = build.resolve_chart(doc)
        assert chart is not None and not errors, (vid, errors)
        view = doc.page.chart_view
        page = site / build._page_href(vid, build.load_manifest(vid), slug).split("#")[0]
        assert escape(view.title) in page.read_text(encoding="utf-8"), vid
        entry = view.key[0]
        unit = re.escape(escape(chart["unit"]))
        m = re.fullmatch(rf"(.*)\. (.*): {NUM} to {NUM}\u00a0{unit}", caption)
        assert m, caption
        assert (html.unescape(m[1]), html.unescape(m[2])) == (view.title, entry.label)
        values = [v for s in chart["series"] if s["key"] == entry.series for v in s["values"]]
        drawn = [v for v in values if v is not None]
        for stated, actual in zip((m[3], m[4]), (min(drawn), max(drawn)), strict=True):
            value, slack = _num(stated)
            assert abs(value - actual) <= slack + 1e-9, (vid, stated, actual)


def test_a_sparkline_breaks_at_a_gap_and_shades_below_zero() -> None:
    chart = {
        "type": "line",
        "unit": "£/MWh",
        "x": [f"2026-09-16T{h:02d}:00:00Z" for h in range(8)],
        "series": [{"key": "p", "values": [10.0, -5.0, -20.0, 4.0, None, 30.0, 25.0, 40.0]}],
    }
    svg = chart_svg.spark(chart, "p")
    lines = re.findall(r'<path d="M([^"]+)" fill="none"', svg)
    assert len(lines) == 2  # the null at 04:00 breaks the line
    ys = [float(p.split()[1]) for line in lines for p in line.split(" L")]
    assert min(ys) == 4 and max(ys) == 48  # 40 at the top, -20 at the bottom
    assert svg.count(f'fill="{chart_svg.colour("fuel-gas")}"') == 1  # one stretch below zero
    assert 'stroke-dasharray="3 3"' in svg  # the zero rule


def test_a_long_sparkline_keeps_its_extremes_in_two_points_a_pixel() -> None:
    days = 6000
    values = [float((i * 37) % 101) for i in range(days)]
    values[1234], values[4321] = -7.0, 250.0
    start = dt.date(2009, 1, 1)
    chart = {
        "type": "line",
        "unit": "MW",
        "x": [(start + dt.timedelta(days=i)).isoformat() for i in range(days)],
        "series": [{"key": "s", "values": values}],
    }
    svg = chart_svg.spark(chart, "s")
    pts = re.search(r'<path d="M([^"]+)" fill="none"', svg)[1].split(" L")
    assert len(pts) <= 2 * 273  # two a pixel column across the 272 px plot
    ys = [float(p.split()[1]) for p in pts]
    assert min(ys) == 4 and max(ys) == 48  # 250 still at the top, -7 at the bottom


def test_a_home_dataset_without_a_chart_fails_the_build(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setitem(build._HOME_SPARKS, "elexon", "inddem")  # a page with no chart
    with pytest.raises(SystemExit):
        build.build(DEFAULT_VAULT, tmp_path)
