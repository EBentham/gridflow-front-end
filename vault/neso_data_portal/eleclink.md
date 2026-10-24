---
source: "neso_data_portal"
package: "eleclink"
dataset_key: "eleclink"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: ElecLink transfer limits
  summary: >-
    NESO's hourly limits on flow each way over the ElecLink interconnector, in MW, with reasons.
  facts:
    vendor: "NESO Data Portal, package `eleclink`: a current datastore table and an archive CSV"
    cadence: "Daily, NESO says"
    grain: "Each row: one hour's import and export limits for one auction"
    history: "NESO's files label hours from 7 November 2022: archive, then the current table"
  landscape: power
  what_it_is: >-
    NESO says it submits these to interconnector capacity calculations, capping GB imports and
    exports, in hourly MW; final capacity can be lower. It says it publishes only restrictions,
    but its October 2026 files hold many No Restriction rows. NESO calls them Net Transfer
    Capacity (NTC) restrictions. Archive rows add an operational date and version.
  how_used:
    - Which hours NESO restricted the link, by direction, from the stated reason
    - "A feature for flow and price models: when NESO restricted the link"
    - Set beside the final capacity the link's trading facilitator publishes
  caveat: "NESO does not say rows stay as uploaded, or define the operational day or `Version`."
  chart:
    type: line
    silver: neso_data_portal/eleclink
    time: operational_period_start_gmt
    filter:
      - {column: auction_type, op: eq, value: Day Ahead}
    dedup: {on: [operational_period_start_gmt], order_by: capture_written_at}
    values:
      - {column: flow_to_gb_mw, series: to_gb}
      - {column: flow_from_gb_mw, series: from_gb}
    aggregation: min
    window: {start: "2026-10-09", end: "2026-10-15"}
    unit: MW
  chart_view:
    title: Day-ahead limits each way, 9 to 15 October 2026
    caption: >-
      Silver `eleclink` day-ahead rows, hourly, as fetched 16 October 2026; no row covers 12 October
      22:00 to 13 October 21:00 UTC. All say No Restriction; lines coincide. Each upload precedes its
      hour; NESO does not say rows are unchanged since.
    alt: >-
      Line chart from neso_data_portal/eleclink of NESO's day-ahead limits each way over ElecLink, MW,
      hourly, 9 to 15 October 2026, with no rows from 22:00 UTC on 12 October to 21:00 on 13 October.
      Both directions are 1,014 MW in every hour drawn, so the To GB line lies under From GB
      throughout.
    x_label: hour start, UTC (NESO labels it GMT)
    y_min: -40
    key:
      - {series: to_gb, label: To GB, note: "Import limit, NESO's `Flow in MW To GB`", paint: petrol}
      - {series: from_gb, label: From GB, note: "Export limit, NESO's `Flow in MW From GB`", paint: clay}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, the current table's dump and the archive CSV. Fetched
      16 October 2026, the table kept every row fetched 8 October unchanged, plus new ones.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=eleclink"
      - "GET https://api.neso.energy/datastore/dump/1f748d48-1daf-4f1a-a5f1-d581e86a2190"
      - "GET https://api.neso.energy/dataset/46daeb44-95a7-4032-8a22-914c896ed261/resource/991a79f8-2e8c-4f42-b308-e3fb0346700d/download/archived_eleclink_link_ntc_data.csv"
    commands:
      - {run: gridflow ingest neso_data_portal eleclink --last 24h, comment: "the dump and archive to bronze"}
      - {run: gridflow transform neso_data_portal eleclink --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: bronze_capture_id, op: eq, value: "bronze/neso_data_portal/eleclink/2026/10/16/raw_20261016T201759Z_1f748d48-1daf-4f1a-a5f1-d581e86a2190_cfed84ef.csv"}
        - {column: operational_period_start_gmt, op: ge, value: "2026-08-19T15:00:00Z"}
        - {column: operational_period_start_gmt, op: le, value: "2026-08-19T16:00:00Z"}
      order_by: [operational_period_start_gmt, auction_type]
      columns: [operational_period_start_gmt, auction_type, data_upload_time_gmt, flow_to_gb_mw,
                reason_for_restriction_to_gb, flow_from_gb_mw, reason_for_restriction_from_gb,
                operational_date, version, hourly_time_period, reason_for_restriction, issue_time,
                resource_id]
    key: [resource_id, issue_time, auction_type, operational_period_start_gmt, operational_date, hourly_time_period]
    caption: "Two hours of 19 August 2026, four auctions each; `Intraday 2` and `3` lower both limits."
    fields:
      operational_period_start_gmt: "Current table: start of the hour; header says GMT, read as UTC"
      auction_type: "The auction: `Day Ahead` or `Intraday 1` to `3`; the archive writes `DayAhead`, `Intraday1`"
      data_upload_time_gmt: "Current table: when NESO says the row was published; GMT, read as UTC"
      flow_to_gb_mw: "The most power that may flow into GB in the hour, MW"
      reason_for_restriction_to_gb: "Current table: NESO's reason for the import limit, or `No Restriction`"
      flow_from_gb_mw: "The most power that may flow out of GB in the hour, MW"
      reason_for_restriction_from_gb: "Current table: NESO's reason for the export limit, or `No Restriction`"
      operational_date: "Archive only: NESO's operational date, `YYYYMMDD`; NESO does not say when it starts"
      version: "Archive only: NESO's `Version`, `001` to `004`; NESO does not define it"
      hourly_time_period: "Archive only: the hour as NESO writes it, like `22:00 to 23:00`; headed GMT"
      reason_for_restriction: "Archive only: NESO's `Reason For Reduction`, one for both directions"
      issue_time: "A copy of the upload time; not taken as when the row first appeared"
      resource_id: "Which file the row came from: the current table or the archive"
      timestamp_utc: "When gridflow fetched the file, UTC; not the hour the limits apply to"
      published_at: "Null: neither file gives gridflow a publication time"
      bronze_capture_id: The bronze file the row was read from
      capture_written_at: When gridflow wrote the capture to bronze, UTC
  notebook:
    lead: >-
      `data.sql` reads `silver_neso_data_portal_eleclink_latest` (the newest capture of each file),
      because `query()` would filter `timestamp_utc`, the capture time. The first cell converts times
      to UTC.
    cells:
      - |
        df = data.sql("""
            SELECT operational_period_start_gmt, auction_type, data_upload_time_gmt,
                   flow_to_gb_mw, flow_from_gb_mw, reason_for_restriction_from_gb
            FROM silver_neso_data_portal_eleclink_latest
            WHERE operational_period_start_gmt >= TIMESTAMPTZ '2026-10-09 00:00:00+00'
              AND operational_period_start_gmt < TIMESTAMPTZ '2026-10-16 00:00:00+00'
            ORDER BY operational_period_start_gmt, auction_type""")
        for c in ["operational_period_start_gmt", "data_upload_time_gmt"]:
            df[c] = df[c].dt.tz_convert("UTC")
        df.head()
      - |
        data.sql("""
            SELECT version, auction_type, count(*) AS rows, count(DISTINCT operational_date) AS dates
            FROM silver_neso_data_portal_eleclink_latest
            WHERE operational_date IS NOT NULL
            GROUP BY version, auction_type ORDER BY version, auction_type""")
      - |
        wide = df.pivot(index="operational_period_start_gmt", columns="auction_type",
                        values="flow_from_gb_mw").asfreq("h")
        ax = wide.plot(drawstyle="steps-post", figsize=(8, 3.5), xlabel="hour start, UTC",
                       ylabel="export limit, MW")
        ax.legend(loc="lower left", bbox_to_anchor=(0, 1), ncols=4);
    needs: ElecLink's current table and archive
    plot_alt: >-
      Step plot, UTC, of NESO's ElecLink export limit by auction, 9 to 15 October 2026. Day Ahead is
      1,014 MW in every hour listed, broken from 22:00 on 12 October to 21:00 on 13 October. Intraday
      1 lists only 9 and 10 October: 0 in 16 hours, otherwise 90 to 1,014.
  related:
    - {dataset: neso_data_portal/ifa, note: "NESO's limits on IFA, another GB interconnector"}
    - {dataset: neso_data_portal/ifa2, note: "NESO's limits on IFA2, another GB interconnector"}
    - {dataset: entsoe/net_transfer_capacity, note: "ENTSO-E's forecast capacity across each GB border, all links together"}
    - {dataset: neso_data_portal/historic-demand-data, note: "ElecLink's half-hourly flow, in NESO's historic demand files"}
