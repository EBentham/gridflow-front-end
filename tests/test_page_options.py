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
