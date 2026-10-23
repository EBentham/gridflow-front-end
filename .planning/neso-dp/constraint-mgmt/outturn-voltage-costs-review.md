# Outturn voltage costs: checker's review (round 1, 2026-10-23)

Page `outturn-voltage-costs`, lead `outturn_voltage_costs_main`, member `outturn_voltage_costs_historical`.

**Verdict: REVISE** (1 major, 6 nits, 0 blockers).

## What I checked and how

- Build `uv run --system-certs --extra build gridflow-build --only neso_data_portal/outturn_voltage_costs_main` in `C:\gridflow-wt\fe-neso-cm`: wrote the page, no errors for this page (the 35-line caveat warning is global). Detector on the built page: `[]`. No em dashes, middle dots, arrows or banned local-data words in the built text.
- Mirror `cmp` against the canonical note in `C:\gridflow-wt\vault-neso-cm`: identical. Note diff against `origin/master`: the `page:` block plus one body bullet (two negative sync costs). The bullet's values are right.
- Chart reproduced from silver with Polars (all eleven historical captures, sums per `settlement_month` over 19 groups): 132 months, 2,508 rows, 2,508 unique (month, group) keys, so dedup drops nothing. Committed series differ from my sums by under 0.0005 (three-decimal rounding). Total peak is 64.60 in October 2022 (sync 22.62, utilisation 41.98). Every number in the alt text and key notes reproduces: total 5.55 (Feb 2015) and 24.71 (Apr 2020, sync 18.30) up to March 2021; utilisation low 3.91 (Feb 2020), high 41.98; sync high 40.73 (Apr 2024); utilisation 9.74 to 14.92 in 2024-25; sync above utilisation in 10 of 12 months of 2023-24. Spec origin `vault`, window and unit as stated.
- Facts reproduced from silver: no shared month between main (April, May 2025) and historical; 11 files of 228 rows; main 38 rows; two negative sync costs (-3.81e-06 NE SCOTLAND 2015-11, -0.00613381 HUMBER 2021-02), none in utilisation or main; zero counts 1,394 / 142 / 16 / 2 as in the note. Frame rows match silver (SE ENGLAND 7.04 is the May 2025 sync maximum). `timestamp_utc` is the month start at UK midnight expressed in UTC (`casting.py` 619-625, `settlement_period_to_utc(value.replace(day=1), 1)`); the frame and notebook show 23:00 UTC for BST months and 00:00 for GMT months.
- Notebook JSON: written by `scripts/run_notebooks.py`, five cells, no error outputs, read-only code, inclusive-end `BETWEEN` in `query()` confirmed. Notebook numbers reproduce (S WALES 93.25 + 12.65 = 105.90; monthly totals 51.28 Apr 2024, 12.76 Feb 2025 as the lowest, 39.94 May 2025; utilisation 9.74 to 15.27).
- NESO text read from the 2026-10-06 catalogue snapshot (package notes) and the 2026-10-08 field-info snapshot (dictionary).
- **Not done:** no screenshots and no server (seat instruction), so the clipping and overlap section of the rubric is unchecked by me; I read the built HTML text instead. The writer's screenshots were not opened.

## Findings

1. **major, `page.family.members[0].differs` (also `page.chart_view.caption`, notebook variable `cur`)**: "The current financial year's file, 2025-26" is wrong. NESO financial years run April to March, so on the capture date (October 2026) the current year is 2026-27 and 2025-26 ended in March 2026. The 2025-26 file is the newest file NESO lists, and the page itself says NESO has paused updates. Evidence: catalogue snapshot 20261006T195819Z lists the 2025-26 file as the last resource. Fix: "NESO's newest file, 2025-26" and, in the chart caption, "The newest file's months are not drawn."

2. **nit, `page.what_it_is` and `page.record.fields.utilisation_costs_gbp_m`**: "utilisation costs are only Obligatory Reactive Power Service payments, allocated per group" is stated as the page's own fact. NESO's package note says: "Please note the utilisation costs presented here are only the ORPS payments, allocated per voltage constraint group." The key note and the related note attribute it to NESO; these two places do not, and the canonical body still carries a verify marker on which payment components the allocation covers. Soften by attribution: "NESO notes that the utilisation costs here are only the Obligatory Reactive Power Service payments, allocated per group". NESO's dictionary comment ("Payments to increase or decrease Mvars") and description ("AS costs for voltage") are consistent with this.

3. **nit, `page.what_it_is`**: "files never share a month" is a universal measured on the files (0 shared keys), not a NESO rule. It follows from NESO naming each file for one financial year, so say that: "Each file covers one financial year, so none share a month." Same for the notebook lead's "The files hold different months".

4. **nit, `page.facts.cadence`, `page.family.members[0].differs`**: "NESO says updates are paused" is undated and paraphrased. NESO's words: "The dataset update is currently paused whilst we work on improvements. We're aware that the data is not displaying in full at present, but once the update is complete, data for all months will be available." The snapshot is October 2026; date it ("NESO's package note, October 2026"). The page also never says where the newest file stops. A vendor-file fact with evidence (catalogue datastore total 38 = 2 months x 19 groups) would help: "its file lists April and May 2025 only". Optional, but it answers the first question a reader has about a paused file.

5. **nit, `page.chart_view.title`**: "Voltage cost per month" reads as a total voltage cost. The caption correctly avoids that (two columns summed over the 19 groups and stacked; not called a NESO total; the historical member is named as the source, in caption and alt). Consider "Sync and utilisation costs per month, all 19 groups".

6. **nit, `page.notebook.lead`**: the UTC conversion is correct (`tz_convert("UTC")` of the UK-zone anchor gives 2024-09-30 23:00 for October 2024 and 2024-11-01 00:00 for November, as the output shows). For monthly data it is only meaningful as an anchor instant, not a month label: a reader who keys on `start_utc` would file October 2024 under 30 September. Add to the lead: "read the month from `settlement_month`; `start_utc` is when the month's first settlement period begins". The `timestamp_utc` field note says "gridflow's anchor, not a measurement" but not which column to use.

7. **nit, `page.what_it_is`**: "to keep voltage within limits" is not NESO's wording (NESO: "outturn system costs for maintaining voltage levels on the network"). The canonical body also presents "within limits" as vendor wording. Use "maintaining voltage levels", as the summary does.

## Confirmed correct (no action)

- Sign: the page makes no sign claim; the body bullet states NESO gives no sign convention; the two negative values and their files are right.
- Chart: monthly sums are positive throughout (lowest total 5.55), nothing clipped or folded; no non-additive column summed.
- Keeping the main file as lead is fine; the chart and frame name their silver tables explicitly.
- Raw feed request URLs and the four listed historical requests match the catalogue; the commands take no window, which is right for whole-file downloads.
