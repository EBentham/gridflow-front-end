---
source: "neso_data_portal"
package: "data-portal-planned-changes-known-issues"
dataset_key: "portal_known_issues"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
last_verified: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Data Portal changes and known issues
  summary: >-
    NESO's log of changes to its Data Portal: maintenance windows, column renames and known issues,
    one numbered item each, edited in place.
  facts:
    vendor: "NESO Data Portal: one CSV, the Planned Changes and Issues Log"
    cadence: "Ad hoc (NESO); gridflow checks daily"
    grain: "Each row: one numbered item, as it reads in one NESO file"
    history: "NESO created the package on 19 November 2020"
  landscape: market
  what_it_is: >-
    NESO's register of "upcoming changes to the NESO Data Portal along with any known issues". Items
    give a title, description, affected datasets and files, a status, a change window and a
    last-updated time. NESO edits items in place: items 239 and 240 are Planned in gridflow's capture
    of NESO's 8 October 2026 file, Deployed in NESO's 16 October file.
  how_used:
    - "See which NESO files will have column IDs renamed, and on what date"
    - "Explain a missing or failed capture by a maintenance window NESO logged"
    - "Compare gridflow's captures item by item; NESO does not say numbers are permanent"
  chart:
    type: bar
    silver: neso_data_portal/portal_known_issues
    filter:
      - {column: published_at, op: ge, value: "2026-10-16"}
      - {column: published_at, op: lt, value: "2026-10-17"}
    dedup: {"on": [po], order_by: published_at}
    group: status
    group_map:
      Deployed: deployed
      Cancelled: cancelled
      Planned: planned
      Postponed: postponed
      Deployed on the test link provided: test_link
    aggregation: count
    sort: value_desc
    unit: items
  chart_view:
    title: "Items by status, NESO's 16 October 2026 file"
    caption: >-
      Silver `portal_known_issues`, NESO's file last modified 16 October 2026: every item counted by
      its `status` as written in that file. NESO edits statuses in place and publishes only its
      current file, so gridflow's captures of other files may count differently.
    alt: >-
      Horizontal bar chart counting items by status in neso_data_portal/portal_known_issues, NESO's
      file last modified 16 October 2026, 246 items in all: Deployed 214, Cancelled 25, Planned 4,
      Postponed 2, and Deployed on the test link provided 1.
    key:
      - {series: deployed, label: Deployed, codes: Deployed, paint: petrol, note: "NESO's status for most items, issue items included, such as item 31"}
      - {series: cancelled, label: Cancelled, codes: Cancelled, paint: petrol}
      - {series: planned, label: Planned, codes: Planned, paint: petrol, note: "Items 189, 241, 255 and 256; item 189's start time is 9 January 2026"}
      - {series: postponed, label: Postponed, codes: Postponed, paint: petrol, note: "Items 14 and 48, with windows in April 2021 and January 2022"}
      - {series: test_link, label: Test link, codes: Deployed on the test link provided, paint: petrol, note: "Item 72, a prototype test from January 2022"}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then the log's one CSV, its file name dated (shown: 16
      October 2026). gridflow downloads it again when CKAN's `last_modified` changes.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=data-portal-planned-changes-known-issues"
      - "GET https://api.neso.energy/dataset/a10cb561-1be2-4567-880d-5bbac1ee9f4f/resource/23021dfa-a3b8-4f62-93bc-b60186c53fa4/download/23021dfa-a3b8-4f62-93bc-b60186c53fa4_16.10.2026.csv"
    commands:
      - {run: gridflow ingest neso_data_portal portal_known_issues --last 24h, comment: "the current file to bronze"}
      - {run: gridflow transform neso_data_portal portal_known_issues --last 24h, comment: "each new capture to silver"}
  record:
    select:
      filter:
        - {column: published_at, op: ge, value: "2026-10-16"}
        - {column: published_at, op: lt, value: "2026-10-17"}
        - {column: po, op: in, value: [239, 240, 241, 242, 243, 244, 255, 256]}
      dedup: {"on": [po], order_by: published_at}
      order_by: [po]
      columns: [po, status, change_issue_title, change_datetime_from, change_datetime_to, last_updated, notes,
                dataset_specific, file_specific, description, published_at, timestamp_utc]
    key: [po, published_at]
    caption: "The eight highest-numbered items in NESO's 16 October 2026 file; it skips 245 to 254."
    fields:
      po: "NESO's item number; unique in each file, permanence not stated by NESO"
      published_at: "CKAN's last-modified time of the file the row came from, read as UTC"
      status: "NESO's status as written in that file: Planned, Deployed, Cancelled and others"
      change_issue_title: "NESO's title for the item, free text"
      change_datetime_from: "When NESO says the change or issue starts, UTC per NESO's dictionary"
      change_datetime_to: "When NESO expects it to end or be fixed, UTC; often blank"
      last_updated: "When NESO last edited the item, UTC; it moves when NESO edits"
      notes: "NESO's note: item 241's moves it to 19 October; its description says 15 October"
      dataset_specific: "Datasets the item touches, as NESO writes them: titles, slugs, No or N/A"
      file_specific: "Files the item touches, as NESO names them; also No, Yes or N/A"
      description: "NESO's text of the change or issue; the frame cuts it at 1,000 characters"
      timestamp_utc: "When gridflow captured the file, UTC; the table has no event time"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `query()` filters on `timestamp_utc`, here the capture time, so these cells use `data.sql()` on
      the `_latest` view: NESO's newest captured file, whole (here, 16 October 2026). Times print in
      UK time.
    cells:
      - |
        items = data.sql("""
            SELECT po, status, change_issue_title, change_datetime_from,
                   change_datetime_to, last_updated, notes, published_at
            FROM silver_neso_data_portal_portal_known_issues_latest
            ORDER BY po
        """)
        items.status.value_counts()
      - |
        items[items.status.isin(["Planned", "Postponed"])][
            ["po", "status", "change_issue_title", "change_datetime_from", "notes"]]
      - |
        sorted(set(range(1, items.po.max() + 1)) - set(items.po))
      - |
        start = items.change_datetime_from.dt.tz_convert("UTC")
        start_year = start.dt.year.astype("Int64").rename("start_year")
        items.groupby(start_year).size().plot.bar(
            color="#155A6E", figsize=(8, 3.5),
            xlabel="year the change window starts, UTC", ylabel="items");
    needs: a capture of the Data Portal changes log
    plot_alt: >-
      Bar plot of the items in NESO's 16 October 2026 file by the year their change window starts,
      UTC: 5 in 2020, 36 in 2021, 26 in 2022, 33 in 2023, 44 in 2024, 38 in 2025 and 59 in 2026. Five
      items have no start and are not drawn.
  related:
    - {dataset: neso_data_portal/constraint-management-intertrip-service-information-cmis, note: "Items 239 and 243, both Deployed, renamed its arming files' column IDs"}
    - {dataset: neso_data_portal/aahedc-tariffs, note: "Item 241 (Planned) announces column ID renames, moved to 19 October"}
    - {dataset: neso_data_portal/transmission-network-use-of-system-tnuos-tariffs, note: "Item 256 (Planned) announces column ID renames in seven tariff files"}
    - {dataset: neso_data_portal/stability-midterm-y-1-utilisation-report, note: "Item 255 (Planned) announces two column ID renames in its 2025/26 report"}
