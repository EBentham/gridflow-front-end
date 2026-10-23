# Current BSUoS charges: writer's report

Page `neso_data_portal/current-balancing-services-use-of-system-bsuos-data`, lead `current_bsuos_ii`, members in page-set
order `current_bsuos_ii`, `_sf`, `_rf`, `_historic_ii`, `_historic_sf`, `_historic_rf`, `_cap_adjustments` (the manifest's
lead and members are right). Written 2026-10-23.

Status: `gridflow-build --only neso_data_portal/current_bsuos_ii` clean; detector `[]`; em dashes, arrows and middle dots
0; canonical note CRLF, mirror `cmp` identical. No member is held: every table has a record and the ledger lists all as
eligible.

Files: canonical note `C:\gridflow-wt\vault-neso-bc\30-vendors\neso-data-portal\datasets\current-balancing-services-use-of-system-bsuos-data.md`
(mirror `vault\neso_data_portal\` in `C:\gridflow-wt\fe-neso-bc`); artefacts `site\hifi\data\series\neso_data_portal\current_bsuos_ii.json`,
`samples\...\current_bsuos_ii.json`, `notebooks\...\current_bsuos_ii.json` and `current_bsuos_ii-5.png`; screenshots
`.planning\neso-dp\balancing-costs\bsuos-shots\` (1440, 1024, 768 full page; 390 through a 390 px iframe). Server on
9921 started with recorded PID 7974 and stopped by that PID; 9670 not touched.

## What one row is, and how the runs relate

- **Current files** (`current_bsuos_ii`, `_sf`, `_rf`): one row per settlement date, settlement period and run; each file
  holds one run (`Run Type` `II`, `SF` or `RF`). Code key `settlement_date, settlement_period, run_type` (registry
  `entity_key`, `run_type_column: run_type`). NESO: "There is a file for each run type we calculate a BSUoS charge for -
  Interim Initial (II), Settlement Final (SF) and Reconciliation Final (RF)" (catalogue notes, snapshot 20261006T195819Z).
- **Historic files**: same grain plus `resource_id` (key `resource_id, settlement_day, settlement_period, run_type`,
  `whole_capture` per `resource_id`). Two header epochs per run (three spellings in II): a variable `BSUoS Price (£/MWh
  Hour)` with half-hourly and repeated daily charges to 31 March 2023, then tariff, fund tariff, volume, recoveries and
  actual cost from 1 April 2023.
- **Runs are revisions, never additive.** NESO's charging-methodology report (cited in K-BAL-1-FACTS BAL-1a): successive
  runs recalculate a settlement day with updated costs and metered volumes; reconciliation is the difference between the
  latest charge and amounts already settled. Measured: on all 17,568 periods the 2023-2024 II, SF and RF files share, the
  tariff is identical in all three runs and volume and actual cost differ on every period. Notebook day 17 January 2024:
  SF actual cost is £15,579 to £26,897 above II in all 48 periods, RF within £678 of SF.
- **Historic II overlap.** Registry `_reconcile_adjudications.json` (category `overlap`, ruling 653): the 2024-2025 upload
  (filename `current_ii_bsuos_data.csv`, body 2025-04-01 to 2025-04-13, 624 keys) and the 2025-2026 upload publish the
  same 624 keys with identical values; both are served. Reproduced through `query()`: 2025-04-01 returns 96 rows, 48 from
  each `resource_id`. The page member line says the 2024-2025 file repeats April 2025 rows of 2025-2026.
- **Cap adjustments** have a record (frozen in the Excel batch: 24,092 rows = 3,550 + 3,550 + 8,496 + 8,496, ledger
  "all" eligible), so the member is shown, not held.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Run names Interim Initial, Settlement Final, Reconciliation Final (`what_it_is`, members) | Catalogue notes; field-info `current_bsuos_ii.json` `Run Type`: "either II (Interim Initial), SF (Settlement Final) or RF (Reconciliation Final)" |
| Tariff £/MWh, "fixed tariff ... applied to each calculation for every BSUoS customers charge" (`fields.bsuos_tariff_gbp_per_mwh`) | field-info `current_bsuos_ii.json`, unit `£/MWh` |
| Volume MWh, calculated as recovery divided by tariff (`fields.volume_mwh`) | field-info `Volume_MWh`: "calculated (Column F divided by C) BSUoS recovery (£) BSUoS tariff (£/MWh)", unit MWh |
| Recovery £, NESO says whole day; equals tariff times volume in these rows (`fields.bsuos_total_recovery_gbp`) | field-info "sum of half hour charges for whole day", unit £. Polars: `abs(recovery - tariff*volume)` max 0.073 (SF), 0.058 (RF), 0.0734 (II) over every row of the three 8 October captures; visible in the eight rows |
| Actual cost £, NESO says whole day, changes every period (`fields.actual_bsuos_cost_gbp`) | field-info "Actual BSUoS cost for whole day.", unit £; the eight rows show 1.11e6 to 1.55e6 across periods 33 to 40 |
| Settlement date is a day label written with midnight text (`fields.settlement_date`) | Registry format `%Y-%m-%dT%H:%M:%S `, dtype date; K-BAL-1-FACTS T01; bronze body `2026-09-29T00:00:00` |
| Periods 1 to 48; 46 or 50 on clock-change days (`fields.settlement_period`) | Registry min 1 max 50; `sp_pair` exclusion checks real day length (`casting.py:354`, K-BAL-1-FACTS HR1 2022-03-27 SP47/48) |
| `timestamp_utc` = period start in UTC from date and period, gridflow's anchor | Silver: 2026-09-29 SP33 = 15:00 UTC (BST); 2026-06-15 SP1 = 2026-06-14 23:00 UTC |
| `published_at` = CKAN last-modified of the whole file, read as UTC | Note "Two clocks" (ADR-030); silver `published_at` 2026-10-07 12:23:52.792085 UTC = sidecar `ckan_last_modified` 2026-10-07T12:23:52.792085 |
| Key `settlement_date, settlement_period, run_type` (`record.key`) | Registry `entity_key` |
| Cadence "Daily on weekdays" | Catalogue extra `Update Frequency: Daily (Weekdays)` |
| History: RF from financial year 2016, II and SF from 2017 | Resource descriptions: Historic RF "from the financial year 2016 -2023"; Historic II and SF "2017-2023" |
| Fixed tariff from April 2023, variable price before (`what_it_is`, `chart_view`, SF member) | Header epochs switch at 2023-04-01 in all three historic runs; field-info calls the tariff "fixed" |
| Chart: SF historic, unweighted daily mean price to 31 March 2023 then tariff, £/MWh, 1 April 2017 to 31 March 2026 | Spec `values` [price, tariff], `aggregation: mean`, `time: settlement_day`, window fixed; series 2 x 3,287 points, 157,776 rows used, `spec_origin: vault` |
| Price unit: header "£/MWh Hour", II dictionary gives £/MWh (key note) | Header text in bronze; K-BAL-1-FACTS T03 (Historic II dictionary explicit £/MWh; SF unit cell blank) |
| Chart price is uncapped; cap workbooks hold capped prices (caption) | Join of the SF workbook rows to historic SF on 12,046 keys: `bsuos_price_mwh_hour` difference max 0.0; workbook price above `capped_bsuos_price_mwh` on 167 (CMP381) and 9 (CMP395) SF periods |
| Alt and key numbers: medians 2.04 (2017-18), 3.11 (2019-20), 8.46 (2022-23); 35.80 on 24 Nov 2021; high 44.80 on 20 Jul 2022; steps 13.41, 14.03, 7.63, 12.17, 10.74, 15.69 on each 1 April and 1 October | Read from the committed series (April-year grouping); no negative daily means (lowest 0.27) |
| `dedup` on `settlement_day, settlement_period` by `published_at` | Each SF resource has one capture today (`duplicates_dropped: 0`); set so a later recapture of a yearly file cannot double rows |
| Raw feed: `package_show`, each file downloaded whole unless `last_modified` unchanged; file names change between uploads | `client.py` `iter_members` (1664-1700); sidecars: Current II URL filename `current_ii_bsuos_data.csv` (8 Oct) then `webprice_output_ii_2026-27_1610260959.csv` (16 Oct) |
| Member request URLs | Every URL is the `request_url` of a bronze sidecar (8 October captures) |
| Commands `gridflow pipeline ... --last 24h`, one per historic table | `cli.py` `pipeline(source, dataset, --last)`, one dataset per call; same form as the approved EAC page |
| Notebook lead: `_latest` view, `settlement_day` both ends included, times in UK time | `source.py` `query()` (inclusive predicate); run output `timestamp_utc` dtype `datetime64[us, Europe/London]`, converted with `tz_convert("UTC")` |
| Plot alt numbers (£15,579 to £26,897; within £678; lowest period 15, peak 33, SF £161,334) | Polars on the three historic tables for 2024-01-17 |
| Cap member: CMP381 £20/MWh, CMP395 £40/MWh; adjustment sign differs | Note body (X-R-FACTS scheme notes); `capped_bsuos_price_mwh` max 20.0 and 40.0; adjustment = revised minus original in CMP381 (all negative), original minus revised in CMP395 (all positive), arithmetic exact to 1e-8 |
| Historic RF member: silver drops 27 March 2022 periods 47 and 48 | Note body; K-BAL-1-FACTS HR1 (body 122,690, silver 122,688) |

## Captures: row counts and repeats

Every bronze capture's body bytes equal the declared content length (no truncation).

| Member | Capture (UTC) | File | Body rows | Silver rows |
|---|---|---|---:|---:|
| current_bsuos_ii | 2026-10-08 09:16:48 | current_ii_bsuos_data.csv | 8,736 | 8,736 |
| current_bsuos_ii | 2026-10-16 19:21:34 | webprice_output_ii_2026-27_1610260959.csv | 9,168 | not in silver (date text, see Defects) |
| current_bsuos_sf | 2026-10-08 09:16:55 | current_sf_bsuos_data.csv | 8,016 | 8,016 |
| current_bsuos_sf | 2026-10-16 19:21:41 | webprice_output_sf_2026-27_1610260959.csv | 8,448 | not in silver |
| current_bsuos_rf | 2026-10-08 09:16:52 | current_rf_bsuos_data.csv | 6,672 | 6,672 |
| current_bsuos_rf | 2026-10-16 19:21:38 | webprice_output_rf_2025-26_1610260959.csv | 7,152 | not in silver |
| historic_ii | 2026-10-08 | 2017-2023 / 2023-2024 / 2024-2025 / 2025-2026 | 105,167 / 18,384 / 624 / 17,520 | same (141,695) |
| historic_sf | 2026-10-08 | 2017-2023 / 2023-2024 / 2024-2025 / 2025-2026 | 105,168 / 17,568 / 17,520 / 17,520 | same (157,776) |
| historic_rf | 2026-10-08 | 2016-2023 / 2023-2024 / 2024-2025 | 122,690 / 17,568 / 17,520 | 122,688 / 17,568 / 17,520 |
| cap_adjustments | 2026-10-08 | CMP381 II / SF, CMP395 II / SF | 3,550 / 3,550 / 8,496 / 8,496 | same (24,092) |

Repeats: silver holds one capture per resource, so no capture repeats another's rows. The only repeated keys are the
Historic II 624 (two resources, adjudicated) and the cap workbooks' II and SF rows for the same periods (different runs,
not duplicates). `dedup` is set on the chart only as a guard; the frame filter picks one date of the single II capture.

## Body corrections (vault note)

- `updated:` 2026-10-10 to 2026-10-23.
- Three Known-issues bullets added after "Workbook scope": the adjustment sign reverses between CMP381 and CMP395; the
  workbook table's `_latest` keeps only the Settlement Final rows, so `query()` returns no Interim Initial workbook rows;
  NESO's 16 October 2026 uploads of the current files write day-first dates the frozen format rejects. Each is
  reproduced above. No existing sentence was changed.

## Not verified

- The per-period versus whole-day basis of total recovery and actual cost stays NESO's open question. The page states
  only what the rows show (recovery equals tariff times volume here; actual cost changes every period) and does not sum
  either.
- Whether the historic price is generation-and-demand or demand-only: not stated on the page.
- The 16 October captures' day-first reading: every value I checked has a day above 12 (for example `28-04-2025`,
  `27-08-2025`), so day-first holds; NESO does not state it.

## Open questions for the seat

1. The page's commands and notebook use the historic files, which still parse. A reader ingesting the current files
   today gets captures the transform will reject (Defects 1). The page does not mention this; tell me if it should.
2. The chart comes from a member (`current_bsuos_historic_sf`), as on the approved notifications page; the frame stays on
   the lead through `record.select.silver`.

## Template problems

- `record.select.silver` is not in the author brief: without it the sample follows the chart's table, so a family page
  that charts a member fails `gridflow-sample` with "column not in silver". Worth one line in the brief.
- A pivot with a named index prints as a second header row (`settlement_period` with blank cells) in the notebook
  drawer. Readable, but untidy.

## Defects

1. **gridflow, current BSUoS records (high):** NESO's 16 October 2026 uploads of `current_bsuos_ii`, `_sf`, `_rf`
   (`webprice_output_<run>_<year>_1610260959.csv`) write `Settlement Date` as day-first `DD-MM-YYYY` with no time and no
   byte-order mark (was `YYYY-MM-DDT00:00:00`). The frozen format `%Y-%m-%dT%H:%M:%S ` fails a strict parse on every
   row (checked read-only on the three bronze files). These captures are not in silver; the next transform of the
   current files will fail. Fix: a new record epoch (same header, date format `%d-%m-%Y`). The new II file also carries
   the 1 October 2026 tariff (12.49 £/MWh) and volume at six decimals.
2. **gridflow, `current_bsuos_cap_adjustments` `_latest` (medium):** the table holds both II and SF workbook rows, and
   `_latest` drops `run_type` from the grain, keeping one row per settlement period (the SF rows, uploaded later):
   12,046 of 24,092. `query("current_bsuos_cap_adjustments", ...)` never returns the CMP381 or CMP395 II rows (checked
   2022-01-24: 48 rows, all SF). Either keep `run_type` in the latest grain for this table or document it.
3. **Vendor, cap workbooks (low):** `Total Net Adjustment to Invoices` is revised minus original in the CMP381
   workbooks (negative) and original minus revised in the CMP395 workbooks (positive); no sign is stated. Logged in the
   vault note.
4. **Vendor, current dictionaries (low, already a TODO):** total recovery and actual cost are described as whole-day
   amounts, but recovery equals tariff times volume on every row of all three current files (within £0.08) and actual
   cost varies by period.
