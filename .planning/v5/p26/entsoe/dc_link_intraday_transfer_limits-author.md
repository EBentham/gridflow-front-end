# dc_link_intraday_transfer_limits: author report (writer, 2026-09-29)

**Status: page built. Recommendation: ship, do not hold.**
- `gridflow-build --only entsoe/dc_link_intraday_transfer_limits` is OK.
- `detect.mjs` returns only the accepted `em-dash-overuse` advisory. Its 174 hits are EIC `-` padding; the rendered text has no `—`, `→` or `·`.
- The mirror is byte-identical to the canonical note (CRLF, `cmp` clean).

**Chart:** a line of one series, GB/NL, 1 August 2026, hourly, 00:00 to 21:00 UTC (22 points).

## Why the data is thin: vendor sparsity, not a connector fault

Every bronze response was classified with a script: root element, TimeSeries count and Point count.

- **168 requests.** The connector sends 8 ordered zone pairs (`client.py:40-49` `_FLOW_PAIRS`) × 19 UTC days (1 to 5 Aug and 8 to 21 Sep 2026).
- **166 are `Acknowledgement_MarketDocument`.** Each says "No matching data found for Data item CB_CAPACITY_FOR_DC_LINKS_INTRADAY_R3 [11.3] (…)".
- **2 are `Publication_MarketDocument`, both GB/NL:**
  - `2026/08/01/raw_20260816T135213Z_15606c0a.xml`: delivery day 2026-07-31T22:00Z to 08-01T22:00Z, 21 declared points.
  - `2026/08/05/raw_20260816T135246Z_78c79b84.xml`: delivery day 2026-08-05T22:00Z to 08-06T22:00Z, 15 declared points.
- **The request parameters match the documented tuple** (A93, `in_Domain` + `out_Domain`, no processType), and two real populated replies prove the request works. Unlike nonbm, this is not a wrong-parameter gap.
- **Why 24 rows:**
  - The 1 August document yields 22 rows, 00:00 to 21:00Z. The HALF_OPEN event-window filter (`h6_market.py:141` opts in; `base.py:1915-1953`) drops positions 1 and 2, which fall on 31 July.
  - The next delivery day, from 22:00Z on 1 August, was answered with an acknowledgement on the 2 August request.
  - The 5 August request returned the **6 August** CET delivery day. Only its first two hours (22:00Z and 23:00Z on 5 August) fall inside that partition's window. Its other 22 hours belong to silver day 2026-08-06, which was never ingested.
- **A03 forward-fill is working.** Silver 1 Aug 00:00 = 600 is position 3, repeating position 2. Positions 15 and 23 are also undeclared and filled (`parsers.py:533-610`).

