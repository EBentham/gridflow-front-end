---
source: "neso_data_portal"
package: "nemolink"
dataset_keys: ["nemolink_intraday", "nemolink_nemo_da_id_weekly_ntcs", "nemolink_ntc"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  held: true
  title: NemoLink transfer limits
  summary: >-
    NESO's hourly limits on flow each way over the NemoLink interconnector, in MW, with reasons.
  facts:
    vendor: "NESO Data Portal, package `nemolink`: two datastore tables and two archive CSVs"
    cadence: "Daily, NESO says"
    grain: "Each row: one hour's import and export limits, with NESO's reason"
    history: "NESO's files label hours from 12 October 2022: archives, then the current table"
  landscape: power
  what_it_is: >-
    NESO says it submits these to interconnector capacity calculations, capping GB imports and
    exports, in hourly MW; final capacity can be lower. It says it publishes only restrictions,
    yet its October 2026 files hold many No Restriction rows. It calls them Net Transfer
    Capacity (NTC) restrictions. Its two older files say Network Transfer Capacity.
  how_used:
    - Which hours NESO restricted the link, by direction, from the stated reason
    - "A feature for flow and price models: when NESO restricted the link"
    - Set beside the final capacity the link's trading facilitator publishes
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, each table's dump and each archive CSV. Fetched 16
      October 2026, the current table kept every row fetched 8 October unchanged, plus new ones.
    commands:
      - {run: gridflow pipeline neso_data_portal nemolink_ntc --last 24h,
         comment: "both files to bronze, then silver"}
      - {run: gridflow pipeline neso_data_portal nemolink_nemo_da_id_weekly_ntcs --last 24h,
         comment: "weekly archive to bronze, then silver"}
      - {run: gridflow ingest neso_data_portal nemolink_intraday --last 24h,
         comment: "bronze only: NESO renamed its columns"}
  family:
    slug: nemolink
    members:
      - dataset: nemolink_ntc
        differs: "Current table: upload time, auction, GMT hour start; archive from December 2022 with versions"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=nemolink"
          - "GET https://api.neso.energy/datastore/dump/7d43e2a0-1c22-4e05-895d-756bae210756"
          - "GET https://api.neso.energy/dataset/24b229de-2806-45a6-89a9-88097d67e5f2/resource/f169676e-67ec-4f2f-befd-1863c713179c/download/archived_nemolink_link_ntc_data.csv"
        held: "NESO does not say rows are unchanged since upload, and archive days and versions are undefined."
      - dataset: nemolink_intraday
        differs: "One table of 24 hourly rows with no date, named `NemoLink-Intraday1-20240127-001`"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=nemolink"
          - "GET https://api.neso.energy/datastore/dump/aae5acff-fd30-4c46-b996-a10e50cf4d50"
        held: "Rows give hours but no date; NESO explains neither the table's name nor whether it changes."
      - dataset: nemolink_nemo_da_id_weekly_ntcs
        differs: "Archive NESO calls weekly: hourly rows labelled 12 October to 16 December 2022"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=nemolink"
          - "GET https://api.neso.energy/dataset/24b229de-2806-45a6-89a9-88097d67e5f2/resource/ed977959-ccec-4cb6-b26f-c528863a243b/download/archived_weekly_nemolink_link_ntc_data.csv"
        held: "Hour labels have no defined day or clock, and no row says when NESO issued it."
  related:
    - {dataset: neso_data_portal/historic-demand-data, note: "NemoLink's half-hourly flow, in NESO's historic demand files"}
    - {dataset: neso_data_portal/interconnector-requirement-and-auction-summary-data, note: "NESO's own trades across links, with the volume cleared on NemoLink"}
    - {dataset: neso_data_portal/viking, note: "The same NESO limits on Viking Link, a current table and archive"}
    - {dataset: neso_data_portal/nsl, note: "The same NESO limits on North Sea Link, current table and archive"}
---

# NemoLink - NESO's Net Transfer Capacity

NESO's **transfer-capacity restrictions for the NemoLink interconnector**, in MW per hourly
period, in each direction. The package notes say these are "the values submitted by NESO to the
interconnector capacity calculation processes which restrict the maximum GB import and export
interconnector flows". The resource descriptions add that they are the restrictions submitted to
the day-ahead and intraday auctions. They are **NESO's input limits**, not measured flows and
not the link's final capacity. The package note says the final capacity also uses the connected
system operator's values and the interconnector's capability, so it "may be lower than the NESO
values shown here". The final values are published by each interconnector's trading facilitator,
not here.

**Direction (FACTS IC1-1).** `To GB` is **import** (foreign to GB) and `From GB` is **export**
(GB to foreign). Each column is a **directional MW maximum**. The two are not one signed net-flow
series. gridflow stores both as non-negative magnitudes in `flow_to_gb_mw` and `flow_from_gb_mw`,
never signed and never netted. A signed convention would be a separate derived definition
downstream.

**Absence and "No Restriction".** The package note says values are published only where NESO
applied a restriction: "If there are no values, NESO has not applied a restriction". The files
do not bear the first half out: they also list hours NESO marks `No Restriction` (bronze read
2026-10-24: in the 16 October current table 13,778 of 16,031 rows To GB and 9,823 From GB, both
on 8,628; in the daily archive 1,752 of 11,280; none in the weekly archive, which has 457 blank
reasons, or the intraday file). So a row is an hour NESO gave a limit for, restricted or not, and
an absent hour is only NESO's word for no restriction. It is not a zero limit, not the nameplate
capacity, and not something to reconstruct. gridflow synthesises no rows.

The far end of the link is not named in the NESO package. The batch research compared NemoLink
with ENTSO-E's GB/Belgium border (`10YGB----------A` / `10YBE----------2`). The agreement was
only partial. NESO's figure is one input to the final capacity, so the comparison neither proves
the two series equivalent nor makes them interchangeable (FACTS IC1-1).
`TODO: verify` the counterpart system operator from a NESO source.

The package holds three gridflow families:

- `nemolink_ntc`: the **current daily NTC dump** plus the **daily archive upload** of earlier
  restrictions, kept as two header epochs in one family.
- `nemolink_nemo_da_id_weekly_ntcs`: an **older weekly-packaged archive** of hourly limits.
- `nemolink_intraday`: a **one-off, undated 24-hour resource** named
  `NemoLink-Intraday1-20240127-001`.

**All three outputs are held (unit E-SEM)**, each for its own reason (see Holds). They exist in
silver but are not eligible for publication or point-in-time model use until E-SEM answers their
questions (RULINGS 565, 567). **This page gives schema, clocks and row counts only. It gives no
data values, sample rows or value statistics.**

- Publisher group: Interconnectors
- Registry group: interconnectors · archetype: FC

Package id `24b229de-2806-45a6-89a9-88097d67e5f2` (catalogue snapshot `20261006T195819Z`).
Package page: [NemoLink](https://www.neso.energy/data-portal/nemolink). Tags: NTC, Nemo Link,
Net Transfer Capacity, Net Transmission Capacity, Network Transfer Capacity, Subscribable.

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Archived Nemo DA & ID Weekly NTCs | CSV | upload | `ed977959-ccec-4cb6-b26f-c528863a243b` |
| Archived NemoLink NTC Data | CSV | upload | `f169676e-67ec-4f2f-befd-1863c713179c` |
| NemoLink NTC Data | CSV | dump | `7d43e2a0-1c22-4e05-895d-756bae210756` |
| NemoLink-Intraday1-20240127-001 | CSV | dump | `aae5acff-fd30-4c46-b996-a10e50cf4d50` |

All four resources are SILVER. The package has no DOC resources, so there is no methodology
file and no `_files` family. The URLs below come from the 2026-10-06 catalogue snapshot and
match the 2026-10-08 capture sidecars. The 2026-10-08 captures are under
`C:/gridflow-data/bronze/neso_data_portal/<family>/2026/10/08/`. Each body's hash and length match
its sidecar (FACTS C-VERIFY). The 2026-10-16 refresh captured the two datastore dumps again (under
`.../<family>/2026/10/16/`, same URLs in the sidecars) and skipped the two archives, whose CKAN
`last_modified` had not moved (gridflow `client.py` `iter_members`; read 2026-10-24).

- **NemoLink NTC Data** -> `nemolink_ntc`, epoch 1 (held). Datastore dump:
  [7d43e2a0-...](https://api.neso.energy/datastore/dump/7d43e2a0-1c22-4e05-895d-756bae210756).
  Captured `raw_20261008T111350Z_7d43e2a0-1c22-4e05-895d-756bae210756_08085f37.csv`,
  1,446,864 bytes, 15,623 rows. CKAN created `2024-09-23T10:53:22`, `last_modified`
  `2026-09-17T09:11:37.682451`.
- **Archived NemoLink NTC Data** -> `nemolink_ntc`, epoch 2 (held). Upload:
  [archived_nemolink_link_ntc_data.csv](https://api.neso.energy/dataset/24b229de-2806-45a6-89a9-88097d67e5f2/resource/f169676e-67ec-4f2f-befd-1863c713179c/download/archived_nemolink_link_ntc_data.csv).
  Captured `raw_20261008T111352Z_f169676e-67ec-4f2f-befd-1863c713179c_11d9c635.csv`,
  733,059 bytes, 11,280 rows. CKAN `last_modified` `2024-11-27T14:20:59.758228`.
- **Archived Nemo DA & ID Weekly NTCs** -> `nemolink_nemo_da_id_weekly_ntcs` (held). Upload:
  [archived_weekly_nemolink_link_ntc_data.csv](https://api.neso.energy/dataset/24b229de-2806-45a6-89a9-88097d67e5f2/resource/ed977959-ccec-4cb6-b26f-c528863a243b/download/archived_weekly_nemolink_link_ntc_data.csv).
  Captured `raw_20261008T111324Z_ed977959-ccec-4cb6-b26f-c528863a243b_e1ca07d4.csv`,
  58,041 bytes, 1,344 rows. CKAN `last_modified` `2024-11-27T14:25:06.891464`.
- **NemoLink-Intraday1-20240127-001** -> `nemolink_intraday` (held). Datastore dump:
  [aae5acff-...](https://api.neso.energy/datastore/dump/aae5acff-fd30-4c46-b996-a10e50cf4d50).
  Captured `raw_20261008T111320Z_aae5acff-fd30-4c46-b996-a10e50cf4d50_1a8ebc90.csv`,
  1,145 bytes, 24 rows. CKAN created `2026-04-15T15:00:40`, `last_modified` **null**
  (metadata_modified `2026-04-15T15:00:40.726688`).

All four resources are `datastore_active` in CKAN. The two archives have `url_type` `upload` and
are captured as file downloads. The two others are captured through the datastore dump. No
resource declares a CKAN `primary_key`. Upload filenames carry no date or issue token, so resolve
URLs from the CKAN resource and do not hard-code them.

## Families

### `nemolink_intraday`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Hourly Time Period (GMT) | `hourly_time_period` | string | — | yes | — | — |
| Flow (MW) To GB | `flow_to_gb_mw` | float64 | — | yes | — | MW |
| Flow (MW) From GB | `flow_from_gb_mw` | float64 | — | yes | — | MW |
| Reason For Reduction | `reason_for_restriction` | string | — | yes | — | — |

- Entity key: `hourly_time_period`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

**Held (unit E-SEM). Schema, clocks and counts only, no data values.**

**The two clocks for this family:**

1. **Vintage (`capture_fallback`).** The resource is a datastore dump, so `published_at` is
   **null** and `available_at` = the capture's `written_at`, `2026-10-08T11:13:20.602585Z`
   (gridflow `@docs/DECISION_LOG/ADR-035-neso-datastore-dump-leg.md` P-10). The resource has no
   CKAN `last_modified` at all (null in the catalogue, empty in the sidecar), so no vendor
   instant could be used even if the rule allowed one. The body has no issue column.
2. **Event time (`none`).** `timestamp_utc` = `event_time` = the **capture time**
   `2026-10-08T11:13:20.602585Z` on all 24 rows. **It is not the hour the limit applies to.**
   The body carries only a clock interval (`Hourly Time Period (GMT)`, kept as the raw string,
   e.g. the dictionary example `22:00 to 23:00`). It has no date, so no row can be placed on a
   calendar.

**Hold question.** The body has no date, and NESO documents neither the resource's lifecycle nor
the meaning of the date in its name (`20240127`). The name suggests a dated Intraday 1 snapshot,
but the body cannot confirm it. The daily archive has no rows labelled `20240127`, so nothing
corroborates the date (FACTS `nemolink_intraday`, IC1-5). The resource was created on
2026-04-15, long after its name's date. The `filename_token` issue recipe cannot read the date
because the sidecar `resource_filename` is the UUID. `TODO: verify` with NESO whether this is a
static historical example (then a DOC reclassification is a candidate) or a resource that is
refreshed, and what `20240127` and `-001` mean.

**Second capture (2026-10-16; bronze read 2026-10-24).**
`raw_20261016T204104Z_aae5acff-fd30-4c46-b996-a10e50cf4d50_d2eaa2ef.csv`, 1,145 bytes, 24 rows.
The 24 data rows are byte-identical to the 2026-10-08 body, but NESO renamed three column ids:
`Hourly Time Period GMT`, `Flow in MW To GB`, `Flow in MW From GB` (`Reason For Reduction`
unchanged). CKAN `last_modified` is still empty; `metadata_modified` moved to
`2026-10-09T08:21:47.747573`. So NESO does touch this resource, though its values did not change
between the two captures. The frozen record has one epoch, so the transform failed the capture
with `HeaderEpochError` and wrote nothing; silver keeps the 2026-10-08 capture (gridflow
`@.planning/phases/v0.22-close/refresh-20261016/DRIFT.md`, BACKLOG remediation row). Until a new
epoch is frozen, `gridflow transform neso_data_portal nemolink_intraday` exits non-zero on this
capture.

**Shape (counts only).** 24 rows, one per hourly interval, in file order from `23:00 to 00:00`
onwards. `hourly_time_period` was measured unique over the body. That is a capture guard only:
the label has no date, so it gives no identity across dates. `_latest` is `whole_capture`.
`TODO: verify` the vendor identity. No silver cell is null, both directions are populated on
every row, and no reason cell is blank (FACTS g5).

**Units (vendor dictionary only, CKAN field info for `aae5acff...`, read 2026-10-08).** Both
flow columns are **MW**, described as "Maximum flow in this direction" (dictionary type `int`,
CKAN `int4`). They are cast to float64, which leaves integers unchanged. The interval and reason
columns have unit `N/A`.

### `nemolink_nemo_da_id_weekly_ntcs`

- Kind: tabular · archetype: FC · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Operational Date (YYYY-MM-DD) & Time GMT/BST (HH:MM - HH:MM) | `operational_date_and_hour` | string | — | yes | — | — |
| Flow (MW) to GB | `flow_to_gb_mw` | float64 | — | yes | — | MW |
| Flow (MW) from GB | `flow_from_gb_mw` | float64 | — | yes | — | MW |
| Reason For Restriction | `reason_for_restriction` | string | — | yes | — | — |

- Entity key: `operational_date_and_hour`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held (unit E-SEM). Schema, clocks and counts only, no data values.**

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the capture's CKAN
   `last_modified`, `2024-11-27T14:25:06.891464`. CKAN emits it without an offset and gridflow
   reads it as UTC (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). All
   1,344 rows share it. The file has no issue column, so this upload instant is the only
   availability clock. **Every target in the file precedes it** (FACTS IC1-6: 1,344 rows before
   the vintage, 0 after), so this vintage is when the archive was uploaded, not when any limit
   was issued.
2. **Event time (`none`).** `timestamp_utc` = `event_time` = the **capture time**
   `2026-10-08T11:13:24.693034Z` on every row. **It is not the restricted hour.** The target is
   carried only by the raw combined label `operational_date_and_hour`, kept byte-identical
   (dictionary example `20221214 23:00 - 00:00`) and not converted to an instant.

**Hold question.** NESO does not document the archive's operational-date rollover or how the
"GMT/BST" header applies to each label. Each labelled day starts in file order at `23:00`, and no
calendar explains that. The autumn label
`20221030` has 24 intervals and no fold marker, so the clock change is not visible in the labels
(FACTS IC1-3). Every target also precedes the upload's `last_modified`, so the forward-target
rule (RULINGS 529) cannot release the file. `TODO: verify` the operational-day definition, the
zone of each label and the DST handling.

**"Weekly" is packaging, not grain (FACTS IC1-2).** Rows are hourly. The body has no week,
auction or issue column, and labelled dates fall on every weekday, so a row's date does not
identify a publication week. gridflow synthesises no week target. `TODO: verify` the weekly
publication calendar. The resource description names day-ahead and intraday auctions, but the
body does not say which auction a row belongs to.

**Shape (counts only).** 1,344 rows = 56 labelled operational days x 24 hourly rows. The exact
combined label was measured unique over the body, so the entity key is a capture guard and
`_latest` is `whole_capture`. `TODO: verify` the vendor identity. Coverage: the labels run from
October to mid-December 2022 and end on the first labelled day of the daily archive in
`nemolink_ntc`, so the two archives share 24 target labels. On those shared labels no
directional value pair is equal under either label interpretation tested (FACTS IC1-4). Their relationship is `TODO: verify`, and nothing joins
them.

**Units (vendor dictionary only, CKAN field info for `ed977959...`, read 2026-10-08).** Both
flow columns are **MW**, "Maximum flow in this direction". The dictionary type is `number` (CKAN
`numeric`), and the body carries non-integer MW figures, so float64 is required. An int64 typing
was caught and fixed in review before merge (RULINGS 566). The label and reason columns have
unit `N/A`.

**Vendor-documentation discrepancies.** The header says `Operational Date (YYYY-MM-DD)`, but
the dictionary example and the body labels use the compact `YYYYMMDD` form. The reason column
id is `Reason For Restriction`, while its dictionary title is `Reason For Reduction`. The flow
column ids use lower-case `to GB` / `from GB`, while the dictionary titles use `To GB` /
`From GB`. gridflow keys on the column ids and keeps the label raw, so none of these change the
silver output.

**Sentinels (FACTS g5).** No negative, `-1`, non-numeric or blank directional value, and no
literal `NA` / `N/A` cell. Zero limits occur and stay numeric zero. No vendor source defines zero
as missing, so a zero is never converted to null or filled. Blank reason cells become null
(457 rows have a null `reason_for_restriction`), and no reason is invented.

### `nemolink_ntc`

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

**Held (unit E-SEM). Schema, clocks and counts only, no data values.**

**Two resources, two epochs, one family.** Epoch 1 is the current dump `NemoLink NTC Data`
(header M in the batch FACTS). Epoch 2 is the upload `Archived NemoLink NTC Data` (header A).
Family membership fixes the bronze directory, so the family stays as registered (RULINGS 565).
`latest_partition: resource_id` (gridflow
`@docs/DECISION_LOG/ADR-039-neso-multi-resource-selection.md`) keeps the newest capture **per
resource**, so a new dump never displaces the archive or the other way round. A row carries its
own epoch's columns, and the other epoch's columns are null: every archive row has null
`data_upload_time_gmt`, `operational_period_start_gmt`, both directional reasons and
`issue_time`, and every dump row has null `operational_date`, `version`, `hourly_time_period`
and `reason_for_restriction`.

**The two clocks for this family:**

1. **Vintage (`capture_fallback`) for both resources.** `published_at` is **null** and
   `available_at` = the capture's `written_at`: `2026-10-08T11:13:50.731833Z` for the dump rows
   and `2026-10-08T11:13:52.336428Z` for the archive rows. A family holding a datastore resource
   must take `capture_fallback`, and that rule extends to the archive upload in the same family
   (ADR-035 P-10, the mixed-family case). That is honest, but much later than the archive's CKAN
   `last_modified` (`2024-11-27T14:20:59.758228`). The dump's CKAN `last_modified`
   (`2026-09-17T09:11:37.682451`, the column-rename date) is recorded in the sidecar but is not
   a row-level clock. **Issue label:** on dump rows, `issue_time` = `data_upload_time_gmt`, which
   the vendor dictionary defines as the "Date and time that data was published" (GMT, read as
   UTC; FACTS T01). It is in the entity key because the same target and auction recur across
   uploads. 651 distinct issue times are in the capture. Archive rows have no issue column, so
   their `issue_time` is null. `Version` is **not** an issue time and has no ordering meaning.
   **`available_at` is not backdated to `Data Upload Time GMT`** (FACTS g2, IC1-6).
2. **Event time (`none`).** `timestamp_utc` = `event_time` = the **capture time** on every row
   (the two `written_at` values above). **It is not the restricted hour.** The engine needs the
   temporal input in every epoch, and the archive has no `Operational Period Start` column, so
   the family cannot use `utc_instant` (FACTS T07). The target hour is carried in the data:
   - Dump rows: `operational_period_start_gmt`, a tz-aware UTC instant that starts the hour.
     The dictionary example `2022-10-20T22:00:00` means 22:00 to 23:00. The GMT reading is
     measured: on 2026-03-29 the distinct target hours give 24 per UTC date and 23 per
     Europe/London date (FACTS IC1-3, C-DST).
   - Archive rows: `operational_date` (raw label, all values parse `%Y%m%d`) plus
     `hourly_time_period` (raw interval text). Both are kept as strings, because the
     operational-date calendar is not documented.

**Hold question.** The dump returns past targets: 15,589 of its 15,623 rows target an hour
before the capture, and 1,652 target an hour before their own upload time. NESO does not state
that a row is unchanged since its `Data Upload Time GMT`, so the dump is not evidence of the
limits **as issued** at the time (FACTS g2). The archive's Operational Date calendar and rollover
and the meaning of `Version` are also undocumented (FACTS T03, T04). `TODO: verify` with NESO a
retention or revision guarantee for the dump (or immutable per-issue files), the archive's
operational-day definition, and what `Version` (`001`, `002`, ...) orders. (Counts are the
2026-10-08 capture; the 2026-10-16 capture has 16,005 of 16,031 targets before the capture and
1,684 before their own upload time.)

**Second capture of the dump (2026-10-16; bronze and silver read 2026-10-24).**
`raw_20261016T204134Z_7d43e2a0-1c22-4e05-895d-756bae210756_d91a1a0a.csv`, 1,484,249 bytes,
16,031 rows, the same post-rename header, CKAN `last_modified` still
`2026-09-17T09:11:37.682451`. Every one of the 15,623 rows of the 2026-10-08 body is present with
identical values (no key missing, no key with a changed value, no full row missing). 408 rows are
new, over 17 new upload times from `2026-10-08T16:10:04` to `2026-10-16T09:30:06` (eight at
09:30, seven at 20:11, one at 16:10, one at 10:30), for target hours `2026-10-07 22:00` to
`2026-10-17 21:00` UTC; 668 distinct upload times in all. So between these two captures NESO only
appended. That does not show rows are never revised, and the hold stands. Silver holds a third
Parquet file of 16,031 rows (`available_at` `2026-10-16T20:41:34.688010Z`), which `_latest` takes
for the dump's `resource_id`; the archive's 2026-10-08 file stays its latest.

**Shape and identity (counts only, 2026-10-08 capture).**

| Resource | Rows | Auction labels (raw spelling) |
|---|---:|---|
| `7d43e2a0...` dump | 15,623 | `Day Ahead`, `Intraday 1`, `Intraday 2`, `Intraday 3`, `Intraday 4` |
| `f169676e...` archive | 11,280 | `DayAhead`, `Intraday1`, `Intraday2`, `Intraday3`, `Intraday4` |

The two resources spell auctions differently, and gridflow keeps both spellings as they are. Do
not compact whitespace to join them without a vendor mapping. The archive carries 8 distinct
three-digit `Version` labels, kept as strings. The dump's grain
`(issue_time, auction_type, operational_period_start_gmt)` and the archive's grain
`(operational_date, auction_type, hourly_time_period)` were each measured unique over the full
body. The dump's `(auction_type, operational_period_start_gmt)` alone is **not** unique (48
duplicate rows), which is why `issue_time` is in the key (FACTS g3, T08). The entity key is the
union of both grains plus `resource_id`, and the other epoch's members are null on each row. It
is a capture guard, not a vendor identity. `TODO: verify` the vendor key.

**Coverage and overlap (FACTS IC1-4).** The archive's labelled operational dates run from
December 2022 to September 2024. The dump's UTC targets start in late September 2024 and run to
the day after capture. Under literal labels the two resources share no `(target, auction)` key,
and a hypothetical earlier-day rollover gives none either. A rollover is not adopted, so
canonical overlap stays `TODO: verify`. Resource partitioning keeps both; it does not decide
which wins on an overlap.

**Units.** Dump: both flow columns are **MW**, "Maximum flow in this direction" (current
dictionary, CKAN field info for `7d43e2a0...`, read 2026-10-08; type `integer`, CKAN `int4`).
Archive: the batch research reads the archive's vendor dictionary
([archived NemoLink NTC data](https://www.neso.energy/data-portal/nemolink/archived_nemolink_ntc_data))
as directional **MW** maxima (FACTS T05, T06). The epoch-2 table above shows `—` because the
field-info snapshot covers only the family's newest datastore resource, so the generator had no
archive dictionary to read. `TODO: verify` that the generated unit column picks up the archive
dictionary. `Data Upload Time GMT` and `Operational Period Start Date and Time GMT` have unit
`ISO 8601`. Auction, reason and Version have no physical unit. Version is typed integer by the
vendor but has no stated meaning, so it stays a raw string.

**Vendor-documentation discrepancies.** The current dictionary's titles still use the pre-rename
names (`Data Upload Time (GMT)`, `Flow (MW) To GB`), while the column ids use the post-rename
names. The resource note dates the rename to 2026-09-17, and only the post-rename header was
captured, so gridflow records no earlier dump epoch (FACTS IC1-4). The dictionary example for
`Auction Type` is `Intraday2`, while the dump body spells it `Intraday 2`.

**Sentinels (FACTS g5).** No negative, `-1`, non-numeric or blank directional value, and no
literal `NA` / `N/A` cell, in either resource. Zero limits occur in both directions, including
multi-day runs, and stay numeric zero. Nothing becomes null, nameplate or a filled value. The
captures also contain explicit `No Restriction` reason text, which is kept as text. Neither
resource has blank reason cells, so every null reason in silver is the other epoch's column.

**Activation (2026-10-09, master `6cccc4e`).** Cutoff 2026-10-08, no prior silver: **26,903 rows**
(15,623 + 11,280), equal to the planned count. `nemolink_intraday` **24** and
`nemolink_nemo_da_id_weekly_ntcs` **1,344** also equal planned. Each family's captures sit
under `C:/gridflow-data/silver/neso_data_portal/<family>/year=2026/month=10/`, one Parquet file
per capture (two for `nemolink_ntc`). `reconcile --all --cutoff 2026-10-08` exited 0 over 69
families with 0 gaps (gridflow `@.planning/v0.22-RESULTS.md` section IC-1; RULINGS 566, 567).

Silver columns beyond the vendor columns, in every family: `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version`. `nemolink_ntc` also carries `issue_time` and `resource_id`. All timestamps
are tz-aware UTC. `dataset_version` is `1+e1` on every row of all three families: record version
1 plus generic **engine** version 1 (`silver/neso_data_portal/generic.py`), not the header
epoch. Archive rows of `nemolink_ntc` also read `1+e1`.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Daily

"Daily" is the package-level statement, and it fits the current dump, which carries several
intraday auctions per day. The two archives are fixed uploads (`last_modified` 2024-11-27, the
same day as their creation) and look static; neither moved by the 2026-10-16 refresh. The
one-off resource has no `last_modified`, but its column ids were renamed by 2026-10-16 (see
`nemolink_intraday`). The dump's new upload times between the 2026-10-08 and 2026-10-16
captures fall mostly at 09:30 and 20:11 GMT (see the second capture under `nemolink_ntc`).
`TODO: verify` whether the archives and the one-off are ever re-issued, and the dump's update
times. For the sibling NSL dump, the batch research found upload-time labels consistent with a
fixed UK-local schedule expressed in GMT. That is an inference, not an availability contract,
and it was not measured for NemoLink (FACTS IC1-3).
gridflow's refresh keeps one state per run, so the dated silver captures sample the vendor's
history and do not hold all of it. No scheduled gridflow refresh exists yet, and captures are
on demand.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `nemolink_intraday`: held: TODO: the body has no date, and the resource's lifecycle and the date in its name are undocumented. (unit E-SEM)
- `nemolink_nemo_da_id_weekly_ntcs`: held: TODO: the archive's operational-date rollover and GMT/BST interpretation are undocumented, and every target precedes the upload's last_modified, so the forward-target rule (RULINGS 529) cannot apply. (unit E-SEM)
- `nemolink_ntc`: held: TODO: the dump returns past targets (rows before the capture) and NESO does not state that a row is unchanged since its `Data Upload Time GMT`, so historical issued limits are not evidenced, and the archive's Operational Date calendar / rollover and Version meaning are undocumented. (unit E-SEM)

The held outputs exist in silver but are not eligible for publication or point-in-time model use
until unit E-SEM answers their questions (RULINGS 565, 567). This page publishes schema, clocks
and row counts only. It gives no data value, sample row or value statistic for any of the three
families. The evidence for each hold is in gridflow
`@.planning/phases/v0.22-K-IC-1/K-IC-1-FACTS.md` (§2 per family, §3 g1–g5, §4 IC1-1 to IC1-6).
Related interconnector packages in the same batch: @eleclink.md, @nsl.md, @ifa.md, @ifa2.md,
@viking.md.
