# Held Generation pages, part 2: writer report (2026-10-24)

Packages: `weekly-wind-availability` (`weekly_wind_availability`) and `wind-bmu-boa-volumes` (`wind_bmu_boa_volumes`). Both are one-table held pages (`page.held: <reason>`), no chart, frame or notebook, and no artefacts.

Gates: canonical notes edited in `C:\gridflow-wt\vault-neso-gen` (Edit tool, CRLF kept, 0 bare LF), mirrored to `C:\gridflow-wt\fe-neso-gen\vault\neso_data_portal\`, `cmp` clean on both. `gridflow-build --only neso_data_portal/<lead>` wrote both pages with no errors (only the repo-wide "Known issues" warning). Detector `[]` on both. No series, sample or notebook file exists for either key. Rendered `<main>` text: no em or en dashes, arrows or middle dots; none of live, now, real-time, planned, shipped, locally, ruling, ledger, TODO, E-SEM, held, yet, soon, pending, coming (the only "our " hit is "half hour through"). Viewport meta present. Screenshots at 1440, 1024, 768 and 390 (390 through a 390 px iframe) on port 9807, in `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\gen-h2-writer\shots\`; I read BOA 1440 and 390 and weekly 768: nothing clipped or overlapping, long URLs wrap. Light mode only. Server started with its PID recorded (37597) and stopped by that PID; 9670 untouched.

## 1. `weekly-wind-availability` (lead `weekly_wind_availability`)

Hold line (15 words): "NESO never defines its week labels, so no row can be tied to a calendar week." The table is one table and every row is a BM unit and a week label, so the line covers the whole table. The horizon mismatch (155 labels against 2 to 52 weeks) is in `what_it_is`, dated.

### Evidence

| Claim | Evidence |
|---|---|
| Hold question: `Week Number` calendar undefined; 155 labels against 2-52 weeks | Ledger line 32; eligibility report line 335; registry `weekly-wind-availability.json` `record.eligibility` |
| "2 to 52 weeks ahead"; "technical availability ... rather than what they are able to actually produce based on wind speed" | Snapshot `20261006T195819Z` package notes and resource description |
| "Weekly, NESO says" | Snapshot extras `Update Frequency: Weekly` |
| Label described only as the week units are available; example `13W20` | Field info `20261008T114228Z/weekly_wind_availability.json` ("Week number for the BMU's are available", example `13W20`); `MW` unit MW |
| Files of 8 and 16 October 2026 each carry 155 labels | Bronze: 08 Oct (`last_modified` 2026-10-08T11:20:20) 281 BM units x 155 labels, `43W26` to `40W29`; 16 Oct (`last_modified` 2026-10-16T20:20:25) 281 x 155, `44W26` to `41W29`; every label has 281 units; 43,555 populated rows each |
| One CSV, upload; downloaded whole unless `last_modified` unchanged | Registry `url_type: upload`; `client.py` `iter_members` upload branch (about lines 1750-1764) |
| Request URLs | Sidecar `request_url` (both captures); `package_show` form as on the approved pages |
| Commands | Keys in the registry; same form as the approved held pages |
| Related | `neso_data_portal/daily_wind_availability` (live sibling; NESO describes it in the same words, by day, 2-14 days); `elexon/uou2t14d` (Elexon page set); `neso_data_portal/14-days-ahead-wind-forecasts` (page set, another agent's held page) |

### Body corrections (canonical note)

- "Captured" now also lists the 2026-10-16 recapture (`raw_20261016T204817Z_..._b4901dfb.csv`, `last_modified` 2026-10-16T20:20:25.674628, 752,941 bytes, 43,555 rows, `44W26` to `41W29`).
- The filename statement and "one header epoch" now cover both captures.
- Clock 1 gives both captures' `last_modified`.
- Hold question paragraph: the label range is dated to the 08 Oct capture, with the 16 Oct range added.
- New "Second capture" paragraph after Activation: second Parquet file, 43,555 rows; `_latest` takes 16 Oct whole.
- Cadence: three `last_modified` observations, not two.
- `updated:` 2026-10-24.

### Unverified / open

- Label `53W26` is in both files and ISO 2026 has 53 weeks, so the labels fit an ISO reading, but NESO does not say so. Not on the page.
- "Capacity changes by unit, as a supply input to longer-range margin outlooks" is a use case, not a NESO statement.

## 2. `wind-bmu-boa-volumes` (lead `wind_bmu_boa_volumes`)

Hold line (16 words): "All years stay out: NESO never says what repeated rows mean, and 2026/27 has positive volumes." "All years" covers the whole table: the six clean files as well as the three rejected ones. Both parts of the ledger question are there: row identity, which applies to every year (repeats on date, period and unit occur in every file except 2026/27), and the positive volumes in 2026/27. `what_it_is` states just before it that NESO defines the volume as negative, and dates the repeats and positives to the files as published on 16 October 2026. BOA (bid-offer acceptance) and BM unit (balancing mechanism unit) are each spelled out once, in the summary.

### Evidence

| Claim | Evidence |
|---|---|
| Hold question | Ledger line 34; eligibility report line 336; registry `record.eligibility` |
| `BOA_Volume` in MW, "The volume of generation curtailed by the BOA", negative "to represent the fact that they reduce the output of the wind farm" | Field info `wind_bmu_boa_volumes.json` |
| Units "used in our wind incentive forecasts" | Snapshot resource descriptions |
| "Daily, NESO says" | Snapshot extras `Update frequency: Daily` |
| Financial years 2018/19 to 2026/27, April to March | Snapshot resource names and descriptions ("from April 2018 to March 2019" ...) |
| Repeats, as published on 16 October 2026 | Bronze: whole-row repeat excess 18 (2018/19), 1 (2019/20), 2 (2024/25) = 21. Repeat excess on date, period and unit: 44, 290, 244, 9, 3, 85, 789, 932 for 2018/19 to 2025/26, and 0 for 2026/27 (total 2,396). The 16 Oct ingest skipped the eight closed files because their `last_modified` was unchanged, so those bodies were still NESO's files on 16 Oct |
| 2026/27 positive volumes | Bronze: 1,044 (08 Oct capture), 1,125 (16 Oct capture); no other file has any |
| Transform rejects 2018/19, 2019/20, 2024/25 | Note's adjudication section (ADR-040, `DuplicateEntityKeyError`); silver holds no rows from those three resources |
| Requests (2018/19, 2024/25, 2026/27) | Sidecar `request_url` for each |
| Related | `elexon/boal`, `elexon/bmunits_reference` (Elexon page set); `neso_data_portal/monthly-operational-metered-wind-output` (page set). The register line's "the project matched these" rests on the note's measured 208 of 209 match to `national_grid_bm_unit` |

### Body corrections (canonical note)

- BOA expansion corrected from "Offer-Acceptances" to "bid-offer acceptances", the Balancing and Settlement Code term (Elexon's BOAL is Bid-Offer Acceptance Level).
- Removed "The newest local capture of each resource is the only capture available", which the data proves wrong. Added a dated "Second capture of 2026/27" paragraph:
  - recaptured 2026-10-16 (`last_modified` 2026-10-16T09:00:18.236752, 160,485 rows, dates to 2026-10-16); the other eight files were skipped as unchanged;
  - rows dated before 2026-10-08 are identical to the first capture as a multiset, so NESO only appended;
  - no repeats, and 1,125 positive volumes;
  - silver holds both 2026/27 captures, so the latest rows over the clean resources are now 920,239.
- Cadence TODO: one capture per closed year; 2026/27 has two, appends only.
- Hold question item 2: the registry's 1,044 is dated to the 08 Oct capture, beside 1,125 on 16 Oct.
- `updated:` 2026-10-24.

### Unverified / open

- `elexon/boal` relation: the note measured a key-level overlap (15,071 of 16,270 unit/period keys). The related line claims only that BOAL records each accepted bid and offer by BM unit, which is BOAL's own summary.
- Whether NESO revises closed years: still unknown, with one capture each.
- `landscape: market` (balancing). `power` would also fit; it is scenery only.

## Template problems

None. The one-table held mode rendered as the brief describes.

## Manifest

The lead and members in the page set match (one table each). No change suggested.

## Defects

- NESO, Weekly Wind Availability: the `Week Number` calendar is undefined, and the files of 8 and 16 October 2026 each carry 155 labels (about three years under an ISO reading) against the documented 2-52 weeks. `BMU_ID` carries the dictionary unit "MW". Already in the note; confirmed on the second capture.
- NESO, Wind BOA Volumes:
  - whole-row repeats in 2018/19, 2019/20 and 2024/25 (21 excess rows), and repeats on date, period and unit in every closed year;
  - positive `BOA_Volume` in 2026/27 against the negative definition, rising from 1,044 (8 Oct) to 1,125 (16 Oct);
  - the 2026/27 resource description is the placeholder "Upload Wind-BMU-BOA-Volumes" (snapshot 6 Oct).

  All confirmed.
- gridflow (registry text, minor): the hold question gives "1,044 positive volumes" with no date, a count from one capture; the 16 Oct capture has 1,125. The question is in code, so I left it alone; the note now dates the count. Suggest dating it or dropping it at the next registry edit.
- No gridflow code defect found.