---

# Data Portal: Planned Changes & Known Issues

NESO keeps this table as the change log of its own Open Data Portal. Each row is one
numbered item: a planned platform change (maintenance windows, datastore patches,
column-ID renames), a known issue NESO is working on, or a past change it has deployed.
The rows give the affected dataset and file, a status, a window, a last-updated time and
notes. The package description says it covers "details of upcoming changes to the NESO
Data Portal along with any known issues that we are working to resolve". It is not market
data and does not feed a model. For gridflow it is an **operations feed**. It is the
vendor's own notice of changes that can break or alter the other NESO packages gridflow
ingests. For example, item 239 renames column IDs in the CMIS arming file on
9 October 2026. Item 241 renames AAHEDC tariff column IDs on 15 October 2026. Item 240
lists 20 datasets affected by a 15–16 October 2026 infrastructure maintenance
window. gridflow keeps the whole register as captured, one snapshot per capture, in
silver (@../README.md).

**Status: eligible.** The one silver output is published with nothing held
(RULINGS 521, `docs/neso_data_portal/eligibility.md:90`). Activated 2026-10-08 with one
capture of 241 rows and capture reconciliation clean at cutoff 2026-10-08
(RULINGS 524–525, `.planning/v0.22-RESULTS.md` §CI).

- Publisher group: Data Portal changes and known issues
- Registry group: plans-reports-analysis · archetype: REG

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Planned Changes and Issues Log | CSV | upload | `23021dfa-a3b8-4f62-93bc-b60186c53fa4` |

