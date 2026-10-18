# Static FFR requirement: review (checker, 2026-10-18)

Verdict: **APPROVE** (no blocker or major; 4 nits, all optional wording or formatting).

Counts: blockers 0, majors 0, nits 4.

## What was checked and held up

- Build `--only neso_data_portal/sffr_requirement` succeeds (only the known 3-dropped-caveat-lines warning). Detector `[]`. Mirror `cmp`
  equal to the vault note. Vault diff against `origin/master` is the `page:` block, `updated`, and one inserted body sentence. Built page:
  0 em or en dashes, middle dots or arrows; no planning words, no local-data references.
- Silver (Polars, read only): 39 rows, 39 distinct `efa_date`, 2026-09-23 to 2026-10-31, every step one day, `service` = `SFFR` on
  all 39, one `published_at` (2026-09-22 14:48:22.737387 UTC, equal to the sidecar `ckan_last_modified`). `efa1` to `efa6` each hold
  only 250.0, 0 nulls (234 values). Bronze CSV: one capture, header `EFA_DATE,Service,EFA1..EFA6`, 39 data rows, 1,650 bytes, sha matches
  the sidecar. So "every block on every date in the file is 250 MW", scoped to the file, is true; no trend implied, no vendor rule
  drawn from one file. Series JSON: 1 series (SFFR), 39 values, all 250.0, 39 of 39 rows used. Alt, caption, key note and notebook
  `plot_alt` agree.
- Block times (focus 2): NESO's field dictionary (`field-info/20261008T114228Z/sffr_requirement.json`) gives unit MW, "requirement
  (before overholding)", and the `EFA_DATE` comment "starts at 23:00 D-1 running through to 23:00". NESO's SFFR auction results
  (`sffr_auction_results_main`, newest capture published 2026-10-16, 231,369 rows against 229,631 in the 2026-10-08 capture, so not
  truncated) label `efa` 1 to 6 as 23:00 to 03:00, 03:00 to 07:00, 07:00 to 11:00, 11:00 to 15:00, 15:00 to 19:00, 19:00 to 23:00,
  one pair of labels per `efa` across all 231,369 rows; `efa` 1 starts on `date` minus one day and 2 to 6 on `date`. On 2025-03-30,
  2025-10-26, 2026-03-29 and 2026-09-23 the labels are the same wall-clock times (naive strings, so UK local wall clock). The new body
  sentence is accurate in every particular, including the three clock-change dates and the capture date. "Block 1 lasts 3 or 5 hours at
  clock changes" follows from those wall-clock blocks (23:00 BST to 03:00 GMT = 5 h; 23:00 GMT to 03:00 BST = 3 h); notebook cell 5
  shows 25 October block 1 from 2026-10-24 22:00 UTC, 5.0 h, other blocks 4.0 h. Same wording as the approved DM and DR pages.
- `timestamp_utc`: silver gives 2026-09-23 -> 2026-09-22 23:00 UTC, 2026-10-24 -> 23 Oct 23:00, 2026-10-25 -> 24 Oct 23:00,
  2026-10-26 and later -> 00:00 UTC. The record caption ("from 26 October ... 00:00 UTC, not 23:00") matches the eight sample rows
  (26, 27, 30, 31 October at 00:00). "Block 1 starts an hour earlier" is true on both sides of the change. `published_at` is described
  only as NESO's last-modified time read as UTC; "issue" appears nowhere.
- How-used join (focus 3): `sffr_auction_results_main` carries `date` (the EFA date, as above), `efa` (Int64, 1 to 6), `accepted_volume`
  (MW), `clearing_price`, `status` (Accepted/Rejected), `service` SFFR. So "join on EFA date and block number" is true, and
  not on `timestamp_utc` is right (the requirement's `timestamp_utc` is UK midnight of the date, not a block start). The related-dataset
  note ("Cleared SFFR MW and clearing price for each EFA date and block") is true (one clearing price per date and block seen on 2026-10-01).
- Catalogue facts: package notes "forecasted requirements for Static Firm Frequency Response", update frequency Monthly, one resource
  titled "Static Firm Frequency Response Requirement" (sidecar `resource_name` matches), sibling package says "results from daily
  auction for static FFR". Raw-feed URLs equal the sidecar `request_url`; commands and "dates select nothing" match the approved pages.
- Consistency with approved DM and DR pages (focus 4): same structure and wording for `what_it_is` clock sentence, the flat-values
  sentence in caption, key note and alt, `published_at` as last-modified time, point-in-time bullet, raw-feed note, related layout. The
  file's own title is named once, as the DM review asked. Differences are justified (one service so key `efa_date`; join by `date`/`efa`
  because the counterpart is the SFFR results, not EAC).
- Notebook: `data.sql` on `silver_neso_data_portal_sffr_requirement_latest`; six cells, outputs real, no errors; cell 3 first/last/39/
  published UTC, cell 4 250/250/39 per block, cell 5 as above; PNG step plot at 250 matches `plot_alt`.
- Screenshots at 1440, 768 and a true 390 px iframe (1024 via the same template): hero, chart and key, raw feed, frame and guide,
  notebook panel, related: nothing clipped or overlapping. At 768 and 390 the folded frame shows fewer columns (known template item).

## Findings

1. **nit** Vault note body, the inserted sentence in the Clocks paragraph. The new lines start at column 0 while the surrounding
   paragraph is indented two spaces, so the sentence is lazily continued but visually breaks the list item. Re-indent the four lines by
   two spaces. Evidence: `git diff origin/master` lines `same six blocks: ...` to `2026-10-16, read 2026-10-18). The date format ...`.
2. **nit** Vault note body, same paragraph. The `TODO: verify` still says the boundaries are unverified against NESO's EAC guidance,
   immediately followed by a sentence that confirms them from NESO's own auction labels. Not wrong, but a reader may take the page's
   firm block times as unsupported. Consider "(EAC guidance itself not read)" after the new sentence, or leave as is.
3. **nit** `page.record.fields.timestamp_utc`. "UK midnight starting calendar date `efa_date`, in UTC" is clumsy and, as in the DM
   review, can be read as the start of the EFA day, which the page puts at 23:00 the evening before. Suggest "UK midnight at the start
   of the calendar date `efa_date`, in UTC; block 1 starts an hour earlier". Silver agrees with either wording.
4. **nit** `page.how_used[1]`. The requirement is one row per date with `efa1` to `efa6` columns, while the auction results carry the block
   as a number in `efa`; the join needs the six columns unpivoted to a block number, which the notebook cell 4 shows but the bullet does
   not say. Optional: "Join those results on EFA date and block number (`efa`), not on `timestamp_utc`." Not a factual error.

## Not findings

- Flat single-line chart: follows the seat ruling for flat requirement files, said plainly.
- Folded-frame hiding `timestamp_utc` at 768 and 390, notebook name-wrapping, runner's blank leading column: seat items in the batch file.
- Report-only figure (accepted volume per block of 114.4 to 256.2 MW against 250): not on the page; plausible (2026-10-01 blocks 163 to 242 MW).
- Gridflow or data defects: none found. The requirement table has a single complete capture. The auction results' newest capture is
  larger than the older one, so the truncated-capture risk does not apply here. The writer's note that the auction results'
  `delivery_start` and `delivery_end` are naive local wall-clock strings is correct (observed above) and belongs to that page's review.
- Server on 9968 started and stopped (connection now refused); 9670 untouched; no file written except this review and scratch files.
