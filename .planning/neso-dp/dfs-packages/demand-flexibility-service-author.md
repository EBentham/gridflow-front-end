# Demand Flexibility Service 2023/24: writer's report

Page `demand-flexibility-service` (family; lead `dfs_utilisation_report_sum`, then `dfs_utilisation_report`,
`dfs_industry_notification`, `dfs_service_requirements`). Writer, 2026-10-23.

## Status

- Build `uv run --system-certs --extra build gridflow-build --only neso_data_portal/dfs_utilisation_report_sum`: passes,
  no errors (the 37-line "Known issues" grammar warning is global, not this page).
- Detector on `site/hifi/data-sources/neso_data_portal/demand-flexibility-service.html`: `[]`. Real em dashes: 0.
- Mirror: `cp` + `cmp` clean; the note keeps CRLF on all 586 lines.
- Screenshots at 1440, 1024, 768 and 390 (390 through a 390 px iframe), light only (the site has no dark theme):
  nothing clipped or overlapping beyond the known template items below. Server on 9871 started with a recorded PID
  and stopped by that PID.
- Files (mine only): canonical note `C:\gridflow-wt\vault-neso-dfs\30-vendors\neso-data-portal\datasets\demand-flexibility-service.md`
  (page block added; body unchanged), its mirror `vault\neso_data_portal\demand-flexibility-service.md`, and
  `site\hifi\data\{series,samples,notebooks}\neso_data_portal\dfs_utilisation_report_sum*` (series JSON, sample JSON,
  notebook JSON + `-5.png`). No staged spec or authored override existed for this lead.
- Manifest lead and members match `site/hifi/data/neso_data_portal.json` (slug `demand-flexibility-service`, lead first).

## The answers the launch prompt asked for

1. **What one row is.** Summary: one half-hour delivery window (key `delivery_date`, `window_from`); the window's
   requirement, accepted MW and indicative accepted cost, then settled volume and cost. Report: one bid outcome of one
   DFS unit in one window (key adds `dfs_unit_id`), `Accepted` or `Rejected`, with tendered MW split by region.
   Notification: one notice, an Anticipated Requirement Notice or "Requirement Published", for a target date
   (`requirement_for`). Requirement: one window's MW requirement, guaranteed acceptance price and eligible
   participants (held). Units from NESO's dictionary: MW for every volume, £ for both cost columns, £/MWh for
   prices. Differences from the 2024-onwards showcase, only where NESO says so: NESO calls this package the Winter
   2023/24 service, says "This dataset will no longer be updated" (catalogue "Not Active") and points to
   `demand-flexibility` for the latest results. The files have no event id column (their headers).
2. **Clock.** NESO's dictionary marks `From`, `To` and the notification time `GMT` (comment field). Every delivery
   date (16 November 2023 to 21 March 2024) and every notification date falls in the GMT half of the year, so for
   these rows GMT, UK local time and UTC agree; whether NESO meant UK local time cannot be told from these rows. The
   page says "GMT in its dictionary" and keeps the labels as text. `timestamp_utc` is gridflow's `date_sp1` anchor,
   00:00 UK time on the delivery date (00:00Z for every row here). The notebook converts `timestamp_utc` from the
   session zone to UTC in its first cell.
3. **Captures.** One capture per table, all written 2026-10-08 (no 16 October recaptures exist in bronze or
   silver): summary 32 rows, report 1,220, notification 30, requirement 32; one `bronze_capture_id` and one
   `published_at` each. Nothing repeats; `dedup: {"on": [delivery_date, window_from], order_by: published_at}` is
   set on the chart and the frame as a guard.
4. **Chart.** Line (drawn as dots: 16 points per series, joined only on consecutive days) of `values`
   `dfs_provider_bids_accepted_total_cost_gbp` (accepted) and `settled_cost_gbp` (settled), summed per delivery date,
   in £, 16 November 2023 to 21 March 2024. Two lines, never stacked or added. Live and Test never share a date here,
   so a day's sum never mixes types; the caption names the two Live days. Held member: one plain line, "NESO does not
   say when each window's requirement was first published."
5. **Related.** `neso_data_portal/demand-flexibility`, `-live-events`, `-test-events`, plus `elexon/system_prices`.

## Evidence

