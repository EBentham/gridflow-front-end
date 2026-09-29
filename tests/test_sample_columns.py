"""A sample frame can set its print order, as a Polars ``.select`` would."""

from __future__ import annotations

from pathlib import Path

import polars as pl
import pytest

from gridflow_front_end import sample


def _silver(tmp_path: Path) -> Path:
    table = tmp_path / "elexon" / "demo"
    table.mkdir(parents=True)
    pl.DataFrame(
        {"a": range(8), "b": range(8), "level": range(8), "ingested_at": range(8)}
    ).write_parquet(table / "part.parquet")
    return tmp_path


def test_named_columns_print_first_and_the_rest_keep_silver_order(tmp_path: Path) -> None:
    df = sample.select_rows(_silver(tmp_path), "elexon/demo", {"columns": ["level"]})
    assert df.columns == ["level", "a", "b", "ingested_at"]


def test_no_columns_keeps_silver_order(tmp_path: Path) -> None:
    assert sample.select_rows(_silver(tmp_path), "elexon/demo", {}).columns == [
        "a", "b", "level", "ingested_at"
    ]


def test_an_unknown_column_is_an_error(tmp_path: Path) -> None:
    with pytest.raises(sample.SampleError):
        sample.select_rows(_silver(tmp_path), "elexon/demo", {"columns": ["nope"]})
