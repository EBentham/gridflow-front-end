# Author revision 2: `neso_data_portal/historic_generation_mix`

Writer: Opus 5.5 (high), 2026-10-06. Answers `historic_generation_mix-review.md` (REVISE: 1 blocker, 3 majors, 11 nits)
and the coordinator's rulings.

## Status

- Canonical note edited (CRLF kept), mirrored with `cp`, `cmp` byte-equal.
- `gridflow-build --only neso_data_portal/historic_generation_mix`: succeeds. `detect.mjs --json` (absolute path): `[]`.
  Em dashes, arrows and middle dots: 0.
- Notebook re-run with `scripts/run_notebooks.py`: 6 cells, no errors, 1 image. Series and sample unchanged (chart spec
  and `record.select` untouched; digests pass).
- Screenshots: `scratchpad/hgm_shots2/w{1440,1024,768,390}.png` (+ crops), every Chrome call under `timeout 60`. The seat's
  new axis reads well: years 2009, 2011 … 2025 at 1440 and 2009, 2014, 2019, 2024 at 390. Nothing clipped or overlapping;
  the hero cadence line wraps to three lines at 390 cleanly.

## Findings and fixes

| # | Sev | Fix |
|---|---|---|
| 1 | blocker | `facts.cadence`: "Half-hourly values; NESO's catalogue lists update frequency as hourly; the chart shows one capture" (the approved `daily_wind_availability` pattern). No claim that history is revised hourly. Body `Publication lag` row: the CKAN `extras` `Update Frequency: Hourly` (probe show JSON and the 20 Aug 2026 catalogue snapshot, reproduced: `[{'key': 'Update Frequency', 'value': 'Hourly'}]`), labelled as NESO's label, not an observed cadence (the sidecars show last-modified 20 min, 14.6 h and 9 min before fetch). |
| 2 | major | `fields.imports`: "Each link's imports summed, MW; exports are not netted off (checked against fuelhh)". |
| 3 | major | `fields.low_carbon` and `renewable`: "includes `storage` and `wind_emb`, which NESO's examples omit (checked)". |
| 4 | major | `how_used[0]`: "Fuel-mix and carbon-intensity features since 2009; biomass sits in `other` before November 2017." `fields.biomass`: "zero in NESO's file before November 2017 (last cell)". `fields.other`: "NESO currently counts batteries, transmission solar here; biomass too before November 2017". New last notebook cell prints monthly means for Oct to Dec 2017 (biomass 0 / 1,491 / 1,545 MW; other 932 / 134 / 95 MW), so the break is visible on the page. Body modelling notes add the `other` side (zero before 2012-02-01 16:30 UTC; 932 to 134 MW) with the seat ruling. |
| 5 | nit | `what_it_is` now carries NESO's "seasonal decomposition applied to correct missing or irregular data points" as a vendor statement. `summary`: "generation mix … MW by source" (was "by fuel type"). |
| 6 | nit | `zero_carbon`: "undocumented: well below NESO's examples (wind, solar, hydro, nuclear) here". `zero_carbon_pct`: "undocumented; in these rows not `zero_carbon` over `generation`, above `low_carbon_pct`". |
| 7 | nit | Caption names `solar`, `imports` and `carbon_intensity`. |
| 8 | nit | Pairs kept, as ruled. Template point (two-column key folds at 390) left for the seat. |
| 9 | nit | Alt adds "3,900 to 4,900 MW in 2023 to 2025" (series maxima 3,895 / 4,091 / 4,912). |
| 10 | nit | `timestamp_utc`: "Half-hour start, UTC: NESO states UTC; start checked against fuelhh, 2021 to 2026". Reproduced: lag-0 wind MAE 0.0 / 12.6 / 17.1 / 18.7 / 9.6 / 10.3 MW for 2021 to 2026, against 188 to 236 MW at +30 min. |
| 11 | nit | "currently" restored in `what_it_is`, the `other` and `solar` guide lines and the `solar` key note. |
| 12 | nit | Each `_pct` line now says "share, percent; matches X over `generation` (checked)"; `gas_pct` adds "NESO names no denominator". `zero_carbon_pct` and `generation_pct` keep their own lines. |
| 13 | nit | Body: `zero_carbon` fits nuclear + wind + hydro + biomass + storage within 1 MW in every year 2009 to 2022; from 2023-01-01 08:30 UTC no fixed sum (up to 1,441 MW off). Reproduced. |
| 14 | nit | Head cell is now `df.nlargest(5, "solar")[...]`: midday rows of 20 Sep (13,127 MW down to 12,461 MW). |
| 15 | nit (template) | Hero id pill breaks mid-word at 390. Template-owned; not touched. |

