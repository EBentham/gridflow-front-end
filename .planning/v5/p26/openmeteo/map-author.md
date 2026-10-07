# Open-Meteo weather-site map: author report

Writer: Opus 5.5 · high, 2026-10-07. Spec: `MAP-weather-locations.md` (ruling #50). Worktree `scratchpad/p26-rest` (branch `v5/p26-rest`), vault worktree `scratchpad/vault-p26-rest`. No git writes.

## What was built

A section titled "Where the weather is taken" on `openmeteo/demand-weather`, `wind-weather` and `solar-weather`.

**Slot.** It sits inside the topsoil `<section>`, after the chart figure and before the bronze raw feed. DESIGN.md "Dataset page anatomy" step 2 makes topsoil the place for what the dataset is, with its chart. Where the weather is taken is part of what the dataset is. It describes no raw response, typed table or notebook, so it belongs to no lower stratum. Keeping it in the same band adds no new stratum to the locked descent; the strata order test still reads sky, topsoil, bronze, silver, gold, deep.

1. **Map.** A static inline SVG, drawn at build time (`map_svg.py`).
   - **Ground:** land in `--daylight` with a 1.1 px ink coast. The sea is the topsoil band and its speckle. The Northern Ireland and Ireland land border is a faint dashed hairline.
   - **Markers:** one per configured site, an ink-ringed dot.
     - A site the page's chart draws keeps its key paint: London clay and Glasgow horizon; Beatrice petrol, Walney horizon, Hornsea olive and Whitelee clay; Cornwall horizon and Kent clay.
     - Every other site is unpainted (daylight fill).
   - **Answered grid point:** a small square, joined to its dot by a hairline. It is drawn for every site; it is only visibly apart from the dot for Triton Knoll (17.7 km).
   - **Labels:** each site's code, lower-case and spaced ("gwynt y mor"), in Hanken italic 13.5 px with a topsoil halo where a label crosses a coast.
     - A greedy placer tries eight positions and takes the first that overlaps no other label or marker.
     - All 7, 12 and 6 labels place.
     - Below 760 px the drawing scales under legible label size, so labels hide there; the card and the table name the sites.
   - **Links and keyboard:**
     - Each marker is an SVG `<a href="#site-<name>" aria-label="<name>" aria-describedby="site-<name>" tabindex="0">`. It is Tab-reachable even in engines that skip SVG links, and without script a click jumps to and lights (`:target`) its table row.
     - The figure's SVG is `role="group"` with a generated accessible name.
   - **Card** (`site.js`, progressive enhancement):
     - Hover or focus opens a card beside the marker. A click or tap pins it; another tap, a tap elsewhere or Escape closes it.
     - The card is built from the row's own cells and header text, so it carries exactly the table's facts: site, group, requested, answered, apart and the statistics. It is `aria-hidden`, because the row is the description.
     - It is clamped inside the map box: beside the marker if there is room, else centred above or below it. At 390 it never runs off-screen (shots below).
   - **Motion:** none, so there is nothing for `prefers-reduced-motion` to stop.
2. **Table.** It sits beside the map at 1240 px and wider (the keyed-index-beside-a-drawing pattern), and beneath it below 1240; DOM order is map, then table.
   - Columns: Site (mono code with a paint swatch) | Requested | Answered | Apart | statistics. The wind table is grouped by the code's region comments.
   - Hovering a row lights its marker, and the reverse. The table scrolls inside its own focusable box at 390.
   - Beneath it are generated definition lines:
     - which mark is which;
     - the statistics' silver table and window;
     - the method of the degree-days, the percentile or the irradiation.

## Statistics and their windows

All statistics use one window, every hour of **2022 to 2025 (four whole calendar years, UTC)**, so every month counts equally and a yearly total is a real year. Each site has all 35,064 hours with no nulls; the distil fails otherwise. Statistics are taken at the answered grid point (the silver rows), from the archive members only. The page says this in the notes line: "Statistics: silver `historical_wind` at the answered point, every hour of 2022 to 2025, UTC."

| Page | Statistic | How | Unit source |
|---|---|---|---|
| demand | Mean temperature | Mean of `temperature_2m_c` | `_c` column; vault field "°C" |
| demand | Coldest hour | Minimum of `temperature_2m_c` and its first stamp, for example London −5.5 at 22:00 UTC, 16 Dec 2022 | same |
| demand | Heating degree-days a year | Sum of silver `hdd_k` ÷ 24 ÷ 4. `hdd_k` = max(0, 15.5 − T) per hour. The base, **15.5 °C**, is read at distil time from gridflow `silver/openmeteo/historical.py` `_HDD_BASE`; the page calls it "gridflow's base, a project choice". | `_k` column |
| wind | Mean at 100 m | Mean of `wind_speed_100m_mps` | `_mps` column (km/h ÷ 3.6 in gridflow) |
| wind | 90th percentile | Polars `quantile(0.9, "linear")`; the page says "one hour in ten blows harder" | same |
| solar | Mean day | Daily kWh/m² = Σ hourly `shortwave_radiation_wm2` ÷ 1000, averaged over the 1,461 days. Each value is the vendor's mean over the hour **ending** at its stamp (vault notes, citing the vendor docs: "Preceding hour mean"), so the window runs from the stamp 01:00 on 1 Jan 2022 to 00:00 on 1 Jan 2026, and each hour counts to the day in which it began. | `_wm2` column |
| solar | Sunniest and darkest month | Calendar month with the highest and lowest mean daily kWh/m² over the four years; the cell shows the month, with its mean day on a second line ("June / 6.09 a day") | same |

Values on the pages:
- **Demand:**
  - mean temperature 9.6 (Glasgow) to 12.0 °C (London);
  - coldest hours −3.8 (Belfast) to −7.8 °C (Manchester, 23:00 UTC 8 Jan 2025);
  - degree-days 1,718 (London) to 2,265 (Glasgow) a year.
- **Wind:**
  - offshore means 7.9 to 9.8 m/s, onshore 6.9 to 7.8;
  - p90 11.1 to 16.0;
  - Triton Knoll has the lowest offshore mean, 7.9, at its displaced grid point.
- **Solar:**
  - mean day 3.10 to 3.31 kWh/m²;
  - June the sunniest (6.03 to 6.42) and December the darkest (0.58 to 0.71) at all six sites.

Configured coordinates are the literal text in `endpoints.py`, so "52.50" keeps its zero. They are parsed from the source, then checked against the module, imported by path, so a site the text parse missed fails loudly. Answered points are shown to 3 decimals; "Apart" is the great-circle distance on a 6,371.0088 km sphere.

## Projection and geometry

- **Source:** Natural Earth 1:50m Admin 0 countries (`ne_50m_admin_0_countries.geojson`, public domain), downloaded once to the session scratchpad and not committed.
- **Kept:** GBR and IRL, **plus the Isle of Man (IMN)**. This is a deliberate departure from "GBR and IRL only". In Natural Earth the Isle of Man is its own feature, and Walney and Gwynt y Môr sit beside it; leaving it out would draw open sea where it stands. It is one 15-point ring. Bobbo can drop it with one line in `scripts/make_outline.py` (`KEEP`).
- **Committed:** `site/hifi/data/geo/gb-ie.json` (21.9 KB): lon/lat rings rounded to 3 decimals, 1,316 points, plus the 56-vertex land border as its own run. Its `_about` is the one-line provenance: source, licence, script.
- **Simplification:** none beyond the 3-decimal rounding and dropping repeated points. The land path is 9.1 KB as drawn (deltas between rounded points), well under the 15 KB target. Douglas-Peucker would have split the shared NI border vertices, so I left it out.
- **Projection:** equirectangular, true scale at 55°N (x = lon × cos 55°, y = lat). It covers 10.75°W to 3.05°E and 49.75°N to 59.5°N, drawn 500 × 616. **Shetland lies north of the frame** (no site is there; Orkney is in it). The crop is stated in `map_svg.py`'s docstring, not on the page.
- **SVG size:** 13.9 to 17.3 KB per page, markers and labels included.
- **Land and sea check:** an automated test (`test_offshore_sites_land_in_the_sea_and_the_rest_on_land`) checks every configured point against the committed outline. All 8 offshore wind points are in the sea, and all onshore wind sites, cities and solar sites are on land. Visually confirmed in every shot.
  - **Exception, shown as it is:** Triton Knoll's *answered* grid point (53.392, 0.171) falls on land at the Lincolnshire coast in the 1:50m outline. The wind caption says "Triton Knoll's is 17.7 km away, at the Lincolnshire coast".

## Content model and data flow

- **Note field:** `page.locations: {title, caption}`, optional (`page_fields.py`).
  - Budgets: title 10 words, caption 40 words.
  - Unknown keys and a missing title or caption are errors.
  - Sites, coordinates and statistics never come from the note.
- **Committed data file:** `site/hifi/data/locations/openmeteo/<lead>.json`, written by `gridflow-distil --locations` (new flag; also `python -m gridflow_front_end.locations`). It reads the gridflow repo (`--gridflow-path`, `$GRIDFLOW_REPO_PATH`, default the local repo) and local silver, read only. It records the `endpoints.py` sha256, the tuple name, the silver table, the window and the HDD base.
- **The build** (stdlib, CI-safe) loads the file and checks what it can without silver:
  - the dataset name;
  - the kind;
  - the window;
  - for every site, configured and answered coordinates inside the map, `offset_km`, and every statistic for its kind;
  - no duplicate sites.

  A declared block with no file fails the build. A committed file whose note has no `locations` block fails it too (`orphan_locations`).
- **Captions:** in the three lead notes, edited in the vault worktree with CRLF kept, copied to `vault/openmeteo/` and `cmp`-equal.
  - demand: "The seven cities gridflow requests, and the archive grid point Open-Meteo answered from, a few kilometres off; London and Glasgow keep their chart colours. The forecast host answers from its own grid points, not drawn." (35 words)
  - wind: "The 12 points gridflow requests near GB wind farms, and the archive grid point Open-Meteo answered from. Triton Knoll's is 17.7 km away, at the Lincolnshire coast. The four charted sites keep their colours; forecast grid points are not drawn." (39)
  - solar: "The six points gridflow requests at GB solar sites, and the archive grid point Open-Meteo answered from, within about 5 km. Cornwall and Kent keep their chart colours; forecast grid points are not drawn." (33; largest offset 5.2 km)

## Files touched

New:
- `src/gridflow_front_end/locations.py`: distil step (Polars).
- `src/gridflow_front_end/map_svg.py`: drawing, table view, file check (stdlib).
- `scripts/make_outline.py`: GeoJSON to outline.
- `site/hifi/data/geo/gb-ie.json`
- `site/hifi/data/locations/openmeteo/historical_demand.json`, `historical_wind.json`, `historical_solar.json`
- `tests/test_locations_map.py`: 24 tests.

Changed:
- `src/gridflow_front_end/page_fields.py`: `locations` field, budgets, docstring.
- `src/gridflow_front_end/artefacts.py`: `locations_dir` and `locations_path`.
- `src/gridflow_front_end/build.py`: load and check the file, `map` in the view, `orphan_locations`.
- `src/gridflow_front_end/distil.py`: `--locations` flag.
- `templates/dataset.html.j2`: the section; CRLF kept.
- `site/hifi/assets/dataset.css`: map, card and table styles.
- `site/hifi/assets/site.js`: the card and the linked highlight.
- Vault: `30-vendors/open-meteo/datasets/historical_{demand,wind,solar}.md`, mirrored to `vault/openmeteo/`.

Not touched: `<vendor>.json`, `theme.css`, other datasets' files. The seat's uncommitted edits in `build.py`, `page_fields.py` and the template were already in the worktree and are preserved. Ruff formatting touched only my hunks in `build.py`.

## Gates

| Gate | Result |
|---|---|
| `uv run --system-certs --extra build gridflow-build --check` | OK: idempotent across 73 pages + 7 hubs (full build, rc 0) |
| `pytest -x -q --deselect tests/test_dataset_page.py::test_a_page_without_a_page_block_is_blank` | 130 passed, 1 deselected |
| `pytest -q` (nothing deselected) | 130 passed, 1 failed: only the known blank-page test, fixed separately |
| `htmlhint --config .htmlhintrc 'site/hifi/**/*.html'` | 184 files, no errors |
| `lychee --no-progress --offline --include-fragments` | 0 errors (1,928 OK); every `#site-*` fragment resolves |
| impeccable `detect.mjs --json` (absolute path), three pages | `[]` on each |
| Em dashes on the three pages | 0 (planning words 0) |
| `ruff check` and `ruff format --check`, the 8 changed or new Python files | all passed |

The shared venv still has the distil extra after `uv run --extra build` (polars 1.44.2 imports).

## Screenshots

Headless Chrome, `timeout 60`, `--timeout=15000 --virtual-time-budget=5000`, own profile. Every width was shot through a same-origin iframe wrapper served from a scratch copy of the built site on port **9880**. The 390 shots are a true 390 px iframe. The server was stopped afterwards; port 9670 was not touched.

Final set, in `scratchpad/map-work/shots/`, prefix `r4-`, plus `r5-demand-weather-390-table.png`, `r5-demand-weather-1024.png` and `r6-solar-weather-768.png` (taken after the month cells moved to two lines so the solar table fits at 768):
- `{demand,wind,solar}-weather-{1440,1024,768,390}.png`, plus `-390b` (the table and notes).
- Cards open at 390: `wind-390-card.png` (Triton Knoll), `wind-390-card-w.png` (Walney), `demand-390-card.png` (Belfast), `solar-390-card.png` (Cornwall).

Checked:
- every marker sits where it should, offshore in the sea;
- no label overlaps another, and every label is readable over a coast;
- side by side at 1440 and stacked at 1024 and 768;
- at 390 the card stays inside the screen in all four card shots, the tapped site's row lights, and the table scrolls in its box;
- **keyboard, measured:** `scratchpad/map-work/focus.sh` focuses a marker in the 390 iframe (and at 768 and 1440) and reads the DOM back. On all six checks:
  - the marker took focus (`tabIndex` 0);
  - the card opened with the row's facts;
  - the halo's opacity was 1 and the row was lit;
  - the card sat inside the frame, for example 16..316 and 59..359 px of a 375 px layout width (the 390 iframe less its scrollbar).
- nothing is clipped.

## For Bobbo's look

1. **Isle of Man kept** (spec said GBR and IRL only); see Geometry. Recommend keep.
2. **Shetland cropped** out of the frame to keep the drawing 500 × 616 rather than about 500 × 720. Recommend keep: no site is there.
3. **Marker colours:** charted sites take their chart paint, the rest are unpainted. On the wind map that makes four colours among 12 sites. The alternative is one paint for all, linked to the chart by name only.
4. **Labels hide below 760 px.** At phone width the map shows dots only; a tap opens the card and the table lists every site.
5. **Desktop layout:** the table sits beside the map at 1240 px and wider (beneath it in DOM order), not under it at all widths. Under it, the row-to-marker highlight would scroll off at desktop heights.
6. DESIGN.md's anatomy step 2 does not yet mention the map. If the seat wants the lock to name it, add one clause: "then, for weather sites, where the data is taken".
7. Seen in passing, not in my files: the wind page's raw-feed URLs still use `%2C`, while demand and solar use plain commas. The seat ruled plain commas on all three.

## Defects (paste into the backlog as is)

- **open_meteo historical_wind: Triton Knoll's archive grid point is on the coast, not at the wind farm.**
  - Silver `latitude`/`longitude` 53.391914, 0.171429 against the request 53.45, 0.42, 17.7 km apart (great-circle).
  - In Natural Earth 1:50m the answered point falls inside the Lincolnshire land polygon.
  - Its 2022 to 2025 mean wind at 100 m is 7.9 m/s, against 9.3 to 9.8 at the other seven offshore sites.
  - This adds evidence to the existing item (15e). The cause (Open-Meteo's cell selection) is not established. Check which cell the archive picks for 53.45, 0.42, and whether the vendor docs offer a way to prefer a sea cell (unverified here) or a moved request point gives an offshore one.

## Revision 1 (after map-review.md: 1 major, 8 nits)

This supersedes items 4 and 5 of "For Bobbo's look" above: labels now hide under 480 px, and the table sits beside the map only from 1440 px.

Same worktree (`scratchpad/p26-rest`, branch `v5/p26-rest`) and vault worktree; no git writes. Every finding is fixed; the optional items are noted where taken.

### 1. Major: the table clipped beside the map (fixed)

- `dataset.css`: the table stacks under the map below 1440 (`max-width: 1439.98px`, was 1239.98). At 1440 the table gets 724 px beside the map, and all three need at most 724.
- Under 840 the cell right padding drops from 14 to 9 px (the first column from 20 to 14), so demand and solar fit at 768.
- Under 760 the stat headers get `min-width: 6em`. Without it, "Mean wind at 100 m, m/s" stacked five lines deep at 390 and left a 114 px gap above the rows; it now takes 44 to 61 px.
- Optional item 3 taken: a one-line hint, "The table scrolls sideways to its statistics.", shows only when the table is wider than its box. `site.js` compares `scrollWidth` with `clientWidth` on load, after the fonts are ready, and on resize; without script it stays hidden.
- Optional item 4 (a browser width test in pytest) not taken: pytest has no browser here. The measurement page `scratchpad/map-work/shot.html?measure=1` does it.

Measured in headless Chrome, true viewport with no scrollbar. Each cell gives the table's `scrollWidth` / `clientWidth`. The page never scrolls sideways (`scrollWidth` equals the viewport at every width).

| viewport | layout | demand | wind | solar | hint |
|---|---|---|---|---|---|
| 1440 | beside | 724/724 | 724/724 | 724/724 | hidden |
| 1366 | stacked | 1214/1214 | 1214/1214 | 1214/1214 | hidden |
| 1280 | stacked | 1138/1138 | 1138/1138 | 1138/1138 | hidden |
| 1240 | stacked | 1102/1102 | 1102/1102 | 1102/1102 | hidden |
| 1024 | stacked | 910/910 | 910/910 | 910/910 | hidden |
| 840 | stacked | 747/747 | 747/747 | 747/747 | hidden |
| 768 | stacked | 683/683 | 683/683 | 683/683 | hidden |
| 600 | stacked, full-bleed box | 766 in 600 | 644 in 600 | 731 in 600 | shown |
| 390 | stacked, full-bleed box | 766 in 390 | 644 in 390 | 731 in 390 | shown |

From 768 up nothing is clipped. Below about 700 px the table scrolls inside its own box, with the hint above it and the box keyboard-focusable.

Screenshots, true-width iframes, `scratchpad/map-work/shots/`:

- `v1-{demand,wind,solar}-weather-{1440,1366,1280,1024,768,600,390}.png`;
- the card open at 390: `v1-wind-390-card.png` (Gwynt y Môr), `v1-demand-390-card.png` (Belfast), `v1-solar-390-card.png` (Cornwall).

### 2. Labels threshold (fixed)

Labels now hide only under 480 px (`max-width: 479.98px`), which is where the drawing actually shrinks. The plot is 500 px down to a 532 px viewport and 448 px at 480 (labels 12.1 px). At 390 it is 358 px, so labels would fall to about 9.7 px; there the card and the table name the sites. Labels are placed at the 500-unit scale and scale with the drawing, so their clearance holds at every width. `v1-wind-weather-600.png` shows all 12 clear.

### 3. Triton Knoll caveat (fixed)

The vault note `30-vendors/open-meteo/datasets/historical_wind.md` caption now reads (40 of 40 words):

> The 12 points gridflow requests at GB wind farms, and the archive grid point answering each. Triton Knoll's is 17.7 km away on the Lincolnshire coast, so its statistics describe that coast, not the farm. Charted sites keep their colours.

It is mirrored to `vault/openmeteo/historical_wind.md`, and `cmp` matches for all three notes (CRLF kept).

### 4. Accessible name (fixed)

`map_svg.accessible_name` reads: "Map of the UK and Ireland with the 12 wind-farm sites where the weather is taken; each links to its row in the table." Demand says "7 cities" and solar "6 solar sites". No dataset code. Test: `test_the_accessible_name_is_in_words`.

### 5. Real site names (fixed)

- gridflow's `endpoints.py` holds only slugs, so the display names are a mapping in our repo: `map_svg.SITE_NAMES`.
- The names follow each farm operator's own spelling: RWE for Gwynt y Môr, Vattenfall for Pen y Cymoedd, Fred. Olsen Renewables for Crystal Rig. The other farm slugs are already the farm's name (Dogger Bank, Hornsea, East Anglia, Triton Knoll, Walney, Beatrice, Seagreen, Whitelee).
- The centroid sites are named for their region, not a farm: `highland_central` is "Central Highlands", `east_anglia_norfolk` is "Norfolk", `wiltshire_somerset` is "Wiltshire and Somerset", plus Kent, Cornwall, Sussex and Oxfordshire. The cities are their names.
- The name is used for the map label, the card heading and the table row. The gridflow code stays beneath it in mono as the key.
- `map_svg.check` fails the build for a site with no display name. Test: `test_every_site_has_its_real_name`.
- Seat check: the operator spellings were not re-checked against the operators' own pages in this revision.

### 6. Tap targets (fixed)

`HIT_R` is now 18 units: 25.8 px at 390 (measured), 32.3 px at 480 and 36 px from 532 up. The closest pair of sites is 32 units apart, so a hit circle never covers a neighbour's dot. Test: `test_tap_targets_are_24_px_at_390_and_never_cover_a_neighbours_dot`.

### 7. Tests split (fixed)

- `tests/test_locations_map.py` is stdlib-only: map, page-field, committed-file, sea/land, label, tap-target, orphan and page tests.
- `tests/test_locations_distil.py` holds the parse, distance, stats and `--distil --locations` tests behind `pytest.importorskip("polars")`.
- With Polars made unimportable (a `ModuleNotFoundError` stub on `PYTHONPATH`): **20 passed, 1 skipped** (the distil module). With Polars installed, both modules run.

### 8. Polish

- Headers now stand alone: "Mean at 2 m, °C", "Mean wind at 100 m, m/s".
- The first column's right padding is 20 px (14 under 840), so `borders_crystalrig` no longer touches Requested.
- Minus signs are left as they are, per the review's cheaper option: a typographic minus in statistics, ASCII in the mono coordinates.

### 9. For the seat

The DESIGN.md anatomy clause ("then, for weather sites, where the data is taken") is left for the seat to add at ratification, with the note that ruling 50 covers these silver-computed statistics.

### Gates, re-run after every change

| Gate | Result |
|---|---|
| `uv run --system-certs --extra build gridflow-build --check` (full) | OK, idempotent across 73 pages + 7 hubs |
| `pytest -x -q`, known `test_a_page_without_a_page_block_is_blank` deselected | 133 passed |
| `pytest -q`, nothing deselected | 133 passed, 1 failed (that known test only) |
| map tests with Polars blocked | 20 passed, 1 skipped |
| `htmlhint --config .htmlhintrc 'site/hifi/**/*.html'` | 184 files, no errors |
| `lychee --offline --include-fragments` | 2,238 total, 1,928 OK, 0 errors |
| impeccable `detect.mjs`, three pages | `[]`, `[]`, `[]` |
| em dashes / planning words, three pages | 0 / 0 |
| `ruff check` + `ruff format --check`, 9 changed Python files incl. both test modules | clean |

Servers: the scratch copy was served on 9880 for measuring and screenshots, then stopped (0 listeners on 9880 afterwards). Port 9670 was never touched.
