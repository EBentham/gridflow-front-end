# Ingest receipt: entsoe/congestion_management_costs

- **Outcome:** ok on retry: 744 silver rows (vendor cadence is monthly, P1M; the 4-day window missed it, a month-aligned window found it)
- **When (UTC):** 2026-09-27T00:22:25Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 0 after (0 → 0 files).
- **Bronze files:** 60 before → 108 after. New bodies: 24, of which ENTSO-E "no matching data" acknowledgements: 24.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsoe congestion_management_costs --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 28.3s
- `gridflow transform entsoe congestion_management_costs --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 7.8s

## Retry (manual, month-aligned; the canonical note says cadence is MONTHLY / P1M)
- `gridflow ingest entsoe congestion_management_costs --start 2026-07-01 --end 2026-09-01` → exit 0, 372 responses (217 "no matching data" acknowledgements, 155 with data).
- `gridflow transform entsoe congestion_management_costs --start 2026-07-01 --end 2026-09-01` → exit 0, 744 rows transformed.
- Silver now: 744 rows in 62 files, e.g. `\silver\entsoe\congestion_management_costs\year=2026\month=07\congestion_management_costs_20260701.parquet`. Nothing pre-existing was overwritten (silver was empty before).

## Files written
- bronze:
  - `bronze/entsoe/congestion_management_costs/2026/09/22/raw_20260927T002153Z_dc86a2c5.meta.json`
  - `bronze/entsoe/congestion_management_costs/2026/09/22/raw_20260927T002153Z_dc86a2c5.xml`
  - `bronze/entsoe/congestion_management_costs/2026/09/22/raw_20260927T002154Z_6b37ae8a.meta.json`
  - `bronze/entsoe/congestion_management_costs/2026/09/22/raw_20260927T002154Z_6b37ae8a.xml`
  - `bronze/entsoe/congestion_management_costs/2026/09/22/raw_20260927T002155Z_0525b887.meta.json`
  - `bronze/entsoe/congestion_management_costs/2026/09/22/raw_20260927T002155Z_0525b887.xml`
  - `bronze/entsoe/congestion_management_costs/2026/09/22/raw_20260927T002156Z_5f76aedd.meta.json`
  - `bronze/entsoe/congestion_management_costs/2026/09/22/raw_20260927T002156Z_5f76aedd.xml`
  - `bronze/entsoe/congestion_management_costs/2026/09/22/raw_20260927T002158Z_3c820381.meta.json`
  - `bronze/entsoe/congestion_management_costs/2026/09/22/raw_20260927T002158Z_3c820381.xml`
  - `bronze/entsoe/congestion_management_costs/2026/09/22/raw_20260927T002158Z_7f7544db.meta.json`
  - `bronze/entsoe/congestion_management_costs/2026/09/22/raw_20260927T002158Z_7f7544db.xml`
  - … and 36 more
- silver:none

## Output tails (keys redacted)
`gridflow ingest entsoe congestion_management_costs --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/congestion_management_costs: 24 responses ingested
Ingestion complete
```

`gridflow transform entsoe congestion_management_costs --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/congestion_management_costs: 0 rows transformed
Transform complete
2026-09-27 01:22:22,070 [WARNING] gridflow.silver.base: No bronze data for entsoe/congestion_management_costs on 2026-09-22
2026-09-27 01:22:22,072 [WARNING] gridflow.silver.base: No bronze data for entsoe/congestion_management_costs on 2026-09-23
2026-09-27 01:22:22,073 [WARNING] gridflow.silver.base: No bronze data for entsoe/congestion_management_costs on 2026-09-24
2026-09-27 01:22:22,075 [WARNING] gridflow.silver.base: No bronze data for entsoe/congestion_management_costs on 2026-09-25
2026-09-27 01:22:22,075 [WARNING] gridflow.silver.base: No bronze data for entsoe/congestion_management_costs on 2026-09-26
```
