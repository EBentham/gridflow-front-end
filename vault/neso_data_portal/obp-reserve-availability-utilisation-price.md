---
source: "neso_data_portal"
package: "obp-reserve-availability-utilisation-price"
dataset_key: "obp_reserve_avail_price"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: OBP reserve availability and prices
  summary: >-
    MW non-BM units declared available for Quick and Slow Reserve on NESO's Open Balancing Platform
    (OBP), per half-hour, with a utilisation price.
  facts:
    vendor: "NESO Data Portal: one CSV, republished under a new file name"
    cadence: "Ad hoc, NESO says, and published through the day"
    grain: "One row per unit, half-hour window, service and `pair_id`"
  landscape: market
  what_it_is: >-
    Non-BM providers declare to OBP, per half-hour window, the MW a unit has available for a
    reserve service at gate closure and a utilisation price in £/MWh. NESO publishes them once OBP
    has accepted and validated them. `pair_id` +1 marks a positive service, -1 a negative one.
    Times are UTC, NESO says; the text has no zone marker.
  how_used:
    - Reserve MW offered per half-hour, by unit and service
    - The utilisation price stack per window, next to OBP's instructed prices
    - Which non-BM units offer reserve, and when they declare zero MW
  chart:
    type: line
    silver: neso_data_portal/obp_reserve_avail_price
    time: time_from
    value: utilisation_price
    filter:
      - {column: availability_power, op: gt, value: 0}
    dedup: {on: [unit_id, time_from, pair_id, service_id], order_by: published_at}
    group: service_id
    group_map: {PSR: slow, PQR: quick, NQR: negative}
    series_order: [slow, quick, negative]
    aggregation: mean
    time_bucket: 1d
    window: {start: "2026-07-01", end: "2026-10-15"}
    unit: £/MWh
  chart_view:
    title: Mean utilisation price offered per day, by service
    caption: >-
      Silver `neso_data_portal/obp_reserve_avail_price`, mean `utilisation_price` per UTC day over
      every unit's half-hours with MW above zero, unweighted by MW, £/MWh, 1 July to 15 October
      2026. NESO states no sign.
    alt: >-
      Line chart from neso_data_portal/obp_reserve_avail_price of the mean utilisation price offered
      per UTC day by service, 1 July to 15 October 2026, in £/MWh. Positive Slow Reserve runs from 171.48
      on 4 July to 322.33 on 18 July, and 237.19 to 279.08 from September. Positive Quick Reserve stays between
      200.12 and 240: 240 on 11 days in mid-July, 203.25 to 208.38 from 2 August to 29 September,
      about 220 after. Negative Quick Reserve is 300 on 14 days from 13 to 28 July, otherwise 154.29
      to 287.14.
    x_label: UTC day of the window start
    key:
      - {series: slow, label: Positive Slow Reserve, codes: PSR, paint: olive, note: "171.48 to 322.33 in July, a few high offers lifting 18 July; 237.19 to 279.08 from September."}
      - {series: quick, label: Positive Quick Reserve, codes: PQR, paint: petrol, note: "200.12 to 240; 240 on 11 days between 13 and 28 July."}
      - {series: negative, label: Negative Quick Reserve, codes: NQR, paint: clay, note: "300 on 14 days between 13 and 28 July; otherwise 154.29 to 287.14."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then the one CSV downloaded whole unless its
      `last_modified` is unchanged. The file name changes with each publication.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=obp-reserve-availability-utilisation-price"
      - "GET https://api.neso.energy/dataset/769ec53a-9940-4df3-a867-6fa62d483097/resource/6bfe7df0-60aa-462d-94cd-44ac0a4abb2c/download/av_20261016_46_qr_sr_nbm.csv"
    commands:
      - {run: gridflow ingest neso_data_portal obp_reserve_avail_price --last 24h, comment: "whole file; window must end recently"}
      - {run: gridflow transform neso_data_portal obp_reserve_avail_price --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: time_from, op: eq, value: "2026-10-14T17:00:00"}
        - {column: unit_id, op: in, value: [ENGQR-05, ENGQR-02, ENGQR-03, CRRH-01, DNNG-01, ENXC-01, HULL-01]}
      dedup: {on: [unit_id, time_from, pair_id, service_id], order_by: published_at}
      order_by: [service_id, unit_id]
      columns: [unit_id, service_id, utilisation_price, availability_power, pair_id, time_from, time_to,
                data]
    key: [unit_id, time_from, pair_id, service_id]
    caption: "Eight rows for the window from 17:00 UTC on 14 October 2026; `ENGQR-05` offers both directions."
    fields:
      unit_id: "The non-BM unit, as NESO registers it"
      service_id: "`PQR`, `NQR`, `PSR`: Positive Quick, Negative Quick, Positive Slow Reserve (NESO); no `NSR` here"
      pair_id: "The MW and price band: +1 for a positive service, -1 negative (NESO)"
      availability_power: "MW available for the service at gate closure for the window (NESO)"
      utilisation_price: "Utilisation price at gate closure for the window, £/MWh (NESO); no sign stated"
      time_from: "Window start, UTC (NESO); the file's text has no zone marker"
      time_to: "Window end, UTC; 30 minutes after `time_from` in these rows"
      data: "Type of data; NESO fixes it at `AV`"
      timestamp_utc: "Equals `time_from`, the window's UTC start"
      published_at: "The CSV's portal last-modified time, read as UTC; one per capture"
      bronze_capture_id: Path of the bronze capture the row was read from
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      Returns a pandas DataFrame from `silver_neso_data_portal_obp_reserve_avail_price_latest`, the
      newest capture, filtered on `timestamp_utc` (the window start), both ends included. Times come
      back in the session's zone; the query cell converts them to UTC. Prices reach ±10,000.
    cells:
      - |
        df = data.neso_data_portal.query(
            "obp_reserve_avail_price", "2025-10-09", "2026-10-16")
        for col in ["time_from", "time_to", "timestamp_utc"]:
            df[col] = df[col].dt.tz_convert("UTC")
        df = df.sort_values(["time_from", "service_id", "unit_id"])
      - |
        df.groupby("service_id").agg(pair_id=("pair_id", "unique"),
            units=("unit_id", "nunique"), first=("time_from", "min"),
            top_mw=("availability_power", "max"),
            lowest_price=("utilisation_price", "min"),
            highest_price=("utilisation_price", "max")).reset_index()
      - |
        skipped = df[df.time_from.between("2026-03-29 00:30Z", "2026-03-29 02:00Z")]
        skipped.groupby("time_from").agg(rows=("unit_id", "size"),
            units=("unit_id", "nunique")).reset_index()
      - |
        day = df[df.time_from.between("2026-10-14 00:00Z", "2026-10-14 23:30Z")]
        mw = day.pivot_table(index="time_from", columns="service_id",
            values="availability_power", aggfunc="sum")
        ax = mw.plot(figsize=(8, 3.5), drawstyle="steps-post")
        ax.set(xlabel="window start, UTC, 14 October 2026", ylabel="MW available");
    needs: a capture of the OBP availability file from 16 October 2026 on
    plot_alt: >-
      Step plot of MW available per half-hour window, 14 October 2026 UTC, summed over units by
      service. `PSR` moves between 140 and 237 MW: 201 to 207 until 04:30, 177, 147 from 06:00, 237 from
      09:30 to 13:30, 140 from 14:00 to 19:30, then 155 to 173. `PQR` stays at 3 to 5 MW and `NQR`
      at 0 to 6.
  related:
    - {dataset: neso_data_portal/obp-non-bm-reserve-instructions, note: "Instructions NESO sent these units through OBP, with indicative prices"}
    - {dataset: neso_data_portal/obp-non-bm-physical-notifications, note: Physical notifications non-BM providers declare to OBP}
    - {dataset: neso_data_portal/quick-reserve-auction-requirement-forecast, note: "Quick Reserve MW NESO forecasts it needs, per half-hour window"}
    - {dataset: neso_data_portal/slow-reserve-requirement-forecast, note: "Slow Reserve MW NESO forecasts it needs, per half-hour window"}
---

# Open Balancing Platform (OBP) - Non-BM Reserve Availability MW and Utilisation Price

For each registered **non-BM** unit, this table says how many MW the provider had available for a
reserve service in a 30-minute UTC window, and the £/MWh price at which that capacity could be
used. The vendor describes it as Non-BM Quick Reserve and Slow Reserve availability and
utilisation-price data **declared by service providers, once the declarations have been accepted
and validated by the OBP system by gate closure**. It is published continuously through the day.
Non-BM here means units that are not Balancing Mechanism units: they take part through the Open
Balancing Platform instead (gridflow `@.planning/phases/v0.22-K-AS-3/K-AS-3-FACTS.md` §8). A row is
one unit, one window, one service and one price band. It is a **declaration at gate closure**, not
a metered delivery and not an instruction. Use it to see which reserve capacity and price levels
non-BM providers offered, and how the offered price stack moved over the year the file spans.
Pair it with the OBP instruction points (`@obp-non-bm-reserve-instructions.md`) and the physical
notification levels (`@obp-non-bm-physical-notifications.md`); the quick-reserve requirement
side is in `@quick-reserve-auction-requirement-forecast.md`. Point-in-time use needs the vintage
rule below (`@../../../20-domain/modelling/point-in-time-correctness.md`).

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT
- Attribution: **Supported by National Energy SO Open Data**

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Non-BM Reserve Availability MW and Utilisation Price | CSV | upload | `6bfe7df0-60aa-462d-94cd-44ac0a4abb2c` |

- The package has **one resource**, and it is the only one: no DOC, HOLD or other file. It
  feeds family `obp_reserve_avail_price`. CKAN datastore active; datastore unique keys declared by
  the vendor: `Unit ID`, `Time From`, `Service ID`.
- Download as listed in the 2026-10-06 catalogue snapshot:
  [av_20261006_44_qr_sr_nbm.csv](https://api.neso.energy/dataset/769ec53a-9940-4df3-a867-6fa62d483097/resource/6bfe7df0-60aa-462d-94cd-44ac0a4abb2c/download/av_20261006_44_qr_sr_nbm.csv)
  (CKAN `last_modified` 2026-10-06T19:31:32.248565 at that snapshot). The file name carries a date
  and a number (`20261006`, `44`) and changes with each publication, so the stable handle is the
  resource id, not the URL. No reviewed source documents the date or the `44` as an issue time
  (FACTS g2); `TODO: verify` what `44` denotes. Observed, not documented (2026-10-23): in both
  captures the number equals the UK settlement period of the file's last window, read as UTC
  (`av_20261008_27`: last `Time From` 12:00 UTC on 8 October, 13:00 BST, period 27;
  `av_20261016_46`: 21:30 UTC on 16 October, 22:30 BST, period 46).
- Captured: `raw_20261008T111500Z_6bfe7df0-60aa-462d-94cd-44ac0a4abb2c_70723223.csv`,
  10,215,008 bytes, 150,309 data rows, one header epoch, strict UTF-8, no BOM, LF line endings,
  no duplicate header (docs profile `@docs/neso_data_portal/profile/families/obp_reserve_avail_price.json`).
  Bronze written 2026-10-08T11:15:00.909612Z; CKAN `last_modified` of the captured file
  2026-10-08T11:01:23.882138.
- Captured again: `raw_20261016T204243Z_6bfe7df0-60aa-462d-94cd-44ac0a4abb2c_60f04f1d.csv`
  (file `av_20261016_46_qr_sr_nbm.csv`), 10,900,128 bytes, 160,395 data rows, ending in a newline.
  Bronze written 2026-10-16T20:42:43.203710Z; CKAN `last_modified` 2026-10-16T20:31:22.615360.
  Both captures are in silver; `_latest` reads the newest whole.

## Families

### `obp_reserve_avail_price`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Data | `data` | string | — | yes | — | — |
| Unit ID | `unit_id` | string | — | no | — | — |
| Time From | `time_from` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | UTC |
| Time To | `time_to` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | UTC |
| Pair ID | `pair_id` | int64 | — | no | — | — |
| Availability Power | `availability_power` | float64 | — | yes | — | MW |
| Utilisation Price | `utilisation_price` | float64 | — | yes | — | £/MWh |
| Service ID | `service_id` | string | — | no | — | — |

- Entity key: `unit_id`, `time_from`, `pair_id`, `service_id`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`time_from`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource, which CKAN emits without an offset and gridflow reads
   as UTC (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). For the first
   capture that is `2026-10-08T11:01:23.882138Z`, shared by all 150,309 of its rows
   (checked 2026-10-13); for the 16 October capture, `2026-10-16T20:31:22.615360Z` on all 160,395. The file has **no issue column**, and the record's issue recipe is
   `none`: no row carries its own declaration or publication time. The vintage is a conservative
   proxy, so no row is published earlier than it was truly available. It does **not** backdate:
   the original availability time of any row is `TODO: verify` (FACTS g2).
2. **Event time (`utc_instant` on `time_from`).** `timestamp_utc` = `event_time` = `time_from`,
   the UTC start of the 30-minute window, with no shift. Equality held on every silver row on
   2026-10-13. Event time is **not** the capture time. A BST-season `Time From` keeps its clock
   because the cells are already UTC. `time_to` is the window end and is kept as a data column.
   The rows support UTC over UK local time (checked 2026-10-23, 16 October capture): on 29 March
   2026, when UK clocks skipped 01:00 to 02:00, the file has windows starting 01:00 and 01:30
   (three rows each), and 26 October 2025 has 48 windows with no repeated key. No time cell in
   either capture carries a zone marker.

**Mixed horizon.** The capture spans `Time From` 2025-10-09T10:00:00 to 2026-10-08T12:00:00
(`Time To` 2025-10-09T10:30:00 to 2026-10-08T12:30:00), so about the 12 months before its
`last_modified`. Of the 150,309 rows, 150,237 start on or before the vintage and **72 start
after it**: those are declared positions for windows still ahead at the vintage instant. The
mixed history/future starts do not satisfy a forward-only forecast test, so the package is
admitted as a **gate-closure declaration / event table**, not as a forecast (FACTS §8, g2). Filter
`available_at <= :as_of` for point-in-time queries. Under `whole_capture`, history older than the
newest capture's window lives only in older captures, so a single capture is not a full archive.
Between the 8 and 16 October 2026 captures no declaration was revised or removed: all 150,309
earlier keys reappear with identical `time_to`, MW and price, the 10,086 new rows all start after
the earlier file's last window, and both files start at 2025-10-09T10:00:00, so the file did not
roll over those eight days (checked 2026-10-23). In the 16 October capture, 60 rows start after
its vintage (21:00 and 21:30 UTC). `TODO: verify` revision and retention over longer spans.

**Columns (vendor dictionary, cited in FACTS; nothing inferred from names).**

| Column | Vendor text | Silver treatment |
|---|---|---|
| `data` | Type of data; fixed value `AV` | string; `AV` in every row |
| `unit_id` | Registered unit ID. The vendor wording ("associated with the corresponding instruction") looks copied from the instructions dictionary | string, stored as-is, no normalisation; 60 distinct IDs in each capture |
| `time_from` / `time_to` | Window start / end datetime, unit UTC | tz-aware UTC datetimes, no shift |
| `pair_id` | Band specifying the MW and price. Comment: positive service `+1`, negative `-1` | int64, kept signed |
| `availability_power` | MW available for the service at gate closure for the window | float64, **MW** |
| `utilisation_price` | Utilisation price available for the service at gate closure for the window | float64, **£/MWh** |
| `service_id` | Name of the non-BM service; vendor examples `PQR, NQR, PSR, NSR` | string |

- **Units** come only from the vendor dictionary: MW for `availability_power`, £/MWh for
  `utilisation_price`. No MW-to-MWh or price-unit conversion is inferred from any other service
  (FACTS g4).
- **Service IDs in the 8 October capture:** `PQR` 58,384 rows, `NQR` 18,381, `PSR` 73,544 (16 October
  capture: `PQR` 60,000, `NQR` 18,877, `PSR` 81,518). `NSR` is a vendor example but is absent from
  both captures. This package's dictionary does not expand the codes; NESO's other reserve packages
  do (catalogue snapshot `20261006T195819Z`): `quick-reserve-auction-requirement-forecast`, "Quick
  Reserve, separated into Negative Quick Reserve (NQR) and Positive Quick Reserve (PQR)", and
  `slow-reserve-requirement-forecast`, "Slow Reserve, separated into Negative Slow Reserve (NSR) and
  Positive Slow Reserve (PSR)".
- **`pair_id` is a signed band, not a sentinel.** In the 8 October capture, `1` in 131,928 rows and `-1` in 18,381 rows.
  The `-1` count equals the `NQR` count, and `1` equals `PQR + PSR`, a measured coincidence
  with the vendor's positive/negative comment, not a documented rule. **`-1` is valid
  negative-service data and is never mapped to null** (FACTS T03, g5).
- **Sentinels and missing values (FACTS g5).** The record declares no null token. No NA tokens,
  percent-bearing numbers, comma numerals or padding were found. Zeros are real values and are
  kept: in the 8 October capture `availability_power` is 0 in 24,941 rows (longest zero run 4,622 in file order),
  `utilisation_price` is 0 in 115 rows (longest run 1). Negative prices are kept as published.
  Nulls in the capture: none in any column. No `min` / `max` bounds are imposed.
- **Value ranges in the capture (this eligible family only):** `availability_power` 0 to 55 MW;
  `utilisation_price` -10000 to 10000 £/MWh. The extremes are **not** reclassified as sentinels
  or caps. `TODO: verify` whether the vendor documents a price cap or floor. In the 16 October
  capture both extremes sit only on 0 MW rows of `EDFE-11` and `EDFE-8`, in windows from 18 to
  25 November 2025 (`NQR` -10000 on 75 rows, `PQR` 10000 on 37).
- **Against the OBP instructions (project check, 2026-10-23).** 21 of the 24 instructed units
  appear here; the three that do not are the RDP units. Of 85 instruction STARTs, 74 find a row
  here for the same unit, service and half-hour window, both read as UTC, and all 74 have
  `target_price` equal to `utilisation_price`. That fits one clock for both files and an
  instruction priced at the declared utilisation price; NESO does not state either.
- **Window length** is 1,800 seconds in every row. `TODO: INTERVAL-CLOSURE`: no reviewed source
  states whether the window is closed or open at either end, so no interval convention is invented.
- **Identity.** The recommended entity key (`unit_id`, `time_from`, `pair_id`, `service_id`) is
  unique in the capture, as are `(unit_id, time_from, pair_id)` and
  `(unit_id, time_from, service_id)` separately (the vendor's own datastore key is
  `Unit ID, Time From, Service ID`). That is a duplicate guard: a repeated key fails as a
  duplicate-entity-key error. It does not prove revision identity, so `_latest` stays
  `whole_capture` and the newest capture replaces the previous one as a whole. Across the two
  captures to date every key kept its values (Mixed horizon above); longer-run identity is
  `TODO: verify`.

**Row count drift.** A later datastore field-info call (2026-10-08T13:22Z, about two hours after
the bronze write) reported 150,431 total records against 150,309 in the captured file, consistent
with continuous publication into an append-or-update datastore. The captured file is the
reference; `TODO: verify` whether the CSV download and the datastore are the same population.

**Activation (2026-10-13, master `638b427`, PR #115).** Transformed with `--start/--end
2026-10-08` (one capture, no prior silver, so nothing was overwritten): **150,309 silver rows**,
equal to the planned count and to the CSV row count, zero exclusions. The batch's reconcile
`--all --cutoff 2026-10-12` exited 0 with 191 families and 0 gaps (gridflow
`@.planning/v0.22-RESULTS.md` §AS-3b; RULINGS 751, 752).

Silver columns beyond the vendor columns: `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version` (all
timestamps tz-aware UTC; `dataset_version` `1+e1` = record version 1, epoch 1). One Parquet file
under `silver/neso_data_portal/obp_reserve_avail_price/year=2026/month=10/`.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc
- The resource description says the data is "continuously published throughout the day"; the
  "Ad hoc" label is the CKAN metadata value, and the two do not agree. The registry refreshes
  daily. `TODO: verify` the vendor's actual publication cadence and latency.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

## Holds

- none

This package has no held output. Its eligibility rests on the declaration / event-table reading
above, not on forecast semantics. Non-holding open questions, all `TODO: verify`: original
availability time and revision behaviour of declared rows over long spans, the file-name number,
longer-run cross-capture identity, interval closure, and any price cap. The service codes are
decoded in NESO's Quick and Slow Reserve forecast packages (Columns above), not in this package. Other packages in the same batch (the mock EAC and ORPS families) are held; their
holds do not affect this page.
