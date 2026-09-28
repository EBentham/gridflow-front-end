"""gridflow-distil: run chart specs against local silver, write committed series.

For every dataset with a chart spec (``chart_spec``), read its silver parquet
directly, apply the spec (filter, de-duplicate, window, group, bucket,
aggregate) and write ``site/hifi/data/series/<vendor>/<dataset>.json``. Commit
those files: ``gridflow-build`` renders charts from them and never reads
silver, so CI (a bare checkout with no silver and no polars) builds the same
pages as a local build.

Usage
-----
    gridflow-distil                                   # every dataset with a spec
    gridflow-distil --dataset elexon/fuelhh           # just one (repeatable)
    gridflow-distil --silver-path D:/silver --dry-run # report, write nothing

Needs the ``distil`` extra: ``uv run --extra distil gridflow-distil``.

A spec with ``"type": "none"`` is a recorded decision that the dataset has no
chart; the distil writes nothing for it and deletes a stale series file if
one is left over. Datasets without a spec are untouched: no spec, no chart.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import polars as pl

from gridflow_front_end import chart_spec
from gridflow_front_end.page_fields import parse_page_fields
from gridflow_front_end.paths import SITE_DIR, resolve_silver_path, resolve_vault_path

GENERATED_BY = "gridflow-distil"
_BUCKET_LABELS = {"30m": "30 minutes", "1h": "1 hour", "1d": "1 day"}


class DistilError(Exception):
    """A spec cannot be distilled against the silver on disk."""


@dataclass(frozen=True)
class SpecSource:
    """One dataset's resolved spec and where it came from."""

    vendor: str
    dataset: str
    spec: dict[str, Any]
    origin: str

    @property
    def key(self) -> str:
        """``<vendor>/<dataset>``."""
        return f"{self.vendor}/{self.dataset}"


def _iso(value: dt.datetime | dt.date) -> str:
    """ISO text for a naive-UTC datetime (``...Z``) or a date."""
    if isinstance(value, dt.datetime):
        return value.strftime("%Y-%m-%dT%H:%M:%SZ")
    return value.isoformat()


def _round(value: float | None) -> float | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    return round(float(value), 3)


def coerce_value(value: Any, dtype: pl.DataType) -> Any:
    """ISO strings in a filter become dates or datetimes when the column is temporal.

    YAML and JSON carry dates as strings; Polars will not compare a Date
    column with a string. The time column is naive UTC after ``_scan``.
    """
    if isinstance(value, list):
        return [coerce_value(v, dtype) for v in value]
    if not isinstance(value, str):
        return value
    if dtype == pl.Date:
        return dt.date.fromisoformat(value)
    if isinstance(dtype, pl.Datetime):
        parsed = dt.datetime.fromisoformat(value)
        if dtype.time_zone and parsed.tzinfo is None:
            return parsed.replace(tzinfo=dt.UTC)
        if not dtype.time_zone and parsed.tzinfo is not None:
            return parsed.astimezone(dt.UTC).replace(tzinfo=None)
        return parsed
    return value


def _filter_expr(flt: Mapping[str, Any]) -> pl.Expr:
    col = pl.col(flt["column"])
    op = flt["op"]
    value = flt.get("value")
    if op == "eq":
        return col == value
    if op == "ne":
        return col != value
    if op == "in":
        return col.is_in(value)
    if op == "not_in":
        return ~col.is_in(value)
    if op == "not_null":
        return col.is_not_null()
    if op == "is_null":
        return col.is_null()
    if op == "gt":
        return col > value
    if op == "ge":
        return col >= value
    if op == "lt":
        return col < value
    if op == "le":
        return col <= value
    raise DistilError(f"unsupported filter op {op!r}")


def _needed_columns(spec: Mapping[str, Any]) -> list[str]:
    cols: list[str] = []
    for key in ("time", "value", "group"):
        if key in spec:
            cols.append(spec[key])
    for flt in spec.get("filter", []):
        cols.append(flt["column"])
    if "dedup" in spec:
        cols.extend(spec["dedup"]["on"])
        cols.append(spec["dedup"]["order_by"])
    return list(dict.fromkeys(cols))


