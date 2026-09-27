"""Page fields read from a dataset's vault note: the dataset page content model.

Page prose, the chart spec and the choices behind every generated part of a
dataset page live in the canonical vault note, in its YAML front matter under
one key (v5 decision D2). The fields follow the locked page anatomy
(DESIGN.md, "Dataset page anatomy", locked 2026-09-27), top to bottom::

    ---
    source: elexon
    dataset_key: fuelhh
    ...
    page:
      # 1. petrol hero
      title: Generation by fuel type             # h1, 6 words or fewer
      summary: One line on what the dataset is.  # 22 words or fewer
      facts:                                     # each 14 words or fewer
        vendor: Elexon BMRS, dataset FUELHH
        cadence: Every 30 minutes
        grain: One row per settlement period and fuel-type code
        history: Elexon publishes from ...       # optional: only where the vendor evidences it
      landscape: power                           # optional drawing: power | market | gas | units
      # 2. topsoil
      what_it_is: >-                             # 60 words or fewer
        ...
      how_used: [...]                            # 2 or 3 uses, 14 words or fewer each
      chart: {...}                               # the chart spec (chart_spec), data only
      chart_view:                                # the words around the chart
        title: Generation by fuel, 20 to 26 September 2026
        caption: ...                             # 40 words or fewer; chart-reading caveats go here
        alt: ...                                 # the chart described for a screen reader
        x_label: settlement date; each starts at 23:00 UTC
        key:
          - {series: wind, label: Wind, codes: WIND}
          - {series: ps, label: Pumped storage, codes: PS, note: ..., paint: hatch-cross}
      # 3. bronze
      raw_feed:
        note: ...                                # 30 words or fewer
        requests: ["GET https://..."]            # the vendor's raw URL
        commands:
          - {run: gridflow ingest elexon fuelhh --start ... --end ..., comment: bronze only}
      # 4. silver
      record:
        select: {filter: [...], dedup: {...}, order_by: [...]}   # picks exactly eight rows
        mark: {fuel_type: PS}                    # optional, unused by the page since the frame (3a) lock
        key: [settlement_date, settlement_period, fuel_type]
        caption: ...                             # 16 words or fewer
        fields: {settlement_date: ..., ...}      # one meaning per column, 14 words or fewer; none for the
                                                 # pipeline columns (data_provider, ingested_at, lineage)
      # 5. gold
      notebook:
        lead: ...                                # 35 words or fewer
        cells: ['df = data.elexon.query("fuelhh", "2026-09-20", "2026-09-26")', ...]
        needs: 20 to 26 September 2026           # "... with <needs> ingested."
        plot_alt: ...
      # 6. foot
      related:
        - {dataset: elexon/fuelinst, note: ...}  # up to 4, 12 words or fewer each
      # a family page (v5 D5) adds its variants; the note is the family's lead member
      family:
        slug: demand-outturn
        members:
          - {dataset: indo, differs: ..., request: "GET https://..."}
    ---

Why front matter and not a fenced block in the body: every vault tool already
``yaml.safe_load``s the front matter (``gridflow_drift_check.py``,
``derive_machine_catalog.py``) and nested keys have precedent
(``v2_fix_history``). A fenced block would be read by the drift check's curl
extractor, which runs any fenced block containing the word "curl" against the
live API. ``propagate-vault-mirror`` copies notes verbatim.

A note with no ``page`` block renders on the legacy template until the Phase 26
fan-out writes one. A note WITH a ``page`` block is on the new template, and
every required field must be present and inside its word budget
(``anatomy_errors``); the build fails otherwise.

This module is stdlib plus PyYAML: the build imports it in CI.
"""

from __future__ import annotations

import datetime as dt
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

import yaml

PAGE_KEY = "page"

# Field names, defined here and nowhere else.
TITLE = "title"
SUMMARY = "summary"
FACTS = "facts"
LANDSCAPE = "landscape"
WHAT_IT_IS = "what_it_is"
HOW_USED = "how_used"
CHART = "chart"
CHART_VIEW = "chart_view"
RAW_FEED = "raw_feed"
RECORD = "record"
NOTEBOOK = "notebook"
RELATED = "related"
FAMILY = "family"

