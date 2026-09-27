"""Run every arch-pack snippet against the real gridflow code and data, read-only.

Run from the gridflow repo with its venv:
    .venv/Scripts/python.exe <this file>
Nothing here writes to the data root: DuckDB is opened read_only=True, the gold
builder's build() (not run()) is called, and the gold directory is listed
before and after to prove it.
"""

from __future__ import annotations

import json
import runpy
import subprocess
import sys
from pathlib import Path

import duckdb
import polars as pl

pl.Config.set_tbl_cols(20)
pl.Config.set_tbl_width_chars(200)
pl.Config.set_fmt_str_lengths(80)

HERE = Path(__file__).resolve().parent
SNIP = HERE / "snippets"
DATA = Path("C:/gridflow-data")
DB = DATA / "gridflow.duckdb"
BRONZE_DAY = DATA / "bronze/elexon/system_prices/2026/09/08"
SILVER_MONTH = DATA / "silver/elexon/system_prices/year=2026/month=09"


def banner(name: str) -> None:
    print(f"\n===== {name} =====")


def gold_files() -> list[str]:
    return sorted(str(p.relative_to(DATA)) for p in (DATA / "gold").rglob("*") if p.is_file())


gold_before = gold_files()
banner("gold directory before")
print(f"{len(gold_before)} files; system_marginal_price present: "
      f"{any('system_marginal_price' in p for p in gold_before)}")

banner("01-cli.sh (options checked with --help, not executed: ingest/transform write)")
for verb in ("ingest", "transform", "build"):
    out = subprocess.run(
        [str(Path(sys.executable).parent / "gridflow.exe"), verb, "--help"],
        capture_output=True, text=True, encoding="utf-8", env={"COLUMNS": "200", "PYTHONIOENCODING": "utf-8", "SYSTEMROOT": "C:\\Windows"},
    ).stdout
    print(verb, "--start" in out, "--end" in out)

banner("02-connector-request.py")
runpy.run_path(str(SNIP / "02-connector-request.py"), run_name="__main__")
sidecar_1 = json.loads((BRONZE_DAY / "raw_20260908T214403Z_3a7fca58.meta.json").read_text())
sidecar_2 = json.loads((BRONZE_DAY / "raw_20260916T190532Z_4c2c01b2.meta.json").read_text())
print("sidecar request_url (capture 1):", sidecar_1["request_url"])
print("sidecar request_url (capture 2):", sidecar_2["request_url"])
expected_get = (SNIP / "02-connector-request.txt").read_text().strip().removeprefix("GET ")
print("02-connector-request.txt matches sidecar:", expected_get == sidecar_1["request_url"])

banner("03-bronze-files.txt")
real_names = sorted(p.name for p in BRONZE_DAY.iterdir())
print(real_names)
listed = [ln.strip() for ln in (SNIP / "03-bronze-files.txt").read_text().splitlines()[1:]]
print("listing matches disk:", listed == real_names)

banner("03-bronze-body-excerpt.json (every excerpt field equals the real body)")
excerpt = json.loads((SNIP / "03-bronze-body-excerpt.json").read_text())
body = json.loads((BRONZE_DAY / "raw_20260908T214403Z_3a7fca58.json").read_text())
real_rec = next(r for r in body["data"] if r["settlementPeriod"] == 37)
ex_rec = excerpt["data"][0]
print("metadata equal:", excerpt["metadata"] == body["metadata"])
print("fields equal:", all(real_rec[k] == v for k, v in ex_rec.items()), "fields shown:", len(ex_rec),
      "of", len(real_rec))
body2 = json.loads((BRONZE_DAY / "raw_20260916T190532Z_4c2c01b2.json").read_text())
rec2 = next(r for r in body2["data"] if r["settlementPeriod"] == 37)
print("capture 2, SP37:", {k: rec2[k] for k in ex_rec})

