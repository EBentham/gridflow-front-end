---
source: "neso_data_portal"
package: "ifa2"
dataset_keys: ["ifa2_ifa_da_id_weekly_itls", "ifa2_ifa_itl"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: IFA2 transfer limits
  summary: >-
    NESO's hourly limits on flow each way over the IFA2 interconnector, in MW, with reasons.
  facts:
    vendor: "NESO Data Portal, package `ifa2`: a current datastore table and an archive CSV"
    cadence: "Ad hoc, NESO says"
    grain: "Each row: one hour's import and export limits; current rows add upload and auction"
    history: "NESO's files label hours from 13 October 2022: archive, then the current table"
  landscape: power
  what_it_is: >-
    NESO says it submits these to interconnector capacity calculations, capping GB imports and
    exports, in hourly MW; final capacity can be lower. It says it publishes only restrictions,
    but its October 2026 archive lists whole days, and many current rows say No Restriction.
    NESO calls them Intraday Transfer Limit (ITL) and, in the archive, Network Transfer Capacity
    (NTC) restrictions.
  how_used:
    - Which hours NESO restricted the link, by direction, from the stated reason
    - "A feature for flow and price models: when NESO restricted the link"
    - Set beside the final capacity the link's trading facilitator publishes
  chart:
    type: line
    silver: neso_data_portal/ifa2_ifa_itl
    time: operational_period_start_gmt
    filter:
      - {column: auction_type, op: eq, value: Intraday 1}
    dedup: {on: [operational_period_start_gmt], order_by: capture_written_at}
    values:
      - {column: flow_to_gb_mw, series: to_gb}
      - {column: flow_from_gb_mw, series: from_gb}
    aggregation: min
    window: {start: "2026-10-09", end: "2026-10-15"}
    unit: MW
  chart_view:
    title: Intraday 1 limits each way, 9 to 15 October 2026
    caption: >-
      Silver `ifa2_ifa_itl`, `Intraday 1` rows (the table has no day-ahead rows), hourly, as fetched 16
      October 2026; none cover 11 October 22:00 to 12 October 21:00 UTC. Each upload precedes its
      hour; NESO does not say rows are unchanged since.
    alt: >-
      Line chart from neso_data_portal/ifa2_ifa_itl of NESO's Intraday 1 limits each way over IFA2,
      MW, hourly, 9 to 15 October 2026, with no rows from 22:00 UTC on 11 October to 21:00 on 12
      October. To GB is 1,014 MW in every hour drawn, under From GB where they match. From GB is 1,014
      in 40 hours; it is 0 from 07:00 to 20:00 on 9 October, 16:00 to 19:00 on 11 October and 08:00 to
      15:00 on 15 October, and mostly 100 to 950 on 13 and 14 October.
    x_label: hour start, UTC (NESO labels it GMT)
    y_min: -40
    key:
      - {series: to_gb, label: To GB, note: "Import limit, NESO's `Flow in MW To GB`", paint: petrol}
      - {series: from_gb, label: From GB, note: "Export limit, NESO's `Flow in MW From GB`", paint: clay}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, the current table's dump and the archive CSV. Fetched
      16 October 2026, the table kept every row fetched 8 October unchanged, plus new ones.
    commands:
      - {run: gridflow pipeline neso_data_portal ifa2_ifa_itl --last 24h,
         comment: "current table to bronze, then silver"}
      - {run: gridflow pipeline neso_data_portal ifa2_ifa_da_id_weekly_itls --last 24h,
         comment: "archive to bronze, then silver"}
  record:
    select:
      filter:
        - {column: bronze_capture_id, op: eq, value: "bronze/neso_data_portal/ifa2_ifa_itl/2026/10/16/raw_20261016T203747Z_f9ff9381-6eb1-40cd-903b-ca7282b9f2a9_c415be4f.csv"}
        - {column: operational_period_start_gmt, op: ge, value: "2026-08-17T04:00:00Z"}
        - {column: operational_period_start_gmt, op: le, value: "2026-08-17T11:00:00Z"}
      order_by: [operational_period_start_gmt, auction_type]
      columns: [operational_period_start_gmt, auction_type, data_upload_time_gmt, flow_to_gb_mw,
                reason_for_restriction_to_gb, flow_from_gb_mw, reason_for_restriction_from_gb, issue_time]
    key: [issue_time, auction_type, operational_period_start_gmt]
    caption: "17 August 2026, 04:00 to 11:00 UTC: the import limit climbs from 0 MW to 1,014."
    fields:
      operational_period_start_gmt: "Start of the hour the limits apply to; header says GMT, read as UTC"
      auction_type: "The auction the limits are for; this table lists `Intraday 1` to `Intraday 4`"
      data_upload_time_gmt: "When NESO says the row was published; its header says GMT, read as UTC"
      flow_to_gb_mw: "The most power that may flow into GB in the hour, MW"
      reason_for_restriction_to_gb: "NESO's reason for the import limit, or `No Restriction`"
      flow_from_gb_mw: "The most power that may flow out of GB in the hour, MW"
      reason_for_restriction_from_gb: "NESO's reason for the export limit, or `No Restriction`"
      issue_time: "A copy of the upload time; not taken as when the row first appeared"
      timestamp_utc: "Equals `operational_period_start_gmt`; gridflow's event time"
      published_at: "Null: gridflow takes no publication time from a datastore dump"
      bronze_capture_id: The bronze file the row was read from
      capture_written_at: When gridflow wrote the capture to bronze, UTC
  notebook:
    lead: >-
      Returns a pandas DataFrame from `silver_neso_data_portal_ifa2_ifa_itl_latest`, the newest
      capture, filtered on the hour's start with both ends included; times come back in
      Europe/London and are converted to UTC.
    cells:
      - |
        df = data.neso_data_portal.query("ifa2_ifa_itl", "2026-10-09", "2026-10-15")
        for c in ["operational_period_start_gmt", "data_upload_time_gmt"]:
            df[c] = df[c].dt.tz_convert("UTC")
        df = df.sort_values(["operational_period_start_gmt", "auction_type"], ignore_index=True)
        df[["operational_period_start_gmt", "auction_type", "data_upload_time_gmt",
            "flow_to_gb_mw", "flow_from_gb_mw", "reason_for_restriction_from_gb"]].head()
      - |
        reasons = df.groupby("auction_type").reason_for_restriction_from_gb.value_counts()
        reasons.unstack(fill_value=0).rename_axis(columns=None).reset_index()
      - |
        wide = df.pivot(index="operational_period_start_gmt", columns="auction_type",
                        values="flow_from_gb_mw").asfreq("h")
        ax = wide.plot(drawstyle="steps-post", figsize=(8, 3.5), xlabel="hour start, UTC",
                       ylabel="export limit, MW")
        ax.legend(loc="lower left", bbox_to_anchor=(0, 1), ncols=4);
    needs: IFA2's current table
    plot_alt: >-
      Step plot, UTC, of NESO's IFA2 export limit, Intraday 1 only, 9 to 15 October 2026, broken
      where NESO lists no hours, 11 October 22:00 to 12 October 21:00 UTC. It is 0 MW in 29 hours,
      longest from 07:00 to 20:00 UTC on 9 October, and reaches 1,014 on most days.
  family:
    slug: ifa2
    members:
      - dataset: ifa2_ifa_itl
        differs: "Current table from December 2024: upload time, auction and hour start in GMT"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=ifa2"
          - "GET https://api.neso.energy/datastore/dump/f9ff9381-6eb1-40cd-903b-ca7282b9f2a9"
        caveat: "NESO does not say rows stay as uploaded, so past limits may not be as issued."
      - dataset: ifa2_ifa_da_id_weekly_itls
        differs: "Archive to December 2024: hours by operational date and GMT/BST range; no upload time"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=ifa2"
          - "GET https://api.neso.energy/dataset/860c8221-c656-4af3-800a-281b9e500489/resource/19725dae-1d69-423e-8d5b-0f4dc8220b6b/download/archived_ifa2.csv"
        caveat: "NESO does not define the operational day or GMT/BST hours; each hour predates the file's upload."
  related:
    - {dataset: neso_data_portal/ifa, note: "The same NESO limits on IFA, another GB interconnector"}
    - {dataset: neso_data_portal/eleclink, note: "NESO's limits on ElecLink, another GB interconnector"}
    - {dataset: entsoe/net_transfer_capacity, note: "ENTSO-E's forecast capacity across each GB border, all links together"}
    - {dataset: neso_data_portal/historic-demand-data, note: "IFA2's half-hourly flow, in NESO's historic demand files"}
---

# IFA2 - NESO's Intraday Transfer Limit

These are NESO's **transfer limits on the IFA2 interconnector** between GB and France, in MW per
hourly period and per direction. The package notes say they are "the values submitted by NESO to
the interconnector capacity calculation processes which restrict the maximum GB import and
export interconnector flows". Each row is a NESO limit submitted to a day-ahead or intraday
capacity auction. It is not a measured flow and not the link's final traded capacity. The notes
add that the final capacity is calculated from these NESO values, the connected system operator's
values and the interconnector's capability, so the final figure may be lower. The trading
facilitator publishes it, not NESO. The package notes say NESO publishes a value **only where it
applied a restriction**, so an hour with no row means NESO applied no restriction. It does not
mean zero capacity, and gridflow does not fill such hours. The files do not follow the notes
literally (bronze read 2026-10-24): the archive lists every hour of each labelled day (7,680 rows
over 320 days of 24), with the reason blank on 2,822 rows and `System Security` on the rest, and
the 2026-10-16 current table gives the reason `No Restriction` for flow to GB on 7,477 of 7,920
rows, from GB on 3,903, and in both directions on 3,682.

Direction convention (K-IC-1-FACTS IC1-1): **To GB = import** (France to GB) and **From GB =
export** (GB to France). Each column is a separate directional maximum in MW. Neither is a signed
net flow, and gridflow does not sign or net them.

The package has two resources and gridflow keeps them as two families:

- `ifa2_ifa_itl`, the **current** datastore dump. It covers targets from 2024-12-19 23:00 UTC
  and carries an upload timestamp and an auction type on each row.
- `ifa2_ifa_da_id_weekly_itls`, an **archive** upload, last modified 2025-02-19. It covers
  operational-date labels from `2022-10-13 00:00` to `2024-12-19 23:00`. It has no auction,
  issue or week column. "Weekly" in its name describes how the files were packaged. Its rows are
  hourly.

**Both outputs are held (unit E-SEM).** The current dump cannot show that a historical row is
unchanged since its upload time. The archive's operational-date and GMT/BST labels have no
documented mapping to UTC instants. See Holds. Both outputs exist in silver, but neither is
eligible for point-in-time model use until E-SEM is answered (gridflow
`@.planning/RULINGS.md` 565, 567). This note gives schema, clocks and row counts; under ruling 66
(2026-10-24) the site page shows the rows, with one line per family naming its question.

Related pages: the sister IFA link is on @ifa.md, and the other GB interconnectors are on
@eleclink.md, @nemolink.md, @nsl.md and @viking.md. For ENTSO-E, see
@../../entsoe/datasets/net_transfer_capacity.md and
@../../entsoe/datasets/cross_border_flows.md. ENTSO-E's France figure is an aggregate for the
whole border, so it cannot validate a single link's limit. A direct join found no exact match per
link for IFA2 (K-IC-1-FACTS IC1-1).

- Publisher group: Interconnectors
- Registry group: interconnectors · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Archived IFA2 DA & ID Weekly ITLs | CSV | upload | `19725dae-1d69-423e-8d5b-0f4dc8220b6b` |
| IFA2 ITL Data | CSV | dump | `f9ff9381-6eb1-40cd-903b-ca7282b9f2a9` |

Both resources are SILVER. There are no DOC resources, so the package has no methodology
document and no `_files` family. Package id `860c8221-c656-4af3-800a-281b9e500489`.

- **Archived IFA2 DA & ID Weekly ITLs** -> `ifa2_ifa_da_id_weekly_itls` (held). Vendor
  description: "Network Transfer Capacity restrictions submitted to Day-ahead and Intraday
  auctions".
  Download: [archived_ifa2.csv](https://api.neso.energy/dataset/860c8221-c656-4af3-800a-281b9e500489/resource/19725dae-1d69-423e-8d5b-0f4dc8220b6b/download/archived_ifa2.csv).
  Captured: `raw_20261008T110857Z_19725dae-1d69-423e-8d5b-0f4dc8220b6b_7e96c2c7.csv`,
  314,203 bytes, 7,680 rows. CKAN `last_modified` `2025-02-19T11:53:27.927475`. The resource is
  `datastore_active` in CKAN, but its `url_type` is `upload`, so gridflow captures the uploaded
  file. A datastore count read on 2026-10-08 returned a total of 7,680, which matches the capture.
- **IFA2 ITL Data** -> `ifa2_ifa_itl` (held). Vendor description: "Intraday Transfer Limit
  restrictions submitted to Day-ahead and Intraday auctions".
  Download (datastore dump): [IFA2 ITL Data](https://api.neso.energy/datastore/dump/f9ff9381-6eb1-40cd-903b-ca7282b9f2a9).
  Captured: `raw_20261008T110920Z_f9ff9381-6eb1-40cd-903b-ca7282b9f2a9_dbd79ced.csv`,
  717,661 bytes, 7,752 rows. A datastore count on 2026-10-08 returned 7,752.

Both captures have a single header epoch. The resource description says NESO renamed the dump's
column ids on **2026-09-17**, from `Data Upload Time (GMT)` to `Data Upload Time GMT`, from
`Operational Period Start Date & Time (GMT)` to `Operational Period Start Date and Time GMT`, and
from `Flow (MW) To GB` / `From GB` to `Flow in MW To GB` / `From GB`. gridflow has captured only
the post-rename header, so the record declares only that epoch. If an older capture with the
pre-rename header ever turned up, it would need a second epoch. No such capture has been observed,
and none is invented here (FACTS IC1-4).

## Families

### `ifa2_ifa_da_id_weekly_itls`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Operational Date (YYYY-MM-DD) & Time GMT/BST (HH:MM - HH:MM) | `operational_date_and_hour` | string | — | yes | — | — |
| Flow (MW) to GB | `flow_to_gb_mw` | float64 | — | yes | — | MW |
| Flow (MW) from GB | `flow_from_gb_mw` | float64 | — | yes | — | MW |
| Reason for restriction | `reason_for_restriction` | string | — | yes | — | — |

- Entity key: `operational_date_and_hour`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held (unit E-SEM).** This note gives schema, clocks and counts; the site page shows the rows with a caveat line (ruling 66, 2026-10-24).

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the
   capture's CKAN `last_modified`, `2025-02-19T11:53:27.927475`. CKAN gives this value without
   an offset, and gridflow reads it as UTC (gridflow
   `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). All 7,680 rows share this one
   value. The file has **no issue column**, so the issue recipe is `none` and the vintage is the
   only availability clock. Every target label is earlier than this vintage, so the archive
   records past restrictions. It does not show when each one was first issued.
2. **Event time (`none`).** The temporal recipe is `none`. `timestamp_utc` and `event_time`
   therefore both equal the **capture time**, `2026-10-08T11:08:57.403566Z` (`written_at` of the
   bronze capture), on every row. **This is not the hour the restriction applies to.** The
   combined label is stored as one raw string, byte for byte as published, and is not turned into
   an instant (see Hold question). A consumer must not read `timestamp_utc` as the target hour.

**Hold question.** The vendor dictionary gives the column as "Operational Date and time for which
restriction applies", with the example `20221214 23:00 - 00:00`. The header says `GMT/BST`, but
nothing says which clock applies to which row, or how the operational date relates to the hour.
Every labelled day in the capture has 24 rows, and in file order each starts at `23:00`. That
pattern points to an operational day that begins the evening before, but it is not a documented
rollover rule. The day labelled `20221030`, a UK autumn clock-change date, also has 24 rows and no
repeated-hour marker, so the body does not show a complete UK-local autumn day. By contrast, the
IFA archive marks a later clock-change day (`20241027`) with `(a)`/`(b)` suffixes (@ifa.md). NESO must define the operational-date rollover and the GMT/BST
reading before any label can become a UTC instant. Because every target is earlier than the
upload's `last_modified`, the forward-target rule (RULINGS 529) cannot release the family either
(FACTS `ifa2_ifa_da_id_weekly_itls` T01, IC1-3, IC1-6).

**Shape of the capture (counts only).** There are 7,680 rows, one per distinct combined label.
The label was measured unique over the full body, and silver confirms 0 duplicate keys. The file
has no auction, week or issue column, so the archive cannot show which auction a row belonged to.
The vendor's resource description says only that the rows were submitted to day-ahead and
intraday auctions. 2,822 rows have a blank `reason_for_restriction`, which is stored as null. No
other silver cell is null.

**Units (vendor dictionary only: CKAN datastore field info for resource `19725dae...`, snapshot
`20261006T195819Z`).** Both flow columns are **MW**, described as the "Maximum flow in this
direction". The dictionary types them as number, with CKAN type `int4`. gridflow casts them to
float64, which leaves whole numbers unchanged. `operational_date_and_hour` and
`reason_for_restriction` have unit `N/A`.

**Sentinels and missing values (FACTS g5).** No null-token map is declared. Full-body checks
found no negative directional values, no `-1`, and no blank, `NA` or `N/A` flow cells. Both
directions are filled on every row. Zero limits occur in both directions. No vendor source defines
zero as missing, so zeros stay numeric zero and are never converted to null. Blank reasons become
null, and gridflow does not invent a reason. `TODO: verify` with NESO whether a zero limit means
a full restriction in that direction.

**Identity.** The combined label was measured unique, but no vendor text declares it a key. The
entity key is therefore a guard on the capture, and `_latest` is `whole_capture`. `TODO: verify`
the vendor's key and whether the archive is ever revised.

**Boundary with the current dump.** The archive's last label, `2024-12-19 23:00`, is the same as
the dump's first target hour. Under the literal reading of the label, one target is shared. Under
a hypothetical rule that moves `22:00`/`23:00` labels to the previous day, none is shared. The
relationship between the archive and the dump is therefore unresolved until the rollover is
documented (FACTS IC1-4). gridflow does not join or splice the two families.

**Activation (2026-10-09, master `6cccc4e`).** Cutoff 2026-10-08, one capture at activation: **7,680 rows**,
equal to the planned count. No prior silver existed, so nothing was overwritten. The family holds
one Parquet file under `year=2026/month=10`. A full `reconcile --all` run with cutoff 2026-10-08
exited 0 over 69 families with 0 gaps (gridflow `@.planning/v0.22-RESULTS.md` section IC-1;
RULINGS 566, 567).

### `ifa2_ifa_itl`

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

- Entity key: `issue_time`, `auction_type`, `operational_period_start_gmt`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`operational_period_start_gmt`)

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

**Held (unit E-SEM).** This note gives schema, clocks and counts; the site page shows the rows with a caveat line (ruling 66, 2026-10-24).

**The two clocks for this family:**

1. **Vintage (`capture_fallback`, not `ckan_last_modified`).** This family reads a datastore
   dump, so its vintage is the gridflow capture time and not a CKAN timestamp (gridflow
   `@docs/DECISION_LOG/ADR-035-neso-datastore-dump-leg.md`). `published_at` is null on every
   row. `available_at` is `2026-10-08T11:09:20.101233Z` on every row (`capture_written_at`, the
   bronze `written_at`). The sidecar's CKAN `last_modified`, `2026-09-17T08:49:23.299201`, is
   the date of the column rename. It is **not** the vintage, and rows must not be backdated to
   it. Each row also carries an **issue** clock: `issue_time` = `data_upload_time_gmt`, which
   the vendor defines as the "Date and time that data was published" in GMT (323 distinct values
   in this capture). `issue_time` labels the row, but it does not set availability. `available_at`
   is never backdated to it (FACTS g2).
2. **Event time (`utc_instant`).** `timestamp_utc` = `event_time` =
   `operational_period_start_gmt`. The silver check confirmed these are equal on every row. The
   vendor defines this column as the start of a **one-hour** operational period in GMT: a value
   of `2022-10-20T22:00:00` covers 22:00 to 23:00. gridflow parses it as UTC (FACTS T02). The
   target hours in this capture run from `2024-12-19 23:00` to `2026-10-08 21:00` UTC
   (7,176 distinct hours), and to `2026-10-16 21:00` in the 2026-10-16 capture.

**Hold question.** The dump returns past targets: 7,742 of 7,752 rows target an hour before the
capture. In 676 rows the target hour is even earlier than the row's own `Data Upload Time GMT`
(2026-10-08 capture; 7,919 of 7,920 and again 676 in the 2026-10-16 capture).
NESO does not state that a returned row is unchanged since its upload time, so the dump cannot
show what limit was in force at an earlier issue. The issued history is therefore not evidenced.
`TODO: verify` with NESO whether the dump retains every upload unchanged, or whether rows can be
revised or replaced, or else obtain immutable files per issue (FACTS T05, g2).

**Shape of the capture (counts only).** There are 7,752 rows with four distinct `auction_type`
labels, `Intraday 1` to `Intraday 4`. No day-ahead row appears in this body, although the vendor
description mentions day-ahead auctions. Auction labels are stored with their exact spelling.
`(issue_time, auction_type, operational_period_start_gmt)` was measured unique over the full body
(0 duplicates in silver). The pair `(auction_type, operational_period_start_gmt)` is not unique,
because one target can carry several uploads. No silver cell is null except `published_at`.

**Units (vendor dictionary only: CKAN datastore field info for resource `f9ff9381...`, snapshot
`20261006T195819Z`).** `Flow in MW To GB` and `Flow in MW From GB` are **MW**, each described as
the "Maximum flow in this direction". The dictionary types them as integer, with CKAN type
`int4`, and gridflow casts them to float64. Both time columns have unit `ISO 8601`, and their
dictionary titles say GMT. `Auction Type` ("Day-ahead (DA) or Intraday (ID) auction") and both
reason columns have unit `N/A`. The dictionary titles still use the pre-rename names, for example
`Data Upload Time (GMT)` and `Flow (MW) To GB`, while the column ids are the post-rename names
that gridflow matches.

**Sentinels and missing values (FACTS g5).** No null-token map is declared. Full-body checks
found no negative or `-1` values, and no blank, `NA` or `N/A` flow cells. No reason cell is
blank. Zero limits occur in both directions and stay numeric zero. Hours with no row are left
absent and are never filled with zero or nameplate capacity, because the package notes say a
missing value means NESO applied no restriction.

**Identity and DST.** Only the GMT wording in the dictionary establishes the clock. This capture
has too few targets on clock-change days to confirm it independently, unlike the other current
interconnector dumps (FACTS IC1-3). `TODO: verify` the vendor's key. No primary key is declared
in the catalogue, so the entity key is a capture guard and `_latest` is `whole_capture`.

**Activation (2026-10-09, master `6cccc4e`).** Cutoff 2026-10-08, one capture at activation: **7,752 rows**,
equal to the planned count. No prior silver existed. The family holds one Parquet file under
`year=2026/month=10`. A full `reconcile --all` run exited 0 with 0 gaps (gridflow
`@.planning/v0.22-RESULTS.md` section IC-1; RULINGS 566, 567).

**Second capture (2026-10-16, bronze and silver read 2026-10-24).**
`raw_20261016T203747Z_f9ff9381-6eb1-40cd-903b-ca7282b9f2a9_c415be4f.csv`, 733,375 bytes,
7,920 rows, the same post-rename header, CKAN `last_modified` still `2026-09-17T08:49:23.299201`.
Every row of the 2026-10-08 body is present unchanged (full-row comparison: 0 missing, and 0 rows
with the same `(Data Upload Time GMT, Auction Type, Operational Period Start)` but different
values). 168 rows are new, uploaded `2026-10-08T17:45:08` to `2026-10-15T17:45:05`, for target
hours `2026-10-08 22:00` to `2026-10-16 21:00`; none carries an upload time before the first
capture. 330 distinct upload instants; auctions still `Intraday 1` to `Intraday 4` only. So
between these two captures NESO only appended; this does not show that rows are never revised, and
the hold stands. Silver holds a second Parquet file of 7,920 rows (`available_at`
`2026-10-16T20:37:47.957284Z`), which `_latest` takes as the whole family. The archive has no
second capture.

Silver columns beyond the vendor columns, for both families: `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and
`dataset_version`. `ifa2_ifa_itl` also has `issue_time`. All timestamps are tz-aware UTC.
`dataset_version` `1+e1` means record version 1, epoch 1.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

"Ad hoc" is the vendor's only statement of cadence. The dump has 323 distinct upload timestamps (330 on 2026-10-16),
but `TODO: verify` the publication schedule for each auction. Each
daily gridflow refresh captures one state of the dump. Because the vintage is the capture time,
the dated silver captures record what the dump returned on each capture day. They do not
reconstruct what was available at each upload. The archive was last modified on 2025-02-19 and
appears closed. `TODO: verify` that NESO will not modify or replace it. No scheduled gridflow
refresh exists yet, so captures run on demand.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
Every gridflow output derived from this package carries the attribution line above.

## Holds

- `ifa2_ifa_da_id_weekly_itls`: held: TODO: the archive's operational-date rollover and GMT/BST interpretation are undocumented, and every target precedes the upload's last_modified, so the forward-target rule (RULINGS 529) cannot apply. (unit E-SEM)
- `ifa2_ifa_itl`: held: TODO: the dump returns past targets (rows before the capture) and NESO does not state that a row is unchanged since its `Data Upload Time GMT`, so historical issued limits are not evidenced. (unit E-SEM)

Both held outputs exist in silver, but neither is eligible for point-in-time model
use until unit E-SEM answers its question (RULINGS 565, 567). Under ruling 66 (2026-10-24) the
site page shows the rows of both, each family with one line naming its question, and draws the
current table's limits only as the table stood when fetched, not as first issued. The holds apply to these captures and to later ones until NESO documents the archive calendar
and confirms that the dump's history is immutable.

Vendor pages: [IFA2 package](https://www.neso.energy/data-portal/ifa2),
[IFA2 ITL dictionary](https://www.neso.energy/data-portal/ifa2/ifa2_itl_data),
[archived IFA2 dictionary](https://www.neso.energy/data-portal/ifa2/archived_ifa2_da__id_weekly_itls).
