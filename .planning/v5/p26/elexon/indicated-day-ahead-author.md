# indicated-day-ahead (lead `indgen`; `inddem`, `imbalngc`, `melngc`): author report

Writer, 2026-09-29. Worktrees as in `BATCH-elexon.md`. The `page:` block is in the canonical
`30-vendors/elexon/datasets/indgen.md` (vault worktree). The four notes were copied byte for byte to
`vault/elexon/{indgen,inddem,imbalngc,melngc}.md` in the front-end worktree (`cmp` clean; CRLF kept:
302/302, 160/160, 159/159, 158/158 lines).

## Status

- Artefacts, all from real data, each run by its own tool:
  - `site/hifi/data/series/elexon/indgen.json`: `gridflow-distil`, `spec_origin: vault`; 2 series,
    45 x-points, 83 rows used.
  - `site/hifi/data/samples/elexon/indgen.json`: `gridflow-sample`.
  - `site/hifi/data/notebooks/elexon/indgen.json` plus `indgen-6.png`: `scripts/run_notebooks.py`;
    6 cells, no errors.
- `uv run --system-certs --extra build gridflow-build --only elexon/indgen`: green. It wrote
  `data-sources/elexon/indicated-day-ahead.html`.
- `detect.mjs --json`: `[]`.
- There was no staged spec and no authored override for any of the four members.
- **Chart.** A line chart from silver `elexon/indgen`, boundary `N`, MW, settlement date 17 September
  2026, with two series:
  - the 10:48 UTC publish of 16 September: 38 points, from 04:00 UTC;
  - the 00:17 UTC publish of 17 September: 45 points, from 00:30 UTC.

  There is one value per half-hour per publish, and nothing is summed across publishes.

## What the checker should look hardest at

1. **Definitions and signs** (`what_it_is`, `family.members[].differs`, `related`). They come from the
   Elexon BSC glossary, fetched 2026-09-29. `INDDEM` is not the demand side of `IMBALNGC`, and the page
   never implies it is.
