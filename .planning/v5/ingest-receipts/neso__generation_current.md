# Ingest receipt: neso/generation_current

- **Outcome:** ok
- **When (UTC):** 2026-09-27T00:32:50Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 9 after (0 → 1 files).
- **Bronze files:** 0 before → 2 after. New bodies: 1, of which ENTSO-E "no matching data" acknowledgements: 0.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest neso generation_current --last 24h` (attempt 1) → exit 0 in 4.4s
- `gridflow transform neso generation_current --last 2d` (attempt 1) → exit 0 in 7.0s

## Files written
- bronze:
  - `bronze/neso/generation_current/2026/09/26/raw_20260927T003243Z_4e48ee5c.json`
  - `bronze/neso/generation_current/2026/09/26/raw_20260927T003243Z_4e48ee5c.meta.json`
- silver:
  - `silver/neso/generation_current/year=2026/month=09/generation_current_20260926.parquet`

## Output tails (keys redacted)
`gridflow ingest neso generation_current --last 24h` (attempt 1):
```
  neso/generation_current: 1 responses ingested
Ingestion complete
```

`gridflow transform neso generation_current --last 2d` (attempt 1):
```
  neso/generation_current: 9 rows transformed
Transform complete
2026-09-27 01:32:47,801 [WARNING] gridflow.silver.base: No bronze data for neso/generation_current on 2026-09-25
2026-09-27 01:32:47,893 [WARNING] gridflow.silver.neso.carbon_intensity: NESO covered-but-not-owned (unconfirmed): neso/generation_current target date 2026-09-27 has a nearer prior bronze partition at 2026-09-26, but no body's recorded request window confirms it covers 2026-09-27 -- 0 window(s) resolved but do not cover this date; unresolved reasons: no_request_params=1. Rows for 2026-09-27 may not exist.
2026-09-27 01:32:47,893 [WARNING] gridflow.silver.base: No bronze data for neso/generation_current on 2026-09-27
```
