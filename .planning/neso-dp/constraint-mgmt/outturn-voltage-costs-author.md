# Outturn voltage costs: writer's report (round 1, 2026-10-23)

Page `outturn-voltage-costs`; members, lead first: `outturn_voltage_costs_main` (lead), `outturn_voltage_costs_historical`.

Files: canonical note `C:\gridflow-wt\vault-neso-cm\30-vendors\neso-data-portal\datasets\outturn-voltage-costs.md` (CRLF kept,
420+ lines all CRLF; mirror `vault\neso_data_portal\outturn-voltage-costs.md` in `C:\gridflow-wt\fe-neso-cm`, `cmp` clean);
artefacts `site\hifi\data\series\neso_data_portal\outturn_voltage_costs_main.json`, `samples\...\outturn_voltage_costs_main.json`,
`notebooks\...\outturn_voltage_costs_main.json` and `outturn_voltage_costs_main-5.png`. No staged chart spec or authored override existed.
Build `--only neso_data_portal/outturn_voltage_costs_main` clean (the 35-line caveat-grammar warning is global, not this note);
detector `[]`; zero em dashes in the built page. Screenshots `.planning\neso-dp\constraint-mgmt\outturn-voltage-costs-shots\`
(1440, 1024, 768 full page; 390 through a 390 px iframe). Server on 9902 started from a shell whose Windows PID (18752) was
recorded; the listener was its child python PID 11136, stopped by `taskkill /PID 11136` only; 9670 not touched.

## 1. What one row is, and how the two files relate

- **One row = one settlement month x one voltage constraint group**, carrying two costs in £m (`sync_costs_gbp_m`,
  `utilisation_costs_gbp_m`) and a `coordinates` text point. No split by type beyond those two cost columns.
  - Code: registry record (gridflow `docs/neso_data_portal/profile/families/outturn_voltage_costs_main.json`, `record.entity_key`
    `[settlement_month, voltage_constraint_group]`; historical adds `resource_id`), `temporal.kind: month`, `latest: whole_capture`
    (historical partitioned by `resource_id`). Generic engine, no hand transformer.
  - NESO: dictionary "Settlement Month: Total cost per Settlement Month. Date presented visually as 01/MMM/YYYY but represents
    the whole 'Month'"; "Voltage Constraint Group ... these 19 voltage requirement areas" (field-info snapshot 20261008T114228Z).
- **Current and historical are disjoint, consecutive files, never revisions.** Historical = eleven financial-year CSVs (2014-15 to
  2024-25), main = the 2025-26 CSV. Measured: 0 shared (month, group) keys between main and any historical file; 0 duplicate keys
  within historical across all eleven files; 0 within main. The page says "files never share a month" and the notebook lead says
  "stack them, never add" (i.e. concatenate; never sum a month across files, which cannot happen anyway).
- **Should historical lead?** My recommendation: **keep the current file as lead** (no manifest change). Lead only decides the
  artefact key and the default frame table; the chart already draws from the historical member (`chart.silver`, BSUoS precedent)
  and the frame names `select.silver: .../outturn_voltage_costs_main` explicitly. If NESO resumes updates, new months land in the
  2025-26 file, so the lead is where a reader looks for the newest rows. A historical lead would also be defensible (2,508 of
  2,546 rows); it would change nothing on the page but the artefact filenames.

## 2. Units, sign, period and clock

| Claim | Evidence |
|---|---|
| Both costs are £m | NESO dictionary unit `£(m)` for `Sync Costs (£m)` and `Utilisation Costs (£m)`; registry column names `*_gbp_m` |
| Sync = BM and trade costs of running units | NESO dictionary: "Costs in the balancing mechanism to run the unit. From trades and balancing mechanism actions." |
| Utilisation = only ORPS payments, allocated per group | NESO package note (catalogue snapshot 20261006T195819Z): "utilisation costs presented here are only the ORPS payments, allocated per voltage constraint group"; dictionary comment "Payments to increase or decrease Mvars" |
| Sign | NESO states none. Utilisation: no value below zero (min 0.0). Sync: two historical rows below zero, `-3.81e-06` (NE SCOTLAND 2015-11) and `-0.00613381` (HUMBER 2021-02); main none. Page makes no sign claim; chart sums are all positive (lowest monthly sync sum 0.15) |
| Zeros are real stored values | historical 1,394 zero sync, 142 zero utilisation (all 142 both-zero rows); main 16 and 2; frame shows SOUTH YORKS 0.0/0.0. Page: "zeros as written", no meaning claimed |
| `settlement_month` is a date label for the whole month | dictionary above; registry `dtype: date`; per-file formats in the record (`%d/%m/%Y` main, map for historical) |
| `timestamp_utc` = start of the month's first settlement period, UTC | gridflow `src/gridflow/silver/neso_data_portal/casting.py:619-625` (`settlement_period_to_utc(value.replace(day=1), 1)`); rows: May 2025 -> `2025-04-30 23:00 UTC` (BST), Nov 2024 -> `2024-11-01 00:00 UTC` (GMT), shown in the frame and in notebook cell 1 output |
| `published_at` = CKAN `last_modified` of the whole file, read as UTC | `generic.py` / `casting.py:570` (`ctx.published_at`), vintage `ckan_last_modified`; one value per capture (main `2025-06-23 11:40:39 UTC`) |
| Notebook times converted | `query()` returns session-zone (UK) times; cell 1 adds `start_utc = timestamp_utc.dt.tz_convert("UTC")` |
| `query()` reads `_latest`, filters `settlement_month` inclusive, drops lineage | gridflow_models `_get_method_registry`: date column `settlement_month`, relation `silver_neso_data_portal_<member>_latest`; `source.py:401-451` inclusive predicate, `_BITEMPORAL_EXCLUDE` drops `event_time, available_at, source_run_id, dataset_version` |

## 3. Captures, row counts, dedup

| Member | Captures | Rows per capture | Months x groups |
|---|---|---|---|
| `outturn_voltage_costs_main` | 1 (2026-10-08, `last_modified` 2025-06-23) | 38 | 2 (Apr, May 2025) x 19 |
| `outturn_voltage_costs_historical` | 11, one per resource (2026-10-08) | 228 each = 2,508 | 12 x 19 per financial year, 2014-04 to 2025-03 |

No truncation (every file is full months x 19 groups; NESO's datastore `total` for main is 38, matching). No capture repeats
rows today (0 duplicate (month, group) keys across all captures). `dedup: {on: [settlement_month, voltage_constraint_group],
order_by: capture_written_at}` is set on **both** the chart and the frame **as a guard**: a re-capture after NESO restates a file
would add a second parquet with the same keys, and both artefacts read every capture. Distil provenance: `duplicates_dropped: 0`.

## 4. Chart

- Stacked area, silver `outturn_voltage_costs_historical`, `values` utilisation (bottom, petrol) then sync (top, clay), `sum` over
  the 19 groups per `settlement_month`, window 2014-04-01 to 2025-03-31 (132 monthly points, 2,508 rows, 11 files), unit £m.
  Summing groups is additive (each row is a group's allocated cost in £m; NESO's own dictionary calls the month "Total cost").
- What it shows (series file): total from 5.55 (Feb 2015) to a peak of 64.60 (Oct 2022); utilisation 3.91 (Feb 2020) to 41.98
  (Oct 2022), then 9.74 to 14.92 in 2024-25; sync peaks 40.73 (Apr 2024) and exceeds utilisation in 10 months of 2023-24.
  All numbers in the alt and key notes were read from the committed series.
- The two 2025-26 months are not drawn (one silver table per chart); the caption says so, and the notebook plot shows
  April 2024 to May 2025 across both files.

## Frame and notebook

- Frame: 8 of 19 groups for May 2025 from the 2025-26 file (`select.silver` explicit, because `sample_silver` otherwise falls
  back to the chart's table). Shows two zero sync costs, a both-zero row, the largest sync value (SE ENGLAND 7.04) and the
  mixed-case `Dumfries & Galloway`.
- Notebook (run by `scripts/run_notebooks.py`, no errors, read-only): cell 1 joins 2024-25 history and the 2025-26 file and
  shows SE ENGLAND with UTC anchors across a clock change and the file boundary; cell 2 ranks 2024-25 group totals (S WALES 105.90,
  of which sync 93.25); cell 3 stacked bars of monthly totals, April 2024 to May 2025. `reset_index()` used in cell 2 to avoid the
  stray index-name header row.

## Body corrections (canonical note)

- Added one bullet under "Sentinels and missing values": the two below-zero historical sync costs with exact values and files,
  and that NESO states no sign convention (silver, checked 2026-10-23). Smallest span; nothing else in the body changed.
- No other body fact found wrong: per-file date formats, 19 labels, 228/38 row counts, month anchors, zero counts (1,394 / 142 /
  16 / 2) and the 0-key overlap all reproduced.

## Unverified / open questions

- What the 2024-05-24 bulk `last_modified` stamps on ten historical files mean (re-upload or not); the page states no publish
  history beyond NESO's file list.
- Whether sync plus utilisation is NESO's complete voltage cost; the page only stacks the two columns and does not call the sum
  a NESO total.
- No documented key joins these groups to `voltage-requirement` groups (the related note says so).
- Dark mode: the site defines no dark theme (no `prefers-color-scheme` or `data-theme` rule in `tokens.css`, `theme.css`,
  `site.js`), so only the light rendering exists; checked light at all four widths.

## Template problems (seat items)

- A member lists at most four requests: the historical member has eleven files, so the four newest are listed and `differs`
  says so.
- At 768 the folded frame shows `sync_costs_gbp_m` but not `utilisation_costs_gbp_m` until unfolded (known follow-up).
- At 390 notebook code breaks names mid-word and the notebook tab label truncates (known follow-ups).
- `gridflow-sample` silently reads the chart's silver when `select.silver` is absent; on a family page whose chart draws from a
  non-lead member this picked 0 rows until `select.silver` was set. Worth a line in the author brief.

## Defects

- **NESO outturn voltage costs: two negative sync costs with no stated sign convention.** `outturn_voltage_costs_historical`
  has `sync_costs_gbp_m = -3.81e-06` (NE SCOTLAND, 2015-11-01, 2015-16 file) and `-0.00613381` (HUMBER, 2021-02-01, 2020-21
  file); NESO's dictionary states no sign. Probably vendor rounding or a small credit; recorded in the vault note, no gridflow
  change needed. Severity: low (data note, not a pipeline bug).
- **NESO outturn voltage costs: current file stalled.** The 2025-26 file (`073f9ffa-...`) holds only April and May 2025 and was
  last modified 2025-06-23; NESO's package note says updates are paused. Not a gridflow defect; a refresh check should notice
  when it resumes, and whether resumed months arrive in the same resource or a new one (the registry maps only `073f9ffa` to
  `outturn_voltage_costs_main`).
- No gridflow code defect found.
