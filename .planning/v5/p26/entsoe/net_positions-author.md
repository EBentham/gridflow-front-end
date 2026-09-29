# entsoe/net_positions: author report

Writer: Opus 5.5 · high, 2026-09-29. The page is built in the batch worktree (`p26-entsoe`). The canonical note is edited in `vault-p26-entsoe`, and the mirror copy is byte-identical (`cmp` clean, CRLF kept).

## Status

- **Build:** `gridflow-build --only entsoe/net_positions` wrote the page on the dataset template with no errors.
- **Detector:** one finding, the accepted advisory `em-dash-overuse` ("66 em-dashes"). It counts the dash padding in the EIC and `REGION_CODE-----` values. The rendered page has no `—` characters.
- **Artefacts:**
  - `series/entsoe/net_positions.json`: `spec_origin: vault`, 2 series × 672 points, 672 rows used.
  - `samples/entsoe/net_positions.json`: `generated_by: gridflow-sample`, 8 rows.
  - `notebooks/entsoe/net_positions.json` plus `-5.png`: written by `run_notebooks.py`, 5 cells, no errors.
  - There was no staged chart spec and no authored override to retire.
- **Screenshots** at 1440, 1024, 768 and 390, taken through CDP with the demo notebook open and the frame unfolded. Nothing is clipped or overlapping, and there is no horizontal overflow at any width. The site has no dark-mode rules (no `prefers-color-scheme` in the CSS), so there is one theme to check.
  - Shots are in `scratchpad/np-shots/open-<w>_t*.png`.

## The three things the brief flagged

- **Sign.** `quantity_mw` is never signed. Every silver row is positive (min 1.5 MW), and the transformer only casts the value (`h6_market.py:86`).
  - ENTSO-E marks direction instead. DDD v3r4 p.55 says the value comes "with indicator whether the value represents import or export".
  - In the XML the indicator is which domain holds the zone. The other domain holds `REGION_CODE-----` (probe `entsoe_A25_net_positions_FR_20260601.xml:19-20`).
  - The DDD does not say which side means export. The page reads zone-as-`out_Domain` as export and labels that "a project reading", checked for DE-LU.
- **Scope.** Silver holds day-ahead positions only.
  - The request sends `contract_MarketAgreement.Type=A01` (daily), and the XML echoes `contract_MarketAgreement.type A01` and `auction.type A01`.
  - The DDD publishes the total (with intraday) separately.
  - Zones: gridflow requests six (`DEFAULT_ZONES`, `endpoints.py:395`). Four carry data: DE-LU, BE, FR and NL, all `PT15M`, with 96 rows per zone per day and exactly one direction per quarter-hour.
  - GB and IE-SEM return a Reason 999 "No matching data" acknowledgement on every bronze day (28 of 28 files).
- **Chart.** DE-LU, 14 to 20 September 2026 UTC, every quarter-hour as sent.
  - It is a stacked area with two series, "exporting" (`in_area_code` = `REGION_CODE-----`, petrol) and "importing" (`in_area_code` = DE-LU, olive).
  - Only one band shows at a time. Height is the size of the position and colour is the direction.
  - The trader's reading: importing up to 11,428 MW at 17:30 on the 14th and all of the 16th, then midday exports from the 15th, peaking at 13,219 MW at 10:45 on the 19th, and exporting all of the 20th.
  - The notebook plots the signed view (export positive), which the chart spec can't express.

## Evidence