def _scan(silver_root: Path, spec: Mapping[str, Any]) -> tuple[pl.LazyFrame, int]:
    table_dir = silver_root / spec["silver"]
    if not table_dir.is_dir():
        raise DistilError(f"silver table not found: {table_dir}")
    files = sorted(table_dir.rglob("*.parquet"))
    if not files:
        raise DistilError(f"no parquet files under {table_dir}")
    # Partition folders (year=/month=) are not columns the spec may use, and
    # files written by older dataset versions may lack newer columns.
    lf = pl.scan_parquet(
        files,
        hive_partitioning=False,
        missing_columns="insert",
        extra_columns="ignore",
    )
    schema = lf.collect_schema()
    missing = [c for c in _needed_columns(spec) if c not in schema]
    if missing:
        raise DistilError(f"{spec['silver']}: column(s) not in silver: {missing}")
    lf = lf.select(_needed_columns(spec))
    time_col = spec.get("time")
    dtype = schema.get(time_col) if time_col else None
    if isinstance(dtype, pl.Datetime) and dtype.time_zone is not None:
        # Normalise to naive UTC inside polars: a tz-aware value crossing into
        # Python needs the IANA database, which Windows does not ship.
        lf = lf.with_columns(
            pl.col(time_col).dt.convert_time_zone("UTC").dt.replace_time_zone(None)
        )
    return lf, len(files)


def _agg_expr(spec: Mapping[str, Any]) -> pl.Expr:
    agg = spec["aggregation"]
    if agg == "count":
        return pl.len().alias("__v")
    col = pl.col(spec["value"])
    exprs = {
        "sum": col.sum(),
        "mean": col.mean(),
        "min": col.min(),
        "max": col.max(),
        "last": col.last(),
    }
    return exprs[agg].alias("__v")


def _apply_groups(df: pl.DataFrame, spec: Mapping[str, Any]) -> tuple[pl.DataFrame, list[str]]:
    """Add the ``__g`` series label column; report raw values the map missed."""
    if "group" not in spec:
        return df.with_columns(pl.lit(spec.get("value", "count")).alias("__g")), []
    if "group_null" in spec:
        # a null group is a real category (a unit with no declared fuel type),
        # kept under its own label instead of being dropped
        label = spec["group_null"]
        df = df.with_columns(pl.col(spec["group"]).cast(pl.String).fill_null(label))
        if spec.get("group_map"):
            spec = {**spec, "group_map": {**spec["group_map"], label: label}}
    raw = pl.col(spec["group"]).cast(pl.String)
    gmap = spec.get("group_map")
    if not gmap:
        return df.with_columns(raw.alias("__g")), []
    present = df.get_column(spec["group"]).cast(pl.String).unique().drop_nulls().to_list()
    unmapped = sorted(v for v in present if v not in gmap)
    default = spec.get("group_default")
    fallback: pl.Expr = pl.lit(default) if default else raw
    return df.with_columns(raw.replace_strict(gmap, default=fallback).alias("__g")), unmapped


def _order_labels(labels: Sequence[str], spec: Mapping[str, Any]) -> list[str]:
    order = [s for s in spec.get("series_order", []) if s in labels]
    return order + sorted(set(labels) - set(order))


