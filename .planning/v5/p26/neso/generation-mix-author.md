# Writer report: `neso/generation-mix` (members `generation`, `generation_current`, `generation_pt24h`)

Writer: Opus 5.5, 2026-10-06. Screenshot port 9871 (server stopped after use).

**Status:** build `--only neso/generation` is clean, detector `[]`, real em dashes 0. **Recommend SHIP.** The one thing
the seat may rule differently is the 30-minute stamp offset (see "Look hardest at").

- **Chart:** stacked area of `generation_percentage` by `fuel` (nine series), silver `neso/generation`, every half-hour
  of 14 to 20 September 2026 UTC (336 points per series). The stacks sum to 99.8 to 100.2.
- **Frame:** the half-hour from 12:00 UTC on 20 September 2026, 8 of its 9 fuels (`other` left out). It prints
  `fuel, generation_percentage, timestamp_utc, period_end_utc` so the value survives the fold at 390.
- **Notebook:** `data.neso.query("generation", "2026-09-14", "2026-09-20")`, a head of nine rows, the per-half-hour
  total `describe()` (min 99.8, max 100.2), and a stacked area plot.

## How this differs from `neso_data_portal/historic_generation_mix`

They are two NESO generation mixes from two different NESO services.

| | This page (Carbon Intensity API) | `historic_generation_mix` (NESO Data Portal) |
|---|---|---|
| Values | Percent only (`perc`) | MW for 11 sources, their total and group totals, NESO's own percentages and a carbon intensity |
| Sources | Nine fuels. Embedded wind is folded into `wind` and pumped storage into `hydro` (both measured) | `wind_emb` and `storage` are separate columns |
| Stamps | NESO's `from`, 30 minutes before the metered half-hour it matches (measured) | `DATETIME` is the half-hour start (the approved note's check against fuelhh) |
| Access | A range route, up to 14 days a call | The whole file since 2009, republished per capture |
| History | Undocumented in the notes | From 1 January 2009, as NESO states |

Nothing on this page contradicts that note. My offset control relied on its finding that `DATETIME` is the half-hour
start (portal vs fuelhh gas, 0.996 at zero lag). Its `wind_emb`, `storage` and `imports` semantics are what my
composition checks compare against.

**Coverage note.** DATA-MATRIX lists `generation` as 31 Jul to 21 Sep. Silver is in fact two blocks with nothing
between them: 31 Jul 23:30 to 5 Aug 23:30 (241 half-hours, `generation_20260801.parquet`) and 12 Sep 23:30 to 21 Sep
23:30 (433, `generation_20260913.parquet`). That makes 674 half-hours × 9 = 6,066 rows. The chart window (14 to 20 Sep)
sits inside the second block, and the gap appears nowhere on the page.

## Files written

- Canonical notes (vault worktree, CRLF kept):
  - `30-vendors/neso/datasets/generation.md`: the `page:` block plus body corrections.
  - `generation_current.md` and `generation_pt24h.md`: body corrections only.
- Mirrors: `vault/neso/generation.md`, `generation_current.md` and `generation_pt24h.md`, copied with `cp` and checked
  byte-equal with `cmp`.
- Artefacts:
  - `site/hifi/data/series/neso/generation.json`: `spec_origin: vault`, 9 series × 336 points.
  - `site/hifi/data/samples/neso/generation.json`: written by `gridflow-sample`, eight rows.
  - `site/hifi/data/notebooks/neso/generation.json` and `generation-6.png`: from `run_notebooks.py`, 6 cells, no errors.
- Built page: `site/hifi/data-sources/neso/generation-mix.html`. The member pages `generation.html`,
  `generation_current.html` and `generation_pt24h.html` point to `#<member>`.
- No staged chart spec or authored override existed for these datasets.

## Evidence table

