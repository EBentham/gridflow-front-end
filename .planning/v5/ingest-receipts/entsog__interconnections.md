# Ingest receipt: entsog/interconnections

- **Outcome:** ok
- **When (UTC):** 2026-09-27T00:30:42Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 194 after (0 → 1 files).
- **Bronze files:** 0 before → 2 after. New bodies: 1, of which ENTSO-E "no matching data" acknowledgements: 0.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsog interconnections --last 24h` (attempt 1) → exit 0 in 4.8s
- `gridflow transform entsog interconnections --last 2d` (attempt 1) → exit 0 in 6.7s

## Files written
- bronze:
  - `bronze/entsog/interconnections/2026/09/27/raw_20260927T003035Z_b9bb888f.json`
  - `bronze/entsog/interconnections/2026/09/27/raw_20260927T003035Z_b9bb888f.meta.json`
- silver:
  - `silver/entsog/interconnections/interconnections.parquet`

## Output tails (keys redacted)
`gridflow ingest entsog interconnections --last 24h` (attempt 1):
```
  entsog/interconnections: 1 responses ingested
Ingestion complete
```

`gridflow transform entsog interconnections --last 2d` (attempt 1):
```
  entsog/interconnections: 582 rows transformed
Transform complete
```
