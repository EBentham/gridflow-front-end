"""The NESO Data Portal hub: NESO's whole catalogue as a plot plan, linking only the pages here."""

from __future__ import annotations

import copy
import html
import re
from pathlib import Path

import pytest

from gridflow_front_end import build
from gridflow_front_end.paths import DEFAULT_VAULT

VENDOR = "neso_data_portal"
SCHED = re.compile(
    r'<section class="sched" id="g-([a-z0-9-]+)".*?<ul class="sched__rows">(.*?)</ul>', re.DOTALL
)
ROW = re.compile(r'<li data-i="(\d+)">(.*?)</li>', re.DOTALL)
LINK = re.compile(r'<a href="([^"]+)">(.*?)</a>', re.DOTALL)
MARKS = re.compile(r'<span class="plot__marks" aria-hidden="true">(.*?)</span>', re.DOTALL)


@pytest.fixture(scope="module")
def site(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("site")
    build.build(DEFAULT_VAULT, out)
    return out


@pytest.fixture(scope="module")
def hub(site: Path) -> str:
    return (site / "data-sources" / f"{VENDOR}.html").read_text(encoding="utf-8")


def _lists(hub: str) -> dict[str, list[tuple[str, str]]]:
    """Group slug → its listed packages as (href or "", title), in list order."""
    out: dict[str, list[tuple[str, str]]] = {}
    for slug, body in SCHED.findall(hub):
        rows = []
        for i, (n, cell) in enumerate(ROW.findall(body)):
            assert int(n) == i
            link = LINK.fullmatch(cell)
            rows.append((link.group(1), link.group(2)) if link else ("", cell))
        out[slug] = rows
    return out


def test_every_catalogue_package_is_listed_once_in_its_group(hub: str) -> None:
    cat = build.load_manifest(VENDOR)["catalogue"]
    lists = _lists(hub)
    assert len(cat["groups"]) == 16 and set(lists) == {g["slug"] for g in cat["groups"]}
    assert sum(len(rows) for rows in lists.values()) == 131
    for g in cat["groups"]:
        titles = [html.unescape(t) for _, t in lists[g["slug"]]]
        assert titles == [build._package_title(p["title"], g["name"]) for p in g["packages"]]
        assert f'<span class="plot__n">{len(g["packages"])} package' in hub


def test_exactly_the_page_set_is_linked_from_its_packages_group(hub: str) -> None:
    m = build.load_manifest(VENDOR)
    pages = [p for g in m["groups"] for p in g["pages"]]
    group_of = {p["slug"]: g["slug"] for g in m["catalogue"]["groups"] for p in g["packages"]}
    renames = m["catalogue"]["page_packages"]
    linked = {href: slug for slug, rows in _lists(hub).items() for href, _ in rows if href}
    assert sorted(linked) == sorted(f"{VENDOR}/{p}.html" for p in pages)
    for page in pages:
        assert linked[f"{VENDOR}/{page}.html"] == group_of[renames.get(page, page)]
    # one solid square per page here, an open square for every other package
    marks = "".join(MARKS.findall(hub))
    assert marks.count("<i></i>") == len(pages)
    assert marks.count('<i class="o"></i>') == 131 - len(pages)


def test_the_catalogue_hub_counts_groups_and_packages_and_drops_the_old_listing(hub: str) -> None:
    assert "<div><dt>Data groups</dt><dd>16</dd></div>" in hub
    assert "<div><dt>Packages</dt><dd>131</dd></div>" in hub
    for gone in ("<dt>Datasets</dt>", "<dt>Grain</dt>", 'class="bed__rows"', "three", "Three"):
        assert gone not in hub
    for word in ("coming soon", "held", "—", " – "):
        assert word not in hub.lower()
    assert hub.count('aria-expanded="true"') == 16 and hub.count('aria-controls="g-') == 16


def test_other_hubs_keep_their_listing(site: Path) -> None:
    for vendor_id in build.REAL_VENDORS:
        if vendor_id == VENDOR:
            continue
        assert "catalogue" not in build.load_manifest(vendor_id)
        hub = (site / "data-sources" / f"{vendor_id}.html").read_text(encoding="utf-8")
        assert 'class="bed__rows"' in hub and "<dt>Datasets</dt>" in hub
        assert 'class="bed plan"' not in hub and "plot__marks" not in hub


def test_plots_keep_their_area_in_proportion_to_their_packages() -> None:
    cat = build.load_manifest(VENDOR)["catalogue"]
    sizes = {g["slug"]: len(g["packages"]) for g in cat["groups"]}
    for kind in ("wide", "narrow"):
        for band in cat["plan"][kind]:
            rects: dict[str, tuple[float, float, float, float]] = {}
            build._plan_place(band, (0.0, 0.0, 1000.0, 700.0), sizes, rects)
            per_package = {s: w * h / sizes[s] for s, (_, _, w, h) in rects.items()}
            assert max(per_package.values()) == pytest.approx(min(per_package.values()))


def test_catalogue_errors_catch_a_page_with_no_package_and_a_partial_plan() -> None:
    m = build.load_manifest(VENDOR)
    assert build.catalogue_errors(VENDOR, m) == []
    bad = copy.deepcopy(m)
    bad["groups"][0]["pages"].append("no-such-package")
    assert any("no package in the catalogue" in e for e in build.catalogue_errors(VENDOR, bad))
    bad = copy.deepcopy(m)
    bad["catalogue"]["plan"]["wide"].pop()
    assert any("wide plan" in e for e in build.catalogue_errors(VENDOR, bad))


@pytest.mark.parametrize(
    ("title", "group", "listed"),
    [
        (
            "Open Balancing Platform (OBP) - Non-BM Instructions",
            "Ancillary services",
            "Open Balancing Platform (OBP): Non-BM Instructions",
        ),
        (
            "FES: Pathways to Net Zero – Flexibility Data table (FLX1)",
            "FES: Pathways to Net Zero",
            "Flexibility Data table (FLX1)",
        ),
        ("Daily Wind Availability", "Generation", "Daily Wind Availability"),
    ],
)
def test_package_titles_lose_their_dashes_and_group_prefix(
    title: str, group: str, listed: str
) -> None:
    assert build._package_title(title, group) == listed
