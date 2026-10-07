# neso_data_portal/embedded_wind_solar_forecast: author report

Writer: Opus 5.5 · high, 2026-10-06. Single page (no family). Port 9865.

## Status

- `gridflow-build --only neso_data_portal/embedded_wind_solar_forecast`: success.
- `detect.mjs --json`: `[]` (no findings, not even advisories). Real em dashes in the built page: 0.
- Artefacts written by the tools:
  - `site/hifi/data/series/neso_data_portal/embedded_wind_solar_forecast.json` (`spec_origin: vault`, 628 points);
  - `site/hifi/data/samples/neso_data_portal/embedded_wind_solar_forecast.json` (`gridflow-sample`);
  - `site/hifi/data/notebooks/neso_data_portal/embedded_wind_solar_forecast.json` and `-5.png` (`run_notebooks.py`, no errors).
- There was no staged chart spec and no authored override to delete.
- Canonical note edited in the vault worktree. The mirror `vault/neso_data_portal/embedded_wind_solar_forecast.md` was copied byte for byte, and `cmp` is clean.
- The canonical note is LF in git HEAD and still LF after the edit (no CRLF in either), so the diff is not a line-ending rewrite.
- Screenshots: 1440, 1024, 768, plus 390 in a 390 px iframe (scratchpad `ewsf_shots/`).
  - The site has no dark theme: no `prefers-color-scheme` or `data-theme` anywhere in `site/hifi/assets/`. Light is the only rendering.
  - Everything is visible at every width except one template problem: the hero key chip clips at 390 (see Template problems).
- **Recommendation: ship.** The data is thin (one forecast issue), but the page says what it is and makes no trend claim.

## What one row is, and the vintage question

- **Grain:** one row per `(settlement_date, settlement_period, issue_time)`. `ENTITY_KEY_COLUMNS`, `silver/neso_data_portal/embedded_wind_solar_forecast.py:135`. The transformer dedups on it (`unique(..., keep="last")`, line 266).
- **Later files never overwrite earlier forecasts:**
  - The transformer is `APPEND_ONLY = True` and `VINTAGE_PER_BRONZE_FILE = True` (lines 131-132).
  - `_write_silver` writes one run-suffixed parquet per vintage (`silver/base.py:2633-2636`).
  - The base view therefore holds every captured issue, each carrying its own `issue_time`.
- **`_latest`:**
  - `silver_neso_data_portal_embedded_wind_solar_forecast_latest` keeps one row per `(settlement_date, settlement_period)` (`silver/latest_views.py:131-133`).
  - It orders by `available_at`, which equals `published_at`, the file's CKAN `last_modified` (`latest_views.py` docstring, "available_at-primary").
- **What silver holds:**
  - Exactly one issue: `issue_time` 2026-08-20 21:25 UTC, from filename `202608202125_embedded_forecast.csv`.
  - One bronze capture: `raw_20260820T214341Z_c90ad5f2.csv`.
  - The 628 rows run from settlement date 20 Aug SP45 (21:00 UTC) to 2 Sep SP48 (22:30 UTC). That is 4 + 13 × 48 = 628, one issue's whole horizon.
  - So DATA-MATRIX's "628 rows, 20 Aug to 2 Sep" is **one forecast file's target periods**, not two weeks of issues. The page never states local coverage.
- **The silver file's date is the capture date:**
  - The file is `year=2026/month=08/embedded_wind_solar_forecast_20260820_run<available_at>.parquet`.
  - The date is the bronze capture partition (`data_date = end.date()`, `connectors/neso_data_portal/client.py:1442`), not a settlement date.

## Evidence table

