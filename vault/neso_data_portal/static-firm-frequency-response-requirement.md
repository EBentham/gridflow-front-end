---
source: "neso_data_portal"
package: "static-firm-frequency-response-requirement"
dataset_key: "sffr_requirement"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-18
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Static FFR requirement
  summary: >-
    NESO's forecast of the Static Firm Frequency Response it needs: MW for each of six EFA blocks
    per EFA date.
  facts:
    vendor: "NESO Data Portal, package `static-firm-frequency-response-requirement`: one CSV file, no archive"
    cadence: "Updated monthly (NESO's catalogue); SFFR is bought in a daily auction"
    grain: One row per EFA date, with six EFA block columns
  landscape: market
  what_it_is: >-
    Static Firm Frequency Response (SFFR) is a NESO frequency response service, bought in a daily
    auction. NESO's file, titled Static Firm Frequency Response Requirement, forecasts the MW
    needed before overholding per EFA date for six EFA blocks, updated monthly. Blocks run
    on the UK clock from 23:00 the evening before; block 1 lasts 3 or 5 hours at clock changes.
  how_used:
    - Requirement per block against cleared SFFR MW in NESO's daily auction results.
    - Join those results on EFA date and block number (`efa`), not on `timestamp_utc`.
    - "Point-in-time studies: each capture is one vintage, stamped with the file's `published_at`."
  chart:
    type: line
    silver: neso_data_portal/sffr_requirement
    time: efa_date
    value: efa1
    group: service
    series_order: [SFFR]
    filter:
      - {column: published_at, op: eq, value: "2026-09-22T14:48:22.737387"}
    aggregation: mean
    window: {start: "2026-09-23", end: "2026-10-31"}
    unit: MW
  chart_view:
    title: Static FFR requirement in EFA block 1, by date
    caption: >-
      Silver `sffr_requirement`, MW before overholding: EFA block 1 (from 23:00 the evening before,
      UK time) per EFA date, 23 September to 31 October 2026, NESO's 22 September file. Every block
      on every date in the file is 250 MW.
    alt: >-
      Line chart of NESO's Static Firm Frequency Response requirement for EFA block 1 in MW, one
      point per EFA date from 23 September to 31 October 2026. The line is flat at 250 MW across
      all 39 dates. Every block on every date in the file is also 250 MW.
    x_label: EFA date
    y_min: 0
    key:
      - {series: SFFR, label: Static FFR, codes: SFFR, paint: petrol, note: "250 MW in every block on all 39 dates in this file."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the file downloaded whole unless its
      `last_modified` is unchanged. Dates select nothing.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=static-firm-frequency-response-requirement"
      - "GET https://api.neso.energy/dataset/1f641071-ffc1-4fca-b83e-2c30772530a3/resource/bf236101-7167-4351-9fa0-c0b2e7c85747/download/sffr-data.csv"
    commands:
      - {run: gridflow ingest neso_data_portal sffr_requirement --last 24h, comment: "whole file; window must end recently"}
      - {run: gridflow transform neso_data_portal sffr_requirement --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: published_at, op: eq, value: "2026-09-22T14:48:22.737387"}
        - {column: efa_date, op: in, value: ["2026-09-23", "2026-09-24", "2026-10-24", "2026-10-25", "2026-10-26", "2026-10-27", "2026-10-30", "2026-10-31"]}
      order_by: [efa_date]
      columns: [efa_date, service, efa1, efa2, efa3, efa4, efa5, efa6, timestamp_utc, published_at]
    key: [efa_date]
    caption: "First, last and clock-change dates; from 26 October `timestamp_utc` is 00:00 UTC, not 23:00."
    fields:
      efa_date: EFA date of the requirement; block 1 starts 23:00 UK time the evening before
      service: "`SFFR`, Static Firm Frequency Response, on every row of this file"
      efa1: Block 1, 23:00 to 03:00 UK time, MW before overholding (NESO)
      efa2: Block 2, 03:00 to 07:00 UK time, MW before overholding (NESO)
      efa3: Block 3, 07:00 to 11:00 UK time, MW before overholding (NESO)
      efa4: Block 4, 11:00 to 15:00 UK time, MW before overholding (NESO)
      efa5: Block 5, 15:00 to 19:00 UK time, MW before overholding (NESO)
      efa6: Block 6, 19:00 to 23:00 UK time, MW before overholding (NESO)
      timestamp_utc: Calendar date `efa_date` at UK midnight, in UTC; block 1 begins an hour before
      published_at: "NESO's last-modified time for the whole file, read as UTC"
      bronze_capture_id: Path of the bronze capture the row was read from
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      Reads the `_latest` view, the newest capture, with `data.sql` so the cells see every date the
      file holds and show `published_at` in UTC; `query()` reads the same view but takes a date range.
    cells:
      - |
        df = data.sql("""
            SELECT efa_date, service, efa1, efa2, efa3, efa4, efa5, efa6,
                   published_at AT TIME ZONE 'UTC' AS published_utc
            FROM silver_neso_data_portal_sffr_requirement_latest
            ORDER BY efa_date""")
        df.groupby("service").agg(
            first=("efa_date", "min"), last=("efa_date", "max"),
            dates=("efa_date", "count"), published_utc=("published_utc", "max")).reset_index()
      - |
        blocks = [f"efa{i}" for i in range(1, 7)]
        long = df.melt(["efa_date", "service"], blocks, var_name="block", value_name="mw")
        long.groupby("block").mw.agg(["min", "max", "count"]).reset_index()
      - |
        import pandas as pd
        n = long.block.str[3:].astype(int)
        local = long.efa_date + pd.to_timedelta(4 * n - 5, unit="h")
        long["start_utc"] = local.dt.tz_localize("Europe/London").dt.tz_convert("UTC")
        long = long.sort_values("start_utc")
        long["hours"] = long.start_utc.diff().shift(-1).dt.total_seconds() / 3600
        long[long.efa_date.eq("2026-10-25")][["efa_date", "block", "start_utc", "hours", "mw"]]
      - |
        long.set_index("start_utc").mw.plot(
            drawstyle="steps-post", color="#155A6E", lw=2, ylim=(0, 300), figsize=(8, 3.5),
            xlabel="EFA block start, UTC", ylabel="requirement, MW");
    needs: a capture of the requirement file
    plot_alt: >-
      Step plot of NESO's Static FFR requirement in MW at each EFA block start in UTC, from 22:00
      on 22 September to 19:00 on 31 October 2026. The line holds 250 MW throughout.
  related:
    - {dataset: neso_data_portal/static-firm-frequency-response-auction-results, note: "Cleared SFFR MW and clearing price for each EFA date and block"}
    - {dataset: neso_data_portal/dynamic-regulation-requirements, note: "The same EFA block layout, for low and high Dynamic Regulation"}
    - {dataset: neso_data_portal/dynamic-moderation-requirements, note: "The same EFA block layout, for low and high Dynamic Moderation"}
    - {dataset: elexon/freq, note: The system frequency Static FFR responds to}
---

# Static Firm Frequency Response Requirement

This package is NESO's **Static Firm Frequency Response Requirement** table: NESO's forecast of how much
**Static Firm Frequency Response (SFFR)** capacity it needs, per EFA block, for each upcoming EFA date. The
CKAN notes say the dataset "will contain our forecasted requirements for Static Firm Frequency Response",
and the resource description says it will contain the forecasted requirements for Static FFR. SFFR is one of
NESO's frequency-response ancillary services; this table is the demand side (how many MW NESO wants to
procure), not auction results or delivery. The auction outcomes live in the sibling package
@./static-firm-frequency-response-auction-results.md. Background on the half-hour grid the EFA blocks sit on:
@../../../20-domain/concepts/settlement-period.md. `TODO: verify` how the requirement relates to SFFR
auction clearing; this page makes no such claim.

