# Aggregated BSAD page: review 1

Page `neso_data_portal/aggregated-bsad` (table `aggregated_bsad`). Checker: Sonnet 5.5 · high, 2026-10-18. Inspection only; port 9923 server and every Chrome process I started are stopped.

**Verdict: REVISE** (1 major, 4 nits, 0 blockers)

## Gates run

- `uv run --system-certs --extra build gridflow-build --only neso_data_portal/aggregated_bsad`: succeeds. The only message is the caveat warning (three "Known issues" lines dropped), which is a seat matter. Whether the dropped lines leave the page inaccurate: no, apart from the point in nit 3.
- `detect.mjs --json`: `[]`.
- Mirror `vault/neso_data_portal/aggregated-bsad.md` is byte-equal to the canonical note (`cmp` clean).
- Page text grep (`—`, `–`, `·`, `→`, live, now, yet, soon, planned, held, locally, "since 20", "% of"): no hits in the page or the `page:` block.
- Screenshots taken at 1440, 1024, 768 and a true 390 (390 px iframe), in sections, plus the unfolded frame at 1440 and 390 (CSS checkbox clicked over the DevTools protocol). Nothing is clipped or overlapping: hero scenery, chart, frame (folded and unfolded), guide, notebook panel, corner labels. The site has no dark theme, so light only.

## What I re-derived (all passed)

- **Six zero columns, from silver.** All 176,544 rows across the 11 parquet files (both captures): `ebca`, `ebva`, `sbva`, `esca`, `esva`, `ssva` and `spa` each have 0 non-zero and 0 null values. `bpa` has 3,181 non-zero rows, none negative. The 2020-21 bronze file (17,531 rows) also has the six at zero and 476 non-zero `bpa` rows.
- **Chart series against silver.** I rebuilt the daily maximum from silver (newest capture per settlement date and period, window 2016-04-01 to 2026-10-15). All 3,485 points match the committed series exactly (0 mismatches, none missing either way). Spot checks: 2017-01-16 is 159.55; 2023-10-20 is 5.56; 2024-05-24 is 7.47; 2024-08-13 is 5.72; 2025-10-24 is 0.78; 2026-01-15 is 10.65; 2016-04-01, 2019-06-10, 2021-04-01 and 2026-10-15 are 0.
- **Alt text.**
  - Three days over 60: 2017-01-16 (159.55), 2017-01-23 (124.8), 2017-03-24 (102.81).
  - The largest value below 60 is 56.56 (2021-11-23).
  - After 2023-10-20 there are exactly four non-zero days, the last 10.65 on 2026-01-15.
  - The only date jump is 2020-03-31 to 2021-04-01.
  - The x axis is true to date: the 2017 tick sits at 131.9 px, which matches 275 days from 2016-04-01.
- **Notebook.**
  - The financial-year table (890, 580, 413, 292, 423, 412, 119, 25, 27, 0; highest 159.55 and so on) matches the same computation on the newest-capture view.
  - The `plot_alt` numbers match: none before period 14; 3 to 55 over periods 14 to 30; 125 at period 31; peak 309 at period 36; 5 at period 46; none after.
  - The runner stamp is `scripts/run_notebooks.py`. Every cell is read-only and no output errors. The plot PNG matches `plot_alt`.
- **Sample rows.** The eight rows match silver (2026-01-15, periods 33 to 40; `timestamp_utc` 16:00 to 19:30 UTC). The caption "steps from 10.65 to 9.15, then zero" is right.
- **Coverage statement.**
  - The CKAN snapshot lists 13 resources, 2013-14 to 2026-27, with none for 2015-16.
  - Silver holds 10 of them (2016-17 to 2019-20, 2021-22 to 2026-27).
  - The 2020-21 bronze file has 11 repeated keys (27/06/2020 periods 1 to 7 and 9 to 11, and 05/07/2020 period 1), each pair identical, so "repeats 11 periods" is exact.
  - Nothing on the page implies 2013-14, 2014-15, 2015-16 or 2020-21 are covered.
- **Units.** £, MWh and £/MWh come from the saved field info (`unit` strings, the pound sign is stored correctly as UTF-8 in the file; it only looks corrupt in a cp1252 console) and from the epoch 1 registry headers.
- **Requests and commands.** The base URL, `/api/3/action/package_show?id=`, the upload URL and `/datastore/dump/<id>` match `sources.yaml`, `endpoints.py` and `client.py`. `--last 24h` matches the admissibility rule (a window ending more than 48 h ago is refused). The skip and keep rules in `raw_feed.note` match `client.py` (upload skip on `last_modified`, dump kept only if the body sha256 changed).
- **Related notes** are 9, 11 and 9 words. `elexon/netbsad` does carry eight terms (`schemas/elexon.py:824-839`).
- **"Superseded, carried as zero."** Independent check of the source, see nit 2: the Elexon BMRA Service Description lists exactly these six (EBCA, EBVA, SBVA, ESCA, ESVA, SSVA) as "NETBSAD variables submitted as zero" for Settlement Days on or after the P217 effective date. The claim is true for the page's window (it starts 1 April 2016).

## Findings

