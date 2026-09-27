# Ingest receipt: neso/intensity_today

- **Outcome:** ok
- **When (UTC):** 2026-09-27T00:33:01Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 48 after (0 → 1 files).
- **Bronze files:** 0 before → 2 after. New bodies: 1, of which ENTSO-E "no matching data" acknowledgements: 0.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest neso intensity_today --last 24h` (attempt 1) → exit 0 in 4.4s
- `gridflow transform neso intensity_today --last 2d` (attempt 1) → exit 0 in 6.3s

## Files written
- bronze:
  - `bronze/neso/intensity_today/2026/09/26/raw_20260927T003255Z_4421d9ea.json`
  - `bronze/neso/intensity_today/2026/09/26/raw_20260927T003255Z_4421d9ea.meta.json`
- silver:
  - `silver/neso/intensity_today/year=2026/month=09/intensity_today_20260926.parquet`

## Output tails (keys redacted)
`gridflow ingest neso intensity_today --last 24h` (attempt 1):
```
  neso/intensity_today: 1 responses ingested
Ingestion complete
```

`gridflow transform neso intensity_today --last 2d` (attempt 1):
```
  neso/intensity_today: 48 rows transformed
Transform complete
2026-09-27 01:32:58,892 [WARNING] gridflow.silver.base: No bronze data for neso/intensity_today on 2026-09-25
2026-09-27 01:32:58,906 [WARNING] gridflow.silver.neso.carbon_intensity: NESO covered-but-not-owned (unconfirmed): neso/intensity_today target date 2026-09-27 has a nearer prior bronze partition at 2026-09-26, but no body's recorded request window confirms it covers 2026-09-27 -- 0 window(s) resolved but do not cover this date; unresolved reasons: no_request_params=1. Rows for 2026-09-27 may not exist.
2026-09-27 01:32:58,906 [WARNING] gridflow.silver.base: No bronze data for neso/intensity_today on 2026-09-27
```