The package has one resource and no DOC, GIS, COVERED or HOLD files.

Download link, as captured on 2026-10-08 (sidecar `request_url`):
https://api.neso.energy/dataset/a10cb561-1be2-4567-880d-5bbac1ee9f4f/resource/23021dfa-a3b8-4f62-93bc-b60186c53fa4/download/23021dfa-a3b8-4f62-93bc-b60186c53fa4_08.10.2026.csv

The file name in the URL carries the upload date. The 2026-10-06 catalogue snapshot
listed `…_05.10.2026.csv`; the capture fetched `…_08.10.2026.csv`. A saved URL therefore
goes stale. The stable handle is the resource id. gridflow resolves the URL through
`package_show` (`src/gridflow/connectors/neso_data_portal/client.py`).

## Families

### `portal_known_issues`

- Kind: tabular · archetype: REG · refresh: adhoc · empty allowed: yes

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| po | `po` | int64 | — | yes | — | — |
| Change_Issue_Title | `change_issue_title` | string | — | yes | — | — |
| Description | `description` | string | — | yes | — | — |
| Dataset_Specific | `dataset_specific` | string | — | yes | — | — |
| File_Specific | `file_specific` | string | — | yes | — | — |
| Status | `status` | string | — | yes | — | — |
| Change_DateTime_From | `change_datetime_from` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | IS0 8601 - UTC |
| Change_DateTime_To | `change_datetime_to` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | IS0 8601 - UTC |
| Last_Updated | `last_updated` | datetime | `%Y-%m-%dT%H:%M:%S` | yes | UTC | IS0 8601 - UTC |
| Notes | `notes` | string | — | yes | — | — |

- Entity key: `po`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Column meanings and units.** These come from the vendor field dictionary, read through
datastore field info (`FI(portal_known_issues)`, K-CI-FACTS §2.5). Every non-time column
has vendor unit `N/A`. The three datetimes have vendor unit `IS0 8601 - UTC`, which is
NESO's own spelling (a zero, not the letter O) and is copied verbatim.

| Column | Vendor title · description |
|---|---|
| `po` | Item · "Item Number". An identifier, not a quantity. |
| `change_issue_title` | Change Issue Title · "Title of the issue" |
| `description` | Description · "Description of the issue" (free text, often multi-line) |
| `dataset_specific` | Dataset Specific · "Is the issue related to a specific dataset" |
| `file_specific` | File Specific · "Is the issue related to a specific file" |
| `status` | Status · "The status of the issue" |
| `change_datetime_from` | Change Date Time From · "The date and time of when the issue will occur" |
| `change_datetime_to` | Change Date Time To · "The date and time of when the issue will be fixed" |
| `last_updated` | Last Updated · "The previous date and time this dataset was updated" |
| `notes` | Notes · "Any related notes for the item" |

**The two clocks.**

- **Vintage (`ckan_last_modified`).** `published_at` = `available_at` = the CKAN
  `last_modified` of the captured file. For the two captures held, that is
  2026-10-08T09:43:34.968862Z (fetched 2026-10-08T11:16:49Z) and 2026-10-16T13:34:40.735778Z
  (fetched 2026-10-16T20:43:02Z).
- **Event time (recipe `none`).** The record has no temporal column. `timestamp_utc`
  (and `event_time`, which copies it) is the **gridflow capture time**: the sidecar
  `written_at`, 2026-10-08T11:16:49.367455Z. It is not taken from any value in the file.
  The three vendor datetimes are descriptive columns. None of them is the row's event
  clock. None of them is non-null on every row (blanks: From 5, To 44, Last_Updated 18),
  and the recipe input must be non-null (K-CI-FACTS §2.5 T05).
- **No issue clock.** `last_updated` is a mutable "last edited" time. It is not an
  immutable publication instant, so the epoch's issue recipe is `none` (g2). Do not use it
  for point-in-time filtering. Use `available_at`.

