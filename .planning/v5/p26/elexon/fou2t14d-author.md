# elexon/fou2t14d: writer report

Writer: Opus 5.5, 2026-09-29. Screenshot port 9743 (my own static server, stopped).

## Status

- `gridflow-build --only elexon/fou2t14d`: green. `detect.mjs --json`: `[]`.
- Canonical note edited in the vault worktree (`30-vendors/elexon/datasets/fou2t14d.md`): 300 lines, all CRLF.
  Mirror `vault/elexon/fou2t14d.md` copied byte for byte (`cmp` clean). The old mirror was stale (LF, the
  2026-05-08 version); it has been replaced.
- Artefacts, all from real data:
  - `site/hifi/data/series/elexon/fou2t14d.json` (`gridflow-distil`, `spec_origin: vault`, 3 series by 72
    points, 216 rows used);
  - `site/hifi/data/samples/elexon/fou2t14d.json` (`gridflow-sample`, 8 rows);
  - `site/hifi/data/notebooks/elexon/fou2t14d.json` and `fou2t14d-5.png` (`scripts/run_notebooks.py`, 5 cells,
    no errors).
- No staged spec or authored override existed for this dataset, so there was nothing to delete.
- `uou2t14d` files were not touched.

## What the page shows

- **Chart:** a line chart with x = `published_at`. It shows the forecast for **delivery date 24 September 2026**
  as each hourly publish from 00:00 UTC on 19 September to 23:00 UTC on the 21st gave it (72 publishes).
  - Series: CCGT (gas), WIND, NUCLEAR.
  - Aggregation is `last`, so there is one value per key and nothing is summed across publishes or fuels.
  - The caption says "Forecasts, not outturn".
- **Frame:** eight consecutive hourly publishes (08:00 to 15:00 UTC on 20 September) of WIND for 24 September.
  The value moves 10,608 → 10,524 → 12,442 → 12,402 → 12,504.
  - `select.columns` is `[output_usable_mw, published_at, settlement_date, fuel_type]`. At 390 only one of the
    two wide columns fits; the value was kept.
- **Notebook:** `query("fou2t14d", "2026-09-24", "2026-10-06")` reads `silver_elexon_fou2t14d_latest`.
  - Cell 3 prints `published_at.unique()`, and the output shows that every row comes from the single
    00:00 UTC publish of 22 September.
  - The plot shows CCGT, WIND and NUCLEAR across the 13 delivery dates of that one publish.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Definition: "forward view of availability (also referred to as Output Usable data under the Grid Code) for generation and interconnector capacity, accounting for planned outages covering 2 days ahead to 14 days ahead; it is aggregated by Fuel Types categories" (`summary`, `what_it_is`) | Elexon OpenAPI (Insights.Api), `/datasets/FOU2T14D` description. Local copy `scratchpad/swagger.json`, captured 2026-09-27 (the same file the windfor checker used). Quoted in the note body Overview. The same text is mirrored at opennetzero.org/03782949 |
