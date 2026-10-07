---
verdict: APPROVE
reviewer: Sonnet 5.5 · high (checker)
reviewed: 2026-10-07 (review 2 appended; review 1 was REVISE)
subject: weather-locations map on openmeteo/demand-weather, wind-weather, solar-weather (worktree scratchpad/p26-rest, branch v5/p26-rest)
blockers: 0
majors: 1
nits: 8
---

# Map review: "Where the weather is taken"

One major (the table is clipped inside its own box at common laptop and tablet widths), eight nits. Data,
coordinates, statistics, accessibility, copy and gates all pass. The major is a CSS breakpoint fix; nothing
about the data or build needs to change.

## What I verified (all pass)

- **Coordinates are read from code, not hand-copied.** `locations.py:87-154` parses the literal text of
  `endpoints.py` and checks it against the imported module. I re-imported
  `gridflow/src/gridflow/connectors/openmeteo/endpoints.py` by path and compared all 25 sites (7 + 12 + 6)
  to the three committed files: names, order and lat/lon identical. The `endpoints_sha256` in each file
  (`3974af2a…`) equals the sha256 of the file on disk today. Wind groups come from the code comments.
- **Stats recomputed from silver, independently** (Polars, tz cast to string, no reuse of `locations.py`):
  all 25 sites match to the stated rounding, none off.
  - demand, every city: mean (London 11.954), coldest hour and its first stamp (Manchester -7.8 at
    2025-01-08 23:00 UTC), degree-days (Glasgow 2,265.1 from my own `max(0, 15.5 - T)`, not from `hdd_k`).
  - wind, all 12: mean 100 m and p90 (linear), e.g. Triton Knoll 7.875 and 12.361.
  - solar, all 6: mean day (3.161 East Anglia, 3.305 Sussex), June sunniest and December darkest with the
    same month means. Each site has 35,064 hours in the window, 1,461 days, no duplicate (location,
    stamp) rows. The hour-ending shift changes nothing visible at 3 decimals (stamp-day mean 3.161 against
    3.161), so the stated convention is honest and harmless.
  - The answered grid points are single per site in silver and equal the committed values. All 25
    configured-to-answered great-circle offsets recomputed (haversine, R 6,371.0088 km) match the file to
    its 0.1 km rounding, none off; London 2.866 (file 2.9), Triton Knoll 17.693 (file 17.7).
  - Conventions on the page match the sources: `_HDD_BASE = 15.5` in `silver/openmeteo/historical.py:46`;
    wind is km/h divided by 3.6 (`historical.py:141-149`); the vault note at
    `vault/openmeteo/historical_solar.md:84,219-221` says irradiance is the preceding-hour mean.
- **The committed data file is a build input.** `site/hifi/data/locations/openmeteo/*.json` and
  `data/geo/gb-ie.json` are tracked paths (`git check-ignore` returns nothing). `build.py` and
  `map_svg.py` import no Polars and never open silver; Polars lives only in `locations.py` behind the
  `distil` extra. A declared block with no file fails the build; an orphan file fails it too
  (`build.py:1025-1038`, `1987`). The raw GeoJSON is not in the tree (`git status` shows only `gb-ie.json`).
- **Markers.** I measured distance to the committed coastline for every configured and answered point.
  All 8 offshore configured points are in the sea (nearest 15.2 km: Triton Knoll; Gwynt y Mor 16.6;
  Beatrice 19.3; Walney 23.7). All 7 cities, 5 onshore wind and 6 solar points are on land (Cardiff
  3.3 km and Belfast 5.9 km from the coast, still land). Only Triton Knoll's *answered* point is on land,
  2.1 km inland on the 1:50m outline, which matches the report. At 3x zoom the Isle of Man sits between
  Walney and the Scottish coast, Beatrice sits off Caithness, and Orkney is drawn.
- **Accessibility, measured in Chrome** at 390 and 1440 on all three pages:
  - every marker is a focusable link (`tabindex=0`); `.focus()` opens the card, `blur` closes it;
  - `aria-describedby` resolves to a `<tr>` for 25 of 25 markers;
  - Escape and a tap outside close a pinned card;
  - the card stays inside both the viewport and the map box for every marker (0 failures of 25), card
    widths 24..359 of a 375 px layout;
  - no horizontal page scroll at 390, 600, 768, 1100, 1240, 1280, 1366 and 1440 (`scrollWidth` equals
    `clientWidth`);
  - the no-script path works (copy of the page with all `<script>` removed): 12 table rows, `:target` on the
    linked row computes the lit background, the card stays `hidden`;
  - the new CSS has no transition or animation, so `prefers-reduced-motion` has nothing to stop.
