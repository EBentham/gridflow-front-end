# entsoe/water_reservoirs: checker review

Checker: Opus 5.5 · high, 2026-09-29. Screenshot port 9850 (stopped). Inputs: vault note diffed against
quant-vault `origin/master` in the vault worktree, the three artefacts, the page built with
`gridflow-build --only entsoe/water_reservoirs`, the writer's report.

## Verdict: APPROVE

No blocker or major findings. Three nits follow; none changes the verdict.

## Findings

1. **nit** · `page.record.select.columns`
   - **What is wrong:** the order is `[timestamp_utc, area_code, reservoir_mwh, published_at, resolution]`.
     At 768 px the frame folds after `reservoir_mwh`, so the eight rows show the same week, zone and
     value, and the column that tells them apart (`published_at`, a key column) is folded away. At 390 px
     only `timestamp_utc` shows. That is template behaviour.
   - **Batch rule:** BATCH-entsoe.md "Samples" says to put the columns that tell rows apart first.
   - **Suggested fix:** `[timestamp_utc, area_code, published_at, reservoir_mwh, resolution]`. The
     value is identical within a week, so it loses nothing by folding first.
   - **Evidence:** screenshot `w768_2.png` shows the columns timestamp_utc, area_code and reservoir_mwh,
     then the fold marker.

