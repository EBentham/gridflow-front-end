# Ingest receipt: entsog/interruptions

- **Outcome:** no data from vendor: ENTSO-G returned `{"message":"No result found"}` for every day, 2026-01-01 to 2026-09-26
- **When (UTC):** 2026-09-27T00:31:19Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 0 after (0 → 0 files).
- **Bronze files:** 10 before → 70 after. New bodies: 30, of which ENTSO-E "no matching data" acknowledgements: 0.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsog interruptions --start 2026-08-27 --end 2026-09-26` (attempt 1) → exit 0 in 5.5s
- `gridflow transform entsog interruptions --start 2026-08-27 --end 2026-09-26` (attempt 1) → exit 0 in 7.7s

## Retry (manual, one allowed)
- `gridflow ingest entsog interruptions --start 2026-01-01 --end 2026-08-27` → exit 0, 238 responses ingested, every body `{"message":"No result found"}`.
- `gridflow transform entsog interruptions --start 2026-01-01 --end 2026-08-27` → exit 0, 0 rows.
- Conclusion: the vendor publishes no interruption events for gridflow's request scope in 2026. Bronze kept (never deleted).

## Files written
- bronze:
  - `bronze/entsog/interruptions/2026/08/27/raw_20260927T003110Z_29e65519.json`
  - `bronze/entsog/interruptions/2026/08/27/raw_20260927T003110Z_29e65519.meta.json`
  - `bronze/entsog/interruptions/2026/08/28/raw_20260927T003110Z_29e65519.json`
  - `bronze/entsog/interruptions/2026/08/28/raw_20260927T003110Z_29e65519.meta.json`
  - `bronze/entsog/interruptions/2026/08/29/raw_20260927T003110Z_29e65519.json`
  - `bronze/entsog/interruptions/2026/08/29/raw_20260927T003110Z_29e65519.meta.json`
  - `bronze/entsog/interruptions/2026/08/30/raw_20260927T003110Z_29e65519.json`
  - `bronze/entsog/interruptions/2026/08/30/raw_20260927T003110Z_29e65519.meta.json`
  - `bronze/entsog/interruptions/2026/08/31/raw_20260927T003110Z_29e65519.json`
  - `bronze/entsog/interruptions/2026/08/31/raw_20260927T003110Z_29e65519.meta.json`
  - `bronze/entsog/interruptions/2026/09/01/raw_20260927T003110Z_29e65519.json`
  - `bronze/entsog/interruptions/2026/09/01/raw_20260927T003110Z_29e65519.meta.json`
  - … and 48 more
- silver:none

## Output tails (keys redacted)
`gridflow ingest entsog interruptions --start 2026-08-27 --end 2026-09-26` (attempt 1):
```
  entsog/interruptions: 30 responses ingested
Ingestion complete
```

`gridflow transform entsog interruptions --start 2026-08-27 --end 2026-09-26` (attempt 1):
```
2026-09-27 01:31:16,461 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-02
2026-09-27 01:31:16,462 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-03
2026-09-27 01:31:16,462 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-04
2026-09-27 01:31:16,462 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-05
2026-09-27 01:31:16,462 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-06
2026-09-27 01:31:16,464 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-07
2026-09-27 01:31:16,464 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-08
2026-09-27 01:31:16,465 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-09
2026-09-27 01:31:16,465 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-10
2026-09-27 01:31:16,466 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-11
2026-09-27 01:31:16,466 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-12
2026-09-27 01:31:16,466 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-13
2026-09-27 01:31:16,466 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-14
2026-09-27 01:31:16,467 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-15
2026-09-27 01:31:16,467 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-16
2026-09-27 01:31:16,467 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-17
2026-09-27 01:31:16,467 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-18
2026-09-27 01:31:16,469 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-19
2026-09-27 01:31:16,469 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-20
2026-09-27 01:31:16,470 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-21
2026-09-27 01:31:16,470 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-22
2026-09-27 01:31:16,471 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-23
2026-09-27 01:31:16,471 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-24
2026-09-27 01:31:16,471 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-25
2026-09-27 01:31:16,472 [WARNING] gridflow.silver.base: No bronze data for entsog/interruptions on 2026-09-26
```
