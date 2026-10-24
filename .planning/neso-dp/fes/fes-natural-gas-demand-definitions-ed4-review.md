# FES natural gas demand definitions (ED4): checker's review (round 1)

Package `fes-natural-gas-demand-definitions-ed4`, table `fes_ed4_gas_demand_defs` (4 editions). Checked in
`C:\gridflow-wt\fe-neso-fes` and `C:\gridflow-wt\vault-neso-fes`.

**Verdict: REVISE.** 1 major, 4 nits. No blockers. The page is honest and the facts hold; the major is one wrong
phrase in the notebook lead, with a one-line fix.

## What was run and passed

- Build `--only neso_data_portal/fes_ed4_gas_demand_defs`: no errors (the global 37-line gotcha warning only; it
  did not stop on another package's files). Detector on the built page: `[]`. 0 em dashes, 0 arrows in the page.
- `cmp` of the canonical note and the mirror: identical.
- Vault diff against `origin/master`: the `page:` block, `updated:` and one body sentence (the 2026 item 2 quote).
  The sentence is true: 2026 item 2 reads "Commercial demand here includes networked CNG used for transport." and
  the 2025 item 2 text lacks it. Smallest span, evidence given.
- Silver read in Polars (42 rows, 10/10/11/11) and checked against the four bronze CSVs with `csv.reader`: every
  description and definition is byte-identical to bronze (42 of 42). Trailing space on items 7 and 8 in every
  edition. Bronze bytes (1,515 / 1,570 / 2,062 / 2,488), BOM on 2024 only, comma cells 6/6/2/4, one embedded newline
  (2025 item 10): all match the note body. Request URLs equal the bronze sidecars' `request_url`;
  `published_at` equals each sidecar's `ckan_last_modified`.
- Catalogue snapshot `20261006T195819Z`: package notes quote ("an agreed set of data tables" ... "natural gas and
  residential heat demand"), created 2023-07-07, update frequency "Ad hoc", 2026 resource calls itself a "Ten-Year
  Outlook" output, field info "Unique Key" / "Description of data item in ED3" / "More in-depth breakdown of
  description": all match the page. Ingest and transform lines match the approved building-block page.
- Screenshots at 1440, 1024, 768 and 390 (390 through a 390 px iframe), server on 9954 started with its PID
  recorded and stopped by that PID (port then closed). Nothing clipped or overlapping: hero chips and the key chip
  wrap, request wells break the long URLs, related slugs wrap, the notebook panel fits. I unfolded the frame in the
  browser pane: it scrolls inside its box (table 7,705 px in a 895 px box), the definition column starts with the
  text and item 11's formulas are readable straight away.

## The six points you asked about

1. **ED3 boundary: holds.** The page links ED3 as related and names it only as the table NESO's dictionary says
   the items describe ("Description of data item in ED3"). Nothing describes ED3's rows, values or the label match.
2. **`type: none`: right.** A 10, 10, 11, 11 bar says four near-equal things the page already says: the grain line
   ("items 1 to 10, plus 11 from 2025"), item 11 in the frame, and notebook output 3 (counts per edition). The
   building-block count bar earns its place because its 49 to 64 step carries the advice to join on edition; this
   table's single step is better read as rows. No chart section renders and the `reason` text does not leak onto the
   page. Agree with the writer.
3. **Caption: true.** 2025 item 11 is `= 1+2+3+4+5+6+8`, 2026 is `= 1+2+4+5+6+8`, so the 2026 total omits item 3.
   Items 2, 3, 5 and 11 each differ between 2025 and 2026 as shown. Every definition is NESO's text verbatim (bronze
   check above), dated by the visible `edition` column and `published_at`. Whether "omits" reads as "transport is
   excluded": mildly, see finding 3.
4. **Edition changes reproduced from silver.** Between 2025 and 2026 the texts of items 2, 3, 5, 8, 10 and 11 differ
   and items 1, 4, 6, 7 and 9 do not (matches notebook output 4). The page claims only the four it shows, and each
   is a real change. (The writer's report calls those four "the definition changes silver shows"; six items
   changed. The page itself does not claim that.) 2024 to 2025 reworded every item; the page does not claim
   otherwise.
5. **Folded definition: reachable, with one gap.** Full text is reachable by unfolding (scrolls sideways) and by the
   notebook, which prints 2026 items 3 and 5 whole. Not all of it: see finding 1.
6. **FES 2026 / FES25: not corrected, not stated.** The 2026 item 5 text is verbatim in the frame and in notebook
   output 5, and the guide says "verbatim", so nothing is silently fixed. But no sentence on the page tells the
   reader NESO's text names two forecasts. It is only in the note body as a `TODO: verify`. See finding 4.

## Findings

1. **major** `page.notebook.lead`: "print NESO's longest texts whole" is wrong. The longest definition is 2025 item
   10 (538 characters); the cell prints 2026 items 5 (494) and 3 (443). Evidence: Polars
   `definition.str.len_chars()` sorted descending gives 2025/10 = 538, 2026/5 = 494, 2026/3 = 443. The writer's
   report also says "up to about 490", which is the same slip. Fix: reword to "and print NESO's two longest 2026
   texts whole", or widen the cell to also print 2025 item 10 and say "three longest".
2. **nit** `page.notebook.cells[2]` (the print cell): the caption's claim rests on item 11's two formulas, and no
   notebook output shows them (they are visible only after unfolding the frame). Adding item 11 for 2025 and 2026
   (and 2026 item 2) to the printed set would make the caption checkable from the notebook alone. Optional.
3. **nit** `page.record.caption`: "the 2026 total omits item 3" is true but gives no reason, and the reason sits in
   the folded `definition` column. At 768 and 390 the frame shows only `item_no` and `edition` until unfolded, so the
   caption is the only visible sentence. A short NESO-sourced tail would help, for example "(NESO's 2026 item 3 text
   says its networked part is already in commercial, item 2)". Do not say item 3 is "counted in item 2": item 3 also
   holds non-networked LNG, which NESO says is not in commercial.
