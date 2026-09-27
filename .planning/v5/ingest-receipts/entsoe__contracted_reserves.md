# Ingest receipt: entsoe/contracted_reserves

- **Outcome:** no data: ENTSO-E answered every request for the domains gridflow queries with Acknowledgement 999 'No matching data found', on 22-25 Sep and again over a month-aligned 1 Jul - 31 Aug retry
- **When (UTC):** 2026-09-27T00:22:41Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 0 after (0 → 0 files).
- **Bronze files:** 10 before → 18 after. New bodies: 4, of which ENTSO-E "no matching data" acknowledgements: 4.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsoe contracted_reserves --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 7.9s
- `gridflow transform entsoe contracted_reserves --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 8.2s

## Retry (month-aligned, the one retry allowed; run after a review found the 4-day window gives false negatives)
- `gridflow ingest entsoe contracted_reserves --start 2026-07-01 --end 2026-09-01` -> exit 0, 62 responses, 62 of them 'no matching data' acknowledgements.
- `gridflow transform entsoe contracted_reserves --start 2026-07-01 --end 2026-09-01` -> exit 0, 0 rows transformed.
- Silver now: 0 rows in 0 files. Nothing pre-existing overwritten (silver was empty before). Bronze kept.

## Files written
- bronze:
  - `bronze/entsoe/contracted_reserves/2026/09/22/raw_20260927T002230Z_3a2347c3.meta.json`
  - `bronze/entsoe/contracted_reserves/2026/09/22/raw_20260927T002230Z_3a2347c3.xml`
  - `bronze/entsoe/contracted_reserves/2026/09/23/raw_20260927T002231Z_c77ba04c.meta.json`
  - `bronze/entsoe/contracted_reserves/2026/09/23/raw_20260927T002231Z_c77ba04c.xml`
  - `bronze/entsoe/contracted_reserves/2026/09/24/raw_20260927T002232Z_ce91837f.meta.json`
  - `bronze/entsoe/contracted_reserves/2026/09/24/raw_20260927T002232Z_ce91837f.xml`
  - `bronze/entsoe/contracted_reserves/2026/09/25/raw_20260927T002233Z_f9f4da6a.meta.json`
  - `bronze/entsoe/contracted_reserves/2026/09/25/raw_20260927T002233Z_f9f4da6a.xml`
- silver:none

## Output tails (keys redacted)
`gridflow ingest entsoe contracted_reserves --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/contracted_reserves: 4 responses ingested
Ingestion complete
```

`gridflow transform entsoe contracted_reserves --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/contracted_reserves: 0 rows transformed
Transform complete
2026-09-27 01:22:38,260 [WARNING] gridflow.silver.base: No bronze data for entsoe/contracted_reserves on 2026-09-22
2026-09-27 01:22:38,261 [WARNING] gridflow.silver.base: No bronze data for entsoe/contracted_reserves on 2026-09-23
2026-09-27 01:22:38,262 [WARNING] gridflow.silver.base: No bronze data for entsoe/contracted_reserves on 2026-09-24
2026-09-27 01:22:38,263 [WARNING] gridflow.silver.base: No bronze data for entsoe/contracted_reserves on 2026-09-25
2026-09-27 01:22:38,263 [WARNING] gridflow.silver.base: No bronze data for entsoe/contracted_reserves on 2026-09-26
```
