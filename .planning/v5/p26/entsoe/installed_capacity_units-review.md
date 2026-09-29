# installed_capacity_units: checker review

Checker: Opus 5.5 (high), 2026-09-29. Page `entsoe/installed_capacity_units`, screenshot port 9859 (CDP, file:// URL, no server left running).

## Verdict: REVISE

1 major, 3 nits. The four points the seat asked about (the key, the chart, the sample, the codes and dates) and the neighbour claims all check out. The one major is an overclaim: the page says in two places that every request returns the whole year, and that is only what we have seen in our replies. It is a two-phrase fix.

## Findings

### 1. major: `page.what_it_is` and `page.notebook.lead` state an observed vendor behaviour as a rule

- **What is wrong.** Two sentences state it as a rule:
  - `what_it_is`: "Each ingest day fetches the whole year document again, so silver holds one copy per fetch".
  - `notebook.lead`: "Each fetch adds a full copy".
- **What is actually known.**
  - The one-request-per-UTC-day part is a code fact (`connectors/entsoe/client.py:162`, `day_subwindows`; `utils/time.py:123-137`).
  - That each one-day reply carries the whole year document was seen in all 72 bronze replies we hold. No vendor document says so: the note quotes none, and `gridflow/.planning/audit/.../vendor-docs/` holds only `entsoe-codes.md`.
- **The page scopes it correctly elsewhere.** `facts.cadence` says "a one-day request returned the whole year", and `raw_feed.note` says "the replies received carried the whole 2026 document". So the two sentences above are measured-on-our-copy universals (rubric §1, last bullet). This matches the pilot's calibrated major: "every point" where the code only sends no filter.
- **"Each ingest day" is also ambiguous.** A reader may take it as a day on which ingest runs. It means each UTC day in the ingest window.
- **Fix.** For example:
  - `what_it_is`: "gridflow requests each UTC day separately, and in the replies received each one carried the whole year document, so silver holds one copy per fetch, told apart by `published_at`."
  - `notebook.lead`: "In the replies received each fetch added a full copy, so keep each unit's latest `published_at`."
  - Alternatively, quote an ENTSO-E API guide statement for this article in the note body and cite it.
- **Evidence.** Silver: 12 files × 639 rows, and every `(timestamp_utc, area_code, unit_mrid)` repeats exactly 12 times (`df.group_by(k3).len()["len"].value_counts()` returns `{12: 639}`). Bronze `raw_20260915T200920Z_58ce819c.xml` has `time_Period` 2025-12-31T23:00Z to 2026-12-31T23:00Z for a request of `periodStart=202609140000&periodEnd=202609150000` (meta `request_url`).

### 2. nit: `page.chart_view.key[smaller].note` gives B08 as "Peat" with only a third-party source

- **What is wrong.** "Peat, marine, solar, waste and energy storage" labels B08 as peat outright. The only source the vault cites is entsoe-py `PSRTYPE_MAPPINGS`, which is not a vendor document (`actual_generation.md:248`; this note's schema row for `production_type`). gridflow has no PSR label table (`grep -rn "B08\|Peat"` over `src/gridflow` finds only business-type hits).
- **Mitigations.**
  - The same sourcing was accepted on the approved `actual_generation` page, and `generation_units_master_data` uses the same label.
  - Silver corroborates it: the three B08 units are IE-SEM `West Offaly Production` (135 MW), `Edenderry Prod` (118) and `Lanesboro Production` (91). Lanesboro is Lough Ree, and all three are Irish peat stations.
- **Fix.** None is needed if the seat accepts the entsoe-py provenance. Otherwise hedge B08 the way B20 is hedged, or drop the word. The seat may escalate this if it treats a third-party mapping as unacceptable evidence.

### 3. nit: `page.related[entsoe/actual_generation_units].note` rests on a local overlap measure

- **What is wrong.** "many of its `unit_mrid` codes appear here" is knowable only from our copy (162 of 175 unit EICs overlap in local silver). It is not a number, so it is not a §3 blocker, but it is a measured statement.
- **Fix.** Use a relation that needs no measurement, for example "Output per unit, keyed on the same kind of unit EIC (`unit_mrid`)".

### 4. nit: vault body, "Silver sample", `ingested_at` is earlier than `published_at`

- **What is wrong.** The corrected sample row has `published_at` 2026-09-15T20:09:21Z but keeps `ingested_at` 2026-05-08T18:00:00Z. `ingested_at` is the transform time (`installed_capacity_units.py:79-83`), so it cannot come before the fetch.
- **Evidence.** In silver, the ABRBO row in `installed_capacity_units_20260914.parquet` has `ingested_at` 2026-09-15 20:09:28.63Z. The `capacity_mw` 99.0, `published_at` 20:09:21 and `P1Y` that the writer changed are correct.
- **Fix.** Set it to about 2026-09-15T20:09:28+00:00.

## Checks that pass (with evidence)

### Seat focus 1: the key

- The transformer dedups `(timestamp_utc, area_code, unit_mrid)` with `keep="last"` inside one `read_bronze(target_date)` (`installed_capacity_units.py:34-48, 74-77`), so the dedup holds within one transform day only.
- Silver has 12 day files (2026-08-01 to 05, fetched 16 Aug; 2026-09-08 to 14, fetched 15 Sep). Each file has 639 rows with 0 key3 duplicates.
- Across the files, key3 gives 639 unique combinations against 7,668 rows, and key4 (with `published_at`) gives 7,668 unique. `published_at` has 62 distinct values and 0 nulls.
- The page's explanation is plain: `what_it_is` explains the copies, the `published_at` guide line says "tells repeated fetches apart", and `notebook.lead` gives the dedup (finding 1 is scoping only).

### Seat focus 2: the chart

- The committed series has `spec_origin: vault`, `rows_used` 639 and `duplicates_dropped` 7,029. The build passes the digest check. There is no staged spec and no authored override.
- A Polars recount, keeping each `(area_code, unit_mrid)` at its latest `published_at` and applying the note's `group_map`, gives gas 167, wind 166, hydro 133, nuclear 70, coal 50, oil 26, smaller 14, biomass 7, other 6. This equals the series, the alt text and the bar labels.
- There is no double count. Every one of the 639 latest rows comes from the 15 Sep fetch (`published_at` 20:09:21 to 20:09:25 UTC, the 2026-09-14 request), and every unit appears in that fetch.
- The title and caption date the capture (15 September 2026), name six zones, and say `count`. The window is a single `timestamp_utc` filter. Nothing non-additive is summed.
- Palette: khaki is used for B20 only, and uncovered codes are unpainted hatches.
- Per-zone counts: GB 230, FR 165, DE-LU 129, NL 51, IE-SEM 33, BE 31. These match the notebook output.

### Seat focus 3: the sample

- The eight rows are `22W201806271---D`, "EDF Luminus Seraing TGV", `B04`, BE:
  - 470.0 MW at `published_at` 2026-08-16 13:43:49, 13:43:55, 13:44:01 and 13:44:08;
  - 300.0 MW at 2026-09-15 20:08:45, 20:08:51, 20:08:58 and 20:09:04.
- The filter `published_at >= 13:43:46` drops the first August copy (13:43:43) to land on exactly eight rows. That is fine.
- In all of silver, Seraing is the only unit whose `capacity_mw`, `production_type` or `unit_name` differs across fetches.
- The caption states the two values and the months and gives no cause. The body's Known issues bullet also states only the observed change.
- `generated_by: gridflow-sample`. The guide has a line for every non-pipeline column, key columns first.

### Seat focus 4: codes and dates

- `timestamp_utc`: "23:00 on 31 December 2025 is midnight CET" is correct. It is `_advance_calendar` at position 1, which returns the period start (`parsers.py:76-93, 527-528`). Bronze `timeInterval.start` is 2025-12-31T23:00:00Z, and CET is UTC+1 in winter, so this is 00:00 on 1 January 2026. The wording passes.
- A33 means year ahead (`_event_window.py:174-175`).
- `MAW` is on every series in bronze.
- B08: see finding 2.

### Seat focus 5: neighbours

- `installed_capacity`: its silver columns are `timestamp_utc, area_code, production_type, capacity_mw, ...` with no unit column. Its only `timestamp_utc` is 2025-12-31 23:00 UTC. So "Zone totals per production type for the same year, not per unit" is true.
- `generation_units_master_data`: its silver columns are `area_code, unit_mrid, unit_name, production_type, implementation_datetime_utc`, so "keyed on the same `unit_mrid`, with implementation dates" is true. All 639 of this table's unit EICs appear among its 660, a local fact that is correctly kept off the page.
- `elexon/bmunits_reference`: `T_ABRBO-1` is in its committed sample.

### Rubric §1: request, commands and notebook

- **Request.** The URL matches the bronze meta `request_url` exactly: parameter order, `%Y%m%d%H%M` format (`endpoints.py:403`), `in_Domain`, and `processType=A33`.
- **Commands.** `--end` is parsed to midnight UTC (`runner.py:458-471`) and `day_subwindows` covers `[start, end)`, so the ingest end date is excluded. The transform iterates dates inclusively (`cli.py:412-414`).
- **Notebook lead.** `query()` returns pandas (`source.py:401-451`), filters with an inclusive-end date predicate and drops the bitemporal lineage columns. The output shows all 639 units for `"2025-12-31"` to `"2025-12-31"`, so the 23:00Z rows are included. `needs` (14 September 2026) matches the commands.
- **Field sources.** In bronze, `inBiddingZone_Domain.mRID`, `registeredResource.mRID/name`, `quantity` and `MktPSRType/psrType` are present, and `PowerSystemResources` children (for example `ABRBO-1`) are nested and dropped (`parsers.py:345-354`). `createdDateTime` 20:09:21Z equals the latest `published_at`.

### Rubric §3: no local data

- A grep of the rendered page for `locally|held|our |since 20|rows|days|% of` finds only the template's aria label "8 rows of 14 columns".
- Every number on the page is in the chart, the eight rows or the notebook output.

### Rubric §4: build and detector

- `gridflow-build --only entsoe/installed_capacity_units` wrote the page. Its three warnings belong to other datasets.
- `detect.mjs --json` returns one `em-dash-overuse` advisory (92 hits, all from the EIC `--` padding). This is accepted under ruling #39.

### Rubric §5: screenshots

- **Captured.** Closed and open (frame unfolded, notebook drawer open) at 1440, 1024, 768 and 390. 390 is a true 390 viewport through a CDP device-metrics override.
- **Overflow.** `scrollWidth` equals `innerWidth` at every width.
- **What I looked at.** The hero turbines, the chart and key, the raw feed, the frame and guide, the notebook and the related datasets. The frame and the notebook `df` scroll inside their own boxes. Nothing overlaps.
- **Accepted, not findings:**
  - the `.ipynb` tab clip at 390 (ruling #39, template);
  - the 390 hero crops the scene's left edge, which is the shared template's responsive crop.
- **Dark mode.** There is no dark theme: no `prefers-color-scheme` or `data-theme` in `site/hifi/assets`.

### Rubric §6: leakage and filler

- No em dashes, arrows, middots, planning labels or "live" wording.
- Related notes are 12 words or fewer.

### Rubric §7: vault body edits

All checked against silver or bronze:

- ABRBO is `B18` at 99 MW, and ABTHB is `B05` at 1,590 MW.
- DRAXX is the production unit.
- The bronze granularity statement is correct.
- The point-in-time field is `published_at`.
- The "one day is enough" advice is correct.
- The mirror is byte-identical to the canonical note (`cmp`).
- Small wording point for the next pass: "365 identical requests" should be "365 requests, each returning the same document", since the requests differ in `periodStart`.