---

# ElecLink - NESO's Net Transfer Capacity

NESO's **directional transfer limits on the ElecLink interconnector** (GB–France), in MW
per hourly period. The package notes say these are the values NESO submits
to the interconnector capacity calculation processes, and they restrict the maximum GB import
and export flows. The resource description adds that they are submitted to the Day-ahead and
Intraday auctions. They are **limit submissions, not measured flows and not final capacity**:
the vendor notes that the final interconnector capacity also uses the connected system
operator's values and the interconnector capability, so it "may be lower than the NESO values
shown here". The package notes say NESO publishes a value only where it has applied a
restriction, so a missing row means NESO applied no restriction. It does not mean zero capacity,
so a consumer must never fill a gap with zero or a nameplate figure (K-IC-1-FACTS g5, IC1-6). The
files do not follow the notes literally (bronze read 2026-10-24): the archive lists 24 hours for
each operational date, auction and version, and gives the reason `No Restriction` on 3,120 of
8,472 rows; the 2026-10-16 current table gives `No Restriction` for flow to GB on 23,354 of 24,599
rows, from GB on 18,822, and in both directions on 18,429.

**Direction.** `To GB` is the foreign-to-GB **import** limit and `From GB` is the GB-to-foreign
**export** limit. Each is a separate directional MW maximum, not one signed net-flow series. Both
columns are populated on every row and no value is negative. gridflow keeps them as two
non-negative columns. Any signed or netted series would be a downstream convention with its own
definition (FACTS IC1-1).

