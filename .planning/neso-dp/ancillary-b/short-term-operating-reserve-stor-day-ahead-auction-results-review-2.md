# Review 2: STOR day-ahead auction results (`stor_da_auction_results`)

**Verdict: APPROVE** (all six round 1 findings fixed; no new findings).

Checked: build `--only neso_data_portal/stor_da_auction_results` exit 0; detector `[]`; mirror `cmp` identical to the
vault note; 0 em dashes on the page; notebook JSON re-run by `scripts/run_notebooks.py`, cell outputs have no errors;
page viewed at 1024 and 390 on my own preview server (port 9998, started with its PID recorded, stopped by that PID,
confirmed down): hero facts, prose and caption wrap cleanly, no horizontal scroll at 390.

## Round 1 findings

1. **major, "every" overclaim: fixed.** `summary` now "The tenders in NESO's daily ... auction"; `facts.vendor` "the daily
   STOR auction results"; `facts.history` "Service days 1 April 2021 to 31 March 2026; NESO's file lacks four";
   `what_it_is` ends "NESO's file has no rows for four service days and none accepted on five; NESO's notices report
   two failed auctions"; `plot_alt` "the line breaks where nothing was accepted or NESO's file has no rows"; the
   notices related note says "two explain gaps in these results". The dropped "NESO ended the auction after launching
   Slow Reserve" sentence is still carried by the EAC related note and the cadence line, so nothing is lost.
2. **nit, caption: fixed.** "each service day's clearing price, the same on every accepted tender that day in NESO's
   file": measured and scoped to the file; notebook cell 4 shows it (1,817 of 1,817, which I reproduced).
3. **nit, UTC start: fixed.** "UTC with NESO's `Z`: 05:00 UK time, so 04:00Z in summer" (checked: months 4 to 9 all 04:00Z).
4. **nit, cadence: fixed.** "Daily; last auction 30 March 2026, for delivery 31 March; package Not Active (NESO)". The last
   file row is delivery 31 March 2026 (TRN-3557), file last modified 30 March 04:28Z.
5. **nit, plot_alt basis: fixed.** Medians on one basis for both periods (below).
6. **nit, related notices note: fixed.** "Mostly STOR auction delays and failures; ..." (6 of the 9 notices).

## New claims, re-derived (Polars on silver, notices file)

- **Notebook counts.** Page output: span 1,826; rows in file 1,822; accepted 1,817; one clearing price 1,817; clearing =
  dearest accepted 1,817. Mine: `date_range` 2021-04-01 to 2026-03-31 = 1,826; UK service days with rows 1,822; with an
  accepted tender 1,817. Four days absent (2 August 2022, 17 August 2022, 29 October 2023, 8 February 2025); five with
  none accepted (8 April, 5 July, 26 July 2021, 24 April 2022, 18 August 2024).
- **Medians.** Daily summed contracted MW: 1,453 days to 1 April 2025 median 1,312; 364 days from 2 April 2025 median
  1,696 (range 811 to 1,955); lowest 50 MW on 20 December 2021. All as in `plot_alt`.
- **18 August 2024.** Notice issued 2024-08-17 08:20Z, "STOR auction results failure", effective from 2024-08-18 04:00Z:
  "technical issue with today's auction resulting in no bids being accepted". The 18 August service day has 96 tenders,
  all Rejected.
- **8 February 2025.** Notice issued 2025-02-07 11:20Z: "technical issue with todays STOR auction resulting in no bids
  being accepted. There will be no replacement auction." The 8 February service day has no rows.
- **1,700 MW.** Notice issued 2025-04-01 08:00Z, "STOR requirements update", effective 2025-04-02 04:00Z: STOR day-ahead
  requirement "increased to 1700MW from the auction on 1 April 2025 (for delivery on 2 April 2025)". The median step
  sits at 2 April 2025 as `plot_alt` says; "when" is temporal and not over-claimed.

## Nothing new

Series and sample are unchanged (chart spec and record select untouched; build digest check passes). Template items
(no dark scheme, `.nb-tab` truncation, caveat-grammar warning) remain seat items. Defects: unchanged and already
logged by the writer (NESO file gaps); no gridflow defect.
