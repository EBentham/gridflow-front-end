"""Distil real gridflow silver series into a committed build input.

Dataset-page snapshot charts were seeded shapes; this module turns a local
gridflow extract into real series for them.

Two steps, deliberately split
-----------------------------
1. ``gridflow-build --refresh-chart-data`` (local, occasional) reads the
   extract at ``$GRIDFLOW_CHART_EXTRACT_PATH`` (default
   ``C:/data_to_seed_gridflow_charts``) and writes
   ``site/hifi/data/chart-series.json`` — a small, **committed** artefact.
2. Every ordinary build reads only that committed file.

The split is not incidental. ``deploy.yml`` runs ``gridflow-build`` from a bare
checkout, so the extract directory does not exist in CI. A build that read the
extract directly would degrade every page to a seeded chart in the one place
that actually publishes, and the deployed site would never carry real data.
Distilling to a committed file makes the local build and the CI build identical,
and keeps ``--check`` idempotent.

When ``chart-series.json`` is absent, or holds no entry for a page, that page
falls back to its seeded chart and keeps its "illustrative, seeded" caption —
the caption always matches the data, in both directions.

Column selection
----------------
The extract's own ``charts/charts-manifest.json`` records a ``plotted_column``
per dataset, chosen by taking the first numeric column. That is wrong for 16
datasets: it plots ``regionid`` for the nine NESO regional-intensity datasets
and ``latitude`` for the six Open-Meteo ones — identifiers and coordinates whose
mean is a flat line. ``_DENY_*`` below rejects that class, and the
constant-series guard in ``_distil_one`` is the backstop: a series with no
variation is not a chart, so it is suppressed rather than shipped under a
caption claiming real data.
"""

from __future__ import annotations

import csv
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

DEFAULT_EXTRACT = Path("C:/data_to_seed_gridflow_charts")

# Sparkline points. `charts.js` scales x by `i / (N - 1)`, so one point divides
# by zero and two draw a bare slope. The floor is 5 because that is what the
# 2026-08-16 charts already ship for the daily-grain GIE and ENTSO-G datasets
# over this 5-day window — raising it would seed pages that currently render.
MAX_POINTS = 120
MIN_POINTS = 5

# Extract source directory → site vendor id. `open-meteo` is `open_meteo` in the
# extract and `openmeteo` on the site; GIE is TWO sources sharing one site
# vendor — AGSI+ (storage, news, unavailability…) and ALSI (lng) are separate
# APIs on separate hosts, so a "one directory per source" assumption silently
# drops `lng`. Their slugs are disjoint; `_collisions` asserts that.
SOURCE_TO_VENDOR: dict[str, str] = {
    "elexon": "elexon",
    "entsoe": "entsoe",
    "entsog": "entsog",
    "gie_agsi": "gie",
    "gie_alsi": "gie",
    "neso": "neso",
    "open_meteo": "openmeteo",
}

# Numeric columns that are identifiers, coordinates, partition keys or flags —
# never measures. Their mean over time is meaningless and usually constant.
_DENY_EXACT = frozenset(
    {
        "latitude",
        "longitude",
        "regionid",
        "region_id",
        "id",
        "mrid",
        "year",
        "month",
        "day",
        "period",
        "settlement_period",
        "settlement_day",
        "data_set",
        "id_point_type",
    }
)
# Substring/suffix rejects. `direction` is excluded because a mean of compass
# bearings is invalid (0° and 359° average to 180°), not merely uninteresting.
_DENY_PATTERN = re.compile(
    r"(^is_|_id$|_eic$|_eic_code$|_number$|_version$|_run_id$|direction|_flag$|_index$)"
)

# Physical-unit suffixes in the gridflow silver naming convention. Used to
# PREFER a real measure among the survivors, never to reject.
_UNIT_TOKEN = re.compile(
    r"_(mw|mwh|gw|gwh|kw|kwh|hz|pct|percentage|eur|gbp|usd|mps|hpa|wm2|gco2|"
    r"mm|cm|kg_m3|therm|scm|bcm|c|k|m)(_|$)"
)

