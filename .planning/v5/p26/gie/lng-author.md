# gie/lng (ALSI LNG terminals): author report

Writer: Opus 5.5 · high, 2026-09-29. Port 9853.

## Status

- **Build:** `gridflow-build --only gie/lng` wrote `data-sources/gie/lng.html` with no errors. The build printed three
  content warnings, all for other GIE datasets (`unavailability`, `about_listing`, `about_summary`); none is for `lng`.
- **Detector:** `detect.mjs --json` returns `[]`, with no advisories at all.
- **Artefacts:**
  - `site/hifi/data/series/gie/lng.json`: `gridflow-distil`, `spec_origin: vault`, 7 series × 10 points.
  - `site/hifi/data/samples/gie/lng.json`: `gridflow-sample`, 8 rows.
  - `site/hifi/data/notebooks/gie/lng.json` and `lng-5.png`: `scripts/run_notebooks.py`, 5 cells, no errors.
- **Retired files:** none to retire. `chart-specs/gie/` and `authored-pages/gie/` do not exist.
- **Notes:**
  - Canonical: `vault-p26-gie/30-vendors/gie/datasets/lng.md`, CRLF throughout (201 CRLF out of 201 LF, final
    version).
  - Mirror: `p26-gie/vault/gie/lng.md`, confirmed identical with `cmp`.
  - **The mirror was LF before this batch, while the canonical note was already CRLF.** The byte-for-byte copy
    therefore changes every line ending in the mirror. Expect a whole-file diff unless git normalises it.
- **Screenshots:** 1440, 1024, 768 and a true 390 (iframe), light and dark. The notebook drawer was opened by a CDP
  click and captured at 1440 and 390. Files are in `scratchpad/lng-shots/`. Nothing is clipped or overlapping.
  - The site has no dark scheme: neither `theme.css` nor `tokens.css` contains `prefers-color-scheme`. Light and
    dark shots are therefore the same design.
  - The static server on 9853 ran under `timeout` (900 s, then 400 s for the re-shoot) and stops by itself. The
    first server expired mid-shoot and truncated two captures, so I re-shot everything on a fresh server; the final
    shots are complete.
  - At 390, the notebook's `head()` table is wider than the drawer. It scrolls sideways inside `.df-wrap`
    (`overflow-x: auto`, theme.css:431) rather than clipping. This is template behaviour.

## Coverage, units and gas day (the three asks)

**Coverage (entities).**
- Every row is a **country-level** ALSI figure. There are no terminal rows and no EU aggregate.
- The connector sends one request per country from `ALSI_COUNTRIES = ["BE","ES","FR","GB","IT","NL","PL","PT"]`
  (endpoints.py:17; client.py:113-125, 361-381). The response envelope labels itself `"dataset": "EU > NL"`.
- Silver holds exactly those 8 `country_code` values, one row each per gas day.
  - It covers 15 gas days (1 to 5 Aug and 13 to 22 Sep), 8 × 15 = 120 rows.
  - There are no duplicates. The dedup key is `(gas_day, country_code)` (alsi.py:154-157).
- **GB is null on every numeric in every row.** The vendor sends `"-"` with `status: "N"` for "United Kingdom
  (Pre-Brexit)", and the transformer's `strict=False` float cast turns `"-"` into null (alsi.py:134-136). The GIE
  README's "GB Pre-Brexit" gotcha agrees.
- The chart sums the 7 non-GB countries. That is legitimate: every row is at the same level and send-out is an
  additive daily energy.
- The page never states the local span. The chart and commands use the one contiguous stretch, 13 to 22 Sep
  (10 gas days).

**Units.**

| Column | Unit | Source |
|---|---|---|
| `send_out_gwh` (charted) | GWh over the gas day | Column name set by the transformer from `sendOut` (alsi.py:98); GIE README "Units: stocks and flows are GWh" |
| `dtrs` | Unconfirmed | schemas/gie.py:62-65 ("UNCONFIRMED non-percentage metric … No unit suffix / acronym expansion asserted"); alsi.py:91-93 |
| `dtmi_lng`, `dtmi_gwh` | Unconfirmed | schemas/gie.py:66-68 |

- `dtrs` and the two `dtmi` members are not charted, not named (no acronym expansion) and not given units on the page.
- Inventory is not in silver at all (see Defects), so no LNG volume or inventory unit appears on the page.

