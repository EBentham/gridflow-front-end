---
source: "neso_data_portal"
package: "voltage-requirement"
dataset_key: "voltage_requirement"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-23
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  held: NESO leaves unstated what each range covers (some run backwards), each group's area and issue times.
  title: Voltage requirement
  summary: >-
    How many voltage machines NESO expects to need overnight in each voltage group, in its
    week-ahead plan.
  facts:
    vendor: "NESO Data Portal, package `voltage-requirement`: one CSV file, three PDFs"
    cadence: "Weekly, as NESO lists it; the file holds earlier plans as well"
    grain: "Each row: one voltage group and date range, with a count and update time"
  landscape: market
  what_it_is: >-
    For each voltage group, the number of voltage machines NESO expects to need overnight. NESO
    describes the plans as covering the next weekend and the following Monday to Friday, and says
    the actual requirement is likely to change. Groups carry codes such as `V_Mersey`; a NESO map
    shows the zones, without a code list.
  how_used:
    - Expected voltage support needs, region by region, for the week ahead
    - Regional voltage needs beside what NESO spends on voltage constraints
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then each file whole unless its `last_modified` is
      unchanged. Three PDFs stay in bronze; the deep dive is not listed.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=voltage-requirement"
      - "GET https://api.neso.energy/dataset/9f4acccb-bf79-452b-aa77-a680ae728722/resource/00881643-7a5e-4eed-b144-06423a88202b/download/overnightvoltagerequirement20-26_1.csv"
      - "GET https://api.neso.energy/dataset/9f4acccb-bf79-452b-aa77-a680ae728722/resource/1cf7b77b-3750-49e5-8d57-6b25ccbc1007/download/ew-voltage-zones.pdf"
      - "GET https://api.neso.energy/dataset/9f4acccb-bf79-452b-aa77-a680ae728722/resource/c28b35c9-34da-49a7-bb7e-90d88799c4a4/download/intro-to-voltage-management.pdf"
    commands:
      - {run: gridflow ingest neso_data_portal voltage_requirement --last 24h, comment: whole file to bronze}
      - {run: gridflow transform neso_data_portal voltage_requirement --last 24h, comment: "the capture's date to silver"}
      - {run: gridflow ingest neso_data_portal voltage_requirement_files --last 24h, comment: the three PDFs}
  related:
    - {dataset: neso_data_portal/outturn-voltage-costs, note: "What NESO spent keeping voltage within limits, by voltage group"}
    - {dataset: neso_data_portal/obligatory-reactive-power-service-orps-utilisation, note: "Reactive power each unit was asked to absorb or produce, monthly"}
    - {dataset: neso_data_portal/constraint-breakdown, note: "NESO's daily constraint costs, with voltage among the reasons"}
    - {dataset: neso_data_portal/24-months-ahead-constraint-cost-forecast, note: "NESO's monthly constraint cost forecast, which covers voltage requirements"}
---

# Week Ahead Overnight Voltage Requirement

NESO publishes, for each regional voltage group, the number of voltage machines (voltage-providing units) it expects to need for the upcoming weekend and the following Monday to Friday overnight periods. The vendor states that the figure is a plan, not a commitment: because voltage need is local and complex, the actual requirement is likely to change, and NESO optimises further towards real time as market conditions, unit running patterns and supply and demand shift. The page therefore answers "how many voltage providers did NESO expect to need per group, for which nights, as last revised when?" It is a forward-looking operating-plan signal for constraint management, not an outturn measurement.

gridflow captures the single CSV as a whole-file snapshot and writes one silver family, `voltage_requirement`. Three PDFs (an introduction to voltage management, a Voltage Deep Dive slide deck from the Operational Transparency Forum, and the group map) are retained as documents only.

**The silver output is held (unit E-SEM).** Rows exist (5,221 after the 2026-10-08 activation; the 2026-10-16 capture has 5,257) and the schema is fixed, but the output is not published as an eligible forecast until the hold question below is answered. No data values for this family appear on this page.

Attribution: Supported by National Energy SO Open Data

- Publisher group: Constraint management
- Registry group: constraint-management · archetype: FC
- Licence: NESO Open Data Licence
- Vendor package page: <https://www.neso.energy/data-portal/voltage-requirement>
- Vendor column dictionary: <https://www.neso.energy/data-portal/voltage-requirement/week_ahead_overnight_voltage_requirement_20-26>

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Week Ahead Overnight Voltage Requirement 20-26 | CSV | upload | `00881643-7a5e-4eed-b144-06423a88202b` |

