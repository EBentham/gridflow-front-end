# Ingest receipt: entsog/aggregate_interconnections

- **Outcome:** ok
- **When (UTC):** 2026-09-27T00:30:02Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 27 after (0 → 1 files).
- **Bronze files:** 0 before → 2 after. New bodies: 1, of which ENTSO-E "no matching data" acknowledgements: 0.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsog aggregate_interconnections --last 24h` (attempt 1) → exit 0 in 4.5s
- `gridflow transform entsog aggregate_interconnections --last 2d` (attempt 1) → exit 0 in 6.3s

## Files written
- bronze:
  - `bronze/entsog/aggregate_interconnections/2026/09/27/raw_20260927T002956Z_95978fa8.json`
  - `bronze/entsog/aggregate_interconnections/2026/09/27/raw_20260927T002956Z_95978fa8.meta.json`
- silver:
  - `silver/entsog/aggregate_interconnections/aggregate_interconnections.parquet`

## Output tails (keys redacted)
`gridflow ingest entsog aggregate_interconnections --last 24h` (attempt 1):
```
  entsog/aggregate_interconnections: 1 responses ingested
Ingestion complete
```

`gridflow transform entsog aggregate_interconnections --last 2d` (attempt 1):
```
  entsog/aggregate_interconnections: 81 rows transformed
Transform complete
```
