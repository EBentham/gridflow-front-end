# Ingest receipt: entsog/operators

- **Outcome:** ok
- **When (UTC):** 2026-09-27T00:31:06Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 557 after (0 → 1 files).
- **Bronze files:** 0 before → 2 after. New bodies: 1, of which ENTSO-E "no matching data" acknowledgements: 0.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsog operators --last 24h` (attempt 1) → exit 0 in 4.3s
- `gridflow transform entsog operators --last 2d` (attempt 1) → exit 0 in 6.7s

## Files written
- bronze:
  - `bronze/entsog/operators/2026/09/27/raw_20260927T003059Z_2a217409.json`
  - `bronze/entsog/operators/2026/09/27/raw_20260927T003059Z_2a217409.meta.json`
- silver:
  - `silver/entsog/operators/operators.parquet`

## Output tails (keys redacted)
`gridflow ingest entsog operators --last 24h` (attempt 1):
```
  entsog/operators: 1 responses ingested
Ingestion complete
```

`gridflow transform entsog operators --last 2d` (attempt 1):
```
  entsog/operators: 1671 rows transformed
Transform complete
```
