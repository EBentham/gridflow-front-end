# Thermal constraint costs: checker review

Page `thermal-constraint-costs` (lead `thermal_constraint_costs`, member `thermal_constraint_costs_xlsx`).

**Verdict: REVISE** (1 major, 4 nits, 0 blockers).

What was run: `gridflow-build --only neso_data_portal/thermal_constraint_costs` (clean, `wrote ... (dataset template)`), detector `[]`, mirror `cmp` clean,
screenshots at 1440, 1024, 768 and 390 (390 through a 390 px iframe) on port 9911 (PID recorded, only that PID stopped), notebook JSON and PNG, canonical note
diffed against `origin/master`. Nothing clipped or overlapping that is not already a listed template follow-up. Em dashes 0.

## Verified correct (no finding)

- **Chart provenance.** `spec_origin: vault`, 364 points per series, window 2025-04-01 to 2026-03-31. Recomputed from silver (read only): dates and values of all three
  series equal the committed series exactly. SCOTEX max 11,635,590 on 2025-08-31, 168 days above zero; SSE-SP max 8,841,754 on 2026-01-22, 261; SSHARN max
  11,571,424 on 2025-06-27, 94. No negatives in the three shown. 2025-04-08 has no rows in the NESO CSV (bronze body: 0 matches; 2,184 rows = 364 x 6) and the
  SVG paths break there (`L88.4` then a new `M92.9`), so "broken at 8 April 2025" is true. Not stacked, lines. Three shown carry 353.5M of 375.1M across the six; SWALEX zero all year.
- **Alt and key numbers** match. "SSE-SP ... high January and February days": January 48.3M and February 29.2M against 1.4M in April.
- **What one row is.** Key `resource_id, settlement_date, constraint_group` is the registry `entity_key`. Five CSV resources read (2,190 / 2,196 / 2,190 / 2,184 / 1,104
  = 9,864), two workbooks (1,464 + 2,190 = 3,654), equal to the ledger row. CSV years 2022-04-01 to 2026-10-01, workbooks 2019-08-01 to 2021-03-31; joined on
  date and group they share 0 rows; 0 duplicate keys. "The workbooks and CSV files cover different years" is true.
- **2021-22 hold.** Bronze body has 360 quoted comma-formatted cells (`"..."`), the registry HOLD reason says the same, and the ledger agrees. The page line is plain
  and says only what the code does.
- **`dedup` guard.** `distil.py:340` sorts by `published_at` and keeps last per `(settlement_date, constraint_group)`; `duplicates_dropped: 0`. Correct as a guard
  for a recapture of an open-year file, which does restate cells (bronze 2026-10-16 against 2026-10-08: 14 cells differ, for example SCOTEX 2026-09-04 11,295,859
  then 9,085,448; header now `Daily Cost GBP`; 1,164 rows to 2026-10-11). The body correction states all of this accurately.
- **Units and clock as NESO states them.** Field dictionary: "The daily spend in GBP for the constraint. This is an integer (rounded)", unit `£`; "The date the
  constraint costs belong to". Catalogue `Update Frequency: Weekly`. `timestamp_utc` GB local midnight in UTC matches the sample (2025-06-25 23:00 UTC for 26 June).
- **Raw feed.** `client.py:1752-1768` skips an upload member only when the newest capture carries the live `last_modified`; otherwise the whole file is downloaded.
  Request URLs match the bronze sidecars. Commands are real; `pipeline` is ingest, transform and gold build.
- **Notebook.** Written by `scripts/run_notebooks.py`, no error output, no write calls, outputs consistent with silver. Table recomputed: SSE-SP 389.6 (2022-23)
  and 336.8 (2024-25), SSHARN 245.0 (2020-21), SCOTEX range 73.9 to 153.3, 2021-22 blank. `plot_alt` matches the PNG.
- **Related notes** are 12 words or fewer. Sample caption "two costs below zero" is right (-114,367 and -57,574).

## Findings

### 1. major: the additivity wording claims more than NESO says or the rows support