| Claim (where on the page) | Evidence |
|---|---|
| Row = one half-hour × one fuel; key `(timestamp_utc, fuel)` (facts.grain, record.key) | `_transform_generation` dedups `unique(subset=["timestamp_utc","fuel"], keep="last")`, `silver/neso/carbon_intensity.py:573-574`; silver has 0 duplicate keys in both files |
| Long form, one row per `generationmix` entry | `_extract_generation_rows`, `carbon_intensity.py:374-388` |
| `timestamp_utc` = vendor `from`, `period_end_utc` = vendor `to`, parsed `%Y-%m-%dT%H:%MZ` as UTC | `carbon_intensity.py:565-566, 643-649` |
| `generation_percentage` = vendor `perc` cast to Float64 | `carbon_intensity.py:569, 652-655` |
| Nine fuel names, lowercase as sent (record.fields.fuel) | Vault `30-vendors/neso/endpoints.md:79` ("fuel types documented by NESO: gas, coal, nuclear, biomass, hydro, imports, solar, wind, other"); bronze bodies send exactly those nine lowercase strings |
| One decimal; nine shares sum to 99.8 to 100.2 (alt, notebook output) | Committed series: stack min 99.8, max 100.2 over 336 points; notebook cell 5 `describe()` min 99.8, max 100.2 |
| `coal` 0 in every half-hour here (key note) | Committed series: coal min = max = 0.0 |
| Alt-text ranges: nuclear 8.8 to 15.5, gas 4.2 to 44.8, imports 0 to 22.4, wind 15.7 to 72.8, solar peak 32.3 on the 20th | Committed series min/max per key (solar max at 2026-09-20T13:00Z) |
| Responses run from the half-hour ending at `from` to the one ending at `to` (raw_feed.note, "checked") | Bronze `generation/2026/09/13/raw_20260926T174333Z_d2d0fdf9.json` for `…/2026-09-13T00:00Z/2026-09-22T00:00Z`: first `from` 2026-09-12T23:30Z, last `to` 2026-09-22T00:00Z (433 periods); the 1 Aug body likewise (241) |
| gridflow sends up to 14 days a call, inputs as path segments (raw_feed.note) | `_MAX_DAYS_PER_REQUEST = 14`, `connectors/neso/carbon_intensity.py:21, 149-161`; `_request(path, {})` sends no query params, `:68`; `build_path`, `endpoints.py:289-312` |
| Request URL `GET https://api.carbonintensity.org.uk/generation/2026-09-14T00:00Z/2026-09-21T00:00Z` | `endpoints.py:148-154` (`/generation/{from_dt}/{to_dt}`), `NESO_DATETIME_FORMAT = "%Y-%m-%dT%H:%MZ"` `:12`; sidecar `request_url` for the held body has the same shape |
| Ingest `--start 2026-09-14 --end 2026-09-21` = one call, one partition; transform `--start/--end 2026-09-14` | `runner.resolve_dates` bare date = midnight UTC, `pipeline/runner.py:479-501`; a single 7-day chunk; bronze `data_date=window_start.date()`, `carbon_intensity.py:79`; transformer reads the exact partition only, `silver/neso/carbon_intensity.py:141-154`; transform end inclusive, `runner.py:1126,1138` |
| Members: `generation_current` = `/generation`, no inputs; `generation_pt24h` = `/generation/{from}/pt24h`, with gridflow sending the ingest (chunk) start as `from` | `endpoints.py:135-147`; `_request_specs` `requires_window` false gives one call, `:132-133`; pt24h goes through the chunk branch, `:149-161` |
| pt24h covers the 24 hours before `from` | Held body for `from` 2026-08-01T00:00Z runs from the period ending 2026-07-31T00:00Z to the one ending 2026-08-01T00:00Z |
| Members agree on shared periods | `generation` and `generation_pt24h` share one half-hour (`from` 2026-07-31T23:30Z): all nine `perc` identical. `generation_current` (27 Sep 00:00) shares none |
| **`timestamp_utc` stamps sit 30 min before the metered half-hour they match** (what_it_is, caption, fields.timestamp_utc, related fuelhh) | Project check (below), Polars on silver. Correlation of half-hour differences, with this route's row at T set against the other at T+s. Columns are s = −30, 0, +30 and +60 min |
| | Gas share vs portal `gas_pct`: 0.52, 0.69, **0.98**, 0.68 |
| | Gas share vs fuelhh CCGT+OCGT MW: 0.46, 0.67, **0.93**, 0.66 |
| | Wind share vs portal `wind_pct`: 0.47, 0.62, **0.92**, 0.63 |
| | Wind share vs fuelhh WIND: 0.32, 0.46, **0.75**, 0.48 |
| | Imports share vs portal: 0.40, 0.10, **0.94**, 0.10 |
| | Biomass share vs fuelhh: 0.17, 0.50, **0.88**, 0.48 |
| | Control, portal gas MW vs fuelhh gas MW: 0.74, **0.996**, 0.75 (the portal's `DATETIME` is the half-hour start, per the approved historic note) |
| | `generation_pt24h` vs fuelhh, 49 points: gas 0.61, 0.76, **0.94**, 0.81; wind 0.04, 0.33, **0.80**, 0.27; biomass −0.48, 0.16, **0.89**, 0.22 |
| | `solar` is symmetric (0.91, 0.94, 0.91), so the test cannot place it; the page says "the metered fuels" only |
| Within the API, the mix and `carbon_intensity` share stamps (how_used, related carbon_intensity) | Gas share vs `carbon_intensity.actual_gco2_kwh` differences: 0.67, **0.88**, 0.61, 0.51 at s = −30, 0, +30 and +60 |
| `wind` includes embedded wind; key note says "tracks", not "matches" (what_it_is, key note) | At the +30 alignment: CI `wind` vs portal (`wind`+`wind_emb`)/`generation` MAE 1.16 points (mean +0.87); vs `wind`/`generation` MAE 7.51 (mean +7.51) |
| `hydro` includes pumped storage (what_it_is, key note) | At +30: CI `hydro` vs portal (`hydro`+`storage`)/`generation` MAE 0.07, p95 0.22; vs `hydro` alone MAE 0.51 (mean +0.50) |
| `imports` is not net (key note) | fuelhh interconnectors net negative in 31.6% of joined half-hours; CI `imports` there has median 2.0, mean 2.5, so it is not netted. Gross is not claimed: vs portal gross `imports_pct` MAE 1.88 with mean −1.86 |
| Denominator undocumented (what_it_is, fields) | The notes and vendor README quote no definition. NESO CI methodology May 2024 (receipt `C:/gridflow-data/receipts/v2.2-G-1/sources/14-neso-ci-national-methodology-v2.txt`) covers the intensity estimate only |
| "national generation mix (beta)" (facts.vendor) | `endpoints.py:134,137` category "Generation Mix - National beta" |
| `query()` reads `silver_neso_generation`, filters `timestamp_utc` with half-open UTC instants (end day included), lineage dropped (notebook.lead) | `gridflow_models/research/handles/_get_method_registry.py:62-97,126-141` (registry: `generation` → `timestamp_utc`, `silver_neso_generation`, source `neso`); `source.py:401-450` EXCLUDE of bitemporal columns |
| `intensity_factors` unit gCO2/kWh (related note) | Column `factor_gco2_kwh`, `carbon_intensity.py:370`; methodology Table 1 "gCO2/kWh" |
| Notebook plot alt | `generation-6.png` viewed: stack to 100, nuclear band ~9 to 15, wind largest most of the week, gas ~45 at the start of the 14th, a daily solar band |

## Body corrections (vault notes)

1. **`generation.md`, Silver layer path line.** Added that the file date is the request window's first day: bronze is
   filed under `window_start.date()` (`connectors/neso/carbon_intensity.py:79`) and the transformer reads only that
   exact partition (`silver/neso/carbon_intensity.py:87-154`). So one silver file holds the whole window. Transform the
   start date only; other dates log "covered-but-not-owned" and write nothing.
2. **All three notes, Known issues.** Two copied bullets described intensity routes (null `actual`, and
   `intensity_period` clock-change counts). Replaced them with a dated correction pointing to `_transform_generation`
   (`carbon_intensity.py:559-586`).
3. **`generation.md`, Known issues.** Added four dated entries:
   - No denominator, with the methodology receipt quoted.
   - The grid, rounding and sum measurements, and the response range convention (half-hour ending at `from` to the
     one ending at `to`).
   - The 30-minute stamp offset, with every correlation.
   - Fuel composition: `wind` includes `wind_emb`, `hydro` includes `storage`, and `imports` is not net.
4. **`generation_current.md`, Known issues.**
   - Filed under the ingest start date (`endpoints.py:135-140`, `carbon_intensity.py:79`): the 27 Sep 00:00Z row sits in
     `generation_current_20260926.parquet`.
   - The silver sample was copied from `generation` (its values are not from `/generation`). Flagged, not rewritten.
   - A pointer to the stamp and composition notes.
5. **`generation_pt24h.md`, Known issues.**
   - The window is the 24 hours before the ingest start, because the chunk start is sent as `from`
     (`endpoints.py:141-147`, `carbon_intensity.py:149-161`). A window longer than 14 days fetches one 24-hour slice
     per chunk.
   - Measured: the held response, agreement with `generation` on the shared half-hour, and the same offset against
     fuelhh.

## Not verified

- **NESO's own definition of the fuels and the denominator.** I worked only from the docs the vault quotes (README,
  `endpoints.md`, the methodology receipt). The live API docs (`carbon-intensity.github.io/api-definitions`) were not
  read; they may define `perc`. The page's "undocumented" for the denominator and for `other` rests on that.
