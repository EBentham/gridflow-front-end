# entsoe/auction_revenue: author report

Writer: Opus 5.5 · high, one agent, two advisor calls. Worktrees as in `BATCH-entsoe.md`; screenshot port 9814.

## Status

- The canonical note now carries a `page:` block, plus body corrections: `vault-p26-entsoe/30-vendors/entsoe/datasets/auction_revenue.md`.
  - It keeps CRLF line endings.
  - The mirror `vault/entsoe/auction_revenue.md` is a byte-for-byte copy (`cmp` clean).
- There was no staged chart spec or authored override to retire.
- **Artefacts:**
  - `site/hifi/data/series/entsoe/auction_revenue.json`: `spec_origin: vault`. It has 2 series × 168 hourly points, `duplicates_dropped: 336` and `rows_used: 336`.
  - `site/hifi/data/samples/entsoe/auction_revenue.json`: 8 rows × 13 columns.
  - `site/hifi/data/notebooks/entsoe/auction_revenue.json` and `auction_revenue-5.png`: 5 cells, no errors, one image.
- **Build:** `gridflow-build --only entsoe/auction_revenue` succeeds.
- **Detector:** one finding, `em-dash-overuse` (advisory; "174 em-dashes", all `--` padding in EIC codes). It is accepted under ruling #39. The page has 0 `—`, 0 `→` and 0 `·`.
- **Seat notes applied:**
  - Point time is written as "period start plus (position minus 1) times resolution".
  - Cadence is written as "hourly (`PT60M`) points in the responses gridflow holds".

## What silver holds (the three questions in the ask)

- **Which figures:** auction revenue only, not congestion income.
  - Every row has `business_type` B07, and the connector pins `businessType=B07` (`endpoints.py:233-242`).
  - Congestion income is the separate dataset `congestion_income` (B10). It has no page, and its silver is empty.
- **Which borders:** GB with NL (`10YNL----------L`) and GB with BE (`10YBE----------2`), both with `in_area_code` GB.
  - The connector requests eight ordered pairs (`client.py:40-49`).
  - In all 224 bronze files (Aug 1-5 and Sep 13-21), the other six pairs return `Acknowledgement_MarketDocument` with Reason 999 ("No matching data found for Data item AUCTION_REVENUE [12.1.A]").
- **Grain and currency:**
  - One row per hour, `in_Domain` and `out_Domain`, from `PT60M` points.
  - `curveType` A03, `auction.type` A02 (explicit) and `contract_MarketAgreement.type` A01 (daily).
  - Currency: `currency_Unit.name` EUR in all 28 populated documents. The parser reads the currency (`parsers.py:312-313`), but the transformer's `output_cols` drop it (`h6_market.py:107-117`). `amount_eur` is only a column name.
- **Summing:** there are no overlapping horizons inside this table, because the request pins `contract_MarketAgreement.Type=A01`. But **each delivery hour sits in two silver partitions**, because one UTC-day request returns both CET delivery days it touches.
  - Silver has 1,296 rows but 744 unique keys, and every duplicate pair agrees on `amount_eur`.
  - The chart spec, the sample `select` and the notebook all dedup on `(timestamp_utc, in_area_code, out_area_code)` before anything is read or summed.
  - The page's what_it_is says the hours of one delivery day can be summed (they are the daily product), and the notebook lead says to drop duplicates first.

## Chart

- **Type:** a line, EUR per hour as sent (`aggregation: last` after dedup, so nothing is summed).
- **Borders:** GB-NL (petrol) and GB-BE (horizon).
- **Window:** delivery days 15 to 21 September 2026, that is `timestamp_utc` from 2026-09-14T22:00Z (inclusive) to 2026-09-21T22:00Z (exclusive).
  - This window is gapless for both borders.
  - BE is active early in the week (81,198 EUR at 11:00 UTC on the 15th), and NL returns from five all-zero days to 115,434 EUR at 11:00 UTC on the 21st.
