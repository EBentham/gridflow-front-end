# elexon/atl: author report

Writer, 2026-09-28. Page: `site/hifi/data-sources/elexon/atl.html` in the p26-elexon worktree.

## Status

- The `page:` block and the body corrections are in the vault worktree note
  `30-vendors/elexon/datasets/atl.md` (CRLF, edited with Edit). The mirror `vault/elexon/atl.md` is a
  byte-for-byte copy (`cmp` clean).
  - The old mirror file was LF, so the mirror diff will show every line changed. The batch file asks for
    this (five other mirror files are already CRLF).
- Artefacts written by the tools:
  - `site/hifi/data/series/elexon/atl.json`: gridflow-distil, `spec_origin: vault`, 206 points;
  - `samples/elexon/atl.json`: gridflow-sample, 8 rows × 13 columns;
  - `notebooks/elexon/atl.json` and `atl-5.png`: `scripts/run_notebooks.py`, 6 cells, 1 image, no errors.
- There was no staged spec or authored override to remove.
- `gridflow-build --only elexon/atl` passes. `detect.mjs --json` returns `[]`.
- Screenshots checked at 1440, 1024 and 768, plus a true 390 (see "Screenshots"). Nothing is clipped or
  overlapping. The site has one theme: no `prefers-color-scheme` or dark rules in the assets, so there
  was no dark mode to check.

## Chart

- Line chart of `total_load_mw` from `elexon/atl`, MW.
- Filter `settlement_date` 14 to 20 Sep 2026. Window `2026-09-13..2026-09-20`, the same week as the
  demand-outturn page.
- `aggregation: last`, no dedup: silver has one row per key (0 duplicate `(settlement_date,
  settlement_period)` across all 403 silver rows).
- Paint: petrol.

## How atl differs from demand-outturn (INDO)

- ATL is the B0610 "Actual Total Load Per Bidding Zone" item (`connectors/elexon/endpoints.py:173-176`).
- It is a different figure from INDO. The notebook merges the two on `(settlement_date,
  settlement_period, timestamp_utc)` and groups `atl_minus_indo_mw` into 6-hour UTC blocks:

  | From UTC hour | Median | Min | Max |
  |---|---|---|---|
  | 00 | 2,510 | -874 | 5,003 |
  | 06 | 6,357 | -23,291 (the 2,670 MW half-hour) | 12,876 |
  | 12 | 7,916 | 2,154 | 15,704 |
  | 18 | 3,686 | 902 | 6,079 |

