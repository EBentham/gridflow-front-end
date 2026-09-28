# elexon/windfor: checker review

Checker, 2026-09-29. Page `site/hifi/data-sources/elexon/windfor.html` in the `p26-elexon` worktree, rebuilt
before judging.

## Verdict: REVISE

2 major, 1 nit. No blockers.

## Findings

### 1. major: `page.summary`, `page.facts.grain`, `page.what_it_is`, `page.raw_feed.note`, `page.record.fields.timestamp_utc` (and body Overview)

**What is wrong.** "Hourly" is stated as a property of the dataset, but no source backs it except our own rows.
It appears in five fields:

- `summary`: "Elexon's hourly forecast";
- `facts.grain`: "One row per target hour and issue time";
- `what_it_is`: "Each issue gives one figure per hour";
- `raw_feed.note`: "one row per hour and issue";
- `record.fields.timestamp_utc`: "Target hour the forecast is for".

The rubric (section 1, last item) does not allow a universal measured on our copy. The body Overview has the same
problem: it reads "hourly, reissued up to 8 times a day: Elexon's OpenAPI description ... says", but the cited
description supports only the reissue schedule.

**Evidence.**
- Local `swagger.json` (scratchpad, 2026-09-27) has no resolution anywhere in the WINDFOR material:
  - no "hour", "hourly", "half-hour" or "resolution" in the descriptions or parameters of `/datasets/WINDFOR`,
    `/datasets/WINDFOR/stream` or `/forecast/generation/wind*`;
  - `DatasetRows.WindGenerationForecast` has only `dataset`, `publishTime`, `startTime` and `generation`.
- The code does not fix a step. `silver/elexon/wind_forecast.py:98` also maps `startTimeOfHalfHrPeriod` to
  `start_time`.
- The only support is local silver: `timestamp_utc.dt.minute()` is 0 on all 860,715 rows. That is a measurement of
  our copy.
- The writer's report lists "Hourly interval" under Unverified.

**Fix.** Either quote a vendor source for the hourly step in the note, or scope the claim to what the page shows.
For example:
- summary: "Elexon's forecast of GB wind generation, issued up to eight times a day; gridflow keeps every issue."
- grain: "One row per target time and issue time".
- what_it_is: "The issues charted give one figure per hour, run to 20:00 UTC on the 22nd".
- raw_feed.note: "one row per target time and issue".
- The `timestamp_utc` field: "Target time the forecast is for, from the vendor `startTime`, UTC".

Put the Overview citation after "reissued up to 8 times a day", not after "hourly". The caption, `x_label` and
`record.caption` say "target hour" about the data they show, which is fine.

### 2. major: `page.chart_view.alt` and `page.notebook.plot_alt`

**What is wrong.** Both alts describe a single fall to "lows" early on the 21st, followed by an end value. They
leave out most of the shape. Every line rises again during the 21st, then falls to its real minimum on the evening
of the 22nd. That minimum is below the "lows" and below the end values, so a screen-reader user is given the wrong
shape and the wrong minimum. The rubric (section 2) requires the alt to match the series minimum. Every number
quoted is a real series value, so this is major, not a blocker.

**Evidence.** Committed `series/elexon/windfor.json`, rebuilt into a Polars frame:

| | 03:30 | 12:30 | 23:30 |
|---|---|---|---|
| Stated "lows", early on the 21st | 4,769 (04:00) | 4,017 (04:00) | 3,449 (05:00) |
| Recovery peak, 21st | 6,734 (14:00) | 6,249 (20:00) | 5,684 (22:00) |
| Series minimum, 22nd | **2,286 (17:00)** | **1,961 (18:00)** | **1,500 (18:00)** |
| End value, 22nd 20:00 (stated) | 2,815 | 2,287 | 1,603 |

- The recovery peaks come from silver `windfor_20260920.parquet`: `max(latest_forecast_mw)` over targets from
  21 Sep 06:00 to 22 Sep 06:00, by `published_at`.
