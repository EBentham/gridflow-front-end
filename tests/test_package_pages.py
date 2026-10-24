"""Package pages: one vault note documents every table of a vendor package on one page."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any

import pytest

from gridflow_front_end import artefacts, build

VENDOR = "neso_data_portal"
REAL_LOAD_MANIFEST = build.load_manifest


def _note(stem: str, tables: list[str], page: str = "") -> str:
    return (
        f'---\nsource: "{VENDOR}"\npackage: "{stem}"\ndataset_keys: {json.dumps(tables)}\n'
        f"{page}---\n\n# Package {stem}\n\n## Families\n\nOne section per table.\n"
    )


def _manifest() -> dict[str, Any]:
    m = copy.deepcopy(REAL_LOAD_MANIFEST(VENDOR))
    # these pages are made up, so NESO's catalogue has no packages for them: the hub lists them as beds
    m.pop("catalogue", None)
    m["groups"] = [{"name": "", "blurb": "", "pages": ["pkg-two", "pkg-one"]}]
    m["families"] = [
        {"slug": "pkg-two", "title": "Package two", "note": "pkg-two", "members": ["t_a", "t_b"]}
    ]
    m["package_tables"] = {"pkg-one": "t_c"}
    m["names"] = {"pkg-one": "Package one"}
    return m


@pytest.fixture
def vault(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A vault with a two-table and a one-table package note, and the page set naming them."""
    manifest = _manifest()
    monkeypatch.setattr(
        build,
        "load_manifest",
        lambda vendor_id="elexon": (
            manifest if vendor_id == VENDOR else REAL_LOAD_MANIFEST(vendor_id)
        ),
    )
    monkeypatch.setattr(build, "_MANIFEST_SLUGS_CACHE", None)
    notes = tmp_path / "vault" / VENDOR
    notes.mkdir(parents=True)
    (notes / "pkg-two.md").write_text(_note("pkg-two", ["t_b", "t_a"]), encoding="utf-8")
    (notes / "pkg-one.md").write_text(_note("pkg-one", ["t_c"]), encoding="utf-8")
    return tmp_path / "vault"


def test_a_package_family_renders_from_its_one_note(vault: Path, tmp_path: Path) -> None:
    out_root = tmp_path / "site"
    datasets, pages, _ = build.build_vendor(build.make_env(), VENDOR, vault, out_root)
    assert (datasets, pages) == (3, 2)
    out = out_root / "data-sources" / VENDOR
    page = (out / "pkg-two.html").read_text(encoding="utf-8")
    assert '<main id="main" class="ds-blank">' in page
    for table in ("t_a", "t_b"):
        assert f'id="{table}"' in page
        pointer = (out / f"{table}.html").read_text(encoding="utf-8")
        assert f'href="pkg-two.html#{table}"' in pointer
    hub = (out_root / "data-sources" / f"{VENDOR}.html").read_text(encoding="utf-8")
    assert f'href="{VENDOR}/pkg-two.html"' in hub and "Package two" in hub


def test_a_single_table_package_is_a_plain_page_under_its_table_key(
    vault: Path, tmp_path: Path
) -> None:
    out_root = tmp_path / "site"
    build.build_vendor(build.make_env(), VENDOR, vault, out_root)
    out = out_root / "data-sources" / VENDOR
    page = (out / "pkg-one.html").read_text(encoding="utf-8")
    assert '<code class="ds-chip" id="t_c">neso_<wbr>data_<wbr>portal/<wbr>t_<wbr>c</code>' in page
    assert 'href="pkg-one.html#t_c"' in (out / "t_c.html").read_text(encoding="utf-8")
    hub = (out_root / "data-sources" / f"{VENDOR}.html").read_text(encoding="utf-8")
    assert f'href="{VENDOR}/pkg-one.html"' in hub and "Package one" in hub
    doc = build.read_note(build.note_path(vault, VENDOR, "t_c"), "t_c", VENDOR, "NESO Data Portal")
    assert (doc.slug, doc.package) == ("t_c", "pkg-one")