The package holds two resources with different shapes in one family. The **current dump** (M
header) runs from late September 2024 and carries a publication timestamp per row. The
**archive upload** (A header) covers the earlier period with an operational-date label, a
version and an hourly GMT range. Both load under the single family `eleclink`, partitioned by
`resource_id` so that neither capture displaces the other (ADR-039).

**The output is held (unit E-SEM).** The dump also returns past targets, and NESO does not state
that a row is unchanged since its `Data Upload Time GMT`. The archive's Operational Date calendar
and Version meaning are also undocumented. See Holds. The output exists in silver, but it is not
eligible for point-in-time model use until E-SEM is answered (RULINGS 565, 567).
This note gives schema, clocks and row counts; under ruling 66 (2026-10-24) the site page shows the
rows, with one line naming the question.

Related: the sibling interconnector packages @ifa.md, @ifa2.md, @nemolink.md, @nsl.md and
@viking.md use the same column conventions. On the ENTSO-E side,
@../../entsoe/datasets/net_transfer_capacity.md is a France–GB border aggregate. A direct join
gave no exact per-link equality for ElecLink, so it cannot validate an individual link's limit
(FACTS IC1-1).

- Publisher group: Interconnectors
- Registry group: interconnectors · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Archived ElecLink NTC Data | CSV | upload | `991a79f8-2e8c-4f42-b308-e3fb0346700d` |
| ElecLink NTC Data | CSV | dump | `1f748d48-1daf-4f1a-a5f1-d581e86a2190` |

