# Writer report: STOR day-ahead auction results

Package `short-term-operating-reserve-stor-day-ahead-auction-results`, one table `stor_da_auction_results` (lead and
only member; the page set's `package_tables` maps the slug to it, so the manifest is right). One-table page, nothing held.

**Status:** `gridflow-build --only neso_data_portal/stor_da_auction_results` exit 0; detector `[]`; 0 em dashes.
Mirror `cmp` identical; note CRLF throughout (367 CRLF, 367 LF).

Files (mine only):
- vault: `C:\gridflow-wt\vault-neso-as-b\30-vendors\neso-data-portal\datasets\short-term-operating-reserve-stor-day-ahead-auction-results.md` (`page:` block + 3 body corrections)
- mirror: `C:\gridflow-wt\fe-neso-as-b\vault\neso_data_portal\short-term-operating-reserve-stor-day-ahead-auction-results.md`
- artefacts: `site\hifi\data\{series,samples}\neso_data_portal\stor_da_auction_results.json`,
  `site\hifi\data\notebooks\neso_data_portal\stor_da_auction_results.json` and `-6.png`
- page: `site\hifi\data-sources\neso_data_portal\short-term-operating-reserve-stor-day-ahead-auction-results.html`
- screenshots: `.planning\neso-dp\ancillary-b\stor-da-auction-shots\` (1440, 1024, 768, 390 via a 390 px iframe)

## The four questions

1. **What one row is.** One tender submission (NESO: `Tender Submission ID` is the "Unique Identifier generated for a
   given tender submission"; non-null and unique on all 121,480 rows): one unit's tendered MW "for the availability
   windows" of one service day, its tendered availability price, `Status` Accepted or Rejected, and for accepted rows
   `Contracted MW` ("Capacity in MW ... for the availabilty windows accepted by us") and `Market Clearing Price`
   ("Availability price offered to Service Provider for a given tender submission"). Units from NESO's dictionary:
   MW for tendered and contracted MW; £/MW/Hr for both prices; `Minimum Acceptable MW` has a blank dictionary entry
   (MW rests on the column name, said so on the page). No signs: no negative value in any numeric column (min tendered
   2, min price 0.01). No window column: one row covers the whole service day.
   Prices, measured over NESO's whole file: one clearing price per service day (1,817 of 1,817 days with an accepted
   tender), and it equals the dearest accepted tender's price on all 1,817 (a uniform, marginal clearing price; NESO
   does not state the rule, so the page shows it only as notebook output). Every accepted tender is priced at or
   below the clearing price; contracted MW never exceeds tendered; 135 accepted tenders are partly contracted, all at
   the clearing price and all at or above their minimum (2021 to 2023 only). 2,136 rejected tenders sit at or below
   the clearing price (1,068 exactly at it; 1,981 of the 2,136 have minimum = tendered, all-or-nothing). Rejected
   rows: contracted MW and clearing price null on all 58,171, never zero.
2. **Time columns.** `Service Delivery From` / `To`, served as `YYYY-MM-DD HH:MM:SSZ` (literal `Z`); the registry
   parses `%Y-%m-%d %H:%M:%SZ`, zone UTC (`registry/short-term-operating-reserve-stor-day-ahead-auction-results.json`).
   NESO's dictionary says `DD/MM/YYYY HH:MM` (example `13/02/2021 05:00`): the body wins, the note already records it.
   UTC is supported by the rows: every start and end is 05:00 Europe/London (04:00Z in summer, 05:00Z in winter), so
   the `Z` tracks the UK clock change as a true UTC instant would. Clock-change rows: 120,803 rows span 24 h, 364 span
   23 h, 313 span 25 h (notebook output). `timestamp_utc` = `event_time` = `service_delivery_from` on every row;
   `published_at` = `available_at` = CKAN `last_modified` 2026-03-30 04:28:01.703705 for all rows. The notebook
   converts the three time columns from the session zone to UTC and derives the UK day explicitly.
3. **Captures.** One silver capture (`..._20261008_run2026-10-08T11-27-32...parquet`), one bronze capture
   (`raw_20261008T112732Z_..._eb962f87.csv`, 121,481 lines = header + 121,480, `declared_content_length` 21,263,175 =
   body size). NESO's datastore total in the field-info snapshot is 121,480. Not truncated; captures cannot repeat
   rows, so no `dedup:` on the chart or frame.
4. **Relation to the buy curve and STOR windows (NESO's text only on the page).** Buy curve package notes: "The buy
   curve used in the daily assessment process is available here", and STOR DA "has been officially decommissioned
   following the launch of the new Slow Reserve service in EAC. The final STOR DA tender was run on 30th March".
   `Buy Curve ID` is "Unique Identifier generated for a given Buy Curve". STOR windows package: "committed windows for
   each STOR Service Day where STOR is required to be provided". Measured (report only, not claimed on the page beyond
   "as in its STOR buy-curve package"): all 1,818 distinct `buy_curve_id` values in the results match a
   `buy_curve_id` in `stor_da_buy_curve`, and each matched curve's `effective_from_date` equals the result's
   `service_delivery_from`. 328 result rows have a null `buy_curve_id`; 4 days have none at all. gridflow has no
   silver join to `stor_windows` (note body, seat ruling 11): the page does not imply one.

## Chart and window

Line, `market_clearing_price` of accepted tenders, `max` per UTC day bucket of `service_delivery_from` (one value per
day, so max = the day's price), 1 April 2025 to 31 March 2026, the auction's final year: 365 points, no gaps,
0.22 (1 April 2025) to 21.00 (16 October 2025), median 3.70. Whole-history daily line rejected: spikes to 175
(12 December 2022) flatten the rest; the notebook's per-year table carries the history (medians 0.45 to 5.00, peaks
21 to 175). Window end is inclusive; the UTC bucket date equals the UK service date because every start is 04:00Z or
05:00Z.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Key `tender_submission_id`, unique | registry `entity_key`; Polars n_unique 121,480 = rows; dictionary description |
| Grain: one row per tender, one service day | (tender_round_id, unit_id) unique; 1 round per service day (1,822 rounds, 1,822 days) |
| Units MW, £/MW/Hr; minimum MW blank in dictionary | field-info snapshot `20261008T114228Z/stor_da_auction_results.json` |
| Rejected rows null, never zero | 58,171 Rejected, 58,171 null contracted and clearing price; 0 Accepted with null contracted |
| One clearing price per day, = dearest accepted | notebook cell 4 output: 1,822 days, 1,817 with acceptance, 1,817 and 1,817 |
| 05:00 UK start, 23/24/25 h | notebook cell 3 output; Polars convert_time_zone check |
| `published_at` is the file's last-modified, read as UTC | bronze sidecar `ckan_last_modified`; vintage `ckan_last_modified` in registry |
| Last tender 30 March 2026, decommissioned after Slow Reserve | catalogue snapshot `20261006T195819Z`, buy-curve package `notes`; results resource description "STOR DA Auction Results for 30/03/2026"; extras "Update Frequency: Not Active" |
| History 1 April 2021 to 31 March 2026 | min/max `service_delivery_from` in NESO's whole file (single complete capture) |
| Raw request URL | bronze sidecar `request_url` |
| Upload downloaded whole unless last_modified unchanged | `client.py` 1751-1767 |
| `--last 24h` | `client.py` `_HISTORICAL_WINDOW_TOLERANCE` 48 h, `_MAX_INGEST_WINDOW` 7 d; same commands as approved SFFR and OBP pages |
| `query()` relation, column, bounds, drops | gridflow_models `_get_method_registry`: `timestamp_utc`, `silver_neso_data_portal_stor_da_auction_results_latest`, TIMESTAMPTZ half-open UTC days, excludes `event_time`, `available_at`, `source_run_id`, `dataset_version` |
| Eight rows | sample: 23 November 2023, KILLPG-1/DIDC03G/SOLUU-1 accepted below 0.30, SEEL-1 at 0.30 with 172 of 270 MW (min 150), DIDC04G/SEVIU-1 rejected at 0.30, BRIDU-1/LBAR-1G rejected at 0.35 |
| Alt and key note numbers | committed series: min 0.22 2025-04-01, max 21.0 2025-10-16, 20.48 2025-09-30, 20.0 2026-01-07/08, Apr-Jun max 4.88, Nov-Feb 1.44 to 20.0, March 0.72 to 6.5, median 3.7 |
| Plot alt numbers | daily contracted MW: before 2 April 2025 5th-95th pct 1,075 to 1,450; from 2 April 2025 811 to 1,955, median 1,696; lowest 50 on 2021-12-20 |

## Body corrections (vault note)

1. Cadence: replaced the `TODO: verify` on whether publication resumes with NESO's own text (buy-curve package notes,
   decommissioned after Slow Reserve launched in EAC; final tender 30 March) and the resource description
   "STOR DA Auction Results for 30/03/2026".
2. Holds, open questions: the matching "whether publication resumes" TODO now states it does not resume.
3. Known issues, identifiers: replaced the `TODO: verify` on trailing whitespace with the check (raw bytes of the
   2026-10-08 capture: no tab, no space beside a comma; silver strip check 0 on all six text identifier columns).

## Unverified

- The clearing rule (marginal, uniform price) is measured on NESO's file, not stated by NESO; the page shows it only as
  notebook output, not as a rule.
- Why tenders at the clearing price were rejected while another at the same price was partly accepted (23 November
  2023): NESO gives no allocation rule; the page does not explain it.
- Interval closure of the service day and the original publication instant of each result stay open (note TODOs).

## Open questions

- Should the guide say "one clearing price per service day" as a fact? It holds on all 1,817 days with an acceptance in
  NESO's whole frozen file; the caption says "the one clearing price of each service day", backed by the notebook.

## Template notes (not page findings)

- The site has no dark colour scheme (no `prefers-color-scheme` in `theme.css`/`tokens.css`): light and dark render
  identically.
- `.nb-tab` ellipsis truncates `stor_da_auction_results.ipynb` at 390 by design.
- Build warns "22 line(s) in 'Known issues and gotchas' sections could not be placed by the caveat grammar"
  (template-wide, not this page).

## Defects

- **NESO data (not gridflow):** NESO's STOR day-ahead results file has no rows for four service days inside its
  1 April 2021 to 31 March 2026 span: 2 August 2022, 17 August 2022, 29 October 2023 and 8 February 2025. Five further
  days have rows but no accepted tender: 8 April, 5 July and 26 July 2021, 24 April 2022, 18 August 2024. The bronze
  capture matches NESO's datastore total (121,480), so gridflow lost nothing. Vault remediation note only; no
  gridflow fix.
- No gridflow defect found.
