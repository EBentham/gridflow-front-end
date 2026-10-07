# neso/intensity_factors: author report

Writer: Opus 5.5 (high), 2026-10-06. Port 9869 (server stopped; port 9670 not touched).

## Status

- `gridflow-build --only neso/intensity_factors`: clean (dataset template, 1 distilled series).
  - The final rebuild reports "neso: 1 error(s) on pages not rendered by --only". That error belongs to a sibling writer's NESO note (`carbon_intensity`, `intensity_stats` and `regional_intensity` also carry `page:` blocks). `_scoped` in `build.py` keeps every error that names this page, and none was kept.
  - The topsoil was re-shot at 1440 and 390 after the final `what_it_is` edit (`scratchpad/if_shots/r_topsoil.png`).
- `detect.mjs --json`: `[]`. Em dashes in the page: 0. Arrows and middle dots: 0.
- Leakage grep over the rendered text (`locally|held|our|live|now|real-time|yet|soon|planned|coming|static|since 20xx|N rows|N days`): no hits.
- Mirror: canonical note copied to `vault/neso/intensity_factors.md`, `cmp` equal; 219 lines, all CRLF.
- No staged spec or authored override existed for this dataset (nothing to delete).
- Artefacts:
  - `site/hifi/data/series/neso/intensity_factors.json` (`spec_origin: vault`, 14 categories, 14 rows used).
  - `samples/neso/intensity_factors.json` (8 rows, `gridflow-sample`).
  - `notebooks/neso/intensity_factors.json` (5 cells, no errors, `run_notebooks.py`).
- Screenshots at 1440, 1024, 768 and 390 (390 as a true 390 px iframe), all looked at: nothing clipped or overlapping.
  - Files: `scratchpad/if_shots/w{1440,1024,768,390}.png`, plus crops and montages.
  - The site has no dark theme, so light is the only rendering.

## What the page says

- **Chart:** a bar chart of all 14 fuels, sorted by factor, from the capture fetched on 26 September 2026.
  - `aggregation: last` over one row per fuel, so nothing is summed or averaged.
  - `group_map` gives plain labels ("Gas (CCGT)", "Pumped storage") so no snake-case code reaches the axis. The longest label fits the 110 px narrow gutter.
  - One fallback key entry (`series: factor_gco2_kwh`, petrol), because `KEY_MAX` is 9 and there are 14 fuels.
  - The five zero-factor fuels are named in the caption, since their bars have no width.