Both resources are SILVER and both feed family `eleclink`. The package has no DOC resources, so
it has no methodology document and no `_files` family. Package id
`46daeb44-95a7-4032-8a22-914c896ed261`. Vendor page:
[eleclink](https://www.neso.energy/data-portal/eleclink).

- **ElecLink NTC Data** (current, M header) -> `eleclink` (held).
  Download: [datastore dump](https://api.neso.energy/datastore/dump/1f748d48-1daf-4f1a-a5f1-d581e86a2190).
  CKAN `url_type` `datastore`, created `2024-09-23T10:50:17`. Captured (B1):
  `raw_20261008T103640Z_1f748d48-1daf-4f1a-a5f1-d581e86a2190_9c6446fc.csv`, 2,217,272 bytes,
  24,359 rows, CKAN `last_modified` `2026-09-17T08:45:57.592028`. Dictionary:
  [ElecLink NTC data](https://www.neso.energy/data-portal/eleclink/eleclink_ntc_data).
- **Archived ElecLink NTC Data** (archive, A header) -> `eleclink` (held).
  Download: [archived_eleclink_link_ntc_data.csv](https://api.neso.energy/dataset/46daeb44-95a7-4032-8a22-914c896ed261/resource/991a79f8-2e8c-4f42-b308-e3fb0346700d/download/archived_eleclink_link_ntc_data.csv).
  CKAN `url_type` `upload`, created `2024-11-27T14:34:11`. Captured (B2):
  `raw_20261008T103643Z_991a79f8-2e8c-4f42-b308-e3fb0346700d_c39f709e.csv`, 546,560 bytes,
  8,472 rows, CKAN `last_modified` `2024-11-27T14:34:10.857133`. Dictionary:
  [Archived ElecLink NTC data](https://www.neso.energy/data-portal/eleclink/archived_eleclink_ntc_data).

Both bodies are UTF-8 with no BOM, no all-blank rows and one header each. Body hashes and byte
lengths match their sidecars (FACTS C-VERIFY). The current resource's description records that
its column ids were renamed on **2026-09-17**:

| Before 2026-09-17 | From 2026-09-17 (captured) |
|---|---|
| `Data Upload Time (GMT)` | `Data Upload Time GMT` |
| `Operational Period Start Date & Time (GMT)` | `Operational Period Start Date and Time GMT` |
| `Flow (MW) To GB` | `Flow in MW To GB` |
| `Flow (MW) From GB` | `Flow in MW From GB` |

Only the post-rename header was captured, and the frozen record has no epoch for the
pre-rename dump header. No earlier M epoch is claimed (FACTS IC1-4). `TODO: verify` how the
engine treats a pre-rename body if one is ever captured.

## Families

### `eleclink`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Data Upload Time GMT | `data_upload_time_gmt` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | ISO 8601 |
| Auction Type | `auction_type` | string | — | yes | — | — |
| Operational Period Start Date and Time GMT | `operational_period_start_gmt` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | ISO 8601 |
| Flow in MW To GB | `flow_to_gb_mw` | float64 | — | yes | — | MW |
| Reason For Restriction To GB | `reason_for_restriction_to_gb` | string | — | yes | — | — |
| Flow in MW From GB | `flow_from_gb_mw` | float64 | — | yes | — | MW |
| Reason For Restriction From GB | `reason_for_restriction_from_gb` | string | — | yes | — | — |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Operational Date | `operational_date` | string | — | yes | — | — |
| Auction Type | `auction_type` | string | — | yes | — | — |
| Version | `version` | string | — | yes | — | — |
| Hourly Time Period (GMT) | `hourly_time_period` | string | — | yes | — | — |
| Flow (MW) To GB | `flow_to_gb_mw` | float64 | — | yes | — | — |
| Flow (MW) From GB | `flow_from_gb_mw` | float64 | — | yes | — | — |
| Reason For Reduction | `reason_for_restriction` | string | — | yes | — | — |

- Entity key: `resource_id`, `issue_time`, `auction_type`, `operational_period_start_gmt`, `operational_date`, `hourly_time_period`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

**Held (unit E-SEM).** This note gives schema, clocks and counts; the site page shows the rows with a caveat line (ruling 66, 2026-10-24).

**The two clocks for this family:**

1. **Vintage (`capture_fallback`, not `ckan_last_modified`).** This is a mixed family: it holds
   a datastore dump and an upload. Under ADR-035 the frozen record's vintage is
   `capture_fallback` (rule V-8), and the upload takes it as well. So on **every** row of both
   resources `published_at` is **null** and `available_at` is the capture's `written_at`:
   `2026-10-08T10:36:40.095321Z` for the dump and `2026-10-08T10:36:43.047166Z` for the archive.
   Each resource has one distinct value in silver. The CKAN `last_modified` of each capture
   (`2026-09-17T08:45:57.592028` for the dump, `2024-11-27T14:34:10.857133` for the archive) is
   kept in the bronze sidecar. It is **not** used as `available_at`. For the archive this is
   honest but later than the file actually became available (ADR-035 "Mixed families").
   `available_at` is **not** backdated to `Data Upload Time GMT` either (FACTS T09, g2).
2. **Event time (`none`).** The temporal recipe is `none`, so `timestamp_utc` and `event_time`
   are the **capture time**, equal to `available_at` on every row. **They are not the target
   hour.** The recipe is `none` because the current target column
   (`operational_period_start_gmt`) is absent from the archive epoch, and the engine requires a
   temporal input in every epoch (rule V-3, FACTS T07). A consumer must not read
   `timestamp_utc` as the hour a limit applies to. The target is:
   - **Current dump:** `operational_period_start_gmt`, a tz-aware UTC instant. The vendor
     defines it as the "Hourly Operational Period Start Datetime for which restriction applies",
     and the period runs one hour from that start. The clock is GMT by the dictionary title.
     Grouping distinct targets by UTC date gives 24 per day on 2025-10-26 and 2026-03-29, and
     grouping by Europe/London gives 25 and 23, which confirms UTC (FACTS T02, IC1-3).
   - **Archive:** `operational_date` + `hourly_time_period`, both kept as **raw strings**. Every
     `Operational Date` parses as `%Y%m%d`, but the archive dictionary does not define the field.
     Its operational-day calendar and rollover (how a `22:00`/`23:00` GMT range attaches to the
     labelled date) are undocumented, so no instant is built (FACTS T03, g1). The spring-DST
     label `20240331` has 24 distinct hourly ranges, which a UK-local civil day could not have.

**Issue clock (current dump only).** `issue_time` = `data_upload_time_gmt`, a UTC instant
(issue recipe `data_column`). The vendor defines it as the "Date and time that data was
published", in GMT. It is equal to `data_upload_time_gmt` on all 24,359 dump rows, with 1,015
distinct issue instants. Archive rows have no issue column, so `issue_time` is null there.
`Version` is not an issue time and carries no ordering (FACTS T04).

**Hold question.** The current dump returns past targets as well as future ones. 1,292 of its
24,359 rows have a target before their own `Data Upload Time GMT`, and 24,337 have a target
before the capture (2026-10-08 capture; 1,292 and 24,574 of 24,599 in the 2026-10-16 capture). NESO does not state that a row returned today is unchanged since its upload
time, so the dump does not evidence the limits as they were historically issued (FACTS g2,
IC1-6). The archive has no issue column, and every target label precedes its vintage, so the
forward-target rule (RULINGS 529) cannot release it. Its Operational Date calendar and rollover
and the meaning of `Version` are undocumented (FACTS T03, T04). `TODO: verify` with NESO (a) a
retention and revision guarantee for dump rows, or immutable per-issue files; (b) the archive
operational-date definition and rollover; (c) the `Version` contract and revision order.

**Shape of a capture (counts only).** 32,831 silver rows = 24,359 (dump) + 8,472 (archive).
Each Parquet file carries the union of both epochs' columns, and the other epoch's columns are
null on every row. Within an epoch the vendor columns have no nulls, except `reason_for_restriction`
(archive), which is null on 216 rows where the vendor cell was blank. A blank reason is kept as
null and no reason is invented (FACTS g5).

Measured coverage, as literal labels. These are coverage bounds, not data values:

| Resource | Target coverage |
|---|---|
| Archive | Operational Date + hour labels `2022-11-07 00:00` to `2024-09-24 23:00` |
| Current dump | `operational_period_start_gmt` `2024-09-25T22:00Z` to `2026-10-08T21:00Z` (to `2026-10-17T21:00Z` in the 2026-10-16 capture) |

The two resources share no target key, either literally or under a hypothetical previous-day
rollover of the `22:00`/`23:00` ranges. Canonical overlap stays `TODO: verify` until the archive
calendar is known (FACTS IC1-4).

**Auction labels.** The current dump uses `Day Ahead`, `Intraday 1`, `Intraday 2`, `Intraday 3`.
The archive uses `DayAhead`, `Intraday1`, `Intraday2`. The vendor dictionary describes the field
as "Day-ahead (DA) or Intraday (ID) auction". gridflow preserves the spellings byte for byte and
never whitespace-compacts them, so the two resources' labels are different strings. Mapping them
to each other is a consumer decision. `TODO: verify` that NESO intends them as the same auction
(FACTS IC1-2). Every interval is one hour. No body carries a weekly or long-term auction value.

**Units (vendor dictionary only).**
- **Current dump** (field info from the current dictionary): `Flow in MW To GB` and
  `Flow in MW From GB` are **MW**, described as "Maximum flow in this direction" (type `int4`).
  They are cast to float64, which leaves integer values unchanged. The two `Data Upload Time` /
  `Operational Period Start` fields carry unit `ISO 8601`. Auction and reason fields have no
  unit.
- **Archive:** the archived dictionary has a field entry for `Auction Type` only. It has none
  for `Operational Date`, `Version`, `Hourly Time Period (GMT)`, the two flow columns or
  `Reason For Reduction`, which is why the generated epoch-2 table shows no vendor unit. FACTS
  T05/T06 still establish the two archive flow columns as **MW** directional limits, from the
  vendor headers (`Flow (MW) To GB`, `Flow (MW) From GB`) and the package notes ("submitted in
  MW per hourly time period"). `Version` has no unit and is kept as a raw string. Its values are
  zero-padded labels such as `001`, so it is not typed as an integer.

**Sentinels and missing values (FACTS g5).** No null-token map is declared. Full-body scans of
both captures found no `N/A`, `NA`, literal `-1`, negative value, non-numeric value or blank
cell in either flow column. `N/A` strings in the dictionary examples are metadata, not CSV
sentinels. Both flow columns contain **zero** values in both resources. No vendor source defines
zero as missing, so zeros are kept as numeric zero and never converted to null or filled.
`TODO: verify` whether NESO means a zero limit as a full restriction in that direction. The
only blanks are the 216 archive reason cells, mapped to null. Absent rows mean "no NESO
restriction" (package notes) and are never synthesised. No bounds are imposed.

**Identity.** No vendor primary key is published for either resource (FACTS C-CATALOG). The
entity key is a completion guard over measured grain, not a vendor revision key. It is
`resource_id` plus the union of each epoch's grain:
- **Current:** `(issue_time, auction_type, operational_period_start_gmt)`. Measured unique on B1.
  `(auction_type, operational_period_start_gmt)` alone is not unique (duplicate excess 120),
  because a target can be re-issued.
- **Archive:** `(operational_date, auction_type, hourly_time_period)`. Measured unique on B2.

On each row the other epoch's key columns are null. `_latest` is `whole_capture` per
`resource_id`: the newest capture of each resource replaces that resource's previous capture as
a whole. The dump does not displace the archive, and the archive does not displace the dump
(FACTS T08, T10; ADR-039). `TODO: verify` the vendor identity and revision key.

**Activation (2026-10-09, master `6cccc4e`, PR #95).** Cutoff 2026-10-08, no prior silver, so
nothing was overwritten. `eleclink` transformed **32,831 rows**, equal to the planned
24,359 + 8,472 (peak working set 568.3 MiB). The family holds two Parquet files under
`year=2026/month=10`, one per resource. `reconcile --all --cutoff 2026-10-08` exited 0 over 69
families with 0 gaps (gridflow `@.planning/v0.22-RESULTS.md` section IC-1; RULINGS 566, 567).

**Second capture of the dump (2026-10-16, bronze and silver read 2026-10-24).**
`raw_20261016T201759Z_1f748d48-1daf-4f1a-a5f1-d581e86a2190_cfed84ef.csv`, 2,239,019 bytes,
24,599 rows, the same M header, CKAN `last_modified` still `2026-09-17T08:45:57.592028`. Every
row of the 2026-10-08 dump is present unchanged (full-row comparison: 0 missing, and 0 rows with
the same `(Data Upload Time GMT, Auction Type, Operational Period Start)` but different values).
240 rows are new, uploaded `2026-10-08T14:30:05` to `2026-10-16T14:30:05`, for target hours
`2026-10-08 22:00` to `2026-10-17 21:00`; none carries an upload time before the first capture.
1,025 distinct upload instants; auctions still `Day Ahead` and `Intraday 1` to `Intraday 3`. So
between these two captures NESO only appended; this does not show that rows are never revised, and
the hold stands. The 2026-10-16 run downloaded no archive body: the client skips an upload whose
newest capture carries the live `last_modified`, so the archive's stamp had not moved. Silver now
holds three Parquet files; `_latest` per `resource_id` takes the 2026-10-16 dump (24,599 rows) and
the 2026-10-08 archive (8,472 rows).

Silver columns beyond the vendor columns: `issue_time`, `resource_id`, `timestamp_utc`,
`published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`,
`source_run_id`, `dataset_version`. All timestamps are tz-aware UTC. `dataset_version` `1+e1`
means record version 1 and engine version 1. It does not identify the epoch, so both resources'
rows carry the same value.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Daily

"Daily" is the only vendor statement of cadence, and it applies to the current dump. A target
can be re-issued by later uploads (1,015 distinct upload instants in one capture). `TODO: verify`
the vendor's daily publication time and whether intraday re-issues follow a schedule. The archive upload has not been modified since
`2024-11-27T14:34:10` (CKAN `last_modified`, unchanged between the 2026-10-06 catalogue snapshot
and the 2026-10-08 capture). That is consistent with a closed archive, but no vendor statement
says it is frozen: `TODO: verify`. gridflow's refresh captures one state per run, so silver
holds a sample of the dump's history, not every intermediate state. No scheduled gridflow
refresh exists yet. Captures are on demand.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `eleclink`: held: TODO: the dump returns past targets (rows before the capture) and NESO does not state that a row is unchanged since its `Data Upload Time GMT`, so historical issued limits are not evidenced, and the archive's Operational Date calendar / rollover and Version meaning are undocumented. (unit E-SEM)

The held output exists in silver but is not eligible for point-in-time model use
until unit E-SEM answers its question (RULINGS 565, 567). Under ruling 66 (2026-10-24) the site
page shows the rows with one line naming the question, and draws the current table's limits only
as the table stood when fetched, not as first issued. The hold covers both resources and later captures until NESO documents dump-row
immutability (or publishes per-issue files) and the archive's date calendar and `Version`
contract.
