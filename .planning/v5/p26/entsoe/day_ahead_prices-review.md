# entsoe/day_ahead_prices: checker review

Checker: Opus 5.5 (high), 2026-09-29. Inputs: vault note diff against quant-vault `origin/master`, the three committed
artefacts, the built page, the writer's report, gridflow `origin/master` code, local silver and bronze (read only).

## Verdict: REVISE

Two majors, both small fixes: one wrong fact the author added to the note body, and one cadence fact stated as a general
rule. The three focus areas (DE-LU, the chart and zone coverage) are sound and reproduced independently.

## Findings

### 1. major: note body, "API endpoint" table, `Rate limit` row

- **What is wrong.** The author changed "codebase configured at 1 req/s" to "6 req/s (`config/sources.yaml:167`,
  `rate_limit_per_second: 6`)". The old text was right.
  - The cited file is `gridflow/.tmp/validation-7day-20260511/config/sources.yaml`, a gitignored validation copy from May.
  - The canonical config says 1.
- **Evidence.**
  - `gridflow/config/sources.yaml:188-192` reads `entsoe:` … `rate_limit_per_second: 1`.
  - `git show origin/master:config/sources.yaml` gives the same line 192.
  - `git check-ignore -v .tmp/validation-7day-20260511/config/sources.yaml` returns `.gitignore:4:.tmp/`.
  - Settings load `config_dir / "sources.yaml"` (`src/gridflow/config/settings.py:259`).
- **Fix.** Restore "configured at 1 req/s" and cite `config/sources.yaml:192`.
- **Related.** The writer's evidence table cites the same stale file for the host (`:164`). The host value is the same in
  the canonical file (`:189`), so the page is unaffected.

### 2. major: `page.facts.cadence`

- **What is wrong.** "Daily, ahead of each delivery day" is stated as a general vendor rule, with no vendor document
  quoted. The writer lists it as unverified.
  - Its only support is the note's "Publication lag ~12:55 CET D-1" line, which has no source, and the bronze timing.
  - This is the case the seat flagged: a cadence given as a rule rather than as what these responses show.
- **Evidence.** The bronze does support a scoped version.
  - The 15 Sep 19:53 UTC fetch for 15 Sep (`bronze/.../2026/09/15/raw_20260915T19532*`) already holds delivery day 16,
    from 15 Sep 22:00 to 16 Sep 22:00 UTC.
  - No ENTSO-E document in the note states the schedule.
- **Fix.** Scope it to the responses, for example "Daily; each reply already held the next delivery day, as sent in these
  responses". Alternatively, drop `cadence` and keep vendor, grain and key.

### 3. nit: `page.what_it_is` (last sentence) and the note body's "No revisions" bullet

- **What is wrong.** "whichever the document lists last" is slightly loose. Each bronze day holds four fetches per zone
  (for example 14 Sep: 15 Sep 19:53, 19:53, 19:54 and 21 Sep 09:59).
  - `read_bronze` concatenates every file in name order (`day_ahead_prices.py:36`) before `unique(keep="last")`
    (`:83`).
  - The kept row is therefore the last-listed series in the latest reply for that day.
- **Evidence.** A re-simulation (every file in name order, UTC-day filter, keep last) matches silver DE-LU on 96 of 96
  quarter-hours for 14, 15 and 16 Sep. On all three days the winning rows come from the 21 Sep 09:59 file.
- **Fix.** "whichever the latest reply lists last".

### 4. nit: `page.record.fields.price_eur_mwh`

- **What is wrong.** "points the vendor omits repeat the previous one" is unscoped. The parser forward-fills only when
  `curveType` is `A03`: `parsers.py`, the `if curve_type != "A03": ... continue` branch before the forward-fill loop.
- **Evidence.** Every day-ahead series in bronze from 12 to 21 Sep is `A03`, so the claim holds in practice.
- **Fix.** Scope it, for example "(curve type A03, as sent)". This is optional.

## What I checked and found correct

- **DE-LU (focus 1).** Reproduced from the code and the rows.
  - The parser never reads `classificationSequence_AttributeInstanceComponent.position` (`parsers.py:284-388`), and the
    dedup is `(timestamp_utc, area_code)` with keep last.
  - Every DE-LU bronze document from 12 to 21 Sep carries sequences 1 and 2 for each delivery day. Sequence order varies:
    `[2,1,1,2]` on the 14th, `[1,2,2,1]` on the 15th and `[2,1,2,1]` on the 16th.
  - Silver matches sequence 1 or 2 as follows:

    | UTC day | Sequence 1 | Sequence 2 | Both equal |
    |---|---|---|---|
    | 14 Sep | 87 | 8 | 1 |
    | 15 Sep | 8 | 88 | 0 |
    | 16 to 20 Sep | all 96 | 0 | 0 |

  - The largest gap is 322.22 EUR/MWh (704.41 against 382.19) at 14 Sep 18:00 UTC.
  - The page states the problem plainly in `what_it_is` and the chart caption, and shows no local number such as 322 or
    the match counts.
  - DE-LU is absent from:
    - the chart: the filter is `area_code ne 10Y1001A1001A82H` and the series has four keys;
    - the eight rows: the same filter;
    - the notebook outputs: `.head()` shows IE-SEM only and the plot is FR and IE-SEM;
    - the alt text and key notes;
    - the HTML: `10Y1001A1001A82H` appears 0 times.
