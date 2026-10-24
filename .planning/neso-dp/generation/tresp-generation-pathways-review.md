# tRESP generation pathways: checker's review (round 1)

Page `neso_data_portal/tresp-generation-pathways` (family page), lead `tresp_generation_pathways_resp_region`, members `_gsp`,
`_la_england`, `_la_scotland`, `_la_wales`. Checked against gridflow code, local silver and bronze (read only, Polars), the NESO
catalogue snapshot `20261006T195819Z`, the field-info snapshot `20261008T114228Z`, the registry and the demand sibling
(`tresp-demand-pathways`, approved).

## Verdict: REVISE (1 major, 4 nits)

Gates: `gridflow-build --only neso_data_portal/tresp_generation_pathways_resp_region` exits 0 (one unrelated caveat-grammar
warning about "Known issues" lines); detector `[]`; no em dashes on the page or in the `page:` block; mirror `cmp` clean against the
vault worktree; the note diff against `origin/master` is the `page:` block, `updated:` and four dated body edits (no whole-file
rewrite). Screenshots at 1440 (slices to the foot), 1024 and 768 (slices through chart, request wells and frame), and a 390 px
iframe (server on 9815, started with its PID recorded and stopped by that PID): hero, chart, all five request wells, the folded
frame and its guide, the notebook panel and the related list are all fully visible, nothing clipped or overlapping; the folded
frame at 390 shows only the first columns (known follow-up). The site has no dark theme. The notebook PNG (`...resp_region-4.png`) shows three lines, one to 2035 then three, as `plot_alt` says.

## Findings

