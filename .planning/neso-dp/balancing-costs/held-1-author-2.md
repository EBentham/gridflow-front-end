# Held pages, Balancing costs part 1: writer round 2 (2026-10-23)

Answers `held-1-review.md` (APPROVE on all four, 10 nits). Every nit is fixed. I also brought the daily cost note body up to the
16 October capture, as the coordinator asked. Page edits are in the `page:` blocks only. The body edit is confined to the cost
note's files section and cadence paragraph. CRLF is kept on every line, and all four notes are mirrored byte for byte (`cmp`
clean).

| Page | Build `--only` | Detector | Em or en dashes / banned words |
|---|---|---|---|
| `bsuos-fixed-tariffs` | `bsuos_fixed_tariffs` ok | `[]` | 0 / 0 |
| `gb-system-inertia-bid-and-offer-costs` | `inertia_bid_offer_costs` ok | `[]` | 0 / 0 |
| `balancing-services-use-of-system-bsuos-daily-forecast` | `bsuos_daily_forecast` ok | `[]` | 0 / 0 |
| `daily-balancing-costs-balancing-services-use-of-system` | `daily_balancing_costs` ok | `[]` | 0 / 0 |

The banned-word scan now also covers "key them". Re-measured in iframes at 390 and 1440 on my 9922 server: `scrollWidth` equals
the viewport on all four, and nothing is outside the viewport, clipped or scrolling. New 390 shots of the two pages whose hold lines
changed: `held-1-shots\r2-*-390.png`. The server was started with its PID recorded (9409, Windows 25660) and stopped by that PID.
Port 9670 was not touched.

## The ten nits

| Finding | Fix |
|---|---|
| 1.1 Fixed tariffs, "Biannual" ambiguous | cadence: "Biannual, as NESO lists it (six monthly): updated when tariffs are published" |
| 2.1 Inertia, B and C are not offer prices | `what_it_is`: "...: at the average bid price (A), or assuming displaced energy is replaced at the average wind bid price (B) or highest bid price (C). NESO calls them indicative: they use all bid prices." ("three ways" dropped for the budget; A, B and C enumerate them) |
| 2.2 Inertia, NESO as tagger | "Some accepted Balancing Mechanism offers are tagged for system inertia." |
| 3.1 Forecast hold line | "Rows give no settlement run or issue time; the header's £ byte is not valid UTF-8." (16 words). "Key them by" is gone. The byte is named, and "no silver table" stays in the raw-feed note |
| 3.2 Forecast, BSUoS not expanded | Expanded in the summary ("...forecast of the Balancing Services Use of System (BSUoS) charge in £/MWh, with the cost and volume behind it") and in `what_it_is`. To fit, the body now says "NESO forecast it per half hour: forecast cost (£) over forecast volume (MWh)" and ends "NESO warns it may bear no relation to later tariffs; it ended with modification CMP361." |
| 4.1 Cost hold line | "Rows are not labelled with a settlement run, so there is no silver table." (the checker's wording) |
| 4.2 Cost raw-feed note | "From NESO's CKAN portal: `package_show`, then each yearly file whole unless `last_modified` is unchanged (first and newest shown). All stay in bronze; the workbook lists NESO's missing settlement periods." |
| 4.3 Cost summary range | "...split into six categories, from energy imbalance to other costs." |
| 4.4 Cost, BSUoS not expanded | "Balancing Services Use of System (BSUoS) charges recover the cost of day-to-day operation of the transmission system." ("from generators and suppliers" dropped, as suggested) |
| 4.5 Cost `how_used[1]` | "An implied overall cost per MWh, with the volume package for the same periods" |

## Cost note body: the 16 October capture as newest

Measured read-only with Polars. For the gap count I used the same calendar-aware method that reproduces the note's 6 gaps on the
8 October capture.

| Fact | 8 October capture | 16 October capture (now newest) |
|---|---|---|
| File | `raw_20261008T100420Z_1d040751-..._8d...csv` | `raw_20261016T200131Z_1d040751-f77f-4641-9130-d49f8cbfe54f_db15c574.csv` |
| Bytes / rows | 733,417 / 8,826 | 774,080 / 9,306 |
| `ckan_last_modified` | 2026-10-03T11:18:19.357113 | 2026-10-16T06:39:44.390449 |
| Settlement dates | 2026-04-01 to 2026-10-01 | 2026-04-01 to 2026-10-11 |
| Duplicate (date, period) pairs | 0 | 0 |
| Missing pairs | 6 | 6 (the same six) |
| Header | new order | new order (identical) |

Edits to the body:

- **Capture paragraph.** It now says all ten resources were captured on 2026-10-08 and the 2026-27 resource again on 2026-10-16,
  which is its newest capture. It keeps the 8 October figures for reference.
- **2026-2027 table row.** Now 774,080 bytes, 9,306 rows, vintage 2026-10-16T06:39:44.390449.
- **Total rows.** 166,538 becomes 167,018, taking each resource's newest capture.
- **Disjointness.** Re-checked on the new capture: no duplicate pairs.
- **In-progress year.** The `TODO` on its last settlement date is replaced by the measured range. The TODO on the vendor's
  publication lag stays, because two captures do not establish it.
- **Cadence paragraph.** It now says the 2026-27 file changed twice in October (2026-10-03 and 2026-10-16).
- **Unchanged.** The missing-periods table ("2026-2027, through captured end: 6", total 70) is still true.

## Defects

- The stale-capture defect on the daily cost note is now fixed in the note (above). The checker's guess that the sibling volume
  note has the same pattern is still unchecked; it is outside this package.
- Registry `eligible` on all four packages, and manifest lists correct: unchanged from round 1.

Summary: I fixed all 10 nits on the four held Balancing costs pages and updated the daily cost note to its 16 October capture.
All four rebuild clean, with detector `[]`, identical mirrors and no layout problems at 390 or 1440.