- **`solar` alignment.** The lag test cannot place `solar`. Its level fits the portal slightly better at zero lag
  (MAE 1.01) than at +30 (1.51), but the portal's own `solar` was never aligned against a metered source.
- **Why the stamps are offset.** One possible reading: NESO labels the metered period by the half-hour ending at its
  start. That is a hypothesis, not stated anywhere.
- **What "current" means for `generation_current`.** The one capture, fetched 00:32:43Z, returned `from` 00:00Z; that
  is a single observation, so the page says only "the one NESO serves as current".
- Vendor history depth: none stated in the notes, so the page has no `history` fact.

## Open questions for the seat

1. **Ship with the offset stated, or hold?** I recommend ship: silver carries NESO's stamp faithfully, the page labels
   the offset as a project check in the caption, `what_it_is`, the `timestamp_utc` guide line and the fuelhh related
   note, and the chart is not wrong as NESO labels it. A hold would be for "wrong stamps" under the ship-or-hold
   ruling; I read that as gridflow mis-stamping, which this is not.
2. **Cross-page consistency.** The `national-carbon-intensity` writer's raw-feed note says responses run from the
   half-hour ending at `from` (same as mine). If the seat accepts the offset finding, that family's intensity rows
   likely carry it too: within the API, the gas share and `actual` align at zero lag. The writer and checker of that
   page may want the same caveat. (Portal `carbon_intensity` vs CI `actual` correlated weakly at every lag, 0.29 to
   0.42, so I did not test the intensity directly.)