| Daily grain, one figure per delivery date, not per half-hour; no unit sent (`what_it_is`, `facts.grain`, `record.fields.output_usable_mw`) | OpenAPI row schema `Insights.Api.Models.Responses.Generation.DatasetRows.AvailabilityByFuelTypeDaily`: `forecastDate` (date), `outputUsable` (int64, no unit), no period field. Bronze rows have the same key set |
| "MW" is gridflow's column name, not a vendor unit (`what_it_is`, fields) | Column `output_usable_mw` (`silver/elexon/fou2t14d.py:99`). The vault note's "MW." cites no vendor. Same treatment as the approved windfor page |
| Delivery date is a London date (`what_it_is`, `record.fields.settlement_date`) | Bronze rows carry `forecastDateTimezone: "Europe/London"` (bronze sample in the note; local bronze 2026/09/20 and 21). `forecastDate` is renamed to `settlement_date` at `fou2t14d.py:95` |
| 2 to 14 days ahead (`summary`, `what_it_is`, related note on NDFD) | OpenAPI FOU2T14D description. For NDFD: OpenAPI `/datasets/NDFD` says "values for the 2 to 14 days ahead". Silver agrees: each publish's delivery dates run London D+2 to D+14 (all 337 publishes) |
| Key and grain `(settlement_date, fuel_type, published_at)`; gridflow keeps every publish (`facts.grain`, `record.key`, `summary`, `what_it_is`) | `ENTITY_KEY_COLUMNS` (`fou2t14d.py:59`); dedup key including `published_at` (`fou2t14d.py:175-179`); `APPEND_ONLY = True` (line 53). No duplicate keys in silver |
| `timestamp_utc` is midnight UTC of the delivery date, set by gridflow (`record.fields.timestamp_utc`) | `fou2t14d.py:132-139` (the no-`settlement_period` branch). Silver: `timestamp_utc == settlement_date at 00:00 UTC` on every row. This is **not** the London day start (23:00 UTC the day before in BST) |
| `INT*` codes are interconnectors; silver drops their zone and name (`record.fields.fuel_type`) | Bronze, all 14 files: every `INT*` row has `interconnector: true` and every other row `false` (45,370 against 40,833). `INT*` rows carry `biddingZone` and `interconnectorName` (for example INTELEC → FRANCE, "Eleclink (INTELEC)"). `output_cols` (`fou2t14d.py:189-198`) does not include those fields |
| `published_at` is the vendor `publishTime`, UTC (`record.fields.published_at`) | `fou2t14d.py:96-97`, 143-148 |
| Request URL (`raw_feed.requests`) | `ParamStyle.PUBLISH_DATETIME`, 24-hour chunks (`endpoints.py:141-145`, `client.py:93-99`); `_to_utc_z` format `%Y-%m-%dT%H:%M:%SZ` (`endpoints.py:267-277`); `page` always sent (`endpoints.py:312-313`). Bronze meta for 2026/09/21: `publishDateTimeFrom=2026-09-21T00:00:00Z&publishDateTimeTo=2026-09-22T00:00:00Z&page=1` |
| Publish windows include both ends; "the end instant is included" (`raw_feed.note`, ingest comment) | `IntervalSemantics.CLOSED` for Elexon `publishDateTimeFrom/To` (`silver/partition_window.py:104-111`); `_PUBLICATION_WINDOW_FILTER_SOURCES` (`silver/base.py:324-328`). 13 of the 14 bronze days hold 25 publishes, 00:00 of that day to 00:00 of the next (18 September lacks its 10:00 publish) |
| Commands: ingest 19 to 22 September, transform 19 to 21 September | Ingest `--end 2026-09-22` requests up to and including the 22 Sep 00:00 publish, which the notebook reads. Transform `--end` is inclusive. There are no `PARTITION_SOURCE_OFFSETS`. Bronze partition = the publish-window start date (`client.py:315`, `data_date = start.date()`) |
| Chart values in `alt` and the nuclear key note | Committed series `series/elexon/fou2t14d.json`, read point by point: gas 21,011 → 21,099 → 21,039, then 20,324 at 20 Sep 21:00, 20,271/20,324, then 19,961, 19,561, 19,161 (21 Sep 14:00 to 16:00). Wind: min 10,524 (20 Sep 09:00), max 12,504 (20 Sep 15:00), 12,442 at 20 Sep 10:00, last 11,606. Nuclear: 3,570 until 4,210 at 20 Sep 21:00. No nulls, 72 x values |
| "each hourly publish, 00:00 UTC on 19 September to 23:00 on the 21st" (caption) | Series x: 72 consecutive hours, none missing (the chart window is fixed on `published_at`, 19 to 21 inclusive) |
| Cadence: "Not stated in Elexon's API docs; the charted publishes are an hour apart" (`facts.cadence`) | Neither the OpenAPI FOU2T14D description and parameters nor the rendered Elexon docs page (bmrs.elexon.co.uk/api-documentation/endpoint/datasets/FOU2T14D, dumped with headless Chrome 2026-09-29, `scratchpad/fou-shots/elexon-fou2t14d-doc.html`) states a schedule or a unit; the page repeats the OpenAPI description word for word. The chart's x values are an hour apart. Scoped to the chart on purpose (see windfor review finding 1) |
| Notebook lead: relation, filter, ends, lineage | gridflow_models manifest resolves `fou2t14d` → `silver_elexon_fou2t14d_latest` with date column `settlement_date` (DATE), checked in the models venv. `query()` builds the inclusive predicate and the EXCLUDE clause (`research/handles/source.py:401-448`). `BITEMPORAL_EXCLUDE` = event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year. The latest view keys on `(settlement_date, fuel_type)` and orders by `available_at` (`latest_views.py:104-107`); `available_at == published_at` on every silver row |
| `plot_alt` values | Silver, publish 2026-09-22 00:00 UTC, pivoted: CCGT 19,214 … 24,826 (1 Oct), 23,872 (2 Oct), 24,910 (6 Oct); WIND min 5,824 (25 Sep), max 15,891 (29 Sep); NUCLEAR 4,210 → 5,158, never falling. Matches the PNG |
| Frame rows | `gridflow-sample` output: 8 real rows, published 20 Sep 08:00 to 15:00 UTC, as listed above |
| Related pages resolve | The build resolves all four (`elexon.json` page set) |

## Note-body corrections (canonical vault note)

1. **Overview.** "Issued daily, this dataset gives …" was unevidenced and contradicted by the data.
   - Replaced with the OpenAPI quote, plus a note that the row schema carries no period and no unit.
   - Added: the OpenAPI states no schedule; Elexon's 2018 CP1506 report says "Every weekday"; silver
     `publishTime`s fall on every hour, weekends included. That last point is labelled a silver observation.
2. **API table, "Publication lag".** "Daily publication." is now "not stated in the OpenAPI", plus the
   closed-window fact with its citation (`partition_window.py:104-111`; 13 of 14 bronze days hold 25 publishes, and 18 September lacks 10:00). Added the CP1506 locator (BSC Panel paper 280/09, 5 July 2018, p5).
