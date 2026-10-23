---
source: "neso_data_portal"
package: "demand-flexibility-service-live-events"
dataset_keys: ["dfs_live_events_service_requirement", "dfs_live_events_service_update_industry", "dfs_live_events_utilisation_report", "dfs_live_events_utilisation_report_sum"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-14
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Demand Flexibility Service 2022/23: Live Events

This is the **frozen historical record of the live Demand Flexibility Service (DFS) events of winter 2022/23**: the
days on which the National Energy System Operator (NESO) actually procured demand reduction from registered providers
at peak winter demand. The package is the live-only half of the first DFS winter; its test events are a separate
package and the later service years are separate packages again. The vendor's package text says the dataset holds
"updates regarding the use of the live service (not test events)" and points test-event readers to the sibling package
(CKAN package `notes`, @.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json; NESO
[Demand Flexibility Service Live Events](https://www.neso.energy/data-portal/demand-flexibility-service-live-events)).
The vendor marks it **Update Frequency: Not Active**: it will not change by design, although two of its four resources
carry a 2026 `last_modified` stamp (see Cadence).

**Frozen historical series.** Treat the package as a closed 2022/23 series. It contains **two delivery dates,
2023-01-23 and 2023-01-24, with five 30-minute windows**, plus the notices NESO sent around them. For the later
service year see @./demand-flexibility-service.md (frozen 2023/24, which carries Test and Live in one table, told apart
by its Service Requirement Type column). The **successor package** for the current service is
@30-vendors/neso-data-portal/datasets/demand-flexibility.md.

Four families come out of four resources, one resource each:

| Family | What one row is | Rows in silver | Silver status |
|---|---|---:|---|
| `dfs_live_events_service_requirement` | one 30-minute delivery window NESO asked for, with the required MW | 5 | eligible |
| `dfs_live_events_service_update_industry` | one notification NESO posted to industry about whether a requirement was anticipated, published or cancelled | 7 | eligible |
| `dfs_live_events_utilisation_report` | one bid of one DFS unit in one window, Accepted or Rejected, with its regional split at D-1 and at D0 | 170 | eligible |
| `dfs_live_events_utilisation_report_sum` | one window total: required, procured (D-1 and D0), accepted cost and settled volume and cost | 5 | eligible |

Package silver total **187 rows**, activation 2026-10-08, window `2026-10-08..2026-10-08`, no prior silver, one resource
each, 0 recorded transform failures, 0 rows excluded (@.planning/v0.22-RESULTS.md section DFS-b; RULINGS 814, 816).
Nothing in this package is held (Holds).

**Things a reader must know before using it.**

- **Test events are real deliveries, not dummy data, and they are not in this package.** The 2022/23 Live and Test
  packages are separate operational series with equal headers and **no shared delivery date** (zero intersection of
  their delivery-date sets). **Never add Live and Test rows together** and never union their tables.
  Their notification-date sets overlap on one day, 2023-01-22, where the Test package publishes a cancellation that
  refers readers to the Live dataset and the Live package publishes the next-day requirement; a shared notification
  date does not mean a shared delivered event (K-DFS-FACTS, cross-package identity). Sibling page:
  @./demand-flexibility-service-test-events.md.
- **There is no event id.** None of the four resources carries one. Join requirement, report and summary rows on
  **delivery date and window** (and on `unit` for a bid row), **inside this package only**. Notifications carry no join
  key to the other three families at all; their date is the day the notice was posted, which is not the delivery date.
- **Windows are GMT labels kept raw.** `window_from` and `window_to` are the vendor's `HH:MM` strings, documented as
  GMT, stored byte-for-byte as `string`. The engine has no recipe that composes a date with a clock label (RULINGS 572 /
  588), so **no window start or end instant is computed**, and there is no settlement-period column.
- **D0 is the event-day forecast, not an issue time.** The `d0_` columns are the providers' updated delivery forecast
  on the event day; the report is updated around 10:00 GMT on that day (the vendor's report update schedule, not a
  stated submission time for the provider forecasts: `TODO: verify` the D0 submission time). The base columns are the volume submitted at D-1. Neither is a publication
  timestamp.
- **Summaries are published values and do not reconcile to the bids at D0 or at settlement.** The D-1 columns
  reconcile to the Accepted report rows; the D0 and settled columns cannot be rebuilt from the captured report (Known
  issues). Keep them as published and never recalculate them.
- **Requirements are held in the neighbouring packages, but not here.** The 2023/24 and the 2022/23 test requirement
  families are held; this package's requirement is eligible, because every one of its five windows starts after the
  file's own `last_modified` (the forward-target exception, RULINGS 529).

- Publisher group: Demand Flexibility Service
- Registry group: dfs · archetype: EVT

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| DFS Service Requirement - LIVE | CSV | upload | `663f3f82-fec8-4c9a-a837-df5db8690a6f` |
| DFS Utilisation Report - LIVE | CSV | upload | `4e87244e-2479-4e6e-84c2-698dffaca41f` |
| Service Update Industry Notifications - LIVE | CSV | upload | `a59a9d56-af4b-4044-b0c8-6379ce1213f8` |
| Utilisation Report Summary - LIVE | CSV | upload | `011f1a15-f63f-4a95-b1eb-453e5ffcd176` |

All 4 resources are dispositioned `SILVER` to their own family and are CSV uploads. The package has **no
documentation (DOC) files**: every resource is a data file. The files are downloadable from the URLs the vendor
publishes (CKAN catalogue snapshot of 2026-10-06). The table gives each resource's download, the `last_modified` of the
captured body (the vintage clock) and its row counts. Every resource has **exactly one observed capture**
(2026-10-08), so same-resource amendments cannot be measured:

| Resource | Download | Captured `ckan_last_modified` | Bronze rows | Silver rows |
|---|---|---|---:|---:|
| DFS Service Requirement - LIVE | [dfs-service-requirement-live230120231430.csv](https://api.neso.energy/dataset/328b830b-4a8e-4dce-a14b-be91ed926b95/resource/663f3f82-fec8-4c9a-a837-df5db8690a6f/download/dfs-service-requirement-live230120231430.csv) | 2023-01-23T14:59:08 | 5 | 5 |
| Service Update Industry Notifications - LIVE | [service-update-industry-notifications-live070320231430.csv](https://api.neso.energy/dataset/328b830b-4a8e-4dce-a14b-be91ed926b95/resource/a59a9d56-af4b-4044-b0c8-6379ce1213f8/download/service-update-industry-notifications-live070320231430.csv) | 2023-03-07T14:29:05 | 7 | 7 |
| DFS Utilisation Report - LIVE | [dfs-participant-utilisation-report-live2501231600.csv](https://api.neso.energy/dataset/328b830b-4a8e-4dce-a14b-be91ed926b95/resource/4e87244e-2479-4e6e-84c2-698dffaca41f/download/dfs-participant-utilisation-report-live2501231600.csv) | 2026-07-27T14:01:36 | 170 | 170 |
| Utilisation Report Summary - LIVE | [utilisation-report-summary-live2501231600-fs.csv](https://api.neso.energy/dataset/328b830b-4a8e-4dce-a14b-be91ed926b95/resource/011f1a15-f63f-4a95-b1eb-453e5ffcd176/download/utilisation-report-summary-live2501231600-fs.csv) | 2026-07-27T13:22:45 | 5 | 5 |

Bronze captures (2026-10-08, @.planning/phases/v0.22-K-DFS/K-DFS-FACTS.md inventory): requirement `20261008T100626Z`
sha `93fcb6a5`, notification `20261008T100629Z` sha `c6e0aaa4`, report `20261008T100633Z` sha `94191b4f`, summary
`20261008T100636Z` sha `9d016003`. The file names embed a date-and-time token (`230120231430`, `070320231430`,
`2501231600`); the vendor's file name is not a per-row issue time, and the notification token does not identify every
row's issue (notification section).

## Families

### `dfs_live_events_service_requirement`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Delivery Date | `delivery_date` | date | `%Y-%m-%d` | no | — | — |
| From GMT | `window_from` | string | — | no | — | — |
| To GMT | `window_to` | string | — | yes | — | — |
| DFS Required MW | `dfs_required_mw` | float64 | — | yes | — | — |

- Entity key: `delivery_date`, `window_from`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`delivery_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What it is.** The demand-reduction volume NESO asked providers for: one row per 30-minute window, for the
delivery dates 2023-01-23 and 2023-01-24 (five windows). The resource description says registered participants submit
bids no later than 15:30, after which NESO notifies results and publishes the utilisation report. The body has **no
issue column** and no event id.

**Two clocks.**

- **Vintage (when it was known): `available_at` = `published_at` = the CKAN `last_modified` of the captured file**
  (ADR-030), here 2023-01-23T14:59:08Z for every row. All five windows start after this stamp, which is why the
  requirement is eligible at issue `none` (a forward target; RULINGS 529, K-DFS-FACTS requirement). That does not
  establish an immutable per-requirement publication time at an earlier filename token.
- **Event time: `event_time` = `timestamp_utc` = the delivery date at the first settlement period of the Europe/London
  day (the recipe `date_sp1` on `delivery_date`), converted to tz-aware UTC at the silver boundary.** It is a
  **date-label anchor, not the window start**: in this January data it falls at 00:00Z of the delivery date
  (2023-01-23T00:00Z and 2023-01-24T00:00Z). The within-day position is the raw string `window_from`.

**Units.** `DFS Required MW` is **MW**: the vendor dictionary leaves its unit cell blank but describes the field as
"DFS volume required (MWs)", and the column name carries the unit (K-DFS-FACTS, requirement T01). The window columns
are `HH:MM` clock labels, documented GMT, with no unit. Delivery Date is `YYYY-MM-DD` in the body.

**Sentinels and typing (g5, g6).** No blank, zero, negative, sentinel token or lexical repair in the body, and no
embedded comma, quote or newline; the production CSV reader agreed with a strict second parse on every cell.
Nothing is mapped to null or trimmed. Window labels stay `string`.

**Identity.** 5 rows, 5 distinct (`delivery_date`, `window_from`) pairs. The vendor's guarantee that this pair is
unique across future editions is `TODO: verify`; `whole_capture` selection prevents any merging of revised rows.

### `dfs_live_events_service_update_industry`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `date` | date | `%Y-%m-%d` | no | — | — |
| Status | `status` | string | — | yes | — | — |
| Type | `type` | string | — | no | — | — |
| Time | `time_label` | string | — | no | — | HH:MM |

- Entity key: `date`, `time_label`, `type`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What it is.** The notices NESO posted to industry about the live service. The resource description names three
kinds: an *Anticipated DFS Requirements Notice* (around 10:00 GMT, only when a requirement is anticipated), a
*DFS Requirement is now published* notice (around 14:30 GMT) and a *DFS Requirement not issued* notice (around 14:30
GMT, when a requirement is no longer expected). The body has 7 rows over 4 posting dates, 2023-01-22 to 2023-03-07.
`status` is free text and is never mined for a date; the dictionary says a published notice refers to the next day.
A cancelled notice has no delivered event, and the notification family has **no join key** to the requirement, report
or summary.

**Two clocks.**

- **Vintage: `available_at` = `published_at` = the CKAN `last_modified` of the captured file** (ADR-030), here
  2023-03-07T14:29:05Z for every row. It is a file stamp, not a row issue time: it is the newest posting date's file
  save (about 54 seconds before the latest label's 14:30 notice time, K-DFS-FACTS notification g1/g2), so it
  says nothing about when the January notices were first posted.
- **Event time: `event_time` = `timestamp_utc` = the posting date `date`, anchored at the first settlement period (the
  recipe `date_sp1`) of the Europe/London day.** It is a **date-label anchor, not the notification time**: the date and
  the `HH:MM` time are separate fields that the engine cannot compose into one instant, so `issue` is `none` and the
  clock stays the string `time_label` (documented GMT notification schedule). Observed event time range is
  2023-01-22T00:00Z to 2023-03-07T00:00Z.

**Units.** None: every column is a date, a clock label (`HH:MM`) or free text/categorical.

**Sentinels and typing (g5, g6).** No blank or sentinel token. **Text padding is kept byte-equal:** 5 `status` cells
and 3 `type` cells carry edge whitespace (for example a `type` value with a trailing space), and because `type` is part
of the entity key a padded and an unpadded spelling would be distinct keys as published. Do not trim before
joining or grouping without checking this. No embedded comma, quote or newline.

**Identity.** 7 rows, 7 distinct (`date`, `time_label`, `type`) keys. Vendor guarantee of that composite: `TODO: verify`.
`TODO: verify` NOTIFICATION-ISSUE-RETENTION: immutable row publication history and a supported split date-and-time
mechanism would settle an issue time. It does not hold the output.

### `dfs_live_events_utilisation_report`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `date` | date | `%d/%m/%Y` | no | — | — |
| DFS Provider | `dfs_provider` | string | — | yes | — | — |
| Unit | `unit` | string | — | no | — | — |
| DFS Volume | `dfs_volume` | float64 | — | yes | — | MW |
| From | `window_from` | string | — | no | — | HH:MM |
| To | `window_to` | string | — | yes | — | HH:MM |
| Price | `price` | float64 | — | yes | — | £/MWh |
| Status | `status` | string | — | yes | — | — |
| North Scotland | `north_scotland` | float64 | — | yes | — | MW |
| South and Central Scotland | `south_and_central_scotland` | float64 | — | yes | — | MW |
| North East England | `north_east_england` | float64 | — | yes | — | MW |
| North West England | `north_west_england` | float64 | — | yes | — | MW |
| Yorkshire | `yorkshire` | float64 | — | yes | — | MW |
| East Midlands | `east_midlands` | float64 | — | yes | — | MW |
| West Midlands | `west_midlands` | float64 | — | yes | — | MW |
| London | `london` | float64 | — | yes | — | MW |
| East England | `east_england` | float64 | — | yes | — | MW |
| South East England | `south_east_england` | float64 | — | yes | — | MW |
| South West England | `south_west_england` | float64 | — | yes | — | MW |
| Southern England | `southern_england` | float64 | — | yes | — | MW |
| North Wales_Merseyside_Cheshire | `north_wales_merseyside_cheshire` | float64 | — | yes | — | MW |
| South Wales | `south_wales` | float64 | — | yes | — | MW |
| Other | `other` | float64 | — | yes | — | MW |
| Total | `total` | float64 | — | yes | — | MW |
| D0 North Scotland | `d0_north_scotland` | float64 | — | yes | — | MW |
| D0 South and Central Scotland | `d0_south_and_central_scotland` | float64 | — | yes | — | MW |
| D0 North East England | `d0_north_east_england` | float64 | — | yes | — | MW |
| D0 North West England | `d0_north_west_england` | float64 | — | yes | — | MW |
| D0 Yorkshire | `d0_yorkshire` | float64 | — | yes | — | MW |
| D0 East Midlands | `d0_east_midlands` | float64 | — | yes | — | MW |
| D0 West Midlands | `d0_west_midlands` | float64 | — | yes | — | MW |
| D0 London | `d0_london` | float64 | — | yes | — | MW |
| D0 East England | `d0_east_england` | float64 | — | yes | — | MW |
| D0 South East England | `d0_south_east_england` | float64 | — | yes | — | MW |
| D0 South West England | `d0_south_west_england` | float64 | — | yes | — | MW |
| D0 Southern England | `d0_southern_england` | float64 | — | yes | — | MW |
| D0 North Wales Merseyside and Cheshire | `d0_north_wales_merseyside_and_cheshire` | float64 | — | yes | — | MW |
| D0 South Wales | `d0_south_wales` | float64 | — | yes | — | MW |
| D0 Other | `d0_other` | float64 | — | yes | — | MW |
| D0 Total | `d0_total` | float64 | — | yes | — | MW |

- Entity key: `date`, `window_from`, `unit`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What it is.** The bid-level outcome of the live events: for each registered DFS unit and each 30-minute window, the
volume it offered, the price, whether NESO accepted or rejected the bid, and how the volume splits across 14 grid
regions. The resource description says it is updated at around 16:30 GMT on days with a published requirement; the
package text says it is updated again at around 10:00 GMT on the day the service is required. The body has **170 rows: 165 Accepted and 5 Rejected**, over **5 windows** on
2023-01-23 and 2023-01-24, from 20 providers and 36 units. The regional names in the header are the vendor's; note the
two spellings of the Wales/Merseyside/Cheshire region (`North Wales_Merseyside_Cheshire` at D-1 and
`D0 North Wales Merseyside and Cheshire` at D0), which map to two distinct silver columns.

**D-1 and D0.** `dfs_volume` and the 14 regional columns plus `other` and `total` are the volume **submitted at D-1**.
The 16 `d0_` columns are the providers' **updated delivery forecast on the event day**; the report is updated around
10:00 GMT on that day (the vendor's update schedule; the time at which providers submit the D0 forecast is
`TODO: verify`). D0 is a forecast
stage, not an issue time: there is no issue column, and a D0 value is not a re-publication timestamp. A unit that
supplied no D0 forecast has blank `d0_` cells (below); in this capture the blanks fall on exactly the 5 Rejected rows
and touch no Accepted bid; the vendor's summary text says the D-1 values are used in that
case.

**Two clocks.**

- **Vintage (when it was known): `available_at` = `published_at` = the CKAN `last_modified` of the captured file**
  (ADR-030), here **2026-07-27T14:01:36Z** for every row. The data describe January 2023; the 2026 stamp is a later
  re-save of the resource by the vendor, and what that change contained is not stated (`TODO: verify`). The vintage is a
  file stamp, so these rows are available no earlier than 2026-07-27 for point-in-time purposes, even though the event
  is old.
- **Event time: `event_time` = `timestamp_utc` = the event `date` at the first settlement period of the Europe/London
  day (recipe `date_sp1`), converted to tz-aware UTC.** It is a **date-label anchor, not the window start**:
  2023-01-23T00:00Z to 2023-01-24T00:00Z. The start and end of the window are the raw GMT `HH:MM` strings
  `window_from` and `window_to`. The report `Date` is `dd/mm/yyyy`.

**Units (vendor dictionary, K-DFS-FACTS g4).** `dfs_volume`, each regional column, `other`, `total` and every `d0_`
counterpart are **MW**. `price` is **£/MWh** (price of the volume submitted, per MWh). `dfs_provider`, `unit` and
`status` are categorical (status is Accepted or Rejected). Units come only from the dictionary, never from a column name.

**Sentinels and typing (g5, g6).** Every `d0_` column has **5 blanks** (kept null). `price` has 3 zeros and `dfs_volume`
and `total` have 5 zeros each, kept as zero, never turned into null. No negative number, sentinel token,
percentage/thousands formatting or padded numeric cell was observed. `unit` and provider identifiers are stored as
published. No embedded comma, quote or newline; UTF-8 and byte-order-mark handling and every cell match the strict
comparison.

**Identity.** 170 rows, 170 distinct (`date`, `window_from`, `unit`) keys. The vendor's procurement rules support one
bid per unit per period; the export-level identity and retention guarantee is `TODO: verify`.

**Regional split is a diagnostic, not a decomposition.** Regional columns sum to `total` in **130 of 170 rows**, and
`total` equals `dfs_volume` in **140 of 170** (tolerance 0.000001 MW). Use the published bid quantity (`dfs_volume`);
never substitute a sum of the regional columns. `TODO: verify` REGIONAL-RECONCILIATION (what the vendor intends the
regional columns to satisfy). It does not hold the output.

### `dfs_live_events_utilisation_report_sum`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `date` | date | `%d/%m/%Y` | no | — | — |
| From | `window_from` | string | — | no | — | HH:MM |
| To | `window_to` | string | — | yes | — | HH:MM |
| DFS Required | `dfs_required` | float64 | — | yes | — | MW |
| DFS Procured | `dfs_procured` | float64 | — | yes | — | MW |
| Bids Accepted Total Cost | `bids_accepted_total_cost` | float64 | — | yes | — | £ |
| D0 DFS Procured | `d0_dfs_procured` | float64 | — | yes | — | MW |
| D0 Bids Accepted Total Cost | `d0_bids_accepted_total_cost` | float64 | — | yes | — | £ |
| Settled Volume | `settled_volume` | float64 | — | yes | — | MW |
| Settled Cost | `settled_cost` | float64 | — | yes | — | £ |

- Entity key: `date`, `window_from`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What it is.** One row per 30-minute window summarising the utilisation report: the requirement, the volume and cost
procured at D-1, the same re-stated at D0 on the updated forecast, and the post-event settled volume and cost (visible
once settlement data is received). The body has 5 rows, one per window, with the same five (date, window) keys as the
requirement. The vendor text says that where a unit's updated D0 forecast was not received, the D-1 values are used.

**Two clocks.**

- **Vintage: `available_at` = `published_at` = the CKAN `last_modified` of the captured file** (ADR-030), here
  **2026-07-27T13:22:45Z** for every row. As for the report, this is a 2026 re-save of a January 2023 event table; the
  content of that change is `TODO: verify`. Settled fields are post-event outturn, so their real availability is later
  than the event; the file stamp is still the only vintage gridflow has.
- **Event time: `event_time` = `timestamp_utc` = the event `date` at the first settlement period of the Europe/London
  day (recipe `date_sp1`), converted to tz-aware UTC** (2023-01-23T00:00Z and 2023-01-24T00:00Z): a date-label anchor,
  not the window start. Window start and end are the raw GMT strings `window_from` / `window_to`. Summary `Date` is
  `dd/mm/yyyy`.

**Units (vendor dictionary).** `dfs_required`, `dfs_procured`, `d0_dfs_procured` and `settled_volume` are **MW**;
`bids_accepted_total_cost`, `d0_bids_accepted_total_cost` and `settled_cost` are **£**. The dictionary publishes no MWh
quantity.

**Sentinels and typing (g5, g6).** No blank, zero or negative numeric cell in the summary, no sentinel token or lexical
repair. The physical header has a trailing space on `Settled Cost` and a byte-order mark; the reader normalises both and
every row and cell survives.

**Identity.** 5 rows, 5 distinct (`date`, `window_from`) keys; vendor guarantee `TODO: verify`.

**Reconciliation to the report.** The D-1 quantities and costs reconcile to the Accepted report rows of the same window
within 0.005 MW and £1 across all 5 windows. The D0 and settlement values do **not** reconcile from the report: summing
the report's `d0_total` with the documented blank fallback reproduces the D0 procured quantity for only 1 of 5
windows and the D0 cost for none, and the settled fields have no report counterpart at all. **Do not add summary and
report quantities together** (the D-1 summary is an aggregation of the Accepted report rows, so the sum double counts),
and never recompute a summary from the report. `TODO: verify` D0-RECONCILIATION: vendor clarification of `D0 Total`,
the regional allocation, the fallback and any publication revision. It does not hold the output.

## Cadence

- Registry refresh: frozen
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Not Active

A closed series: no new live-event rows are expected. The catalogue's own `last_modified` stamps differ by resource:
the requirement and notification resources carry their original 2023 stamps, and the report and summary resources carry
2026-07-27 stamps (above), so a re-save of an unchanged historical file can move the vintage forward. gridflow holds
**one capture per resource** (2026-10-08), so whether a re-save ever changes rows is unmeasured: `TODO: verify` by
comparing any later capture with the hash-pinned bodies. The package's `refresh` is `frozen` and an empty capture is
not allowed.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence). Any output derived from
this package carries the attribution line "Supported by National Energy SO Open Data".

## Holds

- none

All four families are eligible. The requirement family passes the forward-target rule because all five of its windows
start after the file's `last_modified`; the notification, report and summary families are eligible as retrospective
event tables at `issue: none` and vintage `ckan_last_modified` (RULINGS 801 scope, 803 facts, 814 merge, 816
activation). The holds that DFS-b did record are on the neighbouring packages and are not repeated here: the 2023/24
service requirement (@./demand-flexibility-service.md) and the 2022/23 test-event requirement
(@./demand-flexibility-service-test-events.md), each for the question of when a requirement was first published (unit
`v0.22-K-DFS-b`).

**Open questions that do not hold any output** (K-DFS-FACTS, carried as non-holding TODOs):

- `TODO: verify` NOTIFICATION-ISSUE-RETENTION: row-level publication history for the notices.
- `TODO: verify` REGIONAL-RECONCILIATION: what the regional columns should sum to.
- `TODO: verify` D0-RECONCILIATION: how the summary D0 fields are derived from the report.
- `TODO: verify` ENDPOINT-CLOSURE: whether a window end is inclusive or exclusive (`window_to` is kept as published).
- `TODO: verify` the 2026-07-27 re-save of the report and summary resources (what changed, if anything).

## Known issues and gotchas

- **Never add Live and Test.** This package and @./demand-flexibility-service-test-events.md are separate tables with no
  shared delivery date. A union of the two is a different, unestablished series. Test events are real deliveries.
- **No event id: join on date and window, inside the package.** Requirement, report and summary join on (`delivery_date`
  or `date`, `window_from`); a bid row additionally on `unit`. The requirement names the date `delivery_date` and the
  other three families name it `date`. Do not join to the 2023/24 or the current tables on date and window.
- **`event_time` is a date anchor, not the window.** It is the Europe/London midnight of the date label; in this January
  data that equals 00:00Z. Use the string labels for the within-day position. Every window is 30 minutes long, and no
  delivery row falls on a clock-change day.
- **Vintage is a file stamp, and it differs by family.** The requirement is stamped the afternoon of the first delivery
  date, the notification file in March 2023, and the report and summary in July 2026. A point-in-time filter
  (`available_at <= as_of`) therefore excludes the report and summary of January 2023 before 2026-07-27.
- **Summaries are published values, not a roll-up you can rebuild.** The D-1 totals match the Accepted bids; D0 and
  settlement do not. Never sum the summary and the report, and never recompute a summary.
- **Filter on `status = 'Accepted'` for bid counts and accepted-unit statistics.** A report row count is bids, not
  accepted units. In this package the 5 Rejected rows are all unit `DRAX-04` and carry zero volume (`dfs_volume`,
  `total` and every regional column are 0.0; `d0_total` is blank), 2 priced at 3000 and 3 at 0, so they do not change
  a MW sum, but they do inflate a row count. (A Rejected row carrying positive volume is a fact about the current
  successor package, not this one.)
- **D0 blanks are real.** A unit with no D0 forecast has null `d0_` cells (here the 5 blank rows are exactly the 5
  Rejected rows, so no Accepted bid has a blank D0); do not coalesce them to zero. The vendor's
  fallback to the D-1 value is a documented interpretation, not something the stored cells carry.
- **Zero is a value.** Zero prices and volumes are kept as zero. The 5 zero `dfs_volume` rows, the 5 zero `total` rows
  and the 3 zero `price` rows are all Rejected rows (reproduced from silver).
- **Notification text is padded as published.** The `type` key spelling `Anticipated Requirement Notice` appears with a
  trailing space; match on the published spelling or trim in your own query after checking the keys stay unique.
- **A notification date is a posting date.** It can precede delivery by a day, and a cancelled notice has no delivered
  event. Do not read the notice date as the delivery date.
- **Windows are GMT labels, kept raw.** No instant is composed from a date and a window label; the endpoint treatment is
  `TODO: verify` ENDPOINT-CLOSURE.
- **No settlement-period or run-type column exists.** These are aggregate event tables, not a `(date, period,
  run_type)` settlement dataset; none is invented.

## Links

- [NESO package page](https://www.neso.energy/data-portal/demand-flexibility-service-live-events)
- [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence)
- [Successor package (current service)](./demand-flexibility.md)
- [Frozen 2023/24 package](./demand-flexibility-service.md)
- [Sibling 2022/23 test events](./demand-flexibility-service-test-events.md)
- Registry record: `src/gridflow/connectors/neso_data_portal/registry/demand-flexibility-service-live-events.json`
- Evidence: @.planning/phases/v0.22-K-DFS/K-DFS-FACTS.md, @.planning/phases/v0.22-K-DFS/K-DFS-b-SPEC.md, @.planning/v0.22-RESULTS.md