| Claim (field) | Evidence |
|---|---|
| Request URL, parameter order (`raw_feed.requests`) | Bronze `.meta.json` `request_url` for 2026-09-20: `documentType, periodStart, periodEnd, in_Domain, out_Domain, businessType, contract_MarketAgreement.Type, securityToken`. `client.py:249-262` sets `out_domain=mrid` for `domain_style="zone"`; `_domain_params` is at `client.py:548`. DE-LU's EIC has no dashes, so the URL needs no `%2D`. |
| One GET per zone per UTC day; six zones (`raw_feed.note`) | `client.py:163-170` (`day_subwindows`); `DEFAULT_ZONES` at `endpoints.py:395`. |
| GB and IE-SEM return no-data acknowledgements in every response (`raw_feed.note`) | 28 of 28 GB and IE-SEM bronze XMLs contain "No matching data found for Data item IMPLICIT_ALLOCATIONS_NET_POSITIONS [12.1.E]". The vault note's 2026-05-08 live GB probe says the same. |
| Ingest `--end 2026-09-21` excludes that date (`raw_feed.commands`) | `utils/time.py:123-140` `day_subwindows`: `[start, end)`, and a midnight end excludes the date. The dataset has no `PARTITION_SOURCE_OFFSETS`, and each response tiles the UTC day exactly (NL XML: TimeSeries periods 00:00 to 07:00, 07:00 to 15:30 and so on to 24:00). |
| Transform `--end` is inclusive | Batch convention (author brief); the same as the cross_border_flows page. Not re-derived from `runner.py`. |
| Day-ahead only (`summary`, `what_it_is`) | Request `contract_MarketAgreement.Type=A01`; XML `contract_MarketAgreement.type A01`. DDD v3r4 p.55: "Separate publications are foreseen for the day-ahead timeframe and for the aggregated (i.e. total) net position". |
| Exports and imports netted, in MW, per market time unit (`summary`, `what_it_is`) | DDD v3r4 p.55: the regulation text says "for every market time unit the net positions of each bidding zone (MW)"; the description says "netted sum of electricity exports and imports". |
| A size plus a direction, not a sign (`what_it_is`, `quantity_mw`, caption) | DDD p.55 ("indicator whether the value represents import or export"). Silver min `quantity_mw` is 1.5 MW over all 5,376 rows. `h6_market.py:86` only casts. |
| Zone as `out_area_code` = export (project reading) | Hourly join of the signed position with actual_generation minus actual_load, same zone and hour. DE-LU: corr 0.89, sign agreement 0.89. FR 0.52 / 0.96, BE 0.41 / 0.95, NL 0.63 / 0.44 (see Unverified). Against day-ahead price minus the four-zone mean, corr is negative for DE-LU (-0.45), NL (-0.38) and BE (-0.30): exporting zones price below the mean. Corroboration only, not cited on the page: entsoe-py `parse_netpositions` treats `REGION` in `out_domain.mrid` as import (factor -1). |
| Key (`record.key`) | Transformer dedup subset `(timestamp_utc, in_area_code, out_area_code, business_type)`, `h6_market.py:88-98`. |
| `timestamp_utc` = period start + (position - 1) × resolution | `parsers.py:530` (seat note). |
| `published_at` is a fetch-time stamp | Ruling #39. Rows: `published_at` 2026-09-26T18:16:48Z against bronze `fetched_at` 2026-09-26T18:16:~ for data on 2026-09-17. |
| Quarter-hourly in the responses gridflow holds (`facts.cadence`, `resolution`) | Every silver row is `PT15M` (4 zones × 14 days × 96). |
| One direction per quarter-hour "here" (caption) | 0 (timestamp, zone) pairs have more than one row across all silver. |
| Chart numbers (alt) | The committed series: importing max 11,428.3 at 2026-09-14T17:30Z; the 16th is 96 of 96 importing; exporting on the 14th is 10 points, max 852.2; exporting max 13,218.9 at 2026-09-19T10:45Z; the 20th is 96 of 96 exporting, max 12,714.2. |
| Notebook `plot_alt` numbers | The same silver, signed: first point -4,147 at 00:00 on the 14th; min -11,428; export peaks 8,403 (15th) to 13,219 (19th); the 16th is all negative and the 20th all positive. The image was checked by eye. |
| `notebook.lead` | gridflow_models `research/handles/source.py:401-451`: `WHERE` on the `schema_manifest.py:175` date column `timestamp_utc`, inclusive ends via `_date_range_predicate`, bitemporal/lineage exclude, `ORDER BY timestamp_utc` only. |
| Sample rows | `gridflow-sample`: DE-LU 06:00 to 07:45 UTC on 2026-09-17. Rows 1 to 4 are (DE-LU, `REGION_CODE-----`) and rows 5 to 8 are (`REGION_CODE-----`, DE-LU), so the flip happens at 07:00. |

## Note-body corrections (canonical vault note)

1. **Silver schema.** The note said "the silver `out_area_code` will mirror `in_area_code`". That is false: the response carries the zone on one side and `REGION_CODE-----` on the other. Cites the probe XML (lines 19-20) and `h6_market.py:66-72`.
2. **Silver sample.** The old sample was a GB row with `-250.0`, `PT60M` and mirrored codes, none of which matches the rows (GB has no data, no value is negative, all resolutions are `PT15M`). It is replaced with a real DE-LU export row from 2026-09-17T07:00Z, now including `published_at`.
3. **Known issues.** "A negative `quantity_mw` indicates net export ... positive = net import" is replaced with the unsigned value, the DDD's direction-indicator wording and the project reading (DE-LU corr 0.89).
4. **Parameter tuple.** The `A01` row now says it selects the day-ahead position and that the DDD keeps the total separate.
5. **Known issues.** Added that IE-SEM (also in `DEFAULT_ZONES`) returns the same Reason 999 acknowledgement.

I left one stale item alone: "Point-in-time field: `none`" (silver now carries `published_at`). The note's "Historical depth 2014-12-05 onward" is unevidenced, so the page does not use it.

## Unverified

- **Which side means export is not stated by ENTSO-E in anything I could read.** The DDD only says an indicator exists. The API guide and the transparency knowledge-base page returned HTTP 400 to WebFetch.
  - The page therefore says "a project reading" and cites the DE-LU check.
  - For the seat: if the Postman guide can be read, it may settle this.
- **NL sign agreement is only 0.44** (corr 0.63). NL's generation minus load averages -5,341 MW while its position averages +2,045 MW export. That points to incomplete NL generation coverage in `actual_generation`, not to a reversed sign, but I have not proven it. The page claims the check for DE-LU only.
- **The transform `--end` inclusive semantic** follows the brief and the sibling pages; I did not re-read `runner.py`.
- **DE-LU is labelled "DE-LU" from its EIC `10Y1001A1001A82H`.** This matches the `actual_generation` area_name "Germany / Luxembourg".

## Open questions for the seat

- **Is the stacked area acceptable for an unsigned two-direction series?** The alternative was a two-series line. It breaks at each flip, and one- or two-quarter-hour runs (for example 13:00 on the 14th) would draw nothing as single-point segments. The stacked area draws them as slivers.

## Template problems

- **The chart spec cannot sign a value by a direction column.** A `negate`/`sign_by` option (or a group-level sign in `group_map`) would let this page draw the signed position the trader wants, with export above zero and import below, as the notebook does. The same gap will apply to any A25/B09-style "size plus direction" table. I did not work around it.
- **At 390 the key note breaks "DE-LU" at its hyphen** ("DE-" / "LU"). It is cosmetic, not clipped. A non-breaking hyphen in key notes would be template or CSS work.
- **In the unfolded frame and the notebook `.head(8)` output, codes such as `REGION_CODE-----` render with their dashes.** That is expected, and it is where the detector's advisory count comes from.