**Key.** `po` is a **capture uniqueness guard**. The 2026-10-08 capture has 241 non-null, distinct,
integral item numbers, `1..241` (K-CI-FACTS C1/C3, remeasured on silver). NESO does not
say whether an item number can be reassigned or reused.
`TODO: verify` item-number permanence (K-CI-FACTS §2.5 T06, §3.4). That is why `_latest`
is `whole_capture` (it serves the newest complete capture) and not a per-`po` latest.

**Sentinels (g5).** Applied per column, never globally:

- The literal `N/A` is kept as text: `dataset_specific` 9 rows, `file_specific` 53 rows.
  It is not turned into null.
- `No` and `Yes` are vendor categorical answers and are kept as text (`file_specific`:
  No 77, Yes 4; `dataset_specific`: No 43).
- Empty cells become null: `change_datetime_from` 5, `change_datetime_to` 44,
  `last_updated` 18, `notes` 195, `dataset_specific` 1 (item 31).
- `TODO: verify` the vendor's distinction between `N/A`, `No` and a blank cell in
  `dataset_specific` and `file_specific` (K-CI-FACTS §2.5 g5).

**Status values in the 2026-10-08 capture** (241 rows): Deployed 209 · Cancelled 25 ·
Planned 4 · Postponed 2 · Deployed on the test link provided 1. The dictionary's example
value `Pending` does not appear in this capture.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Ad hoc

The file is replaced whenever NESO edits the log. Between the 2026-10-06 catalogue
snapshot (resource `last_modified` 2026-10-05T15:52:26) and the 2026-10-08 capture
(`last_modified` 2026-10-08T09:43:34), NESO uploaded at least one new file. Every capture
is the whole register, from item 1 to the newest. No date window selects rows.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence URL from the package metadata: https://www.neso.energy/data-portal/ngeso-open-licence
(CKAN `license_id` `ESO`).

## Holds

- none

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://api.neso.energy/api/3/action/` |
| Path             | `package_show?id=data-portal-planned-changes-known-issues`, then `resources[]` entry `23021dfa-a3b8-4f62-93bc-b60186c53fa4` (name "Planned Changes and Issues Log", format CSV, `url_type` upload), then GET of that resource's `url` |
| Method           | GET |
| Auth             | None. Keyless public API (@../README.md) |
| Rate limit       | NESO guidance, quoted in @../README.md: CKAN action API, at most one request per second; Datastore API, at most two requests per minute. Enforcement is an IP block |
| Pagination       | None. Single file download (179,505 bytes on 2026-10-08; registry download cap 512 MiB) |
| Historical depth | The package and resource were created 2020-11-19 (CKAN `metadata_created` / resource `created`). Item numbers start at 1. The earliest `change_datetime_from` is 2020-11-25T04:00Z. Only the current register is published, so earlier states cannot be fetched |
| Publication lag  | Not stated by NESO. Update frequency "Ad hoc" (package `extras`) |
| Response format  | JSON (CKAN metadata) → CSV (the data file, UTF-8 with BOM) |

The resource is also loaded in CKAN's Datastore (`datastore_active: true`). That is where
the field dictionary comes from (`datastore_search` with `limit=0` reported `total` 241 on
2026-10-08). gridflow captures the file, not Datastore rows.

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `id` | string | Yes | CKAN package slug (or package id `a10cb561-1be2-4567-880d-5bbac1ee9f4f`) | `data-portal-planned-changes-known-issues` |

### Working curl example

```bash
# Keyless — no auth header. Step 1: metadata; step 2: GET the resource "url" it returns.
curl -X GET \
  "https://api.neso.energy/api/3/action/package_show?id=data-portal-planned-changes-known-issues"
```

---

## Bronze layer

**Path pattern**: `C:/gridflow-data/bronze/neso_data_portal/portal_known_issues/<yyyy>/<mm>/<dd>/raw_<fetched_at>_<resource_id>_<sha256[:8]>.csv` plus a `.meta.json` sidecar
**Format**: Raw CSV, as received. Immutable. The sidecar records `request_url`,
`ckan_last_modified`, `url_type`, `body_sha256` and `written_at`.
**Granularity**: One file per capture, each holding the whole register.

Capture held: `raw_20261008T111649Z_23021dfa-a3b8-4f62-93bc-b60186c53fa4_d334918d.csv`,
179,505 bytes, 241 data rows, one header epoch (K-CI-FACTS §1).