1. **major** `page.raw_feed.note` ("one `package_show`, then each of five files downloaded whole unless its `last_modified` is
   unchanged").
   - The commands beneath it do not do that. A family ingest fetches only that family's own resource: `endpoints.FAMILIES[...]`
     for `tresp_generation_pathways_resp_region` and `_gsp` each carry exactly one name (`('tRESP Generation Pathways per RESP
     Nation and Region', 'CSV')`, `('tRESP Generation Pathways per Grid Supply Point Area', 'CSV')`), and
     `client.py:1698-1760` (`iter_members`) does one `package_show` per family call, then loops over that family's selected
     members only. So each of the three commands makes one `package_show` and downloads one file; the page's single run of three
     commands downloads two files, not five.
   - A reader takes the note to mean `gridflow ingest ... resp_region` pulls all five geographies.
   - Fix, in the pattern of the approved `demand-flexibility` note: "From NESO's CKAN portal: one `package_show`, then the
     table's file downloaded whole, unless its `last_modified` is unchanged. Dates select nothing; silver keeps every capture."
     The five request lines under the members already show every file.

2. **nit** `page.chart_view.title` ("Large solar installed, Holistic Transition, 2025 to 2050") and `caption`.
   - Every value is a NESO projection, and the 2025 bar is dated 31 March 2025, before the 30 January 2026 publication; the note
     body keeps a `TODO` on whether the 2025 rows are modelled starting positions or observed capacity. "Installed" in the title
     can read as outturn. The hero summary says "projected"; the chart does not.
   - NESO's text: the single short-term pathway to 2035 "is informed by the DNOs' Holistic Transition pathway, adjusted by NESO"
     and it is labelled `tRESP - HT`; the long-term ones are "tRESP versions" of the three FES pathways. The title's plain
     "Holistic Transition" is NESO's label, which the caption's `tRESP - HT` gives, so this is wording only.
   - Suggested: "Large solar capacity projected, tRESP Holistic Transition, 2025 to 2050" or "projected" in the caption.

3. **nit** `page.record.fields.projection_year` ("MW installed at 31 March of that year, per NESO").
   - Your question: is "MW installed at 31 March" NESO's statement? In two pieces, yes. `Unit` is "Capacity installed (MW)"
     and `Year` is "the year against which the Pathway value has been provided for, with volume at 31 March" (field info, both
     files). The hero grain line is a fair join of them. "Of that year" is the note's own reading (body: "at 31 March of the
     labelled year", with a `TODO` on a calendar or financial-year convention), not NESO's words, so "per NESO" covers more
     than NESO says. For installed MW at a date the risk is small.
   - Suggested: "Year the value is for: MW installed at 31 March, per NESO" (drop "of that year").

4. **nit** `page.record.fields.value` ("vehicle-to-grid (`Srg_BB005`) is negative in these files, sign unexplained by NESO") and
   `building_block_id` ("all 23 match a ... FES block id").
   - Reproduced: negative values occur only in `Srg_BB005`, and it is never positive in any of the five files. But it is
     "zero or negative", not "negative": the GSP file has 118 exact zeros among its 13,398 `Srg_BB005` rows (13,280 negative).
     Region 638 of 638 negative; England 17,168 of 17,168; Scotland 1,856 of 1,856; Wales 1,276 of 1,276. "Negative on every
     row" would be wrong for GSP, and the page does not say it; the wording is only loose. Suggest "zero or negative".
   - "NESO gives no sign convention" holds for the tRESP files (field info, package notes, resource text). One related fact
     the page does not use: silver `fes_building_blocks_block_definitions` defines `Srg_BB005` as "MW availability, potential MW
     available to participate" in editions 2021 to 2025 (2020: "MW", installed capacity), whereas the tRESP block list says
     "Capacity Installed (MW)". The FES main table (editions 2023 to 2025) is also zero or negative for this block (minimum
     -1,637.5 MW, 2025). So "all 23 match a FES id" is true (every id is in every FES definitions edition 2021 to 2025, and 22 of
     23 in 2020, where `Gen_BB023` is missing; also all 23 in the tRESP block list, all with unit "Capacity Installed (MW)"), but
     for this one block the matching id carries a different FES unit. Not needed for the page; worth a clause if the line is
     touched ("ids only; definitions not compared").

5. **nit** canonical note body, `tresp_generation_pathways_resp_region`, "Cross-geography consistency" and the `TODO` above it.
   - Reproduced exactly (1,334 block, pathway and year groups): GSP total minus region total, maximum 7.3e-12 MW; the three
     local-authority files together minus the region total, maximum 0.00034 MW; Scotland LA sum against the `Scotland` region
     44.88 MW (Gen_BB015, EE, 2050), Wales 60.03 MW (Srg_BB005, HT, 2050). The note's 1e-11, 0.0004, 44.9 and 60.0 are right.
     No nulls on the three-way join. Your phrase "GSP rows and the three LA files each sum to the region total": the GSP rows do;
     the three LA files only do together. Singly they do not: the England file differs from the nine English regions by up to
     72.2 MW, as the mirror image of Scotland and Wales (the totals agree, so the three differences net out).
   - "Within a nation they do not match: the Scottish ... and the Welsh ones" therefore reads as if England were the exception.
     Suggested: add "and the English file differs from the nine English regions by up to 72.2 MW".
   - The older `TODO: verify ... whether the 11 regions tile the whole of Great Britain without overlap` is still there beside
     the new measurement. The values settle the double-counting worry (three independent cuts, 231 GSP areas and 350 ONS
     authorities, each counted once, all agree with the region sum), though NESO states no geometry rule. Say so, or reword the
     `TODO` to geometry only.
   - The page itself carries none of this, so it is safe; and the chart's claim is only "summed over every RESP nation and
     region", never "Great Britain", so the sum is honest as stated. "Indicative" is NESO's word and is on all three
     local-authority member lines; NESO's reason ("defined at the larger tRESP GSP area ... DNOs will disaggregate", "should not
     be used as a target for planning") is in the note body, verbatim from the three resource descriptions.

## What I checked and found correct

- **Chart.** Spec in the note, `spec_origin: vault`, digest passes. Reproduced from silver (`resp_region`, 14,674 rows, one
  capture): `Gen_BB012`, `tRESP - HT`, years 2025, 2030, ..., 2050, sum over the 11 regions: 12,777.64 / 28,738.38 / 44,345.05 /
  55,088.78 / 60,904.58 / 64,451.08 MW; 66 rows used (6 years x 11 regions), 0 duplicates dropped. Series file equals these, and so
  do the alt text and rendered labels (12,778 / 28,738 / 44,345 / 55,089 / 60,905 / 64,451). "About fivefold" is 5.04. "Fastest
  before 2035": +3,192 MW a year 2025 to 2030, +3,121 to 2035, then +2,149, +1,163, +709. The chart is horizontal, as the alt says.
  Summing is additive (installed MW within one block). Block and pathway are both stated in title, caption and key.
- **Region coverage.** 11 values, one row per region per block, pathway and year; the five-cut agreement above means no value is
  counted twice. 2035 is identical under HT, EE and HE (max difference 0.0 over all regions and blocks).
- **Scoped claims.** 23 block ids, the same set in all five files; all 23 in `tresp_building_block_definitions`; FES as in finding
  4. Pathway coverage by year as in the note's table (HT 2025 to 2050; EE and HE 2035 to 2050).
- **Geographies and units.** 231 GSP areas, 14 licence areas, one licence area per GSP area; 296, 32 and 22 ONS codes (prefixes E,
  S and W). `unit` is `MW` on every row of every file. NESO's wording for the three LAD and `Pathway` columns matches the member
  lines.
- **Frame.** Eight rows reproduced from silver: South West, `Gen_BB012`, 2025 (2,599.173781), 2034 HT (6,882.084986), 2035 under
  EE, HE and HT (7,394.227719 each), 2036 EE 7,781.539951, HE 7,772.879666, HT 7,906.370453. Order matches `order_by`. Key
  columns, `published_at` 2026-01-30 08:34:24.152349 UTC and `timestamp_utc` 2026-10-08 11:40:26.441105 UTC match silver. Sample
  is `generated_by: gridflow-sample`; 15 columns, 11 guide lines plus the pipeline columns left out as in the sibling. One
  capture and one `bronze_capture_id` per table; counts 14,674 / 308,154 / 394,864 / 42,688 / 29,348; no repeated key; no nulls.
- **Notebook.** Written by `scripts/run_notebooks.py`, 5 cells, no error outputs, one image. All cells read only (`data.sql`).
  Outputs equal silver: HT 2033 37,671.8, 2034 41,008.4; 2035 44,345.0 under all three; 2036 EE 47,046.9, HE 47,006.3, HT 47,681.7;
  GSP 2050 equals the region sum under each pathway (56,903.5 / 64,451.1 / 56,546.1). `plot_alt` figures (56,903 and 56,546)
  round correctly from 56,903.47 and 56,546.12. `needs` agrees with the commands (region and GSP tables). The lead is accurate:
  `query()` filters on capture time for a table with no event time.
- **Raw feed requests and commands.** All five `GET` URLs equal the bronze sidecars' `request_url`; `package_show` is
  `CKAN_ACTION_PREFIX` plus `?id=tresp-generation-pathways`. Command 3, `gridflow pipeline neso_data_portal
  tresp_generation_pathways_gsp --last 24h`, is real and right: `cli.py` `pipeline(source, dataset, --start/--end/--last)`
  resolves dates once and runs ingest then transform on one context; it matches the line already used on approved pages. `--last
  24h` ends now, so it passes the 48 hour recency screen (`_assert_window_admissible`). Three commands is the limit.
- **Captures.** Every family has only `2026/10/08` in bronze; no 2026-10-16 sidecar names any of the five resource ids (so the
  new dated sentence in "Cadence" is true).
- **Public copy.** No em dashes, "held", local counts or planning words on the page; hero facts match the catalogue snapshot (30
  January 2026 last-modified, 28 January 2026 created, version 1.0, ad hoc). `what_it_is` quotes 11 words from the package
  notes; "DNOs will use it ... ED3 2028-33" is NESO's. Related notes say how the pages relate and the three slugs resolve; the
  member pointers use `#<member>`.
- **Other body edits.** `updated:` 2026-10-24; GSP licence-area sentence (max 1 per area, reproduced); England "indicative"
  sentence (quotes match the resource descriptions word for word); cadence sentence. Smallest span, evidence cited, line endings
  as on `origin/master`.

## Defects for the log

No gridflow defect. One documentation defect for the vault, finding 5 (England omitted from the "within a nation" sentence). One
data observation for the logs, vendor side: NESO describes `Srg_BB005` as "Capacity installed (MW)" in tRESP but as "MW
availability" in the FES 2021 to 2025 definitions, and publishes it zero or negative in both (finding 4).
