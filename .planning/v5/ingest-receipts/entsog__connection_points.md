# Ingest receipt: entsog/connection_points

- **Outcome:** ok
- **When (UTC):** 2026-09-27T00:30:30Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 788 after (0 → 1 files).
- **Bronze files:** 0 before → 2 after. New bodies: 1, of which ENTSO-E "no matching data" acknowledgements: 0.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsog connection_points --last 24h` (attempt 1) → exit 0 in 6.8s
- `gridflow transform entsog connection_points --last 2d` (attempt 1) → exit 0 in 8.9s

## Files written
- bronze:
  - `bronze/entsog/connection_points/2026/09/27/raw_20260927T003021Z_032551b9.json`
  - `bronze/entsog/connection_points/2026/09/27/raw_20260927T003021Z_032551b9.meta.json`
- silver:
  - `silver/entsog/connection_points/connection_points.parquet`

## Output tails (keys redacted)
`gridflow ingest entsog connection_points --last 24h` (attempt 1):
```
  entsog/connection_points: 1 responses ingested
Ingestion complete
```

`gridflow transform entsog connection_points --last 2d` (attempt 1):
```
  entsog/connection_points: 2364 rows transformed
Transform complete
```
