# elexon/temp: review 1

Checker: Opus 5.5, 2026-09-28. Page `site/hifi/data-sources/elexon/temp.html` in the `p26-elexon` worktree; note
`30-vendors/elexon/datasets/temp.md` in `vault-p26-elexon` (the mirror matches it byte for byte, `cmp` clean).

**Verdict: REVISE** (2 major, 3 nit, 0 blocker)

## Findings

### 1. major: the °C unit comes from a gridflow doc that is wrong about TEMP, when Elexon documents it

- **Fields:**
  - `page.what_it_is` ("gridflow's docs give °C");
  - `page.chart_view.caption` ("°C as gridflow's docs give it");
  - `page.record.fields.temperature` ("°C per gridflow's docs");
  - `page.chart.unit`, `page.notebook.cells[2]` (`ylabel="°C"`) and `page.notebook.plot_alt` ("17.7 °C"), which state
    it without qualification.
- **What is wrong:** each sentence is literally true, but its only source is gridflow `docs/endpoints/elexon.md:761`.
  That doc's TEMP section (`:748-761`) is wrong on every other point checked:
  - it shows three readings a day at 00:00, 06:00 and 12:00 UTC;
  - it lists `normal_temperature`, `low_temperature` and `high_temperature` as silver key columns, and calls low and
    high "forecast bounds";
  - its sample reads 5.2 °C on 15 June.

  The bronze response carries none of this (see below), and the writer's own body edits correct the same claims. The
  page names a discredited source as its authority, and the axis, notebook `ylabel` and `plot_alt` state °C on that
  basis. This is the pilot's INDOD "MWh" case (a unit resting on a project source).
- **Ruling on the writer's question:** the page may state °C plainly, as a vendor fact. Elexon's own TEMP description
  gives the unit. The text as I found it: "daily average GB temperature data (in Celsius). This average data is
  calculated by National Grid ESO from the data retrieved from 6 weather stations around Britain."
- **Limits of my evidence:** I did not read Elexon's page directly. `bmrs.elexon.co.uk/api-documentation/endpoint/datasets/TEMP`
  renders only with JavaScript, and WebFetch returned it empty. The text comes from:
  - the search index's summary of that Elexon page;
  - the Open Net Zero dataset mirror (`https://opennetzero.org/03782949`), which quotes it word for word.
- **Fix:**
  1. Capture the description from Elexon's own page (a browser, not WebFetch). Quote it with its URL in the note body,
     in the Overview or the API table.
  2. State °C as Elexon's, for example "Elexon gives it in °C; the response carries no unit field". Remove "gridflow's
     docs" from `what_it_is`, `caption` and `record.fields.temperature`.
  3. Keep the chart unit, the notebook `ylabel` and the `plot_alt` °C.

  If the vendor text cannot be captured, the fallback is "the unit is undocumented; the feed sends none". In that case
  drop the bare °C from the axis, the `ylabel` and the `plot_alt`.
- **Evidence:**
  - bronze `2026/09/14/raw_20260926T182848Z_f88afebb.json` holds only the keys `dataset`, `measurementDate`,
    `publishTime` and `temperature`;
  - silver has no reference columns (schema printed from `silver/elexon/temp/**/*.parquet`: `timestamp_utc`,
    `measurement_date`, `temperature` plus pipeline columns);
  - no `°C` or `Celsius` for TEMP anywhere in `gridflow/src/gridflow/**/*.py`: the only hits are Open-Meteo's
    `schemas/weather.py:59,108` and `silver/openmeteo/historical.py:45`.

### 2. major: "one reading per measurement date" is a universal with no source in the note

- **Fields:**
  - `page.summary` ("one figure per measurement date");
  - `page.facts.cadence` ("One reading per measurement date");
  - `page.what_it_is` ("one reading per measurement date");
  - `page.chart_view.caption` ("one reading per measurement date from 13 to 21 September").
- **What is wrong:**
  - The claim is a rule about the dataset. As the note stands, its only support is the 14 local silver rows (0
    duplicate measurement dates).
  - The code does not enforce it. The key is the publish time (`temp.py:25`, `temp.py:96`
    `unique(subset=["timestamp_utc"])`), so a measurement date published twice keeps two rows. The writer's body edit
    says the same.
  - The chart spec deduplicates on `measurement_date` with `last`, and the caption's "the latest publication of each"
    already implies there can be more than one.
