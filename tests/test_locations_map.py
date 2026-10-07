"""The weather-site map: its page field, the committed site files and the drawing.

Stdlib and the build extra only, so these run where Polars is not installed; the distil step's tests
are in ``test_locations_distil.py``.
"""

from __future__ import annotations

import json
import math
import re
from typing import Any

import pytest

from gridflow_front_end import artefacts, build, map_svg
from gridflow_front_end.page_fields import KeyEntry, anatomy_errors, parse_page_fields
from gridflow_front_end.paths import DEFAULT_VAULT, SITE_DIR


# ------------------------------------------------------------------------- the page field


def _note(locations_block: str) -> str:
    return (
        "---\nsource: open_meteo\npage:\n  title: Weather at wind farms\n"
        + locations_block
        + "---\nbody\n"
    )


def test_locations_field_reads_title_and_caption() -> None:
    fields, errors = parse_page_fields(
        _note(
            "  locations:\n    title: Where the weather is taken\n    caption: >-\n      The sites,\n      drawn.\n"
        )
    )
    assert errors == []
    assert fields.locations is not None
    assert fields.locations.title == "Where the weather is taken"
    assert fields.locations.caption == "The sites, drawn."


def test_locations_field_rejects_unknown_keys_and_missing_caption() -> None:
    _fields, errors = parse_page_fields(_note("  locations:\n    title: Sites\n    sites: [a]\n"))
    assert any("unknown key(s) ['sites']" in e for e in errors)
    assert any("page.locations.caption: missing" in e for e in errors)


def test_locations_caption_has_a_word_budget() -> None:
    long = " ".join(["word"] * 41)
    fields, _ = parse_page_fields(_note(f"  locations:\n    title: Sites\n    caption: {long}\n"))
    assert any("page.locations.caption: 41 words" in e for e in anatomy_errors(fields))


def test_a_note_without_locations_has_none() -> None:
    fields, _ = parse_page_fields(_note(""))
    assert fields.locations is None


# ------------------------------------------------------------------------- the committed files


def _committed(dataset: str) -> dict[str, Any]:
    path = artefacts.locations_path(SITE_DIR, "openmeteo", dataset)
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("dataset", ["historical_demand", "historical_wind", "historical_solar"])
def test_committed_site_files_pass_the_build_check(dataset: str) -> None:
    assert map_svg.check(_committed(dataset), f"openmeteo/{dataset}") == []


def test_offshore_sites_land_in_the_sea_and_the_rest_on_land() -> None:
    rings = map_svg.land_rings()
    for dataset in ("historical_demand", "historical_wind", "historical_solar"):
        for s in _committed(dataset)["sites"]:
            lat, lon = float(s["configured"]["lat"]), float(s["configured"]["lon"])
            offshore = (s.get("group") or "").startswith("Offshore")
            assert map_svg.on_land(lon, lat, rings) is not offshore, s["name"]


def test_projection_keeps_north_up_and_east_right() -> None:
    x0, y0 = map_svg.project(-4.0, 55.0)
    x1, y1 = map_svg.project(-3.0, 56.0)
    assert x1 > x0 and y1 < y0
    assert map_svg.project(map_svg.LON_MIN, map_svg.LAT_MAX) == (0.0, 0.0)
    assert map_svg.project(map_svg.LON_MAX, map_svg.LAT_MIN) == pytest.approx(
        (map_svg.WIDTH, map_svg.HEIGHT), abs=0.6
    )


def test_outline_path_stays_small() -> None:
    land, border = map_svg.outline_paths()
    assert len(land) + len(border) < 15_000
    assert "NaN" not in land and land.count("M") > 10


def test_check_catches_a_broken_file() -> None:
    data = _committed("historical_wind")
    broken = {**data, "sites": [{**data["sites"][0], "stats": {}}]}
    assert any(
        "no ['mean_100m_mps'" in e for e in map_svg.check(broken, "openmeteo/historical_wind")
    )
    assert map_svg.check(data, "openmeteo/historical_solar") == [
        "openmeteo/historical_solar: locations file names 'openmeteo/historical_wind'"
    ]


def test_render_links_each_marker_to_its_row() -> None:
    data = _committed("historical_wind")
    key = [KeyEntry(series="walney", label="Walney", paint="horizon")]
    view = map_svg.render(data, key)
    svg = view["svg"]
    names = [s["name"] for s in data["sites"]]
    assert re.findall(r'<a class="wm-s" href="#site-(\w+)"', svg) == names
    assert re.findall(r'aria-describedby="site-(\w+)"', svg) == names
    walney = re.search(r'href="#site-walney"[^>]*>.*?<circle class="wm-dot"[^>]*fill="(#\w+)"', svg)
    assert walney and walney.group(1) == "#3E8C97"  # the chart's horizon paint
    rows = [r["name"] for g in view["groups"] for r in g["rows"]]
    assert rows == names and view["grouped"]
    assert [c["text"] for c in view["columns"]][:4] == ["Site", "Requested", "Answered", "Apart"]