def test_a_package_page_reads_its_artefacts_under_the_lead_table_key(
    vault: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    site = tmp_path / "site-dir"
    monkeypatch.setattr(build, "SITE_DIR", site)
    sample = artefacts.sample_path(site, VENDOR, "t_a")
    sample.parent.mkdir(parents=True)
    digest = artefacts.select_digest(f"{VENDOR}/t_a", {})
    sample.write_text(json.dumps({"select_sha256": digest}), encoding="utf-8")
    path = build.note_path(vault, VENDOR, "t_a")
    assert path.name == "pkg-two.md"
    doc = build.read_note(path, "t_a", VENDOR, "NESO Data Portal")
    arts, errors = build.check_artefacts(doc)
    assert arts.sample is not None
    assert errors == [
        f"{VENDOR}/t_a: no executed notebook (run scripts/run_notebooks.py and commit it)"
    ]


def test_a_package_note_with_a_page_block_files_its_artefacts_under_the_lead(
    vault: Path, tmp_path: Path
) -> None:
    (vault / VENDOR / "pkg-two.md").write_text(
        _note("pkg-two", ["t_a", "t_b"], page="page:\n  title: Package two\n"), encoding="utf-8"
    )
    found = build.new_template_pages(vault)
    assert (VENDOR, "t_a") in found and (VENDOR, "pkg-two") not in found
    data = tmp_path / "site-dir" / "data"
    data.mkdir(parents=True)
    (data / f"{VENDOR}.json").write_text(json.dumps(_manifest()), encoding="utf-8")
    assert artefacts.note_key(tmp_path / "site-dir", VENDOR, "pkg-two") == "t_a"
    assert artefacts.note_key(tmp_path / "site-dir", VENDOR, "pkg-one") == "t_c"
    assert artefacts.note_key(tmp_path / "site-dir", VENDOR, "other") == "other"


def test_the_page_set_must_have_every_package_note(vault: Path) -> None:
    errors = build.manifest_errors(VENDOR, _manifest(), {"pkg-one"})
    assert errors == [f"{VENDOR}: the page set names notes the vault does not have: ['pkg-two']"]
    assert build.manifest_errors(VENDOR, _manifest(), {"pkg-one", "pkg-two"}) == []


def test_a_table_key_is_on_one_page_only() -> None:
    m = _manifest()
    m["package_tables"]["pkg-one"] = "t_a"
    assert f"{VENDOR}: ['t_a'] are in two families or listed twice" in build.manifest_errors(
        VENDOR, m
    )


def test_a_package_family_is_named_after_its_note_and_has_two_tables() -> None:
    m = _manifest()
    m["families"][0]["note"] = "other"
    m["families"].append(
        {"slug": "pkg-three", "title": "Three", "note": "pkg-three", "members": ["t_d"]}
    )
    m["groups"][0]["pages"].append("pkg-three")
    errors = build.manifest_errors(VENDOR, m)
    assert f"{VENDOR}: package family 'pkg-two' must be named after its note" in errors
    assert (
        f"{VENDOR}: package family 'pkg-three' has one table; list it in `package_tables`" in errors
    )


def test_a_package_note_must_list_the_page_sets_tables(vault: Path) -> None:
    (vault / VENDOR / "pkg-two.md").write_text(_note("pkg-two", ["t_a"]), encoding="utf-8")
    manifest = build.load_manifest(VENDOR)
    docs = {
        key: build.read_note(vault / VENDOR / f"{stem}.md", key, VENDOR, "NESO Data Portal")
        for key, stem in build.manifest_notes(manifest).items()
    }
    assert build.package_errors(manifest, docs) == [
        "t_a: pkg-two.md lists tables ['t_a']; the page set has ['t_a', 't_b']"
    ]
    with pytest.raises(SystemExit):
        build.build_vendor(build.make_env(), VENDOR, vault, vault.parent / "site")


def test_a_package_notes_chart_spec_is_distilled_under_the_lead(
    vault: Path, tmp_path: Path
) -> None:
    distil = pytest.importorskip("gridflow_front_end.distil")
    (vault / VENDOR / "pkg-two.md").write_text(
        _note(
            "pkg-two",
            ["t_a", "t_b"],
            page="page:\n  chart:\n    type: none\n    reason: A test package.\n",
        ),
        encoding="utf-8",
    )
    site = tmp_path / "site-dir"
    (site / "data").mkdir(parents=True)
    (site / "data" / f"{VENDOR}.json").write_text(json.dumps(_manifest()), encoding="utf-8")
    sources, errors, _ = distil.discover_specs(site, vault)
    assert errors == []
    assert [(s.vendor, s.dataset) for s in sources] == [(VENDOR, "t_a")]


_HELD_COMMON = """\
  title: Package held
  summary: A package whose tables are all held.
  facts: {vendor: NESO Data Portal, cadence: Daily file, grain: One row per date and code}
  what_it_is: Two files of a forecast.
  how_used: [A look-ahead feature for procurement., A cross-check on the auction files.]
  related: [{dataset: elexon/fuelhh, note: Generation on the same days}]
"""
DUMP = "GET https://api.neso.energy/datastore/dump/1b85a3f3-80f0-49cf-9b0e-49648fa0cae6"


def _held_family(held_b: str = "held: The history file has no publication instant.") -> str:
    return (
        "page:\n  held: true\n"
        + _HELD_COMMON
        + "  raw_feed:\n    note: Each table's files downloaded whole.\n"
        + "    commands: [{run: gridflow ingest neso_data_portal t_a --last 24h}]\n"
        + "  family:\n    slug: pkg-two\n    members:\n"
        + f'      - {{dataset: t_a, differs: The current file, request: ["{DUMP}", "{DUMP}"],'
        + " held: Its date column's day and month order is not settled.}\n"
        + f'      - {{dataset: t_b, differs: The history file, request: "{DUMP}", {held_b}}}\n'
    )


def _held_single(reason: str = "Its date column's day and month order is not settled.") -> str:
    return (
        f"page:\n  held: {reason}\n"
        + _HELD_COMMON
        + f'  raw_feed:\n    note: The file downloaded whole.\n    requests: ["{DUMP}"]\n'
        + "    commands: [{run: gridflow ingest neso_data_portal t_c --last 24h}]\n"
    )


def test_a_held_package_page_shows_no_rows_and_says_why(vault: Path, tmp_path: Path) -> None:
    notes = vault / VENDOR
    (notes / "pkg-two.md").write_text(
        _note("pkg-two", ["t_a", "t_b"], page=_held_family()), encoding="utf-8"
    )
    (notes / "pkg-one.md").write_text(
        _note("pkg-one", ["t_c"], page=_held_single()), encoding="utf-8"
    )
    out_root = tmp_path / "site"
    datasets, pages, charts = build.build_vendor(build.make_env(), VENDOR, vault, out_root)
    assert (datasets, pages, charts) == (3, 2, 0)
    out = out_root / "data-sources" / VENDOR
    two = (out / "pkg-two.html").read_text(encoding="utf-8")
    # the full anatomy minus rows: no chart, frame, guide or notebook, and no gold stratum
    assert re.findall(r'<section class="stratum stratum--(\w+)', two) == [
        "sky",
        "topsoil",
        "bronze",
        "silver",
        "deep",
    ]
    for absent in (
        "chart--wide",
        'class="pl"',
        "Column guide",
        "Open the demo notebook",
        "<dt>Key</dt>",
    ):
        assert absent not in two, absent
    assert '<p class="g-h" id="gh">Rows not shown</p>' in two
    assert '<h2 class="h-fig" id="sv-h">The silver tables</h2>' in two
    assert re.search(
        r"<dt>neso_<wbr>data_<wbr>portal/<wbr>t_<wbr>a</dt><dd>Its date column\S{1,8}s day and month",
        two,
    )
    assert "The history file has no publication instant." in two
    # the raw feed lists each table's files; the reasons are not repeated there
    assert two.count('<span class="ln">GET ') == 3 and "Rows not shown:" not in two
    one = (out / "pkg-one.html").read_text(encoding="utf-8")
    assert "<dt>neso_<wbr>data_<wbr>portal/<wbr>t_<wbr>c</dt>" in one and "Rows not shown" in one
    # the hub links held pages like any other
    hub = (out_root / "data-sources" / f"{VENDOR}.html").read_text(encoding="utf-8")
    assert f'href="{VENDOR}/pkg-two.html"' in hub and f'href="{VENDOR}/pkg-one.html"' in hub


def test_a_held_page_takes_no_row_sections_and_a_reason_for_each_table(vault: Path) -> None:
    from gridflow_front_end.page_fields import anatomy_errors, parse_page_fields

    fields, errors = parse_page_fields(_note("pkg-two", ["t_a", "t_b"], page=_held_family()))
    assert errors == [] and fields.held and anatomy_errors(fields) == []
    fields, _ = parse_page_fields(_note("pkg-one", ["t_c"], page=_held_single()))
    assert fields.held_reason.startswith("Its date column") and anatomy_errors(fields) == []
    page = _held_family(held_b="held: ''").replace("held: ''", "x: 1")
    fields, errors = parse_page_fields(_note("pkg-two", ["t_a", "t_b"], page=page))
    assert any("members[1]" in e and "unknown key" in e for e in errors)
    fields, _ = parse_page_fields(
        _note("pkg-two", ["t_a", "t_b"], page=_held_family(held_b="x: 1").replace(", x: 1", ""))
    )
    assert any("members[1].held: missing" in e for e in anatomy_errors(fields))
    with_rows = _held_single() + "  chart: {type: none, reason: x}\n  record: {key: [date]}\n"
    fields, _ = parse_page_fields(_note("pkg-one", ["t_c"], page=with_rows))
    errors = anatomy_errors(fields)
    assert any("page.chart: a held page shows no rows" in e for e in errors)
    assert any("page.record: a held page shows no rows" in e for e in errors)
    long = " ".join(["word"] * 17)
    fields, _ = parse_page_fields(_note("pkg-one", ["t_c"], page=_held_single(long)))
    assert any("page.held: 17 words, over its budget of 16" in e for e in anatomy_errors(fields))
    fields, errors = parse_page_fields(_note("pkg-one", ["t_c"], page="page:\n  held: 3\n"))
    assert any("page.held: must be true" in e for e in errors)


def test_a_held_page_with_a_leftover_artefact_fails(
    vault: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    site = tmp_path / "site-dir"
    monkeypatch.setattr(build, "SITE_DIR", site)
    (vault / VENDOR / "pkg-one.md").write_text(
        _note("pkg-one", ["t_c"], page=_held_single()), encoding="utf-8"
    )
    doc = build.read_note(build.note_path(vault, VENDOR, "t_c"), "t_c", VENDOR, "NESO Data Portal")
    assert build.check_artefacts(doc)[1] == []
    sample = artefacts.sample_path(site, VENDOR, "t_c")
    sample.parent.mkdir(parents=True)
    sample.write_text("{}", encoding="utf-8")
    [error] = build.check_artefacts(doc)[1]
    assert "a held page shows no rows; delete its" in error and sample.name in error


@pytest.mark.parametrize(
    "path_of",
    [
        lambda site: artefacts.sample_path(site, VENDOR, "t_c"),
        lambda site: artefacts.notebook_path(site, VENDOR, "t_c"),
        lambda site: artefacts.locations_path(site, VENDOR, "t_c"),
    ],
    ids=["sample", "notebook", "locations"],
)
def test_a_held_page_with_any_row_artefact_still_fails(
    vault: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, path_of: Any
) -> None:
    """Ruling 66 keeps page-level `held` for packages with no silver rows: no frame, no notebook."""
    site = tmp_path / "site-dir"
    monkeypatch.setattr(build, "SITE_DIR", site)
    (vault / VENDOR / "pkg-one.md").write_text(
        _note("pkg-one", ["t_c"], page=_held_single()), encoding="utf-8"
    )
    doc = build.read_note(build.note_path(vault, VENDOR, "t_c"), "t_c", VENDOR, "NESO Data Portal")
    leftover = path_of(site)
    leftover.parent.mkdir(parents=True)
    leftover.write_text("{}", encoding="utf-8")
    [error] = build.check_artefacts(doc)[1]
    assert "a held page shows no rows; delete its" in error and leftover.name in error


def _errors(page: str, tables: list[str] | None = None) -> list[str]:
    from gridflow_front_end.page_fields import anatomy_errors, parse_page_fields

    fields, errors = parse_page_fields(_note("pkg", tables or ["t_c"], page=page))
    return errors + anatomy_errors(fields)


def test_a_caveat_takes_the_held_budget_and_stands_only_beside_rows() -> None:
    from gridflow_front_end.page_fields import parse_page_fields

    sixteen = " ".join(["word"] * 16)
    one_table = "page:\n  caveat: " + sixteen + "\n"
    fields, errors = parse_page_fields(_note("pkg-one", ["t_c"], page=one_table))
    assert errors == [] and fields.caveat == sixteen and not fields.held
    assert not [e for e in _errors(one_table) if "caveat" in e]
    assert "page.caveat: 17 words, over its budget of 16" in _errors(one_table[:-1] + " word\n")
    # a held page has no silver rows; its `held` already says why
    held = _held_single() + "  caveat: The rows are the latest file.\n"
    assert any(e.startswith("page.caveat: a held page shows no silver rows") for e in _errors(held))
    # a family page gives each member its own caveat
    family = _held_family().replace("page:\n  held: true\n", "page:\n  caveat: Latest file.\n")
    assert "page.caveat: a family page gives each member its own caveat" in _errors(
        family, ["t_a", "t_b"]
    )


def _family(member_b: str) -> str:
    """A two-table family page with rows (not held); ``member_b`` is t_b's extra keys."""
    page = _held_family().replace("page:\n  held: true\n", "page:\n")
    page = page.replace(" held: Its date column's day and month order is not settled.", "")
    head = page.rsplit("      - {dataset: t_b", 1)[0]
    return (
        head + f'      - {{dataset: t_b, differs: The history file, request: "{DUMP}"{member_b}}}\n'
    )


def test_a_family_members_caveat_is_for_a_member_whose_rows_are_shown() -> None:
    from gridflow_front_end.page_fields import parse_page_fields

    tables = ["t_a", "t_b"]
    ok = _family(", caveat: The rows are the latest file.")
    fields, errors = parse_page_fields(_note("pkg-two", tables, page=ok))
    assert errors == [] and fields.family is not None
    assert fields.family.members[1].caveat == "The rows are the latest file."
    assert not [e for e in _errors(ok, tables) if "caveat" in e]
    long = _family(", caveat: " + " ".join(["word"] * 17))
    assert "page.family.members[1].caveat: 17 words, over its budget of 16" in _errors(long, tables)
    both = _family(", caveat: Latest file., held: No rows.")
    assert any(
        "members[1].caveat: a member either shows its rows" in e for e in _errors(both, tables)
    )
    on_held = _held_family(held_b="held: The history file has no instant., caveat: Latest file.")
    assert "page.family.members[1].caveat: a held page shows no silver rows; drop it" in _errors(
        on_held, tables
    )

