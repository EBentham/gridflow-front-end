# Writer report, round 2: `day-ahead-power-exchange-prices-nordpool` (table `nordpool_da_prices`)

Answers `day-ahead-power-exchange-prices-nordpool-review.md` (REVISE: 1 major, 4 nits). All five are fixed.

- I edited the canonical note `C:\gridflow-wt\vault-neso-trd\30-vendors\neso-data-portal\datasets\day-ahead-power-exchange-prices-nordpool.md`
  with the Edit tool, keeping CRLF. It is mirrored to `C:\gridflow-wt\fe-neso-trd\vault\neso_data_portal\` and `cmp`
  shows the two identical.
- The rebuild `--only neso_data_portal/nordpool_da_prices` is clean after one fix: the first try had the caption at 41
  words and I trimmed it to 40. The detector returns `[]` and the built page has 0 em dashes.
- The chart spec, the sample selection and the notebook cells are unchanged, so the committed artefacts are unchanged
  and their digests still pass.
- Per the coordinator, I started no server and took no new screenshots. The wording changes are short and replace text
  in the same places.

## Fixes

1. **Major, `page.how_used[2]` and `page.related[0].note` (elexon/mid).** I no longer call this series a check on the
   market index.
   - `how_used[2]` now reads "Compared with Elexon's half-hourly market index price, a different product."
   - `related[0].note` now reads "Elexon's half-hourly market index price: a different product, read side by side".
   - Grounds: `vault/elexon/mid.md` `what_it_is` says day-ahead auction trades carry no weight. The note's own
     cross-check found 6 exact matches in 43,679 joined hours, with a mean absolute difference of about 18.0 £/MWh.
2. **Nit, `page.chart_view.caption`.** "Each date runs 00:00 to 24:00 GMT." became "Each date carries 24 one-hour
   labels, which NESO gives as GMT." I left out the `00:00 - 01:00` to `23:00 - 00:00` codes the review suggested
   because they took the caption over 40 words. To stay within budget I also changed "captured on 16 October 2026" to
   "captured 16 October 2026".
3. **Nit, `page.how_used[1]` and `page.related[2].note`.** "continental" is now "ENTSO-E's European day-ahead prices"
   in both.
4. **Nit, `page.chart_view.alt`.** "105 in 2026" is now "105 in 2026 to 16 October".
5. **Nit, note body.** I dated each sentence that read as a single-capture fact and added the 16 October figures:
   - **Two clocks, point 1:** added the 16 October capture time `2026-10-16T20:42:05.239349Z` on all 44,472 rows. The
     CKAN `last_modified` now "precedes rows dated up to 2026-10-08 (2026-10-17 in the 16 October capture)".
   - **Two clocks, point 2:** `timestamp_utc` equals each capture's own time, one per capture, on every row of each.
   - **Delivery-period labels:** the 44,255 steps and the 1,845 dates are now dated to the 8 October capture. For the
     16 October capture: 44,471 steps, all 3,600 s; latest start 2026-10-17T21:00:00Z; 1,854 dates, 1,852 of them with
     24 rows, 2021-09-20 with 2 and 2026-10-17 with 22.
   - **Delivery before or after capture:** the "10 after" paragraph is now dated to the 8 October capture.
   - **Identity:** 44,256 distinct pairs in the 8 October capture and 44,472 in the 16 October one.
   - **Value range:** "both captures", with 1,845 dates and 1,854 dates respectively. The 591 negatives and 63 zeros
     are the same in both.
   - **Cadence:** the newest delivery date is now "2026-10-08, then 2026-10-17 in the 16 October capture, whose sidecar
     still records it".
   - Evidence for all of these: my round 1 Polars checks (`s1` to `s3` in `scratchpad\nordpool-writer\`), which the
     checker reproduced.

## Correction to my round 1 report (from the checker's observation)

Round 1 said both capture edges "fall on a UK-day boundary in summer time". That was wrong.
- The file starts at 2021-09-20 `22:00 - 23:00`, and both captures end at `21:00 - 22:00`. Read as GMT, both edges sit
  at 22:00 UTC. That is 23:00 BST, not a UK midnight; it is midnight CEST.
- So the edges look like a Nord Pool delivery-day boundary (a CET day) written in GMT labels. They are no evidence of
  UK days.
- This was only in the report and the page claims nothing from it. The rest of the case for reading `date` with GMT
  labels still stands: every step is one hour, there are 24 labels on every complete date, the dictionary titles the
  column "Delivery Period (GMT)", and the morning ramp falls one label earlier in summer.
- For the next vendor check: the note's DST bullet ("supports UTC intervals rather than a UK-local or CET/CEST clock")
  is about the labels. Day boundaries may still follow the CET delivery day. I did not change that sentence: the
  review raised it as an observation, not a finding.

## Defects

Unchanged from round 1. The missing date plus interval-label temporal recipe, which makes `query()` filter on capture
time, and NESO's stale CKAN `last_modified` on a growing file.