3. The note's "Gold view/builder" link points at `uk_imbalance_context.sql`, which reads `silver_neso_carbon_intensity`
   (line 29), not this table. I left it: the note's "Gold layer: None implemented" is right. Remove it at the next vault
   pass if wanted.

## Template observations (not worked around)

- **Y-axis headroom on a percent stack.** The stack tops at 100.2, and the renderer's nice-tick logic extends the axis
  to 125 at desktop and 150 at 390. The band above 100 is empty. Nothing is clipped, but a percent chart reads better
  capped near 100. A possible template option: a fixed `y_max`, or snap to 100 when the unit is `%`.
- At 390 the on-chart series tags are hidden and the key carries the reading; that looked intentional.
- The site has no dark theme (no `prefers-color-scheme` in `tokens.css` or `theme.css`), so the brief's "light and
  dark" check reduces to light.
- Headless capture at 390 through an 11,000 px iframe stopped painting after the chart. A 7,000 px iframe captured the
  whole page. This is a capture artefact, not a page fault.

## Screenshots

Under `C:/Users/Bobbo/AppData/Local/Temp/claude/C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end/5fec4a50-7518-4657-b815-ed1434a34580/scratchpad/shots-genmix/`:

- `final-1440.png`, `final-1024.png`, `final-768.png`.
- `genmix-390c.png`, a true 390 iframe.
- Section cuts: `cut-*`, `genmix-390c-*` and `final-1440-frame.png`.