| Claim on the page | Evidence |
|---|---|
| Issue instant comes from the filename's 12-digit token, read as UTC | `silver/neso_data_portal/_bronze.py` `_ISSUE_TOKEN_PATTERN` `^(\d{12})_embedded_forecast\.csv$`, `_parse_issue_time` `.replace(tzinfo=UTC)`; sidecar `resource_filename: 202608202125_embedded_forecast.csv` |
| `published_at` is the file's CKAN `last_modified`, read as UTC | `_bronze.py` `_parse_ckan_timestamp`; sidecar `ckan_last_modified: 2026-08-20T21:25:03.319647`. It is not a fetch stamp: fetch was 21:43:41 (`fetched_at`). |
| `published_at` orders issues in `_latest` | `latest_views.py` (available_at-primary ordering); silver `available_at == published_at` (checked: identical on all rows) |
| Silver appends every captured issue | `APPEND_ONLY`, `VINTAGE_PER_BRONZE_FILE`, key includes `issue_time` (transformer lines 131-135) |
| Grain and key | `ENTITY_KEY_COLUMNS` (transformer) |
| Settlement period 1 to 48, 46 or 50 on clock-change days | `is_valid_settlement_period` and `_exclude_out_of_calendar_periods` (transformer); schema validator `schemas/neso_data_portal.py:197+` |
| Chart time = settlement period start, UTC | Chart uses `event_time`, derived from the settlement pair via `settlement_period_to_utc` (schema docstring lines 162-167). Checked: SP45 of 20 Aug = 21:00 UTC; SP1 of 21 Aug = 23:00 UTC on 20 Aug (BST). |
| `time_gmt_raw` is "here the period's end, UTC clock; undocumented" | Transformer docstring: start-vs-end convention undocumented, carried unparsed. Checked: `time_gmt_raw == (event_time + 30 min).strftime("%H:%M")` on all 628 rows of this issue. |
| The file states no unit; gridflow's code treats the values as MW | CSV header has no unit (`EXPECTED_COLUMNS`); code names them `_MW_COLUMNS` (transformer line 101) |
| Capacity "the same in these rows" | Eight sample rows: 23,301 solar, 6,417 wind |
| Embedded = distribution-connected, unseen by transmission metering | Transformer docstring line 3-4 ("distribution-connected, and so invisible to transmission metering"); vault note Overview |
| Cadence unstated by NESO | Vault note "Issue cadence TODO (not stated)"; CKAN catalogue snapshot carries no description. Code docstrings say "several times a day" but that is not vendor evidence and one capture cannot observe it, so the page does not say it. |
| Request 1: `GET https://api.neso.energy/api/3/action/package_show?id=embedded-wind-and-solar-forecasts` | `config/sources.yaml:756` base_url; `endpoints.py` `CKAN_ACTION_PREFIX` + `build_action_url("package_show", id=...)`; `DATASETS["embedded_wind_solar_forecast"].package` |
| Request 2: the resource download URL (302 to presigned CDN) | Sidecar `request_url` of the real capture; `fetch()` downloads the selected resource's redirector URL (`client.py:1420-1423`) |
| "The window selects nothing; each ingest captures the current issue whole" | `fetch()` docstring, D-16: "The window is not a selector"; one `package_show` + one download per fetch |
| Commands `--last 24h` for ingest and transform | `resolve_dates`: `--last` gives `(now-24h, now)` (`pipeline/runner.py:492-496`). Ingest partitions bronze at `end.date()` = today (`client.py:1442`); transform iterates `date_range(start.date(), end.date())` (`runner.py:1138`), which includes today. A historical `--end` older than 48 h is refused (`client.py` `_HISTORICAL_WINDOW_TOLERANCE`), so a fixed-date command cannot be given. |
| Chart: line, `embedded_solar_forecast`, filter `issue_time == 2026-08-20T21:25:00Z`, window 20 Aug to 2 Sep | Committed series: 628 points, `silver_first` 2026-08-20T21:00Z, `silver_last` 2026-09-02T22:30Z, `rows_used` 628 |
| Alt numbers: nights at or near zero, 63 at most at 23:30 UTC on the 25th; peaks between 10:00 and 12:30 UTC; 7,808 (21st), 11,182 at 12:00 UTC (24th), 10,051, 8,442, then 7,255 to 7,861 from the 27th | Polars over silver, identical to the series. Daily max by settlement date; night max 63.0 at 2026-08-25 23:30 UTC (SP2 of 26 Aug). |
| Key note "the rows below give capacity, 23,301 MW" | Sample rows |
| Notebook lead: reads `_latest`, filters `settlement_date`, both ends inclusive, drops `event_time` and lineage | gridflow_models `research/handles/source.py:401-447`; `_RELATION_NAME_BY_DATASET` gives `..._latest`, date col `settlement_date` (DATE); `_BITEMPORAL_EXCLUDE` = event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year |
| Notebook converts `issue_time` to UTC | Without it, DuckDB returned `2026-08-20 22:25:00+01:00` (session time zone); the cell's `tz_convert("UTC")` output shows 21:25 UTC |
| Related: `historic_generation_mix` has `wind_emb` and `solar` columns | That note's schema; I worded it as "columns to compare" because its `solar`-is-embedded claim is a deduction there |
| Related: `elexon/windfor` covers operationally metered farms | `vault/elexon/windfor.md` `what_it_is` (quoting Elexon API docs) |
| Related: ENTSO-E returns no A69 data for GB | `vault/entsoe/wind_solar_forecast.md` `what_it_is` |

