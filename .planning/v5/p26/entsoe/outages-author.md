# entsoe/outages (family): author report (writer, port 9836)

**Verdict: HOLD recommended for the whole family page.** The lead's silver (`entsoe/outages_generation`) cannot carry an honest chart, frame or notebook:

- it repeats every outage in every daily file it overlaps;
- it stamps every point after the first in hours instead of minutes (the source of the 2069 dates);
- it drops the period end, the document id, the revision and the status, so cancelled outages cannot be told apart;
- its dedup collapses different documents and generation units;
- the meaning of `unavailable_mw` is unverified, and the bronze reads as *available* MW.

Three of the four other members share most of these defects. The fourth, consumption, is clean in shape but is one DE-LU curve at 0 or 35 MW.

Following the GIE `unavailability` precedent, I wrote **no `page:` block and no artefacts**. The five notes' bodies are corrected and mirrored byte for byte. `gridflow-build --only entsoe/outages_generation` writes `data-sources/entsoe/outages.html (blank)` with exit 0, and `detect.mjs --json` returns `[]`.

Sources: gridflow `master` @ `2822d38`; local silver and bronze under `C:\gridflow-data\{bronze,silver}\entsoe\outages_*` (read only). Scratch scripts are in `scratchpad/outages/` (`a1.py`, `b1.py` to `b8.py`). `b1.py` parses every outage bronze XML directly with lxml into `bronze_periods.parquet`. `b5.py`, `b7.py` and `b8.py` run the real transformers' `read_bronze` and `transform` in memory; they never call `run()` and write nothing.

## 1. What one row is, and what the coverage dates are

**One silver row is one declared `<Point>` of one outage document's period, as fetched on one day.** It is not one outage and not one observation.

- **Outage document.** Each document (root `mRID`, `revisionNumber`, `docStatus`, `createdDateTime`) has exactly one `TimeSeries` (its `mRID` is always "1": 6,661 of 6,661 parsed periods) with exactly one `Available_Period`. The offshore member uses `WindPowerFeedin_Period` instead.
- **Points.** A period carries 1 to 328 points. `curveType` is `A03` (a step curve), resolution `PT1M`, and position *p* means minute *p − 1* from the period start.
- **What silver keeps.** Silver keeps `timestamp_utc` = the point's start and the point's quantity. It keeps no period end, so how long the last step lasts is lost.
- **Consumption is the exception.** It is `PT15M` with one point, so the parser's `A03` forward-fill (`parsers.py:575-601`) expands it to one row per 15 minutes.