1. **Major.** `page.chart` / `page.chart_view.caption` / `page.chart_view.x_label` (rendered chart): the 2020-21 break cannot be seen, so the chart looks as if 2020-21 is covered with zeros.
   - **What is wrong.** The renderer does draw two separate paths, so the line is truly broken. The second path starts at `M458.3 410`. But a zero day sits at y = 410, exactly where the axis line (`M74 18 V410 H884`) runs. In the 1440, 768 and 390 screenshots the stretch from April 2020 to March 2021 is a flat baseline, indistinguishable from 2024 to 2026, which really is zero. The only signals are the caption sentence and the italic x label under the plot. A reader who looks at the plot first reads "no adjustment in 2020-21", which is the false-coverage reading the page must avoid. Zero days and unloaded days are different facts and look the same.
   - **Evidence.** Built page SVG paths for the wide chart: first series path begins `M74.1 410`, second begins `M458.3 410`; no mark in the gap. Screenshots `c1440.png`, `za768.png`, `zb390.png` (scratchpad, `bsadshots`). Series JSON: x skips 2020-03-31 to 2021-04-01 with no null points in between.
   - **Suggested fix.** Probably seat-side (the chart renderer: a hatched or labelled band for a gap in a line chart). A page-side mitigation is to put the warning in the plot's own words, for example in the key note: "The flat line is the axis: no data was loaded for April 2020 to March 2021."

2. **Nit.** `page.what_it_is` ("Elexon's interface document carries the six cost and volume terms as superseded fields, sent as zero") and `page.record.fields.{ebca,ebva,sbva,esca,esva,ssva}` ("superseded, carried as zero (BSC)"): the support is a paraphrase, not read.
   - The author did not read the Elexon document (author report, "Not verified"). The note body gives only the K-AS-4-FACTS paraphrase (line 248); the link in FACTS is NETA IDD Part 1 v57.0, whose page is truncated and itself marked SUPERSEDED as a document version, and I could not find the six fields in what loads.
   - The rule is real and I confirmed it in a different BSC document: the BMRA Service Description (version 24.1, section 7.2 and footnote 1) lists the six as variables submitted as zero from the P217 effective date, and asks that non-zero values be reported to BSCCo.
   - The substance is correct for the page's window. If you keep "interface document", say which one, or name the BMRA service description in the note body with the footnote as the quote. The guide lines are also unscoped (the rule is "from P217", 2015; the page's window starts in 2016 so nothing breaks).
   - `spa` is zero in every row too but the page, correctly, does not call it superseded (BMRA lists SPA as a live term).

3. **Nit.** `page.how_used[0]` ("for imbalance price studies and back-tests"): the page never says that `available_at` is the capture time for the whole history, so a back-test cannot use the table to say when an adjustment was known.
   - The note body says it (Known issues, "Same `available_at` for all history"; methodology permits amended and post-event submissions); the build warning means that line may be among the three dropped. The guide says only that `published_at` is null.
   - Not inaccurate, but it is the one dropped caveat a user of "back-tests" would need. Consider "for imbalance price studies" alone, or one clause on capture time.

4. **Nit.** `page.notebook.needs` ("one capture of each of the package's files"): three of the 13 files cannot reach silver (two fail on encoding, 2020-21 on repeated keys), and there is none for 2015-16. A reader who ingests every file still has no rows for those years. Suggest "one capture of each file from 2016-17 on (2020-21 will not load)".

5. **Nit.** `page.what_it_is`, `page.chart_view.key` (BPA and SPA meaning): the page claims nothing it cannot support, and I found no unsupported claim; but it never says what the adjuster is. Elexon's glossary entry for BPA gives the BSAD methodology formula (option fees for standing reserve, firm regulating reserve and forward contracts, divided by the contracted MWh, set to zero when the denominator is zero) and says it is added when the net imbalance is short. I fetched this page only as a model-summarised read, so I have not confirmed the wording; verify before use. The key note "NESO gives the unit, £/MWh, but not the sign convention" is true as scoped to NESO; if you cite Elexon, the sign note can say who does state it. Optional; the shipping decision is the seat's.

## Not findings (checked)

- Chart choice. A daily maximum is stated in the title and caption and applied by the spec (`aggregation: max`, `dedup` on date and period ordered by `available_at`). The six cost and volume series would be a flat zero line, so `bpa` is the only informative column. A 10-year daily line is a reasonable reading; a recent window would be flat zero since 15 January 2026.
- `settlement_date` as x axis: fine; one point per settlement day with no BST split.
- "gridflow loads 2016-17 on, except 2020-21" (`facts.history`) is a statement about load coverage, but Bobbo's seat ruling says to ship with the loss stated, and it is accurate. Possible reader question (why 2013-15 is absent) is answered only by the omission; acceptable.
- Frame: eight real rows, `shape: (8, 19)`, key columns first in the guide and marked with a square, a guide line for every column except the pipeline ones, no line over 14 words. Unfolded frame scrolls sideways at 1440 (template behaviour, as on the other pages).
- Vault body edits (the 2026-10-16 capture): each edit cites its Polars check; they are smallest-span and consistent with silver (latest view 167,376 rows, all captures 176,544; the 9,168 shared periods are identical; 432 new periods). I did not diff the shared-period values myself beyond the row counts; the counts match.
