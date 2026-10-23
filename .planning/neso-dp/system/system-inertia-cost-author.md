# System inertia cost (`system-inertia-cost`): writer's report

One-table package page, lead key `system_inertia_cost` (the manifest is right: one table, one family, no held
members; the 2026-27 file is a resource-level hold inside the table, not a member). Canonical note
`C:\gridflow-wt\vault-neso-sys\30-vendors\neso-data-portal\datasets\system-inertia-cost.md` (page block added, one
body bullet added; 111 insertions, 0 deletions; LF, as the committed file is); mirror
`C:\gridflow-wt\fe-neso-sys\vault\neso_data_portal\system-inertia-cost.md` (`cmp` clean). Artefacts:
`site\hifi\data\series\neso_data_portal\system_inertia_cost.json`, `samples\...\system_inertia_cost.json`,
`notebooks\...\system_inertia_cost.json` and `system_inertia_cost-5.png`. No staged chart spec or authored override
existed.

## Status

- `gridflow-build --only neso_data_portal/system_inertia_cost`: passes first time on budgets; only the unrelated global
  warning about 35 dropped "Known issues" lines.
- Detector: `[]`.
- Rendered page text: 0 em or en dashes, arrows, middle dots; no "locally", "held", "our", "since 20", "live", "now",
  "real-time", "yet", "soon", "planned", "coming".
- Screenshots at 1440, 1024, 768 and 390 (390 in a 390 px iframe); my server on 9883, started with the batch method
  (shell PID 541, Windows PID 16896), stopped by that PID, port confirmed free. Nothing clipped or overlapping: hero
  and scenery, chart and key, the four raw-feed wells (long URLs break inside the well at 390), folded frame and guide,
  notebook panel, related list. Unfolded frame not opened (headless, no click).

## 1. What one row is

| Claim | Evidence |
|---|---|
| One row = one settlement date (UK calendar day) from one financial-year file | Registry `registry/system-inertia-cost.json`: `entity_key [resource_id, settlement_date]`, `temporal: date_sp1`, `latest: whole_capture` per `resource_id`; resource descriptions (catalogue snapshot `20261006T195819Z`): "This file is updated daily appending to one file per financial year" |
| The value: indicative average daily price for BM accepted offers tagged as System Inertia | Package notes (snapshot): "indicative values for the average daily price (in £ per GVAs) for BM accepted offers tagged as being for System Inertia" |
| How NESO derives it: the day's total cost of tagged offers divided by the inertia shortfall summed over the day's settlement periods | Package notes, steps 1 to 3 ("sum up the total cost of actions ... tagged as system inertia for a given day", "sum up the total volume of inertia shortfall (GVA.s) in each settlement period", divide); worked examples give £2,250/GVA.s and £2,361/GVA.s |
| Tagging gives the most likely main reason, best endeavours | Package notes: "identifies the most likely main reason for a Balancing Mechanism action, and is a best endeavours process" |
| Unit £ per GVA.s; NESO writes £ per GVAs | Field info `gridflow\.planning\research\neso-snapshots\field-info\20261008T114228Z\system_inertia_cost.json`: `"unit": "£ per GVAs"`, type integer, example 1000; the notes write "£/GVA.s". The same entry's description says "(£ per GVA)"; the page follows the unit field and the worked method, as K-SYS-1-FACTS §7 g4 and ruling 642 do |
| A rate, not a day's spend | The method above; FACTS §7 T01 |
| Two column names, one silver column: `Cost` for 2017-18 to 2020-21, `Cost_per_GVAs` after | Registry epochs; bronze headers (2017 to 2020 `Settlement Date,Cost`; 2021 to 2025 `"Settlement Date","Cost_per_GVAs"`) |
| Whole numbers, no nulls | Registry int64; silver: 0 nulls in all 3,281 rows |
| NESO does not say what a zero means | No catalogue or dictionary text covers it (note TODO INERTIA-COST-ZERO). For the report only, not the page: on 3,280 dates shared with `constraint_breakdown`, a zero price meets zero "increasing system inertia" spend on 2,117 days and a priced day meets non-zero spend on 1,035; 128 days disagree (70 priced with no spend, 58 zero with spend) |
| Cadence "Ad hoc" | Snapshot `extras`: "Update frequency: Ad hoc" |

