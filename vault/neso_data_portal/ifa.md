---
source: "neso_data_portal"
package: "ifa"
dataset_keys: ["ifa_da_id_weekly_itls", "ifa_itl"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: IFA transfer limits
  summary: >-
    NESO's hourly limits on flow each way over the IFA interconnector, in MW, with reasons.
  facts:
    vendor: "NESO Data Portal, package `ifa`: a current datastore table and an archive CSV"
    cadence: "Ad hoc, NESO says"
    grain: "Each row: one hour's import and export limits; current rows add upload and auction"
    history: "NESO's files label hours from 14 October 2022: archive, then the current table"
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
    silver: neso_data_portal/ifa_itl
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
      Silver `ifa_itl`, `Intraday 1` rows (the table has no day-ahead rows), one per hour, as NESO's
      file stood when fetched on 16 October 2026. Each upload precedes its hour, but NESO does not say
      rows are unchanged since.
    alt: >-
      Line chart from neso_data_portal/ifa_itl of NESO's Intraday 1 limits each way over IFA, MW,
      hourly, 9 to 15 October 2026. To GB is 2,000 MW in 160 of 168 hours, dipping to 1,480 at 04:00
      UTC on 9 October and to 1,080 at midnight on 11 October. From GB is 2,000 in only 38 hours: it
      is 0 from 07:00 to 21:00 on 9 October, 16:00 to 20:00 on 11 October and 08:00 to 15:00 on 12 and
      15 October, and below 1,000 for most of 11 to 14 October.
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
      - {run: gridflow pipeline neso_data_portal ifa_itl --last 24h,
         comment: "current table to bronze, then silver"}
      - {run: gridflow pipeline neso_data_portal ifa_da_id_weekly_itls --last 24h,
         comment: "archive to bronze, then silver"}
  record:
    select:
      filter:
        - {column: bronze_capture_id, op: eq, value: "bronze/neso_data_portal/ifa_itl/2026/10/16/raw_20261016T203818Z_9e539e05-e09c-4983-91fd-c766f03d0339_9c7df8e4.csv"}
        - {column: operational_period_start_gmt, op: ge, value: "2026-08-17T15:00:00Z"}
        - {column: operational_period_start_gmt, op: le, value: "2026-08-17T18:00:00Z"}
      order_by: [operational_period_start_gmt, auction_type]
      columns: [operational_period_start_gmt, auction_type, data_upload_time_gmt, flow_to_gb_mw,
                reason_for_restriction_to_gb, flow_from_gb_mw, reason_for_restriction_from_gb, issue_time]
    key: [issue_time, auction_type, operational_period_start_gmt]
    caption: "Four hours of 17 August 2026, two auctions each; from 16:00 `Intraday 2` allows no exports."
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
      Returns a pandas DataFrame from `silver_neso_data_portal_ifa_itl_latest`, the newest capture,
      filtered on the hour's start with both ends included; times come back in Europe/London and are converted to UTC.
    cells:
      - |
        df = data.neso_data_portal.query("ifa_itl", "2026-10-09", "2026-10-15")
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
    needs: IFA's current table
    plot_alt: >-
      Step plot, UTC, of NESO's IFA export limit by auction, 9 to 15 October 2026. Intraday 1
      lists every hour: 0 MW in 46 of them, longest from 07:00 to 21:00 UTC on 9 October, and 2,000 at
      times on most days. Intraday 2 lists only 12 October 22:00 to 13 October 21:00 UTC, from 370 to
      2,000.
  family:
    slug: ifa
    members:
      - dataset: ifa_itl
        differs: "Current table from December 2024: upload time, auction and hour start in GMT"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=ifa"
          - "GET https://api.neso.energy/datastore/dump/9e539e05-e09c-4983-91fd-c766f03d0339"
        caveat: "NESO does not say rows stay as uploaded, so past limits may not be as issued."
      - dataset: ifa_da_id_weekly_itls
        differs: "Archive to December 2024: hours by operational date and GMT/BST range; no upload time"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=ifa"
          - "GET https://api.neso.energy/dataset/a95d222b-e390-4ad0-af17-09de957616ed/resource/2b38e754-a92e-4383-827d-5e6c10c882b0/download/archived_ifa-2.csv"
        caveat: "NESO does not define the operational day or GMT/BST hours; each hour predates the file's upload."
  related:
    - {dataset: neso_data_portal/ifa2, note: "The same NESO limits on IFA2, another GB interconnector"}
    - {dataset: neso_data_portal/eleclink, note: "NESO's limits on ElecLink, another GB interconnector"}
    - {dataset: entsoe/net_transfer_capacity, note: "ENTSO-E's forecast capacity across each GB border, all links together"}
    - {dataset: neso_data_portal/historic-demand-data, note: "IFA's half-hourly flow, in NESO's historic demand files"}
---

# IFA - NESO's Intraday Transfer Limit

NESO's **transfer-limit submissions for IFA**, a GB–France interconnector, in MW per hourly
period and per direction. The package notes describe them as the values NESO submits to the
interconnector capacity calculation, which "restrict the maximum GB import and export
interconnector flows". They are **limits, not flows**: each row holds NESO's maximum for flow
**to GB (import)** and NESO's maximum for flow **from GB (export)**, as two separate
non-negative MW figures. The package notes also say that the final interconnector capacity is
calculated from these NESO values, the connected system operator's values and the
interconnector's capability, so the final capacity can be lower than the NESO value. The final
values are published by each interconnector's trading facilitator, not here. The package notes
say values are published only where NESO applied a restriction, so a missing hour means NESO
applied none, not a zero limit. The files do not follow that literally (bronze read 2026-10-24):
the archive lists every hour of each labelled day (11,401 rows over 475 days), with the reason
blank on 3,922 rows and `System Security` on the rest, and the 2026-10-16 current table gives the
reason `No Restriction` for flow to GB on 10,741 of 11,782 rows, from GB on 5,196, and in both
directions on 4,866.

The package has two resources, and gridflow keeps each as its own family:

- `ifa_itl`: the **current** intraday transfer-limit dump (CKAN datastore). Each row is one
  submission: an upload instant, an auction (`Intraday 1` to `Intraday 4`), an hourly target
  start in GMT, and the two directional limits with a reason per direction.
- `ifa_da_id_weekly_itls`: the **archived** day-ahead and intraday limits (a CSV upload). Each
  row is an hour, labelled by one combined operational-date-and-hour string. It has no auction,
  issue or week column. "Weekly" describes how the archive was packaged; the rows are hourly.

**Both outputs are held (unit E-SEM).** The current dump returns past targets and NESO does not
say a row is unchanged since its upload time. The archive's operational-date rollover and
GMT/BST labels are undocumented, and every target precedes the upload. See Holds. The outputs
exist in silver, but they are not eligible for point-in-time model use until
E-SEM is answered (RULINGS 565, 567). This note gives schema, clocks and row counts; under ruling
66 (2026-10-24) the site page shows the rows, with one line per family naming its question.

Related pages: the sister link @ifa2.md has the same two-resource shape. @eleclink.md is another
GB–France link. Interconnector static facts are in @interconnector-register.md. ENTSO-E's
France NTC is a border aggregate across all GB–France links, so it cannot validate an
individual IFA limit. A direct join found no exact per-link equality (K-IC-1-FACTS IC1-1).

- Publisher group: Interconnectors
- Registry group: interconnectors · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Archived IFA DA & ID Weekly ITLs | CSV | upload | `2b38e754-a92e-4383-827d-5e6c10c882b0` |
| IFA ITL Data | CSV | dump | `9e539e05-e09c-4983-91fd-c766f03d0339` |

Both resources are SILVER. The package has no DOC resources, so there is no methodology
document and no `_files` family. Package id `a95d222b-e390-4ad0-af17-09de957616ed`.

- **Archived IFA DA & ID Weekly ITLs** -> `ifa_da_id_weekly_itls` (held).
  Download: [archived_ifa-2.csv](https://api.neso.energy/dataset/a95d222b-e390-4ad0-af17-09de957616ed/resource/2b38e754-a92e-4383-827d-5e6c10c882b0/download/archived_ifa-2.csv).
  Captured: `raw_20261008T110923Z_2b38e754-a92e-4383-827d-5e6c10c882b0_21af7678.csv`,
  482,135 bytes, 11,401 rows. CKAN `last_modified` `2025-08-19T09:35:34.041522`; resource
  created `2025-02-19`. Vendor description: Network Transfer Capacity restrictions submitted to
  day-ahead and intraday auctions.
- **IFA ITL Data** -> `ifa_itl` (held).
  Download: [datastore dump](https://api.neso.energy/datastore/dump/9e539e05-e09c-4983-91fd-c766f03d0339).
  Captured: `raw_20261008T110950Z_9e539e05-e09c-4983-91fd-c766f03d0339_d327b5ff.csv`,
  1,077,108 bytes, 11,566 rows. CKAN `last_modified` `2026-09-17T08:52:40.342385`; resource
  created `2024-12-11`. Vendor description: Intraday Transfer Limit restrictions submitted to
  day-ahead and intraday auctions.

Each capture has one header epoch. The current resource's description announces a column rename
on **2026-09-17** (for example `Flow (MW) To GB` became `Flow in MW To GB`). Only the
post-rename header was captured, so the record has one epoch. An earlier header is not
evidenced locally and is not invented here. A capture taken before the rename would not match
the record's header (K-IC-1-FACTS IC1-4). CKAN declares no datastore primary key for either
resource.

**Coverage (labels and target hours only).** The archive's labels run from operational date
`2022-10-14 00:00` to `2024-12-19 23:00`. The current dump's UTC target starts run from
`2024-12-19 23:00` to `2026-10-08 21:00` in the 2026-10-08 capture, and to `2026-10-16 21:00` in
the 2026-10-16 capture. One literal archive label coincides with a current
target hour. The canonical overlap of the two resources is `TODO: verify`, because the archive's
operational-date rollover is undocumented (K-IC-1-FACTS IC1-4). Do not splice the two families
into one series until it is resolved.

## Families

### `ifa_da_id_weekly_itls`

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

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the capture's CKAN
   `last_modified`, `2025-08-19T09:35:34.041522`. CKAN emits it without an offset, and gridflow
   reads it as UTC (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`).
   Every row of the capture carries this one value. The file has **no issue column**, so the
   issue is `none` and the vintage is the only availability clock. Every target label in the
   file precedes this vintage, so the vintage says when the archive file was last changed, not
   when any limit was first issued.
2. **Event time (`none`).** The temporal recipe is `none`, so `timestamp_utc` = `event_time` =
   the **capture time**, here `2026-10-08T11:09:23.434751Z` (`written_at` of the bronze
   capture), on every row. **It is not the hour the limit applies to.** The target hour lives
   only in the raw string `operational_date_and_hour`, which is kept byte-identical and is not
   converted to an instant (see Hold question).

**Hold question.** The vendor header names the clock as "GMT/BST", and the dictionary says only
"Operational Date and time for which restriction applies." NESO does not define:

- the **operational-date rollover**. Every labelled day starts, in file order, with the
  `23:00` hour, so the date may not be the civil date of each hour;
- how the GMT/BST hour maps to an absolute instant on clock-change days. On the label date
  `20241027` the file has 25 rows, with the `01:00-02:00` hour repeated as `(a)` and `(b)`.
  On the label date `20221030` it has 24 rows with no repeat marker. So the archive is not
  consistent across autumn transitions.

Until NESO defines these, no row can be dated to an absolute hour. Because every target precedes
the upload's `last_modified`, the forward-target rule of RULINGS 529 cannot release the output
either (K-IC-1-FACTS §2 `ifa_da_id_weekly_itls`, IC1-3, IC1-6).

**Label shape.** Labels come in two spellings (K-IC-1-FACTS IC1-4, g1: "spacing/fold
variations"). 9,794 labels have the form `YYYYMMDD HH:MM-HH:MM`, with no spaces around the
hyphen; this count includes the 2 labels that carry an ` (a)` or ` (b)` suffix on the repeated
hour. 1,607 labels have spaces around the hyphen, `YYYYMMDD HH:MM - HH:MM`, which is also the
spelling of the vendor dictionary's example. 9,794 + 1,607 = 11,401, so every row has one of the
two spellings. The spaced form covers operational dates 20221014 to 20230214, and the earliest
labels in the file use it. The unspaced form covers 20230111 to 20241219, so the two spellings
overlap for about a month. **The header promises `YYYY-MM-DD`, but no label contains a dashed
date.** gridflow keeps each label as supplied, spacing and suffix included, and does not
normalise, strip or reinterpret it.

**Shape of the capture (counts only).** 11,401 rows. The combined label was measured unique
over the full body (duplicate excess 0), and 2 rows carry a fold suffix. Every interval measures
one hour. There is no auction, version, week-number or issue column, so the archive does not say
which auction or which submission a row came from. `TODO: verify` whether each row is the
day-ahead or the final intraday value.

**Units (vendor dictionary only: CKAN field info for resource `2b38e754...`;
[archived IFA dictionary](https://www.neso.energy/data-portal/ifa/archived_ifa_da__id_weekly_itls)).**
`Flow (MW) to GB` and `Flow (MW) from GB` are **MW**, "Maximum flow in this direction"
(dictionary type `numeric`), stored as float64. **To GB = import into GB, From GB = export from
GB**, each a directional maximum. They are never signed or netted (K-IC-1-FACTS IC1-1, g4). The
dictionary titles the reason column "Reason For Reduction" ("Reason for NTC restriction"); the
CSV header calls it `Reason for restriction`. It is categorical text with no unit.

**Sentinels and missing values (K-IC-1-FACTS g5).** No negative values, `-1`, non-numeric or
blank values appear in either flow column, and no `NA` or `N/A` token appears in the body. Both
directions are populated on every row. Zero limits occur and are **kept as numeric zero**: no
vendor source defines zero as missing. The reason column is blank on 3,922 rows; those become
null in silver, and no reason is invented. Hours absent from the file are not filled with zero,
a nameplate capacity or a reconstructed limit.

**Identity.** The vendor declares no key. The combined label was measured unique, so it is the
entity key as a capture guard, and `_latest` is `whole_capture`: the newest capture replaces the
family as a whole. `TODO: verify` a vendor-documented identity (K-IC-1-FACTS §2 T02).

### `ifa_itl`

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

1. **Vintage (`capture_fallback`).** This family is a datastore dump, so it does not take the
   CKAN `last_modified` as its vintage. `published_at` is **null** on every row, and
   `available_at` = `capture_written_at` = the gridflow capture time,
   `2026-10-08T11:09:50.125710Z`, on every row (ADR-035). The resource's CKAN `last_modified`
   (`2026-09-17T08:52:40`) matches the date of the announced column rename and is not used as a
   vintage. The row-level upload instant is carried separately as `issue_time` =
   `data_upload_time_gmt` (equal on every row; 482 distinct instants). **`issue_time` is a
   label, not an availability override.** NESO documents it as "Date and time that data was
   published", but not that a row's values are unchanged since then. So `available_at` is not
   backdated to it (K-IC-1-FACTS g2).
2. **Event time (`utc_instant`).** `timestamp_utc` = `event_time` =
   `operational_period_start_gmt`, the **start of the hourly period** the limit applies to. The
   dictionary says the timestamp "reflects the datetime when the period starts the next 1 hour
   time", and the header names GMT. On the 2026-03-29 clock change the targets form 24 distinct
   hours on the UTC date and 23 on the Europe/London date, which supports a UTC clock
   (K-IC-1-FACTS IC1-3). There are 10,390 distinct target hours. Several auctions or uploads
   can address the same hour.

**Hold question.** The dump returns past targets: 11,556 of 11,566 rows have a target hour
before the capture, and 818 rows have a target hour earlier than their own upload instant
(2026-10-08 capture; 11,781 of 11,782 and 824 in the 2026-10-16 capture). NESO
does not state that a row is unchanged since its `Data Upload Time GMT`, so the dump is not
evidence of the limits as historically issued. A NESO retention or revision statement, or
immutable per-issue files, would settle it (K-IC-1-FACTS §2 `ifa_itl` T05, g2, IC1-6).

**Auctions.** The body holds only `Intraday 1`, `Intraday 2`, `Intraday 3` and `Intraday 4`. No
day-ahead row appears, although the dictionary describes the column as "Day-ahead (DA) or
Intraday (ID) auction". Spellings are kept as supplied.

**Units (vendor dictionary only: CKAN field info for resource `9e539e05...`;
[IFA dictionary](https://www.neso.energy/data-portal/ifa/ifa_itl_data-0)).** `Flow in MW To GB`
and `Flow in MW From GB` are **MW**, "Maximum flow in this direction" (dictionary type `int4`),
stored as float64, which leaves integer values unchanged. **To GB = import into GB, From GB =
export from GB**, each a directional maximum, never signed or netted (K-IC-1-FACTS IC1-1, g4).
The two datetime columns carry the dictionary unit "ISO 8601"; the bodies carry no offset, and
the GMT header and dictionary make them UTC. The reason columns are categorical text with no
unit.

**Sentinels and missing values (K-IC-1-FACTS g5).** No negative values, `-1`, non-numeric or
blank values appear in either flow column, and no `NA` or `N/A` token appears in the body. No
cell in silver is null except `published_at`, which is null by design. Zero limits occur,
including runs of consecutive zero hours, and are **kept as numeric zero**. Explicit
`No Restriction` reasons appear, so a missing row and a "no restriction" row are different
things. Absent hours are not filled.

**Identity.** The vendor declares no key. `(issue_time, auction_type,
operational_period_start_gmt)` was measured unique over the full body (duplicate excess 0).
`(auction_type, operational_period_start_gmt)` alone is **not** unique (duplicate excess 72), so
the same auction can address the same hour in more than one upload, and `issue_time` must stay
in the key. `_latest` is `whole_capture`: the newest capture replaces the family as a whole, and
gridflow does not pick a "latest upload per hour". `TODO: verify` the vendor's revision
precedence (K-IC-1-FACTS §2 `ifa_itl` T04, g3).

**Activation (2026-10-09, master `6cccc4e`, PR #95).** Cutoff 2026-10-08, one capture per
family at the time: `ifa_itl` **11,566 rows** and `ifa_da_id_weekly_itls` **11,401 rows**, each equal to the
planned count. No prior silver existed, so nothing was overwritten. Each family holds one Parquet
file under `year=2026/month=10`. `reconcile --all --cutoff 2026-10-08` exited 0 over 69
families with 0 gaps (gridflow `@.planning/v0.22-RESULTS.md` section IC-1; RULINGS 566, 567).

**Second capture of `ifa_itl` (2026-10-16, bronze and silver read 2026-10-24).**
`raw_20261016T203818Z_9e539e05-e09c-4983-91fd-c766f03d0339_9c7df8e4.csv`, 1,097,358 bytes,
11,782 rows, the same post-rename header, CKAN `last_modified` still `2026-09-17T08:52:40.342385`.
Every row of the 2026-10-08 body is present unchanged (full-row comparison: 0 missing, and 0 rows
with the same `(Data Upload Time GMT, Auction Type, Operational Period Start)` but different
values). 216 rows are new, uploaded `2026-10-08T17:30:05` to `2026-10-15T17:30:05`, for target
hours `2026-10-08 22:00` to `2026-10-16 21:00`; none carries an upload time before the first
capture. 491 distinct upload instants; auctions still `Intraday 1` to `Intraday 4` only. So
between these two captures NESO only appended; this does not show that rows are never revised, and
the hold stands. Silver holds a second Parquet file of 11,782 rows (`available_at`
`2026-10-16T20:38:18.017089Z`), which `_latest` takes as the whole family. The archive
`ifa_da_id_weekly_itls` has no second capture, so it still has one.

Silver columns beyond the vendor columns: `issue_time` (`ifa_itl` only), `timestamp_utc`,
`published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`,
`source_run_id`, `dataset_version`. All timestamps are tz-aware UTC. `dataset_version` `1+e1` =
record version 1, epoch 1.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

"Ad hoc" is the only vendor statement of cadence. `TODO: verify` the publication schedule of
the current dump with NESO; the upload instants in the body do not establish one. The
archive's `last_modified` (`2025-08-19`) predates the capture by more than a year, and its last
label is the hour where the current dump starts, so it appears to be a closed archive. `TODO:
verify` that NESO will not append to it. gridflow's daily refresh captures one state per run,
and each capture replaces the family as a whole. The dated silver captures are therefore a
sample of the vendor's state, not its revision history. No scheduled gridflow refresh exists
yet. Captures are on demand.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above. Package page:
[IFA](https://www.neso.energy/data-portal/ifa).

## Holds

- `ifa_da_id_weekly_itls`: held: TODO: the archive's operational-date rollover, GMT/BST interpretation and `(a)`/`(b)` repeated-hour labels are undocumented, and every target precedes the upload's last_modified, so the forward-target rule (RULINGS 529) cannot apply. (unit E-SEM)
- `ifa_itl`: held: TODO: the dump returns past targets (rows before the capture) and NESO does not state that a row is unchanged since its `Data Upload Time GMT`, so historical issued limits are not evidenced. (unit E-SEM)

Both held outputs exist in silver but are not eligible for point-in-time model
use until unit E-SEM answers its question (RULINGS 565, 567). Under ruling 66 (2026-10-24) the
site page shows the rows of both, each family with one line naming its question, and draws the
current table's limits only as the table stood when fetched, not as first issued. The holds apply to the captured bodies and to later captures unless NESO
supplies the missing definitions.
