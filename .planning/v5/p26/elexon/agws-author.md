# agws: author report

Page `elexon/agws`, "Wind and solar generation". Writer: Opus 5.5, 2026-09-28.

- Canonical note: vault worktree `30-vendors/elexon/datasets/agws.md` (CRLF kept, 280 lines).
- Mirror: `vault/elexon/agws.md` in the front-end worktree, byte-identical (`cmp` clean after the last edit).
- Artefacts: `site/hifi/data/series/elexon/agws.json` (gridflow-distil, `spec_origin: vault`, 3 series x 336 points),
  `site/hifi/data/samples/elexon/agws.json` (gridflow-sample), `site/hifi/data/notebooks/elexon/agws.json` and
  `agws-5.png` (run_notebooks.py, 5 cells, 1 image, no errors).
- No staged chart spec and no authored override existed for agws, so there was nothing to delete.

## Build and detector

BUILD_STATUS

## Evidence

Code paths are under `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow\src\gridflow\`. Polars reads were over
`C:\gridflow-data\silver\elexon\agws\`, read only.

| Claim (field) | Evidence |
|---|---|
| Vendor dataset AGWS, ENTSO-E B1630 (`facts.vendor`, `what_it_is`) | `connectors/elexon/endpoints.py:168-172`: path `/datasets/AGWS`, description "Actual or Estimated Wind and Solar Power Generation (B1630)". |
| Grain: one row per settlement period and production type; key `settlement_date, settlement_period, psr_type` (`facts.grain`, `record.key`) | `silver/elexon/agws.py:25` `ENTITY_KEY_COLUMNS`; dedup `agws.py:114-117` on the same three columns, `keep="last"`. Settlement dates 1 to 25 Sep 2026: 48 periods x 3 types per date, no duplicate keys. |
| Every 30 minutes (`facts.cadence`) | Settlement periods are half-hours (`utils/time.py:28-42`); silver shows one document per period, `published_at` 30 minutes apart. |
| Types sent as labels `Solar`, `Wind Offshore`, `Wind Onshore` (`what_it_is`, `record.fields.psr_type`) | `agws.py:61` maps `psrType` to `psr_type`, cast to Utf8 unchanged (`agws.py:83`). Polars over all agws silver: exactly these three labels, paired with business types `Solar generation` / `Wind generation`. Schema docstring `schemas/elexon.py:558-562` "limited to wind/solar PSR types". |
| No column says whether a value is actual or estimated (`what_it_is`) | Silver output columns `agws.py:126-138`; raw record keys in bronze `2026/09/19/raw_*.json`: `businessType, dataset, documentId, documentRevisionNumber, psrType, publishTime, quantity, settlementDate, settlementPeriod, startTime`. No flag in either. |
| Each period in the rows was published 2 h 30 min after it began (`what_it_is`) | Sample rows: period 1 23:00 -> 01:30:01, 14 05:30 -> 08:00:01, 27 12:00 -> 14:30:09, 46 21:30 -> 00:00:15 (next day). Scoped to "the rows below". |
| Request URL (`raw_feed.requests`) | `endpoints.py:300-313` (`publishDateTimeFrom/To` via `_to_utc_z`, plus `page`); `client.py:93-99` 24-hour chunks; bronze sidecar `bronze/elexon/agws/2026/09/19/raw_20260926T183056Z_010ce8de.meta.json` `request_params`: `publishDateTimeFrom=2026-09-19T00:00:00Z`, `publishDateTimeTo=2026-09-20T00:00:00Z`, `page=1`. |
| Bronze filed by publish day (`raw_feed.note`) | `client.py:314` `data_date = start.date()` of the publish chunk; transformer reads one bronze day (`agws.py:27-35`) and silver writes per target date (`silver/base.py:1067,1191`). Silver file `agws_20260926.parquet` holds 25 Sep periods 46-48 and 26 Sep periods 1-45. |
| Period 46 published after midnight UTC, so both commands run a day longer (`raw_feed.note`, `commands`) | Sample row: period 46 of 2026-09-25, `published_at` 2026-09-26 00:00:15 UTC. In September silver every date's periods 46-48 sit in the next day's file. |
| Ingest `--start 2026-09-19 --end 2026-09-27`, end exclusive | Publish-datetime loop `client.py:93-99` (`while current < end`); CLI dates parsed as UTC instants (`cli.py:1237-1254` -> `pipeline/runner.py` `resolve_dates`). Fetches publish days 19 to 26, which cover settlement dates 19 (period 1 published 01:30 on the 19th) to 25 (periods 46-48 published on the 26th). No `PARTITION_SOURCE_OFFSETS` on the transformer (base default `(0,)`, `silver/base.py:417`). |
| Transform `--start 2026-09-19 --end 2026-09-26`, inclusive, by publish day | Transformer reads the bronze day it is given (`agws.py:27-35`); the transform end is an inclusive date per the brief. |
| `timestamp_utc` computed from settlement date and period (`record.fields`) | `agws.py:86-95` calls `settlement_period_to_utc`; `utils/time.py:41-42` period 1 = local midnight in UTC. Matches bronze `startTime` (period 45 of 19 Sep: `startTime` 21:00Z, silver 21:00 UTC). |
| `settlement_date` is the vendor label as sent | `agws.py:58,80` rename and cast `settlementDate` to Date. |
| Period range 1 to 48, 46 or 50 on clock-change days | Schema `settlement_period: int = Field(ge=1, le=50)` (`schemas/elexon.py:565`); `utils/time.py:28-35`. |
| `generation_mw` from `quantity` | `agws.py:62,82`. |
| `business_type`, `document_id`, `document_revision`, `published_at` as sent | `agws.py:59-65`; `published_at` parsed to UTC `agws.py:99-104`. |
| Two rows of each period share one document (`record.fields.document_id`) | Sample rows: ids `...0925260130`, `...0925260800`, `...0925261430`, `...0926260000`, two rows each. Scoped "here". |
| Business types differ for solar and wind (`record.fields.business_type`) | Sample rows: `Solar generation` and `Wind generation`. Scoped "here". |
| Notebook lead: relation `silver_elexon_agws`, filtered on `settlement_date`, both ends included, lineage dropped | `silver/schema_manifest.py:113` `("elexon", "agws"): "settlement_date"`; no agws entry in `silver/latest_views.py`, so the base view; gridflow_models `research/handles/source.py:401-451` (inclusive start/end, `EXCLUDE` of bitemporal columns). Notebook output starts at settlement date 2026-09-19 with no lineage columns. |
| Notebook `needs`: 19 to 26 September 2026 | Same publish days as the ingest command (end 27 exclusive). |
| Chart: silver `elexon/agws`, MW, settlement dates 19 to 25 Sep 2026, one value per type, stacked (`chart_view.caption`) | `page.chart`: filter `settlement_date` ge 2026-09-19 and le 2026-09-25, dedup on the key by `published_at`, `group_map` one type per series, `aggregation: sum` over a single row per series and half-hour. distil: "3 series x 336 points, 1008 rows used". |
| Alt numbers | Committed series: onshore 488 to 8,767; offshore 421 to 11,476; solar 0 to 10,099, daily peaks 6,158 (19th) to 10,099 (20th); wind combined max 19,115 (19th 01:00 UTC), min 1,598 (22nd 17:00 UTC); total 2,015 to 25,051 MW. Solar is 0.0 at every point from 20:00 to 03:59 UTC. |
| `x_label` "each starts at 23:00 UTC" | BST window; series `x` starts 2026-09-18T23:00:00Z. |
| Palette | `solar` default chartreuse; `offshore` horizon (the wind role); `onshore` unpainted `hatch-lines` because DESIGN.md "Colour" gives wind one colour and "no other series colours" (petrol is nuclear). No khaki. No signed values in the window (min 0.0). |
| Key note "FUELHH has no solar code" | fuelhh note (vault) Overview and the fuelhh `page.chart.group_map`: no solar code; Bobbo's ruling 2026-08-31 recorded there. |
| `plot_alt` | `agws-5.png` inspected: offshore about 11,500 MW early on the 19th, onshore about 8,800 MW that day; UTC day 22: offshore max 2,814, onshore max 3,392 (series); solar daily peaks 6,158 to 10,099, 0 overnight. |
| Related: `agpt` every production type | agpt page and silver: 11 types including `Solar`, `Wind Offshore`, `Wind Onshore`. |
| Related: `windfor` is Elexon's wind forecast | `endpoints.py` `"windfor"`: description "Wind Generation Forecast". |
| Related: `fuelhh` has one wind code and no solar | fuelhh `page.chart.group_map` (`WIND` only) and note Overview. |
| Related: ENTSO-E `wind_solar_forecast` covers the same three types as B-codes | `silver/entsoe/wind_solar_forecast.py:23-24` "B16 = Solar, B18 = Wind Offshore, B19 = Wind Onshore". |

## Note-body corrections (canonical note)

1. Silver schema table, `ingested_at`: "Time ingested into bronze" was wrong. The transformer stamps
   `datetime.now(UTC)` at transform time (`silver/elexon/agws.py:119-123`). Row now says so, with the cite.
2. Silver sample, `timestamp_utc`: `2026-05-06T01:30:00+00:00` for period 4 of a BST day was an hour late.
   Period 1 starts at local midnight (23:00 UTC the day before), so period 4 starts 00:30 UTC
   (`utils/time.py:28-42`); the note's own bronze sample has `startTime` 00:30Z. Fixed, with an inline comment citing
   the function.
3. Known issues, publish-day partitioning: the 2026-07-30 reading ("`agws_20260724.parquet` held only periods 41-48",
   "about 30-40 min publish lag") no longer matches silver (re-transformed 2026-09-27). The file now holds periods 1-45
   of 24 July plus 46-48 of 23 July, and every September row has `published_at - timestamp_utc` = 150 minutes. Replaced
   that span only, citing `endpoints.py:168-172` and `client.py:314`; the surrounding advice (filter on
   `settlement_date` across the glob) is unchanged.

Left alone: the curl example (correct for the vendor), the `Dedup key` line (true within one publish day; see open
questions), the schema table's missing lineage columns (a matrix-wide pattern, not an agws error), `last_verified`.

## Not verified

- What the `Solar` figure covers (transmission-metered only, or an estimate including embedded solar). Not in code or
  the note; the page makes no claim about it. The note's existing TODO stands.
- Which values are actual and which estimated. The feed carries no flag; the page says so and nothing more.
- The 150-minute publish lag is measured on September 2026 rows only. The page scopes it to the rows shown; the vault
  body states it as measured.

## Open questions

- Silver dedup is per publish day (`agws.py:114-117`), so a key revised on a later day appears in two files. Across
  all local agws silver 531 keys appear twice (all in 2022 to April 2026; document revisions 2 and 3). The chart spec
  dedups by `published_at`; `query()` in the notebook does not. None in the charted week. Worth a note-body line or a
  `_latest` view later; out of scope here.
- `keep="last"` within a day follows sorted bronze filenames, which start with the fetch timestamp, so a later fetch
  wins; two identical bronze files exist for 19 Sep (same `body_sha256`), harmless.

## Template problems

TEMPLATE_NOTES