- **Copy.** 0 em dashes (and 0 en dashes) on all three pages; no planning words, no local row counts, no
  "live" framing. The statistics line names silver table, point and window ("every hour of 2022 to 2025,
  UTC"). That window is a computation scope the spec required (ruling 50), not a holdings claim.
  Wording is domain-precise (answered grid point, hour ending, great-circle, degree-days with base).
- **Gates, re-run in the worktree.**

  | Gate | Result |
  |---|---|
  | `uv run --system-certs --extra build gridflow-build --check` | OK, idempotent across 73 pages + 7 hubs |
  | `uv run --extra build pytest -x -q` | 65 pass, stops at the known `test_a_page_without_a_page_block_is_blank` |
  | same, with that test deselected | 130 passed |
  | `htmlhint --config .htmlhintrc 'site/hifi/**/*.html'` | 184 files, no errors |
  | `lychee --offline --include-fragments` | 0 errors, 1,928 OK |
  | impeccable `detect.mjs --json`, three pages | `[]`, `[]`, `[]` |

- **Screenshots** (mine, `scratchpad/mapreview/shots/`, a scratch copy of the build served on 9881, stopped
  afterwards, 9670 never touched): `{demand,wind,solar}-{1440,1024,768,390}.png`, the card open at 390 for
  Triton Knoll, Dogger Bank, Beatrice, Walney, Belfast and Cornwall, 1280-wide shots, 3x zooms.
  The 390 shots are a true 390 px iframe.

## Findings

### 1. [MAJOR] The table is clipped inside its own scroll box at 1240 to about 1420 px and again near 768 px

`site/hifi/assets/dataset.css:154,197-199`: the table sits beside the map from 1240 px up, but the table
needs 590 to 698 px (demand 698, solar 682, wind 590 to 668 depending on header wrapping) and beside the
map it gets `viewport - 2 x margin - 500 - 56`. Measured `.wm-tw` `scrollWidth` against `clientWidth`:

| viewport | demand | wind | solar |
|---|---|---|---|
| 1240 | 698 in 531 | 590 in 531 | 682 in 531 |
| 1280 | 698 in 567 | 590 in 567 | 682 in 567 |
| 1366 | 698 in 643 | fits | 682 in 643 |
| 1440 | fits | fits | fits |
| 768 (real width, no scrollbar) | 698 in 668 | fits | 682 in 668 |

`shots/demand-1280.png`: the "Coldest hour" cell is cut mid-text ("at 22:00 UTC, 16 l") and the "Degree-days
a year" column, the page's headline statistic, is entirely out of sight. `shots/demand-768.png`: the same
column reads "Degre / days / ye" and "1,7", cut by the box edge. 1280 and 1366 are the two most common
laptop widths, and the report's evidence covers only 1440, 1024, 768 and 390. Rubric section 5 ("nothing
clipped") makes this a major. Nothing tells the reader the box scrolls.

Fix:
1. Stack until the table fits: `@media (max-width: 1439.98px)` instead of 1239.98 at
   `dataset.css:197`, or make the grid a container query on the `.ds-map` figure with the threshold at
   500 + 56 + 700 = 1256 px of content width. Re-measure at 1240, 1280, 1366 and 1440.
2. Near 768: trim the cell right padding (`dataset.css:180-181`, 14 px) to about 9 px under 840 px, which
   frees about 35 px on 7 columns, and re-measure demand (needs 698) and solar (682) against the 668 px box.
3. (Optional, not needed for the re-check.) Where the table still cannot fit (all of 390 to about 600), add a
   visible cue that it scrolls, such as a right-edge fade on `.wm-tw` or a one-line "Scroll for the
   statistics" hint above it. At 390 the statistics, the point of the table, begin off-screen.
4. (Optional.) Add a check that `scrollWidth <= clientWidth` for the three tables at 768, 1280 and 1440, so
   the next width regression is caught.

Items 1 and 2 are the fix; 3 and 4 are suggestions.

### 2. [NIT] Labels hide at 760 px although the drawing is still full size down to about 530 px

`dataset.css:200-203` hides `.wm-labs` below 760 px "because the drawing scales under legible label size".
Measured plot width is 500.0 px at viewports of 600, 768 and 1100, so the 13.5 px labels are still full
size and readable from 530 to 759 px (`shots/*-768.png` show them well, since they are shown at 768).
They only fall below about 10 px when the plot drops under about 400 px, around a 430 px viewport. Judgement
of the author's choice: hiding labels on phones is right, 760 is too early. Fix: move the threshold to
`max-width: 479.98px` (or hide when the plot is narrower than 400 px), then take a 600 px shot to confirm
the labels clear each other, since placement was solved at 500 px scale only and that scale still applies.

### 3. [NIT] The Triton Knoll caveat is accurate but stops short of the consequence

`vault/openmeteo/historical_wind.md:57-60` (mirrored): "Triton Knoll's is 17.7 km away, at the Lincolnshire
coast." True: answered point 53.392, 0.171 is 2.1 km inside the coastline on the 1:50m outline, and the
distance is right. But the table then shows 7.9 m/s mean and 12.4 m/s p90 for an offshore farm beside
9.3 to 9.8 m/s at the other offshore sites, with only the statistics note ("at the answered point") to
connect them. A reader will take 7.9 for the farm. Fix: add "so its statistics describe that coastal point,
not the farm." The caption is at 39 of 40 words, so trim the last sentence to "The four charted sites keep
their colours; forecast points are not drawn." (saves 1) and cut "near GB wind farms" to "at GB wind farms" or
drop "and" phrasing to fit; the build enforces the budget. A reader can also be told the forecast host
answers 0.9 km from the request here (silver `forecast_wind` Triton Knoll: 53.4427, 0.4298), which supports
the "own grid points" claim; optional.

### 4. [NIT] The map's accessible name carries a raw dataset code

`build.py:1366-1368` builds the SVG `aria-label` as "Map of the UK and Ireland with the 12 sites of
openmeteo/historical_wind; each links to its row in the table." A screen reader speaks the slug. The
rubric and `BATCH-rest.md` rule is no bare codes. Fix: use the page title (`v.title`, "Weather at GB wind
farms") or "the 12 wind sites", for example "Map of the UK and Ireland with the 12 wind-farm sites; each
links to its row in the table."

### 5. [NIT] Labels and cards show the machine code, not the site's name

`map_svg.py:128-130` turns `gwynt_y_mor` into "gwynt y mor" and `borders_crystalrig` into "borders
crystalrig"; `pen_y_cymoedd` becomes "pen y cymoedd". The spec asked for the code spaced and lower-case, so
this follows it, but a Welsh or Scottish reader sees "mor" for Gwynt y Môr and "crystalrig" for Crystal Rig,
and the page never states a farm's real name. Fix, optional and cheap: a `label` per site in the committed
file (written by `locations.py` from a small name table beside the code comments, or an optional `names:`
map in the note's `locations:` block), used for map labels, the card heading and a small second line in the
row; keep the code in mono as the key. If left, say so in the seat's ratification list.

### 6. [NIT] Tap targets are 17.8 px at 390

`map_svg.py:333` `r="13"` renders 17.8 px across at 390 (plot 343 px). WCAG 2.2 AA 2.5.8 wants 24 px unless
spacing exempts; the closest pairs are 22.2 px (demand) and 22.7 px (solar) apart, under the 24 px the
exemption needs, so only the equivalent table row covers it. Not blocking because the table is a
same-page equivalent. Fix: raise `r` so the hit circle is at least 24 px at 390 (r about 17.5 units) for the
demand and solar maps and check that neighbouring circles overlap no more than the nearer dot, or give the
hit circles `pointer-events` priority to the nearest site by sorting.

### 7. [NIT, upper end] Under the stated test gate the whole map test module can skip

`tests/test_locations_map.py:17` is a module-level `pl = pytest.importorskip("polars")`, followed by
`from gridflow_front_end import distil, locations` (line 19). The spec's gate is
`uv run --extra build pytest -x -q`, and Polars belongs to the `distil` extra (`pyproject.toml:22`), not
`build`. The run passes here only because Polars happens to be in the shared venv (the author's report says
so too). I reproduced the clean case by blocking Polars before pytest imports it
(`sys.modules['polars'] = None`): the module reports `1 skipped`, so all 24 tests are skipped, including the
ones that need no Polars: `test_offshore_sites_land_in_the_sea_and_the_rest_on_land`,
`test_labels_never_overlap`, `test_committed_site_files_pass_the_build_check`,
`test_render_links_each_marker_to_its_row`, `test_the_three_pages_carry_the_map`, the field-budget tests.
CI does not run pytest, so nothing breaks today, but the map's own guards vanish in a build-only
environment. Fix: keep the Polars-dependent tests (`test_demand_stats`, `test_wind_stats_and_a_missing_hour`,
`test_solar_days_follow_the_hour_ending_stamp`, `test_distil_flag_runs_the_locations_step`, the
`locations.py` parse tests) in their own module with the `importorskip`, and move the rest into a module
that imports only `map_svg`, `build`, `artefacts` and `page_fields`. Re-run with Polars blocked to confirm
the stdlib tests execute.

### 8. [NIT] Small polish

- `map_svg.py:178-181` and `_num` mix a typographic minus in statistics ("−5.5") with ASCII hyphens in
  the mono coordinates ("-0.1278", "-3.52"). Pick one; the mono columns read fine either way, so the cheaper
  fix is to leave coordinates and note nothing.
- The wind table headers read "Mean at 100 m, m/s" and "90th percentile, m/s" (`map_svg.py:193`); say "Mean
  wind at 100 m" so the column stands alone, and the demand header "Mean, °C" could say "Mean at 2 m".
- At 1440 `borders_crystalrig` and its Requested value touch (`shots/wind-1440.png`, 800 px): widen the first
  column's right padding by 6 px.

### 9. [NIT, for the seat] DESIGN.md does not yet name the map

`DESIGN.md:117-146` "Dataset page anatomy" step 2 says topsoil holds prose then the chart. The author placed
the map inside topsoil, after the chart and before bronze, with a sound reason (no lower stratum fits, no new
stratum added), and says so. I agree with the slot. The lock says the design file and tokens change
together, so when the seat ratifies, add the one clause the author proposed ("then, for weather sites,
where the data is taken") or the next dataset page that reads the file will disagree with it. Also note
for the seat that these are the only dataset-page statistics computed from our own silver rather than
vendor or code facts; ruling 50 covers it and the page scopes them, but the review rubric section 3 reads
the opposite, so the ruling should be recorded against it.

## The author's choices

| Choice | Judgement |
|---|---|
| Isle of Man kept (spec said GBR and IRL only) | Agree, keep. Walney and Gwynt y Mor sit beside it; without it the drawing shows open sea where land is. One line in `scripts/make_outline.py` (`KEEP`) drops it. |
| Shetland cropped | Agree, keep. No site is there, Orkney is drawn, frame 500 x 616. The crop is only in a docstring; fine. |
| Table beside the map on wide screens | Right idea, wrong threshold: it clips the table at 1240 to about 1420 (finding 1). Fine at 1440. |
| Labels hidden under 760 | Hide on phones, yes; 760 is too early (finding 2). |
| Marker colours: charted sites keep chart paint, the rest unpainted | Acceptable. The row swatches act as the key and the caption says which sites keep colours. Hollow dots reading as "not charted" is the right, honest reading. |
| Outline simplification: none beyond 3 dp rounding | Fine. 21.9 KB file, 9.1 KB land path, 13.9 to 17.3 KB per page. |

## Evidence index

- Recompute scripts and silver extracts: `scratchpad/mapreview/recompute.py`, `stats.py` (output: 25 of 25 OK).
- Screenshots: `scratchpad/mapreview/shots/` (`demand-1280.png`, `demand-768.png`, `wind-1440.png`,
  `wind-390-triton.png`, `solar-390-cornwall.png`, `zoom-wind-east.png`, `zoom-wind-north.png`).
- Browser measurements: `scratchpad/mapreview/srv/measure.html` and `nojs-measure.html`.
- Note: headless Chrome screenshots of a URL with a `#fragment` come out blank in this environment, so the
  fragment and no-script behaviour were verified by DOM measurement, not by picture.


---

# Review 2 (after Revision 1)

**Verdict: APPROVE.** All nine findings are fixed or taken as prescribed; no new defects. Re-checked in the
worktree, scratch copy of the build served on 9881 and stopped afterwards (0 listeners; 9670 untouched).

## Findings against the worktree

| # | Finding | Status | Evidence |
|---|---|---|---|
| 1 | Table clipped beside the map | Fixed | Stack breakpoint `dataset.css:202` is now `max-width: 1439.98px`; padding trim at 839.98 (`:205`). Measured table `scrollWidth`/`clientWidth` in Chrome (iframe with a scrollbar): 1440 709/709 on all three pages; 1366 1199/1199; 1280 1123/1123; 1024 895/895; 768 668/668 (demand, wind, solar). Nothing clipped from 768 up. `shots/r2-demand-768.png`: "Degree-days a year" and 1,718 to 2,265 fully visible. At 390 the table scrolls (766, 644, 731 in 375) and the optional hint "The table scrolls sideways to its statistics." is shown (`hint hidden=false`), hidden at every wider width. |
| 2 | Labels hide at 760 | Fixed | Now `max-width: 479.98px` (`dataset.css:217`); labels show at 600 and 768 (`r2-demand-768.png`), absent at 390 as intended. |
| 3 | Triton Knoll caveat | Fixed | Caption (rendered, `r2-wind-1440.png`): "...17.7 km away on the Lincolnshire coast, so its statistics describe that coast, not the farm." Build enforces the 40-word budget and passes. |
| 4 | Accessible name had a dataset code | Fixed | `map_svg.accessible_name`: "Map of the UK and Ireland with the 12 wind-farm sites where the weather is taken; ..." |
| 5 | Machine codes as names | Fixed | `map_svg.SITE_NAMES` (`map_svg.py:135-161`), 25 entries, used for label, card heading, row and marker `aria-label`; code kept in mono beneath; `check` fails a site with no name (`:331`). Visible in the 1440 and 390-card shots ("Gwynt y Môr" with the code under it). |
| 6 | Tap targets 17.8 px | Fixed | `HIT_R = 18` (`map_svg.py:56`). Closest pair 22.2 px apart at 390, so hit circles overlap each other but not a neighbour's 7.5 px dot (3.9 px radius, 9.3 px clear); card test unaffected. |
| 7 | Test module skipped without Polars | Fixed | With `sys.modules['polars'] = None`: `20 passed, 1 skipped` (only `test_locations_distil.py` skips). Previously all 24 skipped. |
| 8 | Polish | Fixed | Headers "Mean at 2 m, °C", "Mean wind at 100 m, m/s"; `borders_crystalrig` no longer touches Requested (`r2-wind-1440.png`). Mixed minus left, per my own cheaper option. |
| 9 | DESIGN.md clause | Left for the seat, as the author says | Still to add at ratification, with the ruling 50 note against rubric section 3. |

## Overflow

No page overflows at 1440, 1366, 1280, 1024, 768 or 390: document `scrollWidth` equals `clientWidth` for all
three pages at every width (1425, 1351, 1265, 1009, 753 and 375 in the scrollbar-bearing iframes). All card
checks still pass: 0 of 25 cards outside the viewport or map box at 390 and 1440, Escape and outside tap close
a pinned card, focus and blur work, `aria-describedby` resolves for all 25 markers.

## Site display names

Spelling checked against public sources (WebSearch):
- **Gwynt y Môr**: correct, with the circumflex (Wikipedia "Gwynt y Môr"; RWE, owner, uses the same).
  Welsh *môr* is sea, so the accent is required.
- **Pen y Cymoedd**: correct, no accents, three words (Vattenfall's project; Wales's largest onshore wind farm).
- **Crystal Rig**: correct, two words (Wikipedia "Crystal Rig Wind Farm"; Fred. Olsen Renewables).
- Dogger Bank, Hornsea, East Anglia, Triton Knoll, Walney, Beatrice, Seagreen, Whitelee: the farms' usual
  spellings; the search did not return an operator page for each, so these eight are not individually
  confirmed but are plain, unaccented, and match the existing chart keys. Seagreen is one word as written.
- Region names (Central Highlands, Norfolk, Wiltshire and Somerset, Kent, Cornwall, Sussex, Oxfordshire) and the
  seven city names are standard English spellings, not farm names, and are labelled as regions in the author's
  notes. Unverified against a source only in the sense that none is needed.

## Gates re-run

`gridflow-build --check` OK (73 pages + 7 hubs); `pytest -q` 133 passed with the known test deselected;
htmlhint 184 files, no errors; lychee `--offline --include-fragments` 1,928 OK, 0 errors; detector `[]` x3;
0 em dashes on the three pages.

## Remaining, none blocking

- DESIGN.md clause (finding 9) for the seat at ratification.
- The operator spellings of the eight unmatched farm names were not individually confirmed against operator pages.