def distil_spec(spec: Mapping[str, Any], silver_root: Path) -> dict[str, Any]:
    """Run one validated spec against silver.

    Args:
        spec: A spec that ``chart_spec.validate_spec`` accepts (not ``none``).
        silver_root: The silver root (``C:/gridflow-data/silver``).

    Returns:
        The chart payload: ``x_kind``, ``x``, ``series``, ``window`` and
        ``provenance``. The caller adds identity and the spec digest.

    Raises:
        DistilError: The silver table or a column is missing, or the spec
            selects no rows, or the series is longer than ``max_points``.
    """
    lf, n_files = _scan(silver_root, spec)
    rows_read = lf.select(pl.len()).collect().item()
    schema = lf.collect_schema()
    for flt in spec.get("filter", []):
        typed = dict(flt)
        if "value" in typed:
            typed["value"] = coerce_value(typed["value"], schema[flt["column"]])
        lf = lf.filter(_filter_expr(typed))
    is_time = spec["type"] in chart_spec.TIME_CHART_TYPES
    time_col = spec.get("time")

    df = lf.collect()
    rows_matched = df.height
    if rows_matched == 0:
        raise DistilError(f"{spec['silver']}: the filters select no rows")
    provenance: dict[str, Any] = {
        "silver": spec["silver"],
        "files": n_files,
        "rows_read": rows_read,
        "rows_matched": rows_matched,
    }

    window: dict[str, str] | None = None
    if is_time:
        assert time_col is not None
        dtype = df.schema[time_col]
        if not dtype.is_temporal():
            raise DistilError(f"time column {time_col!r} is {dtype}, not a date or datetime")
        first, last = df.get_column(time_col).min(), df.get_column(time_col).max()
        provenance["silver_first"] = _iso(first)
        provenance["silver_last"] = _iso(last)
        win = spec["window"]
        if "last" in win:
            n, unit = int(win["last"][:-1]), win["last"][-1]
            span = dt.timedelta(days=n) if unit == "d" else dt.timedelta(hours=n)
            start = last - span
            df = df.filter(pl.col(time_col) > start)
            window = {
                "rule": f"last {win['last']} of silver",
                "start": _iso(start),
                "end": _iso(last),
            }
        else:
            lo = dt.date.fromisoformat(win["start"])
            hi = dt.date.fromisoformat(win["end"]) + dt.timedelta(days=1)
            if dtype == pl.Date:
                bounds: tuple[Any, Any] = (lo, hi)
            else:
                bounds = (dt.datetime.combine(lo, dt.time()), dt.datetime.combine(hi, dt.time()))
            df = df.filter((pl.col(time_col) >= bounds[0]) & (pl.col(time_col) < bounds[1]))
            window = {"rule": "fixed", "start": win["start"], "end": win["end"]}

    if "dedup" in spec:
        before = df.height
        df = df.sort(spec["dedup"]["order_by"], nulls_last=False, maintain_order=True).unique(
            subset=spec["dedup"]["on"], keep="last", maintain_order=True
        )
        provenance["duplicates_dropped"] = before - df.height

    if "value" in spec:
        before = df.height
        df = df.filter(pl.col(spec["value"]).is_not_null())
        provenance["null_values_dropped"] = before - df.height
    if df.height == 0:
        raise DistilError(f"{spec['silver']}: no rows left after window, dedup and null filtering")
    provenance["rows_used"] = df.height

    df, unmapped = _apply_groups(df, spec)
    if unmapped:
        provenance["unmapped_groups"] = unmapped
    null_groups = df.get_column("__g").null_count()
    if null_groups:
        df = df.filter(pl.col("__g").is_not_null())
        provenance["null_groups_dropped"] = null_groups

    max_points = spec.get("max_points", chart_spec.DEFAULT_MAX_POINTS)
    if is_time:
        assert time_col is not None
        df = df.sort(time_col, maintain_order=True)
        bucket = spec.get("time_bucket")
        x_expr = pl.col(time_col).dt.truncate(bucket) if bucket else pl.col(time_col)
        if bucket:
            provenance["time_bucket"] = _BUCKET_LABELS[bucket]
        agg = (
            df.with_columns(x_expr.alias("__x"))
            .group_by(["__x", "__g"], maintain_order=True)
            .agg(_agg_expr(spec))
        )
        xs = sorted(agg.get_column("__x").unique().to_list())
        if len(xs) > max_points:
            raise DistilError(
                f"{len(xs)} time points exceed max_points={max_points}; add a time_bucket"
            )
        labels = _order_labels(agg.get_column("__g").unique().to_list(), spec)
        lookup = {(row[0], row[1]): row[2] for row in agg.iter_rows()}
        series = [
            {"key": label, "values": [_round(lookup.get((x, label))) for x in xs]}
            for label in labels
        ]
        return {
            "x_kind": "time",
            "x": [_iso(x) for x in xs],
            "series": series,
            "window": window,
            "provenance": provenance,
        }

    agg = df.group_by("__g", maintain_order=True).agg(_agg_expr(spec))
    order = spec.get("sort", "value_desc")
    if order == "label":
        agg = agg.sort("__g")
    else:
        agg = agg.sort(["__v", "__g"], descending=[order == "value_desc", False])
    if "limit" in spec:
        provenance["categories_total"] = agg.height
        agg = agg.head(spec["limit"])
    if agg.height > max_points:
        raise DistilError(f"{agg.height} categories exceed max_points={max_points}")
    return {
        "x_kind": "category",
        "x": [str(g) for g in agg.get_column("__g").to_list()],
        "series": [
            {
                "key": spec.get("value", "count"),
                "values": [_round(v) for v in agg.get_column("__v").to_list()],
            }
        ],
        "window": None,
        "provenance": provenance,
    }


