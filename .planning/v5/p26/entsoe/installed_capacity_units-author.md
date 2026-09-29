# installed_capacity_units: writer report

Writer: Opus 5.5 (high), 2026-09-29. Page: `entsoe/installed_capacity_units` (group 4, port 9832).

## Status

- Canonical note: `vault-p26-entsoe/30-vendors/entsoe/datasets/installed_capacity_units.md`. It has a `page:` block and body corrections. The mirror `vault/entsoe/installed_capacity_units.md` is byte-identical (checked with `cmp`), and it was previously LF against a CRLF canonical.
- Artefacts, all written by their tools:
  - `site/hifi/data/series/entsoe/installed_capacity_units.json` (`gridflow-distil`, `spec_origin: vault`);
  - `samples/entsoe/installed_capacity_units.json` (`gridflow-sample`);
  - `notebooks/entsoe/installed_capacity_units.json` (`scripts/run_notebooks.py`: 5 cells, no errors, no image).
- Nothing to retire: there was no staged spec and no authored override.
- `gridflow-build --only entsoe/installed_capacity_units`: wrote the page with no errors. Its three content warnings belong to other datasets (`total_nominated_capacity`, `redispatching_cross_border`, `countertrading`).
- `detect.mjs --json`: one finding only, `em-dash-overuse`, advisory. It counts 92 hits, all from the `--` padding in rendered EIC codes. The page has 0 real em dashes, 0 arrows and 0 middots.
- Screenshots at 1440, 1024, 768 and 390:
  - checked closed, and open (notebook drawer open, frame unfolded);
  - 390 was checked through a 390 px iframe;
  - nothing is clipped or overlapping.
- Dark mode: the site has no dark-mode rules (no `prefers-color-scheme` or `color-scheme` in any stylesheet), so there is one theme.
- Screenshot files are in the scratchpad under `icu-shots/`.
- Headless Chrome sometimes stopped painting partway down a tall capture. That is a tool artefact: a retry, or a shorter capture scrolled to a fragment, painted fully.

## The table in one paragraph

A71/A33 is ENTSO-E's list of production units per bidding zone for one year, one `P1Y` point per unit.

- **Why every row is on 31 Dec 2025.** The 2026 document's `time_Period` runs from 2025-12-31T23:00Z to 2026-12-31T23:00Z. So `timestamp_utc` is 23:00 UTC on 31 December, which is midnight CET on 1 January 2026.
- **Why 7,668 rows.** gridflow asks for one UTC day per zone (`client.py:162`, `day_subwindows`). Each one-day reply we hold carried the whole year document. The local silver has 12 ingest days (1 to 5 Aug and 8 to 14 Sep 2026, fetched on 16 Aug and 15 Sep) × 639 units, which is 7,668.
- **Areas.** Six zones: GB 230 units, FR 165, DE-LU 129, NL 51, IE-SEM 33, BE 31.
- **Types.** 18 PSR types appear: B01 to B06, B08, B10 to B14, B16 to B20 and B25.
- **The key.** The transformer dedups on `(timestamp_utc, area_code, unit_mrid)` within one transform day. Across days a unit repeats 12 times. `(timestamp_utc, area_code, unit_mrid, published_at)` is unique on all 7,668 rows, and that is the page's `record.key`.

## How this table differs from its neighbours

