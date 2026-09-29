# agws: checker review

Page `elexon/agws`, "Wind and solar generation". Checker: Opus 5.5, 2026-09-29. Against `review-rubric.md`.

## Verdict: REVISE

One major finding, no blockers, no nits. Everything else in the rubric checks out (below).

## Findings

1. **major**, `page.how_used[1]`. "Scoring a wind forecast such as WINDFOR against outturn, offshore and onshore
   apart" says WINDFOR can be scored per wind type. It cannot. WINDFOR carries a single total wind forecast with
   no production-type column. Evidence: `gridflow/src/gridflow/schemas/elexon.py:246-256` (`ElexonWindForecast`:
   `settlement_date`, `settlement_period`, `timestamp_utc`, `initial_forecast_mw`, `latest_forecast_mw`,
   `published_at`, no `psr_type`). Local windfor silver columns: `timestamp_utc, latest_forecast_mw, published_at`
   plus lineage, with no type column. This overclaims about a sibling dataset (the pilot's "same flow" class).
   Fix: score WINDFOR against onshore plus offshore summed, or give the "apart" scoring to a per-type forecast
   (`entsoe/wind_solar_forecast` carries B18 and B19). The `related` windfor note ("to score against this outturn")
   is fine as written.

## Checked and clean

### Facts
- Grain and key: `ENTITY_KEY_COLUMNS` and dedup `silver/elexon/agws.py:26,114-117`. Settlement dates 19 to 25 Sep
  have 1,008 rows and 1,008 distinct keys: 48 periods x 3 types per date.
- Derived columns:
  - `timestamp_utc` comes from `settlement_period_to_utc` (`agws.py:87-96`). The window's first and last values
    are 2026-09-18 23:00 and 2026-09-25 22:30 UTC.
  - `settlement_date` is cast as sent (`agws.py:80`).
  - `ingested_at` is stamped at transform time (`agws.py:119-124`).
- `psr_type` labels: all agws silver has exactly `Solar`, `Wind Offshore` and `Wind Onshore`, paired with
  `Solar generation` / `Wind generation`, so "solar and wind differ here" holds.
- No actual-or-estimated flag: the bronze record keys are `businessType, dataset, documentId,
  documentRevisionNumber, psrType, publishTime, quantity, settlementDate, settlementPeriod, startTime`.
- "Two and a half hours" and "period 46 published after midnight UTC" match the eight rows (01:30:01, 08:00:01,
  14:30:09, 00:00:15 next day).
- `raw_feed.requests`: host, path, `publishDateTimeFrom/To` and `page` match `endpoints.py:35-36,168-172,300-313`
  and the bronze sidecar `request_url` for 2026-09-19.
- `raw_feed.commands`:
  - `client.py` loops `while current < end` in 24 h chunks, and a bare `--end` is midnight UTC
    (`runner.py:_parse_window_bound`). So the ingest `--end 2026-09-27` fetches publish days 19 to 26.
  - Transform `--end` is inclusive (`run_transform`, `date_range`).
  - `PARTITION_SOURCE_OFFSETS` keeps the default `(0,)`.
  - Publish days 19 to 26 cover settlement dates 19 (period 1 published 01:30 on the 19th) to 25 (periods 46 to 48
    published on the 26th).
- `notebook.lead`, `needs` and `cells` are consistent with the commands. The cells are read-only.
- Related:
  - agpt carries all 11 types including the three labels.
  - fuelhh fuel types include `WIND` and no solar code.
  - `entsoe/wind_solar_forecast.py:23-24` maps B16, B18 and B19.
  - windfor's endpoint description is "Wind Generation Forecast".

### Chart provenance
- The series is `spec_origin: vault` with 3 series x 336 points and 1,008 rows used. No staged spec and no
  authored override exist. The build digest check passes.
- **Writer flag 2 (`aggregation: sum`).** There is exactly one row per series and half-hour in the window: 0
  duplicate `(timestamp_utc, psr_type)` pairs and 0 duplicate keys. The distil provenance shows
  `duplicates_dropped: 0`. So "one value per production type" is accurate, and "summed" in the caption refers
  correctly to the stack's top edge.
- Alt numbers were recomputed from the committed series and all match:
  - onshore 488 to 8,767;
  - offshore 421 to 11,476;
  - solar 0 to 10,099, with settlement-day peaks 6,158 to 10,099 and 0 at every point from 20:00 to 03:59 UTC;
  - wind combined 1,598 (22nd) to 19,115 (19th);
  - total 2,015 to 25,051.
- `plot_alt` also matches: offshore 11,476 and onshore 8,767 on the 19th. On the 22nd, both stay below 3,400 by
  settlement day (3,392 and 2,202) and by UTC day (3,392 and 2,814). The PNG was inspected.
- **Writer flag 1 (palette).** The onshore `hatch-lines` complies with the rules. DESIGN.md:43-44 gives wind one
  colour (horizon) and forbids other series colours. The offshore/onshore split is the dataset's point, so merging
  the two (as agpt does) would defeat it. The key note explains the hatch. There is no khaki and nothing signed
  (minimum 0.0). The rest is taste, for Bobbo.

### No local data
- Grepping the `page:` block and the rendered text for `locally|held|our |since 20|rows|% of|live|now|real-time|—|→|·`
  found only false positives: "our" inside "half-hour" and "colour", and "the rows below" meaning the page's
  eight rows.

### Budgets and structure
- `gridflow-build --only elexon/agws` passes after a fresh rebuild.
- `detect.mjs --json` returns `[]`.
- Samples are `generated_by: gridflow-sample`.
- The guide covers all 9 non-pipeline columns, key columns first.
- The notebook is `generated_by: scripts/run_notebooks.py`, with 5 cells and no errors.

### Distinct from agpt and fuelhh
- agpt stacks every type with wind summed, over 14 to 20 Sep.
- fuelhh has one `WIND` code and no solar.
- agws splits offshore and onshore over 19 to 25 Sep, and the page says what the others lack.

### Rendering
- Headless Chrome full-page shots at 1440, 1024 and 768, and at 390 in a 390 px iframe, were looked at section
  by section. Hero scenery tops, chart tags, axis ticks (UK midnight), key notes, stratum corner labels, frame,
  guide and related are all fully visible, with no overlap.
- At 390 the hero scenery shows the right-hand part of the scene (offshore wind, interconnector). That is the
  template's crop, not agws content.
- The opened states (frame unfolded via `#fx`, notebook open) were **measured, not seen**: browser-pane
  screenshots timed out. At 390, 768, 1024 and 1440:
  - no element extends past the viewport outside a scroll container;
  - `scrollWidth` is at most `innerWidth`;
  - the notebook image sits within its box.
  At 390 the `.head()` table scrolls in its own container (517 px in 300), which is the template issue the writer
  reported.
- The site has no dark theme: there is no `prefers-color-scheme` or `data-theme` in any CSS or JS.

### Vault body edits (writer flag 3)
1. `ingested_at` is transform time: verified at `agws.py:119-124`. The smallest span was changed.
2. The sample `timestamp_utc` for period 4 of 2026-05-06 (a BST day) is 00:30 UTC. This matches the note's own
   bronze `startTime` 00:30Z.
3. The July publish-day claim was rechecked:
   - `agws_20260724.parquet` holds 23 Jul periods 46 to 48 (9 rows) and 24 Jul periods 1 to 45 (135 rows).
   - `ingested_at` is 2026-09-27, confirming the re-transform.
   - `published_at - timestamp_utc` is 150 min on all 3,600 rows of settlement dates 1 to 25 Sep.
   - The replaced span is scoped to BST and cites code. The surrounding advice is unchanged.
