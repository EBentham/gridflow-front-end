# entsoe/forecast_margin: author report

**Status.** Built with `gridflow-build --only entsoe/forecast_margin`: no errors. The detector returns only the accepted `em-dash-overuse` advisory, which counts the EIC `--` padding. The rendered page has 0 real em dashes. Screenshots are clean at 1440, 1024, 768 and 390.

**Recommendation: no hold.** The page stands on three zones, BE, FR and NL. I found one gridflow data defect (below): silver drops the sign of the margin. The page states the defect and leaves DE-LU out of the chart, following the precedent of `day_ahead_prices`, which leaves out DE-LU's mixed price sequences. If the seat prefers not to ship while the sign is lost in silver, holding the page is a reasonable alternative. The chart would then gain DE-LU once gridflow keeps `business_type`.

## Files

- **Canonical note:** `vault-p26-entsoe/30-vendors/entsoe/datasets/forecast_margin.md`.
  - Edited with the Edit tool. It is CRLF, with 0 LF-only lines.
  - The front matter contains no `---`. EIC dashes are written as `\x2D`.
- **Mirror:** `p26-entsoe/vault/entsoe/forecast_margin.md`. `cmp` shows it identical to the canonical note.
  - Before this round the mirror was an LF copy that differed from the canonical note. The copy fixed that.
- **Artefacts:**
  - `site/hifi/data/series/entsoe/forecast_margin.json`: `spec_origin: vault`, 3 points, `rows_used` 3, `duplicates_dropped` 33.
  - `site/hifi/data/samples/entsoe/forecast_margin.json`: `gridflow-sample`, 8 rows.
  - `site/hifi/data/notebooks/entsoe/forecast_margin.json` plus `forecast_margin-5.png`: `run_notebooks.py`, 5 cells, 1 image, no errors.
- **Retired files:** there was no staged spec and no authored override for this dataset.

## What the data is

- **Contents.** Local silver has 12 daily files (1 to 5 Aug and 8 to 14 Sep 2026), each with 4 rows: 48 rows in all.
  - Every row has the same `timestamp_utc`, 2025-12-31 23:00 UTC, and `resolution` `P1Y`.
  - The values are identical in every file: DE-LU 4126.0, BE 180.0, FR 1500.0, NL 41891.044.
- **Why every file repeats the year.** The explanation is the same as for `installed_capacity`.
  - gridflow sends one request per zone per UTC day (`client.py:162`, `day_subwindows`).
  - Each one-day reply carries the whole 2026 year document, with period `2025-12-31T23:00Z` to `2026-12-31T23:00Z`.
  - So every daily file repeats it. The transformer dedups only within one day (`forecast_margin.py:62`).
- **Zones.** gridflow queries six zones by default (`endpoints.py:395`, `DEFAULT_ZONES`). GB and IE-SEM (`10Y1001A1001A59C`) return code 999 acknowledgements.
- **Unit.** `quantity_Measure_Unit.name` is `MAW` in every bronze reply, which is MW.
- **Meaning and sign.**
  - Reg. 543/2013 Art. 2(30) defines the term (quoted below).
  - The sign is carried by `TimeSeries/businessType`, not by `quantity`. ENTSO-E Code Lists v29r0, section 3.4 BusinessTypeList, p. 16:
    - A91 "positive forecast margin";
    - A92 "Negative forecast margin".
  - Bronze: all 12 DE-LU replies are A92, and all 36 FR, NL and BE replies are A91 (`grep businessType | uniq -c`: 36 A91, 12 A92).
  - The parser reads `business_type` (`parsers.py:453`), but the transformer's `output_cols` (`forecast_margin.py:75-83`) do not keep it. DE-LU's negative margin of 4,126 MW therefore sits in silver as +4126.0.

## Definition (sourced)

EUR-Lex returned an empty page to the fetcher. I took the text from the as-adopted version of the regulation on legislation.gov.uk (`/eur/2013/543/article/2/adopted` and `/article/8/adopted`). Two fetches returned identical wording.

