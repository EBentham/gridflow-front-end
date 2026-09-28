"""Format every sample value exactly as Polars prints it. Run with gridflow's venv (it has polars).

Writes vals.json: {specimen_id: {"columns": [...], "dtypes": [...], "rows": [[str, ...], ...]}}.
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

import polars as pl

HERE = Path(__file__).parent
PACK = json.loads((HERE.parent.parent / "pack" / "specimens.json").read_text(encoding="utf-8"))
MAP = {"Date": pl.Date, "Int32": pl.Int32, "String": pl.String, "Float64": pl.Float64}

out: dict[str, dict] = {}
for s in PACK["specimens"]:
    cols = s["schema"]["columns"]
    schema = {c["column"]: MAP.get(c["dtype"], pl.Datetime("us", "UTC")) for c in cols}
    rows = []
    for r in s["sample_rows"]["rows"]:
        o = {}
        for k, dt in schema.items():
            v = r.get(k)
            if v is not None and dt == pl.Date:
                v = date.fromisoformat(v)
            elif v is not None and isinstance(dt, pl.Datetime):
                v = datetime.fromisoformat(v)
            o[k] = v
        rows.append(o)
    df = pl.DataFrame(rows, schema=schema, orient="row")
    with pl.Config(tbl_formatting="ASCII_MARKDOWN", tbl_hide_column_data_types=True,
                   tbl_hide_dataframe_shape=True, tbl_cols=-1, tbl_rows=-1, tbl_width_chars=4000,
                   fmt_str_lengths=200):
        text = str(df)
    lines = [ln for ln in text.splitlines() if ln.startswith("|")]
    head = [c.strip() for c in lines[0].strip("|").split("|")]
    body = [[c.strip() for c in ln.strip("|").split("|")] for ln in lines[2:]]
    assert head == list(schema), (head, list(schema))
    assert len(body) == 8 and all(len(b) == len(head) for b in body)
    out[s["id"]] = {"columns": head, "dtypes": [c["dtype"] for c in cols], "rows": body}

(HERE / "vals.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
for k, v in out.items():
    print(k, v["rows"][0])
