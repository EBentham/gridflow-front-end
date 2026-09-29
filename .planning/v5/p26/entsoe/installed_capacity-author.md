# entsoe/installed_capacity: author report

Writer: Opus 5.5 · high, 2026-09-29. Port 9831.

## Files touched

- Canonical note: `vault-p26-entsoe/30-vendors/entsoe/datasets/installed_capacity.md` (the `page:` block plus body corrections; CRLF kept, 0 LF-only lines).
- Mirror: `p26-entsoe/vault/entsoe/installed_capacity.md` (`cmp` identical).
- Artefacts, all in `p26-entsoe/site/hifi/data/`:
  - `series/entsoe/installed_capacity.json` (`gridflow-distil`, `spec_origin: vault`);
  - `samples/entsoe/installed_capacity.json` (`gridflow-sample`);
  - `notebooks/entsoe/installed_capacity.json` and `installed_capacity-5.png` (`scripts/run_notebooks.py`).
- Built page: `p26-entsoe/site/hifi/data-sources/entsoe/installed_capacity.html`.
- No staged spec and no authored override existed, so nothing was deleted.

## Gates

- **Build:** `gridflow-build --only entsoe/installed_capacity` wrote the page with no errors.
- **Detector:** `detect.mjs --json` returns one finding, `em-dash-overuse` with `advisory: true`.
  - It counts the `--` padding in the EIC codes (the frame's `10YNL----------L`).
  - The page has 0 real em dashes, 0 `→` and 0 middle dots. This finding is accepted under ruling #39.
- **Local-data grep:** the rendered text has no hits for `locally`, `held`, `our`, `since 20..`, `N rows/days`, `% of`, `live`, `real-time` or `now`.

## Coverage: what the silver actually is

- **One date.**
  - Every row has `timestamp_utc = 2025-12-31 23:00 UTC`.
  - The response's `time_Period.timeInterval` and each `Period/timeInterval` run from `2025-12-31T23:00Z` to `2026-12-31T23:00Z` with `resolution` `P1Y` and a single `position` 1.
  - So the row is the installed capacity for the year 2026, stamped at the year's start: midnight CET on 1 January 2026.
  - Parser: `_advance_calendar(start, 1, "P1Y")` returns `start` (`parsers.py:87-91`).
- **It is a single annual snapshot.** The page never shows or implies a trend.
- **Areas.**
  - gridflow requests six zones (`DEFAULT_ZONES`, `endpoints.py:395`): GB, FR, NL, BE, DE-LU and IE-SEM.
  - Four send data: DE-LU (20 types), NL (20), FR (15) and BE (12).
  - GB and IE-SEM return the acknowledgement: "No matching data found for Data item INSTALLED_GENERATION_CAPACITY_AGGREGATED_R3 [14.1.A]".
- **PSR types.** 21 distinct codes: B01 to B20 and B25.
  - DE-LU sends no B14 row. It sends B07, B08 and B13 as 0.0.
  - NL sends 0.0 for ten codes but has no B25 row.
  - BE and FR omit codes rather than send 0.
  - The page shows this as "A type may come as 0 MW or not at all", with the DE-LU example; the notebook's pivot output shows the NaN versus 0 difference.
- **Unit.** `quantity_Measure_Unit.name` is `MAW`, which is MW. The schema docstring says "Total installed capacity in MW" (`schemas/entsoe.py:175-180`).
- **Doubles.**
  - There are 67 distinct `(timestamp_utc, area_code, production_type)` keys.
  - Each key appears in all 12 daily silver files, with identical `capacity_mw` every time (0 keys have differing values).
  - Cause: the connector sends one request per zone per UTC day (`client.py` `fetch`, `day_subwindows`). Each one-day request returns the whole-year document.
  - The transformer's `unique(... keep="last")` (`installed_capacity.py:74`) acts within one transform day only.
  - Within a file there are no duplicate area and type pairs.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Document A68, process A33 (`facts.vendor`) | `endpoints.py:94-96` `EntsoeDocType("A68","A33",...,domain_style="in_domain")`; bronze `<type>A68</type>`, `<process.processType>A33</process.processType>` |
| One `P1Y` point per year, as sent (`facts.cadence`) | Bronze `<resolution>P1Y</resolution>` with one `<Point>`; silver `resolution` is only `P1Y` |
| `sources.yaml` schedules weekly fetches | `config/sources.yaml:244-248` `schedule: "weekly"` |
| Grain: one row per year, zone and type, per silver file | Transformer dedup key (`installed_capacity.py:74`); 12 copies of each key across files (Polars `group_by(key).len()` gives 12 for all 67) |
| Key `[timestamp_utc, area_code, production_type]` | `installed_capacity.py:74` |
| 2026 figure stamped at 23:00 UTC on 31 Dec 2025, which is midnight CET (`what_it_is`, `record.fields.timestamp_utc`, chart caption) | Bronze `<start>2025-12-31T23:00Z</start><end>2026-12-31T23:00Z</end>`; silver has one unique `timestamp_utc` |
| Six zones requested; GB and IE-SEM return no-data acknowledgements | `endpoints.py:395`; bronze 2026/09/14 `raw_20260915T200825Z_2a96083c.xml` (GB) and `raw_20260915T200833Z_f7677597.xml` (IE-SEM) are `Acknowledgement_MarketDocument` Reason 999 |
| DE-LU sends B07 as 0 but no B14 | Notebook pivot output (B07 row 0.00 for DE-LU, B14 NaN for DE-LU); silver pivot |
| Raw request URL and parameter order | Bronze `.meta.json` `request_url` for 2026/09/14 DE-LU: `documentType=A68&periodStart=202609140000&periodEnd=202609150000&in_Domain=10Y1001A1001A82H&processType=A33&securityToken=...`; `client.py:283-310` builds it in this order |
| One GET per zone and UTC day; each one-day request returned the whole year's document | `client.py:152-165` (`day_subwindows`); every bronze GL document for Aug 1-5 and Sep 8-14 carries the 2025-12-31T23:00Z/2026-12-31T23:00Z interval |
| Ingest `--end` is exclusive and transform `--end` inclusive | `day_subwindows` docstring (`utils/time.py:133-140`, "An end that falls exactly at midnight excludes that date"); transform as on the approved ENTSO-E pages |
| Chart values: solar 104,029.51 … other 2,030.47; sum 294,940.88 MW | Committed series `x`/`values`; hand sum of the silver DE-LU rows matches |
| Grouping is additive | Each PSR code is a disjoint technology within one zone and one year; one copy is kept per key (`dedup`, `duplicates_dropped: 220`) before codes are summed |
| `area_code` comes from `inBiddingZone_Domain.mRID` | Bronze TimeSeries carries `inBiddingZone_Domain.mRID`; `parsers.py:289-297` maps it to `in_domain`; transformer renames it to `area_code` (`installed_capacity.py:62`) |
| `production_type` is the PSR code from `MktPSRType/psrType` as sent | `parsers.py:347-348`. No "unknown" clause: the parser initialises `production_type = ""` (`parsers.py:269`) and emits it as is (`:448`), so the transformer's `fill_null("unknown")` (`installed_capacity.py:69-72`) cannot fire on an absent code |
| PSR names in the key (B25 energy storage, B02 lignite, B03 coal-derived gas, B06 oil and the rest) | Vendor code lists cited in `actual_generation.md:248`: ENTSO-E code list v36r0 and ENTSO-E's Postman `psrType` list, which has B25 "Energy storage". B07, B08 and B13 are left unnamed on the page |
| `capacity_mw` is MW (`MAW`) from `quantity` | `parse_timeseries_xml(..., value_tag="quantity")` (`installed_capacity.py:43`); bronze `MAW` |
| `published_at` is response `createdDateTime`, a fetch-time stamp | `installed_capacity.py:85` (`with_published_at`); bronze `createdDateTime` 2026-08-16T13:43:06Z versus meta `fetched_at` 13:43:06.0; ruling #39 |
| Notebook: `query()` on `timestamp_utc`, whole UTC days, both ends included, lineage dropped | `gridflow_models .../source.py:401-445`; `_get_method_registry.py:62-92`; `schema_manifest.py:169` (date column `timestamp_utc`) |
| Frame: NL, eight codes, one copy each, B02 and B10 sent as 0 | Sample JSON rows (B02 0.0, B10 0.0) |
| DE-LU sends no nuclear (B14) row (chart caption) | Silver has no DE-LU B14 row; notebook pivot shows NaN |
| `plot_alt` values | Notebook plot and pivot: DE-LU B16 104,029.51; DE-LU B19 67,922.93; FR B14 62,990; BE maximum is B16 11,683 |

## Body corrections (canonical note)

1. **Granularity:**
   - Was: "One file per (zone, year-window)."
   - Now: one file per zone per requested UTC day, and each day's reply carries the whole-year document (`client.py` `fetch`, `day_subwindows`).
2. **Bronze sample `businessType`:**
   - Was: `B01`.
   - Now: `A37`, as every bronze GL document sends it.
3. **Bronze sample `quantity`:**
   - Was: `9000`.
   - Now: `104029.51`, the real DE-LU B16 value in `raw_20260915T200831Z_7c380e27.xml`.
4. **Point-in-time field:**
   - Was: "none".
   - Now: `published_at`, the response `createdDateTime`, a fetch-time stamp (`installed_capacity.py:85`).
5. **Silver schema table:** added a `published_at` row, which the transformer outputs but the table lacked.
6. **Silver sample:**
   - `timestamp_utc`: `2026-01-01T00:00:00+00:00` becomes `2025-12-31T23:00:00+00:00`.
   - `capacity_mw`: 9000.0 becomes 104029.51.
   - `resolution`: `"365 days, 0:00:00"` becomes `"P1Y"`.
7. **Known issues:**
   - Removed: "Use a yearly window, P1Y resolution means short windows return EMPTY". Bronze shows one-day windows returning the full document.
   - Added: the one-day-window fact, and that the dedup key holds within one file only.

## Not verified

- The vault's "Historical depth ~2014 onwards" and "Publication lag: yearly publication, around start of year". Neither is quoted from a vendor document, so neither is used on the page. There is no `history` fact.
- What B20 "Other" and B25 "Energy storage" contain. The key says B20 is undocumented. B25's name is evidenced by the Postman `psrType` list cited in `actual_generation.md:248`, but not what it covers.
- Whether a request for a 2025 day would return the 2025 document. Local silver holds only 2026, so the page states nothing about other years.
- **Dark mode.** The site has no dark theme: no `prefers-color-scheme` or `data-theme` rule in `tokens.css`, `theme.css` or `site.js`. The "dark" shots render the same as light, so light and dark were both checked, trivially.

## Open questions

1. **IE-SEM (`10Y1001A1001A59C`).** It returns no A68 data. Is that the right domain for Ireland's installed capacity, or does ENTSO-E publish it under another EIC? This needs research; the page states only what came back.
2. **Should the connector request A68 once per year instead of once per zone per day?** Today a 7-day ingest fetches the same year document 7 times per zone and writes 7 identical silver files.
3. **Is the lead chart area right?** It is DE-LU, matching `actual_generation`'s chart so load factors line up. FR (nuclear-led) would be the other obvious choice.

## Template problems

- **Bar-label clipping.** The bar-chart category label column is fixed-width. At 390 a 28-character label ("Oil, waste, other renewables") clipped at the left edge. I fixed it on my side by shortening the labels to "Oil, waste, others" and "Coal and lignite". The template could wrap or truncate long category labels.
- **Key code line indent.** In the key, a long code list wraps onto its own line with a small leading indent (" B06, B09, …"). This is cosmetic.
- **Notebook filename clip at 390.** The filename (`installed_capacity.ip…`) clips at 390. This is the known issue the seat is fixing (ruling #39); I left it.
- **Headless paint artefact.** Shooting with a window much taller than the page (8,000 px at 1440, page about 3,950 px) left everything below about 1,700 px unpainted. Matching the window height to the page fixed it. This affects the process, not the page.

## Screenshots

`scratchpad/ic-shots/`:
- `1440-light.png`, `1440-dark.png`, `1024-light.png`, `1024-dark.png`, `768-light.png` and `768-dark.png`;
- `390-light.png`, a 390 px iframe inside a 500 px window.

Zooms: `z768chart.png`, `z390chart.png`, `z390key.png` and `z390misc.png`.

**Frame:** the template has no unfold control. The frame folds statically behind the `…` column, so only the folded state exists.

**Notebook drawer:** I opened it ("Open the demo notebook") in the browser pane and checked it numerically, because pane screenshots come back blank.
- At 1440: no element off screen or clipped.
- At 390: the only clip is the `nb-tab` filename (a scrollWidth of 218 in a 207 px tab), the known seat item. The document has no horizontal scroll (`scrollWidth` 390), and the plot image is 300 px wide.

After the label fix, nothing is clipped or overlapping at any width apart from the known notebook filename clip.

## Defects

- **[vault, fixed here] Wrong window advice.** `installed_capacity.md` said short windows return EMPTY. Bronze shows one-day windows (for example `periodStart=202608010000&periodEnd=202608020000`) returning the full 2026 `P1Y` document for FR, NL, BE and DE-LU.
- **[vault, fixed here] Stale samples.**
  - Bronze: `businessType` B01 should be A37; `quantity` 9000 is not a real value.
  - Silver: `timestamp_utc` should be 2025-12-31T23:00Z, not 2026-01-01T00:00Z; `resolution` should be "P1Y", not "365 days, 0:00:00".
  - Schema: `published_at` was missing from the table and the point-in-time line.
- **[gridflow, inefficiency] Repeated year document.** `installed_capacity`, with ENTSO-E chunking by day (`client.py` `fetch` via `day_subwindows`), re-requests the identical A68 `P1Y` year document once per zone per UTC day. Every daily silver file repeats all rows, and dedup (`silver/entsoe/installed_capacity.py:74`) acts within one file only. Readers must drop duplicates across files. Candidate for gridflow BACKLOG and the vault remediation page.
- **[gridflow/research] IE-SEM returns nothing.** IE-SEM (`10Y1001A1001A59C`) answers A68/A33 with Ack 999 "No matching data". It is unknown whether this is the wrong EIC for this data item or a vendor gap. Open a research unit.
- **[gridflow, minor dead code] `unknown` fill never fires.** In `silver/entsoe/installed_capacity.py:69-72`, `fill_null("unknown")` on `production_type` cannot fire. `parse_timeseries_xml` initialises `production_type = ""` (`connectors/entsoe/parsers.py:269`), so a TimeSeries with no `MktPSRType` lands as an empty string, not null and not `unknown`. No such row exists in the local data.
- **[gridflow, seat item already open] Wrong docstring.** The `silver/entsoe/_published_at.py` docstring calls `createdDateTime` a forecast issue time; it is a fetch-time stamp (ruling #39).
