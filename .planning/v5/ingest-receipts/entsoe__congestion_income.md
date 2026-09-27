# Ingest receipt: entsoe/congestion_income

- **Outcome:** no data: ENTSO-E answered every request for the domains gridflow queries with Acknowledgement 999 'No matching data found', on 22-25 Sep and again over a month-aligned 1 Jul - 31 Aug retry
- **When (UTC):** 2026-09-27T00:21:49Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 0 after (0 → 0 files).
- **Bronze files:** 80 before → 144 after. New bodies: 32, of which ENTSO-E "no matching data" acknowledgements: 32.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsoe congestion_income --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 38.3s
- `gridflow transform entsoe congestion_income --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 7.5s

## Retry (month-aligned, the one retry allowed; run after a review found the 4-day window gives false negatives)
- `gridflow ingest entsoe congestion_income --start 2026-07-01 --end 2026-09-01` -> exit 0, 496 responses, 496 of them 'no matching data' acknowledgements.
- `gridflow transform entsoe congestion_income --start 2026-07-01 --end 2026-09-01` -> exit 0, 0 rows transformed.
- Silver now: 0 rows in 0 files. Nothing pre-existing overwritten (silver was empty before). Bronze kept.

## Files written
- bronze:
  - `bronze/entsoe/congestion_income/2026/09/22/raw_20260927T002110Z_2a29d94e.meta.json`
  - `bronze/entsoe/congestion_income/2026/09/22/raw_20260927T002110Z_2a29d94e.xml`
  - `bronze/entsoe/congestion_income/2026/09/22/raw_20260927T002111Z_feed1996.meta.json`
  - `bronze/entsoe/congestion_income/2026/09/22/raw_20260927T002111Z_feed1996.xml`
  - `bronze/entsoe/congestion_income/2026/09/22/raw_20260927T002112Z_0b71cfb5.meta.json`
  - `bronze/entsoe/congestion_income/2026/09/22/raw_20260927T002112Z_0b71cfb5.xml`
  - `bronze/entsoe/congestion_income/2026/09/22/raw_20260927T002113Z_49d281fc.meta.json`
  - `bronze/entsoe/congestion_income/2026/09/22/raw_20260927T002113Z_49d281fc.xml`
  - `bronze/entsoe/congestion_income/2026/09/22/raw_20260927T002114Z_aed7cdae.meta.json`
  - `bronze/entsoe/congestion_income/2026/09/22/raw_20260927T002114Z_aed7cdae.xml`
  - `bronze/entsoe/congestion_income/2026/09/22/raw_20260927T002115Z_18a00d3d.meta.json`
  - `bronze/entsoe/congestion_income/2026/09/22/raw_20260927T002115Z_18a00d3d.xml`
  - … and 52 more
- silver:none

## Output tails (keys redacted)
`gridflow ingest entsoe congestion_income --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/congestion_income: 32 responses ingested
Ingestion complete
```

`gridflow transform entsoe congestion_income --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/congestion_income: 0 rows transformed
Transform complete
2026-09-27 01:21:46,563 [WARNING] gridflow.silver.base: No bronze data for entsoe/congestion_income on 2026-09-22
2026-09-27 01:21:46,565 [WARNING] gridflow.silver.base: No bronze data for entsoe/congestion_income on 2026-09-23
2026-09-27 01:21:46,566 [WARNING] gridflow.silver.base: No bronze data for entsoe/congestion_income on 2026-09-24
2026-09-27 01:21:46,568 [WARNING] gridflow.silver.base: No bronze data for entsoe/congestion_income on 2026-09-25
2026-09-27 01:21:46,568 [WARNING] gridflow.silver.base: No bronze data for entsoe/congestion_income on 2026-09-26
```
