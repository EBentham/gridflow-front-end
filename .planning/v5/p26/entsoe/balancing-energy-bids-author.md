# balancing-energy-bids (family): author report (writer, 2026-09-29)

Writer: Opus 5.5 · high, one agent, one advisor call. Worktrees as in `BATCH-entsoe.md`; screenshot port 9823 (unused: `file://` captures, no server started).
Family: lead `balancing_energy_bids` (A37/A47/B74), member `aggregated_balancing_energy_bids` (A24/A51).

**Status: HOLD recommended for the whole family page. No `page:` block written, no artefacts made. Both note bodies corrected and mirrored. Page builds blank, detector `[]`.**

- `gridflow-build --only entsoe/balancing_energy_bids`: exit 0, `wrote: data-sources/entsoe/balancing-energy-bids.html (blank)`; member pointers `balancing_energy_bids.html` and `aggregated_balancing_energy_bids.html` rewritten.
- `detect.mjs --json site/hifi/data-sources/entsoe/balancing-energy-bids.html`: `[]`.
- No series, sample or notebook for either member (none existed). No staged chart spec and no authored override to retire.

**Recommended ruling for the seat:** hold the family page blank (like nonbm, netbsad, and the procured_balancing_capacity and current_balancing_state recommendations) until a gridflow fix unit lands and bronze is re-ingested with paging. **Yes.** Also mark `balancing_energy_bids` silver unpublished until then. **Yes.**

The two members fail for different reasons:
- **Lead:** each row is a true bid, but the table is truncated and holed. Any chart, sum or "eight rows of a quarter-hour" would misstate the market.
- **Aggregated member:** faithful to bronze. It only loses its zone, the same document-level area defect as procured_balancing_capacity. But the family page draws its chart, frame and notebook from the lead, so the aggregated member cannot carry the page on its own.

## What a row is

| Member | One silver row is | Direction | Product | Unit | Price |
|---|---|---|---|---|---|
| `balancing_energy_bids` | one Point of one `Bid_TimeSeries`: a bid's offered MW for one quarter-hour, at a connecting area | `flowDirection.direction` `A01`/`A02` (up/down per the note; unverified in-repo) | BE: `standard_MarketProduct` `A05` or `A07`; FR: `original_MarketProduct` `A02` (+ `A05` from the platform document); DE-LU: `A07` | `MAW` (MW), PT15M | `energy_Price.amount`, EUR per `MWH`, **dropped** (silver has no price column) |
| `aggregated_balancing_energy_bids` | one Point of one of two TimeSeries: BE's aggregated offered MW for one quarter-hour and one direction | `A02` (mRID 1), `A01` (mRID 2) | `standard_MarketProduct` `A01`, `businessType` `A14` | `MAW`, PT15M, curve `A03` forward-filled | none sent |

**aFRR or mFRR is not established.** No repo or vault source defines `A05`, `A07`, `A02` (product), `A01` (product, aggregated) or `A14`. The vendor payload undercuts the usual reading: DE-LU's 1,400 `A07` bids all carry `auction.mRID` `AUCTION-mFRR`, as do the `A05` bids in the FR/BE platform documents (acquiring domain `10Y1001C--00085O`). This is a named unknown, and none of it is stated as fact on any page.

## Coverage, explained (report only; local facts)

`balancing_energy_bids`, 81,563 rows:
- Bronze holds two ingest runs: 1 to 5 Aug (fetched 2026-08-16 14:12 to 14:13 UTC) and 13 to 21 Sep (fetched 2026-09-26 18:21 to 18:23 UTC).
- 6 Aug to 12 Sep is simply not ingested. It is not a vendor gap.
- 14 days × (FR 100 + DE-LU 100 + BE 4,629 to 6,796) = 81,563.
- GB, NL and IE-SEM return code 999 on every day.

`aggregated_balancing_energy_bids`, 768 rows:
- Bronze holds 1 to 5 Aug (all six zones code 999) and 22 to 25 Sep (fetched 2026-09-27 00:20 UTC).
- Only BE is populated: 4 days × 2 directions × 96 quarter-hours = 768.

