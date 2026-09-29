# dc_link_intraday_transfer_limits: checker review (2026-09-29)

**Verdict: REVISE.** One major and three nits. Do not hold the page.

**Why not a hold.** The chart shows 22 real hourly points from one real vendor document (`2026/08/01/raw_20260816T135213Z_15606c0a.xml`).
- It is labelled as one day in the title, caption, alt and `needs`, and it implies no trend.
- It teaches three mechanisms a practitioner needs for this document type, and each one is verified below: the Reason 999 acknowledgement, the delivery-day trim and the A03 forward-fill.

A thin but honest page is better than a blank one here. The writer's suggested data op (ingest 31 Jul to 6 Aug) is for the seat and does not change this verdict.

## Findings

1. **major: `page.summary`.** The sentence "ENTSO-E's intraday transfer limits on DC interconnector borders in MW, one direction per series, for the eight zone pairs gridflow requests" reads as if all eight requested pairs are DC borders.
   - **Why it is wrong.** Four of them are AC borders that cannot carry an A93 limit: `FR-BE`, `FR-DE-LU`, `NL-DE-LU` and `NL-BE` (`gridflow/connectors/entsoe/client.py:40-49`, `_FLOW_PAIRS`). Only the four GB borders (FR, NL, BE, IE-SEM) are DC links.
   - **Why major.** It is the first sentence on the page and overstates the dataset's scope, the same overclaim class the pilot rated major.
   - **Fix.** Scope it, for example: "...in MW, one series per ordered zone pair. gridflow requests eight pairs, and its four GB borders are the DC links."
   - **Other fields are fine.** `raw_feed.note` ("for eight ordered pairs") and the `related` notes make no DC claim.

2. **nit: `page.what_it_is` and `page.chart_view.caption`.** Both say "CET delivery day", and the caption says "the CET delivery day from 22:00 UTC on 31 July".
   - Midnight CET is 23:00 UTC. 22:00 UTC is midnight CEST (summer time). Both documents run 22:00Z to 22:00Z (bronze `period.timeInterval`).
   - The writer's own body edit says "CET/CEST delivery day (22:00Z to 22:00Z in summer)", as does `base.py:1921-1940`.
   - Fix: use "CEST" or "CET/CEST" in both fields.

3. **nit: `page.related[3].note` (elexon/fuelhh).** "Elexon's half-hourly Netherlands interconnector flow, `INTNED`" says what the dataset is, not how it relates (rubric 6).
   - Suggested: "Half-hourly flow on the same link (`INTNED`), to set against this limit". That is 11 words or fewer.

4. **nit: writer's report only (no page change).** "8 ordered zone pairs × 19 UTC days" gives 152, not 168.
   - Bronze partitions 2026-09-13 and 2026-09-14 each hold 16 files, fetched on 2026-09-15 and again on 2026-09-26. That makes 21 requests per pair, and 8 × 21 = 168.
   - The 166 and 2 split is still correct.

## The four focus items

**1. Thin data is vendor sparsity, not a connector bug.** Confirmed.
- **Bronze.** The dataset holds 168 `raw_*.xml` files and 168 sidecars.
  - 166 have root `Acknowledgement_MarketDocument`, all `<code>999</code>`, all "No matching data found for Data item CB_CAPACITY_FOR_DC_LINKS_INTRADAY_R3 [11.3]".
  - 2 are `Publication_MarketDocument`, both `in_Domain` `10YGB----------A` and `out_Domain` `10YNL----------L`.
- **The request tuple.** Every sidecar `request_url` is `documentType=A93&periodStart&periodEnd&in_Domain&out_Domain&securityToken`, with no processType. That matches `endpoints.py:146-150` (`zone_pair`, no extra params).
- **The platform recognises the request.** It names the data item in every acknowledgement, and the identical GB/NL request returns data on two days. This is a well-formed request. The contrast is Elexon `nonbm`, where the request itself was wrong.
- **Why most requests are empty.**
  - Four of the eight pairs are AC borders, so they return nothing by nature (finding 1).
  - Only one direction per border is requested.
  - That is a gridflow coverage gap, which the writer has already routed to the seat. It is not a parse or request defect.
- **Coverage wording.** The page states no local coverage, which is correct under rubric 3.
  - `what_it_is` explains the trim: "silver keeps the hours inside the UTC request day".
  - The caption's "The line ends at 21:00, the last hour of the document" is true.
  - The following hours (22:00 and 23:00 on 1 Aug) belong to the 2 Aug delivery day. Both the 1 Aug and 2 Aug requests overlap it, and neither returned a document for it (the 2 Aug reply is an acknowledgement). So the end is a vendor fact and not a gap in our copy.
  - The unrequested 31 Jul and 6 Aug partitions are not needed for anything the page shows.

**2. Whether the page is worth publishing.** Yes (see the verdict).
- The committed series matches silver exactly: 22 values, `rows_used` 22, and a Polars read of the silver 1 Aug partition gives the same 22 values.
- The chart draws straight segments between the hourly block values. The key note "Hourly blocks as sent" and the notebook's `steps-post` plot cover that, and the renderer is template territory.

