# demand-forecasts: author report

Family page `demand-forecasts` (lead `ndf`; members `ndfd`, `tsdf`, `tsdfd`). Writer, 2026-09-29.

## Status

- **Page block:** `page:` block in the lead note `30-vendors/elexon/datasets/ndf.md`, in the vault worktree. The other three notes carry no `page:` block. All four notes are mirrored byte for byte to `vault/elexon/` (CRLF kept).
- **Artefacts:**
  - `site/hifi/data/series/elexon/ndf.json` (`gridflow-distil`, `spec_origin: vault`, 2 series, 48 points, 86 rows used).
  - `samples/elexon/ndf.json` (`gridflow-sample`).
  - `notebooks/elexon/ndf.json` and `ndf-6.png` (`scripts/run_notebooks.py`: 6 cells, 1 image, no errors).
  - There was no staged spec and no authored override to retire.
- **Build:** `gridflow-build --only elexon/ndf` passes. It writes `demand-forecasts.html` and rewrites the `ndf`, `ndfd`, `tsdf` and `tsdfd` pointers.
- **Detector:** `detect.mjs --json` returns `[]`.
- **Screenshots:** headless Chrome at 1440, 1024 and 768, and at 390 through a 390 px iframe. The notebook drawer was opened through a same-origin wrapper at 1440 and 390. Nothing is clipped or overlapping.
  - The site has no dark theme: there is no `prefers-color-scheme` or `data-theme` rule in `assets/`. Light is the only mode.
  - The `[4]` DataFrame output scrolls sideways at 390 (`.df-wrap { overflow-x: auto }`, `theme.css:431`), the same as other notebooks.

## Chart

- **Type:** a line, one value per half-hour.
- **Data:** settlement date 17 September 2026 (23:00 UTC on 16 Sep to 22:30 UTC on 17 Sep), from two NDF publishes on 16 Sep.
- **Series:**
  - `morning` = the 07:45 UTC publish (38 points, from 04:00 UTC);
  - `evening` = the 22:47 UTC publish (48 points).
