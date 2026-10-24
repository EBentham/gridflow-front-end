# Transmission Entry Capacity (TEC) register: checker's review

Page `transmission-entry-capacity-tec-register`, table `tec_register`. Checker, 2026-10-24.

**Verdict: REVISE** (1 major, 4 nits, 0 blockers). Every number, the chart, the key, the running-total reading and
the 16 October failure reproduce. The one major is wording: the page does not say plainly that it stops at the
5 October file.

## What I ran

- Build `uv run --system-certs --extra build gridflow-build --only neso_data_portal/tec_register`: exit 0, page
  written (the "37 line(s) ... dropped" warning is the global caveat-grammar notice). Detector `[]`. Em dashes,
  arrows, middle dots on the page: 0. Mirror `cmp` identical.
- Series and sample artefacts: `spec_origin: vault`, `gridflow-distil`, `gridflow-sample`; notebook from
  `run_notebooks.py`, all cells read-only (`data.sql`), no errors.
- Screenshots at 1440, 1024 and 768 (headless Chrome, port 9851) and 390 (390 px viewport, browser pane): nothing
  clipped or overlapping; no horizontal overflow at 390 (`scrollWidth` 390). Chart, key, folded frame, guide and
  notebook panel all legible. The site has no dark theme, so no dark capture. Server stopped by PID.

## Reproduced from silver and bronze (Polars, read only)

1. **Chart.** One silver file, 2,196 rows, one `published_at` (2026-10-06 10:47:29.757067 UTC). Summing
   `mw_increase_decrease` by the note's group map gives storage 176,055.23; solar with storage 139,876.70; other
   combinations 119,201.08 (344 rows); wind 106,795.18; gas 29,594.00; pumped and others 10,720.10; nuclear
   7,620.00; solar 6,938.61; total 596,800.9 MW. Same as the committed series. No nulls, minimum 0.0, so "none
   negative" is true. The chart sums the per-row increment, never the cumulative column (cumulative sums to
   729,484 MW, which would overstate). Staged rows do not overlap: the running total of `mw_connected +
   mw_increase_decrease` over stages reproduces the cumulative column (item 3), and 2,054 distinct `project_id`
   against 2,195 project numbers is exactly the 141 extra staged rows, so no project is split across technology
   rows. Unit (MW) and the file date (named for 5 October, uploaded 6 October = CKAN `last_modified`
   2026-10-06T10:47:29) are stated in title, caption and alt. Alt matches the series; eight bars sum to 596,801.
