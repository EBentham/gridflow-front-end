# Ingest receipt: neso/intensity_current

- **Outcome:** ok
- **When (UTC):** 2026-09-27T00:19:24Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 1 after (0 → 1 files).
- **Bronze files:** 0 before → 2 after. New bodies: 1, of which ENTSO-E "no matching data" acknowledgements: 0.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest neso intensity_current --last 24h` (attempt 1) → exit 0 in 17.2s
- `gridflow transform neso intensity_current --last 2d` (attempt 1) → exit 0 in 12.0s

## Files written
- bronze:
  - `bronze/neso/intensity_current/2026/09/26/raw_20260927T001911Z_1fc8349c.json`
  - `bronze/neso/intensity_current/2026/09/26/raw_20260927T001911Z_1fc8349c.meta.json`
- silver:
  - `silver/neso/intensity_current/year=2026/month=09/intensity_current_20260926.parquet`

## Output tails (keys redacted)
`gridflow ingest neso intensity_current --last 24h` (attempt 1):
```
  neso/intensity_current: 1 responses ingested
Ingestion complete
```

`gridflow transform neso intensity_current --last 2d` (attempt 1):
```
  neso/intensity_current: 1 rows transformed
Transform complete
2026-09-27 01:19:20,312 [WARNING] gridflow.silver.base: No bronze data for neso/intensity_current on 2026-09-25
2026-09-27 01:19:20,353 [WARNING] gridflow.silver.neso.carbon_intensity: NESO covered-but-not-owned (unconfirmed): neso/intensity_current target date 2026-09-27 has a nearer prior bronze partition at 2026-09-26, but no body's recorded request window confirms it covers 2026-09-27 -- 0 window(s) resolved but do not cover this date; unresolved reasons: no_request_params=1. Rows for 2026-09-27 may not exist.
2026-09-27 01:19:20,353 [WARNING] gridflow.silver.base: No bronze data for neso/intensity_current on 2026-09-27
```
