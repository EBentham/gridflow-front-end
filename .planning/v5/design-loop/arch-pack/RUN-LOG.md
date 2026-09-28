# Run log: arch-pack snippets

Run 2026-09-27 by claude-opus-5-5, from the gridflow repo (`master` at 2822d38) with its own venv:

```
cd C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow
.venv\Scripts\python.exe ..\gridflow-front-end\.planning\v5\design-loop\arch-pack\_verify.py
```

Read-only throughout: DuckDB opened with `read_only=True`; the gold builder's `build()` called (it returns a frame; `run()` is what writes); no ingest, transform, build, init, reset or prune; no network calls (the connector snippet only builds the request path). The gold directory is listed before and after: 69 files both times, no `system_marginal_price` written. The DuckDB session sets `TimeZone = 'UTC'` for display only. Exit code 0.

## Result per snippet

| Snippet | How checked | Result |
|---|---|---|
| `01-cli.sh` | Not executed (both commands write). `gridflow ingest/transform/build --help` run; `--start` and `--end` present on all three; `gridflow --help` lists 11 commands | UNVERIFIED by execution (writes); options GREEN |
| `02-connector-request.py` | Executed | GREEN: prints `/balancing/settlement/system-prices/2026-09-08 {'page': 1}` |
| `02-connector-request.txt` | Compared with `request_url` in both real sidecars | GREEN: identical |
| `03-bronze-files.txt` | Compared with the real directory listing | GREEN |
| `03-bronze-body-excerpt.json` | Every shown field compared with the real body (8 of 22 fields, 1 of 44 records) | GREEN |
| `03-bronze-sidecar.json` | Compared with the real sidecar as parsed JSON | GREEN: equal |
| `04-silver-files.txt` | Compared with the real directory; each `_run` suffix equals its bronze sidecar's `written_at` | GREEN |
| `04-silver-vintages.sql` | Executed on the catalogue (read-only) | GREEN: 2 rows, 9.56 and 110.0 |
| `05-latest-view-ddl.sql` | Rendered by `latest_view_sql(...)` from gridflow and compared (whitespace-insensitive); also compared by eye with the SQL stored in the catalogue | GREEN |
| `05-latest-view.sql` | Executed | GREEN: 1 row, 110.0 |
| `05-as-of.sql` | Executed (as of 2026-09-09 12:00 UTC) | GREEN: 1 row, 9.56 |
| `06-gold-build.sh` | Not executed (writes gold). `gridflow build --help` checked | UNVERIFIED by execution (writes); options GREEN |
| `06-gold-spread.py` | One-line excerpt of `gold/system_marginal_price.py:48`; exercised by `06-gold-build.py` | GREEN (via 06-gold-build.py) |
| `06-gold-build.py` | Executed, `build()` only | GREEN: spread 0.0, abs_imbalance 346.717783, hour_of_day 17, day_of_week 2 |
| `07-client.py` | Executed (no-arg `GridflowClient()`, which resolves the catalogue from settings) | GREEN: 1 row, 110.0 |
| `08-run-tracking.sql` | Table definition; its column list compared with the catalogue's `pipeline_runs` columns | GREEN: match |

Extra check: the rows' `source_run_id` joins to a `pipeline_runs` row with `operation = transform`.

## Observations kept out of the copy

- The transform run that wrote both example vintages (`494e780a-...`, 2026-09-16) is recorded in `pipeline_runs` as `failed` with `rows_out = 0`. Its error names a different date whose bronze had no usable sidecar timestamp; the 2026-09-08 files were written earlier in the same run and kept its id. So a silver row's `source_run_id` can point at a run whose final status is `failed`. That is why the run-tracking snippet is the table definition, not this run's row. Possibly worth a gridflow issue; not a page claim.
- Earlier draft of `07-client.py` printed `available_at` as `2026-09-09 18:44:29 BST`: the client returns timestamps in the machine's timezone. The snippet now converts to UTC so every stop shows the same instant.
- Every example row is labelled `vintage_policy = vendor`, so the publication-lag fallback did not stamp it.

## Full output of the final run

