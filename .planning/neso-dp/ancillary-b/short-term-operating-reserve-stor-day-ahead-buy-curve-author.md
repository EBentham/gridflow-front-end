# Writer report: STOR day-ahead buy curve

Package `short-term-operating-reserve-stor-day-ahead-buy-curve`, one table `stor_da_buy_curve` (lead and only member;
the page set's `package_tables` maps the slug to it, so the manifest is right). The hash TXT is a separate files
family (`stor_da_buy_curve_files`, DOC, no silver), named in the raw-feed note. Nothing held.

**Status:** `gridflow-build --only neso_data_portal/stor_da_buy_curve` exit 0; detector `[]`; 0 em dashes.
Mirror `cmp` identical; note CRLF throughout (424 CRLF, 424 lines). Server on 9989 started and stopped by its own PID.

Files (mine only):
- vault: `C:\gridflow-wt\vault-neso-as-b\30-vendors\neso-data-portal\datasets\short-term-operating-reserve-stor-day-ahead-buy-curve.md` (`page:` block only; no body edits)
- mirror: `C:\gridflow-wt\fe-neso-as-b\vault\neso_data_portal\short-term-operating-reserve-stor-day-ahead-buy-curve.md`
- artefacts: `site\hifi\data\{series,samples}\neso_data_portal\stor_da_buy_curve.json`,
  `site\hifi\data\notebooks\neso_data_portal\stor_da_buy_curve.json` and `-6.png`
- page: `site\hifi\data-sources\neso_data_portal\short-term-operating-reserve-stor-day-ahead-buy-curve.html`
- screenshots: `.planning\neso-dp\ancillary-b\stor-da-buy-curve-shots\` (1440, 1024, 768, 390 via a 390 px iframe;
  slices and `-full`)

## The four questions

1. **What one row is.** One point of one service day's buy curve: `buy_curve_step_id` (NESO: "Unique identifier for
   each buy curve step"; 5,475 distinct = rows), `buy_curve_id` (one per service day), `mw`, `availability_price`.
   Every one of the 1,825 curves in NESO's file is exactly three points forming one step: (MW, 0), (MW, P), (0, P),
   with MW and P both non-zero (notebook cell 4 output: 1,825 of 1,825). 1,822 list them in that step order; three
   (`BCN-00000007`, `BCN-00000176`, `BCN-00001499`) list the same points in reverse. So each day's curve is fully
   described by two numbers: the MW and the price.
   How NESO uses it, in NESO's words only: package notes "The buy curve used in the daily assessment process is
   available here"; hash resource "shared ahead of the STOR Day Ahead Auction to give confidence that we have set the
   volume and price cut offs before the auction". Dictionary: `MW` "Maximum MW associated with maximum prices listed in
   the availability price field"; price "Maximum availaibility price associated with maximum MW requirement". The
   assessment-principles PDF the note cites is not quoted locally, so the page rests on the catalogue text only.
   Units: `mw` MW (header and dictionary title; dictionary `unit` is the type word `integer`); price £/MWh from the
   vendor header `Availability Price (£/MWh)` (dictionary unit `Number`). No negative values; zeros are vertices.
   Measured against the results (report and notebook output only, never stated as a rule on the page): clearing price
   is at or below the curve price on all 1,817 days with an accepted tender, and every one of 63,309 accepted tenders
   is priced at or below it; but contracted MW exceeds the curve MW on 708 of 1,817 days (ratio 0.82 to 1.30, median
   1.00, up to 401 MW over), so the MW is not a cap the results obey. The page calls it "NESO's maximum MW
   requirement" (dictionary words) and makes no capping claim. 36,185 of 57,843 rejected tenders were priced at or
   below the curve price.
2. **Times.** `Effective From Date` / `To` served `YYYY-MM-DD HH:MM:SSZ` (literal `Z`), parsed `%Y-%m-%d %H:%M:%SZ`
   zone UTC (registry). Dictionary example `2021-04-01T04:00:00` (no `Z`): body wins, note already says so. UTC is
   supported by the rows: all 5,475 starts and ends are 05:00 Europe/London (04:00Z summer, 05:00Z winter); 5,445 rows
   span 24 h, 15 span 23 h, 15 span 25 h (notebook cell 3 output). Example in the frame: 28 March 2026 runs
   05:00Z to 04:00Z (23 hours). `timestamp_utc` = `event_time` = `effective_from_date` on every row; `published_at` =
   `available_at` = CKAN `last_modified` 2026-03-30 04:22:46.013246 for all rows. Curves are contiguous (each end =
   next start) except across the missing 17 August 2022. The workbench returns all five datetime columns in
   Europe/London; the query cell converts every zone-aware column to UTC (checked: all five `datetime64[us, UTC]`),
   and a 28 to 31 March query returns 12 rows, both ends included.
3. **Captures.** One silver capture (`stor_da_buy_curve_20261008_run2026-10-08T11-27-35...parquet`, 5,475 rows), one
   bronze capture (`raw_20261008T112735Z_..._d240b649.csv`, 5,476 lines = header + 5,475; `declared_content_length`
   1,036,153 = `body_size_bytes`). NESO's datastore total in the field-info snapshot is 5,475. Not truncated; one
   capture cannot repeat rows, so no `dedup:`.
4. **Chart.** Line, `availability_price`, `max` per UTC day of `effective_from_date` (each day has one curve whose two
   non-zero-price points share the price, so max = the curve's price), 1 April 2025 to 31 March 2026, the auction's
   final year, matching the auction-results page's window: 365 points, no gaps, 6.82 (29 March 2026) to 33.53
   (19 March 2026), median 9.83. The UTC bucket date equals the UK service date because every start is 04:00Z or
   05:00Z. The MW is 1,700 on every day of the window but 1 April 2025 (1,260), said in the caption. The page chart
   types plot against time only, so the curve's own shape (MW against price) is drawn in the notebook: four service
   days (1 April 2021, 1 April 2025, 16 October 2025, 19 March 2026) as step curves.
   Whole-history line rejected: spikes to 250.69 (10 December 2022) flatten the rest; the notebook's per-year table
   carries the history.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Key `buy_curve_step_id` | registry `entity_key`; dictionary "Unique identifier for each buy curve step"; n_unique 5,475 = rows |
| One curve per service day, three points, one step | Polars: 1,825 curves, 1,825 UK dates, 3 rows each, point set {(Q,0),(Q,P),(0,P)} on 1,825; notebook cell 4 |
| "volume and price cut-offs" (what_it_is, summary) | catalogue snapshot `20261006T195819Z`, hash resource description |
| "used to assess each day" | catalogue snapshot package `notes` |
| MW is NESO's maximum MW requirement | field-info `20261008T114228Z/stor_da_buy_curve.json` MW and price descriptions |
| Price £/MWh | vendor header `Availability Price (£/MWh)` (registry `source`, bronze header) |
| Last curve 31 March 2026; Not Active; ended after Slow Reserve | max `effective_from_date` 2026-03-31 04:00Z; extras "Update Frequency: Not Active"; package notes |
| History 1 April 2021 to 31 March 2026, bar 17 August 2022 | min/max and date gap in NESO's whole file (single capture = datastore total) |
| 05:00 UK start/end; 23/25 h days | Polars convert_time_zone; notebook cell 3 output |
| `published_at` NESO's last-modified, read as UTC | bronze sidecar `ckan_last_modified`; registry vintage `ckan_last_modified` |
| Raw requests | bronze sidecar `request_url`; `client.py` `_package_show` |
| Whole file unless `last_modified` unchanged | `client.py` 1751-1767 |
| `--last 24h` | `client.py` `_HISTORICAL_WINDOW_TOLERANCE` 48 h (130), `_MAX_INGEST_WINDOW` 7 d (146); same as approved OBP and sibling pages; `cli.py` `--last` on ingest and transform |
| Hash TXT a separate key `stor_da_buy_curve_files`, no silver | registry families and resource disposition DOC; bronze dir `stor_da_buy_curve_files` |
| `query()` relation, column, bounds | gridflow_models `_DATE_COLUMN_BY_DATASET` = `timestamp_utc`; relation `silver_neso_data_portal_stor_da_buy_curve_latest`; docstring "End of the range, inclusive"; 28 to 31 March check |
| Eight rows | `BCS-5632` to `5639`: 28 March 2026 (23 h, 1,700 MW, 7.17), 29 March (6.82), first two points of 30 March (7.26) |
| Key note and alt numbers | committed series: max 33.53 2026-03-19, min 6.82 2026-03-29, median 9.83; April to November min 7.52, monthly peaks 15.62 to 22.63; December 6.91 to 13.81; January peak 26.24 on the 20th |
| Plot alt numbers | notebook cell 5 index rows: 1,311/6.78, 1,260/13.08, 1,700/21.50, 1,700/33.53 (trial run; same data) |
| Related: results linked on `buy_curve_id` | all 1,818 distinct result ids match a curve; each matched curve's `effective_from_date` = result `service_delivery_from` (re-run, not taken from the sibling) |

## Body corrections

None. The body's counts (1,825 curves, 5,475 rows, 5,445/15/15 durations, value ranges, 7 curves without results,
the missing 17 August 2022, `(Curve ID, MW)` 3,650 distinct) all re-check. Optional addition for the seat: the body
could say every curve is one step (Q,0),(Q,P),(0,P), three listed in reverse; I did not add it as it corrects nothing.

## Unverified

- How NESO used the MW in clearing: contracted MW exceeds it on 708 of 1,817 days; NESO gives no rule. Page silent.
- How NESO relates the curve's £/MWh to the results' £/MW/h (note TODO stands). The notebook compares the figures as
  written, with a comment naming both units; the page claims nothing about it.
- The assessment-principles and operational-guidance PDFs cited in the body (not read; no live fetch).

## Open questions

- Is the notebook's clearing-price comparison across the two labelled units acceptable to the checker? It is
  numeric output with both units named in the cell comment. If not, drop `clearing_at_or_below` from that cell.

## Template problems

- The chart types plot only against time or as categories, so a curve (MW on x, price on y) cannot be drawn on the
  page; it lives in the notebook. A step or x-y chart type would let curve packages (this one, SFFR buy orders) draw
  their curves on the page. Seat item.
- No dark scheme in the site: light and dark render identically (as the sibling noted).
- Build warns "22 line(s) in 'Known issues and gotchas' sections could not be placed" (template-wide).
- At 390 and 768 the notebook panel wraps long code lines mid-string (`"2021-04-` / `01"`); template behaviour, same
  on the sibling page.

## Defects

- **NESO data (not gridflow):** NESO's STOR day-ahead buy-curve file has no curve for service day 17 August 2022
  (already a vault TODO). Its ids skip numbers: `BCN-` runs 0 to 1877 with 53 numbers unused, `BCS-` 0 to 5643 with
  169 unused; the bronze capture equals NESO's datastore total (5,475), so gridflow lost nothing. Three curves list
  their points in reverse step order (`BCN-00000007`, `-00000176`, `-00001499`), same points. Vault remediation note
  only; no gridflow fix.
- **NESO data, open question:** contracted MW in the auction results exceeds the buy curve's MW on 708 of 1,817
  service days (up to 401 MW over); NESO's dictionary calls the MW the "maximum MW requirement". Worth a vault TODO
  beside the existing unit-relation TODO.
- No gridflow defect found.
