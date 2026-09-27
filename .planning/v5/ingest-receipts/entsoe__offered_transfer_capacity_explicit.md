# Ingest receipt: entsoe/offered_transfer_capacity_explicit

- **Outcome:** no data: ENTSO-E answered every request for the domains gridflow queries with Acknowledgement 999 'No matching data found', on 22-25 Sep and again over a month-aligned 1 Jul - 31 Aug retry
- **When (UTC):** 2026-09-27T00:26:54Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 0 after (0 → 0 files).
- **Bronze files:** 80 before → 144 after. New bodies: 32, of which ENTSO-E "no matching data" acknowledgements: 32.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsoe offered_transfer_capacity_explicit --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 45.3s
- `gridflow transform entsoe offered_transfer_capacity_explicit --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 9.3s

## Retry (month-aligned, the one retry allowed; run after a review found the 4-day window gives false negatives)
- `gridflow ingest entsoe offered_transfer_capacity_explicit --start 2026-07-01 --end 2026-09-01` -> exit 0, 496 responses, 496 of them 'no matching data' acknowledgements.
- `gridflow transform entsoe offered_transfer_capacity_explicit --start 2026-07-01 --end 2026-09-01` -> exit 0, 0 rows transformed.
- Silver now: 0 rows in 0 files. Nothing pre-existing overwritten (silver was empty before). Bronze kept.

## Files written
- bronze:
  - `bronze/entsoe/offered_transfer_capacity_explicit/2026/09/22/raw_20260927T002609Z_457d6a96.meta.json`
  - `bronze/entsoe/offered_transfer_capacity_explicit/2026/09/22/raw_20260927T002609Z_457d6a96.xml`
  - `bronze/entsoe/offered_transfer_capacity_explicit/2026/09/22/raw_20260927T002610Z_279ea201.meta.json`
  - `bronze/entsoe/offered_transfer_capacity_explicit/2026/09/22/raw_20260927T002610Z_279ea201.xml`
  - `bronze/entsoe/offered_transfer_capacity_explicit/2026/09/22/raw_20260927T002612Z_0bb156c9.meta.json`
  - `bronze/entsoe/offered_transfer_capacity_explicit/2026/09/22/raw_20260927T002612Z_0bb156c9.xml`
  - `bronze/entsoe/offered_transfer_capacity_explicit/2026/09/22/raw_20260927T002612Z_bd3ed385.meta.json`
  - `bronze/entsoe/offered_transfer_capacity_explicit/2026/09/22/raw_20260927T002612Z_bd3ed385.xml`
  - `bronze/entsoe/offered_transfer_capacity_explicit/2026/09/22/raw_20260927T002613Z_3dfbf5e4.meta.json`
  - `bronze/entsoe/offered_transfer_capacity_explicit/2026/09/22/raw_20260927T002613Z_3dfbf5e4.xml`
  - `bronze/entsoe/offered_transfer_capacity_explicit/2026/09/22/raw_20260927T002614Z_e3398c91.meta.json`
  - `bronze/entsoe/offered_transfer_capacity_explicit/2026/09/22/raw_20260927T002614Z_e3398c91.xml`
  - … and 52 more
- silver:none

## Output tails (keys redacted)
`gridflow ingest entsoe offered_transfer_capacity_explicit --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/offered_transfer_capacity_explicit: 32 responses ingested
Ingestion complete
```

`gridflow transform entsoe offered_transfer_capacity_explicit --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/offered_transfer_capacity_explicit: 0 rows transformed
Transform complete
2026-09-27 01:26:50,942 [WARNING] gridflow.silver.base: No bronze data for entsoe/offered_transfer_capacity_explicit on 2026-09-22
2026-09-27 01:26:50,946 [WARNING] gridflow.silver.base: No bronze data for entsoe/offered_transfer_capacity_explicit on 2026-09-23
2026-09-27 01:26:50,952 [WARNING] gridflow.silver.base: No bronze data for entsoe/offered_transfer_capacity_explicit on 2026-09-24
2026-09-27 01:26:50,955 [WARNING] gridflow.silver.base: No bronze data for entsoe/offered_transfer_capacity_explicit on 2026-09-25
2026-09-27 01:26:50,956 [WARNING] gridflow.silver.base: Event-window filter unresolved for entsoe/offered_transfer_capacity_explicit on 2026-09-26 (NO_SIDECAR); filtering disabled for this partition (all-or-nothing, D-7e)
2026-09-27 01:26:50,957 [WARNING] gridflow.silver.base: No bronze data for entsoe/offered_transfer_capacity_explicit on 2026-09-26
```