def build_payload(source: SpecSource, silver_root: Path) -> dict[str, Any]:
    """Distil one dataset and wrap the chart with identity and provenance."""
    chart = distil_spec(source.spec, silver_root)
    return {
        "dataset": source.key,
        "generated_by": GENERATED_BY,
        "spec_origin": source.origin,
        "spec_sha256": chart_spec.spec_digest(source.spec),
        "type": source.spec["type"],
        "unit": source.spec["unit"],
        "caption": source.spec.get("caption", ""),
        "value_column": source.spec.get("value"),
        "aggregation": source.spec["aggregation"],
        "window": chart["window"],
        "provenance": chart["provenance"],
        "spec": source.spec,
        "x_kind": chart["x_kind"],
        "x": chart["x"],
        "series": chart["series"],
    }


def dumps_payload(payload: Mapping[str, Any]) -> str:
    """Serialise a payload one key per line and one series per line.

    The files are re-committed after every distil, so a diff should read as
    "these series changed", not as thousands of one-number lines.
    """

    def one(value: object) -> str:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(", ", ": "))

    keys = list(payload)
    lines = ["{"]
    for i, key in enumerate(keys):
        comma = "," if i < len(keys) - 1 else ""
        value = payload[key]
        if key == "series" and isinstance(value, list):
            lines.append(f"  {json.dumps(key)}: [")
            for j, item in enumerate(value):
                lines.append(f"    {one(item)}{',' if j < len(value) - 1 else ''}")
            lines.append(f"  ]{comma}")
        else:
            lines.append(f"  {json.dumps(key)}: {one(value)}{comma}")
    lines.append("}")
    return "\n".join(lines) + "\n"