**Data-op suggestion for the seat (class 2, not mine):** `gridflow ingest entsoe dc_link_intraday_transfer_limits --start 2026-07-31 --end 2026-08-07` plus a transform would complete both populated delivery days. The page does not need it.

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| Document type A93, Article 11.3 (`facts.vendor`) | `endpoints.py:146-150`; the acknowledgement Reason text says `[11.3]`; the note's Overview |
| A93 = "DC link capacity", B06 = "DC link constraint", MAW = "Mega watt", A03 = "Variable sized Block" | ENTSO-E code list v29r0 PDF (eepublicdownloads.azureedge.net mirror), extracted with pypdf 2026-09-29 |
| `business_type` `B06` (what_it_is, fields) | Both populated bronze files; silver `business_type` unique = `B06` |
| Unit MW (`MAW`) | Bronze `quantity_Measure_Unit.name` = `MAW`; code list |
| Cadence "`PT60M` in these rows" | Silver `resolution` unique = `PT60M`; scoped to the rows shown, per the seat's ruling |
| Grain and key include business type | Dedup `unique(subset=[timestamp_utc, in_area_code, out_area_code, business_type])`, `h6_market.py:91-99` |
| No published limit → acknowledgement, Reason 999, "No matching data found" | 166 bronze acknowledgements; the note's live call of 2026-05-08 |
| "Documents here span a CET delivery day" (scoped to the two documents shown); silver keeps the UTC request day | Both documents' `period.timeInterval` run 22:00Z to 22:00Z; `base.py:1921-1940` (the vendor's "measured CET/CEST delivery-day over-span"); HALF_OPEN filter |
| "The GB and NL pair is BritNed" | The approved `cross_border_flows` note's border table (`GB–NL (BritNed)`); NESO's catalogue lists "BritNed - NESO's Intraday Trading Limit". **Not verified against ENTSO-E text**: the data-view page returns HTTP 400 |
| Request URL | Bronze sidecar `request_url` for 2026-08-01 GB/NL: parameter order documentType, periodStart, periodEnd, in_Domain, out_Domain, securityToken |
| One GET per pair per UTC day, eight ordered pairs; acknowledgements stored in bronze | `client.py:131-167` (day sub-windows), `:211-228` (pairs); the acknowledgement XMLs are in bronze |
| Ingest end excluded, transform end included | Same connector and `day_subwindows` as the approved `cross_border_flows` commands |
| `timestamp_utc` = period start + (position − 1) × resolution | `parsers.py:530` |
| A03 point repeats until the next declared one | `parsers.py:533-610`; silver 00:00 = 600 (position 3 undeclared) |
| `published_at` is a fetch-time stamp | `h6_market.py:105` `with_published_at`; `createdDateTime` 13:52:13 vs `fetched_at` 13:52:12.33, and 13:52:46 vs 13:52:46.38 |
| Chart values in alt and caption (600, 450, 1,021, 1,032 to 1,038, 980, 620, 300, 650, 600) | Committed series `values`, 22 points, `rows_used` 22 |
| Line ends at 21:00; document from 22:00 UTC on 31 July | Series `x` last = 21:00Z; bronze period start |
| Eight rows 14:00 to 21:00, 300 MW low at 17:00 | `gridflow-sample` output |
| Notebook lead (inclusive ends, lineage dropped, time-ordered only) | gridflow_models `research/handles/source.py:401-446`; `schema_manifest.py:163` date column `timestamp_utc` |
| Related: NTC, flows and schedules request the same eight pairs | `endpoints.py` zone_pair entries all go through `_FLOW_PAIRS` |
| Related: Elexon `INTNED` as the Netherlands interconnector flow | The fuelhh note maps INTNED to imports; the page names BritNed once only, in `what_it_is` (unverified against ENTSO-E) |

## Page choices

- **One day, one series.** Including the two 5 August rows would draw a four-day gap with two points after it, which reads like a trend. The chart, commands, notebook and sample all stay on 1 August, so `needs` matches the commands.
- **Eight rows, 14:00 to 21:00.** These show the 300 MW low, and at 20:00 an A03 repeat (650, position 23 undeclared).
- **Direction is not stated.** `in_area_code` says "the limit's direction is not verified". A project check is suggestive but not conclusive:
  - on the 24 silver hours, Elexon `INTNED` (positive taken as import) never exceeds the A93 value;
  - GB exports on 5 August 22:00 to 23:00 (−1,036 and −1,004 MW) exceed the limit (670 and 880);
  - but on 6 August (bronze only), import runs up to 13 MW above it.

  So "limit on NL to GB" fits, but I did not put it on the page.
- **Notebook plot** uses `drawstyle="steps-post"`, because A03 values are blocks. The site chart uses the standard line; the key note says "Hourly blocks as sent".

## Note body corrections (canonical note)

1. **Bronze path pattern.** `raw_<uuid>.xml` → `raw_<YYYYMMDDTHHMMSSZ fetch time>_<sha256[:8]>.xml` plus the `.meta.json` sidecar (`bronze/writer.py:33-34,57`).
2. **Bronze sample.** "A populated response would mirror A61 structure with `<businessType>A28</businessType>`" was wrong. It is replaced by the real GB/NL document: B06, MAW, A03, PT60M, the CET delivery-day period, and an excerpt showing undeclared position 3.
3. **Silver schema, `business_type`.** "Usually `A28`" → `B06` ("DC link constraint") in the populated responses.
4. **Silver schema.** Added the missing `published_at` row (`h6_market.py:105`, fetch-time stamp).
5. **Silver sample.** It was fabricated (GB→FR, A28, 1850 MW on 2026-05-06). It is replaced with the real 2026-08-01 17:00Z row (300 MW, B06).
6. **Known issues.** Added a "Delivery-day over-span is trimmed" bullet, citing `h6_market.py:141` and `base.py:1915-1953`, with the 5 August example.

