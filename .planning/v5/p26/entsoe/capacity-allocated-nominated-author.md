# capacity-allocated-nominated: author report

Family page `capacity-allocated-nominated`: lead `total_capacity_allocated`, member `total_nominated_capacity`. Writer: Opus 5.5 · high, 2026-09-29.

## Status

- `page:` block is on the lead's canonical note: `vault-p26-entsoe/30-vendors/entsoe/datasets/total_capacity_allocated.md`. Body corrections are in both notes. Both notes are mirrored byte for byte to `p26-entsoe/vault/entsoe/` (CRLF kept: 291/291 and 211/211 lines).
- Artefacts, all from real data:
  - `site/hifi/data/series/entsoe/total_capacity_allocated.json`: `spec_origin: vault`, 2 series × 192 points.
  - `site/hifi/data/samples/entsoe/total_capacity_allocated.json`: 8 rows.
  - `site/hifi/data/notebooks/entsoe/total_capacity_allocated{.json,-5.png}`: 5 cells, no errors.
  - No staged chart spec or authored override existed for either dataset.
- `gridflow-build --only entsoe/total_capacity_allocated`: OK. It wrote `capacity-allocated-nominated.html`, plus pointer pages `total_capacity_allocated.html` and `total_nominated_capacity.html` that redirect to `#<member>`.
- `detect.mjs --json`: only `em-dash-overuse`, advisory (84 hits, all the `--` padding in rendered EIC codes). The page has 0 real em dashes and 0 arrows.
- Screenshots, light, at 1440, 1024, 768 and 390 (390 via a 390 px iframe, captured in offset windows; the drawer was also measured at 390 in the Browser pane):
  - Nothing is clipped or overlapping.
  - The notebook filename tab clips at 390 (`total_capacity_alloca…`). This is the known template item from ruling #39, left alone.
  - The notebook df table scrolls sideways in its own container at 390 (391 px of content in 300 px). The page itself has no horizontal scroll.
  - **The site has no dark theme** (no `prefers-color-scheme` or `data-theme` in `theme.css`, `dataset.css`, `tokens.css` or `site.js`), so the "dark" shots render identically to light.

## Chart

- **Chart:** capacity already allocated into GB, from silver `entsoe/total_capacity_allocated` only.
  - Filter: `in_area_code` = GB.
  - Series: `out_area_code` NL (petrol) and BE (horizon), MW, hourly rows, `aggregation: last`.
  - Window: 14 to 21 September 2026 UTC.
- **Why not "allocated against nominated for one border":** the chart builder reads one silver table, and `group` is one column (`distil.py:186-201`). Six allocated ordered pairs collide on both `in_area_code` and `out_area_code`, so the chart is GB only. The trader comparison (allocated against nominated, Belgium into GB, same window) is in the notebook as a step plot.
- **Window choice:** 14 to 21 September is gapless for both GB pairs (192/192 hours each). It shows both GB steps:
  - NL: 0, then 850 MW at 22:00 on 19 September, then 900 MW at 22:00 on 20 September.
  - BE: 725 MW, then 0 at 22:00 on 20 September.
