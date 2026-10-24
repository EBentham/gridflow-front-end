# Data Portal changes and known issues: author report, round 2

Writer, 2026-10-24. Answers `data-portal-planned-changes-known-issues-review.md` (1 major, 5 nits) under the seat's
rulings. All six are fixed.

## Status

- `gridflow-build --only neso_data_portal/portal_known_issues`: success, on the first try. The only warning is the
  build-wide caveat-grammar notice.
- Detector `[]`. 0 em dashes and 0 en dashes in the built page.
- Canonical note: 527 lines, 527 CR. Mirror copied; `cmp` equal.
- Series, sample and notebook are unchanged: the chart spec, `record.select` and the cells were not touched, and the
  digest checks pass. No new screenshots: every change rewords prose in sections already checked at all four widths.

## Fixes

1. **Major: the 8 October file (seat ruling 1).** Each change says the 8 October file is known only through
   gridflow's capture. Silver shows the claim (both captures; the checker confirmed it).
   - `what_it_is`: "items 239 and 240 are Planned in gridflow's capture of NESO's 8 October 2026 file, Deployed in
     NESO's 16 October file." It stays within 60 words: "Each item gives a title, a description, the datasets
     and files it touches" became "Items give a title, description, affected datasets and files".
   - `chart_view.caption`: "NESO edits statuses in place and publishes only its current file, so gridflow's captures
     of other files may count differently." (40 words in total.) "Publishes only its current file" is in the note
     body: "Only the current register is published".
   - `how_used[2]`: "Compare gridflow's captures item by item; NESO does not say numbers are permanent".
2. **Nit: `record.fields.description`.** It now reads "NESO's text of the change or issue; the frame cuts it at 1,000
   characters". The committed sample has rows 242, 243, 244 and 256 at 1,003 characters ending "...". The others are
   shorter and whole.
3. **Nit: `record.fields.notes`.** It now reads "NESO's note: item 241's moves it to 19 October; its description says
   15 October". This matches silver: the note is "Has been rescheduled for 19/10/2026" and the description says "15th
   October 2026".
4. **Nit: `chart_view.key[planned].note`.** "window opened" is now "item 189's start time is 9 January 2026". Silver
   `change_datetime_from` is 2026-01-09 11:00Z.
5. **Nit: related notes.** Each now gives NESO's status from the 16 October file:
   - "Items 239 and 243, both Deployed, renamed its arming files' column IDs"
   - "Item 241 (Planned) announces column ID renames, moved to 19 October"
   - "Item 256 (Planned) announces column ID renames in seven tariff files"
   - "Item 255 (Planned) announces two column ID renames in its 2025/26 report"

   All are 12 words or fewer.
6. **Nit: note body, now stale after the second capture.**
   - Line 231: "For the one capture held" is now "For the two captures held". It gives both `last_modified` values
     (2026-10-08T09:43:34.968862Z and 2026-10-16T13:34:40.735778Z) and both fetch times.
   - The Key paragraph now opens with "The 2026-10-08 capture has 241 ...".
   - The `po` row of the silver schema reads "Range `1..241` in the 2026-10-08 capture".

## Defects

Unchanged from round 1:
- Item 256's double-encoded pound sign (vendor).
- Item 241's note and description disagree on the date (vendor).
- The batch file and ledger give 241 rows; that is the 8 October file, and the 16 October file has 246.
