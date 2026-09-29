# Dataset fan-out: ENTSO-E batch (24 pages)

Opened on 2026-09-29, after Bobbo said "yes" to the next vendor batch and then asked to "increase the speed... spin up more agents in parallel".

- **Agents:** each page gets a writer and a checker, both Opus 5.5 · high.
- **Limits:** up to **6 agents at once**, and no launches once the 5-hour window passes about 92%.
- **Ship rule (ruling #36):** the batch goes to main once every page is APPROVED and the gates are green. Held pages stay blank.

## Where things are

- **Front-end worktree** (build, artefacts, mirror): `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\a0012501-ff9a-440a-b654-cec67ac10bcf\scratchpad\p26-entsoe`
  - Branch `v5/p26-entsoe`, off `main` after the Elexon ship.
  - The `.venv` is synced with the `build` and `distil` extras.
- **Vault worktree** (canonical notes): `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\a0012501-ff9a-440a-b654-cec67ac10bcf\scratchpad\vault-p26-entsoe`
  - Branch `docs/v5-p26-entsoe`, off quant-vault `origin/master`.
  - Notes are at `30-vendors/entsoe/datasets/<dataset>.md`. They use CRLF line endings, so edit them with the Edit tool.
- **Mirror copy:** `vault/entsoe/<dataset>.md` in the front-end worktree. After every edit, copy it from the vault note byte for byte.
  - Four canonical notes are newer than the mirror because they carry live-probe findings: `aggregated_balancing_energy_bids`, `balancing_energy_bids`, `balancing_financial_expenses_income` and `congestion_management_costs`.
  - Canonical wins, so copying brings those findings in.
- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\v5\p26\entsoe\`
  - Writer: `<page>-author.md`.
  - Checker: `<page>-review.md`, then `-review-2.md` and so on for re-checks.
- **Rules:**
  - Writer: `.planning/v5/author-brief.md`.
  - Checker: `.planning/v5/review-rubric.md`.
  - Look and anatomy: `DESIGN.md`, section "Dataset page anatomy".
- **Worked examples:** the live Elexon pages. Their notes are in `vault/elexon/` and their pages under `site/hifi/data-sources/elexon/`.
  - `fuelhh`: a stacked area.
  - `system_prices`: a price line.
  - `bmunits_reference`: a register with no time axis.
  - `demand-forecasts`: a family led by `ndf`.
  - `remit`: an event register.
  - `fou2t14d`: a forecast across publishes.
- **Data truth:** the ENTSO-E rows of `.planning/v5/DATA-MATRIX.md`.
  - Local silver is at `C:\gridflow-data\silver\entsoe\<dataset>\`. It is read only.

## The 24 pages

| Group | Pages | Ports |
|---|---|---|
| 1 | `day_ahead_prices`, `actual_generation` (the cross-vendor proof), `actual_load`, `wind_solar_forecast`, `generation_forecast`, `cross_border_flows` | 9801 to 9806 |
| 2 | `commercial_schedules`, `net_positions`, `net_transfer_capacity`, `auction_revenue`, `capacity-allocated-nominated` (family), `dc_link_intraday_transfer_limits` | 9811 to 9816 |
| 3 | `current_balancing_state`, `procured_balancing_capacity`, `balancing-energy-bids` (family), `congestion-management` (family), `actual_generation_units`, `generation_units_master_data` | 9821 to 9826 |
| 4 | `installed_capacity`, `installed_capacity_units`, `water_reservoirs`, `forecast_margin`, `load-forecasts` (family), `outages` (family) | 9831 to 9836 |

Each family's slug, title and members are fixed in `site/hifi/data/entsoe.json`.
- The first member is the lead, and the lead's note carries the `page:` block.
- Build a family with `--only entsoe/<lead>`. The family slug on its own renders nothing.

| Family | Members (lead first) |
|---|---|
| `load-forecasts` | load_forecast, load_forecast_weekly, load_forecast_monthly, load_forecast_yearly |
| `outages` | outages_generation, outages_production, outages_consumption, outages_transmission, outages_offshore_grid |
| `congestion-management` | redispatching_internal, redispatching_cross_border, countertrading, congestion_management_costs |
| `capacity-allocated-nominated` | total_capacity_allocated, total_nominated_capacity |
| `balancing-energy-bids` | balancing_energy_bids, aggregated_balancing_energy_bids |

## Shared-worktree rules (up to six agents in the one worktree)

- **Your files only.** Touch only your own dataset's files:
  - its vault note(s) and their mirror copies;
  - `site/hifi/data/{series,samples,notebooks}/entsoe/<dataset>*`;
  - its built page.
- **Hands off shared files.** Never edit the template, CSS, Python, `entsoe.json` or another dataset's files. Report a template problem instead.
- **Contention.** A DuckDB lock or a busy notebook kernel means another agent is running. Wait a minute and retry.
- **Screenshots.**
  - Use headless Chrome with your own `--user-data-dir` under the scratchpad, or a static server on your port.
  - **Wrap every Chrome call in `timeout 60`, with `--timeout=15000 --virtual-time-budget=5000`.** A hung call once stalled an agent for an hour.
  - Chrome won't render below 500 px, so a true 390 check needs a 390 px iframe.
  - Stop any server you start.
- **Cleanup.** Never delete a directory whose path is built from a variable: the guard halts you. Leave Chrome profile folders in place.
- **Samples.** `gridflow-sample` needs eight rows. `record.select.columns` sets which columns print first; put the columns that tell rows apart first.
- **Thin data.** State a handful of rows or a single date plainly, in domain terms, and never invent a trend. If the rows can't build a page, say so in the report and the seat decides whether to hold it.
- **No git** in either repo. The seat commits, mirrors and merges.

## Seat rulings for this batch (ruling #39)

- **EIC codes (amended by ruling #40):**
  - **In the note's front matter** (the `page:` block, chart keys), a literal `---` is forbidden: the vault's scripts
    split the note on it. The build rejects it. Write the dashes as `\x2D` escapes inside a double-quoted YAML
    string, for example `"10YFR-RTE\x2D\x2D\x2D\x2D\x2D\x2DC"`; they render as ordinary dashes.
  - **In the sample rows and the note body** below the front matter, write codes plainly. Pick sample rows on merit,
    never to avoid codes.
  - **The detector's "em-dash overuse" finding** counts the `--` padding in rendered codes. It is advisory and
    accepted as long as the prose has no dashes. The detector gate is: no non-advisory findings.
- **`published_at` on ENTSO-E forecast tables:** it is the response's `createdDateTime`, within seconds of the fetch.
  - It is not the forecast's issue time. The gridflow code comment calling it one is wrong (a seat item).
  - Describe it as a fetch-time stamp.
- **Notebook header clip at 390:** a long `.ipynb` filename clips the `gridflow_models` label. This is template work that the seat fixes; leave it.