- The NL line sits on the x axis from 14 to 19 September; its key note says so.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Allocated definition (`what_it_is`, `summary`, family `differs`) | Reg. 543/2013 Art. 12(1)(c), as adopted (legislation.gov.uk/eur/2013/543/article/12/adopted): "prior to each capacity allocation the total capacity already allocated through previous allocation procedures per market time unit and per direction". Now quoted in the allocated note body. |
| Nominated definition | Art. 12(1)(b): "for every market time unit and per direction between bidding zones the total capacity nominated". Art. 12(2)(b): published "no later than one hour after each round of nomination". Now quoted in the nominated note body. |
| gridflow asks for contract type `A01` (daily) | `endpoints.py:263-274` (`extra_params` `businessType=A29`, `auction.Category=A01`, `contract_MarketAgreement.Type=A01`). Comment "A01=daily products" at `endpoints.py:324`. The bronze `meta.json` `request_url` confirms it. |
| Nominated request | `endpoints.py:256-262`: `businessType=B08` only. Bronze `request_url` for GB/BE on 2026-09-20. |
| `raw_feed.requests` and parameter order | Bronze `raw_20260926T180334Z_aea3bdbf.meta.json` `request_url`: `documentType, periodStart, periodEnd, in_Domain, out_Domain, businessType, auction.Category, contract_MarketAgreement.Type, securityToken`. |
| "One GET per ordered pair per UTC day, eight pairs" | `client.py:38-48` (`_FLOW_PAIRS`, one direction each). `client.py:211-229` (one task per pair). `day_subwindows` (`utils/time.py:123`) splits the window per UTC day. |
| Commands, ingest end excluded | `day_subwindows`: `end` is exclusive, and an end at midnight excludes that date. Transform `--end` is inclusive, as on the sister pages. There are no `PARTITION_SOURCE_OFFSETS` in `h6_market.py`. `EVENT_WINDOW_FILTER = True` (`h6_market.py:228`) keeps only the request's UTC day, so silver day D reads bronze day D. |
| Grain and key | Dedup `unique(subset=[timestamp_utc, in_area_code, out_area_code, business_type], keep="last")` at `h6_market.py:91-99`. |
| `timestamp_utc` = period start + (position − 1) × resolution | `parsers.py:530` and `582` (ruling #39). |
| An A03 point repeats until the next one (`quantity_mw` field) | `parsers.py:533-600`: an A03 curve is forward-filled to the Period end. |
| Allocated replies: one point per 22:00 to 22:00 UTC Period | Bronze GB/NL 2026-09-20: two Periods (`2026-09-19T22:00Z` to `2026-09-20T22:00Z`, and `2026-09-20T22:00Z` to `2026-09-21T22:00Z`), each with one Point at position 1 (850, then 900). The facts cadence line says only "one value per day-long Period"; the 22:00 boundary is stated only for the September window (caption, x label, alt). |
| Nominated `PT60M` on GB pairs, `PT15M` on FR/DE-LU | Silver `resolution` per pair: GB/FR, GB/NL and GB/BE `PT60M`; FR/DE-LU `PT15M`. |
| `published_at` is a fetch-time stamp | `h6_market.py:105,114`, ruling #39. Silver: `published_at` 18:02 to 18:04 UTC on 2026-09-26, the same minutes as the bronze file names `raw_20260926T1802..`. |
| `in_area_code` GB means into GB (project check) | Nominated silver (= contract `A07`) against `cross_border_flows` hourly mean, same ordered pair: r = 0.93 (GB/FR), 0.93 (GB/NL), 0.88 (GB/BE). This agrees with the `cross_border_flows` and `net_transfer_capacity` pages. |
| Chart alt values | Committed series: netherlands is 0 from 14 Sep 00:00, 850 from 19 Sep 22:00, 900 from 20 Sep 22:00 to 21 Sep 23:00; belgium is 725 from 14 Sep 00:00, 0 from 20 Sep 22:00. |
| Key note "replies echo auction category `A04`, not `A01`" | Bronze: every GB/NL allocated reply has `<auction.category>A04</auction.category>`. The other five pairs echo `A01`. |
| Sample rows | `gridflow-sample` output: GB/BE and GB/NL at 21:00 and 22:00 UTC on 19 and 20 September. The steps are visible (NL 0 to 850, 850 to 900; BE 725 to 0). |
| `plot_alt` | Silver GB/BE, 14 to 21 September: allocated is 725, then 0 from 20 Sep 22:00. Nominated maximum is 1,055 at 14 Sep 10:00; it is above 725 on 7 of 8 days; it is 0 from 21 Sep 04:00 to 23:00. |
| Notebook lead: relation, date column, inclusive ends, lineage dropped | `gridflow_models/research/handles/source.py:401-451`: `_relation_name_for_dataset`, `_date_range_predicate` inclusive, `_present_bitemporal_exclude_clause`. `schema_manifest.py:188-189` gives `timestamp_utc` for both tables. The runner executed both queries without error. |
| "Nominations follow later rounds too, so they can exceed allocated" | The definitions: allocated counts only "previous allocation procedures". The nominated replies carry contract series `A01`, `A06` and `A07` (see defects). |
| Related | All four pages are in `site/hifi/data/entsoe.json`. `auction_revenue` is explicit allocations (`endpoints.py:230-238`, `B07`). The allocated replies carry `auction.type` `A02` (Explicit per `.planning/audit/2026-05-31-vendor-truth-audit/vendor-docs/entsoe-codes.md` §4). |

## Body corrections (smallest spans)

**`total_capacity_allocated.md`**

1. Query parameters table: `in_Domain` "Source EIC" became "Receiving zone EIC (project check …)", and `out_Domain` "Destination EIC" became "Sending zone EIC". Evidence: the project check above.
2. Bronze sample: "`<auction.Category>A01</auction.Category>` echoing the request" was wrong for GB/NL. Replaced with the real GB/NL reply structure: `auction.type` A02, `auction.category` A04, two 22:00 UTC Periods of one point each. Cites the file name, `parsers.py:582-600` and `h6_market.py:228`.
3. Silver sample: the GB→FR 1500 MW row matched no reply (the note's own probe found GB→FR empty). Replaced with a real GB/NL row, including `published_at`. The schema line now names `published_at` (`h6_market.py:105,114`).
4. Known issues: "many GB borders post-Brexit publish no allocation entries because…" is contradicted: GB/NL and GB/BE return Publication documents; GB/FR and GB/IE-SEM return Acknowledgements. Also added the Art. 12(1)(c) definition and the 12(2) timing.

**`total_nominated_capacity.md`**

1. Publication lag "D-1" became Art. 12(2): no later than one hour after each round of nomination.
2. Query parameters table: same direction fix as the allocated note, with the correlation evidence.
3. Silver schema: added `published_at`, and a note that there is no contract-type column.
4. Known issues:
   - "`contract_MarketAgreement.type` is `A01` by default" was wrong. GB replies carry three series, `A01`, `A06` and `A07`; FR/DE-LU carries `A07` only, at `PT15M`.
   - Added the silver dedup defect bullet.
   - "silver preserves the as-published positions" was wrong: the parser forward-fills A03 (`parsers.py:533-600`).
   - Added the Art. 12(1)(b) definition.
5. Implementation delta: "3 TimeSeries (one per nominated MarketAgreement / direction split)" became one per contract type, same direction.
6. Modelling notes: "> 100% would indicate over-nomination (rare and a data flag)" was wrong for this tuple. Allocated counts only earlier procedures, and silver's GB/BE nominated series exceeds 725 MW in many September hours.

## gridflow and data defects

1. **Nominated silver keeps one of three contract series (gridflow defect, major for the data).**
   - GB/FR, GB/NL and GB/BE replies each carry three TimeSeries, contract types `A01`, `A06` and `A07`, in that order.
   - `parse_timeseries_xml` reads `contract_MarketAgreement.type` into no returned field. The H6 dedup key `(timestamp_utc, in_area_code, out_area_code, business_type)` with `keep="last"` (`h6_market.py:91-99`) drops `A01` and `A06`.
   - Silver equals the `A07` series in all 336 hours on each GB pair. It also equals `commercial_schedules` exactly on those pairs (100% of 312 matched hours).
   - Fix: carry the contract type as a column and add it to the key (T2, silver shape change).
2. **Allocated `auction.Category` filter.** The GB/NL replies echo `auction.category` `A04` although the request sends `auction.Category=A01`. Either the lowercase-`a` parameter is ignored for this border, or the platform maps it. Not verified live. The silver rows carry no auction category.
3. **Silver has no contract or auction columns on either table**, so a reader cannot tell which product a row belongs to. This follows from defect 1.
4. **Data observation, not on the page:**
   - Some allocated days are partial in silver, because one CET Period was absent from the replies: FR/DE-LU and NL/BE on 15 and 16 September, GB/BE on 2 and 3 August and on 13 September.
   - Silver covers 1 to 5 August and 13 to 21 September.
   - The page never states either.

## Not verified

- **Contract codes.** The meanings Daily, Long term and Intraday for `A01`, `A06` and `A07` come from entsoe-py's `MARKETAGREEMENTTYPE` map, not an ENTSO-E code list. The page prints only the code `A07`; the note body labels the meanings with their source.
- **Why allocated capacity is zero** on GB/NL from 13 to 19 September and on GB/BE from 20 September. The page states values only, no cause.
- **Continental direction.** "Into GB" is a project check on GB pairs only. For continental pairs the page draws nothing and claims nothing.
- **What a 22:00 to 22:00 UTC allocated Period means.** It looks like a CET delivery day, but the page does not call it one; it says "day-long Period" in the facts. In winter it would presumably start at 23:00 UTC; not checked.
- **"Headroom: `net_transfer_capacity` minus capacity already allocated"** (how_used) comes from the note's modelling notes. It is a use, not a fact claim, but it is not vendor-documented.

## Open questions for the seat

1. Nominated silver's contract-type loss (defect 1): hold the page, or ship it with the family `differs` line saying "silver keeps only the last contract series, `A07`"? I shipped the wording and did not hold.
2. The page has no dark theme to check (see Status). Confirm that "light and dark" in the rubric reduces to light for this site.

## Template or runner problems (not worked around, except item 1)

1. **`scripts/run_notebooks.py` df parser and named indexes.** A DataFrame with a named index gives a two-row pandas header. The parser flattens it into `["", "", "allocated", "nominated", "timestamp_utc", "", ""]`, which renders a header that doesn't line up with the body. I avoided it with `.reset_index()`. Other pages that print a named-index frame will show the same fault.
2. **390 px iframe captures in headless Chrome go blank below about 2,860 px.** I captured in offset windows (negative `margin-top`). Useful for other writers.
3. The notebook tab filename clips at 390 (known, ruling #39).
