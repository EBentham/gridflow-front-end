"""Execute the demo notebooks for real on the gridflow_models kernel (read-only cells only).

Writes <name>_analysis.ipynb (executed, with outputs) and run.log beside this file.
Run with the gridflow_models venv: .venv\\Scripts\\python.exe run_cells.py
"""
from __future__ import annotations

import datetime as dt
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient

HERE = Path(__file__).parent

SETUP = "from gridflow_models import setup_notebook\ndata, models, common = setup_notebook()"

CELLS = {
    "fuelhh": [
        SETUP,
        "data.elexon",
        'df = data.elexon.query("fuelhh", "2026-09-20", "2026-09-26")',
        'df[["settlement_date", "settlement_period", "fuel_type", "generation_mw"]].head()',
        'wind = df[df.fuel_type == "WIND"]\n'
        'wind.plot(x="timestamp_utc", y="generation_mw", ylabel="MW",\n'
        '          color="#3E8C97", figsize=(8, 3.5))',
    ],
    "bmunits_reference": [
        SETUP,
        "data.elexon",
        'df = data.sql("SELECT * FROM silver_elexon_bmunits_reference ORDER BY bm_unit_id")',
        'df[["bm_unit_id", "fuel_type", "registered_capacity_mw", "company_name"]].head()',
        "df.fuel_type.value_counts(dropna=False)",
    ],
}


def run(name: str, cells: list[str], log: list[str]) -> None:
    nb = nbformat.v4.new_notebook()
    nb.cells = [nbformat.v4.new_code_cell(src) for src in cells]
    nb.metadata["kernelspec"] = {"name": "gridflow_models", "display_name": "gridflow_models", "language": "python"}
    t0 = time.perf_counter()
    NotebookClient(nb, kernel_name="gridflow_models", timeout=600,
                   resources={"metadata": {"path": str(HERE)}}).execute()
    secs = time.perf_counter() - t0
    out = HERE / f"{name}_analysis.ipynb"
    nbformat.write(nb, out)
    log.append(f"{name}: executed {len(cells)} cells in {secs:.1f} s on kernel gridflow_models -> {out.name}")
    for c in nb.cells:
        kinds = []
        for o in c.outputs:
            if o.output_type == "stream":
                kinds.append(f"stream:{o.name}:{o.text.strip()[:120]!r}")
            elif o.output_type == "error":
                kinds.append(f"ERROR {o.ename}: {o.evalue}")
            else:
                kinds.append(f"{o.output_type}[{','.join(sorted(o.data))}]")
        log.append(f"  In [{c.execution_count}]: {c.source.splitlines()[0][:70]!r} -> {kinds or ['(no output)']}")


if __name__ == "__main__":
    log = [f"run {dt.datetime.now(dt.UTC).isoformat(timespec='seconds')}"]
    for name, cells in CELLS.items():
        run(name, cells, log)
    (HERE / "run.log").write_text("\n".join(log) + "\n", encoding="utf-8")
    print("\n".join(log))
