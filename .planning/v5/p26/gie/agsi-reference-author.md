# agsi-reference (GIE AGSI+ operator and facility register): writer report

Family `agsi-reference`, lead `about_listing`, member `about_summary`. Writer port 9852.

## Status

- `page:` block written on the lead's canonical note. Body corrections made on both notes. Both notes mirrored byte for byte (CRLF kept).
- Series (`gridflow-distil`) and sample (`gridflow-sample`) written from real silver. Nothing is committed; the seat commits.
- **Notebook: done** (update, after the seat refreshed the views with `runner.refresh_views`). `run_notebooks.py --dataset gie/about_listing` ran 6 cells in 9.2 s with no errors. The outputs match the expected counts:
  - `.head()`: the first five operators by `entity_code`;
  - `entity_level`: facility 121, company 64 (185 rows);
  - `entity_type`: SSO 64, ASF 50, DSR 48, ASR 13, NaN 5, GRP 4, SRC 1.
- **Build: green.** `gridflow-build --only gie/about_listing` wrote `data-sources/gie/agsi-reference.html`; the only warnings are the existing "no Pydantic class" content warnings for other GIE members.
- **Detector: `[]`.** No findings, so no advisories to accept.
- **Screenshots.**
  - **How.** A static server on port 9852 (stopped afterwards) and headless Chrome over CDP with true device-width viewports (`scratchpad\agref_shot.mjs`, profile under `scratchpad\agref-cdp-*`, each run wrapped in `timeout 60`).
  - **Widths.** 1440, 1024, 768 and 390, full page. No horizontal overflow: `scrollWidth` equals `innerWidth` at every width.
  - **Nothing clipped or overlapping.** Checked the hero (turbines, gas terminal and offshore-platform labels), the chart bars, the labels ("United Kingdom" and "Czech Republic" at 390) and the key notes (reflowing to 1, 2 or 3 columns), the raw feed (URLs and commands wrap), the frame (folds behind `…` at every width; at 390 only `entity_level` and `entity_code` show before the fold), the column guide, the notebook cells (the SQL wraps at 390), related links and the corner labels.
  - **Dark mode.** The site has no dark theme: no `prefers-color-scheme` or `data-theme` rules in `theme.css` or `tokens.css`. Emulated dark captures at 1440 and 390 render identically to light.
  - Files: `scratchpad\agref-shots\page-<width>[-dark].png` and cropped `c-*.png`.
- **Notebook scratch copy.** `scratchpad\agref-wh\gridflow.duckdb` from the earlier attempt was not used for the final notebook, which ran against the refreshed warehouse; I left it in place.

## Blocker (resolved: the seat refreshed the views)

- **Symptom.** The warehouse holds `silver_gie_agsi_storage`, `_storage_reports`, `_unavailability` and `silver_gie_alsi_lng`, but no `silver_gie_agsi_about_listing` or `silver_gie_agsi_about_summary`.
- **Cause.** The warehouse file was last written 2026-09-27 00:23 UTC, and these silver files 00:31 UTC, so no view refresh followed that transform.
- **Why it blocks.** `data.sql()`, `query()` and `tail()` all read the warehouse view (`gridflow_models/research/handles/source.py:273-282`, `data.py:255-270`).
- **Workarounds tried.** A scratch copy of the warehouse with the two views registered works. But `gridflow_models` takes the warehouse from `configs/settings.yaml` (`gridflow_data_dir: "C:/gridflow-data"`), passed as constructor arguments that beat `GRIDFLOW_MODELS_GRIDFLOW_DATA_DIR` (`config/settings.py:156-160`). No process-scoped override exists, and I did not edit any config.
- **Recommended ruling: yes.** Run gridflow's view refresh on the warehouse, from the gridflow repo, while no other agent's notebook kernel holds the file: `uv run python -c "from gridflow.config.settings import load_settings; from gridflow.pipeline import runner; runner.refresh_views(load_settings())"` (`pipeline/runner.py:777-788`; it re-registers views over the existing parquet and changes no data). Don't use `gridflow init`: it runs `init_catalogue` (`cli.py:1209-1224`), which does more than refresh views. Then run:
  - `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow_models\.venv\Scripts\python.exe scripts/run_notebooks.py --dataset gie/about_listing`
  - `uv run --system-certs --extra build gridflow-build --only gie/about_listing`
  - the detector
  - screenshots at 1440, 1024, 768 and 390
