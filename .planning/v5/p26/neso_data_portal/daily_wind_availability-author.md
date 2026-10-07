# neso_data_portal/daily_wind_availability: author report

Writer: Opus 5.5 · high, 2026-10-06. Screenshot port 9866 (server stopped).

## Status

- **Build:** `gridflow-build --only neso_data_portal/daily_wind_availability` succeeds with no errors.
- **Detector:** `detect.mjs --json` returns `[]`, so there are no advisories at all.
- **Mirror:** byte-equal to the canonical note (`cmp`). Both files are CRLF, 311 of 311 lines.
- **Staged spec or authored override:** none existed for this dataset.
- **Artefacts:** all four are new and untracked in the front-end worktree:
  - `site/hifi/data/series/neso_data_portal/daily_wind_availability.json` (`spec_origin: vault`)
  - `site/hifi/data/samples/neso_data_portal/daily_wind_availability.json` (`generated_by: gridflow-sample`)
  - `site/hifi/data/notebooks/neso_data_portal/daily_wind_availability.json`
  - `site/hifi/data/notebooks/neso_data_portal/daily_wind_availability-5.png`
- **Chart:** a line of the daily sum of `availability_mw` over BM units for each availability day, 22 August to 3 September 2026. All 13 points come from one NESO file, published 20 Aug 2026 21:20 UTC. `ASHWW-1` (-1 MW) is filtered out. The values run from 25,381 to 26,474 MW.
- **Recommendation:** ship. The data is thin but accurate: one capture, 13 days, and the page claims no trend.

## The task's starting assumption was wrong

The brief described "percentile bands" and "per BM unit or in aggregate". Neither is true:

- The file has exactly three columns, `BMU_ID, Date, MW` (connector `endpoints.py:106`, transformer `daily_wind_availability.py:44`, and the bronze header).
- There is one value per unit per day.
- There is no aggregate row and no percentile.

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| Technical availability in MW, daily, 2 to 14 days ahead (summary, `what_it_is`, `facts`) | NESO CKAN text, captured in gridflow `.planning/phases/neso-data-portal/_probe/package_search_p0.json`. The package notes say "wind generator availability in megawatts (MW) at a daily resolution for 2-14 days ahead". The resource description says it is technical availability, "rather than what they are able to actually produce based on wind speed". Now quoted in the note body (Overview). Also `daily_wind_availability.py:3`. |
| Coverage fits the horizon | The one capture was published 20 Aug and covers days 22 Aug to 3 Sep (D+2 to D+14), from Polars over silver. |
| One row = unit × availability day × file version; key `bmu_id, availability_date, published_at` | `ENTITY_KEY_COLUMNS` (`daily_wind_availability.py:74-78`). Silver has 0 duplicates on the key and 0 on `(bmu_id, availability_date)`, because it holds one capture. |
| Captures accumulate rather than overwrite | `APPEND_ONLY = True` and `VINTAGE_PER_BRONZE_FILE = True` (`:70-71`). `_latest` view key `(bmu_id, availability_date)` (`latest_views.py:115-117`). Each capture is a whole-file snapshot (`client.py:1381-1392`). |
| `published_at` is NESO's CKAN `last_modified`, read as UTC, not a forecast issue time (`record.fields`) | `_bronze.py:72-74`. The sidecar has `ckan_last_modified: 2026-08-20T21:20:07.510686` and silver `published_at` is `2026-08-20 21:20:07.510686 UTC`. |
| `timestamp_utc` is the start of the GB day in UTC, 23:00 the day before in BST | `daily_wind_availability.py:190-205` (`settlement_period_to_utc(date, 1)`). Silver shows availability_date 2026-08-31 → `2026-08-30 23:00 UTC`. |
| `bmu_id` matches Elexon `national_grid_bm_unit`, not `bm_unit_id` (`what_it_is`, `fields`, `related`) | Polars join against `elexon/bmunits_reference`: 231 of 276 IDs match `national_grid_bm_unit`, all `fuel_type` WIND. 0 match `bm_unit_id`. The page words it as a project check. `elexon/uou2t14d` silver also carries `national_grid_bm_unit`. |
| `-1` sent and undocumented (caption, `fields`, record caption) | Bronze lines 171-183: `ASHWW-1` is -1 on all 13 days. Neither the vendor text nor the code defines it. |
| Requests: `package_show`, then the redirector | `client.py:1419-1423` and `endpoints.py:135-147`. The redirector URL is taken verbatim from the bronze sidecar `request_url`, and its shape is validated (`client.py:1062-1153`). |
| Ingest `--last 24h`; a dated past window is refused | `client.py:1340-1349`: an end more than 48 h old raises `NesoHistoricalWindowError`, and the error text itself recommends `--last 24h`. The bronze partition is `end.date()` (`client.py:1444`). |
| Transform `--start D --end D` on the ingest day | `pipeline/runner.py:1125-1138`: dates are inclusive and each one is transformed. A single date avoids a no-bronze day inside the window. |
| Notebook lead: `query()` reads `..._latest`, filters `availability_date`, both ends inclusive, lineage dropped | `schema_manifest.py:24-65` (`_latest` for APPEND_ONLY with a spec), `schema_manifest.py:272` (date column), and `gridflow_models/research/handles/source.py:401-450`. The notebook output confirms it. |
| Chart values in the alt text | The committed series: 25,744 / 25,968 / 25,751 / 25,786 / 25,598 / 25,665 / 25,381 ×3 / 26,215 / 26,474 ×3. `rows_used` is 3,575. |
| "The MW axis does not start at zero" (caption) | Rendered axis: 25,250 to 26,750 at 1440, 1024 and 768, and 25,000 to 27,000 at 390. The caption therefore names no number. |

