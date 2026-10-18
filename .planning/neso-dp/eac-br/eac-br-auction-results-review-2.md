# Balancing Reserve auction results (`eac-br-auction-results`): checker re-review (Revision 1)

Checker, 2026-10-18. Re-check of the writer's "Revision 1" in `eac-br-auction-results-author.md` against review 1 (2 majors, 7 nits).

## Verdict: APPROVE

Both majors are fixed and verified against silver; the seven nits are fixed, with three small leftovers, all nits. Nothing above nit.

Gates, run myself: `gridflow-build --only neso_data_portal/eac_br_results_summary` succeeds; `detect.mjs --json` returns `[]`; 0 em dashes in the page; mirror `cmp` equal to the canonical note; note is 492 lines, 492 CRLF. `pytest -q`: 153 passed, 3 failed (`test_dataset_page.py::test_hubs_and_landing_link_every_page`, two in `test_package_pages.py`; they fail on `catalogue` pages-without-package, the hub writer's in-progress work, not this page). `test_chart_spec.py` + `test_distil.py`: 48 passed. Page grep for `checked`, `locally`, `held`, `our`, `since 20`, `% of`, digits before `rows`/`days`, `live`, `now`, `yet`, `real-time`, `planned`, `soon`, dash, middle dot, arrow: no hits.

## Major 1 (NBR line reads as a £0 price): fixed

The chart spec now filters `cleared_volume > 0`; the series was re-distilled (`spec_origin: vault`, digest passes, `rows_used` 39,673 of 57,216). Re-derived independently from silver (UTC reading, UK day 23:00 to 23:00):
- `clearing_price` is 0 on all 17,543 windows with `cleared_volume` 0, so "NESO records £0 where nothing cleared" is exact. 39,673 windows cleared.
- The committed series equals my daily means over cleared windows on every point: PBR 596 points, NBR 257 points, no series point missing from silver, none extra, max difference 0.0005 (rounding).
- NBR has 339 gap days, 11 of them before 2024-12-04; from 4 December 2024 it has exactly two points, 2024-12-04 (1 window) and 2025-08-20 (16 windows), both 0.0. The key note "Gaps are days when no negative reserve cleared; from December 2024 almost every day" and the alt ("cleared on two days only, both at 0", "11 gap days before December") are true.
- Spot days (cleared windows only): PBR 2024-03-13 9.579, 2024-07-04 1.470 (minimum), 2024-10-27 4.523 (50 windows), 2024-12-13 40.471, 2025-01-21 51.542 (maximum), 2025-10-29 3.910; NBR 2024-05-25 1.543. PBR clears every day (92.1% of days between 2 and 10, so "mostly 2 to 10" holds). NBR maximum 1.55 on 2024-04-14 and 2024-04-21, so "at or below 1.55, reached in April 2024" holds. The window ends on the newest silver day, 29 October 2025.
- Caption now says "unweighted mean over cleared half-hours", names the £0 convention, and says a day with no clears is a gap. Rendered chart (1440 and 390): the isolated NBR days draw as dots, the gaps are visible, nothing clipped.
- The notebook's first query now averages price over cleared windows (`mean_price_cleared`); output reproduces: PBR 943 to 955 means 12.99, 37.63, 51.54, 26.70, 8.46, 4.63, 6.54 over 48 windows each, NBR 0 windows and NaN price for all seven.

## Major 2 (commands did not fetch what the notebook reads): fixed

`raw_feed.commands` is now `gridflow pipeline neso_data_portal eac_br_results_summary --last 24h` and the same for `eac_br_results_by_unit`; `notebook.needs` is "a capture of the summary and by-unit tables"; the orphan sell-orders transform is gone. Checked in `cli.py`: `pipeline` resolves one window, then runs ingest then transform on it, the same as the two separate commands the page used before, and a transform date with no bronze only warns. The notebook reads exactly the summary and by-unit `_latest` views; cell 4 output reproduces (`units_mw` equals `cleared_volume`: 452, 401, 379, 381 at 139.99, 139.99, 179.99, 179.99). Two lines fit the three-command limit (`COMMANDS_COUNT = (1, 3)`), which is the writer's reason for `pipeline` over four lines. The raw-feed note says "run one line per table", which fits the commands.

## Nits from review 1

3. Universals: "(checked)" is gone everywhere. `what_it_is` now scopes the reconciliation "Across NESO's archive"; by-unit `differs` says "no rows at 0 MW" (true: 0 by-unit rows with `executed_quantity` 0). Closed. See leftover B.
4. Clock: x label and caption say "UK (inferred)" and "reading NESO's clockless text as UTC"; the body no longer forbids a reading and says the site chart's UTC reading rests on the evidence. The writer's correction of my "14h45m every time" is right and I checked it against silver: in 595 of 596 auctions the latest sell `order_entry_time` is 14h44m to 15h29m before the auction's first window string (my range 14:44:56 to 15:29:15, so the two at 15h29m10s and 15h29m15s round into it); auction 187 is the exception, 29h15m (last entry 2024-03-28 17:44). Time of day of that last entry: 06:30 to 07:15 on BST days and 07:30 to 08:15 on GMT days (truncated to the minute; the writer's 06:31 to 07:16 and 07:31 to 08:16 are the same values rounded). Both are within one minute and the pattern, an hour earlier in BST, is right. Closed. (My review 1 said "about 07:00 to 07:14" and "14h 45m every time"; both were loose, the writer's version is the accurate one.)
5. PBR/NBR: `what_it_is` says "read as positive and negative reserve" and the field line says NESO's dictionary lists only the codes (true; dictionaries read "[NBR,PBR]"). Closed.
6. History and cadence: history reads "in NESO's archive dump"; cadence "later auctions are in NESO's newer EAC package". Closed. See leftover C.
7. Zero-MW sell orders: defect entry withdrawn in the report; sell `differs` now says "zero-MW orders can read executed" (true: 28,370, all with `quantity` 0). Closed.
8. Code polish: new tests pass (`time_text` without `day`, a failing parse, the bucket clash); `validate_spec` rejects `time_text.day` with a sub-day `time_bucket`; the docstring says a day is a date at `T00:00:00Z`. A bad format becomes a `DistilError` naming `time_text` (tested). See leftover A for the unknown zone.
9. Wording: title now "Mean Balancing Reserve clearing price, March 2024 to October 2025"; the notebook columns are `windows_cleared`, `mean_mw_per_window`, `mean_price_cleared`, and the lead describes both queries. Closed.

## Leftovers (all nit)

A. `distil.py`, unknown time zone: the writer's report says an unknown zone is raised as a `DistilError`, but it is not. With `zone: Europe/Lndon`, `validate_spec` returns `[]` and `distil_spec` raises `polars.exceptions.ComputeError: unable to parse time zone` from `_scan`, because Polars rejects the zone when the expression is built, before the `try` around `lf.collect()`. Only a bad format is wrapped. Fix: build the expression inside the `try`, or check the zone with `zoneinfo`/Polars in `validate_spec`. No effect on this page.
B. `page.related[0].note`: "All `auction_unit` values are National Grid BM unit IDs in the register" is a measured universal over the archive without a scope (157 of 157 distinct values match `national_grid_bm_unit`; 0 match `bm_unit_id`, so it is true). Suggest "in NESO's archive" for consistency with `what_it_is`.
C. `page.facts.cadence`: "later auctions are in NESO's newer EAC package" rests on our measurement that the newer package's Balancing Reserve rows start at `2025-10-29T23:00:00Z` (note body), not on a vendor sentence. It matches the data; say "appear to be" or cite the vendor text if one exists.

## Render

Re-shot myself with headless Chrome: 1440, 1024 and 768 folded; 1440 unfolded with the notebook open; 390 folded and unfolded with the notebook open, through a 390 px iframe. Hero, chart with gaps and dots, the key note, raw feed (member headings break at 390), the two-line command block, the frame, guide, notebook cells, plot and related list are fully visible. No dark scheme exists (no `prefers-color-scheme` in any stylesheet).
