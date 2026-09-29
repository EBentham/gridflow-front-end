# agsi-storage: author report

Family page `agsi-storage` (lead `storage`, member `storage_reports`). Writer: Opus 5.5, 2026-09-29.

## Status

- `page:` block written on the canonical `30-vendors/gie/datasets/storage.md` (vault worktree `vault-p26-gie`), body corrections on `storage.md` and `storage_reports.md`, both mirrored byte for byte into `p26-gie/vault/gie/` (`cmp` clean; CRLF kept, 409/409 and 299/299; git normalises to LF, so the diff is content only).
- Artefacts: `site/hifi/data/series/gie/storage.json` (distil, `spec_origin: vault`, 5 series x 10 points, 50 rows used), `samples/gie/storage.json` (gridflow-sample, 8 rows x 31 columns), `notebooks/gie/storage.json` + `storage-5.png` (run_notebooks, 5 cells, no errors).
- No staged spec and no authored override existed for gie.
- `gridflow-build --only gie/storage`: wrote `data-sources/gie/agsi-storage.html`, no errors. Four pre-existing content WARNs for other gie datasets (see "Template problems").
- `detect.mjs --json`: `[]`.
- Screenshots at 1440, 1024, 768, 390 (390 via a 390 px iframe), static server on 9851, stopped after. Nothing clipped or overlapping. The site has no dark theme (`tokens.css`/`theme.css` hold no `prefers-color-scheme` or `data-theme` rule), so the dark shots equal the light ones.
- First render: Italy (clay) and Austria (bronze) read as one orange, and Germany (petrol) and the Netherlands (horizon) were two teals on adjacent lines. Repainted to IT horizon, FR olive, AT dashed (`hatch-lines`, the one unpainted line allowed), DE petrol, NL clay. The notebook colours now match (DE petrol, FR olive, IT horizon, NL clay).

## Coverage (the brief's first question)

| Table | What the rows are | Evidence |
|---|---|---|
| `storage` | Country level only: 9 entities, `entity_level = country`, codes AT, BE, DE, ES, FR, GB, IT, NL, PL; one row per country per gas day; 15 gas days x 9 = 135 | Polars group_by on silver: 9 groups x 15 rows each. Connector default scope `COUNTRY` for `storage` (`connectors/gie/client.py:177-181`), country list `AGSI_COUNTRIES` (`connectors/gie/endpoints.py:14`) |
| `storage_reports` | Only the EU aggregate: `entity_level = aggregate_type`, `entity_code = eu`, `entity_name = EU`, `country_code = ""`, `country_name = null`; one row per gas day = 15 | Silver group_by: 1 group x 15. Default scope `AGGREGATE_TYPE` (`client.py:177-181`), default aggregate types `("EU",)` (`client.py:191-194`, `endpoints.py:25`); the runner calls `connector.fetch(ds, ds_start, end_dt)` with no params (`pipeline/runner.py:947`), so the CLI can never ask for another scope. Bronze meta: every request is `type=EU&date=...` |
| GB | Present in `storage` every day as "United Kingdom (Pre-Brexit)", status `N`, every numeric null except `consumption_full_pct = 0.0` | Silver; bronze body sends `"-"` placeholders and `"consumptionFull":"0"` |
| EU vs countries | Never sum: EU working gas volume 1,131.5658 against 899.4094 for the eight non-GB countries on 13 to 22 Sep; EU gas in storage 794.8308 against 632.8453 on 22 Sep | Polars join of summed country rows to the EU rows. The EU aggregate covers storage in countries outside gridflow's list |