- **Duplicates in other zones.** FR, BE and IE-SEM duplicate series are identical: 2,976, 2,976 and 480 duplicated
  periods, none with differing prices. NL sends one series. No zone's price changes between fetches.
- **Chart (focus 2).**
  - Recomputed from silver: FR, NL and BE hourly means of exactly 4 quarter-hours per hour, and IE-SEM with 1 value per
    hour, as sent. Maximum difference from the committed series is 0.0005 (rounding). There are 168 points per series
    and no nulls.
  - Provenance: `spec_origin: vault`, `rows_used` 2,184, and no staged spec or override.
  - The caption says "the quarter-hour prices of FR, NL and BE averaged to each hour; IE-SEM as sent, hourly". That is
    the hourly mean in words, and the key note repeats "means of four quarter-hours". Not a finding.
  - Currency and unit: bronze `currency_Unit.name` is EUR and `price_Measure_Unit.name` is MWH on every series, and
    silver `currency` is EUR for every row of every zone. The spec also filters `currency eq EUR`.
  - Every alt-text figure matches the series:
    - 14th peaks: FR 305.82, NL 400.0, BE 441.735;
    - lowest: NL -3.053 at 20 Sep 11:00;
    - IE-SEM: 1.095 at 19 Sep 04:00 to 359.165 at 20 Sep 08:00, and 146.8 to 359.2 on the 20th;
    - negative hours for FR, NL and BE on 19 and 20 Sep, between 08:00 and 14:00 UTC.
  - x label: every zone's periods open at 22:00 UTC in bronze, IE-SEM included.
- **Zone coverage (focus 3).**
  - Silver holds 5 zones: IE-SEM PT60M, and DE-LU, FR, NL and BE PT15M, across August and September. There are no GB
    rows.
  - All 45 GB bronze replies are `Acknowledgement_MarketDocument` with reason 999 ("No matching data found ...
    ENERGY_PRICES [12.1.D]") and HTTP 200.
  - The page states the 15/60-minute split for 14 to 20 Sep only. It shows averaging only in the chart and keeps
    `resolution` in the guide.
- **Seat note on "position times resolution".** Not repeated. The guide says "from the vendor period start and point
  position", and the body keeps `start + (position-1)*resolution`, matching `parsers.py:530`.
- **Raw feed and commands.**
  - The request matches bronze `request_url`: parameter order `documentType, periodStart, periodEnd, in_Domain,
    out_Domain, securityToken`.
  - Ingest `--end` is exclusive (`utils/time.py` `day_subwindows`).
  - Transform `--end` is inclusive (`pipeline/runner.py:1126,1138`). `PARTITION_SOURCE_OFFSETS` is `(0,)`, so no
    widening is needed.
  - `EVENT_WINDOW_FILTER` keeps rows inside the requested day.
- **Notebook.**
  - The lead matches `source.py` `query()`: `SELECT * EXCLUDE(...) ... ORDER BY timestamp_utc`, inclusive ends.
  - `.head()` shows `+01:00` stamps.
  - Every cell is read-only, and there are no errors.
  - `plot_alt` matches the PNG: FR about -1.3 to 333, IE-SEM 1 to 359.
- **Eight rows.** Real (`gridflow-sample`), and they match the caption.
- **Guide.** Key columns come first. The `published_at` line follows ruling #39.
- **Gates.**
  - Mirror: `cmp` is clean.
  - `gridflow-build --only entsoe/day_ahead_prices` succeeds.
  - `detect.mjs` returns only the accepted em-dash advisory (EIC padding).
- **Text.** No local-data words, provenance dates, dashes, arrows, middle dots, "live" framing or planning labels.
- **Related links.** Each note is 12 words or fewer. The zones match `DEFAULT_ZONES` and `_FLOW_PAIRS`.
- **Layout.** Looked at 1440, 1024, 768 and 390 (390 through the Browser pane), with the frame folded and unfolded and
  the notebook open.
  - Nothing is clipped or overlapping. The frame and notebook output scroll inside their regions at 390, and the page's
    scroll width is 390.
  - There is no dark scheme in any stylesheet; a forced-dark capture at 1440 differs only in a small hero area.

## Template observations (not findings for this page)

- At 390 the chart's unit label "EUR/MWh" starts 0.9 px from the viewport edge, outside the 16 px gutter. It is fully
  visible, and its placement comes from the chart template.
- The notebook header clip at 390 is covered by ruling #39.
