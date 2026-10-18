# Dynamic Regulation requirements: review (checker, 2026-10-18)

Verdict: **REVISE** (no blocker; 2 majors, both wording the approved Dynamic Moderation page already carries; 4 nits).

Counts: blockers 0, majors 2, nits 4.

## What was checked and held up

- Build `--only neso_data_portal/dr_requirements` succeeds (the 3 dropped-caveat-lines warning is the known one). Detector `[]`.
  Mirror `cmp` equal to the vault note. Built page text has no em or en dashes, middle dots, arrows, "locally", "our", "now",
  "live", "since 20", local paths or planning words.
- Silver (read only, Polars): 78 rows, 39 EFA dates 2026-09-23 to 2026-10-31 with a one-day step throughout (no gap), `DRH` 39 and
  `DRL` 39, one `published_at` (2026-09-22 14:48:17.409242 UTC), one bronze capture. Every one of `efa1` to `efa6` holds only
  480.0 and has no nulls, so all 468 block values are 480 MW. Bronze CSV: 78 data rows, header `EFA_DATE,Service,EFA1..EFA6`,
  sidecar `ckan_last_modified` 2026-09-22T14:48:17.409242, resource name "Indicative DR Requirements".
- Series JSON: two series of 39 points, every value 480.0, x 2026-09-23 to 2026-10-31, `rows_used` 78, spec filter pins the file.
  Alt, key notes and notebook `plot_alt` agree on 480 MW and 39 dates. Samples file is the 8 rows shown.
- Render (zoomed at 1440): the clay low line is drawn dashed over the petrol high line, as the key notes and alt say. No trend is
  implied and no vendor rule is drawn from one file. Notebook step plot PNG matches its alt (solid petrol, dashed clay, flat 480).
- `timestamp_utc` (focus 2): silver gives 2026-09-22 23:00 UTC for 23 September, 2026-10-24 23:00 UTC for 25 October,
  2026-10-26 00:00 UTC for 26 October. UK clocks go back on 25 October 2026, so 25 October opens at 00:00 BST (23:00 UTC the day
  before) and 26 October at 00:00 GMT. The sample rows show exactly that, so "the clock-change date 25 October and the next" is
  accurate.
- `efa1` (focus 2): notebook cell 5 reproduces block starts from UK local to UTC. On 25 October block 1 starts 2026-10-24 22:00 UTC and
  lasts 5.0 h, blocks 2 to 6 start 03:00, 07:00, 11:00, 15:00, 19:00 UTC and last 4 h. Block 1 is 3 h on the spring change date by
  the same rule (EFA 1 from 23:00 the evening before to 03:00 UK time). The notebook's start-time arithmetic (`4n-5` hours from
  UK midnight, localised to Europe/London) is correct and has no ambiguous local times. The plot alt's span (22:00 on 22 September to
  19:00 on 31 October UTC) is right.
- Dictionary (focus 4): gridflow profile `field_info` for the family gives each `EFA1`..`EFA6` "Our requirement for the service
  (before overholding) for this EFA", unit MW; `Service` "DR-L = Dynamic Regulation Low / DR-H = Dynamic Regulation High"; the body holds
  `DRL` and `DRH`. The `service` line is accurate. `published_at` is described as NESO's last-modified time read as UTC, which matches
  the registry vintage and the sidecar; "issue" appears nowhere.
- Notebook (focus 3): run against the local warehouse with the gridflow_models interpreter, read only. `data.sql` on
  `silver_neso_data_portal_dr_requirements_latest` returns 78 rows, 2026-09-23 to 2026-10-31. `query("dr_requirements", ...)` maps to the
  same `_latest` view (`_RELATION_NAME_BY_DATASET`), returns 78 rows for 23 September to 31 October, 4 rows for 25 to 26 October, 0 for
  January to August 2026. The lead does say what is read (the `_latest` view, the newest capture) and cell outputs are real with no
  errors. See nit 4 on the stated reason.
- Raw feed: `request_url` matches the sidecar; `package_show?id=dynamic-regulation-requirements`; commands and "dates select nothing" match
  the approved BR and DM pages. Related links resolve (`eac-auction-results`, `dynamic-moderation-requirements`,
  `long-term-forecasts-for-dc-dm-dr-requirements`, `elexon/freq`).
- Screenshots at 1440, 768 and a true 390 px iframe: nothing clipped or overlapping in hero, chart, key, frame, guide or notebook panel.
  At 390 the folded frame shows only `efa_date`, `service`, `efa1`, `efa2` (known template item, not a finding).

