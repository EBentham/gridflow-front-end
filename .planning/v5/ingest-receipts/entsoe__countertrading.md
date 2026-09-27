# Ingest receipt: entsoe/countertrading

- **Outcome:** ok
- **When (UTC):** 2026-09-27T00:23:26Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 12 after (0 → 2 files).
- **Bronze files:** 80 before → 144 after. New bodies: 32, of which ENTSO-E "no matching data" acknowledgements: 30.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsoe countertrading --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 37.9s
- `gridflow transform entsoe countertrading --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 6.7s

## Files written
- bronze:
  - `bronze/entsoe/countertrading/2026/09/22/raw_20260927T002246Z_9e7c6f10.meta.json`
  - `bronze/entsoe/countertrading/2026/09/22/raw_20260927T002246Z_9e7c6f10.xml`
  - `bronze/entsoe/countertrading/2026/09/22/raw_20260927T002247Z_98162536.meta.json`
  - `bronze/entsoe/countertrading/2026/09/22/raw_20260927T002247Z_98162536.xml`
  - `bronze/entsoe/countertrading/2026/09/22/raw_20260927T002248Z_094fe77a.meta.json`
  - `bronze/entsoe/countertrading/2026/09/22/raw_20260927T002248Z_094fe77a.xml`
  - `bronze/entsoe/countertrading/2026/09/22/raw_20260927T002249Z_afcf5bcb.meta.json`
  - `bronze/entsoe/countertrading/2026/09/22/raw_20260927T002249Z_afcf5bcb.xml`
  - `bronze/entsoe/countertrading/2026/09/22/raw_20260927T002250Z_df112847.meta.json`
  - `bronze/entsoe/countertrading/2026/09/22/raw_20260927T002250Z_df112847.xml`
  - `bronze/entsoe/countertrading/2026/09/22/raw_20260927T002251Z_6c9ebe14.meta.json`
  - `bronze/entsoe/countertrading/2026/09/22/raw_20260927T002251Z_6c9ebe14.xml`
  - … and 52 more
- silver:
  - `silver/entsoe/countertrading/year=2026/month=09/countertrading_20260922.parquet`
  - `silver/entsoe/countertrading/year=2026/month=09/countertrading_20260925.parquet`

## Output tails (keys redacted)
`gridflow ingest entsoe countertrading --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/countertrading: 32 responses ingested
Ingestion complete
```

`gridflow transform entsoe countertrading --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/countertrading: 12 rows transformed
Transform complete
2026-09-27 01:23:23,213 [WARNING] gridflow.silver.base: No bronze data for entsoe/countertrading on 2026-09-23
2026-09-27 01:23:23,216 [WARNING] gridflow.silver.base: No bronze data for entsoe/countertrading on 2026-09-24
2026-09-27 01:23:23,224 [WARNING] gridflow.silver.base: Event-window filter unresolved for entsoe/countertrading on 2026-09-26 (NO_SIDECAR); filtering disabled for this partition (all-or-nothing, D-7e)
2026-09-27 01:23:23,224 [WARNING] gridflow.silver.base: No bronze data for entsoe/countertrading on 2026-09-26
```
