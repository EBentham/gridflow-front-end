# Thermal constraint costs: writer report, round 2

Answers `thermal-constraint-costs-review.md` (REVISE: 1 major, 4 nits) and the seat's ruling on the major. Note edited in the
vault worktree (CRLF kept), mirrored and `cmp` clean. Build `--only neso_data_portal/thermal_constraint_costs` clean, detector
`[]`, 0 em dashes. The notebook was re-run because a cell was added; the series and sample did not change (chart and record
specs untouched).

## Fixes

1. **Major: additivity wording** (seat ruling: NESO lists exactly these six; state only what the rows show).
   - `page.what_it_is`: no longer says the six are a subset or "do not add up". Now: the files give the outturn cost per
     date for six constraint groups NESO's diagrams locate; "Summed by year, they are three quarters or more of Constraint
     Breakdown's thermal cost in 2019-21, a fifth in 2025-26; NESO does not reconcile them."
   - The numbers are now visible on the page: a new notebook cell joins the six groups' daily sum to
     `constraint_breakdown` `thermal_constraints_cost_gbp` on shared dates and prints yearly £ million and share: 0.74
     (2019-20), 0.83 (2020-21), 0.54, 0.49, 0.33, 0.19 (2025-26), 0.25 (2026-27 to 1 October). Same figures as my silver
     measurement and the checker's.
   - `page.how_used[2]`: "Set against Constraint Breakdown's daily thermal cost, date by date." (no part-whole claim).
     `how_used[0..1]` say "constraint group" and "Group costs" instead of "boundary".
   - `page.related[0].note`: "NESO's daily thermal constraint cost, one of four reasons".
   - `page.notebook.needs`: adds "Constraint Breakdown's yearly files", which the new cell reads.
   - Body: the "not NESO's whole thermal cost" sentence is replaced by: NESO's diagram descriptions list exactly these six;
     the by-year shares above; median day 0.07 in 2025-26; its 8 equal dates are all zero on both sides; a few dates have the
     six above Breakdown; NESO's text does not reconcile the two (`TODO: verify`).
2. **B6 and B7 source**: key notes now read "B6 [B7] in NESO's Operational Transparency Forum deck of 24 June 2026", no
   "papers". The day counts dropped from those two notes to stay within 18 words (still in the alt). The body alias line now
   names the deck, its date, the "Transparency | Network Congestion" table and links
   `https://www.neso.energy/document/383631/download`.
3. **Summary**: "NESO's daily spend in pounds on thermal constraints for six named constraint groups, one file per
   April-to-March year."
4. **Related forecast note**: "NESO's monthly constraint cost forecast, 24 months ahead, thermal and voltage" (from that
   package's note: thermal, voltage or stability boundaries plus voltage requirements).
5. **Four of six files**: `raw_feed.note` now ends "The CSV table lists four of its six file URLs." I kept the choice of
   four (2022-23, 2025-26 for the chart and rows, the open 2026-27 file, and the held 2021-22 file the connector still
   downloads), which the checker left to the seat.

## Checks

- Removed wording absent from the built page: "papers", "do not add up", "part these", "made before", "transmission
  boundaries" (0 matches).
- Notebook: 6 cells, no errors; new output table 2019-20 to 2026-27 (no 2021-22 row, as expected for an inner join).
  `plot_alt` unchanged and still true (plot cell unchanged).
- Screenshots: the 390 px iframe capture (`thermal-shots\thermal-390.png`) is complete. The round-2 headless captures at
  1440, 1024 and 768 stopped painting below the chart (blank page colour, chart key missing), and a fresh Chrome profile
  did the same. The built HTML has all six sections, so I checked in the browser pane at 1440 and 768: every stratum is laid
  out and visible (positions read by script: sky 64, topsoil 894, bronze 2238, silver 3180, gold 4090, deep 4839; page height
  5418 at 1024), the key, raw feed, frame, guide and notebook render with nothing clipped, and the console has no errors. So
  those three PNGs in `thermal-shots\` are not a true picture of the page; the round-1 set showed the same layout correctly.
  Servers: 9901 started from Bash with PIDs 15195, 15239, 15365 and 15448 recorded, each stopped by `kill <pid>`; 9670 not
  touched.

## Defects

None new. Round 1's defects stand (open-year header rename blocking silver, already in the 2026-10-16 drift record; NESO's
2026-27 description reading "25-26"; the six groups' sum not reconciling with Constraint Breakdown).