The page states none of these local counts: it names the nine countries (a code fact) and "EU aggregate".

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Request URL `GET https://agsi.gie.eu/api?country=DE&date=2026-09-22&page=1&size=300` (`raw_feed.requests`, family `storage`) | `storage_params_for_date` builds scope params, then `date`, `page`, `size` (`endpoints.py:196-220`); `size` 300 (`endpoints.py:22`). Bronze meta `request_url` for AT/BE 2026-09-22 has exactly this shape |
| `storage_reports` URL `...?type=EU&date=2026-09-22&page=1&size=300` | `_storage_scope_params` returns `{"type": entity_key}` (`endpoints.py:406-407`); bronze meta, all 16 storage_reports files |
| One call per country and gas day (`what_it_is`, `raw_feed.note`) | `build_storage_query_plan(date_mode="exact")` loops targets x gas days (`endpoints.py:326-350`); `_fetch_agsi_storage` asserts one gas day per request (`client.py:202-203`) |
| Ingest `--end 2026-09-22` fetches 22 Sep ("the end day is fetched") | `resolve_dates` makes a bare date midnight UTC (`pipeline/runner.py:479-501`); `gas_day_range` takes `.date()` of both ends and is inclusive (`endpoints.py:182-193`) |
| Bronze filed by gas day; transform reads only that day, no offsets | `RawResponse(data_date=gas_day)` (`client.py:204-213`, `:351`); bronze meta `data_date` = request date and path `2026/09/22/`; `read_bronze` reads the target date's folder only (`silver/gie/agsi.py:128-148`, `:275-288`) |
| Transform end inclusive | Same convention as all approved pages (`runner.run_transform` date loop); commands match the chart window 13 to 22 Sep |
| Key `[gas_day, entity_level, entity_code, entity_url]` | Dedup dict key (`silver/gie/agsi.py:233-241`) |
| `gas_day` = vendor `gasDayStart` date; `event_time` labelled 06:00 UTC | `_first(row, "gas_day_start", "gas_day")` (`agsi.py:158`); `gas_day_event_time_expr` fixed 06:00 UTC, a project convention that "deliberately differs" from the DST-aware vault page (`silver/base.py:383-400`); silver `event_time` = `gas_day 06:00 UTC` |
| `gas_day_end` = next date at 00:00 UTC | `_safe_datetime` turns a 10-char date into `T00:00:00+00:00` (`agsi.py:56-57`), applied at `:193`; silver 2026-09-22 row has `2026-09-23 00:00:00 UTC` |
| `updated_at` zoneless, read as UTC | Bronze `"updatedAt":"2026-09-25 18:11:53"`; `_safe_datetime` adds UTC to a naive value (`agsi.py:59-62`) |
| `ingested_at` is the silver transform time (not shown on page) | `now = datetime.now(UTC)` in `transform` (`agsi.py:154`, `:226`) |
| `entity_level` `country` on every `storage` row | `_storage_entity_level` returns `country` when `request_country` is set (`agsi.py:561-576`); silver |
| Chart unit `%` for `storage_pct_full` | Vendor `full`; schema clamps 0 to 100 (`schemas/gie.py:42-47`); in silver it equals `gas_in_storage_gwh / working_gas_volume_gwh * 100` to 2 dp for every entity (max abs error 0.0) |
| "five countries with the largest working gas volume" (caption) | 22 Sep `working_gas_volume_gwh`: DE 247.494, IT 203.4249, NL 144.0428, FR 123.8779, AT 100.2789, PL 36.8491, ES 35.8318, BE 7.61 |
| Alt values | Committed series: it 84.66 to 86.03, fr 76.74 to 81.09, at 67.1 to 67.87 (21st), 67.81 (22nd), de 55.81 to 56.99, nl 52.55 to 56.26; ordering IT > FR > AT > DE > NL on every day, so no crossing |
| `net_withdrawal_gwh` within 0.1 of withdrawal minus injection (guide) | 8 rows: AT 60.6 - 4.29 = 56.31 vs 56.3; IT 1.1 - 240.06 = -238.96 vs -238.9; all entities max abs diff 0.1 |
| `consumption_full_pct` = stock over consumption, GB sends 0 | 8 rows, e.g. DE 141.04 / 903.9 = 15.60; GB `0.0` with nulls |
| Contracted and available capacity on the working-gas-volume scale | contracted + available = WGV for AT, ES, FR, IT, NL, PL (ratio 1.000), DE 1.027, BE 0.96 |
| `covered_capacity_gwh_per_day` 100 on every row but GB's | 8 rows; all 120 non-GB silver rows are 100.0 |
| `trend` tracks the day's change in `storage_pct_full` | 8 rows: AT -0.06 (67.87 to 67.81), FR 0.27, IT 0.12, NL 0.3; PL 0.09 vs 0.08 |
| Status `C`/`E`/`N` in these rows | 22 Sep: NL `E`, GB `N`, rest `C` |
| `info` is `[]` text | `_json_string([])` gives `"[]"` (`agsi.py:65-70`); every silver row `"[]"` |
| Notebook lead: `silver_gie_agsi_storage`, `gas_day`, both ends | gridflow_models `_RELATION_NAME_BY_DATASET["storage"] = silver_gie_agsi_storage`, date column `gas_day` (gridflow `silver/schema_manifest.py:230`), DATE predicate `BETWEEN ? AND ?` (`_get_method_registry.py`, `_date_range_predicate`) |
| `notebook.source: gie_agsi` needed | `artefacts.notebook_source` falls back to the vendor id (`gie`), which has no handle; with the field, cell 2 prints the `data.gie_agsi` card |
| Plot alt values | net withdrawal: FR min -759.2 on 20 Sep; DE -71.7 (15th), -711.1 (19th), -1.0 (22nd); NL -429.5 (22nd); every point of DE, FR, IT, NL < 0 |
| Family `differs` | as the coverage rows above |
| Related | `gie/unavailability`, `gie/about_listing`, `gie/lng` are in `gie.json`; `entsog/physical_flows` has a page, its flows are `flow_gwh_per_day` per gas day |

