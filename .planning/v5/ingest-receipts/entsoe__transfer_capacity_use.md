# Ingest receipt: entsoe/transfer_capacity_use

- **Outcome:** no data: ENTSO-E answered every request for the domains gridflow queries with Acknowledgement 999 'No matching data found', on 22-25 Sep and again over a month-aligned 1 Jul - 31 Aug retry
- **When (UTC):** 2026-09-27T00:29:52Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 0 after (0 → 0 files).
- **Bronze files:** 80 before → 144 after. New bodies: 32, of which ENTSO-E "no matching data" acknowledgements: 32.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsoe transfer_capacity_use --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 42.9s
- `gridflow transform entsoe transfer_capacity_use --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 7.5s

## Retry (month-aligned, the one retry allowed; run after a review found the 4-day window gives false negatives)
- `gridflow ingest entsoe transfer_capacity_use --start 2026-07-01 --end 2026-09-01` -> exit 0, 496 responses, 496 of them 'no matching data' acknowledgements.
- `gridflow transform entsoe transfer_capacity_use --start 2026-07-01 --end 2026-09-01` -> exit 0, 0 rows transformed.
- Silver now: 0 rows in 0 files. Nothing pre-existing overwritten (silver was empty before). Bronze kept.

## Files written
- bronze:
  - `bronze/entsoe/transfer_capacity_use/2026/09/22/raw_20260927T002906Z_d6baf410.meta.json`
  - `bronze/entsoe/transfer_capacity_use/2026/09/22/raw_20260927T002906Z_d6baf410.xml`
  - `bronze/entsoe/transfer_capacity_use/2026/09/22/raw_20260927T002907Z_87f324eb.meta.json`
  - `bronze/entsoe/transfer_capacity_use/2026/09/22/raw_20260927T002907Z_87f324eb.xml`
  - `bronze/entsoe/transfer_capacity_use/2026/09/22/raw_20260927T002907Z_930a9ace.meta.json`
  - `bronze/entsoe/transfer_capacity_use/2026/09/22/raw_20260927T002907Z_930a9ace.xml`
  - `bronze/entsoe/transfer_capacity_use/2026/09/22/raw_20260927T002908Z_c010eff2.meta.json`
  - `bronze/entsoe/transfer_capacity_use/2026/09/22/raw_20260927T002908Z_c010eff2.xml`
  - `bronze/entsoe/transfer_capacity_use/2026/09/22/raw_20260927T002912Z_bbb909b0.meta.json`
  - `bronze/entsoe/transfer_capacity_use/2026/09/22/raw_20260927T002912Z_bbb909b0.xml`
  - `bronze/entsoe/transfer_capacity_use/2026/09/22/raw_20260927T002913Z_9b27eddf.meta.json`
  - `bronze/entsoe/transfer_capacity_use/2026/09/22/raw_20260927T002913Z_9b27eddf.xml`
  - … and 52 more
- silver:none

## Output tails (keys redacted)
`gridflow ingest entsoe transfer_capacity_use --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/transfer_capacity_use: 32 responses ingested
Ingestion complete
```

`gridflow transform entsoe transfer_capacity_use --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/transfer_capacity_use: 0 rows transformed
Transform complete
2026-09-27 01:29:49,483 [WARNING] gridflow.silver.base: No bronze data for entsoe/transfer_capacity_use on 2026-09-22
2026-09-27 01:29:49,486 [WARNING] gridflow.silver.base: No bronze data for entsoe/transfer_capacity_use on 2026-09-23
2026-09-27 01:29:49,490 [WARNING] gridflow.silver.base: No bronze data for entsoe/transfer_capacity_use on 2026-09-24
2026-09-27 01:29:49,493 [WARNING] gridflow.silver.base: No bronze data for entsoe/transfer_capacity_use on 2026-09-25
2026-09-27 01:29:49,493 [WARNING] gridflow.silver.base: Event-window filter unresolved for entsoe/transfer_capacity_use on 2026-09-26 (NO_SIDECAR); filtering disabled for this partition (all-or-nothing, D-7e)
2026-09-27 01:29:49,493 [WARNING] gridflow.silver.base: No bronze data for entsoe/transfer_capacity_use on 2026-09-26
```
