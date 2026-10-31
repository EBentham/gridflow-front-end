"""The notebook runner keeps every figure a cell draws.

``scripts/run_notebooks.py`` imports nbformat and nbclient at the top, which only the
gridflow_models interpreter has; ``outputs()`` uses neither, so stand-ins let the test load it.
"""

from __future__ import annotations

import base64
import importlib.util
import struct
import sys
import types
from pathlib import Path
from typing import Any

import pytest

RUNNER = Path(__file__).resolve().parents[1] / "scripts" / "run_notebooks.py"


class Node(dict):
    """An nbformat node: a dict also read by attribute."""

    __getattr__ = dict.__getitem__


def _png(width: int, height: int) -> bytes:
    """As much of a PNG as ``png_size`` reads: the signature, then the IHDR chunk's size."""
    return b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR" + struct.pack(">II", width, height)


@pytest.fixture
def runner(monkeypatch: pytest.MonkeyPatch) -> Any:
    monkeypatch.setitem(sys.modules, "nbformat", types.ModuleType("nbformat"))
    nbclient = types.ModuleType("nbclient")
    nbclient.NotebookClient = None  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "nbclient", nbclient)
    monkeypatch.setattr(sys, "path", list(sys.path))  # the runner puts src/ on it
    spec = importlib.util.spec_from_file_location("run_notebooks", RUNNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_two_figures_from_one_cell_keep_their_own_files(runner: Any) -> None:
    first, second = _png(640, 480), _png(800, 600)
    cell = Node(
        execution_count=4,
        outputs=[
            Node(output_type="display_data", data={"image/png": base64.b64encode(png).decode()})
            for png in (first, second)
        ],
    )
    images: dict[str, bytes] = {}
    out = runner.outputs(cell, "demo", images)
    assert [images[o["src"]] for o in out] == [first, second]
    assert [(o["width"], o["height"]) for o in out] == [(640, 480), (800, 600)]