**Gas day.**
- `gas_day` is GIE's `gasDayStart` string parsed to a date (alsi.py:56-67). It is the only date field the
  transformer reads.
- `event_time` is `gas_day` at 06:00 UTC, a fixed gridflow labelling convention and not the vendor's clock
  (alsi.py:27-28 → base.py:383-400, whose docstring says it deliberately differs from the DST-aware vault page).
- The vendor also sends `gasDayEnd` (the next date), which silver drops.
- The page says: "GIE's `gasDayStart` date; gridflow labels it 06:00 UTC in `event_time`". It makes no claim about
  what hour ALSI's gas day starts.

## Chart

- **Chart:** `stacked-area` of `send_out_gwh` by `country_code`, `aggregation: sum`. Each country has one row per
  day, so the sum is the value itself.
- **Window:** fixed 13 to 22 Sep 2026 on `gas_day` (a `Date` column, so there is no hour offset).
- **Filter:** `country_code ne GB`.
- **Stack order, bottom to top:** NL, IT, PT, PL, BE, ES, FR.
- **Paints:** petrol, olive, hatch-lines, hatch-dots, chartreuse, clay, horizon. There is no khaki.
  - Portugal was bronze at first but read too close to Spain's clay, so it became `hatch-lines`.
- **Values:** the committed series matches silver exactly. Per country, min to max:

| Country | Min to max (GWh per gas day) | Note |
|---|---|---|
| NL | 587.2 to 763.6 | |
| IT | 505.8 to 699.8 | |
| PT | 173.2 to 187.4 | |
| PL | 84.8 to 190.5 | |
| BE | 91.8 to 263.8 | Rising 18 to 22 Sep |
| ES | 295.0 to 697.9 | |
| FR | 354.4 (15th) to 1,085.1 (21st) | |

  The stacked total is 2,689.8 on the 13th and 3,723.5 on the 21st.
- **Caption:** says "ten gas days … too short a window to read a trend" and "GB is left out: GIE sends it as `-`".

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Country-level rows, eight countries requested (`summary`, `facts.grain`, `what_it_is`) | endpoints.py:17; client.py:113-125, 361-381; silver `group_by(country_code)` → 8 codes × 15 each |
| Key `(gas_day, country_code)` | alsi.py:154-157 `unique(subset=["gas_day","country_code"], keep="last")`; silver has 8 rows per gas day |
| `gas_day` from `gasDayStart` | alsi.py:56-67 |
| `event_time` = gas_day 06:00 UTC, project label (`record.fields.gas_day`) | alsi.py:27-28; base.py:383-400; silver `event_time` = `2026-09-20 06:00:00 UTC` for gas day 2026-09-20 |
| `send_out_gwh` from `sendOut`, GWh | alsi.py:98; GIE README units line |
| `dtrs` not a percentage, units unconfirmed | schemas/gie.py:62-65; alsi.py:91-93, 101 |
| `dtmi_lng`, `dtmi_gwh` from `dtmi.{lng,gwh}`, units unconfirmed | alsi.py:117-123; schemas/gie.py:66-68 |
| `country_code` from `code`, `country_name` from `name` | alsi.py:103-104 |
| GB `-` placeholders stored as null | GIE README "GB Pre-Brexit"; alsi.py:134-136; bronze GB records `"sendOut": "-"`, `"status": "N"` |
| LNG inventory in the response but not in silver (`what_it_is`, `raw_feed.note`) | Bronze record keys: `inventory: {"lng": "513.53", "gwh": "3332.02"}`; field map alsi.py:95-97 expects `lngInventory`/`gasInStorage`; silver schema has no `lng_in_storage_gwh` |
| Response also carries `status`, `updatedAt`, capacity fields not kept (`raw_feed.note`) | Bronze keys `availableCapacity, contractedCapacity, coveredCapacity, gasDayEnd, info, status, updatedAt`; `output_cols` alsi.py:167-181 |
| Request URL (`raw_feed.requests`) | client.py:374-381 (`country`, `from`, `till` as `%Y-%m-%d`, `page`, `size=DEFAULT_PAGE_SIZE=300`), path `/api` (endpoints.py:11), host `sources.yaml` `gie_alsi.base_url`; bronze sidecar `request_url` `https://alsi.gie.eu/api?country=NL&from=2026-09-13&till=2026-09-22&page=1&size=300` |
| One request per country for the whole window, paged at `size=300` (`raw_feed.note`) | client.py:361-415 (no date chunking; pages until `last_page`); endpoints.py:22 `DEFAULT_PAGE_SIZE = 300`; sidecar `from=2026-09-13&till=2026-09-22`, `total_pages: 1` |
| `till` included, ingest end day fetched (`raw_feed.note`, command comment) | `runner.resolve_dates`: a bare date is midnight UTC (runner.py:479-501); client formats `end.strftime("%Y-%m-%d")` into `till`; that bronze file holds a record with `gasDayStart` 2026-09-22 |
| Transform window equals ingest window | Bronze lands under the window start date (`data_date=start.date()`, client.py:395). A transform for later days falls back to the nearest earlier partition (base.py:2337-2390), and `_filter_records_to_gas_day` keeps only that day (alsi.py:46, 189-221). Silver 13 to 22 Sep all come from partition `2026/09/13` |
| Notebook lead: relation, date column, inclusive ends, lineage dropped, order | gridflow_models `research/handles/source.py:401-445`; `_relation_name_for_dataset("lng")` → `silver_gie_alsi_lng`, date column `gas_day` (gridflow `silver/schema_manifest.py:233`); `_BITEMPORAL_EXCLUDE` drops `event_time, available_at, vintage_policy, source_run_id, dataset_version` |
| `data.gie_alsi` resolves; notebook cells read-only | `run_notebooks.py` run: 5 cells, card + df + image, no errors; the read-only guard passed after replacing `.drop(` |
| Chart alt and plot alt numbers | `series/gie/lng.json` values (above); plot PNG viewed |
| Eight rows (`record.caption`) | `gas_day eq 2026-09-20`, `order_by country_code` → 8 rows, GB all null |
| Related: `gie/storage` and `entsog/physical_flows` resolve | Build resolved both; `gie/storage` → `storage.html` → pointer to `agsi-storage.html#storage` |

