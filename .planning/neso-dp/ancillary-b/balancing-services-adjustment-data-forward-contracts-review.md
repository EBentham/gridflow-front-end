# BSAD forward contracts page: review

Page `neso_data_portal/balancing-services-adjustment-data-forward-contracts` (table `bsad_forward_contracts`). Checker, 2026-10-18.

**Verdict: REVISE** (2 major, 5 nits, no blockers).

## What was checked and held

- Build `--only neso_data_portal/bsad_forward_contracts` succeeds (only the caveat-grammar warning). `detect.mjs --json` returns `[]`. `cmp` of vault note against mirror clean. Staged chart spec absent; series `spec_origin: vault`.
- Chart reproduced from silver (Polars, newest capture per settlement date and period, window 2017-04-01 to 2026-09-30): 3,105 days per series, 0 mismatches against the committed series (max difference 2e-9). Buy peak 23,988,237.84 on 2022-08-11; 13 days above £10M, 11 in 2022, then 2025-11-21 (£14.80M) and 2026-01-06 (£10.20M); both lines under £1.6M to March 2020 (buy max 1,593,607.50, sell max 907,571.82); sell peak 2,639,168.04 on 2023-05-29; only gap 2020-03-31 to 2021-04-01. Alt text, caption and key notes all match. In the rendered page the coloured lines break across 2020-21 and only the zero rule crosses.
- Failed files, from bronze: 2016-17 has 17,522 non-blank rows, 17,520 distinct pairs, 2 repeated pairs with identical content; 2020-21 has 17,536 rows, 17,520 distinct pairs, 16 repeated pairs, all 16 with conflicting values (for example 25/08/2020 period 1 once all zero, once with volumes). The note's Holds table is right. The page says in the history fact, chart caption, x label and alt text that these files are not loaded; it never implies coverage.
- Row meaning and units: field-info JSON gives BCA and SCA in £, BSA, BVA, SSA and SVA in MWh, with the descriptions the page quotes; NESO gives no sign. The page says so on bca, bva, sca and sva, and says NESO does not explain the `ssa` negatives (8 rows, all -0.001; one `bsa` of -1 is not on the page). No column names a contract or party. Settlement periods 46 or 50 on clock-change days confirmed in silver (8 autumn, 8 spring days).
- Second capture, from bronze: 9,600 rows against 9,168; 9,168 shared periods; 72 differ, all 2026-10-06 to 2026-10-08, all zero in the older capture; 432 new periods; 2026-10-16 and 2026-10-17 all zero. Silver 159,024 rows across captures, 149,856 in the latest view (149,856 distinct pairs). Late-starting rows: 27 and 55, as written.
- Raw feed: `package_show?id=...`, the 2017-18 upload URL and the 2026-27 dump URL match the catalogue snapshot (`url_type` upload and datastore); upload-skip and dump-unchanged behaviour match `client.py` `iter_members`. Package text ("updated twice daily", BSC, outside the balancing mechanism) matches the snapshot `notes`.
- Notebook: written by `scripts/run_notebooks.py`, no errors, cells read-only; the three outputs and every number in `plot_alt` (140.9 at periods 9 and 10, 92.4 at 15 and 16, 83.6 at 37 and 38, under 2 at 37 to 40) reproduce from silver. Lead matches `query()` (DATE column, inclusive BETWEEN, view `..._latest`).
- Sample rows match silver. No dashes, middle dots or arrows on the page. Layout looked at in a browser tab and headless captures at 1440, 1024, 768 and 390 (390 through an iframe); nothing clipped in the sections that rendered (hero to chart; the headless captures stop rendering below the chart because of scroll-reveal, the lower sections were looked at in the browser tab at desktop width).

## Findings

1. **major** `page.what_it_is`: "The newest days of one capture read zero and were filled by the next." This cites our captures ("one capture", "the next"), which the seat ruling allows only as a property of NESO's file. Evidence: it describes two silver captures (2026-10-08 and 2026-10-16). Fix: "NESO's current-year file can show its newest days as zero and fill them in a later upload." No dates or counts. (The sentence is true as a statement about the raw file: all-zero 2026-10-06 to 2026-10-08 in the first dump, filled in the second.)

2. **major** Canonical note body, "Files by disposition": the unchanged sentence "Silver covers settlement days `2017-04-01` to `2026-10-08`" is now false and contradicts the new "Later capture" paragraph two lines below ("settlement dates 2026-04-01 to 2026-10-17"). Silver `settlement_date` max is 2026-10-17 (Polars over all 10 files). The author report says the stale-note defect is fixed; this span was missed. Fix by naming the capture ("to 2026-10-08 at activation; 2026-10-17 now") or moving the clause into the Later capture paragraph.

3. **nit** Canonical note, "Known issues": "Never deduplicate on `(date, period)`" stands beside a chart spec that deduplicates on exactly that pair, ordered by `available_at`. It is safe here (149,856 latest rows are 149,856 distinct pairs; the 8,784 duplicates dropped in the window are the first capture of 2026-27, 183 days x 48), but the note should say the chart relies on that disjointness to take the newest capture. Also "silver's 149,424 rows hold 149,424 distinct pairs" is an activation-time figure now beside 149,856.

4. **nit** Canonical note, "Event clock": "Of the populated rows, 27 have a period start after their capture time ... 55 in the 2026-10-16 capture". The counts are right (27 and 55), but every one of those rows is all zero (none has a non-zero value), so "populated" means non-blank only. Say "non-blank rows" or add "all zero".

5. **nit** Canonical note, new "Later capture" paragraph: "as the methodology's later inclusion of contracts allows" gives a cause for the zero-then-filled pattern from a methodology PDF the writer says was not read. Soften to what was observed, or mark the cause `TODO: verify`.

6. **nit** `page.notebook.needs`: "a capture of NESO's yearly files from 2017-18" does not carry "except 2020-21"; the yearly-sums output then skips 2020 with no explanation. Add the exception.

7. **nit** `page.how_used[1]`: "When in the day NESO buys or sells forward, per settlement period." NESO's dictionary says the period is where the adjustment "occurred"; it is not stated to be when a trade was struck. Safer: "Which settlement periods carry the forward buying and selling." Also optional: `what_it_is` could say each row is a settlement-period total, not one contract (the page currently implies it with "no contract or party named" and the grain line).

Not findings: 132 days in the chart window are all zero in the latest view (spread over 2018 to 2026, including 2026-09-12 and 13) and appear as dips; they are identical in both captures, so no claim is wrong. Template items (caveat-grammar warning, exponent display of `bca` in the folded frame, mid-word break of the long view name at 390) are seat items.
