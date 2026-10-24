# Monthly operational metered wind output: checker's review (round 1)

Package page `monthly-operational-metered-wind-output`, table `metered_wind_output_monthly`. Checker port 9814 (server
started with its PID recorded and stopped by that PID).

**Verdict: APPROVE.** 0 blockers, 0 majors, 8 nits.

Gates run: `gridflow-build --only neso_data_portal/metered_wind_output_monthly` passes (the known "Known issues"
caveat-grammar warning only); detector `[]`; 0 em dashes, no arrows or middle dots, no "live", "locally", "held", "our"
in the page text; canonical note and mirror `cmp` identical; note diff against `origin/master` read in full (180 lines).
Screenshots at 1440, 1024, 768 and 390 (390 in a 390 px iframe, `--force-prefers-reduced-motion`); nothing clipped or
overlapping; I looked at 1440 and 390 in detail.

## What I reproduced

1. **The overlap is 1 to 5 April 2026, not August and September.** Silver, all captures: 193 keys appear twice, all in
   2026-04-01 to 2026-04-05 (last key 5 April P1), one row from the 2025-26 file (`7622b040`, `published_at`
   2026-04-07 10:00 UTC) and one from the 2026-27 file (`c9bc94c4`, 2026-10-03 11:17 UTC). The 2026-27 file is never
   lower: gap 0.0 to 70.874 MW, mean 31.29, median 31.54, 0 negative, 3 equal (2026-04-02 P11, P12, P18). Max is
   2026-04-03 P5 (01:00 UTC), min 2026-04-02 P11 (04:00 UTC): both match the plot alt. "M08/M09" are the note's file
   codes. ADR-040 (Context and Committed entries) and RULINGS 547 say exactly this: 193 keys, 2026-04-01 P1 to
   2026-04-05 P1, "NESO states no precedence, so both rows are served". The batch file's "August and September" is
   wrong; the writer is right. The page's statement is true and plain, with nit 1.
2. **Chart.** Rebuilt from silver with the spec (dedup on `[sett_date, sett_period]` keeping the latest
   `published_at`, window 2025-04-01 to 2026-09-30, daily mean): 548 days, every day a complete 46, 48 or 50 periods;
   series JSON equals my values to 3 decimals (max difference 0.0005). On 3 April the chart uses the 2026-27 value
   (13,918.85 total, not the 2025-26 one). Stacking is honest: the two regional means sum to the total mean on every
   day (max difference 4e-12), and 0 of 149,234 rows have `total` differing from the two regions by more than 1e-6.
   Alt numbers hold: min 881.35 on 2026-08-16, max 16,868.28 on 2026-03-25, England and Wales larger on 443 of 548 days,
   84 of 103 days above 12,000 fall between September 2025 and March 2026. The caption says "the mean of each
   settlement date's half-hours" and "the top edge is NESO's total". NESO's silence on average versus spot is stated
   once, on the `scottish_wind_output` guide line (nit 5). NESO's dictionary indeed says only "Operational Metered MW".
3. **3 October file and 16 October upload.** Bronze (read only): the 16 October capture is the 2026-2027 file at CKAN
   `last_modified` 2026-10-16T06:38:45, 387,247 bytes, 9,409 rows, to 2026-10-14 P1, 0 duplicate keys; header
   `England Wales Wind Output` against `England/Wales Wind Output` in the 3 October file. Its 8,785 keys shared with the
   3 October body are identical in all three columns (0 differences), so the April overlap is unaffected. Failure
   record `996658c4...json`: `HeaderEpochError`, message names the one epoch. Silver stops at 2026-10-01 P1 with
   `published_at` 2026-10-03. BACKLOG line 576 logs 20bp ("fresh install gets no 2026-27 rows", extends section 19).
   The page's coverage line is true.
