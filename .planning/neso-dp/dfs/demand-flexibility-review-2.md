# Demand Flexibility Service page: checker's second review

Checker, 2026-10-18, after Revision 1. Page `neso_data_portal/demand-flexibility`.

**Verdict: REVISE** (1 major, 1 nit). All five earlier findings are fixed; one new defect came in with the changed `notebook.needs` line.

## Gates

- Rebuilt with `--only neso_data_portal/demand_flexibility_utilisation_summary`: succeeds, only the old caveat-grammar warning. Detector `[]`. No em dashes, arrows or middle dots in the page. Mirror `cmp` clean against the vault worktree note.
- Chart artefact untouched and digest check still passes (the series was not regenerated; spec unchanged).

## Earlier findings

1. **Seasons: fixed.** No "(checked)" remains anywhere. Member line: "current-season MW and cost sum the report's Accepted bids". Guide lines are scoped to current windows ("in current windows, the report's Accepted bids summed"; "current windows: accepted MW × price × 0.5 h"). Both are true on the 1,230 current windows (reproduced in review 1). Nothing implies the report covers the archive.
2. **Loss statement: fixed.** `what_it_is` now says NESO's newest summary file puts two events in one window, silver's key (no `event_id`) cannot hold it, so the page stops at the 6 October 2026 file. This matches the failure record and the chart window; no planning words. The dropped requirement clause leaves the sentence accurate.
3. **Raw-feed note: fixed.** "each of the table's files downloaded whole".
4. **Zeros: fixed.** Caption and `x_label` now say days with no windows are absent and a day with nothing accepted is drawn at zero; the alt says "one point per day with windows". True against silver (40 archive, 14 downwards, 32 upwards zero days).
5. **History: fixed.** "Archive 29 Nov 2024 to 27 Mar 2026; current file starts 14 Apr 2026" reads as a file fact.

Raw-feed headings at 390 px: confirmed fixed. All four member keys now wrap at the underscores (screenshot, 390 px iframe) and nothing in the headings is cut.

## New findings

1. **major** `page.notebook.needs`. The template appends "ingested" to the field, so the rendered line is: "Needs gridflow and gridflow-models installed, with summary capture of 6 October 2026, and report; newer summary files fail ingested." That is garbled public copy. It also says a reader needs a "summary capture of 6 October 2026", which nobody can fetch: NESO re-publishes the current file in place, so a fresh ingest gets the newest file, which fails to load. Evidence: rendered `demand-flexibility.html`, notebook "Needs" paragraph; template wording is "Needs gridflow and gridflow-models installed, with {needs} ingested". Fix: write a fragment that reads in that frame, for example `a capture of the summary and report files (the summary view is empty until the newest NESO file loads)`, or cut the clause about failure since `what_it_is` already says it.

2. **nit** (seat matter, already reported by the writer, not blocking) At 390 px the ingest and transform command lines still cut `demand_flexibility_utilisation_summar` (the well keeps each argument whole). The headings are fixed; the command well is not.