## 2. Times and the clock

| Claim | Evidence |
|---|---|
| `timestamp_utc` = 00:00 UK time on the settlement date, in UTC (a day label) | `silver/neso_data_portal/casting.py:617-628` (`date_sp1` calls `settlement_period_to_utc(date, 1)`); `utils/time.py:28-42` (period 1 starts 00:00 UK local) |
| Scoped to the rows | Silver, all 3,281 rows: `timestamp_utc` converted to Europe/London is 00:00 on the row's own `settlement_date` every time. Frame: 30 March 2025 at 00:00 UTC, 31 March 2025 at 23:00 UTC the evening before |
| `event_time` = `timestamp_utc`; `available_at` = `published_at` = CKAN `last_modified`, read as UTC | Registry `vintage: ckan_last_modified`; `_bronze.py:192-206` (naive CKAN stamp read as UTC); silver `published_at` per file equals each sidecar's `ckan_last_modified` (2026-04-10 09:06:09.725049 for the 2025-26 file) |
| Workbench | `query()` reads `silver_neso_data_portal_system_inertia_cost_latest`, date column `settlement_date` typed DATE, `BETWEEN` with both ends (checked in the gridflow_models venv: `_relation_name_for_dataset`, `_DATE_COL_SQL_TYPE`). A read-only query I ran returns `timestamp_utc`, `published_at` and `capture_written_at` as `datetime64[us, Europe/London]` (31 March 2025 shows `00:00+01:00`) and `settlement_date` as `datetime64[ms]`. The query cell converts `timestamp_utc`; its output shows `+00:00` |

## 3. Captures, truncation, repeats

One capture per file, all on 8 October 2026 (bronze `system_inertia_cost/2026/10/08/`, 10 CSVs and sidecars). **No
16 October recapture.** Silver: one Parquet per admitted file, all written 2026-10-08.

| File (FY) | Filename | Body bytes = declared length | Bronze rows | Silver rows | Distinct dates | `last_modified` |
|---|---|---|---:|---:|---:|---|
| 2017-18 | `inertia_costs17.csv` | 5,150 = 5,150 | 365 | 365 | 365 | 2021-12-07 12:12:09 |
| 2018-19 | `inertia_costs18.csv` | 5,347 = 5,347 | 365 | 365 | 365 | 2021-12-07 12:14:12 |
| 2019-20 | `inertia_costs19.csv` | 5,386 = 5,386 | 366 | 366 | 366 | 2021-12-07 12:14:59 |
| 2020-21 | `inertia_costs20.csv` | 5,534 = 5,534 | 365 | 365 | 365 | 2021-12-07 12:15:37 |
| 2021-22 | `inertia_costs.csv` | 5,463 = 5,463 | 361 | 361 | 361 | 2022-04-07 08:30:42 |
| 2022-23 | `inertia_costs22.csv` | 5,499 = 5,499 | 362 | 362 | 362 | 2024-04-02 16:17:02 |
| 2023-24 | `inertia_costs.csv` | 5,651 = 5,651 | 366 | 366 | 366 | 2025-01-21 15:54:38 |
| 2024-25 | `inertia_costs.csv` | 5,725 = 5,725 | 365 | 365 | 365 | 2025-09-04 13:30:48 |
| 2025-26 | `inertia_costs.csv` | 5,681 = 5,681 | 366 (to 2026-04-01) | 366 | 366 | 2026-04-10 09:06:09 |
| 2026-27 | `inertia_costs.csv` | 45 = 45 | 1 (`01/04/2026,0`) | 0 (resource hold) | | 2026-04-14 14:54:26 |