FIELDS = (
    TITLE,
    SUMMARY,
    FACTS,
    LANDSCAPE,
    WHAT_IT_IS,
    HOW_USED,
    CHART,
    CHART_VIEW,
    RAW_FEED,
    RECORD,
    NOTEBOOK,
    RELATED,
    FAMILY,
)
REQUIRED = (
    TITLE,
    SUMMARY,
    FACTS,
    WHAT_IT_IS,
    HOW_USED,
    CHART,
    RAW_FEED,
    RECORD,
    NOTEBOOK,
    RELATED,
)

LANDSCAPES = ("power", "market", "gas", "units")

# Word budgets, from the Phase 24 lock (round-1 A content model, schema option 4,
# notebook drawer 1). A budget is a maximum; counts split on whitespace.
BUDGET = {
    "title": 6,
    "summary": 22,
    "fact": 14,
    "what_it_is": 60,
    "use": 14,
    "chart_title": 10,
    "chart_caption": 40,
    "chart_alt": 90,
    "x_label": 8,
    "key_label": 4,
    "key_note": 18,
    "key_tag": 3,
    "raw_note": 30,
    "command_comment": 6,
    "record_caption": 16,
    "meaning": 14,
    "notebook_lead": 35,
    "needs": 12,
    "plot_alt": 60,
    "related_note": 12,
    "differs": 14,
}
HOW_USED_COUNT = (2, 3)
KEY_MAX = 9
RELATED_MAX = 4
CELLS_COUNT = (2, 4)
REQUESTS_COUNT = (1, 4)
COMMANDS_COUNT = (1, 3)
FAMILY_MEMBERS = (2, 12)

# Chart paints: the scenery palette (DESIGN.md "Colour"), plus unpainted
# hatches for codes the palette does not cover. Khaki is the vendor code OTHER
# and nothing else, so only a series keyed ``other`` may take it.
PAINTS = (
    "horizon",
    "chartreuse",
    "clay",
    "petrol",
    "olive",
    "bronze",
    "khaki",
    "hatch-lines",
    "hatch-cross",
    "hatch-dots",
    "hatch-vertical",
)
# A series named after a palette role gets that role's paint by default.
DEFAULT_PAINT = {
    "wind": "horizon",
    "solar": "chartreuse",
    "gas": "clay",
    "nuclear": "petrol",
    "imports": "olive",
    "biomass": "bronze",
    "other": "khaki",
}

_DATASET_RE = re.compile(r"^[a-z0-9_]+/[a-z0-9_]+$")
_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_COLUMN_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_FENCE = "---"


def words(text: str) -> int:
    """Word count used for every budget: whitespace-separated tokens."""
    return len(text.split())


@dataclass(frozen=True)
class KeyEntry:
    """One entry in the chart's key, in the order the key lists them."""

    series: str
    label: str
    codes: str = ""
    note: str = ""
    paint: str = ""
    tag: str = ""


@dataclass(frozen=True)
class ChartView:
    """The words and key around a chart; the spec itself is data only."""

    title: str = ""
    caption: str = ""
    alt: str = ""
    x_label: str = ""
    key: tuple[KeyEntry, ...] = ()


@dataclass(frozen=True)
class Command:
    """One gridflow CLI call in the raw-feed block."""

    run: str
    comment: str = ""


@dataclass(frozen=True)
class RawFeed:
    """The bronze stratum: the vendor's raw URL and the gridflow calls."""

    note: str = ""
    requests: tuple[str, ...] = ()
    commands: tuple[Command, ...] = ()


@dataclass(frozen=True)
class Record:
    """The silver stratum: which real rows are shown, and what each column means."""

    select: dict[str, Any] = field(default_factory=dict, hash=False, compare=False)
    mark: dict[str, Any] = field(default_factory=dict, hash=False, compare=False)
    key: tuple[str, ...] = ()
    caption: str = ""
    fields: dict[str, str] = field(default_factory=dict, hash=False, compare=False)