**3. Direction and the BritNed name.**
- **Direction.** The page claims no direction.
  - The summary's "one direction per series" only describes the ordered pair.
  - `record.fields.in_area_code` says "the limit's direction is not verified".
  - The chart label is the neutral "GB and NL".
  - Fine.
- **BritNed.** "The GB and NL pair is BritNed" appears once, in `what_it_is`.
  - ENTSO-E's document does not name the link. But BritNed is the only GB and NL interconnector in service, so the identification is a physical fact.
  - The approved `cross_border_flows` note uses the same label (`vault/entsoe/cross_border_flows.md:167`). Acceptable as stated, so no finding.

**4. Point times, cadence and the delivery-day trim.** All correct.
- **Point times.** `timestamp_utc` reads "period start plus (position minus one) resolutions", which matches `parsers.py:530`.
- **Cadence.** Scoped to "`PT60M` in these rows" (silver `resolution` unique `PT60M`).
- **The trim.** HALF_OPEN event-window filter (`h6_market.py:141`; `base.py:1915-1953`).
  - Positions 1 and 2 (22:00Z and 23:00Z on 31 Jul) are dropped from silver day 1 Aug.
  - The 5 Aug request returned the 6 Aug delivery day, and silver 5 Aug keeps only 22:00Z (670) and 23:00Z (880).
- **A03 forward-fill.** Undeclared positions 3, 15 and 23 land on silver 00:00 (600), 12:00 (1032) and 20:00 (650), each repeating the previous point (`parsers.py:575-600`).

## Other checks (no finding)

- **Facts.**
  - The grain and key match the dedup `unique(subset=[timestamp_utc, in_area_code, out_area_code, business_type])` (`h6_market.py:91-99`).
  - `published_at` is `with_published_at` over `createdDateTime` (`h6_market.py:105`): 13:52:13Z against `fetched_at` 13:52:13.85, and 13:52:46Z against 13:52:46.38. "Fetch-time stamp" is right.
  - `B06` = "DC link constraint" and `MAW` = megawatt are accepted on the writer's code-list v29r0 citation. The PDF was not in the scratchpad to re-read.
- **Raw feed.**
  - The request URL matches the 1 Aug GB/NL sidecar parameter for parameter.
  - The ingest `--end 2026-08-02` is exclusive: `day_subwindows` gives a single 1 Aug window (`utils/time.py:123-147`).
  - The transform end is inclusive.
  - `needs: 1 August 2026` matches the commands.
- **Notebook.**
  - The lead matches `query()` (`gridflow_models/research/handles/source.py:401-446`): an inclusive `timestamp_utc` predicate, the bitemporal columns excluded, and `ORDER BY` the date column only.
  - The notebook was written by `scripts/run_notebooks.py`, every cell is read-only and no output has an error.
  - The `.head(8)` output is 00:00 to 07:00 and matches silver.
  - `plot_alt` matches the PNG.
- **Chart provenance.**
  - The series has `spec_origin: vault`, the build's digest check passes, and no staged spec is left under `chart-specs/entsoe/`.
  - The alt values (600, 450 at 03:00, 1,021 at 07:00, 1,032 to 1,038 from 08:00 to 14:00, then 980, 620, the 300 low at 17:00, 650 at 19:00 and 20:00, 600 at 21:00) all match the series.
  - The line is painted `petrol`, with no khaki.
- **Local data and leakage.**
  - The grep hits "live" ×2 and "our " ×2 are substrings of "delivery" and "hour". "8 rows" is the template's frame `aria-label`.
  - There are no em dashes, `→` or `·` in the prose, and no planning labels.
- **Sample.** `generated_by: gridflow-sample`, 8 rows from 14:00 to 21:00. The guide covers every non-pipeline column, key columns first.
- **Build and detector.**
  - `gridflow-build --only entsoe/dc_link_intraday_transfer_limits` is OK.
  - `detect.mjs` returns only the accepted `em-dash-overuse` advisory (174 hits, all EIC padding).
  - The mirror is byte-identical to the canonical note (`cmp`).
- **Screenshots.**
  - Taken with CDP headless Chrome on port 9825 at 1440, 1024, 768 and a true 390 (device-metrics override, `innerWidth` 390).
  - I also took them with the frame unfolded and the notebook open, at 1440 and 390. Files are in `scratchpad/dcrev-shots/`.
  - `scrollWidth` equals `innerWidth` at every width, and no `code` or `pre` runs past the viewport.
  - The hero scenery, chart, key, raw feed, frame and guide, notebook plot and related list are all fully visible.
  - The only clip is the notebook-tab `.ipynb` name at 390, the known seat item.
  - There is no dark theme (`tokens.css` and `theme.css` have no `prefers-color-scheme`).
- **Vault body edits.**
  - Each of the six body corrections cites evidence and fixes a small span.
  - The fabricated A28 and GB-FR sample has been replaced with the real 1 Aug 17:00 row.
  - The curl example is unchanged.