- For `plot_alt`, the eight issues on the 20th have minima of 1,500 to 2,286 MW at 17:00 to 19:00 UTC on the 22nd,
  against the stated "lows of 3,400 to 4,800 MW early on the 21st". The plot PNG shows the same shape.

**Fix.** Suggested wording for the alt:

> ... All three peak at 20,629 at 01:00 on the 20th and fall to a first trough of 4,769, 4,017 and 3,449 early on
> the 21st. They recover to 6,734, 6,249 and 5,684 later that day, then reach their lows of 2,286, 1,961 and 1,500
> at 17:00 or 18:00 on the 22nd, ending at 2,815, 2,287 and 1,603. From 02:00 to 23:00 on the 21st each later issue
> is lower.

Make the same change in `plot_alt`, using the eight-issue ranges: a trough of 3,400 to 4,800, a recovery to about
5,700 to 6,700, and lows of 1,500 to 2,300 MW on the evening of the 22nd.

### 3. nit: `page.chart_view.caption`

**What is wrong.** "Where lines meet, the later issue repeats hours already begun." It is true where the lines
coincide, but it can be read more broadly than the chart supports:

- The lines also cross at points where the values are not equal: 03:30 and 12:30 between 08:00 and 09:00 on the
  20th and between 03:00 and 04:00 on the 22nd, and 12:30 and 23:30 between 01:00 and 02:00 on the 21st. A reader
  can take "meet" to include those.
- "Hours already begun" does not say *before which issue*. The 23:30 issue does not repeat the 12:30 figures for
  13:00 to 23:00 on the 20th, although those hours had begun before 23:30.

**Evidence.**
- Exact equality in the committed series:
  - all three issues equal only for 20 Sep 00:00 to 03:00;
  - `issue_0330 == issue_2330` over the same hours;
  - `issue_1230 == issue_2330` for 20 Sep 00:00 to 12:00.
