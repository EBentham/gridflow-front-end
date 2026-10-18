# Balancing Reserve requirement forecast: checker review

Family page `balancing-reserve-auction-requirement-forecast` (lead `br_auction_requirement_fc_da`; members
`br_auction_requirement_fc_da_archive` and `br_auction_requirement_fc_medium_term`, both held). Checker, 2026-10-18.

## Verdict: REVISE

2 majors, 8 nits, 0 blockers. Both majors are one-sentence wording fixes in the note's `page:` block; the data, chart,
time-zone handling, key, holds and notebook are right.

What passed (checked, not assumed):

- `gridflow-build --only neso_data_portal/br_auction_requirement_fc_da` succeeds; detector on the built page returns `[]`.
  Mirror is byte-identical to the canonical note (`cmp`). Artefacts: series `spec_origin: vault`, sample
  `generated_by: gridflow-sample`, notebook `generated_by: scripts/run_notebooks.py`; no staged chart spec or authored
  override remains.
- Chart values against silver, service day 2026-10-18 (auction 2026-10-17, produced 2026-10-16): 48 windows; positive
  200 x8, 400 x8, 600 x8, 500 x8, 600 x8, 400 x8 (value counts 400:16, 200:8, 500:8, 600:16); negative 1450.0 in all 48.
  Steps fall on windows 9, 17, 25, 33, 41 (03:00, 07:00, 11:00, 15:00, 19:00 local), which are the EFA block edges.
  Alt text, key notes and `plot_alt` match the series (min 200, max 1450, 48 points).
- Seat ruling on time: the x axis ticks (00:00 to 21:00) are the local labels as written, the axis label reads "window
  start, UK local time as written", and the caption says "on the UK clock as NESO writes it". Nothing on the page implies
  UTC for a local time: the SVG has no tooltips or UTC text, the frame shows `service_window_start_time` as bare text
  with no zone, the notebook plot repeats "UK local time as written". UK local is also true: joining the 9 October day-ahead
  requirement to NESO's cleared `PBR` volume on `eac_results_summary.delivery_start` matches 48 of 48 windows with a mean
  absolute difference of 2.6 MW when the label is read as UK local (BST, minus one hour to UTC) against 43.0 MW if it
  were UTC; the note also cites the vendor EAC explainer (Appendix B) for the UK local clock.
- `timestamp_utc` field line is right. `casting.py:610-626` builds it as `settlement_period_to_utc(service_delivery_date, 1)`,
  i.e. UK midnight of the delivery date in UTC. Silver: one value for all 48 rows, 2026-10-17 23:00 UTC for 18 October
  (BST). Window 1 is 23:00 UK local the previous day (22:00 UTC), one hour before the anchor, also after the clock
  change (28 Oct onward: anchor 00:00 UTC, window 1 23:00 UTC). Archive rows for 2024-10-27 confirm the anchor is
  23:00 UTC on the change day too, and that `5x`/`6x` repeat the `5`/`6` start labels.
- `published_at`: code reads CKAN's naive `last_modified` as UTC (`_bronze.py:192-206`, "corroborated, never a vendor
  contract"); the page says "read as UTC". Silver value 2026-10-16 13:05:02.317939 equals the sidecar. Correct.
- Key `auction_date`, `service_window` equals the registry `entity_key`; one row per auction date and window; 48 per
  ordinary day. `forecast_produced_on` is a date (registry dtype `date`, issue `none`) and the page says so. Issue time
  versus delivery window is stated plainly in the field lines.
- Held lines against the registry hold questions (`BR-ARCHIVE-AVAILABILITY`, `BR-MT-ARCHIVE-AVAILABILITY`): the
  day-ahead archive line ("does not say when each archived forecast was published, or whether it is ever amended")
  restates the question's two halves in plain words. The medium-term line matches its first half (publication instant
  unknown). No codes, no planning words. See nit 3.
- Raw requests equal the newest bronze sidecars' `request_url` for all four resources (2026-10-16). Commands match the
  reviewed demand-flexibility page and `client.py` (`--last 24h` window rules, `last_modified` skip at lines 1752-1765).