## Body corrections (canonical note, each the smallest span)

1. **Overview.** The note said "`BMU_ID` joins straight to Elexon BM units". It now says the ID is National Grid's, matches `national_grid_bm_unit` and never `bm_unit_id`, and gives the join counts. I also added NESO's own description, quoted from the CKAN probe capture.
2. **Bronze sample.** The rows were hand-authored (`T_ABRBO-1,2026-08-16,42.5`). I replaced them with the real first rows of `raw_20260820T214333Z_e91f317b.csv` and noted the whole-number MW and the trailing CR-only line.
3. **Silver path pattern.** `<year>/<month>/<day>/data_<run_suffix>.parquet` is now `year=<YYYY>/month=<MM>/daily_wind_availability_<YYYYMMDD>_run<stamp>.parquet` (`silver/base.py:2633-2635`, and the actual file).
4. **Silver schema rows.** The `bmu_id` join target is corrected. `availability_mw` now reads "technical availability" and flags `-1`.
5. **Silver sample.** The `T_` IDs and invented values are replaced with real rows. I added the lineage-column note (no `ingested_at` column exists in this table).
6. **Known issues.** Two bullets added: the `-1` sentinel, and the all-null row defect.

## Not verified

- **How often NESO republishes.** Superseded by revision 2: NESO's CKAN `extras` give `Update Frequency: Hourly`, and the page now states that as a catalogue fact (see `-author-2.md`).
- **What `-1` means.** Undocumented.
- **Why 45 of 276 IDs are missing from the Elexon register snapshot.** These may be new units or a register lag. They are not investigated, and the page claims no count.
- **Whether `MW` values are always whole numbers.** True in the one capture, but not stated on the page.

## Open questions for the seat

- **Holdings.** Silver holds a single vintage, so the page shows nothing about revisions between captures. That is fine for a thin-but-accurate ship. A second capture would let a later page show vintages.
- **`needs`.** The notebook `needs` reads "NESO's file of 20 August 2026". The reader cannot fetch that file any more, because backfill is refused. The wording is honest, but the seat may prefer a generic phrasing.