- **Spec:** filter `settlement_date eq` plus `published_at in [...]`; `group: published_at`, with `group_map` on the cast strings.
- **Why this reading:** NDF's distinguishing trait is that silver keeps every publish. A week of one line would duplicate the INDO page's chart, and a week also puts partial days at both axis edges (the 07:45 publishes run from 04:00 to 04:00).
- **Revision and scoring:** the eight-row frame follows the 16:30 UTC half-hour through eight publishes. The notebook scores the 07:45 and last publishes against INDO over 14 to 20 September.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| NDF request: `GET .../datasets/NDF?publishDateTimeFrom=...T00:00:00Z&publishDateTimeTo=...T00:00:00Z&page=1`; same shape for NDFD, TSDF, TSDFD (`raw_feed.requests`, `family.members[].request`) | `connectors/elexon/endpoints.py:126-134, 210-219` (all `PUBLISH_DATETIME`, default `publishDateTimeFrom/To`); `build_params` `endpoints.py:300-313` adds `page` (`supports_pagination` default True); `_to_utc_z` `endpoints.py:267-277` gives `%Y-%m-%dT%H:%M:%SZ`; 24 h chunks, `client.py:92-99` (`max_chunk_hours=24`). The connector sends no `boundary` param for TSDF. |
| "24-hour publish windows"; "each silver file holds one UTC publish day" (`raw_feed.note`) | `client.py:92-99`; bronze `data_date = start.date()` `client.py:314`; transformer reads bronze day D only (`demand_forecast.py:34-58`); Elexon publication-window filter on `published_at` (`silver/elexon/_publication_window.py` docstring; `silver/base.py:1687-1712`). Checked: every NDF and TSDF silver row's `published_at` date equals its file date. |
| Ingest `--end 2026-09-21` is exclusive, transform `--end 2026-09-20` inclusive (`raw_feed.commands`) | `client.py:95-99` `while current < end` (exclusive instant); same semantics as the approved INDO page. Window covers the notebook's needs (publishes 13 to 20 Sep); the chart needs only 16 Sep. |
| Key `(settlement_date, settlement_period, forecast_type, published_at)`; "every publish stays" (`record.key`, `published_at` meaning, `what_it_is`, ndf `differs`) | `demand_forecast.py:31-32` (`ENTITY_KEY_COLUMNS`, `OPTIONAL_ENTITY_KEY_COLUMNS`), `:150-153` (`unique` on those four). Silver check: 0 duplicates on the four columns. |
| `forecast_type` is `day_ahead` on NDF, `2_14_day` on NDFD (field meaning) | `demand_forecast.py:147-148`. |
| `timestamp_utc` = start of the half-hour from settlement date and period | `demand_forecast.py:127-138` (`settlement_period_to_utc`). The eight rows show period 36 = 16:30 UTC. |
| `national_demand_mw` = vendor `demand` | `demand_forecast.py:67-68`; bronze sample `"demand":20260`. |
| `published_at` from `publishTime` | `demand_forecast.py:70-71, 113-118`. |
| NDF silver has no `transmission_demand_mw` and no `boundary` | `demand_forecast.py:163-175` (select of present columns; `boundary` not in `output_cols`); silver schema checked (12 columns, listed in the frame). |
| NDFD: one figure per date, period fixed at 1 (ndfd `differs`) | `demand_forecast.py:86-91`; bronze NDFD rows carry only `publishTime`, `forecastDate`, `demand`; silver `settlement_period` unique = `[1]`. |
| "2 to 14 days ahead" (NDFD, TSDFD) | Elexon dataset names ("2-14 Day Ahead", `endpoints.py:131-134, 215-219`). Silver lead (forecast date minus publish date) runs exactly 2 to 14. |
| TSDF: `N` plus boundaries `B1` to `B17`; one vintage per publish day, that is, per (period, boundary) per UTC publish day (tsdf `differs`, `what_it_is`); the 2026-09-15 file kept rows from two publishes (00:17 and 07:45) | `tsdf.py:112-115` (dedup key without `published_at`, run per daily transform); tsdf.md live-verified 18 boundaries; silver: 18 boundary values. Silver: 22,500 key duplicates across files, 0 within a file, so there is one survivor per publish day. |
| TSDF `N` is "transmission system demand, the `ITSDO` quantity" (`what_it_is`) | Dataset name (`endpoints.py:211-212` "Transmission System Demand Forecast"; schema docstring `schemas/elexon.py:400-405`) and NESO's TSD definition quoted in `indo.md` (#01:268). Project check only: TSDF `N` minus same-publish NDF has a floor of exactly 500 MW (median 500, max 7,672), which fits TSD = ND + 500 MW BST station-load estimate + pumping + exports. Not stated by Elexon; not on the page. |
| `NDF` is the quantity `INDO` reports (`what_it_is`, related) | Names (National Demand Forecast / Initial National Demand Outturn; NESO "National Demand ... equivalent to INDO", `indo.md` #01:244); ndf.md gotcha live check 2026-07-31. The notebook output shows the scale match. |
| TSDFD `timestamp_utc` is midnight UTC; NDFD's is 23:00 UTC in BST (body corrections) | `tsdfd.py:79-82`; `schemas/elexon.py:510-511`; NDFD silver rows show 23:00 UTC the day before. |
| `query()` relation and date column, both ends included, lineage dropped (`notebook.lead`) | gridflow_models `research/handles/source.py:401-451`; registry run: ndf, ndfd, tsdf use `settlement_date` (DATE); **tsdfd uses `timestamp_utc` (TIMESTAMPTZ)**; exclude list `event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year`. |
| "The first cell converts times to UTC" (lead) | The INDO notebook output shows `query()` timestamps as `+01:00`. My cell `tz_convert("UTC")`; the output head shows `+00:00`. |
| Cadence "NDF and TSDF about every 30 minutes; NDFD and TSDFD daily" (`facts.cadence`) | ndf.md gotcha (live-verified 2026-07-31: "republished roughly every 30 minutes"); tsdf.md gotcha (same); ndfd.md / tsdfd.md "Daily publication". The eight rows show several publishes per day. |
| Chart numbers (alt, key note): 07:45 line starts at 04:00 at 18,180 MW; within 460 MW until 07:00; higher from 07:30, by up to 2,712 MW at 15:00; peaks 29,970 at 18:30; the 22:47 line peaks 29,000 at 18:00, dips 18,000 at 03:00 | Committed `series/elexon/ndf.json` values (read back: morning 38 points, first `2026-09-17T04:00:00Z` 18180; the difference is -460 at 04:00, and every point from 07:30 to 22:30 is positive; max difference +2,712 at 15:00). |
| Eight rows: 28,734 down to 26,554 MW across publishes 16 Sep 07:45 to 17 Sep 16:18 (`record.caption`) | `samples/elexon/ndf.json`. |
| Plot alt: 07:45 minus INDO peaks 3,603 MW at 15:00 UTC on 15 Sep, lowest -1,360 on 19 Sep; last publish -1,015 to 2,943 MW; mean abs errors 875 and 574 MW | Notebook outputs (cell 5 text) plus a Polars re-computation of the same logic (326 matched half-hours; identical means). |
| Related notes | indo/itsdo pairings as above; windfor: residual demand = demand minus wind (standard use, no numeric claim); embedded wind and solar: NESO "suppress the electricity demand" (`indo.md` #01:292). All four keys resolve (build passes). |

## Note-body corrections (smallest span, each cited in the note)

**ndf.md**
- Dedup key placeholder replaced with `(settlement_date, settlement_period, forecast_type, published_at)` (`demand_forecast.py:150-153`).
- `transmission_demand_mw`: "always `null` in live NDF silver" corrected to "absent from NDF silver" (`demand_forecast.py:110-111,174`). The same fix is made in the "Pairs with INDO" gotcha.
- `ingested_at`: "Time ingested into bronze" corrected to the silver transform time (`demand_forecast.py:155-160`).
- Silver sample: `timestamp_utc` for 6 May period 9 corrected from `04:00` to `03:00` UTC (the bronze `startTime` is `03:00Z`). The non-existent `transmission_demand_mw` and `issue_time` keys are replaced with `published_at`.
- Forecast-revision gotcha: "up to 47 distinct vintages" replaced with the mechanism. A period keeps a vintage from every publish that covers it, across up to three publish days, so a one-window count understates it. No replacement count is given.

**ndfd.md**
- Dedup key placeholder replaced with the four-column key: one row per forecast date per publish.
- `settlement_date` source corrected from `settlementDate` to `forecastDate`.
- `settlement_period` corrected from "1..50" to "always 1 (placeholder)".
- `timestamp_utc` is period 1's start: 23:00 UTC the day before, in BST.
- `transmission_demand_mw` is absent from NDFD silver.
- `ingested_at` is the transform time.
- Silver sample corrected: `settlement_date` `2026-04-03`, period `1`, `timestamp_utc` `2026-04-02T23:00`, and `published_at` in place of `issue_time`.
- Gotcha: "join on `forecast_date`" corrected to "join on `settlement_date`". Silver has no `forecast_date` column. "Full daily aggregate" changed to "which daily statistic is undocumented".

**tsdf.md**
- Point-in-time field: `ingested_at (no native PIT field)` corrected to `published_at` (`tsdf.py:98-110`). A missing `published_at` schema row is added.
- Dedup key placeholder replaced with `(settlement_date, settlement_period, boundary)`, applied per daily transform.
- `ingested_at` is the transform time (`tsdf.py:117-123`).
- Silver sample `timestamp_utc` corrected from `04:00` to `03:00`.
- Vintage gotcha: "all vintages collapse to one arbitrary survivor" corrected to "one survivor per publish day". Row order, not publish time, picks the survivor; in the 2026-09-15 file it was the day's earliest publish.

**tsdfd.md**
- `timestamp_utc` corrected from "settlement-period derived" to "`forecast_date` at 00:00 UTC" (`tsdfd.py:79-82`).
- Point-in-time field corrected to `published_at` (`tsdfd.py:84-90`).
- Dedup `(forecast_date)` is per daily transform, so a date recurs once per publish.
- `ingested_at` is the transform time (`tsdfd.py:101-107`).
- "Daily aggregate" changed to "which daily statistic is undocumented".

## Not verified

- **What the NDFD and TSDFD daily figure is (peak, average or total).** The fields and the notes give no vendor evidence. In the project's data NDFD sits near the day's NDF maximum (within about 2 GW at a 2-day lead), and TSDFD is exactly NDFD plus 500 MW in every silver row. Neither fact is on the page.
- **Why NDF has a 07:45 UTC publish that covers exactly 04:00 to 04:00 UTC the next day, and why the rolling publishes end at 03:30 UTC and extend a day at about 10:48 UTC.** This was measured on silver, and nothing vendor-side documents it. The page states it only as what the chart shows ("starts at 04:00 UTC"; "the 07:45 UTC publish").
- **The `B1` to `B17` boundary meanings.** They sum to about 2.4 times `N`, so they are not parts of it. The page says only "boundaries".

## Open questions

1. **NDFD and TSDFD vendor definition.** Should a research unit fetch Elexon's dataset description for NDFD and TSDFD, to settle peak versus other daily statistic?
2. **TSDF silver.** Silver keeps one arbitrary (row-order) vintage per publish day. Is that a schema decision for gridflow, with `published_at` in the key as NDF has it? The note already flags this.

## Template problem (reported, not worked around)

- **The frame folds by silver column order.** For NDF the columns that tell the eight rows apart (`national_demand_mw`, `published_at`) are 5th and 6th. At 768 and 390 they sit behind `…`, so the visible rows look identical: the key columns plus `timestamp_utc` and `forecast_type`, all constant here. Nothing is clipped, but the frame's point is lost below 1024.
  - A note can choose rows but not column order.
  - Worth considering: pin non-constant columns first, or fold constant columns first.
  - The same will affect any vintage table (NDF, TSDF, and the indicated-day-ahead family).

## Revision 1 (after `demand-forecasts-review.md`, REVISE: 1 major, 3 nits)

- **Major, `page.what_it_is` attribution:**
  - Now reads "`NDF` forecasts GB national demand, which NESO equates with `INDO`" and "`TSDF` forecasts transmission system demand, which NESO equates with `ITSDO`". This matches the `demand-outturn` wording.
  - NESO's equivalences are quoted in `indo.md` (#01:244, #01:268).
- **Nit 1, notebook lead:** "The first cell converts times" is now "The query cell converts times".
- **Nit 2, boundary count:** the unscoped "17 transmission boundaries `B1` to `B17`" is gone.
  - `what_it_is` now says "beside other boundary codes (`B1`, `B2` and so on)".
  - `family.members[tsdf].differs` now says "Transmission demand at `N` plus other boundary codes; one vintage per publish day".
- **Nit 3, grain:** `facts.grain` now covers all four members (13 words): "NDF: half-hour and publish; TSDF: half-hour, boundary, publish day; NDFD, TSDFD: date, publish". The keys come from `demand_forecast.py:150-153`, `tsdf.py:112-115` and `tsdfd.py:99`.
- **Optional body note, taken:** `ndfd.md` and `tsdfd.md` say "the fields do not say which daily statistic" instead of "undocumented".
- **Artefacts:** unchanged. No chart, record-select or notebook-cell edits, so the series, sample and notebook digests still hold.
- **Checks re-run:** `gridflow-build --only elexon/ndf` passes and `detect.mjs --json` returns `[]`. All four notes are re-copied to the mirror, byte-identical with CRLF kept.

## Revision: column order

- **Change:** `record.select.columns: [published_at, national_demand_mw, settlement_period]`, checked against silver's column names. The rest follow in silver's order: `settlement_date`, `timestamp_utc`, `forecast_type`, then the pipeline columns.
  - These are the two columns that differ across the eight rows, then the target period. The date, period, `timestamp_utc` and `forecast_type` are the same in all eight rows, and the caption names them.
  - `record.fields` is reordered to match. Its words and key are unchanged.
- **Artefacts:** re-ran `gridflow-sample --dataset elexon/ndf`, which rewrote `samples/elexon/ndf.json`. The series and notebook are untouched.
- **Mirror:** the vault note is mirrored byte for byte (295 lines, CRLF).
- **Build:**
  - `gridflow-build --only elexon/demand-forecasts` renders nothing. It reports "0 template page(s)" and left the page file unchanged.
  - The family page builds under its lead key: `--only elexon/ndf` wrote `demand-forecasts.html` with the new order (`published_at`, `national_demand_mw`, `settlement_period`, ...).
  - `detect.mjs --json` returns `[]` on the rebuilt page.
- **Screenshots (headless Chrome, port 9725, server stopped):**
  - **1280:** the frame shows `published_at`, `national_demand_mw`, `settlement_period`, `settlement_date`, `timestamp_utc` and `forecast_type` before the `…`. The eight falling values (28,734 to 26,554 MW) sit beside their publish times.
  - **390 (390 px iframe):** only `published_at` fits before the `…`. The eight distinct publish times now tell the rows apart, but `national_demand_mw` folds, because the two columns together need about 350 px against about 330 px of box.
  - Nothing is clipped or overlapping at either width.
