"""gridflow-sample: pick a dataset page's eight real silver rows and commit them.

For every vault note on the new dataset template, read ``page.record.select``
(a filter, an optional de-duplication and an order), run it against local
silver (read only), and write ``site/hifi/data/samples/<vendor>/<dataset>.json``:
every column in silver order with its dtype, and the eight rows with each value
formatted exactly as Polars prints it (the page's "values formatted by Polars").
``gridflow-build`` renders the record and the "Eight rows" table from that file.

Usage
-----
    gridflow-sample                               # every note with page.record
    gridflow-sample --dataset elexon/fuelhh       # just one (repeatable)
    gridflow-sample --dry-run                     # print the rows, write nothing

Needs the ``distil`` extra: ``uv run --extra distil gridflow-sample``.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import polars as pl

from gridflow_front_end import artefacts
from gridflow_front_end.distil import _filter_expr, coerce_value
from gridflow_front_end.page_fields import parse_page_fields
from gridflow_front_end.paths import SITE_DIR, resolve_silver_path, resolve_vault_path

GENERATED_BY = "gridflow-sample"
ROWS = 8


class SampleError(Exception):
    """A record selection cannot be run against the silver on disk."""


def dtype_label(dtype: pl.DataType) -> str:
    """Polars' dtype as the schema shows it: ``Datetime(us, UTC)``, ``Int32``, ``String``."""
    if isinstance(dtype, pl.Datetime):
        if dtype.time_zone:
            return f"Datetime({dtype.time_unit}, {dtype.time_zone})"
        return f"Datetime({dtype.time_unit})"
    return str(dtype)


def _scan(silver_root: Path, silver: str) -> pl.LazyFrame:
    table_dir = silver_root / silver
    if not table_dir.is_dir():
        raise SampleError(f"silver table not found: {table_dir}")
    files = sorted(table_dir.rglob("*.parquet"))
    if not files:
        raise SampleError(f"no parquet files under {table_dir}")
    # Newest file first: its schema (the current transformer's columns, in
    # order) is the reference; older files lacking a column get nulls. A column
    # can be all-null (type Null) in one daily file and String in the next
    # (ENTSOG generic silver), so frames are stacked to a common supertype.
    columns = list(pl.read_parquet_schema(files[-1]))
    frames = [pl.scan_parquet(f, hive_partitioning=False) for f in files[::-1]]
    return pl.concat(frames, how="diagonal_relaxed").select(columns)


# Polars' markdown table is read back by splitting rows on "|" and cells on line ends, so a value
# holding either (ENTSOG point lists such as "Isle of Grain|Milford Haven") would split its own
# cell. They print as private-use stand-ins and are put back once each cell is cut out.
_MASKS = (("|", "\ue000"), ("\r\n", "\ue001"), ("\n", "\ue002"), ("\r", "\ue003"))
_STAND_INS = "[\ue000-\ue003]"


def _mask(expr: pl.Expr) -> pl.Expr:
    for raw, stand_in in _MASKS:
        expr = expr.str.replace_all(raw, stand_in, literal=True)
    return expr


def _unmask(cell: str) -> str:
    for raw, stand_in in _MASKS:
        cell = cell.replace(stand_in, raw)
    return cell


def _masked(df: pl.DataFrame) -> pl.DataFrame:
    """``df`` with ``|`` and line ends masked in its String and List(String) columns."""
    exprs: list[pl.Expr] = []
    for name, dtype in df.schema.items():
        if dtype == pl.String:
            text, masked = df[name], _mask(pl.col(name))
        elif isinstance(dtype, pl.List) and dtype.inner == pl.String:
            text, masked = df[name].list.join(""), pl.col(name).list.eval(_mask(pl.element()))
        else:
            continue
        if text.str.contains(_STAND_INS).any():
            raise SampleError(f"column {name!r} holds a character the table reader uses as a mask")
        exprs.append(masked)
    return df.with_columns(exprs) if exprs else df


def polars_text(df: pl.DataFrame) -> list[list[str]]:
    """Every cell as Polars prints it in a table (no shape, no dtype row).

    A ``|`` or a line end inside a value is kept: it is masked while Polars prints and restored in
    the cell, so the cell reads as Polars prints the value.

    Args:
        df: The eight sample rows, in print order.

    Returns:
        One list of cell strings per row.

    Raises:
        SampleError: The printed table cannot be read back cell for cell.
    """
    df = _masked(df)
    with pl.Config(
        tbl_formatting="ASCII_MARKDOWN",
        tbl_hide_column_data_types=True,
        tbl_hide_dataframe_shape=True,
        tbl_cols=-1,
        tbl_rows=-1,
        tbl_width_chars=60000,
        fmt_str_lengths=1000,
        fmt_float="mixed",
    ):
        text = str(df)
    lines = [ln for ln in text.splitlines() if ln.startswith("|")]
    head = [c.strip() for c in lines[0].strip("|").split("|")]
    if head != df.columns:
        raise SampleError(f"could not read Polars' table header back: {head}")
    body = [[_unmask(c.strip()) for c in ln.strip("|").split("|")] for ln in lines[2:]]
    if len(body) != df.height or any(len(b) != df.width for b in body):
        raise SampleError("Polars' table cannot be read back cell for cell")
    return body