4. **Row, units, frame, notebook.** Frame values equal silver exactly (eight rows, 1 April 2026 P1 to P4, both files).
   `timestamp_utc` P1 = 2026-03-31 23:00 UTC (GB midnight in BST). Notebook JSON written by `run_notebooks.py`,
   outputs match silver: 193 rows (2025-26, to 2026-04-04 23:00 UTC, which is 5 April P1) and 240 rows (2026-27), gap
   statistics as above; plot shows the stated shape. `query()`: inclusive `BETWEEN` on a DATE column, session-zone times
   (20r), `_latest` per `resource_id`. Raw feed: `package_show` URL and the resource download URLs match the bronze
   sidecars' `request_url`; "downloaded whole unless its `last_modified` is unchanged" matches `iter_members`
   (newest capture's `ckan_last_modified` equals the live value). Commands match the approved constraint-breakdown page.
   Vendor quote ("expected to be different to the data published as part of the wind forecasting metrics, as that data
   uses settlement metering") confirmed in the catalogue probe. 46 and 50 period days: 8 each in silver.

## Findings

1. **Nit** `page.what_it_is`, `page.chart_view.caption`: "both cover 1 to 5 April 2026" / "share 1 to 5 April 2026".
   The 2025-26 file reaches only the first half-hour of 5 April (193 keys = 4 days x 48 + P1); 5 April is otherwise
   covered by the 2026-27 file alone. Evidence: silver max `sett_date` of `7622b040` is 2026-04-05 with one period.
   Suggest "from 1 April to the first half-hour of 5 April 2026".
2. **Nit** `page.what_it_is`: "NESO's 16 October upload renamed a column, so this page stops at its 3 October file."
   True, but the "so" hides the actor: the page stops because gridflow's loader rejects the new header, not because NESO
   removed anything. One clause ("which gridflow's loader does not yet accept") would make it plain.
3. **Nit** `page.record.fields.sett_period`: "46 on spring and 50 on autumn clock-change days" omits the normal 48 (the
   rubric's known nit) and reads as a period number. Other pages say "1 to 48; 46 or 50 on clock-change days".
4. **Nit** `page.record.fields.timestamp_utc`: "GB midnight plus 30 minutes per period" reads as P1 = 00:30. The frame
   shows P1 at midnight (23:00 UTC in BST). Say "for each period after the first".
5. **Nit** `page.record.fields` and `page.chart_view.caption`: the "average or spot not stated" caveat sits only on
   `scottish_wind_output`. `england_wales_wind_output` and `total` carry none, and the chart caption says "mean of each
   settlement date's half-hours" without it. Evidence: NESO's dictionary (note, Units) is silent for all three.
6. **Nit** `page.related[2].note` (`wind-bmu-boa-volumes`): "Accepted bids and offers on wind BM units, for curtailed
   output" states more than the held note supports: the note says "Offer-Acceptances", the dictionary calls the value
   curtailed generation, and the 2026-27 sign contradicts that. Suggest "Balancing acceptances taken on wind BM units".
7. **Nit** `page.what_it_is`: the page never says NESO gives no precedence between the two files or that which is right is
   an open question to NESO (ADR-040 ledger question; note TODO). The chart caption states the page's own choice, which
   is honest, but one clause would let a reader see the choice is the page's, not NESO's.
8. **Nit** (canonical note body, not page copy) Cadence section: "TODO: verify whether any scheduler actually runs that
   daily capture" is now answered: the 16 October capture came from the first daily refresh (gridflow BACKLOG section 19,
   RULINGS 888). Also the notebook's `needs` ("2025-26 and 2026-27 yearly files ingested") will not reproduce on a fresh
   install until 20bp is fixed (a new ingest takes the 16 October file, which the transform rejects). Seat item, not a
   page fault; refresh page, chart window and notebook outputs when 20bp lands (and the ADR-040 ledger entry, R-1).

## Seat items (not findings)

- At 390 px the frame shows only `sett_period` and the fold marker; `resource_id` is behind "Show the folded columns"
  (writer's template note, confirmed).
- Headless Chrome needs `--force-prefers-reduced-motion` for the content below the chart to paint (confirmed).
- Scotland's hatch is dense at full window; legible at 1440 and 390, acceptable.
