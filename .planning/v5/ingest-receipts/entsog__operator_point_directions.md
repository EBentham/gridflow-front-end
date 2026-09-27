# Ingest receipt: entsog/operator_point_directions

- **Outcome:** ok
- **When (UTC):** 2026-09-27T00:30:55Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 1,225 after (0 → 1 files).
- **Bronze files:** 0 before → 2 after. New bodies: 1, of which ENTSO-E "no matching data" acknowledgements: 0.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsog operator_point_directions --last 24h` (attempt 1) → exit 0 in 6.0s
- `gridflow transform entsog operator_point_directions --last 2d` (attempt 1) → exit 0 in 6.7s

## Files written
- bronze:
  - `bronze/entsog/operator_point_directions/2026/09/27/raw_20260927T003048Z_c057dd9a.json`
  - `bronze/entsog/operator_point_directions/2026/09/27/raw_20260927T003048Z_c057dd9a.meta.json`
- silver:
  - `silver/entsog/operator_point_directions/operator_point_directions.parquet`

## Output tails (keys redacted)
`gridflow ingest entsog operator_point_directions --last 24h` (attempt 1):
```
  entsog/operator_point_directions: 1 responses ingested
Ingestion complete
```

`gridflow transform entsog operator_point_directions --last 2d` (attempt 1):
```
  entsog/operator_point_directions: 3675 rows transformed
Transform complete
```