2. **Grain and key.**
   - Silver holds one row per (half-hour, zone) per UTC publish day. It is not one row per half-hour.
   - `record.key` is (date, period, boundary, `published_at`). That key is unique over indgen silver:
     25,956 rows and 25,956 distinct keys. The transformer's 3-column dedup key is not unique across
     files (14,076 distinct).
   - `imbalngc` and `melngc` silver have no zone column at all.

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| INDGEN is the sum of positive Physical Notifications (exporting BM units), half-hour average MW, for each System Zone and nationally (`what_it_is`, `differs`, `fields.indicated_generation_mw`) | https://elexon.co.uk/glossary/indicated-generation; body now quotes it with the link |
| INDDEM is the sum of negative PNs (importing units), so values are negative (`what_it_is`, `differs`) | https://elexon.co.uk/glossary/indicated-demand. Bronze 17 Sep: `demand` min/max at N −22,653/−11,005, every boundary negative (probe over 47,970 joined rows). The notebook head shows −16,171 to −18,313 |
| IMBALNGC = INDGEN minus the Transmission System Demand forecast (`what_it_is`, `differs`, `related` tsdf) | https://elexon.co.uk/glossary/indicated-imbalance. Project check, bronze 17 Sep, same publish and boundary: `imbalance − (generation − tsdf.demand)` max abs 334 MW at N, ≤148 elsewhere. Silver (all joined publishes) max abs 63 MW. Notebook cell 5 on the 00:17 publish shows min −62, max 0 |
| IMBALNGC is not INDGEN + INDDEM | Bronze 17 Sep 10:48 N: generation 28,167, demand −22,185, imbalance 2,090 (g+d = 5,982) |
| MELNGC = sum of submitted MELs minus the National Demand Forecast; larger means more spare capacity (`what_it_is`, `differs`, `how_used` 2, `related` ndf) | https://elexon.co.uk/glossary/indicated-margin. **Not reproduced**: gridflow holds no MEL table |
| Imbalance sign (field meaning only, not stated on the page as a rule) | The glossary states no sign. By its definition, positive = INDGEN above the forecast. `schemas/elexon.py:336-339` docstring: "negative = system short, positive = long". Body records both |
| Unit MW for imbalance and margin | `schemas/elexon.py:338` (imbalance MW), `:358-361` (margin MW). The glossary definitions are differences of MW quantities |
| `boundary` values `N` and `B1`..`B17` (`fields.boundary`, `what_it_is`, `differs`) | indgen/inddem silver `value_counts`: 18 values, N + B1..B17. Bronze 17 Sep, all four: 18 boundaries per publish |
| "gridflow sends no `boundary`, so the national row and every zone arrive" (`raw_feed.note`) | `connectors/elexon/endpoints.py` `build_params` (≈l.284-315): PUBLISH_DATETIME adds only from/to and `page`. Bronze has 18 boundaries |
| Request URL shape, 24 h windows, `page=1` (`raw_feed.requests`, `family.request`) | `endpoints.py:121-139,200-209` (paths); `max_chunk_hours: int = 24`; `client.py:93-99` chunks; bronze meta `request_url` for 2026-09-17 (unencoded form as on the approved `ndf` page) |
| Ingest `--end` exclusive; transform `--end` inclusive (`commands`) | `client.py:96` `while current < end`; the transform convention is as on the approved ndf/indo pages. The window 16 to 18 (ingest) and 16 to 17 (transform) covers publish days 16 and 17, the two the chart uses |
| One silver file per UTC publish day; dedup `(date, period, boundary)` `keep="last"`, unsorted (`grain`, `fields.published_at`) | `silver/elexon/indgen.py:114-117`, `inddem.py:114-117`; bronze meta shows one file per 24 h publish window |
| imbalngc/melngc drop `boundary` (`grain`, `differs`) | `imbalngc.py:117` (dedup on date, period), `:127-135` (no boundary in output_cols); `melngc.py:116,126-134` |
| Which publish silver keeps: 00:17 UTC, plus about 10:48 UTC for the half-hours that publish adds (chart key notes, frame caption "both kept publishes") | Bronze row order: newest publish first (17 Sep file: row 0 is 23:47, the last rows are 00:17). Silver vs "earliest publish per key" recomputed from bronze for all 14 files × 4 datasets: 0 value, 0 `published_at` and 0 `timestamp_utc` mismatches. The imbalngc/melngc survivor equals the `N` row in all 14 files |
| `timestamp_utc` = vendor `startTime` (`fields.timestamp_utc`) | Same 14×4 recompute: 0 mismatches |
| Day-ahead line starts 04:00 UTC; for earlier half-hours silver keeps another 16 Sep publish (key note) | Silver file 20260916 holds 00:17 (periods to 03:30 UTC 17 Sep) and 10:48 (from 04:00 UTC 17 Sep); series `day_ahead` first point 04:00 |
| Same-day line starts 00:30 UTC: the publish holds no earlier half-hours (key note) | Bronze 17 Sep, publish 00:17, N: first `startTime` 00:30 UTC; series `same_day` first point 00:30 at 25,277 |
| Alt text numbers | Committed series: within 1,122 MW (min diff −1,122 at 05:00) to 06:30; from 07:00 same_day > day_ahead at every point, max +5,992 at 11:30; day_ahead min 22,495 at 13:00; peaks 18:30, 33,220 / 31,228 |
| Frame rows (caption) | `gridflow-sample` output: 17 Sep period 36 (16:30 UTC), boundaries B1/B6/B9/N × publishes 10:48 16 Sep and 00:17 17 Sep |
| Notebook lead: relations, `settlement_date` filter, inclusive, lineage dropped | gridflow_models `research/handles/source.py:401-450`; `schema_manifest.py:122-130` (date column `settlement_date` for all four); tsdf is the same path |
| plot_alt numbers | Silver, 00:17 17 Sep publish, N: tsdf max 33,351 at 18:00; melngc min 24,475 at 18:30; imbalngc min −1,026 at 07:30, max 6,430 at 22:30; span 00:30 to 22:30 |
| Cadence "about every 30 minutes" | Bronze 17 Sep: 47 publishes at about :17 and :47 (same basis as the approved `ndf` fact) |

## Note-body corrections (canonical vault, then mirror)

All four notes:

