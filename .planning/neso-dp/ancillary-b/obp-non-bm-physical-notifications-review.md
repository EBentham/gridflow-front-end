# Review: OBP non-BM physical notifications (checker, 2026-10-23)

**Verdict: REVISE** (0 blockers, 3 majors, 6 nits). The page's headline claims all reproduce from silver. The majors are one
wrong number and one wrong time range in the vault note and notebook, and body paragraphs the second capture made stale.

Gates run by me: `gridflow-build --only neso_data_portal/obp_physical_notifications` ok (digests pass, related pages resolve);
detector `[]`; `cmp` of note against mirror clean; vault diff 134 insertions, 9 deletions. Screenshots taken myself at 1440, 1024
(full page), 768 and 390 (chart and frame, no horizontal overflow: 768 and 390 scroll width equals client width): nothing
clipped or overlapping. My 9995 server is stopped; 9670 untouched.

## What I reproduced (no finding)

1. **De-duplication.** Silver has two files, 495,086 and 523,890 rows. Joining on `(unit_id, time_from)`: 0 earlier rows
   missing, 0 differences in `time_to`, `level_from`, `level_to`; 28,804 new rows, earliest start `2026-10-08 12:30:00`; 0
   duplicate keys inside each file; both start `2025-10-08 16:00:00`. The series artefact reports `files: 2, rows_read:
   1,018,976, duplicates_dropped: 144, rows_used: 144`: the 3 units x 48 buckets exist once each. The sample's eight rows all
   carry the 2026-10-16 capture's `published_at` and bronze path, and equal my deduped silver rows for `AFFR-1` 09:00 to 11:30.
   The notebook reads `_latest`: the output shows 48 windows per `GSET` unit (not 96) and 10 rows, not 20, for 29 March.
2. **Chart.** Rebuilt from silver (newest capture wins): 48 values per unit, equal to the committed series to 3 dp, same
   timestamps. Every window of the three units that day is 1,800 s with `level_from == level_to`; no bucket holds two rows.
   Every key-note and alt number matches (GSET-07 -17.0323 at 03:30, 04:00, 04:30, 14:00 to 15:30, -15.8229 at 13:30, 15.4355 at
   06:30, 15.0873 at 16:30, 15.9734 at 18:00, 12.4974 at 20:00; GSET-04 and GSET-02 as stated).
3. **Time zone.** Five units (`ENGQR-01`, `-02`, `-03`, `-05`, `ANSC-101`) have windows starting 01:00 and 01:30 on 29 March 2026
   (10 rows, all zero), contiguous. All five have the same single gap, 06:30 to 07:00 UTC, each running to 06:30 and resuming at
   07:00. The page states UTC as NESO's unit and offers the 29 March rows as the observation, which is scoped well enough (see
   nit 5). The notebook converts `time_from` and `time_to` to UTC in cell one and cell three. NESO's unit is "UTC" in the field
   info; the dictionary example ends in `Z`, the served cells do not.
4. **What a row is and the instructions link.** Dictionary wording matches ("Window Start Datetime", "PN at Gate Closure for
   window start time in MW", same for the end); `datastore_unique_keys` is `["Unit ID","Time From"]` with
   `datastore_append_or_update: true` in snapshot `20261006T195819Z`; no sign convention stated; levels -49.9 to 50 in both
   captures. The package notes point to the two sibling packages; the instructions dictionary reads "Power from PN in absolute
   values." The Unit ID description is word for word the instructions one. 21 of the 24 instructed units have PN rows (the three
   missing, `NGED-004`, `NGED-005`, `UKPN-002`, are the units with service `RDP`); all 60 availability units do.
5. **Rolling 12 months.** The page does not claim it. The note's Identity paragraph is corrected (pure append, both files start
   2025-10-08T16:00:00). Counts quoted in the new sentences check: 37 units with both signs, 51 all-zero (both levels), 37,502
   level jumps between contiguous windows, no window crosses a :00/:30 boundary, no overlap, 416,661 windows of 1,800 s in the
   newer capture.
6. **Service codes.** The page names none (only unit IDs). The body's `RDP` is used bare as the instructions' service id, not
   described as undecoded; nothing contradicts the Checked facts.
7. **Raw feed, commands, files.** Requests, `--last 24h` and "window must end recently" match `client.py` (48 h tolerance,
   line 130; check at 1543) and the approved instruction page. Sidecars confirm three file names and the two `ckan_last_modified`
   values; bronze line counts are header plus rows.

