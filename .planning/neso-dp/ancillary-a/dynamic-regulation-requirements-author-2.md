# Dynamic Regulation requirements: author report, round 2

Fixes for `dynamic-regulation-requirements-review.md` (2 majors, 4 nits), worded as the approved Dynamic Moderation page
words them. Writer, 2026-10-18.

## Status

- Canonical note edited with the Edit tool (258 lines, 258 CR); mirror copied, `cmp` equal.
- `gridflow-build --only neso_data_portal/dr_requirements`: exit 0. Detector: `[]`. Built page: 0 em or en dashes,
  middle dots, arrows; no `locally`, `our`, `now`, `live`.
- Artefacts unchanged: the chart spec, record select and notebook cells did not change (the digests pass), so no
  re-distil, re-sample or notebook run was needed.
- Looked at a true 390 px view of the changed text (what it is, caption, key notes, record caption): nothing clipped.
  My server on 9944 is stopped; 9670 untouched.

## Findings and fixes

1. **major, NESO's file title.** `what_it_is` now reads: "Dynamic Regulation is a NESO frequency response service, with
   a low (`DRL`) and a high (`DRH`) product. NESO's file, titled Indicative DR Requirements and called its latest view,
   gives MW before overholding per EFA date for six EFA blocks. Blocks run on the UK clock from 23:00 the evening
   before; block 1 lasts 3 or 5 hours at clock changes." (DM's shape; the title is the resource name in the sidecar.)
2. **major, every value 480 MW.** Caption ends "Every block on every date in the file is 480 MW." Key notes: DRH "480 MW
   in every block, all 39 dates in this file; the low line runs along it."; DRL "480 MW in every block on all 39 dates,
   drawn dashed over the high line." Alt adds "Every block on every date in the file is also 480 MW." Evidence: silver
   `efa1`..`efa6` unique values `[480.0]`, no nulls; notebook cell 4 gives min 480, max 480, count 234 per product. The
   caption was shortened to stay within 40 words ("NESO's 22 September file", "from 23:00 the evening before, UK time").
3. **nit, `efa1` and block 1 length.** `efa1`: "Block 1, 23:00 to 03:00 UK time, MW before overholding (NESO)". The 3 or 5 hour
   length moved to `what_it_is` in DM's words (the reviewer's longer wording ran over the 60-word budget).
4. **nit, notebook lead.** Now: "Reads the `_latest` view, the newest capture, with `data.sql` so the cells see every date
   the file holds and show `published_at` in UTC; `query()` reads the same view but takes a date range." (Both read
   `silver_neso_data_portal_dr_requirements_latest`; cell 1 casts `published_at` to UTC.)
5. **nit, `timestamp_utc` and record caption.** `timestamp_utc`: "UK midnight starting calendar date `efa_date`, in UTC;
   block 1 starts an hour earlier". Record caption: "First and last dates; around 25 October's clock change
   `timestamp_utc` goes from 23:00 to 00:00 UTC." (silver: 25 Oct 2026-10-24 23:00 UTC, 26 Oct 2026-10-26 00:00 UTC).
6. **nit, third use.** `how_used[2]`: "Point-in-time studies: each capture is one vintage, stamped with the file's
   `published_at`." (registry `latest: whole_capture`, `vintage: ckan_last_modified`).

Also aligned with DM: `facts.grain` says "service" for the row dimension, as DM does.

## Defects

None new. The template item from round 1 (the notebook runner's named-index header) stands for the seat.