def discover_specs(
    site_dir: Path, vault_path: Path
) -> tuple[list[SpecSource], list[str], list[str]]:
    """Every dataset with a spec, from vault notes and the staging directory.

    Returns:
        ``(sources, errors, notes)``. Errors are invalid specs or unreadable
        files; notes are non-fatal (a staged spec shadowed by a vault one).
    """
    candidates: set[tuple[str, str]] = set()
    staging = chart_spec.staging_dir(site_dir)
    if staging.is_dir():
        candidates |= {(p.parent.name, p.stem) for p in staging.glob("*/*.json")}
    vault_charts: dict[tuple[str, str], dict[str, Any]] = {}
    errors: list[str] = []
    if vault_path.is_dir():
        for note in sorted(vault_path.glob("*/*.md")):
            fields, page_errors = parse_page_fields(note.read_text(encoding="utf-8"))
            key = (note.parent.name, note.stem)
            errors.extend(f"{key[0]}/{key[1]}: {e}" for e in page_errors)
            if fields.chart is not None:
                vault_charts[key] = fields.chart
                candidates.add(key)
    sources: list[SpecSource] = []
    notes: list[str] = []
    for vendor, dataset in sorted(candidates):
        try:
            spec, origin, spec_notes = chart_spec.resolve_spec(
                site_dir, vendor, dataset, vault_charts.get((vendor, dataset))
            )
        except (ValueError, TypeError) as exc:
            errors.append(str(exc))
            continue
        notes.extend(spec_notes)
        if spec is None:
            continue
        problems = chart_spec.validate_spec(spec)
        if problems:
            errors.extend(f"{vendor}/{dataset}: {p}" for p in problems)
            continue
        sources.append(SpecSource(vendor, dataset, spec, origin))
    return sources, errors, notes


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for ``gridflow-distil``."""
    parser = argparse.ArgumentParser(prog="gridflow-distil", description=__doc__.split("\n")[0])
    parser.add_argument(
        "--silver-path",
        default=None,
        help="Silver root (default C:/gridflow-data/silver or $GRIDFLOW_SILVER_PATH).",
    )
    parser.add_argument(
        "--vault-path",
        default=None,
        help="Vault root, flat <vendor>/<slug>.md (default: the repo mirror).",
    )
    parser.add_argument(
        "--dataset",
        action="append",
        default=[],
        metavar="VENDOR/SLUG",
        help="Distil only this dataset; repeatable.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Distil and report, write nothing.")
    args = parser.parse_args(argv)

    silver_root = resolve_silver_path(args.silver_path)
    vault_path = resolve_vault_path(args.vault_path)
    print(f"[gridflow-distil] silver: {silver_root}")
    print(f"[gridflow-distil] vault:  {vault_path}")
    sources, errors, notes = discover_specs(SITE_DIR, vault_path)
    for note in notes:
        print(f"  NOTE: {note}")
    if args.dataset:
        wanted = set(args.dataset)
        unknown = wanted - {s.key for s in sources}
        errors.extend(f"{k}: no valid chart spec found" for k in sorted(unknown))
        sources = [s for s in sources if s.key in wanted]
    if errors:
        print(f"[gridflow-distil] {len(errors)} spec error(s):", file=sys.stderr)
        for err in errors:
            print(f"  ERROR: {err}", file=sys.stderr)
        return 1

    failures = 0
    for source in sources:
        out = chart_spec.series_path(SITE_DIR, source.vendor, source.dataset)
        if source.spec["type"] == "none":
            if out.is_file() and not args.dry_run:
                out.unlink()
                print(f"  {source.key}: no chart (spec type none); removed stale {out.name}")
            else:
                print(f"  {source.key}: no chart (spec type none)")
            continue
        try:
            payload = build_payload(source, silver_root)
        except DistilError as exc:
            failures += 1
            print(f"  FAIL {source.key}: {exc}", file=sys.stderr)
            continue
        prov = payload["provenance"]
        span = (
            f"{payload['window']['start']} .. {payload['window']['end']}"
            if payload["window"]
            else "no time axis"
        )
        print(
            f"  {source.key} ({source.origin}): {len(payload['series'])} series x "
            f"{len(payload['x'])} points, {prov['rows_used']} rows used, {span}"
        )
        if prov.get("unmapped_groups"):
            print(f"    NOTE: group values not in group_map: {prov['unmapped_groups']}")
        if not args.dry_run:
            out.parent.mkdir(parents=True, exist_ok=True)
            # LF on every platform so the committed bytes do not depend on
            # the machine that ran the distil.
            out.write_text(dumps_payload(payload), encoding="utf-8", newline="\n")
    written = len(sources) - failures
    verb = "would write" if args.dry_run else "wrote"
    print(f"[gridflow-distil] {verb} {written} series file(s); {failures} failure(s)")
    if not args.dry_run and written:
        print(
            "[gridflow-distil] commit site/hifi/data/series/: CI builds from it, not from silver."
        )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
