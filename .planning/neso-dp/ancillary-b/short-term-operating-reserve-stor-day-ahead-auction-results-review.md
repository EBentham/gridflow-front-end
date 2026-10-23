# Review: STOR day-ahead auction results (`stor_da_auction_results`)

**Verdict: REVISE** (1 major, 5 nits; no blockers).

Checked: build `--only neso_data_portal/stor_da_auction_results` exit 0; detector `[]`; mirror `cmp` identical to the
vault note; note diff against `origin/master` read; artefacts (series, samples, notebook JSON and plot) read; page
rendered at 1024 and 390 in my own preview tab on port 9998 (nothing clipped or overlapping, no horizontal scroll at
390; the site has no dark scheme). My server was stopped by its own PID. Every number below was re-derived with Polars
(lazy, read only) from the one silver capture, the bronze sidecar and CSV, the catalogue snapshot `20261006T195819Z`
and the field-info snapshot.

## Confirmed (no finding)

- **Chart.** Reproduced from silver: accepted tenders, per UK service day, 1 April 2025 to 31 March 2026 = 365 days,
  no gaps, min 0.22 (1 April 2025), max 21.00 (16 October 2025), median 3.70; 20.48 on 30 September; 20.00 on 7 and 8
  January. Alt and key note match the series: April to June 0.22 to 4.88, November to February 1.44 to 20.00, March
  0.72 to 6.50. `spec_origin: vault`, build digest check passes. Caption names dataset, unit, window and aggregation.
  The notebook's per-year table matches my own (days 362/362/365/363/365; medians 1.90, 5.00, 0.73, 0.45, 3.70; peaks
  169, 175, 28.45, 98.9, 21.0; mean MW 1258.27, 1302.28, 1263.85, 1304.43, 1672.61).
- **Clearing price equals the dearest accepted price.** The page shows it only as notebook cell 4 output (1,817 of
  1,817); no guide line, caption, summary or note states it as NESO's rule. Verified: one price per day on all 1,817
  days, equal to the day's highest accepted tendered price on all 1,817; no accepted tender above it.
- **Times.** Every start and end is 05:00 Europe/London; the UTC start hour is 04 in months 4 to 9 and 05 in months 11
  to 2 (March and October mix both); 120,803 rows span 24 h, 364 span 23 h, 313 span 25 h. UTC date equals UK date on
  all rows, so the UTC day bucket of the series is safe. The notebook cell is right: `query()` returns session-zone
  times (checked in gridflow_models: designated date column `timestamp_utc`, TIMESTAMPTZ half-open UTC days so both
  ends are included, relation `silver_neso_data_portal_stor_da_auction_results_latest`, excludes `event_time`,
  `available_at`, `vintage_policy`, `source_run_id`, `dataset_version`, `month`, `year`); `tz_convert("UTC")` then the
  London date derived explicitly. Output cells have no errors; written by `scripts/run_notebooks.py`.
- **Row and units.** 121,480 rows = unique `tender_submission_id`; one round per day; Accepted 63,309, Rejected 58,171;
  rejected rows null on both outcome columns, no accepted row null; units MW and £/MW/Hr from NESO's dictionary;
  `Minimum Acceptable MW` dictionary entry blank and said so. `service_name` has one value; `timestamp_utc` =
  `event_time` = `service_delivery_from`; `published_at` = `available_at` = 2026-03-30 04:28:01.703705 on every row.
- **Eight rows.** Match silver for 23 November 2023 (83 tenders that day; clearing 0.30; SEEL-1 270 offered, 150
  minimum, 172 contracted; DIDC04G and SEVIU-1 rejected at 0.30; BRIDU-1 and LBAR-1G at 0.35). `generated_by:
  gridflow-sample`.
