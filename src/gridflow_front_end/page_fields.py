"""Page fields read from a dataset's vault note (v5 decision D2).

Page prose and the chart spec live in the canonical vault note, in its YAML
front matter under one key::

    ---
    source: elexon
    dataset_key: fuelhh
    ...
    page:
      summary: One line on what the dataset is.
      what_it_is: >-
        A short paragraph.
      how_used:
        - One domain use.
        - Another.
      caveats:
        - A real caveat.
      chart:
        type: line
        ...
    ---

Why front matter and not a fenced block in the body: every vault tool already
``yaml.safe_load``s the front matter (``gridflow_drift_check.py``,
``derive_machine_catalog.py``) and nested keys have precedent
(``v2_fix_history``), so the fields add no new parsing surface. A fenced block
would be read by the drift check's curl extractor, which runs any fenced block
containing the word "curl" against the live API. ``propagate-vault-mirror``
copies notes verbatim, so either form survives the mirror.

Field names are provisional until the Phase 24 content-model lock; they are
defined here and nowhere else. Absent fields change nothing on the page.
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

import yaml

PAGE_KEY = "page"
SUMMARY = "summary"
WHAT_IT_IS = "what_it_is"
HOW_USED = "how_used"
CAVEATS = "caveats"
CHART = "chart"

_TEXT_FIELDS = (SUMMARY, WHAT_IT_IS)
_LIST_FIELDS = (HOW_USED, CAVEATS)
FIELDS = (*_TEXT_FIELDS, *_LIST_FIELDS, CHART)


@dataclass(frozen=True)
class PageFields:
    """Page fields from one vault note; every field is optional."""

    summary: str | None = None
    what_it_is: str | None = None
    how_used: tuple[str, ...] = ()
    caveats: tuple[str, ...] = ()
    chart: dict[str, Any] | None = field(default=None, hash=False, compare=False)

    @property
    def is_empty(self) -> bool:
        """True when the note declares no page field at all."""
        return not (self.summary or self.what_it_is or self.how_used or self.caveats or self.chart)


def front_matter_text(text: str) -> str | None:
    """The raw YAML between a note's opening and closing ``---`` lines.

    Uses the same boundaries as ``build._parse_frontmatter`` so both readers
    agree on where the front matter ends.
    """
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return text[3:end]


def _as_text(errors: list[str], name: str, value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{PAGE_KEY}.{name}: must be a non-empty string")
        return None
    if "---" in value:
        errors.append(f"{PAGE_KEY}.{name}: must not contain '---' (breaks front-matter parsing)")
    return value.strip()


def _as_list(errors: list[str], name: str, value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
        errors.append(f"{PAGE_KEY}.{name}: must be a list of non-empty strings")
        return ()
    if any("---" in v for v in value):
        errors.append(f"{PAGE_KEY}.{name}: must not contain '---' (breaks front-matter parsing)")
    return tuple(v.strip() for v in value)


def _jsonable(value: object) -> object:
    """YAML reads an unquoted ``2026-09-01`` as a date; specs are JSON-shaped.

    Normalising here keeps a vault spec and its staged JSON twin byte-equal
    under ``chart_spec.spec_digest``.
    """
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    return value


def parse_page_fields(text: str) -> tuple[PageFields, list[str]]:
    """Read the ``page`` block from a vault note's front matter.

    Args:
        text: The whole vault note.

    Returns:
        ``(fields, errors)``. ``fields`` is empty (``is_empty``) when the note
        has no ``page`` key; ``errors`` lists malformed fields. The chart spec
        is returned as found; ``chart_spec.validate_spec`` validates it.
    """
    raw = front_matter_text(text)
    if raw is None:
        return PageFields(), []
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        return PageFields(), [f"front matter is not valid YAML ({exc})"]
    if not isinstance(data, Mapping) or PAGE_KEY not in data:
        return PageFields(), []
    page = data[PAGE_KEY]
    if not isinstance(page, Mapping):
        return PageFields(), [f"{PAGE_KEY}: must be a mapping of page fields"]
    errors: list[str] = []
    unknown = set(page) - set(FIELDS)
    if unknown:
        errors.append(f"{PAGE_KEY}: unknown field(s) {sorted(unknown)}; known: {list(FIELDS)}")
    chart = page.get(CHART)
    if chart is not None and not isinstance(chart, Mapping):
        errors.append(f"{PAGE_KEY}.{CHART}: must be a mapping (a chart spec)")
        chart = None
    fields = PageFields(
        summary=_as_text(errors, SUMMARY, page.get(SUMMARY)),
        what_it_is=_as_text(errors, WHAT_IT_IS, page.get(WHAT_IT_IS)),
        how_used=_as_list(errors, HOW_USED, page.get(HOW_USED)),
        caveats=_as_list(errors, CAVEATS, page.get(CAVEATS)),
        chart=_jsonable(chart) if chart is not None else None,  # type: ignore[arg-type]
    )
    return fields, errors
