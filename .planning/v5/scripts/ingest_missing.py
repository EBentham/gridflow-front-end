"""Bounded `gridflow ingest` + `gridflow transform` for datasets with no local silver (v5 Phase 22).

Class-2 data op. For each target: count bronze files / silver rows before, run ingest then
transform over a small window (one retry on a non-zero exit), count after, list files
written, write a receipt to .planning/v5/ingest-receipts/<site-vendor>__<dataset>.md.

The shared catalogue C:\\gridflow-data\\gridflow.duckdb was locked by another process on
2026-09-27, so runs point GRIDFLOW_DUCKDB_PATH at a scratch catalogue (set P22_DUCKDB). Bronze
and silver still land in GRIDFLOW_DATA_DIR; only the run log and watermarks go to scratch.

    uv run python .planning/v5/scripts/ingest_missing.py [source/dataset ...]
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

FE = Path(__file__).resolve().parents[3]
GRIDFLOW = Path(os.environ.get("GRIDFLOW_REPO", r"C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow"))
DATA = Path(os.environ.get("GRIDFLOW_DATA_DIR", r"C:\gridflow-data"))
EXE = GRIDFLOW / ".venv" / "Scripts" / "gridflow.exe"
RECEIPTS = FE / ".planning" / "v5" / "ingest-receipts"
DUCKDB = os.environ.get("P22_DUCKDB")
SITE = {"gie_agsi": "gie", "gie_alsi": "gie", "open_meteo": "openmeteo"}
KEY_RE = re.compile(r"(securityToken=|x-key[:=]\s*|api[_-]?key[=:]\s*)[^&\s\"']+", re.IGNORECASE)

# (source, dataset) -> (ingest window args, transform window args)
WIN_ENTSOE = (["--start", "2026-09-22", "--end", "2026-09-26"], ["--start", "2026-09-22", "--end", "2026-09-26"])
WIN_MONTH = (["--start", "2026-08-27", "--end", "2026-09-26"], ["--start", "2026-08-27", "--end", "2026-09-26"])
WIN_SNAP = (["--last", "24h"], ["--last", "2d"])
WIN_WEEK = (["--last", "7d"], ["--last", "8d"])

TARGETS: dict[tuple[str, str], tuple[list[str], list[str]]] = {
    **{("entsoe", d): WIN_ENTSOE for d in (
        "activated_balancing_prices", "activated_balancing_qty", "aggregated_balancing_energy_bids",
        "balancing_financial_expenses_income", "commercial_schedules_net_positions", "congestion_income",
        "congestion_management_costs", "contracted_reserves", "countertrading", "cross_zonal_balancing_capacity",
        "imbalance_prices", "imbalance_volume", "offered_transfer_capacity_continuous",
        "offered_transfer_capacity_explicit", "offered_transfer_capacity_implicit", "outages_offshore_grid",
        "redispatching_cross_border", "transfer_capacity_use")},
    **{("entsog", d): WIN_SNAP for d in (
        "aggregate_interconnections", "balancing_zones", "connection_points", "interconnections",
        "operator_point_directions", "operators")},
    ("entsog", "interruptions"): WIN_MONTH,
    ("entsog", "urgent_market_messages"): WIN_MONTH,
    **{("gie_agsi", d): WIN_WEEK for d in ("about_listing", "about_summary", "news", "news_item")},
    **{("neso", d): WIN_SNAP for d in (
        "generation_current", "intensity_current", "intensity_today", "regional_current", "regional_england",
        "regional_postcode", "regional_regionid", "regional_scotland", "regional_wales")},
}


def scrub(text: str) -> str:
    return KEY_RE.sub(r"\1<redacted>", text)


def files(root: Path) -> set[str]:
    return {p.relative_to(DATA).as_posix() for p in root.rglob("*") if p.is_file()} if root.is_dir() else set()


def silver_rows(src: str, ds: str) -> int:
    root = DATA / "silver" / src / ds
    fs = sorted(root.rglob("*.parquet")) if root.is_dir() else []
    if not fs:
        return 0
    import polars as pl

    return sum(pl.scan_parquet(f, hive_partitioning=False).select(pl.len()).collect().item() for f in fs)


def bronze_bodies(paths: set[str]) -> dict[str, int]:
    """Classify new bronze bodies: ENTSO-E acknowledgement (no data) vs data."""
    out = {"bodies": 0, "entsoe_no_data_ack": 0}
    for p in paths:
        if p.endswith(".meta.json"):
            continue
        out["bodies"] += 1
        try:
            head = (DATA / p).read_bytes()[:600]
        except OSError:
            continue
        if b"Acknowledgement_MarketDocument" in head:
            out["entsoe_no_data_ack"] += 1
    return out


def run(cmd: list[str]) -> tuple[int, str, float]:
    env = dict(os.environ)
    if DUCKDB:
        env["GRIDFLOW_DUCKDB_PATH"] = DUCKDB
    env["PYTHONIOENCODING"] = "utf-8"
    env["COLUMNS"] = "200"
    t0 = time.time()
    try:
        r = subprocess.run(cmd, cwd=GRIDFLOW, env=env, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=1200)
        return r.returncode, scrub((r.stdout or "") + (r.stderr or "")), time.time() - t0
    except subprocess.TimeoutExpired as e:
        return 124, scrub(f"TIMEOUT after 1200s\n{e.stdout or ''}"), time.time() - t0


def tail(text: str, n: int = 25) -> str:
    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]
    return "\n".join(lines[-n:])


def last_error(text: str) -> str:
    for ln in reversed(text.splitlines()):
        if re.search(r"(Error|error|Exception|Unknown|not found|No transformer|401|403|404|429|503)", ln):
            return ln.strip()[:300]
    return ""


def do(src: str, ds: str, iw: list[str], tw: list[str]) -> dict[str, object]:
    b_root, s_root = DATA / "bronze" / src / ds, DATA / "silver" / src / ds
    b0, s0 = files(b_root), files(s_root)
    rows0 = silver_rows(src, ds)
    steps = []
    for name, args in (("ingest", ["ingest", src, ds, *iw]), ("transform", ["transform", src, ds, *tw])):
        for attempt in (1, 2):
            rc, out, dt = run([str(EXE), *args])
            steps.append({"step": name, "attempt": attempt, "cmd": "gridflow " + " ".join(args), "rc": rc,
                          "seconds": round(dt, 1), "tail": tail(out), "error": last_error(out) if rc else ""})
            if rc == 0:
                break
        if rc != 0 and name == "ingest":
            break
    b1, s1 = files(b_root), files(s_root)
    rows1 = silver_rows(src, ds)
    new_b, new_s = sorted(b1 - b0), sorted(s1 - s0)
    touched_s = sorted(p for p in (s0 & s1) if (DATA / p).stat().st_mtime > time.time() - 3600)
    cls = bronze_bodies(set(new_b))
    ing_ok = any(s["step"] == "ingest" and s["rc"] == 0 for s in steps)
    tr_ok = any(s["step"] == "transform" and s["rc"] == 0 for s in steps)
    alltext = "\n".join(s["tail"] for s in steps)
    if rows1 > 0:
        outcome = "ok"
    elif re.search(r"401|403|unauthori[sz]ed|forbidden|api key|API_KEY", alltext, re.IGNORECASE):
        outcome = "auth"
    elif cls["bodies"] and cls["entsoe_no_data_ack"] == cls["bodies"]:
        outcome = "no data for gridflow's GB scope (ENTSO-E acknowledgement 999 on every request)"
    elif re.search(r"404|410|decommission|retired|not found", alltext, re.IGNORECASE) and not ing_ok:
        outcome = "retired endpoint / not found"
    elif not ing_ok:
        outcome = "error (ingest): " + (next((s["error"] for s in steps if s["error"]), "") or "non-zero exit")
    elif not tr_ok:
        outcome = "error (transform): " + (next((s["error"] for s in steps if s["step"] == "transform" and s["error"]), "") or "non-zero exit")
    else:
        outcome = "empty (commands succeeded, no silver rows produced)"
    return {"source": src, "dataset": ds, "bronze_files_before": len(b0), "bronze_files_after": len(b1),
            "silver_files_before": len(s0), "silver_files_after": len(s1), "silver_rows_before": rows0,
            "silver_rows_after": rows1, "new_bronze": new_b, "new_silver": new_s, "silver_overwritten": touched_s,
            "bronze_classes": cls, "steps": steps, "outcome": outcome,
            "at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")}


def receipt(r: dict[str, object]) -> str:
    def lst(xs: list[str], n: int = 12) -> str:
        if not xs:
            return "none"
        more = f"\n  - … and {len(xs) - n} more" if len(xs) > n else ""
        return "\n" + "\n".join(f"  - `{x}`" for x in xs[:n]) + more

    steps = "\n".join(
        f"- `{s['cmd']}` (attempt {s['attempt']}) → exit {s['rc']} in {s['seconds']}s"
        + (f"; error: `{s['error']}`" if s["error"] else "")
        for s in r["steps"]  # type: ignore[union-attr]
    )
    tails = "\n\n".join(f"`{s['cmd']}` (attempt {s['attempt']}):\n```\n{s['tail']}\n```" for s in r["steps"])  # type: ignore[union-attr]
    return f"""# Ingest receipt: {r['source']}/{r['dataset']}

