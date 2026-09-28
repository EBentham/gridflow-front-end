"""Designer 1, architecture round 1: every piece of copy on the board.

Pack wording (ARCH-PACK.md / pack.json) is used as is, only split into markup (``<code>`` around code tokens).
Lines that are NOT pack wording are registered in NEW and listed in 1-notes.md.
"""
from __future__ import annotations

import json
from pathlib import Path

PACK_DIR = Path(__file__).resolve().parents[3] / "arch-pack"
PACK = json.loads((PACK_DIR / "pack.json").read_text(encoding="utf-8"))
SNIP = PACK_DIR / "snippets"
GH = "https://github.com/EBentham/gridflow/blob/master/"
GHT = "https://github.com/EBentham/gridflow/tree/master/"
GHM = "https://github.com/EBentham/gridflow-models/blob/main/"

NEW: list[str] = []


def new(s: str) -> str:
    """Register a line of copy that is not pack wording."""
    if s not in NEW:
        NEW.append(s)
    return s


def snip(name: str) -> str:
    return (SNIP / name).read_text(encoding="utf-8").rstrip("\n")


def sec(sid: str) -> dict:
    return next(s for s in PACK["sections"] if s["id"] == sid)


PARTS = {p["id"]: p for p in sec("drawing")["parts"]}

# ------------------------------------------------------------------ opening
H1 = new("How gridflow is built")
LEDE = sec("opening")["lede"]
SCOPE = sec("opening")["scope"]
OPEN_LINKS = [(GH + "pyproject.toml", "pyproject.toml"), (GH + "src/gridflow/cli.py", "src/gridflow/cli.py")]

# ------------------------------------------------------------------ drawing
H2_DRAW = new("One section through gridflow")
DRAW_INTRO = new("Sources on the grid above, their cables down through bronze, silver and gold, and the readers at the foot. "
                 "Each part is keyed to its file on GitHub.")

# sources, west to east (the order they stand in the drawing and in the index)
SRC_ORDER = ["elexon", "neso", "neso_data_portal", "open_meteo", "gie_alsi", "gie_agsi", "entsog", "entsoe"]


def src(key: str) -> dict:
    p = PARTS[f"source-{key}"]
    line = p["index"].split(": ", 1)[1]
    return {"key": key, "label": p["label"], "human": p["human_name"], "line": line, "url": p["links"][0]}


# below ground, top to bottom: (part id, index line as HTML with code marked, [(url, shown path)])
C = lambda s: f"<code>{s}</code>"  # noqa: E731
UG = [
    ("boundary-vendor-connector",
     "One async httpx client per source; a semaphore caps requests in flight; tenacity retries with jittered backoff.",
     [(GH + "src/gridflow/connectors/base.py", "src/gridflow/connectors/base.py"),
      (GH + "src/gridflow/utils/retry.py", "src/gridflow/utils/retry.py")]),
    ("boundary-connector-bronze",
     f"Each response is stored byte for byte with a {C('.meta.json')} sidecar; both land by temp file and atomic rename.",
     [(GH + "src/gridflow/bronze/writer.py", "src/gridflow/bronze/writer.py")]),
    ("stratum-bronze",
     f"{C('bronze/{source}/{dataset}/{YYYY}/{MM}/{DD}/raw_{fetched_at}_{hash8}.json')}, one file per response page.",
     [(GH + "src/gridflow/bronze/writer.py", "src/gridflow/bronze/writer.py")]),
    ("boundary-bronze-silver",
     f"One Polars transformer per dataset: strict types, UTC, Pydantic checks counted not raised, then "
     f"{C('available_at')}, {C('source_run_id')}, {C('dataset_version')}.",
     [(GH + "src/gridflow/silver/base.py", "src/gridflow/silver/base.py"),
      (GH + "src/gridflow/silver/elexon/system_prices.py", "src/gridflow/silver/elexon/system_prices.py")]),
    ("stratum-silver",
     f"{C('silver/{source}/{dataset}/year=YYYY/month=MM/')}; append-only datasets keep one file per capture, suffixed "
     f"{C('_run{capture time}')}.",
     [(GH + "src/gridflow/storage/paths.py", "src/gridflow/storage/paths.py"),
      (GH + "src/gridflow/silver/base.py", "src/gridflow/silver/base.py")]),
    ("boundary-silver-views",
     f"One view per dataset over {C('read_parquet')} with Hive partitioning; append-only datasets also get a "
     f"{C('_latest')} view.",
     [(GH + "src/gridflow/storage/duckdb.py", "src/gridflow/storage/duckdb.py"),
      (GH + "src/gridflow/silver/latest_views.py", "src/gridflow/silver/latest_views.py")]),
    ("catalogue",
     f"Views over the Parquet, plus the {C('pipeline_runs')}, {C('pipeline_watermarks')} and {C('quality_reports')} "
     f"tables. No server.",
     [(GH + "src/gridflow/storage/duckdb.py", "src/gridflow/storage/duckdb.py")]),
    ("stratum-gold",
     f"Polars builder {C('system_marginal_price')}; SQL views {C('gold_uk_imbalance_context')}, "
     f"{C('gold_gb_day_ahead_benchmark')}, {C('gold_eu_gas_storage')}.",
     [(GH + "src/gridflow/gold/system_marginal_price.py", "src/gridflow/gold/system_marginal_price.py"),
      (GHT + "src/gridflow/gold/views", "src/gridflow/gold/views")]),
]

