"""Package pages: one vault note documents every table of a vendor package on one page."""

from __future__ import annotations

import copy
import json
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
