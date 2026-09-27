# Ingest receipt: entsoe/redispatching_cross_border

- **Outcome:** ok on retry: 288 silver rows (only 4 of 496 July-August responses carried data; the 4-day September window had none)
- **When (UTC):** 2026-09-27T00:29:01Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 0 after (0 → 0 files).
- **Bronze files:** 192 before → 256 after. New bodies: 32, of which ENTSO-E "no matching data" acknowledgements: 32.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsoe redispatching_cross_border --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 39.1s
- `gridflow transform entsoe redispatching_cross_border --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 7.4s

## Retry (month-aligned, the one retry allowed; run after a review found the 4-day window gives false negatives)
- `gridflow ingest entsoe redispatching_cross_border --start 2026-07-01 --end 2026-09-01` -> exit 0, 496 responses, 492 of them 'no matching data' acknowledgements.
- `gridflow transform entsoe redispatching_cross_border --start 2026-07-01 --end 2026-09-01` -> exit 0, 288 rows transformed.
- Silver now: 288 rows in 4 files, e.g. `\silver\entsoe\redispatching_cross_border\year=2026\month=07\redispatching_cross_border_20260706.parquet`. Nothing pre-existing overwritten (silver was empty before). Bronze kept.

## Files written
- bronze:
  - `bronze/entsoe/redispatching_cross_border/2026/09/22/raw_20260927T002819Z_5f4185db.meta.json`
  - `bronze/entsoe/redispatching_cross_border/2026/09/22/raw_20260927T002819Z_5f4185db.xml`
  - `bronze/entsoe/redispatching_cross_border/2026/09/22/raw_20260927T002820Z_becff154.meta.json`
  - `bronze/entsoe/redispatching_cross_border/2026/09/22/raw_20260927T002820Z_becff154.xml`
  - `bronze/entsoe/redispatching_cross_border/2026/09/22/raw_20260927T002821Z_8333f5c3.meta.json`
  - `bronze/entsoe/redispatching_cross_border/2026/09/22/raw_20260927T002821Z_8333f5c3.xml`
  - `bronze/entsoe/redispatching_cross_border/2026/09/22/raw_20260927T002825Z_2141ad75.meta.json`
  - `bronze/entsoe/redispatching_cross_border/2026/09/22/raw_20260927T002825Z_2141ad75.xml`
  - `bronze/entsoe/redispatching_cross_border/2026/09/22/raw_20260927T002827Z_710dae8a.meta.json`
  - `bronze/entsoe/redispatching_cross_border/2026/09/22/raw_20260927T002827Z_710dae8a.xml`
  - `bronze/entsoe/redispatching_cross_border/2026/09/22/raw_20260927T002827Z_bb2fcdea.meta.json`
  - `bronze/entsoe/redispatching_cross_border/2026/09/22/raw_20260927T002827Z_bb2fcdea.xml`
  - … and 52 more
- silver:none

## Output tails (keys redacted)
`gridflow ingest entsoe redispatching_cross_border --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/redispatching_cross_border: 32 responses ingested
Ingestion complete
```

`gridflow transform entsoe redispatching_cross_border --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/redispatching_cross_border: 0 rows transformed
Transform complete
2026-09-27 01:28:58,843 [WARNING] gridflow.silver.base: No bronze data for entsoe/redispatching_cross_border on 2026-09-22
2026-09-27 01:28:58,846 [WARNING] gridflow.silver.base: No bronze data for entsoe/redispatching_cross_border on 2026-09-23
2026-09-27 01:28:58,849 [WARNING] gridflow.silver.base: No bronze data for entsoe/redispatching_cross_border on 2026-09-24
2026-09-27 01:28:58,851 [WARNING] gridflow.silver.base: No bronze data for entsoe/redispatching_cross_border on 2026-09-25
2026-09-27 01:28:58,852 [WARNING] gridflow.silver.base: Event-window filter unresolved for entsoe/redispatching_cross_border on 2026-09-26 (NO_SIDECAR); filtering disabled for this partition (all-or-nothing, D-7e)
2026-09-27 01:28:58,852 [WARNING] gridflow.silver.base: No bronze data for entsoe/redispatching_cross_border on 2026-09-26
```
