"""Chart spec schema, validation and the committed series files it produces.

A chart spec says, for one dataset, exactly which silver rows a page's chart
plots and how they are reduced: the silver table, filters, de-duplication, the
series grouping, the aggregation, the time window, the unit and the caption.
``gridflow-distil`` (``distil.py``) runs a spec against local silver and writes
one committed JSON file per dataset; ``gridflow-build`` renders from that file
and never touches silver, so CI builds from a bare checkout.

Where a spec lives
------------------
Canonical: the dataset's vault note, under the ``page.chart`` key of its YAML
front matter (see ``page_fields``). Until the Phase 26 authors write those
notes, specs are staged in this repo at
``site/hifi/data/chart-specs/<vendor>/<dataset>.json``. A vault spec wins over
a staged one; having both is reported so the staged copy can be deleted.

This module is stdlib-only on purpose: the build imports it in CI, where
polars and silver are absent.

Spec shape (every key is listed in ``_ALLOWED_KEYS``)::

    {
      "type": "line",                  # line | stacked-area | bar | none
      "silver": "elexon/fuelhh",       # <source>/<table> under the silver root
      "time": "timestamp_utc",         # time column (time charts only)
      "value": "generation_mw",        # measure column (optional for count)
      "filter": [{"column": "fuel_type", "op": "not_null"}],
      "dedup": {"on": ["timestamp_utc"], "order_by": "published_at"},
      "group": "fuel_type",            # series split (time) or category (bar)
      "group_map": {"CCGT": "gas"},    # raw group value -> series label
      "group_default": "other",        # label for values group_map misses
      "group_null": "no fuel type",    # keep null group values as their own series
      "series_order": ["wind", "gas"],
      "aggregation": "sum",            # sum | mean | min | max | count | last
      "time_bucket": "1d",             # 30m | 1h | 1d, truncates before aggregating
      "window": {"last": "7d"},        # or {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
      "sort": "value_desc",            # bar only: value_desc | value_asc | label
      "limit": 12,                     # bar only: keep the first N categories
      "max_points": 2000,              # refuse a series longer than this
      "unit": "MW",
      "caption": "What the chart shows, in one sentence."
    }

``caption`` is optional: a page on the new dataset template keeps its caption
in the note's ``page.chart_view`` (page words, not data), so editing the words
never forces a re-distil.

``{"type": "none", "reason": "..."}`` records a deliberate no-chart decision
(for example a reference table whose only numeric column is an identifier).
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

CHART_TYPES = frozenset({"line", "stacked-area", "bar", "none"})
TIME_CHART_TYPES = frozenset({"line", "stacked-area"})
AGGREGATIONS = frozenset({"sum", "mean", "min", "max", "count", "last"})
FILTER_OPS = frozenset({"eq", "ne", "in", "not_in", "not_null", "is_null", "gt", "ge", "lt", "le"})
TIME_BUCKETS = frozenset({"30m", "1h", "1d"})
BAR_SORTS = frozenset({"value_desc", "value_asc", "label"})
DEFAULT_MAX_POINTS = 2000

_ALLOWED_KEYS = frozenset(
    {
        "type",
        "silver",
        "time",
        "value",
        "filter",
        "dedup",
        "group",
        "group_map",
        "group_default",
        "group_null",
        "series_order",
        "aggregation",
        "time_bucket",
        "window",
        "sort",
        "limit",
        "max_points",
        "unit",
        "caption",
        "reason",
    }
)
_NONE_KEYS = frozenset({"type", "reason"})

_SILVER_RE = re.compile(r"^[a-z0-9_]+/[a-z0-9_]+$")
_COLUMN_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_LAST_RE = re.compile(r"^([1-9][0-9]{0,3})([hd])$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _check_column(errors: list[str], key: str, value: object) -> None:
    if not isinstance(value, str) or not _COLUMN_RE.match(value):
        errors.append(f"{key}: must be a column name, got {value!r}")


def _check_filter(errors: list[str], filters: object) -> None:
    if not isinstance(filters, list):
        errors.append("filter: must be a list of {column, op, value} objects")
        return
    for i, flt in enumerate(filters):
        where = f"filter[{i}]"
        if not isinstance(flt, Mapping):
            errors.append(f"{where}: must be an object")
            continue
        extra = set(flt) - {"column", "op", "value"}
        if extra:
            errors.append(f"{where}: unknown key(s) {sorted(extra)}")
        _check_column(errors, f"{where}.column", flt.get("column"))
        op = flt.get("op")
        if op not in FILTER_OPS:
            errors.append(f"{where}.op: must be one of {sorted(FILTER_OPS)}, got {op!r}")
            continue
        has_value = "value" in flt
        if op in {"not_null", "is_null"}:
            if has_value:
                errors.append(f"{where}: op {op!r} takes no value")
        elif op in {"in", "not_in"}:
            value = flt.get("value")
            if not isinstance(value, list) or not value:
                errors.append(f"{where}.value: op {op!r} needs a non-empty list")
        elif not has_value or isinstance(flt.get("value"), (list, Mapping)):
            errors.append(f"{where}.value: op {op!r} needs one scalar value")


def _check_window(errors: list[str], window: object) -> None:
    if not isinstance(window, Mapping):
        errors.append('window: must be {"last": "<n>d|<n>h"} or {"start": ..., "end": ...}')
        return
    keys = set(window)
    if keys == {"last"}:
        if not isinstance(window["last"], str) or not _LAST_RE.match(window["last"]):
            errors.append(f"window.last: must look like '7d' or '48h', got {window['last']!r}")
    elif keys == {"start", "end"}:
        start, end = window["start"], window["end"]
        for name, val in (("start", start), ("end", end)):
            if not isinstance(val, str) or not _DATE_RE.match(val):
                errors.append(f"window.{name}: must be YYYY-MM-DD, got {val!r}")
        if isinstance(start, str) and isinstance(end, str) and start > end:
            errors.append("window: start is after end")
    else:
        errors.append('window: must have exactly "last", or exactly "start" and "end"')


def validate_spec(spec: object) -> list[str]:
    """Validate one chart spec.

    Args:
        spec: The parsed spec (from a vault note's ``page.chart`` or a staged
            JSON file).

    Returns:
        Human-readable error strings; empty when the spec is valid.
    """
    if not isinstance(spec, Mapping):
        return ["chart spec must be an object"]
    errors: list[str] = []
    unknown = set(spec) - _ALLOWED_KEYS
    if unknown:
        errors.append(f"unknown key(s) {sorted(unknown)}")

    chart_type = spec.get("type")
    if chart_type not in CHART_TYPES:
        errors.append(f"type: must be one of {sorted(CHART_TYPES)}, got {chart_type!r}")
        return errors
    if chart_type == "none":
        extra = set(spec) - _NONE_KEYS
        if extra:
            errors.append(f"type 'none' takes only a reason; drop {sorted(extra)}")
        if not isinstance(spec.get("reason"), str) or not spec["reason"].strip():
            errors.append("reason: a 'none' spec must say why the dataset has no chart")
        return errors
    if "reason" in spec:
        errors.append("reason: only a 'none' spec carries a reason")

    silver = spec.get("silver")
    if not isinstance(silver, str) or not _SILVER_RE.match(silver):
        errors.append(f"silver: must be '<source>/<table>' under the silver root, got {silver!r}")

    aggregation = spec.get("aggregation")
    if aggregation not in AGGREGATIONS:
        errors.append(f"aggregation: must be one of {sorted(AGGREGATIONS)}, got {aggregation!r}")
    if "value" in spec:
        _check_column(errors, "value", spec["value"])
    elif aggregation != "count":
        errors.append("value: required unless aggregation is 'count'")

    if not isinstance(spec.get("unit"), str) or not spec["unit"].strip():
        errors.append("unit: required, a non-empty string")
    if "caption" in spec and (not isinstance(spec["caption"], str) or not spec["caption"].strip()):
        errors.append("caption: must be a non-empty string when given")

    if "filter" in spec:
        _check_filter(errors, spec["filter"])

    if "dedup" in spec:
        dedup = spec["dedup"]
        if not isinstance(dedup, Mapping) or set(dedup) != {"on", "order_by"}:
            errors.append('dedup: must be {"on": [columns], "order_by": column}')
        else:
            on = dedup["on"]
            if not isinstance(on, list) or not on:
                errors.append("dedup.on: must be a non-empty list of columns")
            else:
                for col in on:
                    _check_column(errors, "dedup.on[]", col)
            _check_column(errors, "dedup.order_by", dedup["order_by"])

    if "group" in spec:
        _check_column(errors, "group", spec["group"])
    for key in ("group_map", "group_default", "group_null", "series_order"):
        if key in spec and "group" not in spec:
            errors.append(f"{key}: needs a group column")
    if "group_map" in spec:
        gmap = spec["group_map"]
        if not isinstance(gmap, Mapping) or not gmap:
            errors.append("group_map: must be a non-empty object of raw value -> label")
        elif not all(isinstance(k, str) and isinstance(v, str) for k, v in gmap.items()):
            errors.append("group_map: keys and labels must be strings")
    if "group_default" in spec:
        if "group_map" not in spec:
            errors.append("group_default: only meaningful with a group_map")
        if not isinstance(spec["group_default"], str) or not spec["group_default"]:
            errors.append("group_default: must be a non-empty string")
    if "group_null" in spec and (
        not isinstance(spec["group_null"], str) or not spec["group_null"].strip()
    ):
        errors.append("group_null: must be a non-empty label")
    if "series_order" in spec:
        order = spec["series_order"]
        if not isinstance(order, list) or not all(isinstance(s, str) for s in order):
            errors.append("series_order: must be a list of series labels")
        elif len(set(order)) != len(order):
            errors.append("series_order: labels repeat")

    if "max_points" in spec:
        mp = spec["max_points"]
        if not isinstance(mp, int) or isinstance(mp, bool) or mp < 2:
            errors.append("max_points: must be an integer >= 2")

    if chart_type in TIME_CHART_TYPES:
        _check_column(errors, "time", spec.get("time"))
        if "window" not in spec:
            errors.append("window: required for a time chart")
        else:
            _check_window(errors, spec["window"])
        if "time_bucket" in spec and spec["time_bucket"] not in TIME_BUCKETS:
            errors.append(f"time_bucket: must be one of {sorted(TIME_BUCKETS)}")
        for key in ("sort", "limit"):
            if key in spec:
                errors.append(f"{key}: only a bar chart takes {key}")
    else:  # bar: a category axis, no time axis
        if "group" not in spec:
            errors.append("group: a bar chart needs a category column")
        for key in ("time", "window", "time_bucket"):
            if key in spec:
                errors.append(f"{key}: a bar chart has no time axis")
        if "sort" in spec and spec["sort"] not in BAR_SORTS:
            errors.append(f"sort: must be one of {sorted(BAR_SORTS)}")
        if "limit" in spec:
            lim = spec["limit"]
            if not isinstance(lim, int) or isinstance(lim, bool) or lim < 1:
                errors.append("limit: must be a positive integer")
    return errors


def spec_digest(spec: Mapping[str, Any]) -> str:
    """Stable SHA-256 of a spec, recorded in its series file.

    The build compares it with the digest of the spec it finds today, so a
    spec edited without re-running the distil fails the build instead of
    shipping a chart that no longer matches its caption.
    """
    canonical = json.dumps(spec, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def staging_dir(site_dir: Path) -> Path:
    """Directory of staged specs, ``<site>/data/chart-specs``."""
    return site_dir / "data" / "chart-specs"


def series_dir(site_dir: Path) -> Path:
    """Directory of committed distilled series, ``<site>/data/series``."""
    return site_dir / "data" / "series"


def staged_spec_path(site_dir: Path, vendor: str, dataset: str) -> Path:
    """Path of one staged spec file."""
    return staging_dir(site_dir) / vendor / f"{dataset}.json"


def series_path(site_dir: Path, vendor: str, dataset: str) -> Path:
    """Path of one committed series file."""
    return series_dir(site_dir) / vendor / f"{dataset}.json"


def load_staged_spec(site_dir: Path, vendor: str, dataset: str) -> dict[str, Any] | None:
    """Read a staged spec, or ``None`` when the dataset has none.

    Raises:
        ValueError: The file exists but is not valid JSON.
        TypeError: The file holds JSON that is not an object.
    """
    path = staged_spec_path(site_dir, vendor, dataset)
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: not valid JSON ({exc})") from exc
    if not isinstance(data, dict):
        raise TypeError(f"{path}: a spec must be a JSON object")
    return data


def resolve_spec(
    site_dir: Path,
    vendor: str,
    dataset: str,
    vault_chart: Mapping[str, Any] | None,
) -> tuple[dict[str, Any] | None, str, list[str]]:
    """Pick the spec for one dataset: the vault note's, else the staged one.

    Args:
        site_dir: The ``site/hifi`` directory.
        vendor: Site vendor id (``elexon``).
        dataset: Dataset slug (``fuelhh``).
        vault_chart: ``page.chart`` from the vault note, if it has one.

    Returns:
        ``(spec, origin, notes)`` where origin is ``"vault"``, ``"staging"`` or
        ``""`` and notes are non-fatal observations (both sources present).
    """
    staged = load_staged_spec(site_dir, vendor, dataset)
    notes: list[str] = []
    if vault_chart is not None:
        if staged is not None:
            notes.append(
                f"{vendor}/{dataset}: vault note carries page.chart; the staged spec "
                f"{staged_spec_path(site_dir, vendor, dataset).name} is ignored and can be deleted"
            )
        return dict(vault_chart), "vault", notes
    if staged is not None:
        return staged, "staging", notes
    return None, "", notes


def load_series(site_dir: Path, vendor: str, dataset: str) -> dict[str, Any] | None:
    """Read one committed series file, or ``None`` when it does not exist.

    Raises:
        ValueError: The file exists but is not valid JSON.
        TypeError: The file holds JSON that is not an object.
    """
    path = series_path(site_dir, vendor, dataset)
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: not valid JSON ({exc})") from exc
    if not isinstance(data, dict):
        raise TypeError(f"{path}: a series file must be a JSON object")
    return data


def check_series(
    series: Mapping[str, Any] | None, spec: Mapping[str, Any] | None, key: str
) -> list[str]:
    """Cross-check a committed series file against the spec found today.

    Args:
        series: The loaded series file, or ``None``.
        spec: The resolved spec, or ``None``.
        key: ``<vendor>/<dataset>`` for messages.

    Returns:
        Errors that must fail the build: a series with no spec, a spec with no
        series, or a series distilled from a different spec.
    """
    if spec is None:
        return (
            [f"{key}: series file has no chart spec (delete it or restore the spec)"]
            if series
            else []
        )
    if spec.get("type") == "none":
        return [f"{key}: spec says no chart but a series file exists (delete it)"] if series else []
    if series is None:
        return [f"{key}: chart spec has no distilled series (run gridflow-distil and commit it)"]
    errors: list[str] = []
    if series.get("spec_sha256") != spec_digest(spec):
        errors.append(f"{key}: series was distilled from a different spec (re-run gridflow-distil)")
    x = series.get("x")
    groups = series.get("series")
    if not isinstance(x, list) or not x or not isinstance(groups, list) or not groups:
        errors.append(f"{key}: series file has no x values or no series")
    else:
        for grp in groups:
            values = grp.get("values") if isinstance(grp, Mapping) else None
            if not isinstance(values, list) or len(values) != len(x):
                errors.append(f"{key}: a series length does not match its x axis")
                break
    return errors
