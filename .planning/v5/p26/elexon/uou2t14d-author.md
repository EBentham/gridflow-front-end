# uou2t14d: writer's report

Page: `elexon/uou2t14d`, "Availability forecast by BM unit". Build `--only elexon/uou2t14d` green, detector `[]`.
Chart: `line`, x = `settlement_date`, one publish (`published_at` = 2026-09-21 20:00 UTC), delivery dates 23 September
to 5 October 2026, three units (Peterhead Block 1, Heysham 1 Generator 1, Seagreen 6), `aggregation: last`, nothing
summed.

## The two findings that shape the page

1. **Silver does not keep every publish, and the key has no publish time in code.** The brief expected "the silver
   key includes a publish time". For this dataset it does not. `silver/elexon/uou2t14d.py:133-136` dedups on
   `(settlement_date, [settlement_period], bm_unit_id)` with `keep="last"` over one bronze day at a time; the
   class is not `APPEND_ONLY` and has no `published_at` in `ENTITY_KEY_COLUMNS` (`:26`). The vendor publishes every hour
   (bronze 2026-09-21: 24 publishes plus the next day's 00:00, 7,215 rows each), so each fetched day's publishes
   collapse to one row per unit and delivery date. The survivor is the last row read: files in sorted name order
   (`:40`, names are ingest time plus a body-hash prefix), and within a file the API lists the newest publish first. So
   the kept publish is set by file order, not publish time: silver's main publish per day is 16:00, 20:00, 08:00 or
   12:00 UTC depending on the day, plus a 23:00 publish for the one new date it adds. Rows from different fetched days
   coexist (one file per day), so `(settlement_date, bm_unit_id, published_at)` has 0 duplicates in local silver, while
   `(settlement_date, bm_unit_id)` has 73,424. `fou2t14d` was fixed for exactly this (F-06: `APPEND_ONLY`, `published_at`
   unconditional in the key); `uou2t14d` was not.
2. **Units without an Elexon id collapse to one row.** The vendor says the dataset "is aggregated by National Grid
   Balancing Mechanism Units" and marks `bmUnit` nullable (OpenAPI `AvailabilityByBmUnitDaily`). In the 2026-09-21 20:00
   UTC publish, each forecast date has 555 NGC units, 81 of them with `bmUnit` null. The dedup key uses `bm_unit_id`, and
   Polars `unique` treats nulls as equal, so one null row survives per date (always `WTGRW-1` in the files probed): silver
   has 475 units per date, not 555. The frame shows that one null row on purpose.

Both are gridflow defects for the seat. I did not work around them; the page states them as code facts.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Title / summary: forward view of each BM unit's available output, one figure per delivery date, 2 to 14 days ahead | Vendor OpenAPI `/datasets/UOU2T14D` description: "forward view of availability ... from 2 days ahead to 14 days ahead"; row schema named `AvailabilityByBmUnitDaily`, fields `forecastDate` (date), no period. Quoted in the note body Overview. |
| `facts.vendor` Elexon BMRS, dataset UOU2T14D | `connectors/elexon/endpoints.py:146-147` path `/datasets/UOU2T14D` |
| `facts.cadence` not stated in Elexon's API docs | OpenAPI description and parameters give no schedule. |
| `facts.grain` one row per delivery date and BM unit per fetched day | `uou2t14d.py:133-136` dedup per bronze day; `read_bronze` reads one `bronze/<y>/<m>/<d>` dir (`:29-53`); silver file per day `uou2t14d_YYYYMMDD.parquet`. |
| `record.key` settlement_date, bm_unit_id, published_at | Local silver: 0 duplicates on these three, 73,424 on the first two. Code does not guarantee the three-column key (see Unverified). |
| `what_it_is`: "what the Grid Code calls Output Usable", "per National Grid BM unit", "accounting for planned outages" | OpenAPI description, quoted in the note body. |
| `what_it_is`: one row per unit and date from each fetched day, picked by bronze file order, not publish time | `uou2t14d.py:40` `sorted(bronze_path.glob("raw_*.json"))`; `:136` `unique(subset=dedup_cols, keep="last")`; no `published_at` in the key. |
| `chart`: one publish, `published_at eq 2026-09-21T20:00:00Z` | `distil.py:78-97` coerces ISO strings for tz-aware columns; series `rows_matched: 39` = 3 units x 13 dates. |
| `chart_view.caption`: 20:00 UTC publish of 21 September, delivery dates 23 September to 5 October, one figure per unit and date, nothing summed | Committed series: `x` 2026-09-23 .. 2026-10-05 (13 points), `aggregation: last`, one row per unit per date after the publish filter. |
| `chart_view.alt` and key notes: Peterhead 0 through 29 Sep then 1,180; Heysham 0 then 262, 360, 476, 498 from 3 Oct; Seagreen 89 (23rd) to 299 (24th), ends 172 | `site/hifi/data/series/elexon/uou2t14d.json` values, printed and checked. |
| Key labels: Peterhead Block 1, Heysham 1 Generator 1, Seagreen 6 | `bmunits_reference` silver `bm_unit_name`: "Peterhead Block 1", "Heysham 1 Generator 1", "Seagreen1 Offshore WF 6" (shortened as on the `pn` page). |
| Key notes: fuel type CCGT, NUCLEAR, WIND | The rows' own `fuel_type` (vendor `fuelType`), sample and silver. |
| Paints clay, petrol, horizon | Palette roles gas, nuclear, wind (`page_fields.py` `DEFAULT_PAINT`); no khaki. |
| `raw_feed.note`: 4-hour publish windows, the most the API accepts | `endpoints.py:150` `max_chunk_hours=4  # API rejects ranges > 4 hours`; `client.py:93-98` chunk loop. |
| `raw_feed.requests` URL | Bronze meta `request_url` for 2026-09-21: `publishDateTimeFrom=...T20:00:00Z&publishDateTimeTo=2026-09-22T00:00:00Z&page=1`, parameter order and format as sent (colons URL-encoded on the wire). |
| Ingest `--start 2026-09-21 --end 2026-09-22`: six 4-hour publish windows, bronze day 21 | `pipeline/runner.py:479-500` bare date = midnight UTC; `client.py:94-98` `while current < end`, 24 h / 4 h = 6; `client.py:314` `data_date = start.date()`. Bronze 2026-09-21 holds exactly six files. |
| Transform `--start/--end 2026-09-21` | `base.py:417` `PARTITION_SOURCE_OFFSETS = (0,)` default, not overridden; charted publish lives in bronze day 21. |
| `record.select`: eight rows, delivery date 30 Sep, 20:00 publish | `gridflow-sample` output, `generated_by: gridflow-sample`. Filter on `national_grid_bm_unit` so the null-id row can be picked. |
| Field `bm_unit_id`: null for units sent without one, one kept per date | OpenAPI `bmUnit` nullable; dedup on it (`:133-136`); frame row 8 is `null`, `WTGRW-1`. |
| Field `output_usable_mw`: no unit sent, MW by gridflow's column name | OpenAPI `outputUsable` integer, no unit field; column name `uou2t14d.py:66`. Same wording as `fou2t14d`. |
| Field `national_grid_bm_unit`: Elexon's id adds a prefix such as `T_` | OpenAPI: "Elexon BMUs differs from NGC BMUs by including a prefix e.g. 'T_'". |
| Field `published_at` from `publishTime`, UTC | `uou2t14d.py:63-64, 98-103`; bronze carries `publishTime` only. |
| Field `settlement_date` from `forecastDate` | `uou2t14d.py:62`. |
| Field `timestamp_utc`: midnight UTC of the delivery date, set by gridflow | `uou2t14d.py:125-131` (no `settlementPeriod` in the feed); frame shows `2026-09-30 00:00:00 UTC`. |
| `notebook.lead`: relation `silver_elexon_uou2t14d`, filtered on `settlement_date`, both ends, every stored publish, no latest view, lineage dropped | gridflow `schema_manifest.py:143` date column `settlement_date`; `_preferred_relation` (`schema_manifest.py:18-65`) gives `_latest` only for `APPEND_ONLY` with a `LATEST_VIEW_SPECS` entry, and `latest_views.py:94-107` has `fou2t14d` only; gridflow_models `research/handles/source.py:401-451` (`BETWEEN`-style inclusive predicate, `EXCLUDE` bitemporal columns). |
| Notebook outputs | `scripts/run_notebooks.py` run; cell 3 prints min 2026-09-23, max 2026-10-05; cell 4 shows 28 Sep to 2 Oct for the three units; cell 5 step plot `uou2t14d-5.png`. Read-only calls only. |
| `related` | All four have pages in `site/hifi/data/elexon.json`; build resolved them. |

## Note-body corrections (canonical vault note, copied byte for byte to the mirror; 301 lines, all CRLF)

- Overview: "every BM Unit's declared availability MW for every settlement period" corrected to one figure per NGC BM
  Unit per forecast date, daily rows, no settlement period; added the vendor's OpenAPI description as a quote.
- API table, Publication lag: "Daily publication." corrected to "not stated" plus the bronze observation (a publish
  every hour, 13 forecast dates each, moving on a day at the 23:00 UTC publish), dated.
- Silver, Dedup key: "_inline in transformer_" replaced by the actual key, `keep="last"` per bronze day, not
  `APPEND_ONLY`, survivor by file order (`uou2t14d.py:40, 133-136`).
- Silver, Point-in-time field: "`ingested_at` (no native PIT field)" corrected to `published_at` (vendor `publishTime`),
  plus `available_at`.
- Silver schema: `settlement_period` marked absent (`uou2t14d.py:112-131`); `timestamp_utc` derivation corrected to
  midnight UTC (`:125-131`); `bm_unit_id` nullable Yes, with the null-collapse note; `ingested_at` is transform time
  (`:138-142`), not bronze ingest time.
- Silver sample: replaced the stale row (with `"settlement_period": "..."`) by a real silver row (T_PEHE-1, 30 Sep,
  20:00 publish).
- Known issues: row-count claim ("multi-hundred-thousand rows for a single 4-hour query") corrected to 36,075 rows per
  window for 2026-09-21; added the null-`bmUnit` collapse and the file-order survivor.

Left alone: pre-existing em dashes in the body, the curl example (still valid for the vendor), `last_verified`.

## Unverified

- **The three-column key is not guaranteed by code.** A publish at 00:00 UTC appears in two bronze days (the 20:00 to
  24:00 window of day D and the 00:00 to 04:00 window of day D+1). It never wins in day D's file today only because the
  API lists newest first and later rows overwrite; nothing enforces that. If two fetched days ever kept the same
  publish, `(settlement_date, bm_unit_id, published_at)` would repeat.
- "Newest first within a response" and "window includes both ends" are observed in bronze, not documented by Elexon.
  The page states neither; the body note cites bronze for the hourly publishes.
- Whether Output Usable is a daily peak, a minimum or something else is undocumented in the OpenAPI text; the page says
  only "one figure per delivery date".
- The key label "Seagreen 6" shortens the register name "Seagreen1 Offshore WF 6", as the approved `pn` page does.

## Open questions for the seat

1. Open a gridflow issue for `uou2t14d`: make it `APPEND_ONLY` with `published_at` in the key (as F-06 did for
   `fou2t14d`), key on `national_grid_bm_unit` (never null in bronze) instead of the nullable `bm_unit_id`, and add a
   `_latest` view. When it lands, this page's grain, key, `what_it_is`, raw-feed note, `bm_unit_id` field and notebook
   lead need a rewrite, and the frame's null row will change.
2. DATA-MATRIX marks `uou2t14d` "agree"; with 80 of 555 units dropped per date, that row should carry the defect.

## Differences from the sister page (`fou2t14d`), all from code

- Sister grain "every publish kept" and key `(settlement_date, fuel_type, published_at)` from `APPEND_ONLY` and an
  unconditional `published_at` key. Here: one row per unit and date per fetched day; the key is stated with
  `published_at` but code only dedups on date and unit.
- Sister notebook reads `silver_elexon_fou2t14d_latest`; here there is no latest view, so `query()` returns every
  stored publish and the notebook filters one publish itself.
- Sister request uses 24-hour windows; here the connector sends 4-hour windows (`max_chunk_hours=4`).
- Sister's `settlement_date` field says "a London date"; I did not claim that (not in the vendor text), and wrote
  "Delivery date forecast, from the vendor `forecastDate`".
- Shared wording kept: "delivery date", "publish", "Output Usable", "no unit sent, MW by gridflow's column name", the
  `timestamp_utc` line, and the related-dataset notes mirror each other.

## Template and site notes

- The site has no dark scheme (no `prefers-color-scheme` or `data-theme` in `site/hifi/assets/`, nothing in
  `DESIGN.md`), so the "light and dark" checks render identically. Screenshots taken both ways anyway.
- Nothing clipped or overlapping at 1440, 1024, 768 or 390 (390 in a 390 px iframe). Scenery tops, scene edges and the
  stratum corner labels are whole. At 390 the request URL and the notebook code wrap inside their boxes.
- The frame folds after `national_grid_bm_unit` and `published_at` at 768 and after `output_usable_mw` at 390. I put
  `national_grid_bm_unit` third so the null-id row keeps its identity at 768.
- No template problems found. No staged chart spec or authored override existed for this dataset.

## Artefacts

- `site/hifi/data/series/elexon/uou2t14d.json` (`spec_origin: vault`, 3 series x 13 points)
- `site/hifi/data/samples/elexon/uou2t14d.json` (8 rows, 13 columns)
- `site/hifi/data/notebooks/elexon/uou2t14d.json`, `uou2t14d-5.png`
- Built page `site/hifi/data-sources/elexon/uou2t14d.html`
- Screenshots: `<scratchpad>/uou-shots/w{1440,1024,768,390}-{light,dark}-t*.png`
