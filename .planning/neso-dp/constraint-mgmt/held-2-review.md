# Held pages, Constraint management part 2: checker review (2026-10-23)

Verdicts: both pages APPROVE. 0 blockers, 0 majors, 9 nits (4 on the congestion page, 5 on the voltage page). No note-body
findings: every body correction I re-derived is right.

| Page | Verdict |
|---|---|
| `operational-transparency-forum-network-congestion-data` | APPROVE |
| `voltage-requirement` | APPROVE |

## What I ran and read

Batch file, standing instructions, rubric and author brief (held-page section), the writer's report, both canonical note
diffs against `origin/master` in `C:\gridflow-wt\vault-neso-cm`, the mirrors in `C:\gridflow-wt\fe-neso-cm\vault\neso_data_portal\`,
the built pages, both registry JSON files (eligibility question per family), the ledger rows (53 and 55), the 2026-10-06
catalogue snapshot (package notes, extras, resource descriptions), the 2026-10-08 field dictionaries, the bronze sidecars and
bodies of all three families (`otf_network_congestion`, `voltage_requirement`, `voltage_requirement_files`), the group-map and
introduction PDFs (text), `refresh-20261016/ingest.log` and `reconcile.log`, and the neighbours' `page:` blocks for the related
notes.

Gates, my own runs: `gridflow-build --only neso_data_portal/otf_network_congestion` and `.../voltage_requirement` both ok, only
the known vault-wide "Known issues" warning; `cmp` canonical note against mirror clean on both; detector `[]` on both; no series,
samples or notebook files exist for either family (held mode). `updated: 2026-10-23` on both notes. Rendered text, checked on
the UTF-8 page text: 0 replacement characters, em or en dashes, arrows or middle dots; none of live, now, yet, soon, pending,
coming, planned, shipped, real-time, locally, ruling, ledger, TODO, E-SEM, our copy. The words "rows" and "capture" appear only in
the held reason, the "Rows not shown" label and the shared transform comment ("the capture's date to silver", same wording as the
approved pages). No page states a capture date, size or row count. Viewport meta, `<main>`, language attribute present.

Overflow at 390 px, measured (the writer did not): both pages in a true 390 px viewport (browser pane emulating 390 by 844).
`clientWidth`, `scrollWidth` and `body.scrollWidth` are all 390 on both pages; 0 non-SVG elements extend past the right edge; 0
elements with inner horizontal scroll or clipped overflow. I looked at the raw feed and "The silver tables" sections at 390 on
both: long request URLs wrap, nothing clipped, one "Rows not shown" entry. Viewport emulation reset to desktop.

Server: port 9914, started from Bash (a PowerShell start was blocked by the guard), Windows PID 30884 (shell PID 17563)
recorded, stopped by that PID only, port confirmed down. Port 9670 not touched.

## The four asks

**1. "Rows not shown" lines against the ledger's question.** The ledger rows name only the topic and the unit; the question is
the registry's `eligibility.question` for each family, which the writer used. Both lines are plain, free of codes and accurate.
- Congestion: "NESO does not explain its dates, how actuals are derived, or when forecasts were issued." Registry question: is
  Date a week start, week end or reporting label; how are actuals calculated; when was each forecast issued. The dictionary has
  an empty description and unit for `Date` (field info 20261008T114228Z), and describes Actual only as "Actual <boundary>
  boundary constraint limit", so "does not explain" is true on all three. The forward-target half of the question (26 targets on
  or before the vintage) is not on the page, which is right: it is the project's test, not a NESO fact.
- Voltage: "NESO leaves unstated which nights each range covers, each group's area and when rows were issued." Registry question
  has four parts: overnight window and endpoint inclusivity, reversed ranges, which zone each `V_` code covers, whether `Last
  Updated` is an original issue time. The line covers three of the four. **Is it still honest? Yes.** Nothing in it is false and
  nothing implies the date ranges are sound; "which nights each range covers" is a fair reading of the window and inclusivity
  part, and a reader cannot tell which nights a range covers when 17 rows end before they start. But it is the weaker half of the
  question: the reversed ranges are the one concrete, checkable oddity (17 rows in each capture, start 2025-08-23 to end
  2025-08-18 on nine rows and start 2025-08-26 to end 2025-08-22 on eight, re-derived from bronze), and a 16-word line can
  carry them. See finding 6.

**2. "The later rows carry a forecast only" (congestion `what_it_is`).** True of NESO's file and not a local-data reference.
Re-derived from both bronze bodies: every one of the 26 later rows has all 11 Actual cells blank and all 11 Forecast cells
populated (the first blank row is 2026-10-17 in the 8 October body and 2026-10-24 in the 16 October body, every earlier row
has actuals, and Forecast is populated on all 53 rows in both). It states no count, date, coverage or "held" fact, and anyone
who downloads the file sees it; it also follows from NESO's own description of a window running "forward and backward from the
published date". The only weakness is that "the later rows" is vague (later than what?). See finding 2. Keep the claim.

**3. Raw feed against bronze, capture dates, 16 October note bodies.**
- Every request URL equals the `request_url` of the newest sidecar: congestion CSV `otf_constraint_data_14-10-2026.csv`
  (sidecar of the 16 October capture; the 8 October capture's name was `07-10-2026`); voltage CSV
  `overnightvoltagerequirement20-26_1.csv` (same name on both captures); voltage group map `ew-voltage-zones.pdf` and
  introduction `intro-to-voltage-management.pdf` (8 October sidecars; `ingest.log` line 330 confirms all three PDFs were
  unchanged on 16 October). Dataset and resource ids match the catalogue snapshot. `package_show?id=` slugs are right.
- Voltage shows two of three PDFs under the four-request cap (package_show, CSV, group map, introduction); the deep dive
  (`voltage-deep-dive.pdf`, id `633e7e26...`) is left out. **Does it say so? Yes, tersely:** "Three PDFs (an introduction, a deep
  dive and the group map) stay in bronze; two shown." It does not name the one not listed; the note is at the 30-word cap. See
  finding 7.
- The commands are real: `voltage_requirement_files` is a real family (three PDFs, catalogue only), and both transforms run
  (`reconcile.log` lines 248 and 265 drained one file each on 16 October). `ingest.log` lines 253, 329 and 330 match.
- No stale capture date on either page; the only date-like token is the congestion file name, which is explained in the raw-feed
  note and is the newest bronze URL.
- Note bodies for the 16 October recaptures, all re-derived and correct. Congestion: second body 53 rows 2026-04-18 to 2027-04-18,
  first 2026-04-11 to 2027-04-11; 38 Saturdays and 15 Sundays in the first, 37 and 16 in the second; one 8-day step
  (2026-12-26 to 2027-01-03) in both; 26 blank-Actual rows in both; 52 shared dates, 13 rows and 28 cells changed, 11 Actual cells
  of 2026-10-17 filled from blank, 3 Actual cells of 2026-10-03 restated (`B6` 4550 to 4750, `B6a` 6200 to 6150, `B9` 11500 to
  7500), 14 Forecast cells on 11 dates from 2027-01-03 to 2027-04-11; 5,706 and 5,705 bytes. Voltage: 5,221 and 5,257 rows,
  288,655 and 290,643 bytes; 0 keys dropped, 0 changed, 36 added in four ranges by nine groups (Saturday to Monday and Tuesday to
  Friday pairs, `last_updated` 2026-10-09T14:16Z and 2026-10-16T12:50Z); the newest 18 rows carry `last_updated` 14:19Z and 14:20Z
  against `last_modified` 13:22:22, and 12:50Z against 11:52:51 (57 to 58 minutes); the 18 rows starting 2020-07-31 and
  2020-08-02 with `last_updated` 2021-07-30T15:22Z are present in both bodies; `(start_date, group)` repeats once per body and
  the three-part key is unique. The body edits are scoped (the deletions are the single-capture phrasings they replace).

**4. Overflow at 390.** Measured, none on either page; see above.

## Findings

### Page 1, `operational-transparency-forum-network-congestion-data`: APPROVE

1. **nit** `page.how_used[0]`: "Forecast boundary limits set against the actual limit NESO later reported" asserts that the
   forecast came before the actual, which is exactly what the page's own reason says NESO does not state ("when forecasts were
   issued"); the note body also records that a past row's forecast may be a rebuilt value, and that three published Actuals were
   restated between the two uploads. It is the one place the page comes close to contradicting its hold. Suggest "Forecast
   boundary limits compared with the actual limit for the same week" (12 words, under the 14 budget).
2. **nit** `page.what_it_is`: "the later rows carry a forecast only" does not say later than what, and the comma-and joins it to
   a statement about NESO's dictionary, so it reads as if the dictionary says it. The fact is right (ask 2). Suggest "and the
   rows after the latest actual carry a forecast only" (replaces three words with six; the field is at 56 of 60, so 59).
3. **nit** `page.raw_feed.note`: "The file's name carries the upload date." The note body is careful that the date token is "a
   name, not a documented publication instant"; the three names seen (30-09, 07-10, 14-10-2026) do match the CKAN
   `last_modified` day, but NESO does not say so. Suggest "The file's name carries a date and changes with each upload."
4. **nit** `page.related[0]` and `page.related[1]`: "under other codes" reads as the same boundaries named differently. What
   the note establishes is only that no exact code is shared (11 labels against 12 and 31 codes), with a vendor crosswalk still
   a `TODO: verify`; NESO's own aliases (`B6 (SCOTEX)`, `B15 (ESTEX)`) cover a few. Suggest "with different boundary codes"
   (the fact as measured) in both notes; both stay well under 12 words.

### Page 2, `voltage-requirement`: APPROVE

5. **nit** `page.what_it_is`, `page.summary`: "the following Monday to Friday nights" and "the weekdays after" are NESO's package
   wording stated in the page's own voice, on a page whose reason says NESO leaves unstated which nights each range covers (the
   rows the file actually carries are Saturday to Monday and Tuesday to Friday pairs, so Monday sits in the weekend range). Attribute
   it, for example "NESO describes the plans as covering the next weekend and the following Monday to Friday nights", trimming
   elsewhere to stay inside 60 words (the field is at 59).
6. **nit** `page.held`: honest as written (ask 1) but it drops the reversed-ranges question and weakens "overnight window and
   endpoint inclusivity" to "which nights". A 16-word line that carries all four: "NESO leaves unstated what each range covers
   (some run backwards), each group's area and issue times." (16 words by whitespace count, no codes.)
7. **nit** `page.raw_feed.note`: "two shown" is correct but terse and does not say which PDF is left out or why. Suggest "Three
   PDFs stay in bronze; the deep dive is not listed." in place of the parenthetical and "two shown" (25 words in all), since the
   other two are visible in the list.
8. **nit** `page.facts.cadence`: "each upload is the whole file, earlier plans included" states a rule from two uploads; the note
   body itself says two captures do not establish that published rows never change. The file holding earlier plans is something
   anyone downloading it sees, so say that: "Weekly, as NESO lists it; the file holds earlier plans as well."
9. **nit** `page.related[0]`: "the cost side of these plans" implies a link NESO does not state. The outturn page's own summary
   is the cost of maintaining voltage per voltage constraint group. Suggest "What NESO spent keeping voltage within limits, by
   voltage group" (10 words).

## Defects (for the seat to paste)

- **gridflow, `voltage_requirement`:** all three writer defects reproduce from bronze. `Last Updated` in the newest upload of each
  capture sits 57 to 58 minutes after CKAN `last_modified` (so UK local time labelled `Z` is plausible, unproven); 18 rows start in
  2020 with a 2021-07-30 update stamp (probable year slip); the file is cumulative over the two uploads compared (0 dropped, 0
  changed, 36 added, one weekly upload between the captures was never captured itself).
- **gridflow, `otf_network_congestion`:** NESO restated three published Actuals for 2026-10-03 between the 7 and 14 October
  uploads (the `B9` figure moved from 11500 to 7500), and revised far-dated Forecasts; no Forecast on a date on or before either
  vintage changed in this pair. Matters for any forward-target ruling.
- **Seat items, not findings:** registry status reads `eligible` on both packages while each family is held (known pattern); the
  held pages are not in the sidebar nav, so `aria-current` does not appear (template behaviour, as on the part 1 pages); manifest
  lead and member lists are right for both (one-table pages).
