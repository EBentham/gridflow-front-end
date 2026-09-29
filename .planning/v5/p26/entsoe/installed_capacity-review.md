# entsoe/installed_capacity: review

Checker: Opus 5.5 · high, 2026-09-29. Port 9846 (server stopped).

## Verdict: REVISE

One major (the notebook's pivot output labels each zone over the wrong column) and four nits. Every
fact, number, the chart and the frame check out against code, bronze and silver.

## Findings

1. **major**, `page.notebook.cells[1]` (rendered output `[4]`, the `wide` pivot table).
   - **What is wrong:** the zone headers sit one column to the right of their values, so the table
     misattributes every value.
     - `pivot_table` gives a two-row header: the columns name `area_code` above the index name
       `production_type`. `scripts/run_notebooks.py` flattened it into one row of 10 header cells.
     - The body rows have 5 cells.
     - The rendered `<thead>` reads `<th></th><th>area_code</th><th>10Y1001A1001A82H</th><th>10YBE----------2</th><th>10YFR-RTE------C</th><th>10YNL----------L</th><th>production_type</th><th></th>…`.
     - The first body row reads `<th>B01</th><td>8855.90</td><td>846.099</td>…`.
   - **What a reader sees:** at 1440 and at 390, the `10Y1001A1001A82H` (DE-LU) label sits over BE's
     column. The reader therefore reads DE-LU B14 as 2,056 MW and FR B14 as 486 MW, and the NL
     column appears empty. This contradicts the page's own "DE-LU sends no B14". The seat's point 4
     rule (outputs are real and read truly) fails for this cell.
   - **Evidence:**
     - Notebook JSON `columns` is `["area_code", "10Y1001A1001A82H", …, "production_type", "", "", "", ""]`.
     - Every other notebook in `site/hifi/data/notebooks/` starts `columns` with `""`, the index header.
     - Screenshots: `scratchpad/icr/w1440_nb1.png` and `w390_nbA.png`.
   - **Fix:** on the author's side, give the pivot a one-row header and rerun `run_notebooks.py` and
     the build. For example, add `.rename_axis(index=None, columns=None)` to the `pivot_table` call.
     Better still, rename the columns to `DE-LU`, `BE`, `FR` and `NL` in this cell, so the table is
     readable without EIC codes.
   - The runner's flattening of a two-level pandas header is a separate seat item.

2. **nit**, `page.facts.cadence`.
   - **What is wrong:** "`sources.yaml` schedules weekly fetches" suggests that gridflow fetches
     weekly. Nothing does.
   - **Evidence:**
     - `schedule` is declared at `config/settings.py:60`.
     - Its only reader is `scripts/seed_canonical_schema.py:296-302`, which builds a metadata map.
     - Searching `src/` finds no scheduler that uses it.
   - **Suggested fix:** "One `P1Y` point per year, as sent", or "`sources.yaml` labels it weekly".
   - The same phrase is on `generation_units_master_data`.

3. **nit**, `page.what_it_is` / `page.summary`.
   - **What is wrong:** the page never uses the phrase "a single annual snapshot", which the seat asked
     for. The meaning is already there: "one MW figure for the year", "the 2026 figure", and no trend
     anywhere on the page, the chart and alt included.
   - **Suggested fix:** add the phrase to `what_it_is`, for example "one MW figure for the year, a
     single annual snapshot".

4. **nit**, `page.notebook.lead`.
   - **Is it right?** Yes.
     - `query()` filters `timestamp_utc` on whole UTC days, both ends included
       (`source.py:401-445`; date column from `silver/schema_manifest.py:169`).
     - The only stamp is 2025-12-31 23:00 UTC, so `"2025-12-31"` returns the 2026 rows.
     - That holds whichever 2026 day was ingested (`needs` gives 14 September).
   - **Is it plain?** Only partly. The lead never says outright that you query 31 December 2025 even
     though you ingested 14 September.
   - **Suggested fix:** "The 2026 row is stamped 31 December 2025 whatever day you ingest, so query
     that day; each silver file repeats it, so drop duplicates."

5. **nit**, `page.what_it_is`.
   - **What is wrong:** two claims are measured on the responses we hold but read as general rules:
     - "GB and IE-SEM return no-data acknowledgements";
     - "DE-LU sends B07 as 0 but no B14".
   - Both are true in every held response: bronze 1 to 5 Aug and 8 to 14 Sep, and the 2026 document.
   - The approved sibling pages scope such claims ("in these responses", "as sent"). The rubric's
     calibration notes also flag unscoped measured universals.
   - **Suggested fix:** "... return no-data acknowledgements in these responses" and "in the 2026
     document, DE-LU sends B07 as 0 but no B14".

## What I checked, with evidence

- **Chart values:** the Polars dedup over the 12 silver files, then the DE-LU sum by `group_map`, gives:
  - solar 104,029.51, wind 77,149.35, gas 35,678.02, coal 31,907.13, storage 23,427.61, biomass 8,855.90, misc 6,286.94, hydro 5,575.95, other 2,030.47;
  - a total of 294,940.88.
  - These equal the committed series (`rows_read 804`, `rows_matched 240`, `duplicates_dropped 220`, `rows_used 20`, `spec_origin: vault`) and every number in the alt text.
  - No staged spec and no authored override exist.
- **Additivity:** within one zone and year, each PSR code is a distinct type row, and one copy per key is kept before summing, so the groups add.
  - `capacity_mw` is MW (`MAW` in bronze; the schema docstring says "Total installed capacity in MW").
  - Khaki is used only for B20 (the vendor's Other). Codes the palette does not cover are hatched.
- **Zero versus missing:**
  - DE-LU sends B07, B08 and B13 as 0.0 and has no B14 row. The caption, `what_it_is` and the misc key note all say so correctly.
  - NL sends 0.0 for B02, B03, B06, B07, B08, B09, B10, B12, B13 and B15, and has no B25. The frame caption, "B02 and B10 are sent as 0", is true.
  - BE and FR omit codes rather than send 0.
- **Coverage:**
  - Four zones send data: DE-LU and NL with 20 codes each, FR with 15, BE with 12.
  - GB and IE-SEM return `Acknowledgement_MarketDocument` code 999 "No matching data found… INSTALLED_GENERATION_CAPACITY_AGGREGATED_R3" (bronze 2026/09/14 `…2a96083c.xml` and `…f7677597.xml`).
  - The six zones requested match `DEFAULT_ZONES` (`endpoints.py:395`), and the six bronze `request_url`s show them.
- **Repeats:**
  - There are 67 keys. `group_by(key).len()` gives 12 for all 67, `n_unique(capacity_mw)` is 1 for all, and each file holds 67 unique keys.
  - One-day requests return the full interval 2025-12-31T23:00Z to 2026-12-31T23:00Z (bronze for 1 to 5 Aug and 8 to 14 Sep).
  - No text, chart or frame counts the repeats: the chart dedups, the frame dedups, and the notebook uses `drop_duplicates`.
- **Raw feed:**
  - The URL and parameter order equal the bronze `request_url` (`documentType, periodStart, periodEnd, in_Domain, processType, securityToken`).
  - The ingest end is excluded (`day_subwindows`, `utils/time.py`). The transform end is included (`runner.py:1126`, `date_range`).
- **Frame fields:**
  - `inBiddingZone_Domain.mRID` maps to `in_domain` (`parsers.py:289-297`), then to `area_code` (`installed_capacity.py:62`).
  - `psrType` comes from `parsers.py:347-348`.
  - `published_at` is the response `createdDateTime`: 20:08:31Z in the document versus `fetched_at` 20:08:31.63 (ruling #39).
  - `timestamp_utc` 2025-12-31 23:00 UTC is midnight CET.
- **Notebook:**
  - All cells are read-only and there are no errors.
  - The plot matches `plot_alt`: DE-LU solar is about 104k, DE-LU onshore wind about 68k, FR nuclear about 63k, DE-LU has no nuclear bar, and every BE bar is under 12,000.
- **Related:** `bmunits_reference` does carry `registered_capacity_mw` per unit.
- **Vault body edits** (the diff against `origin/master`), each checked against bronze or code:
  - granularity;
  - `businessType` A37;
  - the `quantity` value 104029.51 (matches bronze);
  - the point-in-time field and the `published_at` schema row;
  - the silver sample values;
  - the known-issue rewrite.
  - All are small spans. The mirror is `cmp`-identical.
- **Local-data and leakage grep** of the rendered text: no hits for `locally`, `held`, `our`, `since 20`, `N rows/days`, `% of`, `live`, `now`, `real-time`, em dashes, `→` or middle dots.
- **Gates:**
  - `gridflow-build --only entsoe/installed_capacity` wrote the page.
  - The detector returns only the accepted `em-dash-overuse` advisory (EIC padding).
- **Screenshots** (`scratchpad/icr/`):
  - 1440, 1024 and 768 were shot directly; 390 through a 390 px iframe.
  - They cover the hero, the chart and key, the raw feed, the unfolded frame (`#fx` checked; the frame is an `overflow-x: auto` scroller, 2138/1265), the open notebook and the related datasets.
  - Nothing is clipped. There is no page-level horizontal scroll (`scrollWidth` 375 at 390).
  - The site has no dark theme (0 `prefers-color-scheme` or `data-theme` rules), so dark renders as light.

## Note on the writer's report

The report says the template has no unfold control. It does: the `…` header cell is a checkbox (`#fx`, "Show the folded columns"). I checked the unfolded state; it is fine.
