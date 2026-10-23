# System frequency (`system-frequency-data`): writer's report

Family page, lead key `system_frequency`; members `system_frequency`, `_dmy_csv`, `_gmt_csv`, `_gmt_zip`,
`_offset_csv`, `_offset_zip`. Canonical note `C:\gridflow-wt\vault-neso-sys\30-vendors\neso-data-portal\datasets\system-frequency-data.md`
(page block added, CRLF, 890 lines, all CRLF); mirror `C:\gridflow-wt\fe-neso-sys\vault\neso_data_portal\system-frequency-data.md`
(`cmp` clean). Artefacts: `site\hifi\data\series\neso_data_portal\system_frequency.json`,
`samples\neso_data_portal\system_frequency.json`, `notebooks\neso_data_portal\system_frequency.json` and
`system_frequency-6.png`.

## Status

- `gridflow-build --only neso_data_portal/system_frequency`: passes (after trimming four over-budget fields).
- Detector `detect.mjs --json`: `[]`.
- Rendered page: 0 em dashes, 0 arrows, 0 middle dots; no "locally", "since 20", "live", "now", planning words.
- **Screenshots not taken** (seat ruling: the checker takes them). The PowerShell guard blocked both server starts on
  port 9881 before they ran; no server or background process was started.

## Manifest note (lead)

The lead `system_frequency` is the bronze home: the registry gives it no `record` and no transformer, so it has
**no silver table** (`registry/system-frequency-data.json`, family 0: `"transformer": null`, no `record`). The template
copes: the chart names its silver explicitly (`neso_data_portal/system_frequency_gmt_csv`) and the frame follows the
chart (`artefacts.sample_silver`). The page treats the lead as "Bronze only" in its member well. The manifest is not
wrong as such (the lead must be first in the page set), but the seat should know the lead key has no rows of its own;
`list_datasets()` also lists `system_frequency` while `query()` rejects it (see Defects).

## 1. What one row is, per shape; silver and held

| Member | Row | Body | Silver |
|---|---|---|---|
| `system_frequency` | none: bronze home; every monthly file is captured here | CSV or ZIP | No table; the four typed tables read its bronze (sibling-fed, `generic.py:298`) |
| `system_frequency_dmy_csv` | one second, `dtm` kept as the raw 2014 string (`31/01/2014 23:59:59`), `f` | CSV | **Held**: NESO's descriptions give no zone for the 2014 times, and one October 2014 hour repeats |
| `system_frequency_offset_csv` | one second, `dtm` parsed from `%Y-%m-%d %H:%M:%S %z`, converted to UTC; `f` | CSV, 2015 to 2018 | Eligible |
| `system_frequency_offset_zip` | same as above | ZIP with one CSV (`f 2019 M.csv`), 2019 | Eligible |
| `system_frequency_gmt_zip` | one second, `dtm` naive, typed UTC (alt format `%Y-%m-%d` for date-only midnights); `f` | ZIP with one CSV (`fNew YYYY M.csv`), Jan 2020 to Mar 2022 | Eligible |
| `system_frequency_gmt_csv` | same as above | CSV, Apr 2022 onward | Eligible |

Ledger row (`gridflow\.planning\v0.22-FE-LEDGER.md:131`): 4 typed families eligible; held `system_frequency_dmy_csv`
"(2014 zone unstated)". Key everywhere `(resource_id, dtm)`, `_latest` = `whole_capture` per `resource_id`.

## 2. Clocks (evidence scoped to the rows)

| Claim | Evidence |
|---|---|
| Offset shape labels are UK clock time with an offset | Bronze `f-2015-3.csv` rows 2422801-2422802: `2015-03-29 00:59:59 +0000` then `2015-03-29 02:00:00 +0100` (the 01:00 hour skipped). `f-2015-10.csv`: `01:00:00 +0100` to `01:59:59 +0100`, then `01:00:00 +0000` to `01:59:59 +0000` (hour repeated, offsets differ). |
| Offset shape converted to UTC gives contiguous seconds | Silver: 2015-03-29, 2015-10-25, 2018-03-25, 2018-10-28 (`_offset_csv`), 2019-03-31, 2019-10-27 (`_offset_zip`): each 86,400 rows, 86,400 distinct, max step 1 s |
| GMT shape labels do not follow the UK clock | Bronze `fnew-2023-3.csv`: `2023-03-26 00:59:59`, `01:00:00`, ..., `01:59:59`, `02:00:00` all present (a UK clock skips that hour). The page's eight rows show exactly these seconds. |
| GMT shape stated by NESO | Package notes (catalogue snapshot `20261006T195819Z`): "Time values are all given in Greenwich Mean Time (GMT) starting January 2020." Registry: `zone: "UTC"`. |
| GMT shape contiguous on change days | Silver: 2020-03-29, 2020-10-25, 2021-03-28, 2021-10-31 (`_gmt_zip`), 2022-10-30, 2023-03-26, 2025-03-30, 2025-10-26, 2026-03-29 (`_gmt_csv`): each 86,400 rows, max step 1 s. Notebook cell 3 shows 86,400 for one change day in each typed table. |
| 2014 shape has no stated zone | Registry hold question (unit H-R1); note body "Holds". Not read further (held). |
| `timestamp_utc` = `event_time` = `dtm` in typed tables | Registry `temporal: utc_instant` on `dtm`; the eight sample rows show equality. |
| `published_at` = CKAN `last_modified` of the whole file | Registry `vintage: ckan_last_modified`; sample rows show 2023-04-03 12:24:55 for March 2023, matching the sidecar. |
| Hz | NESO field information for `f`: title "System Frequency (Hz)", unit `Hz` (`gridflow\docs\neso_data_portal\profile\families\system_frequency.json`, `field_info`). |
| Statutory limit | Package notes: "keep the system frequency at 50 Hz, with a statutory limit of 0.5 Hz above or below this value." |
| Workbench times | `query()` filters `timestamp_utc >= ? AND < ?` on UTC day bounds, both ends included (`source.py:401-451`, `_date_range_predicate`), reads `silver_neso_data_portal_<table>_latest`; returns `datetime64[us, Europe/London]`; drops lineage and hive `year`/`month`. Notebook cell 1 converts `dtm` to UTC. |