## Could not verify

- The ENTSO-E data-view page and API guide (both HTTP 400) and the docstore host (DNS failure). Only the code-list PDF was readable.
- The link name BritNed against ENTSO-E text.
- The limit's direction (see above).
- Note Overview claims, left in place and not used on the page:
  - "Limits are typically updated within the trading day as DC link operators reassess capability…";
  - "Historical depth 2014-12-05 onward (intraday updates only published when capability changes)";
  - the gotcha "Article 11.3 only requires a publication when a DC link operator revises a previously published intraday limit".

  The two real documents are full-day hourly curves with `revisionNumber` 1, not isolated revisions, so the "only on revision" claim looks doubtful.
- Whether the reverse pairs (`in_Domain` NL, `out_Domain` GB) would return data. gridflow never requests them.

## Open questions and gridflow defects (for the seat)

1. **Stale code evidence.** `_event_window.py:557-575` classifies A93 FILTER_SAFE on "never observed populated … EMPTY probe only". Two populated own payloads now exist (bronze 2026-08-16), and they confirm the trim works as intended on real data. The evidence and limitation text should be updated (gridflow unit).
2. **Pair list is a poor fit for A93.**
   - Four of the eight pairs are AC borders (FR-BE, FR-DE-LU, NL-DE-LU, NL-BE), which cannot carry a DC-link limit.
   - Only one direction per border is requested.
   - GB's other DC links, to NO2 (NSL) and DK1 (Viking), and continental DC links (NorNed, COBRA, ALEGrO) are absent.

   This needs a research unit with named unknowns, not a blocker.
3. **Data gap.** Silver day 2026-08-06 (and 07-31) was never ingested (see the data-op suggestion above).

## Template problems

- **Inline code in `notebook.lead` does not wrap.** `silver_entsoe_dc_link_intraday_transfer_limits` (47 characters) pushed the 390 layout to 405 px. I reworded the lead to "the silver relation for `dc_link_intraday_transfer_limits`" rather than touch CSS; `overflow-wrap: anywhere` on prose `code` would fix it for good.
- **The notebook tab clips the `.ipynb` name at 390.** This is the known seat item; left as is.

## Screenshots

- CDP headless Chrome on port 9816 (`scratchpad/dc_shot.mjs`, every call under `timeout 60`), file URL, at 1440, 1024, 768 and 390. The frame was unfolded and the notebook opened at 1440 and 390.
- Files: `scratchpad/dc-shots/`.
- `scrollWidth == innerWidth` at every width after the lead fix, and no `code` or `pre` runs past the viewport.
- Hero scenery, chart, key, raw feed, frame and guide, notebook plot (lazy image checked after scrolling into view) and related are all fully visible.
- There is no dark theme, so there is a single light pass.
- The Chrome profile folders (`%TEMP%\cdp-dc-*`) are left in place.

## Files touched

- Canonical note: `vault-p26-entsoe/30-vendors/entsoe/datasets/dc_link_intraday_transfer_limits.md`.
- Mirror: `p26-entsoe/vault/entsoe/dc_link_intraday_transfer_limits.md`.
- Artefacts under `p26-entsoe/site/hifi/data/`:
  - `series/entsoe/dc_link_intraday_transfer_limits.json`;
  - `samples/entsoe/dc_link_intraday_transfer_limits.json`;
  - `notebooks/entsoe/dc_link_intraday_transfer_limits.json` and `-5.png`.
- Built page: `p26-entsoe/site/hifi/data-sources/entsoe/dc_link_intraday_transfer_limits.html`.
- No staged spec or authored override existed.