2. **Key.** `project_number`: 2,195 distinct of 2,196, the repeat is the Immingham pair `PRO-000053` (Built 1,268
   MW; Scoping +50 MW from 2027-07-01, gate 1; same `project_id`). Both rows are in the frame and the guide says
   "Immingham's two lines share one"; the frame caption says "Immingham's two unstaged lines". NESO's dictionary
   calls it "Unique Project Number"; the resource description explains the unnumbered pair ("second line will fall
   away"). Stated correctly. In the 16 October file the pair is `PRO-000053-1` and `-2` and the column is unique
   (2,226 of 2,226), as the note body says.
3. **Running total.** 262 staged rows, 121 projects, all stage-suffixed. Gap to the running total: 258 exactly
   equal, 259 within 1e-9, all 262 within 0.01 MW (the three outliers are PRO-001034, -001046, -001104 stage 2,
   57.00 against 57.01). The guide says "NESO: total across all stages; in these rows, the running total to this
   stage": worded as measured, not as NESO's rule. The body says "measured on the 2026-10-08 capture" and "the
   vendor does not state this rule". Good. 135 rows differ from `mw_connected + mw_increase_decrease`, 134 staged
   plus the Immingham Scoping row: true.
4. **16 October failure.** Bronze `.../2026/10/16/raw_20261016T204705Z_...csv`: 2,226 rows, header identical to the
   5 October file (15 columns), 1,858 of 1,858 populated dates `yyyy-mm-dd`, 0 `dd/mm/yyyy`; the 5 October file is
   1,831 of 1,831 `dd/mm/yyyy`. Registry `format: "%d/%m/%Y"`; `casting.py:267-268` strict `strptime(pl.Date, ...)`.
   gridflow's own record, `state/neso_data_portal/completion_failures/tec_register/*.json`:
   `InvalidOperationError ... conversion from str to date failed in column 'MW Effective From'`; and `DRIFT.md` row
   `tec_register | str→date cast`. `client.py` `iter_members` skip rule and `_assert_window_admissible` read as
   described. Body claims on project-id stability (2,192 shared numbers keep their id; 3 numbers dropped, 34 added;
   1 id dropped, 29 added) all reproduce.
5. **Rest.** Row grain, units (MW; `number` for stage and gate), the date column (only `mw_effective_from`, "past
   dates may still be seen", labelled a contract date in the notebook axis, the guide and the plot alt),
   `agreement_type` values, `host_to` values (NGET, OFTO, SHET, SPT), gate blank until countersigned, status "as far
   as we are aware", request URLs (match the sidecar `request_url`), commands, the `data.sql` lead, notebook outputs
   (status table and `count 262.00, max 0.01` match silver), `plot_alt` (2020 to 2039, no 2021, pre-2026 bars under
   5 GW at most 4.79, Scoping 62% of 2028 and over 72% after, 2037 90.19 GW, 2033 84.42 GW) and the four related
   notes (each 12 words or fewer; embedded header lacks `Agreement Type`, interconnector header has import and
   export columns) are correct. Body corrections are minimal, each cites evidence, and the curl-free note was not
   rewritten beyond the stale TODOs the data answers.

## Findings

1. **major** `page.what_it_is` (and `page.chart_view.caption`): the page does not say plainly that it stops at the
   5 October file. The only mention is `raw_feed.note`: "NESO's 16 October 2026 file writes dates year first;
   gridflow's record parses day first, so its transform fails." That states the failure but not the consequence: the
   chart, frame and notebook describe an older file while NESO has published a newer one. A reader who reaches the
   chart first sees "file of 5 October 2026" with no sign it is not NESO's current file. The precedent page
   (`monthly-operational-metered-wind-output`) puts it in `what_it_is`: "This page stops at the 3 October file:
   gridflow does not read the header NESO renamed on 16 October." Suggest adding to `what_it_is`: "This page stops at
   the file named for 5 October: gridflow cannot yet read NESO's 16 October file, which writes dates year first."
   Evidence: built page text, only occurrence in `raw_feed.note`.
2. **nit** `page.chart_view.caption` / `alt`: "MW due to be added" sums rows whose effective date has passed.
   `mw_effective_from <= 2026-10-06` on 96 rows carrying 17,056.76 MW, and 16 Built rows carry 2,477.05 MW (NESO keeps
   the contracted date until built, so this is the vendor's reading, and the guide says past dates occur). The caption
   says "due at each row's effective date" which stays true, but adding "some dates already past" next to the chart
   would stop a reader taking the whole 596,801 MW as future. The caption also omits NESO's duplicate-entry warning
   (present in `what_it_is`).
3. **nit** `page.what_it_is`, evidence table: the definition "the MW a customer is contracted to inject into the
   transmission system" is not in NESO's catalogue text (the snapshot `notes` and the resource description say only
   "projects that hold contracts for TEC"); the writer's table attributes it to the package description. It is the
   standard CUSC meaning and true, but it is the note's own wording, and the register also holds Demand,
   Interconnector, Substation and Reactive Compensation plant types, so "generation capacity" is narrower than the
   rows. Either drop the attribution or soften to "NESO's list of contracts".
4. **nit** `page.record.fields.plant_type`: "several are joined by ;" renders a lone semicolon as tiny code
   (visible at 1440 and 390). Write "joined by semicolons".
5. **nit** `page.notebook.needs`: "a capture of the TEC register file ingested". An ingest today captures the 16
   October file, whose transform fails, so the notebook returns nothing on a fresh install. Same limit as the
   precedent page and a seat item, but saying "the 5 October file" (or that newer files need the date-format fix)
   would stop a reader being surprised.

## Not findings

- Seat ruling to ship with the newer-file gap stated: accurate (silver holds only the 5 October file; the 16
  October transform fails). Finding 1 asks only that the statement be easy to see.
- The writer's defect text (accept both date formats; `alt_formats` only handled on the datetime path) matches
  `casting.py`: line 268 is a single strict format for dates.

## Round 2

**Verdict: APPROVE.** Rebuilt `--only neso_data_portal/tec_register`: exit 0. Detector `[]`. Mirror `cmp` identical.
Em dashes 0. Checked on the built page text and the note; layout unchanged, so no new screenshots.

1. **Major, newer-file gap: fixed.** `what_it_is` now ends "This page stops at NESO's 5 October 2026 file: gridflow
   cannot read the dates in its 16 October file." True (bronze 16 October: 1,858 of 1,858 dates year first; the
   record's strict `%d/%m/%Y` cast fails) and it states the consequence. The raw feed note still carries the detail.
2. **Past effective dates: fixed, honest.** Caption: "Contracted increases, not built capacity; some effective
   dates are already past." Alt: "contracted TEC increases in MW, some with effective dates already past". Re-derived:
   96 rows in the summed file have `mw_effective_from` on or before 2026-10-06 (17,056.76 MW), so "some" is true; no
   number is claimed, so nothing undated or unverifiable is on the page. The chart title, caption and alt name NESO's
   5 October file, and past dates stay past as time passes, so the wording cannot go stale. Accepted as worded.
3. **TEC definition: fixed.** The "MW a customer is contracted to inject" sentence is gone. The opening now reads
   "NESO's list of projects holding Transmission Entry Capacity contracts" (hero summary identical), against NESO's
   package notes "A list of projects that hold contracts for Transmission Entry Capacity (TEC) with us" (snapshot
   20261006T195819Z). A close paraphrase that claims nothing beyond NESO's text. "MW due to change" matches the
   dictionary's "increase or decrease". The duplicate-entries sentence matches NESO's note 1.
4. **`plant_type` guide: fixed.** Now "several are joined by semicolons".
5. **Notebook `needs`: fixed.** "Needs gridflow and gridflow-models installed, with NESO's TEC register file of 5
   October 2026 ingested." Consistent with the lead and the `what_it_is` sentence.

**Running-total wording across pages:** this page's guide line and the embedded register's
(`vault/neso_data_portal/embedded-register.md:112`) are the same string: "NESO: total across all stages; in these
rows, the running total to this stage". No findings remain.