# NESO's regional feed mixes grain in one column: regionid 1–14 are the DNO
# licence areas, 15–17 are England/Scotland/Wales and 18 is GB. A mean over all
# eighteen averages the DNO regions together with aggregates that already
# contain them, so the same megawatt is counted twice. Keeping 1–14 is not a
# reading of the data — it is removing rows that are sums of other rows.
_DNO_REGIONS = frozenset(str(i) for i in range(1, 15))

# Datasets where the whole-file mean is not the right series, as
# `(source, dataset) -> (column, allowed values, caption label)`. Open-Meteo
# covers seven GB cities, so an unsliced mean would be a seven-city average
# under a page whose own copy says `location=london`. Absent from this table
# means "aggregate every row", the default.
SERIES_SLICES: dict[tuple[str, str], tuple[str, frozenset[str], str]] = {
    ("open_meteo", "forecast_demand"): ("location", frozenset({"london"}), "location=london"),
    ("open_meteo", "historical_demand"): ("location", frozenset({"london"}), "location=london"),
    ("neso", "regional_intensity"): ("regionid", _DNO_REGIONS, "14 DNO regions"),
    ("neso", "regional_intensity_fw24h"): ("regionid", _DNO_REGIONS, "14 DNO regions"),
    ("neso", "regional_intensity_fw48h"): ("regionid", _DNO_REGIONS, "14 DNO regions"),
}

_TOKEN_SPLIT = re.compile(r"[^a-z0-9]+")

_MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def resolve_extract_path(cli_arg: str | None) -> Path:
    """Extract root: CLI flag, then ``$GRIDFLOW_CHART_EXTRACT_PATH``, then default."""
    if cli_arg:
        return Path(cli_arg).expanduser().resolve()
    env_path = os.environ.get("GRIDFLOW_CHART_EXTRACT_PATH")
    if env_path:
        return Path(env_path).expanduser().resolve()
    return DEFAULT_EXTRACT


def series_path(site_dir: Path) -> Path:
    return site_dir / "data" / "chart-series.json"


def load_series(site_dir: Path) -> dict[str, dict]:
    """Committed series keyed ``"<vendor>/<slug>"``; empty when the file is absent.

    Absent is a normal state, not an error: a checkout without a refresh (CI,
    a fresh clone) builds every page with its seeded chart.
    """
    path = series_path(site_dir)
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(
            f"[gridflow-build] WARNING: {path.name} unreadable ({exc}); "
            "all snapshot charts fall back to seeded",
            file=sys.stderr,
        )
        return {}
    entries = payload.get("series")
    return entries if isinstance(entries, dict) else {}


def _pretty_date(iso: str) -> str:
    """``2026-08-01`` → ``1 Aug 2026``. Returns the input unchanged if unparseable."""
    try:
        d = date.fromisoformat(iso[:10])
    except ValueError:
        return iso
    return f"{d.day} {_MONTHS[d.month - 1]} {d.year}"


def _is_denied(column: str) -> bool:
    return column in _DENY_EXACT or bool(_DENY_PATTERN.search(column))


def _tokens(name: str) -> set[str]:
    return {t for t in _TOKEN_SPLIT.split(name.lower()) if t}


def rank_columns(
    value_columns: list[str], dataset: str, recorded: str | None
) -> list[tuple[str, str]]:
    """Plottable columns in preference order, as ``(column, reason)`` pairs.

    Preference: the extract's own recorded choice when it survives the denylist
    (it is the reviewed decision and reproduces the shipped charts), then a
    unit-suffixed column sharing a word with the dataset slug, then any other
    unit-suffixed column, then whatever is left in declared order.

    A list rather than a single pick because a column can look right and still
    carry no signal — ``lolpdrm``'s ``loss_of_load_probability`` is 0 across the
    whole window, and ``soso``'s ``trade_quantity_mw`` is 25 MW in every row.
    The caller walks this list and takes the first column that survives the
    guards, so those pages plot ``derated_margin_mw`` and ``trade_price``
    instead of falling back to a seeded chart they do not need.
    """
    candidates = [c for c in value_columns if not _is_denied(c)]
    if not candidates:
        return []
    slug_tokens = _tokens(dataset)
    ranked: list[tuple[str, str]] = []
    seen: set[str] = set()

    def add(column: str, reason: str) -> None:
        if column not in seen:
            seen.add(column)
            ranked.append((column, reason))

    if recorded and recorded in candidates:
        add(recorded, "extract charts-manifest")
    unit_cols = [c for c in candidates if _UNIT_TOKEN.search(c)]
    for c in unit_cols:
        if _tokens(c) & slug_tokens:
            add(c, "unit-suffixed, name matches dataset")
    for c in unit_cols:
        add(c, "unit-suffixed")
    for c in candidates:
        add(c, "first non-identifier column")
    return ranked


