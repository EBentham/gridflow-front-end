---
source: "neso_data_portal"
package: "demand-flexibility-service-test-events"
dataset_keys: ["dfs_test_events_service_requirement", "dfs_test_events_service_update_industry", "dfs_test_events_utilisation_report", "dfs_test_events_utilisation_report_sum"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-14
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Demand Flexibility Service 2022/23 test events
  summary: >-
    NESO's Demand Flexibility Service in winter 2022/23, test events only: MW asked per half-hour
    window, bids accepted, their cost and delivery.
  facts:
    vendor: "NESO Data Portal, package `demand-flexibility-service-test-events`: four tables, one CSV file each"
    cadence: "Not Active in NESO's catalogue; files last modified March 2023 or July 2026"
    grain: "Summary: one row per half-hour test window; the report adds DFS unit"
    history: "Test events on 19 days, 15 November 2022 to 28 March 2023"
  landscape: market
  what_it_is: >-
    NESO's Demand Flexibility Service test events, winter 2022/23; live events are a separate
    package. NESO set a MW requirement per half-hour window, providers bid per DFS unit the day
    before, and NESO accepted or rejected each bid. The summary adds a 10:00 update on the day and
    settled delivery. There is no event id: rows join on date and window.
  how_used:
    - Delivered against accepted MW per test window, for sizing what DFS bids deliver.
    - "Bid stacks from the report: Accepted and Rejected volume against price, per window."
    - Join report and summary on date and window, within this package only.
  chart:
    type: line
    silver: neso_data_portal/dfs_test_events_utilisation_report_sum
    time: date
    values:
      - {column: dfs_required, series: required}
      - {column: dfs_procured, series: accepted}
      - {column: settled_volume, series: settled}
    dedup: {"on": [date, window_from], order_by: published_at}
    aggregation: mean
    window: {start: "2022-11-15", end: "2023-03-28"}
    unit: MW
  chart_view:
    title: MW asked, accepted and settled per test day
    caption: >-
      Silver `dfs_test_events_utilisation_report_sum`, MW: each test day's requirement, D-1
      accepted volume and settled volume, averaged over its half-hour windows (two; four on 12
      December), 15 November 2022 to 28 March 2023. Days without a test are absent.
    alt: >-
      Dot chart from neso_data_portal/dfs_test_events_utilisation_report_sum of DFS test days, MW per
      half-hour window averaged over each day, 19 days from 15 November 2022 to 28 March 2023:
      requirement, D-1 accepted and settled volume. The requirement steps between 25 and 300 MW.
      Settled sits above accepted on the first five days (133.39 against 75.9 MW on 15 November) and
      below it on most later days. Accepted peaks at 268.33 MW on 15 March. Settled peaks at 269.0 on
      21 February; it is 0.725 MW on 21 March and 1.01 on 28 March.
    x_label: delivery date; days without a test absent
    y_min: -10
    key:
      - {series: required, label: Requirement, paint: olive, note: "The MW NESO asked for per window; 25 to 300 MW across the test days."}
      - {series: accepted, label: Accepted at D-1, paint: petrol, note: "Volume of the accepted bids; on average above the requirement on 19 January and 15 March."}
      - {series: settled, label: Settled, paint: clay, note: "Delivered volume; above accepted on the first five days, 1.01 MW or less on 21 and 28 March."}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each table's CSV downloaded whole unless
      its `last_modified` is unchanged. Dates select nothing; the window must end within 48 hours.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=demand-flexibility-service-test-events"
    commands:
      - {run: gridflow pipeline neso_data_portal dfs_test_events_utilisation_report_sum --last 24h, comment: "summary file to bronze, then silver"}
      - {run: gridflow pipeline neso_data_portal dfs_test_events_utilisation_report --last 24h, comment: "report file, read by the notebook"}
  record:
    select:
      filter:
        - {column: date, op: in, value: ["2022-11-15", "2023-01-19", "2023-03-21", "2023-03-28"]}
      dedup: {"on": [date, window_from], order_by: published_at}
      order_by: [date, window_from]
      columns: [date, window_from, dfs_required, dfs_procured, d0_dfs_procured, settled_volume,
                bids_accepted_total_cost, d0_bids_accepted_total_cost, settled_cost, window_to,
                timestamp_utc, published_at]
    key: [date, window_from]
    caption: "15 November, 19 January (morning), 21 and 28 March; 28 March is in British Summer Time."
    fields:
      date: "Date of the test event, NESO's `dd/mm/yyyy` label read as a date"
      window_from: "Window start, NESO's `HH:MM` label, GMT in its dictionary; kept as text"
      dfs_required: Requirement NESO published for the window, MW
      dfs_procured: "Volume accepted at D-1, MW: the report's Accepted bids summed, so never add both"
      d0_dfs_procured: "Accepted volume updated at 10:00 GMT on the day, MW; D-1 where no update"
      settled_volume: Volume delivered, MW, after the event once settlement data arrived (NESO)
      bids_accepted_total_cost: "Cost of the accepted volumes, £, as NESO publishes it"
      d0_bids_accepted_total_cost: "Cost updated at 10:00 GMT on the day, £; D-1 where no update"
      settled_cost: Cost of the volume delivered, £, once settled (NESO)
      window_to: "Window end, NESO's `HH:MM` label, GMT in its dictionary; kept as text"
      timestamp_utc: "00:00 UK time on `date`, in UTC (23:00 the day before for 28 March)"
      published_at: "NESO's last-modified time for the whole file, read as UTC"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `query()` reads each table's `_latest` view, filtering `date` with both ends included;
      lineage columns dropped. Times come back in UK time, so the first cell converts them to UTC.
      Window labels stay text.
    cells:
      - |
        s = data.neso_data_portal.query("dfs_test_events_utilisation_report_sum", "2022-11-15", "2023-03-28")
        r = data.neso_data_portal.query("dfs_test_events_utilisation_report", "2022-11-15", "2023-03-28")
        for df in (s, r):
            for c in ("timestamp_utc", "published_at"):
                df[c] = df[c].dt.tz_convert("UTC")
        s = s.sort_values(["date", "window_from"], ignore_index=True)
        s.iloc[[0, 1, -2, -1]][["date", "window_from", "window_to", "timestamp_utc", "published_at"]]
      - |
        r.groupby("status", as_index=False).agg(bids=("unit", "size"), units=("unit", "nunique"),
                                                 min_price=("price", "min"), max_price=("price", "max"))
      - |
        ax = s.plot.scatter(x="dfs_procured", y="settled_volume", color="#155A6E", figsize=(5, 4),
                            xlabel="accepted MW at D-1", ylabel="settled MW")
        ax.axline((0, 0), slope=1, color="grey", lw=0.8);
    needs: the summary and report tables of the 2022/23 test events
    plot_alt: >-
      Scatter plot of settled against D-1 accepted MW for the 40 test windows, with a grey line
      where the two are equal. Accepted runs from 7.0 to 270.69 MW, settled from 0.72 to 269.2. 17
      windows sit above the line, among them both 15 November windows: 74.31 and 77.49 MW accepted,
      125.36 and 141.42 settled.
  related:
    - {dataset: neso_data_portal/demand-flexibility, note: "NESO's current package for the service, from winter 2024/25"}
    - {dataset: neso_data_portal/demand-flexibility-service, note: "The next winter, 2023/24, with Test and Live rows in one table"}
    - {dataset: neso_data_portal/demand-flexibility-service-live-events, note: "Live events of the same winter, published separately: never add them"}
    - {dataset: elexon/system_prices, note: Imbalance prices for the same half-hours as each window}
  family:
    slug: demand-flexibility-service-test-events
    members:
      - dataset: dfs_test_events_utilisation_report_sum
        differs: "Window totals: MW asked and accepted, cost, D0 update, settled volume and cost"
        request: "GET https://api.neso.energy/dataset/22bc9bdd-4919-439a-95b8-5213bb3bdf4c/resource/e4804faf-92be-43d0-a1ec-3e52a50f9666/download/utilisation-report-summary-test280320231300-fs.csv"
      - dataset: dfs_test_events_utilisation_report
        differs: "Bids per DFS unit, Accepted or Rejected, with price and MW by region"
        request: "GET https://api.neso.energy/dataset/22bc9bdd-4919-439a-95b8-5213bb3bdf4c/resource/fc466b76-6823-4dd9-8b4a-aab464e0e77b/download/dfs-participant-utilisation-report-test280320231300.csv"
      - dataset: dfs_test_events_service_update_industry
        differs: "NESO's notices to industry by posting date: requirement anticipated, published or not issued"
        request: "GET https://api.neso.energy/dataset/22bc9bdd-4919-439a-95b8-5213bb3bdf4c/resource/a2dd7992-32d5-4723-b0f5-273caaecbde1/download/service-update-industry-notifications-test270320231430.csv"
      - dataset: dfs_test_events_service_requirement
        differs: MW NESO asked for per window, with the window's GMT start and end labels
        request: "GET https://api.neso.energy/dataset/22bc9bdd-4919-439a-95b8-5213bb3bdf4c/resource/000066dc-aa75-4bec-a5a2-9c935b1873d2/download/dfs-service-requirement-test270320231430.csv"
        held: The requirement file has no publication time; the notices give one only per date.
---

# Demand Flexibility Service 2022/23: Test Events

This package is NESO's published record of the **test events of the first winter of the Demand Flexibility Service
(DFS), November 2022 to March 2023**. The DFS is how NESO buys short-notice demand reductions from registered
providers for a half-hour delivery window: NESO publishes a requirement, providers bid demand-reduction volume per
DFS unit, NESO accepts bids up to the requirement, and delivered volume is settled afterwards. The vendor describes
the organisation's data as "our test and live DFS events" for a service giving extra flexibility during peak winter
demand (CKAN organisation text, `.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json`; NESO
[DFS test events](https://www.neso.energy/data-portal/demand-flexibility-service-test-events)).

**Frozen historical series.** The package's update frequency is "Not Active" and the registry refresh is `frozen`.
Nothing new is expected; a model reads it as a closed 2022/23 history.

**Test events are real deliveries, not dummy data.** The applicable NESO guidance describes tests as exercising real
provider delivery under the same operational process as live events, with onboarding and regular tests and
guaranteed-acceptance arrangements (K-DFS-FACTS, package `demand-flexibility-service-test-events`). The bids,
volumes and settled quantities are real provider behaviour. They are a test series: not a stand-in for the live
series, and not a reason to discard them.

Four tables, one per resource:

| Family | What one row is | Rows (silver) | Silver status |
|---|---|---:|---|
| `dfs_test_events_service_requirement` | one requirement window of a test event | 40 | **held** (no publication time) |
| `dfs_test_events_service_update_industry` | one notification NESO posted to industry (anticipated, published or not issued) | 40 | eligible |
| `dfs_test_events_utilisation_report` | one bid outcome (Accepted / Rejected) of one DFS unit in one window, with the D-1 and D0 regional split | 739 | eligible |
| `dfs_test_events_utilisation_report_sum` | one window summary: required, procured, accepted cost, settled volume and cost (D-1, D0, settled) | 40 | eligible |

**What a model gets from it, and what it must not do.**

- **Live and Test 2022/23 are separate packages with no shared delivery date.** The sibling package
  @./demand-flexibility-service-live-events.md has equal headers but a disjoint set of delivery dates. **Never add
  or union the two series.** They are separate silver tables on purpose. Their notification dates overlap on one
  day only (a Test cancellation notice and a Live publication), and that overlap does not mean overlapping
  deliveries.
- **The 2023/24 package carries both event types in one table** (`Service Requirement Type` is Test or Live); see
  @./demand-flexibility-service.md. It is a later epoch of the service with a different header. Do not stack it onto
  this package without carrying the event type explicitly.
- **There is no event id.** A delivery date alone is not an event (back-to-back tests can run on one date). Join on
  **date + window** (and **unit** for bids), **within this package only**.
- **Windows are GMT labels, kept raw.** `window_from` / `window_to` are the vendor's HH:MM strings. The vendor
  documents delivery starts and ends and the notification schedule in GMT. The engine has no date-plus-clock-label
  recipe (RULINGS 572 / 588), so **no window start or end instant is computed** and no settlement-period column is
  invented. Every window measured is 30 minutes long and no delivery row falls on a clock-change day.
- **Requirements are held** (Holds): the requirement table is unpublished until NESO says when each requirement was
  first issued.
- **D0 is the event-day delivery forecast**, not an issue time. The report carries the D-1 submitted bid and the D0
  forecast side by side; the D0 columns are blank on many rows.
- **Summaries are published values.** They do not reconcile exactly to the bids (Known issues); they are kept as
  published and never recalculated.
- **Some test regional values are negative.** They are kept signed, never clamped.

The current-service successor is @./demand-flexibility.md (ad hoc, event ids, zonal report). It has a different
schema epoch and is not interchangeable with these tables.

- Publisher group: Demand Flexibility Service
- Registry group: dfs · archetype: EVT

## Files by disposition

All four resources are disposition **SILVER** (CSV uploads that gridflow parses). There are **no DOC, HOLD or SKIP
resources** in this package, hence no document download links. The package id is
`22bc9bdd-4919-439a-95b8-5213bb3bdf4c`.

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| DFS Service Requirement - TEST | CSV | upload | `000066dc-aa75-4bec-a5a2-9c935b1873d2` |
| DFS Utilisation Report - TEST | CSV | upload | `fc466b76-6823-4dd9-8b4a-aab464e0e77b` |
| Service Update Industry Notifications - TEST | CSV | upload | `a2dd7992-32d5-4723-b0f5-273caaecbde1` |
| Utilisation Report Summary - TEST | CSV | upload | `e4804faf-92be-43d0-a1ec-3e52a50f9666` |

**Where each resource is fetched from** (sidecar `request_url`; bronze under
`C:/gridflow-data/bronze/neso_data_portal/<family>/2026/10/08/`, one capture each, all on 2026-10-08).
`ckan_last_modified` is the vendor's CKAN value and is the vintage (see the clocks).

| Family | Fetch URL | Bytes | Rows | `ckan_last_modified` |
|---|---|---:|---:|---|
| `dfs_test_events_service_requirement` | `https://api.neso.energy/dataset/22bc9bdd-4919-439a-95b8-5213bb3bdf4c/resource/000066dc-aa75-4bec-a5a2-9c935b1873d2/download/dfs-service-requirement-test270320231430.csv` | 1,164 | 40 | 2023-03-27T13:29:56 |
| `dfs_test_events_service_update_industry` | `https://api.neso.energy/dataset/22bc9bdd-4919-439a-95b8-5213bb3bdf4c/resource/a2dd7992-32d5-4723-b0f5-273caaecbde1/download/service-update-industry-notifications-test270320231430.csv` | 8,730 | 40 | 2023-03-27T13:28:50 |
| `dfs_test_events_utilisation_report` | `https://api.neso.energy/dataset/22bc9bdd-4919-439a-95b8-5213bb3bdf4c/resource/fc466b76-6823-4dd9-8b4a-aab464e0e77b/download/dfs-participant-utilisation-report-test280320231300.csv` | 145,065 | 739 | 2026-07-27T13:58:49 |
| `dfs_test_events_utilisation_report_sum` | `https://api.neso.energy/dataset/22bc9bdd-4919-439a-95b8-5213bb3bdf4c/resource/e4804faf-92be-43d0-a1ec-3e52a50f9666/download/utilisation-report-summary-test280320231300-fs.csv` | 2,807 | 40 | 2026-07-27T13:46:55 |

Saved field info: `.planning/research/neso-snapshots/field-info/20261008T114228Z/dfs_test_events_*.json`.

## The two clocks, family by family

Every silver row carries a **vintage** clock and an **event** clock. The recipes are the same for all four
families; the event clock is keyed on each family's own date column.

| Clock | Value in this package |
|---|---|
| **Vintage** (when the data was available) | `published_at` = the CKAN `last_modified` of the captured file (ADR-030); `available_at` = `published_at`. No table has an issue column (`issue: none`), so gridflow cannot reconstruct an original publication instant. **The vintage is the vendor's last file modification, not the date of the original release.** |
| **Event time** (what the row is about) | Temporal recipe `date_sp1` on the family's date column: `timestamp_utc` / `event_time` is the **Europe/London midnight (first settlement period) of that date label**, so for a summer date it is 23:00Z of the previous UTC day. It is a **date anchor, not a window start**. The within-day position is the raw `window_from` / `time_label` string. |

| Family | Vintage clock (`ckan_last_modified`) | Event clock |
|---|---|---|
| `dfs_test_events_service_requirement` | 2023-03-27 (held) | `date_sp1(delivery_date)`: date-label anchor of the delivery date |
| `dfs_test_events_service_update_industry` | 2023-03-27 | `date_sp1(date)`: date-label anchor of the **posting** date; `time_label` is the GMT schedule label |
| `dfs_test_events_utilisation_report` | **2026-07-27** | `date_sp1(date)`: date-label anchor of the delivery date |
| `dfs_test_events_utilisation_report_sum` | **2026-07-27** | `date_sp1(date)`: date-label anchor of the delivery date |

Two consequences:

- The report and summary resources carry a **2026-07-27 modification stamp**, years after the March 2023 events they
  describe, and the package metadata was modified the same day. Their `available_at` is therefore 2026-07-27, not
  the date NESO first released them. Whether the content changed on that date or only its metadata is not
  established: `TODO: verify` the original release date of the report and summary files with NESO.
- The requirement and notification stamps (2023-03-27) fall **before** the last delivery dates of the package. That
  is why the requirement table is held (Holds): most of its windows start on or before the stamp, so the stamp
  cannot serve as a point-in-time bound for them.

## Units and sentinels

**Units come only from the vendor's own dictionary** (saved field info; K-DFS-FACTS g4). None is inferred from a
column name.

| Columns | Unit (vendor dictionary) |
|---|---|
| `dfs_required_mw` | **MW** (vendor dictionary unit cell) |
| `dfs_volume`, every regional column (`north_scotland` ... `south_wales`, `other`, `total`), every `d0_` regional column and `d0_total` | **MW** |
| `price` | **£/MWh** |
| `dfs_required`, `dfs_procured`, `d0_dfs_procured`, `settled_volume` | **MW** |
| `bids_accepted_total_cost`, `d0_bids_accepted_total_cost`, `settled_cost` | **£** |
| `window_from`, `window_to`, `time_label` | HH:MM clock labels in **GMT** (vendor text); no physical unit |
| `unit`, `dfs_provider`, `status`, `type` | identifiers and categories: no physical unit |

Nothing is converted or rescaled. No scoped DFS CSV publishes an MWh quantity column, and a half-hour MW value is
not turned into energy here.

**Typing and sentinels (K-DFS-FACTS g5 / g6).** Identifiers, categories and free text are `string`, byte-equal.
Dates are `date`. Measured values are `float64`. Every window and notification clock label is a raw `string`.
**Zeros are real values and stay zero; blanks stay null; negative values stay signed.** The production CSV reader
and a strict second parse agreed on every row and cell of all four bodies, and FACTS found no `-1`, `NA`, `N/A` or
literal-null token, no percent sign, no thousands separator and no padded number in any numeric column. **No token
is mapped to null and no sentinel rule, bound, clamp or trim is applied.** Padding in notification text (`status`,
`type`) is kept byte-equal, including inside the key column `type`, so two keys that differ only by trailing space
are distinct as published. The bodies carry a byte-order mark and two summary headers have trailing spaces; the
reader removes both before the header is matched to the frozen epoch.

## Families

The "Vendor unit" column is the unit stated in the vendor's dictionary; it is sparse because the dictionary gives a
unit for only some columns. All four families are `whole_capture` with one frozen resource each, so silver holds
exactly the rows of the one captured file. Silver also carries the standard clock columns `timestamp_utc`,
`event_time`, `published_at`, `available_at` and `capture_written_at`.

### `dfs_test_events_service_requirement`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

**Held.** 40 rows are in silver and none is released. This page therefore gives the **schema, row count, clocks and
hold question only, and states no data values** for this family. The vendor describes the file as the DFS service
requirements, with registered participants invited to submit bids no later than 15:30. See Holds.

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Delivery Date | `delivery_date` | date | `%Y-%m-%d` | no | — | — |
| From GMT | `window_from` | string | — | no | — | — |
| To GMT | `window_to` | string | — | yes | — | — |
| DFS Required MW | `dfs_required_mw` | float64 | — | yes | — | MW |

- Entity key: `delivery_date`, `window_from`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`delivery_date`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

### `dfs_test_events_service_update_industry`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

One row per notification NESO posted to industry. The vendor describes three notice kinds, each with a scheduled
GMT posting time: an anticipated-requirement notice (about 10:00, only when a requirement is anticipated), a
requirement-published notice (about 14:30) and a requirement-not-issued notice (about 14:30). `date` is the **posting
date**, which can precede the delivery date; a cancelled notice has no delivered event. `time_label` is the GMT
schedule label as published, a string; the date and time cannot be composed into an issue instant by the engine, so
the issue stays `none`. The 40 rows cover 20 posting dates from 2022-11-14 to 2023-03-27. The key is the structured
date, time and type, not `status`. `status` and `type` text is kept byte-equal: 11 `status` cells and 1 `type` cell
carry edge padding, and one `status` cell contains a comma.

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

### `dfs_test_events_utilisation_report`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

One row per DFS unit per half-hour window per bid outcome. The vendor describes the file as the accepted and rejected
bids for DFS with a regional breakdown, updated at around 16:30 GMT on days with a published requirement. Measured:
**739 rows, 613 Accepted and 126 Rejected, across 40 windows on 19 delivery dates (2022-11-15 to 2023-03-28)**.
Entity key (date, `window_from`, `unit`) is distinct on all 739 rows.

- **Two bid stages share each row.** The first block (`dfs_volume`, `price`, the 14 regions, `other`, `total`) is
  the **D-1 submitted bid**. The `d0_` block is the **event-day (D0) delivery forecast** for the same unit and
  window. D0 is a forecast stage, not an issue timestamp. D0 columns are blank on 126 rows each (`d0_other` 136,
  `d0_total` 128); blanks stay null and are not back-filled from D-1. The vendor's **summary** dictionary (`D0 DFS
  Procured`, `D0 Bids Accepted Total Cost`) says the unit's D-1 values are used where no D0 update was received; the
  report's own D0 regional columns carry no such wording, and gridflow applies no fallback in either table.
- **Zeros stay zero.** `dfs_volume` and `total` each have 18 zero cells.
- **Negative regional values.** `other` and `d0_other` each hold 4 negative values. They are not `-1` / `NA`
  sentinels, are kept as published, and must never be clamped. `TODO: verify` with NESO the meaning of a negative
  regional allocation (non-holding; NEGATIVE-REGIONAL-VALUES).
- **Regional columns are not a reliable decomposition.** The regional columns sum to `total` in 714 of 739 rows, and
  `total` equals `dfs_volume` in 727 (tolerance 0.000001 MW). Never rebuild the bid volume from the regions.
  `TODO: verify` REGIONAL-RECONCILIATION (non-holding).
- **`price` is in £/MWh** (vendor dictionary). What price a Rejected row carries (bid or clearing) is not
  established: `TODO: verify`.
- The regional column `north_wales_merseyside_cheshire` and its D0 counterpart `d0_north_wales_merseyside_and_cheshire`
  are spelled differently by the vendor; both spellings are the vendor's, and neither is normalised.

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

### `dfs_test_events_utilisation_report_sum`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

One row per half-hour window (40 rows over 19 delivery dates, the same windows as the report). The vendor describes
the file as a summary of the utilisation report, updated at around 16:30 GMT. Three stages sit on each row: the
**D-1** values (`dfs_required`, `dfs_procured`, `bids_accepted_total_cost`), the **D0** updated forecast
(`d0_dfs_procured`, `d0_bids_accepted_total_cost`) and the post-event **settled** outturn (`settled_volume`,
`settled_cost`). Quantities are MW and costs £. Entity key (date, `window_from`) is distinct on all 40 rows; it
replaces the draft key that used a settled volume.

**These are published values and they do not reconcile exactly to the bids.** Against the Accepted report rows of
the same window: D-1 quantity matches in all 40 windows, D-1 cost in 38 (two windows differ by a few pounds),
D0 quantity in 31 and D0 cost in 30 (blank D0 falling back to D-1). Settlement is separate post-event outturn and is
not derivable from bids. Values are kept as published and never recalculated.
`TODO: verify` SUMMARY-RECONCILIATION (non-holding): corrected source data or vendor explanation of precision,
revisions and D0 fallback.

**Never add the summary to the report.** `dfs_procured` is an aggregation of the Accepted report rows of the same
window, so adding the two double counts.

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

## Cadence

- Registry refresh: frozen
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Not Active

The series is closed: one capture per resource (2026-10-08) is the whole history. Because there is a single capture,
whether NESO ever amended a row in place is unmeasured; the report and summary resources do show a later metadata
stamp (2026-07-27, see the clocks). `TODO: verify` by comparing any future capture against the hash-pinned bodies.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence). Any output derived
from this package carries the attribution line "Supported by National Energy SO Open Data".

## Holds

- `dfs_test_events_service_requirement`: held: TODO: REQUIREMENT-ISSUE-AVAILABILITY — the 2022/23 DFS test-event service requirement upload (last_modified 2023-03-27) carries no issue column and publishes 40 delivery windows, 38 of them starting on or before its last_modified; when was each requirement first published, and does NESO retain earlier requirement editions? (unit v0.22-K-DFS-b)

**What the hold means.** The requirement table is written to silver and reconciled, but **no consumer-facing output
is released from it**: no gold view, chart, front-end page or model input. A requirement is knowable only from its
first publication, and this file has no issue column; its single vendor stamp falls after the start of 38 of its 40
windows, so it cannot tell a model what was known beforehand. The other three families are released (eligible),
with the vendor stamps above as their vintage.

**What would release it.** Immutable per-issue publications of the requirement, or a seat-approved retrospective
contract that accepts the file's stamp as availability for historical targets. Neither exists today.

**Open questions that do not hold any output** (carried as `TODO: verify`):

- NOTIFICATION-ISSUE-RETENTION: whether NESO retains the immutable publication history of the notifications; the
  split date and time fields cannot form an issue recipe, and the filename date token is not every row's issue.
- REGIONAL-RECONCILIATION and NEGATIVE-REGIONAL-VALUES (report), SUMMARY-RECONCILIATION (summary): above.
- ENDPOINT-CLOSURE: whether the window end instant belongs to the window. Literal ends are preserved.
- The original release date of the report and summary files (clocks above).
- Whether the vendor guarantees the composite identity of the exports (date, window, unit). The keys are measured to
  be distinct on this capture only.

## Known issues and gotchas

- **Do not union with the Live package.** Equal headers invite it. The Live and Test delivery-date sets do not
  intersect and they are separate operational series (@./demand-flexibility-service-live-events.md).
- **No event id.** Never join to another package. Within this package join the report and summary on
  (`date`, `window_from`), and add `unit` when joining bid rows.
- **`timestamp_utc` is a date anchor, not the window.** It is the London midnight of the date label. Use
  `window_from` for the within-day position, and do not build an instant from it.
- **Summary procurement is the Accepted report rows.** Filter the report on `status = 'Accepted'` before summing MW,
  and never add summary procurement to report procurement. A count of all report rows is bids, not accepted units.
- **D0 blanks are real blanks.** Do not coalesce them to zero or to the D-1 value.
- **Do not clamp or take absolute values** of negative regional cells or of any summary value.
- **`available_at` for the report and summary is 2026-07-27**, so a point-in-time filter (`available_at <= as_of`)
  keeps these two tables out for any `as_of` before that date, while the notifications appear from 2023-03-27.
- **Requirements are held**; no value is published from this page or from silver until the hold is answered.
- **No `run_type`, no revision column.** These are bid, award and outturn tables with no settlement run; never
  collapse them with settlement data on (date, period), and there is no settlement-period column to join on.

## Implementation delta

Where the code or a source differs from the docs or from another source:

- **Silver names** follow the DFS rule: vendor name lower-cased with runs of non-alphanumerics as one `_`, except
  `From GMT` / `From` to `window_from`, `To GMT` / `To` to `window_to`, and the notification `Time` to `time_label`
  (an SQL reserved word otherwise).
- **Two region spellings** (`north_wales_merseyside_cheshire` versus `d0_north_wales_merseyside_and_cheshire`) follow
  the vendor header exactly; silver does not unify them.
- **Draft proposals superseded.** The profile drafts keyed some families on a status or quantity; the frozen records
  key on date, window and unit (or posting date, time and type), as measured.
- **Vendor says GMT, files carry no zone.** Window and notification labels are documented as GMT; the records keep
  them as raw strings and compute nothing from them.
- **Download cap**: the registry sets `max_download_bytes` 536,870,912; the largest body here is 145,065 bytes.

## Activation receipt

DFS-b merged as PR #122 (`40e4a46`), triple-green (RULINGS 814). Activation on 2026-10-14 with window
`2026-10-08..2026-10-08` and no prior silver (RULINGS 816, `.planning/v0.22-RESULTS.md` section "DFS-b"): this
package wrote **40 + 40 + 739 + 40 = 859** rows, each equal to the spec plan, with 0 transform failures. Across
the three frozen DFS packages the transform wrote 2,360 rows. Reconcile `--all --cutoff 2026-10-13` exited 0 over
239 families with 0 gaps. The package holds 3 eligible families and 1 held-with-silver (eligibility report
`docs/neso_data_portal/eligibility.md`).

## Links

- Sibling Live package (separate series, never add): @./demand-flexibility-service-live-events.md
- 2023/24 frozen package (carries both event types): @./demand-flexibility-service.md
- Current-service successor package: @./demand-flexibility.md
- Vendor index: @../README.md, @../coverage.md
- Settlement-period context (no SP column here): @../../../20-domain/concepts/settlement-period.md
- Evidence in the gridflow repo: `.planning/phases/v0.22-K-DFS/K-DFS-FACTS.md` (package
  `demand-flexibility-service-test-events`, cross-package identity), `K-DFS-b-SPEC.md`, `.planning/RULINGS.md`
  (801, 803, 804, 814, 816), `.planning/v0.22-RESULTS.md` ("DFS-b")