3. **Dedup key.** "_inline in transformer_" is now the actual key, with `fou2t14d.py:175-179` and line 59. Also
   added the `_latest` view (`latest_views.py:104-107`) and the fact that `query()` reads it.
4. **Silver schema table.**
   - `settlement_period` row: written only if bronze carries it (`fou2t14d.py:120`), and the live rows do not.
   - `timestamp_utc` row: midnight UTC of `settlement_date` in the live shape (`fou2t14d.py:132-139`).
   - `ingested_at` row: "Time ingested into bronze" is wrong. It is stamped at silver transform
     (`fou2t14d.py:181-186`).
5. **Silver sample.** Removed the stale `"settlement_period": "..."` line.
6. **Known issues, the "TODO: verify whether Elexon serves historical publications" item.** Added a dated
   update: a fetch on 2026-09-26 returned all 25 publishes of the 13 September window (bronze file and request
   named), so publishes at least 13 days old were served then. How far back Elexon serves is still unverified.

Left alone on purpose:
- the curl example (its `T00:00Z` format is valid for the vendor);
- "Historical depth: Several years." (unevidenced, but not used on the page);
- the dated 2026-09-17 measurements in Known issues (they are dated snapshots, not wrong).

## Unverified

- **Publish cadence.** The only vendor statement found is Elexon CP1506 (2018 assessment report, p5: FOU2T14D
  "Every weekday"). It predates the Insights API, and silver contradicts it (24 publishes on Sunday 13 September
  2026). The page states no dataset-level cadence, only that the charted publishes are an hour apart.
- **What moves `outputUsable` between publishes.** Elexon says only "accounting for planned outages". The page
  names no cause for any revision. The REMIT related note says "to look for the outage behind a revision", which
  is a use, not a claim.
- **Unit.** No Elexon doc found states MW for FOU2T14D, so the page says "no unit sent; MW by gridflow's column
  name".
- **How far back Elexon serves old publishes** (see correction 6).

## Open questions / for the checker

- **Frame column order.** `select.columns` leads with `output_usable_mw` rather than a key column, so the value
  survives the fold at 390. At 390 only one of `output_usable_mw` and `published_at` (23 characters) fits. The
  caption says the rows are hourly publishes 08:00 to 15:00, in order, so the publish time is recoverable. At 768
  and wider, the value, publish time and both other keys all show. The guide still lists the key columns under
  "Identifies a row".
- **Chart window avoids a missing publish.** Silver lacks the 18 September 10:00 UTC publish, and the renderer
  would break the line there (gap > 1.5 steps, `chart_svg.py:352-358`). A 13 to 21 September window would
  therefore show an unexplained break, a local gap the page may not describe. The window was chosen to start
  on the 19th.
- **The ingest comment differs from fuelhh/windfor** ("the end instant is included", not "the end is
  exclusive"). This is deliberate: Elexon's `publishDateTimeTo` is closed (code and bronze above), and the
  notebook depends on the 22 Sep 00:00 publish that comes from that closed end.
- **Glossary error outside my files.** `20-domain/glossary.md:123-124` says FOU2T14D gives "day-ahead
  generation availability forecasts by BM Unit". It is 2 to 14 days ahead, by fuel type; the by-unit dataset is
  UOU2T14D. I did not edit it. It needs a separate vault fix.
- **Sister dataset.** `uou2t14d` (by BM unit, written next) is related as "the same forward availability, per BM
  unit instead of per fuel", which is the OpenAPI's own contrast.

- **Guide wording.** `record.fields.settlement_date` reads "Delivery date the forecast is for, from the vendor `forecastDate`, a London date" (reworded after self-review, so it no longer reads as a forecast of the date).

## Template problems

None blocking.

## Screenshots checked (the site has no dark theme, so light equals dark)

- **Method:** headless Chrome at 1440, 1024 and 768 full page, and 390 through a same-origin 390 px iframe.
  - Each width was shot folded, and opened (`#fx` checked, notebook drawer opened by the wrapper script).
  - The pages were served by my server on 9743, now stopped.
  - Profiles are left in place: `scratchpad/fou-shots/ud`, `ud2`, `ud3`, `ud4`. The final pass (`v2-*.png`, profile `ud4`) was taken on the last build, covering the frame band at 1440 and 1024 folded and open, the 768 drawer, and 390.
- **Result: nothing is clipped or overlapping.** Checked:
  - hero title and quick facts;
  - scenery (turbine tops, offshore wind, labels; the 390 crop shows the right-hand scene as on other pages);
  - chart, axis labels and x label;
  - key, including the nuclear note wrapping at 768 and 390;
  - raw-feed URL and command wrapping at 390;
  - frame folded and unfolded (it scrolls inside its box when unfolded, as on other pages), and the guide;
  - notebook cells [1] to [5] with the DataFrame and the plot;
  - related list;
  - stratum corner labels.
- **No page-level horizontal scroll:** `scrollWidth` is 375 at a 390 viewport and 753 at 768.
