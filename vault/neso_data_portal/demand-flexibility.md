---
source: "neso_data_portal"
package: "demand-flexibility"
dataset_keys: ["demand_flexibility_industry_notification", "demand_flexibility_service_requirement", "demand_flexibility_utilisation_report", "demand_flexibility_utilisation_summary"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-14
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Demand Flexibility Service

The Demand Flexibility Service (DFS) is how the National Energy System Operator (NESO) buys short-notice demand
reductions from registered providers: for a half-hour delivery window NESO publishes a requirement, providers bid
demand-reduction volume per DFS unit, NESO accepts bids up to the requirement, and the delivered volume is settled
afterwards. The vendor's package text says the service "allows the NESO to access additional flexibility" and that
the auction results are published in this package, while the older results page (the frozen
`demand-flexibility-service` package) "will no longer be updated, but will be retained to share historical data"
(CKAN package `notes`, @.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json; NESO
[Demand Flexibility Service](https://www.neso.energy/data-portal/demand-flexibility)). This page documents only the
**current-service package** `demand-flexibility`; the three frozen DFS packages (`demand-flexibility-service`,
`-live-events`, `-test-events`) are ingest-only and are not described here. Related page for the sibling short-notice
product in this vendor: @./short-term-operating-reserve-stor-day-ahead-buy-curve.md.

Four families come out of seven resources (4 Archive 2025/2026 plus 3 current). Each family has one **Archive
2025/2026** resource, and every family except the notification also has a **current** resource (the notification is
archive-only):

| Family | What one row is | Silver status |
|---|---|---|
| `demand_flexibility_service_requirement` | one requirement window of one service requirement type (Live / Test) | **held** (no publication time) |
| `demand_flexibility_industry_notification` | one notification NESO issued to industry (archive only) | eligible |
| `demand_flexibility_utilisation_report` | one bid outcome (Accepted / Rejected) of one DFS unit in one window | eligible (current resource loaded; the archive resource is ingested but not tabled) |
| `demand_flexibility_utilisation_summary` | one window total: requirement, procured, accepted cost, settled volume and cost | eligible |

**The shape of the package, in one paragraph.** The archive and current resources are **disjoint seasons, not
copies**: the Archive 2025/2026 resources span delivery dates 2024-11-29 to 2026-03-27 and the current resources start
at 2026-04-14, with **zero shared date/window keys** in all three paired families (K-DFS-FACTS, current/archive
boundaries). Each family is therefore **one silver table keyed by resource** (`resource_id` is in every entity key),
holding the newest capture of each resource, and the two seasons are read together by stacking. The two seasons have
**different headers** (epochs): the archive has no event columns and wide regional report columns, the current
resource adds `event_id`, event type and tag, explicit local and UTC window labels, and a long-form zone column. Where
a column does not exist in an epoch the silver cell is **null and never fabricated**.

**What a model gets from it, and what it does not.**

- **Window labels are raw vendor clocks, kept as strings.** `window_from` / `window_to` hold the vendor label exactly as
  published (current: `From_Local` / `To_Local` plus `window_from_utc` / `window_to_utc`; archive: `From` / `To`). The
  engine has no date-plus-clock-label recipe (RULINGS 572 / 588), so **no window start or end instant is computed**.
  The silver `event_time` is a **date-label anchor**, not a window start (see Two clocks). The archive requirement
  dictionary says its `From` / `To` are GMT while the archive report and summary dictionaries say local time, which
  is unresolved: `TODO: verify` ARCHIVE-CLOCK-CONSISTENCY. Do not join archive tables through synthesised instants.
- **Procured MW is positive on rejected bids.** In the utilisation report `dfs_procured_mw` is the bid quantity and is
  greater than zero on every one of the 3,890 Rejected rows; accepted procurement is `WHERE status = 'Accepted'`.
- **Summary procurement equals accepted report rows, so never add them.** `dfs_procured_mw` and
  `dfs_provider_bids_accepted_total_cost_gbp` in the summary are an aggregation of the Accepted report rows of the
  same window; adding the summary to the report double counts. Settlement fields are additional outturn data and
  cannot be derived from bids.
- **Settled values can be negative and can be blank.** Signs are kept as published; blanks stay null.
- **Requirements are held.** No requirement value is published from this page or from silver until NESO says when a
  requirement was first published (Holds).
- **The archive utilisation report is ingested but not tabled.** It repeats four whole rows, so no key is lossless and
  the capture fails the duplicate guard rather than being deduplicated (Recorded failure).

- Publisher group: Demand Flexibility Service
- Registry group: dfs · archetype: EVT

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| DFS Industry Notification (Archive 2025/2026) | CSV | upload | `3d042450-b556-450f-a4b5-cdb075cdf9c1` |
| DFS Service Requirement | CSV | upload | `3635fd80-49d7-4d02-964d-cc8c08d50302` |
| DFS Service Requirement (Archive 2025/2026) | CSV | upload | `f5605e2b-b677-424c-8df7-d0ce4ee03cef` |
| DFS Utilisation Report | CSV | upload | `3ebf77d7-05df-466e-a023-dc45a90efeea` |
| DFS Utilisation Report (Archive 2025/2026) | CSV | upload | `cc36fff5-5f6f-4fde-8932-c935d982ecd8` |
| DFS Utilisation Report Summary | CSV | upload | `705e573c-ddac-4675-b410-82916b35c4fe` |
| DFS Utilisation Report Summary (Archive 2025/2026) | CSV | upload | `25698259-0b66-42f0-ac59-ef0df5245812` |

All 7 resources are dispositioned `SILVER` to their own family and are **CSV uploads**. The package has **no
documentation (DOC) files**: every resource is a data file, so there is no DOC download to link. The data files are
downloadable from the URLs the vendor publishes (CKAN catalogue snapshot of 2026-10-06,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json). The table gives, per resource, the rows in
the one captured body and the rows now in silver (activation 2026-10-08, window `2026-10-08..2026-10-08`, no prior
silver; @.planning/v0.22-RESULTS.md section DFS-a; RULINGS 809):

| Resource | Download | Captured `ckan_last_modified` | Bronze rows | Silver rows |
|---|---|---|---:|---:|
| Industry Notification (Archive) | [dfs-industry-notification.csv](https://api.neso.energy/dataset/829e325f-8926-40ab-9dd6-8b7aea6cb244/resource/3d042450-b556-450f-a4b5-cdb075cdf9c1/download/dfs-industry-notification.csv) | 2026-03-27T10:44:31 | 191 | 191 |
| Service Requirement (Archive) | [dfs-service-requirement.csv](https://api.neso.energy/dataset/829e325f-8926-40ab-9dd6-8b7aea6cb244/resource/f5605e2b-b677-424c-8df7-d0ce4ee03cef/download/dfs-service-requirement.csv) | 2026-03-27T10:45:09 | 1,132 | 1,132 (held) |
| Service Requirement (current) | [dfs-service-requirement.csv](https://api.neso.energy/dataset/829e325f-8926-40ab-9dd6-8b7aea6cb244/resource/3635fd80-49d7-4d02-964d-cc8c08d50302/download/dfs-service-requirement.csv) | 2026-10-08T09:47:40 | 1,238 | 1,238 (held) |
| Utilisation Report (Archive) | [dfs-utilisation-report.csv](https://api.neso.energy/dataset/829e325f-8926-40ab-9dd6-8b7aea6cb244/resource/cc36fff5-5f6f-4fde-8932-c935d982ecd8/download/dfs-utilisation-report.csv) | 2026-03-27T12:04:05 | 9,950 | **0: recorded failure** |
| Utilisation Report (current) | [dfs-utilisation-report.csv](https://api.neso.energy/dataset/829e325f-8926-40ab-9dd6-8b7aea6cb244/resource/3ebf77d7-05df-466e-a023-dc45a90efeea/download/dfs-utilisation-report.csv) | 2026-10-06T11:06:32 | 14,663 | 14,663 |
| Utilisation Summary (Archive) | [dfs-utilisation-report-summary.csv](https://api.neso.energy/dataset/829e325f-8926-40ab-9dd6-8b7aea6cb244/resource/25698259-0b66-42f0-ac59-ef0df5245812/download/dfs-utilisation-report-summary.csv) | 2026-04-09T08:55:59 | 1,130 | 1,130 |
| Utilisation Summary (current) | [dfs-utilisation-report-summary.csv](https://api.neso.energy/dataset/829e325f-8926-40ab-9dd6-8b7aea6cb244/resource/705e573c-ddac-4675-b410-82916b35c4fe/download/dfs-utilisation-report-summary.csv) | 2026-10-06T11:06:52 | 1,230 | 1,230 |

Package silver total **19,584 rows**: 17,214 in the three eligible families (191 + 14,663 + 2,360) and 2,370 in the held
requirement family. The failed archive report (9,950 bronze rows) is not in silver. Every resource has **exactly one observed capture**
(2026-10-08), so same-resource amendments cannot be measured yet. The current requirement resource's
`last_modified` was 2026-10-06T09:48 in the 2026-10-06 catalogue snapshot and 2026-10-08T09:47 in the capture:
the current resources are re-published in place, so a later capture will carry a later vintage and replace the rows
of that resource.

## Families

### `demand_flexibility_industry_notification`

- Kind: tabular · archetype: EVT · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Notification Issued Date | `notification_issued_date` | date | `%d/%m/%Y` | no | — | YYYY-MM-DD |
| Notification Issued Time | `notification_issued_time` | string | — | no | — | HH:MM:SS |
| Requirement For | `requirement_for` | date | `%d/%m/%Y` | no | — | YYYY-MM-DD |
| Requirement Type | `requirement_type` | string | — | no | — | — |
| Status | `status` | string | — | yes | — | — |
| Notification Type | `notification_type` | string | — | no | — | — |

- Entity key: `resource_id`, `notification_issued_date`, `notification_issued_time`, `requirement_for`, `requirement_type`, `notification_type`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: date_sp1 (`notification_issued_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What it is.** The notices NESO sent to industry about DFS requirements (what is being asked for, for which date).
The package has only the **Archive 2025/2026** notification resource: 191 rows, posting dates 2024-11-29 to
2026-03-27 (NESO [archive notification dictionary](https://www.neso.energy/data-portal/demand-flexibility/dfs_industry_notification_archive_20252026)).
There is **no Event ID**, so a notification can never be joined to a requirement, report or summary row by id; a
join through `requirement_for` is a date-level association only. `status` is free text and is never mined for a
date.

**Two clocks.**

- **Vintage (when it was known): `available_at` = `published_at` = the CKAN `last_modified` of the captured file**
  (ADR-030), here 2026-03-27T10:44:31Z for every row. It is a file stamp, not a row issue time: the newest
  notification time in the body is about 928 seconds after it, so `last_modified` is not an immutable per-row issue
  instant (K-DFS-FACTS notification g1/g2).
- **Event time: `event_time` = `timestamp_utc` = the posting date `notification_issued_date`, anchored at the first
  settlement period (the recipe `date_sp1`) on the Europe/London day**, converted to tz-aware UTC at the silver
  boundary. It is a **date-label anchor, not the notification time**: the notification date and time are separate
  fields and the engine cannot compose them into one issue instant, so `issue` is none and the time stays the string
  `notification_issued_time`. The vendor documents the time as GMT. Verified: `event_time` equals `timestamp_utc` on
  all 191 rows, spanning 2024-11-29T00:00Z to 2026-03-27T00:00Z.

**Units.** None: every column is a date, a clock label or free text/categorical (K-DFS-FACTS notification g4).

**Sentinels and typing (g5, g6).** No blank, sentinel token or padded cell, and no embedded comma, quote or newline;
the production CSV reader agreed with a strict second parse on every row. Nothing is mapped to null or trimmed. Dates
are `dd/mm/yyyy` in the body.

**Identity.** 191 rows, 191 distinct (issued date, issued time) pairs, but only 190 distinct requirement dates, so
`requirement_for` alone is not an identity. The five-column key plus `resource_id` is unique across all 191 rows
(vendor guarantee of that composite: `TODO: verify`). `resource_id` is in the key so a future current notification
resource cannot displace the archive. Registry `empty allowed` stays `no`: `TODO: verify` NOTIFICATION-EMPTY-LIFECYCLE
(a valid empty capture or retention policy would settle it) and NOTIFICATION-ISSUE-RETENTION (immutable publication
history plus a split date-and-time mechanism would settle an issue time). Neither holds the output.

### `demand_flexibility_service_requirement`

- Kind: tabular · archetype: EVT · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Delivery Date | `delivery_date` | date | `%d/%m/%Y` | no | — | YYYY-MM-DD |
| From | `window_from` | string | — | no | — | — |
| To | `window_to` | string | — | yes | — | — |
| Service Requirement MW | `service_requirement_mw` | float64 | — | yes | — | MW |
| Service Requirement Type | `service_requirement_type` | string | — | no | — | — |
| Guaranteed Acceptance Price GBP per MWh | `guaranteed_acceptance_price_gbp_per_mwh` | float64 | — | yes | — | £/MWh |
| Dispatch Type | `dispatch_type` | string | — | yes | — | — |
| Participant Bids Eligible | `participant_bids_eligible` | string | — | yes | — | — |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Event ID | `event_id` | string | — | yes | — | — |
| DFS Submission Time_Local | `dfs_submission_time` | datetime | `%d/%m/%Y %H:%M` | yes | Europe/London | HH:MM |
| Event Type | `event_type` | string | — | yes | — | — |
| Event Tag | `event_tag` | string | — | yes | — | — |
| Delivery Date | `delivery_date` | date | `%d/%m/%Y` | no | — | YYYY-MM-DD |
| From_Local | `window_from` | string | — | no | — | HH:MM |
| To_Local | `window_to` | string | — | yes | — | HH:MM |
| From_UTC | `window_from_utc` | string | — | yes | — | HH:MM |
| To_UTC | `window_to_utc` | string | — | yes | — | HH:MM |
| Service Requirement MW | `service_requirement_mw` | float64 | — | yes | — | MW |
| Service Requirement Type | `service_requirement_type` | string | — | no | — | — |
| Guaranteed Acceptance Price GBP per MWh | `guaranteed_acceptance_price_gbp_per_mwh` | float64 | — | yes | — | £/MWh |
| Dispatch Type | `dispatch_type` | string | — | yes | — | — |
| Participant Bids Eligible | `participant_bids_eligible` | string | — | yes | — | — |
| Zonal Cap | `zonal_cap` | string | — | yes | — | MW |

- Entity key: `resource_id`, `delivery_date`, `window_from`, `service_requirement_type`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: date_sp1 (`delivery_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**This family is held. No requirement data value is published on this page** (no sample rows and no value
statistics); only the row counts, schema and clocks below are stated.

**What it is.** The requirement NESO set for a delivery window: the volume wanted, the type (Live or Test), the
guaranteed acceptance price, the dispatch type and, in the current epoch, an event identity, a submission deadline,
the local and UTC window labels and a zonal cap. Silver holds 2,370 rows: 1,132 from the Archive 2025/2026 resource
and 1,238 from the current resource. Epoch 1 is the archive header (8 columns) and epoch 2 the current header (15
columns); an archive row carries null `event_id`, `event_type`, `event_tag`, `dfs_submission_time`,
`window_from_utc`, `window_to_utc` and `zonal_cap`, never invented values.

**Two clocks.**

- **Vintage: `available_at` = `published_at` = the CKAN `last_modified` of the captured file** (ADR-030):
  2026-03-27T10:45:09Z for the archive resource and 2026-10-08T09:47:40Z for the current one. Because the family is
  held, this vintage is **not** a statement of when any requirement was first known.
- **Event time: `event_time` = `timestamp_utc` = `delivery_date` anchored at the first settlement period on the
  Europe/London day, in tz-aware UTC** (`date_sp1`). A date-label anchor, not a window start. The window labels stay
  strings (current: local and UTC labels; archive: a label the dictionary calls GMT, `TODO: verify`
  ARCHIVE-CLOCK-CONSISTENCY). The one typed instant is `dfs_submission_time`, the current resource's
  `DFS Submission Time_Local` read as a `%d/%m/%Y %H:%M` UK-local datetime and converted to UTC (ambiguous local
  times would raise; none occurs in the captured body; evidence: NESO current DFS participation guidance,
  [document 346011](https://www.neso.energy/document/346011/download), Appendix 1 and Appendix 6). **It is the
  auction-close deadline for bids, not a publication time**, and is never used as `issue`.

**Units (vendor dictionary as cited in K-DFS-FACTS g4; none inferred from a column name).** `service_requirement_mw`
and the cap in `zonal_cap` are MW; `guaranteed_acceptance_price_gbp_per_mwh` is £/MWh; `event_id`, `event_type`,
`event_tag`, `dispatch_type`, `participant_bids_eligible` and the window labels carry no physical unit.
`zonal_cap` is structured text, not a scalar, and is never parsed in silver. The archive requirement dictionary is
[NESO archive requirement](https://www.neso.energy/data-portal/demand-flexibility/dfs_service_requirement_archive_20252026).

**Sentinels and typing (g5, g6).** No blank, token or padded cell needs repair; zero is a published value and is kept
(it is not a null). `participant_bids_eligible` and `zonal_cap` hold quoted comma lists; CSV quoting is faithful, so
split on the quoting, not on commas. Identifiers (`event_id`) are strings byte-equal to the file, never cast.

**Identity.** Key = (`resource_id`, `delivery_date`, `window_from`, `service_requirement_type`); the 1,132 archive and
1,238 current rows are each unique on it. Two simultaneous windows of different type (Live and Test) are told apart
only by `service_requirement_type`, so **`delivery_date` plus window start alone is not a key**. Within the current
resource `event_id` links to the report and summary; `TODO: verify` EVENT-ID-NAMESPACE (a vendor reset policy), so
never use an Event-ID-only join across resources or time. Vendor guarantee of the composite key: `TODO: verify`.
`TODO: verify` ENDPOINT-CLOSURE (inclusive or exclusive `window_to`): ends are kept literal.

### `demand_flexibility_utilisation_report`

- Kind: tabular · archetype: EVT · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Delivery Date | `delivery_date` | date | `%d/%m/%Y` | no | — | YYYY-MM-DD |
| Registered DFS Participant | `registered_dfs_participant` | string | — | yes | — | — |
| DFS Unit ID | `dfs_unit_id` | string | — | no | — | — |
| DFS Volume MW | `dfs_volume_mw` | float64 | — | yes | — | — |
| From | `window_from` | string | — | no | — | — |
| To | `window_to` | string | — | yes | — | — |
| Service Requirement Type | `service_requirement_type` | string | — | no | — | — |
| Utilisation Price GBP per MWh | `utilisation_price_gbp_per_mwh` | float64 | — | yes | — | £/MWh |
| Status | `status` | string | — | yes | — | — |
| North Scotland | `north_scotland` | float64 | — | yes | — | — |
| South and Central Scotland | `south_and_central_scotland` | float64 | — | yes | — | — |
| North East England | `north_east_england` | float64 | — | yes | — | — |
| North West England | `north_west_england` | float64 | — | yes | — | — |
| Yorkshire | `yorkshire` | float64 | — | yes | — | — |
| East Midlands | `east_midlands` | float64 | — | yes | — | — |
| West Midlands | `west_midlands` | float64 | — | yes | — | — |
| London | `london` | float64 | — | yes | — | — |
| East England | `east_england` | float64 | — | yes | — | — |
| South East England | `south_east_england` | float64 | — | yes | — | — |
| South West England | `south_west_england` | float64 | — | yes | — | — |
| Southern England | `southern_england` | float64 | — | yes | — | — |
| North Wales Merseyside and Cheshire | `north_wales_merseyside_and_cheshire` | float64 | — | yes | — | — |
| South Wales | `south_wales` | float64 | — | yes | — | — |
| Other | `other` | float64 | — | yes | — | — |
| Total | `total` | float64 | — | yes | — | — |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Event ID | `event_id` | string | — | yes | — | — |
| Event Type | `event_type` | string | — | yes | — | — |
| Event Tag | `event_tag` | string | — | yes | — | — |
| Delivery Date | `delivery_date` | date | `%d/%m/%Y` | no | — | YYYY-MM-DD |
| From_Local | `window_from` | string | — | no | — | HH:MM |
| To_Local | `window_to` | string | — | yes | — | HH:MM |
| From_UTC | `window_from_utc` | string | — | yes | — | HH:MM |
| To_UTC | `window_to_utc` | string | — | yes | — | HH:MM |
| Registered DFS Participant | `registered_dfs_participant` | string | — | yes | — | — |
| DFS Unit ID | `dfs_unit_id` | string | — | no | — | — |
| Zone | `zone` | string | — | yes | — | — |
| DFS Procured MW | `dfs_procured_mw` | float64 | — | yes | — | MW |
| Service Requirement Type | `service_requirement_type` | string | — | no | — | — |
| Utilisation Price GBP per MWh | `utilisation_price_gbp_per_mwh` | float64 | — | yes | — | £/MWh |
| Status | `status` | string | — | yes | — | — |

- Entity key: `resource_id`, `delivery_date`, `window_from`, `service_requirement_type`, `dfs_unit_id`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: date_sp1 (`delivery_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What it is.** The outcome of each bid: one row per DFS unit and service window with the status (`Accepted` or
`Rejected`), the bid quantity and the utilisation price. Silver holds the **current resource only**: 14,663 rows, of
which 10,773 are Accepted and 3,890 Rejected, delivery dates 2026-04-14 to 2026-10-06. Provider
(`registered_dfs_participant`) is an attribute; the measured key does not need it. Epoch 1 (archive, regional wide
format, 25 columns) is frozen in the registry so the archive capture fails on its key guard and not on header drift;
**no archive report row is in silver** (next section). Epoch 2 (current, 15 columns) is the only epoch with rows.

**Procured quantity and status.** `dfs_procured_mw` (current) and `dfs_volume_mw` (archive) are **separate silver
names** for different vendor fields and are never coalesced. The current `dfs_procured_mw` is the quantity of the bid
and is **positive on Rejected rows**, so accepted procurement is `SUM(dfs_procured_mw) WHERE status = 'Accepted'`.
Zone is a long-form identifier (`zone`, a string); the archive's 14 regional columns plus `other` and `total` are
**tendered regional volume**, never summed into or substituted for `dfs_volume_mw` (`TODO: verify`
REGIONAL-RECONCILIATION).

**Two clocks.**

- **Vintage: `available_at` = `published_at` = the CKAN `last_modified` of the captured file** (ADR-030), here
  2026-10-06T11:06:32Z for every silver row. It is a file stamp: a bid outcome is a retrospective event row and the
  file is refreshed in place, so `available_at` is not the time a given bid result was first known.
- **Event time: `event_time` = `timestamp_utc` = `delivery_date` anchored at the first settlement period on the
  Europe/London day, in tz-aware UTC** (`date_sp1`): 2026-04-14 is 2026-04-13T23:00Z (British Summer Time), and the
  silver `event_time` runs 2026-04-13T23:00Z to 2026-10-05T23:00Z. A date-label anchor, **not a window start**; the
  window start is the string pair `window_from` (local) and `window_from_utc` (UTC), e.g. local `16:00` is UTC
  `15:00` in summer. Verified: `event_time` equals `timestamp_utc` on all rows.

**Units (vendor dictionary as cited in K-DFS-FACTS g4; the generated unit column above is blank for the archive
quantities, the dictionary supplies them).** `dfs_procured_mw`, `dfs_volume_mw` (archive tendered volume), and every
archive regional column, `other` and `total`: **MW**. `utilisation_price_gbp_per_mwh`: **£/MWh**. `event_id`, `zone`,
`registered_dfs_participant`, `dfs_unit_id` and the labels: identifiers/categories with no unit. Archive dictionary:
[NESO archive report dictionary](https://www.neso.energy/data-portal/demand-flexibility/dfs_utilisation_report_archive_20252026).

**Sentinels and typing (g5, g6).** No blank cell or sentinel token in either resource. In the current resource the
numeric columns have no zero or negative values. In the archive the regional columns contain long runs of zero, which
the vendor's submission guidance permits where allocation information is unavailable; they are kept, not nulled
(`total` is zero in 206 archive rows while the bid volume is non-zero, below). Strict UTF-8 and CSV parsing agree with
the production reader on every row.

**Identity.** Current key (`resource_id`, `delivery_date`, `window_from`, `service_requirement_type`, `dfs_unit_id`):
14,663 distinct of 14,663 rows. The key never includes provider.

**Recorded failure of the archive resource (ADR-040, RULINGS 804).** The Archive 2025/2026 report (9,950 bronze rows,
resource `cc36fff5-5f6f-4fde-8932-c935d982ecd8`) **repeats four whole rows identical on every published column**:
the units `AXLE-01` and `AXLE-03` each at 2025-01-05 16:00 and 16:30, all four Rejected. The same key has 9,946
distinct values across 9,950 rows, and adding the end label, status, price or any published field cannot tell the
repeats apart, so **no published-column key is lossless**. The duplicate guard therefore fails the capture with
`DuplicateEntityKeyError` (activation: 8 rows sharing a key, four repeated pairs), and it stays unloaded with its
failure record. Nothing is deduplicated, re-keyed or given an occurrence index. This is a recorded failure, not a
hold of the family: a corrected NESO upload re-enters loudly. Question for NESO: *are the repeated AXLE-01 and
AXLE-03 rows of 2025-01-05 16:00 and 16:30 separate bids or a publication defect, and can NESO publish a corrected
file or a bid identifier?* `TODO: verify` ARCHIVE-REPORT-IDENTITY. Facts measured on the **bronze body, not in
silver**: regional columns sum to `total` in 9,352 of 9,950 rows and `total` equals the bid volume in 9,730 (diagnostic
tolerance 0.000001 MW), with `total` zero but the bid volume non-zero in 206 rows (K-DFS-FACTS report g5), which is why
the regional values are never summed to rebuild the bid volume. The reconcile gate adjudicated this failure; the
resource disposition stays `SILVER`.

### `demand_flexibility_utilisation_summary`

- Kind: tabular · archetype: EVT · refresh: adhoc · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Delivery Date | `delivery_date` | date | `%d/%m/%Y` | no | — | YYYY-MM-DD |
| From | `window_from` | string | — | no | — | — |
| To | `window_to` | string | — | yes | — | — |
| Service Requirement Type | `service_requirement_type` | string | — | no | — | — |
| Service Requirement MW | `service_requirement_mw` | float64 | — | yes | — | MW |
| DFS Procured MW | `dfs_procured_mw` | float64 | — | yes | — | MW |
| DFS Provider Bids Accepted Total Cost GBP | `dfs_provider_bids_accepted_total_cost_gbp` | float64 | — | yes | — | £ |
| Settled Volume MW | `settled_volume_mw` | float64 | — | yes | — | MW |
| Settled Cost GBP | `settled_cost_gbp` | float64 | — | yes | — | £ |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Event ID | `event_id` | string | — | yes | — | — |
| Event Type | `event_type` | string | — | yes | — | — |
| Event Tag | `event_tag` | string | — | yes | — | — |
| Delivery Date | `delivery_date` | date | `%d/%m/%Y` | no | — | YYYY-MM-DD |
| From_Local | `window_from` | string | — | no | — | HH:MM |
| To_Local | `window_to` | string | — | yes | — | HH:MM |
| From_UTC | `window_from_utc` | string | — | yes | — | HH:MM |
| To_UTC | `window_to_utc` | string | — | yes | — | HH:MM |
| Service Requirement Type | `service_requirement_type` | string | — | no | — | — |
| Service Requirement MW | `service_requirement_mw` | float64 | — | yes | — | MW |
| DFS Procured MW | `dfs_procured_mw` | float64 | — | yes | — | MW |
| DFS Provider Bids Accepted Total Cost GBP | `dfs_provider_bids_accepted_total_cost_gbp` | float64 | — | yes | — | £ |
| Settled Volume MW | `settled_volume_mw` | float64 | — | yes | — | MW |
| Settled Cost GBP | `settled_cost_gbp` | float64 | — | yes | — | £ |

- Entity key: `resource_id`, `delivery_date`, `window_from`, `service_requirement_type`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: date_sp1 (`delivery_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What it is.** One row per delivery window and requirement type: the requirement, what was procured, the total cost of
accepted bids, and (after settlement data arrives) the settled volume and cost. Silver holds 2,360 rows: 1,130 from the
archive (delivery 2024-11-29 to 2026-03-27) and 1,230 from the current resource (2026-04-14 to 2026-10-06). The 1,230
current rows carry a non-null `event_id` and the UTC labels; the 1,130 archive rows hold null there. NESO
[archive summary dictionary](https://www.neso.energy/data-portal/demand-flexibility/dfs_utilisation_report_summary_archive_20252026).

**Procurement duplicates the report; settlement is extra.** Procurement equals an aggregation of the window's Accepted
report rows: the current summary's procurement volumes match the Accepted bid sums and its accepted cost matches within
a diagnostic £1; the archive procurement components reconcile the same way. Worked example, current event 142, delivery
2026-10-06, local `16:00` to `16:30` (UTC `15:00`): 22 Accepted report rows sum to 49.9 MW, and the summary says 49.9 MW
and £4,816.22, with settlement still blank. Archive example, 2026-03-27 `16:30` to `17:00`: 5 Accepted rows, 8 MW and
£432 in both the report aggregation and the summary, with settled 2.69 MW and £145.44. **Never add summary and report
procurement together**; settlement fields cannot be derived from bids. The summary is also updated after procurement
(settlement fields appear once settlement data is received), which the file's single `last_modified` does not resolve.

**Two clocks.**

- **Vintage: `available_at` = `published_at` = the CKAN `last_modified` of the captured file** (ADR-030):
  2026-04-09T08:55:59Z for the archive resource and 2026-10-06T11:06:52Z for the current one. Settlement values are
  added to existing windows after the event, so this is **not** the time a settled number became known, and a
  backtest must not treat the settled columns as known at the auction.
- **Event time: `event_time` = `timestamp_utc` = `delivery_date` anchored at the first settlement period on the
  Europe/London day, in tz-aware UTC** (`date_sp1`); the current series runs 2026-04-13T23:00Z to 2026-10-05T23:00Z and
  the archive series 2024-11-29T00:00Z to 2026-03-27T00:00Z. Not a window start; the window labels stay strings
  (current local plus UTC; archive documented local, in contrast to the archive requirement's GMT, `TODO: verify`
  ARCHIVE-CLOCK-CONSISTENCY).

**Units (vendor dictionary as cited in K-DFS-FACTS summary g4).** `service_requirement_mw`, `dfs_procured_mw` and
`settled_volume_mw`: **MW**. `dfs_provider_bids_accepted_total_cost_gbp` and `settled_cost_gbp`: **£**. There is no MWh
column in this summary. The labels, `event_*` and `service_requirement_type` carry no unit.

**Sentinels and typing (g5, g6).** Blank settlement cells stay null: 514 blanks in each settlement column (2 archive,
512 current, which are windows not yet settled). **Negative settled values stay signed**: 42 negative `settled_volume_mw`
and 45 negative `settled_cost_gbp` (all in the current resource); these are numeric values and not a `-1` sentinel.
Their business meaning (an adjustment or a delivery in the opposite direction) is not stated by the vendor: `TODO:
verify` SIGNED-SETTLEMENT-SEMANTICS. Zero accepted quantity and cost are real values (the accepted columns contain long
zero runs) and are kept. No lexical repair, no bound, no sign change.

**Identity.** Key (`resource_id`, `delivery_date`, `window_from`, `service_requirement_type`): 1,130 of 1,130 archive and
1,230 of 1,230 current rows are unique. The current resource has 142 distinct Event IDs (against 113 in the report); why the report has fewer events is not stated (`TODO: verify`). Vendor guarantee of the composite key: `TODO: verify`.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

The vendor says email alerts are triggered by any modification to the files. The current resources are re-published in
place (the current requirement resource's `last_modified` moved from 2026-10-06 to 2026-10-08 between the catalogue
snapshot and the capture), while the Archive 2025/2026 resources carry March and April 2026 stamps. gridflow has **one
capture per resource** (all on 2026-10-08), so whether a refresh appends to or replaces a file, and whether earlier
rows are ever amended, is unmeasured: `TODO: verify` by comparing later captures with the hash-pinned bodies.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence). Any output derived from
this package carries the attribution line "Supported by National Energy SO Open Data".

## Holds

- `demand_flexibility_service_requirement`: held: TODO: REQUIREMENT-ISSUE-AVAILABILITY — the DFS service requirement resources (current and Archive 2025/2026) carry no issue column and publish delivery windows starting on or before their last_modified (archive 1,126 of 1,132 starts, current 1,230 of 1,238), and the current DFS Submission Time_Local is the auction-close deadline, not a publication time; when was each requirement first published, and does NESO retain earlier requirement editions? (The archive requirement dictionary labels From/To GMT while the archive report and summary dictionaries label theirs local time — TODO: ARCHIVE-CLOCK-CONSISTENCY; window_from holds the vendor label of each resource as published.) (unit v0.22-K-DFS-a)

**What the hold means.** The requirement table is built (2,370 rows in silver, schema and clocks above) but **its
values are not published**: the file has no issue column and almost all of its windows start before the file's own
`last_modified`, so the table is a retrospective record and the vintage proves nothing about when a requirement was
known (the supplied forward-target rule fails, RULINGS 529). The hold question above, in unit `v0.22-K-DFS-a`, is the
E-SEM question; what settles it is an immutable per-requirement publication time or an explicit seat ruling to accept
a retrospective contract. The hold is on that one family: the notification, report and summary are eligible as
retrospective event tables at `issue: none` and vintage `ckan_last_modified` (RULINGS 803 facts, 804 split and
archive-report failure, 807 merge, 809 activation).

**Other open questions that do not hold any output** (K-DFS-FACTS, carried as non-holding TODOs):

- `TODO: verify` ARCHIVE-CLOCK-CONSISTENCY: the archive requirement dictionary labels `From` / `To` GMT, the archive
  report and summary dictionaries label them local time. A corrected dictionary or an export specification settles it.
- `TODO: verify` ARCHIVE-REPORT-IDENTITY: the repeated archive report rows (above).
- `TODO: verify` REGIONAL-RECONCILIATION: whether archive regional columns should sum to `total` and to the bid volume.
- `TODO: verify` SIGNED-SETTLEMENT-SEMANTICS: negative settled values (above).
- `TODO: verify` ENDPOINT-CLOSURE: inclusive or exclusive window end.
- `TODO: verify` EVENT-ID-NAMESPACE: whether future resource editions reuse an Event ID.
- `TODO: verify` NOTIFICATION-ISSUE-RETENTION and NOTIFICATION-EMPTY-LIFECYCLE (notification section).

## Known issues and gotchas

- **Two seasons, one table: stack, do not merge.** Archive and current rows are disjoint seasons from different
  resources. Filter by `resource_id` when you need one season; an archive row has null event and UTC-label columns.
- **`event_time` is a date anchor, not the window.** It is the Europe/London midnight (first settlement period) of the
  date label, so in summer it is 23:00Z of the previous UTC day. Use the string labels `window_from` /
  `window_from_utc` for the within-day position, and do not build instants from them in the archive until the clock
  question is settled. Every delivery window measured is 30 minutes long, there is no settlement-period column, and
  no delivery row falls on a clock-change Sunday.
- **Procured MW is positive on rejected bids.** Filter on `status = 'Accepted'` before summing accepted MW. A count of
  all report rows is bids, not accepted units.
- **Never add the summary to the report.** Summary procurement is the Accepted report rows; the pair is two views of
  one quantity.
- **Settled values can be negative or blank.** 512 current summary windows have no settlement yet, and 42 volumes and 45
  costs are negative. Do not coalesce blanks to zero or take absolute values.
- **Requirements are held and the archive report is not tabled.** The report silver table has no rows before
  2026-04-14, so there is no bid history for 2024-11-29 to 2026-03-27 even though the archive summary covers it.
- **`dfs_volume_mw` and `dfs_procured_mw` are different fields** (archive tendered volume against current procured
  volume) and are separate silver columns; both are null in the epoch that does not have them.
- **No `run_type`, no revision column.** These are bid, award and outturn tables with no settlement run; the vintage is
  the file's `last_modified` and a later capture replaces that resource's rows (ADR-039).
- **Window-label clocks differ by epoch and file.** Current: local plus UTC (all boundary pairs agree under
  Europe/London); archive requirement: documented GMT; archive report and summary: documented local.

Related pages: @./short-term-operating-reserve-stor-day-ahead-buy-curve.md,
@./short-term-operating-reserve-stor-day-ahead-auction-results.md,
@../../../20-domain/concepts/settlement-period.md.