- **Expected outputs.** I verified the cells' SQL against an in-memory view over the same parquet with gridflow's DDL. The query returns 185 rows (1,665 without the newest-day filter). `entity_level` counts are facility 121 and company 64. `entity_type` counts are SSO 64, ASF 50, DSR 48, ASR 13, NaN 5, GRP 4, SRC 1.
- **Scratch copy.** `scratchpad\agref-wh\gridflow.duckdb` holds the two views registered. It was not used for any committed artefact, and I left it in place.

## What one row is, and how the members differ

| Question | Answer | Evidence |
|---|---|---|
| What is a row? | One EIC: either a storage system operator (`entity_level = company`, `entity_type = SSO`) or a facility listing (`entity_level = facility`). Not a country. | `silver/gie/agsi.py:462-489` (listing), `579-634` (summary); silver: 64 company and 121 facility rows per partition in both members |
| Are the two members the same rows? | Same 185 EICs in both, in two shapes. The listing is flat, from `show=listing`; the summary is a nested tree `SSO > Europe/Non-EU > <Country> > [companies]`. | Polars set difference of `entity_code` between members: empty both ways |
| Where do they differ? | `entity_name`: listing = `short_name` (else `name`), summary = full `name` (65 EICs differ). Summary adds `short_name`, `country_name`, operational dates, `aggregate_code/name` (EU/NE), operator links and `has_image`. Blank facility `type`: listing null, summary `""`. UK rows: listing kept `GB`, summary kept `GB*` (9 EICs). | `endpoints.py:265,281`; `agsi.py:590-632`; join of the two members on `entity_code` |
| Why 1,665 rows "on one date"? | 9 silver partitions (19 to 27 Sep), each an identical copy of 185 rows (185 x 9 = 1,665). They all come from one bronze capture fetched 2026-09-27 00:31 UTC, filed under `2026/09/20`. `fallback_to_latest_partition = True` makes each transform day with no bronze read the newest bronze folder. | `agsi.py:309,402-428`; bronze `.meta.json` (`fetched_at` 2026-09-27T00:31:37Z, `data_date` 2026-09-20); partition equality check (lineage dropped): all equal |
| Natural key | `entity_code` (the EIC) alone, `keep="last"`. The dedup subset is whichever of `id, url, turl, entity_code, eic` exist, and only `entity_code` does. | `agsi.py:387-391` |
| EIC codes | Company EICs (`21X...`, `25X...`, `37X...`, `55X...`); facility EICs (`21W...`, `25W...`, `37W...`, `55W...`), plus GIE placeholders such as `PRIOR_OSM_000001` and `PRIOR_EWE_000001`. Some contain `---` (`25X-GSALLC-----E`, `16ZAS01--------8`), so none of those appear in the front matter. | silver; `page_fields.py:379-380` rejects `---` in any parsed page string, so `\x2D` escapes do not help |
| Vendor EICs repeat | The 27 Sep payload has 71 company entries (64 EICs) and 127 facility entries (121 EICs). The 7 repeated company EICs are SEFE (AT, DE), Uniper (AT, DE), EWE (DE, NL), and 4 UK operators (`GB`, `GB*`). The 6 repeated facility EICs are 5 UK facilities (`GB`, `GB*`) and `21W000000000095N` (Edison Stoccaggio group to 2025-03-01, then VGS HUB2). | bronze JSON parsed in Python |

## Evidence table (page claims)

