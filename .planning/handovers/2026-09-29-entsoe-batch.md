# ENTSO-E batch: live tracker (opened 2026-09-29)

- **Brief:** `.planning/v5/p26/BATCH-entsoe.md`.
- **Reports:** `.planning/v5/p26/entsoe/`.
- **Worktrees:** in the session scratchpad.
  - `p26-entsoe` on branch `v5/p26-entsoe`.
  - `vault-p26-entsoe` on branch `docs/v5-p26-entsoe`.
  - If the scratchpad is cleared, recreate both from GitHub.
- **Throttle (Bobbo 2026-09-29):** "increase the speed... spin up more agents in parallel".
  - Up to 10 agents at once (raised 18:20 UTC: 35% used with 1h31m left).
  - No launches above about 92% of the 5-hour window. The window resets at 19:50 UTC.
- **Ship:** under ruling #36, as with Elexon.
- **19:03 UTC, 85% used, 47m left:** the capacity family check and the auction_revenue re-check are the last agents
  running. Nothing more starts before the reset. The 19:53 UTC timer resumes: rows marked "writers after the reset",
  starting with group 3 (balancing-energy-bids, congestion-management, actual_generation_units,
  generation_units_master_data), then group 4.
- **18:57 UTC, 82% used, 53m left:** only checks and fixes for pages already written may start now, up to about
  90%. Nothing new until the 19:50 reset; the resume timer is set for 19:53 UTC.
- **18:46 UTC, 73% used, 1h04m left:** no new writers. Checks and revisions for pages already written may launch up
  to about 90%. After that, everything waits for the 19:50 UTC reset. Then resume the "writers after the reset" rows in
  order, with checkers as writers finish, keeping up to 10 agents at a time.
- **Pause on new writers (18:34 UTC, 59% used, 1h16m left, rising about 12 points per 7 minutes):** in-flight pages finish
  their checks and revisions. Groups 3 and 4 start after the 19:50 UTC reset. (At 18:38 the rate had slowed, 63% with 1h12m left, so two group-3 writers started.)

## Per page (agent ids resume with SendMessage)