4. **nit** `page.record.fields.definition` or `page.notebook.lead`: state NESO's 2026 item 5 inconsistency in one
   clause ("NESO's 2026 item 5 names both 'FES 2026' and 'FES25'; typos are NESO's too"). Verbatim reproduction is
   honest, but a reader of the notebook output sees the two names with no remark and may blame gridflow. The same
   applies to NESO's typos in the 2026 item 3 text ("is not be added", "gas networked gas demand"). `definition`'s
   guide line is 13 words, so there is room for one more clause only if it is reworded.
5. **nit** `page.summary` and `page.related[2]`:
   - summary: "its FES natural gas demand summary table (ED3)" fits the 2025 and 2026 resource titles ("Natural Gas
     Demand Summary (ED3)"). NESO's 2023 and 2024 ED3 files were titled "Natural Gas and Residential Heat Demand
     Summary (ED3)", and `what_it_is` quotes package notes saying the same for the whole package, while the 2025 and
     2026 ED4 resource descriptions say natural gas only. Either say "natural gas demand summary tables (ED3)" or
     add that NESO's 2025 and 2026 descriptions drop "residential heat".
   - related ED6: "NESO's text notes file for the FES road transport table" says what ED6 is, not how it relates to
     gas demand definitions; the link is weak. Swap it or give the relation (for example item 3, transport gas).

## Template and seat items (not findings)

- The frame cannot wrap long text: at 768 and 390 only `item_no` and `edition` show, so the folded frame is a column
  of numbers and years until unfolded. The writer already logged this.
- `raw_feed.requests` allows four, so the 2024 file URL is left off (the note says "Shown: 2023, 2025 and 2026").
- The ED3 and WS1 related links point to held pages, which is allowed.

## Defects (pasteable)

- None new for gridflow. The writer's two entries stand (frame cannot show long text; NESO's 2026 item 5 names two
  forecasts). Add: the writer's "definition up to about 490 characters" should read 538 (2025 item 10).

---

## Round 2

**Verdict: APPROVE.** No findings above nit; all five round 1 findings are fixed. Rebuilt with
`--only neso_data_portal/fes_ed4_gas_demand_defs`: no errors (only the global 37-line gotcha warning). Detector `[]`.
`cmp` of the canonical note and the mirror: identical. 0 em dashes in the built page. Notebook JSON written by
`scripts/run_notebooks.py`, 6 cells, no error outputs. Checked from the built page text and the notebook JSON; layout
is unchanged (words and one notebook cell), so no server and no new screenshots.

1. **Major (notebook lead, "longest texts"): fixed.** The last cell now picks `defs.definition.str.len().nlargest(3)`.
   Silver lengths: 2025 item 10 = 538, 2026 item 5 = 494, 2026 item 3 = 443, then 232 (no tie at the cut). The
   notebook output prints exactly those three, in that order, whole (item 10 with its embedded newline). The lead now
   says "the three longest definitions whole, NESO's typos included", which is true.
2. **Nit (item 11 formulas in the notebook): fixed.** New cell output shows `= 1+2+3+4+5+6+8` (2025) and
   `= 1+2+4+5+6+8` (2026), equal to silver.
3. **Nit (caption reason): fixed, and sourced.** Caption: "2025 and 2026: the 2026 total omits item 3, whose
   networked CNG is in item 2." NESO's 2026 item 3 text: "The networked element of gas demand for transport is
   included within the commercial demand"; NESO's 2026 item 2 text: "Commercial demand here includes networked CNG used
   for transport." The caption claims only the networked part, not that item 3 is counted in item 2, so the
   non-networked LNG point is respected.
4. **Nit (FES 2026 / FES25): fixed.** `what_it_is` ends "The 2026 item 5 text (file of 16 September 2026) names the
   earlier forecast "FES 2026", then "FES25"." Both names are verbatim from silver (`In the FES 2026 10 Year Forecast`
   ... `hence the FES25 10 Year Forecast`), uncorrected, and the date is the resource's `last_modified`
   (2026-09-16T14:59:52). Reading both as the earlier forecast follows NESO's "hence"; the note body still says which
   edition is meant is unverified, which is consistent.
5. **Nit (ED3 naming, ED6 relation): fixed.**
   - Summary now says the items are for "FES ED3 summary tables, titled Natural Gas Demand Summary from 2025", which
     matches the catalogue (2023 and 2024 titled "Natural Gas and Residential Heat Demand Summary", 2025 and 2026
     "Natural Gas Demand Summary").
   - `what_it_is` adds that the 2025 and 2026 ED4 file descriptions say natural gas only; the snapshot agrees.
   - ED6 related note, "Does for road transport table ED5 what this page does for ED3", matches ED6's own note ("a
     codebook for ED5") and its reciprocal link to this page.

Body edit unchanged and still true. Frame sample unchanged. No new issues.