@dataclass(frozen=True)
class Notebook:
    """The gold stratum's demo notebook: the dataset cells after the fixed two."""

    lead: str = ""
    source: str = ""
    cells: tuple[str, ...] = ()
    needs: str = ""
    plot_alt: str = ""


@dataclass(frozen=True)
class Related:
    """One related dataset in the deep foot."""

    dataset: str
    note: str


@dataclass(frozen=True)
class FamilyMember:
    """One variant listed on a family page."""

    dataset: str
    differs: str
    request: str = ""


@dataclass(frozen=True)
class Family:
    """A family page (v5 D5): the lead note's page, listing every variant."""

    slug: str
    members: tuple[FamilyMember, ...] = ()


@dataclass(frozen=True)
class Facts:
    """The quick facts under the hero's one-liner (the key comes from ``record.key``)."""

    vendor: str = ""
    cadence: str = ""
    grain: str = ""
    history: str = ""


@dataclass(frozen=True)
class PageFields:
    """Page fields from one vault note; ``present`` is False when it has no ``page`` block."""

    present: bool = False
    title: str | None = None
    summary: str | None = None
    facts: Facts = field(default_factory=Facts)
    landscape: str | None = None
    what_it_is: str | None = None
    how_used: tuple[str, ...] = ()
    chart: dict[str, Any] | None = field(default=None, hash=False, compare=False)
    chart_view: ChartView = field(default_factory=ChartView)
    raw_feed: RawFeed = field(default_factory=RawFeed)
    record: Record = field(default_factory=Record)
    notebook: Notebook = field(default_factory=Notebook)
    related: tuple[Related, ...] = ()
    family: Family | None = None
    declared: frozenset[str] = frozenset()

    @property
    def is_empty(self) -> bool:
        """True when the note declares no page field at all."""
        return not self.declared


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


