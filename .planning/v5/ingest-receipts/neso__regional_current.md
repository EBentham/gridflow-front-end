# Ingest receipt: neso/regional_current

- **Outcome:** ok
- **When (UTC):** 2026-09-27T00:33:12Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 162 after (0 → 1 files).
- **Bronze files:** 0 before → 2 after. New bodies: 1, of which ENTSO-E "no matching data" acknowledgements: 0.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest neso regional_current --last 24h` (attempt 1) → exit 0 in 4.5s
- `gridflow transform neso regional_current --last 2d` (attempt 1) → exit 0 in 6.3s

## Files written
- bronze:
  - `bronze/neso/regional_current/2026/09/26/raw_20260927T003305Z_08f81d9c.json`
  - `bronze/neso/regional_current/2026/09/26/raw_20260927T003305Z_08f81d9c.meta.json`
- silver:
  - `silver/neso/regional_current/year=2026/month=09/regional_current_20260926.parquet`

## Output tails (keys redacted)
`gridflow ingest neso regional_current --last 24h` (attempt 1):
```
  neso/regional_current: 1 responses ingested
Ingestion complete
```

`gridflow transform neso regional_current --last 2d` (attempt 1):
```
  neso/regional_current: 162 rows transformed
Transform complete
2026-09-27 01:33:09,658 [WARNING] gridflow.silver.base: No bronze data for neso/regional_current on 2026-09-25
2026-09-27 01:33:09,676 [WARNING] gridflow.silver.neso.carbon_intensity: NESO covered-but-not-owned (unconfirmed): neso/regional_current target date 2026-09-27 has a nearer prior bronze partition at 2026-09-26, but no body's recorded request window confirms it covers 2026-09-27 -- 0 window(s) resolved but do not cover this date; unresolved reasons: no_request_params=1. Rows for 2026-09-27 may not exist.
2026-09-27 01:33:09,676 [WARNING] gridflow.silver.base: No bronze data for neso/regional_current on 2026-09-27
```
