# Quick Reserve requirement forecast: checker review

Package `quick-reserve-auction-requirement-forecast` (table `qr_auction_requirement_fc`). Checker, 2026-10-18.

## Verdict: APPROVE

0 blockers, 0 majors, 2 nits. Both nits are wording; neither is a wrong statement.

## What I checked and how

- **Build and detector.** `gridflow-build --only neso_data_portal/qr_auction_requirement_fc`: exit 0, page written (the
  3 dropped "Known issues" lines warning is the known one). Detector `--json` on the built page: `[]`. No em or en
  dashes, middle dots or arrows in the page text; no "locally", "live", "now", planning words. `cmp` canonical note
  against the mirror: identical. Vault diff against `origin/master`: the `page:` block, `updated`, and two inserted body
  sentences only; no existing sentence changed.
- **Silver (1,874 rows, one capture).** 1,874 distinct `(auction_date, service_window)`. `service_delivery_date` is
  `auction_date` + 1 day on every row. 38 days x 48 windows plus 25 October with 50 (`5x`, `6x`). Two production dates:
  2026-08-31 for service days 23 to 30 September (384 rows, 8 days) and 2026-09-22 for 1 to 31 October (1,490 rows, 31
  days). `published_at` is the single value 2026-09-22 14:48:27.491459 UTC, equal to the sidecar's CKAN `last_modified`.
- **Chart (1 October 2026).** Series file: 48 points, x from 23:00 (30 Sept) to 22:30, positive 500 in window 1, 300 for
  the 12 points 23:30 to 05:00, 500 from 05:30; negative 300 in all 48. Reproduced from silver (rows for service day 1
  October; windows 1 to 48 with the start labels as written). The axis label reads "window start, UK local time as
  written"; the caption says "on the UK clock as NESO writes it"; the alt text says UK local time. The `Z` on the series
  file's x values is the known seat item; the drawn labels are the local labels. Rendered at 1440 and a 390 px iframe:
  correct shape, nothing clipped.
- **"The same on every day in this file."** True. Scanned every service day in silver: window numbers 2 to 13 are 300 MW
  and every other window is 500 MW on all 39 days (0 exceptions), under both production dates; negative is 300 MW on all
  1,874 rows. Notebook cell 4 shows only the pairs 500/300 (1,404 rows) and 300/300 (470 rows); cell 5 shows the 300 MW
  run starting at window 2 and ending at window 13 on 38 days, with 14 windows on 25 October (`5x`, `6x` added). 38 x 12
  + 14 = 470. The claim is scoped to "this file" and states no vendor rule.
- **What one row is and issue time.** The page says one row per auction date and half-hour window, 48 on an ordinary
  day. It never calls `published_at` an issue time (field line: NESO's last-modified for the whole file, read as UTC;
  the how-used line says each capture is one vintage stamped with it). `forecast_produced_on` is described as a date
  only, not a publication time, which matches the registry (`dtype date`, `issue: none`). The two production dates
  appear only in the frame and the notebook output (and "produced on different dates" in the caption); nothing on the
  page says whether NESO replaces or appends at its monthly update. The note body keeps its own `TODO: verify` on that.
- **`timestamp_utc` line.** Silver: 1 October gives 2026-09-30 23:00 UTC; 25 October gives 2026-10-24 23:00 UTC; one
  value per day. Window 1 starts an hour earlier in UTC in both summer and winter. True.
- **Clock-change windows.** 25 October in the bronze file: windows 5 and 6 read 01:00 and 01:30, then `5x` and `6x`
  repeat 01:00 and 01:30, then 7 at 02:00. NESO's field comment (snapshot `20261008T114228Z`) says `7x` and `8x` are
  the repeated hour at the GMT to BST change and that the BST to GMT day has no window 5 or 6. The file contradicts
  that, so "unlike NESO's dictionary" is true (see nit 1 for its plainness).
- **Related, Slow Reserve.** Registry JSON for the two packages differs only in the product word in the two MW column
  names, `Service window` versus `Service Window` Start Time, package ids and resource ids; entity key, temporal recipe,
  `latest` and `vintage` are identical. I also read the Slow Reserve silver: same eight columns, 1,874 rows distinct on
  the same key, day-first local labels, `5x`, `6x` on 25 October, `date_sp1` UTC midnight pattern. So the related
  line, and the body sentence ("same eight-column layout, key, clocks and temporal recipe"), hold; the body cites the
  registry only, and "clocks" is established by the silver, not the registry, which I confirmed here.
- **Other claims.** Catalogue snapshot: `Update frequency: Monthly`, "daily auction at 14:00", delivery "between 23:00
  and 23:00 D+1", one resource, no archive. MW unit from the dictionary. UK-local reading against EAC: joining the
  requirement to cleared `PQR` on `delivery_start` fits better read as UK local (mean absolute gap 46.6 MW over 1,968
  windows) than as UTC (61.6 MW); `NQR` is a tie (38.4 vs 38.4). The weak separation is expected because cleared volume
  is not the requirement; the page's UK-local statement rests on NESO's "local time" comment and the 25 October
  repeats, not on this join, and makes no matching claim. `date_columns.py` maps `service_delivery_date` to DATE as the
  notebook lead needs.
- **Responsive.** 1440 and 390 px viewed section by section; 390 px frame has no horizontal overflow. 1024 and 768 are
  the known folded-frame and notebook items.

## Findings

1. **Nit.** `record.fields.service_window` ("Window `1` to `48`; autumn clock change adds `5x`, `6x`, unlike NESO's
   dictionary"). Accurate, but a reader cannot tell what NESO's dictionary says, and "adds" has no stated baseline.
   Evidence: dictionary comment is "service window 7x and 8x are the repeated hour" at GMT to BST and "no service window
   5 or 6" on the BST to GMT day, while the file's 25 October has 5, 6, `5x`, `6x`. Suggested wording: "Window `1` to
   `48`; on the autumn clock-change day the repeated hour is `5x`, `6x` (NESO's dictionary says otherwise)". Optional.
2. **Nit.** `chart_view.key[0].note` ("300 MW from 23:30 to 05:30, 500 MW otherwise"). Read as inclusive, the window
   starting 05:30 is 500 MW, not 300; the 300 MW windows end at 05:29. The alt text is exact ("to the window starting
   05:00 ... 500 MW from 05:30"). Suggested: "300 MW from 23:30 until 05:30" or "300 MW for the windows starting 23:30 to
   05:00". Optional.

## Housekeeping

I started a throwaway static server on 9965 and stopped it; I did not touch 9670. I wrote a temporary one-line iframe
HTML file into the front-end worktree's `site/hifi` for the 390 px view and deleted it straight away (it was never
tracked). Scratch files are under the scratchpad `qr-checker\`.