| Page | State | Writer | Checker | Next |
|---|---|---|---|---|
| day_ahead_prices | APPROVED: review 2 left one major ("afternoon" should be "evening": the 19:53 UTC fetches), which the seat fixed, mirrored and rebuilt | a3832f1aa7ea3b06d | af7698a43e3be4872 | done |
| actual_generation | APPROVED (review 2); optional nits: B07 and B08 are also in the vendor list; "DE-LU" wraps at its hyphen at 1440 | a764d6bcc53324bb2 | aec318644be7fe476 | done |
| actual_load | APPROVED (review 2) | afa2e30d1849a63bd | a24ae1f85e1a79713 | done |
| wind_solar_forecast | APPROVED (review 2) | a21e8456c9ebdbc7f | a2f6ec605542e237d | done |
| generation_forecast | APPROVED (review 2) | a9ca9d520ca0d49ab | a6c61259813ce01e3 | done |
| cross_border_flows | APPROVED (review 2), line-cite nit applied by the seat | aaad21b6d79fe8b11 | abd692feda2530f4a | done |
| commercial_schedules | APPROVED (review 2) | a31494e4d83ddddc5 | a511e8538be41f2c9 | done |
| net_positions | APPROVED (4 nits; sign correction confirmed) | affea4b8af88a3d6b | a90d8f640060a2b41 | done |
| net_transfer_capacity | APPROVED (review 2); a dead domain link in the note body is left for the seat (it is not on the page) | af6a9dcd642a89a55 | a57d6b2c71914570c | done |
| auction_revenue | APPROVED (review 2); nit: the A03 citation says §4.3 but should be §4 | a745ee86e95b1e284 | a0f2a1125adccad7d | done |
| capacity-allocated-nominated (family, lead total_capacity_allocated) | written (allocated into GB from NL and BE, 14 to 21 Sep; ships with the A07-only loss stated); APPROVED on re-check (all 8 findings fixed; review-2) | aa5201e596dbf26ce | a455406fcf3b6a9f0 | done |
| dc_link_intraday_transfer_limits | APPROVED: the checker said REVISE, not hold, with one major (summary implied all 8 pairs are DC). The seat fixed it within the 22-word budget, then mirrored and rebuilt. 3 nits left | aafc74fa32a44daac | a8e78e2d10063228c | done |
| group 2 rest: dc_link_intraday_transfer_limits | queued | — | — | writers |
| current_balancing_state | HELD blank (ruling #41): silver has no zone, no sign and wrong times (13l). The note body was corrected but is unchecked | aff7fcf8159bb3639 | — | after the gridflow fix: page block, then checker |
| procured_balancing_capacity | HELD blank (ruling #42): silver rows are arbitrary picks across 4 countries (13o). The note body was corrected but is unchecked | a7d2508a74e6ebbfa | — | after the gridflow fix |
| balancing-energy-bids (family, lead balancing_energy_bids) | **HELD** (ruling #44): lead stops at 100 series and drops BE bids at dedup; aggregated area blank. Note edits in both notes and mirrors go to a held branch at PR time | a963682b7f587ae52 | — | held |
| congestion-management (family, lead redispatching_internal) | written (NL internal redispatch, down series only, 15-21 Sep); seat: ships with the direction loss stated (as A07); checker running | a696043a3c83b78e1 | a40db70347a68ee3a | verdict |
| actual_generation_units | REVISE (2 blockers: unlabelled wrong sample rows; 'single-unit plants' advice unsafe in FR); writer resumed | aa26b6043c67cd777 | a307fc1083fa679bf | re-check |
| generation_units_master_data | written (unit count by type, 6 zones, no MW); seat: event_time stays in the key, 'Smaller types' label ok; checker running | a20a17cf260cfe31f | a9307d180d54daee9 | verdict |
| installed_capacity | written (DE-LU 2026 capacity by type, bar; 4 zones, daily repeats noted); checker running | ae278337fa1293ec8 | aadbd72a6a196372e | verdict |
| load-forecasts (family, lead load_forecast) | REVISE (1 major: loss stated only in codes, summary promises max/min; 4 nits); writer resumed | a0639f624b8567137 | a8fde62593ddf835d | re-check |
| installed_capacity_units | writer running | abc4b218164a9acf8 | | report |
| water_reservoirs | written (FR only, 4 weekly points in two pieces); seat: ships thin-but-accurate with coverage stated; swap the blank-page test at PR time; checker running | ad11aa4256be63ae4 | a328b581d4bd66dc5 | verdict |
| still queued: forecast_margin, outages (family) | queued | | | writers as slots free (GIE checkers first) |

## At PR time

- `tests/test_dataset_page.py` uses `entsoe/water_reservoirs` as its blank-page example. If that page gets content,
  switch the test to a page that stays blank; `gie/lng` won't do, because its scenery text says "coming ashore".
- Held pages: restore their mirror notes from origin/main, and leave their artefacts out (same as netbsad and nonbm).
  **current_balancing_state** and **procured_balancing_capacity** are held, so keep its unchecked note-body edits out of both PRs and save them on a held branch.

## Seat items

**Remediation list (Bobbo 2026-09-29):** log each gridflow or data defect as it is found, in gridflow `.planning/BACKLOG.md`
item 13 and in the vault page `10-projects/gridflow/specs/remediation-from-site-batches.md` (on the branch for PR quant-vault#55).
Logged so far: 13a to 13af.

- Ruling #39, amended by #40: EIC codes in a note's front matter use `-` escapes (the vault scripts split the note on `---`).
  The build now rejects a literal one: guard in `page_fields.parse_page_fields`, tests in `tests/test_front_matter_fence.py`,
  on this branch. Rows and body stay plain, and the dash advisory is accepted. `published_at` is the fetch time.
- Template fix, on this branch: in `theme.css`, `.nb-tab` now truncates with an ellipsis and `.nb-kern` no longer shrinks, so
  long `.ipynb` names stop clipping `gridflow_models` at 390. Check it at 390 on generation_forecast.
- gridflow: the ENTSO-E code comment calls `published_at` a "leak-proof forecast issue time", but it is the response's
  createdDateTime, within seconds of the fetch. The parser files `outBiddingZone_Domain` series under the same zone, so the
  dedup keeps the later series (seen on BE, 8 Sep; from generation_forecast).
- gridflow (from actual_generation): where ENTSO-E sends a separate consumption series for a production type, silver
  keeps whichever row arrives last, with nothing recording which. 19,623 of 100,831 rows hold consumption, not
  generation (NL gas reads about 140 MW against more than 7,000 MW generated). The page ships with this stated and a
  chart that avoids it (seat, same as boal and pn). Add to gridflow BACKLOG at close.
- Branch commits: `e33083c`, the front-matter guard now reads the raw text only, so escaped codes work anywhere (tests in
  `test_front_matter_fence.py`; the old value checks were removed); `0055438`, the notebook tab truncates.
- gridflow (from cross_border_flows): gridflow requests one direction per border for eight pairs (`client.py:40-49`),
  so silver can't show both directions. `in_area_code` is the receiving zone; the note said the opposite.
- gridflow (from day_ahead_prices): DE-LU gets two numbered price sequences per delivery day, up to 322 EUR/MWh apart,
  and silver keeps whichever the document lists last, so the stored series mixes them. The page leaves DE-LU out of the
  chart and rows and says so; it ships with that caveat.
- Template gap (from net_positions): the chart spec cannot negate a value by a direction column, so a signed line is
  impossible when ENTSO-E sends size plus direction. The page uses two stacked bands instead.
- gridflow and vault (from net_transfer_capacity): FR to BE and FR to DE-LU returned "No matching data" on all 19 days, so
  2 of the 8 requested pairs are dead requests. The vault note said NTC caps flow, but flow exceeds NTC in 141 of 432 hours
  on NL from DE-LU. The note is fixed in the batch.
- Template (from dc_link): wrapped `code` in `notebook.lead` does not break at 390, so the writer reworded to fit. It needs
  an `overflow-wrap` rule on lead code.
- Front-end bug (from capacity-allocated-nominated): the notebook runner gives a DataFrame with a named index a misaligned
  header (the #49 fix covers the plain index only). The writer worked around it with `.reset_index()`. Fix it in
  `build._output_html`.