def _mean_per_timestamp(
    csv_path: Path,
    time_column: str,
    column: str,
    slice_on: tuple[str, frozenset[str], str] | None = None,
) -> list[float]:
    """Mean of ``column`` per distinct ``time_column`` value, in time order.

    Mean-per-timestamp is the aggregation the extract's own chart harness
    recorded and the 2026-08-16 charts shipped with; keeping it means the
    build reproduces those series rather than inventing a second convention.
    Rows whose value is blank or non-numeric are skipped, not zero-filled.
    ``slice_on`` is an optional ``(column, allowed, label)`` filter — see
    ``SERIES_SLICES``.
    """
    totals: dict[str, float] = defaultdict(float)
    counts: dict[str, int] = defaultdict(int)
    with csv_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            return []
        if time_column not in reader.fieldnames or column not in reader.fieldnames:
            return []
        if slice_on and slice_on[0] not in reader.fieldnames:
            return []
        for row in reader:
            if slice_on and row.get(slice_on[0]) not in slice_on[1]:
                continue
            raw = row.get(column)
            if raw in (None, "", "null", "NULL", "None"):
                continue
            try:
                value = float(raw)
            except ValueError:
                continue
            key = row.get(time_column) or ""
            if not key:
                continue
            totals[key] += value
            counts[key] += 1
    return [totals[k] / counts[k] for k in sorted(totals)]


