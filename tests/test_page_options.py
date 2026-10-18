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
