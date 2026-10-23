# Stability midterm (Y-1) utilisation (`stability-midterm-y-1-utilisation-report`): checker's review

**Verdict: REVISE.** 0 blockers, 1 major, 4 nits. Every number on the page reproduces from silver; the one major is that the
December to March blank is stated only in the alt text, and NESO's own explanation of such a blank is in the package text
the page already cites.

Checked in `C:\gridflow-wt\fe-neso-sys` (branch `feat/neso-dp-system`) and `C:\gridflow-wt\vault-neso-sys`. Build
`--only neso_data_portal/stability_midterm_y1` passes (only the unrelated global warning about 35 dropped Known-issues
lines); detector `[]`; mirror `cmp` clean; note is 301 lines, all CRLF; no em dash, en dash, arrow or middle dot in the
`page:` block or the rendered page; no staged spec or authored override; manifest lead and member list are right.

## What I reproduced (Polars on silver, bronze file, NESO catalogue and field snapshots)

| Check | Result |
|---|---|
| Silver | One parquet, 61 rows, one `published_at` (2026-09-28 16:54:21.377483), one `bronze_capture_id`, one `capture_written_at` (8 Oct 2026); key unique (61 of 61); `timestamp_utc` equals the start on all rows |
| Bronze | One capture dir only (`2026/10/08`), CSV 62 lines (header + 61), 3,950 bytes, sidecar `ckan_last_modified` 2026-09-28T16:54:21.377483, `request_url` equals the page's second GET; field-info `total` 61 |
| No 16 October recapture | `refresh-20261016/ingest.log:282`: "stability_midterm_y1: 0 responses ingested, 1 unchanged since newest capture". No second bronze file exists |
| Chart series vs silver | Count by `month_and_year`: Oct 25 CRUA-4 2; Nov 25 CRUA-4 1; Apr DEEPS-1 6; May DEEPS-1 8, HIRWN-1 2, CRUA-2 1; Jun DEEPS-1 5, HIRWN-1 5, CRUA-2 1; Jul DEEPS-1 6, HIRWN-1 10; Aug DEEPS-1 8, HIRWN-1 6. Totals 2, 1, 6, 11, 11, 16, 14. Equal to the series file element for element (`duplicates_dropped` 0, 61 of 61 used, `spec_origin: vault`, digest passes) |
| Alt text and key notes | All numbers in the alt (2, 1, 6/8/5/6/8, 2/5/10/6, 1 each in May and June, July highest at 16) and in the key notes (3,052 / 496 / 483 / 483 MVA.s, one inertia value per unit; DEEPS-1 every month April to August; CRUA-4 only unit in Oct and Nov) are right |
| Drawn shape | Read from the built SVG paths: 19.2 px per instruction, 1 Oct = x 74, 1 Dec = 221.9, 1 Apr = 515.4. Tops are 2, 1, 6, 11, 16, 14 instructions. CRUA-4's area drops to the baseline at 1 Dec and DEEPS-1's starts at 1 Apr; nothing is drawn between, so the area does not bridge the gap |
| Month label | `month_and_year` equals the month of the end instant on 61 of 61 rows; differs from the start month on exactly 3 (DEEPS-1 starts 28 Apr, 28 May, 30 Jul, all crossing a month end) |
| Row size | Shortest 16 min (CRUA-4, 10 Nov 2025, `00:16:00`), longest `304:25:00` (HIRWN-1, 2 Jun 2026); 48 three-part and 13 two-part duration texts; no overlap within a unit, smallest gap 60 s |
| Four 12-second rows | DEEPS-1 starts 2026-04-03 20:45 (+12 s), 04-09 21:06 (+12), 04-12 22:20 (-12), 04-23 23:50 (+12); file lines 5, 7, 8, 9. Notebook cell 4 output identical |
| Notebook | JSON from the runner; no error output; no `refresh` or `backfill` call in any cell (the word appears only in the help card list). Output equals my hours: CRUA-4 2.4 and 0.3, DEEPS-1 514.5 / 325.9 / 487.9 / 412.4 / 392.2, HIRWN-1 13.5 / 446.0 / 411.6 / 467.1, CRUA-2 4.0 and 25.2. Plot image viewed: matches `plot_alt` (514.5 in April, 411.6 to 467.1 from June, CRUA-4 bars invisible, December to March empty) |
| NESO text | Catalogue snapshot `20261006T195819Z`: "an indicative overview of the monthly utilisation of BMU's with a Stability Y-1 contract", "based on instructions provided by NESO's Control Room", "Time values are all given in GMT", the 25/26 contracts "covering the delivery period of Oct-25 to Sep-26", "From 15th July onwards" consolidation, "Update frequency: Monthly". Field-info `20261008T114228Z`: inertia "MVA.s", duration unit "Hours and Minutes" with example `08:30:00`, `Month & Year` "the month and year of the utilisation period". NESO defines neither "Y-1" nor "midterm" |
| Clock | Registry marks both datetimes `zone: UTC`; `casting.py:600-604` casts the start as `timestamp_utc`. No row falls on 26 Oct 2025 or 29 Mar 2026 (nearest: 25 Oct 02:03 to 03:15 for CRUA-4; then April), so the rows cannot test NESO's GMT statement; the page does not claim they do |
| Elexon register | `elexon/bmunits_reference` silver (one capture, 26 Sep 2026): `T_HIRWN-1` national id `HIRWN-1`, fuel `OCGT`, 299 MW; `T_CRUA-2`, `T_CRUA-4` ids `CRUA-2`, `CRUA-4`, fuel `PS` (Drax Pumped Storage); no `DEEPS-1` under any id, name or national id (the nearest, `T_DEPKG-1` Deeside Peakers, is a different id) |
| Body edits | Each is the smallest span and verified: the intro now quotes NESO; "25/26" is a contract year (NESO text); label equals the end month "in this capture ... NESO does not state that rule"; 12-second detail; 16 October log cited |
| Layout | Screenshots at 1440, 1024, 768 and a 390 px iframe: chart, key, frame, guide, notebook and related list all visible, no overlap or clipping. Folded frame shows 8 rows with the key columns marked |