def select_rows(silver_root: Path, silver: str, select: Mapping[str, Any]) -> pl.DataFrame:
    """Run a note's ``record.select`` against silver; exactly eight rows or an error."""
    lf = _scan(silver_root, silver)
    schema = lf.collect_schema()
    for i, flt in enumerate(select.get("filter", [])):
        col = flt.get("column")
        if col not in schema:
            raise SampleError(f"select.filter[{i}]: column {col!r} not in silver")
        typed = dict(flt)
        if "value" in typed:
            typed["value"] = coerce_value(typed["value"], schema[col])
        lf = lf.filter(_filter_expr(typed))
    df = lf.collect()
    if "dedup" in select:
        dd = select["dedup"]
        df = df.sort(dd["order_by"], nulls_last=False, maintain_order=True).unique(
            subset=dd["on"], keep="last", maintain_order=True
        )
    order = select.get("order_by", [])
    if order:
        df = df.sort(order, maintain_order=True)
    if df.height != ROWS:
        raise SampleError(f"select picks {df.height} rows; it must pick exactly {ROWS}")
    # A Polars ``.select`` order, as a reader would print the table: the named columns first, every
    # other column after them in silver's order, so the frame folds the ones that matter least.
    first = list(select.get("columns", []))
    missing = [c for c in first if c not in df.columns]
    if missing:
        raise SampleError(f"select.columns: {missing} not in silver")
    return df.select(first + [c for c in df.columns if c not in first])


def build_payload(
    vendor: str,
    dataset: str,
    silver: str,
    select: Mapping[str, Any],
    mark: Mapping[str, Any],
    silver_root: Path,
) -> dict[str, Any]:
    """Select, format and describe one dataset's eight rows."""
    df = select_rows(silver_root, silver, select)
    text = polars_text(df)
    nulls = df.select(pl.all().is_null()).rows()
    rows = [
        [None if nulls[r][c] else text[r][c] for c in range(df.width)] for r in range(df.height)
    ]
    marked = [
        r
        for r in range(df.height)
        if all(k in df.columns and rows[r][df.columns.index(k)] == str(v) for k, v in mark.items())
    ]
    if mark and len(marked) != 1:
        raise SampleError(
            f"record.mark {dict(mark)} matches {len(marked)} of the eight rows; needs 1"
        )
    return {
        "dataset": f"{vendor}/{dataset}",
        "generated_by": GENERATED_BY,
        "select_sha256": artefacts.select_digest(silver, select),
        "silver": silver,
        "columns": [
            {
                "name": name,
                "dtype": dtype_label(dtype),
                "lineage": name in artefacts.LINEAGE_COLUMNS,
            }
            for name, dtype in df.schema.items()
        ],
        "rows": rows,
        "mark": marked[0] if mark else None,
    }


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for ``gridflow-sample``."""
    parser = argparse.ArgumentParser(prog="gridflow-sample", description=__doc__.split("\n")[0])
    parser.add_argument(
        "--silver-path", default=None, help="Silver root (default C:/gridflow-data/silver)."
    )
    parser.add_argument("--vault-path", default=None, help="Vault mirror root (default ./vault).")
    parser.add_argument(
        "--dataset", action="append", default=[], help="<vendor>/<dataset>; repeatable."
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the rows, write nothing.")
    args = parser.parse_args(argv)
    silver_root = resolve_silver_path(args.silver_path)
    vault = resolve_vault_path(args.vault_path)
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    wanted = set(args.dataset)
    failures = 0
    for note in sorted(vault.glob("*/*.md")):
        key = f"{note.parent.name}/{note.stem}"
        if wanted and key not in wanted:
            continue
        fields, errors = parse_page_fields(note.read_text(encoding="utf-8"))
        if not fields.present or not fields.record.select:
            continue
        if errors:
            print(f"  FAIL {key}: {errors}", file=sys.stderr)
            failures += 1
            continue
        silver = artefacts.sample_silver(
            note.parent.name, note.stem, fields.record.select, fields.chart
        )
        try:
            payload = build_payload(
                note.parent.name,
                note.stem,
                silver,
                fields.record.select,
                fields.record.mark,
                silver_root,
            )
        except (SampleError, pl.exceptions.PolarsError) as exc:
            print(f"  FAIL {key}: {exc}", file=sys.stderr)
            failures += 1
            continue
        print(f"  {key}: {len(payload['columns'])} columns, mark row {payload['mark']}")
        if args.dry_run:
            for row in payload["rows"]:
                print("   ", row)
            continue
        out = artefacts.sample_path(SITE_DIR, note.parent.name, note.stem)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(artefacts.dumps(payload), encoding="utf-8")
        print(f"  wrote {out.relative_to(SITE_DIR.parent.parent)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
