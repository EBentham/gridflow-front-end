# Spec: weather-locations map on the three Open-Meteo pages

Approved by Bobbo 2026-10-06 (ruling #50): "yes go ahead with the map, download is fine … to include coordinates etc."
Runs after the 19 dataset pages, before the local review build, as ONE Opus 5.5 · high `claude` subagent in the
batch worktree `...\scratchpad\p26-rest` (branch `v5/p26-rest`). Front-end lane: Opus executes, Bobbo validates visually.

## What it adds

A section on `openmeteo/demand-weather`, `wind-weather` and `solar-weather`, after the chart and before the raw
feed (the subagent picks the exact slot from `DESIGN.md` "Dataset page anatomy" and says why), titled in domain terms
(e.g. "Where the weather is taken").

1. **Map.** An inline SVG of the UK and Ireland outline, drawn at build time, with one marker per configured site:
   - Configured coordinates: gridflow `connectors/openmeteo/endpoints.py` `DEMAND_LOCATIONS` (7), `WIND_LOCATIONS`
     (12, grouped in code as offshore southern North Sea, offshore Irish Sea, offshore Moray/Forth, onshore Scotland,
     onshore Wales), `SOLAR_LOCATIONS` (6). Read them from code at distil time; never hand-copy.
   - A faint second mark at the grid point Open-Meteo answered from (silver `latitude`/`longitude`), joined to the
     configured point by a hairline when they differ. State the distance. Triton Knoll is ~18 km off (logged 15e).
   - Hover, focus or tap shows a card: site name, configured lat/lon, answered lat/lon and distance, and the stats.
   - Keyboard reachable (each marker focusable, `aria-describedby` to its table row). Works at 390 px (tap opens the
     card; the card never runs off-screen).
2. **Table beneath** (the no-JS and screen-reader path): one row per site with the same facts. Hovering a row
   highlights its marker and vice versa.
3. **Stats from local silver only**, computed by the distil step and committed as a build input (generated HTML is
   gitignored and CI builds from a bare checkout, so the data must be a committed file under
   `site/hifi/data/…/openmeteo/`). Scope every stat to the window it was computed over, and name the window on the page.
   - Demand cities (`historical_demand`): mean temperature, coldest hour, heating degree-days per year (state the base
     temperature used and that it is the project's choice).
   - Wind sites (`historical_wind`): mean 100 m wind speed and a high percentile (e.g. p90). No turbine thresholds
     unless sourced.
   - Solar sites (`historical_solar`): mean daily irradiation (kWh/m² per day from the hourly W/m² means, stating the
     hour-ending convention) and the sunniest and darkest months.
   - Units from code column names / vendor docs, never memory.

## Geometry

- Source: Natural Earth 1:50m admin 0 countries, `ne_50m_admin_0_countries.geojson` from
  `github.com/nvkelso/natural-earth-vector` (public domain, about 1 MB). Download approved once (ruling #50).
- Keep GBR and IRL only. Project with a simple equirectangular-at-latitude or transverse-ish projection suitable for
  GB (state which), simplify to roughly 15 KB of SVG path, and commit ONLY the simplified outline (plus a one-line
  provenance note naming the source and licence). Do not commit the raw GeoJSON.
- Offshore sites must land in the sea on the drawing; check every marker visually.

## Design

- Follow `DESIGN.md` and `site/hifi/assets/tokens.css`: the section sits in the topsoil band like the chart; land in a
  quiet tone, sea as the band background, markers in the series colours the page already uses; Red Hat Mono for
  coordinates. No map tiles, no third-party requests, no new libraries. Vanilla JS in `site.js` or `charts.js`
  (whichever owns similar interaction), progressive enhancement over the static SVG.
- Respect `prefers-reduced-motion`. No em dashes. No planning words.

## Content model and authoring

- Add the section through the page model (`page_fields.py` / `templates/dataset.html.j2` / `build.py`), not hand
  HTML. Prefer a small `locations:` block in the lead note's `page:` front matter only for prose (a one-line caption,
  within a word budget); the coordinates and stats come from the committed data file, not the note.
- Canonical notes are edited in the vault worktree and mirrored byte for byte (cp, then cmp) as in `BATCH-rest.md`.

## Gates

- `uv run --system-certs --extra build gridflow-build` and `--check`; `uv run --extra build pytest -x -q` (add tests
  for the new field and the distil output); htmlhint; `lychee --offline`; the impeccable detector (absolute path in
  `BATCH-rest.md`) on the three pages; 0 em dashes; ruff on changed files.
- Screenshots of all three pages at 1440, 1024, 768 and a true 390 iframe, plus the card open at 390.

## Report

`.planning/v5/p26/openmeteo/map-author.md`: what was built, the stats and their windows, projection and
simplification, the files touched, gates, screenshots, and anything left for Bobbo's look. Then a Sonnet 5.5 · high
checker reviews it against this spec and the rubric (`map-review.md`), with the usual revise loop.
