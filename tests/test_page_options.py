"""Page options for package pages: related page slugs and the other content-model additions."""

from __future__ import annotations

import dataclasses
from typing import Any

from gridflow_front_end import build
from gridflow_front_end.page_fields import Related, anatomy_errors
from gridflow_front_end.paths import DEFAULT_VAULT


def _doc(vendor: str, slug: str) -> build.DatasetDoc:
    cfg = build.REAL_VENDORS[vendor]
    return build.read_note(build.note_path(DEFAULT_VAULT, vendor, slug), slug, vendor, cfg["label"])


def _view(doc: build.DatasetDoc) -> tuple[dict[str, Any], list[str]]:
    arts, errors = build.check_artefacts(doc)
    assert errors == []
    arts.chart, chart_errors, _ = build.resolve_chart(doc)
    assert chart_errors == []
    return build.page_view(doc, arts, [])


def _with_page(doc: build.DatasetDoc, **changes: Any) -> build.DatasetDoc:
    return dataclasses.replace(doc, page=dataclasses.replace(doc.page, **changes))


def test_a_related_entry_may_name_a_package_page_slug() -> None:
    doc = _doc("neso_data_portal", "constraint_breakdown")
    rel = (
        Related("neso_data_portal/aggregated-bsad", "Balancing adjustments outside the mechanism"),
        Related("elexon/demand-outturn", "Demand outturn, a family page"),
        Related("elexon/system_prices", "Imbalance prices"),
    )
    page = dataclasses.replace(doc.page, related=rel)
    assert not [e for e in anatomy_errors(page) if "related" in e]
    view, errors = _view(_with_page(doc, related=rel))
    assert errors == []
    assert [r["href"] for r in view["related"]] == [
        "aggregated-bsad.html",
        "../elexon/demand-outturn.html",
        "../elexon/system_prices.html",
    ]


def test_a_related_slug_must_name_a_page_in_the_page_set() -> None:
    doc = _doc("neso_data_portal", "constraint_breakdown")
    rel = (Related("neso_data_portal/no-such-package", "Nothing"),)
    _view_, errors = _view(_with_page(doc, related=rel))
    assert any("related neso_data_portal/no-such-package has no page" in e for e in errors)
    for bad in (
        "neso_data_portal/Aggregated-BSAD",
        "neso_data_portal/aggregated-",
        "aggregated-bsad",
    ):
        page = dataclasses.replace(doc.page, related=(Related(bad, "x"),))
        assert any("related[0].dataset" in e for e in anatomy_errors(page)), bad


def test_needs_must_be_a_noun_phrase_the_sentence_can_hold() -> None:
    from gridflow_front_end.page_fields import needs_problem

    # the two values that read as broken copy on the showcase pages
    assert "';'" in (
        needs_problem("summary capture of 6 October 2026, and report; newer summary files fail")
        or ""
    )
    assert needs_problem("one capture of each file from 2016-17 on; 2020-21 will not load")
    assert "'will'" in (needs_problem("every file, 2020-21 will not load") or "")
    assert "says 'ingest'" in (needs_problem("Ingest the summary table") or "")
    assert "verb 'download'" in (needs_problem("download both files") or "")
    assert "full stop" in (needs_problem("the BM unit register.") or "")
    assert "verb 'run'" in (needs_problem("run the summary pipeline for a day") or "")
    assert "clause" in (needs_problem("a capture that fails on 2020-21") or "")
    for ok in (
        "20 to 26 September 2026",
        "the BM unit register",
        "publishes from 19 September to 00:00 UTC on 22 September 2026",
        "a capture of NESO's yearly files from 2016-17",
        "`regional_intensity` for 13 to 21 September 2026",
    ):
        assert needs_problem(ok) is None, ok


def test_every_note_on_the_template_has_a_needs_line_that_reads() -> None:
    from gridflow_front_end.page_fields import needs_problem

    for vendor, slug in sorted(build.new_template_pages(DEFAULT_VAULT)):
        doc = _doc(vendor, slug)
        assert needs_problem(doc.page.notebook.needs) is None, f"{vendor}/{slug}"


def test_a_clause_in_needs_fails_the_anatomy_check_with_the_rule() -> None:
    doc = _doc("neso_data_portal", "aggregated_bsad")
    nb = dataclasses.replace(doc.page.notebook, needs="each file; 2020-21 will not load")
    errors = anatomy_errors(dataclasses.replace(doc.page, notebook=nb))
    [msg] = [e for e in errors if "notebook.needs" in e]
    assert "noun phrase" in msg and "with <needs> ingested" in msg


CURRENT = "GET https://api.neso.energy/datastore/dump/11111111-2222-3333-4444-555555555555"
ARCHIVE = "GET https://api.neso.energy/datastore/dump/66666666-7777-8888-9999-000000000000"


def _dfs_note(request: str) -> str:
    return (
        "---\npage:\n  family:\n    slug: demand-flexibility\n    members:\n"
        f"      - {{dataset: a, differs: Current file, request: {request}}}\n"
        f'      - {{dataset: b, differs: One file, request: "{CURRENT}"}}\n---\n'
    )


