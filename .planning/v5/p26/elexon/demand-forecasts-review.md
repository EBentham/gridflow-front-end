# demand-forecasts: checker review

Family page `demand-forecasts` (lead `ndf`; members `ndfd`, `tsdf`, `tsdfd`). Checker, 2026-09-29, against
`review-rubric.md`.

## Verdict: REVISE

One major (an attribution) and three nits. All the facts, chart numbers, notebook numbers, requests and commands check
out against the code and silver. The fix is one clause in `what_it_is`.

## Findings

### 1. major: `page.what_it_is`: the mappings to INDO and ITSDO are stated as fact, with no source named

- **Text:** "`NDF` forecasts GB national demand, the quantity `INDO` reports" and "`TSDF` forecasts transmission system
  demand, the `ITSDO` quantity".
- **What each link rests on:**
  - Elexon gives only the dataset names: "National Demand Forecast (Day-ahead)" and "Transmission System Demand
    Forecast" (`connectors/elexon/endpoints.py:126-129, 210-213`; the `ElexonTSDF` docstring,
    `schemas/elexon.py:400-405`).
  - The equivalences come from NESO, and are quoted only in the sibling note `indo.md` (Modelling notes, #01:244 and
    #01:268): National Demand "is equivalent to" INDO, and Transmission System Demand "is equivalent to" ITSDO.
  - Nothing in `ndf.md` or `tsdf.md` cites a vendor definition.
- **What the author used besides:** a project measurement, a TSDF `N` minus NDF floor of 500 MW, which is not on the page.
- **What I measured** (settlement dates 14 to 20 Sep, last publish per half-hour):
  - NDF against INDO: mean absolute difference 574 MW. NDF against ITSDO: 3,013 MW.
  - TSDF `N` against ITSDO: 1,085 MW (mean +295). TSDF `N` against INDO: 3,616 MW.
- **Ruling:** the mappings are almost certainly right, but they are name matching plus NESO's definitions of the outturn
  series. No source says what NDF or TSDF forecast. This is the pilot's overclaim class: the interconnector sign
  precedent requires the page to say whose statement it is.
- **Inconsistency with the approved sibling:** the `demand-outturn` page attributes the same definitions ("NESO defines
  `INDO` as national demand, and `ITSDO` as ...").
- **Fix:** attribute the link to NESO. For example: "`NDF` forecasts GB national demand, which NESO equates with `INDO`,
  for each half-hour ..." and "`TSDF` forecasts transmission system demand, which NESO equates with `ITSDO`, as boundary
  `N` ...".
- **Related notes are fine:** `related[indo]` and `related[itsdo]` say "to score ... against". That is a use, not an
  identity, and it matches the approved `demand-outturn` related notes.

### 2. nit: `page.notebook.lead`: "The first cell converts times to UTC"

- On the page, the notebook's first cell is `[1]` (`setup_notebook()`), then the `[2]` help card.
- The conversion happens in cell `[3]`, which is `[2]` in the inline preview.
- **Fix:** say "The query cell converts times to UTC".

### 3. nit: `page.what_it_is` and `family.members[tsdf].differs`: "17 transmission boundaries `B1` to `B17`"

- **The count:** it comes from `tsdf.md`'s live check (2026-07-31), and local silver has the same 18 values. But the same
  note's schema row calls the list "Vendor-managed value list, no fixed enumeration".
- **The meaning:** nothing documents what the `B*` values are. The author's own report says they sum to about 2.4 times
  `N`, and that "The page says only 'boundaries'". The page actually says "transmission boundaries".
- **Fix:** scope the count, for example "boundaries `B1` to `B17` (in the note's live check)", or drop the count.

### 4. nit: `page.facts.grain`: only two of the four members

- "NDF: one row per half-hour per publish; NDFD one per date per publish" leaves out TSDF and TSDFD. The
  `demand-outturn` grain covers every member.
- TSDF: one row per half-hour per boundary per UTC publish day (`tsdf.py:112-115`, deduplicated within each daily
  transform). TSDFD: one per forecast date per publish day (`tsdfd.py:99`).
- **Fix:** add them if the budget allows. Otherwise leave it; each member's `differs` line already carries its grain.

### Note on the vault body (not a finding)

- **Where:** `ndfd.md` and `tsdfd.md` now say "which daily statistic is undocumented".
- **The problem:** that is a claim about vendor documentation that nobody fetched. The page's own wording, "the fields
  do not say which daily statistic", is the evidenced form.
- **Suggestion:** use that wording in the note bodies too. This is optional: it is not on the page.

## The three items the seat asked about

1. **The mappings to INDO and ITSDO** (`what_it_is`): they must be attributed. See finding 1.
2. **The 07:45 UTC publish: passes.** The page states only what the chart shows:
   - the key note "Starts at 04:00 UTC: this publish holds no earlier half-hours of the day";
   - the alt text "The 07:45 line starts at 04:00 UTC, at 18,180 MW".
   Both are scoped to the one drawn publish. Silver confirms it: the `2026-09-16 07:45` publish covers `2026-09-17
   04:00` to `2026-09-18 03:30` UTC (48 rows). The page never states the "04:00 to 04:00 every day" pattern.
3. **The notebook scoring against INDO over 14 to 20 Sep: passes.** I recomputed it in Polars from silver:
   - 326 matched half-hours, from `2026-09-14 04:00` to `2026-09-20 22:30` UTC;
   - no duplicate 07:45 timestamps;
   - mean absolute error 875.3 (07:45) and 574.3 (last), matching the output of cell 5;
   - 07:45 publish: highest +3,603 MW at `2026-09-15 15:00` UTC, lowest -1,360 MW at `2026-09-19 16:00` UTC;
   - last publish: from -1,015 to +2,943 MW.
   All of these match `plot_alt`, and the PNG shows the same shape. The last publish comes 9 to 44 minutes before the
   half-hour starts (median 13).
   - `needs` ("published 13 to 20 September") matches the ingest window: `--start 2026-09-13 --end 2026-09-21`,
     exclusive (`client.py:95-99`, `while current < end`).
   - `query()` filters on `settlement_date`, both ends included, and drops the lineage columns
     (gridflow_models `research/handles/source.py:401-451`).

## Checks that passed

- **Grain and key:** `demand_forecast.py:150-153` deduplicates on `(settlement_date, settlement_period, forecast_type,
  published_at)`. Silver has 0 duplicates on that key. In every NDF and TSDF file, the `published_at` date equals the
  file date.
- **`forecast_type`:** `demand_forecast.py:147-148`.
- **NDFD:** `settlement_period` is fixed at 1 (`:86-91`).
- **TSDF:**
  - dedup key without `published_at` (`tsdf.py:112-115`); 0 duplicates within a file, which gives one vintage per
    publish day;
  - 18 boundary values: `N` and `B1` to `B17`.
- **TSDFD:** `timestamp_utc` is midnight UTC on the forecast date (`tsdfd.py:79-82`).
- **`ingested_at`:** stamped at transform time, which the body fixes correctly state.
- **Requests:** host, path, `publishDateTimeFrom`/`To` in `%Y-%m-%dT%H:%M:%SZ` form, and `page=1` for all four
  (`endpoints.py:126-134, 210-219, 267-313`).
- **Chart:**
  - Series `spec_origin: vault`; the build's digest check passes. There is no staged spec and no authored override.
  - Numbers in the alt text and key note, read back from the series: morning 38 points from 04:00 at 18,180; a gap of
    460 MW at most until 07:00; positive from 07:30, with the largest gap 2,712 MW at 15:00; peaks 29,970 at 18:30 and
    29,000 at 18:00; lowest point 18,000 at 03:00.
  - Filter on the two publishes plus `settlement_date`: `aggregation: last` has nothing to combine, so the chart shows
    one value per half-hour as the caption says.
  - Paints are petrol and clay (line paints).
- **Eight rows:** `generated_by: gridflow-sample`; eight real publishes of period 36, falling from 28,734 to 26,554 MW.
  The guide has one line per non-pipeline column, key columns first.
- **Notebook:** written by `scripts/run_notebooks.py`, read-only cells, no errors.
- **Build and detector:** `gridflow-build --only elexon/ndf` succeeds; `detect.mjs --json` returns `[]`.
- **Mirrors:** all four mirror copies are byte-identical to the vault notes.
- **No local-data statements or leakage:** grepped the rendered text. There is no local-data wording, no planning
  labels, no em dashes, no "→", and no "live", "now" or "real-time". Every `related` note is 12 words or fewer.
- **Vault body edits:** smallest spans, each with `file:line`. The sample corrections check out:
  - NDF and TSDF period 9 on 6 May is 03:00 UTC;
  - NDFD `2026-04-02T23:00` and `published_at` come from the note's own bronze sample.
- **Screenshots:** headless Chrome at 1440, 1024 and 768, and 390 through a `file://` wrapper page holding a 390 px
  iframe. A `data:` URL iframe renders blank, and the browser pane's screenshots time out.
  - Nothing is clipped or overlapping in the hero, the chart, the key, the raw feed, the frame and guide, the inline
    notebook or the related section.
  - The unfolded frame (the `#fx` toggle) was checked at 1440 and 390. It scrolls sideways inside its box, as on other
    pages.
  - The site has no dark theme (no `prefers-color-scheme` or `data-theme` rule in `site/hifi/assets/`), so light is the
    only mode.
  - I could not open the notebook drawer in headless Chrome. The author's report says it was checked at 1440 and 390.
- **Not a finding (known template limit):** at 768 and 390 the frame folds the demand and `published_at` columns.