## Template problems (report only, nothing worked around)

- **No dark theme.** The site has none: no `prefers-color-scheme` or `data-theme` anywhere in `site/hifi/assets`. The rubric's "light and dark" check has only one theme to look at, and the dark captures are identical to the light ones.
- **Notebook tab truncation.** At 390 the tab truncates `daily_wind_availability.ipynb` to `daily_wind_availabili…`. This is ellipsis by design, not overlap, but it affects any long dataset key.
- **Line y axis.** The line renderer does not start the y axis at zero, and its ticks vary with width (25,250 at ≥768, 25,000 at 390). A caption cannot quote the axis start reliably.
- **390 capture method.** A direct `--window-size=390` is not a true 390 viewport, because Chrome lays out at about 500 px and crops. A 390 iframe at 9000 px height stopped painting partway down. An iframe sized near the page height (6400) with `--virtual-time-budget=10000` painted fully.

## Screenshots

These are under the scratchpad at `dwa_shots/`:

- Final full pages: `final_1440.png`, `final_1024.png`, `final_768.png`, `final_390.png` (390 iframe).
- Earlier crops: `g_390_*.png`, `k_768.png`, `k_1024.png`.

What I checked:

- The hero scenery, including the turbine tops, at all four widths.
- The chart and key.
- The raw-feed boxes; the long redirector URL wraps.
- The frame: folded to two columns at 390, and up to `event_time` at 1440.
- The column guide, notebook panel, related list, and every stratum corner label.

Nothing is clipped or overlapping.

## Defects

- **gridflow / NESO Data Portal `daily_wind_availability`: an all-null row reaches silver.**
  - The vendor CSV ends with a line holding only `\r`.
  - `read_csv_bronze_body` passes the whole body to `pl.read_csv` (`src/gridflow/silver/csv_bronze.py:123-128`) with no blank-row drop, so that line becomes a row of nulls.
  - The strict casts in `daily_wind_availability.py:184-188` keep the nulls. Schema validation is fail-soft by design (`silver/base.py:2021-2027`), so the row is written: null `bmu_id`, `availability_date`, `availability_mw` and `timestamp_utc`, with valid `published_at` and lineage.
  - As a result, silver holds 3,589 rows where 3,588 are real (DATA-MATRIX counts the null row).
  - A query on `availability_date` never returns it. The `_latest` view gets a null-keyed group, and any `data.sql` sum or count includes it.
  - Fix: drop all-null or blank rows in `read_csv_bronze_body`, or in the transformer before casting. This may also affect the other NESO Data Portal CSVs: check `historic_generation_mix` and `embedded_wind_solar_forecast` bronze tails.
- **Vendor data / NESO `daily-wind-availability`: undocumented `-1` MW.**
  - In the 20 Aug 2026 file, `ASHWW-1` is `-1` on every day.
  - NESO does not define it. gridflow carries it verbatim, which is correct.
  - Consumers that sum availability must exclude it. Log it on the vault remediation page as a vendor-semantics unknown.
- **gridflow / silver `base.py` (low): the APPEND_ONLY filename stamp disagrees with the row stamp.**
  - The silver file is `daily_wind_availability_20260820_run2026-08-20T21-43-33.257005-00-00.parquet`, which is the bronze sidecar `written_at`.
  - The rows' `available_at` is `2026-08-20 21:20:07.510686` (`ckan_last_modified`).
  - `_write_silver`'s docstring (`base.py:2616-2625`) says the suffix is the ISO `available_at`. Either the docstring or the stamp passed in (`base.py:1019-1067`, `_timestamp_from_sidecar`) is wrong.
- **Vault (fixed in this branch): stale `daily-wind-availability.md`.**
  - Fabricated `T_`-prefixed bronze and silver samples.
  - A wrong join claim ("joins straight to Elexon BM units").
  - A wrong silver path pattern.