- **Silver sample `timestamp_utc`.** Changed 2026-05-06T04:00 to 03:00 UTC for period 9 in BST. The note's
  own bronze sample shows `startTime` 03:00Z, and silver = `startTime` in every row checked.
- **`ingested_at`.** Changed "Time ingested into bronze" to "silver transform time". Evidence:
  `indgen.py:119-124`, `inddem.py:119-124`, `imbalngc.py:119-125`, `melngc.py:118-124`.

`indgen`:

- **Dedup key.** "_inline in transformer_" now gives the explicit key and `keep="last"` unsorted, with
  lines 114-117.
- **`boundary`.** "`N` or `Z` (zonal)" changed to "`N` or `B1` to `B17`".
- **Gotcha.** "multiple publishes per period" now explains which publish survives and the need to
  filter on `published_at`.
- **New "Definition" bullet** with a glossary link.

`inddem`:

- **Overview.** "the GB demand component of the NESO indicated-imbalance forecast" is wrong. It now reads
  "sum of negative PNs, so negative; not the demand in IMBALNGC" (glossary links).
- **Dedup key, `boundary`, and `indicated_demand_mw`.** Same fixes as `indgen`; the demand notes add
  "negative".
- **Gotcha.** "latest wins after dedup" is wrong. It now describes the unsorted `keep="last"`, so the
  survivor is the day's earliest publish.

`imbalngc`:

- **Overview.** "(generation minus demand)" changed to "INDGEN minus the TSDF forecast; not INDGEN plus
  INDDEM" (glossary link).
- **Unit.** MWh changed to MW (`schemas/elexon.py:338`).
- **Dedup key.** Adds that `boundary` is in neither the key nor the output (`imbalngc.py:117,127-135`),
  so the surviving zone depends on API row order. It was `N` in the files checked.
- **Gotcha.** "keeps the latest" is wrong. It now describes the unsorted `keep="last"`, so the survivor is
  the earliest publish of the day.
- **New "Sign" bullet.** The glossary states no sign; the code docstring's sign and the project's 334 MW
  check are given, each labelled.

`melngc`:

- **Overview.** "canonical short-term de-rated margin signal" is wrong. It now reads "sum of MELs minus
  the National Demand Forecast; not de-rated; LOLPDRM differs" (glossary link).
- **Dedup key.** Same `boundary` note as `imbalngc` (`melngc.py:116,126-134`).

Not touched: existing em dashes in the bodies, the curl examples (correct for the vendor), and
`last_verified`.

## Unverified

- **MELNGC.** The MEL-minus-forecast definition is the vendor's; no MEL data exists to reproduce it.
  The `related` note links `elexon/ndf` as "the national demand forecast MELNGC subtracts", on the
  glossary's term "National Demand Forecast". I did not check that it is numerically the NDF dataset.
- **Zones.** That `B1` to `B17` are Elexon's "System Zones" is inferred: the glossary names System Zones
  plus a national value, and the field carries `N` plus `B1` to `B17`. The page does not map codes to
  places.
- **Imbalance sign.** No vendor sign sentence exists. The page states only the definition. The body
  records the code docstring's "negative = short" as a code claim.
- **Opened notebook drawer.** Its outputs table and plot were not screenshotted in the rendered page;
  headless `--screenshot` cannot click. The JSON outputs and the PNG were inspected directly.
- **Dark mode.** The site has no dark theme: no `prefers-color-scheme` or `data-theme` in the CSS or
  JS. `--force-dark-mode` renders were identical, so one scheme per width was checked.

## Screenshots

Taken with headless Chrome at 1440, 1024, 768 and 390 (a 390 px iframe), served from `site/hifi` on
127.0.0.1:9751. The server was started under `timeout 1500`, so it exits by itself; Chrome profiles are
under `scratchpad/ida-chrome/`.

Nothing is clipped or overlapping at any width: hero scenery tops and labels, chart axes, key notes,
the frame fold and guide, the notebook drawer, stratum corner labels and related. At 390 the hero
shows the right-hand part of the scene (offshore wind, interconnector, substation) with labels whole.