- The page states the difference only as measured in the notebook. It gives no cause, because no
  definition of B0610 total load is quoted in the repo or vault (see open questions).

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Endpoint `/datasets/ATL`, `PUBLISH_DATETIME` params, 24 h chunks (`raw_feed.note`, `requests`) | `connectors/elexon/endpoints.py:173-177` (`max_chunk_hours` default 24, `:39`). `client.py:93-99`: chunk loop `while current < end`. `endpoints.py:300-313`: `publishDateTimeFrom/To` via `_to_utc_z`, plus `page`. |
| Request URL format | Bronze sidecar `bronze/elexon/atl/2026/09/20/raw_20260926T182917Z_308e17e6.meta.json` `request_params`: `publishDateTimeFrom=2026-09-20T00:00:00Z`, `publishDateTimeTo=2026-09-21T00:00:00Z`, `page=1`. |
| Ingest `--end` exclusive; ingest 14 to 22, transform 14 to 21 (`commands`) | `client.py:96` `while current < end`. Bronze partition = chunk start date (`client.py:315`, `data_date`); silver day D reads bronze day D (`silver/elexon/atl.py:31-37`). Settlement date 20, period 48 is in silver file `atl_20260921.parquet` (published `2026-09-21 00:29:01`, shown in the frame). Period 1 of the 14th was published `2026-09-14 00:59:05`, so no day-early start is needed. |
| "run a day past 20 September: its period 48 was published after midnight UTC" | The frame's last row: period 48, `published_at` 2026-09-21 00:29:01 UTC. |
| Grain one row per settlement period; key `(settlement_date, settlement_period)` | `silver/elexon/atl.py:26-29` (`ENTITY_KEY_COLUMNS`), `:115` `unique(subset=[...], keep="last")`. |
| `timestamp_utc` computed from date and period (`fields`) | `atl.py:88-97` `settlement_period_to_utc`. The vendor's `startTime` is not read (not in `column_mapping`, `atl.py:61-69`). |
| `total_load_mw` = vendor `quantity`, MW | `atl.py:65`; MW from the schema column name `ElexonATL.total_load_mw` (`schemas/elexon.py:590`). |
| `document_id` / `document_revision` / `published_at` sources | `atl.py:64`, `:66-67`, and `:101-106` (parsed as UTC). |
| No `business_type` column | `atl.py:70` renames only present keys; `:137` selects available columns. Local silver schema has no `business_type`; the vault bronze sample and the bronze file for the 20th carry no `businessType`. |
| Cadence "One vendor document per settlement period, each published on its own" | Each row has its own `documentId` and its own `publishTime`: the frame shows 8 distinct ids and 8 distinct `published_at`. There is deliberately no "half-hourly" or "every 30 minutes", because many periods have no row. |
| Chart numbers: daily highs 30,836 to 34,330; lows 19,958 to 22,392 at 03:30 to 05:00 UTC; 2,670 MW at 06:30 UTC on the 18th between 25,600 and 30,651; lone dots on the 16th (06:30) and 18th (23:30) | Committed series (206 points). Polars over the series: per settlement date min/max; lone points from the renderer's run logic (`chart_svg.py:307-322`) with its mean step, 49.0 min. Row check: 18 Sep, period 15 = 25,600, period 16 = 2,670, period 18 = 30,651 (period 17 has no row). |
| "many half-hours have no row, mostly before midday" (caption, `what_it_is`, alt; scoped to the week charted) | Series: 206 of 336 half-hours present; of the 130 absent, 92 are before 12:00 UTC. Numbers are not on the page; the gaps are visible in the chart. |
| "the line breaks at two or more in a row but joins across a single one" (caption) | `chart_svg.py:307-322`: `_runs` splits at `gap > step*1.5`, with `step` the mean spacing (`:259`). Here that is 49.0 min, so the threshold is 73.5 min: a single missing half-hour (60 min) is bridged, two (90 min) break. 43 single gaps are bridged in this series. |
| Notebook lead: relations, date column, inclusive ends, lineage dropped | `gridflow_models/research/handles/source.py:401-451`. `_RELATION_NAME_BY_DATASET['atl']` = `silver_elexon_atl`; date column `settlement_date` (`gridflow/silver/schema_manifest.py:114`). `_BITEMPORAL_EXCLUDE` = event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year. |
| Notebook `timestamp_utc` converted to UTC | The kernel returns `timestamp_utc` in local time (+01:00): the first run showed `2026-09-14 00:00:00+01:00`. Cell 2 now calls `tz_convert("UTC")`, so the `from_hour_utc` blocks are UTC. |
| `what_it_is` "median 7,916 MW above INDO from 12:00 to 18:00 UTC" | Notebook cell 6 output, row `from_hour_utc` 12. |
| `plot_alt` | `atl-5.png`: INDO continuous; ATL broken at NaN, peaking near 34,000 MW; INDO evening peaks up to about 30,800 MW (30,813 on the 16th per the INDO page); ATL dip to about 2,700 MW on the 18th. |
| Related: `elexon/agpt` "same B-series group" | `endpoints.py:162` comment "ENTSO-E / B-series datasets (AGPT, AGWS, ATL)". |
| Related: `elexon/ndf` "forecast of national demand, not of total load" | Matches the demand-outturn page's ndf note ("Day-ahead forecast of national demand"). |

## Note body corrections (vault note, smallest span each)

1. Silver schema, `business_type` row: now says it is written only if the response carries
   `businessType` (`silver/elexon/atl.py:70`, `:137`). The note's own bronze sample has none, so silver
   has no such column.
2. Silver schema, `ingested_at` row: "Time ingested into bronze" is now "Silver transform time"
   (`atl.py:117-121`). This is the same stale fact as the fuelhh one.
3. Silver sample:
   - `timestamp_utc` for settlement date 2026-05-06, period 5 was `02:00Z`; it is `01:00Z`, checked
     with `settlement_period_to_utc(date(2026,5,6), 5)` and matching the bronze `startTime`;
   - the placeholder `"business_type": "..."` line is removed.