| Member (brief's numbers) | Files (daily partitions) | What the dates are |
|---|---|---|
| `outages_generation`: 11,011 rows, 2015 to 2069 | 13, 8 to 20 Sep 2026 | Position-1 rows are period starts, from 2015-11-15 (IRNPS-2, period to 2049, `A09` cancelled). Every later position is mis-stamped by the 1-hour fallback, up to 2069-06-26 (Emsland B, position 381,181, period ending 2026-12-19). The true last point is 2026-09-24 22:00. Period ends (not in silver) run to 2099-12-31. |
| `outages_production`: 3,551 rows, 2024 to 2077 | 12: 1 to 5 Aug, 8 to 14 Sep 2026 | Period starts from 2024-12-31 23:00. 2077 is the same mis-stamp; the true last point is 2026-11-07. |
| `outages_consumption`: 1,738 rows, 1 Aug to 20 Sep | 18: 1 to 5 Aug, 8 to 20 Sep 2026 (gap 6 Aug to 7 Sep) | Real 15-minute points. DE-LU returned one document per request day whose period is exactly that UTC day (96 rows), 0 MW in August and 35 MW in September. NL returned one 2.5-hour document on 3 Aug (10 rows). GB, FR, BE and IE-SEM always returned Ack 999. |
| `outages_transmission`: 3,981 rows, 2025 to 2052 | 12: 1 to 5 Aug, 8 to 14 Sep 2026 | Starts from 2025-01-11. 2052 is the mis-stamp; the true last point is 2026-11-13. |
| `outages_offshore_grid`: 4 rows, 16 Sep | 4, 22 to 25 Sep 2026 | **One** outage: NL "Borssele Alpha-Zeeuwse Kust Landstation 220kV Zwart", unplanned `A54`, period 2026-09-16 15:14 to 2026-09-25 09:00, one point 50.71 (`nominalP` 376). It was fetched on 4 days, giving 4 identical rows. |

## 2. Reproductions

### 2a. Repetition across daily files (GIE's failure, different cause)

The connector sends one request per zone (or zone pair) per UTC day (`client.py:162-163`, `DEFAULT_ZONES` GB, FR, NL, BE, DE-LU, IE-SEM at `endpoints.py:395`). It files each response under the request's start date (`client.py:312`). ENTSO-E returns every outage overlapping the requested day.

The outage transformers are exempt from the event-window trim ("open-ended revision horizon, never trimmed", `silver/entsoe/_event_window.py:181-195`), and dedup runs within one day's file. So an outage is written once per day it is fetched.

| Member | Distinct document versions (mRID, rev) | Bronze fetches of them | Versions in every daily file | Silver rows / distinct business rows |
|---|---|---|---|---|
| generation | 951 (909 mRIDs, 42 with 2 revisions) | 5,423 over 13 days | 236 in all 13 | 11,011 / 1,724 |
| production | 569 (564 mRIDs) | 933 over 12 days | 12 in all 12 | 3,551 / 1,046 |
| transmission | 78 (74 mRIDs) | 281 over 12 days | 4 in all 12 | 3,981 / 678 |
| offshore grid | 1 | 4 over 4 days | 1 in all 4 | 4 / 1 |
| consumption | 20 | 20 | n/a (new document per day) | 1,738 / 1,738 |

"Distinct business rows" means every column except the pipeline columns (`data_provider`, `ingested_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version`). `query()` reads these relations on `timestamp_utc` (`silver/schema_manifest.py:180-184`), and `silver/latest_views.py` has no outage view, so a notebook would get every repeat.

### 2b. The key: does it keep versions or collapse them?

**Within one daily file it collapses them; across files it keeps everything.** Neither behaviour is revision-aware.

- **Generation**, key `(timestamp_utc, unit_mrid)` (`outages_generation.py:89`). `unit_mrid` is the **production** unit (`production_RegisteredResource.mRID`). The generation unit (`pSRType.powerSystemResources.mRID`) is never parsed.
  - On 2026-09-15, 1,142 parsed rows became 805 (= the silver file, identical on all business columns plus `published_at`: `b5.py`).
  - The 337 dropped rows sit in 285 groups. All 285 span more than one document, 41 mix cancelled and active, and 18 differ in MW. `keep="last"` picks by parse order.
  - Across the bronze, 64 of 221 production units have outages on more than one generation unit. For example, `ABTH7`, `ABTH8` and `ABTH9` under `ABTHB` share start 2019-12-13 23:00, so two of the three vanish from every file.
- **Production**, key `(timestamp_utc, area_code, unit_mrid, timeseries_mrid)` (`outages_h7.py:210`). `timeseries_mrid` is always "1", so it separates nothing.
  - Across the 12 files, 5,678 parsed rows became 3,551: 2,127 dropped in 1,288 groups. All span more than one document; 797 mix cancelled and active, and 560 differ in MW.
  - Example: on 4 August, 24 documents for "Global Tech I" with start 2026-08-04 00:00 became one row.
- **Transmission**: 3,983 parsed rows became 3,981 (2 dropped).
- **Revision and status.** No member keeps `revision_number`: the parser reads it (`parsers.py:139-140`), but no `output_cols` includes it. Generation also drops `document_mrid` and `document_status` (`outages_generation.py:102-113`).
  - Generation: 299 of 951 versions are `A09` cancelled.
  - Production: 402 of 569 versions are cancelled. Silver keeps `document_status` there (2,399 of 3,551 rows `A09`); active documents arrive with it empty.
  - `DocStatus` is never sent (`endpoints.py:54-92`), so the API returns both. `A13` was never seen.

### 2c. The `PT1M` timestamp defect

- `_RESOLUTION_MAP` (`parsers.py:35-43`) has no `PT1M`.
- `_resolve_resolution` falls back to `timedelta(hours=1)` (`parsers.py:50-51`), so `timestamp = start + (position - 1) × 1 h` (`parsers.py:530`).
- The `A03` forward-fill is skipped with a warning (`parsers.py:547-555`). That skip is why silver is not minute-expanded, and is the one lucky side of this defect.

Position 1 is correct; every later position is 60 times too late.

| Member | Versions with more than one point | Versions with a point stamped past their own period end | Latest mis-stamp | True last point |
|---|---|---|---|---|
| generation | 187 of 951 | 173 | 2069-06-26 11:00 | 2026-09-24 22:00 |
| production | 90 of 569 | 90 | 2077-01-02 23:00 | 2026-11-07 11:00 |
| transmission | 6 of 78 | 6 | 2052-10-08 03:00 | 2026-11-13 23:00 |

Fixing this by adding `PT1M` to the map would switch on the forward-fill: every outage becomes one row per minute up to the 100,000-position cap (`parsers.py:585-592`), which is about 69 days. The fix needs design (emit steps with an end column), not a map entry.

### 2d. What `quantity` means (unverified; blocks any MW chart)

gridflow renames the `<quantity>` of `Available_Period` to `unavailable_mw` (`outages_generation.py:64`, `outages_h7.py:71`). The notes say "unavailable, not available". The only source for that is the project's own spec (`quant-vault/10-projects/gridflow/specs/entsoe-connector-extension.md:108-116`), not vendor text. The bronze evidence reads the other way:

- The element is named `Available_Period`.
- Generation: `quantity < nominalP` in 950 of 951 versions (one equal), and `quantity = 0` in 551 of 951. An outage notice of "0 MW unavailable" would be empty.
- Production: `quantity < nominalP` in 567 of 569 versions (2 equal), and 0 in 121.
- Profiles step like availability. Schwarze Pumpe B (`nominalP` 755) runs 613, 463, 389, 315 ...; Niederaußem H (638) goes 0 then 536; Schkopau A (450) goes 0 then 50.

This is domain truth that is not in the repo. I did not rule it. The notes now say "unverified" with this evidence, and the Defects section opens a research item.

## 3. Why no member can carry the page now

- **Chart.** The honest event-register chart (as in `remit`: each outage once, latest revision, active only, by production type or MW in force at a stated instant) cannot be built from the lead's silver:
  - there is no `document_mrid` or `revision_number` to dedup on;
  - there is no status to drop cancellations;
  - there is no `production_type`;
  - there is no period end, so nothing can be "in force";
  - timestamps after position 1 are wrong;
  - MW is of unknown sign.

  A count of `unit_mrid` values from one file would count production units, not outages, and would mix cancelled with active. A `type: none` chart does not rescue the frame or the notebook.
- **Frame and key.** `(timestamp_utc, unit_mrid)` is not an outage identity (section 2b). Eight rows would look sound while describing a table that is not, and the guide cannot honestly say what `unavailable_mw` means.
- **Notebook.** `data.entsoe.query("outages_generation", ...)` windows on `timestamp_utc`, which includes wrong-dated rows and every cross-file repeat.
- **Other members as lead.** The family's lead and members are fixed in `site/hifi/data/entsoe.json` (the seat's file). Of the others:
  - production and transmission share every defect above;
  - offshore is a single outage;
  - consumption is structurally clean (no repeats, `published_at` equals fetch time) but is one DE-LU curve at 0 or 35 MW with unverified meaning. That is thin data, and it cannot stand for a family of event registers.

