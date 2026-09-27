# Ingest receipt: entsog/balancing_zones

- **Outcome:** ok
- **When (UTC):** 2026-09-27T00:30:15Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 48 after (0 → 1 files).
- **Bronze files:** 0 before → 2 after. New bodies: 1, of which ENTSO-E "no matching data" acknowledgements: 0.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsog balancing_zones --last 24h` (attempt 1) → exit 0 in 4.2s
- `gridflow transform entsog balancing_zones --last 2d` (attempt 1) → exit 0 in 8.2s

## Files written
- bronze:
  - `bronze/entsog/balancing_zones/2026/09/27/raw_20260927T003006Z_a300a71c.json`
  - `bronze/entsog/balancing_zones/2026/09/27/raw_20260927T003006Z_a300a71c.meta.json`
- silver:
  - `silver/entsog/balancing_zones/balancing_zones.parquet`

## Output tails (keys redacted)
`gridflow ingest entsog balancing_zones --last 24h` (attempt 1):
```
  entsog/balancing_zones: 1 responses ingested
Ingestion complete
```

`gridflow transform entsog balancing_zones --last 2d` (attempt 1):
```
  entsog/balancing_zones: 144 rows transformed
Transform complete
```