Fields: `page.what_it_is` ("six of what NESO calls significant constraint boundaries, so they do not add up to its total thermal cost"),
`page.how_used[2]` ("the part these boundaries name"), `page.related[0].note` ("NESO's daily thermal constraint total"); same claim in the note body ("The six are
not NESO's whole thermal cost").

I reproduced the comparison (six-group daily sum from both thermal tables against `constraint_breakdown.thermal_constraints_cost_gbp`, latest capture per date).
The number in the note is right: in 2025-26 the median day is 0.073 of the Breakdown figure (364 dates; below on 356, equal on 8, none above). But the wording says
more than that:

1. NESO never says the six are a subset of anything. The catalogue (package notes and every resource description) says the files give "outturn system costs for
   thermal constraints across a number of significant constraint boundaries"; the Network Diagram resource descriptions list exactly SCOTEX, SSHARN, SWALEX, SEIMP,
   ESTEX and SSE-SP as "the constraints contained in the thermal constraints data". So on NESO's text the six ARE "a number of significant boundaries". "Six **of**
   what NESO calls significant boundaries" invents a larger set, and "so" presents a measured cross-dataset gap as if NESO's sentence implied it.
2. The relation to Constraint Breakdown is not constant. By summed cost the six are 0.74 of the Breakdown thermal figure in 2019-20 and 0.83 in 2020-21, then
   0.54, 0.49, 0.33, 0.19 (2025-26). In the first two years the two agree to within 5 pounds on 60 and 76 non-zero days (200 non-zero dates equal exactly across
   the history). So for 2019-21 the six very nearly were the whole figure; "do not add up to its total" as a present-tense universal is not true of those years.
3. "The part these boundaries name" asserts a part-whole relationship. The writer's own report says "Nothing in NESO's text reconciles the two; worth a vendor
   question". Fourteen dates have the six above the Breakdown figure (10 in 2019-21, the five I listed being 1 to 2 pounds, which looks like rounding; but
   2023-03-03 six = 0 against Breakdown -141,345, 2023-04-11 above by 3,963, 2023-06-02 six = 0 against -525, and 2024-05-24 six = 100,613 against Breakdown 0), so a
   strict part of a whole does not hold either.
4. "NESO's daily thermal constraint total" is also the writer's reading: Breakdown calls it the cost of one of four reasons, and NESO says actions can be
   retagged after the event, so the two series may not share a basis.

Fix: state only what NESO says and what the page can show. For example `what_it_is`: "...These files give the outturn cost per date for the six constraint groups
NESO lists in its diagrams. NESO does not say whether they cover all thermal constraint cost." Then `how_used[2]`: "Set against Constraint Breakdown's daily thermal
cost: the two do not agree, and NESO does not reconcile them." If the author wants the gap on the page, scope it to the window and the other dataset by name ("In
2025-26 the six groups' daily sum is a small fraction of Breakdown's thermal cost on most days") and keep the 2019-21 contrast out of a universal. `related[0].note`:
"NESO's daily thermal constraint cost, one of four reasons". In the body, add the by-year share (0.74 to 0.19) beside the 2025-26 median, and note that the 8 equal
dates in 2025-26 are all zero on both sides.

### 2. nit: B6/B7 are sourced to one NESO slide, but the page says "congestion papers"

Fields: `page.chart_view.key[0].note`, `key[2].note`, and the labels "Boundary B6" / "Boundary B7".

NESO's own source exists and I read it: the Operational Transparency Forum slides of 24 June 2026 (neso.energy/document/383631), "Transparency | Network
Congestion" table, rows "B6 (SCOTEX)" and "B7 (SSHARN)". So this is NESO's naming, not gridflow's, and it is not a finding of substance. But it is one slide on a
different dataset (network congestion), the plural "papers" is not supported, and a reader cannot find it. Suggested wording: "NESO's Operational Transparency
Forum slides (June 2026) list SCOTEX as B6." Also the note body gives the alias line without the document link; add `https://www.neso.energy/document/383631/download`.
SSE-SP note ("Drawn on NESO's Scotland network diagram") is exact: the Network Diagram Scotland description says "This file shows the location of the SSE-SP
constraint group".

### 3. nit: `page.summary` calls all six "named transmission boundaries"

NESO's text uses "constraint groups" for the six and "significant constraint boundaries" for the whole; the page itself labels SSE-SP "group" and the other two
"Boundary". Say "six named constraint groups at transmission boundaries" or "six named constraint groups".

### 4. nit: `page.related[3].note` ("made before these outturns")

The cost forecast file covers the next 24 months from October 2026, so it was not made before any outturn on this page, and its scope is thermal, voltage and
stability boundary management plus voltage requirements (vault note for that package), wider than thermal. Suggested: "NESO's monthly constraint cost forecast, 24 months ahead, thermal and voltage".

### 5. nit: the CSV member lists four of six files without saying so

Fields: `page.family.members[0].request`. The list shows 2022-23, 2025-26, 2026-27 and the held 2021-22 file; 2023-24 and 2024-25 are absent. The four-request
limit is a known template follow-up, so this is only a choice of which four. Showing the held file in place of 2023-24 and 2024-25 is the odd pick; the raw feed
note says each file is downloaded whole, which covers it. No change required if the seat prefers it.

## Seat items observed (not findings)

- The 16 October cost-column rename is not on the page, as ruled; the first command still fails on it today (`HeaderEpochError`), already logged as a gridflow defect.
- At 390 the folded frame shows two columns and the notebook tab label clips; four requests per member; family raw feed omits `package_show`. All listed.
- No dark theme exists on the site, so light only.
