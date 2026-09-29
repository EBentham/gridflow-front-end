# ENTSO-E batch: live tracker (opened 2026-09-29)

- **Brief:** `.planning/v5/p26/BATCH-entsoe.md`.
- **Reports:** `.planning/v5/p26/entsoe/`.
- **Worktrees:** in the session scratchpad.
  - `p26-entsoe` on branch `v5/p26-entsoe`.
  - `vault-p26-entsoe` on branch `docs/v5-p26-entsoe`.
  - If the scratchpad is cleared, recreate both from GitHub.
- **Throttle (Bobbo 2026-09-29):** "increase the speed... spin up more agents in parallel".
  - Up to 6 agents at once.
  - No launches above about 92% of the 5-hour window. The window resets at 19:50 UTC.
- **Ship:** under ruling #36, as with Elexon.

## Per page (agent ids resume with SendMessage)

| Page | State | Writer | Checker | Next |
|---|---|---|---|---|
| day_ahead_prices | writer running | a3832f1aa7ea3b06d | — | checker |
| actual_generation | writer running | a764d6bcc53324bb2 | — | checker |
| actual_load | writer running | afa2e30d1849a63bd | — | checker |
| wind_solar_forecast | writer running | a21e8456c9ebdbc7f | — | checker |
| generation_forecast | writer running | a9ca9d520ca0d49ab | — | checker |
| cross_border_flows | writer running | aaad21b6d79fe8b11 | — | checker |
| group 2: commercial_schedules, net_positions, net_transfer_capacity, auction_revenue, capacity-allocated-nominated, dc_link_intraday_transfer_limits | queued | — | — | writers |
| group 3: current_balancing_state, procured_balancing_capacity, balancing-energy-bids, congestion-management, actual_generation_units, generation_units_master_data | queued | — | — | writers |
| group 4: installed_capacity, installed_capacity_units, water_reservoirs, forecast_margin, load-forecasts, outages | queued | — | — | writers |

## At PR time

- `tests/test_dataset_page.py` uses `entsoe/water_reservoirs` as its blank-page example. If that page gets content,
  switch the test to a page that stays blank; `gie/lng` won't do, because its scenery text says "coming ashore".
- Held pages: restore their mirror notes from origin/main, and leave their artefacts out (same as netbsad and nonbm).

## Seat items

_none yet_