### Bronze sample

Header and one data row, verbatim from the 2026-10-08 capture. The body starts with a
UTF-8 BOM (`EF BB BF`, not shown). Rows run newest first, so item 241 is the first data
line.

```csv
po,Change_Issue_Title,Description,Dataset_Specific,File_Specific,Status,Change_DateTime_From,Change_DateTime_To,Last_Updated,Notes
31,SOP dataset is being updated manually,We are currently experiencing technical issues so therefore we have created a new file Updated System Operating Plan - Data Table. Please use this until further notice. Our team is currently working to implement a fix as soon as possible.,,No,Deployed,2021-06-11T15:00:00,,2021-06-10T12:00:00,
```

No fixture exists under `tests/fixtures/neso_data_portal/` for this family. The capture
above is the evidence of the response's shape.

---

## Silver layer

**Path pattern**: `C:/gridflow-data/silver/neso_data_portal/portal_known_issues/year=<yyyy>/month=<mm>/portal_known_issues_<yyyymmdd>_run<written_at>_<hash>.parquet` (one file per capture)
**Transformer class**: `gridflow.silver.neso_data_portal.generic.Generic_PortalKnownIssues`, a class generated by `make_generic_transformer` from the frozen record (ADR-034)
**Pydantic schema**: none. Typing is driven by the record in `src/gridflow/connectors/neso_data_portal/registry/data-portal-planned-changes-known-issues.json`, epoch 1, record version `1`
**Dedup key**: `(po)` within a capture. Across captures, `_latest` is `whole_capture`
**Point-in-time field**: `available_at` (the CKAN `last_modified` of the capture)

DuckDB views: `silver_neso_data_portal_portal_known_issues` (all captures),
`silver_neso_data_portal_portal_known_issues_latest` (newest complete capture), and the
alias `silver_portal_known_issues`. Each returns 241 rows from 1 capture as of 2026-10-09.
`dataset_version` is `1+e1`.

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| `po` | `int` | Yes (0 null) | `po` | Item number. Capture uniqueness guard. Range `1..241` in the 2026-10-08 capture |
| `change_issue_title` | `str` | Yes (0 null) | `Change_Issue_Title` | |
| `description` | `str` | Yes (0 null) | `Description` | Free text, can span several lines |
| `dataset_specific` | `str` | Yes (1 null) | `Dataset_Specific` | Mixes `No`, `N/A`, a CKAN slug (e.g. `dynamic-containment-data`), a dataset title, or several titles separated by newlines |
| `file_specific` | `str` | Yes (0 null) | `File_Specific` | Mixes `No`, `Yes`, `N/A` and file names |
| `status` | `str` | Yes (0 null) | `Status` | Five values in this capture (see Families) |
| `change_datetime_from` | `datetime[UTC]` | Yes (5 null) | `Change_DateTime_From` | Start of the change or issue window. Observed range 2020-11-25T04:00Z – 2026-10-15T21:00Z |
| `change_datetime_to` | `datetime[UTC]` | Yes (44 null) | `Change_DateTime_To` | Expected end or fix. Observed range 2021-04-22T04:23Z – 2026-10-16T01:00Z |
| `last_updated` | `datetime[UTC]` | Yes (18 null) | `Last_Updated` | When the item was last edited. Mutable, not an issue clock. Observed range 2020-01-01T12:00Z – 2026-10-08T10:30Z |
| `notes` | `str` | Yes (195 null) | `Notes` | |
| `timestamp_utc` | `datetime[UTC]` | No | derived | Gridflow capture time (`capture_written_at`), recipe `none` |
| `published_at` | `datetime[UTC]` | No | derived | CKAN `last_modified` of the capture (ADR-030) |
| `bronze_capture_id` | `str` | No | derived | Bronze path of the capture |
| `capture_written_at` | `datetime[UTC]` | No | derived | Sidecar `written_at` |
| `event_time` | `datetime[UTC]` | No | derived | = `timestamp_utc` |
| `available_at` | `datetime[UTC]` | No | derived | = `published_at` |
| `source_run_id` | `str` | No | derived | Transform run id |
| `dataset_version` | `str` | No | derived | `<record version>+e<engine version>` = `1+e1` |