- **Outcome:** {r['outcome']}
- **When (UTC):** {r['at']}
- **Data dir:** `{DATA}`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** {r['silver_rows_before']:,} before → {r['silver_rows_after']:,} after ({r['silver_files_before']} → {r['silver_files_after']} files).
- **Bronze files:** {r['bronze_files_before']} before → {r['bronze_files_after']} after. New bodies: {r['bronze_classes']['bodies']}, of which ENTSO-E "no matching data" acknowledgements: {r['bronze_classes']['entsoe_no_data_ack']}.
- **Overwritten:** {('existing silver files rewritten: ' + ', '.join(r['silver_overwritten'])) if r['silver_overwritten'] else 'nothing (no pre-existing silver or bronze was rewritten; no snapshot needed)'}.

## Commands
{steps}

## Files written
- bronze:{lst(r['new_bronze'])}
- silver:{lst(r['new_silver'])}

## Output tails (keys redacted)
{tails}
"""


def main(argv: list[str]) -> None:
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    targets = TARGETS
    if argv:
        want = {tuple(a.split("/", 1)) for a in argv}
        targets = {k: v for k, v in TARGETS.items() if k in want}
    log = RECEIPTS / "_ingest-log.jsonl"
    for (src, ds), (iw, tw) in targets.items():
        r = do(src, ds, iw, tw)
        (RECEIPTS / f"{SITE.get(src, src)}__{ds}.md").write_text(receipt(r), encoding="utf-8")
        with log.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({k: v for k, v in r.items() if k not in ("steps",)}, default=str) + "\n")
        print(f"{src}/{ds}: {r['outcome']} rows {r['silver_rows_before']} -> {r['silver_rows_after']}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
