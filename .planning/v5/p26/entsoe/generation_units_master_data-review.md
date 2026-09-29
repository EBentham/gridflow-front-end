# Review: entsoe/generation_units_master_data (production unit register)

Checker: Opus 5.5 · high, 2026-09-29. Screenshots on port 9847 (static server from the scratchpad root, stopped).

## Verdict: APPROVE

Three nits, no blocker, no major. The nits are optional wording fixes.

## Findings

1. **nit** · `page.facts.cadence`
   - **What is wrong.** "`sources.yaml` schedules it weekly" names a scheduler that does not exist.
     - `schedule: "weekly"` (`gridflow/config/sources.yaml:272`) loads into `DatasetConfig.schedule` (`config/settings.py:60`).
     - No gridflow code reads that field: a grep of `src/` and `scripts/` for `.schedule` or `["schedule"]` finds nothing.
     - The approved `elexon/bmunits_reference` page words the same fact as "`sources.yaml` declares it weekly".
   - **Suggest.** "declares it weekly".

2. **nit** · `page.related[0].note` ("MW per unit on the same `unit_mrid`; this register drops it")
   - **What is wrong.** "This register" reads as ENTSO-E's A95 register, and that register does carry MW.
     - Every bronze `TimeSeries` has `nominalIP_PowerSystemResources.nominalP`. For example, Seraing's generating units are 150+150+170 in the 2026-08-01 XML and 150+150 in the 2026-09-08 XML.
     - Gridflow's parser drops the field (`parsers.py:641-719`).
     - The chart caption says it correctly: "silver carries no MW".
   - **Suggest.** "silver here drops it" (still within 12 words).

3. **nit** · `page.what_it_is` ("not commissioning: one unit's moved from 2018 to 2025 between two requests")
   - The claim is right. The reason given is the weaker of the two in view.
   - **Why the Seraing move is weak.** Seraing's new date (2025-11-01) arrives with the record's reconfiguration: SERAING TV is removed and the unit goes from 470 to 300 MW. A reader could take that as a re-commissioning.
   - **Stronger evidence already on the page.** The frame shows CATTENOM 3 at 2000-01-01, in both requests: a placeholder-looking date on a 1990s unit.
   - **Suggest (optional).** Keep the sentence, or point to Cattenom as well. Either way, add no count of units sharing 2000-01-01: that is a local statistic.

## What was checked, with evidence

**Chart provenance**

- **Source.** The committed series has `spec_origin: vault`, `generated_by: gridflow-distil`, and a filter of `event_time eq 2026-09-08T00:00:00Z`.
- **One request, no double count.** Provenance reads `rows_read 1317`, `rows_matched 660`, `rows_used 660`. It uses the 8 September request only.
- **Counts match silver.** A Polars `group_by("production_type").len()` over `event_time == 2026-09-08` gives:
  - B04 175;
  - B19 90 + B18 82 = 172;
  - B11 77 + B12 29 = 106;
  - B05 40 + B06 26 + B02 8 + B03 3 + B08 3 = 80;
  - B14 70;
  - B10 27;
  - B01 7 + B16 5 + B17 4 + B25 4 + B13 1 = 21;
  - B20 9.
  - The total is 660, equal to the request's row count. The alt, the bars and the key all match.
