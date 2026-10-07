# Dataset fan-out: the last 19 pages (Open-Meteo, NESO Data Portal, NESO carbon intensity, ENTSOG)

Opened 2026-10-06. Bobbo: "let's do all the remaining pages", with the plan approved in chat (ruling #49).

- **Agents:** each page gets a writer (Opus 5.5 · high) and a checker (**Sonnet 5.5 · high**). Revisions and
  re-checks go back to the same agents.
- **Concurrency:** at most 6 agents at once, rolling. No launches past about 85% of the 5-hour window.
- **Shipping:** nothing is pushed until Bobbo has looked at the full local build and approved it. Held pages stay blank.

## Where things are

- **Front-end worktree** (build, artefacts, mirror): `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\5fec4a50-7518-4657-b815-ed1434a34580\scratchpad\p26-rest`
  - Branch `v5/p26-rest`, cut from `main`. The `.venv` is synced with the build and distil extras.
- **Vault worktree** (canonical notes): `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\5fec4a50-7518-4657-b815-ed1434a34580\scratchpad\vault-p26-rest`
  - Branch `docs/v5-p26-rest`, cut from quant-vault `origin/master`.
  - Notes live at `30-vendors/<vault vendor>/datasets/<note>.md`. Edit them with the Edit tool, which keeps their CRLF line endings.
- **Mirror:** `vault/<site vendor>/<dataset>.md` in the front-end worktree. After every edit, `cp` the canonical note over
  it and check with `cmp` (git normalises line endings at commit; the copy must still be byte-equal on disk).
  - **Every mirror for these four sources is currently stale.** Your first mirror copy brings in whatever the canonical
    note already holds beyond the mirror (for example `historic-generation-mix` gained a `solar` composition section on
    2026-09-25). Read the canonical note, not the mirror, and treat that extra content as part of the page's truth.

  | Site vendor (`--only` prefix, mirror folder) | Vault folder | Note name differences |
  |---|---|---|
  | `openmeteo` | `open-meteo` | none |
  | `neso_data_portal` | `neso-data-portal` | canonical `historic-generation-mix.md` → mirror `historic_generation_mix.md`; `embedded-wind-and-solar-forecasts.md` → `embedded_wind_solar_forecast.md`; `daily-wind-availability.md` → `daily_wind_availability.md` |
  | `neso` | `neso` | none |
  | `entsog` | `entsog` | none |

- **Reports:** `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\v5\p26\<site vendor>\`
  - Writer: `<page>-author.md`.
  - Checker: `<page>-review.md`, then `-review-2.md` and so on for re-checks.
- **Rules:**
  - Writer: `.planning/v5/author-brief.md`.
  - Checker: `.planning/v5/review-rubric.md`.
  - Look and anatomy: `DESIGN.md`, section "Dataset page anatomy".
- **Worked examples** (all live on main, notes in this worktree's `vault/`):
  - `elexon/fuelhh`: a stacked area. `elexon/system_prices`: a price line.
  - `elexon/bmunits_reference`: a register with no time axis. `elexon/remit`: an event register.
  - `elexon/demand-forecasts` (lead `ndf`): a family.
  - `entsog/physical_flows`: the one live ENTSOG page; the closest example for every ENTSOG page.
  - `gie/storage` (family `agsi-storage`) and `gie/about_listing` (family `agsi-reference`, a register family).
  - ENTSO-E forecasts (`entsoe/` load and wind/solar forecast notes): forecast pages.
- **Data truth:**
  - The matching rows of `.planning/v5/DATA-MATRIX.md`.
  - Local silver, read only: `C:\gridflow-data\silver\{open_meteo,neso_data_portal,neso,entsog}\<dataset>\`.
  - gridflow code, read only: `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow\src\gridflow\`
    (`connectors/{openmeteo,neso_data_portal,neso,entsog}/`, `silver/<same>/`, `schemas/`).
  - The vendor README and `endpoints.md` under the vault's `30-vendors/<vault vendor>/`.

## The 19 pages

Families are fixed in `site/hifi/data/<site vendor>.json`; the lead (first member) carries the `page:` block. Build a
family with `--only <site vendor>/<lead>`, because the family slug renders nothing.

| # | Page | Members (lead first) | Writer port | Checker port |
|---|---|---|---|---|
| 1 | `openmeteo/demand-weather` | historical_demand, forecast_demand | 9861 | 9881 |
| 2 | `openmeteo/wind-weather` | historical_wind, forecast_wind | 9862 | 9882 |
| 3 | `openmeteo/solar-weather` | historical_solar, forecast_solar | 9863 | 9883 |
| 4 | `neso_data_portal/historic_generation_mix` | single | 9864 | 9884 |
| 5 | `neso_data_portal/embedded_wind_solar_forecast` | single | 9865 | 9885 |
| 6 | `neso_data_portal/daily_wind_availability` | single | 9866 | 9886 |
| 7 | `neso/national-carbon-intensity` | carbon_intensity, intensity_at, intensity_current, intensity_date, intensity_fw24h, intensity_fw48h, intensity_period, intensity_pt24h, intensity_today | 9867 | 9887 |
| 8 | `neso/intensity-statistics` | intensity_stats, intensity_stats_block | 9868 | 9888 |
| 9 | `neso/intensity_factors` | single | 9869 | 9889 |
| 10 | `neso/regional-carbon-intensity` | regional_intensity + 17 more (see `neso.json`) | 9870 | 9890 |
| 11 | `neso/generation-mix` | generation, generation_current, generation_pt24h | 9871 | 9891 |
| 12 | `entsog/nominations-allocations` | nominations, renominations, allocations | 9872 | 9892 |
| 13 | `entsog/capacity-by-indicator` | firm_available + 9 more (see `entsog.json`) | 9873 | 9893 |
| 14 | `entsog/gas-quality` | gcv, wobbe_index, methane_content, hydrogen_content, oxygen_content | 9874 | 9894 |
| 15 | `entsog/aggregated_physical_flows` | single | 9875 | 9895 |
| 16 | `entsog/cmp` | cmp_auction_premiums, cmp_unavailable_firm_capacity, cmp_unsuccessful_requests | 9876 | 9896 |
| 17 | `entsog/tariffs-and-simulations` | tariffs, tariff_simulations | 9877 | 9897 |
| 18 | `entsog/reference-data` | operators, balancing_zones, connection_points, interconnections, aggregate_interconnections, operator_point_directions | 9878 | 9898 |
| 19 | `entsog/urgent_market_messages` | single | 9879 | 9899 |

`entsog/interruptions` has no page (the vendor returns no result); leave it alone. The owner's review server, when
running, is on port **9670**: never stop it.

## Known risks to check first

- **Open-Meteo:** history runs back to 2021; forecasts cover 1 Aug to 22 Sep. Establish what one row is (location,
  variable, time), which locations and variables gridflow requests, the time zone and the time-stamp meaning from the
  connector, and whether forecast rows keep the run they came from or are overwritten by later fetches.
- **NESO Data Portal:** `historic_generation_mix` holds 930k rows from 2009; establish the key, the settlement-period
  versus timestamp convention, and what the canonical note's `solar` composition section establishes.
  `embedded_wind_solar_forecast` and `daily_wind_availability` cover two weeks: establish the forecast issue stamp
  versus the target time, and what a row of availability is.
- **NESO carbon intensity:** many members are a single snapshot or a 1 to 2 day window. Expect thin but accurate
  wording. Establish units (gCO2/kWh), the intensity index bands, actual versus forecast fields and how gridflow stores
  them, and whether the regional members are the same data reached by different routes.
- **ENTSOG:**
  - Units come from the rows (`unit` columns) or the code, never memory; ENTSOG mixes kWh/d and other units.
  - `capacity-by-indicator`: the four "available through" members cover only 31 Jul to 4 Aug, while the firm and
    interruptible members run 1 Aug to 21 Sep.
  - `cmp`: the CMP tables cover 31 Jul to 4 Aug, and **known defect 8a**: `cmp_unsuccessful_requests` has null
    `timestamp_utc`/`event_time` on all 5,197 rows (`silver/entsog/generic.py` about lines 185 to 187; fixed only on
    the unmerged gridflow branch `fix/silver-entsog-cmp-timestamp`). Reproduce it first; the page must not imply that
    member has times. Recommend a hold if the family cannot be honest without it.
  - `reference-data`: registers with no time axis.
  - `tariffs-and-simulations`: 61k and 14k rows over one tariff year (Oct 2025 to Apr 2026); state currency and units
    from the rows.
  - `urgent_market_messages`: 133 messages, 2021 to 2026, an event register.

## Shared-worktree rules

- **Your files only:**
  - your dataset's canonical vault notes and their mirror copies;
  - `site/hifi/data/{series,samples,notebooks}/<site vendor>/<dataset>*`;
  - your built page.

  Never edit the template, CSS, Python, `<vendor>.json` or another dataset's files. Report a template problem instead.
- **Contention:** a DuckDB lock or a busy notebook kernel means another agent is running. Wait a minute, then retry.
  Large silver (NESO regional, NESO Data Portal history, ENTSOG tariffs): read with Polars lazily and select columns.
- **Screenshots:**
  - Use headless Chrome with your own `--user-data-dir` under the scratchpad, or a static server on your port.
  - **Wrap every Chrome call in `timeout 60`, with `--timeout=15000 --virtual-time-budget=5000`.**
  - A true 390 check needs a 390 px iframe.
  - Stop any server you start.
- **Cleanup:** never delete a directory whose path is built from a variable, because the guard halts you. Leave Chrome profile folders in place.
- **Samples:** `gridflow-sample` needs eight rows. `record.select.columns` sets the print order; put the columns that tell rows apart first.
- **Notebooks** run with the gridflow_models interpreter via `scripts/run_notebooks.py --dataset <site vendor>/<ds>`.
- **Thin data:** state a handful of rows or a narrow window plainly, in domain terms, and never invent a trend. If the rows can't support a page, say so and the seat decides whether to hold it.
- **Defects:** report every gridflow or data defect in your final message, and in a "Defects" section of your report
  written so it can be pasted into the backlog as is. The seat logs them.
- **No git writes** in either repo (read-only `git diff`/`git show` is fine). The seat commits, mirrors and merges.

## Seat rulings carried over

- **No literal `---` in front matter** (ruling #40). Write any dashes there as `\x2D` escapes in a double-quoted string.
- **Time stamps:** say what a stamp truly is, from the code. Never call a fetch or ingest stamp a publish or issue time.
- **Point times and cadence:** a point's time comes from the code. State cadence "as sent in the responses we hold",
  never as a vendor rule, and scope observations the same way.
- **Ship or hold:** ship with the loss stated when the chart and sample rows avoid the defect and the page says
  plainly what silver loses. Hold when silver misleads overall: repeated rows, arbitrary picks, wrong stamps, a lost
  sign on the main value. Thin but accurate ships.
- **Units** come from code or the vendor, never memory. Never mix units on one axis.
- **Public copy:** no planning words ("yet", "soon", "planned", "coming", "not yet"), no local-data references, no
  bare codes, plain English. Related links to held pages are allowed.
- **Detector:** the gate is no non-advisory findings. The em-dash-overuse advisory is accepted only when codes or CLI
  flags trigger it and the prose uses no dashes. Real em dashes in a page must number 0.