| Claim (field) | Evidence |
|---|---|
| title, summary: register of AGSI+ storage operators and facilities with EIC, country, parent | silver columns; `endpoints.py:257-295` |
| facts.vendor: `/api/about`; `show=listing` gives the flat form | `endpoints.py:139-153` (`default_params={"show": "listing"}`); bronze meta `request_url` |
| facts.cadence: whole-register snapshot per call; `sources.yaml` says weekly | `client.py:258-265` (`paginated=False`, one request); `config/sources.yaml` `about_listing: schedule: "weekly"` |
| facts.grain: one row per EIC, `entity_level` says which | dedup `agsi.py:387-391`; rows built `agsi.py:465-488` |
| what_it_is: EICs repeat in the payload (operator under two countries, UK before and after Brexit); silver keeps one row per EIC | bronze parse (above); vendor's own `(Post-Brexit)` short names and `Non-EU` branch |
| how_used 1: gridflow's connector fetches this listing to plan company and facility storage queries | `client.py:183-185,311-316`; `endpoints.py:442-454` |
| how_used 2: roll facility storage up via `company_code` | `company_code` = facility `company` else parent EIC, `endpoints.py:290` |
| how_used 3: operational dates only in `about_summary` | listing drops them (`agsi.py:476-488`); summary keeps them (`agsi.py:625-626`) |
| chart: facility rows, dedup on `entity_code` (newest `ingested_at`), grouped by `country_code`, 8 named plus `rest`, count | committed series: provenance `rows_read 1665, rows_matched 1089, duplicates_dropped 968, rows_used 121`; `spec_origin: vault` |
| chart_view.alt values: Germany 63; 13 others 18; France 8; Netherlands 7; Romania 7; Austria 5; United Kingdom 5; Czech Republic 4; Poland 4 | `site/hifi/data/series/gie/about_listing.json` `x`/`values` |
| key note (rest): IT, DK, HU, SK, BE, BG, ES, HR, IE, LV, PT, SE, UA | series `provenance.unmapped_groups` (13 codes) |
| key note (UK): each listed under `GB` and again under `GB*`; silver kept `GB` | bronze: all 5 `GB` facility EICs also appear under `GB*`; listing silver has no `GB*` |
| caption: "as fetched 27 September 2026" | bronze meta `fetched_at` 2026-09-27T00:31:37Z |
| caption: entries GIE names historical or decommissioned count too | silver names containing "historical data prior to" and "(decommissioned)" are in the 121 |
| raw_feed.note: one unpaginated GET, no dates sent | `client.py:238-265` (only `default_params`; dates only for `unavailability`) |
| raw_feed.note: bronze filed under the `--start` date, not the fetch time | `client.py:262` (`data_date=start.date()`); meta `data_date` 2026-09-20 against `fetched_at` 2026-09-27 |
| raw_feed.note: a transform day with no bronze copies the newest capture | `agsi.py:402-428` (newest folder by mtime) |
| raw_feed.requests | bronze meta `request_url` `https://agsi.gie.eu/api/about?show=listing` |
| commands: `ingest ... --start 2026-09-27` (end defaults to now); `transform ... --start 2026-09-27 --end 2026-09-27` (one inclusive day) | `pipeline/runner.py:479-500` (`resolve_dates`), `1134-1138` + `utils/time.py:113-120` (inclusive `date_range`) |
| record.key `entity_code` | `agsi.py:387-391` |
| fields.entity_name: `short_name` else `name`; summary keeps full `name` | `endpoints.py:265,281`; `agsi.py:588,619` |
| fields.country_code: `GB*` exists and is dropped here by EIC dedup | bronze; listing silver has no `GB*` |
| fields.entity_type: blank becomes null | `endpoints.py:489-494` (`_optional_text` skips `""`) |
| fields.company_name: `short_name` of the entry the facility is listed under | `endpoints.py:265,291`; e.g. EWE facilities show "EWE Gasspeicher" while the kept EWE company row is "EWE Gasspeicher (NL) (5) (8)" |
| fields.entity_url: the `/api` storage query URL GIE sends | silver values `https://agsi.gie.eu/api?country=..&company=..[&facility=..]` |
| notebook.lead: `query()` filters on `ingested_at`, a transform time | gridflow `silver/schema_manifest.py:226`; `gridflow_models` reads it via `_schema_manifest.py:35,58` |
| notebook.lead: each transform day holds a whole copy | partition equality check above |
| related gie/storage_reports: same EIC as `entity_code` at company and facility level | `agsi.py:173-180` (`entity_code` from `code`/`eic` or the request's facility/company) |
| related gie/unavailability: `facility` names facilities by these EICs | unavailability `facility` is JSON `{"eic", "name"}` (silver) |
| related gie/storage: gridflow fetches nine of the countries listed here | `endpoints.py:14` `AGSI_COUNTRIES` (9, all present in the listing); `client.py:180` |
| family differs (summary): full names, country names, operational dates; its UK rows keep `GB*` | `agsi.py:590-632`; summary silver: 9 EICs with `GB*` |

## Body corrections (canonical notes, mirrored)

`about_listing.md`:
1. **Dedup key.** It said `(entity_level, entity_code)`; it is `entity_code` alone, `keep="last"`, and repeated EICs lose their earlier entries (`agsi.py:387-391`).
2. **Point-in-time.** Added that `event_time` is the transform target date at 00:00 UTC (`base.py:2228-2232`), and that a multi-day transform writes one copy per day (`agsi.py:309,405-406`).
3. **`entity_name` source.** It said `name` (or `short_name`); it is `short_name`, else `name` (`endpoints.py:265,281`).
4. **`country_code`.** It said ISO-2; GIE also sends `GB*`.
5. **`entity_type`.** It said `SSO` / `DSR`; facilities carry `ASF`, `DSR`, `ASR`, `GRP` or `SRC`, and a blank becomes null (`endpoints.py:489-494`).
6. **`company_name`.** It said "from parent `name`"; it is the parent entry's `short_name`, else `name` (`endpoints.py:265,291`).
7. **`ingested_at`.** Now described as the silver transform time (`agsi.py:381`).
8. **Operational dates.** Removed the false claim that `operational_*_date` pass through: `_records_from_payload` builds fixed fields (`agsi.py:462-489`).
9. **Silver sample.** `entity_name` and `company_name` "GSA LLC" corrected to "GSA".
10. **Modelling filter.** It pointed at `operational_end_date`, which this table lacks; it now points to `about_summary`.

`about_summary.md`:
1. **Overview.** Removed "used at silver level to enrich storage/storage_reports ... and to plan expected bronze counts". No gridflow code reads this table; planning fetches `about_listing` (`client.py:311-316`).
2. **Bronze sample.** Companies carry `data: {type, country: {code, name}, code, name}` rather than top-level `type`/`country`/`url`. Facilities carry a `country` dict and no `company`.
3. **Dedup key.** Corrected as for the listing, noting that this member keeps the `GB*` UK rows because `Non-EU` follows `Europe`.
4. **Point-in-time.** Same note as the listing.
5. **Schema table.**
   - `short_name`: company-only.
   - `country_code`, `country_name`, `entity_type`: sources corrected (`data.country.*` / `data.type` for companies).
   - `company_code` and `company_name`: derived from the enclosing company (`agsi.py:588,627-628`), not a `company` field.
   - `aggregate_code/name`: always EU/Europe or NE/Non-EU.
   - `has_image`: nullable, company-only.
   - `ingested_at`: the transform time.
6. **Silver sample.** `country_name` None corrected to "Austria".
7. **Live shape.** Added the `Non-EU` branch in two places.
8. **Implementation delta.** It said `country` is a string in the live response; it is a `{code, name}` dict (bronze 2026-09-27).

The curl examples are unchanged; they match the connector.

## Unverified

- **Facility type codes** (`ASF`, `DSR`, `ASR`, `GRP`, `SRC`): meanings are not documented in gridflow or the vault, and I did not call GIE's docs. The page names them only as "other codes for facilities".
- **Bracketed numbers in names** (`Bulgartransgaz (4)`, `EWE Gasspeicher (NL) (5) (8)`): part of the name GIE sends; their meaning is unknown and the page does not interpret them.
- **Which duplicate survives** depends on payload order (keep last). The UK key note and the summary's "UK rows keep `GB*`" describe this capture and the current order.
- **Unfolded frame.** I checked the frame folded only. The unfolded state (the `…` expanded) was not captured; the folded columns are `company_name`, `entity_url` and the pipeline columns.

## Open questions

1. The notebook blocker is resolved (the seat refreshed the views).
2. Should `record.key` stay `entity_code` (what silver enforces), or should the page say the vendor's natural key is wider, (EIC, country) for operators? I kept `entity_code` and put the repeat in `what_it_is`, the key note and the guide.
3. The chart counts every facility listing, including historical and closed entries. A current-only count needs `about_summary`'s end dates, but family rule D5 puts the chart on the lead's table. Keep, or chart from the member?

## Template problems

None found. One observation: `rest` (the "13 others" bar) sorts second under `value_desc`, above France. This is honest (18 > 8) but reads a little oddly. There is no sort option that pins a bucket last.

## Defects

- **gridflow `silver/gie/agsi.py:387-391`: AGSI reference dedup drops real vendor listings.**
  - `AgsiJsonTransformer.transform` dedups `about_listing` and `about_summary` on `entity_code` alone with `keep="last"`. The 2026-09-27 `/api/about` payload lists 7 company EICs twice and 6 facility EICs twice:
    - SEFE, Uniper and EWE under two countries;
    - four UK operators and five UK facilities under both `GB` and post-Brexit `GB*`;
    - `21W000000000095N`, used for both the Edison Stoccaggio group and VGS HUB2.
  - 13 listings are silently dropped, and the survivor depends on payload order. `about_listing` keeps the pre-Brexit `GB` rows; `about_summary` keeps `GB*`.
  - Facility `company_name` can disagree with the surviving company row (EWE facilities say "EWE Gasspeicher"; the kept company row is the NL entry).
  - Fix idea: key on (`entity_code`, `country_code`), plus the operational start date for facilities.
- **gridflow `silver/gie/agsi.py:309,402-428`: the reference transform copies one capture into every day.**
  - `fallback_to_latest_partition = True` makes any transform day with no bronze read the newest bronze folder (by mtime). A multi-day transform therefore writes N identical partitions.
  - Local silver holds 9 identical 185-row partitions (19 to 27 Sep) from one capture fetched 2026-09-27 00:31 UTC.
  - `event_time` is set to each target date (`base.py:2228-2232`), so the copies look like dated observations of the register.
- **gridflow `connectors/gie/client.py:262`: bronze for dateless AGSI endpoints is filed under `--start`, not the fetch date.** `data_date=start.date()`, so the 27 Sep capture sits under `bronze/gie_agsi/about_*/2026/09/20/`.
- **gridflow `silver/gie/agsi.py:462-489`: `about_listing` discards the payload's `operational_start_date` and `operational_end_date`.** The listing payload carries them, but `_records_from_payload` builds fixed fields only.
- **gridflow: blank facility `type` is inconsistent between the members.** It becomes null in `about_listing` (`endpoints.py:489-494`) but stays `""` in `about_summary` (`agsi.py:624`).
- **Data state: the warehouse has no views for the AGSI reference tables.**
  - `C:\gridflow-data\gridflow.duckdb` (mtime 2026-09-27 00:23 UTC) has no `silver_gie_agsi_about_listing` or `silver_gie_agsi_about_summary` view, while the silver files date from 00:31 UTC. `data.sql()`, `query()` and `tail()` fail for both tables until views are refreshed.
  - Also note `gridflow_models`: `configs/settings.yaml` values beat `GRIDFLOW_MODELS_*` env vars (`config/settings.py:156-160`), so the warehouse cannot be redirected per process.
  - Resolved 2026-09-29 by the seat's `refresh_views` (with a snapshot first). The root cause, a transform that ran without its view refresh landing, is still worth a backlog line.
- **Vault: the `about_listing` and `about_summary` notes were stale against the code.** Wrong dedup key, name source, type values, country shape and a false pass-through claim. Corrected on branch `docs/v5-p26-gie`.

## Files written

- Canonical notes: `scratchpad\vault-p26-gie\30-vendors\gie\datasets\about_listing.md` (page block and body) and `about_summary.md` (body).
- Mirror: `scratchpad\p26-gie\vault\gie\about_listing.md` and `about_summary.md`, byte-identical.
- Artefacts: `scratchpad\p26-gie\site\hifi\data\series\gie\about_listing.json` and `scratchpad\p26-gie\site\hifi\data\samples\gie\about_listing.json`. Notebook: `scratchpad\p26-gie\site\hifi\data\notebooks\gie\about_listing.json` (no plot, so no PNG). Built page: `scratchpad\p26-gie\site\hifi\data-sources\gie\agsi-reference.html`.
- There was no staged chart spec or authored override for these datasets to retire.

## Nits fixed (after the APPROVE review, `agsi-reference-review.md`)

1. **`page.chart_view.caption`.** "Entries GIE names historical or decommissioned count too" is now "Closed and historical entries count too, whether or not their names say so." (36 of 40 words.)
2. **`page.chart_view.key[uk].note`.** Now reads "Each is listed under `GB` to 2020 and again under post-Brexit `GB*`; silver kept the pre-Brexit `GB` entry." (17 of 18 words.)
3. **Grain scoped to one transform day.**
   - `page.facts.grain` now reads "One row per EIC per transform day; `entity_level` says operator or facility".
   - `page.what_it_is` now ends "silver keeps one row per EIC per transform day".
   - `page.record.fields.entity_code` now reads "The listing's `eic`; one row per EIC per transform day, the last sent".
   - `record.key` stays `[entity_code]`.

**Checks.**
- The canonical note is edited with CRLF kept (339 lines, 339 CRs), and both mirrors are byte-identical (`cmp`).
- `gridflow-build --only gie/about_listing` is green, and `detect.mjs --json` returns `[]`.
- The new wording appears in the rendered `agsi-reference.html`.
- The chart spec, record select and notebook cells are unchanged, so the series, sample and notebook artefacts did not need regenerating (the build's digest checks passed).
- I did not touch the server on port 9670.
