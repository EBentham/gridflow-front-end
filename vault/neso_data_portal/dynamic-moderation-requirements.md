---
source: "neso_data_portal"
package: "dynamic-moderation-requirements"
dataset_key: "dm_requirements"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-18
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Dynamic Moderation requirements
  summary: >-
    NESO's latest view of the Dynamic Moderation it needs: MW for the low and high products in
    each EFA block.
  facts:
    vendor: "NESO Data Portal, package `dynamic-moderation-requirements`: one CSV file, no archive"
    cadence: "Ad hoc (NESO's catalogue); NESO publishes updates in the same file"
    grain: One row per EFA date and service, with six EFA block columns
  landscape: market
  what_it_is: >-
    Dynamic Moderation is a NESO frequency response service, with a low (`DML`) and a high (`DMH`)
    product. NESO's file, titled Indicative DM Requirements and called its latest view, gives MW
    before overholding per EFA date for six EFA blocks. Blocks run on the UK clock from 23:00 the
    evening before; block 1 lasts 3 or 5 hours at clock changes.
  how_used:
    - Requirement per block against cleared `DML` and `DMH` MW in NESO's EAC results.
    - To join EAC results, convert each block's UK start time to UTC.
    - "Point-in-time studies: each capture is one vintage, stamped with the file's `published_at`."
  chart:
    type: line
    silver: neso_data_portal/dm_requirements
    time: efa_date
    value: efa1
    group: service
    series_order: [DMH, DML]
    filter:
      - {column: published_at, op: eq, value: "2026-09-22T14:48:12.082389"}
    aggregation: mean
    window: {start: "2026-09-23", end: "2026-10-31"}
    unit: MW
  chart_view:
    title: Dynamic Moderation requirement in EFA block 1, by date
    caption: >-
      Silver `dm_requirements`, MW before overholding: EFA block 1 (23:00 the evening before to
      03:00, UK time) for each EFA date, 23 September to 31 October 2026, from the file NESO last
      modified on 22 September 2026.
    alt: >-
      Line chart of NESO's Dynamic Moderation requirement for EFA block 1 in MW, one point per EFA
      date from 23 September to 31 October 2026. Both lines are flat across the 39 dates: the high
      product, DMH, at 570 MW and the low product, DML, at 530 MW.
    x_label: EFA date
    y_min: 0
    key:
      - {series: DMH, label: High product, codes: DMH, paint: petrol, note: "570 MW on all 39 dates here; every block repeats on every date in this file."}
      - {series: DML, label: Low product, codes: DML, paint: clay, note: "530 MW on all 39 dates here."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the file downloaded whole unless its
      `last_modified` is unchanged. Dates select nothing.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=dynamic-moderation-requirements"
      - "GET https://api.neso.energy/dataset/c6e7dc26-64c3-4651-a664-16a8512768ab/resource/2aae8747-776d-4fe5-af9c-adcf38f1af8a/download/dm-requirements.csv"
    commands:
      - {run: gridflow ingest neso_data_portal dm_requirements --last 24h, comment: "whole file; window must end recently"}
      - {run: gridflow transform neso_data_portal dm_requirements --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: published_at, op: eq, value: "2026-09-22T14:48:12.082389"}
        - {column: efa_date, op: in, value: ["2026-09-23", "2026-10-25", "2026-10-26", "2026-10-31"]}
      order_by: [efa_date, service]
      columns: [efa_date, service, efa1, efa2, efa3, efa4, efa5, efa6, timestamp_utc, published_at]
    key: [efa_date, service]
    caption: "First and last dates; around 25 October's clock change `timestamp_utc` goes from 23:00 to 00:00 UTC."
    fields:
      efa_date: EFA date of the requirement; block 1 starts 23:00 UK time the evening before
      service: "`DML` (low) or `DMH` (high); NESO's column dictionary lists Dynamic Regulation's `DR-L`, `DR-H`"
      efa1: Block 1, 23:00 to 03:00 UK time, MW before overholding (NESO)
      efa2: Block 2, 03:00 to 07:00 UK time, MW before overholding (NESO)
      efa3: Block 3, 07:00 to 11:00 UK time, MW before overholding (NESO)
      efa4: Block 4, 11:00 to 15:00 UK time, MW before overholding (NESO)
      efa5: Block 5, 15:00 to 19:00 UK time, MW before overholding (NESO)
      efa6: Block 6, 19:00 to 23:00 UK time, MW before overholding (NESO)
      timestamp_utc: UK midnight starting calendar date `efa_date`, in UTC; block 1 starts an hour earlier
      published_at: "NESO's last-modified time for the whole file, read as UTC"
      bronze_capture_id: Path of the bronze capture the row was read from
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      Reads with `data.sql` from the `_latest` view, the newest capture, because NESO updates the
      file in place and a dated `query()` on `efa_date` finds only the dates a capture holds.
    cells:
      - |
        df = data.sql("""
            SELECT efa_date, service, efa1, efa2, efa3, efa4, efa5, efa6,
                   published_at AT TIME ZONE 'UTC' AS published_utc
            FROM silver_neso_data_portal_dm_requirements_latest
            ORDER BY efa_date, service""")
        df.groupby("service").agg(
            first=("efa_date", "min"), last=("efa_date", "max"),
            dates=("efa_date", "count"), published_utc=("published_utc", "max"))
      - |
        blocks = [f"efa{i}" for i in range(1, 7)]
        df.drop_duplicates(["service", *blocks])[["service", *blocks]]
      - |
        first = df[df.efa_date == df.efa_date.min()].set_index("service")[blocks].T
        first.index = [b[3:] for b in blocks]
        ax = first.plot.bar(
            color=["#155A6E", "#C77E3C"], ylim=(0, 750), figsize=(8, 3.5), rot=0,
            xlabel="EFA block (1 opens 23:00 UK time the evening before)", ylabel="requirement, MW")
        ax.legend(title="service", loc="upper center", ncols=2);
    needs: a capture of the requirement file
    plot_alt: >-
      Bar plot of NESO's Dynamic Moderation requirement in MW for EFA blocks 1 to 6 of EFA date 23
      September 2026. High, DMH (petrol): 570 MW in blocks 1 and 6, 510 MW in blocks 2 to 5. Low,
      DML (clay): 530 MW in blocks 1, 4 and 6, 500 MW in blocks 2, 3 and 5.
  related:
    - {dataset: neso_data_portal/eac-auction-results, note: "Cleared `DML` and `DMH` MW and price for each EFA block"}
    - {dataset: neso_data_portal/dynamic-regulation-requirements, note: "The same requirement layout for Dynamic Regulation, `DRL` and `DRH`"}
    - {dataset: neso_data_portal/long-term-forecasts-for-dc-dm-dr-requirements, note: "NESO's twelve-month outlook for this service, as weights over bands"}
    - {dataset: elexon/freq, note: The system frequency Dynamic Moderation responds to}
---

# Dynamic Moderation Requirements

This package is NESO's **Dynamic Moderation Requirements** table: NESO's latest view of how much
**Dynamic Moderation (DM)** capacity it needs, per service direction and per EFA block, for each upcoming
EFA date. The CKAN notes say the dataset "will contain our forecasted requirements for Dynamic Moderation",
and the resource description says it is NESO's "latest view" of the requirement, with any update to the
requirement published in the same place. DM is one of the frequency-response ancillary services (with
Dynamic Containment and Dynamic Regulation); this table is the demand side of the service (how many MW NESO
wants to procure), not auction results or delivery. Background on the half-hour grid the EFA blocks sit on:
@../../../20-domain/concepts/settlement-period.md. `TODO: verify` how the requirement relates to EAC
auction clearing and to the sibling requirement tables; this page makes no such claim.

Each row is one **EFA date** and one **service code**: `DML` (the low product) or `DMH` (the high product).
The six EFA blocks of the day are kept **wide**, as six value columns `efa1` to `efa6`. The vendor
dictionary states that each value is NESO's requirement "for the service (before overholding) for this
EFA", in **MW**. These are **requirements, not settlement accounting runs**: no `run_type` applies and
none is fabricated (RULINGS 707).

**The silver output is eligible and not held.** Single capture, 78 rows, all 78 target dates after the
vintage, zero validation failures (see Bronze capture and Holds).

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: FC
- Package page: [Dynamic Moderation Requirements](https://www.neso.energy/data-portal/dynamic-moderation-requirements)
  (CKAN package name `dynamic-moderation-requirements`, id `c6e7dc26-64c3-4651-a664-16a8512768ab`;
  tags: Dynamic Moderation, Forecast, Requirments (sic), Subscribable)
- Attribution: Supported by National Energy SO Open Data

## Files by disposition

The package has **one resource**, an uploaded CSV: **1 SILVER, 0 DOC, 0 HOLD**. There are **no DOC
files, so there are no document downloads**. The resource is fetched from its upload URL:

- [Indicative DM Requirements](https://api.neso.energy/dataset/c6e7dc26-64c3-4651-a664-16a8512768ab/resource/2aae8747-776d-4fe5-af9c-adcf38f1af8a/download/dm-requirements.csv)
  · CSV · resource id `2aae8747-776d-4fe5-af9c-adcf38f1af8a` · filename `dm-requirements.csv` ·
  `url_type` upload · CKAN `last_modified` 2026-09-22T14:48:12.082389 (identical in the 2026-10-06
  catalogue snapshot `20261006T195819Z` and in the capture sidecar `request_params.ckan_last_modified`).
  The CKAN resource declares no byte size or hash.

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Indicative DM Requirements | CSV | upload | `2aae8747-776d-4fe5-af9c-adcf38f1af8a` |

## Families

### `dm_requirements`

- Kind: tabular · archetype: FC · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| EFA_DATE | `efa_date` | date | `%d/%m/%Y` | no | — | — |
| Service | `service` | string | — | no | — | — |
| EFA1 | `efa1` | float64 | — | yes | — | MW |
| EFA2 | `efa2` | float64 | — | yes | — | MW |
| EFA3 | `efa3` | float64 | — | yes | — | MW |
| EFA4 | `efa4` | float64 | — | yes | — | MW |
| EFA5 | `efa5` | float64 | — | yes | — | MW |
| EFA6 | `efa6` | float64 | — | yes | — | MW |

- Entity key: `efa_date`, `service`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`efa_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What it is.** One row per EFA date per service code. The capture has 39 EFA dates, 2026-09-23 to
2026-10-31, each with exactly one `DML` row and one `DMH` row (78 rows). `(efa_date, service)` is unique
in the capture (78 distinct keys, 0 duplicate excess, 0 full-row duplicates) and is the registry key. No
vendor guarantee of a primary key or of revision identity was found, so the key is a measured property of
one capture, not a vendor contract (`TODO: verify` vendor uniqueness and revision identity).

**Vendor dictionary** (CKAN resource field info, snapshot `20261006T195819Z`, as read in the batch
research, @.planning/phases/v0.22-K-AS-1/K-AS-1-FACTS.md in the gridflow checkout):

| Column | Vendor title and description | Vendor unit |
|---|---|---|
| `EFA_DATE` | "EFA Date": "EFA Date the requirement is for"; example `16/02/2022` | none |
| `Service` | "Service Type": text copied from the Dynamic Regulation dictionary (see Gotchas) | none |
| `EFA1` to `EFA6` | "EFA 1" to "EFA 6": "Our requirement for the service (before overholding) for this EFA" | MW |

**Units.** Only from the vendor dictionary above: every `EFA1` to `EFA6` column is **MW**, and each is a
requirement **before overholding**. Nothing is converted and no unit is inferred from a column name.
`EFA_DATE` and `Service` carry no unit.

**Sentinels and lexical rules.** The body is read with strict UTF-8, no trimming and no null-token map.
Across the captured body there are no blank cells, no `-1`, `N/A`, `NA`, `NULL`, `null` or `NaN` tokens,
no padded cells, no thousands separators and no percentage signs; no numeric parse failure occurs. A blank
numeric cell would become null, never zero, and a zero would stay zero (none occurs in this capture).
Dictionary text containing `NA` is metadata, not a body sentinel. The body carries a leading **UTF-8 BOM**
and CRLF line endings; the existing CSV reader handles both and the first header is read as `EFA_DATE`.

**Clocks.** Two clocks, stated separately:

- **Vintage.** The record's vintage is `ckan_last_modified`: `available_at` equals `published_at`, which is
  the CKAN `last_modified` of the captured upload (2026-09-22T14:48:12.082389, read as UTC, ADR-030/ADR-035).
  Every row of the capture carries that same instant. The body has **no issue or production column**
  (`issue: none`): there is no per-row publication time, so the vintage is the file's last-modified, not a
  per-forecast issue time.
- **Event time.** `date_sp1(efa_date)`: `timestamp_utc` and `event_time` are the start of settlement
  period 1 of `efa_date`, that is Europe/London midnight of the EFA date, converted to UTC (silver:
  `efa_date` 2026-09-23 gives 2026-09-22T23:00:00Z; 2026-10-31, after the clock change, gives
  2026-10-31T00:00:00Z). This is a **date-label anchor**, not the start of EFA block 1 and not the start of
  any block: an EFA day begins at 23:00 local time on the previous calendar date, and the six blocks run on
  the UK local clock. The engine cannot compose a date plus block label into a row-specific instant
  (RULINGS 572/588, 720), so the six blocks stay wide and no block start is derived. The EFA block
  boundaries are NESO's own: EFA 1 runs 23:00 local on the previous date to 03:00, then four-hour blocks
  to 23:00, so EFA 1 is 3 hours on the spring clock-change date and 5 on the autumn one (EAC explainer
  Appendix B; DC history dictionary; @.planning/phases/v0.22-K-AS-1/K-AS-1-FACTS.md §5.1). The date format
  is `%d/%m/%Y` (day first; confirmed in the body, e.g. `23/09/2026`).

**Whole-capture semantics.** `latest` is `whole_capture`: each capture is a replacement view of the table.
The vendor describes the resource as the "latest view" with updates published in place, which supports
replacement semantics, but only one capture exists, so amendment-in-place and dropped-target behaviour are
not measured (`TODO: verify`).

**Forward-target property.** In the one capture, all 78 target dates and all 468 EFA starts (78 rows times
6 blocks) are after the vintage, so the table passes the forward-target check (RULINGS 529) in that
capture. That is a measurement of one capture and must not be generalised.

**Value ranges.** From FACTS (§4.6), as measured in the single capture: `efa1` 530 to 570, `efa2` 500 to
510, `efa3` 500 to 510, `efa4` 510 to 530, `efa5` 500 to 510, `efa6` 530 to 570 (MW). The captured values
are whole numbers. Each service carries one block profile on all 39 dates of the capture (`DMH` 570,
510, 510, 510, 510, 570; `DML` 530, 500, 500, 530, 500, 530; silver, 2026-10-18). These are one
capture's observations, not vendor limits.

## Bronze capture

One capture exists (2026-10-08), so there is no capture-pair history. The measured bronze body:

| Item | Value |
|---|---|
| Bronze file | `C:/gridflow-data/bronze/neso_data_portal/dm_requirements/2026/10/08/raw_20261008T101004Z_2aae8747-776d-4fe5-af9c-adcf38f1af8a_a1deb27a.csv` |
| Format | CSV, strict UTF-8 with BOM, CRLF, header as the vendor column list above |
| Size and rows | 3,171 bytes · 78 data rows (matches `declared_content_length`) |
| SHA-256 | `a1deb27a6f9f0e4444ce2ec318c6aa27bc2956df50ff9f7af7ee36648409a14f` (matches the sidecar) |
| Sidecar `fetched_at` | `2026-10-08T10:10:04.984767+00:00` |
| Sidecar `written_at` | `2026-10-08T10:10:04.991898+00:00` |
| Empty-capture marker | false |

The vintage is the CKAN `last_modified` (2026-09-22T14:48:12.082389), not the capture time: the file was
captured about 15 days after NESO last modified it.

Silver lives at `C:/gridflow-data/silver/neso_data_portal/dm_requirements/year=2026/month=10/` (partitioned
by capture month), one Parquet file for this capture with **78 rows**. System columns: `timestamp_utc`,
`published_at`, `available_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `source_run_id`,
`dataset_version`.

Activation (RULINGS 725, 2026-10-13): the transform for `--start/--end 2026-10-08`, with no prior silver,
gave 78 rows for this family, equal to the plan (batch total 112,730 rows over 9 families, 0 validation
failures). The reconcile run over all families (cutoff 2026-10-12) exited 0 with 159 families, 0 gaps, 47
adjudicated and 0 stale; none of the adjudications concerns this package. Merge: PR #112, `7e3c023`
(RULINGS 723).

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

The vendor says only that updates to the requirement "will be published here", with no schedule. One
capture exists, so the real rate of change is not measured. No rate limit or pagination for the upload
download was found in the documentation read: `TODO: verify`.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence). gridflow
outputs derived from this package carry the attribution line above.

## Holds

- none

The `dm_requirements` output is not held. Open items that do not hold the output but limit what can be
claimed:

- `TODO: verify` amendment-in-place and dropped-target behaviour: with one capture per resource, whether
  NESO changes a published requirement or removes a target date between captures is unmeasured. Settle by
  comparing later complete captures with the hash-pinned body above.
- `TODO: verify` vendor uniqueness and revision identity for `(efa_date, service)`.
- `TODO: verify` the vendor `Service` dictionary text, which describes Dynamic Regulation (see Gotchas).
- `TODO: verify` whether "before overholding" needs any adjustment before comparing these figures with
  procured volumes; this page makes no such claim.

## Gotchas

- **The vendor `Service` dictionary describes DR, not DM.** The dictionary says "DR-L = Dynamic Regulation
  Low, DR-H = Dynamic Regulation High" with example `DR-L`, but the resource's own description identifies
  Dynamic Moderation, and the body carries `DML` and `DMH` (NESO's EAC guidance independently lists the
  DML/DMH and DRL/DRH product codes). The dictionary text was copied from the DR table. gridflow keeps the
  literal codes `DML` and `DMH` byte-equal and never relabels DM rows as DR; do not use the dictionary text
  to interpret `service`. The sibling @./dynamic-regulation-requirements.md carries `DRL` and `DRH`.
- **The temporal anchor is not an EFA block start.** `event_time` is local midnight of the EFA date. EFA 1
  starts at 23:00 local time on the previous date, so joining on `event_time` as if it were the start of
  block 1 is wrong. Use `efa_date` and the wide block columns.
- **Wide blocks, no per-block clock.** `efa1` to `efa6` are separate columns of one row; there is no
  row-specific instant per block. EFA blocks follow the UK local clock, so DST days are not 24 hours: do
  not assume equal block lengths.
- **Point-in-time use.** Select with `available_at <= :as_of`. Because `available_at` is the file's CKAN
  last-modified, a later capture of an amended table carries a later vintage; do not backdate it.
- **Day-first dates.** `EFA_DATE` is `dd/mm/yyyy` (`%d/%m/%Y`).
- **No `run_type`.** The package has no settlement-run dimension; none is fabricated.

## Modelling notes

A forward look at NESO's indicative DM requirement per EFA date, service direction (`DML`, `DMH`) and EFA
block, for comparison with procured volumes once those are in scope. Use the whole capture as one
point-in-time vintage and join on `efa_date` plus the block column, not on `event_time`. Because the table
is a latest view that is replaced in place, a history of how the requirement changed needs several captures
over time; ingest cadence is `adhoc`, so an additional capture schedule would be a later scope decision
(`TODO`). See @../../../20-domain/concepts/settlement-period.md for the half-hour grid behind the
`date_sp1` anchor.

## Links

- Package page: [Dynamic Moderation Requirements](https://www.neso.energy/data-portal/dynamic-moderation-requirements)
- Resource page: [Indicative DM Requirements](https://www.neso.energy/data-portal/dynamic-moderation-requirements/indicative_dm_requirements)
- Upload: [dm-requirements.csv](https://api.neso.energy/dataset/c6e7dc26-64c3-4651-a664-16a8512768ab/resource/2aae8747-776d-4fe5-af9c-adcf38f1af8a/download/dm-requirements.csv)
- EAC guidance cited by the batch research: [document 277671](https://www.neso.energy/document/277671/download)
- Licence: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence)
- Registry record: `src/gridflow/connectors/neso_data_portal/registry/dynamic-moderation-requirements.json` (gridflow checkout)
- Eligibility report: `docs/neso_data_portal/eligibility.md` (gridflow checkout)
- Batch evidence: @.planning/phases/v0.22-K-AS-1/K-AS-1-FACTS.md, @.planning/phases/v0.22-K-AS-1/K-AS-1-SPEC.md and @.planning/v0.22-RESULTS.md (gridflow checkout)
- Sibling package: @./dynamic-regulation-requirements.md
- Domain: @../../../20-domain/concepts/settlement-period.md