4. Implementation delta: "Same B-series as AGPT (B0610)" is now "Same B-series group as AGPT (B1620);
   ATL is B0610" (`connectors/elexon/endpoints.py:162-176`).

Left alone: the curl example, which is correct for the vendor. Also left alone, and not carried onto
the page, because nothing evidences them:

- "Historical depth: several years";
- "Publication lag: soon after each settlement period closes";
- "ATL is what the EU transparency platform consumes for GB load".

The silver schema table does not list the lineage columns (`event_time`, `available_at`,
`source_run_id`, `dataset_version`) that silver carries. It is an omission rather than a wrong fact, so
it is not edited.

## Not verified

- **Why about 130 of 336 half-hours have no row.**
  - The bronze file for the 20th is a single page (`total_pages: 1`) holding 28 records for a 24-hour
    publish window. So the vendor's response lacked them; gridflow did not drop them.
  - Every row's `published_at` minus `timestamp_utc` is 119 minutes, so no late publications appear in
    the fetched windows.
  - Whether Elexon publishes the missing periods later, under another query style, or never is
    unknown. AGPT, from the same B-series group, has all 48 periods locally for the same dates.
  - The page states none of this; it only scopes "many half-hours have no row" to the week charted.
- **The 2,670 MW half-hour** (18 Sep, period 16): a vendor value as sent. Its cause is unknown and the
  page gives none. Similar low runs exist in August silver (for example 592 to 1,058 MW on 2 Aug) but
  are outside the window.
- **What B0610 total load includes** (and so why it exceeds INDO most in daytime). No definition is
  quoted in the repo or vault; the ENTSO-E vault note `30-vendors/entsoe/datasets/actual_load.md`
  describes the ENTSO-E A65/A16 series, not Elexon's ATL.
- **Interactive states, now checked.** Unfolded frame (`#fx` checked) and notebook drawer open (button
  clicked on load):
  - captured from a scratchpad copy of the page (`atl-shot/`, served on 9723, then stopped);
  - checked at 1440, 768 (iframe) and 390 (iframe); nothing is clipped or overlapping;
  - wide frames and notebook tables scroll sideways inside `.df-wrap` / `.ds-dfs` (`overflow-x: auto`)
    by design.
  - The notebook plot is `loading="lazy"`: in the first 390 iframe capture it had not loaded and showed
    its alt text. With `eager` in the scratch copy it renders, so that was a capture artefact.

## Open questions

1. Research unit, recommended: does ATL return full days through a settlement-date query or the stream
   endpoint, and does Elexon publish the missing periods later? Until then, any GB load model using ATL
   must handle missing half-hours.
2. Where is Elexon's definition of B0610 actual total load? With it, `what_it_is` could say what the
   ATL minus INDO gap is made of.

## Template problem (report only; nothing worked around)

- `chart_svg.py:259` sets `_Plot.step` to the **mean** spacing of the points present, and `_runs`
  (`:307-322`) breaks a line only when a gap exceeds `1.5 * step`.
  - For a sparse half-hourly series like this one (step 49 min), a single missing half-hour is drawn
    as a straight segment, which interpolates against the brief's "time gaps break the line".
  - Suggested fix: derive the step from the minimum or modal spacing (or the distilled grain).
  - The caption says what is rendered today. It would need its last clause changed once the renderer
    is fixed ("the line breaks where a half-hour has no row").
- Headless Chrome on this machine has a 500 px minimum viewport, so a plain `--window-size=390,...`
  shot is a 500 px layout cropped to 390 and looks clipped. The true 390 check here used a 390 px
  iframe in a local wrapper file (scratchpad `atl-wrap390.html`). Other writers' "390" shots may have
  the same artefact.

## Screenshots

In the scratchpad `atl-shots/`:

- `atl-1440.png`, `atl-1024.png`, `atl-768.png`, and crops `c1440-*`;
- `sheet768.png`, `sheet1024.png`;
- the true 390: `real-390.png` and crops `r390-*`.

