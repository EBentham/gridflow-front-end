# Slow Reserve requirement forecast: checker review

Package `slow-reserve-requirement-forecast` (table `slow_reserve_requirement_fc`). Checker, 2026-10-18.

## Verdict: REVISE

0 blockers, 1 major, 3 nits. The facts, the chart and the body correction all hold; the major is the seat ruling's
own condition (the caption does not say the negative requirement matches), a one-clause fix.

## What I checked and how it held up

- **Build and detector.** `gridflow-build --only neso_data_portal/slow_reserve_requirement_fc`: exit 0, page written (the
  3 dropped "Known issues" lines warning is the known one; "2 errors on pages not rendered by --only" belong to other
  packages). Detector `--json`: `[]`. Built page text: no em or en dashes, middle dots, arrows, "locally", "our",
  "live", "now", "since 20", "held", planning words or TODOs. `cmp` of the canonical note and the mirror: equal.
  Vault diff against `origin/master` (+124 / -4): the `page:` block, `updated`, and one body span only.
- **Silver and bronze, reproduced (item 1).** 1,874 rows, 1,874 distinct `(auction_date, service_window)`, no nulls.
  Positive requirement unique values `[1800.0]`, negative `[1800.0]`; the bronze CSV (read as text) holds only `1800`
  in both columns. 38 service days with 48 windows, one (25 October) with 50. Window ids on 25 October:
  `1 2 3 4 5 6 5x 6x 7 ... 48`. `forecast_produced_on`: 2026-08-31 on 384 rows (service days 23 to 30 September, 8
  days), 2026-09-22 on 1,490 rows (1 to 31 October, 31 days); each service day has one production date. Days from
  production to service day: 23 to 30 for 31 August, 9 to 39 for 22 September (matches the notebook alt). One
  `published_at`, 2026-09-22 14:48:32.823004 UTC, equal to the sidecar's CKAN `last_modified`. Request URL equals the
  sidecar's `request_url`; `package_show` form matches the approved QR, DM and DR pages.
- **Series, sample, notebook.** Series file: two series over 39 days, `aug` 8 points and `sep` 31 points, every value
  1,800, `rows_used` 1,874, `spec_origin: vault`. Key notes, alt and caption dates agree with it. Samples file: the
  8 rows shown, `gridflow-sample`. Notebook: `run_notebooks.py`, 5 cells, no errors; cell 3 reproduces 384 and 1,490
  windows and 8 and 31 days; cell 4 shows the single pair 1,800 / 1,800 for 1,874 windows; the plot (read in full)
  matches its alt, petrol for 31 August and clay for 22 September.
- **Issue time and earlier editions (item 2).** `forecast_produced_on` is described as "a date only, not a publication
  time" (registry `dtype date`, `issue: none`); `published_at` as "NESO's last-modified time for the whole file, read
  as UTC" (registry vintage `ckan_last_modified`). Nothing on the page calls either an issue time, and nothing says
  whether NESO keeps, replaces or appends earlier editions at its monthly update. The note body keeps its own
  `TODO: verify` on that. The point-in-time line says each capture is one vintage stamped with `published_at`, the same
  line the approved QR page carries.
- **Window numbers and the clock change (item 3).** The frame and record line say `5x`, `6x` belong to 25 October's
  repeated hour, scoped to that date, with no spring claim. Reproduced: on 25 October windows 5 and 6 and then `5x` and
  `6x` read `01:00` and `01:30` twice; 7 starts at `02:00`. NESO's dictionary comment (snapshot `20261008T114228Z`) says
  `7x`, `8x` at the spring change and no windows 5 or 6 on the autumn day, so the file contradicts it; the page does not
  repeat the dictionary's claim. Converting each start label from Europe/London (second occurrence for `x`) gives 1,874
  distinct UTC instants, so the `x` convention separates the pair. See nit 2 on parity with the QR line.
- **`timestamp_utc` and window 1.** Window 1 of 23 September starts `22/09/2026 23:00` local, `timestamp_utc`
  2026-09-22 23:00 UTC; 25 October: window 1 `24/10/2026 23:00`, `timestamp_utc` 2026-10-24 23:00 UTC; 26 October: window
  1 `25/10/2026 23:00`, `timestamp_utc` 2026-10-26 00:00 UTC. In every case window 1 is one local hour before the UTC
  anchor of UK midnight, so "window 1 starts an hour earlier" is true on summer, change and winter days. Every end
  label ends `:29` or `:59`.
- **Body correction and related claims (item 4).** Registry `balancing-reserve-auction-requirement-forecast.json`: the
  lead family `br_auction_requirement_fc_da` (and the other two) have nine columns, the same eight as this table plus
  `Forecast type` / `forecast_type`, and the same `entity_key` `[auction_date, service_window]`. Local BR silver has 48
  windows per day, `1` to `48`. So "the same window columns as Balancing Reserve, whose records add a `forecast_type`
  column" is true and the old sentence ("same layout as ... Balancing Reserve") was wrong. Quick Reserve:
  `quick-reserve-auction-requirement-forecast.json` has the same eight silver columns and dtypes (only the product word
  in the two MW names and the header spelling `Service window Start Time` differ), same key, `temporal`, `latest`,
  `vintage`, `issue` and monthly refresh. The Quick Reserve half of the sentence is right and kept. The change is the
  smallest span that fixes it and cites the registry file.