def _downsample(values: list[float], limit: int = MAX_POINTS) -> list[float]:
    """Block-mean ``values`` down to at most ``limit`` points.

    Averaging rather than striding: the chart is a shape, and striding a
    5-second frequency series (28 800 points) would alias rather than summarise.
    """
    n = len(values)
    if n <= limit:
        return values
    out: list[float] = []
    for i in range(limit):
        lo = (i * n) // limit
        hi = max(((i + 1) * n) // limit, lo + 1)
        chunk = values[lo:hi]
        out.append(sum(chunk) / len(chunk))
    return out


def _distil_one(
    entry: dict, extract_root: Path, recorded: dict[str, str]
) -> tuple[dict | None, str]:
    """Build one series entry, or ``(None, reason)`` when it must stay seeded."""
    source, dataset = entry["source"], entry["dataset"]
    ranked = rank_columns(entry.get("value_columns") or [], dataset, recorded.get("column"))
    if not ranked:
        return None, "every value column is an identifier, coordinate or flag"
    csv_name = Path(entry["csv"].replace("\\", "/")).name
    csv_path = extract_root / source / csv_name
    if not csv_path.is_file():
        return None, f"csv not found: {csv_path.name}"
    # The two extract manifests disagree on the time grain for 20 Elexon
    # datasets: manifest.json names `settlement_date` where the chart harness
    # used `timestamp_utc`. The coarse one collapses 11 989 half-hourly rows to
    # five daily means, so prefer the harness's column — it is the reviewed
    # choice, same as `plotted_column`.
    time_column = recorded.get("time_column") or entry.get("time_column") or ""

    slice_on = SERIES_SLICES.get((source, dataset))

    column = why = ""
    raw: list[float] = []
    rejected: list[str] = []
    for candidate, reason in ranked:
        series = _mean_per_timestamp(csv_path, time_column, candidate, slice_on)
        if len(series) < MIN_POINTS:
            rejected.append(f"{candidate}: {len(series)} point(s)")
            continue
        # Constant-series guard, BEFORE rounding: a flat line is not a chart,
        # and it is the signature of an identifier or a column that is simply
        # zero across the window.
        if max(series) == min(series):
            rejected.append(f"{candidate}: constant")
            continue
        column, why, raw = candidate, reason, series
        break
    if not column:
        return None, "no column with usable variation — " + "; ".join(rejected)

    values = [round(v, 3) for v in _downsample(raw)]
    coverage = entry.get("coverage") or {}
    start, end = coverage.get("min", ""), coverage.get("max", "")
    return (
        {
            "source": source,
            "dataset": dataset,
            "column": column,
            "column_reason": why,
            "time_column": time_column,
            "slice": slice_on[2] if slice_on else "",
            "aggregation": (
                f"mean of {column} per {time_column}"
                + (f" across {slice_on[2]}" if slice_on else "")
            ),
            "points": len(values),
            "points_raw": len(raw),
            "downsampled": len(values) < len(raw),
            "start": start,
            "end": end,
            "start_label": _pretty_date(start),
            "end_label": _pretty_date(end),
            "values": values,
        },
        why,
    )


def _collisions(built: dict[str, dict], key: str, source: str) -> str | None:
    prior = built.get(key)
    if prior and prior["source"] != source:
        return f"{key}: {prior['source']} and {source} both claim this slug"
    return None


def distil(extract_root: Path) -> tuple[dict, list[str], list[str]]:
    """Read the extract and return ``(payload, notes, problems)``.

    ``payload`` is what gets written to ``site/hifi/data/chart-series.json``.
    ``notes`` records every dataset that was NOT turned into a chart and why —
    counted and reported, never silently dropped.
    """
    manifest_path = extract_root / "manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"no extract manifest at {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    # The extract's own chart harness recorded, per dataset, which column it
    # plotted and which time column it grouped by (the latter only inside the
    # `aggregation` sentence, e.g. "mean of national_demand_mw per timestamp_utc").
    recorded_columns: dict[tuple[str, str], dict[str, str]] = {}
    charts_manifest = extract_root / "charts" / "charts-manifest.json"
    if charts_manifest.is_file():
        for spark in json.loads(charts_manifest.read_text(encoding="utf-8")).get("sparklines", []):
            per = re.search(r"\bper (\S+)$", spark.get("aggregation", ""))
            recorded_columns[(spark["source"], spark["dataset"])] = {
                "column": spark.get("plotted_column", ""),
                "time_column": per.group(1) if per else "",
            }

    built: dict[str, dict] = {}
    notes: list[str] = []
    problems: list[str] = []
    for entry in manifest.get("series", []):
        source, dataset = entry["source"], entry["dataset"]
        if not entry.get("chartable"):
            notes.append(f"{source}/{dataset}: not chartable ({entry.get('status', 'unknown')})")
            continue
        vendor = SOURCE_TO_VENDOR.get(source)
        if vendor is None:
            problems.append(f"{source}/{dataset}: no site vendor mapped for source {source!r}")
            continue
        recorded = recorded_columns.get((source, dataset), {})
        series, why = _distil_one(entry, extract_root, recorded)
        if series is None:
            notes.append(f"{source}/{dataset}: {why}")
            continue
        recorded_column = recorded.get("column")
        if recorded_column and recorded_column != series["column"]:
            problems.append(
                f"{source}/{dataset}: extract picked {recorded_column!r}; "
                f"using {series['column']!r} ({series['column_reason']})"
            )
        key = f"{vendor}/{dataset}"
        clash = _collisions(built, key, source)
        if clash:
            problems.append(clash)
            continue
        built[key] = series

    window = manifest.get("window") or {}
    payload = {
        "generated_from": str(extract_root),
        "extract_generated_by": manifest.get("generated_by", ""),
        "window": window,
        "window_label": (
            f"{_pretty_date(window.get('start', ''))} – {_pretty_date(window.get('end', ''))}"
            if window
            else ""
        ),
        "count": len(built),
        "series": built,
    }
    return payload, notes, problems


# Collapses an indented `"values": [ ... ]` block back onto one line. This file
# is regenerated and re-committed on every extract, so a diff must be readable:
# one changed line per series, not 9 800 changed lines of one number each.
_VALUES_BLOCK_RE = re.compile(r'("values": \[)([^\]]*)(\])')


def write_series(payload: dict, site_dir: Path) -> Path:
    """Write the distilled payload, sorted and newline-terminated for stable diffs."""
    path = series_path(site_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
    text = _VALUES_BLOCK_RE.sub(
        lambda m: m.group(1) + ", ".join(m.group(2).split()).replace(",,", ",") + m.group(3),
        text,
    )
    path.write_text(text + "\n", encoding="utf-8")
    return path