Each row is one **EFA date** with one **service** label (`SFFR`). The six EFA blocks of the day are kept
**wide**, as six value columns `efa1` to `efa6`. The vendor dictionary states that each value is NESO's
requirement "for the service (before overholding) for this EFA", in **MW**. These are **requirements, not
settlement accounting runs**: no `run_type` applies and none is fabricated (RULINGS 707).

**The silver output is eligible and not held.** Single capture, 39 rows, all 39 target dates after the
vintage, zero validation failures (see Bronze capture and Holds).

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: FC
- Package page: [Static Firm Frequency Response Requirement](https://www.neso.energy/data-portal/static-firm-frequency-response-requirement)
  (CKAN package name `static-firm-frequency-response-requirement`, id `1f641071-ffc1-4fca-b83e-2c30772530a3`;
  tags: Day-Ahead, Day-ahead Auction, Requirement, SFFR, Static FFR, Subscribable)
- Attribution: Supported by National Energy SO Open Data

## Files by disposition

The package has **one resource**, an uploaded CSV: **1 SILVER, 0 DOC, 0 HOLD**. There are **no DOC files,
so there are no document downloads**. The resource is fetched from its upload URL:

- [Static Firm Frequency Response Requirement](https://api.neso.energy/dataset/1f641071-ffc1-4fca-b83e-2c30772530a3/resource/bf236101-7167-4351-9fa0-c0b2e7c85747/download/sffr-data.csv)
  · CSV · resource id `bf236101-7167-4351-9fa0-c0b2e7c85747` · filename `sffr-data.csv` · `url_type` upload ·
  CKAN `last_modified` 2026-09-22T14:48:22.737387 (identical in the 2026-10-06 catalogue snapshot
  `20261006T195819Z` and in the capture sidecar `request_params.ckan_last_modified`). The CKAN resource
  declares no byte size or hash. The resource is `datastore_active`; gridflow captures the upload file, not
  the datastore.

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Static Firm Frequency Response Requirement | CSV | upload | `bf236101-7167-4351-9fa0-c0b2e7c85747` |

## Families

### `sffr_requirement`

- Kind: tabular · archetype: FC · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| EFA_DATE | `efa_date` | date | `%d/%m/%Y` | no | — | — |
| Service | `service` | string | — | yes | — | — |
| EFA1 | `efa1` | float64 | — | yes | — | MW |
| EFA2 | `efa2` | float64 | — | yes | — | MW |
| EFA3 | `efa3` | float64 | — | yes | — | MW |
| EFA4 | `efa4` | float64 | — | yes | — | MW |
| EFA5 | `efa5` | float64 | — | yes | — | MW |
| EFA6 | `efa6` | float64 | — | yes | — | MW |

- Entity key: `efa_date`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`efa_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What it is.** One row per EFA date. The capture has 39 consecutive EFA dates, 2026-09-23 to 2026-10-31,
each with exactly one row whose `Service` is `SFFR`. `efa_date` is unique in the capture (39 distinct keys)
and is the registry key. No vendor guarantee of a primary key or of revision identity was found, so the key
is a measured property of one capture, not a vendor contract (`TODO: verify` vendor uniqueness and revision
identity). `service` is registered nullable, but it is `SFFR` on every captured row.

**Vendor dictionary** (CKAN resource field info, snapshot `20261006T195819Z`, as read in the batch research,
@.planning/phases/v0.22-K-AS-2/K-AS-2-FACTS.md in the gridflow checkout):

| Column | Vendor title and description | Vendor unit |
|---|---|---|
| `EFA_DATE` | "EFA DATE": "The EFA DATE that the sFFR requirement volume is for."; comment "EFA Date starts at 23:00 D-1 running through to 23:00"; example `01/04/2023` | none |
| `Service` | "Service": "The ancillary service that the requirement applies to. SFFR = Static Firm Frequency Response"; example `SFFR` | none |
| `EFA1` to `EFA6` | "EFA 1" to "EFA 6": "Our requirement for the service (before overholding) for this EFA"; example `250` | MW |

**Units.** Only from the vendor dictionary above: every `EFA1` to `EFA6` column is **MW**, and each is a
requirement **before overholding**. Nothing is converted and no unit is inferred from a column name.
`EFA_DATE` and `Service` carry no unit.

**Sentinels and lexical rules** (FACTS g5). The body is read with strict UTF-8, no trimming and no null-token
map. Across the captured body there are no blank cells, no `-1`, `NA` or `N/A` tokens, no padded cells, no
thousands separators, no percentage signs and no zero runs; strict date and numeric casts pass and a faithful
second parse agrees cell for cell. A blank numeric cell would become null, never zero, and a zero would stay
zero (none occurs in this capture). The body carries a leading **UTF-8 BOM** and CRLF line endings; the
existing CSV reader handles both and the first header is read as `EFA_DATE`.

**Clocks.** Two clocks, stated separately:

- **Vintage.** The record's vintage is `ckan_last_modified`: `available_at` equals `published_at`, which is
  the CKAN `last_modified` of the captured upload (2026-09-22T14:48:22.737387, read as UTC, ADR-030/ADR-035).
  Every row of the capture carries that same instant. The body has **no issue or production column** (`issue:
  none`): there is no per-row publication time, so the vintage is the file's last-modified, not a
  per-requirement issue time.
- **Event time.** `date_sp1(efa_date)`: `timestamp_utc` and `event_time` are the start of settlement period 1
  of `efa_date`, that is Europe/London midnight of the EFA date, converted to UTC (silver: `efa_date`
  2026-09-23 gives 2026-09-22T23:00:00Z; 2026-09-24 gives 2026-09-23T23:00:00Z). This is a **date-label
  anchor**, not the start of EFA block 1 and not the start of any block: the vendor comment says an EFA date
  starts at 23:00 on D-1, and the blocks run on the UK local clock. The engine cannot compose a date plus
  block label into a row-specific instant (RULINGS 572/588, 720), so the six blocks stay wide and no block
  start is derived. The block boundaries used in the batch research are the AS-1 EFA definition (EFA 1 from
  23:00 on the previous date to 03:00, then 03:00-07:00, 07:00-11:00, 11:00-15:00, 15:00-19:00, 19:00-23:00,
  all local time); gridflow does not apply them to any column. NESO's own SFFR auction results confirm
  those boundaries for this service: `delivery_start` and `delivery_end` per `efa` run 23:00 on the
  previous date to 03:00, then four-hour blocks to 23:00, on the UK local wall clock, unchanged on the
  clock-change dates 2025-03-30, 2025-10-26 and 2026-03-29 (silver `sffr_auction_results_main`, capture
  published 2026-10-16, read 2026-10-18). NESO's EAC guidance itself was not read; SFFR is not an EAC
  product. The date format is `%d/%m/%Y` (day first;
  confirmed in the body, e.g. `23/09/2026`).

**Whole-capture semantics.** `latest` is `whole_capture`: each capture is a replacement view of the table.
The vendor describes the dataset as forecasted requirements with a monthly update frequency, which is
consistent with replacement semantics, but only one capture exists, so amendment-in-place and
dropped-target behaviour are not measured (`TODO: verify`).

**Forward-target property.** In the one capture, all 39 delivery dates and all 234 operational EFA block
starts (39 rows times 6 blocks) are after the vintage (0 on or before), so the table passes the
forward-target check (RULINGS 529) in that capture. The observed horizon is 1 through 39 days after the
vintage. That is a measurement of one capture and must not be generalised.

**Value shape.** Every EFA value in the single capture is `250` (MW), for all six blocks of all 39 dates;
the vendor example is also `250`. This is one capture's observation, not a vendor limit or a fixed level
(`TODO: verify` whether the requirement varies by block or date in other captures).

## Bronze capture

One capture exists (2026-10-08), so there is no capture-pair history. The measured bronze body:

| Item | Value |
|---|---|
| Bronze file | `C:/gridflow-data/bronze/neso_data_portal/sffr_requirement/2026/10/08/raw_20261008T111740Z_bf236101-7167-4351-9fa0-c0b2e7c85747_151d3950.csv` |
| Format | CSV, strict UTF-8 with BOM, CRLF, header as the vendor column list above |
| Size and rows | 1,650 bytes · 39 data rows (matches `declared_content_length`) |
| SHA-256 | `151d39502f04b3d15e82dd658ebe932353a2dfe572555d818aceff3f9ed60727` (matches the sidecar) |
| Sidecar `fetched_at` | `2026-10-08T11:17:40.962084+00:00` |
| Sidecar `written_at` | `2026-10-08T11:17:40.964081+00:00` |
| Empty-capture marker | false |

The vintage is the CKAN `last_modified` (2026-09-22T14:48:22.737387), not the capture time: the file was
captured about 16 days after NESO last modified it.

Silver lives at `C:/gridflow-data/silver/neso_data_portal/sffr_requirement/year=2026/month=10/` (partitioned
by capture month), one Parquet file for this capture with **39 rows**. System columns: `timestamp_utc`,
`published_at`, `available_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `source_run_id`,
`dataset_version`.

Activation (RULINGS 731, 2026-10-13): the transform for `--start/--end 2026-10-08`, with no prior silver,
gave 39 rows for this family, equal to the plan (batch total 241,160 rows over 11 families). The reconcile
run over all families (cutoff 2026-10-12) exited 0 with 170 families, 0 gaps, 47 adjudicated and 0 stale;
none of the adjudications concerns this package. Merge: PR #113, `fccbdeb` (RULINGS 730).

## Cadence

- Registry refresh: monthly
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Monthly

The vendor states a monthly update frequency; the real rate of change is not measured from one capture. No
rate limit or pagination for the upload download was found in the documentation read: `TODO: verify`.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence). gridflow
outputs derived from this package carry the attribution line above.

## Holds

- none

The `sffr_requirement` output is not held. Open items that do not hold the output but limit what can be
claimed:

- `TODO: verify` original issue instants and whether published values can be amended after publication
  (FACTS TODO SFFR-REQUIREMENT-ISSUE / IMMUTABILITY). Settle with vendor publication or revision evidence, or
  with capture history. Consequence: the upload vintage is kept; the measured all-forward capture stays
  eligible.
- `TODO: verify` amendment-in-place and dropped-target behaviour across captures: with one capture, whether
  NESO changes a published requirement or removes a target date is unmeasured. Settle by comparing later
  complete captures with the hash-pinned body above.
- `TODO: verify` vendor uniqueness and revision identity for `efa_date`.
- `TODO: verify` whether "before overholding" needs any adjustment before comparing these figures with
  procured volumes; this page makes no such claim.
- `TODO: verify` the empty-publication behaviour of this resource (FACTS EMPTY-PUBLICATION): a populated
  capture does not settle it, and the family is registered `empty allowed: no`.

## Gotchas

- **The temporal anchor is not an EFA block start.** `event_time` is local midnight of the EFA date. EFA 1
  starts at 23:00 local time on the previous calendar date, so joining on `event_time` as if it were the
  start of block 1 is wrong. Use `efa_date` and the wide block columns.
- **Wide blocks, no per-block clock.** `efa1` to `efa6` are separate columns of one row; there is no
  row-specific instant per block. EFA blocks follow the UK local clock, so DST days are not 24 hours: do not
  assume equal block lengths.
- **Point-in-time use.** Select with `available_at <= :as_of`. Because `available_at` is the file's CKAN
  last-modified, a later capture of an amended table carries a later vintage; do not backdate it.
- **Day-first dates.** `EFA_DATE` is `dd/mm/yyyy` (`%d/%m/%Y`).
- **Same wide form as the AS-1 requirement tables.** The DM and DR requirement tables
  (@./dynamic-moderation-requirements.md, @./dynamic-regulation-requirements.md) use the same
  `EFA_DATE` plus `EFA1`-`EFA6` shape, but they carry one row per service code per date; this table has a
  single `SFFR` service, so the key is `efa_date` alone.
- **Not the auction results.** The requirement is not the buy curve or the cleared volume; those are the
  separate families in @./static-firm-frequency-response-auction-results.md, which have their own keys and
  holds.
- **No `run_type`.** The package has no settlement-run dimension; none is fabricated.

## Modelling notes

A forward look at NESO's forecast SFFR requirement per EFA date and EFA block, for comparison with procured
volumes once those are in scope. Use the whole capture as one point-in-time vintage and join on `efa_date`
plus the block column, not on `event_time`. Because the table is replaced in place, a history of how the
requirement changed needs several captures over time; the registry refresh is `monthly`, matching the
vendor's stated update frequency. See @../../../20-domain/concepts/settlement-period.md for the half-hour
grid behind the `date_sp1` anchor.

## Links

- Package page: [Static Firm Frequency Response Requirement](https://www.neso.energy/data-portal/static-firm-frequency-response-requirement)
- Resource page: [Static Firm Frequency Response Requirement](https://www.neso.energy/data-portal/static-firm-frequency-response-requirement/static_firm_frequency_response_requirement)
- Upload: [sffr-data.csv](https://api.neso.energy/dataset/1f641071-ffc1-4fca-b83e-2c30772530a3/resource/bf236101-7167-4351-9fa0-c0b2e7c85747/download/sffr-data.csv)
- Licence: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence)
- Registry record: `src/gridflow/connectors/neso_data_portal/registry/static-firm-frequency-response-requirement.json` (gridflow checkout)
- Eligibility report: `docs/neso_data_portal/eligibility.md` (gridflow checkout)
- Batch evidence: @.planning/phases/v0.22-K-AS-2/K-AS-2-FACTS.md, @.planning/phases/v0.22-K-AS-2/K-AS-2-SPEC.md and @.planning/v0.22-RESULTS.md (gridflow checkout)
- Sibling packages: @./static-firm-frequency-response-auction-results.md, @./dynamic-moderation-requirements.md, @./dynamic-regulation-requirements.md
- Domain: @../../../20-domain/concepts/settlement-period.md
