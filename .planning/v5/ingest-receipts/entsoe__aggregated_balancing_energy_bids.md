# Ingest receipt: entsoe/aggregated_balancing_energy_bids

- **Outcome:** ok
- **When (UTC):** 2026-09-27T00:20:36Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 768 after (0 → 4 files).
- **Bronze files:** 60 before → 108 after. New bodies: 24, of which ENTSO-E "no matching data" acknowledgements: 20.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsoe aggregated_balancing_energy_bids --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 31.1s
- `gridflow transform entsoe aggregated_balancing_energy_bids --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 8.9s

## Files written
- bronze:
  - `bronze/entsoe/aggregated_balancing_energy_bids/2026/09/22/raw_20260927T002001Z_c106356d.meta.json`
  - `bronze/entsoe/aggregated_balancing_energy_bids/2026/09/22/raw_20260927T002001Z_c106356d.xml`
  - `bronze/entsoe/aggregated_balancing_energy_bids/2026/09/22/raw_20260927T002003Z_35e099d3.meta.json`
  - `bronze/entsoe/aggregated_balancing_energy_bids/2026/09/22/raw_20260927T002003Z_35e099d3.xml`
  - `bronze/entsoe/aggregated_balancing_energy_bids/2026/09/22/raw_20260927T002004Z_3c4879e6.meta.json`
  - `bronze/entsoe/aggregated_balancing_energy_bids/2026/09/22/raw_20260927T002004Z_3c4879e6.xml`
  - `bronze/entsoe/aggregated_balancing_energy_bids/2026/09/22/raw_20260927T002005Z_d0fb22c5.meta.json`
  - `bronze/entsoe/aggregated_balancing_energy_bids/2026/09/22/raw_20260927T002005Z_d0fb22c5.xml`
  - `bronze/entsoe/aggregated_balancing_energy_bids/2026/09/22/raw_20260927T002006Z_d6eb5fbe.meta.json`
  - `bronze/entsoe/aggregated_balancing_energy_bids/2026/09/22/raw_20260927T002006Z_d6eb5fbe.xml`
  - `bronze/entsoe/aggregated_balancing_energy_bids/2026/09/22/raw_20260927T002007Z_06189df2.meta.json`
  - `bronze/entsoe/aggregated_balancing_energy_bids/2026/09/22/raw_20260927T002007Z_06189df2.xml`
  - … and 36 more
- silver:
  - `silver/entsoe/aggregated_balancing_energy_bids/year=2026/month=09/aggregated_balancing_energy_bids_20260922.parquet`
  - `silver/entsoe/aggregated_balancing_energy_bids/year=2026/month=09/aggregated_balancing_energy_bids_20260923.parquet`
  - `silver/entsoe/aggregated_balancing_energy_bids/year=2026/month=09/aggregated_balancing_energy_bids_20260924.parquet`
  - `silver/entsoe/aggregated_balancing_energy_bids/year=2026/month=09/aggregated_balancing_energy_bids_20260925.parquet`

## Output tails (keys redacted)
`gridflow ingest entsoe aggregated_balancing_energy_bids --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/aggregated_balancing_energy_bids: 24 responses ingested
Ingestion complete
```

`gridflow transform entsoe aggregated_balancing_energy_bids --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/aggregated_balancing_energy_bids: 768 rows transformed
Transform complete
2026-09-27 01:20:32,628 [WARNING] gridflow.silver.base: No bronze data for entsoe/aggregated_balancing_energy_bids on 2026-09-26
```
