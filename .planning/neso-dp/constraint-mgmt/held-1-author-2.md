# Held pages, Constraint management part 1: writer revision 2 (2026-10-23)

All eight page nits and the note-body nit from `held-1-review.md` are fixed, plus two note-body corrections the review's
Defects section asked for (day-ahead duplicate causes, cost forecast pound-sign reading). Canonical notes in
`C:\gridflow-wt\vault-neso-cm\30-vendors\neso-data-portal\datasets\` (Edit tool, CRLF on every line: 221/221, 296/296,
315/315, 366/366), re-mirrored to `C:\gridflow-wt\fe-neso-cm\vault\neso_data_portal\`, `cmp` clean on all four.

| Page | Build `--only` | Detector | Rendered text sweep |
|---|---|---|---|
| `24-months-ahead-constraint-cost-forecast` | `constraint_cost_fc_24m`: ok | `[]` | 0 dashes or replacement characters, no banned words |
| `24-months-ahead-constraint-limits` | `constraint_limits_24m`: ok | `[]` | same |
| `constraint-management-intertrip-service-information-cmis` | `cmis_intertrip`: ok | `[]` | same |
| `day-ahead-constraint-flows-and-limits` | `da_constraint_flows_limits`: ok | `[]` | same |

The builds print one "error on pages not rendered by --only, left for the full build": it belongs to another agent's
page (my four render and pass). No server was started in this revision. The changes are word-level, so the part 1
screenshots and the checker's 390 px overflow measurements still describe the layout.

## The fixes

| # | Field | Change |
|---|---|---|
| 1 | cost `page.held` | "NESO dropped £m from the column name, and the dictionary's £m is unconfirmed." (13 words) |
| 2 | cost `page.what_it_is` | "In NESO's words it does not include" becomes "NESO says it does not include" (a paraphrase, no longer presented as a quote) |
| 3 | limits `page.what_it_is` | "A boundary splits the transmission network in two." Unattributed: I did not read the NESO ETYS source in full, so it is not cited as NESO's |
| 4 | intertrip `page.what_it_is` | Opens "Units contracted under NESO's Constraint Management Intertrip Service (CMIS) are armed to manage network constraints."; "its arming and disarming times, the fee"; "NESO says times are GB local; each ends in +00:00." (60 words) |
| 5 | intertrip `page.held` and `what_it_is` | Held: "Times carry +00:00 though NESO says local time, and the fee's unit is given two ways." (16). What it is: "For the arming fee since 2024-25, NESO's dictionary describes £/MWh but gives the unit as £ per settlement period." |
| 6 | intertrip `page.raw_feed.note` | "... each yearly file unless `last_modified` is unchanged (first and newest). Headers differ by year; the newest's October 2026 header is not read into silver." (30 words) Explains why no transform line is shown |
| 8 | day-ahead `page.held` | "Boundary and half-hour pairs repeat, and NESO does not explain 99999 limits or the flow's unit." (16). Checked on both captures: 8,166 `Limit_MW` cells are `99999`, 3,365 `Flow_MW` cells blank; the dictionary gives the flow no unit |
| 9 | day-ahead `page.raw_feed.note` | "Everything stays in bronze." becomes "The diagrams are re-issued under new names." (the ingest comment still says "bronze only") |
| 7 | intertrip note body | "NESO restated three published costs" corrected: `WHILW-1`, `WHILW-2`, `BLLA-1` (armed 2026-04-03T03:49) had a cost of 0 on 2026-10-08 and a nonzero cost on 2026-10-16; **zeros filled in, not figures revised**. Four zero-cost rows on 8 October, one on 16 October. Fixed in "A third header", the Cadence block ("edited in place ... filled in the cost ... where it had been 0") and the sentinel bullet ("a zero in the current-year file may be a cost not yet entered") |

## Further note-body corrections (from the review's Defects)

- **Day-ahead, "Why the capture failed":** replaced "others fall on ordinary dates, so a fold rule alone does not explain
  them" with what both captures show (checked 2026-10-23): all 44 value-differing key groups are the repeated autumn hour
  (01:00 and 01:30 on 2024-10-27 and 2025-10-26, 11 boundaries each), so a fold rule would separate them; the 1,392
  whole-row duplicates are two whole repeated days, 2025-08-12 at 11 boundaries (528 excess) and 2026-08-19 at 18 boundaries
  (864), which no fold rule explains. Added the `99999` and blank-flow counts.
- **Cost forecast, Units paragraph:** the registry's "undecodable symbol before `m`" does not reproduce; the field-info bytes
  hold a valid `C2 A3` pound sign in title, description and unit. The question is the file's missing unit, not a garbled
  character.

## Defects (for the seat to paste)

- **gridflow, `da_constraint_flows_limits`:** the duplicate keys have two separable causes (fold rows: 44 groups; two whole
  repeated days: 1,392 rows), identical on both captures. Also, the ruling 632 adjudication reason cites "ERROEX,
  2025-08-12T00:00:00, 265 and -3" as a value-differing pair, but no value-differing key group falls on 2025-08-12; the two
  rows are probably different raw keys (seconds against minutes spelling). Worth checking when the adjudication is revisited.
- **gridflow, `cmis_intertrip`:** the 2026-10-14 upload filled in three zero costs (current-year zeros can be costs not yet
  entered) and dropped every unit from the header; the 16 October capture still fails the header check.
- **Registry, `constraint_cost_fc_24m` hold question:** reword from "undecodable symbol" to the missing unit in the file.
- Unchanged: package registry status reads `eligible` on all four packages; manifest entries correct; the OTF related links
  resolve to a page the next batch writes.