- **August was rejected:** GB-BE has no document for delivery day 4 August, which would need a local-gap explanation.
- **NL zero days:** delivery days 13 to 19 September each carry one declared `price.amount` 0 at position 1, repeated by the A03 rule. I checked the bronze files for 2026/09/13 to 19; the key note says so.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Document type A25, business type B07 (`facts.vendor`) | `endpoints.py:233-242`; bronze `<type>A25</type>`, `<businessType>B07</businessType>` |
| Daily explicit auction: A01 pinned, series carry `auction.type` A02 (`what_it_is`) | `endpoints.py:239-240` `extra_params`; all 28 populated bronze docs: `auction.type` A02, `contract_MarketAgreement.type` A01 |
| Article 12.1.A (`what_it_is`) | Vendor text in each Reason 999 acknowledgement: "AUCTION_REVENUE [12.1.A]" |
| EUR as sent in `currency_Unit.name`; silver drops it | 28/28 docs `currency_Unit.name` EUR; `parsers.py:312-313`; `h6_market.py:107-117` (no currency column) |
| Hourly `PT60M` points (`facts.cadence`) | 54/54 `<resolution>PT60M</resolution>` in bronze; silver `resolution` has one value, `PT60M` |
| Grain: one row per hour and zone pair; key adds `business_type` (`facts.grain`, `record.key`) | Transformer dedup subset `h6_market.py:91-99` |
| Point time = period start + (position − 1) × resolution (`record.fields.timestamp_utc`) | `parsers.py:530`, `:582` |
| A03 point repeats until the next declared one (`record.fields.amount_eur`, key note) | `parsers.py:533-600` forward-fill; bronze NL 09/13-19: one point, value 0, per Period |
| `amount_eur` from `price.amount` | `h6_market.py:130` `value_tag = "price.amount"` |
| `published_at` is a fetch-time `createdDateTime` | Ruling #39; `h6_market.py:105`; bronze `createdDateTime` 2026-08-16T13:59:15Z vs meta `fetched_at` 13:59:15.30 |
| Two of eight pairs return a series (`raw_feed.note`, `summary`) | `client.py:40-49`; bronze meta `request_url` tally (14 of each pair); Reason 999 on the six others |
| A reply can span two delivery days (`raw_feed.note`) | Request `periodStart=202608010000&periodEnd=202608020000` returns `period.timeInterval` 2026-07-31T22:00Z to 2026-08-02T22:00Z (`2026/08/01/raw_20260816T135915Z_74c44c36.xml`); 2 of 28 docs had one Period |
| Request URL: parameter order and values | Bronze `.meta.json` `request_url` (`documentType, periodStart, periodEnd, in_Domain, out_Domain, businessType, contract_MarketAgreement.Type, securityToken`); `client.py:283-306` |
| Ingest `--end` exclusive; bronze 14-20 covers delivery days 14-21 | `utils/time.py:123-142` `day_subwindows`; UTC day D returns delivery days D and D+1 |
| Transform day D reads bronze day D only | `silver/base.py:417` `PARTITION_SOURCE_OFFSETS = (0,)`, not overridden in `h6_market.py` |
| Most hours in two silver files; one copy kept (`chart_view.caption`; scoped "most" because under the page's commands delivery day 21 lands in file 20 only) | Silver: 1,296 rows, 744 keys, 0 value conflicts; series `provenance.duplicates_dropped: 336`; `_event_window.py:210` EXEMPT (no trim) |
| `query()` relation, date column, both ends, lineage dropped, and duplicates returned (`notebook.lead`) | Explore trace: `storage/duckdb.py:180` plain glob view; `schema_manifest.py:151` `timestamp_utc`; `_get_method_registry.py:94-96` `< end + 1 day`; `schema_manifest.py:77-85` lineage; `source.py:449` `ORDER BY timestamp_utc` |
| Chart numbers (alt, key notes) | Committed series: NL max 115,433.72 at 2026-09-21T11:00Z, zero until 2026-09-19T22:00Z, 14,711.94 max on delivery day 20; BE 81,197.76 (15th 11:00), 78,442.32 (16th 11:00), 13,209.6 (18th 11:00), other days max 4,367.85 |
| Notebook plot numbers (`plot_alt`) | Delivery-day sums from the series: BE 247,326 / 381,571 / 654 / 50,966 / 6,171 / 11,218 / 830; NL 0 ×5 / 41,271 / 660,098; the PNG matches |
| Sample rows | `gridflow-sample` output: 21 Sep 08:00-11:00 UTC, both borders; NL 42,566.24 to 115,433.72; BE 0.0 |
| Related pages resolve | The build resolved `entsoe/total_capacity_allocated` (family member), `cross_border_flows`, `day_ahead_prices` and `elexon/mid` with no error |

## Note-body corrections (canonical note; each cites evidence inline)

1. **Bronze granularity:** "One file per (border, day or longer-horizon window)" becomes one file per (ordered pair, UTC request day), and a reply can span two CET delivery days.
2. **Bronze sample:** the speculative "Populated payload would mirror A92…" is replaced with the observed populated payload:
   - GB-NL and GB-BE only; Reason 999 for the six other pairs;
   - A02, A01, EUR, A03, `PT60M`, `price.amount`;
   - 22:00-to-22:00 UTC Periods "in these documents"; a one-UTC-day request "can return" both delivery days it touches (2 of the 28 documents had one Period).
   - The cited file is `2026/09/20/raw_20260926T175330Z_005f5299.xml`.
3. **Silver schema, `amount_eur`:** the source is `Point.price.amount`, not `Point.quantity` (`h6_market.py:130`). The currency is dropped (`:107`).
4. **Silver schema:** added the missing `published_at` row (`createdDateTime`, a fetch-time stamp; `h6_market.py:105`).
5. **Silver sample:** the placeholder (GB-FR, `P1D`, 45000.0) is replaced with a real row (GB-NL, 2026-09-21T11:00Z, 115433.72, `PT60M`, `published_at`).
6. **Known issues:** added a bullet on cross-partition duplicates, citing `_event_window.py:210` and `h6_market.py:98`, with the 1,296 rows / 744 keys measurement.
7. **Modelling notes:** "implied £/MW" becomes "EUR/MW" (the currency is EUR).

Left alone, and not used on the page:
- "Historical depth 2014-12-05 onward" (no vendor evidence in the note).
- "Publication is sparse… weekly or monthly" (not evidenced; GB-NL and GB-BE publish daily documents with hourly points).
- The parameter table's "Source EIC" / "Destination EIC" labels (see open question 1).

## Not verified

- **Direction.** Whether an amount covers the `out_Domain` to `in_Domain` direction, the reverse, or the whole border is not stated in the response, the code or the note.
  - gridflow never requests the reverse orientation, so the page says only "the ordered pair as sent" and "which direction an amount covers is not stated".
  - A project check was inconclusive. Revenue divided by `total_capacity_allocated` MW, set against the GB (Elexon `mid` APXMIDP, ×1.16) minus NL/BE day-ahead spread: among hours with implied price above 5 EUR/MW, GB was dearer in only 100 of 195 (NL) and 52 of 71 (BE).
- **A03 semantics for amounts.** The code repeats a block's value on every omitted hour, so a block is read as per-hour amounts, not a block total. ENTSO-E's A03 definition supports a per-position value, but I did not read the vendor guide.
  - The notebook's daily sums rely on this, and so does the page's `what_it_is` sentence that the hours of one delivery day can be summed.
  - The all-zero NL days are unaffected.
- **"Explicit capacity auctions … Article 12.1.A"** rests on the acknowledgement text and the note's overview, not on the ENTSO-E guide itself.

## Open questions (for the seat)

1. **Direction of B07 amounts.** Should gridflow also request the reverse orientation (`in_Domain` NL/BE, `out_Domain` GB) to settle it? That would be a gridflow change (`client.py:40-49` `_FLOW_PAIRS` is shared by every zone-pair dataset).
2. **Silver defect (gridflow seat item).** `AuctionRevenueTransformer` is EXEMPT from the event-window trim on an inferred P1M basis (`_event_window.py:210-215` and `:816-844`, "No populated live payload was obtained for B07"). The populated bronze shows daily documents with `PT60M` points and two-delivery-day Periods.
   - The result is that every delivery hour is written to two partitions, and the `silver_entsoe_auction_revenue` view (a plain glob) returns both.
   - The classification evidence is stale. The dataset probably wants `EVENT_WINDOW_FILTER = True` or a cross-partition dedup.
   - `congestion_income` shares the same inference.
3. **Currency column.** The transformer drops `currency_unit`, so a non-EUR document would land silently in `amount_eur`. All 28 documents held say EUR.
4. **`total_capacity_allocated` does not line up hour for hour with revenue.** 67 hours have capacity above 0 and revenue 0, and 6 have revenue above 0 and capacity 0. The page's how_used says only "set against … for an implied price". The related note says "MW allocated on the same ordered pairs", which is true.

## Template problems (report only; nothing worked around)

1. **Detector:** `em-dash-overuse` counts the `--` padding in EIC codes (174 hits). Advisory; accepted by ruling #39.
2. **At 390 px** the long `&contract_MarketAgreement.Type=A01` parameter wraps onto an indented continuation with a small gap above it. It is readable, not clipped (the same behaviour as `cross_border_flows`).
3. **Notebook images use `loading="lazy"`,** so a headless full-page capture shows `[5]` blank until the image is scrolled to.
   - Forced eager, it loads: 724 px natural width, 300 px wide at 390 with its right edge at 363 of 390; 724 px at 1440.
   - Not a page defect, but checkers should force `loading='eager'` before judging.
4. **No dark theme.** The "dark" captures at 1440 and 390 are byte-identical to the light ones (`cmp`).
5. **The notebook shows the matplotlib `<Axes …>` repr as a text output before the plot.** This is cosmetic and the same on other pages.
6. **Frame fold.** `select.columns` puts `amount_eur`, `resolution` and `published_at` before `business_type`, so at 768 the frame folds after `amount_eur` and the value column stays in view.
   - The first draft had `business_type` fourth, which hid `amount_eur` at 768. Fixed after the advisor's check.
   - The `…` header is a checkbox (`#fx`, "Show the folded columns"). Unfolded, the frame scrolls inside its own box: 2,272 px in 683 at 768, and 2,304 px in 390 at 390, with no page overflow.
   - Files: `fold-768.png`, `unfold-768.png`, `unfold-390.png`.

## Screenshots

- **Method:** CDP headless Chrome on port 9814 (`scratchpad/ar_shot.mjs`, each call under `timeout 60`), from `file://`. There are no `fetch` calls in the site JS.
- **Files:** `scratchpad/ar-shots/`:
  - `p-{1440,1024,768,390}.png`;
  - `p-{1440,390}-dark.png`;
  - `c{0,1400,2800,4200}-390.png` (390 bands);
  - `nb-{1440,390}.png` and `nbimg-{390,1440}.png` (notebook open);
  - `r2-{1440,1024,768,390}.png` (after the column reorder), `fold-768.png`, `unfold-{768,390}.png`.
- **Checks:**
  - `scrollWidth` equals `innerWidth` at every width.
  - No element outside the SVG scenery extends past the viewport.
  - Fully visible at every width: the turbine tops, the chart axes and key, the section-corner labels, the frame and guide, the notebook drawer and the related list.
- Chrome profiles are left under `%TEMP%\cdp-ar-*`.

## Spend

About 260k tokens (the context counter ran from 15.00M to about 14.74M), Opus 5.5 · high, one agent, one Explore (haiku) sub-search, two advisor calls.
