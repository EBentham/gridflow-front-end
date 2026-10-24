# Review: data-portal-planned-changes-known-issues (lead `portal_known_issues`)

Checker, 2026-10-24. Worktrees `C:\gridflow-wt\fe-neso-dpc` and `C:\gridflow-wt\vault-neso-dpc`.

## Verdict: REVISE

0 blockers, 1 major, 5 nits. The numbers, chart, captures and quotes all reproduce. The one major is the
"8 October file" wording, which the reader cannot check.

## Findings

1. **major** `page.what_it_is` (also `page.chart_view.caption` and `page.how_used[2]`): the page cites an 8 October
   file that nobody can fetch.
   - `what_it_is` says "items 239 and 240 read Planned in its 8 October 2026 file and Deployed on 16 October". "Its"
     is NESO's, so a reader will try to open NESO's 8 October file.
   - The note body says it cannot be fetched (`30-vendors/neso-data-portal/datasets/data-portal-planned-changes-known-issues.md:299`,
     "Only the current register is published, so earlier states cannot be fetched"). The evidence is gridflow's own
     capture: sidecar `raw_20261008T111649Z_...meta.json`, 179,505 bytes, `ckan_last_modified` 2026-10-08T09:43:34.
   - Nothing on the page shows the 8 October values: not the chart, the eight rows nor the notebook outputs. It is
     local history presented as a vendor fact with no source (rubric 3).
   - Two other spots lean on the same idea. The caption says "an earlier or later file counts differently" (true
     for gridflow's captures: 8 October is Deployed 209, 16 October is 214). `how_used[2]` says "Compare NESO's
     files item by item".
   - Fix, either way:
     - Say whose evidence it is: "gridflow's capture of NESO's 8 October 2026 file has items 239 and 240 as
       Planned; NESO's 16 October file has them Deployed. NESO publishes only its current file."
     - Or use something the reader can see: item 241's note ("Has been rescheduled for 19/10/2026") sitting beside
       a description that still says 15th October. Both are in the frame.
   - Re-word the caption and `how_used[2]` to match ("compare gridflow's captures item by item", "another day's
     count may differ").
   - The wording is not dishonest about NESO's data, since 239 and 240 did move. It fails because it implies a
     check the reader cannot make.

2. **nit** `page.record.fields.description`: says "NESO's full text of the change or issue".
   - The frame does not show the full text. The sample cuts at 1,000 characters plus "..." (rows 242, 243, 244 and
     256 are 1003 characters ending in "..."; silver holds longer text, for example item 256 ends after seven
     groups of renames).
   - The writer's report says the frame prints these cells in full; it does not. Drop "full".
   - The 51 "→" in the frame are NESO's own text, cut at that point: in silver the eight rows have 73.

3. **nit** `page.record.fields.notes`: "item 241's reschedules it, its description unchanged" does not parse.
   - Silver: note "Has been rescheduled for 19/10/2026", description "will be updated on 15th October 2026".
   - Suggest "item 241's note moves it to 19 October; its description still says 15 October".

4. **nit** `page.chart_view.key[planned].note`: "item 189's window opened 9 January 2026".
   - Silver 189: `change_datetime_from` 2026-01-09 11:00Z, no `change_datetime_to`, `last_updated` 2026-01-09 11:10Z.
   - NESO's dictionary calls From the time the issue "will occur"; it never calls it an opened window.
   - Suggest "item 189's start time is 9 January 2026". The page rightly never says why it is still Planned or
     that it is resolved.

5. **nit** `page.related[0..3].note`: present tense "rename" and "renames".
   - NESO's text says "will be updated on" a date.
   - Items 239 and 243 are Deployed; 241, 255 and 256 are Planned. One tense for all is loose.
   - Suggest "announce renames of ..." or give the status ("Item 239 (Deployed) ...").
   - The facts check out: 239 is the 2026-2027 arming file, 243 has four earlier arming files, 241 is AAHEDC, 255 has
     two column IDs ("Inertia (in MVA.s)", "Month & Year"), and 256 lists seven files.

6. **nit** note body, now stale after the second capture:
   - Line 231, "For the one capture held, that is 2026-10-08T09:43:34.968862Z", is wrong with two captures held.
   - Lines 243 to 244 ("The capture has 241 ... 1..241") and 366 ("Range 1..241 in this capture") read as current.
   - Line 260 is labelled "in the 2026-10-08 capture" and is fine.
   - Smallest edit: line 231 ("the two captures held are ..."); add "in the 2026-10-08 capture" to 243 and 366.

## Verified, no finding

- **Chart**
  - Polars over silver on the 16 October capture (`published_at` 2026-10-16 13:34:40.735778, 246 rows, dedup on `po`
    drops 0): Deployed 214, Cancelled 25, Planned 4, Postponed 2, "Deployed on the test link provided" 1. These match
    the committed series (`spec_origin: vault`, `rows_used` 246, `rows_read` 487), the alt text and notebook cell 3.
  - NESO's five values are kept apart. The bar label "Test link" is the writer's short form, and the key beside
    it gives NESO's full value.
  - The title and caption date it to NESO's 16 October 2026 file and say statuses are edited in place.
  - The filter pins the capture day; dedup set.
  - Palette: all petrol, nothing khaki, nothing summed.
- **Captures**
  - 8 October: `published_at` 09:43:34, 241 rows, items 1 to 241.
  - 16 October: 13:34:40, 246 rows, items 1 to 244 plus 255 and 256; the gap is 245 to 254 (notebook cell 5 agrees).
  - Items 1 to 238 identical in every vendor column.
  - 239 and 240 moved from Planned to Deployed, each with a new `last_updated`.
  - 241 moved from 15 October to 19 October 11:00 with the note.
  - 242 to 244, 255 and 256 are new. The manifest's "241 rows" is the 8 October file; the page says 16 October throughout.
- **Key notes**
  - Planned = 189, 241, 255, 256 (silver). Postponed = 14 and 48, from 2021-04-16 and 2022-01-22. Test link = item 72,
    "Prototype testing", from 2022-01-16.
  - Item 31 ("SOP dataset is being updated manually") is Deployed. Its description says "working to implement a fix", and
    the page does not call it resolved.
  - No issue is called resolved anywhere on the page.
- **Defect (item 256)**
  - The raw 16 October CSV holds bytes `C3 82 C2 A3` once, and silver, the sample and the frame show `Â£` as published.
  - It is stated in the note's Known issues bullet (body, the "Mojibake in NESO's text" bullet). The page's Known issues
    section is not rendered by the template, so the page shows it only in the frame and does not state it. Not a
    finding; a seat decision if a line is wanted.
- **Row, key, guide**
  - The key `[po, published_at]` matches the registry (`entity_key [po]`, `latest whole_capture`, `temporal none`, vintage
    `ckan_last_modified`).
  - "Unique in each file" is enforced in code: `silver/neso_data_portal/casting.py:582` rejects a capture with duplicate keys.
  - The guide covers all 14 non-lineage columns; precedent for `bronze_capture_id` and `capture_written_at` exists on approved pages.
  - The frame cells equal silver except for the 1,000-character cut and one trailing space trimmed on item 256's `dataset_specific`.
- **Notebook**
  - It uses `data.sql()` on `silver_neso_data_portal_portal_known_issues_latest`.
  - It was written by `scripts/run_notebooks.py`: 4 cells after the help card, no errors.
  - Times print in UK time (item 14 shows `13:00+01:00` for 12:00Z).
  - The plot alt (5/36/26/33/44/38/59, five with no start) matches Polars on `change_datetime_from.dt.year`.
  - `cells_sha256` is present.
- **Other facts**
  - `config/sources.yaml:1025` is the `portal_known_issues` row, `schedule: "daily"`.
  - The `request_url` pattern, package id and the 16 October file name match the sidecar.
  - The quote "upcoming changes to the NESO Data Portal along with any known issues" is inside the package description in the note body.
  - UTC for From, To and Last_Updated is from the dictionary and registry.
  - History 19 November 2020 matches the note.
- **Mirror and note**
  - Mirror `cmp` is equal.
  - The vault diff against `origin/master` is `page:` block, `updated`, the line-number fix (`:1021` to `:1025`, correct) and two Known-issues bullets.
  - Line endings: the working tree is CRLF on all 526 lines, the git index LF; this is the normal Windows checkout, not a finding.
- **Build, detector, copy**
  - `gridflow-build --only neso_data_portal/portal_known_issues` succeeds (the 37-line caveat-grammar warning is the build-wide notice).
  - Detector `[]`.
  - 0 em or en dashes, 0 middle dots.
  - All 51 "→" sit inside the frame, in NESO's text. There are none in the writer's own copy, which is what rubric 6 targets.
  - No planning labels, no "live", no "locally".
- **Layout** (headless preview on port 9971, PID recorded, stopped by PID)
  - At 390, 768 and 1440 the document has no horizontal overflow (`scrollWidth` 390 at 390, 753 at 768) and no element
    sticks out of the viewport. At 1024 I did not re-measure, but the page is fluid between 768 and 1440.
  - The folded frame, unfolded frame (a 20,564 px scroller inside its own box), chart, key and guide are all fully visible.
  - Multi-line cells (item 240's 20 datasets) print on one line in the frame.
  - Template items, not findings: the unfolded frame is very wide, and the notebook file tab "portal_known_issues.ipynb"
    is ellipsised at 390 (227 px text in a 207 px tab).

## Round 2

Checker, 2026-10-24. Rebuilt with `--only neso_data_portal/portal_known_issues`: success. Mirror `cmp` equal. Detector `[]`.
Built page: 0 em or en dashes, 0 middle dots, 51 "→" (all still NESO's text in the frame). Series, sample and notebook
untouched (digest checks pass). Checked the built page text and the note; no layout change, so no server was started.

Verdict: **APPROVE** (no finding above nit).

1. **Fixed** (was major). `what_it_is` now reads "items 239 and 240 are Planned in gridflow's capture of NESO's 8 October
   2026 file, Deployed in NESO's 16 October file". The chart caption says NESO "publishes only its current file, so
   gridflow's captures of other files may count differently" (supported by the note body, line 299). `how_used[2]` is
   "Compare gridflow's captures item by item". The page no longer implies the reader can fetch the 8 October file.
2. **Fixed.** Guide for `description`: "NESO's text of the change or issue; the frame cuts it at 1,000 characters". Matches
   the sample (rows 242, 243, 244 and 256 are 1,003 characters ending "...").
3. **Fixed.** Guide for `notes`: "NESO's note: item 241's moves it to 19 October; its description says 15 October". It parses
   now and matches silver. "item 241's" is still terse (nit, not worth another round).
4. **Fixed.** "item 189's start time is 9 January 2026" (silver `change_datetime_from` 2026-01-09 11:00Z).
5. **Fixed.** Related notes give NESO's status: 239 and 243 "both Deployed, renamed"; 241, 255 and 256 "(Planned) announces".
   Statuses match silver. All 12 words or fewer.
6. **Fixed, one residual nit.** Line 231 now covers both captures; the Key paragraph and the `po` schema row say "2026-10-08
   capture". Residual: the Event-time bullet (line 236) still gives only the 2026-10-08 `written_at` as "the gridflow capture
   time". It is an example, not wrong, and it is not on the page. Optional.

No new findings. Nothing in the changed wording introduces a claim silver contradicts.