## Findings

1. **Major.** Vault note body, `Two clocks` item 1 (line 203) and `Known issues` first bullet (line 241): stale against the
   second capture the writer added. Line 203 says `published_at` and `available_at` are 2026-10-08T11:01:24Z "one value on all
   495,086 rows" and ends "(one capture exists)"; line 241 says "Every row carries 2026-10-08T11:01:24Z". Evidence: the newer
   silver file carries only `2026-10-16 20:31:22.674649 UTC` on all 523,890 rows (including the 495,086 rows that also sat in the
   first capture), and `_latest` returns that file, so through `_latest` no row is available before 2026-10-16T20:31:22Z. That
   is the point-in-time fact a backtester needs, and the note now contradicts itself (the Cadence paragraph says there are two
   captures). Fix: say the value is one per capture, give both, and say `_latest` carries the newer for every row, so an as-of
   query before it sees nothing; drop "(one capture exists)". Line 204 ("`capture_written_at` ... 2026-10-08T11:14:57Z carried on
   every row") needs the same treatment.
2. **Major.** Vault note `Typing` (line 156): "On 2025-10-26 (clocks back) the three units present each have 48 whole half-hours."
   Wrong. The three units (`EDFE-8`, `EDFE-11`, `EDFE-21`) have 119, 50 and 95 windows that day, of which 6, 47 and 15 are 1,800
   s; what is true is that each unit's windows cover exactly 24 h (86,400 s, 2025-10-26 00:00 to 2025-10-27 00:00 UTC). Reword to
   that (it still fits UTC and cannot exclude local time alone, as the note says).
3. **Major.** `page.notebook.plot_alt`: "GSET-07 changes only at half-hour starts, from -17.03 (03:30 to 04:30, 14:00 to 15:30) up to
   15.97 at 18:00." The plot draws each window from start to end (`-6.png`, x label "window start and end"): the -17.03 blocks
   run 03:30 to 05:00 and 14:00 to 16:00 (the last windows start 04:30 and 15:30 and end 30 minutes later). The "to 04:30 /
   15:30" ranges are window starts, which suits the line chart but misdescribes this plot. Fix: "03:30 to 05:00, 14:00 to 16:00"
   (and keep 15.97 at 18:00, its window being 18:00 to 18:30). The rest of the alt is right (AFFR-1 levels -4, -2, 0, 2 only).
4. **Nit.** `page.how_used[0]` "declared MW profile, minute by minute": windows run 60 s to 1,800 s and 416,661 of 523,890 are
   a half-hour, so a reader will expect one value per minute. Suggest "in windows of one to thirty minutes" (the one to thirty is
   from this capture; or "in windows, down to a minute").
5. **Nit.** `page.what_it_is`: "the text has no zone marker but holds 01:00 on 29 March 2026, which UK clocks skipped" reads as
   proof of UTC for the whole file; it only rules out UK local time on that day (the writer's own Unverified list says so).
   Suggest "so it is not UK local time, at least on that day".
6. **Nit.** `page.related[0].note` and `how_used[2]` drop the end of NESO's phrase: the dictionary says "Power from PN in absolute
   values." On a page that says NESO states no sign, leaving out "in absolute values" hides the one hint NESO gives about
   how the instruction target relates to the signed PN. Suggest quoting it in full where there is room (the related note has
   a 12 word budget; it is at 11, so "target MW as power from PN in absolute values" needs trimming elsewhere).
7. **Nit.** `page.notebook.lead`: "UK time here" has no referent on a public page; the sibling page says "UK time on UK machines".
8. **Nit.** Chart key: label and code are both `GSET-07` etc, so the legend shows the name twice ("GSET-07 GSET-07"). Drop
   `codes` or give a fuller label.
9. **Nit.** Vault note leftovers beside the writer's edits: line 216 TODO still says "the rolling window length" (the page-check
   shows growth, not a window; say "whether old rows are ever dropped"); lines 146 and 243 quote "400,690 ... 1,800 s" (first capture)
   next to sentences dated 2026-10-16 (second capture has 416,661), and the zero and negative counts in the Sentinels paragraph
   (407,637, 42,083) are undated first-capture figures; date them "(2026-10-08 capture)".

## Public copy greps

No em or en dashes, arrows or middle dots in the page prose; none of live, now, yet, soon, planned, shipped, locally, held, ledger,
"our ", "since 20", "% of". No local counts on the page: the 29 March and 21 September values are visible in notebook outputs, the
chart and the frame.