| Table | Document | One row is | Key | Capacity? |
|---|---|---|---|---|
| `installed_capacity` | A68/A33 | zone × PSR type × year (× fetch) | `(timestamp_utc, area_code, production_type)` | Zone total per type. Local silver has no GB or IE rows. DE-LU sums to about 295 GW, against 64 GW in this table's DE-LU list. |
| **`installed_capacity_units`** | A71/A33 | production unit × year × fetch | `(timestamp_utc, area_code, unit_mrid)` per day, plus `published_at` across days | Per unit, MW |
| `generation_units_master_data` | A95 (`Implementation_DateAndOrTime`) | unit | `(area_code, unit_mrid)` | None. It has implementation dates and no time axis. All 639 A71 unit EICs appear among its 660 (a measured fact, kept off the page). |

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Document A71, process A33, `in_Domain` (facts.vendor, request) | `connectors/entsoe/endpoints.py:97-102`. Bronze meta `request_params` (for example `2026/08/01/raw_20260816T134341Z_c6fc9fc5.meta.json`). |
| Request URL and parameter order: `documentType, periodStart, periodEnd, in_Domain, processType, securityToken` (raw_feed.requests) | `client.py:283-306`. Bronze meta `request_url`. |
| One GET per zone per UTC day, six zones (raw_feed.note) | `client.py:162` `day_subwindows`. `DEFAULT_ZONES = [GB, FR, NL, BE, DE-LU, IE-SEM]` at `endpoints.py:395`. |
| "a one-day request returned the whole year" (facts.cadence, raw_feed.note, what_it_is) | Bronze: every one of the 72 replies has `time_Period` from 2025-12-31T23:00Z to 2026-12-31T23:00Z, for requests `periodStart=YYYYMMDD0000`, `periodEnd`= the next day (probe `icu_p2.py`). |
| One `P1Y` point per unit (cadence, fields.resolution, fields.capacity_mw) | Bronze: every TimeSeries has 1 Period and 1 Point, `resolution` P1Y. Silver `resolution` is P1Y on all rows. |
| `timestamp_utc` = period start: 23:00 UTC on 31 Dec 2025 is midnight CET | `parsers.py:527-528` `_advance_calendar` (position 1 gives the start). Bronze `timeInterval.start`. Winter CET = UTC+1. |
| Ingest end excluded; transform end included (commands) | `--end` is parsed to midnight UTC (`pipeline/runner.py:499` `_parse_window_bound`). `day_subwindows` covers `[start, end)` (`utils/time.py:123-137`). The transform end is inclusive (`cli.py:412-414` comment, "transform date iteration is inclusive"). |
| PSR code labels in the key: B04 fossil gas, B02 lignite, B03 coal-derived gas, B05 hard coal, B06 oil, B10/B11/B12 hydro, B13 marine, B14 nuclear, B16 solar, B17 waste, B18/B19 wind, B20 Other, B25 energy storage, B08 peat | Approved `actual_generation` note, "PSR codes": ENTSO-E code list v36r0, plus the Postman `psrType` list for B02, B03, B06, B20 and B25. **B08 Fossil Peat comes only from entsoe-py `PSRTYPE_MAPPINGS` (de facto).** The body of this note now points there. The "Other ... undocumented" wording matches the approved `actual_generation` key. |
| A33 = year ahead (facts.vendor) | `silver/entsoe/_event_window.py:174-175` ("A33 year-ahead installed capacity per production unit"). |
| Notebook lead: relation `silver_entsoe_installed_capacity_units`, both ends included, lineage dropped | `source.py:426-451`, `_get_method_registry.py:94-96`, `schema_manifest.py:77-85`. |
| Rows without `unit_mrid` are dropped (fields.unit_mrid) | `silver/entsoe/installed_capacity_units.py:68,73` |
| `published_at` = response `createdDateTime`, a fetch-time stamp (fields.published_at) | `installed_capacity_units.py:88`, `_published_at.py`, seat ruling #39. Bronze `createdDateTime` is 0 to 1 s after the meta `fetched_at`. |
| Each ingest day holds a full copy, told apart by `published_at` (what_it_is, notebook.lead) | 12 files × 639 rows. Key4 unique: 7,668 of 7,668. `published_at` has 62 distinct values. |
| A production unit can hold several generating units; gridflow keeps the production unit only (what_it_is) | Bronze nests `MktPSRType/PowerSystemResources` (GB: 382 generating units in 230 production units). `parsers.py:345-348` reads only `psrType`. |
| `MAW` is the unit (fields.capacity_mw) | Bronze `quantity_Measure_Unit.name` is `MAW` on every series. |
| Chart: 639 units after dedup to the latest fetch; values 167 / 166 / 133 / 70 / 50 / 26 / 14 / 7 / 6 (alt, title) | Committed series: `rows_used` 639, `duplicates_dropped` 7,029. The latest fetch for every zone was 2026-09-15 20:08 to 20:09 UTC. |
| Khaki only for B20 "Other"; unpainted hatches for hydro, coal, oil and the smaller types; no non-additive sum | Spec: `aggregation: count`, with `other` mapped from B20 only. |
| Eight rows show Seraing at 470 then 300 MW (record.caption) | Committed sample. Bronze confirms `22W201806271---D` is 470 in all five 16 Aug fetches and 300 in all seven 15 Sep fetches. It is the only unit that differs. |
| `query()` filters on `timestamp_utc` with both ends inclusive, drops lineage, keeps `published_at` (notebook.lead) | `schema_manifest.py:170` date column. `_get_method_registry.py:94-96`. `BITEMPORAL_EXCLUDE` at `schema_manifest.py:77-85` has no `published_at`. |
| Related: `ABRBO` recurs in BM unit IDs | `samples/elexon/bmunits_reference.json` has `T_ABRBO-1` / `ABRBO-1`. |
| Related: many `actual_generation_units` `unit_mrid` codes appear here | 162 of its 175 unit EICs overlap (a local measure, so the page says "many", not a number). |

