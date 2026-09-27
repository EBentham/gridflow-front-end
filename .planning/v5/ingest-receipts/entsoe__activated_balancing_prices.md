# Ingest receipt: entsoe/activated_balancing_prices

- **Outcome:** no data: ENTSO-E answered every request for the domains gridflow queries with Acknowledgement 999 'No matching data found', on 22-25 Sep and again over a month-aligned 1 Jul - 31 Aug retry
- **When (UTC):** 2026-09-27T00:19:46Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 0 after (0 → 0 files).
- **Bronze files:** 10 before → 18 after. New bodies: 4, of which ENTSO-E "no matching data" acknowledgements: 4.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsoe activated_balancing_prices --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 8.0s
- `gridflow transform entsoe activated_balancing_prices --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 6.5s

## Retry (month-aligned, the one retry allowed; run after a review found the 4-day window gives false negatives)
- `gridflow ingest entsoe activated_balancing_prices --start 2026-07-01 --end 2026-09-01` -> exit 0, 62 responses, 62 of them 'no matching data' acknowledgements.
- `gridflow transform entsoe activated_balancing_prices --start 2026-07-01 --end 2026-09-01` -> exit 0, 0 rows transformed.
- Silver now: 0 rows in 0 files. Nothing pre-existing overwritten (silver was empty before). Bronze kept.

## Files written
- bronze:
  - `bronze/entsoe/activated_balancing_prices/2026/09/22/raw_20260927T001937Z_aad6db52.meta.json`
  - `bronze/entsoe/activated_balancing_prices/2026/09/22/raw_20260927T001937Z_aad6db52.xml`
  - `bronze/entsoe/activated_balancing_prices/2026/09/23/raw_20260927T001938Z_f84273c7.meta.json`
  - `bronze/entsoe/activated_balancing_prices/2026/09/23/raw_20260927T001938Z_f84273c7.xml`
  - `bronze/entsoe/activated_balancing_prices/2026/09/24/raw_20260927T001939Z_9f2ab763.meta.json`
  - `bronze/entsoe/activated_balancing_prices/2026/09/24/raw_20260927T001939Z_9f2ab763.xml`
  - `bronze/entsoe/activated_balancing_prices/2026/09/25/raw_20260927T001940Z_58903cdf.meta.json`
  - `bronze/entsoe/activated_balancing_prices/2026/09/25/raw_20260927T001940Z_58903cdf.xml`
- silver:none

## Output tails (keys redacted)
`gridflow ingest entsoe activated_balancing_prices --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/activated_balancing_prices: 4 responses ingested
Ingestion complete
```

`gridflow transform entsoe activated_balancing_prices --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/activated_balancing_prices: 0 rows transformed
Transform complete
2026-09-27 01:19:44,304 [WARNING] gridflow.silver.base: No bronze data for entsoe/activated_balancing_prices on 2026-09-22
2026-09-27 01:19:44,305 [WARNING] gridflow.silver.base: No bronze data for entsoe/activated_balancing_prices on 2026-09-23
2026-09-27 01:19:44,305 [WARNING] gridflow.silver.base: No bronze data for entsoe/activated_balancing_prices on 2026-09-24
2026-09-27 01:19:44,306 [WARNING] gridflow.silver.base: No bronze data for entsoe/activated_balancing_prices on 2026-09-25
2026-09-27 01:19:44,306 [WARNING] gridflow.silver.base: Event-window filter unresolved for entsoe/activated_balancing_prices on 2026-09-26 (NO_SIDECAR); filtering disabled for this partition (all-or-nothing, D-7e)
2026-09-27 01:19:44,306 [WARNING] gridflow.silver.base: No bronze data for entsoe/activated_balancing_prices on 2026-09-26
```
