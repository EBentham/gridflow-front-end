# openmeteo/demand-weather: writer response to review 1

Writer: Opus 5.5 · high, 2026-10-06. Responds to `demand-weather-review.md` (REVISE: 0 blockers, 2 majors, 6 nits) and the seat ruling.

## Status

- **Build:** `gridflow-build --only openmeteo/historical_demand` wrote `demand-weather.html` with no errors for this page.
- **Budgets:** `anatomy_errors` returns `[]`.
- **Detector:** `node C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow-front-end/.claude/skills/impeccable/scripts/detect.mjs --json` returns `[]`. The page has 0 em dashes.
- **Mirrors:** both canonical notes were copied with `cp` and checked with `cmp`; both are byte-equal and still CRLF.
- **Notebook:** rerun by `scripts/run_notebooks.py` after the plot cell changed. 5 cells, no errors; the plot cell now outputs only the image.
- **Series and sample:** unchanged. The chart spec and `record.select` were not touched, and the build's digest check passes.
- **Screenshots:** at 390 and 1440, offsets 0 and 1800, files `scratchpad/shots-dw/r2-*.png`.
  - Checked: hero, what it is, how it's used, chart caption, raw feed and both member blocks, frame caption and guide.
  - Nothing is clipped or overlapping.
  - The server on port 9861 was stopped. Port 9670 was not touched.

## Which stamp is the fetch time (checked before quoting the share)

| Stamp | What the code says it is |
|---|---|
| Bronze sidecar `fetched_at` | Set when the `RawResponse` is built, right after the HTTP call (`connectors/openmeteo/client.py:128`) |
| Bronze sidecar `written_at` | Set when the bronze body is durably written (`bronze/writer.py:57-79`). This is the fetch-time stamp I used. |
| Silver `ingested_at` | `datetime.now(UTC)` inside `transform()`, i.e. the silver build time (`silver/openmeteo/historical.py:260`) |
| Silver `available_at` | `datetime.now(UTC)` on a normal (non-re-ingest) run, also the silver build time (`silver/base.py:1181`); `VINTAGE_POLICY = None` (`forecast.py:37`) |

- **Method.** For every one of the 6,048 `forecast_demand` silver rows, I reproduced the transform's partition pick:
  - the day's own window-start partition if it has files, else the nearest earlier one;
  - within that partition, the last file by name.
- **I then compared the file's sidecar `written_at` with the row's `timestamp_utc`:**
  - **847 rows (14.0%) were fetched before their hour,** at most 120.1 hours (five days) ahead. All of them come from the fetch made at 22:52 UTC on 4 Sep (window 21 Aug to 9 Sep).
  - **5,201 rows were fetched after their hour,** by up to 373.5 hours.

  | Window | Fetched (`written_at`, UTC) | Rows | Hours after target, min to max |
  |---|---|---|---|
  | 1 to 6 Aug | 16 Aug 13:28 | 840 | 254 to 373 |
  | 20 Aug to 6 Sep | 3 Sep 20:06 | 168 | 333 to 356 |
  | 21 Aug to 9 Sep | 4 Sep 22:52 | 3,360 | -120 to 359 (847 ahead) |
  | 13 to 22 Sep | 26 Sep 17:44 | 1,680 | 91 to 330 |
- **The seat's count holds.** It used `ingested_at` and found about 14% before the hour and up to about 373 hours after. That gives the same result here only because ingest and transform ran in the same pipeline run: `ingested_at` minus `written_at` is 0 to 1 second on every row. By code, `ingested_at` is the build time. A transform run on another day would move it, but not the bronze stamp. The page states the share without naming a stamp, and it is the bronze fetch time.

## Findings and what I changed

1. **[major] `family.members[1].differs`: done.**
   - Now: "Forecast host, own grid cells; silver keeps one value per hour, no run time" (14 words).
   - `raw_feed.note` now says which layer does what: "Bronze keeps every fetch, filed under its window's start date; silver keeps one value per hour and city." (30 words in total)
2. **[major] `how_used[2]`: done.**
   - The forward-use bullet is gone. It now reads: "The `forecast_demand` request as a template for capturing real forecasts."
   - Per the seat ruling, the fetch timing is stated in domain terms in `what_it_is` (60 words): "`forecast_demand` the forecast host, and silver keeps no fetch time for it. Of those rows, about one in seven were fetched before the hour, up to five days ahead; the rest up to 373 hours after."
   - `summary` no longer says "as forecasts". It now says "from Open-Meteo's archive and forecast hosts".
   - No day-ahead or forward wording is left on the page. I grepped for `day-ahead`, `forward`, `overwrit` and `fetched ahead`.
3. **[nit] `record.caption`: done.** It now reads "From `historical_demand`: Birmingham, 16:00 to 23:00 UTC on 8 January 2026, the hours snowfall began." (15 words)
4. **[nit] `notebook.plot_alt`: done.** The range now reads "between -6 and 7 °C", which agrees with the -5.8 °C low.
5. **[nit] Notebook legend: done.**
   - The legend is now below the axes in four columns with no frame: `ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.3), frameon=False);`.
   - The x-axis label is now `UTC`.
   - The trailing `;` suppresses the Legend repr.
   - I checked the PNG: the legend clears every line.