One CSV, UTF-8, header row `Start Date, End Date, Group, Units, Notes, Last Updated`. CKAN `last_modified` of the first captured resource is 2026-10-02T13:22:22.101474; the activation capture is 288,655 bytes and 5,221 data rows. The second capture (fetched 2026-10-16T20:48:07 UTC, bronze `raw_20261016T204807Z_00881643-7a5e-4eed-b144-06423a88202b_b02e1765.csv`) has `last_modified` 2026-10-16T11:52:51.701032, 290,643 bytes and 5,257 data rows, under the same file name and header. Download: [overnightvoltagerequirement20-26_1.csv](https://api.neso.energy/dataset/9f4acccb-bf79-452b-aa77-a680ae728722/resource/00881643-7a5e-4eed-b144-06423a88202b/download/overnightvoltagerequirement20-26_1.csv). The resource name carries "20-26" but is a single rolling file; gridflow treats each capture as the whole current state (`latest: whole_capture`), not as a financial-year slice.

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| [Introduction to voltage management](https://api.neso.energy/dataset/9f4acccb-bf79-452b-aa77-a680ae728722/resource/c28b35c9-34da-49a7-bb7e-90d88799c4a4/download/intro-to-voltage-management.pdf) | PDF | upload | `c28b35c9-34da-49a7-bb7e-90d88799c4a4` |
| [Voltage Deep Dive](https://api.neso.energy/dataset/9f4acccb-bf79-452b-aa77-a680ae728722/resource/633e7e26-2b4f-47b0-80de-f39882a2c227/download/voltage-deep-dive.pdf) | PDF | upload | `633e7e26-2b4f-47b0-80de-f39882a2c227` |
| [Week ahead overnight voltage requirement group map](https://api.neso.energy/dataset/9f4acccb-bf79-452b-aa77-a680ae728722/resource/1cf7b77b-3750-49e5-8d57-6b25ccbc1007/download/ew-voltage-zones.pdf) | PDF | upload | `1cf7b77b-3750-49e5-8d57-6b25ccbc1007` |

The three PDFs are bronze-captured and catalogued in the `voltage_requirement_files` family (624,915 / 1,074,224 / 186,375 bytes for the Deep Dive / Introduction / group map). They are explanatory documents and a diagram; they contain worked quantitative examples but do not become tabular silver. They are the vendor's own explanation of geographically defined voltage zones and of requirements expressed as counts of providers, and they are the evidence behind the `Units` interpretation below.

## Families

### `voltage_requirement`

- Kind: tabular · archetype: FC · refresh: weekly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Start Date | `start_date` | date | `%Y-%m-%d` | no | — | — |
| End Date | `end_date` | date | `%Y-%m-%d` | yes | — | — |
| Group | `group` | string | — | no | — | — |
| Units | `units` | int64 | — | yes | — | count of voltage machines/providers (see below) |
| Notes | `notes` | string | — | yes | — | — |
| Last Updated | `last_updated` | datetime | `%Y-%m-%dT%H:%MZ` | no | UTC | — |

- Entity key: `start_date`, `group`, `last_updated` (measured unique in each captured body; the vendor gives no identity guarantee, TODO: verify vendor key guarantee)
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`start_date`)

Silver also carries the standard gridflow columns: `timestamp_utc`, `published_at`, `event_time`, `available_at`, `bronze_capture_id`, `capture_written_at`, `source_run_id`, `dataset_version`.

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

#### The two clocks

- **Vintage** (`ckan_last_modified`): `published_at` and `available_at` are the CKAN `last_modified` of the captured CSV. Every row of one capture carries the same vintage. It says when NESO last replaced the file, not when an individual row was first issued.
- **Event time** (temporal recipe `date_sp1` on `start_date`): `event_time` (and `timestamp_utc`, which equals it) is the start of settlement period 1 of `start_date`, i.e. the start of the GB settlement day, not UTC midnight; in British Summer Time that instant falls on the previous UTC calendar day. `end_date` is kept as a plain date and is not used for event time.
- **Revision timestamp**: `last_updated` is a separate, typed UTC column. It is NOT mapped to an `issue_time`: the vendor dictionary defines it as the last update, not the original issue, so the issue recipe is `none` and no issue/availability claim is made from it. Note that `last_updated` can be later than the capture's `available_at` for some rows, another reason it is not used as availability. Measured 2026-10-23: in each capture, the 18 rows of the newest upload (two plan ranges by nine groups) carry a `last_updated` 57 to 58 minutes after the file's CKAN `last_modified` (2026-10-02T14:19Z and 14:20Z against 13:22:22; 2026-10-16T12:50Z against 11:52:51). Read as UK local time (BST) instead of UTC, both would fall 2 to 3 minutes before the upload, so the literal `Z` may label local time. TODO: verify the zone of `Last Updated` with NESO; gridflow parses it as UTC.

#### Column semantics and units

- `Units` is a count of required voltage machines/providers for the group and night range. It is not an MVAr figure. Source: the captured vendor field info, the vendor package description and the Introduction PDF. The only unit is "count"; no other unit is declared or inferred.
- `Last Updated` carries a literal `Z`; it is parsed as UTC (all distinct spellings in the capture parse). The vendor dictionary example uses the same shape.
- `Start Date` and `End Date` are variable-duration plan ranges, not one fixed week. A small number of rows have `End Date` earlier than `Start Date` (17 rows in each capture, on two plan ranges: start 2025-08-23 to end 2025-08-18, and start 2025-08-26 to end 2025-08-22). They are stored as-is; endpoints are never swapped or "corrected".
- Probable year slip, measured 2026-10-23 in both captures: 18 rows (two plan ranges by nine groups) start on 2020-07-31 and 2020-08-02, yet carry `last_updated` 2021-07-30T15:22Z. Every other row starts on or after 2021-03-20, and no row starts on 2021-07-31 or 2021-08-02, so these read like 2021 plans keyed as 2020. They are stored as published. TODO: verify with NESO.
- `Group` values are stored exactly as published: `V_Mersey`, `V_Midlands`, `V_North`, `V_NorthLondon`, `V_SWPen`, `V_Scotland`, `V_SouthCentral`, `V_SouthEast`, `V_SouthWales`. The group-map PDF labels are Mersey, Midlands, North, North London, Central, SouthEast and South Wales; no explicit code-to-zone crosswalk is published, so the mapping of `V_SWPen`, `V_Scotland` and `V_SouthCentral` to zones or members is unestablished (TODO: verify an explicit NESO code list). Codes are never normalised or aliased.
- `Notes` is free text and almost always blank. Do not infer the overnight operating window of the whole family from any one note (TODO: verify exact overnight start and end).

#### Sentinels and nulls

No `NA`, `N/A` or `-1` token was observed. Zero requirements are real values and are preserved (never nulled). Blank `Notes` are null. Absence of a sentinel in one capture is not a vendor missing-value policy (TODO: verify vendor missing-value definition).

#### Dedup

`(start_date, group)` repeats once in each captured body; adding `last_updated` makes the key unique. The entity key therefore includes `last_updated`, and `latest` stays `whole_capture` rather than collapsing revisions.

### `voltage_requirement_files`

- Kind: files · archetype: FC · refresh: weekly · empty allowed: no
- files: catalogue only

The three DOC PDFs above. Bronze bytes are retained and indexed; no silver is produced.

## Cadence

- Registry refresh: weekly
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Weekly
- Package tags (snapshot): Constraint, Group, Last Updated, Management, Note, Subscribable, Units, Voltage.

Two captures compared (measured 2026-10-23): the file is cumulative. The 2026-10-16 body keeps every key of the 2026-10-02 body with unchanged values (0 keys dropped, 0 changed) and adds 36 rows: four plan ranges by nine groups, 2026-10-10 to 10-12 and 10-13 to 10-16 (`last_updated` 2026-10-09T14:16Z, an upload between the two captures that was not captured itself) and 2026-10-17 to 10-19 and 10-20 to 10-23 (`last_updated` 2026-10-16T12:50Z). In both captures, each weekly upload adds a weekend range (Saturday to Monday) and a weekday range (Tuesday to Friday) and lands on a Friday (2026-10-02, 2026-10-09 by `last_updated`, 2026-10-16). Two captures do not establish that published rows never change; TODO: verify with NESO.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

## Activation receipt

Activated 2026-10-10 (CON batch, `master` `49f7c1a`, PR #104), cutoff 2026-10-08, no prior silver: `voltage_requirement` 5,221 rows, equal to the planned count and to the real-body row count. Reconcile `--all --cutoff 2026-10-08` exited 0 with 0 gaps. Silver path: `C:/gridflow-data/silver/neso_data_portal/voltage_requirement/year=2026/month=10/` (one Parquet file per capture).

Second capture (2026-10-16 refresh): the ingest wrote one response for `voltage_requirement` and found the three PDFs unchanged since their 2026-10-08 capture; the reconcile drained one silver file for 2026-10-16 with 5,257 rows (vintage 2026-10-16T11:52:51), with no epoch or schema drift (gridflow `@.planning/phases/v0.22-close/refresh-20261016/ingest.log` and `reconcile.log`).

The sibling resource `Monthly utilisation data of voltage contracted units` belongs to a different package (`voltage_units_utilisation`, header-only body) and is outside this page.

## Holds

- `voltage_requirement`: held: TODO: what is the overnight operating window and endpoint inclusivity of Start/End Date, what do the reversed ranges mean, which zone/members does each V_ group code cover, and is Last Updated an original issue time with the row available and immutable from then? (unit E-SEM)

The hold is a semantics hold, not a data-quality failure: the capture parsed fully (no exclusions) and the schema is final. Related unresolved items: vendor corrections or explanations for reversed ranges; the original issue/revision model for `Last Updated`; the explicit group-code crosswalk; the vendor's identity guarantee for the entity key. Until these are settled the family is not used as a forecast-issue input, and historical targets do not pass the forward-only availability test.

## References

- @docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md (CKAN `last_modified` as `published_at`)
- @docs/DECISION_LOG/ADR-040-neso-reconcile-adjudication.md
- @docs/neso_data_portal/eligibility.md
- @src/gridflow/connectors/neso_data_portal/registry/voltage-requirement.json
- Batch evidence: @.planning/phases/v0.22-K-CON/K-CON-FACTS.md (section 7), @.planning/v0.22-RESULTS.md (section CON)
