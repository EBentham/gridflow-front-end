# 1-day-ahead-demand-forecast: checker's review

Family page `1-day-ahead-demand-forecast`, lead `demand_forecast_1d_day_ahead_national`, held member
`demand_forecast_1d_historic_day_ahead`. Checked 2026-10-24 in `C:\gridflow-wt\fe-neso-dem` against the canonical note in
`C:\gridflow-wt\vault-neso-dem`.

## Verdict: REVISE

One major (the page says the archive "keeps every day-ahead forecast since 2018"; the archive file itself does not
support that), three nits. The chart, the hold line, the capture counts, the notebook and the frame are right.

Gates I ran: `gridflow-build --only neso_data_portal/demand_forecast_1d_day_ahead_national` rewrote the page
byte-identical (`cmp` against the writer's copy); the only errors are the two orphan artefacts of another writer's tRESP
page. Detector `[]`. Mirror `cmp` clean with the vault note (505 of 505 lines CRLF). No staged chart spec and no authored
override for the dataset. Series `spec_origin: vault`, digest check passed. Zero em dashes in the page or the `page:` block.

## Findings

1. **major, `page.what_it_is` (also the note body intro, line 21 to 22 of the note, "the vendor's archive of every
   day-ahead forecast since 2018").** The page says "the archive keeps every day-ahead forecast since 2018" as its own
   fact. NESO's wording (catalogue snapshot `20261006T195819Z`, resource `9847e7bb`) is "All historic day ahead demand
   forecasts from 2018 to the most recent forecast"; the page drops the attribution and the file contradicts it:
   - In the 2026-10-16 archive capture, 23 consecutive target dates (25 Sep to 17 Oct) carry exactly one issue each, all
     stamped about 08:20 to 09:10 on the day before, although NESO publishes the current file twice daily. Over all
     3,210 target dates: 1,458 have one issue, 1,748 two, 4 three
     (`pl.col("forecast_timestamp").n_unique()` by `targetdate`).
   - For 17 October the archive's only issue (`2026-10-16T08:36:38Z`) differs from the current file's midday values on
     all 12 points (differences 1 to 103 MW; windows identical). I reproduced this.
   - The writer's own "Unverified" section says whether the archive keeps the midday publication is unsettled, so the
     page should not assert it, and it is the claim a reader would lean on when benchmarking against the archive.
   Fix: "NESO describes the archive as all day-ahead forecasts from 2018" (what_it_is), and the same softening in the
   note intro. `facts.history` ("holds day-ahead forecasts from 2018") and the member `differs` ("every day-ahead forecast
   NESO has kept") are fine as written. This wording will be copied to the three sibling pages, so fix it here first.

2. **nit, `page.chart_view.caption`.** "in the file last changed at 11:00 UTC on 16 October" states the zone as fact. CKAN
   emits the stamp without an offset and gridflow reads it as UTC (ADR-030); the column guide correctly says "read as
   UTC". Say "stamped 11:00 UTC" or "read as UTC" to match.

3. **nit, `page.record.fields.cardinalpoint`.** "its sample curve image shows where each sits" points at a PNG the page
   neither shows nor links, so the reader cannot follow it. NESO's dictionary explains the concept but lists no codes.
   Either say so ("NESO does not list the codes") or drop the image reference.

4. **nit, note body "CP clock zone conflict" paragraph.** "the current file then held the midday publication" is an
   inference from the 11:00:01 UTC stamp falling in NESO's 12:00 UK slot, not something the file says. Add "by its
   stamp" or "which its stamp places in the midday slot". The numbers in that paragraph are all correct (below).

## Answers to the seat's points

1. **Chart.** Reproduced from silver (both captures, 24 rows, `targetdate == 2026-10-17`, dedup on
   `targetdate, cardinalpoint` by `published_at`): 12 bars, 0 duplicates dropped. Values match the committed series and
   the alt text exactly: 23,736 / 23,347 / 23,137 / 21,223 / 20,520 / 24,504 / 26,221 / 22,121 / 21,333 / 30,269 /
   31,966 / 23,946. Trough 20,520 (`1B`, 430 to 730), peak 31,966 (`4B`, 1830 to 2000). All 12 `group_map` labels match
   the 17 October windows in the file (3C 1700 to 1800, 4B 1830 to 2000, which differ from 9 October). `sort: label`
   gives true time-of-day order. A bar per point is the honest choice: all 12 rows share one midnight anchor, the window
   clocks are text, and the two dictionaries disagree on UTC or UK time (current: "Time UTC"; archive: UK time in effect
   at the forecast time and date), so a time axis would invent instants; the caption says the windows are as NESO writes
   them. Order is the same in either zone. The page never charts the held file. Caption and key note are accurate (17
   October 2026 is a Saturday). Alt text is true to the series (the walk skips the 24,504, 22,121 and 30,269 bars it
   passes, which is fine). One reading to be aware of, not a finding: `02:00-02:30 peak` (23,137) is lower than
   `01:00-01:30 trough` (23,347); correct per NESO's window definitions and covered by the key note.
2. **Shared hold line.** "Forecast time stamps end in Z, but NESO does not confirm UTC; some are email-recovery times."
   is true. Registry question for the historic file: FORECAST_TIMESTAMP zone undocumented (values carry Z but sit after
   the file's CKAN `last_modified` when read as UTC), whether it is the immutable issue instant, some timestamps are
   vendor-documented email-recovery times. The field-info dictionary gives only the example `2018-03-28T14:57:45Z` with
   no zone and carries the recovery comment. The line follows the registry, not "settlement-time zone" (the seat's
   paraphrase was wrong, the writer was right to follow the registry). Plain, no codes ("Z" is the literal suffix), 15
   words. It does not name the immutable-issue-instant question; the recovery clause covers the practical effect. Leave it.
   For the siblings, by registry question: 2-day is the same minus the recovery comment; 7-day says the field "has no
   vendor definition" and its zone is undocumented; the 2 to 14 day historic file matches the 1-day question without the
   recovery clause, but its half-hourly member's hold is a different question (whether `GDATETIME` labels the half-hour
   end), so it needs its own line.
3. **Captures.** Bronze and silver agree. Current: 578 bytes, 12 data rows each, targets 2026-10-09 and 2026-10-17, no
   repeated row. Historic: 58,561 then 58,657; all 58,561 earlier rows are present unchanged in the second capture; the 96
   added are 8 target dates (10 to 17 Oct) x 12 rows, one issue each. `F_Point`: 36,300 `NA` and 2,414 blank, then 36,300
   and 2,478. The midday difference is stated accurately in the note: windows identical on all 12, all 12 values differ
   (1 to 103 MW), the archive's 17 October issue is `2026-10-16T08:36:38Z`, its file stamp 11:00:18. On 8 October the
   current file equals the archive on all 12 values and windows, so the claim is correctly scoped to that capture. The
   page itself makes no such claim; only finding 1 concerns it.
4. **Notebook and frame.** Opened both in the browser. The notebook has two cells plus setup; every cell is read-only,
   output has no error, and the table shows 12 rows in start-time order with `published_at` `2026-10-16 11:00:01
   +00:00`, equal to silver in UTC (the session zone would print 12:00:01+01:00). `tail()` is `ORDER BY targetdate DESC
   LIMIT 100` on the `_latest` view (code read), so the lead is accurate; the plot is the picture committed
   (`plot_alt` values correct). The unfolded frame scrolls and shows all 16 columns including the lineage ones.
5. **Row, units, links, body edits.** One row is one target date and cardinal point per publication; key includes
   `published_at` (precedent: constraint breakdown). MW is from the archive dictionary and the field line says so. Related
   links resolve and their reasons are true (`elexon/ndf` half-hourly forecast, `elexon/indo` outturn). Raw requests match
   the bronze sidecar URLs; the connector does one `package_show` and skips an unchanged file. Body corrections are scoped
   and cite evidence: all re-derived true (capture sizes and counts, vintages, 3C and 4B windows, "8 of 12 blank in each
   capture", 36,300/2,414 and 36,300/2,478, 96 added rows). Only the unchanged intro sentence in finding 1 is stale.

## Rendering

Screenshots at 1440, 1024, 768 and 390 (390 through a 390 px iframe), hero, chart, raw feed, frame and guide, notebook
panel, related. Nothing clipped or overlapping. At 390 the longest bar labels start about 14 px from the edge; at 768
the bar labels are about 9 px (already noted by the writer). The site has no dark theme. Server on 9851 started with its
PID recorded and stopped by that PID.

## Defects (pasteable)

- **NESO 1-day-ahead archive (vendor/data):** the archive file holds one issue per target date for the 23 most recent
  target dates (morning only) although the current file is published twice daily; the 17 October current (midday) values
  differ from the archive's issue on all 12 points. A backtest from the archive sees the morning forecast. More captures
  needed to confirm the archive's rule. No gridflow change.