## Does the procured_balancing_capacity bug apply?

- **Lead:** no, the area survives. `connecting_Domain.mRID` sits inside each `Bid_TimeSeries` and is parsed (BE 78,763, FR 1,400, DE-LU 1,400 rows; no blanks).
  - It has the **same class** of bug, though: a dedup key that omits the column telling rows apart (the product).
- **Aggregated:** yes, defect 1 exactly. `area_Domain.mRID` is a child of the document root, and `parsers.py:302` reads it only inside TimeSeries, so `area_code == ""` on all 768 rows.
  - With one zone populated nothing collapses. Silver equals my bronze re-parse row for row.
  - It is latent, though: every document numbers its series `1` and `2`. The day a second zone publishes, the key `(timestamp_utc, "", bid_mrid, direction)` merges zones exactly as it does in procured_balancing_capacity.

## gridflow and data defects

| # | Member | Defect | Evidence |
|---|---|---|---|
| 1 | lead | **Paging never reaches page two.** The loop steps `offset` by 4800 and stops below 4800. Its counter `count_timeseries_or_none` counts only local name `TimeSeries`, and A37 sends `Bid_TimeSeries`, so it counts 0 and stops after `offset=0`. Live pages carry 100 series. | `client.py:63`, `:313-349`, `:483-512`. All 42 populated zone-day requests total exactly 100 `Bid_TimeSeries` across their ZIP entries (94+6, 95+5, 96+4, 93+7, 99+1, 100). |
| 2 | lead | **FR and DE-LU hold only the first quarter-hour.** Page one of FR and DE-LU is 100 bids for 00:00 to 00:15 UTC (`reserveBid_Period` and ZIP entry names `..._202609140000-202609140015.xml`). Silver: exactly 100 rows per day, one `timestamp_utc` (00:00) per day. All 1,400 DE-LU rows are `A02`. | Polars `group_by(area_code, date)`: `ts` = 1 for FR and DE-LU on all 14 days. The gridflow event-window note itself says the DE-LU response "ends far short of the request end" (`_event_window.py:546-548`). |
| 3 | lead | **BE dedup collision drops real bids.** BE numbers series 1 to 81 per document and reuses one mRID for an `A05` and an `A07` series (100 series, 68 to 81 unique mRIDs). The key `(timestamp_utc, area_code, bid_mrid, direction)` omits the product, and `unique(keep="last")` keeps whichever parsed later. | `h8_balancing.py:148`, `:104`. gridflow parser re-parse: 88,146 in-window BE points → 78,763 (9,383 lost, 10.6%). With `standard_market_product` and `original_market_product` in the key: 90,946 → 90,946 (zero collisions). BE on 15 Sep 12:00 UTC: 50 bids, 1,524 MW → 42 rows. My simulation reproduces silver exactly (key, value and product `equals` → True). |
| 4 | lead | **BE loses 22:00 to 24:00 UTC every day.** BE documents run 22:00Z to 22:00Z. The HALF_OPEN filter drops the day-D document's first eight quarter-hours, and no request returns them for D-1. The FILTER_SAFE evidence is a DE-LU probe that starts at the request start. | `h8_balancing.py:152`, `_event_window.py:528-556`. 10,628 parsed points dropped over 14 days. Silver BE runs 00:00 to 21:45 each day (88 quarter-hours). |
| 5 | lead | **Price dropped.** `energy_Price.amount` (EUR/`MWH`) is on every Point. Silver has no price column. This is a known v0.19 carry, restated. | `h8_balancing.py:32`, `:134-147`. |
| 6 | lead | **Other bid attributes dropped:** `acquiring_Domain.mRID`, `auction.mRID`, `status` (`A06`/`A11`), `divisible`. | `h8_balancing.py:134-147`. |
| 7 | aggregated | **Area empty.** It is the procured_balancing_capacity defect 1. | `parsers.py:302`, `:121-145`. Bronze root `<area_Domain.mRID>10YBE----------2</area_Domain.mRID>`. Silver `area_code` `['']`. |
| 8 | aggregated | **Stale classification:** "never observed populated" (UNKNOWN). BE is populated and its documents align to the UTC day. | `_event_window.py:910-936`. |
| 9 | both | **Fixtures unrepresentative.** The A37 fixture is `Balancing_MarketDocument`/`TimeSeries`/`quantity` (the vault already notes this). The A24 fixture puts the area inside TimeSeries with `B74`, where live has it at document level with `A14`. | `tests/fixtures/entsoe/*balancing_energy_bids_gb.xml`; bronze. |