## Body corrections (canonical note)

1. **Bronze path pattern:**
   - Was: `raw_<fetched_at>_<uuid>.csv`.
   - Now: `raw_<fetched_at>_<sha256 of body, first 8 hex>.csv`.
   - Evidence: `bronze/writer.py:57` with `body_hash = sha256(body).hexdigest()[:8]`; real file `raw_20260820T214341Z_c90ad5f2.csv` matches `body_sha256` `c90ad5f2…`.
2. **Bronze sample:**
   - Was invented rows `20260816,00:30,20260816,1,1250,6800,0,15900`, with the wrong date format (the vendor sends `2026-08-16T00:00:00`, parsed with `%Y-%m-%dT%H:%M:%S`, transformer `_VENDOR_DATE_FORMAT`). Its `TIME_GMT` 00:30 for SP1 is also impossible on a BST date (SP1 ends 23:30 UTC the previous day).
   - Now: the first two real rows of the 20 Aug capture, plus a one-line note on the format.
3. **Silver path pattern:**
   - Was: `<year>/<month>/<day>/data_<run_suffix>.parquet`.
   - Now: `year=<YYYY>/month=<MM>/embedded_wind_solar_forecast_<YYYYMMDD>_run<available_at>.parquet`, noting that the date is the capture partition.
   - Evidence: `storage/paths.py:58-61`, `silver/base.py:2633-2636`, real file name.
4. **Silver sample:**
   - Was invented values (SP1, `time_gmt_raw` "00:30", 1250/6800/15900, `published_at` *before* `issue_time`).
   - Now: the real first row of the 20 Aug issue (SP45, "21:30", 857/6417/0/23301, `published_at` 21:25:03.319647).

No other body text changed. The body's existing em dashes are not rendered, so they were left alone.

## Unverified

- **NESO's issue cadence and forecast horizon.** No vendor statement exists in the vault or the catalogue snapshot. The code comment "several times a day" is unevidenced, and one capture cannot show cadence. The page states neither. The horizon shown (to 2 Sep, about 13 days) is just what this issue covers.
- **`TIME_GMT` as period end.** This holds on all rows of the one issue held. NESO does not document it, and the page says "here" and "undocumented".
- **The filename token being UTC.** This is gridflow's D-15 corroboration (token 21:25 against `last_modified` 21:25:03), not a vendor statement. The page says "read as UTC".
- **Whether `EMBEDDED_*_CAPACITY` ever changes within or between issues.** It is constant within this one issue; the page says only "the same in these rows".

## Open questions (for the seat)

1. **Duplicate rows if the same issue is captured on two ingest dates.** Both captures carry the same `issue_time` and `published_at`, so `available_at` is equal. They land in different capture partitions (different file names), so the base view would hold two rows with the same key `(settlement_date, settlement_period, issue_time)`.
   - `_latest` would pick one arbitrarily, but the values are identical, so this is harmless to `_latest`. The base view, though, would break its documented grain.
   - This is not reproducible locally (one capture only). Worth a gridflow check; it is logged in Defects as "to verify".