- **Art. 2(30):** "'year-ahead forecast margin' means the difference between the yearly forecast of available generation capacity and the yearly forecast of maximum total load taking into account the forecast of total generation capacity, the forecast of availability of generation and the forecast of reserves contracted for system services;"
- **Art. 8(1):** "For their control areas, TSOs shall calculate and provide for each bidding zone the year-ahead forecast margin evaluated at the local market time unit to the ENTSO for Electricity. The information shall be published one week before the yearly capacity allocation but no later than the 15th calendar day of the month before the year to which the data relates."

The page quotes Art. 2(30) up to "maximum total load" and names it as Article 2(30). The note body carries the full quote and the Art. 8(1) text.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Art. 2(30) quote (what_it_is) | legislation.gov.uk `eur/2013/543/article/2/adopted`, point (30); fetched twice, same text |
| A91 positive, A92 negative (what_it_is, how_used, caption, fields, record.caption) | ENTSO-E Code Lists v29r0 §3.4 BusinessTypeList p.16, from `pdftotext` of `eepublicdownloads.azureedge.net/.../entso-e-code-list-v29r0.pdf`, lines 947-951 inside §3.4 (lines 425-1099) |
| Silver drops it (what_it_is, caption, fields) | `silver/entsoe/forecast_margin.py:75-83` output_cols have no `business_type`; `parsers.py:453` emits it |
| DE-LU sent as A92, 4,126 (caption, alt, record.caption) | Bronze `2026/09/14/raw_20260915T201814Z_45ecfc97.xml` and 11 more; A92 on all 12 DE-LU replies; silver value 4126.0 |
| 2026 stamped 23:00 UTC 31 Dec 2025 (what_it_is, caption, fields) | Silver `timestamp_utc` unique value; bronze `Period/timeInterval/start` `2025-12-31T23:00Z`; position 1 = start (`parsers.py:527-528`, `_advance_calendar` at `:76-93`) |
| 23:00 UTC is midnight CET (fields.timestamp_utc) | 1 January is in winter time, CET = UTC+1 |
| MW, `MAW` (facts, fields, caption) | `quantity_Measure_Unit.name` `MAW` in every bronze reply |
| One `P1Y` point per year, as sent (cadence) | Every row has `resolution` `P1Y`; one Point per TimeSeries in bronze |
| Grain: one row per year and zone, per silver file | Dedup `(timestamp_utc, area_code)` within a day (`forecast_margin.py:62`); 12 copies across files |
| Key `(timestamp_utc, area_code, published_at)` | Unique on 48 of 48 rows (Polars `unique().height` 48) |
| Each silver file repeats it; one copy kept (caption) | Series provenance: `rows_matched` 36, `duplicates_dropped` 33, `rows_used` 3 |
| Chart values NL 41,891, FR 1,500, BE 180 (alt, title) | Committed series `values` [41891.044, 1500.0, 180.0], x [nl, fr, be] |
| BE bar is a sliver (alt) | Screenshots: BE is a 1 to 2 px bar with a "180" label |
| One GET per zone and UTC day, six zones (raw_feed.note) | `client.py:162` day_subwindows; `endpoints.py:395` DEFAULT_ZONES |
| One-day request returns the whole year's document (raw_feed.note) | 72 bronze replies: 48 `GL_MarketDocument`, 24 acknowledgements. All 48 have `time_Period` `2025-12-31T23:00Z` to `2026-12-31T23:00Z` (`grep | sort | uniq -c`). Scoped as "in these responses" |
| DE-LU is the only A92 zone (lead defect) | `grep -l 'businessType>A92' | xargs grep -l 10Y1001A1001A82H | wc -l` gives 12, and 12 A92 tags in total |
| related `load_forecast_yearly` "for the same zones" | Silver `load_forecast_yearly` `area_code` uniques: DE-LU, BE, FR, NL (12 files) |
| GB and IE-SEM return code 999 (raw_feed.note) | Bronze acknowledgements, e.g. `2026/08/01/raw_20260816T135005Z_747838e7.xml` (GB), `..._e0944def.xml` (IE-SEM) |
| Request URL and parameter order (raw_feed.requests) | bronze `.meta.json` `request_url`: documentType, periodStart, periodEnd, outBiddingZone_Domain, processType, securityToken; `client.py:293-294` |
| Ingest end excluded, transform end included (commands) | `utils/time.py:123-143` day_subwindows, `[start, end)`; transform `--end` inclusive (brief); silver file `forecast_margin_20260914` matches bronze day 14 Sep |
| `published_at` is a fetch-time stamp (fields) | Ruling #39; `published_at` within seconds of `fetched_at` in `.meta.json` (e.g. 13:50:07 against 13:50:07.45) |
| Sample = last two fetches, four zones each (record.caption) | `published_at ge 2026-09-15T20:18:01Z` gives 8 rows: files 20260913 and 20260914 |
| query() relation, date column, lineage dropped (notebook.lead) | `gridflow_models/.../handles/source.py:426-450`; `schema_manifest.py:164` `timestamp_utc`; the same reading as `installed_capacity`, which its checker approved |
| plot_alt | `forecast_margin-5.png`: labelled bars NL 41,891, FR 1,500, BE 180 |
| related resolve | Build green; `load_forecast_yearly.html` is a refresh pointer to `load-forecasts.html#load_forecast_yearly` |

