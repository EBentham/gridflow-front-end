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
- **Pause on new writers (18:34 UTC, 59% used, 1h16m left, rising about 12 points per 7 minutes):** in-flight pages finish
  their checks and revisions. Groups 3 and 4 start after the 19:50 UTC reset.

## Per page (agent ids resume with SendMessage)

| Page | State | Writer | Checker | Next |
|---|---|---|---|---|
| day_ahead_prices | Revision 1 done; re-check running | a3832f1aa7ea3b06d | af7698a43e3be4872 | verdict |
| actual_generation | REVISE (blocker: point time; majors: defect understated, cadence as rule); writer revising | a764d6bcc53324bb2 | aec318644be7fe476 | verdict |
| actual_load | APPROVED (review 2) | afa2e30d1849a63bd | a24ae1f85e1a79713 | done |
| wind_solar_forecast | APPROVED (review 2) | a21e8456c9ebdbc7f | a2f6ec605542e237d | done |
| generation_forecast | APPROVED (review 2) | a9ca9d520ca0d49ab | a6c61259813ce01e3 | done |
| cross_border_flows | Revision 1 done; re-check running | aaad21b6d79fe8b11 | abd692feda2530f4a | re-check |
| commercial_schedules | written (into GB from FR, BE, NL, IE-SEM, hourly, 14 to 20 Sep); checker running | a31494e4d83ddddc5 | a511e8538be41f2c9 | verdict |
| net_positions | writer running | affea4b8af88a3d6b | — | checker |
| net_transfer_capacity | writer running | af6a9dcd642a89a55 | — | checker |
| auction_revenue | writer running | a745ee86e95b1e284 | — | checker |
| capacity-allocated-nominated (family, lead total_capacity_allocated) | writer running | aa5201e596dbf26ce | — | checker |
| dc_link_intraday_transfer_limits | writer running (thin: 24 rows, 1 to 5 Aug) | aafc74fa32a44daac | — | checker |
| group 2 rest: dc_link_intraday_transfer_limits | queued | — | — | writers |
| group 3: current_balancing_state, procured_balancing_capacity, balancing-energy-bids, congestion-management, actual_generation_units, generation_units_master_data | queued | — | — | writers |
| group 4: installed_capacity, installed_capacity_units, water_reservoirs, forecast_margin, load-forecasts, outages | queued | — | — | writers |

## At PR time

- `tests/test_dataset_page.py` uses `entsoe/water_reservoirs` as its blank-page example. If that page gets content,
  switch the test to a page that stays blank; `gie/lng` won't do, because its scenery text says "coming ashore".
- Held pages: restore their mirror notes from origin/main, and leave their artefacts out (same as netbsad and nonbm).

## Seat items

**Remediation list (Bobbo 2026-09-29):** log each gridflow or data defect as it is found, in gridflow `.planning/BACKLOG.md`
item 13 and in the vault page `10-projects/gridflow/specs/remediation-from-site-batches.md` (on the branch for PR quant-vault#55).
Logged so far: 13a to 13h.

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
