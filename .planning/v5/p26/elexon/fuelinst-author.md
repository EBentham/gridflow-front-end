# fuelinst: author report

Page: `elexon/fuelinst`, "Five-minute generation by fuel type". Written 2026-09-28.

## Status

- Canonical note: `vault-p26-elexon/30-vendors/elexon/datasets/fuelinst.md` (CRLF kept; vault diff 134+ / 7-).
- Mirror: `p26-elexon/vault/elexon/fuelinst.md`, byte-identical (`cmp` clean after the last edit).
- Artefacts: `site/hifi/data/series/elexon/fuelinst.json` (`spec_origin: vault`, 9 series x 288 points),
  `samples/elexon/fuelinst.json` (`generated_by: gridflow-sample`), `notebooks/elexon/fuelinst.json` + `fuelinst-5.png`
  (run by `scripts/run_notebooks.py`, no errors).
- No staged chart spec or authored override existed for this dataset (nothing to delete).
- `gridflow-build --only elexon/fuelinst`: passes. `detect.mjs --json`: `[]`.

## How it differs from fuelhh (the design choice)

- **Chart:** fuelhh is a week of half-hours. fuelinst shows one GB day at full five-minute grain (288 instants), so the
  within-half-hour steps show. The day is settlement date 20 September, the first day of fuelhh's window, so the
  reader can compare the two charts.
- **Frame:** eight consecutive five-minute `PS` rows around midnight. The timestamp column shows the cadence, and
  00:00 appears twice (once from each daily file), which is the fuelinst-specific gotcha.
- **Prose:** stresses what is different. `timestamp_utc` is the publish time, not the interval start. There is no
  settlement date or period, and no `published_at`. The doubled midnight instant is untrimmed.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Grain "one row per five-minute instant and fuel-type code, per daily file" (facts.grain; scoped because the frame shows 00:00 twice) | `fuelinst.py:105` dedups within one file only |