I checked the hero scenery, chart, key, raw feed, frame and guide, notebook panel, related list and corner labels at
every width. Nothing is clipped or overlapping.

## Defects (pasteable)

- **NESO generation mix: stamps sit 30 minutes before the metered half-hour (research unit; vendor labelling, not a
  gridflow bug).**
  - Datasets: `neso/generation` and `neso/generation_pt24h` (and probably `generation_current` and the national
    intensity routes; untested).
  - Measured 2026-10-06 on silver 31 Jul to 5 Aug and 12 to 21 Sep 2026. A row with vendor `from` = T tracks the
    metered half-hour starting at T+30 min, in both `elexon/fuelhh` and the NESO Data Portal `historic_generation_mix`.
    Differenced correlation at +30 vs zero lag: gas 0.93 to 0.98 vs 0.67 to 0.69; imports 0.94 vs 0.10; biomass 0.88
    vs 0.50. Control (portal vs fuelhh) peaks at zero lag, 0.996.
  - Named unknowns:
    - NESO's stated meaning of `from`/`to` on `/generation`.
    - Whether `/intensity` `actual` shares the offset.
    - Whether `solar` (estimated embedded) shares it.
  - Consequence: joins of these tables to settlement-period data on `timestamp_utc` are off by one half-hour for the
    metered fuels. No gridflow change until the unknowns are answered.
- **NESO generation mix: share denominator and fuel composition undocumented (research unit).**
  - Measured: `wind` includes embedded wind (matches portal `wind`+`wind_emb` over `generation`, MAE 1.2 points).
    `hydro` includes pumped storage (matches `hydro`+`storage`, MAE 0.07). `imports` is not net of exports, yet is
    1.9 points below the portal's gross share on average.
  - Named unknowns: the denominator NESO divides by; what `imports` counts; what `other` holds.
- **NESO non-ranged routes filed under the ingest start date, not the data's date (gridflow, low).**
  - `connectors/neso/carbon_intensity.py:79` sets `data_date=window_start.date()` for every non-reference route.
  - For `generation_current` (no inputs) the row's half-hour has nothing to do with the CLI window: the
    2026-09-27T00:00Z row is in `generation_current_20260926.parquet`.
  - For `generation_pt24h` the rows are the 24 hours *before* the filed date (31 Jul rows filed under 2026-08-01).
  - Query by `timestamp_utc` works; date-partition reasoning does not.
- **`generation_pt24h` multi-chunk windows fetch slices, not the window (gridflow, low, behaviour to document or fix).**
  - The route goes through `_request_specs`' 14-day chunk branch (`connectors/neso/carbon_intensity.py:149-161`) with
    `from` = chunk start.
  - So `--start A --end B` with B − A > 14 days fetches one 24-hour slice before each chunk start, leaving gaps of
    13 days between slices. A window ≤ 14 days fetches only the 24 hours before A.
- **Vault notes `generation*.md` carried copied intensity-route gotchas (vault, fixed in this batch).** The bullets on
  null `actual` and `intensity_period` clock-change counts were replaced with a dated correction. Other NESO
  generation-family or regional notes may carry the same copy.
- **Vault `generation_current.md` silver sample was copied from `generation` (vault, nit).** Its values are not from
  `/generation`. Flagged in the note, not rewritten.