## Note body corrections (canonical `30-vendors/gie/datasets/lng.md`)

1. **`gas_day` row, source field.** "`gasDayStart` / `gasDay` / `date`" became "`gasDayStart`", with the note "the only
   date field the transformer reads (`silver/gie/alsi.py:56-67`)". The code requires and parses only `gasDayStart`.
2. **`lng_in_storage_gwh` row.** Appended "**Not written:** the live response sends inventory as `inventory: {lng,
   gwh}`, which this field map does not match (`silver/gie/alsi.py:96-97`), so silver has no such column."
3. **`send_out_gwh` row, notes.** "LNG send-out" became "LNG send-out over the gas day, GWh".
4. **`injection_gwh` row.** Appended "**Not written:** the live response has no `injection` field."
5. **`lng_pct_full` row.** Appended "**Not written:** it needs `lng_in_storage_gwh`, which is absent
   (`silver/gie/alsi.py:142`)."
6. **`trend` row.** Appended "**Not written:** the live response has no `trend` field."
7. **`event_time` row.** "base transformer / Added at write time" became "derived / `gas_day` at 06:00 UTC, gridflow's
   fixed labelling convention (`silver/gie/alsi.py:27-28`, `silver/base.py:383-400`)".
8. **Modelling notes, GB.** "GB coverage may contain null numeric values" became "GB numeric values arrive as `-`
   placeholders (status `N`) and are stored as null".

I left the curl-free endpoint section, pagination and the other rows unchanged, because they match the code.

## Could not verify

- **Vendor documentation of units.** The code says ALSI's official documentation sits behind a login
  (schemas/gie.py:63, 66), so none of the units is confirmed against a vendor doc.
  - `send_out_gwh` = GWh rests on gridflow's column name and the vault README.
  - `dtrs` and `dtmi_*` rest on nothing; the page says they are unconfirmed.
  - One local observation, deliberately left off the page: `dtmi_gwh / dtmi_lng` runs 5.9 to 7.1 across these rows,
    and each country's send-out stays below its `dtrs`.
- **Meaning of `status` codes.** The codes `C`, `E` and `N` are not stated anywhere in the code. The page and note
  give no meaning; the note body names only `N` as the value GB carries.
- **ALSI's gas-day clock (hour).** It is not in the response; the response carries dates only. The page names only
  gridflow's 06:00 UTC label.
- **Whether ALSI offers terminal-level queries.** The connector never asks for them, and the page only says rows are
  country level.

## Open questions for the seat

1. **Inventory defect and the hub copy.** The hub copy in `gie.json` promises LNG terminal inventory in two places
   (`intro` and the ALSI `groups[].blurb`, "LNG terminal inventory and send-out"). Silver carries no inventory,
   so the hub overclaims until gridflow is fixed. `gie.json` is not my file; I recommend the seat edits it or holds
   that wording. The page itself says plainly that inventory is not in silver.
2. **Should the page wait for the inventory fix?** I think it can ship as is. Send-out is a real, correctly typed
   column, and the page is honest about what is missing. The seat decides.

## Template and tool problems (not worked around)

- `chart_view.x_label` renders as plain text, so backticks show literally. I first wrote
  "gas day (GIE's `gasDayStart` date)" and saw the backticks on the axis; I rewrote it without them. The build could
  reject or strip backticks in `x_label`.
- `gridflow-build` content warnings for GIE datasets say "no Pydantic class declared in gridflow.schemas.elexon". The
  message names the wrong module for a GIE dataset. This is a cosmetic build bug.
- `scripts/run_notebooks.py`'s `READ_ONLY_VERBS` rejects pandas `.drop(` (a read-only DataFrame method), which is a
  false positive. I worked around it inside my own cells by filtering first.
- My own slip, recorded for the seat: a mis-escaped path in my CDP script created a Chrome profile folder **outside**
  the scratchpad, at `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\a0012501-ff9a-440a-b654-cec67ac10bcf\scratchpadlng-cdp`.
  - Per the rules I left the profile in place. I removed the one stray empty file the slip created beside it.
  - No Chrome process is left running on that profile.

## Defects (paste as is)

- **gie_alsi/lng: LNG inventory never reaches silver.**
  - ALSI sends inventory as a nested object, `"inventory": {"lng": "513.53", "gwh": "3332.02"}` (bronze
    `gie_alsi/lng/2026/09/13/raw_20260926T174756Z_2d7fcb5d.json`).
  - `LNGTerminalTransformer.transform` maps only `lngInventory`/`gasInStorage` to `lng_in_storage_gwh`
    (`silver/gie/alsi.py:95-97`). No `lng_in_storage_gwh` column is ever written.
  - As a result, the derived `lng_pct_full` (`alsi.py:142-149`) is never written either.
  - Fix: extract `inventory.gwh` (and `inventory.lng`) like `dtmi` (`alsi.py:117-123`), then bump `DATASET_VERSION`.
- **gie_alsi/lng: schema and vault list columns the live response cannot fill.**
  - `injection_gwh` and `trend` map from `injection` and `trend`, which ALSI does not send. All 128 bronze records
    carry exactly these keys: `availableCapacity, code, contractedCapacity, coveredCapacity, dtmi, dtrs, gasDayEnd,
    gasDayStart, info, inventory, name, sendOut, status, updatedAt, url`.
  - The columns are silently absent. Either drop them from `schemas/gie.py:LNGTerminal` and `output_cols`, or map
    the fields ALSI does send.
- **gie_alsi/lng: transformer drops vendor fields a reader needs.**
  - Dropped fields: `status` (per-row `C`/`E`/`N`, where `E` appears on NL 2026-09-17, FR 2026-09-18 and IT
    2026-08-01), `updatedAt` (vendor record time), `gasDayEnd`, `contractedCapacity`, `availableCapacity` and
    `coveredCapacity` (`alsi.py:167-181`).
  - Estimated and confirmed values are indistinguishable in silver, and there is no vendor publish time, so the frame
    cannot be vintaged by vendor time.
- **vault `20-domain/concepts/gas-day.md` is stale.** It says GIE `gas_day` is stored "no derived UTC timestamp".
  gridflow now stores `event_time` = `gas_day` 06:00 UTC (`silver/base.py:383-400`, `silver/gie/alsi.py:27-28`).
  The same docstring notes the conflict with the DST-aware vault page (P0.6-DOC-1).
- **front-end `site/hifi/data/gie.json` overclaims inventory.** `intro` and the ALSI group blurb say "LNG terminal
  inventory"; silver `gie_alsi/lng` has no inventory column until the first defect above is fixed.