def test_a_member_may_list_each_of_its_files() -> None:
    from gridflow_front_end.page_fields import parse_page_fields

    fields, errors = parse_page_fields(_dfs_note(f'["{CURRENT}", "{ARCHIVE}"]'))
    assert errors == []
    first, second = fields.family.members
    assert first.requests == (CURRENT, ARCHIVE)
    assert second.requests == (CURRENT,)
    assert not [e for e in anatomy_errors(fields) if "request" in e]
    fields, _ = parse_page_fields(_dfs_note(f'["{CURRENT}", "ftp://x"]'))
    assert any("members[0].request: must start" in e for e in anatomy_errors(fields))
    fields, _ = parse_page_fields(_dfs_note(f'["{CURRENT}"' + f', "{CURRENT}"' * 4 + "]"))
    assert any("5 requests; at most 4" in e for e in anatomy_errors(fields))


def test_each_file_is_a_row_of_the_members_well_wrapped_like_one() -> None:
    doc = _doc("neso_data_portal", "demand_flexibility_utilisation_summary")
    fam = doc.page.family
    one = fam.members[0]
    two = dataclasses.replace(one, requests=(CURRENT, ARCHIVE))
    single, errors = _view(doc)
    assert errors == []
    page = dataclasses.replace(fam, members=(two, *fam.members[1:]))
    double, errors = _view(_with_page(doc, family=page))
    assert errors == []
    html = str(double["variants"][0]["request"])
    assert html == str(build.request_lines(CURRENT)) + str(build.request_lines(ARCHIVE))
    assert html.count('<span class="ln">GET ') == 2 and html.count("<wbr>") >= 6
    # the other members, and a member with one file, render as before
    assert double["variants"][1:] == single["variants"][1:]
    assert str(single["variants"][0]["request"]) == str(build.request_lines(one.requests[0]))


def test_a_long_table_key_in_a_command_may_break_at_its_underscores_on_a_phone() -> None:
    row = str(
        build.command_row(
            "gridflow ingest neso_data_portal demand_flexibility_utilisation_summary --last 24h"
        )
    )
    assert (
        '<span class="nw nw-cut">demand_<wbr>flexibility_<wbr>utilisation_<wbr>summary</span>'
        in row
    )
    # shorter arguments and flags with their values stay whole, as before
    assert '<span class="nw">neso_data_portal</span>' in row
    assert '<span class="nw">--last 24h</span>' in row
    assert str(build.command_row("gridflow ingest elexon system_prices --start 2026-09-16")) == (
        '<span class="nw">gridflow</span> <span class="nw">ingest</span> '
        '<span class="nw">elexon</span> <span class="nw">system_prices</span> '
        '<span class="nw">--start 2026-09-16</span>'
    )


def test_a_long_url_segment_may_break_at_its_hyphens_on_a_phone() -> None:
    url = "GET https://api.neso.energy/datastore/dump/829e325f-8926-40ab-9dd6-8b7aea6cb244"
    row = str(build.request_lines(url))
    assert '<span class="nw">https://api.neso.energy/</span>' in row
    assert '<span class="nw">datastore/</span><wbr><span class="nw">dump/</span>' in row
    assert (
        '<span class="nw nw-cut">829e325f-<wbr>8926-<wbr>40ab-<wbr>9dd6-<wbr>8b7aea6cb244</span>'
        in row
    )
    # a host is never cut, and a short segment with a date keeps its hyphens whole
    short = str(build.request_lines("GET https://transparency.entsog.eu/api/v1/2026-09-13"))
    assert "nw-cut" not in short


def test_the_cut_points_work_below_768_px_only() -> None:
    css = (build.SITE_DIR / "assets" / "theme.css").read_text(encoding="utf-8")
    assert "@media (max-width: 767.98px) { .ds-well .nw-cut { white-space: inherit; } }" in css
    assert "@media (min-width: 768px) { .ds-well .nw-cut wbr { display: none; } }" in css


def test_a_member_of_a_shown_family_may_say_why_its_rows_are_not_shown() -> None:
    doc = _doc("neso_data_portal", "demand_flexibility_utilisation_summary")
    fam = doc.page.family
    reason = "The newest capture failed on a date format change."
    held = dataclasses.replace(fam.members[-1], held=reason)
    page = dataclasses.replace(fam, members=(*fam.members[:-1], held))
    view, errors = _view(_with_page(doc, family=page))
    assert errors == [] and view["held"] == []
    assert [v["held"] for v in view["variants"]] == [""] * (len(fam.members) - 1) + [reason]
    html = build.render_page(build.make_env(), view)
    assert f'<p class="ds-variants__d">Rows not shown: {reason}</p>' in html
    # the page still shows the lead's rows and notebook
    assert 'class="pl"' in html and "Open the demo notebook" in html


def test_a_url_segment_too_long_for_any_well_may_break_at_every_width() -> None:
    name = "b4634e50af5e4d3bb7f610422776a819_dcrequirementshistorical1_d5c3b48a-a0a9-4d57.csv"
    row = str(build.request_lines(f"GET https://api.neso.energy/dataset/x/download/{name}"))
    # no nowrap and no nw-cut class, so theme.css never hides its break points
    assert '<span class="nw-long">b4634e50af5e4d3bb7f610422776a819_<wbr>dcrequirements' in row
    assert 'class="nw nw-cut">b4634' not in row