- Silver on the 20th shows where the 23:30 figures do come from:
  - 13:00 to 16:00 equal the 16:30 issue (16,845 against 12:30's 16,237 at 13:00);
  - 20:00 to 23:00 differ from every earlier issue (8,455 against 19:30's 8,337 at 20:00).

**Fix.** Suggested wording: "Lines coincide only on hours that had begun before the earlier issue: to 03:00 on the
20th for all three, to 12:00 for the later two."

## The writer's two flagged items

1. **Caption and alt comparing the three issues.** I re-derived the claims from the committed series and from
   silver:
   - the peak of 20,629 at 01:00 on the 20th is shared by all three;
   - strict ordering 03:30 > 12:30 > 23:30 holds for every hour from 02:00 to 23:00 on the 21st, and fails at 00:00
     and 01:00, so the alt's scoped claim is true;
   - the key note (4,106 against 6,338 at 12:00 on the 21st) is correct;
   - the end values are correct.

   The problems are the omitted real minimum (finding 2) and the caption's loose wording (finding 3).

2. **Silver has no `settlement_date`, `settlement_period` or `initial_forecast_mw` and is keyed on
   `(timestamp_utc, published_at)`. The writer is right.**
   - All 1,850 silver files share one schema: `timestamp_utc`, `latest_forecast_mw`, `published_at`, `data_provider`,
     `ingested_at`, then the four lineage columns.
   - The transformer writes only the columns it has (`wind_forecast.py:175-186`). `/datasets/WINDFOR` rows carry
     only `dataset`, `publishTime`, `startTime` and `generation` (OpenAPI `DatasetRows.WindGenerationForecast`; the
     bronze file for 20 Sep has the same keys). So `has_sp` is false, and the dedup is
     `["timestamp_utc", "published_at"]` (`:160-165`).
   - `resolve_entity_key` (`:43-58`) returns the same key when the settlement columns are absent. No
     `(timestamp_utc, published_at)` pair is duplicated across September.
   - The pydantic `ElexonWindForecast` does not contradict silver: it declares the three fields optional
     (`schemas/elexon.py:249-252`), and silver just never fills them.
   - DATA-MATRIX's `vs =` compares the vault table with pydantic, not with the silver files, so it could not see the
     gap. The body edit is correct and cites the right lines.

## Checked and passing

- **Request URL.** `raw_feed.requests` matches `request_url` and `request_params` in bronze
  `2026/09/20/*.meta.json` exactly. The code path is `endpoints.py:152-156` (PUBLISH_DATETIME), with 24-hour chunks
  and `page`.
- **Commands.**
  - Ingest end is exclusive: `client.py` loops `while current < end`, and `resolve_dates` treats a bare date as
    midnight UTC.
  - One-day bronze: `data_date = start.date()` at `client.py:314`.
  - Transform end is inclusive: `runner.py:1126`.
  - There is no `PARTITION_SOURCE_OFFSETS`. `read_bronze` reads only day D.
- **Vendor quotes.** "Up to 8 times a day at 03:30 ... 23:30" and "wind farms which are visible to the ESO and have
  operational metering" appear verbatim in the OpenAPI descriptions. Silver on the 20th has exactly those eight
  publish times, each with 73 targets from 19 Sep 20:00 to 22 Sep 20:00.
- **Chart provenance.**
  - `spec_origin: vault`; the build's digest check passes.
  - There is no staged spec and no authored override.
  - Provenance: 219 rows matched (3 × 73) and 207 used (3 × 69). The window is 20 Sep 00:00 to 22 Sep 20:00.
  - Paints are clay, petrol and horizon for lines. No khaki, and no sums.
- **Record.** Eight real rows (`gridflow-sample`), for target 21 Sep 12:00, one per issue on the 20th, from 6,338
  down to 4,106 as captioned. Key columns come first in the guide. There are no lines for the pipeline columns.
- **Notebook.**
  - The lead matches `_date_range_predicate`: TIMESTAMPTZ, half-open with the end day included. The manifest's date
    column is `timestamp_utc`.
  - Written by `scripts/run_notebooks.py`, read-only, with no errors in the outputs.
  - `published_at.dt.day == 20` selects only issues from the 20th.
  - `needs` matches the commands' window.
- **Related.** FUELINST is five-minute, per its note. All four notes are 12 words or fewer, and the build resolves
  them.
- **Local-data grep.** The page block and rendered text contain no "locally", "held", "since 20", local counts, em
  dashes, middle dots or arrows. The only hits are "hour" matching "our " and the template's help card.
- **Build and detector.** `gridflow-build --only elexon/windfor` passes, and `detect.mjs --json` returns `[]`.
  The mirror is byte-identical to the vault note.
- **Screenshots**, from headless Chrome over CDP, with a true 390 by device-metrics override. Shots are in
  `scratchpad/windfor-review-shots/`.
  - Widths: 1440, 1024, 768 and 390, each folded, with the frame unfolded, and with the notebook open. The
    notebook plot is loaded at 1440 and 390.
  - Nothing is clipped or overlapping, including the scenery turbines, corner labels, chart key and note, and the
    wrapped URL and commands at 390.
  - `scrollWidth == innerWidth` at every width and in every state.
  - The site has no dark mode (no `prefers-color-scheme` or `data-theme` in `site/hifi/assets`), so light is the
    only theme.

## Notes for the seat (not findings)

- **Pydantic schema and the static key.** `ElexonWindForecast` and the static `ENTITY_KEY_COLUMNS` still describe
  the settlement-coordinate shape, which this endpoint never produces. `resolve_entity_key` covers it at runtime.
  A schema docs cleanup in gridflow would stop the next reader tripping on it.
- **DATA-MATRIX blind spot.** The `vs` column compares the vault with pydantic, not with the silver files, so it
  misses columns that are declared but never written.
- **`group_map` keys depend on how Polars prints a datetime** (`"2026-09-20 03:30:00.000000+00:00"`). A Polars
  version that prints it differently would break a re-distil, though not CI. Grouping on a formatted time in
  `chart_spec` would remove this.