## Choices

- **View.**
  - The chart is a bar count of production units per `psrType`, grouped into 9 series: all six zones, the 2026 document, and only the latest fetch (dedup on `(area_code, unit_mrid)` by `published_at`).
  - It is not a MW sum. A sum would headline GB's list as 2026 installed capacity, which is dubious (see Defects).
  - There is no time axis, so no trend is implied.
  - The title and caption date the capture (15 September 2026), following the `bmunits_reference` precedent.
- **Frame.** The eight rows are one unit across eight fetches, not eight units, because that shows the two facts a reader must know: rows repeat per fetch, and the year document was revised between fetches. `published_at` and `capacity_mw` print first.
- **Notebook.** It uses `query()` rather than `sql()`: the table has a manifest date column, and the cell shows the dedup a reader needs.

## Body corrections (canonical note, smallest spans)

1. **Overview, "Updated yearly."** No evidence. Replaced with "One `P1Y` point per unit in the responses received (2026-09-29 check; no vendor update cadence verified)."
2. **Live verification, "ABRBO for Aberthaw".** Wrong. ABRBO is `B18` (wind offshore) in the bronze. Aberthaw B is a separate unit, `ABTHB`, `B05`. The gloss is now cited to bronze.
3. **Bronze granularity, "one file per (zone, year-window)".** Wrong. It is one file per zone per requested UTC day (`client.py:162`), each holding the whole year document.
4. **Silver dedup key.** Added that it applies within one transform day only (`installed_capacity_units.py:74-77`), and that copies repeat across days.
5. **Point-in-time field, `ingested_at`.** Stale. It is now `published_at` (`installed_capacity_units.py:88`). `ingested_at` is the transform time (`:79-83`).
6. **Silver schema.** Added the `published_at` row, and the 2025-12-31T23:00Z note on `timestamp_utc`.
7. **Silver sample.** It had `timestamp_utc` 2026-01-01T00:00Z, `capacity_mw` 100.0 and resolution `"365 days, 0:00:00"`. These are now 2025-12-31T23:00Z, 99.0 and `"P1Y"`, and `published_at` is added.
8. **Known issues, "Use a yearly window, `max_query_days: 365` matches".** Wrong. The connector splits into days regardless, so a year window makes about 365 identical requests per zone. Replaced with "One day is enough".
9. **Known issues, "DRAXX-1".** Silver holds the production unit `DRAXX`. The `-1` names belong to the dropped generating units.
10. **Silver schema, `production_type`.** Added a pointer to the PSR code sources in the `actual_generation` note, and the codes the 2026 document uses.
11. **Known issues, two bullets added.**
    - The year document changed between fetches (Seraing, 470 to 300 MW).
    - The parser drops `highVoltageLimit`, `nominalP` and the `PowerSystemResources` children (`parsers.py:345-348`).

Left as found and unverified: the API table's "Historical depth: yearly snapshots from ~2014", "Publication lag: yearly publication", and "366 KB observed for GB" (358,845 bytes in our Sep fetch). `last_verified` was not changed.

## Unverified

