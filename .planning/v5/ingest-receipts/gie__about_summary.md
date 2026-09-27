# Ingest receipt: gie_agsi/about_summary

- **Outcome:** ok
- **When (UTC):** 2026-09-27T00:31:57Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 1,665 after (0 → 9 files).
- **Bronze files:** 0 before → 2 after. New bodies: 1, of which ENTSO-E "no matching data" acknowledgements: 0.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest gie_agsi about_summary --last 7d` (attempt 1) → exit 0 in 4.8s
- `gridflow transform gie_agsi about_summary --last 8d` (attempt 1) → exit 0 in 6.7s

## Files written
- bronze:
  - `bronze/gie_agsi/about_summary/2026/09/20/raw_20260927T003150Z_0659fbc3.json`
  - `bronze/gie_agsi/about_summary/2026/09/20/raw_20260927T003150Z_0659fbc3.meta.json`
- silver:
  - `silver/gie_agsi/about_summary/year=2026/month=09/about_summary_20260919.parquet`
  - `silver/gie_agsi/about_summary/year=2026/month=09/about_summary_20260920.parquet`
  - `silver/gie_agsi/about_summary/year=2026/month=09/about_summary_20260921.parquet`
  - `silver/gie_agsi/about_summary/year=2026/month=09/about_summary_20260922.parquet`
  - `silver/gie_agsi/about_summary/year=2026/month=09/about_summary_20260923.parquet`
  - `silver/gie_agsi/about_summary/year=2026/month=09/about_summary_20260924.parquet`
  - `silver/gie_agsi/about_summary/year=2026/month=09/about_summary_20260925.parquet`
  - `silver/gie_agsi/about_summary/year=2026/month=09/about_summary_20260926.parquet`
  - `silver/gie_agsi/about_summary/year=2026/month=09/about_summary_20260927.parquet`

## Output tails (keys redacted)
`gridflow ingest gie_agsi about_summary --last 7d` (attempt 1):
```
  gie_agsi/about_summary: 1 responses ingested
Ingestion complete
```

`gridflow transform gie_agsi about_summary --last 8d` (attempt 1):
```
  gie_agsi/about_summary: 1665 rows transformed
Transform complete
```
