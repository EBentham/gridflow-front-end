# procured_balancing_capacity: author report (writer, 2026-09-29)

Writer: Opus 5.5 · high, one agent, two advisor calls. Worktrees as in `BATCH-entsoe.md`; screenshot port 9822.

**Status: HOLD recommended. No `page:` block written. Note body corrected and mirrored. Page builds blank, detector `[]`.**

- `gridflow-build --only entsoe/procured_balancing_capacity`: exit 0, `wrote: data-sources/entsoe/procured_balancing_capacity.html (blank)`.
- `detect.mjs --json`: `[]`.
- No artefacts made (series, sample or notebook). None existed before. There was no staged chart spec and no authored override to retire.

**Recommended ruling for the seat:** hold the page blank, like nonbm and netbsad (ruling #37), until a gridflow fix unit lands. **Yes.** Also mark this silver table unpublished until then. **Yes.**

Unlike nonbm, a `page:` block here *would* build: 440 rows pass the eight-row sampler, and distil would produce a series. But every row is one arbitrary survivor per quarter-hour, drawn from four countries' series. Its area, agreement type and direction are all blank, and its price is gone. No chart, caption or eight-row frame built on this silver can be true against the rubric.

## Why coverage is 1 to 5 August only (report-only; local facts)

- Bronze holds one ingest run: 30 files, all fetched between 2026-08-16 14:14:28 and 14:15:12 UTC, for data dates 1 to 5 August 2026.
  - Silver was transformed at 14:15:14 the same day (`ingested_at`).
- The sibling H8 datasets share that run: `current_balancing_state`, `balancing_energy_bids` and `aggregated_balancing_energy_bids` hold bronze for 1 to 5 Aug only, fetched from 14:10 UTC the same day.
- So the thin coverage is simply one five-day smoke ingest. No later ingest was run. It is not a vendor limit.
- Within those days, silver holds 88 rows per day (00:00 to 21:45 UTC). That is 5 × 88 = 440, the DATA-MATRIX figure. The missing 22:00 to 24:00 is explained below.

## What silver holds versus what ENTSO-E sent

Bronze requests, one per zone in `DEFAULT_ZONES` per UTC day (`client.py:249`, `endpoints.py:395`):
- GB (`10YGB----------A`) and IE-SEM (`10Y1001A1001A59C`) return acknowledgement reason 999, "No matching data found", on all five days.
- FR, NL, BE and DE-LU each return a `Balancing_MarketDocument` of about 105 kB.

What the populated responses carry (read with lxml straight from bronze, 2,000 declared points):

| Field | Where it sits | Values seen | In silver? |
|---|---|---|---|
| `area_Domain.mRID` | document level, once | FR, NL, BE, DE-LU EICs | **No**: `area_code` is `""` on all 440 rows |
| `type_MarketAgreement.type` (lowercase `.type`) | per TimeSeries | `A01` (all four), `A13` (NL) | **No**: `market_agreement_type` is `""` on all rows |
| `businessType` | per TimeSeries | `B95` on every series | yes (`B95` on all rows) |
| `flowDirection.direction` | per TimeSeries | `A01` and `A02` in every area | **No**: parsed, then dropped by `output_cols` |
| `mktPSRType.psrType` | per TimeSeries | `A03` (FR, BE, DE-LU), `A04` (NL) | **No**: tag not matched |
| `standard_MarketProduct.marketProductType` | per TimeSeries | `A01` (all but BE) | no |
| `quantity` + `quantity_Measure_Unit.name` | per Point, `MAW` | 1 to 202 | `quantity_mw`, but see the collapse |
| `procurement_Price.amount`, `currency_Unit.name` `EUR`, `price_Measure_Unit.name` `MAW` | per Point | 0 to 13.75 | **No**: transformer reads `quantity` only |
| `curveType` | per TimeSeries | `A03` on all; one Point at position 1 per series | forward-filled by the parser over the Period |
| resolution | per Period | `PT15M` | yes |

- **Reserve type (FCR, aFRR, mFRR):** the repo does not establish it for A15.
  - The connector hard-codes `processType=A51` (`endpoints.py:354-360`).
  - `businessType` is `B95` throughout, so the repo's `A95`-`A98` to fcr/afrr/mfrr/rr mapping (`contracted_reserves.py:68`, `activated_balancing_*.py`) does not apply.
  - The repo has no code list for `A51`, `psrType` `A03`/`A04` or agreement type `A13`. My outside knowledge says `A51` is aFRR, but I did not state it anywhere.
  - Named unknown for a research unit.
- **Direction:** `A01` and `A02` in every area; meaning unverified in-repo (vendor code list: up, down).
- **Unit:** `MAW` for quantity (MW). Price is EUR per `MAW`; the per-hour or per-period basis is unverified.
- **Series are not totals.** For example, on 1 August 22:00 to 02:00 UTC, DE-LU has 42 up series summing 262 MW and 58 down series summing 275 MW, each with its own price. BE shows 23 up and 32 down series. Each series looks like one accepted offer, but that is unverified.
- **Market agreement:** `A01` everywhere; NL also sends `A13`. Nothing here should be summed across direction or agreement type, and silver cannot separate either.

## gridflow and data defects (for a gridflow fix unit)

1. **Document-level area not parsed.** `area_Domain.mRID` is a child of the document root, but `parse_timeseries_xml` reads it only among TimeSeries children (`parsers.py:302`). `_root_document_metadata` (`parsers.py:121-145`) takes only mRID, revision, status and createdDateTime. Result: `area_code == ""`.
2. **Lowercase agreement tag not matched.** Live responses spell it `type_MarketAgreement.type`; the parser accepts `Type_MarketAgreement.Type`, `type_MarketAgreement.Type`, `MarketAgreement.Type` and `marketAgreement.Type` (`parsers.py:320-326`). Result: `market_agreement_type == ""`.
3. **Flat `mktPSRType.psrType` not matched.** The parser reads a nested `MktPSRType`/`psrType` (`parsers.py:345`).
4. **Direction and price dropped.** Direction is parsed (`flow_direction`) but is absent from `output_cols` and the dedup key (`h8_balancing.py:172-183`). `procurement_Price.amount` never becomes a value, since `value_tag="quantity"` (`h8_balancing.py:32`, `parsers.py:148-153`).
5. **Dedup collapse.** With defects 1 and 2, the key `(timestamp_utc, area_code, market_agreement_type)` is effectively `timestamp_utc`, and `unique(keep="last")` (`h8_balancing.py:104`) keeps whichever point parsed last.
   - Reproduced with gridflow's own parser on 1 August 2026 bronze: 8,020 points (FR alone: 1,060) → 96 after the key → 88 in the UTC day window.
   - Silver's values switch between countries through each day. Checked on 1 August: each silver value equals the last point parsed at that time, in file order.
     - 00:00: 5.0, from DE-LU (`raw_…1eaf3f9e.xml`).
     - 02:00: 1.0, from BE (`…3795e1df`).
     - 10:00 and 20:00: 2.0, from NL (`…7cd270de`).
   - `20-domain` in the vault has no `A51` entry, so the A51 meaning stays unverified.
6. **Paging stops after page one.** `_ENTSOE_PAGE_SIZE = 4800` (`client.py:63`), and the loop breaks at a page with fewer than 4800 series (`client.py:347`). Every populated A15 response carried exactly 100 series (20 of 20 files). Most ended before the day did:
   - DE-LU at 02:00 UTC every day;
   - BE between 02:00 and 10:00 UTC;
   - NL at 02:00 UTC on 3 and 5 August.

   FR reached 22:00 UTC on every day, but with exactly 100 series it may still be truncated. `offset=100` was never requested.
   - The comment at `client.py:55-62` says 4800 series per response. The canonical `balancing_energy_bids` note says "increment `offset` by 100" and its probe also saw 100 series. The 100-per-page vendor rule is sourced only there; I did not verify it against the ENTSO-E guide.
7. **22:00 to 24:00 UTC lost every day.** Documents run from 22:00 UTC to 22:00 UTC (the CEST day). The day-D request's document ends at D 22:00Z; the day-D+1 document starts at D 22:00Z and its first eight quarter-hours are outside D+1's UTC window. The HALF_OPEN event-window filter (`EVENT_WINDOW_FILTER = True`, `h8_balancing.py:187`) drops them.
   - Reproduced: 2,216 parsed points before 2026-08-02T00:00Z in the 2 August bronze, and 0 at or after 2026-08-01T22:00Z in the 1 August bronze.
   - The classification itself records the upper edge as unobserved (`_event_window.py:515-519`).
8. **Fixture unrepresentative.** `tests/fixtures/entsoe/procured_balancing_capacity_gb.xml` puts `area_Domain.mRID` inside TimeSeries with a capitalised `Type_MarketAgreement.Type`, which is why the tests pass. Also, GB has no data at all live.

## Evidence table

| Claim | Evidence |
|---|---|
| Silver has 440 rows, 88 per day, 00:00 to 21:45 UTC, 1 to 5 Aug | Polars on `silver/entsoe/procured_balancing_capacity/**`: `group_by(date)` gives 88 rows per day, first 00:00 and last 21:45 |
| `area_code` and `market_agreement_type` are empty; `business_type` is B95 on all rows | Polars `group_by(area_code, market_agreement_type, business_type, resolution)`: one group, 440 rows |
| Parser leaves area and agreement type empty on live XML | `parse_timeseries_xml(FR 08-01, value_tag="quantity")[0]`: `area_domain ''`, `market_agreement_type ''`, `flow_direction 'A02'`, `production_type ''` |
| 8,020 → 96 → 88 collapse | gridflow venv, all 1 Aug bronze, `unique(subset=[timestamp_utc, area_domain, market_agreement_type])` |
| 100 series per populated response | lxml count of `TimeSeries` in all 20 populated files: 100 each |
| Requests go to six zones, GB and IE-SEM return ack 999 | `.meta.json` `request_params.area_Domain`, 962-byte `Acknowledgement_MarketDocument` bodies |
| One ingest run on 16 Aug for 1 to 5 Aug | `.meta.json` `fetched_at` 14:14:28 to 14:15:12; silver `ingested_at` 2026-08-16 |
| `published_at` is createdDateTime, within seconds of fetch | `h8_balancing.py:91`; GB 08-01: created 14:14:29Z, `fetched_at` 14:14:28.9 |
| Series each have their own quantity and price | lxml profile: DE-LU up, 22:00 to 02:00: 42 series, 262 MW, price 0.15 to 0.75 |

## Body corrections in the canonical note (mirrored byte for byte)

All are small spans in `30-vendors/entsoe/datasets/procured_balancing_capacity.md` (LF endings at HEAD; kept):
- Overview: "reports the total MW under contract for each interval" → the MW is split across many series, each with one direction, quantity and price.
- API table, Pagination: "not iterated by current connector" → pages in steps of 4800, stops below 4800, and live pages carry 100 (`client.py:63`, `:347`).
- Bronze granularity: "(control_area, …)" → "(zone in `DEFAULT_ZONES`, UTC day window, offset page)" (`client.py:249`, `endpoints.py:395`).
- After the fixture sample: one paragraph on how live A15 documents differ.
- Silver schema:
  - `area_code` and `market_agreement_type` are empty on live responses, with the parser lines cited.
  - `business_type` is `B95`, replacing "often empty".
  - Added the `published_at` row (`h8_balancing.py:91`).
  - `ingested_at` is stamped at transform time (`h8_balancing.py:99`).
- Silver sample: labelled as the GB fixture.
- Known issues:
  - GB ack extended to August, adding IE-SEM.
  - Added bullets for the silver collapse, paging after page one, and the 22:00 to 24:00 loss.
  - "`business_type` often empty…" replaced by "`B95` throughout".
  - The stale "pagination not iterated" bullet was replaced.
- Implementation delta: the "offset hard-coded" bullet corrected, and "which the parser surfaces correctly" corrected (it does not).

Not changed:
- the curl example (right for the vendor);
- "`processType=A51` (procurement)" in the overview (the A51 meaning is unverified in-repo);
- `last_verified` (seat's call).

## Not verified

- The ENTSO-E 100-per-offset page size (only the vault's `balancing_energy_bids` note and observed counts).
- The meanings of `processType` `A51`, `psrType` `A03`/`A04`, `type_MarketAgreement` `A13`, and direction `A01`/`A02` for A15.
- Whether one series is one accepted offer.
- The time basis of the price unit.

## If the seat ships anyway (not recommended): the shape I would have used

- **Request:** `https://web-api.tp.entsoe.eu/api?documentType=A15&periodStart=202608010000&periodEnd=202608020000&area_Domain=10YFR-RTE\x2D\x2D\x2D\x2D\x2D\x2DC&offset=0&processType=A51&securityToken=$ENTSOE_API_KEY` (parameter order from the bronze `request_url`).
- **Commands:** `gridflow ingest --source entsoe --dataset procured_balancing_capacity --start 2026-08-01 --end 2026-08-06` and `gridflow transform … --end 2026-08-05`.
- **Chart:** `type: none`, since no silver column supports a truthful series.

I would still recommend against it: the frame would show eight rows with a blank `area_code`.

## Screenshots (blank page)

- Headless Chrome, `file://`, each call under `timeout 60`, profile `scratchpad/pbc-chrome`.
- 1440, 1024 and 768, plus 390 via a 390 px iframe. Files: `scratchpad/pbc-shots/`.
- Hero name, the id chip, scenery (turbines whole, labels whole) and the footer: nothing clipped or overlapping.
- `--force-dark-mode` captures look identical to light (the hero is petrol in both). Dark is not separately evidenced.
- Chrome stayed alive after each capture until `timeout` ended it (exit 124). Every PNG was written first. Dropping `--remote-debugging-port` may avoid the wait.

## Template problems

None found. The blank render is as designed.

## Open questions for the seat

1. Hold and unpublish the silver until a gridflow fix unit lands? Recommend yes to both.
2. The fix unit's named unknowns:
   - the A15 page size;
   - the code meanings above;
   - whether series are offers;
   - the price time basis;
   - a document-level area fallback for every H8 dataset that uses `area_Domain` (`current_balancing_state` and `aggregated_balancing_energy_bids` may share defect 1: worth a check).