## Evidence table

| Claim | Evidence |
|---|---|
| Lead silver = 81,563 rows; BE 78,763, FR 1,400, DE-LU 1,400; `B74`, `PT15M` on all; directions A01 61,512 / A02 20,051 | Polars `value_counts` on `silver/entsoe/balancing_energy_bids/**` |
| Silver is exactly the gridflow parse + UTC-day window + key dedup | `parse_timeseries_xml(value_tag="quantity")` on all bronze, per-day window, `unique(keep="last")`: 81,563 rows, `equals(silver)` True |
| 100 series per populated request | lxml count of `Bid_TimeSeries` per file, summed per request (`.meta.json` `request_url` + `zip_entry`) |
| FR/DE-LU cover 00:00 to 00:15Z only | document `reserveBid_Period.timeInterval`; ZIP entry names; silver `n_unique(timestamp_utc)` = 1 per day |
| BE mRID reuse across products | per-document mRID `Counter`: 1 Aug 100 series / 81 unique, 15 Sep 100 / 68 unique; the duplicate pairs differ in `standard_MarketProduct` |
| A07 labelled `AUCTION-mFRR` for DE-LU | tag census: 1,400 DE-LU series `(acquiring 10Y1001C--00085O, AUCTION-mFRR, A07)` |
| Aggregated silver = 768 rows, BE only, `A14`, `A01`, 96 per direction per day, values 93 to 581 MW | Polars on silver; per-day min/max; re-parse `equals` True |
| A24 documents UTC-day aligned, two series, curve A03, 83 to 95 declared points per series | bronze 22 to 25 Sep, lxml |
| `published_at` is createdDateTime, a fetch-time stamp | `h8_balancing.py:91`; lead `published_at` 2026-08-16 14:12:08 vs `fetched_at` 14:12:07 (FR 1 Aug); aggregated 00:20:05 vs 00:20:05 |
| `ingested_at` stamped at transform | `h8_balancing.py:99` |
| Request URLs | lead `.meta.json`: `https://web-api.tp.entsoe.eu/api?documentType=A37&periodStart=202609150000&periodEnd=202609160000&connecting_Domain=10YBE----------2&businessType=B74&offset=0&processType=A47&securityToken=<redacted>`; aggregated: `documentType=A24&periodStart=…&periodEnd=…&area_Domain=10YBE----------2&processType=A51` (no offset; `endpoints.py:348-353`) |

## Body corrections (canonical notes, mirrored byte for byte, CRLF kept)

`30-vendors/entsoe/datasets/balancing_energy_bids.md` (+39/-13):
- **API table, Pagination:** added the observed 100 series per response and that gridflow never requests `offset=100`.
- **Bronze granularity:** one file per ZIP entry, over six zones per UTC day, naming which zones publish (`client.py:249`, `:367-381`, `endpoints.py:395`).
- **Live shape by zone:** a new block after the price callout (BE, FR and DE-LU envelopes; mRID reuse; `AUCTION-mFRR`; codes unverified).
- **Point-in-time field:** "none" → `published_at` as a fetch-time stamp.
- **Silver schema:**
  - `timestamp_utc` formula → `(position - 1)` (`parsers.py:530`);
  - `quantity_mw` source → `quantity.quantity` alias;
  - `bid_mrid` "the bid identity" corrected;
  - `direction` source → `flowDirection.direction`;
  - `resolution` PT15M;
  - added a `published_at` row;
  - `ingested_at` transform-time;
  - a list of fields not carried to silver.
