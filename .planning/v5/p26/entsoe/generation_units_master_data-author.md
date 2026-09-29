# Author report: entsoe/generation_units_master_data (production unit register)

Writer: Opus 5.5 · high, 2026-09-29. Screenshot port 9826 (CDP; `file://` URL, no server started).

## Status

- **Canonical note:** `vault-p26-entsoe/30-vendors/entsoe/datasets/generation_units_master_data.md`, with the `page:` block and body corrections. It keeps CRLF line endings; the vault diff is surgical.
- **Mirror:** `p26-entsoe/vault/entsoe/generation_units_master_data.md`, a byte-for-byte copy (`cmp` clean).
  - The old mirror was LF, so the mirror's git diff shows a whole-file line-ending change. That is expected; don't "fix" it.
- **Artefacts:** all from real silver.
  - `site/hifi/data/series/entsoe/generation_units_master_data.json`: `spec_origin: vault`, 1 series × 8 bars, 660 rows used.
  - `site/hifi/data/samples/entsoe/generation_units_master_data.json`: 8 rows, 11 columns.
  - `site/hifi/data/notebooks/entsoe/generation_units_master_data.json`: 5 cells, no errors, no images.
- **Leftovers:** no staged chart spec or authored override existed for this dataset.
- **Build:** `gridflow-build --only entsoe/generation_units_master_data` exits 0. The "error(s) on pages not rendered by --only" belong to other pages.
- **Detector:** one finding, `em-dash-overuse`, which is advisory. It counts the `--` padding in the EIC codes (the ruling #39 accepted case).
  - The rendered page has 0 real em dashes, 0 `→` and 0 middots.
- **Screenshots:** 1440, 1024, 768 and 390, light and dark. No horizontal overflow at any width.
  - The site has no `prefers-color-scheme` rule in any stylesheet, so dark renders the same as light.
  - Two bar labels were clipped at 390 and have been fixed (see "Template problems").
  - Chart text boxes were measured numerically at every width; nothing now falls outside the viewport.

## What the dates mean, what a row is (the hard questions)

- **One row = one production unit (A95, B11), per zone, per requested date.**
  - The parser emits one record per `TimeSeries` (`parsers.py:681-719`).
  - The `TimeSeries` counts in bronze equal the silver rows exactly: 657 for the 2026-08-01 request and 660 for the 2026-09-08 request, so nothing is collapsed.
  - Nested `GeneratingUnit_PowerSystemResources` are never emitted: the fallback pass matches only the exact tags `MktGeneratingUnit|MktGenerationUnit|GeneratingUnit|ProductionUnit` (`parsers.py:721-750`).
- **1,317 rows = two copies of the register.**
  - Dedup `(area_code, unit_mrid)` runs within one transform (`generation_units_master_data.py:68-69`).
  - Each requested date writes its own file (`year=2026/month=08/..._20260801.parquet` and `month=09/..._20260908.parquet`).
  - 657 `(area, unit)` keys appear in both files. Across the table the key is `(event_time, area_code, unit_mrid)`.
  - `event_time` is the transform's target date, which is the requested date: this transformer has no `timestamp_utc`, so it takes the fallback at `silver/base.py:2221-2231`.
  - No `unit_mrid` appears in more than one zone.
- **`implementation_datetime_utc` is not a commissioning date. Its vendor meaning is undocumented.** It is the per-unit `implementation_DateAndOrTime.date` as 00:00 UTC (`parsers.py:694-701`, `_parse_utc` at `:96-104`). The evidence:
  - **BE `EDF Luminus Seraing TGV` (`22W201806271---D`) changed between the two requests.**
    - The 2026-08-01 response dates it 2018-10-14, with `nominalP` 470 MW and three generating units (GT1, GT2, SERAING TV).
    - The 2026-09-08 response dates it 2025-11-01, with 300 MW and two generating units (SERAING TV gone).
    - So the date moved when the record changed. Both rows are in the page's eight rows.
  - **Shared dates look like placeholders.** In the 2026-09-08 request, 131 units share 2000-01-01 and 60 DE-LU units share 2018-10-01. The CATTENOM 3 rows in the frame show 2000-01-01.
  - **Rows can postdate the request.** In the frame, `Nordseecluster A` (DE-LU) is dated 2026-09-12 in the 2026-09-08 request, and `KALLO BESS` (BE) is dated 2027-01-01 in both requests.
  - **Range:** 1960-01-01 (FR `LOGIS NEUF 2`) to 2027-01-01. The note body said "1990"; corrected.
  - The page states only "undocumented, but not commissioning", with the Seraing move as the visible reason. The page never plots or trends the dates.
- **Areas:** six bidding zones, gridflow's `DEFAULT_ZONES` (`endpoints.py:395`): GB, FR, NL, BE, DE-LU and IE-SEM. The notebook's `value_counts()` output shows the per-zone counts for the 8 September request (230, 175, 135, 52, 35, 33).
- **PSR types:** 18 codes in the 2026-09-08 request (B01 to B06, B08, B10 to B14, B16 to B20, B25). There are no empty `production_type` or `unit_name` values and no null dates in either request.
- **Capacity:** the XML carries `nominalIP_PowerSystemResources.nominalP` (MAW) per unit, plus per generating unit, but silver maps none of it. That is why the chart is a **count**, not installed capacity.
  - Summing is impossible here and would anyway be the job of `installed_capacity_units` (its `unit_mrid` values all match: 639 of 639).
  - No size threshold is visible: 139 of the 660 units have `nominalP` under 100 MW. The page states no threshold.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Vendor A95 / B11, one request per zone, `BiddingZone_Domain`, single date param (facts.vendor, raw_feed) | `connectors/entsoe/endpoints.py:119-126`; `client.py:139-157,287-289`; the bronze `.meta.json` `request_url` gives param order `documentType, Implementation_DateAndOrTime, BiddingZone_Domain, BusinessType, securityToken` |
| `sources.yaml` schedules it weekly (facts.cadence) | `gridflow/config/sources.yaml:270-273` (`schedule: "weekly"`, `max_query_days: 365`) |
| Ingest sends only `--start`'s date; `--end` is accepted but unused by the request (it defaults to now if omitted), so `--end 2026-09-09` is harmless (commands, raw_feed.note) | `client.py:152-157` (date_param builds unit tasks once, no day chunking) and `:287-289` (`data_date = period_start.date()`); `runner.resolve_dates` `pipeline/runner.py:479-501` |
| Transform `--end` inclusive; writes one file per requested date (raw_feed.note) | bronze partition = `data_date` (meta `data_date: 2026-09-08`); silver files `_20260801` and `_20260908` |
| Grain / key `(event_time, area_code, unit_mrid)` | `generation_units_master_data.py:68-69`; `silver/base.py:2203-2231` (target-date fallback); Polars: 0 duplicate keys within a file, 657 across files |
| `unit_mrid` from `registeredResource.mRID`, rows without it dropped (fields) | `parsers.py:702-703`; `generation_units_master_data.py:58,68` |
| `area_code` from the TimeSeries' `biddingZone_Domain.mRID` (fields) | `parsers.py:692-693` |
| `unit_name` empty string when absent (fields) | `generation_units_master_data.py:59` (`fill_null("")`); schema default `""` `schemas/entsoe.py:289` |
| `production_type` is the first `psrType` (fields) | `parsers.py:706`; in the XML the unit's `MktPSRType/psrType` precedes the nested `generatingUnit_PSRType.psrType` |
| Date as 00:00 UTC (fields) | `_parse_utc` `parsers.py:96-104` (`%Y-%m-%d` + UTC); the rows show `00:00:00 UTC` |
| "not commissioning; one unit's moved from 2018 to 2025 between two requests" (what_it_is, caption) | Bronze `2026/08/01/raw_20260816T134743Z_75c225d8.xml` against `2026/09/08/raw_20260915T201337Z_5e25323d.xml`, `22W201806271---D`; both rows in the eight |
| `query()` filters on `implementation_datetime_utc` (notebook.lead) | gridflow `silver/schema_manifest.py:166`; gridflow_models `research/handles/source.py:401-446` |
| Relation `silver_entsoe_generation_units_master_data` and the `event_time` filter work in `data.sql` | Notebook run 2026-09-29: cell 5 `value_counts` totals 660 (230+175+135+52+35+33), so exactly one request |
| Chart values 175, 172, 106, 80, 70, 27, 21, 9 (alt) | Committed series `values`; the Polars pivot of the 2026-09-08 request per code: B04 175; B18+B19 82+90; B11+B12 77+29; B02+B03+B05+B06+B08 8+3+40+26+3; B14 70; B10 27; B01+B13+B16+B17+B25 7+1+5+4+4; B20 9 |
| "fetched 15 September" (caption) | Meta `fetched_at` 2026-09-15T20:13:34Z to 20:13:39Z for all six 2026-09-08 files |
| Related: same `unit_mrid` (installed_capacity_units, actual_generation_units, outages_production) | Silver column `unit_mrid` in all three; overlap with the 2026-09-08 register: 639/639, 174/175, 45/46 |
| Related: Elexon silver shares no key (how_used, related; worded without prescribing a name match, since naming conventions differ, e.g. ENTSO-E `ABRBO` against Elexon `ABRBO-1`) | `bmunits_reference` silver has `bm_unit_id` and `national_grid_bm_unit`, and its bronze `eic` is not mapped (vault note there); ENTSO-E `unit_mrid` is a W-code EIC |
| PSR code meanings in key notes | ENTSO-E code list (standard); **not re-fetched this session** (the vendor pages returned 403/400). Corroborated by unit names: B08 are Edenderry, West Offaly, Lanesboro (peat); B13 RANCE (tidal); B25 are the BESS units; B10 includes Turlough Hill and Waldeck II; B02 includes Neurath and Niederaußem; B14 is Doel, Tihange, Cattenom; B03 includes Hamborn and Huckingen (steelworks gas) |

## Body corrections made (canonical note, each dated 2026-09-29)

1. **Bronze path** was `raw_<uuid>.xml`. It is now `raw_<YYYYMMDDTHHMMSSZ>_<sha256[:8]>.xml` plus `.meta.json`; the date folder is the requested date (`bronze/writer.py:33-57,85`). Granularity is now "per (zone, requested date)".
2. **Dedup key:** added that the dedup runs within one transform, that each request is its own file, and that the table key is `(event_time, area_code, unit_mrid)` (`generation_units_master_data.py:68-69`, `base.py:2221-2231`).
3. **Point-in-time field:** added that gridflow_models `query()` filters on it (`schema_manifest.py:166`), so `query()` selects by record date across requests.
4. **`ingested_at`:** was "optional". It is now "transform time, `datetime.now(UTC)`, same on every row" (`generation_units_master_data.py:71-75`).
5. **"as far back as 1990"** is now "1960", citing FR `LOGIS NEUF 2` in the bronze of the 2026-09-08 request.
6. **Added gotchas:**
   - the date is not commissioning and its meaning is undocumented (the Seraing, placeholder and future-date evidence);
   - the XML carries `nominalP`, voltage, generating units, control area and provider, which silver drops;
   - no size threshold is visible (139 of 660 under 100 MW).
7. **Modelling notes:** "Asset commissioning timeline, `implementation_datetime_utc` for new-build curves" is struck through and marked wrong.

The curl example and the API table are unchanged: they are right for the vendor.

## Not verified

- **PSR code meanings** against a vendor fetch. Both `transparency.entsoe.eu/.../Guide.html` and the Zendesk code list refused (400/403). The meanings rest on the standard list plus the unit-name corroboration above.
- **What `Implementation_DateAndOrTime` (the request parameter) filters.** Units dated after the requested date come back, and the 2026-08-01 request (fetched 2026-08-16) returned Seraing's 2018 version while the 2026-09-08 request returned the 2025-11-01 version. Whether that is the request date or the registry changing between fetches is undocumented. The page makes no claim about it.
- **Whether a unit with several `MktPSRType` blocks exists in these responses** (175 `MktPSRType` for 175 `TimeSeries` in FR). This was not checked for every zone; the parser would keep the first.

## Open questions (for the seat)

1. **The key includes a lineage column.** `event_time` is in `record.key` (the hero Key fact and the frame's key square) because it is the only thing that tells the two requests apart. The guide's "Identifies a row" lists only `area_code` and `unit_mrid`, since pipeline columns get no line; the caption explains `event_time`. Accept this, or keep the frame to one request? Single-request rows would lose the Seraing evidence that backs the "not commissioning" line.
2. **"Smaller types" bar label.** A descriptive label ("Biomass, solar, waste, storage") clipped at 390. The key note lists all five codes and names. Is this acceptable?

## Template problems (seat's; not worked around)

1. **The bar chart's label column is fixed width at 390 (about 17 characters).** Longer labels spill left past the SVG. `overflow` is visible, but beyond the viewport they are cut: "Biomass, solar, storage" measured left = −7 px.
   - I shortened my labels.
   - "Hydro, not pumped" sits at 13 px against the SVG's 16 px, fully on screen.
   - Suggest sizing the label column to the longest label, or wrapping.
2. **A key column that is a lineage column** gets the key square and the hero Key entry but no guide line (`build.py:1110-1111`: pipeline columns are excluded from `guided`). Suggest letting a key lineage column carry a `record.fields` line.
3. **Raw-feed URL wrapping at 390** splits `2026-09-08` mid-token (`=2` / `026-09-08`), splits the EIC padding, and leaves a blank line before `&Implementation_DateAndOrTime`. Cosmetic; nothing is lost.
4. **The notebook filename clips at 390.** This is the known seat item; left alone.
5. **No dark scheme exists** in any stylesheet, so the "light and dark" check is a single check.

## Defects (pasteable)

- **[gridflow] A95 silver drops capacity and structure.**
  - `parse_generation_units_master_data_xml` (`connectors/entsoe/parsers.py:641-719`) maps only area, EIC, name, first PSR type and date.
  - The XML also carries, per unit, `nominalIP_PowerSystemResources.nominalP` (MW), `production_PowerSystemResources.highVoltageLimit` (kV), `ControlArea_Domain`, `Provider_MarketParticipant` and nested `GeneratingUnit_PowerSystemResources` (EIC, name, `nominalP`, PSR type).
  - Consumers must join `installed_capacity_units` for MW.
  - Evidence: bronze `2026/09/08/*.xml`: 660 `nominalIP...nominalP` and 243+ generating-unit blocks in FR alone. Severity: gap (M).
- **[gridflow] The silver register accumulates one full copy per requested date, and `query()` reads it by record date.**
  - Each transform writes `_YYYYMMDD.parquet` (`generation_units_master_data.py`). The only snapshot identifier is the lineage `event_time` (the `base.py:2221-2231` fallback).
  - gridflow_models `query()` filters on `implementation_datetime_utc` (`schema_manifest.py:166`), so `query("generation_units_master_data", s, e)` returns units whose *record date* falls in the window, duplicated across every request held. That is misleading for a register.
  - Fix options: a `requested_date` vendor-level column, a latest-snapshot view, or a manifest date column of `event_time`.
  - Evidence: 1,317 rows = 657 + 660 with 657 repeated keys. Severity: silent-misread (M).
- **[gridflow] The parser's document-level defaults come from the whole tree.**
  - The first loop (`parsers.py:661-677`) walks `root.iter()`, so the "document" `area_code` and `implementation_datetime` defaults end up as the *last TimeSeries'* values.
  - This is harmless today because every TimeSeries carries its own. A TimeSeries missing either would silently inherit another unit's zone or date.
  - Severity: latent (L).
- **[vault, fixed in this note]** The note claimed dates reach back to "1990" (the real minimum is 1960-01-01) and listed a "commissioning timeline" use (wrong). Both are corrected with evidence.
- **[research unit, named unknowns]**
  - (a) The vendor meaning of the per-unit `implementation_DateAndOrTime.date`.
  - (b) What the `Implementation_DateAndOrTime` request parameter filters: rows dated after it are returned, and whether a fetch-time registry change or the parameter explains Seraing's 2018 to 2025 switch.
  - (c) The PSR code list, to cite from the vendor.
  - Disposition: the page states only "undocumented, not commissioning".
