---
source: "neso_data_portal"
package: "ancillary-services-important-industry-notifications"
dataset_keys: ["as_industry_notifications_balancing", "as_industry_notifications_dc_dm_dr", "as_industry_notifications_quick_reserve", "as_industry_notifications_sffr_important", "as_industry_notifications_slow_reserve", "as_industry_notifications_stor_important"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-18
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Ancillary services industry notifications
  summary: >-
    NESO's notices on changes to ancillary-service procurement: raised requirements, delayed or
    failed auctions, outages and archived files, one file per service group.
  facts:
    vendor: "NESO Data Portal, package `ancillary-services-important-industry-notifications`: six uploaded CSV files"
    cadence: Ad hoc, as NESO's catalogue states; gridflow downloads each file whole
    grain: "One row per notice: issue time, effective times and free text"
    history: Notices issued from March 2024 in NESO's STOR and DC/DM/DR files
  landscape: market
  what_it_is: >-
    NESO posts a notice when ancillary-service procurement changes: a raised requirement, a delayed
    or failed auction, a platform outage, an archived file. Each row gives when NESO issued it, when
    it starts and may stop, and free text. Each service or group has a file, and one notice is
    often posted to several, sometimes reworded. NESO gives no notice id.
  how_used:
    - "Flags for auction days NESO called unusual: raised requirements, delays, failed auctions."
    - Dates when an enduring change took effect, for requirement and auction series.
    - "Point-in-time work: treat a notice as known from `published_at`, the file's vintage."
  chart:
    type: bar
    silver: neso_data_portal/as_industry_notifications_dc_dm_dr
    filter:
      - {column: published_at, op: eq, value: "2026-08-19T15:12:17.130148"}
    group: service
    group_map: {"DC, DM, DR": all_three, DM: dm, DC: dc, "DM, DR": dm_dr, "DC, DM": dc_dm}
    aggregation: count
    sort: value_desc
    unit: notices
  chart_view:
    title: DC, DM and DR notices by service label
    caption: >-
      Silver `as_industry_notifications_dc_dm_dr`, one member of this family: every notice in
      NESO's file last modified 19 August 2026, counted by its `service` value. A combined label is
      one value as NESO writes it, not split into services.
    alt: >-
      Horizontal bar chart counting notices by service label in
      neso_data_portal/as_industry_notifications_dc_dm_dr, NESO's file last modified 19 August 2026.
      The combined label DC, DM, DR has 12 notices, DM alone 11, DC alone 3, and DC, DM and DM, DR
      one each.
    key:
      - {series: all_three, label: "DC, DM and DR", codes: "DC, DM, DR", paint: hatch-lines, note: "Mostly auction-result delays, new columns, EAC outages and archiving."}
      - {series: dm, label: DM alone, codes: DM, paint: petrol, note: "Dynamic Moderation: here each one raises the DM requirement, for one auction or onwards."}
      - {series: dc, label: DC alone, codes: DC, paint: petrol, note: "Dynamic Containment: two Data Portal maintenance notices and one raised DC requirement."}
      - {series: dc_dm, label: DC and DM, codes: "DC, DM", paint: hatch-lines, note: "An extra 100 MW of DC and DM in the 29 May 2026 auction."}
      - {series: dm_dr, label: DM and DR, codes: "DM, DR", paint: hatch-lines, note: "DM raised to 300 MW and DR to 480 MW, from 3 February 2025 delivery."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then each file downloaded whole unless its
      `last_modified` is unchanged. Dates select nothing. Swap in any member's key.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=ancillary-services-important-industry-notifications"
    commands:
      - {run: gridflow ingest neso_data_portal as_industry_notifications_balancing --last 24h, comment: "whole file; window must end recently"}
      - {run: gridflow transform neso_data_portal as_industry_notifications_balancing --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      silver: neso_data_portal/as_industry_notifications_balancing
      filter:
        - {column: published_at, op: eq, value: "2026-09-04T10:50:39.380805"}
        - {column: timestamp_utc, op: ge, value: "2026-03-26T00:00:00Z"}
      order_by: [notification_issued_date_time]
      columns: [notification_issued_date_time, effective_from_date_time, effective_to_date_time, service, notes,
                description, published_at, timestamp_utc]
    key: [notification_issued_date_time]
    caption: "The eight newest notices in NESO's Balancing Reserve file, last modified 4 September 2026."
    fields:
      notification_issued_date_time: "When NESO issued the notice, UK local time in the file, as UTC"
      effective_from_date_time: "When the notice takes effect (NESO), UK local time converted to UTC"
      effective_to_date_time: "When NESO expects it to stop applying, as UTC; blank cells kept null"
      service: "The service it concerns, as NESO writes it; `BR` in these rows"
      notes: "NESO's free-text note; three 2025 notes in this file sit one row off"
      description: The notice itself, NESO's free text, kept exactly as written
      published_at: "NESO's last-modified time for the whole file, as UTC; can precede an issue time"
      timestamp_utc: "The issue time again, in UTC: the column `query()` filters on"
      bronze_capture_id: Path of the bronze capture the row was read from
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `query()` reads each table's `_latest` view, filtering `timestamp_utc`, the issue time, by UTC
      day, both ends included; times come back in the machine's zone, UK here. The next cell finds
      issue times several files share.
    cells:
      - |
        import pandas as pd
        files = ["balancing", "dc_dm_dr", "quick_reserve", "slow_reserve", "stor_important"]
        frames = []
        for f in files:
            t = data.neso_data_portal.query("as_industry_notifications_" + f, "2024-01-01", "2026-09-30")
            frames.append(t.assign(file=f))
        df = pd.concat(frames, ignore_index=True)
        df.groupby("file").tail(1)[["file", "notification_issued_date_time", "effective_from_date_time", "notes"]]
      - |
        shared = df.groupby("notification_issued_date_time", as_index=False).agg(
            files=("file", "nunique"), texts=("description", "nunique"), which=("file", ", ".join))
        shared[shared.files > 1].tail(6)
      - |
        import matplotlib.pyplot as plt, matplotlib.dates as mdates
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.scatter(df.notification_issued_date_time, df.file, marker="|", s=300, color="#155A6E")
        ax.xaxis.set_major_locator(mdates.MonthLocator((1, 7)))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        ax.set_xlabel("notice issued");
    needs: one capture of each file except SFFR's
    plot_alt: >-
      Strip plot of issue times, one tick per notice, for the five files from March 2024 to
      September 2026. STOR's ticks end in April 2025 and Slow Reserve's begin in March 2026. Ticks
      line up across files where one notice was posted to several, most often DC/DM/DR with Quick
      Reserve.
  related:
    - {dataset: neso_data_portal/eac-auction-results, note: "The daily EAC auctions most of these notices are about"}
    - {dataset: neso_data_portal/dynamic-moderation-requirements, note: The DM requirement that many DC/DM/DR notices raise}
    - {dataset: neso_data_portal/balancing-reserve-auction-requirement-forecast, note: "The PBR and NBR requirement some Balancing Reserve notices change"}
    - {dataset: neso_data_portal/short-term-operating-reserve-stor-day-ahead-auction-results, note: The STOR auctions whose delays and failures the STOR file reports}
  family:
    slug: ancillary-services-important-industry-notifications
    members:
      - dataset: as_industry_notifications_balancing
        differs: "Balancing Reserve: requirement changes, EAC outages, negative-reserve valuation days; `service` `BR`"
        request: "GET https://api.neso.energy/dataset/fc8dadc7-235d-44b0-bab2-320dc76095de/resource/13f8f6b1-690b-4695-993e-dbc26f9bbe54/download/balancing-reserve-important-industry-notifications.csv"
      - dataset: as_industry_notifications_dc_dm_dr
        differs: "Dynamic Containment, Moderation and Regulation; one `service` value can name several"
        request: "GET https://api.neso.energy/dataset/fc8dadc7-235d-44b0-bab2-320dc76095de/resource/5d6c5cf8-7f18-43d9-ab8c-ba3f88352f30/download/dc-dm-dr-important-industry-notifications.csv"
      - dataset: as_industry_notifications_quick_reserve
        differs: "Quick Reserve; no `service` column; often issued with the DC/DM/DR notices"
        request: "GET https://api.neso.energy/dataset/fc8dadc7-235d-44b0-bab2-320dc76095de/resource/a72085a8-e167-406d-8504-ed72d7e142af/download/qr-important-industry-notifications.csv"
      - dataset: as_industry_notifications_slow_reserve
        differs: "Slow Reserve; no `service` column; NESO's file starts 26 March 2026"
        request: "GET https://api.neso.energy/dataset/fc8dadc7-235d-44b0-bab2-320dc76095de/resource/11a90fe4-27c1-46b5-9619-016f2752413d/download/sr-important-industry-notifications.csv"
      - dataset: as_industry_notifications_stor_important
        differs: "Mostly STOR auction delays and failures; can take effect before its issue time"
        request: "GET https://api.neso.energy/dataset/fc8dadc7-235d-44b0-bab2-320dc76095de/resource/1dbebd85-6b42-4d8f-8542-16a83d17dc14/download/stor-important-industry-notifications.csv"
      - dataset: as_industry_notifications_sffr_important
        differs: Static FFR notices, same columns as Balancing Reserve
        request: "GET https://api.neso.energy/dataset/fc8dadc7-235d-44b0-bab2-320dc76095de/resource/9b51636d-fca5-4d00-946b-4e19770f1904/download/sffr-important-industry-notifications.csv"
        held: 'One row: blank description, note "Example note", dates that could be day or month first.'
---

# Ancillary Services Important Industry Notifications

NESO's running log of **important notices about changes to ancillary-services procurement**.
The vendor describes the package as the latest update on important ancillary-services
procurement changes, and asks users to subscribe to be told of new ones. Each row is one
notice: when it was issued, which service it concerns, a free-text description, the date and
time it takes effect, the date and time it is expected to stop applying, and a free-text note.
The package holds **six CSV files, one per service line**: Balancing Reserve, DC/DM/DR
(Dynamic Containment, Dynamic Moderation, Dynamic Regulation), Quick Reserve, SFFR (Static Firm
Frequency Response), Slow Reserve and STOR (Short Term Operating Reserve). gridflow maps each file
to its own family; matching headers across the files do not authorise merging them.

This is a **text event log, not a numeric series**. There is nothing to plot. Its value to a model
is as a dated record of market-design and procurement events, for example an EAC archiving
change or a notice that negative-reserve valuation is expected to be non-zero on named auction
days. Use it to explain regime changes in the auction and requirement datasets, and to flag days
whose prices or volumes may be unusual. The reserve-service and balancing context is in
@../../../20-domain/markets/gb-balancing-mechanism.md.

The package is small and slow-moving: the six captures hold **67 eligible rows and one held row**
in total, and the vendor refreshes them ad hoc (see Cadence). Five families are eligible. The
SFFR family is **held**: its output is not published, and this page shows none of its values
(see Holds).

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Balancing Reserve Important Industry Notifications | CSV | upload | `13f8f6b1-690b-4695-993e-dbc26f9bbe54` |
| DC, DM, DR Important Industry Notifications | CSV | upload | `5d6c5cf8-7f18-43d9-ab8c-ba3f88352f30` |
| Quick Reserve Important Industry Notifications | CSV | upload | `a72085a8-e167-406d-8504-ed72d7e142af` |
| SFFR Important Industry Notifications | CSV | upload | `9b51636d-fca5-4d00-946b-4e19770f1904` |
| STOR Important Industry Notifications | CSV | upload | `1dbebd85-6b42-4d8f-8542-16a83d17dc14` |
| Slow Reserve Important Industry Notification | CSV | upload | `11a90fe4-27c1-46b5-9619-016f2752413d` |

There are **no DOC or other-disposition resources** in this package: all six are CSV uploads and
all six go to silver. Download links are the URLs in the 2026-10-06 catalogue snapshot. The
stable handle is the resource id, not the file name.

| Family | Download | Newest capture (2026-10-08) | Bytes | Data rows | Eligibility |
|---|---|---|---:|---:|---|
| `as_industry_notifications_balancing` | [balancing-reserve-important-industry-notifications.csv](https://api.neso.energy/dataset/fc8dadc7-235d-44b0-bab2-320dc76095de/resource/13f8f6b1-690b-4695-993e-dbc26f9bbe54/download/balancing-reserve-important-industry-notifications.csv) | `raw_20261008T081601Z_13f8f6b1-690b-4695-993e-dbc26f9bbe54_5e93ae28.csv` | 5,507 | 13 | eligible |
| `as_industry_notifications_dc_dm_dr` | [dc-dm-dr-important-industry-notifications.csv](https://api.neso.energy/dataset/fc8dadc7-235d-44b0-bab2-320dc76095de/resource/5d6c5cf8-7f18-43d9-ab8c-ba3f88352f30/download/dc-dm-dr-important-industry-notifications.csv) | `raw_20261008T081606Z_5d6c5cf8-7f18-43d9-ab8c-ba3f88352f30_619f429b.csv` | 12,006 | 28 | eligible |
| `as_industry_notifications_quick_reserve` | [qr-important-industry-notifications.csv](https://api.neso.energy/dataset/fc8dadc7-235d-44b0-bab2-320dc76095de/resource/a72085a8-e167-406d-8504-ed72d7e142af/download/qr-important-industry-notifications.csv) | `raw_20261008T081611Z_a72085a8-e167-406d-8504-ed72d7e142af_5a7c2ece.csv` | 5,597 | 13 | eligible |
| `as_industry_notifications_sffr_important` | [sffr-important-industry-notifications.csv](https://api.neso.energy/dataset/fc8dadc7-235d-44b0-bab2-320dc76095de/resource/9b51636d-fca5-4d00-946b-4e19770f1904/download/sffr-important-industry-notifications.csv) | `raw_20261008T081615Z_9b51636d-fca5-4d00-946b-4e19770f1904_437edca5.csv` | 176 | 1 | **held** |
| `as_industry_notifications_slow_reserve` | [sr-important-industry-notifications.csv](https://api.neso.energy/dataset/fc8dadc7-235d-44b0-bab2-320dc76095de/resource/11a90fe4-27c1-46b5-9619-016f2752413d/download/sr-important-industry-notifications.csv) | `raw_20261008T081621Z_11a90fe4-27c1-46b5-9619-016f2752413d_68b9895a.csv` | 1,537 | 4 | eligible |
| `as_industry_notifications_stor_important` | [stor-important-industry-notifications.csv](https://api.neso.energy/dataset/fc8dadc7-235d-44b0-bab2-320dc76095de/resource/1dbebd85-6b42-4d8f-8542-16a83d17dc14/download/stor-important-industry-notifications.csv) | `raw_20261008T081624Z_1dbebd85-6b42-4d8f-8542-16a83d17dc14_5e5108a0.csv` | 2,486 | 9 | eligible |

Bronze path pattern: `C:/gridflow-data/bronze/neso_data_portal/<family>/2026/10/08/<file>`. Each
family has exactly **one** capture and **one** resource so far. Every body passed strict UTF-8
validation and its SHA-256 matched its sidecar; there are no ragged rows and no all-blank rows
(gridflow `@.planning/phases/v0.22-K-AS-2/K-AS-2-FACTS.md` §2, C04). Bytes and rows are
measured from the bodies, not copied from the catalogue. No capture is header-only, and every
family's registry setting is `empty allowed: no`.

## Families

The six files share two header shapes and one observed header epoch each. The Balancing Reserve,
DC/DM/DR, SFFR and STOR files carry six columns including `Service`. The Quick Reserve and Slow
Reserve files carry five columns and **have no `Service` column**; gridflow does not add one. These
are two shared shapes, not a chronological schema change. No file has a notification id, a
separate publication timestamp or a last-updated column.

### `as_industry_notifications_balancing`

- Kind: tabular · archetype: EVT · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Notification Issued Date Time | `notification_issued_date_time` | datetime | `%d/%m/%Y %H:%M` | no | Europe/London | YYYY-MM-DDTHH:MM:SS |
| Service | `service` | string | — | yes | — | — |
| Description | `description` | string | — | yes | — | — |
| Effective From Date Time | `effective_from_date_time` | datetime | `%d/%m/%Y %H:%M` | no | Europe/London | YYYY-MM-DDTHH:MM:SS |
| Effective To Date Time | `effective_to_date_time` | datetime | `%d/%m/%Y %H:%M` | yes | Europe/London | YYYY-MM-DDTHH:MM:SS |
| Notes | `notes` | string | — | yes | — | — |

- Entity key: `notification_issued_date_time`
- Latest: `whole_capture`
- Temporal recipe: local_instant (`notification_issued_date_time`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Eligible.** 13 silver rows. `service` is `BR` on all 13. Issue labels run from
`2024-03-29T09:00Z` to `2026-09-04T11:00Z` (silver UTC). Blanks: Effective To 12, Notes 8. Four
rows take effect after their issue label and nine at the same minute. The Description column has
one embedded newline, 11 comma-bearing cells and one padded cell, all kept byte-equal.

**The two clocks.**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN `last_modified`
   of the capture, `2026-09-04T10:50:39.380805` (offset-less in CKAN, read as UTC; gridflow
   `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). All 13 rows share it.
2. **Event time (`local_instant` on `notification_issued_date_time`).** `timestamp_utc` =
   `event_time` = the issue label read as UK local time and converted to UTC. Checked equal on
   every silver row on 2026-10-13. It is **not** the capture time.

### `as_industry_notifications_dc_dm_dr`

- Kind: tabular · archetype: EVT · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Notification Issued Date Time | `notification_issued_date_time` | datetime | `%d/%m/%Y %H:%M` | no | Europe/London | YYYY-MM-DDTHH:MM:SS |
| Service | `service` | string | — | yes | — | — |
| Description | `description` | string | — | yes | — | — |
| Effective From Date Time | `effective_from_date_time` | datetime | `%d/%m/%Y %H:%M` | no | Europe/London | YYYY-MM-DDTHH:MM:SS |
| Effective To Date Time | `effective_to_date_time` | datetime | `%d/%m/%Y %H:%M` | yes | Europe/London | YYYY-MM-DDTHH:MM:SS |
| Notes | `notes` | string | — | yes | — | — |

- Entity key: `notification_issued_date_time`
- Latest: `whole_capture`
- Temporal recipe: local_instant (`notification_issued_date_time`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Eligible.** 28 silver rows. `service` has five distinct values, kept as strings: `DC` (3),
`DM` (11), `DC, DM, DR` (12), `DC, DM` (1), `DM, DR` (1). Combined labels are one value, not
a list; do not split them. Issue labels run from `2024-03-11T10:00Z` to `2026-08-19T15:15Z`.
Blanks: Effective To 16, Notes 4. Service has 14 comma-bearing cells; Description has 23
comma-bearing cells and one cell containing a literal quote, plus Unicode punctuation and spacing
(valid UTF-8). All kept byte-equal. Eighteen rows take effect after their issue label and ten at
the same minute.

**The two clocks.**

1. **Vintage (`ckan_last_modified`).** `2026-08-19T15:12:17.130148`, read as UTC, shared by all 28
   rows.
2. **Event time (`local_instant`).** The issue label as UK local time in UTC. Checked equal to
   `timestamp_utc` and `event_time` on every row. Not the capture time.

### `as_industry_notifications_quick_reserve`

- Kind: tabular · archetype: EVT · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Notification Issued Date Time | `notification_issued_date_time` | datetime | `%d/%m/%Y %H:%M` | no | Europe/London | YYYY-MM-DDTHH:MM:SS |
| Description | `description` | string | — | yes | — | — |
| Effective From Date Time | `effective_from_date_time` | datetime | `%d/%m/%Y %H:%M` | no | Europe/London | YYYY-MM-DDTHH:MM:SS |
| Effective To Date Time | `effective_to_date_time` | datetime | `%d/%m/%Y %H:%M` | yes | Europe/London | YYYY-MM-DDTHH:MM:SS |
| Notes | `notes` | string | — | yes | — | — |

- Entity key: `notification_issued_date_time`
- Latest: `whole_capture`
- Temporal recipe: local_instant (`notification_issued_date_time`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Eligible.** 13 silver rows; no `service` column. Issue labels run from `2024-12-20T15:00Z`
to `2026-08-19T15:15Z`. Blanks: Effective To 12, Notes 1. Description has 11 comma-bearing cells
and one cell containing a literal quote. Five rows take effect after their issue label and eight
at the same minute.

**The two clocks.**

1. **Vintage (`ckan_last_modified`).** `2026-08-19T15:11:33.729145`, read as UTC, shared by all 13
   rows.
2. **Event time (`local_instant`).** The issue label as UK local time in UTC; equal to
   `timestamp_utc` and `event_time` on every row. Not the capture time.

### `as_industry_notifications_sffr_important`

- Kind: tabular · archetype: EVT · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Notification Issued Date Time | `notification_issued_date_time` | string | — | no | — | YYYY-MM-DDTHH:MM:SS |
| Service | `service` | string | — | yes | — | — |
| Description | `description` | string | — | yes | — | — |
| Effective From Date Time | `effective_from_date_time` | string | — | yes | — | YYYY-MM-DDTHH:MM:SS |
| Effective To Date Time | `effective_to_date_time` | string | — | yes | — | YYYY-MM-DDTHH:MM:SS |
| Notes | `notes` | string | — | yes | — | — |

- Entity key: `notification_issued_date_time`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Held.** 1 silver row. The silver output exists on disk but is not cleared for publication, and
**this page gives none of its values** (see Holds). Because the slash-date order of its timestamp
labels is unresolved, all three timestamp columns stay **raw strings** and there is no parsed
instant.

**The two clocks.**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN `last_modified`
   of the capture, `2024-03-01T10:05:43.277634` (read as UTC).
2. **Event time: none.** The recipe is `none`, so `timestamp_utc` = `event_time` = the capture
   time (`capture_written_at`, 2026-10-08T08:16:15Z; checked equal on the row on 2026-10-13). It
   says nothing about when the notice was issued or takes effect. A consumer must not read
   `timestamp_utc` here as an event time.

### `as_industry_notifications_slow_reserve`

- Kind: tabular · archetype: EVT · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Notification Issued Date Time | `notification_issued_date_time` | datetime | `%d/%m/%Y %H:%M` | no | Europe/London | YYYY-MM-DDTHH:MM:SS |
| Description | `description` | string | — | yes | — | — |
| Effective From Date Time | `effective_from_date_time` | datetime | `%d/%m/%Y %H:%M` | no | Europe/London | YYYY-MM-DDTHH:MM:SS |
| Effective To Date Time | `effective_to_date_time` | datetime | `%d/%m/%Y %H:%M` | yes | Europe/London | YYYY-MM-DDTHH:MM:SS |
| Notes | `notes` | string | — | yes | — | — |

- Entity key: `notification_issued_date_time`
- Latest: `whole_capture`
- Temporal recipe: local_instant (`notification_issued_date_time`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Eligible.** 4 silver rows; no `service` column. Issue labels run from `2026-03-26T14:45Z` to
`2026-08-19T15:15Z`. Blanks: Effective To 3, Notes 3. Description has three comma-bearing cells.
One row takes effect after its issue label and three at the same minute.

**The two clocks.**

1. **Vintage (`ckan_last_modified`).** `2026-08-19T15:11:10.135838`, read as UTC, shared by all 4
   rows.
2. **Event time (`local_instant`).** The issue label as UK local time in UTC; equal to
   `timestamp_utc` and `event_time` on every row. Not the capture time.

### `as_industry_notifications_stor_important`

- Kind: tabular · archetype: EVT · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Notification Issued Date Time | `notification_issued_date_time` | datetime | `%d/%m/%Y %H:%M` | no | Europe/London | YYYY-MM-DDTHH:MM:SS |
| Service | `service` | string | — | yes | — | — |
| Description | `description` | string | — | yes | — | — |
| Effective From Date Time | `effective_from_date_time` | datetime | `%d/%m/%Y %H:%M` | no | Europe/London | YYYY-MM-DDTHH:MM:SS |
| Effective To Date Time | `effective_to_date_time` | datetime | `%d/%m/%Y %H:%M` | yes | Europe/London | YYYY-MM-DDTHH:MM:SS |
| Notes | `notes` | string | — | yes | — | — |

- Entity key: `notification_issued_date_time`
- Latest: `whole_capture`
- Temporal recipe: local_instant (`notification_issued_date_time`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Eligible.** 9 silver rows. `service` is `STOR` on all 9. Issue labels run from
`2024-03-01T10:00Z` to `2025-04-01T08:00Z`. Blanks: Effective To 3, Notes 2. Description has two
comma-bearing cells and Notes has three. This is the one family where effective-from can **precede**
the issue label (2 of 9 rows; 7 take effect after). Effective-from alone is not unique here (8
distinct values in 9 rows); the issue label is (9 distinct).

**The two clocks.**

1. **Vintage (`ckan_last_modified`).** `2025-04-01T07:32:28.323998`, read as UTC, shared by all 9
   rows.
2. **Event time (`local_instant`).** The issue label as UK local time in UTC; equal to
   `timestamp_utc` and `event_time` on every row. Not the capture time.

## Time semantics shared by all six families

**Clocks in the file.** The vendor dictionary states `UK local time` for the issue, effective-from
and effective-to columns. The captured CSVs spell them **day-first with no seconds and no offset**
(`%d/%m/%Y %H:%M`), not in the dictionary's ISO example (`YYYY-MM-DDTHH:MM:SS`). The "Vendor unit"
column above is that dictionary format string, not a physical unit. For the five typed families
gridflow parses with `Europe/London`, `ambiguous: raise`. In the captured bodies no label falls
in a repeated or skipped local hour, so nothing was rejected. The zone evidence is the vendor
dictionary (K-AS-2 FACTS §3).

**Issue time is not an availability instant (`issue: none`).** The record exposes no `issue_time`.
For the newest row of every eligible family, the issue label converts to an instant **later than the
file's CKAN `last_modified`**, by 560.6 s (Balancing Reserve), 162.9 s (DC/DM/DR), 206.3 s (Quick
Reserve), 229.9 s (Slow Reserve) and 1,651.7 s (STOR). So in silver the newest row of each of those
five families has `available_at` earlier than `timestamp_utc`. This is expected under this record,
not corruption: `available_at` is the vintage of the whole file, and the issue label is the
vendor's own, unverified label for when the notice was issued (seat ruling over the research
proposal, RULINGS 727). These are event tables, not forecasts, so the forward-target rule
(RULINGS 529) does not apply.

**Whole-capture selection.** `_latest` takes the newest whole capture of each file, so every row
of a family shares one `published_at`/`available_at`, the vintage of that upload. A point-in-time
query `WHERE available_at <= :as_of` therefore returns the whole file or none of it, never "the
notices issued by then". To reconstruct what was known at an issue label, filter on
`timestamp_utc` yourself and accept that the upload may postdate it. `TODO: verify` whether the
vendor appends in place, amends rows or removes expired notices: each family has one capture
only, so no revision behaviour has been measured.

**End time.** `Effective To Date Time` is "expected to become inactive". The vendor does not say
whether the end is inclusive or exclusive. gridflow keeps the endpoint as given.
`TODO: verify` interval closure. A blank end is kept null; the vendor does not say that a blank
means open-ended. `TODO: verify`.

## Units, nulls and text

- **Units.** None. Every column is a timestamp or free text. The vendor gives no physical unit,
  and none is inferred. Nothing is extracted from `Description` or `Notes` into numeric columns.
- **Nulls.** Blank cells are kept as nulls (counts per family above). No sentinel token (`-1`,
  `NA`, `N/A`) occurs in any body, so no null-token map is configured (K-AS-2 FACTS g5). A blank
  does not mean zero.
- **Free text is byte-equal.** Embedded newlines, quotes, commas, padding, and Unicode punctuation
  survive. The reader was checked against an independent parse of every row: all ordered cells
  agree (FACTS g6, C06).
- **Dictionary quirk.** The dictionary gives `DC, DM, DR` as the example value of `Description` in
  five of the six files (Slow Reserve's example is blank), although that is a service label. It
  gives `N/A` as the `Service` example in all four files that have a `Service` column. Trust the
  data, not the examples.

## Silver sample

Slow Reserve, the shortest eligible family (2 of 4 rows; silver timestamps are tz-aware UTC;
the `bronze_capture_id`, `capture_written_at`, `source_run_id` and `dataset_version` columns are
omitted for width). Notice the `available_at` of the second row is earlier than its
`timestamp_utc`.

```python
[
    {
        "notification_issued_date_time": datetime(2026, 4, 24, 11, 0, tzinfo=UTC),
        "description": "Please note for EAC auctions on 24/04/2026 and 25/04/2026 (delivery days 25/04/2026 and 26/04/2026), we forsee underlying systems conditions indicating a non-zero valuation of negative reserve",
        "effective_from_date_time": datetime(2026, 4, 24, 11, 0, tzinfo=UTC),
        "effective_to_date_time": None,
        "notes": None,
        "timestamp_utc": datetime(2026, 4, 24, 11, 0, tzinfo=UTC),
        "event_time": datetime(2026, 4, 24, 11, 0, tzinfo=UTC),
        "published_at": datetime(2026, 8, 19, 15, 11, 10, 135838, tzinfo=UTC),
        "available_at": datetime(2026, 8, 19, 15, 11, 10, 135838, tzinfo=UTC),
    },
    {
        "notification_issued_date_time": datetime(2026, 8, 19, 15, 15, tzinfo=UTC),
        "description": "The EAC sell orders for August and September will be archived on 1st October. There will be no archiving activity during September.",
        "effective_from_date_time": datetime(2026, 8, 19, 15, 15, tzinfo=UTC),
        "effective_to_date_time": datetime(2026, 10, 1, 16, 0, tzinfo=UTC),
        "notes": None,
        "timestamp_utc": datetime(2026, 8, 19, 15, 15, tzinfo=UTC),
        "event_time": datetime(2026, 8, 19, 15, 15, tzinfo=UTC),
        "published_at": datetime(2026, 8, 19, 15, 11, 10, 135838, tzinfo=UTC),
        "available_at": datetime(2026, 8, 19, 15, 11, 10, 135838, tzinfo=UTC),
    },
]
```

The description text is the vendor's own, including its spelling ("forsee").

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

The vendor gives no fixed schedule. `TODO: verify` what triggers an update. The CKAN
`last_modified` of each resource is: balancing 2026-09-04; DC/DM/DR, Quick Reserve and Slow
Reserve 2026-08-19; STOR 2025-04-01; SFFR 2024-03-01. One capture per
file exists (2026-10-08). No scheduled refresh has run yet, so ad hoc behaviour across captures
has not been observed.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `as_industry_notifications_sffr_important`: held: TODO: SFFR-NOTIFICATION-DATE-ORDER — is `01/03/2024 10:00` day-first or month-first, and is the single "Example note" row a real notification or a template placeholder? (unit v0.22-K-AS-2)

The quoted line is the registry record's hold text, kept verbatim. The record names the unit that
opened the question (v0.22-K-AS-2). `TODO: unit to be assigned` for answering it: no source in the
AS-2 evidence assigns this hold to a unit. The hold follows the
seat ruling of 2026-10-13 (RULINGS 727, PROXY-SOURCED), which went over the research proposal: the
research recommended an unheld raw-string record, the seat held it because one row cannot settle
either question.

Why it is held: with a single row, no evidence in
the resource settles whether `dd/mm` or `mm/dd` is meant. The vendor dictionary documents an
ISO-style example rather than the captured spelling, and the sibling files do not independently
establish this file's convention. The second question is whether that row is a genuine notice or a
placeholder; the file contains no other populated row, and no primary vendor text was found
declaring it a fixture.

What would lift the hold:

1. An explicit vendor statement of this file's date format, or a later publication in this
   resource containing an unambiguous date (a day greater than 12).
2. A vendor statement that the populated row is, or is not, a real notice.
3. A second capture of the same resource, to measure whether it is ever amended.

If both answers arrive, the family can take the same typed recipe as its siblings. `TODO: verify`
that the siblings' convention may be applied, which is not assumed. The silver output stays on
disk. This page publishes no data values from it: the row count (1), the schema and the vintage
are the only content given. The package-level `eligibility: eligible` in the front matter is the
registry entry for the whole package (6 resources, all SILVER); the hold is per family. The other
five families are **not** held.

## Activation

Merged as PR #113 (master `fccbdeb`, triple-green: CI 2/2, diff review APPROVE on the first pass
with 0 findings, verification passed; RULINGS 730). Transformed (RULINGS 731) for
`--start/--end 2026-10-08` with no prior silver, so nothing was overwritten: balancing **13**,
DC/DM/DR **28**, Quick Reserve **13**, SFFR **1** (held), Slow Reserve **4**, STOR **9**. Every
count equals the planned count. Reconcile `--all --cutoff 2026-10-12` exited 0 over 170 families
with 0 gaps, 47 adjudicated and 0 stale (gridflow `@.planning/v0.22-RESULTS.md` §AS-2).

Silver path pattern:
`C:/gridflow-data/silver/neso_data_portal/<family>/year=2026/month=10/<family>_20261008_run<capture-time>_<hash>.parquet`.
The `year`/`month` partition is the **capture** month: even the 2024 issue labels sit under
`year=2026/month=10`. Silver columns beyond the vendor columns: `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version`. All timestamps are tz-aware UTC (the SFFR vendor columns stay strings).
`dataset_version` reads `1+e1` (record version 1, epoch 1).

## Known quirks

- **Newest-row ordering.** `available_at` is earlier than `timestamp_utc` on the newest row of
  five families (see Time semantics). Do not drop such rows as impossible.
- **Identity is a measured key, not a vendor key.** The issue label has no duplicates in any file
  (13, 28, 13, 1, 4 and 9 distinct values), and is the entity key under whole-capture selection.
  The vendor guarantees no identifier, and no `key_latest` is used. Two notices issued in the same
  minute would collide. `TODO: verify` with a vendor identity statement or a genuine id column.
  The other columns are no substitute: effective-from alone fails uniqueness in STOR, and
  Description alone fails in DC/DM/DR.
- **No revision history.** There is only one capture per file. Whether the vendor edits or deletes
  a notice is unmeasured. `TODO: verify` with a second capture of each resource and a row
  comparison.
- **`Service` can be a list-like string.** DC/DM/DR carries values such as `DC, DM, DR`. Filter
  with equality on the exact string or parse it yourself.
- **Two shapes.** Quick Reserve and Slow Reserve have no `service`. Their service is the family.
- **One notice, several files.** The five eligible files hold 67 rows but 43 distinct issue labels
  (2026-10-08 captures): 17 labels occur in two to four files, usually with identical text, but
  two (2024-03-28 14:00Z, 2026-03-26 14:45Z) and the eclipse notice (2026-08-07 14:35Z) are
  reworded per service. Do not count a union of the files as distinct notices.
- **Balancing Reserve notes sit one row off.** In the Balancing Reserve body the 2025-11-25 notice
  (EAC production outage) carries the note "This is an enduring change for the EAC sandbox
  environment...", the 2025-11-30 forecast-upload notice carries "...for the EAC PRODUCTION
  environment", and the 2025-10-08 sandbox notice has none. The DC/DM/DR and Quick Reserve files
  put those notes on the sandbox and production notices. Checked against the raw CSV, so it is
  the vendor's content, kept byte-equal; trust Notes in this file only with care.
- **Notices describe other datasets.** A notice such as the Slow Reserve archiving notice concerns
  the EAC auction datasets, which live in other NESO packages. The text is not machine-readable:
  there is no structured link from a notice to the dataset it concerns.
- **Contract transfer family (same batch, other package).** `contract_transfer_obligation` is part
  of the same AS-2 batch but belongs to a different package. It has **no record** and no silver
  output (bronze only), because its 12 rows hold five identical duplicates and no source-column key
  can tell them apart (RULINGS 538). It is documented in
  @contract-transfer-of-obligation.md, with its two open questions CONTRACT-TRANSFER-IDENTITY and
  CONTRACT-TRANSFER-PERIOD.

## Modelling notes

`TODO`: modelling use is not yet designed. The five eligible families are a candidate source of
dated regime-change flags for reserve and response models (for example, "an EAC change took effect
from this date"). Parse the free text yourself; nothing is extracted. Use `timestamp_utc` (issue)
or `effective_from_date_time` as the flag date, never `available_at` on its own. For a strict
point-in-time model, `available_at` is the date the whole file became visible, so a historic
backtest should treat these notices as known only from that vintage, not from the issue label. No
gold view reads these families; only the source registry entry (`config/sources.yaml`) refers to
them. The held SFFR family must not be used.

## Links

- [Package page](https://www.neso.energy/data-portal/ancillary-services-important-industry-notifications)
- [NESO Enduring Auction Capability (EAC) page](https://www.neso.energy/industry-information/balancing-services/enduring-auction-capability-eac)
- Registry record: @../../../../Python/gridflow/src/gridflow/connectors/neso_data_portal/registry/ancillary-services-important-industry-notifications.json
- Eligibility report: @../../../../Python/gridflow/docs/neso_data_portal/eligibility.md
- Batch evidence: @../../../../Python/gridflow/.planning/phases/v0.22-K-AS-2/K-AS-2-FACTS.md
- Batch spec: @../../../../Python/gridflow/.planning/phases/v0.22-K-AS-2/K-AS-2-SPEC.md
- Activation receipt: @../../../../Python/gridflow/.planning/v0.22-RESULTS.md
- Domain: @../../../20-domain/markets/gb-balancing-mechanism.md
- Related: @contract-transfer-of-obligation.md
