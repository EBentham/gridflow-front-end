---
source: "neso_data_portal"
package: "interconnector-register"
dataset_key: "interconnector_register"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-24
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Interconnector register
  summary: >-
    NESO's list of interconnector projects with connection contracts: import and export capacity in
    MW, build status, connection site and contracted dates.
  facts:
    vendor: "NESO Data Portal, package `interconnector-register`: one CSV, replaced at each upload"
    cadence: "Twice weekly, on Tuesdays and Fridays (NESO); gridflow checks daily"
    grain: "Each row: one interconnector project, or one stage of a staged project"
  landscape: power
  what_it_is: >-
    NESO lists the interconnectors holding connection contracts with it, built and future. Each row
    gives import capacity (power NESO accepts into the transmission system at the link's site) and
    export capacity, in MW: currently connected, contracted change and total. NESO calls total import
    firm Transmission Entry Capacity (TEC). Moyle's stage rows read as cumulative: never add them.
  how_used:
    - Contracted interconnector import and export capacity by build status, from one dated file
    - "When contracted links or changes are due, from `mw_effective_from`: contract dates, not history"
    - "What changed between NESO's files, by `project_number` and `published_at`"
  chart:
    type: bar
    silver: neso_data_portal/interconnector_register
    filter:
      - {column: published_at, op: ge, value: "2026-10-16"}
      - {column: published_at, op: lt, value: "2026-10-17"}
      - {column: project_number, op: ne, value: PRO-001292-1}
    dedup: {on: [project_number], order_by: published_at}
    group: project_status
    group_map:
      Scoping: Scoping
      Built: Built
      Awaiting Consents: Awaiting Consents
      Under Construction/Commissioning: Construction
    value: mw_import_total
    aggregation: sum
    sort: value_desc
    unit: MW
  chart_view:
    title: "Import capacity by status, NESO's 16 October 2026 file"
    caption: >-
      Silver `interconnector_register`, NESO's 16 October 2026 file: `mw_import_total`, MW, summed by
      project status, one row per project number. Moyle counts once, by its stage 2 row: its 500 MW
      matches Moyle's TEC in NESO's package description (captured 6 October 2026).
    alt: >-
      Horizontal bar chart from neso_data_portal/interconnector_register, NESO's file of 16 October
      2026: contracted import capacity in MW summed by project status, largest first. Scoping 26,830
      MW, Built 10,791 MW (Moyle counted once, at 500 MW), Awaiting Consents 4,000 MW and
      Construction (NESO's Under Construction/Commissioning) 1,400 MW.
    key:
      - {series: mw_import_total, label: Import capacity, paint: olive, note: "Construction is NESO's Under Construction/Commissioning. Import is NESO's firm TEC; export totals by status run higher"}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then the register's one CSV, its file name dated (shown:
      16 October 2026). gridflow downloads it again when CKAN's `last_modified` changes.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=interconnector-register"
      - "GET https://api.neso.energy/dataset/a7cca714-9dbb-42b1-99c8-4bc7211605a8/resource/64f7908f-f787-4977-93e1-5342a5f1357f/download/interconnector-register-16-october-2026.csv"
    commands:
      - {run: gridflow ingest neso_data_portal interconnector_register --last 24h, comment: "the current file to bronze"}
      - {run: gridflow transform neso_data_portal interconnector_register --last 24h, comment: "each new capture to silver"}
  record:
    select:
      filter:
        - {column: published_at, op: ge, value: "2026-10-16"}
        - {column: published_at, op: lt, value: "2026-10-17"}
        - {column: project_number, op: in, value: [PRO-000280, PRO-000282, PRO-000285, PRO-001288,
                                                     PRO-001292-1, PRO-001292-2, PRO-001454, PRO-003462]}
      dedup: {on: [project_number], order_by: published_at}
      order_by: [project_number]
      columns: [project_number, project_name, stage, mw_import_current, mw_import_increase_decrease,
                mw_import_total, mw_effective_from, project_status, gate, mw_export_current,
                mw_export_increase_decrease, mw_export_total, host_to, connection_site, customer_name,
                published_at]
    key: [project_number, published_at]
    caption: "Eight projects from NESO's 16 October 2026 file, with both overlapping Moyle stage rows."
    fields:
      project_number: "NESO's unique project id; a staged project adds a dash and the stage number"
      published_at: "CKAN's last-modified time of the file the row came from, read as UTC"
      project_name: "Project name as NESO writes it; Moyle's rows read Auchencrosh (interconnector CCT)"
      stage: "Stage of a staged contract; blank when the project is not staged (NESO)"
      mw_import_current: "Import capacity currently connected, MW; NESO states 0 until the project is built"
      mw_import_increase_decrease: "Import capacity contracted to connect or be removed at a future date, MW"
      mw_import_total: "NESO: import contracted across all stages, firm TEC, MW; Moyle rows read 475, 500"
      mw_export_current: "Export capacity currently connected, MW; 0 until the project is built (NESO)"
      mw_export_increase_decrease: "Export capacity contracted to connect or be removed at a future date, MW"
      mw_export_total: "NESO: export contracted across all stages, MW; Moyle rows read 500, 500"
      mw_effective_from: "Contracted effective date, future only per NESO; Moyle's 16 October rows show 2022"
      project_status: "Build stage as far as NESO is aware: Scoping, Awaiting Consents, Built and others"
      gate: "Gate 1 or Gate 2 of the contract; blank until countersigned (NESO)"
      host_to: "Transmission owner responsible for the connection, as NESO's code (`NGET`, `SHET`, `SPT`)"
      connection_site: "Substation where the link connects to the transmission system, as NESO writes it"
      customer_name: "The contract holder's company name, as NESO writes it"
      timestamp_utc: "When gridflow wrote the capture, UTC; not a contract or effective date"
      bronze_capture_id: "Path of the bronze capture the row was read from"
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      Reads with `data.sql` from the `_latest` view, NESO's newest captured file: `query()` filters on
      capture time. Moyle's stage 1 row is dropped before adding, and times print in UK time.
    cells:
      - |
        df = data.sql("""
            SELECT project_number, project_name, stage, project_status,
                   mw_import_current, mw_import_increase_decrease,
                   mw_import_total, mw_export_total, mw_effective_from,
                   gate, published_at
            FROM silver_neso_data_portal_interconnector_register_latest
            ORDER BY project_number""")
        df[df.project_name.duplicated(keep=False)]
      - |
        one = df[df.project_number != "PRO-001292-1"]
        one.groupby("project_status").agg(
            projects=("project_number", "count"),
            import_mw=("mw_import_total", "sum"),
            export_mw=("mw_export_total", "sum")).reset_index()
      - |
        due = one[one.project_status != "Built"]
        year = due.mw_effective_from.dt.year
        span = range(year.min(), year.max() + 1)
        by_year = (due.groupby(year).mw_import_total.sum()
                      .reindex(span, fill_value=0))
        by_year.plot.bar(color="#6B7A3A", figsize=(8, 3.5),
                         xlabel="contracted effective year",
                         ylabel="import capacity, MW");
    needs: a capture of the interconnector register
    plot_alt: >-
      Bar plot of contracted import capacity, MW, of projects not yet built, by the year NESO's file
      dates it: 1,400 in 2027, 750 in 2028, 4,400 in 2029, 6,600 in 2030 (the most), 1,900 in 2031,
      6,380 in 2032, 1,800 in 2033, none in 2034, 3,600 in 2035, 1,000 in 2036 and 4,400 in 2037.
  related:
    - {dataset: neso_data_portal/transmission-entry-capacity-tec-register, note: "NESO's sister register of Transmission Entry Capacity contracts for generation projects"}
    - {dataset: neso_data_portal/embedded-register, note: "NESO's sister register for embedded generation projects in Scotland"}
    - {dataset: neso_data_portal/ifa, note: "NESO's hourly transfer limits on IFA, built here at 1,988 MW"}
    - {dataset: neso_data_portal/brit-ned, note: "NESO's hourly transfer limits on BritNed, listed here as Britned"}
---

# Interconnector Register

The Interconnector Register is NESO's list of interconnector projects that hold connection
contracts with it. The package description says it covers "active interconnectors and future
interconnector projects". Each row is one project, or one stage of a staged project. It gives
the capacity the project holds today, the change contracted for a future date, and the total
contracted across stages. Capacity is given separately for **import** and **export**, in MW
(vendor dictionary). The register also gives the project's build status, the host
transmission owner (TO), a gate classification and a project identifier.

The package note says the "MW Total MW Import figures represent firm Transmission Entry
Capacity (TEC)". It names Moyle as a special case: Moyle "holds a total of 500MW TEC which is
subject to operational restrictions". Import and export follow the CUSC definitions the
package quotes (paragraphs 9.4 and 9.5): import is power NESO accepts into the transmission
system at the interconnector's connection site, export is power transported to that site.

Use it as a contracted-capacity reference for GB interconnection: which links are built and
at what MW, and which are contracted for the future with a target effective date. Do **not**
read it as a flow or availability series. It holds contracted capacity, not metered flows
(see @./historic-demand-data.md) and not the day-by-day trading limits NESO submits for
BritNed (see @./brit-ned.md). Its sister registers are @./transmission-entry-capacity-tec-register.md
and @./embedded-register.md.

The data comes from a CKAN upload-file package on the NESO Open Data Portal (@../README.md).
**Status: eligible.** The single silver output is not held (eligibility report
`docs/neso_data_portal/eligibility.md`; no hold question). Activation was RULINGS 504
(v0.22 E, 2026-10-08), the docs-wave closure for this page RULINGS 879. No later ruling (591
and 596 concern the demand-forecast pairing, 494 and 499 the bootstrap and capture sweep for
other families) binds this family.

Supported by National Energy SO Open Data

- Publisher group: Connection registers
- Registry group: connection-registers · archetype: REG

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Interconnector Register | CSV | upload | `64f7908f-f787-4977-93e1-5342a5f1357f` |

There are no DOC, CATALOGUE-ONLY or excluded resources in this package. The package has
exactly one resource (`num_resources: 1`, CKAN package id
`a7cca714-9dbb-42b1-99c8-4bc7211605a8`, catalogue snapshot `20261006T195819Z`). The resource
is also loaded into the CKAN Datastore (`datastore_active: true`); its field dictionary is the
source of the units below. gridflow downloads the uploaded CSV and does not read the Datastore.

### Resource download links

The URL is the `request_url` in the capture's bronze sidecar (capture 2026-10-08):

| Resource | Disposition | Download |
|---|---|---|
| Interconnector Register (CSV) | SILVER → `interconnector_register` | [interconnector-register-05-october-2026.csv](https://api.neso.energy/dataset/a7cca714-9dbb-42b1-99c8-4bc7211605a8/resource/64f7908f-f787-4977-93e1-5342a5f1357f/download/interconnector-register-05-october-2026.csv) |

The filename carries a date (here "05 October 2026") and changes with each upload, so the
download URL is not stable. The stable handle is the resource id. The resource description
says the file "contains the latest version of the Interconnector Register including all
changes up to publication".

## Families

### `interconnector_register`

- Kind: tabular · archetype: REG · refresh: daily · empty allowed: yes

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Project Name | `project_name` | string | — | yes | — | — |
| Customer Name | `customer_name` | string | — | yes | — | — |
| Connection Site | `connection_site` | string | — | yes | — | — |
| Stage | `stage` | float64 | — | yes | — | — |
| MW Import - Current | `mw_import_current` | float64 | — | yes | — | MW |
| MW Export - Current | `mw_export_current` | float64 | — | yes | — | MW |
| MW Import - Increase / Decrease | `mw_import_increase_decrease` | float64 | — | yes | — | MW |
| MW Export - Increase / Decrease | `mw_export_increase_decrease` | float64 | — | yes | — | MW |
| MW Import - Total | `mw_import_total` | float64 | — | yes | — | MW |
| MW Export - Total | `mw_export_total` | float64 | — | yes | — | MW |
| MW Effective From | `mw_effective_from` | date | `%Y-%m-%d` | yes | — | yyyy-mm-dd |
| Project Status | `project_status` | string | — | yes | — | — |
| HOST TO | `host_to` | string | — | yes | — | — |
| Project Number | `project_number` | string | — | no | — | — |
| Gate | `gate` | float64 | — | yes | — | — |

- Entity key: `project_number`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

### The two clocks

- **Vintage clock: `ckan_last_modified`.** `published_at` and `available_at` both equal the
  CKAN `last_modified` of the resource at capture. For the first capture that is
  `2026-10-06T10:47:52.001303` (for the second, `2026-10-16T18:06:23.602416`), which gridflow reads as UTC (CKAN gives it without an offset;
  ADR-030 D-15, corroborated rather than vendor-documented). The resource is
  `url_type=upload`, so this is the file's upload time, not a release time for any one row.
  The vendor says the file is updated "twice weekly on Tuesdays and Fridays" (resource
  description; package extra "Update Frequency: Twice weekly"). 2026-10-06 was a Tuesday,
  which agrees. gridflow checks daily and downloads the file again only when CKAN's
  `last_modified` differs from the newest capture's (gridflow `connectors/neso_data_portal/client.py`,
  `iter_members`, upload-member skip); it does not compare bodies for an upload resource.
- **Event clock: none.** The temporal recipe is `none`. `timestamp_utc` (and `event_time`,
  copied from it) is the **capture time**, the bronze write instant, the same on every row
  (`2026-10-08T11:12:01.239214Z` for the first capture, `2026-10-16T20:40:23.132896Z` for
  the second). It is not a date of any contracted
  change. The register has no per-row event instant; the closest business date is
  `mw_effective_from`, which is a calendar date and not a clock (see below).
- **Point-in-time use.** Filter on `available_at`, never on `mw_effective_from`, to decide
  what was known when. A row enters silver only with the capture whose file contains it.
  `_latest` is `whole_capture`: the newest capture is the whole current register, and a
  project dropped from a later file is not carried forward.

## Column meanings and units

Units come only from the vendor field dictionary (Datastore field info, snapshot
`field-info/20261008T114228Z/interconnector_register.json`, "unit" entry). They are not
inferred from the column names.

| Column | Meaning (vendor dictionary) | Unit |
|---|---|---|
| `project_name` | "Name of Generation Project" | none given |
| `customer_name` | "Name of Generator" | none given |
| `connection_site` | "Name of Generation Connection Site" | none given |
| `stage` | "Staged TEC": how much TEC the customer will connect and when. Filled only when the project is staged, otherwise empty. | none given |
| `mw_import_current` / `mw_export_current` | Import / export capacity currently connected to the National Grid. Vendor comment: "Field will state 0MW until the project is built and connected". | MW |
| `mw_import_increase_decrease` / `mw_export_increase_decrease` | Import / export capacity contracted to connect or be removed at a future date. Vendor comment: "0MW unless the TEC is due to increase or decrease". | MW |
| `mw_import_total` / `mw_export_total` | Total import / export capacity contracted across all stages. | MW |
| `mw_effective_from` | Date on which the connection is contracted to be effective from. Only filled for future connections or increases/decreases to TEC, otherwise empty. | `yyyy-mm-dd` (a date format, not a physical unit) |
| `project_status` | The project's stage in its build cycle ("Indicates what stage the Project is at in it's build cycle", vendor spelling). | none given |
| `host_to` | Which TO is responsible for the connection. Vendor comment lists "NGET, SHET, SPT or OFTO". | none given |
| `project_number` | Unique project identifier. If a project has more than one stage the number is followed by a dash and the stage number. | none given |
| `gate` | Which Gate the project is contracted at. Filled only once a signed Gate 1 or Gate 2 contract is countersigned. | none given |

Notes on these meanings:

- **Dictionary template text.** The `project_name`, `customer_name` and `connection_site`
  descriptions say "Generation Project", "Generator" and "Generation Connection Site". The
  same wording is used across NESO's connection registers (compare @./transmission-entry-capacity-tec-register.md);
  here the rows are interconnectors. The dictionary strings also carry trailing tabs and
  carriage returns, and a few characters that did not decode (for example in the `stage`
  and `project_status` text). gridflow does not use these strings at run time.
- **MW sign and rescaling.** Values are not rescaled. MW is the vendor unit for all six
  capacity columns. The measured values are all non-negative, but the dictionary does not say
  whether a negative `increase_decrease` ("removed at a future date") could appear.
  TODO: verify how a contracted reduction is encoded (negative increase/decrease, or only a
  lower total). No negative value appears in either capture.
- **Arithmetic.** In both captures, `current + increase_decrease = total` holds exactly in
  all 35 rows, for import and for export. The dictionary does not state this identity.
- **Status vocabulary.** The vendor's `project_status` comment defines Scoping, Awaiting
  Consents and Consents Approved, and says the classifications are produced "as far as we
  are aware" and that NESO holds no authority over them. The capture also contains "Built"
  and "Under Construction/Commissioning" and does not contain "Consents Approved". TODO: verify
  the full status vocabulary; only the four observed values are established.
- **Gate.** The package note says the Gate column was added from 21 November 2025 and stays
  blank until agreements are countersigned. The dictionary type is a number, example 1.
  Observed values are 1, 2 or blank; 2 first appears in the 16 October 2026 file
  (NeuConnect, `PRO-001288`).
- **`mw_effective_from` is a date, not an instant.** The dictionary gives only `yyyy-mm-dd`,
  with no time of day or zone. gridflow keeps it as a Date. TODO: verify the exact effective
  instant and zone; no timestamp conversion is made (RESEARCH E, pilot time columns).
- **Duplicate-looking rows.** The package note warns that capacity "across stages and
  technology types is currently presented in aggregate, which may result in duplicate
  entries". Staged projects carry the stage in the project number
  (`PRO-001292-1`, `PRO-001292-2`). `project_number` is unique in each capture
  (35 values in 35 rows), but `project_name` is not (the staged project appears twice).
  Treat `project_number` as the row key and do not sum `*_total` columns across the stages
  of one project.

### Missing values and sentinels

- **Blank, not a sentinel.** Missing values are empty CSV fields and become null in silver.
  The register has no `NA`, `N/A` or other placeholder text in either capture, and no
  numeric sentinel such as -999.
- **Zero is a real value.** The vendor states the "current" columns hold `0MW` until a
  project is built and the "increase / decrease" columns hold `0MW` unless a change is due.
  Zeros are kept as 0.0 and are not turned into null.
- **Structural blanks.** `stage` is blank unless the project is staged, `gate` is blank until
  countersigned, and `mw_effective_from` is blank when no future change is contracted. A
  blank in these columns is not an error. Observed: `stage` is blank in 33 of 35 rows and
  `mw_effective_from` in 10, in both captures; `gate` in 29 (5 October file) and 25 (16 October file).
- **Required key.** `project_number` is the only non-nullable column and is present in every
  row.

## Silver as of 2026-10-16

First capture only (the 5 October 2026 file). Where the 16 October 2026 file differs, see
"Second capture (checked 2026-10-24)" below.

Query time 2026-10-16, over `C:/gridflow-data/silver/neso_data_portal/interconnector_register/`.
A daily refresh runs concurrently, so a later query may show more captures.

- **One bronze capture and one silver file (first capture; there are now two).** Bronze:
  `raw_20261008T111201Z_64f7908f-f787-4977-93e1-5342a5f1357f_149feca5.csv` (5,536 bytes,
  sha256 prefix `149feca5`, written 2026-10-08T11:12:01Z, UTF-8 with a byte-order mark).
  Silver: `year=2026/month=10/interconnector_register_20261008_run2026-10-08T11-12-01…parquet`.
- **35 rows, 23 columns** (the 15 vendor columns plus the engine columns `timestamp_utc`,
  `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`,
  `source_run_id`, `dataset_version`). The activation count in the v0.22 RESULTS "E"
  section is also 35 rows (reconcile `--cutoff 2026-10-08`: exit 0, 0 gaps).
- **Single clock values.** `published_at` = `available_at` = `2026-10-06T10:47:52.001303Z`
  on every row; `timestamp_utc` = `2026-10-08T11:12:01.239214Z` on every row.
- **Project status.** Scoping 19, Built 12, Awaiting Consents 3, Under
  Construction/Commissioning 1.
- **Host TO.** NGET 30, SPT 3, SHET 2.
- **Built links and the staged-row trap.** The 12 "Built" rows include both stage rows of
  the staged Moyle project (`PRO-001292-1` and `-2`, customer Moyle Interconnector Limited
  in bronze). Their "current" import values are 270 and 475 MW while the project total is
  500 MW, so the two stage rows overlap and must not be summed. A plain sum of
  `mw_import_current` over "Built" rows would double count Moyle. TODO: verify whether the
  "current" values of a stage row are cumulative to that stage or additive. The numbers
  read as cumulative (checked 2026-10-24, both captures): stage 1's import total (475 MW)
  equals stage 2's import current, and stage 2's import total (500 MW) equals the 500 MW
  TEC the package note gives Moyle. Export is 500 MW current and total on both rows. NESO
  does not state the rule.
- **Future links.** 23 of the 35 rows have `mw_import_current` = 0 and 23 have
  `mw_export_current` = 0. They are the not-yet-connected projects: Scoping 19, Awaiting
  Consents 3 and Under Construction/Commissioning 1.
- **Effective dates.** 25 rows carry `mw_effective_from`, ranging 2022-04-01 to 2037-10-31.
  Three of them lie before the capture date: the two Moyle stages (2022-04-01, 2022-08-01,
  status Built) and the Under Construction/Commissioning project (2026-08-01, still showing
  0 MW current; first capture only, as the 16 October file moves it to 2027-07-07). So an
  effective date earlier than the capture does not by itself mean the
  capacity is already connected. TODO: verify how and when NESO moves capacity from
  "increase / decrease" into "current".
- **Gate.** Gate = 1 on 6 rows, all of them future projects with status Scoping (first
  capture; the 16 October file has Gate 1 on 9 rows and Gate 2 on 1).

### Second capture (checked 2026-10-24)

- **Two captures, 70 silver rows.** A second bronze capture,
  `raw_20261016T204023Z_64f7908f-f787-4977-93e1-5342a5f1357f_d191824c.csv` (5,540 bytes,
  written 2026-10-16T20:40:23Z), holds the file `interconnector-register-16-october-2026.csv`
  (CKAN `last_modified` `2026-10-16T18:06:23.602416`). Silver now has 35 rows per capture,
  70 in all: the same 35 project numbers appear in both, so every key repeats across
  captures. Charts and frames over this table must pick one capture or de-duplicate on
  `project_number`.
- **What changed.** Five rows differ between the files: `gate` is newly filled on four
  (1 on SENECA, GB-EU MPI and The Superconnection; 2 on NeuConnect, the first Gate 2 row),
  and three `mw_effective_from` dates moved (NeuConnect 2026-08-01 to 2027-07-07, Teeside
  MPI 2033-10-31 to 2035-10-30, The Superconnection 2027-09-01 to 2032-10-28). No MW value,
  status or host TO changed. The 16 October file has Gate 1 on 9 rows and Gate 2 on 1.
- **Past effective dates.** In the 16 October file only the two Moyle stage rows carry an
  effective date before the capture; NeuConnect's moved into 2027.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Twice weekly
- Resource description: "This file will be updated twice weekly on Tuesdays and Fridays."
- Organisation text: "Data showing the latest contracted position, published twice weekly."
- Captures are append-only in bronze; the file is not downloaded again while CKAN's
  `last_modified` matches the newest capture's.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

## Holds

- none

Eligibility is "eligible" in `docs/neso_data_portal/eligibility.md`, with no hold question.
The only open points are the `TODO: verify …` items above (effective instant, contracted
reduction encoding, status vocabulary, stage semantics, when "increase / decrease" becomes
"current"). None of them blocks publication, because gridflow converts none of these
fields into a timestamp or a derived quantity.