No truncation (every body equals NESO's declared length; bronze rows equal silver rows for the nine admitted files).
No repeats within or across files: 3,281 rows, 3,281 distinct dates. Seven dates are absent, exactly as the note says
(2021-11-24 to 26, 2021-12-08, 2022-05-16, 2022-05-17, 2022-08-18). `dedup: {on: [settlement_date], order_by:
published_at}` is set on the chart and the frame as a guard (`duplicates_dropped: 0`). It keys on the date alone, so
a future cross-file overlap (the held 2026-27 row would repeat 2026-04-01 if read day first) keeps the newer upload.

## 4. Chart

`system_inertia_cost`, line, `time: settlement_date`, `value: cost_gbp_per_gvas`, `aggregation: last` (one row per
date), window 1 April to 30 June 2025 (the first quarter of the 2025-26 file), 91 points, unit `£/GVA.s`,
`y_min: -400` so zero days sit just off the axis. One series only; no other cost series is drawn.

Committed series: 61 of 91 days above zero, 30 at zero in runs of one to six days; priced days run from 1,427
(12 April) to 9,366 (17 June), median 2,969; every day is priced from 21 May to 17 June; 15 May reaches 7,714. Why
this window: a daily line over a whole year is a dense comb (about half of all days are zero), and the 2025-26 year
holds one day at 58,570 that flattens the rest. A quarter shows both the price level and the zero days honestly. The
multi-year picture is in the notebook: a per-year table (days, days above zero, median above zero, max: 7 days above
zero in 2017-18, 195 in 2024-25, 174 in 2025-26; the 58,570 is the 2025-26 max) and a log-scale dot plot of every
priced day.

Frame: 27 March to 3 April 2025. It shows the spring clock change (`timestamp_utc` moves from 00:00 to 23:00 UTC from
31 March), a zero day (31 March) and the file boundary on 1 April (`resource_id` and `published_at` change).

Notebook: 5 cells (setup, help card, 3 of mine), 5.9 s, no errors, read-only.

## Body corrections

None needed: every body fact I re-derived holds (row counts, date ranges, missing days, zero counts per file,
`last_modified` values, filename formats, the hold). One addition under "Known issues and gotchas": a bullet on the
isolated 58,570 day (2025-07-25), with a TODO for NESO.

## Unverified

- What a zero price means. NESO is silent; the constraint-breakdown cross-check above mostly agrees, but not always.
- Whether the 58,570 day is valid.
- Whether NESO revises a closed year's file: one capture per file exists.
- The legacy (2017 to 2020) dictionary text: K-SYS-1-FACTS cites it from NESO's web page; the local field-info snapshot
  covers only the 2026-27 resource.

## Open questions for the seat

- **Consistency with the held bid-and-offer page.** `gb-system-inertia-bid-and-offer-costs` is held because "NESO's
  units disagree, £/GVA or £ per GVAs, and it never says what a zero means". This package has the same two traits
  (field description "(£ per GVA)", unit "£ per GVAs"; zeros unexplained), yet the ledger marks it eligible, and here
  NESO's own worked method settles the unit as £/GVA.s. I shipped it and stated both on the page ("NESO writes £ per
  GVAs"; "NESO does not say what a zero means"). The seat may want to confirm the two rulings sit together.

## Template problems

- None blocking. The notebook panel numbers cells from the setup cell, so I wrote the lead without cell numbers
  ("the query cell", "the next").

## Defects

- **NESO data: one isolated extreme inertia price.** `system_inertia_cost` silver (bronze 2026-10-08, 2025 resource
  `a6a52241-1774-48d8-935f-2bef0d843e18`): 2025-07-25 carries `cost_gbp_per_gvas` 58,570 £/GVA.s, four times the
  highest value on any other day in any file (14,650 on 2022-03-09); nearby days are zero or about 4,000 to 4,800.
  The column has no range rule. Question for NESO: is it valid (a tiny shortfall denominator) or an error? Until it is
  answered, any yearly mean or max of this table is driven by one day. Logged in the note's Known issues.
- **NESO metadata: the unit text disagrees within one field.** The `Cost_per_GVAs` dictionary entry's description says
  "Daily average cost of unit of inertia (£ per GVA)" while its unit is "£ per GVAs"; the package notes and worked
  examples use £/GVA.s. Already settled for this table (ruling 642); recorded so the vendor question can carry it.
- **NESO data: what a zero means is undocumented (known, INERTIA-COST-ZERO).** New evidence for that question: against
  `constraint_breakdown` "increasing system inertia" spend, zero prices meet zero spend on 2,117 of 3,280 shared dates
  and priced days meet non-zero spend on 1,035; 128 dates disagree (70 priced with no inertia spend, 58 zero-priced
  with spend).