**Recommendation:** hold the whole `outages` family blank until gridflow fixes items D1 to D6 below and silver is rebuilt. After that, the `remit` pattern applies: dedup on `document_mrid` ordered by `revision_number`, drop `A09`, then count by production type, or show MW in force at a stated instant once D5 settles the sign.

## 4. Evidence table

| Claim | Evidence |
|---|---|
| One request per zone (pair) per UTC day | `client.py:162-163` (`day_subwindows`), `:211-226` (zone pairs), `:246-263` (zones); `DEFAULT_ZONES` `endpoints.py:395` |
| Bronze filed under the request start date | `client.py:312` `data_date = ... period_start` |
| Outages never trimmed to the day | `_event_window.py:95-99` (exempt set), `:181-195` (reasons) |
| Generation key and dropped columns | `outages_generation.py:89` (unique), `:102-113` (output_cols) |
| H7 keys | `outages_h7.py:131, 157-163, 186, 210` |
| `timeseries_mrid` always "1" | `b7.py`: 6,661 of 6,661 parsed periods |
| Revision parsed, not kept | `parsers.py:139-140`; absent from every `output_cols` |
| Only `BusinessType=A53`; no `DocStatus` sent; the CLI cannot pass either | `endpoints.py:59,67,75,91` (`extra_params`), optional params listed at `:60,68,77,84,92`; `client.py:567-576` forwards only `optional_params`; `cli.py:185-216` has no fetch-param option. Silver `outage_type` is `planned` on every row of generation, production, consumption and transmission |
| Offshore sends no `BusinessType` and got `A54` | `endpoints.py:79-85`; bronze doc `QBsoKMPWpXESvc4wPw7QIQ` |
| `PT1M` falls back to 1 hour; the forward-fill is skipped | `parsers.py:35-43, 50-51, 530, 547-555`; section 2c |
| `curveType` `A03`, `PT1M`, one TimeSeries, one period per document | `b2.py` over all 6,661 parsed periods |
| Silver = current code's output | `b5.py`: generation 2026-09-15 and transmission 2026-09-10 recomputed in memory, identical to the silver files (805, 373 rows) |
| `published_at` = document `createdDateTime` | `outages_generation.py:100`, `outages_h7.py:107`, `_published_at.py`. Generation: 2025-10-02 to 2026-09-21. Transmission: from 2025-11-08. Production: from 2025-10-06. Consumption: equal to the bronze file's fetch stamp to the second (`raw_20260816T133844Z` has `createdDateTime` 2026-08-16T13:38:44Z) |
| Real namespace and period element | Every bronze doc: `urn:iec62325.351:tc57wg16:451-6:outagedocument:3:0`; offshore `WindPowerFeedin_Period` (parsed via `parsers.py:408-413`) |
| Response casing for transmission | Bronze tags `in_Domain.mRID`, `out_Domain.mRID` (the request uses `In_Domain`/`Out_Domain`, `endpoints.py:76`) |
| Page builds blank, detector clean | `gridflow-build --only entsoe/outages_generation`: exit 0, `wrote: data-sources/entsoe/outages.html (blank)`, no outage warnings; `detect.mjs --json`: `[]` |
| No staged spec, override or artefacts to retire | `site/hifi/data/chart-specs/entsoe/`, `authored-pages/entsoe/` and `site/hifi/data/{series,samples,notebooks}/entsoe/` hold no `outages*` file |