- **Silver sample:** labelled as the GB fixture.
- **Known issues:**
  - the offset bullet is rewritten with its measured effect;
  - added the BE dedup collision and the BE 22:00 to 24:00 loss;
  - "bid_mrid is the bidder identity" is corrected;
  - "Direction casing varies" now says only `flowDirection.direction` appears live.
- **Implementation delta:** "Pagination not implemented…4800" → the loop exists, but its step and counter both miss A37.

`30-vendors/entsoe/datasets/aggregated_balancing_energy_bids.md` (+32/-16):
- Tuple line: `B74` → live `A14`.
- Bronze granularity: six zones per UTC day, no offset. Added a live-shape block (BE only; document-level area; UTC-day period; two series; `A14`, `A01`, A03; 83 to 95 declared points).
- Point-in-time field → `published_at`.
- Silver schema:
  - `timestamp_utc` formula;
  - `area_code` empty with its cause cited;
  - `business_type` `A14`;
  - `bid_mrid` `1`/`2`;
  - `direction` present;
  - `standard_market_product` `A01`;
  - added a `published_at` row;
  - `ingested_at` transform-time.
- Silver sample labelled as the GB fixture.
- Known issues:
  - the "envelope unverified, TODO" line is replaced by the populated-envelope update;
  - added the area defect (and the latent zone merge), BE-only coverage, and the stale classification;
  - the product bullet is corrected.