```text

===== gold directory before =====
69 files; system_marginal_price present: False

===== 01-cli.sh (options checked with --help, not executed: ingest/transform write) =====
ingest True True
transform True True
build True True

===== 02-connector-request.py =====
/balancing/settlement/system-prices/2026-09-08 {'page': 1}
sidecar request_url (capture 1): https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/2026-09-08?page=1
sidecar request_url (capture 2): https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/2026-09-08?page=1
02-connector-request.txt matches sidecar: True

===== 03-bronze-files.txt =====
['raw_20260908T214403Z_3a7fca58.json', 'raw_20260908T214403Z_3a7fca58.meta.json', 'raw_20260916T190532Z_4c2c01b2.json', 'raw_20260916T190532Z_4c2c01b2.meta.json']
listing matches disk: True

===== 03-bronze-body-excerpt.json (every excerpt field equals the real body) =====
metadata equal: True
fields equal: True fields shown: 8 of 22
capture 2, SP37: {'settlementDate': '2026-09-08', 'settlementPeriod': 37, 'startTime': '2026-09-08T17:00:00Z', 'createdDateTime': '2026-09-09T17:44:29Z', 'systemSellPrice': 110.0, 'systemBuyPrice': 110.0, 'priceDerivationCode': 'N', 'netImbalanceVolume': -346.7177825220955}

===== 03-bronze-sidecar.json equals the real sidecar =====
True

===== 04-silver-files.txt =====
['system_prices_20260908_run2026-09-08T21-44-03.546999-00-00.parquet', 'system_prices_20260908_run2026-09-16T19-05-32.981753-00-00.parquet']
listing matches disk: True
run stamp 1 == sidecar written_at: True
run stamp 2 == sidecar written_at: True

===== 04-silver-vintages.sql =====
shape: (2, 8)
┌─────────────────┬───────────────────┬───────────────────┬──────────────────┬─────────────────────────┬────────────────┬──────────────────────────────────────┬─────────────────┐
│ settlement_date ┆ settlement_period ┆ system_sell_price ┆ system_buy_price ┆ available_at            ┆ vintage_policy ┆ source_run_id                        ┆ dataset_version │
│ ---             ┆ ---               ┆ ---               ┆ ---              ┆ ---                     ┆ ---            ┆ ---                                  ┆ ---             │
│ date            ┆ i32               ┆ f64               ┆ f64              ┆ datetime[μs, UTC]       ┆ str            ┆ str                                  ┆ str             │
╞═════════════════╪═══════════════════╪═══════════════════╪══════════════════╪═════════════════════════╪════════════════╪══════════════════════════════════════╪═════════════════╡
│ 2026-09-08      ┆ 37                ┆ 9.56              ┆ 9.56             ┆ 2026-09-08 17:48:45 UTC ┆ vendor         ┆ 494e780a-a127-4fa8-b371-25caf146c094 ┆ 2.0.0           │
│ 2026-09-08      ┆ 37                ┆ 110.0             ┆ 110.0            ┆ 2026-09-09 17:44:29 UTC ┆ vendor         ┆ 494e780a-a127-4fa8-b371-25caf146c094 ┆ 2.0.0           │
└─────────────────┴───────────────────┴───────────────────┴──────────────────┴─────────────────────────┴────────────────┴──────────────────────────────────────┴─────────────────┘

===== 05-latest-view.sql =====
shape: (1, 5)
┌─────────────────┬───────────────────┬───────────────────┬──────────────────┬─────────────────────────┐
│ settlement_date ┆ settlement_period ┆ system_sell_price ┆ system_buy_price ┆ available_at            │
│ ---             ┆ ---               ┆ ---               ┆ ---              ┆ ---                     │
│ date            ┆ i32               ┆ f64               ┆ f64              ┆ datetime[μs, UTC]       │
╞═════════════════╪═══════════════════╪═══════════════════╪══════════════════╪═════════════════════════╡
│ 2026-09-08      ┆ 37                ┆ 110.0             ┆ 110.0            ┆ 2026-09-09 17:44:29 UTC │
└─────────────────┴───────────────────┴───────────────────┴──────────────────┴─────────────────────────┘

===== 05-as-of.sql =====
shape: (1, 4)
┌─────────────────┬───────────────────┬───────────────────┬─────────────────────────┐
│ settlement_date ┆ settlement_period ┆ system_sell_price ┆ available_at            │
│ ---             ┆ ---               ┆ ---               ┆ ---                     │
│ date            ┆ i32               ┆ f64               ┆ datetime[μs, UTC]       │
╞═════════════════╪═══════════════════╪═══════════════════╪═════════════════════════╡
│ 2026-09-08      ┆ 37                ┆ 9.56              ┆ 2026-09-08 17:48:45 UTC │
└─────────────────┴───────────────────┴───────────────────┴─────────────────────────┘

===== 04: source_run_id resolves to a transform row in pipeline_runs =====
shape: (1, 2)
┌──────────────────────────────────────┬───────────┐
│ source_run_id                        ┆ operation │
│ ---                                  ┆ ---       │
│ str                                  ┆ str       │
╞══════════════════════════════════════╪═══════════╡
│ 494e780a-a127-4fa8-b371-25caf146c094 ┆ transform │
└──────────────────────────────────────┴───────────┘

===== 08-run-tracking.sql (table definition; columns compared with the catalogue) =====
['run_id', 'source', 'dataset', 'operation', 'started_at', 'completed_at', 'status', 'rows_in', 'rows_out', 'rows_skipped', 'duration_seconds', 'error_message', 'parameters']
columns match catalogue: True
tables: ['pipeline_runs', 'pipeline_watermarks', 'quality_reports']

===== 05-latest-view-ddl.sql (rendered by gridflow, compared with the catalogue) =====
CREATE OR REPLACE VIEW "silver_elexon_system_prices_latest" AS SELECT * FROM "silver_elexon_system_prices" QUALIFY ROW_NUMBER() OVER (PARTITION BY "settlement_date", "settlement_period" ORDER BY "available_at" DESC NULLS LAST, CASE "run_type" WHEN 'II' THEN 1 WHEN 'SF' THEN 2 WHEN 'R1' THEN 3 WHEN 'R2' THEN 4 WHEN 'R3' THEN 5 WHEN 'RF' THEN 6 WHEN 'DF' THEN 7 ELSE 0 END DESC) = 1
catalogue stored sql: CREATE VIEW silver_elexon_system_prices_latest AS SELECT * FROM silver_elexon_system_prices QUALIFY (row_number() OVER (PARTITION BY settlement_date, settlement_period ORDER BY available_at DESC NULLS LAST, CASE  WHEN ((run_type = 'II')) THEN (1) WHEN ((run_type = 'SF')) THEN (2) WHEN ((run_type = 'R1')) THEN (3) WHEN ((run_type = 'R2')) THEN (4) WHEN ((run_type = 'R3')) THEN (5) WHEN ((run_type = 'RF')) THEN (6) WHEN ((run_type = 'DF')) THEN (7) ELSE 0 END DESC) = 1);
snippet file equals rendered DDL (whitespace-insensitive): True

===== vintage_policy labels on this period, and base-view vintage count per key =====
shape: (1, 2)
┌────────────────┬─────┐
│ vintage_policy ┆ n   │
│ ---            ┆ --- │
│ str            ┆ i64 │
╞════════════════╪═════╡
│ vendor         ┆ 92  │
└────────────────┴─────┘

===== 06-gold-build.py (build() only; nothing written) =====
shape: (1, 8)
┌─────────────────┬───────────────────┬──────────────────┬───────────────────┬────────┬───────────────┬─────────────┬─────────────┐
│ settlement_date ┆ settlement_period ┆ system_buy_price ┆ system_sell_price ┆ spread ┆ abs_imbalance ┆ hour_of_day ┆ day_of_week │
│ ---             ┆ ---               ┆ ---              ┆ ---               ┆ ---    ┆ ---           ┆ ---         ┆ ---         │
│ date            ┆ i32               ┆ f64              ┆ f64               ┆ f64    ┆ f64           ┆ i8          ┆ i8          │
╞═════════════════╪═══════════════════╪══════════════════╪═══════════════════╪════════╪═══════════════╪═════════════╪═════════════╡
│ 2026-09-08      ┆ 37                ┆ 110.0            ┆ 110.0             ┆ 0.0    ┆ 346.717783    ┆ 17          ┆ 2           │
└─────────────────┴───────────────────┴──────────────────┴───────────────────┴────────┴───────────────┴─────────────┴─────────────┘

===== 07-client.py =====
shape: (1, 5)
┌─────────────────┬───────────────────┬───────────────────┬──────────────────┬─────────────────────────┐
│ settlement_date ┆ settlement_period ┆ system_sell_price ┆ system_buy_price ┆ available_at            │
│ ---             ┆ ---               ┆ ---               ┆ ---              ┆ ---                     │
│ date            ┆ i32               ┆ f64               ┆ f64              ┆ datetime[μs, UTC]       │
╞═════════════════╪═══════════════════╪═══════════════════╪══════════════════╪═════════════════════════╡
│ 2026-09-08      ┆ 37                ┆ 110.0             ┆ 110.0            ┆ 2026-09-09 17:44:29 UTC │
└─────────────────┴───────────────────┴───────────────────┴──────────────────┴─────────────────────────┘

===== gold directory after =====
69 files; unchanged: True
```