- **Fix:** the Elexon quote from finding 1 fixes this too. It is a separate claim in separate fields, not a second
  independent problem.
  - "Daily average", once quoted, makes one value per measurement date the vendor's definition. Word the summary,
    cadence and `what_it_is` from it (for example "Elexon's daily average temperature, one value per measurement
    date").
  - For the chart caption, "one point per measurement date" describes the chart, which is true by the dedup.
  - Keep "the latest publication of each".
  - Without the quote, scope the claim to what the page shows ("one per measurement date in these rows").
- **Evidence:** Polars over `C:\gridflow-data\silver\elexon\temp\**\*.parquet`:
  `group_by('measurement_date').len().filter(len > 1)` returns 0 rows of 14. That count is local data, so it is not
  evidence for a universal.

### 3. nit: the "so" in `page.what_it_is` names the wrong cause

- **Field:** `page.what_it_is`, "gridflow keys each row on the publish time, so a reading published the next morning
  ... arrives with the next day."
- **What is wrong:** the reading arrives with the next day for three reasons, none of them the dedup key:
  - the connector fetches by publish window (`client.py` `PUBLISH_DATETIME` loop, `while current < end`, 24-hour
    chunks);
  - bronze partitions by the window's start date (`_fetch_datetime_range`, `data_date = start.date()`);
  - silver reads one bronze date per file (`temp.py:27-35`), and `query()` filters on `timestamp_utc`.
- **Fix:** for example "gridflow fetches and dates each row by its publish time, so ...".

### 4. nit: the hero scenery alt says "generation data" on a temperature page (seat)

- **Field:** landscape (unset, so the default is `power`).
- **What is wrong:** the scenery `aria-label` reads "Drawing of where generation data comes from: onshore wind ...".
  No landscape fits a weather reading. The writer reported this and the brief offers no fitting option, so it is the
  seat's template call, not a writer fix.

### 5. nit: the Open-Meteo `related` notes say what the datasets are, not how they relate

- **Fields:** `page.related[2].note` ("Hourly 2 m temperature at seven UK cities, from reanalysis") and
  `page.related[3].note`.
- **What is wrong:** both are true (`vault/openmeteo/historical_demand.md:12-14`, `forecast_demand.md:12-13`: seven
  population centres including Belfast, ERA5 reanalysis). The rubric asks how the datasets relate. Once finding 1
  lands, a relating note would read, for example, "City-level hourly temperature against this six-station GB daily
  average".

## Checked and correct

**Grain, key and columns**
- Grain and key: `ENTITY_KEY_COLUMNS = ("timestamp_utc",)` at `temp.py:25`, dedup at `:96`.
- `timestamp_utc` is `publishTime` (`temp.py:58-59,80-84`).
- `measurement_date` is cast to a Date (`:93-94`).
- The frame's eight rows are real (`generated_by: gridflow-sample`). The key column is first, and row 1 shows the
  09:06 publication for 13 September.
- The guide has one line per non-pipeline column.

**The 13 September reading**
- The bronze `2026/09/13` window holds `{"data":[]}`.
- The bronze `2026/09/14` window holds `measurementDate 2026-09-13, publishTime 2026-09-14T09:06:00Z, 17.7` and
  the 14th's reading at 15:45.
- The key note, `raw_feed.note`, `record.caption` and `notebook.lead` all state this correctly.

**Raw request and commands**
- `raw_feed.requests`: `endpoints.py:157-160` (PUBLISH_DATETIME), `_to_utc_z` and `build_params` (`page`). The
  bronze sidecar's `request_url` is the same URL with the colons percent-encoded by the HTTP client.
- `raw_feed.commands`: ingest `--end 2026-09-22` is exclusive (the publish-window loop `while current < end`), so it
  fetches windows 14 to 21. Transform `--end 2026-09-21` is inclusive (`runner.py` `date_range`). No
  `PARTITION_SOURCE_OFFSETS`.
- These cover chart measurement dates 13 to 21, frame dates 13 to 20 and the notebook window. `notebook.needs`
  matches.

**Notebook**
- `notebook.lead`: `query()` on `silver_elexon_temp`, TIMESTAMPTZ half-open `[start, end+1)` (gridflow_models
  `_get_method_registry.py`), `source.py:140` bitemporal EXCLUDE.
- The notebook JSON came from `scripts/run_notebooks.py`. Every cell is read-only and no output has an error. The
  `head()` output and the plot match `plot_alt`; I read `temp-5.png`.

**Chart**
- Series `spec_origin: vault`, digest passes, no staged spec or authored override.
- Values `[17.7, 18.6, 18.3, 16.9, 16.6, 16.0, 17.1, 16.6, 16.0]`. `alt` and `plot_alt` match them.
- Dedup (`distil.py:282`) sorts by `timestamp_utc` and keeps the last, so "the latest publication of each" is right.

**Build, detector and wording**
- `gridflow-build --only elexon/temp` succeeds. `detect.mjs --json` returns `[]`.
- Grep of the rendered text finds no "locally", "held", "our", "since 20", row or day counts, "% of", em dashes,
  middle dots, "→", "live", "now" or planning labels.

**Note body edits (7)**
- Each fixes the smallest span and cites `temp.py` lines or the bronze sample. All are correct against the code.

## Rendering (section 5)

**Setup:** headless Chrome through a static server on 9717, full-page captures read segment by segment.
- 1440, 1024 and 768: direct window captures.
- 390: a 390 px iframe.
- Frame unfolded and notebook expanded: a scratch copy of the page with `#fx` `checked` and `#nb-demo` not `hidden`,
  captured at 1440, 768 and 390.

**Results:** nothing clipped or overlapping.
- Hero turbine tops and the offshore wind label are visible.
- The chart, key note, raw-feed blocks, both frame states, the guide, every notebook cell and the plot, the stratum
  corner labels and the related list are all fully visible.
- The unfolded frame and the `head()` table run past the panel edge at 390 and 1440, but both are horizontal scroll
  regions (`dataset.css:14` `.fw`, `theme.css:431` `.df-wrap`), not clipping.

**Dark mode:** there is none. There is no `prefers-color-scheme` in `site/hifi/assets/`, so the light captures are
the only rendering.

## For the seat

- **Y-axis:** the known "y-axis forced to include 0" issue does not show on this build. The chart's axis runs 15 to
  19.
- **Notebook headers:** I checked the expanded `head()` output at 1440 and 768 for the known header-shift issue. The
  three headers sit right-aligned over their own columns, and I could not see a one-column shift on this page. Either
  way it is the seat's template issue, not a finding.
- **gridflow docs:** `docs/endpoints/elexon.md:748-761` (the TEMP section) needs a gridflow docs fix. The writer
  flagged this too.