# drawing labels: the pack's own drawing labels, set lower-case like a hand-annotated plate
LAB = {pid: (PARTS[pid]["label"] if PARTS[pid]["label"].startswith("DuckDB")
            else PARTS[pid]["label"][0].lower() + PARTS[pid]["label"][1:]) for pid, _, _ in UG}

READERS = [
    ("reader-cli", "The gridflow command",
     ", ".join(C(v) for v in ["init", "ingest", "transform", "build", "pipeline", "backfill", "export-csv", "status",
                             "quality", "reset", "prune"]) + ".",
     [(GH + "src/gridflow/cli.py", "src/gridflow/cli.py")], None),
    ("reader-client", "GridflowClient, read-only, returns Polars",
     f"{C('from gridflow.serving.client import GridflowClient')}: {C('query')}, {C('get_system_prices')}, "
     f"{C('get_imbalance_context')}, {C('get_gas_storage')} and more.",
     [(GH + "src/gridflow/serving/client.py", "src/gridflow/serving/client.py")], None),
    ("reader-notebooks", "Notebooks",
     "Any notebook can open a GridflowClient; the gridflow_models workbench notebooks do, through their setup helper.",
     [(GHM + "src/gridflow_models/research/notebook_setup.py", "src/gridflow_models/research/notebook_setup.py")], None),
    ("reader-gridflow-models", "gridflow_models, reading as of a time",
     f"Training and backtests read silver Parquet directly, keeping only rows whose {C('available_at')} is at or before "
     f"the as-of time.",
     [(GHM + "src/gridflow_models/data/gridflow_source.py", "src/gridflow_models/data/gridflow_source.py")],
     ("models.html", "Models page")),
]

# ------------------------------------------------------------------ journey
H2_JOURNEY = new("One row, from a command to a DataFrame")
EXAMPLE = ("The example row throughout: Elexon <code>system_prices</code>, settlement date 2026-09-08, period 37. "
           "Two captures of the same day hold two versions: first published at 9.56, then 110.00 a day later.")

STOPS = {s["id"]: s for s in sec("journey")["stops"]}


def stop(n: int) -> dict:
    return next(s for s in sec("journey")["stops"] if s["id"].startswith(f"stop-{n}-"))


# pack bodies with code tokens marked (wording unchanged)
BODY = {
    1: stop(1)["body"].replace("ingest", C("ingest"), 1).replace("transform", C("transform"), 1),
    2: stop(2)["body"],
    3: stop(3)["body"].replace(".meta.json", C(".meta.json")),
    4: stop(4)["body"].replace("available_at", C("available_at")).replace("source_run_id", C("source_run_id"))
                     .replace("dataset_version", C("dataset_version")),
    5: stop(5)["body"].replace("silver_elexon_system_prices_latest", C("silver_elexon_system_prices_latest"))
                     .replace("latest available_at", "latest " + C("available_at")),
    6: stop(6)["body"].replace("system_marginal_price", C("system_marginal_price")),
    7: stop(7)["body"].replace("get_system_prices", C("get_system_prices")).replace("_latest", C("_latest"))
                     .replace("available_at", C("available_at")),
}
MECH = stop(5)["mechanism"]

