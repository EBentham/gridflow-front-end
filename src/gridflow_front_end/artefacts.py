"""Committed page artefacts beside the chart series: sample rows and demo notebooks.

A dataset page on the new template shows three things read from real data:
the chart (``chart_spec`` / ``gridflow-distil``), the silver record and its
eight rows, and the demo notebook with its outputs. Each is produced locally
from real data by a read-only command and committed; ``gridflow-build``
renders from the committed file and never touches silver or a kernel, so CI
builds from a bare checkout.

- ``site/hifi/data/samples/<vendor>/<dataset>.json``: written by
  ``gridflow-sample`` (``sample.py``, the ``distil`` extra) from local silver,
  every value formatted by Polars.
- ``site/hifi/data/notebooks/<vendor>/<dataset>.json`` plus its plot image(s):
  written by ``scripts/run_notebooks.py``, run with the gridflow_models
  interpreter, which executes the cells for real on the ``gridflow_models``
  kernel.

Each file records the digest of the note fields it was made from; the build
fails when the note changes and the artefact was not regenerated. This module
is stdlib-only: the build, the sample command and the notebook runner (a
different interpreter) all import it.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

SETUP_CELL = "from gridflow_models import setup_notebook\ndata, models, common = setup_notebook()"
KERNEL = "gridflow_models"
# Added to every silver row by the silver base transformer; shown under one label.
LINEAGE_COLUMNS = (
    "event_time",
    "available_at",
    "source_run_id",
    "dataset_version",
    "vintage_policy",
)


def _digest(payload: object) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def samples_dir(site_dir: Path) -> Path:
    """Committed sample rows, one file per dataset."""
    return site_dir / "data" / "samples"


def notebooks_dir(site_dir: Path) -> Path:
    """Committed executed notebooks, one JSON file (plus images) per dataset."""
    return site_dir / "data" / "notebooks"


def sample_path(site_dir: Path, vendor: str, dataset: str) -> Path:
    """Where ``gridflow-sample`` writes one dataset's rows."""
    return samples_dir(site_dir) / vendor / f"{dataset}.json"


def notebook_path(site_dir: Path, vendor: str, dataset: str) -> Path:
    """Where the notebook runner writes one dataset's executed notebook."""
    return notebooks_dir(site_dir) / vendor / f"{dataset}.json"


def select_digest(silver: str, select: Mapping[str, Any]) -> str:
    """Digest of the row selection a sample file was made from."""
    return _digest({"silver": silver, "select": dict(select)})


def sample_silver(
    vendor: str, dataset: str, select: Mapping[str, Any], chart: Mapping[str, Any] | None
) -> str:
    """The silver table a record is read from: explicit, else the chart's, else the dataset's."""
    explicit = select.get("silver")
    if isinstance(explicit, str) and explicit:
        return explicit
    if chart and isinstance(chart.get("silver"), str):
        return str(chart["silver"])
    return f"{vendor}/{dataset}"


def notebook_source(vendor: str, source: str) -> str:
    """The ``data.<source>`` handle: explicit, else the vendor id."""
    return source or vendor


def notebook_cells(source: str, cells: Sequence[str]) -> list[str]:
    """The whole demo notebook: the setup cell, the source's help card, then the dataset's cells."""
    return [SETUP_CELL, f"data.{source}", *cells]


def cells_digest(cells: Sequence[str]) -> str:
    """Digest of the cells a notebook file was executed from."""
    return _digest({"kernel": KERNEL, "cells": list(cells)})


def load_json(path: Path) -> dict[str, Any] | None:
    """A committed artefact, or None when absent."""
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"{path}: must hold a JSON object")
    return data


def dumps(payload: Mapping[str, Any]) -> str:
    """Stable, diff-friendly JSON for committed artefacts."""
    return json.dumps(payload, indent=1, ensure_ascii=False) + "\n"