Cross-check (report only, not on the page): `_offset_zip` lowest reading 48.787 Hz at 2019-08-09 15:53:49 UTC, i.e.
16:53:49 BST, which is the time of the widely reported 9 August 2019 event: consistent with the offset conversion.

## 3. Volume, captures and repeats

All reads lazy (`scan_parquet`, selected columns, aggregates only). Row counts from Parquet metadata.

| Table | Files (captures) | Rows | Captures per resource | Repeated `dtm` in a resource | Distinct `dtm` across table | Null `f` |
|---|---:|---:|---:|---:|---:|---:|
| `_dmy_csv` | 11 | 28,857,600 | 1 | 0 | not read (held) | not read |
| `_offset_csv` | 48 | 126,230,400 | 1 | 0 | 126,230,400 | 0 |
| `_offset_zip` | 12 | 31,536,000 | 1 | 0 | 31,536,000 | 0 |
| `_gmt_zip` | 27 | 70,934,400 | 1 | 0 | 70,934,400 | 0 |
| `_gmt_csv` | 53 | 139,449,600 | 1 | 0 | 139,449,600 | 0 |

One capture per resource (all 2026-10-08), so no truncation and no repeats. `dedup: {on: [dtm], order_by: published_at}`
is set on the chart and frame as a guard (`duplicates_dropped: 0`). Each month spans exactly its UTC month (first and
last `dtm` checked per resource in each table).

## 4. Chart

`system_frequency_gmt_csv`, `f` in Hz, line, every second 13:00:00 to 13:29:59 UTC on 22 December 2023,
unaggregated, 1,800 points (`max_points: 1800`), filtered with `ge`/`lt` on `dtm` like the Elexon `freq` page.
Series: lowest 49.275 Hz at 13:10:11; pre-dip range 49.878 to 50.042 Hz to 13:09:51; two-step fall from 49.88 Hz at
13:09:51 (to 49.644 at 13:09:55, then 49.275 at 13:10:11); below 49.5 Hz for 60 seconds, 13:10:03 to 13:11:02; back
to 50 Hz at 13:21:09; peak 50.134 Hz at 13:26:07. No cause is stated. December 2023's file carries a
`last_modified` of 2026-04-17 (a re-upload); the chart shows the captured copy.

Frame: eight seconds either side of 01:00 and 02:00 UTC on 26 March 2023 (from the March 2023 file), showing the hour
the UK clock skips is present in GMT-shape rows.

Notebook (ran clean, 6 cells, 10 s): rows around the minimum; 86,400 rows that day, 60 seconds below 49.5 Hz
(13:10:03 to 13:11:02); 86,400 rows on one clock-change day in each typed table; the 30-minute plot with a dashed
line at 49.5 Hz.

## Body corrections

None. The body already matches the code and silver on everything I checked (row counts, clocks, vintages, coverage,
ranges, Hz). Only the `page:` block was added.

## Unverified

- What `dtm` marks within the second (instant, start or end; sample or one-second aggregate): NESO does not say;
  the page makes no claim.
- Whether NESO's re-uploads (for example December 2023 on 2026-04-17) changed values: one capture per file exists.
- The raw note's "each monthly file downloaded whole unless its `last_modified` is unchanged" is from
  `iter_members` (`client.py:1659-1720`); not exercised.

## Open questions and template problems

- The page allows three commands; the four typed tables each need a transform. The page shows ingest plus the
  `_gmt_csv` transform, and the raw note says the other three transform the same way by their own keys. The seat may
  prefer a fourth command when the template allows it.
- The lead member has no silver; worth a line in the template docs that a family's frame may come from a member
  through `chart.silver` or `record.select.silver`.
- `sed -i` on the note stripped every CR once (restored to 890/890 CRLF by script before mirroring); the brief's
  warning holds.

## Defects

- **gridflow_models: the workbench serves the held 2014 table, filtered by capture time.**
  `data.neso_data_portal.query("system_frequency_dmy_csv", start, end)` reads
  `silver_neso_data_portal_system_frequency_dmy_csv_latest` with no hold check, and filters `timestamp_utc`, which for
  this table is the capture time. A 2014 window returns 0 rows; a window on 8 October 2026 returns all 28,857,600 held
  rows (DuckDB count, `timestamp_utc` 2026-10-08 11:27:47 to 11:28:21 UTC). Expected: held tables refused or flagged
  by `query()`, as the note's "no consumer path presents it as eligible" intends.
- **gridflow_models: `list_datasets("neso_data_portal")` lists `system_frequency`, which `query()` rejects.** The
  bronze home has no silver relation; `_validate_dataset_for_source` raises "unknown dataset", so `query()` returns an
  empty frame telling the reader to run `list_datasets()`, which names it.
