# Ingest receipt: gie_agsi/about_listing

- **Outcome:** ok
- **When (UTC):** 2026-09-27T00:31:45Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 1,665 after (0 → 9 files).
- **Bronze files:** 0 before → 2 after. New bodies: 1, of which ENTSO-E "no matching data" acknowledgements: 0.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest gie_agsi about_listing --last 7d` (attempt 1) → exit 0 in 5.3s
- `gridflow transform gie_agsi about_listing --last 8d` (attempt 1) → exit 0 in 8.2s

## Files written
- bronze:
  - `bronze/gie_agsi/about_listing/2026/09/20/raw_20260927T003137Z_5f257f7e.json`
  - `bronze/gie_agsi/about_listing/2026/09/20/raw_20260927T003137Z_5f257f7e.meta.json`
- silver:
  - `silver/gie_agsi/about_listing/year=2026/month=09/about_listing_20260919.parquet`
  - `silver/gie_agsi/about_listing/year=2026/month=09/about_listing_20260920.parquet`
  - `silver/gie_agsi/about_listing/year=2026/month=09/about_listing_20260921.parquet`
  - `silver/gie_agsi/about_listing/year=2026/month=09/about_listing_20260922.parquet`
  - `silver/gie_agsi/about_listing/year=2026/month=09/about_listing_20260923.parquet`
  - `silver/gie_agsi/about_listing/year=2026/month=09/about_listing_20260924.parquet`
  - `silver/gie_agsi/about_listing/year=2026/month=09/about_listing_20260925.parquet`
  - `silver/gie_agsi/about_listing/year=2026/month=09/about_listing_20260926.parquet`
  - `silver/gie_agsi/about_listing/year=2026/month=09/about_listing_20260927.parquet`

## Output tails (keys redacted)
`gridflow ingest gie_agsi about_listing --last 7d` (attempt 1):
```
  gie_agsi/about_listing: 1 responses ingested
Ingestion complete
```

`gridflow transform gie_agsi about_listing --last 8d` (attempt 1):
```
  gie_agsi/about_listing: 1665 rows transformed
Transform complete
```
