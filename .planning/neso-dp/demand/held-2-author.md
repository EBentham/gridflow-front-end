# Held Demand pages, part 2: writer report (2026-10-24)

Three held pages: two one-table pages (`page.held: <reason>`) and one family page (`page.held: true`, a reason per member). Each built with `--only neso_data_portal/<lead>` (`demand_forecast_2_52w`, `school_holiday_percentages`, `transmission_losses_main`). No error lines; only the repo-wide "Known issues" warning. Detector `[]` on all three. Canonical note and mirror `cmp` clean on all three. Notes stay pure CRLF (0 LF-only lines). No series, sample or notebook artefact, staged spec or authored override exists for any key. Every hold line is 16 words or fewer.

Rendered `<main>` text: no em or en dashes, arrows or middle dots. None of live, now, real-time, soon, pending, planned, shipped, locally, ruling, ledger, TODO, E-SEM, RULINGS, held, yet, coming, "our ". Viewport meta and `<main>` present. The "Rows not shown" lines render under "The silver tables".

Screenshots at 1440, 1024, 768 and 390 (390 through a 390 px iframe) on port 9848 are in `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\dem-h2-writer\shots\`. I looked at transmission losses 1440, school holidays 390 and long-term 768. Nothing is clipped or overlapping, and long request URLs and keys wrap. Dark mode not checked. The first Chrome batch wrote no files because it had no `--user-data-dir`; adding one fixed it. Server started with `python -m http.server ... & echo $!` (PID 22293) and stopped by that PID only. Port 9848 free afterwards; 9670 untouched.

All facts below come from code, NESO's catalogue snapshot `20261006T195819Z`, bronze sidecars and silver read with Polars (lazy, read only). Each table has exactly one capture (2026-10-08) and no 16 October recapture, so the notes' "one capture" statements still hold and needed no correction.

## 1. `long-term-2-52-weeks-ahead-national-demand-forecast` (`demand_forecast_2_52w`)

Hold line: "NESO never defines its ESI weeks, and one week number appears twice with two peak dates." It covers both parts of the registry question (the ESI week has no definition; 2027 week 29 appears twice).

| Claim | Evidence |
|---|---|
| Ad hoc | Snapshot extras `Update Frequency: Ad hoc`; resource description "updated on an ad hoc basis" |
| 2 to 52 weeks ahead; national demand = GB's generation requirement, without station load, pumped storage pumping and interconnector exports | Resource description (snapshot) |
| "Balancing supply and demand positions ... NESO's stated purpose" | Package notes: "assist the industry to make efficient decisions in balancing their supply and demand positions" |
| Peak date plus four MW values (peak, minimum, minimum daytime, minimum overnight); ESI week with calendar and financial year labels | Vendor dictionary as quoted in the note; registry header |
| No issue time | Registry `issue.kind: none`; no issue column in the header |
| One week number twice | Silver: `(calendar_year, esiwk)` = (2027, 29) has 2 rows, `cdate_peak` 2027-07-21 and 2027-07-22; every other pair is unique |
| Request lines | Sidecar `request_url`; `package_show` form as on the approved pages |
| Whole file unless `last_modified` unchanged | `client.py` `iter_members` upload branch (about lines 1752-1768) |

Body addition (note, "ESI week and year labels"): a measured finding. `financial_year` equals `calendar_year` on every row except the 13 rows whose peak dates fall from January to March 2027, which carry 2026. The label changes between peak dates 2027-03-31 and 2027-04-05. That fits an April financial year labelled by its first calendar year. The note says plainly that this is a measurement and not NESO's definition. It bears on the note's open question about which month the financial year starts in.

## 2. `school-holiday-percentages` (`school_holiday_percentages`)

Hold line: "NESO calls the `Total` rows percentages but never states their scale: out of 1 or 100." This is the registry question (the scale of `Total` is not stated). The line gives no values. Silver shows the `Total` rows run 0.0 to 1.0, and the local-authority rows are only 0.0 or 1.0; neither range is on the page.

| Claim | Evidence |
|---|---|
| Population-weighted percentage of public schools on holiday across GB and per local authority, with population multipliers; private schools and the City of London excluded; dates from local authority websites; an input to NESO's demand models | Package notes and resource descriptions (snapshot) |
| 1 or 0 per authority | Dictionary comment "currently either 1 or 0" (note body) |
| Yearly | Snapshot extras `Update frequency: Yearly` |
| Six yearly files, 2021/22 to 2026/27 | Snapshot resource list; registry (6 resources) |
| 2024/25 writes dates day first | Registry `formats_by_filename` (`%d/%m/%Y`) |
| Request lines (2021/22, 2024/25, 2026/27) | Sidecar `request_url` of each capture |

Body corrections: none needed. The note is accurate against the data and code.

## 3. `transmission-losses` (`transmission_losses_main`, `transmission_losses_financial_year`)

**Recommendation: a full page, for the seat to rule.** I found no honest reason to hold either table:

- gridflow rules both tables eligible: RULINGS 538 ("BMUs + 2 transmission-losses eligible"); the eligibility report (`docs/neso_data_portal/eligibility.md` lines 306-307 and 463: "eligible", 0 held); the registry has no `eligibility` block on either record (package status `eligible`); the note says "Both families ... neither is held" and its Holds section reads "none".
- The front-end ledger row (line 25) has "—" in both the Eligible and the Held column. That is the only source of the hub's hold, and it looks like a ledger omission: compare the BM units row, which says "reference list".
- The data are clean. Monthly: 161 rows, `Apr-13` to `Aug-26`, unique labels. Yearly: 13 rows, `2013-14` to `2025-26`. No nulls. One vintage per file. All units are TWh (dictionary).
- What a full page would need: `temporal: none`, so `query()` filters on capture time; the notebook would use `data.sql()`. The chart needs a time axis built from the `Apr-13` labels, or `type: none`. A bar chart by financial year from the yearly table is the obvious reading.

Held page written anyway. Each hold line is a true NESO fact and the best plain reason I could give, but neither is gridflow's reason:

- Monthly: "Each year's months do not add up to NESO's yearly figures; NESO does not say why." In silver no financial year matches in every column. GB total differences per year run from 0.0 (2023-24) to 0.2215 TWh (2022-23).
- Yearly: "NESO's yearly figures differ from the sums of their months, most in 2021-22 and 2022-23." Silver: yearly minus monthly GB totals are -0.0485 TWh in 2021-22 and +0.2215 TWh in 2022-23; every other year is within 0.032 TWh.

| Claim | Evidence |
|---|---|
| NGET (England and Wales), SPT, SHETL, GB total, TWh | Resource description; dictionary units (note) |
| Monitored after the event, hard to forecast, depends on where generation runs, chiefly the north-south balance; optimising for losses would raise costs | Package notes (snapshot) |
| Monthly file updated monthly, yearly file annually | Resource descriptions |
| Months from April 2013, years from 2013-14 "in NESO's files" | Bronze bodies (first rows `Apr-13`, `2013-14`) |
| Request lines | Sidecar `request_url` |
| Related `elexon/fuelhh` reason | Package notes: losses sensitive to the geographic generation pattern |

Body corrections: none. The note's reconciliation table matches silver: 2022-23 GB +0.221523, 2021-22 -0.048470, 2023-24 0.0.

## Unverified

- That the 13 January-to-March rows mean an April financial year (stated in the note as a measurement only).
- The transmission losses related line "a yardstick for the size of losses" (historic demand) is a reader use, not a NESO statement.

## Open questions

1. Transmission losses: hold or full page? I recommend a full page (evidence above). If the seat keeps the hold, the note body ("neither is held", Holds "none") disagrees with the page. That is true for gridflow but a checker will see the mismatch, so the seat should say which stands.
2. Should the ledger row for transmission losses read "both" in the Eligible column? A seat item; I did not touch the ledger.

## Template problems

None.

## Defects

- Front-end ledger (`gridflow/.planning/v0.22-FE-LEDGER.md` line 25): `transmission-losses` shows "—" as Eligible though RULINGS 538, the eligibility report and the registry make both tables eligible. This made the hub hold a package gridflow publishes. New.
- NESO, Transmission Losses: the financial-year file is not the sum of the monthly file. 2022-23 GB differs by +0.2215 TWh and 2021-22 by -0.0485 TWh; NESO gives no reason. Already recorded in the note (open item); repeated here for the remediation page.
- NESO, Long Term 2-52 Weeks Ahead Demand Forecast: 2027 week 29 still appears twice (2027-07-21, 2027-07-22) in the only file (last modified 2026-09-29). Confirms the existing hold evidence.
- No gridflow code defect found.

## Transmission losses: full page (seat ruling, 2026-10-24)

The seat ruled a full page. The `held:` lines are gone, and the lead is `transmission_losses_main`, then `transmission_losses_financial_year`. Built with `--only neso_data_portal/transmission_losses_main` with no errors ("charts: 1 template page"); detector `[]`; canonical note and mirror `cmp` clean; CRLF intact (0 LF-only lines). Rendered `<main>`: no em or en dashes, arrows or middle dots, none of the banned words; viewport meta present. Screenshots at 1440, 1024, 768 and 390 (390 through a 390 px iframe), plus a chart close-up at 1440 and a 390 strip, on port 9848, are in `...\scratchpad\dem-h2-writer\shots-full\`. I looked at 1440, 768, 390 and the close-up: nothing clipped or overlapping, and long URLs and keys wrap. Server PID 24294, stopped by that PID; 9848 free; 9670 untouched.

New artefacts (uncommitted): `site/hifi/data/series/neso_data_portal/transmission_losses_main.json`, `samples/.../transmission_losses_main.json`, `notebooks/.../transmission_losses_main.json` and `transmission_losses_main-5.png`.

**Chart.** A stacked area per month and network (NGET at the bottom, SPT, SHETL) from the lead table. The time axis comes from the `Apr-13` labels through `time_text: {format: "%b-%y"}`, which sets each month at its first day; all 161 labels parse. The window is 1 April 2013 to 31 July 2026: 3 series x 160 points, no duplicates dropped (`dedup` on `month_vendor` as a guard; one capture). August 2026 is left out. At 0.1412 TWh GB it is below every earlier month (the next lowest is March 2022, 0.234) and every earlier August (0.349 to 0.628), in a file last modified 25 September 2026. The caption says it is left out and that NESO does not say whether it is complete; the frame shows it. The x label says NESO states no day boundary. The stack top is the three networks summed, which differs from NESO's GB total by at most 0.001 TWh; that total is in the frame. The alt values come from the committed series: 2013-2019 months 0.33 to 0.73; maximum 0.969 in January 2023; minimum 0.234 in March 2022; Scottish share 8.8% to 25.8%; January average 0.66 against 0.42 in June. I chose this over a bar per financial year because the brief takes the chart from the lead's table, and a yearly bar from the monthly table would derive one table from the other.

**Frame.** Every August from 2019 to 2026 (the text labels sort in date order this way), with `dedup` on `month_vendor` as a guard. August 2026 shows plainly against the others. Key `month_vendor` (unique, 161 of 161). The column guide covers every column the frame shows before the fold plus the four lineage columns.

**Where the reader meets the yearly-against-monthly gap.** In `what_it_is` ("2022-23 is 0.22 TWh higher, 2021-22 0.05 TWh lower") and in the `gb_totals` column guide ("2022-23's months sum 0.22 TWh below NESO's yearly figure"). The facts block accepts only vendor, cadence, grain and history (`page_fields.py` line 487), so it cannot go there. The notebook prints the whole table.

**Notebook.** `data.sql()` on the `_latest` views (lead: `query()` filters on capture time). Cell 1 lists the months in order (`ORDER BY strptime(month_vendor, '%b-%y')`, tail through `Aug-26`). Cell 2 sets NESO's yearly GB figure against the months summed per year: gaps of -0.0016, -0.0005, -0.0013, +0.0013, -0.0022, +0.0002, -0.0003, +0.0001, -0.0485, +0.2215, 0.0000, +0.0316 and -0.0076 TWh, 2013-14 to 2025-26, matching the note's table. Cell 3 is a bar plot of those gaps. The first run failed on `GROUP BY ALL` with the mixed aggregate; an explicit `GROUP BY` fixed it. Needs: "NESO's two transmission losses files".

**Related.** `elexon/fuelhh` (NESO: losses are very sensitive to the geographic generation pattern) and `neso_data_portal/historic-demand-data` (a yardstick for scale). Both are true. I added no Elexon ITSDO link, because the losses-to-gap link on that page is unconfirmed.

**Body correction.** The monthly section now records the `Aug-26` figure against earlier months and Augusts, with a `TODO: verify` on whether it is a part-month. The note's "neither is held" now agrees with the page.

### Defects (full page)

- NESO, Transmission Losses monthly file (last modified 2026-09-25): `Aug-26` GB 0.1412 TWh (NGET 0.1162, SPT 0.0153, SHETL 0.0096), below every earlier month and every earlier August. NESO does not say whether its newest month is complete. New; log for remediation. The ledger omission and the yearly gap are already logged by the seat and not repeated here.

## Round 2: the two held pages (review `held-2-review.md`)

Both pages rebuilt with `--only neso_data_portal/<key>` (no errors), detector `[]` on both, canonical notes and mirrors `cmp` clean (transmission losses rechecked too), CRLF intact. The rendered text is clean: no dashes or arrows, no banned words. The new hold lines are 16 words each. No screenshots this round (prose changes only, and the coordinator asked for build, `cmp` and detector).

### `long-term-2-52-weeks-ahead-national-demand-forecast`

1. **major, fixed.** `page.held` now reads "NESO never defines its ESI weeks, and 2027's week 29 appears twice, with two peak dates." (the checker's wording).
2. **nit, fixed.** `how_used` no longer states a horizon in the page's own voice: "Weekly peak and minimum GB demand, which NESO labels 2 to 52 weeks ahead" and "Balancing supply and demand positions, the purpose NESO states for it".
3. **nit, fixed (note body).** "ESI week and year labels" now adds the numbering: 2026 runs weeks 42 to 53 (week 53 peak 2026-12-30), 2027 runs weeks 1 (peak 2027-01-05) to 52, so week numbers 42 to 52 occur under both years and only 2027 week 29 repeats. "Key and coverage" adds that the two week 29 rows are identical in all four MW columns and differ by one day in `CDATE_peak`: this points at a repeated row but does not prove one. No MW values printed, as the note's held rule requires. Cadence's horizon item adds the measured span: peak dates 2026-10-15 to 2027-12-29, about 1 to 64 weeks after the capture and 2 to 65 weeks after `last_modified`. All reproduced from silver on 2026-10-24.
4. **nit, fixed.** `related[0]` now reads "NESO's national demand forecast 2 to 14 days ahead". The two forecast pages are not yet built in this worktree; that is a seat item, as the checker says.
5. **nit, fixed (note body).** The financial-year item in the `TODO: verify` list now says "(the data suggest April: see the measurement below)".

### `school-holiday-percentages`

1. **major, fixed.** `page.held` now reads "All rows stay out: NESO never states whether `Total` rows are out of 1 or 100." (the checker's wording, with `Total` in backticks as on the rest of the page).
2. **nit, fixed.** `facts.grain` now reads "Each row: one local authority on one date, plus one `Total` row per date" (14 words).
3. **nit, applied though optional.** `what_it_is` "its population multiplier" is now "a population multiplier", so it no longer implies one weight per authority (same word count).

### Defects (round 2)

The checker's two new NESO observations are now in the note body: identical MW values on the repeated 2027 week 29 rows, and a week 53 in 2026 with a span of about 64 weeks. They stand as data observations for remediation. No gridflow defect.

## Transmission losses: round 2 (review `transmission-losses-review.md`)

Rebuilt with `--only neso_data_portal/transmission_losses_main` with no error on this page. The "3 error(s) on pages not rendered by --only" line comes from other agents' pages: `_scoped` in `build.py` keeps every error that names the page being built. Detector `[]`; canonical note and mirror `cmp` clean; CRLF intact. The sample was regenerated after the frame's column order changed; series and notebook are unchanged (their spec and cells did not change, and the build's digest check passed). No screenshots this round (wording, column order and note body only).

1. **major, fixed (note body).** The monthly event-time item now says the site page's chart is the one exception: it places each month at the first day of its label (`time_text` `%b-%y`) only to draw the axis, its x label says NESO states no day boundary, silver keeps the label as text, and the boundary and zone stay unverified. The Holds paragraph is narrowed to "do not treat either label as an instant in any zone or join on it as one (the site chart's first-day placement draws an axis only)". The implementation-delta line about the rejected date cast points to that item.
2. **nit, fixed.** `what_it_is` now reads "NESO's yearly GB total for 2022-23 is 0.22 TWh above its months summed; 2021-22's is 0.05 TWh below." (60 words in all). It names the GB total and the direction, and no longer reads as true of every year.
3. **nit, fixed.** The caption now says "The stack's top is NESO's GB total within 0.001 TWh." To fit 40 words I dropped "as NESO labels it" (the x label says it) and "stacked by network" (the key shows it).
4. **nit, fixed.** `related[1]` is now "GB demand by half hour, for scale".
5. **nit, fixed.** The `Aug-26` paragraph is rewrapped to the note's width. The one remaining long line in that part of the note (262) is an existing field-info path.
6. **nit: a guide for the yearly table cannot go in the column guide.** `build.py` line 1296 fails any `record.fields` entry naming a column the lead's silver table lacks ("page.record.fields names columns silver does not have"), and the family template has one frame and one guide, from the lead. What fits: the yearly member's `differs` line now reads "One row per financial year (`2013-14`); columns `sum_of_` plus the monthly names, TWh" (13 words), which is true of all five columns. A real guide for a second member is a template item for the seat. Also, so the August 2026 total the caption points to is visible at 390 px, the frame now prints `gb_totals` second (`columns: [month_vendor, gb_totals, nget, spt, shetl, financial_year, ...]`), with the guide in the same order.
