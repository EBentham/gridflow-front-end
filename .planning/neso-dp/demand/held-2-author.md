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