## Units (the brief's second question)

- Charted column: `storage_pct_full`, percent (vendor `full`), verified exactly as stock over working gas volume. Only one unit is on the axis.
- Flows `injection_gwh`, `withdrawal_gwh`, `net_withdrawal_gwh`: GWh per gas day, per the code's names and the vault. GIE's own unit statement is not in any source I could read (the `docs/gie_agsi_endpoint_catalog.yaml` links the v006/v007 PDF but quotes no units).
- Stock-scale columns `gas_in_storage_gwh`, `working_gas_volume_gwh`, `consumption_gwh`, `contracted_capacity_gwh_per_day`, `available_capacity_gwh_per_day` are **1,000 times the flow scale**. For every entity (9 countries + EU), the day-on-day change in `gas_in_storage_gwh` x 1,000 matches `injection_gwh - withdrawal_gwh` (median error 0.0 to 5.4 GWh; DE 13 to 14 Sep: 0.2822 x 1,000 = 282.2 vs 282.1). If the flows are GWh, the stocks are TWh. The `_gwh` suffix on them is wrong, and the two `_gwh_per_day` capacity names are wrong twice over: they are volumes, not rates. The page says the stock moves by net injection divided by 1,000 and steers comparison to `storage_pct_full`; it does not assert "TWh" as GIE's unit.
- `covered_capacity_gwh_per_day` is 100 wherever it has a value, and its meaning is undocumented.

## storage_reports (the brief's third question)

Same transformer and columns as `storage` (a subclass, `agsi.py:291-301`), same `/api` endpoint, but:
- the connector's default scope is the aggregate `type=EU`, and the CLI cannot pass another, so silver holds one EU row per gas day;
- `schema_cls = None` (`agsi.py:301`): no `GasStorage` validation and no 0 to 100 clamp on `storage_pct_full`;
- on those rows `entity_code` is the vendor's lowercase `eu`, `country_code` is `""` and `country_name` is null (`agsi.py:173-188`).
Country, company and facility scopes exist in the connector (`endpoints.py:398-455`) but need a direct `connector.fetch(..., scope=...)` call.

## Body corrections

`storage.md`:
1. Overview: "the AGSI footprint" replaced by gridflow's own list `AGSI_COUNTRIES` (`endpoints.py:14`).
2. Gas-day pointer: "gas day starts at 06:00 UTC" replaced by what gridflow stores: `gasDayStart` date, `event_time` fixed 06:00 UTC as a project convention (`silver/base.py:383-400`).
3. Silver table: `gas_day` note (fixed 06:00 UTC label); `gas_day_end` (next date at 00:00 UTC, `agsi.py:56-57,193`); `updated_at` (zoneless, read as UTC, `agsi.py:48-62`); `gas_in_storage_gwh`, `working_gas_volume_gwh`, `consumption_gwh` (1,000x the flow scale, checked); `consumption_full_pct` (GB sends 0); `net_withdrawal_gwh` (sign checked); `contracted_`/`available_capacity` (volumes on the WGV scale); `covered_capacity` (100, meaning undocumented).
4. Known issues: "All values in GWh" replaced by the unit finding; the gas-day bullet as in 2; "Other ISO-2 codes return empty data" replaced by: the list is gridflow's, the EU aggregate covers more storage, never sum countries.

`storage_reports.md`:
1. Overview: added the default `type=EU` scope and that a CLI ingest holds only EU rows (`client.py:177-181`, `endpoints.py:25`, `runner.py:947`).
2. Gas-day pointer, as in `storage.md`.
3. "Pydantic schema: GasStorage" replaced by none, `schema_cls = None` (`agsi.py:301`), so no clamp.
4. Table: `entity_code` `eu` lowercase; `country_code` empty string and `country_name` null on aggregate rows (`agsi.py:182`, `:186-188`); `storage_pct_full` not clamped; the same unit, time and capacity rows as `storage.md`.
5. Known issues: units bullet and gas-day bullet, as in `storage.md`.

Left alone: the curl examples (valid vendor calls), the vendor-doc prose, the gold section.

## Could not verify