6. **[nit] `chart_view.alt`: done.** It now reads "London starts near 16.4 °C and Glasgow near 14.5 °C; both fall to their lows…" (85 words)
7. **[nit, advisory] ERA5-only statements in the canonical `historical_demand.md` body: done,** each as a one-clause scoping.
   - H1: "(archive, population centres)".
   - `models` row: "Model override (default Best Match blends IFS HRES, ERA5, ERA5-Land) — not used". I kept the body's existing dash.
   - Point-in-time line: "Values from the ERA5 part are stable once published; whether recent hours from the IFS part are later replaced is unverified."
   - "ERA5 grid-cell snapping" is now "Grid-cell snapping".
8. **[nit] Forecast example window: done.** The family `request` for `forecast_demand` now uses `start_date=2026-10-06&end_date=2026-10-12`. That window starts today, so the example shows the member returning forecast hours.

**One more body correction (`forecast_demand.md`, Point-in-time line).** It now says that `available_at` and `ingested_at` are the silver build clock (`base.py:1181`, `historical.py:260`), and that the fetch time lives only in the bronze sidecar (`writer.py:57-79`). This confirms the reviewer's added defect.

## Template issues from round 1

Both are now fixed in the seat's template; I saw this in the round-2 shots:
- The family member headings no longer show the upper-case code.
- The `hourly=` value now wraps at a comma, not mid-word.

The hub `openmeteo.json` wording ("GB", "ERA5") is unchanged; it is the seat's file.

## Defects

Additions and updates to round 1 (pasteable):

- **open_meteo `forecast_*`: no column holds the fetch time.**
  - Silver `available_at` and `ingested_at` are both the silver build clock (`silver/base.py:1181`, `silver/openmeteo/historical.py:260`; `VINTAGE_POLICY = None`). The fetch time exists only in bronze sidecars.
  - A transform run apart from its ingest would stamp every row with the later build time.
  - Any lead-time or point-in-time use of these tables built from `available_at` is wrong.
  - Fix direction: carry the bronze `written_at` per file, via `VINTAGE_PER_BRONZE_FILE`, or add an explicit fetch or run column.
- **open_meteo `forecast_demand`: the stored rows are mostly not forecasts.**
  - Measured against the bronze `written_at`, 847 of 6,048 rows (14.0%) were fetched before their hour (at most 120 h ahead, all from the 4 Sep fetch). The rest were fetched 91 to 373 h after.
  - Cause: `client.py:109-116` sends the `--start`/`--end` window unchanged, and the ingests behind this table used windows that began 13 to 15 days before the fetch.
  - This is the round-1 leakage defect, now quantified. The same check probably applies to `forecast_wind` and `forecast_solar`.
- Round-1 items stand unchanged: silver collapse depends on partition layout; `snowfall_cm` vault text; "GB" and "ERA5" in the hub; the historical 5-day vintage-policy assumption.

## Summary

Both majors and all six nits are fixed. The forecast member now states its real fetch timing (one in seven rows fetched before the hour, the rest up to 373 hours after), measured on the bronze fetch stamp. The build is clean and the detector returns `[]`.

## Nits fixed (review 2, APPROVE with 3 nits)

1. **Scope and reason in `what_it_is`.**
   - Now (60 words, at budget): "`historical_demand` reads the archive; `forecast_demand` the forecast host, with dates sent unchanged. Its fetches asked for windows mostly past, so about one in seven silver rows was fetched before its hour (up to five days ahead), the rest up to about 374 hours after."
   - The scope is `forecast_demand` rows in silver.
   - The reason rests on code (`client.py:109-116` sends `start_date`/`end_date` unchanged) and on the four bronze sidecars: each window began 13 to 15 days before its fetch. It makes no guess about intent.
   - To fit the budget, the first sentence lost the redundant "Open-Meteo" and now reads "Nine weather variables at seven cities, London to Belfast, plus derived heating, cooling and air-density columns."
2. **The forecast bullet as a use of the data.** `how_used[2]` now reads "The forecast member's request and columns, a template for capturing real forecasts." That is word for word the approved solar-weather bullet.
3. **"373 hours" is now "about 374 hours"** (373.5 h). No "373" remains in either note or on the built page.

Checks after the edits:
- Both canonical notes copied with `cp` and checked with `cmp`: byte-equal.
- `gridflow-build --only openmeteo/historical_demand` wrote the page with no errors.
- `detect.mjs --json` (absolute path) returns `[]`.
- The page has 0 em dashes.
- The series, sample and notebook are unchanged; the build's digest check passes.

One-line summary: all three review-2 nits are fixed; the fetch-timing sentence is scoped to `forecast_demand` silver rows and explains why most were late, the forecast use matches solar-weather, and 373 is now "about 374"; build clean, detector `[]`.