- **Catalogue and dictionary claims.** Catalogue snapshot `20261006T195819Z`: positive and negative Slow Reserve,
  +/- 0.2 Hz within 15 minutes of a loss event, daily auction at 14:00, delivery 23:00 to 23:00 D+1, "daily forecast of
  requirements", "updated monthly", one resource. Dictionary: MW unit, "Time given in local time", "service window 1
  starts at 23:00 D-1", "Date that the forecast was produce[d]". The page leaves the 14:00 out (no zone given).
- **EAC join bullet.** `eac_results_summary` products `PSR` and `NSR` carry service type "Slow Reserve", in 30-minute
  windows with UTC `delivery_start`. Converting each start label from UK local to UTC matches all 1,200 distinct
  windows from 22 September 22:00 UTC to 17 October for each product. Reading the label as UTC also matches 1,198,
  because contiguous half-hours overlap after an hour's shift, so the join cannot prove the direction by value, as the
  writer says. The direction rests on NESO's "local time" comment, and the earliest EAC window (31 March 22:00 UTC) is
  the 23:00 UK start of service day 1 April, consistent with it. The bullet states only the dictionary-backed method.
  Writer's side observation reproduced: cleared `NSR` is 0 MW in all 1,200 windows (1,968 rows) in that range, cleared
  `PSR` 1,793 to 1,868 MW (mean 1,803), against a negative requirement of 1,800 MW. Not on the page; correctly left out.
- **Raw feed, commands.** `ingest ... --last 24h` and `transform ... --last 24h` with "dates select nothing" and the
  unchanged-`last_modified` skip match `client.py` (`_assert_window_admissible`, the unchanged-capture branch) and the
  approved DM and QR pages word for word.
- **Notebook query claim.** `data.sql` on `silver_neso_data_portal_slow_reserve_requirement_fc_latest` returns the
  whole capture; `_RELATION_NAME_BY_DATASET` and `_date_range_predicate` in gridflow_models as the writer states.
- **Render.** Looked at 1440 (hero to related, section by section), 1024 (page height and width), a true 390 px iframe
  (chart, key, folded frame, guide, notebook tab) and measured width at 390 and 768: document scroll width equals client
  width, nothing clipped or overlapping. Folded-frame and notebook-wrapping items are the known template ones.

## Findings

1. **Major.** `page.chart_view.caption` (and `page.chart_view.alt`). The seat ruling accepts a positive-only chart if
   "the caption and key notes say plainly that negative is also 1,800 MW in every row". The key notes do. The caption
   says only "the positive requirement, mean of each service day's windows ... split by the date each forecast was
   produced"; neither caption nor alt tells a reader, or a screen-reader user, that the negative requirement is also
   1,800 MW and would sit exactly under this line. The approved Dynamic Regulation page was held to the same standard
   (its review's finding 2). Evidence: silver unique positive `[1800.0]` and negative `[1800.0]` on all 1,874 rows.
   Suggested caption ending: "... split by the date each forecast was produced. The negative requirement is also
   1,800 MW in every window, so a second line would sit exactly on this one." and in the alt: "The negative requirement is
   the same, 1,800 MW throughout." Check the build's caption and alt length budgets after the edit.
2. **Nit.** `page.record.fields.service_window` ("Window number: `1` to `48`, plus `5x`, `6x` for 25 October's repeated
   hour"). Accurate and plain, but the approved Quick Reserve line warns of the surprise ("... NESO's dictionary omits
   `5`, `6`"), and NESO's dictionary comment for this file is the same (autumn day has no windows 5 or 6). Someone
   checking the file against NESO's dictionary gets no warning here. Optional: "Window number: `1` to `48`, plus `5x`,
   `6x` for 25 October's repeated hour (NESO's dictionary says otherwise)".
3. **Nit.** `page.facts.cadence` ("Updated monthly (NESO's catalogue), with a forecast for every daily auction"). The
   catalogue supports "updated monthly" and "daily forecast of requirements"; "a forecast for every daily auction" is
   stronger than either and is true only of this file's span (auction dates 22 September to 30 October are contiguous).
   The approved Quick Reserve line is "Updated monthly (NESO's catalogue); each auction is daily". Optional: use it.
4. **Nit.** `page.notebook.lead` ("... because NESO updates the file monthly and a dated `query()` on
   `service_delivery_date` finds only the days a capture holds"). Word for word the approved Quick Reserve lead, so not
   a regression, but `query()` reads the same `_latest` view as `data.sql` here, so it is not the real contrast (the
   Dynamic Regulation review's nit 4, which that page then reworded). Optional: "Reads the `_latest` view, the newest
   capture, with `data.sql` so the cells see every day the file holds; `query()` reads the same view but takes a date
   range."

## Not findings

- The positive-only, production-date split is the seat's ruling; the key notes carry the negative value. Notebook
  cell 4 backs it.
- Template items (folded frame at 390 and 768, mid-word wrapping, stray column in the grouped table, the `Z` on series
  x labels, notebook tab clip) are on the batch file's list.
- Observation for the seat, not a page finding: cleared `NSR` in `eac_results_summary` is 0 MW in every window from 22
  September to 17 October 2026 while the file forecasts a 1,800 MW negative requirement (the writer reported it in the
  Defects section; reproduced here). Worth a line in the gridflow backlog if it is not already there.

## Housekeeping

I served `site/hifi` on 9966 and stopped it; 9670 untouched. I wrote small iframe wrapper HTML files into the
front-end worktree's `site/hifi` for the 390 px and cropped views and deleted all of them (never tracked); `git status`
shows no leftover `_sr_chk` file. Scratch files are under the scratchpad `sr-checker\`. I briefly navigated the shared
Browser pane tab (another agent's, then showing the Static FFR page) while looking for a preview, then stopped using it.
