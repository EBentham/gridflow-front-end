---
source: "neso_data_portal"
package: "demand-flexibility-service"
dataset_keys: ["dfs_industry_notification", "dfs_service_requirements", "dfs_utilisation_report", "dfs_utilisation_report_sum"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-14
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Demand Flexibility Service 2023/24
  summary: >-
    NESO's Demand Flexibility Service, winter 2023/24: per half-hour window, the volume asked,
    bids accepted and their cost, and what was delivered.
  facts:
    vendor: "NESO Data Portal, package `demand-flexibility-service`: four tables, one CSV file each"
    cadence: "Not Active in NESO's catalogue; NESO no longer updates the files"
    grain: "Summary: one row per half-hour delivery window; the report adds DFS unit"
    history: "Winter 2023/24: delivery dates 16 November 2023 to 21 March 2024"
  landscape: market
  what_it_is: >-
    NESO's Demand Flexibility Service for winter 2023/24. For each half-hour window NESO published
    a requirement, providers bid volume and price per DFS unit, and NESO accepted bids; the
    summary totals each window and later adds settled delivery. `Live` and `Test` events share
    each file, and both were settled. There is no event id: rows join on date and window.
  how_used:
    - DFS accepted and settled cost per event day, as a winter balancing-cost feature.
    - "Bid stacks from the report: Accepted and Rejected volume against price, per window."
    - Delivered against accepted MW per window; settlement came later, so not known at auction.
  chart:
    type: line
    silver: neso_data_portal/dfs_utilisation_report_sum
    time: delivery_date
    values:
      - {column: dfs_provider_bids_accepted_total_cost_gbp, series: accepted}
      - {column: settled_cost_gbp, series: settled}
    dedup: {"on": [delivery_date, window_from], order_by: published_at}
    aggregation: sum
    window: {start: "2023-11-16", end: "2024-03-21"}
    unit: "£"
  chart_view:
    title: Accepted and settled DFS cost per day, winter 2023/24
    caption: >-
      Silver `dfs_utilisation_report_sum`, £: each delivery date's indicative accepted cost and
      settled cost, summed over its windows, 16 November 2023 to 21 March 2024. Days with no event
      are absent. 29 November and 1 December are `Live`; the rest `Test`.
    alt: >-
      Dot chart of NESO's Demand Flexibility Service cost per day in pounds from
      neso_data_portal/dfs_utilisation_report_sum, 16 delivery dates from 16 November 2023 to 21
      March 2024, accepted cost and settled cost. The two Live days lead: accepted £3,031,162 and
      £3,573,586, settled £2,299,489 and £2,464,136. Test days to 17 January sit between about
      £0.59 million and £1.56 million. Both series fall from 2 February and stay under £90,000 from 29
      February; the lowest is 1 March, £15,911 accepted and £15,276 settled.
    x_label: delivery date; days with no event absent
    key:
      - {series: accepted, label: Accepted cost, paint: petrol, note: "Indicative cost of accepted bids, NESO's figure; highest £3,573,586 on 1 December (`Live`)."}
      - {series: settled, label: Settled cost, paint: clay, note: "Cost of the delivered volume once settled; above accepted cost on 7 of the 16 days."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each table's one file downloaded whole
      unless its `last_modified` is unchanged. Dates select nothing; NESO no longer updates the files.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=demand-flexibility-service"
    commands:
      - {run: gridflow pipeline neso_data_portal dfs_utilisation_report_sum --last 24h, comment: "summary file to bronze, then silver"}
      - {run: gridflow pipeline neso_data_portal dfs_utilisation_report --last 24h, comment: "report file, read by the notebook"}
  record:
    select:
      filter:
        - {column: delivery_date, op: in, value: ["2023-11-29", "2023-12-15", "2024-03-21"]}
      dedup: {"on": [delivery_date, window_from], order_by: published_at}
      order_by: [delivery_date, window_from]
      columns: [delivery_date, window_from, service_requirement_type, dfs_required_mw, dfs_procured_mw,
                settled_volume_mw, dfs_provider_bids_accepted_total_cost_gbp, settled_cost_gbp, window_to,
                timestamp_utc, published_at]
    key: [delivery_date, window_from]
    caption: "`Live` windows of 29 November 2023; `Test` windows of 15 December 2023 and 21 March 2024."
    fields:
      delivery_date: Delivery date of the window, as NESO labels it
      window_from: "Window start, NESO's `HH:MM` label, GMT in its dictionary; kept as text"
      service_requirement_type: "`Live` or `Test`, NESO's event type; the summary settles both"
      dfs_required_mw: Requirement NESO published for the window, MW
      dfs_procured_mw: "Total accepted MW: the report's Accepted bids summed, so never add both"
      settled_volume_mw: Delivered volume, MW, once settled (NESO); above accepted MW in some windows
      dfs_provider_bids_accepted_total_cost_gbp: "Indicative cost of the accepted bids, £, as NESO publishes it"
      settled_cost_gbp: Cost of the delivered volume, £, once settled (NESO)
      window_to: "Window end, NESO's `HH:MM` label, GMT in its dictionary; kept as text"
      timestamp_utc: "Set by gridflow: 00:00 UK time on the delivery date, in UTC"
      published_at: "NESO's last-modified time for the whole file, read as UTC"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `query()` reads each table's `_latest` view, filtering `delivery_date` with both ends
      included; lineage columns dropped. Times come back in UK time, so the first cell converts
      them to UTC. Window labels stay text.
    cells:
      - |
        s = data.neso_data_portal.query("dfs_utilisation_report_sum", "2023-11-16", "2024-03-21")
        r = data.neso_data_portal.query("dfs_utilisation_report", "2023-11-16", "2024-03-21")
        for df in (s, r):
            df["timestamp_utc"] = df.timestamp_utc.dt.tz_convert("UTC")
        s = s.sort_values(["delivery_date", "window_from"], ignore_index=True)
        s[["delivery_date", "window_from", "window_to", "timestamp_utc", "service_requirement_type"]].head(4)
      - |
        key = ["delivery_date", "window_from"]
        accepted = (r[r.status == "Accepted"].groupby(key, as_index=False).dfs_volume_mw.sum()
                    .rename(columns={"dfs_volume_mw": "accepted_bids_mw"}))
        w = s[key + ["service_requirement_type", "dfs_required_mw", "dfs_procured_mw",
                     "settled_volume_mw"]].merge(accepted, on=key)
        w.head(8)
      - |
        colour = w.service_requirement_type.map({"Live": "#C77E3C", "Test": "#155A6E"}).tolist()
        ax = w.plot.scatter(x="dfs_procured_mw", y="settled_volume_mw", c=colour, figsize=(5, 4),
                            xlabel="accepted MW", ylabel="settled MW")
        ax.axline((0, 0), slope=1, color="grey", lw=0.8);
    needs: the summary and report tables for winter 2023/24
    plot_alt: >-
      Scatter plot of settled against accepted MW per window, with a grey line where the two are
      equal. The six Live windows (clay) sit at 449 to 487 MW accepted and 299 to 358 MW settled,
      all below the line. Test windows (petrol) run from 56 to 523 MW accepted; 12 sit above the line.
  related:
    - {dataset: neso_data_portal/demand-flexibility, note: "The successor page NESO points to for later results"}
    - {dataset: neso_data_portal/demand-flexibility-service-live-events, note: "Winter 2022/23 `Live` events, a separate series; never add"}
    - {dataset: neso_data_portal/demand-flexibility-service-test-events, note: "Winter 2022/23 `Test` events, a separate series; never add"}
    - {dataset: elexon/system_prices, note: Imbalance prices for the same half-hours as each window}
  family:
    slug: demand-flexibility-service
    members:
      - dataset: dfs_utilisation_report_sum
        differs: "Window totals: MW asked and accepted, accepted cost, then settled volume and cost"
        request: "GET https://api.neso.energy/dataset/e5277fca-2a2b-4836-933b-f24a676b9ed8/resource/71a9cb04-8935-4e3a-bdd6-17f6fff0a7c6/download/dfs-utilisation-report-summary.csv"
      - dataset: dfs_utilisation_report
        differs: "Bids per DFS unit, Accepted or Rejected, with tendered MW split by region"
        request: "GET https://api.neso.energy/dataset/e5277fca-2a2b-4836-933b-f24a676b9ed8/resource/ed7019b0-32b7-425c-a2fb-5ba9e32733fb/download/dfs-utilisation-report.csv"
      - dataset: dfs_industry_notification
        differs: "Notices that a requirement may be, or has been, published for a date"
        request: "GET https://api.neso.energy/dataset/e5277fca-2a2b-4836-933b-f24a676b9ed8/resource/94b4d470-a54e-41d7-ae6e-be158db9b9d4/download/dfs-industry-notification.csv"
      - dataset: dfs_service_requirements
        differs: "Requirement per window: MW, guaranteed acceptance price and eligible providers"
        request: "GET https://api.neso.energy/dataset/e5277fca-2a2b-4836-933b-f24a676b9ed8/resource/7914dd99-fe1c-41ba-9989-5784531c58bb/download/dfs-service-requirements.csv"
        held: The requirement file has no publication time; the notices give one only per date.
---

# Demand Flexibility Service 2023/24

The Demand Flexibility Service (DFS) is how the National Energy System Operator (NESO) bought short-notice demand
reductions from registered providers during peak winter demand: for a half-hour delivery window NESO published a
requirement, providers bid demand-reduction volume per DFS unit, NESO accepted bids, and the delivered volume was settled
afterwards. This package is the **Winter 2023/24 results page**. The vendor's package text says it holds "updates and
information relating to both **live** and **test** DFS events" and ends with "This dataset will no longer be updated"
(CKAN package `notes`, @.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json; NESO
[Demand Flexibility Service 2023/24](https://www.neso.energy/data-portal/demand-flexibility-service)). For the vendor's
latest auction results it points at the successor package, documented in @./demand-flexibility.md.

**This is a frozen historical series.** Four CSV files, one per family, each captured once. The delivery dates run from
2023-11-16 to 2024-03-21 in the three eligible families. The files carry **both Test and Live events in one table**,
kept explicit in a type column (`service_requirement_type`, or `requirement_type` in the notification file). **Test
events are real deliveries, not dummy data**: the vendor's participation guidance describes tests as exercising the
operational process with real provider delivery, and NESO settled them (the summary file has settled volumes and costs
for Test windows). Do not drop `Test` rows as noise, and do not treat the two types as interchangeable either.

What a model gets from it:

| Family | What one row is | Silver rows | Status |
|---|---|---:|---|
| `dfs_industry_notification` | one notice to industry: an anticipated-requirement notice, or "requirement published" | 30 | eligible |
| `dfs_service_requirements` | one delivery window of one requirement (Test or Live) | 32 | **held** |
| `dfs_utilisation_report` | one bid outcome (Accepted or Rejected) of one DFS unit in one window, with tendered MW split by region | 1,220 | eligible |
| `dfs_utilisation_report_sum` | one window total: required, procured, accepted cost, settled volume and cost | 32 | eligible |

Package silver total: **1,314 rows** (1,282 in the three eligible families and 32 in the held requirement family).
Activation 2026-10-08, transform window `2026-10-08..2026-10-08`, no prior silver, one resource per family, **0
validation failures and 0 rows excluded** (@.planning/v0.22-RESULTS.md section DFS-b; RULINGS 814, 816).

**How the rows relate.**

- **There is no event id in this package.** Rows join **only on delivery date plus window start (plus DFS unit for bids),
  and only within this package.** The notification file has no event id at all, so a notification relates to a
  delivery only through its `requirement_for` date (a date-level association, not an identity).
- **Window labels are GMT labels kept raw.** `window_from` / `window_to` hold the vendor's `HH:MM` text exactly as
  published; the vendor documents them as GMT. The engine has no date-plus-clock-label recipe (RULINGS 572 / 588), so
  no window start or end instant is computed anywhere. Every window is 30 minutes long, there is no settlement-period
  column, and no delivery date is a clock-change Sunday.
- **Summaries are published values.** The summary's procurement fields equal the aggregate of the Accepted report rows
  of the same window (checked on all 32 windows, below), so **never add summary procurement to report procurement**.
  Its settlement fields are later outturn and cannot be derived from the bids.
- **The frozen 2022/23 Live and Test packages are separate series.** They are `demand-flexibility-service-live-events`
  and `demand-flexibility-service-test-events`, with their own tables and no shared delivery date with each other.
  Never add them to this package or to each other.
- **Requirements are held.** The requirement table is built in silver, but no requirement value is published from this
  page or from a published artifact (Holds). The 2022/23 Live requirement is the one requirement table in the three
  frozen packages that is not held.
- **Successor package.** The current service, with event ids, explicit local and UTC clocks and zonal caps, is
  @./demand-flexibility.md. Its tables are a different epoch, not a continuation of these files; do not stack them
  without reading that page.

Related pages in this vendor: @./demand-flexibility-service-live-events.md, @./demand-flexibility-service-test-events.md
(the 2022/23 frozen series), @./demand-flexibility.md (the current service).

- Publisher group: Demand Flexibility Service
- Registry group: dfs · archetype: EVT

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| DFS Industry Notification | CSV | upload | `94b4d470-a54e-41d7-ae6e-be158db9b9d4` |
| DFS Service Requirements | CSV | upload | `7914dd99-fe1c-41ba-9989-5784531c58bb` |
| DFS Utilisation Report | CSV | upload | `ed7019b0-32b7-425c-a2fb-5ba9e32733fb` |
| DFS Utilisation Report Summary | CSV | upload | `71a9cb04-8935-4e3a-bdd6-17f6fff0a7c6` |

All four resources are dispositioned `SILVER` to their own family and are CSV uploads. The package has **no
documentation (DOC) files and no other-disposition resources**, so there is no DOC download to link; the four data files
are downloadable from the URLs the vendor publishes (CKAN catalogue snapshot of 2026-10-06). The stable handle is the
resource id, not the file name. CKAN package id `e5277fca-2a2b-4836-933b-f24a676b9ed8`, author "National Grid ESO",
package created 2023-09-20.

| Family | Download | Newest capture (2026-10-08) | Bytes | Data rows | Captured `ckan_last_modified` |
|---|---|---|---:|---:|---|
| `dfs_industry_notification` | [dfs-industry-notification.csv](https://api.neso.energy/dataset/e5277fca-2a2b-4836-933b-f24a676b9ed8/resource/94b4d470-a54e-41d7-ae6e-be158db9b9d4/download/dfs-industry-notification.csv) | `raw_20261008T100622Z_94b4d470-a54e-41d7-ae6e-be158db9b9d4_7a8cf000.csv` | 4,501 | 30 | 2024-03-21T11:54:07 |
| `dfs_service_requirements` | [dfs-service-requirements.csv](https://api.neso.energy/dataset/e5277fca-2a2b-4836-933b-f24a676b9ed8/resource/7914dd99-fe1c-41ba-9989-5784531c58bb/download/dfs-service-requirements.csv) | `raw_20261008T100640Z_7914dd99-fe1c-41ba-9989-5784531c58bb_b6411b04.csv` | 21,755 | 32 | 2024-03-14T12:00:12 |
| `dfs_utilisation_report` | [dfs-utilisation-report.csv](https://api.neso.energy/dataset/e5277fca-2a2b-4836-933b-f24a676b9ed8/resource/ed7019b0-32b7-425c-a2fb-5ba9e32733fb/download/dfs-utilisation-report.csv) | `raw_20261008T100659Z_ed7019b0-32b7-425c-a2fb-5ba9e32733fb_23c27ea9.csv` | 168,260 | 1,220 | 2024-03-21T14:04:20 |
| `dfs_utilisation_report_sum` | [dfs-utilisation-report-summary.csv](https://api.neso.energy/dataset/e5277fca-2a2b-4836-933b-f24a676b9ed8/resource/71a9cb04-8935-4e3a-bdd6-17f6fff0a7c6/download/dfs-utilisation-report-summary.csv) | `raw_20261008T100705Z_71a9cb04-8935-4e3a-bdd6-17f6fff0a7c6_01be5836.csv` | 1,899 | 32 | 2024-04-10T07:56:25 |

Bronze path pattern: `C:/gridflow-data/bronze/neso_data_portal/<family>/2026/10/08/<file>`. Each family has exactly **one
resource and one capture**. Every body decoded as strict UTF-8 and its SHA-256 matched its sidecar; the production
CSV reader agreed with an independent strict parse on every row and cell (K-DFS-FACTS g6; gridflow
`@.planning/phases/v0.22-K-DFS/K-DFS-FACTS.md`). Byte and row figures are measured from the bodies, not copied from
the catalogue. Because there is one capture per resource, same-resource amendments cannot be measured:
`TODO: verify` by comparing any later capture with the hash-pinned bodies. All four families keep registry
`empty allowed: no` and refresh `frozen`.

## Families

Each family has one header epoch, matched one-to-one to the header the production reader returns (a UTF-8 BOM and edge
whitespace in header names are removed by the reader). Silver column names are the vendor name lower-cased with each run
of non-alphanumerics as one underscore, except `From` as `window_from` and `To` as `window_to` (SQL reserved words). Every
silver table also carries the engine columns `timestamp_utc`, `published_at`, `event_time`, `available_at`,
`capture_written_at`, `bronze_capture_id`, `source_run_id` and `dataset_version`.

**Units come only from the vendor field dictionary** (CKAN `datastore` field info, snapshot
@.planning/research/neso-snapshots/field-info/20261008T114228Z/), never from a column name. Where the dictionary leaves
the unit as `N/A` the table shows a dash.

**The two clocks (the same pattern for all four families).**

1. **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN `last_modified` of the captured
   file (ADR-030, gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). It is a file stamp, not a row
   issue time: the files carry no issue column, `issue` is none, and `last_modified` is not an immutable per-row
   publication instant.
2. **Event time (`date_sp1` on the family's date column).** `timestamp_utc` = `event_time` = the date label (delivery
   date, or the notification's issued date) anchored at the first settlement period of that Europe/London day and
   converted to tz-aware UTC at the silver boundary. It is a **date-label anchor, not a window start and not the
   notification time**. Every date in this package is in the GMT half of the year, so the anchor is `00:00Z` of the date
   (verified on every silver row, 2026-10-14). The within-day position is only the raw string `window_from`.

### `dfs_industry_notification`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Notification Issued Date | `notification_issued_date` | date | `%d/%m/%Y` | no | — | — |
| Notification Issued Time | `notification_issued_time` | string | — | no | — | HH:MM |
| Requirement For | `requirement_for` | date | `%d/%m/%Y` | no | — | — |
| Requirement Type | `requirement_type` | string | — | no | — | — |
| Status | `status` | string | — | yes | — | — |
| Notification Type | `notification_type` | string | — | no | — | — |

- Entity key: `notification_issued_date`, `notification_issued_time`, `requirement_for`, `requirement_type`, `notification_type`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`notification_issued_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Eligible.** 30 silver rows. The vendor describes the file as indicating when NESO is considering issuing a DFS
service requirement for a Live or Test event, has issued one, or has stood the service down after an Anticipated
Requirement Notice (ARN). Issued dates run from 2023-11-15 to 2024-03-21 and target dates (`requirement_for`) from
2023-11-16 to 2024-03-21. `requirement_type` is **28 Test and 2 Live**; `notification_type` is **16 Requirement
Published and 14 Anticipated Requirement Notice**. `status` is the free-text body of the notice; it is never mined for a
date. `notification_type` is the vendor's wording as published (its dictionary example spells the ARN value differently
from the data; the data spelling is the one stored).

**The two clocks.**

- **Vintage:** `published_at` = `available_at` = 2024-03-21T11:54:07.592418Z for every row. The newest issued time in
  the body is about 352 seconds after it, so `last_modified` is not a per-row issue time (K-DFS-FACTS notification
  g1/g2).
- **Event time:** `date_sp1` on `notification_issued_date`; `timestamp_utc` runs 2023-11-15T00:00Z to 2024-03-21T00:00Z.
  This is the posting date, not the notification instant: the date and time are separate fields the engine cannot
  compose, so the issue recipe is none and `notification_issued_time` stays a raw string. The vendor documents the
  time as **GMT**.

**Units.** None: every column is a date, a clock label or categorical / free text (K-DFS-FACTS g4).

**Sentinels and typing (g5, g6).** No blank, sentinel token or embedded comma, quote or newline. **14 `status` cells carry
trailing whitespace and are kept byte-equal**; nothing is trimmed or mapped to null. Dates are `dd/mm/yyyy` in the body.

**Identity.** 30 rows, 30 distinct issued-date-and-time pairs, 16 distinct target dates; the five-column key above is
unique across all 30 rows. It replaces the profiler's incidental key on `status`. Vendor guarantee of that composite:
`TODO: verify`. There is no event id. Non-holding open questions: `TODO: verify` NOTIFICATION-ISSUE-RETENTION (immutable
publication history plus a split date-and-time mechanism would settle an issue time).

### `dfs_service_requirements`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Delivery Date | `delivery_date` | date | `%d/%m/%Y` | no | — | — |
| From | `window_from` | string | — | no | — | 17:00 |
| To | `window_to` | string | — | yes | — | HH:MM |
| DFS Required MW | `dfs_required_mw` | float64 | — | yes | — | MW |
| Service Requirement Type | `service_requirement_type` | string | — | yes | — | — |
| Guaranteed Acceptance Price GBP per MWh | `guaranteed_acceptance_price_gbp_per_mwh` | float64 | — | yes | — | £/MWh |
| Despatch Type | `despatch_type` | string | — | yes | — | — |
| Participant Bids Eligible | `participant_bids_eligible` | string | — | yes | — | — |

- Entity key: `delivery_date`, `window_from`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`delivery_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**HELD. No value of this table is published from this page or from any published artifact.** The table is built in
silver (32 rows, 32 delivery windows, schema and clocks as above, 0 validation failures), and its row count and schema
are the only things stated here. The hold, and the question that settles it, are under Holds.

What the vendor says the file is: "MW requirements for Demand Flexibility Live and Test Events and details of Registered
DFS Participant bid eligibility". The dictionary defines the columns as follows.

**Units (vendor dictionary).** `dfs_required_mw` is **MW** (the volume of DFS required for the service window).
`guaranteed_acceptance_price_gbp_per_mwh` is **£/MWh** (the price at or below which NESO commits to accepting all
tendered bids for the window). `delivery_date`, `service_requirement_type` (Live or Test), `despatch_type` (all
participants, or a sub-group) and `participant_bids_eligible` (a comma-separated list) are dimensionless. **Dictionary
defect:** the `From` entry has its `unit` and `example` swapped (unit `17:00`, example `HH:MM`), which is why the table
above shows `17:00` as the vendor unit; both `From` and `To` are `HH:MM` clock labels documented as **GMT**.

**The two clocks.**

- **Vintage:** `published_at` = `available_at` = the CKAN `last_modified` of the capture, 2024-03-14T12:00:12.712070Z for
  every row.
- **Event time:** `date_sp1` on `delivery_date`. This is the service date, anchored at the first settlement period;
  the GMT window labels stay raw strings. There is no issue column, so `issue` is none.

**Sentinels and typing (g5, g6).** Blanks stay null, **zeros stay zero** (a zero guaranteed acceptance price is a real
value for competitive tests in the vendor's guidance, not a null token), nothing is trimmed or mapped. Participant lists
contain embedded commas inside quoted CSV cells and are kept as published. All casts passed strictly.

**Identity.** The key above (delivery date and window start) is unique across all 32 rows. It carries no event id; the
file has none. Vendor guarantee of that composite: `TODO: verify`.

### `dfs_utilisation_report`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Delivery Date | `delivery_date` | date | `%d/%m/%Y` | no | — | — |
| Registered DFS Participant | `registered_dfs_participant` | string | — | yes | — | — |
| DFS Unit ID | `dfs_unit_id` | string | — | no | — | — |
| DFS Volume MW | `dfs_volume_mw` | float64 | — | yes | — | MW |
| From | `window_from` | string | — | no | — | HH:MM |
| To | `window_to` | string | — | yes | — | HH:MM |
| Service Requirement Type | `service_requirement_type` | string | — | yes | — | — |
| Despatch Time | `despatch_time` | string | — | yes | — | — |
| Utilisation Price GBP per MWh | `utilisation_price_gbp_per_mwh` | float64 | — | yes | — | £/MWh |
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
| North Wales, Merseyside and Cheshire | `north_wales_merseyside_and_cheshire` | float64 | — | yes | — | MW |
| South Wales | `south_wales` | float64 | — | yes | — | MW |
| Other | `other` | float64 | — | yes | — | MW |
| Total | `total` | float64 | — | yes | — | MW |

- Entity key: `delivery_date`, `window_from`, `dfs_unit_id`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`delivery_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Eligible.** 1,220 silver rows over 32 delivery windows on 16 delivery dates (2023-11-16 to 2024-03-21): **59 DFS
units of 25 registered participants**. The vendor describes it as "details of DFS bid assessment for Live and Test
Events", with a breakdown by GSP, updated within about one hour of bid-submission gate closure (one hour after the
requirements are issued) and only on days with a service requirement. **One row is one bid outcome**, not one unit-day.

- `status`: **946 Accepted and 274 Rejected**. Provider is an attribute, not part of the key.
- `service_requirement_type`: **993 Test rows and 227 Live rows**.
- `despatch_time` is a **category**, not a time: **`day-ahead` 365, `within-day 1` 372, `within-day 2` 483**. The vendor
  describes it as the stage at which the requirement was issued (Day-Ahead, Within-Day AM or Within-Day PM); the data
  holds `within-day 1` and `within-day 2`. Whether 1 is AM and 2 is PM is `TODO: verify`. It is never parsed as a
  clock or used as an issue instant.
- The regional columns are the same tendered volume split across the 14 regions and `other`; `total` is the tendered
  total over all regions. The vendor dictionary calls these GSP groups.

**The two clocks.**

- **Vintage:** `published_at` = `available_at` = 2024-03-21T14:04:20.246404Z for every row. The report was documented as
  updated within about an hour of gate closure, so this one stamp is the last update of the whole season, not the
  time each row was known.
- **Event time:** `date_sp1` on `delivery_date`; `timestamp_utc` runs 2023-11-16T00:00Z to 2024-03-21T00:00Z. The
  window start/end stay raw GMT strings (`window_from`, `window_to`).

**Units (vendor dictionary).** `dfs_volume_mw` and every regional column and `total` are **MW**, all described as
**tendered** volume (the dictionary calls the report volume "DFS volume tendered for service window", not a delivered
volume). `utilisation_price_gbp_per_mwh` is **£/MWh** (tendered utilisation price; the dictionary types it as integer,
silver stores `float64`). Participant, unit, type, status and despatch time are dimensionless. The measured range is
`dfs_volume_mw` 1 to 94 MW and price £150 to £6,750 per MWh.

**Sentinels and typing (g5, g6).** No blank in any column, no sentinel token, no negative number, no percentage or
thousands formatting. Regional zeros are real values (the vendor's participation guidance permits a zero regional entry
where allocation information is unavailable) and are kept. The comma-bearing header `North Wales, Merseyside and
Cheshire` is one quoted CSV cell and one silver column.

**Regional columns are never summed into the bid volume.** `total` equals `dfs_volume_mw` on **all 1,220 rows**, but the
14 regions plus `other` sum to `total` on only **1,133 of 1,220** rows (diagnostic tolerance 0.000001 MW).
`TODO: verify` REGIONAL-RECONCILIATION (rounding versus optional regional allocation; a vendor note or corrected export
would settle it). Non-holding: the output stays eligible and the regional columns are kept as published.

**Identity.** 1,220 rows, 1,220 distinct (delivery date, window start, DFS unit) keys, supported by the service's one-bid
per unit per window grain. The key replaces the profiler's incidental choices. Vendor guarantee of that composite:
`TODO: verify`. There is no event id.

### `dfs_utilisation_report_sum`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Delivery Date | `delivery_date` | date | `%d/%m/%Y` | no | — | — |
| From | `window_from` | string | — | no | — | HH:MM |
| To | `window_to` | string | — | yes | — | HH:MM |
| Service Requirement Type | `service_requirement_type` | string | — | yes | — | — |
| DFS Required MW | `dfs_required_mw` | float64 | — | yes | — | MW |
| DFS Procured MW | `dfs_procured_mw` | float64 | — | yes | — | MW |
| DFS Provider Bids Accepted Total Cost GBP | `dfs_provider_bids_accepted_total_cost_gbp` | float64 | — | yes | — | £ |
| Settled Volume MW | `settled_volume_mw` | float64 | — | yes | — | MW |
| Settled Cost GBP | `settled_cost_gbp` | float64 | — | yes | — | £ |

- Entity key: `delivery_date`, `window_from`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`delivery_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Eligible.** 32 silver rows, one per delivery window (**26 Test and 6 Live**), 2023-11-16 to 2024-03-21. The vendor
describes it as a "summary of procured and delivered DFS volumes", updated after the utilisation report is updated and
when the relevant settlement data has been processed. **These are published values and are kept as published, never
recalculated.**

**The two clocks.**

- **Vintage:** `published_at` = `available_at` = 2024-04-10T07:56:25.272181Z for every row. This is the latest of the
  four files, as expected: the settlement fields arrive after the bid fields, so the stamp reflects the settlement
  update, not the time of procurement.
- **Event time:** `date_sp1` on `delivery_date`; `timestamp_utc` runs 2023-11-16T00:00Z to 2024-03-21T00:00Z. Window
  labels are raw GMT strings.

**Units (vendor dictionary).** `dfs_required_mw`, `dfs_procured_mw` and `settled_volume_mw` are **MW**.
`dfs_provider_bids_accepted_total_cost_gbp` ("indicative total cost of accepted DFS bids") and `settled_cost_gbp` are **£**
(a currency amount, not a rate). There is no MWh value column in this file. The dictionary titles the delivered fields
"Volume of DFS delivered" and "Cost of DFS delivered" (visible once settlement data is received); the data headers are
`Settled Volume MW` and `Settled Cost GBP`.

**Reconciles to the report, by construction.** On all 32 windows `dfs_procured_mw` equals the sum of `dfs_volume_mw`
over the Accepted report rows of the same date and window, and the accepted-bid total cost equals the sum of
`dfs_volume_mw x price x 0.5 h` within £1 (maximum difference £0.50, rounding of the published cost). Worked example,
2024-03-21 17:30 to 18:00 (Test): 26 Accepted report rows aggregate to 80 MW and £26,372, which is exactly what the
summary publishes as procured and accepted cost; the settlement fields on the same row are 71 MW and £24,363.
**Never add summary procurement to report procurement in gold** (the pair is two views of one quantity), and do not
rebuild settlement from bids.

**Sentinels and typing (g5, g6).** No blank, zero or negative numeric cell, and every window has a settled volume and
cost (none are blank in this frozen season; the current successor package differs). The file has a UTF-8 BOM and the
reader removes it. Settled volume exceeds procured volume on **12 of the 32 windows**: delivered can differ from
procured in either direction, so do not assume `settled <= procured` (`TODO: verify` the vendor's settlement semantics).

**Identity.** 32 rows, 32 distinct (delivery date, window start) keys. The key replaces the profiler's incidental key on
`settled_cost_gbp`. Vendor guarantee of that composite: `TODO: verify`. The 32 windows are the same 32 windows as the
requirement table, with none unmatched (K-DFS-FACTS, cross-package identity).

## Cadence

- Registry refresh: frozen
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Not Active

The vendor states "This dataset will no longer be updated" and retains it "to share historical data". The four files
carry last-modified stamps between 2024-03-14 and 2024-04-10, the last matching the settlement update of the summary. The
package metadata itself was last modified 2026-09-22 (CKAN `metadata_modified`), which is a catalogue edit, not a data
change. gridflow has one capture per resource, so whether any file is ever amended again is unmeasured: `TODO: verify`
by comparing later captures with the hash-pinned bodies. `TODO: verify` ENDPOINT-CLOSURE (whether the window end is
inclusive or exclusive; literal ends are kept).

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence). Any output derived from
this package carries the attribution line "Supported by National Energy SO Open Data".

## Holds

- `dfs_service_requirements`: held: TODO: REQUIREMENT-ISSUE-AVAILABILITY — the 2023/24 DFS service requirement upload (last_modified 2024-03-14) carries no issue column and publishes 32 delivery windows, 29 of them starting on or before its last_modified; when was each requirement first published, and does NESO retain earlier requirement editions? (unit v0.22-K-DFS-b)

**What the hold means.** The requirement table is loaded (32 rows in silver, schema and clocks above) but **its values are
not published**. The file has no issue column and 29 of its 32 windows start on or before the file's own
`last_modified`, so the table is a retrospective record and the vintage proves nothing about when a requirement was
known; the supplied forward-target exception (every target after the vintage, RULINGS 529) fails. This is the E-SEM
question: the unit of the requirement is MW, and the unanswered question is when each requirement became known to
the market. What settles it is an immutable per-requirement publication time (earlier requirement editions, or an
issue-specific file) or an explicit seat ruling accepting a retrospective contract. The hold is on that one family
(RULINGS 803 facts, 804 split, 814 merge, 816 activation, 801 pickup). The notification, report and summary are eligible
as retrospective event tables at `issue: none` and vintage `ckan_last_modified`.

**Other open questions that do not hold any output** (K-DFS-FACTS, carried as non-holding TODOs):

- `TODO: verify` NOTIFICATION-ISSUE-RETENTION: an immutable publication history plus a split date-and-time mechanism
  would settle an issue time for the notices.
- `TODO: verify` REGIONAL-RECONCILIATION: whether regional bid columns should sum to `total` and to the bid volume.
- `TODO: verify` the despatch-time labels `within-day 1` and `within-day 2` against the vendor's Within-Day AM and PM.
- `TODO: verify` settlement semantics where settled volume exceeds procured volume.
- `TODO: verify` ENDPOINT-CLOSURE: inclusive or exclusive window end.

## Known issues and gotchas

- **Frozen historical series.** No more data will arrive. The delivery dates end on 2024-03-21 and the series is not
  continued by the successor package; read @./demand-flexibility.md for the current service.
- **Test events are real deliveries.** Test rows are provider deliveries, settled like Live ones. They are not dummy
  data and not to be dropped. Equally, they are not Live: **filter on `service_requirement_type` (or
  `requirement_type` for notices)** and report the two separately. This table carries both in one file; the 2022/23
  series publishes them as two separate packages with no shared delivery date, which must never be added to this one or
  to each other.
- **No event id: join on date and window, within this package.** Reports and summaries join on `delivery_date` +
  `window_from` (+ `dfs_unit_id` for bids). Notices join to deliveries only by date through `requirement_for`. The date
  alone is not an event identity: there can be several windows and both types on one day.
- **Window labels are raw GMT strings.** `event_time` is the Europe/London midnight of the date label (00:00Z here), not
  the window start. Do not build instants by adding `window_from` unless you take the vendor's GMT label as given; all
  delivery dates fall in the GMT half of the year.
- **Never add summary procurement to report procurement.** `dfs_procured_mw` and the accepted cost in the summary are
  the Accepted report rows aggregated. Accepted volume is `WHERE status = 'Accepted'`; a plain sum of `dfs_volume_mw`
  over the report includes 274 Rejected bids.
- **Report volumes are tendered, not delivered.** Delivered volume and cost are only in the summary's settled fields.
- **Regional columns do not always sum to the bid.** Use `dfs_volume_mw` or `total` for the bid; regional columns only
  for the split (1,133 of 1,220 rows agree).
- **Padding is real.** 14 notification `status` cells have trailing whitespace and are kept byte-equal; do not compare
  `status` with an untrimmed literal.
- **Requirement values are held.** Do not read the held table into a published artifact or quote its values. The
  summary's `dfs_required_mw` is a separate published summary column and is not the requirement table.
- **No `run_type`, no revision column.** These are bid, award and outturn tables with no settlement run; never dedup on
  `(date, period)`; the vintage is the file's `last_modified`, and a later capture replaces the rows of that resource
  (ADR-039).

Related pages: @./demand-flexibility.md, @./demand-flexibility-service-live-events.md,
@./demand-flexibility-service-test-events.md, @../../../20-domain/concepts/settlement-period.md.