| Claim on the page | Evidence |
|---|---|
| Four tables, one CSV file each; request URLs | registry `gridflow/src/gridflow/connectors/neso_data_portal/registry/demand-flexibility-service.json` (one resource per family); bronze sidecars `request_url` for all four (`.../2026/10/08/*.meta.json`) |
| `package_show` then whole-file download unless `last_modified` unchanged; dates select nothing | `connectors/neso_data_portal/client.py` `iter_members` docstring (lines ~1661-1672): upload member `unchanged` when newest capture carries the live `last_modified` |
| Cadence "Not Active"; NESO no longer updates the files | catalogue snapshot `20261006T195819Z`, package `demand-flexibility-service`: extra `Update frequency: Not Active`; notes "This dataset will no longer be updated" |
| Successor page NESO points to | same package notes: "Please visit .../demand-flexibility for the latest auction results" |
| Key `delivery_date`, `window_from` (summary); report adds `dfs_unit_id` | registry `entity_key`; silver: 32 distinct summary keys, 1,220 distinct report keys |
| Units MW, £, £/MWh | field-info snapshot `20261008T114228Z/dfs_utilisation_report_sum.json`, `dfs_utilisation_report.json` (`unit` MW, `£`, `£/MWh`; checked as UTF-8 bytes C2 A3) |
| Window labels GMT | field-info `comment: "GMT"` on `From`, `To` (summary, report, requirement) and `Notification Issued Time` |
| `timestamp_utc` = 00:00 UK time on delivery date | registry `temporal: date_sp1` on `delivery_date`; silver: every summary row 00:00Z |
| `published_at` = file last-modified, read as UTC | registry `vintage: ckan_last_modified`; silver `published_at` 2024-04-10T07:56:25.272181Z = catalogue `last_modified` 2024-04-10T07:56:25.272181 (no zone) |
| `dfs_procured_mw` = report Accepted bids summed | silver: max abs difference 0.0 MW over 32 windows; accepted cost vs MW x price x 0.5 h max £0.50 |
| Settled above accepted MW in some windows | silver: 12 of 32 windows; visible in the frame (15 Dec 17:00 and 17:30) and notebook plot |
| Summary settles both types | silver: every Test and Live row has settled volume and cost |
| Chart alt and key numbers | committed series: accepted £3,031,162 (29 Nov) and £3,573,586 (1 Dec); settled £2,299,489 and £2,464,136; Test days to 17 Jan accepted £895,500 to £1,557,000, settled £593,446 to £1,227,107; from 29 Feb all under £90,000 (max £84,947); 1 Mar £15,911 and £15,276; settled above accepted on 7 of 16 days |
| Live days 29 Nov and 1 Dec; the rest Test | silver: each date carries one type |
| Notebook lead | gridflow_models `research/handles/source.py` `query()` + `_get_method_registry.py`: relation `silver_neso_data_portal_dfs_utilisation_report_sum_latest`, `delivery_date` DATE `BETWEEN` (both ends), bitemporal columns dropped |
| Plot alt | notebook output: Live accepted 449 to 487 MW, settled 299 to 358; Test accepted 56 to 523; 12 windows above the line, all Test |

## Body corrections

None. Every body fact I re-derived held (row counts, 946 Accepted and 274 Rejected, 59 units of 25 participants,
28 Test and 2 Live notices, 16 and 14 notification types, reconciliation, 12 of 32 settled above procured, CRLF).

## Unverified

- Whether NESO's "GMT" means UK local time; no row can tell, since every date is in winter.
- The note body's claim that NESO's participation guidance describes tests as real deliveries (not in the snapshot I
  read); the page says only that the summary settles both, which the rows show.

## Open questions

- None blocking. The requirement table stays held per the ledger.

## Template problems (seat items, already on the follow-up list or new)

- New: a family page does not print `raw_feed.requests`; the `package_show` line I set (as approved family pages do)
  appears nowhere on the page, only "one `package_show`" in the note.
- Known: the notebook runner garbles a MultiIndex frame (columns shifted, the first index level lost). I flattened
  the cell with a `merge`, so this page is unaffected.
- Known: notebook tab label ends in an ellipsis at 390 px; long names in the notebook break mid-word at 390.

## Defects

- **NESO dictionary, `dfs_service_requirements` `From`:** `unit` and `example` swapped (`unit: "17:00"`,
  `example: "HH:MM"`), field-info snapshot `20261008T114228Z`. Already in the note body; nothing new.
- **NESO data, `dfs_utilisation_report` regional columns:** the 14 regions plus `other` do not sum to `total` on 87
  of 1,220 rows. Already in the note as a non-holding question; nothing new.
- No new gridflow or data defect found.