- **Rows:** eight of the 14 fuels by `fuel in [...]`: the two gas splits, the three import countries, `coal`, `other` and `wind` (0).
- **Notebook:** uses `data.sql()` on `silver_neso_intensity_factors`, because `query()` would filter on `ingested_at`.

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| One row per fuel; key `fuel` (`facts.grain`, `record.key`) | `silver/neso/carbon_intensity.py:553` `unique(subset=["fuel"], keep="last")`; `_extract_factor_rows` :364-371 emits one row per key of `data[0]` |
| Raw request is `GET https://api.carbonintensity.org.uk/intensity/factors`, no parameters (`raw_feed.requests`) | `connectors/neso/endpoints.py:76-82` (`path_template="/intensity/factors"`, `reference=True`); bronze sidecar `request_url` is that URL, `request_params: {}` |
| One call whatever the window; "the window is ignored" (`commands`) | `connectors/neso/carbon_intensity.py:132-133`: `requires_window` False returns one `(start, end)` spec, and the path has no date fields; `data_date=None` for reference endpoints (:79) |
| `transform` rewrites one silver file from the newest bronze capture; a revised factor replaces the old row (`raw_feed.note`, `how_used[2]`) | `carbon_intensity.py:132-139` (reference read: `sorted(rglob("raw_*.json"), reverse=True)[:1]`), :251 (`write_parquet` to the single `intensity_factors.parquet`); the dateless non-partition path in `silver/base.py` `run()` calls `read_bronze` per date, which always returns that one body |
| Bronze keeps each fetch | Bronze is one immutable `raw_<ts>_<hash>.json` per call under the fetch date (`bronze/neso/intensity_factors/2026/09/26/raw_20260926T174349Z_2dec0311.json`) |
| `sources.yaml` declares it weekly (`facts.cadence`) | `gridflow/config/sources.yaml:626-629` (`schedule: "weekly"`, `max_query_days: 0`) |
| `fuel` is NESO's name lowercased and snake-cased; `Gas (Combined Cycle)` becomes `gas_combined_cycle` (`fields.fuel`) | `carbon_intensity.py:542-547`; bronze key `"Gas (Combined Cycle)"`, silver `gas_combined_cycle` |
| The response states no unit; gCO2/kWh is gridflow's label (`what_it_is`, `fields.factor_gco2_kwh`) | Bronze body is bare integers keyed by fuel name; the column name `factor_gco2_kwh` is `schemas/neso.py:52`; `docs/endpoints/neso.md:19` says "in `gCO2/kWh`" |
| NESO's API definitions do not say whether a factor is combustion only or life cycle (`what_it_is`) | carbon-intensity.github.io/api-definitions, fetched 2026-10-06 in two checks. (1) The route section: "Get Carbon Intensity factors for each fuel type", with no unit, basis or import text. (2) The whole page, every section: no sentence mentions life cycle, lifecycle, combustion or an emissions basis. The only scope line is the intro's "The Carbon Intensity forecast includes CO2 emissions related to electricity generation only", which concerns the forecast, not the factors. |
| "Carbon Intensity factor" is NESO's own term (`what_it_is`) | The same page's route heading: "Get Carbon Intensity factors for each fuel type". The page title keeps gridflow's "Emission factors". |
| Gas split by cycle, imports by country (Dutch, French, Irish) (`what_it_is`, `record.caption`) | Bronze keys `Gas (Combined Cycle)`, `Gas (Open Cycle)`, `Dutch Imports`, `French Imports`, `Irish Imports` |
| "imports carry one factor per country" (key note) | Same bronze keys: one value each (474, 53, 458). This describes the response only; how NESO sets them is not claimed. |
| `generation` needs gas and imports mapped first (`how_used[0]`, related note) | Silver `neso/generation*` fuel values: `biomass, coal, gas, hydro, imports, nuclear, other, solar, wind` (Polars, 2026-10-06). gridflow `.planning/phases/V1-vault-vendor-validation-and-docs/neso-VALIDATION.md` section 5: "Joins between the two on `fuel` will need a mapping table" |
| Chart values: Coal 937, Oil 935, OCGT 651, Dutch 474, Irish 458, CCGT 394, Other 300, Biomass 120, French 53, five fuels 0 (alt, caption) | Committed series `x`/`values`, matching silver exactly |
| "fetched 26 September 2026" (chart title, caption, alt) | Sidecar `fetched_at: 2026-09-26T17:43:49Z`; silver `ingested_at 2026-09-26 17:43:49Z`. The capture is dated the way the approved `bmunits_reference` page does it. |
| `query()` filters on `ingested_at`, a transform time (`notebook.lead`) | `silver/schema_manifest.py:241` (`("neso","intensity_factors"): "ingested_at"`); `carbon_intensity.py:665-669` stamps `ingested_at = datetime.now(UTC)` at transform |
| Relation `silver_neso_intensity_factors` | Notebook ran: cell 4 and cell 5 outputs are real frames (coal 937 ... ; gas and imports filter, 5 rows) |
| `neso/carbon_intensity` is also gCO2/kWh (related note) | `docs/endpoints/neso.md:17` ("Forecast, actual, and index values in `gCO2/kWh`"); columns `forecast_gco2_kwh`, `actual_gco2_kwh` |
| Related pages resolve | Build passed (`related` resolution is a build error otherwise) |

## Body corrections (canonical note)

1. **Silver layer:** added a `**Write mode**` line. Silver is one file, rewritten each transform from the newest bronze body only; a revised factor replaces the old row, and only bronze keeps earlier fetches. Cites `carbon_intensity.py:132-139`, `:251`. The note was silent on this.
2. **Known issues and gotchas:** two bullets added.
   - The 14 factor fuels against the 9 `generation` fuels need a mapping (validation record section 5, plus the silver check).
   - The response has no unit, and the API definitions page states no unit, basis or import treatment (checked 2026-10-06). The methodology PDF was not read.
3. **Links:** relabelled "Gold view/builder" to "Gold view (does not read this table)". `gold/views/uk_imbalance_context.sql` has no reference to factors (grep returns nothing). "Gold layer: None implemented" was already right.