## 5. Body corrections (canonical notes and mirror, byte for byte)

Notes are in `vault-p26-entsoe/30-vendors/entsoe/datasets/`, CRLF kept. Each mirror under `p26-entsoe/vault/entsoe/` passes `cmp` as identical. Front matter is untouched; there is no `page:` block. `git diff --stat`: 70 insertions and 54 deletions across 5 files. (One `sed` stripped CRLF from the lead mid-edit; I restored CRLF on all 200 lines before mirroring, and the diff shows no whole-file rewrite.)

**`outages_generation.md`** (31 lines changed):
1. Bronze granularity: added the one-request-per-zone-per-day behaviour and the re-filing of a multi-day outage (`client.py:162-163, 312`).
2. Bronze sample: namespace changed to the real `451-6:outagedocument:3:0`; resolution `PT60M` changed to `PT1M`.
3. Point-in-time: removed "No vendor `published_at` is surfaced ... dropped" (false: `outages_generation.py:100`). Now `published_at` = `createdDateTime`, the notice's creation time and not the fetch time, and it feeds `available_at`.
4. Schema `timestamp_utc`: "start + position * resolution" changed to "(position − 1) × resolution" (`parsers.py:530`). Added: one row per point, period end not kept, `PT1M` steps by an hour.
5. Schema `unit_mrid`: now "Production-unit EIC; the generation unit is not kept".
6. Schema `unavailable_mw`: now "meaning unverified".
7. Schema `resolution`: "Typically `PT60M`" changed to "ISO code as sent; `PT1M` in every document received September 2026".
8. Schema: added a `published_at` row.
9. Silver sample: `resolution` changed to `PT1M`.
10. Known issues, 30-day bullet: added that gridflow sends 1-day windows for six zones.
11. Known issues, status bullet: "The default query returns Active outages only" was false. gridflow sends no `DocStatus`, 299 of 951 versions are `A09`, and this silver cannot mark them.
12. Known issues: replaced "`unavailable_mw` is the unavailable MW" with the unverified-meaning bullet and its evidence.
13. Known issues: added four bullets (repeats across files, `PT1M` timestamps, the dedup collapse, planned only).
14. Implementation delta: "A54 reachable via override" changed to "not reachable" (`client.py:567-576`, CLI).

