# Ingest receipt: entsoe/cross_zonal_balancing_capacity

- **Outcome:** no data: ENTSO-E answered every request for the domains gridflow queries with Acknowledgement 999 'No matching data found', on 22-25 Sep and again over a month-aligned 1 Jul - 31 Aug retry
- **When (UTC):** 2026-09-27T00:24:10Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 0 after (0 → 0 files).
- **Bronze files:** 80 before → 144 after. New bodies: 32, of which ENTSO-E "no matching data" acknowledgements: 32.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsoe cross_zonal_balancing_capacity --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 37.7s
- `gridflow transform entsoe cross_zonal_balancing_capacity --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 6.7s

## Retry (month-aligned, the one retry allowed; run after a review found the 4-day window gives false negatives)
- `gridflow ingest entsoe cross_zonal_balancing_capacity --start 2026-07-01 --end 2026-09-01` -> exit 0, 496 responses, 496 of them 'no matching data' acknowledgements.
- `gridflow transform entsoe cross_zonal_balancing_capacity --start 2026-07-01 --end 2026-09-01` -> exit 0, 0 rows transformed.
- Silver now: 0 rows in 0 files. Nothing pre-existing overwritten (silver was empty before). Bronze kept.

## Files written
- bronze:
  - `bronze/entsoe/cross_zonal_balancing_capacity/2026/09/22/raw_20260927T002332Z_026f5d33.meta.json`
  - `bronze/entsoe/cross_zonal_balancing_capacity/2026/09/22/raw_20260927T002332Z_026f5d33.xml`
  - `bronze/entsoe/cross_zonal_balancing_capacity/2026/09/22/raw_20260927T002333Z_49151ca0.meta.json`
  - `bronze/entsoe/cross_zonal_balancing_capacity/2026/09/22/raw_20260927T002333Z_49151ca0.xml`
  - `bronze/entsoe/cross_zonal_balancing_capacity/2026/09/22/raw_20260927T002334Z_5ee55dfa.meta.json`
  - `bronze/entsoe/cross_zonal_balancing_capacity/2026/09/22/raw_20260927T002334Z_5ee55dfa.xml`
  - `bronze/entsoe/cross_zonal_balancing_capacity/2026/09/22/raw_20260927T002335Z_60e347cd.meta.json`
  - `bronze/entsoe/cross_zonal_balancing_capacity/2026/09/22/raw_20260927T002335Z_60e347cd.xml`
  - `bronze/entsoe/cross_zonal_balancing_capacity/2026/09/22/raw_20260927T002336Z_282bd37d.meta.json`
  - `bronze/entsoe/cross_zonal_balancing_capacity/2026/09/22/raw_20260927T002336Z_282bd37d.xml`
  - `bronze/entsoe/cross_zonal_balancing_capacity/2026/09/22/raw_20260927T002337Z_abdae4be.meta.json`
  - `bronze/entsoe/cross_zonal_balancing_capacity/2026/09/22/raw_20260927T002337Z_abdae4be.xml`
  - … and 52 more
- silver:none

## Output tails (keys redacted)
`gridflow ingest entsoe cross_zonal_balancing_capacity --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/cross_zonal_balancing_capacity: 32 responses ingested
Ingestion complete
```

`gridflow transform entsoe cross_zonal_balancing_capacity --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/cross_zonal_balancing_capacity: 0 rows transformed
Transform complete
2026-09-27 01:24:08,004 [WARNING] gridflow.silver.base: No bronze data for entsoe/cross_zonal_balancing_capacity on 2026-09-22
2026-09-27 01:24:08,006 [WARNING] gridflow.silver.base: No bronze data for entsoe/cross_zonal_balancing_capacity on 2026-09-23
2026-09-27 01:24:08,007 [WARNING] gridflow.silver.base: No bronze data for entsoe/cross_zonal_balancing_capacity on 2026-09-24
2026-09-27 01:24:08,009 [WARNING] gridflow.silver.base: No bronze data for entsoe/cross_zonal_balancing_capacity on 2026-09-25
2026-09-27 01:24:08,009 [WARNING] gridflow.silver.base: No bronze data for entsoe/cross_zonal_balancing_capacity on 2026-09-26
```