### Silver sample

Two rows from the 2026-10-08 capture. The long `description` of item 239 is cut at `…`.
The engine columns repeat across rows and are shown once.

```python
[
    {
        "po": 239,
        "change_issue_title": "Changes to Datasets",
        "description": "As part of our ongoing efforts to align with data management best practices and improve consistency across datasets, the Column IDs of the following data file belonging to Constraint Management Intertrip Service Information (CMIS) dataset will be updated on 9th October 2026. …",
        "dataset_specific": "Constraint Management Intertrip Service Information (CMIS)",
        "file_specific": "Constraint Management Intertrip Arming 2026-2027",
        "status": "Planned",
        "change_datetime_from": datetime(2026, 10, 9, 11, 0, tzinfo=UTC),
        "change_datetime_to": datetime(2026, 10, 9, 16, 0, tzinfo=UTC),
        "last_updated": datetime(2026, 10, 1, 14, 0, tzinfo=UTC),
        "notes": None,
        "timestamp_utc": datetime(2026, 10, 8, 11, 16, 49, 367455, tzinfo=UTC),
        "published_at": datetime(2026, 10, 8, 9, 43, 34, 968862, tzinfo=UTC),
        "bronze_capture_id": "bronze/neso_data_portal/portal_known_issues/2026/10/08/raw_20261008T111649Z_23021dfa-a3b8-4f62-93bc-b60186c53fa4_d334918d.csv",
        "capture_written_at": datetime(2026, 10, 8, 11, 16, 49, 367455, tzinfo=UTC),
        "event_time": datetime(2026, 10, 8, 11, 16, 49, 367455, tzinfo=UTC),
        "available_at": datetime(2026, 10, 8, 9, 43, 34, 968862, tzinfo=UTC),
        "source_run_id": "dd171889-3522-4d80-8494-0d44c6994b95",
        "dataset_version": "1+e1",
    },
    {
        "po": 2,
        "change_issue_title": "Dynamic Containment Masterdata - Delivery date format corrections",
        "description": "The \"Delivery Date\" field of the Dynamic Containment Masterdata file has multiple date formats (DD/MM/YYYY & DD-MMM-YY) in the source file which is preventing this field to be recognized as a date in the datastore API. We intend to rectify this so that all dates in this field have the format DD/MM/YYYY.",
        "dataset_specific": "dynamic-containment-data",
        "file_specific": "Dynamic Containment Masterdata",
        "status": "Deployed",
        "change_datetime_from": None,
        "change_datetime_to": None,
        "last_updated": datetime(2020, 11, 19, 14, 45, tzinfo=UTC),
        "notes": None,
        # engine columns as above
    },
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **Whole register per capture.** Every capture re-sends items 1..N. Rows are snapshots
  of the log, not events. To read the current state, use the `_latest` view (newest
  complete capture). Unioning captures repeats every item once per capture.
- **Rows are mutable between captures.** Status, windows, `last_updated` and notes can
  change while the item number stays the same. Item-number permanence is unconfirmed
  (`TODO: verify`, see Families). Diffing two captures on `po` assumes something the
  vendor has not stated.
- **Newest first.** The resource description notes the table "has now been sorted in
  descending order". Do not rely on file order. Sort on `po`.
- **UTF-8 BOM and multi-line cells.** The body starts with `EF BB BF`. The silver CSV
  reader strips it (`src/gridflow/silver/neso_data_portal/readers.py`). A naive
  `csv.DictReader` with `encoding="utf-8"` reads the first column as `\ufeffpo`.
  `description` cells contain quoted newlines.
- **Window inverted on item 37.** `change_datetime_to` (2021-08-02T06:30Z) is earlier than
  `change_datetime_from` (2021-08-26T06:00Z). It is the only such row. The item's own text
  describes maintenance on "the 26nd August between 6am - 6:30am". The `To` date looks
  like a data-entry slip. gridflow keeps the value as published.
- **`last_updated` after the file's `last_modified`.** On item 241, `last_updated`
  (2026-10-08T10:30Z) is 47 minutes later than the capture's CKAN `last_modified`
  (2026-10-08T09:43:34Z). It is the only such row. This supports treating `last_updated`
  as a hand-maintained field, not a publication clock. gridflow parses it as UTC, as the
  vendor dictionary documents.
- **`last_updated` earlier than the register on item 21.** Its `last_updated` is
  2020-01-01T12:00Z. That is before the resource's CKAN `created` (2020-11-19) and before
  the item's own window (`change_datetime_from` 2021-02-22T15:00Z). It is the only row
  dated before 2020-11-19. gridflow keeps the value as published.
- **Future windows.** Three `Planned` items (239, 240, 241) have `change_datetime_from`
  after the capture time. That is expected for a forward-looking register, not a clock
  error.
- **`dataset_specific` is not a key.** It mixes CKAN slugs, portal titles,
  newline-separated lists of titles, `No` and `N/A`. Item 240 lists 20 datasets
  in one cell. Joining it to gridflow package slugs needs a crosswalk that does not exist
  yet.
- **Datastore `_id`.** The Datastore field list has an `_id` column that is not in the
  CSV. gridflow does not carry it.
- **Download URL changes on every upload** (see Files by disposition).
- **Edited in place, numbers not contiguous (2026-10-16 capture).** NESO's file last
  modified 2026-10-16T13:34:40Z has 246 rows: items 1..244, 255 and 256; there are no items
  245..254. Against the 2026-10-08 file, items 1..238 are unchanged; 239 and 240 moved from
  `Planned` to `Deployed`; 241 moved to 19 October 2026 with the note "Has been rescheduled
  for 19/10/2026" while its `description` still says 15th October. Statuses in that file:
  Deployed 214, Cancelled 25, Planned 4, Postponed 2, Deployed on the test link provided 1.
- **Mojibake in NESO's text (item 256, 2026-10-16 capture).** The raw CSV reads
  `TDR Tariff in Â£/(Site Day)` (bytes `C3 82 C2 A3`): a pound sign double-encoded by NESO.
  gridflow keeps it byte for byte.

---

## Implementation delta

- **Ingest schedule**: the registry and vendor cadence are `adhoc` ("Update Frequency:
  Ad hoc"), but `config/sources.yaml:1025` registers `portal_known_issues` with
  `schedule: "daily"`. That is the poll cadence of the ingest config, not a vendor claim.
  Recorded, not assessed further.
- **Timestamp text**: the dictionary examples show a trailing `Z`
  (`2021-01-05T04:00:00Z`). Every populated raw value in the capture has no zone suffix
  (`YYYY-MM-DDTHH:MM:SS`: From 236, To 197, Last_Updated 223). The record parses them with
  `%Y-%m-%dT%H:%M:%S` and zone `UTC`, as the dictionary's unit documents.
- **Datastore type of `po`**: the Datastore declares `po` as `numeric`. The record types it
  `int64`. Every observed value is integral (K-CI-FACTS C3).

---

## Modelling notes

- Not a model input. No target or feature use is planned.
- **Operational use:** an early warning for the other NESO packages gridflow ingests.
  `Planned` items that rename column IDs (239: CMIS arming file, 9 October 2026; 241:
  AAHEDC tariffs, 15 October 2026) predict header-epoch changes that the generic engine
  will reject until a new record epoch is frozen. Maintenance windows (240) explain
  missing captures.
- Derived feature not yet built: a crosswalk from `dataset_specific` / `file_specific`
  free text to gridflow package slugs and family keys, so that open items can be flagged
  per family. `TODO`.
- Related: every other `neso_data_portal` package (@../README.md).

---

## Links

- [NESO package page](https://www.neso.energy/data-portal/data-portal-planned-changes-known-issues)
- [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence)
- Vendor README: @../README.md
- Connector: `src/gridflow/connectors/neso_data_portal/client.py`
- Registry record: `src/gridflow/connectors/neso_data_portal/registry/data-portal-planned-changes-known-issues.json`
- Silver transformer: `src/gridflow/silver/neso_data_portal/generic.py` (`make_generic_transformer`), typing in `src/gridflow/silver/neso_data_portal/casting.py`, CSV reader in `src/gridflow/silver/neso_data_portal/readers.py`
- Pydantic schema: none (record-driven)
- Gold view/builder: none
- Evidence: `.planning/phases/v0.22-K-CI/K-CI-FACTS.md` §2.5, §3.4; `.planning/v0.22-RESULTS.md` §CI; `docs/neso_data_portal/eligibility.md:90`