Open states: `open-1440.png`, `open-768c.png`, `open-390b.png`, and crops `o1440-*`, `o768-sheet`,
`o390-sheet`, `open-check`. `atl-390.png` is the misleading 500 px capture; ignore it. Direct
(non-iframe) 768 captures stalled twice; the iframe wrapper worked. Headless Chrome did not exit after the
first capture: I left its processes running (never kill processes); the dev server is stopped.

## Revision 1 (2026-09-29): renderer fix merged (main 165ce0a)

- **What changed upstream.** `chart_svg.py:193-200` `_step` is now the series' smallest spacing
  (30 min here). The gap threshold is 45 min, so the line breaks at every missing half-hour. The
  template problem reported above (mean-step bridging) is resolved.
- **Rendered result.** The chart is now 70 pieces, 33 of them lone points drawn as dots (33 `r="3.2"`
  circles in each of the wide and narrow SVGs).
- **The 2,670 MW half-hour.** On the 18th it is now the end of a two-point piece: 06:00 is 25,600 MW,
  06:30 is 2,670 MW, and there is no row at 07:00.
- **`chart_view.caption` reworded (38 words):** "... Many half-hours have no row: the line breaks at
  each one, and a reading with no neighbour shows as a dot." It replaces "breaks at two or more in a
  row but joins across a single one".
- **`chart_view.alt` reworded:**
  - "in short pieces and lone dots: the line breaks at every half-hour with no row, most of them before
    midday UTC";
  - highs and lows unchanged (30,836 to 34,330; 19,958 to 22,392 at 03:30 to 05:00 UTC);
  - "At 06:30 UTC on the 18th the line drops from 25,600 to 2,670 MW and stops there".
  - The old "two lone readings" sentence is gone (there are now 33).
- **Earlier change.** `facts.cadence` became "One vendor document per settlement period, each published
  on its own" (dropped "Half-hourly", a universal on a sparse series).
- **Gates.** Mirror re-copied (`cmp` clean). `gridflow-build --only elexon/atl` wrote the page with no
  errors; `detect.mjs --json` returns `[]`. No other text needed changing: nothing else describes
  bridging, and there are 0 hits for the old wording in the note or the page.
- **Screens.**
  - Checked 1440 (via a 1440 px iframe) and a true 390 (390 px iframe): `atl-shots/rev1-1440.png`,
    `rev1-1440-chart.png`, `rev1-390.png`, `rev1-390-sheet.png`.
  - Nothing is clipped or overlapping; dots sit inside the plot frame at both widths.
- **New template nit (report only).**
  - Since the fix, the narrow (390) x-axis ends "... 19 20 21": a "21" label sits at the axis end
    (x 350 of the 360 viewBox), about 6 px from "20" and not overlapping (`rev1-390-axis.png`).
  - The chart holds no settlement date 21.
  - Cause: `chart_svg.py:234` `hi_edge = hi + step` now lands exactly on the 21st's 23:00 UTC boundary,
    so `_midnights(lo, hi_edge, ...)` (`:261-264`) yields a zero-width day-21 tick at the edge.
  - The wide axis drops its label via the `x + half <= fr.x1 + 8` check; the narrow axis keeps it.
  - Suggested fix: skip a day tick whose start is at or past `hi_edge`.
  - This likely affects every line page whose last point is the final half-hour of its window.

## Revision 2 (2026-09-29): the review's three nits (`atl-review.md`, APPROVE)

1. `how_used[2]`:
   - was "A load feature for a GB power price model, once missing half-hours are handled."
   - now "A total-load feature for a GB power price model."
   - The gaps are no longer presented as a property of ATL in general; they stay scoped to the week
     charted in `what_it_is` and the caption.
2. `facts.cadence`:
   - was "One vendor document per settlement period, each published on its own."
   - now "Each settlement period sent as its own document, as the frame shows."
   - Scoped to the eight rows: 8 distinct `document_id` and `published_at`.
3. `summary`:
   - was "... actual total load for each half-hour settlement period: ..."
   - now "Great Britain's actual total load by settlement period: one MW figure per period, Elexon data
     item B0610." (17 words)

Gates: mirror re-copied (`cmp` clean); `gridflow-build --only elexon/atl` wrote the page with no
errors; `detect.mjs --json` returns `[]`; 0 hits for the old wording in the rendered page. The layout
is unchanged, since all three edits are the same length or shorter in existing fields, so the Revision 1
screens stand.