## Findings

1. **major** `page.chart_view.caption` (and `alt`, `key`): the December to March blank is stated only in the alt text
   ("then nothing from December to March"). Visually the reader sees four empty month ticks and cannot tell data that are
   missing from months that had no instructions. NESO answers this in the package text the page already cites: "Where
   there is no update to this dataset for a given month, it is due to the service not being utilised in that month."
   Fix: one sentence in the caption, for example "No instructions are in the file for December to March; NESO's package
   text says a month with no update is one when the service was not used." Keep it NESO's statement, not ours; the file
   shows no row, it cannot show why. (The drawn area is honest across the gap: it does not bridge it, verified in the
   SVG; the issue is only the missing words.) Evidence: catalogue snapshot `20261006T195819Z`, package `notes`; SVG
   paths for CRUA-4 (`... L221.9 390.8 L221.9 410 ...`) and DEEPS-1 (starts at `515.4`).
2. **nit** `page.chart_view.key[1].note`, `key[2].note` and `page.related[3]`: the Elexon fuel-type notes are undated
   and uncited on the page, DEEPS-1 gets no fuel note and no sentence on why, and the match is by id (NESO's `HIRWN-1`
   to Elexon's national grid BM unit id), which NESO does not state. Nothing is false: HIRWN-1 `OCGT` and CRUA `PS` are
   in the register, and the page makes no claim about DEEPS-1. But the largest unit in the chart (33 of 61
   instructions) looks left out for no reason. Suggest dating the register in the related note ("Elexon's register of 26
   September 2026 lists fuel type and capacity for the CRUA and HIRWN units", trim to 12 words) and adding to the
   DEEPS-1 note: "Not in Elexon's BM unit register as of 26 September 2026." That is a dated fact about Elexon's
   register, not a claim about the unit. Leaving the asymmetry as is is also defensible; I would do it.
3. **nit** `page.summary`: "start and cease in GMT" states the clock as fact, while every other place says "NESO gives
   GMT, read as UTC". The registry types the columns UTC (no shift), which is gridflow's reading of NESO's statement.
   Suggest "start and cease as NESO gives them (GMT)". The hero is the one spot a recruiter reads first.
4. **nit** `page.chart_view.caption`: "which here is the month each one ends" is scoped by "here" only; the field guide
   says "in this file", which is the clearer observation. It is true of all 61 rows and the chart counts all 61, so no
   change is required, but "which in this file is the month each one ends" matches the guide and cannot be read as
   NESO's rule. (Answer to the writer's open question: keep "this file", not "these rows"; the rows shown are 8 of 61
   and would under-scope it.)
5. **nit** note body, `Month & Year` bullet (vault note, not the public page): NESO's own description ("the month and
   year of the utilisation period") is not quoted next to the new end-month observation, so the tension with the
   dictionary wording lives only in the writer's Defects text. Add the dictionary quote to the bullet; optional.

## The five questions

1. **Chart.** Reproduced exactly from silver; notes and alt text agree with the series file. A stacked area across a
   gap is acceptable here because the renderer breaks the area at the gap (checked in the SVG) rather than ramping from
   November's 1 to April's 6; the gap itself needs words (finding 1). Within a run of months the area ramps between
   mid-month points, which makes a monthly count read as continuous (a template item the writer already lists).
2. **Month label.** True on 61 of 61 rows; worded "in this file" in the field guide and "here" in the caption, and the
   body says "NESO does not state that rule". Not presented as a NESO rule. Finding 4 is wording only.
3. **Elexon fuel-type notes.** Right against the register as captured 26 September 2026; DEEPS-1 is absent under every
   id, name and national id. The page handles it by silence, which is honest but unexplained (finding 2).
4. **What a row is, Y-1, clock.** One control-room instruction to a unit on a Stability Y-1 contract, contracted inertia
   in MVA.s; "Y-1" is not defined and the page says so; NESO's GMT statement is attributed to NESO in the guide, and the
   summary should match (finding 3).
5. **Captures.** One capture, 61 rows, no 16 October recapture, NESO's file last modified 28 September 2026; notebook
   hours per unit and month and the four DEEPS-1 12-second discrepancies match silver.

## Not findings

- `chart_view.x_label` "month as NESO labels each instruction", and the axis showing "1 Dec" to "1 Mar" with no year
  (template items, seat).
- The notebook plot's palette puts a brown on CRUA-2 (alphabetical order in the hours plot); it is not the chart palette.
- Not verified by me: that NESO's GMT statement is true of the rows (no row touches a clock change, as the writer says),
  and what "Y-1", "midterm" and "BMUID-1" mean.

## Process

Server: python http.server on port 9897 started with output to /dev/null, Windows PID 452 (command line confirmed
before stopping), stopped by that PID only. One scratch HTML wrapper I briefly copied into `site/hifi/` by mistake was
removed straight away (it was untracked; `git status` now shows only the writer's files). No other file written except
this review; no git writes, ingest, live API or drift check. Scratch files are in `...\scratchpad\midterm-checker\`.
