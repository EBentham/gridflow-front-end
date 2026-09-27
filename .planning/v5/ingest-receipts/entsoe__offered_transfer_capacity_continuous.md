# Ingest receipt: entsoe/offered_transfer_capacity_continuous

- **Outcome:** no data: ENTSO-E answered every request for the domains gridflow queries with Acknowledgement 999 'No matching data found', on 22-25 Sep and again over a month-aligned 1 Jul - 31 Aug retry
- **When (UTC):** 2026-09-27T00:25:59Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 0 after (0 → 0 files).
- **Bronze files:** 80 before → 144 after. New bodies: 32, of which ENTSO-E "no matching data" acknowledgements: 32.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsoe offered_transfer_capacity_continuous --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 53.7s
- `gridflow transform entsoe offered_transfer_capacity_continuous --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 20.7s

## Retry (month-aligned, the one retry allowed; run after a review found the 4-day window gives false negatives)
- `gridflow ingest entsoe offered_transfer_capacity_continuous --start 2026-07-01 --end 2026-09-01` -> exit 0, 496 responses, 496 of them 'no matching data' acknowledgements.
- `gridflow transform entsoe offered_transfer_capacity_continuous --start 2026-07-01 --end 2026-09-01` -> exit 0, 0 rows transformed.
- Silver now: 0 rows in 0 files. Nothing pre-existing overwritten (silver was empty before). Bronze kept.

## Files written
- bronze:
  - `bronze/entsoe/offered_transfer_capacity_continuous/2026/09/22/raw_20260927T002458Z_f59e290f.meta.json`
  - `bronze/entsoe/offered_transfer_capacity_continuous/2026/09/22/raw_20260927T002458Z_f59e290f.xml`
  - `bronze/entsoe/offered_transfer_capacity_continuous/2026/09/22/raw_20260927T002500Z_66a71a06.meta.json`
  - `bronze/entsoe/offered_transfer_capacity_continuous/2026/09/22/raw_20260927T002500Z_66a71a06.xml`
  - `bronze/entsoe/offered_transfer_capacity_continuous/2026/09/22/raw_20260927T002500Z_81ae4700.meta.json`
  - `bronze/entsoe/offered_transfer_capacity_continuous/2026/09/22/raw_20260927T002500Z_81ae4700.xml`
  - `bronze/entsoe/offered_transfer_capacity_continuous/2026/09/22/raw_20260927T002502Z_2c19413a.meta.json`
  - `bronze/entsoe/offered_transfer_capacity_continuous/2026/09/22/raw_20260927T002502Z_2c19413a.xml`
  - `bronze/entsoe/offered_transfer_capacity_continuous/2026/09/22/raw_20260927T002503Z_d2b76c40.meta.json`
  - `bronze/entsoe/offered_transfer_capacity_continuous/2026/09/22/raw_20260927T002503Z_d2b76c40.xml`
  - `bronze/entsoe/offered_transfer_capacity_continuous/2026/09/22/raw_20260927T002505Z_742c08ca.meta.json`
  - `bronze/entsoe/offered_transfer_capacity_continuous/2026/09/22/raw_20260927T002505Z_742c08ca.xml`
  - … and 52 more
- silver:none

## Output tails (keys redacted)
`gridflow ingest entsoe offered_transfer_capacity_continuous --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/offered_transfer_capacity_continuous: 32 responses ingested
Ingestion complete
```

`gridflow transform entsoe offered_transfer_capacity_continuous --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/offered_transfer_capacity_continuous: 0 rows transformed
Transform complete
2026-09-27 01:25:53,786 [WARNING] gridflow.silver.base: No bronze data for entsoe/offered_transfer_capacity_continuous on 2026-09-22
2026-09-27 01:25:53,794 [WARNING] gridflow.silver.base: No bronze data for entsoe/offered_transfer_capacity_continuous on 2026-09-23
2026-09-27 01:25:53,802 [WARNING] gridflow.silver.base: No bronze data for entsoe/offered_transfer_capacity_continuous on 2026-09-24
2026-09-27 01:25:53,810 [WARNING] gridflow.silver.base: No bronze data for entsoe/offered_transfer_capacity_continuous on 2026-09-25
2026-09-27 01:25:53,810 [WARNING] gridflow.silver.base: Event-window filter unresolved for entsoe/offered_transfer_capacity_continuous on 2026-09-26 (NO_SIDECAR); filtering disabled for this partition (all-or-nothing, D-7e)
2026-09-27 01:25:53,810 [WARNING] gridflow.silver.base: No bronze data for entsoe/offered_transfer_capacity_continuous on 2026-09-26
```