**`outages_production.md`** (22 lines changed): granularity (re-filing); sample namespace and `PT1M`; point-in-time `published_at`; schema `timestamp_utc`, `unavailable_mw` and `resolution`, plus a new `published_at` row; sample `resolution` "1:00:00" changed to "PT1M" (the parser emits the ISO code, `parsers.py:438,459`); "dedup by ... revision" annotated that silver has no revision column; status bullet (no `DocStatus` sent, 402 of 569 versions cancelled, empty status for active); a "Shared with A80" bullet.

**`outages_consumption.md`** (18 lines changed): sample namespace and `PT15M`; `published_at` = `createdDateTime`, equal to the fetch time to the second, with a new `mRID` each day; schema `timestamp_utc` (the `A03` forward-fill to 15 minutes, 96 rows per day); `outage_type` always planned; `resolution` `PT15M` plus a `published_at` row; sample "1:00:00" changed to "PT15M"; the 30-day bullet (gridflow sends 1-day windows); a new "one aggregate curve per request day" bullet.

**`outages_transmission.md`** (28 lines changed): granularity; sample namespace, lowercase `in_Domain.mRID`/`out_Domain.mRID` (the response casing) and `PT1M`; `published_at`; schema `timestamp_utc`, `in_area_code`/`out_area_code` source casing, `unavailable_mw`, `resolution`, plus a `published_at` row; sample "1:00:00" changed to "PT1M"; status bullet (9 of 78 versions cancelled); a "Shared with A80" bullet.

**`outages_offshore_grid.md`** (25 lines changed):
- Added the one real NL document under Live verification.
- Sample heading "hypothetical PASS shape" changed to the real element names: `businessType` `A54`, `WindPowerFeedin_Period`, `PT1M` and the namespace. "May be absent" is kept and not flipped on one document.
- Added `published_at`; schema `timestamp_utc` (`WindPowerFeedin_Period`, `parsers.py:408-413`) and `resolution`, plus a `published_at` row; sample "1:00:00" changed to "PT1M".
- `outage_type` bullet annotated; added a repeated-across-files bullet.