# the real outputs (ARCH-PACK.md "Real output" blocks), as rows
OUT2 = "/balancing/settlement/system-prices/2026-09-08 {'page': 1}"
OUT4 = (["settlement_date", "settlement_period", "system_sell_price", "system_buy_price", "available_at",
         "vintage_policy", "source_run_id", "dataset_version"],
        [["2026-09-08", "37", "9.56", "9.56", "2026-09-08 17:48:45 UTC", "vendor",
          "494e780a-a127-4fa8-b371-25caf146c094", "2.0.0"],
         ["2026-09-08", "37", "110.0", "110.0", "2026-09-09 17:44:29 UTC", "vendor",
          "494e780a-a127-4fa8-b371-25caf146c094", "2.0.0"]])
OUT5L = (["settlement_date", "settlement_period", "system_sell_price", "system_buy_price", "available_at"],
         [["2026-09-08", "37", "110.0", "110.0", "2026-09-09 17:44:29 UTC"]])
OUT5A = (["settlement_date", "settlement_period", "system_sell_price", "available_at"],
         [["2026-09-08", "37", "9.56", "2026-09-08 17:48:45 UTC"]])
OUT6 = (["settlement_date", "settlement_period", "system_buy_price", "system_sell_price", "spread", "abs_imbalance",
         "hour_of_day", "day_of_week"],
        [["2026-09-08", "37", "110.0", "110.0", "0.0", "346.717783", "17", "2"]])
OUT7 = (["settlement_date", "settlement_period", "system_sell_price", "system_buy_price", "available_at"],
        [["2026-09-08", "37", "110.0", "110.0", "2026-09-09 17:44:29 UTC"]])
NUMERIC = {"settlement_period", "system_sell_price", "system_buy_price", "spread", "abs_imbalance", "hour_of_day",
           "day_of_week"}

# stop 5 figure
FIG5_H = new("What was known, and when")
FIG5_CAP = new("Elexon system_prices, settlement date 2026-09-08, period 37: each version of system_sell_price from its "
               "available_at, 8 to 10 September 2026, UTC. Buy and sell are equal in both versions.")


def links_of(n: int) -> list[tuple[str, str]]:
    return [(lk["url"], lk["file"]) for lk in stop(n)["links"]]


# ------------------------------------------------------------------ correctness
H2_CORRECT = new("How it stays correct")
CORR = sec("correctness")
RULES = [(r["rule"], [(lk["url"], lk["file"]) for lk in r["links"]]) for r in CORR["rules"]]
RUN_H = "Run tracking"
CI_H = "CI"


def mark_codes(s: str, toks: list[str]) -> str:
    for t in toks:
        s = s.replace(t, C(t))
    return s


RUN_TEXT = mark_codes(CORR["run_tracking"]["text"], ["pipeline_runs", "source_run_id", "pipeline_watermarks",
                                                     "gridflow quality", "quality_reports"])
RUN_LINKS = [(lk["url"], lk["file"]) for lk in CORR["run_tracking"]["links"]]
CI_TEXT = mark_codes(CORR["ci"]["text"], ["src/gridflow"])
CI_LINKS = [(lk["url"], lk["file"]) for lk in CORR["ci"]["links"]]
RULE_CODES = ["available_at"]

# ------------------------------------------------------------------ where to look
H2_LOOK = new("Where to look in the code")
LOOK_KEEP = ["which sources and endpoints are configured", "how a connector requests, limits and retries",
             "how raw responses are stored", "how bronze becomes silver: validation, timestamps, file names",
             "a complete transformer, Elexon system prices", "how the latest version is chosen",
             "the catalogue, its views and run tables", "gold builders and SQL views", "reading data into Polars",
             "every command"]
LOOK = [(e["for"], [(lk["url"], lk["file"]) for lk in e["links"]])
        for e in sec("where_to_look")["entries"] if e["for"] in LOOK_KEEP]