- B08 = peat rests on entsoe-py's mapping only; no ENTSO-E document we hold lists it.
- `record.key` is `[timestamp_utc, area_code, unit_mrid, published_at]` on purpose, which differs from the transformer's dedup key. The checker should confirm the reasoning: the dedup key holds within one transform day, but across days it repeats 12 times.
- Whether ENTSO-E revises the A71 document during the year as a rule, or whether Seraing is a one-off. We saw one change between two fetch dates.
- Whether a one-day request always returns the whole year. It did in all 72 replies we hold. The page scopes this as "returned" and "the replies received".
- The vault note's history depth ("from ~2014") and "yearly publication": no vendor quote.

## Open questions for the seat

1. **GB's 2026 list looks stale** (domain truth, not in the repo, so nothing is said on the page). GB's A71 document for 2026 lists:
   - under `B05` hard coal: `LOAN` 2,400 MW, `RATS` 2,020, `FIDL` 1,961, `FERR` 1,960, `COTPS` 2,008, `EGGPS` 2,100, `RUGPS` 976, `WBUPS` 2,012;
   - under `B14` nuclear: `OLDS`, `WYLF`, `HUNB`, `DNGB`, `HINB`;
   - under `B11` run-of-river: `DINO` 2,016 and `FFES` 384, which by name look like pumped storage.

   These names suggest a pre-2020 register that ENTSO-E still serves for 2026. GB also has 104 of its 230 units under 100 MW, down to 1 MW (`VPI-TRAD`).

   Recommended ruling: yes, open a research unit with these named unknowns: when GB's A71 was last updated, and whether GB still submits it. Keep the page as written: it counts units, dates the capture, and says "Types are as ENTSO-E sends them".
2. Should the page ever show a MW view? Not until question 1 is answered.

## Template problems (seat's files; not worked around)

- At 390 the notebook header clips the long `.ipynb` name (`installed_capacity_uni…`). This is known, per ruling #39.
- None new.

## Defects (pasteable)

- **gridflow, ENTSO-E connector (BACKLOG 13): year documents are fetched once per day.**
  - `client.py:162` splits every window into UTC-day requests, including A33 year-ahead datasets (`installed_capacity_units`, and likely `installed_capacity`, `load_forecast_yearly` and `forecast_margin`).
  - Each one-day request for A71/A33 returns the whole year document, so bronze and silver hold one full copy per ingest day. Our silver has 12 copies of 639 units (7,668 rows); a one-year backfill would make about 365 requests per zone and 365 copies.
  - `max_query_days: 365` in `sources.yaml` has no effect on this.
  - Readers must dedup on `(area_code, unit_mrid)` by `published_at`, and a naive capacity sum is inflated 12 times.
  - Fix direction: for horizon datasets, request once per year, or collapse copies in silver.
- **gridflow, silver transformer (BACKLOG 13): the dedup key does not span days.** `installed_capacity_units.py:74-77` dedups `(timestamp_utc, area_code, unit_mrid)` within one transform day only. Across days, repeated fetches of the same year document sit side by side with no key column except `published_at`.
- **gridflow, parser (BACKLOG 13, low): A71 fields are dropped.** `parse_timeseries_xml` drops, for A71:
  - `production_PowerSystemResources.highVoltageLimit` (kV);
  - `nominalIP_PowerSystemResources.nominalP`;
  - the nested generating units (`PowerSystemResources` mRID, name, nominalP): 382 in GB's 230 production units.

  The generating-unit names (for example `ABRBO-1`) are the likelier join key to Elexon BM units (`T_ABRBO-1`).
- **gridflow, transformer (cosmetic): `fill_null("unknown")` never fires.** `installed_capacity_units.py:70` fills a null `production_type` with `"unknown"`, but the parser returns `""` for a missing `psrType` (`parsers.py:269`). The same applies to `unit_name` and `unit_mrid`, where the `""` checks work.
- **Vendor data, research item (not a code defect): GB's A71/A33 document for 2026 looks stale.** It lists stations that appear to be retired, and pumped-storage names under `B11`; see open question 1. The label is held; the page makes no claim.
- **Vault note (fixed in this branch):** the ABRBO/Aberthaw gloss, the silver sample values, the bronze granularity, the point-in-time field, and the "yearly window" advice (see Body corrections).