The notebook's first code cell was reflowed to short lines after the first pass, where one 90-character
line wrapped mid-token at 768. About one in five tall (9,000 px) headless renders came back partial
(blank below about 2,000 px). A retake fixed it each time; this is not a page fault.

## Open questions (for the seat)

1. **gridflow row-order dependence.** This is a gridflow code issue, not page work.
   - `indgen` and `inddem` dedup with `keep="last"` and no sort. `imbalngc` and `melngc` also drop
     `boundary` from the key and output.
   - What silver holds therefore depends on the order the API returns rows. Today that is newest first,
     so silver holds each publish day's earliest publish and, for imbalngc/melngc, the `N` row.
   - If Elexon reorders the rows, silver silently changes meaning. The page states only the code facts.
   - The fix belongs in gridflow: sort by `published_at`, and add `boundary` to the imbalngc/melngc
     key and output. Worth a gridflow issue.
2. **One chart spec reads one silver table.** A trader's view of generation against the demand forecast
   with margin cannot be drawn in the chart, so it is in the notebook. The caption says so. This is by
   design; I raise it only in case a multi-table chart is wanted for family pages.

## Template problems

- `run_notebooks.py` mis-parses a DataFrame whose index has a name. `timestamp_utc` printed on a
  second header row, and the columns shifted: 12 headers for 6 values. I avoided it with
  `nat.reset_index().head()`. The parser should handle a named index. Not blocking.
- None blocking the build.

## Revision 1 (after `indicated-day-ahead-review.md`: REVISE, 1 major, 3 nits)

Only `page:` fields in the canonical `indgen.md` changed. The note was mirrored byte for byte (`cmp`
clean, CRLF 302/302). The series, sample and notebook were not re-run: their inputs did not change and
the build's digest check passed.

- **Major 1: the zone row that `imbalngc`/`melngc` silver keeps.** Evidence: `imbalngc.py:117`,
  `melngc.py:116`, where `keep="last"` has no sort and `boundary` is not in the output.
  - `family.members[imbalngc].differs`: now "`INDGEN` minus transmission demand forecast, MW; silver
    keeps the zone row listed last, unlabelled" (14 words).
  - `family.members[melngc].differs`: now "Summed MELs minus national demand forecast; silver keeps the zone
    row listed last, unlabelled" (14).
  - `facts.grain`: now "One row per half-hour, zone, publish day; IMBALNGC, MELNGC keep one unlabelled
    zone row" (14).
  - `what_it_is`: rewritten to 59/60 words. It ends "Silver keeps one unlabelled `IMBALNGC` and `MELNGC`
    zone row per half-hour, the API's last (`N` in this window)." That scopes the `N` observation to the
    window shown. The Elexon definitions are kept. "(exporting units)" and "so is negative" were dropped
    for budget; the `inddem` member line still says "so negative".
  - `notebook.lead`: "national rows" now reads "the 00:17 UTC publish, with `boundary` filtered to `N`
    where present" (33 words). It no longer claims the imbalngc/melngc rows are national. Cell 5's check
    (−62 to 0 MW against INDGEN `N` minus TSDF `N`) remains the visible evidence for the window.
- **Nit 2: `chart_view.alt`.** The peaks are now paired with their publishes: "at 33,220 (00:17) and
  31,228 MW (10:48)" (90/90 words). The values were checked against the committed series: `same_day` max
  33,220 and `day_ahead` max 31,228, both at 18:30.
- **Nit 3: `related[elexon/ndf]`.** No change. The checker accepts it as a term match. It stays listed
  under "Unverified" for the seat.
- **Nit 4: code wraps mid-token at 390.** No change. This is template CSS (the code block breaks words
  at any character), which I may not edit. Reported to the seat as a template item.

**Checks.** `gridflow-build --only elexon/indgen` is green (it wrote `indicated-day-ahead.html`), and
`detect.mjs --json` returns `[]`. The rendered page shows the new text.

**Screenshots.** Headless Chrome, each call under `timeout 60`, at 1280 and at 390 in a 390 px iframe,
served on 127.0.0.1:9751 under `timeout 400`. The facts, what it is, the member lines, the notebook lead,
chart, frame, guide and related are all whole. Nothing is clipped or overlapping.
