# Balancing Reserve requirement forecast: author report

Family page `balancing-reserve-auction-requirement-forecast`, lead `br_auction_requirement_fc_da`, members
`br_auction_requirement_fc_da_archive` (rows not shown) and `br_auction_requirement_fc_medium_term` (rows not shown).
Writer, 2026-10-18.

## Status

- `gridflow-build --only neso_data_portal/br_auction_requirement_fc_da`: success. The build's stderr warning about
  3 dropped "Known issues and gotchas" lines does not come from this note (it has no such section; it uses
  "Known quirks").
- Detector on `site/hifi/data-sources/neso_data_portal/balancing-reserve-auction-requirement-forecast.html`: `[]`.
- Rendered page: 0 em dashes, 0 middle dots, 0 arrows.
- Canonical note edited with the Edit tool; CRLF kept (555 lines, 555 CR); vault diff +143 / -6. Mirror copied and
  `cmp` equal.
- Artefacts (worktree `C:\gridflow-wt\fe-neso-as-a`):
  `site/hifi/data/series/neso_data_portal/br_auction_requirement_fc_da.json` (spec_origin vault, 2 series x 48 points),
  `site/hifi/data/samples/neso_data_portal/br_auction_requirement_fc_da.json` (gridflow-sample, 8 rows),
  `site/hifi/data/notebooks/neso_data_portal/br_auction_requirement_fc_da.json` and `-5.png` (run_notebooks.py, 5 cells,
  no errors). No staged chart spec or authored override existed for this dataset.
