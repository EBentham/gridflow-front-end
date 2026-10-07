# Tracker: last 19 dataset pages (opened 2026-10-06)

Brief: `.planning/v5/p26/BATCH-rest.md`. Ruling #49. Worktrees under this session's scratchpad
(`...\5fec4a50-7518-4657-b815-ed1434a34580\scratchpad\p26-rest` and `...\vault-p26-rest`).
Writers Opus 5.5 · high; checkers Sonnet 5.5 · high (`model: sonnet`). Max 6 agents running at once until 2026-10-06 ~20:15; then **max 2** (Bobbo: let it run overnight, ~60% of the 5-hour window used).

| # | Page | Writer agent | Checker agent | State |
|---|---|---|---|---|
| 1 | openmeteo/demand-weather | ac1ad6e5a5e605705 | ac27d88b5ab5e7ecb | **APPROVED, nits fixed** |
| 2 | openmeteo/wind-weather | ae9cfe6ad7881da29 | a2df0f9d5aabe5779 | **APPROVED, nits fixed** |
| 3 | openmeteo/solar-weather | a5706f8ebd6b34d3b | a2444531a1dcca8d2 | **APPROVED** (review-2) |
| 4 | neso_data_portal/historic_generation_mix | a42efd78868f6a132 | af643d9360ae06335 | **APPROVED, nits fixed** |
| 5 | neso_data_portal/embedded_wind_solar_forecast | af56914fc30342023 | aac8b54e5b7600c54 | REVISE 1 (catalogue: hourly, 14 days ahead, recommends Jun-Dec resource; seat ruled state both) -> **APPROVED, nits fixed** |
| 6 | neso_data_portal/daily_wind_availability | a6af0bb32a7e89c85 | a901892479a69716d | **APPROVED** (review-2) |
| 7 | neso/national-carbon-intensity | a9024c9f403f98608 | a73facf34e652838b | REVISE 1 (major: carbon_intensity note lines 223, 251 still advise forecast as ex-ante feature; fix in note + 8 nits; gold view comment same wording -> log as gridflow defect) -> **APPROVED** (review-2) |
| 8 | neso/intensity-statistics | a3afb6492f56c9279 | af2296146eeb3a8e4 | **APPROVED, nits 2-6 fixed** (nit 1 ruled no change) |
| 9 | neso/intensity_factors | a76df4f3995c37c73 | a6ff67be70686a477 | REVISE 1 (majors: how_used[2] revision-spotting not deliverable; how_used[0] mix weighting must say approximate: gas/imports factors split) -> **APPROVED, nit fixed** |
| 10 | neso/regional-carbon-intensity | a01430cfb5e2746c8 | a56743096cc4f545a | REVISE 1 (majors: GB key note needs figures/observation wording; notebook legend covers S Wales peak) -> **APPROVED, nit fixed**. Look hardest: one-day transform command (bronze filed under window's first day, carbon_intensity.py:87-154); GB key 'not the national forecast' (within 17 of national actual, up to 173 off national forecast); regional has no actual; members agree exactly |
| 11 | neso/generation-mix | a4df38f28b134e7a5 | a6693b1164025dae8 | REVISE 1 (majors: offset holds for gas/wind/imports/biomass only, solar at zero lag; imports note fails 42/213, 1.9 pt below portal) -> **APPROVED, nits fixed**. Look hardest: 30-min offset (row from=T tracks metered half-hour T+30 vs fuelhh and DP mix); wind incl embedded, hydro incl pumped storage, imports gross; denominator undocumented; stacks 99.8-100.2 |
| 12 | entsog/nominations-allocations | a82af5895913647fa | aace40f62cc7dc57b | **APPROVED, nits fixed** (compact ticks confirmed at 390; broken vault link to gas-nominations.md pre-existing, seat item) (writer's hold = 390 axis clip only; seat FIXED compact ticks, rebuild then check). Look hardest: key (dedup on vendor id = 4 key cols + indicator + unit); Moffat entry asked of National Gas TSO is empty; BBL filters return nothing; NG allocation rows are not-applicable placeholders |
| 13 | entsog/capacity-by-indicator | a514d2addd9a46f1e | (none: held) | **HOLD** (ruling #52: generic silver drops records whose validity doesn't start on the fetched day, generic.py:157-161,332). At ship: park its 10 notes + page block + artefacts on `v5/p26-entsog-gas-held` / `docs/v5-p26-entsog-gas-held`, restore origin versions on the ship branches so the page renders blank. |
| 14 | entsog/gas-quality | a9802e0851424abd9 | a17f638c1646d59e3 | **APPROVED** (review-2) |
| 15 | entsog/aggregated_physical_flows | a898082c0f4774258 | a7d9fe5b7e3cc0f09 | **APPROVED** (review-3; sample to regenerate after the `|` sampler fix) |
| 16 | entsog/cmp | aa198e1b410597f33 | (none: held) | **HOLD** (ruling #53). Writer edited nothing; page stays blank. Defects in cmp-author.md. |
| 17 | entsog/tariffs-and-simulations | ad8672822a5dd3135 | a873752c769e7732f | REVISE 1 (repeats ruling met; majors: simulation meaning + text/N-A, folded frame no price, NG TSO omission stated, Transgaz zero claim false) -> **APPROVED, nits fixed**. Seat ruling: identical per-day repeats of a static register ship if copies identical + page says so; any differing copy = hold. |
| 18 | entsog/reference-data | a63e00eb1ac0dfe8f | a3e8042348406f4b5 | **APPROVED** (review-3; sample to regenerate after `|` fix) |
| 19 | entsog/urgent_market_messages | a446373239566cba7 | abaeb209d2da41d9d | REVISE 1 (majors: snapshot not history unstated; placeholder capacities; last_update wording) -> **APPROVED, nits fixed** (writer: ship, 133=133; 101 messages in 133 versions) |

## Defects logged

- Item 15 Open-Meteo 15a-15g and item 16 NESO Data Portal 16a-16h: logged to gridflow BACKLOG + vault remediation page (committed and pushed on `docs/v5-p26-rest`). Next: 17 NESO carbon intensity, 18 ENTSOG.

## Seat fixes on the branch

- theme.css `.ds-chip`: wraps long key chips (clipped at 390 px). Verify at the local review build.
- build.py + dataset.html.j2: member headings drop the invented uppercased-slug code (affects live GIE/ENTSOG families too).
- chart_svg.py: spans over 400 days tick on 1 January, labelled by year (9 wide, 4 narrow). Tests 107 green.
- openmeteo.json hub: ERA5 -> archive (reanalysis + forecast blend); demand cities UK (Belfast), wind/solar GB.
- hero chips use the `breakable` filter (wrap at _ and /); tests updated; 107 green.
- build.py request_lines: comma lists in a request get <wbr> after each comma (hourly= wraps cleanly).

- chart_svg.py fmt_num: axis steps >= 1e5 print compact ticks (50M, 0.3M, 2bn); fixes ENTSOG 390 clipping. Rebuild ENTSOG pages to pick it up.
- sample.py `_scan`: per-file scan + concat diagonal_relaxed, newest file's columns (ENTSOG Null-vs-String columns across daily files broke gridflow-sample).
- chart_svg.py: unit label shifts right when wider than the left margin (gCO2/kWh clipped at 390).

- page_fields.py FAMILY_MEMBERS (2, 12) -> (2, 18) for regional carbon intensity.
- Local preview: launch.json `rest-review` on 9670 serving this worktree's site/hifi (full build passed 20:15).

## Collected for the end-of-batch template pass (one subagent, before the local build)

- tests/test_dataset_page.py:219 `test_a_page_without_a_page_block_is_blank` uses `neso/national-carbon-intensity` as the blank family example; that family now has a page block. Move the example to a held family (e.g. an ENTSO-E held family) like 1b6ed6e did.

- A series at 0 throughout draws under the x axis (North Scotland on regional-carbon-intensity): give line charts a little headroom below 0, or draw series above the axis line.
- Overlapping chart lines (gas-quality: series with identical values hide each other) and the folded sample table at 390: look at both in the template pass.
- sample.py polars_text (lines ~67-87) can't read back values containing `|` (ENTSOG points_names). Fix, then REGENERATE `entsog/aggregated_physical_flows` sample with the official command and rebuild.
- Related-dataset line 'summed by balancing zone' in `physical_flows` (live) and `nominations` notes overstates aggregated_physical_flows (3 entry sources only). Reword in both canonical notes + mirrors.
- Column guide squeezes meanings to ~150 px at 1440 on long guides (entsog/reference-data).
- Regenerate `entsog/reference-data` (operators) sample after the `|` sampler fix too.
- Percent charts: y axis runs past 100 (125 desktop, 150 at 390) on stacked shares (generation-mix); cap a percent axis at 100.

## Seat working rule (Bobbo, 2026-10-06)

Keep the seat context thin: no seat spot-checks (checkers reproduce numbers); collect template issues for one end-of-batch subagent; short relays.

## RESUMED 2026-10-07 02:03 (one agent at a time). Was: PAUSED (Bobbo, 2026-10-06 ~22:00): 12 of 19 approved. Resume at 02:00 on 7 Oct (session cron) with ONE agent at a time, sequentially (ruling #51), until all 19 pages + the map are done, then the end-of-batch template pass, the full local build and gates, and hand Bobbo the localhost link. Nothing is pushed until he approves.

## Launch queue (cap 2; revisions and re-checks first)

4. Writers 13 to 19 (ENTSOG) in table order, each followed by its checker and revise loop before the next starts.
5. Map subagent DONE (map-author.md: gates green; Triton Knoll answered cell 17.7 km, on the coast, caveat stated, to backlog). Checker REVISE (table clipped beside map 1240-1420 and ~768; 6 nits). Revision 1 done (breakpoint 1440, real site names via map_svg.SITE_NAMES, 133 tests pass). Review 2 APPROVE (8 farm names unverified against operator pages; flag to Bobbo). MAP DONE.
6. DONE (139 tests, gates green; ruff drift pre-exists on origin/main). Holds parked to scratchpad/held-capacity (14 files; mirror notes restored to origin/main). Full build + check + htmlhint + lychee green. 9670 serving. Defects logged: 17a-17q (34ac67b), 18a-18w (b150fb0), 15h (7424062) on docs/v5-p26-rest; gridflow BACKLOG.md edits local, uncommitted. Vault canonical capacity notes parked to scratchpad/held-capacity/vault-canonical, restored to origin/master (== mirror). SHIPPED 2026-10-07: PR #57 squash c2c6027, deploy green and live; vault PR #59 merged fadf53d; held branches v5/p26-entsog-gas-held + docs/v5-p26-entsog-gas-held pushed; ruling 54. End-of-batch template pass -> v5/p26/TEMPLATE-PASS.md (one Opus subagent, + DESIGN.md map clause: the 'Collected' list), then full build + gates, refresh preview (launch.json rest-review, 9670), tell Bobbo.

## Map extension: APPROVED (ruling #50), spec `.planning/v5/p26/MAP-weather-locations.md`; runs after writer 19, before the template pass

Open-Meteo locations section on the 3 weather pages: inline SVG UK+Ireland outline (Natural Earth 1:50m, simplified ~15 KB), markers at gridflow's configured coordinates + faint dot at the answered grid cell, hover/tap card, linked table beneath (no-JS, a11y); stats from silver (demand: mean temp, coldest hour, HDD/yr; wind: mean 100 m speed + high percentile; solar: mean daily irradiation, sunniest/darkest month). No tiles/third parties. One Opus subagent after the 19 pages, before the local review.

## Holds

- entsog/capacity-by-indicator (ruling #52).
- entsog/cmp (ruling #53), nothing to park.


## Compaction checkpoint (2026-10-07 ~03:40)

Done: rows 1-12, 14, 15 approved; 13 held. Next: writer 16 cmp (running), then 17 tariffs, 18 reference-data, 19 urgent_market_messages, each writer -> Sonnet checker -> revise loop, ONE agent at a time. Then map (MAP-weather-locations.md), template pass (Collected list), defect logging items 17 (NESO carbon intensity) + 18 (ENTSOG) from the reports' Defects sections, park held capacity notes, full build + gates, refresh 9670, tell Bobbo. No push.