**Not changed:** the curl examples and API tables (the vendor request shapes are right; gridflow's own request is documented in the new lines); the vendor's "30-day window / 1-day often returns 999" claim, which is kept as a vendor claim with gridflow's actual behaviour beside it; the overviews; the modelling notes, although "capacity tightness = installed − sum(unavailable_mw)" depends on D5; history depth.

## 6. Could not verify

1. **What `quantity` means** (section 2d): available or unavailable MW. No vendor text is on file.
2. Whether ENTSO-E returns *every* outage overlapping the window, or also outages merely updated in it. The repetition pattern fits "overlapping", but I did not read that in vendor documentation.
3. The vendor claims in the notes that I left alone: "1-day windows often return 999" (gridflow's 1-day windows got 365 to 786 generation documents a day), the 200-document cap, and "adding `BusinessType` to A79 produces an Acknowledgement".
4. What `A13` (withdrawn) looks like: never seen.
5. Why production has 71% cancelled versions (402 of 569) against 31% for generation. This was not investigated.
6. Consumption's 0 MW (August) and 35 MW (September) DE-LU values: I did not verify whether they are aggregates of real notices or a placeholder curve.

## 7. Open questions for the seat

1. **Hold scope.** Hold the whole family (recommended), or split consumption out? Splitting would need an `entsoe.json` change (the seat's) and would still be a thin, single-zone page.
2. **Research item for D5** (the meaning of `quantity`) before any outage MW chart, ENTSO-E or elsewhere. The same question applies to `installed_capacity_units`, which carries `nominalP`.
3. **Target silver shape after the fix.** Once D1 to D4 land, should silver be one row per step, with `document_mrid`, `revision_number`, `document_status`, `period_start`, `period_end`, generation unit and `production_type`? That is the shape a `remit`-style event-register page needs. Should it be append-only per fetch with a latest view, like `elexon/remit`?
4. Ruling #39 (`published_at` = fetch time) is about forecast tables. For outage documents `published_at` is the notice's creation time (up to about a year before the fetch). Consumption is the exception: equal to the fetch time. The checker should not apply #39 across this family.

## 8. Template problems

None. The blank family page renders the title and all five member ids unclipped at 1440, 1024, 768 and 390 (390 in an iframe). Screenshots are in `scratchpad/outages/shots/`. Light theme only, since the page carries no content of mine.

## 9. Defects (paste into gridflow BACKLOG, remediation item 13, as is)

- **D1. ENTSO-E `PT1M` is unmapped, so every outage point after position 1 is stamped in hours.** `_RESOLUTION_MAP` (`connectors/entsoe/parsers.py:35-43`) lacks `PT1M`, and `_resolve_resolution` falls back to 1 hour (`:50-51`), so `start + (position − 1) × 1 h` (`:530`).
  - Every outage document received is `curveType` `A03` at `PT1M`.
  - Measured: generation 173 of 951 versions, production 90 of 569 and transmission 6 of 78 carry points stamped after their own period end, up to 2069-06-26, 2077-01-02 and 2052-10-08. The true last points are in September to November 2026.
  - Do not just add `PT1M`: that enables the `A03` forward-fill (`:547-601`), which would emit one row per minute up to the 100,000-position cap. Emit steps with an explicit `period_end`/`step_end` instead. Affects all five outage datasets and any other `PT1M` document type.
- **D2. The outage silver drops the outage's identity and end.**
  - No member keeps `revision_number` (parsed at `parsers.py:139-140`) or the period end (`timeInterval/end`).
  - `outages_generation` also drops `document_mrid`, `document_status`, `production_type` and `timeseries_mrid` (`silver/entsoe/outages_generation.py:102-113`). It keys on the **production** unit and never parses the generation unit (`production_RegisteredResource.pSRType.powerSystemResources.mRID`/`.name`) or `nominalP`.
  - Result: cancelled outages (299 of 951 generation versions are `A09`) are indistinguishable from active ones, and an outage's duration cannot be recovered.
- **D3. Outage dedup collapses different documents within a file, in parse order.**
  - Generation `(timestamp_utc, unit_mrid)` (`outages_generation.py:89`): on 2026-09-15, 337 of 1,142 parsed rows were dropped in 285 groups, all multi-document, 41 mixing cancelled and active. Sibling generation units (for example `ABTH7`, `ABTH8`, `ABTH9` under `ABTHB`) collapse to one row.
  - Production `(timestamp_utc, area_code, unit_mrid, timeseries_mrid)` (`outages_h7.py:210`; `timeseries_mrid` is always "1"): 2,127 of 5,678 parsed rows were dropped in 1,288 groups, 797 mixing cancelled and active, 560 with differing MW. Example: 24 documents for Global Tech I on 2026-08-04 00:00 became one row.
  - The key must include `document_mrid` (and the generation unit for A80), with revision-aware ordering.
- **D4. Outage silver repeats each outage in every daily file it overlaps, and `query()` returns the repeats.** The connector requests one UTC day per zone (`client.py:162-163`) and files by request date (`:312`). The outage transformers are exempt from the event-window trim (`_event_window.py:181-195`), dedup is per file, and there is no latest view (`silver/latest_views.py` has none for outages). `query()` windows on `timestamp_utc` (`schema_manifest.py:180-184`).
  - Measured: generation 951 versions in 11,011 rows (1,724 distinct business rows; 236 versions in all 13 files); production 569 versions in 3,551 (1,046); transmission 78 in 3,981 (678); offshore 1 in 4 (1).
  - Same effect as GIE 8b, different cause. Fix with append-only-plus-latest-view (as `elexon/remit`), or dedup across partitions on `(document_mrid, revision_number)`.
- **D5. The meaning of `unavailable_mw` is unverified and probably inverted.** `<quantity>` of `Available_Period` is renamed `unavailable_mw` (`outages_generation.py:64`, `outages_h7.py:71`) on the strength of the project spec alone.
  - Bronze: `quantity < nominalP` in 950 of 951 generation versions and 567 of 569 production versions, and `quantity = 0` in 551 and 121. Profiles step like availability (Schwarze Pumpe B, `nominalP` 755: 613, 463, 389, ...).
  - Research unit: confirm from ENTSO-E's data description (items 15.1.A to D, 10.1.A to C, 7.1.A and B) whether it is available capacity, then rename or keep. Also keep `nominalP` so unavailable MW = `nominalP` − available can be derived.
- **D6. Only planned outages are requested, and the CLI cannot ask for more.** `BusinessType=A53` is fixed in `extra_params` for generation, production, consumption and transmission (`endpoints.py:59,67,75,91`). `BusinessType` is not a forwarded optional param (`client.py:567-576`), and `gridflow ingest` has no fetch-param option (`cli.py:185-216`).
  - Unplanned outages (A54) are never fetched; `outage_type` is `planned` on every row of these four. Offshore (no `BusinessType`) did return `A54`. Fetch both A53 and A54.
- **D7 (minor).** Consumption `A03` curves are forward-filled to 15 minutes: 20 documents became 1,738 rows (`parsers.py:575-601`). Fine as a series, but it is a different grain from the other four members sharing the `_H7OutageTransformer` family.
- **Vault (fixed in `docs/v5-p26-entsoe`, not a gridflow defect).** The five notes claimed:
  - that `published_at` was dropped (A80);
  - "default query returns Active only", which is false;
  - "A54 reachable via override", which is false;
  - `PT60M` or "1:00:00" resolutions (all `PT1M`, or `PT15M` for consumption);
  - the wrong namespace, and capitalised response domain tags for A78;
  - "`unavailable_mw` is the unavailable MW" as fact;
  - a hypothetical offshore shape.