- **NESO text.** Buy-curve package notes ("decommissioned following the launch of the new Slow Reserve service in EAC",
  "final STOR DA tender was run on 30th March"), the results resource description ("STOR DA Auction Results for
  30/03/2026") and the "Not Active" extra are as quoted. All 1,818 distinct `buy_curve_id` in the results exist in
  `stor_da_buy_curve`. The page makes no join claim to `stor_windows`.
- **Raw feed.** Request URL equals the bronze sidecar `request_url`; `package_show` path is built by
  `build_action_url`; the file is skipped when `ckan_last_modified` is unchanged (`client.py` 1751-1767); `--last 24h`
  fits the 48 h and 7 d window rules and matches the approved OBP and SFFR pages. Bronze: one capture, 121,481 lines,
  21,263,175 bytes = declared length; no tab and no padding space (body correction 3 holds).
- **Body corrections** (cadence, resumes TODO, whitespace TODO) each cite evidence and fix the smallest span.
- No em dashes, middle dots, arrows, planning words or local-count phrases in the `page:` block.

## Findings

1. **major** `page.summary`, `page.facts.vendor`, `page.notebook.plot_alt`. "Every tender in NESO's daily ...
   auction" and "one uploaded CSV of every daily STOR auction result" overclaim. NESO's file has no rows at all for
   four service days inside its span (2 August 2022, 17 August 2022, 29 October 2023, 8 February 2025: 1,822 of 1,826
   days present; the notebook's own cell 4 prints 1,822) and five days where every tender was rejected (8 April, 5 July
   and 26 July 2021, 24 April 2022, 18 August 2024; 1,817 accepted days). Two of the nine have a NESO explanation in
   the industry-notifications file the page already links: the 17 August 2024 auction (delivery 18 August) and the 7
   February 2025 auction (delivery 8 February, "no replacement auction") both failed with no bids accepted. The page
   never says any of this, and `facts.history` ("Service days 1 April 2021 to 31 March 2026 in NESO's file") reads as
   continuous. The author report records the gap as a vault-only defect. Fix: drop "Every" ("The tenders in NESO's
   daily ... auction"), change "every daily" in the vendor fact, and add one scoped sentence (for example in
   `what_it_is`): NESO's file has no rows for four service days in its span and five days with none accepted; two
   follow NESO's notices of failed auctions. `plot_alt` "the line breaks where no tender was accepted" is then also
   loose: four of the nine breaks are days with no rows; say "where nothing was accepted or NESO's file has no rows".
2. **nit** `page.chart_view.caption`. "the one clearing price of each service day" states a market rule as fact. NESO's
   dictionary defines the column per tender submission ("for a given tender submission"); one price per day is
   measured (true on all 1,817 days; the notebook shows it). The page claims no NESO rule elsewhere, so scope it:
   "each service day's clearing price: the same on every accepted tender that day (notebook, cell 4)". That wording
   also explains why the chart can use `max`.
3. **nit** `page.record.fields.service_delivery_from` (and `.service_delivery_to`). "UTC as NESO writes it, with a
   `Z`: 05:00 UK time", beside sample rows that all read 05:00 UTC (a winter day), invites reading the start as 05:00
   UTC always. In summer the served start is 04:00Z (months 4 to 9, all 04:00Z). Add "04:00Z in summer" or "the `Z`
   moves with the UK clock change". The notebook shows only the UK start, so nothing else on the page says this.
4. **nit** `page.facts.cadence`. "NESO marks the file Not Active": the "Update Frequency: Not Active" extra is on the
   package, not the file. Also "the last on 30 March 2026" beside "service days ... to 31 March 2026" leaves the
   one-day lag unexplained; NESO's own notice words it "auction on 1 April 2025 (for delivery on 2 April 2025)", and
   the last file row is delivery on 31 March. Suggest: "the last auction on 30 March 2026, for delivery on 31 March;
   NESO marks the package Not Active".
5. **nit** `page.notebook.plot_alt`. Two bases in one sentence: "Mostly 1,075 to 1,450 MW" is the 5th to 95th
   percentile range for the days to 1 April 2025 (my check: 1,075 and 1,450), while "then 811 to 1,955, median 1,696"
   is minimum to maximum afterwards (the 5th to 95th percentile would be narrower). Use one basis for both. The
   medians and the 50 MW low on 20 December 2021 are right. NESO's 1 April 2025 notice that the STOR day-ahead
   requirement rose to 1,700 MW from the auction for delivery on 2 April 2025 explains the step; citing it is optional.
6. **nit** `page.related[2].note`. "NESO's notices of STOR auction delays and failures": the STOR notices file has 9
   rows, 6 on auction publication delays or failures, 1 on a requirement change, 2 on portal maintenance; the sibling
   page says "Mostly STOR auction delays and failures". Use "Mostly" for consistency.

## Not findings

- Template: no dark scheme; `.nb-tab` truncation at 390; 22 caveat-grammar warnings (seat items).
- The writer's open question on "one clearing price per service day" is answered by finding 2: keep as measured, scoped.
- Defects to log (NESO data, no gridflow fault): four service days with no rows and five with none accepted. Explained
  by NESO notices: 18 August 2024 (none accepted) and 8 February 2025 (no rows). No explanation in the notices file
  for 2 and 17 August 2022 and 29 October 2023 (no rows), or 8 April, 5 July and 26 July 2021 and 24 April 2022
  (none accepted).