2. **Chart choice.** The spec allows only one `value` column, so the chart shows solar only; wind appears in the frame and the notebook plot. If the seat prefers wind, change `value` and the words. See Template problems.

## Template problems

1. **The hero key chip clips at 390 px.**
   - `.ds-chip` (`site/hifi/assets/theme.css:526-529`) is `inline-block`, 15 px mono, with no `overflow-wrap`.
   - `neso_data_portal/embedded_wind_solar_forecast` (45 characters) runs off the right edge at 390 (it shows `..._forec`).
   - The same will hit any dataset key longer than about 38 characters (for example ENTSO-E's longer keys).
   - Suggested fix (seat's call): `overflow-wrap: anywhere;` on `.ds-chip`, or `max-width: 100%` plus wrap.
   - Major under rubric section 5, but not fixable by an author.
2. **Wide tables chart only one value column.** `chart_spec` has a single `value` and no unpivot (`distil.py` `_apply_groups` labels the series by the value column). Datasets that store series as separate columns (here wind and solar forecast) cannot chart both. An optional `values: [col, ...]` that melts to `group` would fix it.
3. **Snapshot-only sources do not fit the fixed-date notebook model.**
   - The ingest commands can only capture the current file (historical windows are refused), so a reader can never reproduce the 20 Aug issue.
   - `needs` was written as "one capture of the current file", and the lead tells the reader to change the dates.
   - Consider a template wording for snapshot sources.
4. **`query()` drops `event_time` and this table has no `timestamp_utc`,** so the notebook has no instant column. The plot uses the row position (periods from the first in the issue). Nothing to fix in the template; noted for the other two NESO Data Portal pages.
5. **Minor: the notebook tab name ellipsises at 390** (`embedded_wind_solar_f…`). This looks intentional.

## Defects (paste as is)

- **gridflow, docstring (low):**
  - `silver/neso_data_portal/embedded_wind_solar_forecast.py` module docstring calls the file "a rolling day-ahead forecast ... republished ... several times a day".
  - The 2026-08-20 21:25 UTC issue (`202608202125_embedded_forecast.csv`) runs from the current period to 13 days ahead (to 2 Sep SP48), so "day-ahead" is wrong. "Several times a day" has no vendor citation.
  - The same unevidenced cadence claim appears in `silver/latest_views.py:128-129` ("republished several times a day").
  - Fix: drop "day-ahead", and cite or remove the cadence.
- **gridflow, to verify (medium if real):**
  - If the same NESO embedded-forecast issue is captured by two ingests on different UTC dates, the two silver files share `(settlement_date, settlement_period, issue_time)`.
  - That puts duplicate entity keys in the base view `silver_neso_data_portal_embedded_wind_solar_forecast`. `available_at` is the same, so the run-suffixed filenames differ only by the capture-date part.
  - There is no cross-partition dedup in the APPEND_ONLY write path (`silver/base.py:2633-2636`).
  - There is no identical-body skip in the ingest path: `bronze/writer.py` hashes the body only for the file name and sidecar (lines 33, 57, 80), and `pipeline/runner.py` mentions identical bytes only in the backfill refusal (line 433).
  - Reasoned from code; not reproduced locally (one capture held).
- **Vault, fixed in this branch:** in the `embedded-wind-and-solar-forecasts.md` body, the bronze and silver samples were invented, with the wrong date format and an impossible BST `TIME_GMT`. Both path patterns were wrong. All are corrected with citations (see Body corrections).
- **Vendor data observation (no gridflow action):**
  - NESO's embedded solar forecast in the 21:25 UTC 20 Aug 2026 issue is non-zero at night: up to 63 MW at 23:30 UTC on 25 Aug.
  - It runs from 1 to 63 MW across 22:00 to 01:30 UTC on the nights after 24 and 25 Aug, plus scattered 1 to 4 MW periods on later nights.
  - Physically implausible for GB solar. This is the vendor's value; silver passes it through unchanged. The page's alt text states it as seen.
- **Front-end template:** `.ds-chip` (`site/hifi/assets/theme.css:526-529`) does not wrap; keys longer than about 38 characters clip at 390 px.