| Key `(timestamp_utc, fuel_type)` (`record.key`, facts) | `silver/elexon/fuelinst.py:29,105` (`unique(subset=["timestamp_utc","fuel_type"], keep="last")`) |
| `timestamp_utc` is Elexon's publish time, not the interval `startTime` (summary, what_it_is, fields) | `fuelinst.py:61-100`: `publishTime`/`publishDateTime` map to `published_at`, which becomes `timestamp_utc`; `startTime` is used only when no publish field exists. Local bronze: all 80,920 rows have `publishTime` present |
| Silver keeps no settlement date/period and no `published_at` (what_it_is) | `fuelinst.py:115-121` output_cols = timestamp_utc, fuel_type, generation_mw, data_provider, ingested_at |
| Interconnector codes and `PS` are signed (what_it_is, fields, key) | Visible: chart imports band runs -6,343 to 6,023 MW; the eight `PS` rows are -251 to -129 MW |
| Imports sign "checked on FUELHH against demand; Elexon does not state it" (key note) | fuelhh vault note Known issues (gridflow_models RULINGS #542). Scoped to FUELHH on purpose; not re-checked on FUELINST |
| `PS` sign meaning undocumented; `OTHER` undocumented (key notes) | fuelhh note (same vendor codes); no vendor doc in either note |
| No solar code (what_it_is) | Chart key lists all 20 codes present; none is solar |
| Coal and oil 0 MW at every instant here (key note) | Committed series: `coal_oil` min = max = 0.0 over the 288 points |
| Requests: `GET .../datasets/FUELINST?publishDateTimeFrom=...T00:00:00Z&publishDateTimeTo=...T00:00:00Z&page=1` | `endpoints.py:116-120` (PUBLISH_DATETIME, default `from_param`/`to_param`), `endpoints.py:33,40` (pagination on, 24-h chunks), `endpoints.py:267-278` (`%Y-%m-%dT%H:%M:%SZ`), `endpoints.py:312-313` (`page`). Local bronze sidecar `2026/09/20/*.meta.json` shows this exact URL |
| 24-hour publish windows that include both ends, so each midnight instant lands in two daily files; silver does not trim it (raw_feed.note) | `client.py:93-99` (24-h chunks from `--start`), `silver/partition_window.py:3-8` (Elexon publish window CLOSED at both ends, boundary instant written to both partitions), `silver/elexon/_publication_window.py:39-42` (fuelinst exempt from the trim), `fuelinst.py:105` (dedup within one file only). Visible in the eight rows (00:00 twice) |
| Ingest `--end` exclusive; `--start 2026-09-19 --end 2026-09-21` (commands) | `client.py:93-99` `while current < end`; `pipeline/runner.py:479-501` (a bare date is midnight UTC). The chart reads silver days 19 and 20, which need bronze partitions 19 and 20 only (no `PARTITION_SOURCE_OFFSETS`, base default `(0,)` at `silver/base.py:417`) |
| Transform end inclusive (commands) | `pipeline/runner.py:1138` `date_range(start_dt.date(), end_dt.date())` |
| Chart: 288 values published 23:05 UTC 19 Sep to 23:00 UTC 20 Sep, groups summed, 00:00 counted once (caption) | Spec filter `gt 2026-09-19T23:00:00`, `le 2026-09-20T23:00:00`; `dedup {on: [timestamp_utc, fuel_type], order_by: ingested_at}`; series provenance: `rows_matched 5780`, `duplicates_dropped 20`, `rows_used 5760`, `silver_first 23:05Z`, `silver_last 23:00Z` |
| "GB day 20 September", "GB day starts 23:00 UTC" (caption, x_label) | BST in September: the GB day runs 23:00Z to 23:00Z. Publish time is five minutes after `startTime` in the note's vendor bronze sample (02:55 to 03:00), so publish times 23:05Z to 23:00Z cover intervals starting 23:00Z to 22:55Z |
| Alt values: nuclear about 3.3 GW; gas 2.3 to 9.2 GW, peak 18:30; wind 16.2 GW early, 5.4 GW at 19:05; imports -6.3 GW at 04:20 to 6.0 GW at 16:10, crossing zero at 14:05 | Committed series: nuclear 3,321 to 3,346; gas 2,324 (09:35) to 9,165 (18:30); wind 16,176 (19 Sep 23:55) to 5,413 (19:05); imports -6,343 (04:20) to 6,023 (16:10); one sign change at 14:05 |
| Eight rows are `PS` 23:40 to 00:10 UTC with 00:00 from two daily files (record.caption) | `gridflow-sample` output; the two 00:00 rows differ only in `ingested_at`/`available_at` (files 20260919 and 20260920) |
| `query()` reads relation `silver_elexon_fuelinst`, `timestamp_utc >= start 00:00Z AND < end+1 00:00Z`, lineage dropped, duplicates kept (notebook.lead) | gridflow_models `research/handles/source.py:401-449`, `_get_method_registry.py:62-96` (TIMESTAMPTZ half-open); gridflow `schema_manifest.py:121` (date col `timestamp_utc`); no `_latest` view for fuelinst, and the view is plain `read_parquet` (`storage/duckdb.py:445`) |
| "returned in local time" (notebook.lead) | Notebook run without `tz_convert` printed `2026-09-19 01:00:00+01:00` for 00:00Z; no TimeZone is set in `_pandas_client.py`, so DuckDB's session default applies. The first cell converts to UTC |
| plot_alt values | Net INT sum over 19-20 Sep: about -5,600 overnight on the 19th (-5,585 at 03:00, min -5,623 at 01:55), 1,201 at 19:45, -6,343 at 04:20 on the 20th, 6,023 at 16:10 |
| Related: agpt "with solar"; windfor "Elexon's wind forecast" | agpt silver `psr_type` includes `Solar`, `endpoints.py:165` (B1620); `endpoints.py:154` "Wind Generation Forecast" |

## Note-body corrections (canonical note)

1. **Pydantic schema:** it said "Not declared". It is `ElexonFuelInst` (`schemas/elexon.py:87-103`), the `schema_cls` at
   `fuelinst.py:28`.
2. **Point-in-time field:** it said `published_at`. Silver has none: the publish time becomes `timestamp_utc`
   (`fuelinst.py:86-121`).
3. **Silver schema, `timestamp_utc` row:** it said "derived from (settlement_date, settlement_period) via
   settlement_period_to_utc". It comes from `publishTime`, with `startTime` only as a fallback (`fuelinst.py:61-100`).
4. **Silver schema, `ingested_at` row:** it said "Time ingested into bronze". It is the silver transform time
   (`fuelinst.py:107-112`), the same stale fact the pilot found on fuelhh.
5. **Silver sample:** `timestamp_utc` changed from `00:00` to `03:00`, to match the bronze sample's `publishTime` under the code.
6. **Known issues, first bullet:** "derived from `startTime`" became "derived from the publish time".
7. **Known issues, new bullet:** the midnight instant is in two daily files (code citations as above), scoped to
   date-bounded ingests.
8. **Implementation delta:** "No Pydantic schema" replaced with the `ElexonFuelInst` fact.

Left untouched: the Overview's "the half-hour aggregates feed FUELHH" (unverified; nothing on the page repeats it),
`last_verified`, the curl example and the vendor parameter table.

## Screenshots

- **1440, 1024 and 768** (headless Chrome, light): hero scenery, chart, key, frame, guide, notebook preview and related
  are all fully visible.
- **Fixed:** the `imports` band's `tag: net imports` was clipped ("et imports") because the band only starts mid-chart.
  I removed the tag; the key still names the series.
- **390:** headless Chrome lays out wider than 390 (its minimum window width), so those shots look cut off. I re-checked
  at a true 390 in the browser pane:
  - no horizontal overflow (`scrollWidth` 390);
  - the hero, chart and key fit;
  - the frame folds `generation_mw` behind `…`, and unfolds into its own horizontal scroll box;
  - the opened notebook drawer has no clipped elements (checked numerically after pane screenshots wedged);
  - the related list fits.
- **Dark:** the site has no dark theme (no `prefers-color-scheme` or `data-theme` in the assets), so light is the only
  mode.

## Unverified

- Whether a FUELINST value is an instantaneous reading or an average over its five minutes. The page avoids both words.
- The import-positive sign for FUELINST codes specifically (checked on FUELHH only; the key note says so).
- Whether publish time is always `startTime` + 5 min. The page does not state it as a rule. The body cites only the
  vendor bronze sample; every local bronze row agrees, but that is not stated.

## Open questions

- The doubled midnight rows mean `data.elexon.query("fuelinst", ...)` returns duplicate keys for every midnight inside
  the range. Should gridflow trim fuelinst, or add a `_latest` view? That is an upstream gridflow issue, not a page issue.
- DuckDB hands `TIMESTAMPTZ` back in the machine's local zone. That affects every page whose notebook plots
  `timestamp_utc` (fuelhh's wind plot included). A gridflow_models-level `SET TimeZone='UTC'` may be wanted.

## Template notes (not worked around)

- A one-day chart starting at exactly 00:00 UTC would get a second day label ("21 Sep") centred on the right edge
  (`chart_svg.py:204-214`), where it would likely clip. I avoided it by choosing the GB day; a UTC-midnight one-day
  window on another page would hit it.
- A time chart with a one-day window gets no hour ticks, only the day label.

## Process note

- I ran one read-only `git diff --stat` in the vault worktree to confirm the CRLF edit was not a whole-file rewrite.
  No other git commands.