- **Other checks.**
  - A count, so no non-additive column is summed.
  - Khaki is used only on B20 (ENTSO-E's Other). Codes the palette does not cover are hatched.
  - No staged spec or authored override is left.

**Code meanings**

- **Official list.** Gridflow has no B-code label map in `src/` (only `schemas/entsoe.py:127` for B16, B18 and B19). Its cached official list v36r0 (`gridflow/.planning/audit/2026-05-31-vendor-truth-audit/vendor-docs/entsoe-codes.md`) confirms B01, B04, B05, B10 to B14, B16 to B20.
- **Postman list.** The vault's `actual_generation.md` cites ENTSO-E's Postman `psrType` list for B02 lignite, B03 coal-derived gas, B06 oil and B25 energy storage.
- **B08 peat** is de facto only (entsoe-py). The writer's corroboration holds: Edenderry, West Offaly and Lanesboro are the peat stations.
- Every key note matches these sources.

**Dates**

- **Seraing move.** Silver has exactly one `(area, unit)` whose date differs between the two requests: BE Seraing TGV, 2018-10-14 then 2025-11-01. No type or name differs.
- **Range.** 1960-01-01 to 2027-01-01.
- **Rows dated after the request.** In the 8 September request: DE-LU GuD Dradenau (2026-11-01), Nordseecluster A (2026-09-12) and KALLO BESS (2027-01-01).
- **Placeholder-looking dates.** 131 units share 2000-01-01; 60 share 2018-10-01, all DE-LU.
- **What the page claims.** Only "undocumented, not commissioning", which the evidence supports. It plots and trends no date. The guide line matches the parser: `_parse_utc` at `parsers.py:96-104`, midnight UTC.
- **Request parameter left alone.** The 2026-08-01 request lacks two units dated 2026-08-03 and 2026-08-18, yet carries KALLO BESS dated 2027. So what the request parameter filters is genuinely unknown, and the page rightly says nothing about it.

**No MW**

- The silver schema has no MW column.
- "Capacity" and "MW" appear only as disclaimers: the caption, `how_used[1]` and the `related` note (see nit 2).

**Key and grain**

- **Row identity.** `unique(subset=[area_code, unit_mrid])` runs within one transform (`generation_units_master_data.py:68-69`), and each requested date writes its own file.
- **`event_time`** is the target-date fallback (`silver/base.py:2221-2231`, and `_event_time_column` returns `timestamp_utc`, which this table lacks).
- **No duplicate keys.** 0 duplicates on `(event_time, area_code, unit_mrid)` across all 1,317 rows, and 0 on `(area_code, unit_mrid)` within one request.
- **Seat ruling 1.** Its wording is accurate.

**Raw feed and commands**

- **URL.** The page URL equals the bronze `.meta.json` `request_url`: parameter order `documentType, Implementation_DateAndOrTime, BiddingZone_Domain, BusinessType, securityToken`. This follows `endpoints.py:119-126`, `client.py:287-289` and the `data_date` in the meta.
- **Commands.**
  - `date_param` types build one task per unit with no day chunking (`client.py:152-157`), and send `--start`'s date. So `--end 2026-09-09` is harmless.
  - Transform `--end` is inclusive.
  - The fetch date of 15 September matches the meta `fetched_at` (2026-09-15T20:13:34Z to 20:13:39Z).

**Fields**

- `unit_mrid` comes from `registeredResource.mRID`, and rows without one are dropped (`parsers.py:702`, `:709`; transformer `:68`).
- `area_code` comes from the TimeSeries' `biddingZone_Domain.mRID`.
- `production_type` is the first `psrType` or `generatingUnit_PSRType.psrType` in the TimeSeries.
- `unit_name` becomes an empty string when absent (`fill_null("")`, transformer `:59`).

**Notebook**

- **Lead.** It is accurate: `schema_manifest.py:166` maps this dataset to `implementation_datetime_utc`, and `query()` filters on the manifest's date column (`gridflow_models .../handles/source.py:426-440`).
- **Artefact.** Written by `scripts/run_notebooks.py`. Three read-only cells, no errors.
  - `value_counts` totals 660 (230, 175, 135, 52, 35, 33), so the notebook reads exactly one request.
- No plot, so no `plot_alt` is needed.
- `needs` matches the commands.

**Related**

- `unit_mrid` exists in all three ENTSO-E silver tables. Overlap with the 8 September register:
  - `installed_capacity_units`: 639 of 639;
  - `actual_generation_units`: 174 of 175;
  - `outages_production`: 45 of 46.
- `bmunits_reference` silver has no EIC column, so "silver shares no key" holds.

**No local data**

- A text sweep of the rendered page for `locally`, `held`, `our `, `since 20`, `% of`, and digits followed by "rows" or "days" finds nothing.
- "rows" appears only in guide lines and the template's help card.
- "fetched 15 September" dates the capture of a register snapshot, as the calibration notes ask.

**Leakage and style**

- No em dashes, `→` or middots in the prose.
- No "live", "now" or "real-time".
- Related notes are 12 words or fewer.

**Build and detector**

- `gridflow-build --only entsoe/generation_units_master_data` exits 0.
- `detect.mjs --json` returns only the accepted advisory `em-dash-overuse` (61, from the EIC padding).

**Mirror**

- `cmp` of the vault note against `vault/entsoe/generation_units_master_data.md` is clean.

**Screenshots and measurements**

- **Coverage.** Every section at 1440, 1024, 768 and 390; 390 was a true 390 px iframe. The screenshots show the frame unfolded and the notebook open; the folded frame was checked by measurement at each width.
- **Nothing lost.** Numerically, no text leaf lies outside the viewport unless it sits in a scroll container. The unfolded frame scrolls inside its `.fw` wrapper (`overflow-x: auto`) at every width, and the chart's SVG text is inside the viewport.
- **Template items, not this page's findings.**
  - The scenery's "battery storage" label sits at x=-1 at 390 and still reads in full.
  - The raw-feed URL wraps mid-token at 390.
  - The notebook filename clips at 390 (a known seat item).
- **Dark mode.** No stylesheet has a dark scheme (`prefers-color-scheme` or `data-theme`), so dark renders the same as light.

**Body edits**

- All seven edits cite `file:line` or bronze evidence and fix small spans.
- The curl example and the API table are unchanged.

**Seat rulings 1 and 2** are applied, and their wording is accurate. The "Smaller types" key note lists all five codes with correct meanings.
