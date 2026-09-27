# Ingest receipt: entsoe/outages_offshore_grid

- **Outcome:** ok
- **When (UTC):** 2026-09-27T00:28:15Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 4 after (0 → 4 files).
- **Bronze files:** 144 before → 192 after. New bodies: 24, of which ENTSO-E "no matching data" acknowledgements: 20.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsoe outages_offshore_grid --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 28.3s
- `gridflow transform entsoe outages_offshore_grid --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 6.8s

## Files written
- bronze:
  - `bronze/entsoe/outages_offshore_grid/2026/09/22/raw_20260927T002744Z_8c1af72e.meta.json`
  - `bronze/entsoe/outages_offshore_grid/2026/09/22/raw_20260927T002744Z_8c1af72e.xml`
  - `bronze/entsoe/outages_offshore_grid/2026/09/22/raw_20260927T002745Z_0eacb3d5.meta.json`
  - `bronze/entsoe/outages_offshore_grid/2026/09/22/raw_20260927T002745Z_0eacb3d5.xml`
  - `bronze/entsoe/outages_offshore_grid/2026/09/22/raw_20260927T002747Z_7acbe9d7.meta.json`
  - `bronze/entsoe/outages_offshore_grid/2026/09/22/raw_20260927T002747Z_7acbe9d7.xml`
  - `bronze/entsoe/outages_offshore_grid/2026/09/22/raw_20260927T002747Z_bd99947a.meta.json`
  - `bronze/entsoe/outages_offshore_grid/2026/09/22/raw_20260927T002747Z_bd99947a.xml`
  - `bronze/entsoe/outages_offshore_grid/2026/09/22/raw_20260927T002748Z_9c39354f.meta.json`
  - `bronze/entsoe/outages_offshore_grid/2026/09/22/raw_20260927T002748Z_9c39354f.xml`
  - `bronze/entsoe/outages_offshore_grid/2026/09/22/raw_20260927T002749Z_a048d1cb.meta.json`
  - `bronze/entsoe/outages_offshore_grid/2026/09/22/raw_20260927T002749Z_a048d1cb.xml`
  - … and 36 more
- silver:
  - `silver/entsoe/outages_offshore_grid/year=2026/month=09/outages_offshore_grid_20260922.parquet`
  - `silver/entsoe/outages_offshore_grid/year=2026/month=09/outages_offshore_grid_20260923.parquet`
  - `silver/entsoe/outages_offshore_grid/year=2026/month=09/outages_offshore_grid_20260924.parquet`
  - `silver/entsoe/outages_offshore_grid/year=2026/month=09/outages_offshore_grid_20260925.parquet`

## Output tails (keys redacted)
`gridflow ingest entsoe outages_offshore_grid --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/outages_offshore_grid: 24 responses ingested
Ingestion complete
```

`gridflow transform entsoe outages_offshore_grid --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/outages_offshore_grid: 4 rows transformed
Transform complete
2026-09-27 01:28:12,429 [WARNING] gridflow.connectors.entsoe.parsers: Skipping ENTSO-E A03 forward-fill for document QBsoKMPWpXESvc4wPw7QIQ series 1: missing or unmapped resolution
2026-09-27 01:28:12,527 [WARNING] gridflow.connectors.entsoe.parsers: Skipping ENTSO-E A03 forward-fill for document QBsoKMPWpXESvc4wPw7QIQ series 1: missing or unmapped resolution
2026-09-27 01:28:12,532 [WARNING] gridflow.connectors.entsoe.parsers: Skipping ENTSO-E A03 forward-fill for document QBsoKMPWpXESvc4wPw7QIQ series 1: missing or unmapped resolution
2026-09-27 01:28:12,538 [WARNING] gridflow.connectors.entsoe.parsers: Skipping ENTSO-E A03 forward-fill for document QBsoKMPWpXESvc4wPw7QIQ series 1: missing or unmapped resolution
2026-09-27 01:28:12,543 [WARNING] gridflow.silver.base: No bronze data for entsoe/outages_offshore_grid on 2026-09-26
```