## Findings

1. **major** `page.what_it_is` and `page.summary`. NESO's own title for this file is "Indicative DR Requirements" (resource name in the
   sidecar and in the note's file table; the note's overview says "NESO's indicative requirement"). The page never says NESO labels
   the figures indicative, which matters to anyone reading 480 MW as a firm requirement. The approved Dynamic Moderation page names its
   file title once ("NESO's file, titled Indicative DM Requirements and called its latest view"). Suggest the same here: "NESO's file,
   titled Indicative DR Requirements and called its latest view, ...".

2. **major** `page.chart_view.caption`, `page.chart_view.key[0].note`, `key[1].note`. The seat ruling asks the caption, key notes and
   alt to say plainly that every value in the file is 480 MW. The chart shows block 1 only. The caption says only "The two lines coincide"
   (no 480 MW, no dashed line); the key notes say 480 MW for the 39 dates but the only statement about the other blocks is "the rows show
   every block", which is vague and not quite true (the eight rows cover four dates, not all 39). Nowhere outside the unfolded
   frame and notebook cell 4 does the page say blocks 2 to 6 are also 480 MW on every date. The approved DM key note says "every block
   repeats on every date in this file". Suggest: DRH note "480 MW in every block on all 39 dates in this file; the low product's line
   runs along it." and DRL note "480 MW in every block on all 39 dates, drawn dashed over the high line."; add the same to the caption
   ("every block on every date in the file is 480 MW; the low line is dashed over the high one"). Evidence: Polars unique of each of
   `efa1`..`efa6` is `[480.0]`, 0 nulls.

3. **nit** `page.record.fields.efa1`, `page.what_it_is`. "spring change 3 hours, autumn 5" is terse (a reader can take "change" as a change
   of the requirement) and leaves off "before overholding" that `efa2` to `efa6` carry. DM (approved) states "block 1 lasts 3 or 5 hours at
   clock changes" in `what_it_is` and gives `efa1` the plain wording. Suggest `efa1`: "Block 1, 23:00 to 03:00 UK time, MW before
   overholding (NESO)" and, in `what_it_is`, "block 1 lasts 3 hours on the spring clock-change date and 5 on the autumn one". Facts are right
   (5.0 h reproduced in notebook cell 5).

4. **nit** `page.notebook.lead`. "NESO updates the file in place, so a dated `query()` on `efa_date` returns only the dates your capture
   holds" reads as a reason to prefer `data.sql`, but `data.sql` on `_latest` returns only the same dates, and `query()` reads the same
   view (verified above). The wording is the approved DM wording, so this is optional, but it is not the real contrast. What differs: `query()`
   needs a start and end date and shows timestamps in the session's UK time (`+01:00`), whereas the cell picks columns and shows `published_at`
   in UTC. Suggest "Reads the `_latest` view, the newest capture, with `data.sql` so the cells see every date the file holds and show
   `published_at` in UTC; `query()` reads the same view but takes a date range."

5. **nit** `page.record.fields.timestamp_utc`, `page.record.caption`. "UK midnight opening the EFA date" can be read as the start of the
   EFA day, which the page puts at 23:00 the evening before (the trailing "block 1 starts an hour earlier" rescues it but is easy to miss).
   DM's approved wording: "UK midnight starting calendar date `efa_date`, in UTC; block 1 starts an hour earlier". The record caption
   says which rows are shown but not what to look at; DM's says "around 25 October's clock change `timestamp_utc` goes from 23:00 to
   00:00 UTC". Suggest both.

6. **nit** `page.how_used[2]`. "Forward requirement per product and block as a feature for response price models" is a plausible use,
   not in the note (its overview says a forward-looking procurement-volume signal). DM's review flagged the same line and the approved DM
   page replaced it (point-in-time studies, each capture a vintage stamped with `published_at`). Same replacement fits here.

## Not findings

- The flat two-line chart is within the seat ruling once finding 2 is applied. `type: none` question: seat's call.
- The runner's stray header cell in grouped notebook tables, folded-frame width at 768 and 390 and long relation names wrapping: seat
  items in the batch file. Cell 3 and cell 4 output tables render without a visible stray column in the built page.
- Unverified-in-writer-report item (`DRL` as the low-frequency side): the page says only "low" and "high", as NESO's dictionary does.
  The note body's "low-frequency side" wording is not on the page.
- Gridflow or data defects: none found on this package (single capture, no truncation).