## Unchanged and still open

- `solar` is never called embedded or estimated (the G-1 deduction stands).
- Template: a two-column key folds at 390 (finding 8); the id pill wraps mid-word (finding 15).

## Defects (additions to the first report's list, pasteable)

- **NESO historic_generation_mix: `other` and `biomass` break at November 2017.** In the capture published 2026-09-26
  18:19:36 UTC, `biomass` is 0 before 2017-11-01 20:00 UTC and `other` falls from a monthly mean of 932 MW (Oct 2017) to
  134 MW (Nov 2017) as `biomass` rises to 1,491 MW. Biomass sat inside `other` before then (seat ruling). `other` is also 0
  before 2012-02-01 16:30 UTC. NESO gives no reason. Do not treat either column as one series across the break.
- **NESO historic_generation_mix: catalogue says `Update Frequency: Hourly`.** The vault's "not stated" was wrong (fixed).
  The captures held show last-modified gaps of minutes to hours before fetch, so this is a label, not an observed cadence.
- **Correction to the first report:** `zero_carbon` fits nuclear + wind + hydro + biomass + storage through 2022, not 2018.

## Nits fixed (review 2: APPROVE, 2 nits)

- **A. "Biomass sits in `other`" stated as fact.** Reworded to what the rows show.
  - `how_used[0]`: "Fuel-mix and carbon-intensity features since 2009; mind the November 2017 `biomass` and `other` switch."
  - `fields.biomass`: "zero until 1 Nov 2017, when `other` drops by about as much".
  - `fields.other`: "currently includes batteries, transmission solar (NESO); drops as `biomass` starts (last cell)".
  - Measured at half-hour level (26 Sep 2026 capture), `biomass + other` is 1,462 / 1,463 / 1,462 MW at 18:30 to 19:30
    UTC on 1 Nov 2017, then 1,464 / 1,463 MW at 20:30 / 21:00. The one switch half-hour, 20:00, counts both (2,595 MW).
  - Caution for the seat: **monthly** means do not run on (Oct 2017 932 MW, Nov 1,625 MW, while coal and `generation`
    also rise), so the continuity claim is only made at the switch.
  - The body note now says the sum "suggests" biomass sat inside `other`, and that NESO does not say so.
- **B. Zero before November 2017 not page-visible.** Verified file-wide: `biomass` is 0 on all 154,848 half-hours before
  2017-11-01 20:00 UTC. The last notebook cell now queries 2009-01-01 to 2017-11-01. It prints "biomass max before 20:00
  UTC, 1 Nov 2017: 0.0" and shows the six switch half-hours with `biomass`, `other` and `biomass_plus_other`. The claim is
  now on the page. The old Oct to Dec monthly cell is gone (the cell count stays at 4).
- Optional "(checked)" consolidation not taken: the build needs a line per column, and each line stands alone in the guide.
- Checks: canonical note CRLF kept and mirrored (`cmp` equal). `gridflow-build --only` succeeds. `detect.mjs --json`
  returns `[]`; em dashes, arrows and middle dots are 0. The notebook re-ran: 6 cells, no errors. 390 render of the guide
  is clean (`scratchpad/hgm_shots3/w390_guide.png`).

Summary: both review-2 nits fixed; the November 2017 switch is worded as measured at half-hour level, shown in the last
cell, and the pre-switch zero is printed; build clean, detector `[]`.