Left alone:
- The copy-pasted Known-issues bullets about timestamps and `intensity_period`. They are irrelevant here, but not wrong.
- The Overview sentence "explains how generation technologies are weighted inside the Carbon Intensity methodology". It is unverified (see below) but outside the page. It is flagged here rather than rewritten.

## Not verified

- **Combustion versus life cycle.** Nothing the note quotes, and nothing on the API definitions page, says which. NESO links a methodology PDF:
  - `https://api.neso.energy/dataset/f406810a-1a36-48d2-b542-1dfb1348096e/resource/36638178-e993-4d34-afdc-4ada83993585/download/neso-ci-national-methodology_v2.pdf`, reached from the "National Carbon Intensity Forecast Methodology" page.
  - I did not download it: a file download needs Bobbo's permission.
  - The page states plainly that the API definitions do not say.
- **Unit.** gCO2/kWh is gridflow's label (column name and gridflow docs). No NESO text seen states the unit for this route.
- **Imports.** Whether the three import factors are fixed per country or derived from something else is not stated anywhere seen.
  - The vault's `20-domain/concepts/carbon-intensity.md` says "Imports use a flow-weighted average of the source country's intensity". That is the vault's own unsourced statement, not a vendor quote, so it is not used.
- **Whether NESO ever revises the factors.** gridflow calls them "Static" (`endpoints.py:80`), but no vendor evidence was seen. The page avoids "static" and states only what silver and bronze would do with a change.
- **The Overview's "weighted inside the Carbon Intensity methodology"** (note body, not on the page): unverified for the same reason.

## Open questions (for the seat)

1. Should a research unit read the methodology PDF above? It would give the factors' basis, their source and the import treatment, and the page could then state them with a quote. Until then the page says the docs do not say. Recommendation: yes, low priority. The page ships accurate without it.
2. Bar labels are plain names via `group_map` rather than silver codes. The frame and guide below show the codes, and the `fuel` guide line shows the mapping rule. Acceptable, or should the chart show raw codes?

## Template problems

- None blocking.
- One observation: for a bar chart with more than 9 categories, `KEY_MAX` forces a single fallback key entry. `_bars` then labels each bar with the category name, so plain labels need a `group_map` even when nothing is grouped. That works, but a `label_map` (or letting `group_map` carry display names explicitly) would state the intent better. For the seat to consider; nothing was worked around.

## Defects

Pasteable for the gridflow backlog and the vault remediation page:

- **Vault ERD asserts a join that fails (docs).**
  - `quant-vault/10-projects/gridflow/data-layer-erd.md:331` draws `NESO_INTENSITY_FACTORS ||--o{ NESO_GENERATION : fuel`. Only 7 of the 14 factor codes match a `generation` fuel.
  - Gas is split (`gas_combined_cycle`, `gas_open_cycle` against `gas`). Imports are split by country (`dutch_imports`, `french_imports`, `irish_imports` against `imports`). `oil` and `pumped_storage` have no `generation` category.
  - Evidence: silver `neso/generation*` distinct `fuel` (2026-10-06); gridflow `neso-VALIDATION.md` section 5.
  - Fix: annotate the relation as needing a mapping table, or remove it.
- **Domain concept states an unsourced import method (docs).**
  - `quant-vault/20-domain/concepts/carbon-intensity.md` says "Imports use a flow-weighted average of the source country's intensity". No vendor quote backs it.
  - The `/intensity/factors` response carries one fixed factor per import country (Dutch 474, French 53, Irish 458 on 26 Sep 2026).
  - Fix: source it from the NESO methodology PDF or remove it.
- **Unit and basis of `factor_gco2_kwh` undocumented (docs gap).**
  - The response sends bare numbers. The API definitions page states no unit or emissions basis for `/intensity/factors` (checked 2026-10-06).
  - gridflow names the column `factor_gco2_kwh` and `docs/endpoints/neso.md:19` says gCO2/kWh, with no vendor citation.
  - Fix: a research unit reads `neso-ci-national-methodology_v2.pdf` and cites the unit and basis in the vault note.
- **Note link mislabelled (fixed in this branch).** `30-vendors/neso/datasets/intensity_factors.md` Links called `uk_imbalance_context.sql` the "Gold view/builder" for this table, but that view does not read it. The link is now relabelled.
- **Minor, code comment (no data impact).** `connectors/neso/endpoints.py:80` describes the factors as "Static"; no vendor evidence supports that. Silver handles a change correctly anyway (newest capture wins, bronze keeps each).