Not changed: both curl examples (right for the vendor), the overviews, the modelling notes, `last_verified` (the seat's call), and the front matter (no `page:` block, no `---`).

## Not verified

- Meanings of product codes `A05`, `A07`, `A02`, `A01`, `businessType` `A14`, status `A06`/`A11`, and `divisible` `A01`/`A02`. Also whether direction `A01`/`A02` means up/down for A37/A24 (vault claim only).
- That 100 series is the vendor's page size for A37. It is observed on all 42 requests, and the vault's §4.1 citation says "increment by 100", but I did not read the ENTSO-E guide. Whether FR's or DE-LU's full day has thousands of bids is not measured (no live calls).
- Whether BE's 100 series are the whole day. Very likely not: every response is exactly 100.
- Whether one `Bid_TimeSeries` is one BSP offer (nothing names the BSP).

## If the seat ships anyway (not recommended): the shape I would have used

- **Chart:** none from the lead. A BE-only line of offered MW by direction would understate by at least 10.6% plus unknown truncation. FR and DE-LU would be single points.
- **The aggregated member alone** could carry a truthful small page: BE aggregated offered MW, two lines (`A01`, `A02`), 22 to 25 Sep 2026, 93 to 581 MW. That needs `area_code` either fixed or explained in the frame.
  - It would mean swapping the family lead in `entsoe.json`, a shared file, so it is the seat's call, not a workaround I attempted.
- **Commands (lead):** `gridflow ingest --source entsoe --dataset balancing_energy_bids --start 2026-09-13 --end 2026-09-22` and `gridflow transform … --start 2026-09-13 --end 2026-09-21`. BE's 22:00 to 24:00 cannot be recovered by widening the window, because the filter drops it.

## Screenshots (blank family page)

- Headless Chrome, `file://`, every call under `timeout 60` with `--timeout=15000 --virtual-time-budget=5000`. Profile: `scratchpad/beb-chrome`.
- Widths: 1440, 1024 and 768, plus 390 via a 390 px iframe. Files are in `scratchpad/beb-shots/`.
- Hero name, both id chips (the long `entsoe/aggregated_balancing_energy_bids` chip fits at 390, ending at about 373 px), scenery (turbines, labels, interconnector) and footer: nothing clipped or overlapping.
- The `--force-dark-mode` capture looks identical to light (a petrol hero). Dark is not separately evidenced, as in procured_balancing_capacity.
- Every Chrome call exited 0. No server was started on 9823.

## Template problems

None found. The blank render is as designed.

## Open questions for the seat

1. Hold the family page and mark `balancing_energy_bids` silver unpublished until the fix? Recommend **yes** to both.
2. Should the family lead become `aggregated_balancing_energy_bids` once its area is fixed? It is the smaller but faithful table. A shared-file (`entsoe.json`) decision.
3. Named unknowns for the fix unit:
   - the A37 page size;
   - the product, status and business-type code meanings (and why `A07` bids are `AUCTION-mFRR`);
   - the time basis of the price unit;
   - whether a series is one BSP offer;
   - a document-level `area_Domain` fallback across all H8 datasets.
4. The `_event_window.py` entries for A37 (FILTER_SAFE on DE-LU evidence only) and A24 (UNKNOWN) need re-classifying from the BE evidence.

## Defects (pasteable, for gridflow BACKLOG and the vault remediation page)

- **ENTSO-E A37 paging dead (`balancing_energy_bids`).** `count_timeseries_or_none` (`client.py:483-512`) counts only `TimeSeries`, and A37 sends `Bid_TimeSeries`, so the paging loop (`client.py:313-349`) always stops after `offset=0`. Its step `_ENTSOE_PAGE_SIZE = 4800` (`client.py:63`) also misses the observed 100-series page.
  - Effect: every zone-day is cut at 100 bids. FR and DE-LU silver hold only 00:00 UTC (100 rows a day). BE holds 100 series a day.
  - Fix: count `Bid_TimeSeries` for ReserveBid roots, page in steps of 100 until a short page, then re-ingest.
- **ENTSO-E A37 dedup key omits product (`balancing_energy_bids`).** BE reuses one series mRID for an `A05` and an `A07` bid, and `unique_subset = (timestamp_utc, area_code, bid_mrid, direction)` (`h8_balancing.py:148`) with `keep="last"` drops one of each pair.
  - Measured: 9,383 of 88,146 BE points (10.6%) lost, 13 to 21 Sep and 1 to 5 Aug 2026.
  - Fix: add `standard_market_product` and `original_market_product` to the key (zero collisions then), and re-transform.
- **ENTSO-E A37 BE 22:00 to 24:00 UTC lost daily.** BE documents run 22:00Z to 22:00Z, and the HALF_OPEN filter (`h8_balancing.py:152`) drops the pre-midnight quarter-hours, which no request returns for the prior day. 10,628 points lost over 14 days.
  - The FILTER_SAFE evidence (`_event_window.py:528-556`) is DE-LU only. Same class as procured_balancing_capacity defect 7.
- **ENTSO-E A37 price and bid attributes dropped.** `energy_Price.amount` (EUR/MWh), `acquiring_Domain.mRID`, `auction.mRID`, `status` and `divisible` are not in `BalancingEnergyBidsTransformer.output_cols` (`h8_balancing.py:134-147`). The price is the existing v0.19 carry; the rest are new.
- **ENTSO-E A24 area empty (`aggregated_balancing_energy_bids`).** `area_Domain.mRID` is at document level, and `parse_timeseries_xml` reads it only inside TimeSeries (`parsers.py:302`, `_root_document_metadata` `:121-145`). All 768 BE rows (22 to 25 Sep 2026) have `area_code == ""`.
  - A zone merge is latent under the key `(timestamp_utc, area_code, bid_mrid, direction)`, because every document numbers its series `1`/`2`.
  - Same root cause as procured_balancing_capacity and current_balancing_state.
- **Stale A24 classification.** `_event_window.py:910-936` says "never observed populated". BE is populated 22 to 25 Sep 2026, with UTC-day documents.
- **Fixtures unrepresentative.** The A24 fixture puts `area_Domain.mRID` inside TimeSeries with `businessType` `B74`; live has document-level area and `A14`.
