# Ingest receipt: entsog/urgent_market_messages

- **Outcome:** ok
- **When (UTC):** 2026-09-27T00:31:32Z
- **Data dir:** `C:\gridflow-data`. Catalogue: scratch `GRIDFLOW_DUCKDB_PATH` (the shared `gridflow.duckdb` was locked by another process; run log and watermarks for this run are not in it).
- **Silver rows:** 0 before → 133 after (0 → 1 files).
- **Bronze files:** 0 before → 2 after. New bodies: 1, of which ENTSO-E "no matching data" acknowledgements: 0.
- **Overwritten:** nothing (no pre-existing silver or bronze was rewritten; no snapshot needed).

## Commands
- `gridflow ingest entsog urgent_market_messages --start 2026-08-27 --end 2026-09-26` (attempt 1) → exit 0 in 4.5s
- `gridflow transform entsog urgent_market_messages --start 2026-08-27 --end 2026-09-26` (attempt 1) → exit 0 in 8.5s

## Files written
- bronze:
  - `bronze/entsog/urgent_market_messages/2026/09/27/raw_20260927T003123Z_423ca35e.json`
  - `bronze/entsog/urgent_market_messages/2026/09/27/raw_20260927T003123Z_423ca35e.meta.json`
- silver:
  - `silver/entsog/urgent_market_messages/urgent_market_messages.parquet`

## Output tails (keys redacted)
`gridflow ingest entsog urgent_market_messages --start 2026-08-27 --end 2026-09-26` (attempt 1):
```
  entsog/urgent_market_messages: 1 responses ingested
Ingestion complete
```

`gridflow transform entsog urgent_market_messages --start 2026-08-27 --end 2026-09-26` (attempt 1):
```
  entsog/urgent_market_messages: 4123 rows transformed
Transform complete
```