## Chart

- **Type:** a bar by `area_code` for BE, FR and NL.
  - Filter: `area_code ne 10Y1001A1001A82H` and `timestamp_utc eq 2025-12-31T23:00:00Z`.
  - Dedup on `(timestamp_utc, area_code)`, keeping the latest `published_at`.
  - `sum` over the one remaining row each, sorted by value, descending.
- **Window:** the 2026 year document, stamped 23:00 UTC on 31 December 2025.
- **Why DE-LU is out:** its value would be drawn with the wrong sign, which rubric §2 forbids. The caption says why.
- **Paints:** NL olive, FR horizon, BE clay. These match `day_ahead_prices`.

## Body corrections (canonical note, smallest spans)

1. **Overview.** The paraphrase "TSO-published reserve margin metric ..., indicating capacity surplus over expected peak demand" is replaced by the verbatim Art. 2(30) and Art. 8(1) text, with its source.
   - Added: the responses we hold carry one `P1Y` point, not a value per market time unit.
2. **Code 999 line.** "GB returns code 999" now names GB and IE-SEM. Added a **Sign** paragraph with the code-list citation, and the fact that DE-LU is A92 while FR, NL and BE are A91.
3. **Bronze granularity.** "One file per (zone, query window)" was wrong. It is one file per zone per requested UTC day (`client.py:162`), each holding the whole year's document.
4. **Bronze sample.** DE-LU was shown as A91 with quantity 12500. It is now A92 with 4126, as sent, and `quantity_Measure_Unit.name` `MAW` is added.
5. **Dedup key.** Added "within one transform day only" (`forecast_margin.py:62`).
6. **Silver schema.**
   - `forecast_margin_mw` said "MW (positive = surplus)". It is now: unsigned, and `businessType` is not kept (`forecast_margin.py:75-83`).
   - `timestamp_utc` is now described as the period start (`parsers.py:527-528`).
   - The missing `published_at` row is added (DATA-MATRIX `≈`).
7. **Silver sample.** The fictional 2026-05-06 row is replaced by the real NL row from the 14 Sep file (published_at 20:18:12, ingested_at 20:18:17.839353).
8. **Known issues.**
   - "P1Y mapped to 365 days approximation" was stale. `P1Y` uses calendar arithmetic (`parsers.py:47`, `:76-93`).
   - "Negative or zero margin indicates shortfall" is replaced by: a negative margin is not visible in silver (A92, sign dropped).
   - Added: IE-SEM also returns code 999.
   - Added: the repeated-year-document note and the cross-file dedup recipe.

I left the curl example, the query-parameter table, "Historical depth ~5 years" and "Publication lag Yearly" unchanged. The curl example is valid for the vendor. The other two I could not verify, and the page does not use them.

## Could not verify

- **NL's value.** NL's 41,891.044 MW is more than an order of magnitude above FR's 1,500 and BE's 180. The feed does not say how each TSO computes its margin. The page states the values as sent and claims no cause.
- **Other years.** Whether a request for a 2025 day returns the 2025 document. Local data holds only the 2026 document, so the page says nothing about other years.
- **Code list version.** The code list I read is v29r0 (2014). A newer release could, in principle, reword A91 and A92. A web-search summary gave the same meanings, but I read no newer PDF myself.
- **Time unit.** Art. 8(1) asks for a margin "evaluated at the local market time unit", but the replies carry one `P1Y` point. The page says only what the replies carry.