- GIE's stated units for any field (no vendor doc quoted in the vault or repo). The GWh-per-day reading of the flows rests on gridflow's names and the vault.
- The time zone of `updatedAt`.
- What `status` `C`/`E`/`N` mean. The note says confirmed, estimate, no value; no vendor quote. The page only names the letters.
- What `coveredCapacity` and `consumption` measure (the period of `consumption`).
- `storage_reports.md`: "Aggregate `EU` row co-exists with country rows in the same response". The `type=EU` responses we hold contain only the EU row (`total: 1`). Left in the note; I did not reproduce what query would return both.
- The EU gas-day start instant (06:00 CET/CEST per the vault concept page) is not stated on the page. The page says only what gridflow stores.

## Open questions for the seat

1. Should the page say "TWh" for the stock columns? I kept it relative ("net injection divided by 1,000") because GIE's unit is not quoted in our sources. A research unit could settle it from the GIE API PDF.
2. Frame shows 8 of 9 countries on 22 Sep (BE left out, the smallest by working gas volume) so GB's null row stays visible.

## Template problems

- The family variant heading prints the slug upper-cased as if it were a vendor code (`STORAGE`, `STORAGE_REPORTS`). `build.py:1363` uses `mem.dataset.upper()` when the note title has no `(CODE)`, and `_extract_api_code_from_title` falls back to `slug.upper()` (`build.py:754-759`). The approved ENTSO-E family shows the same (`TOTAL_CAPACITY_ALLOCATED`). For non-Elexon vendors this reads as a fake vendor code.
- The build's content warnings name the wrong module for gie: "no Pydantic class declared in gridflow.schemas.elexon" for `storage_reports`, `unavailability`, `about_listing`, `about_summary`.
- With no `notebook.source`, a vendor whose id is not a gridflow source (gie has `gie_agsi` and `gie_alsi`) gets `data.gie`. The other gie writers need `source:` too.

## Defects

Pasteable into gridflow `.planning/BACKLOG.md` item 12+ and the vault remediation page:

- **gie_agsi storage / storage_reports: stock columns mislabelled `_gwh`.** `gas_in_storage_gwh`, `working_gas_volume_gwh` and `consumption_gwh` hold values on a scale 1,000 times the flow columns (`injection_gwh`, `withdrawal_gwh`, `net_withdrawal_gwh`). For all 9 countries and the EU aggregate, the day-on-day change in `gas_in_storage_gwh` x 1,000 matches `injection_gwh - withdrawal_gwh` (median error under 6 GWh; silver 2026-08-01 to 09-22). If the flows are GWh, the stocks are TWh (EU working gas volume 1,131.57). Source: `silver/gie/agsi.py:201-207`, `schemas/gie.py:24-30`. The vault GIE README ("stocks and flows are GWh") and both dataset notes repeated the error (notes corrected in docs/v5-p26-gie; README not touched). Fix: confirm GIE's units from the API PDF, then rename or rescale with a DATASET_VERSION major bump; the gold view `gold_eu_gas_storage` carries the same names.
- **gie_agsi storage / storage_reports: `contracted_capacity_gwh_per_day` and `available_capacity_gwh_per_day` are volumes, not per-day rates.** contracted + available equals `working_gas_volume_gwh` (ratio 1.000 for AT, ES, FR, IT, NL, PL; 1.027 DE; 0.96 BE). `covered_capacity_gwh_per_day` is 100.0 on every non-null row, so it looks like a percentage, not GWh/day. Source: `agsi.py:214-220`, `schemas/gie.py:33-35`.
- **gie_agsi storage_reports: CLI ingests only the EU aggregate.** Default scope `AGGREGATE_TYPE` with `("EU",)` (`connectors/gie/client.py:177-194`), and `pipeline/runner.py:947` passes no params, so the country/company/facility scopes the dataset exists for are unreachable from `gridflow ingest`. Decide whether that is intended; if so, document it in sources.yaml.
- **gie_agsi storage_reports: no schema validation.** `schema_cls = None` (`silver/gie/agsi.py:301`, "under rework on another branch"), so `storage_pct_full` is not clamped and aggregate rows carry `country_code = ""` (not null) and `country_name = null` (`agsi.py:182-188`).
- **gie_agsi storage: `gas_day_end` is the vendor's next-date label stored at 00:00 UTC** (`agsi.py:56-57`, `:193`). It is neither the vendor's gas-day end instant nor consistent with the fixed 06:00 UTC `event_time` label (`silver/base.py:383-400`). Low severity; document or derive it from the same convention.
- **gie_agsi storage: `updated_at` treats the vendor's zoneless `updatedAt` as UTC** (`agsi.py:59-62`) without evidence of GIE's zone. Unverified; worth a check against the API PDF.