- Notebook: `data.sql` on `silver_neso_data_portal_br_auction_requirement_fc_da_latest` runs in the models interpreter
  (I re-ran cell 3's query read-only: pandas frame, 48 rows, one group 2026-10-17 / 2026-10-18 / 2026-10-16). `_latest`
  is `whole_capture` (`latest_views.py:84-87`, newest complete capture); `query()` filters `service_delivery_date` with
  `BETWEEN` (`_get_method_registry.py:58-96`). The lead says what it reads. Read-only cells, no errors; the committed
  plot (`...-5.png`) shows the real steps.
- No local-data references on the page: grep of the built page for `locally`, `our`, `since 20`, `live`, `now`,
  planning words returns nothing; the only `held` is "reserve held on BM units" (not a status). Capture times and bronze
  paths appear only inside the eight rows. Zero em dashes, en dashes, middle dots, arrows.
- Layout: looked at 1440 (hero), 1024, 768 and 390 (a true 390 px viewport): no horizontal page overflow at 390 or 768
  (`scrollWidth` equals viewport), hero scenery, chart, key notes, raw feed, folded and unfolded frame, guide, notebook
  panel and related list all fully visible. The site has no dark scheme (no `prefers-color-scheme` in `assets/*.css`).

## Findings

1. **major** `page.what_it_is`, `page.notebook.lead`, `page.family.members[0].differs` ("whose file holds one delivery
   day", "NESO replaces the file daily, so it holds one service day", "Day-ahead forecast for the next service day"). A
   rule about what the vendor's file contains, proved only by the project's own two captures. NESO's stated fact is that
   the file is overwritten daily; that it therefore holds exactly one day is an inference (the note body itself says
   "Two captures do not make a vendor rule" and keeps the amendment question as `TODO: verify`). The author's own
   evidence row for this claim is "both captures hold 48 rows of one day" (author report, evidence table row
   "Day-ahead file holds one delivery day"). Rubric 1 and 3: a measured-on-our-copy universal. Fix: say what NESO says
   and what the page shows, for example `what_it_is`: "... then the day-ahead refinement, a file NESO replaces daily."
   and `notebook.lead`: "Reads with `data.sql` from the `_latest` view, the newest capture, because NESO replaces the
   file daily and a dated `query()` finds rows only for the day it holds." and drop "the next" in `differs` ("Day-ahead
   forecast; NESO replaces the file daily").

2. **major** `page.how_used[2]` ("Join on delivery date and window label, not `timestamp_utc`, which is one per day.").
   Sits directly under the bullet that tells the reader to compare against cleared `PBR`/`NBR` from NESO's EAC results,
   and the related line says "for the same windows". `eac_results_summary` has no window label or delivery-date column:
   its columns are `auction_id`, `auction_product`, `service_type`, `delivery_start`, `delivery_end`, `cleared_volume`,
   `clearing_price`, `linked_service_window_id` (null on the PBR/NBR rows I read), plus lineage. The only join that works
   is on the UTC instant `delivery_start`, which needs the local `service_window_start_time` text converted with the UK
   zone (my check: 48 of 48 windows match with the one-hour BST shift; none if the text is treated as UTC). The page never
   tells the reader the text must be converted, and the advice as written cannot be followed against the table it names.
   The bullet is true only for joining this table to another table of the same package. Fix: say which join each
   bullet means, e.g. "Join to EAC results on the window's UTC instant: read `service_window_start_time` as UK local
   time, then convert." and keep the window-label join as a separate bullet limited to the package's own tables, with the
   `5x`/`6x` caveat if retained.

3. **nit** `page.family.members[2].held` ("Shares a table with its archive, and NESO does not say when archived
   forecasts were published."). Two problems: after "Rows not shown:" the sentence has no subject ("Rows not shown:
   Shares a table ..."), and "its archive" reads as a separate member, contradicting the line above it ("a current and an
   archive file"). Suggest: "Its table includes the archive file, and NESO does not say when archived forecasts were
   published." (16 words or fewer holds).

4. **nit** `page.record.select.columns` and the folded frame. The two MW columns are the point of the page, but their long
   names exhaust the width budget: at 1024 the folded frame shows `service_window`, the start time and the positive
   column, with `negative_...` behind the fold; at 768 neither MW column is visible until the frame is unfolded. This is
   the template's fold, not a page error, but the reader's first look at the frame carries no requirement value at 768.
   Optional: `select.columns` cannot shorten silver names; report to the seat only.

5. **nit** Template (already reported by the writer, confirmed): the unfolded frame scrolls horizontally inside its own
   pane (1024: scrollbar under the frame; page `scrollWidth` 1009 below the 1024 viewport, so the page itself does not
   overflow). Conflicts with the ruling that the frame folds and never scrolls.

6. **nit** Template (confirmed): the notebook preview breaks identifiers mid-word at 390 and 768
   (`silver_neso_data_portal_br_auction_requirement_fc_da_lates` / `t`) and the preview tab label truncates
   ("br_auction_requiremen..."). Nothing is clipped off-screen; reading the SQL is awkward.

7. **nit** `page.chart_view.caption` / chart axis. The line starts at 23:00 on 17 October, left of the first tick
   (00:00), but the axis shows no date and the caption says only "service day 18 October 2026". The alt text and
   `what_it_is` ("from 23:00 UK time") say it; the caption could add "from 23:00 the evening before". Also `chart_view`
   key note for positive reserve cites "EFA block edges" without defining EFA; fine for the audience, noted only.

8. **nit** `page.raw_feed.requests` / `page.family.members[].request`. The download URLs carry a vendor hash prefix
   that the note says "can change" (it already differs between the 8 and 16 October captures: `69ca2874...` against
   `132671df...`). The page presents the 16 October URL as the address with no hint that the prefix changes when NESO
   replaces the file; the resource id is the stable part. One short clause in `raw_feed.note` would cover it.

9. **nit** `page.record.fields.service_window` ("the autumn clock change adds `5x`, `6x`"). True (archive rows for
   2024-10-27 carry `5x`/`6x` repeating the `5`/`6` start labels), but the note body also says the spring change omits
   `5` and `6` (body line 525); "1 to 48" with only the autumn case stated leaves the spring day unexplained.

10. **nit** Artefact only, not on the page: `site/hifi/data/series/neso_data_portal/br_auction_requirement_fc_da.json`
    stamps the local labels with `Z` in `x` ("2026-10-17T23:00:00Z", `x_kind: time`). The template draws them as the local
    clock via `time_text` and nothing on the page shows the `Z`, so the seat ruling holds, but anyone reading the JSON
    would take them as UTC. Worth a note in the template for `time_text` series.

## Vault body edits (rubric 7)

Three edits, each minimal and evidenced: `updated`, the "Files by disposition" capture paragraph, and the "Cadence"
paragraph. The measured claims check out against silver (each archive 46,414 + 432 rows; 432 = 9 service days x 48;
672 = 14 days x 48 = 432 archived + 240 current). They name local capture dates, row counts and a local path, which is
acceptable in the vault but must not (and does not) reach the page. Cosmetic: the "Files by disposition" paragraph has a
ragged line break ("the current file). Two captures / do not make a vendor rule").

## Not independently verified

- The vendor's "forecasts published after 27 February are Live Demand Forecasts" (no year): untouched, not on the page.
- The notebook runner was not re-run (it writes files); I re-ran cell 3's query read-only and checked outputs against silver.