banner("03-bronze-sidecar.json equals the real sidecar")
print(json.loads((SNIP / "03-bronze-sidecar.json").read_text()) == sidecar_1)

banner("04-silver-files.txt")
silver_names = sorted(p.name for p in SILVER_MONTH.glob("system_prices_20260908_run*.parquet"))
print(silver_names)
listed = [ln.strip() for ln in (SNIP / "04-silver-files.txt").read_text().splitlines()[1:]]
print("listing matches disk:", listed == silver_names)
print("run stamp 1 == sidecar written_at:",
      sidecar_1["written_at"].replace(":", "-").replace("+", "-") in silver_names[0])
print("run stamp 2 == sidecar written_at:",
      sidecar_2["written_at"].replace(":", "-").replace("+", "-") in silver_names[1])

con = duckdb.connect(str(DB), read_only=True)
con.execute("SET TimeZone = 'UTC'")  # display only; values are stored as UTC instants
for name in ("04-silver-vintages.sql", "05-latest-view.sql", "05-as-of.sql"):
    banner(name)
    print(con.sql((SNIP / name).read_text()).pl())

banner("04: source_run_id resolves to a transform row in pipeline_runs")
print(con.sql(
    "SELECT DISTINCT s.source_run_id, r.operation FROM silver_elexon_system_prices s "
    "JOIN pipeline_runs r ON r.run_id = s.source_run_id "
    "WHERE s.settlement_date = DATE '2026-09-08' AND s.settlement_period = 37"
).pl())

banner("08-run-tracking.sql (table definition; columns compared with the catalogue)")
snippet_cols = [
    ln.split()[0] for ln in (SNIP / "08-run-tracking.sql").read_text().splitlines()[1:-1]
]
real_cols = [r[0] for r in con.execute(
    "SELECT column_name FROM information_schema.columns WHERE table_name = 'pipeline_runs' "
    "ORDER BY ordinal_position"
).fetchall()]
print(snippet_cols)
print("columns match catalogue:", snippet_cols == real_cols)
print("tables:", [r[0] for r in con.execute("SELECT table_name FROM duckdb_tables()").fetchall()])

banner("05-latest-view-ddl.sql (rendered by gridflow, compared with the catalogue)")
from gridflow.silver.latest_views import LATEST_VIEW_SPECS, latest_view_sql  # noqa: E402

cols = {r[0] for r in con.execute(
    "SELECT column_name FROM information_schema.columns WHERE table_name = ?",
    ["silver_elexon_system_prices"],
).fetchall()}
ddl = latest_view_sql(
    "silver_elexon_system_prices",
    "silver_elexon_system_prices_latest",
    LATEST_VIEW_SPECS[("elexon", "system_prices")],
    cols,
)
print(ddl)
stored = con.execute(
    "SELECT sql FROM duckdb_views() WHERE view_name = 'silver_elexon_system_prices_latest'"
).fetchone()[0]
print("catalogue stored sql:", stored)

def _norm(s: str) -> str:
    return " ".join(s.replace("(", " ( ").replace(")", " ) ").split())


print("snippet file equals rendered DDL (whitespace-insensitive):",
      _norm((SNIP / "05-latest-view-ddl.sql").read_text()) == _norm(ddl))

banner("vintage_policy labels on this period, and base-view vintage count per key")
print(con.sql(
    "SELECT vintage_policy, count(*) n FROM silver_elexon_system_prices "
    "WHERE settlement_date = DATE '2026-09-08' GROUP BY 1"
).pl())
con.close()

banner("06-gold-build.py (build() only; nothing written)")
runpy.run_path(str(SNIP / "06-gold-build.py"), run_name="__main__")

banner("07-client.py")
runpy.run_path(str(SNIP / "07-client.py"), run_name="__main__")

gold_after = gold_files()
banner("gold directory after")
print(f"{len(gold_after)} files; unchanged: {gold_before == gold_after}")