- Screenshots at 1440, 1024, 768 and a 390 px iframe, all sections looked at: nothing clipped or overlapping. The
  site has no dark theme (no `prefers-color-scheme` in any stylesheet), so one set per width. Shots in the session
  scratchpad `br-req\` folder (f-1440, f-1024, f-768, f-390 and slices).

## The page in one paragraph

Chart: line, silver `br_auction_requirement_fc_da`, two columns as series (`values`), MW, service day 18 October 2026
(auction 17 October, produced 16 October), one value per half-hour window, x = `service_window_start_time` read with
`time_text` (local label drawn on its own clock), `y_min: 0`. Positive 200/400/600/500/600/400 MW stepping at 03:00,
07:00, 11:00, 15:00, 19:00 (EFA block edges); negative 1,450 MW flat. Frame: eight windows of that day (1, 8, 9, 16, 17,
24, 25, 48). Notebook: `data.sql` on the `_latest` view (see below), groupby showing one day of 48 rows, the six step
rows, a step plot.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Key `auction_date`, `service_window`; `_latest` whole capture | registry `src/gridflow/connectors/neso_data_portal/registry/balancing-reserve-auction-requirement-forecast.json` (fc_da record: `entity_key`, `latest: whole_capture`) |
| Medium-term key adds `resource_id`, `latest_partition: resource_id` | same registry, medium_term record |
| One row per auction date and window, 48 on an ordinary day; autumn adds `5x`, `6x` (grain, `service_window` field) | K-AS-1-FACTS §4.1-4.2 (B1 windows 1-48; archive 50 labels with `5x`/`6x`); note body "Window layout" (EAC explainer Appendix B) |
| Window clocks UK local, kept as text (fields, x_label, caption) | registry dtype `string`; FACTS §4.1 T01 (vendor dictionary FI:50-51); corroborated: NESO EAC `eac_results_summary` PBR rows for 9 Oct 2026 start 2026-10-08 22:00 UTC, i.e. 23:00 BST, and cleared MW track this requirement window by window (report only) |
| End label `:29`/`:59` | silver rows (frame); FACTS §4.1 T02 |
| MW for both requirement columns (field lines, unit) | registry header `... Requirement MW`; FACTS g4 (vendor dictionary FI:79,91) |
| Negative given as a positive figure (key note, field) | frame rows and chart: `negative_balancing_reserve_requirement_mw` = 1450.0 |
| `forecast_produced_on` a date, not a publication time | registry `issue: {kind: none}`, dtype date; FACTS §4.1 |
| `timestamp_utc` = UK midnight of the delivery date in UTC; window 1 an hour earlier | registry `temporal: date_sp1(service_delivery_date)`; silver: 18 Oct rows `timestamp_utc` 2026-10-17 23:00 UTC, window 1 label 2026-10-17 23:00 local (22:00 UTC) |
| `published_at` = file last-modified, read as UTC | registry `vintage: ckan_last_modified`; sidecar `ckan_last_modified` 2026-10-16T13:05:02.317939 = silver `published_at` |
| Medium-term without detailed wind and solar forecasts; day-ahead refines it | note body para 2 (vendor package description) |
| Current files overwritten daily, earlier days to archives (cadence fact, member differs) | note body para 2 and Cadence (vendor wording); measured agreement below |
| Day-ahead file holds one delivery day (what_it_is, lead) | notebook output: one group (17 Oct, 18 Oct, 16 Oct) of 48 rows; both captures hold 48 rows of one day |
| Chart values, alt, key notes | committed series: positive {200, 400, 500, 600}, negative {1450}, 48 x values 2026-10-17T23:00 to 2026-10-18T22:30 |
| Steps on EFA block edges | series changes at 03:00, 07:00, 11:00, 15:00, 19:00; EFA 1 starts 23:00 local (FACTS §5.1, EAC explainer Appendix B) |
| `query()` reads `silver_neso_data_portal_br_auction_requirement_fc_da_latest`, filters `service_delivery_date` (DATE, BETWEEN) | `gridflow_models` `_get_method_registry.py:58-96`, resolved in the models interpreter: `service_delivery_date DATE silver_..._fc_da_latest` |
| Raw requests | newest sidecars (2026-10-16) `request_url` for all four resources; `package_show` per `endpoints.py:255` and the eac-br page |
| Ingest and transform `--last 24h`; dates select nothing; skip when `last_modified` unchanged | `client.py:1474-1545` (window end must not be future or older than about 48 h), `client.py:1752-1765` (unchanged skip); same lines as the reviewed demand-flexibility page |
| `PBR`, `NBR` in EAC results (related, how_used) | silver `eac_results_summary`: products PBR and NBR, delivery 2026-03-31 22:00 to 2026-10-17 21:30 UTC |
| Holds | registry hold questions (BR-ARCHIVE-AVAILABILITY, BR-MT-ARCHIVE-AVAILABILITY); ledger row 79 |

## Body corrections (canonical note)

1. "Files by disposition": "Each resource has exactly one captured body so far (2026-10-08)" was stale. Bronze now
   holds a second capture of every resource (2026-10-16). Replaced with the two capture dates and what was measured on
   silver: in both archives all 46,414 rows of the 2026-10-08 body are in the 2026-10-16 body with equal values, window
   labels and production dates; each archive gained 432 rows (service days 2026-10-09 to 2026-10-17); the rows
   comparable with the 2026-10-08 current files are equal (48 day-ahead rows for 2026-10-09; all 672 medium-term rows,
   432 now archived and 240 still in the current file). The vendor-rule TODO is kept.
2. "Cadence": "Captures to date: one per resource ... No scheduled refresh has run yet" replaced with the two
   captures, eight days apart.
3. Front matter `updated` 2026-10-13 to 2026-10-18.

Nothing else in the body was changed. The capture-specific counts elsewhere (48 rows, vintages of 2026-10-07) describe
the first capture and remain true of it.

## Unverified

- The vendor's "forecasts published after 27 February are Live Demand Forecasts" (no year): not checked, untouched.
- The 08:15 auction time zone (body TODO): not settled by a vendor statement. The EAC result times support UK local for
  the window clock only.
- Whether the requirement is exactly what NESO tries to buy in the auction: the page says "requirement for each daily
  auction" (vendor wording). Cleared PBR on 9 October sits within a few MW of it (197 to 600 MW against 200 to 600);
  cleared NBR was 2 to 4 MW against 1,450. Not stated on the page.

## Open questions

1. Archive holds: the second capture is the first evidence for the hold questions (archived values unchanged over
   8 days, and the 9 October day-ahead rows archived exactly as published before delivery). It does not answer when
   each forecast was first public, so the holds stand; the evidence may help the unit that owns them.
2. The day-ahead archive's 15-day leads (12,097 rows labelled `Dayahead`, FACTS §4.2) look like medium-term figures
   placed in the day-ahead archive. Unexplained; held anyway.
3. Medium-term current file alone is all-forward (FACTS §4.3). Serving it separately would give the page a
   medium-term against day-ahead comparison (for 18 October the two are identical). A scope decision for the seat.

## Template problems (report only, nothing worked around)

- The unfolded sample frame scrolls horizontally in an 800 px pane (folded state is fine). Bobbo's ruling says the
  frame folds and never scrolls; worth a look at the template, not this page.
- Notebook preview wraps long identifiers mid-word at 768 and 390
  (`silver_neso_data_portal_br_auction_requirement_fc_da_lates` / `t`). Nothing is clipped.
- A rolling current file makes `notebook.needs` awkward: a reader can only ingest today's day, so the notebook uses
  `data.sql` on `_latest` with `needs: a capture of the day-ahead table`. Other rolling-file pages will hit the same.

## Checker: look hardest at

- The x axis: `time_text` reads the UK-local labels as if UTC, so ticks show the local clock as written (00:00 to
  21:00, first point 23:00 on 17 October). Caption and x label say so; confirm that reads honestly.
- The two `held` lines (16 words each) and the medium-term one, which holds a table whose current file is all-forward.
- The `timestamp_utc` field line ("window 1 starts an hour earlier") across clock-change days: true by construction
  (window 1 = 23:00 local the day before), but worth re-deriving.

## Defects

- No new gridflow or data defect found on this package.
- Evidence for the BR archive holds (not a defect): between the 2026-10-08 and 2026-10-16 captures, both Balancing
  Reserve archives (`br_auction_requirement_fc_da_archive`, medium-term archive resource
  `fb2e0eea-b1c0-4ba3-a817-0561182a6e26`) kept all 46,414 earlier rows unchanged and appended 432 rows (2026-10-09 to
  2026-10-17) equal to the rows the current files held before. Supports, but does not settle, BR-ARCHIVE-AVAILABILITY
  and BR-MT-ARCHIVE-AVAILABILITY (publication time is still unknown).
- Template: unfolded sample frame scrolls horizontally at 800 px; notebook preview breaks identifiers mid-word at
  768 and 390.
