# Ingest receipt: entsoe/offered_transfer_capacity_implicit

- **Outcome:** no data: ENTSO-E answered every request for the domains gridflow queries with Acknowledgement 999 'No matching data found', on 22-25 Sep and again over a month-aligned 1 Jul - 31 Aug retry
- **When (UTC):** 2026-09-27T00:27:40Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 0 after (0 → 0 files).
- **Bronze files:** 80 before → 144 after. New bodies: 32, of which ENTSO-E "no matching data" acknowledgements: 32.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsoe offered_transfer_capacity_implicit --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 38.1s
- `gridflow transform entsoe offered_transfer_capacity_implicit --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 7.5s

## Retry (month-aligned, the one retry allowed; run after a review found the 4-day window gives false negatives)
- `gridflow ingest entsoe offered_transfer_capacity_implicit --start 2026-07-01 --end 2026-09-01` -> exit 0, 496 responses, 496 of them 'no matching data' acknowledgements.
- `gridflow transform entsoe offered_transfer_capacity_implicit --start 2026-07-01 --end 2026-09-01` -> exit 0, 0 rows transformed.
- Silver now: 0 rows in 0 files. Nothing pre-existing overwritten (silver was empty before). Bronze kept.

## Files written
- bronze:
  - `bronze/entsoe/offered_transfer_capacity_implicit/2026/09/22/raw_20260927T002658Z_04b2a561.meta.json`
  - `bronze/entsoe/offered_transfer_capacity_implicit/2026/09/22/raw_20260927T002658Z_04b2a561.xml`
  - `bronze/entsoe/offered_transfer_capacity_implicit/2026/09/22/raw_20260927T002659Z_57040072.meta.json`
  - `bronze/entsoe/offered_transfer_capacity_implicit/2026/09/22/raw_20260927T002659Z_57040072.xml`
  - `bronze/entsoe/offered_transfer_capacity_implicit/2026/09/22/raw_20260927T002700Z_c5479a49.meta.json`
  - `bronze/entsoe/offered_transfer_capacity_implicit/2026/09/22/raw_20260927T002700Z_c5479a49.xml`
  - `bronze/entsoe/offered_transfer_capacity_implicit/2026/09/22/raw_20260927T002702Z_55c0e586.meta.json`
  - `bronze/entsoe/offered_transfer_capacity_implicit/2026/09/22/raw_20260927T002702Z_55c0e586.xml`
  - `bronze/entsoe/offered_transfer_capacity_implicit/2026/09/22/raw_20260927T002703Z_4a5ce552.meta.json`
  - `bronze/entsoe/offered_transfer_capacity_implicit/2026/09/22/raw_20260927T002703Z_4a5ce552.xml`
  - `bronze/entsoe/offered_transfer_capacity_implicit/2026/09/22/raw_20260927T002704Z_9d81f331.meta.json`
  - `bronze/entsoe/offered_transfer_capacity_implicit/2026/09/22/raw_20260927T002704Z_9d81f331.xml`
  - … and 52 more
- silver:none

## Output tails (keys redacted)
`gridflow ingest entsoe offered_transfer_capacity_implicit --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/offered_transfer_capacity_implicit: 32 responses ingested
Ingestion complete
```

`gridflow transform entsoe offered_transfer_capacity_implicit --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/offered_transfer_capacity_implicit: 0 rows transformed
Transform complete
2026-09-27 01:27:36,925 [WARNING] gridflow.silver.base: No bronze data for entsoe/offered_transfer_capacity_implicit on 2026-09-22
2026-09-27 01:27:36,930 [WARNING] gridflow.silver.base: No bronze data for entsoe/offered_transfer_capacity_implicit on 2026-09-23
2026-09-27 01:27:36,934 [WARNING] gridflow.silver.base: No bronze data for entsoe/offered_transfer_capacity_implicit on 2026-09-24
2026-09-27 01:27:36,939 [WARNING] gridflow.silver.base: No bronze data for entsoe/offered_transfer_capacity_implicit on 2026-09-25
2026-09-27 01:27:36,939 [WARNING] gridflow.silver.base: Event-window filter unresolved for entsoe/offered_transfer_capacity_implicit on 2026-09-26 (NO_SIDECAR); filtering disabled for this partition (all-or-nothing, D-7e)
2026-09-27 01:27:36,940 [WARNING] gridflow.silver.base: No bronze data for entsoe/offered_transfer_capacity_implicit on 2026-09-26
```