def _jsonable(value: object) -> object:
    """YAML reads an unquoted ``2026-09-01`` as a date; specs are JSON-shaped.

    Normalising here keeps a vault spec and its staged JSON twin byte-equal
    under ``chart_spec.spec_digest``.
    """
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    if isinstance(value, Mapping):
        # YAML 1.1 reads an unquoted ``on:`` key (the dedup spec's) as the boolean True.
        return {("on" if k is True else str(k)): _jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    return value


class _Reader:
    """Collects type errors while reading the ``page`` mapping into dataclasses."""

    def __init__(self) -> None:
        self.errors: list[str] = []

    def text(self, path: str, value: object, *, required: bool = False) -> str:
        if value is None:
            if required:
                self.errors.append(f"{path}: missing")
            return ""
        if isinstance(value, (dt.date, dt.datetime)):
            value = value.isoformat()
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            value = str(value)
        if not isinstance(value, str) or not value.strip():
            self.errors.append(f"{path}: must be a non-empty string")
            return ""
        if _FENCE in value:
            self.errors.append(f"{path}: must not contain '---' (breaks front-matter parsing)")
        return " ".join(value.split()) if "\n" not in value.strip() else value.strip()

    def mapping(self, path: str, value: object) -> Mapping[str, Any]:
        if value is None:
            return {}
        if not isinstance(value, Mapping):
            self.errors.append(f"{path}: must be a mapping")
            return {}
        return value

    def seq(self, path: str, value: object) -> list[Any]:
        if value is None:
            return []
        if not isinstance(value, list):
            self.errors.append(f"{path}: must be a list")
            return []
        return value

    def unknown(self, path: str, value: Mapping[str, Any], known: tuple[str, ...]) -> None:
        extra = set(value) - set(known)
        if extra:
            self.errors.append(f"{path}: unknown key(s) {sorted(extra)}; known: {list(known)}")


def _prose(text: str) -> str:
    """Folded YAML prose to one line (``>-`` already folds; ``|`` keeps newlines)."""
    return " ".join(text.split())


def _read(page: Mapping[str, Any]) -> tuple[PageFields, list[str]]:
    r = _Reader()
    p = f"{PAGE_KEY}"
    r.unknown(p, page, FIELDS)

    facts_m = r.mapping(f"{p}.{FACTS}", page.get(FACTS))
    r.unknown(f"{p}.{FACTS}", facts_m, ("vendor", "cadence", "grain", "history"))
    facts = Facts(
        vendor=r.text(f"{p}.facts.vendor", facts_m.get("vendor")),
        cadence=r.text(f"{p}.facts.cadence", facts_m.get("cadence")),
        grain=r.text(f"{p}.facts.grain", facts_m.get("grain")),
        history=r.text(f"{p}.facts.history", facts_m.get("history")),
    )

    view_m = r.mapping(f"{p}.{CHART_VIEW}", page.get(CHART_VIEW))
    r.unknown(f"{p}.{CHART_VIEW}", view_m, ("title", "caption", "alt", "x_label", "key"))
    key_entries: list[KeyEntry] = []
    for i, entry in enumerate(r.seq(f"{p}.chart_view.key", view_m.get("key"))):
        where = f"{p}.chart_view.key[{i}]"
        em = r.mapping(where, entry)
        r.unknown(where, em, ("series", "label", "codes", "note", "paint", "tag"))
        key_entries.append(
            KeyEntry(
                series=r.text(f"{where}.series", em.get("series"), required=True),
                label=r.text(f"{where}.label", em.get("label"), required=True),
                codes=r.text(f"{where}.codes", em.get("codes")),
                note=_prose(r.text(f"{where}.note", em.get("note"))),
                paint=r.text(f"{where}.paint", em.get("paint")),
                tag=r.text(f"{where}.tag", em.get("tag")),
            )
        )
    chart_view = ChartView(
        title=r.text(f"{p}.chart_view.title", view_m.get("title")),
        caption=_prose(r.text(f"{p}.chart_view.caption", view_m.get("caption"))),
        alt=_prose(r.text(f"{p}.chart_view.alt", view_m.get("alt"))),
        x_label=r.text(f"{p}.chart_view.x_label", view_m.get("x_label")),
        key=tuple(key_entries),
    )

    raw_m = r.mapping(f"{p}.{RAW_FEED}", page.get(RAW_FEED))
    r.unknown(f"{p}.{RAW_FEED}", raw_m, ("note", "requests", "commands"))
    commands: list[Command] = []
    for i, cmd in enumerate(r.seq(f"{p}.raw_feed.commands", raw_m.get("commands"))):
        where = f"{p}.raw_feed.commands[{i}]"
        cm = r.mapping(where, cmd)
        r.unknown(where, cm, ("run", "comment"))
        commands.append(
            Command(
                run=r.text(f"{where}.run", cm.get("run"), required=True),
                comment=r.text(f"{where}.comment", cm.get("comment")),
            )
        )
    raw_feed = RawFeed(
        note=_prose(r.text(f"{p}.raw_feed.note", raw_m.get("note"))),
        requests=tuple(
            r.text(f"{p}.raw_feed.requests[{i}]", v)
            for i, v in enumerate(r.seq(f"{p}.raw_feed.requests", raw_m.get("requests")))
        ),
        commands=tuple(commands),
    )

    rec_m = r.mapping(f"{p}.{RECORD}", page.get(RECORD))
    r.unknown(f"{p}.{RECORD}", rec_m, ("select", "mark", "key", "caption", "fields"))
    fields_m = r.mapping(f"{p}.record.fields", rec_m.get("fields"))
    record = Record(
        select=dict(_jsonable(r.mapping(f"{p}.record.select", rec_m.get("select")))),  # type: ignore[arg-type]
        mark=dict(_jsonable(r.mapping(f"{p}.record.mark", rec_m.get("mark")))),  # type: ignore[arg-type]
        key=tuple(
            r.text(f"{p}.record.key[{i}]", v)
            for i, v in enumerate(r.seq(f"{p}.record.key", rec_m.get("key")))
        ),
        caption=_prose(r.text(f"{p}.record.caption", rec_m.get("caption"))),
        fields={str(k): _prose(r.text(f"{p}.record.fields.{k}", v)) for k, v in fields_m.items()},
    )

    nb_m = r.mapping(f"{p}.{NOTEBOOK}", page.get(NOTEBOOK))
    r.unknown(f"{p}.{NOTEBOOK}", nb_m, ("lead", "source", "cells", "needs", "plot_alt"))
    cells: list[str] = []
    for i, cell in enumerate(r.seq(f"{p}.notebook.cells", nb_m.get("cells"))):
        if not isinstance(cell, str) or not cell.strip():
            r.errors.append(f"{p}.notebook.cells[{i}]: must be a non-empty string")
            continue
        if _FENCE in cell:
            r.errors.append(f"{p}.notebook.cells[{i}]: must not contain '---'")
        cells.append(cell.strip("\n").rstrip())
    notebook = Notebook(
        lead=_prose(r.text(f"{p}.notebook.lead", nb_m.get("lead"))),
        source=r.text(f"{p}.notebook.source", nb_m.get("source")),
        cells=tuple(cells),
        needs=r.text(f"{p}.notebook.needs", nb_m.get("needs")),
        plot_alt=_prose(r.text(f"{p}.notebook.plot_alt", nb_m.get("plot_alt"))),
    )

    related: list[Related] = []
    for i, rel in enumerate(r.seq(f"{p}.{RELATED}", page.get(RELATED))):
        where = f"{p}.related[{i}]"
        rm = r.mapping(where, rel)
        r.unknown(where, rm, ("dataset", "note"))
        related.append(
            Related(
                dataset=r.text(f"{where}.dataset", rm.get("dataset"), required=True),
                note=_prose(r.text(f"{where}.note", rm.get("note"), required=True)),
            )
        )

    family: Family | None = None
    if page.get(FAMILY) is not None:
        fm = r.mapping(f"{p}.{FAMILY}", page.get(FAMILY))
        r.unknown(f"{p}.{FAMILY}", fm, ("slug", "members"))
        members: list[FamilyMember] = []
        for i, mem in enumerate(r.seq(f"{p}.family.members", fm.get("members"))):
            where = f"{p}.family.members[{i}]"
            mm = r.mapping(where, mem)
            r.unknown(where, mm, ("dataset", "differs", "request"))
            members.append(
                FamilyMember(
                    dataset=r.text(f"{where}.dataset", mm.get("dataset"), required=True),
                    differs=_prose(r.text(f"{where}.differs", mm.get("differs"), required=True)),
                    request=r.text(f"{where}.request", mm.get("request")),
                )
            )
        family = Family(
            slug=r.text(f"{p}.family.slug", fm.get("slug"), required=True),
            members=tuple(members),
        )

    how_used = tuple(
        _prose(r.text(f"{p}.how_used[{i}]", v))
        for i, v in enumerate(r.seq(f"{p}.{HOW_USED}", page.get(HOW_USED)))
    )
    chart = page.get(CHART)
    if chart is not None and not isinstance(chart, Mapping):
        r.errors.append(f"{p}.{CHART}: must be a mapping (a chart spec)")
        chart = None
    title = r.text(f"{p}.{TITLE}", page.get(TITLE))
    summary = _prose(r.text(f"{p}.{SUMMARY}", page.get(SUMMARY)))
    what = _prose(r.text(f"{p}.{WHAT_IT_IS}", page.get(WHAT_IT_IS)))
    landscape = r.text(f"{p}.{LANDSCAPE}", page.get(LANDSCAPE))

    fields = PageFields(
        present=True,
        title=title or None,
        summary=summary or None,
        facts=facts,
        landscape=landscape or None,
        what_it_is=what or None,
        how_used=how_used,
        chart=_jsonable(chart) if chart is not None else None,  # type: ignore[arg-type]
        chart_view=chart_view,
        raw_feed=raw_feed,
        record=record,
        notebook=notebook,
        related=tuple(related),
        family=family,
        declared=frozenset(str(k) for k in page),
    )
    return fields, r.errors


def parse_page_fields(text: str) -> tuple[PageFields, list[str]]:
    """Read the ``page`` block from a vault note's front matter.

    Args:
        text: The whole vault note.

    Returns:
        ``(fields, errors)``. ``fields.present`` is False when the note has no
        ``page`` key; ``errors`` lists malformed fields (types and unknown
        keys). Required fields and word budgets are checked separately by
        ``anatomy_errors``; the chart spec by ``chart_spec.validate_spec``.
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
    return _read(page)


def _budget(errors: list[str], path: str, text: str, budget: str) -> None:
    limit = BUDGET[budget]
    n = words(text)
    if n > limit:
        errors.append(f"{path}: {n} words, over its budget of {limit}")


def _count(errors: list[str], path: str, n: int, bounds: tuple[int, int]) -> None:
    lo, hi = bounds
    if not lo <= n <= hi:
        errors.append(f"{path}: {n} entries; needs {lo} to {hi}")


def anatomy_errors(fields: PageFields) -> list[str]:
    """Required fields and word budgets for a note on the new template.

    Args:
        fields: A note's page fields with ``present`` True.

    Returns:
        Human-readable errors; the build fails on any. Checks that need the
        committed artefacts (every schema column has a meaning, every series
        has a key entry) are made by the build, which has them.
    """
    e: list[str] = []
    p = PAGE_KEY
    for name in REQUIRED:
        if name not in fields.declared:
            e.append(f"{p}.{name}: missing (required on the dataset page template)")
    if fields.title:
        _budget(e, f"{p}.title", fields.title, "title")
    if fields.summary:
        _budget(e, f"{p}.summary", fields.summary, "summary")
    if FACTS in fields.declared:
        for name in ("vendor", "cadence", "grain"):
            if not getattr(fields.facts, name):
                e.append(f"{p}.facts.{name}: missing")
        for name in ("vendor", "cadence", "grain", "history"):
            value = getattr(fields.facts, name)
            if value:
                _budget(e, f"{p}.facts.{name}", value, "fact")
    if fields.landscape and fields.landscape not in LANDSCAPES:
        e.append(f"{p}.landscape: must be one of {list(LANDSCAPES)}")
    if fields.what_it_is:
        _budget(e, f"{p}.what_it_is", fields.what_it_is, "what_it_is")
    if HOW_USED in fields.declared:
        _count(e, f"{p}.how_used", len(fields.how_used), HOW_USED_COUNT)
        for i, use in enumerate(fields.how_used):
            _budget(e, f"{p}.how_used[{i}]", use, "use")

    chart_type = (fields.chart or {}).get("type")
    view = fields.chart_view
    if fields.chart is not None and chart_type != "none":
        if "caption" in fields.chart:
            e.append(f"{p}.chart.caption: put the caption in {p}.chart_view.caption")
        for name, budget in (("title", "chart_title"), ("caption", "chart_caption")):
            value = getattr(view, name)
            if not value:
                e.append(f"{p}.chart_view.{name}: missing")
            else:
                _budget(e, f"{p}.chart_view.{name}", value, budget)
        if not view.alt:
            e.append(f"{p}.chart_view.alt: missing (the chart described for a screen reader)")
        else:
            _budget(e, f"{p}.chart_view.alt", view.alt, "chart_alt")
        if view.x_label:
            _budget(e, f"{p}.chart_view.x_label", view.x_label, "x_label")
        if not view.key:
            e.append(f"{p}.chart_view.key: missing (one entry per series)")
        if len(view.key) > KEY_MAX:
            e.append(f"{p}.chart_view.key: {len(view.key)} entries; at most {KEY_MAX}")
        for i, entry in enumerate(view.key):
            where = f"{p}.chart_view.key[{i}]"
            _budget(e, f"{where}.label", entry.label, "key_label")
            if entry.note:
                _budget(e, f"{where}.note", entry.note, "key_note")
            if entry.tag:
                _budget(e, f"{where}.tag", entry.tag, "key_tag")
            paint = entry.paint or DEFAULT_PAINT.get(entry.series, "")
            if not paint:
                e.append(f"{where}.paint: required for series {entry.series!r}")
            elif paint not in PAINTS:
                e.append(f"{where}.paint: must be one of {list(PAINTS)}")
            elif paint == "khaki" and entry.series != "other":
                e.append(f"{where}.paint: khaki is the vendor code OTHER only (series 'other')")

    if RAW_FEED in fields.declared:
        rf = fields.raw_feed
        if not rf.note:
            e.append(f"{p}.raw_feed.note: missing")
        else:
            _budget(e, f"{p}.raw_feed.note", rf.note, "raw_note")
        if fields.family is None:
            _count(e, f"{p}.raw_feed.requests", len(rf.requests), REQUESTS_COUNT)
        for i, req in enumerate(rf.requests):
            if not re.match(r"^(GET|POST) https://", req):
                e.append(f"{p}.raw_feed.requests[{i}]: must start 'GET https://' (the raw URL)")
        _count(e, f"{p}.raw_feed.commands", len(rf.commands), COMMANDS_COUNT)
        for i, cmd in enumerate(rf.commands):
            if not cmd.run.startswith("gridflow "):
                e.append(f"{p}.raw_feed.commands[{i}].run: must be a gridflow CLI call")
            if cmd.comment:
                _budget(e, f"{p}.raw_feed.commands[{i}].comment", cmd.comment, "command_comment")

    if RECORD in fields.declared:
        rec = fields.record
        if not rec.select:
            e.append(f"{p}.record.select: missing (the filter that picks the eight rows)")
        else:
            extra = set(rec.select) - {"silver", "filter", "dedup", "order_by"}
            if extra:
                e.append(f"{p}.record.select: unknown key(s) {sorted(extra)}")
        if not rec.key:
            e.append(f"{p}.record.key: missing (the columns that identify a row)")
        for col in rec.key:
            if not _COLUMN_RE.match(col):
                e.append(f"{p}.record.key: {col!r} is not a column name")
        if not rec.caption:
            e.append(f"{p}.record.caption: missing")
        else:
            _budget(e, f"{p}.record.caption", rec.caption, "record_caption")
        if not rec.fields:
            e.append(
                f"{p}.record.fields: missing (a meaning for every column but the pipeline ones)"
            )
        for col, meaning in rec.fields.items():
            _budget(e, f"{p}.record.fields.{col}", meaning, "meaning")

    if NOTEBOOK in fields.declared:
        nb = fields.notebook
        if not nb.lead:
            e.append(f"{p}.notebook.lead: missing")
        else:
            _budget(e, f"{p}.notebook.lead", nb.lead, "notebook_lead")
        _count(e, f"{p}.notebook.cells", len(nb.cells), CELLS_COUNT)
        if not nb.needs:
            e.append(f"{p}.notebook.needs: missing")
        else:
            _budget(e, f"{p}.notebook.needs", nb.needs, "needs")
        if nb.plot_alt:
            _budget(e, f"{p}.notebook.plot_alt", nb.plot_alt, "plot_alt")
        for i, cell in enumerate(nb.cells):
            if "setup_notebook" in cell:
                e.append(f"{p}.notebook.cells[{i}]: the setup cell is added by the template")

    if RELATED in fields.declared:
        if not 1 <= len(fields.related) <= RELATED_MAX:
            e.append(f"{p}.related: {len(fields.related)} entries; needs 1 to {RELATED_MAX}")
        for i, rel in enumerate(fields.related):
            if not _DATASET_RE.match(rel.dataset):
                e.append(f"{p}.related[{i}].dataset: must be <vendor>/<dataset>")
            _budget(e, f"{p}.related[{i}].note", rel.note, "related_note")

    if fields.family is not None:
        fam = fields.family
        if fam.slug and not _SLUG_RE.match(fam.slug):
            e.append(f"{p}.family.slug: must be a kebab-case slug")
        _count(e, f"{p}.family.members", len(fam.members), FAMILY_MEMBERS)
        for i, mem in enumerate(fam.members):
            _budget(e, f"{p}.family.members[{i}].differs", mem.differs, "differs")
            if not mem.request:
                e.append(f"{p}.family.members[{i}].request: missing (the variant's raw URL)")
            elif not re.match(r"^(GET|POST) https://", mem.request):
                e.append(f"{p}.family.members[{i}].request: must start 'GET https://'")
    return e