2. **nit** · `page.how_used[1]`
   - **What is wrong:** "as Article 16 intends" puts an intent on the regulation. Art. 16(1)(d) only
     requires the prior-year figure to be published alongside ("including the figure for the same week
     of the previous year").
   - **Response content:** gridflow's A72 responses carry one `Point` per document, so the prior-year
     figure is not in the rows. A reader needs last year's weeks ingested to make the comparison.
   - **Suggested fix:** "Article 16 publishes the same week's figure a year earlier" (or similar).
   - **Evidence:** legislation.gov.uk/eur/2013/543/article/16; bronze FR XML `<position>1` only.

3. **nit** · `page.chart_view.key[0].note`
   - **What is wrong:** "stamped at the week's start, 22:00 UTC Sunday" is unscoped. The rule is
     Monday 00:00 Paris time, which is 23:00 UTC in winter.
   - **Why only a nit:** every drawn point is a summer week, and `what_it_is` scopes it correctly ("in
     these rows (midnight Monday in Paris)").
   - **Suggested fix:** "22:00 UTC Sunday here" or "Monday 00:00 Paris time".

Recorded, not findings (for a cold re-check):

- **Vault note body, "Silver sample":** the illustrative row still has no `published_at`, and it still
  uses an NO-1 zone that the connector cannot request. The writer states this in the report and did not
  invent a value. The body schema table now lists the column, which is enough.
- **Failing blank-page test:** `test_dataset_page.py::test_a_page_without_a_page_block_is_blank` fails,
  as seat ruling 2 expects.
- **Detector advisory:** `em-dash-overuse` ("43 em-dashes") counts the dashes in `10YFR-RTE------C`,
  which rulings #39 and #40 accept. The rendered text has 0 real em dashes (`grep -c "—"` gives 0), and
  no middle dots or arrows.
- **Thin-coverage wording:** "in the responses gridflow holds", "Of gridflow's six zones, only France
  returns a document" and "No weeks stamped 9 to 30 August are drawn" fall under seat ruling 1 (thin
  coverage stated plainly, not held) and the BATCH cadence ruling ("as sent in the responses we hold").
  - The gap sentence describes what the chart draws, not a local holding count.
  - It is exact: 9, 16, 23 and 30 August are the four Sunday 22:00 UTC stamps between 2 August and
    6 September.

## Evidence

### Focus 1: the key

- **Code key:** `silver/entsoe/water_reservoirs.py:59` runs
  `unique(subset=["timestamp_utc","area_code"], keep="last")`. It acts on one `read_bronze(target_date)`
  frame (`:27-41`), so it dedups within one partition only.
- **Rows per week in silver** (Polars over all 18 files): `group_by("timestamp_utc","area_code").len()`
  gives 26 Jul ×2, 2 Aug ×3, 6 Sep ×6 and 13 Sep ×7. `n_unique(reservoir_mwh)` is 1 for each week.
- **Uniqueness:**
  - The per-file maximum of `group_by(file, timestamp_utc, area_code).len()` is 1.
  - `(timestamp_utc, area_code, published_at)` is unique on 18 of 18 rows.
  - So the page's three-column key holds, and the grain line ("per silver file; each day's file repeats
    it") is exact.
- **Chart:**
  - The spec has `dedup: {on: [timestamp_utc, area_code], order_by: published_at}` and
    `aggregation: last`.
  - The series provenance reads `rows_read 18`, `duplicates_dropped 14`, `rows_used 4`, so no repeat
    is counted.
- **Sample:** 8 real rows (`generated_by: gridflow-sample`): 2 copies of the 26 Jul week (files 0801
  and 0802) and 6 of the 6 Sep week (files 0908 to 0913).
  - The 0913 copy is the 26 Sep re-fetch. The partition held two files, and the within-file dedup kept
    the later one.
  - The caption "one copy per requested day, same value" is exact, and the rows make no count claim.
- **Notebook:** it dedups the same way (`sort_values("published_at").drop_duplicates(key, keep="last")`),
  and cell 4 outputs exactly 4 rows.

### Focus 2: the chart

- **Series values:** series `x` = 2026-07-26T22Z, 08-02T22Z, 09-06T22Z, 09-13T22Z. The values are
  2261238, 2191776, 1989272 and 1952966. These equal silver for each week, and match the alt text,
  caption and plot_alt.
- **What the stamp marks:** the start of the week.
  - The FR XML has `<start>` 2026-09-06T22:00Z, `<end>` 2026-09-13T22:00Z, `<resolution>P7D`,
    `<position>1`.
  - `parsers.py:530` sets `start + (position-1)×res`, so `timestamp_utc` is the Period start.
  - 26 Jul 2026 is a Sunday, and 22:00 UTC is Monday 00:00 CEST.
- **Drawing:** the renderer draws points mid-week, and the break is visible at 1440, 1024, 768 and 390.
  The x_label "points drawn mid-week" and the alt agree.
- **Request-to-week mapping:** all 19 FR documents follow it:
  - 0801 and 0802 give the 26 Jul week;
  - 0803 to 0805 give 2 Aug;
  - 0908 to 0913 give 6 Sep;
  - 0914 to 0920 (26 Sep run) give 13 Sep.
  - The 0913 request [13 Sep 00:00, 14 Sep 00:00) overlaps the 13 Sep 22Z week by 2 h, but returns
    only the 6 Sep week. So "the week containing its start" is the right wording, and it is scoped to
    the responses gridflow holds.

### Focus 3: "weekly average" and MWh

- **The regulation:** legislation.gov.uk/eur/2013/543/article/16, fetched 2026-09-29. EUR-Lex returned
  an empty page, as it did for the writer.
  - Art. 16(1)(d) reads "aggregated weekly average filling rate of all water reservoir and hydro
    storage plants (MWh) per bidding zone including the figure for the same week of the previous year".
  - Art. 16(2)(d) reads "on the third working day following the week to which the information
    relates".
  - Both match the quotes now in the note body verbatim.
- **The link to A72:** the no-data acknowledgements name data item `[16.1.D]`, which ties A72 to this
  article.
- **Unit:** all 19 FR `GL_MarketDocument`s carry `quantity_Measure_Unit.name` `MWH`. No code parses it:
  a grep for `Measure_Unit` over `src/gridflow` finds nothing, and `EntsoeWaterReservoirs`
  (`schemas/entsoe.py:265-274`) has no unit column. `record.fields.reservoir_mwh` says so ("the unit
  field is not stored").
- **Overstatement:** none.
  - "weekly average" and "MWh" are the regulation's own words, attributed in `what_it_is`.
  - The summary's "energy stored" glosses a filling figure in MWh, and that gloss is fair.

### Focus 4: zones

- **The zone list:** `endpoints.py:395` sets `DEFAULT_ZONES = ["GB","FR","NL","BE","DE-LU","IE-SEM"]`.
  `client.py:249` loops over it unconditionally, with no zone parameter.
- **No other zone can be passed:**
  - `client.py:306` calls `_optional_filter_params` (`:567-575`), which forwards only
    `doc_type.optional_params`.
  - A72 (`endpoints.py:113-118`) declares none; the dataclass default is `()`.
  - So `**params` cannot add a zone. The body's corrected implementation-delta line is right.
- **Bronze tally:** 126 XML files.
  - 19 are `GL_MarketDocument`s, all `in_Domain=10YFR-RTE------C`, `MWH`, 1 Point each.
  - The other 107 are `Acknowledgement_MarketDocument`s: 21 each for GB, NL, BE, DE-LU and IE-SEM,
    plus FR for 14 Sep (fetched 15 Sep, before that week ended) and 21 Sep.
  - Silver `area_code` has only `10YFR-RTE------C`.

### Other rubric checks

- **Request URL:** `raw_feed.requests` matches bronze `2026/09/08/raw_20260915T201243Z_1c699540.meta.json`
  `request_url` in host, path, parameter order and `ENTSOE_DT_FORMAT`.
- **Commands:**
  - Ingest `--end 2026-09-15` excludes 15 Sep: `day_subwindows` covers `[start, end)`, and a midnight
    end drops that date (`utils/time.py:123`).
  - Transform `--end 2026-09-14` is inclusive (`pipeline/runner.py` `date_range(start.date(), end.date())`).
  - Starting ingest at 27 Jul is right: the 26 Jul day would return the 19 Jul week.
  - There are no `PARTITION_SOURCE_OFFSETS`.
  - `notebook.needs` "27 July to 14 September 2026" matches the commands.
- **Notebook:**
  - The lead matches `SourceClient.query` (`gridflow_models/research/handles/source.py:401-451`):
    the date column `timestamp_utc` (`silver/schema_manifest.py:191`), inclusive ends via
    `_date_range_predicate`, the bitemporal exclude, and `ORDER BY` the date column only.
  - The cells are read-only, and no output has an error. `generated_by: scripts/run_notebooks.py`.
  - The PNG shows two segments at about 2,261 to 2,192 GWh and about 1,989 to 1,953 GWh with a break,
    as `plot_alt` says.
- **Record fields:**
  - `area_code` comes from `inBiddingZone_Domain.mRID` (the FR XML tag; `parsers.py:292`, renamed in
    `water_reservoirs.py:53`).
  - `published_at` is `createdDateTime` via `with_published_at` (`:70`). It is a fetch-time stamp:
    `createdDateTime` 13:46:44Z against the fetch file stamp `20260816T134644Z` (ruling #39).
  - `resolution` holds the ISO code as sent (`parsers.py:459`).
- **Related:** Polars on silver shows that France has B10 and B12 in both `actual_generation`
  (`production_type`) and `installed_capacity`. All notes are 12 words or fewer.
- **Chart provenance:**
  - The series has `spec_origin: vault` and the build's digest check passes.
  - No staged spec (`site/hifi/data/chart-specs/entsoe/water_reservoirs.json`) or authored override
    exists.
  - The paint is `petrol` for one line; there is no khaki and nothing is summed.
- **No local data:** a grep of the rendered text for `locally`, `held`, `our `, `since 20`, `% of`,
  `N rows/days` finds nothing. The hits on "rows" are "in these rows" (scoping) and the help card.
- **Leakage and filler:** no planning labels, no "live", "now" or "real-time".
- **Build and detector:**
  - `gridflow-build --only entsoe/water_reservoirs` wrote the page and printed no errors.
  - The detector reports only the accepted advisory above.
  - The mirror `vault/entsoe/water_reservoirs.md` is byte-identical to the canonical note (`cmp`).
- **Vault body edits:** each cites evidence and changes the smallest span:
  - the regulation quote;
  - the publication lag (Art. 16(2)(d));
  - the dedup key scope (`:59`);
  - point-in-time `published_at` (`:70`);
  - the timestamp source (`parsers.py:530`);
  - `ingested_at` = transform time (`:61`);
  - `resolution` `P7D` (`parsers.py:459`);
  - the 30-day gotcha amended with bronze evidence;
  - NL and BE acknowledgements added;
  - the percentage gotcha marked unverified;
  - the `**params` claim corrected (`client.py:249`, `:306`, `endpoints.py:113`).

  The curl example is untouched.

### Screenshots (rubric 5)

- **Method:** headless Chrome under `timeout 60` with `--timeout=15000 --virtual-time-budget=5000`, served
  on 127.0.0.1:9850. Files are under the scratchpad at `wr-review-shots/`.
- **What I looked at:** the hero scenery (turbine tops), the facts and key row, the chart and its axes,
  the key note, the x_label, each stratum's corner label, the request and command blocks, the frame and
  its guide, the notebook panel and header, and the related notes.
- **1440, 1024, 768:** nothing is clipped or overlapping.
- **390:** a 390 px iframe.
  - With a 9000 px iframe, headless painting stopped at about 3,170 px. That is a capture artefact:
    the real page at 390 is 5,212 px tall.
  - Re-captured with the iframe sized to 5,212 px (`w390b_*.png`), the whole page painted. Nothing is
    clipped, and the notebook header fits `water_reservoirs.ipynb` and `gridflow_models`.
  - Measured in a browser tab at 390: document `scrollWidth` 390, and no element leaves the viewport
    except intended `sr-only` spans.
  - All 8 frame rows are present. Unfolded, the frame is 2,037 px wide inside its own `overflow:auto`
    box, and the page does not scroll sideways.
- **Dark mode:** no `prefers-color-scheme` or `data-theme` rules exist in `site/hifi/assets`, so there is
  only one mode to check.