## Open questions for the seat

1. **Ship or hold.** Ship with DE-LU left out and the defect stated, or hold until gridflow keeps `business_type`? I recommend shipping; the seat decides.
2. **Checker focus.** The DE-LU exclusion and the `forecast_margin_mw` guide line ("unsigned: the A91 or A92 sign is dropped") are the page's one judgement call.
3. **`how_used[2]` is deliberate.** "Flagging a zone whose TSO sends a negative margin (A92) for the year" is a use of the feed that silver cannot deliver today, because it drops the sign. `what_it_is` says so two sentences earlier. I kept it because it names the use the defect blocks. If the checker reads it as a contradiction, the fallback is "Flagging a zone whose TSO sends a negative margin (A92), read from bronze".

## Template problems

- **None found.** The BE bar (180 against 41,891) renders as a thin but visible labelled sliver at every width.
- **No dark theme.** The site has no dark mode: there is no `prefers-color-scheme` or `data-theme` in `assets/*.css` or `*.js`. The rubric's "light and dark" check therefore reduces to light. This is not a defect of this page.

## Screenshots

- **How they were taken:** headless Chrome, each call under `timeout 60`, with `--timeout=15000 --virtual-time-budget=5000`, served on 127.0.0.1:9834. The server was stopped afterwards.
- **390:** taken through a 390 px iframe in a 500 px window.
- **Files:** in the scratchpad at `fm-shots/`: `w1440.png`, `w1024.png`, `w768.png`, `w390.png`, and slices `w<width>_<n>.png`.
- **What I checked at each width:**
  - hero scenery and turbine tops;
  - chart and legend;
  - the frame (folded) and its guide;
  - the notebook panel (at 390 the header is not clipped: the filename is short);
  - the stratum corner labels;
  - related datasets.
- **Result:** nothing clipped or overlapping.

## Defects (paste into gridflow BACKLOG and the vault remediation page)

- **[gridflow, silver transformer, data semantics] `forecast_margin` drops the sign of the margin.**
  - ENTSO-E carries the sign of A70 forecast margin in `TimeSeries/businessType`: A91 "positive forecast margin", A92 "Negative forecast margin" (ENTSO-E Code Lists v29r0 §3.4, p.16). `quantity` is sent unsigned.
  - `parse_timeseries_xml` emits `business_type` (`connectors/entsoe/parsers.py:453`), but `ForecastMarginTransformer.transform` does not keep it (`silver/entsoe/forecast_margin.py:75-83`).
  - DE-LU's 2026 margin is sent as A92, 4126 MW (every DE-LU reply, e.g. `bronze/entsoe/forecast_margin/2026/09/14/raw_20260915T201814Z_45ecfc97.xml`). Silver holds it as +4126.0, indistinguishable from a positive margin.
  - Fix: negate `quantity` when `business_type == "A92"`, or keep `business_type` as a column. Bump `DATASET_VERSION` and re-transform.
  - A test should assert that an A92 fixture yields a negative `forecast_margin_mw`.
- **[gridflow, inefficiency, same as `installed_capacity`] Repeated year document.**
  - One-day chunking (`client.py:162`) re-requests the identical A70 `P1Y` year document once per zone per UTC day. Every daily silver file repeats it (12 files, 4 identical rows each), and dedup (`forecast_margin.py:62`) acts within one file only.
  - Readers must drop duplicates across files. Cross-reference the `installed_capacity` and `installed_capacity_units` BACKLOG items rather than filing a duplicate.
- **[vault] `forecast_margin.md` stale facts, corrected in this batch.** The note had the sign semantics, bronze granularity, `P1Y` handling, a fictional silver sample, and a missing `published_at` row wrong. See "Body corrections".
- **[vault] Dead domain link.** `forecast_margin.md` links to `20-domain/concepts/capacity-adequacy.md`, which does not exist in the vault. It is left as is, outside this page's scope.
- **[gridflow, code comment, seat item already open] `published_at`.** It is the response `createdDateTime` (a fetch-time stamp), not an issue time (ruling #39).
