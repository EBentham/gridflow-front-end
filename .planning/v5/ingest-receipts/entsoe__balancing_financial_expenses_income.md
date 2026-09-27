# Ingest receipt: entsoe/balancing_financial_expenses_income

- **Outcome:** no data: every request for the GB control area (A87) answered with Acknowledgement 999, in a 4-day September window and a month-aligned July–August retry
- **When (UTC):** 2026-09-27T00:20:54Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 0 after (0 → 0 files).
- **Bronze files:** 10 before → 18 after. New bodies: 4, of which ENTSO-E "no matching data" acknowledgements: 4.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsoe balancing_financial_expenses_income --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 8.6s
- `gridflow transform entsoe balancing_financial_expenses_income --start 2026-09-22 --end 2026-09-26` (attempt 1) → exit 0 in 8.8s

## Retry (manual, month-aligned; cadence is MONTHLY / P1M per the canonical note)
- `gridflow ingest entsoe balancing_financial_expenses_income --start 2026-07-01 --end 2026-09-01` → exit 0, 62 responses, all 62 "no matching data" acknowledgements.
- `gridflow transform ... --start 2026-07-01 --end 2026-09-01` → exit 0, 0 rows. Bronze kept.

## Files written
- bronze:
  - `bronze/entsoe/balancing_financial_expenses_income/2026/09/22/raw_20260927T002042Z_8f9cfca8.meta.json`
  - `bronze/entsoe/balancing_financial_expenses_income/2026/09/22/raw_20260927T002042Z_8f9cfca8.xml`
  - `bronze/entsoe/balancing_financial_expenses_income/2026/09/23/raw_20260927T002043Z_8d39efb7.meta.json`
  - `bronze/entsoe/balancing_financial_expenses_income/2026/09/23/raw_20260927T002043Z_8d39efb7.xml`
  - `bronze/entsoe/balancing_financial_expenses_income/2026/09/24/raw_20260927T002044Z_6f3c017f.meta.json`
  - `bronze/entsoe/balancing_financial_expenses_income/2026/09/24/raw_20260927T002044Z_6f3c017f.xml`
  - `bronze/entsoe/balancing_financial_expenses_income/2026/09/25/raw_20260927T002045Z_a3a670c2.meta.json`
  - `bronze/entsoe/balancing_financial_expenses_income/2026/09/25/raw_20260927T002045Z_a3a670c2.xml`
- silver:none

## Output tails (keys redacted)
`gridflow ingest entsoe balancing_financial_expenses_income --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/balancing_financial_expenses_income: 4 responses ingested
Ingestion complete
```

`gridflow transform entsoe balancing_financial_expenses_income --start 2026-09-22 --end 2026-09-26` (attempt 1):
```
  entsoe/balancing_financial_expenses_income: 0 rows transformed
Transform complete
2026-09-27 01:20:50,396 [WARNING] gridflow.silver.base: No bronze data for entsoe/balancing_financial_expenses_income on 2026-09-22
2026-09-27 01:20:50,397 [WARNING] gridflow.silver.base: No bronze data for entsoe/balancing_financial_expenses_income on 2026-09-23
2026-09-27 01:20:50,397 [WARNING] gridflow.silver.base: No bronze data for entsoe/balancing_financial_expenses_income on 2026-09-24
2026-09-27 01:20:50,398 [WARNING] gridflow.silver.base: No bronze data for entsoe/balancing_financial_expenses_income on 2026-09-25
2026-09-27 01:20:50,399 [WARNING] gridflow.silver.base: No bronze data for entsoe/balancing_financial_expenses_income on 2026-09-26
```