def test_labels_never_overlap() -> None:
    data = _committed("historical_wind")
    sites = [
        (s["name"], *map_svg.project(float(s["configured"]["lon"]), float(s["configured"]["lat"])))
        for s in data["sites"]
    ]
    placed = map_svg.place_labels(sites)
    boxes = []
    for name, (x, y, anchor) in placed.items():
        w = len(map_svg.label_text(name)) * map_svg._LABEL_CH
        left = {"start": x, "end": x - w, "middle": x - w / 2}[anchor]
        boxes.append((left, y - 11, left + w, y + 3))
    for i, a in enumerate(boxes):
        for b in boxes[i + 1 :]:
            assert not (a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3])


DATASETS = ("historical_demand", "historical_wind", "historical_solar")


def test_every_site_has_its_real_name() -> None:
    for dataset in DATASETS:
        for s in _committed(dataset)["sites"]:
            assert s["name"] in map_svg.SITE_NAMES, s["name"]
    assert map_svg.label_text("gwynt_y_mor") == "Gwynt y Môr"
    assert map_svg.label_text("borders_crystalrig") == "Crystal Rig"
    data = _committed("historical_wind")
    unnamed = {**data, "sites": [{**data["sites"][0], "name": "new_site"}]}
    assert any("no display name" in e for e in map_svg.check(unnamed, "openmeteo/historical_wind"))
    svg = map_svg.render(data, [])["svg"]
    assert 'aria-label="Gwynt y Môr"' in svg and ">Gwynt y Môr</text>" in svg


def test_the_accessible_name_is_in_words() -> None:
    for dataset, noun in zip(DATASETS, ("7 cities", "12 wind-farm sites", "6 solar sites")):
        name = map_svg.accessible_name(_committed(dataset))
        assert noun in name and "openmeteo" not in name and "_" not in name


def test_tap_targets_are_24_px_at_390_and_never_cover_a_neighbours_dot() -> None:
    # at a 390 px viewport the drawing is 343 px wide (390 less two 16 px gutters and a scrollbar)
    assert 2 * map_svg.HIT_R * 343 / map_svg.WIDTH >= 24
    for dataset in DATASETS:
        pts = [
            map_svg.project(float(s["configured"]["lon"]), float(s["configured"]["lat"]))
            for s in _committed(dataset)["sites"]
        ]
        for i, a in enumerate(pts):
            for b in pts[i + 1 :]:
                assert math.dist(a, b) > map_svg.HIT_R + map_svg._DOT_R, dataset


def test_orphan_locations_is_empty_for_the_mirror() -> None:
    assert build.orphan_locations(DEFAULT_VAULT) == []


@pytest.mark.parametrize(
    ("slug", "n"), [("historical_demand", 7), ("historical_wind", 12), ("historical_solar", 6)]
)
def test_the_three_pages_carry_the_map(slug: str, n: int) -> None:
    cfg = build.REAL_VENDORS["openmeteo"]
    doc = build.parse_vault_file(
        DEFAULT_VAULT / "openmeteo" / f"{slug}.md", "openmeteo", cfg["label"]
    )
    arts, errors = build.check_artefacts(doc)
    assert errors == []
    chart, chart_errors, _ = build.resolve_chart(doc)
    assert chart_errors == []
    arts.chart = chart
    members = [
        build.parse_vault_file(
            DEFAULT_VAULT / "openmeteo" / f"{m.dataset}.md", "openmeteo", cfg["label"]
        )
        for m in doc.page.family.members
    ]
    view, view_errors = build.page_view(doc, arts, members)
    assert view_errors == []
    html = build.render_page(build.make_env(), view)
    topsoil = html.split('<section class="stratum stratum--topsoil', 1)[1].split("</section>", 1)[0]
    # the map sits in the topsoil band, after the chart
    assert topsoil.index('id="chart-h"') < topsoil.index('id="map-h"')
    assert topsoil.count('class="wm-s"') == n
    assert len(re.findall(r'<tr id="site-\w+" data-site=', topsoil)) == n
    assert "every hour of 2022 to 2025, UTC" in topsoil
    assert "—" not in topsoil
