---
source: "neso_data_portal"
package: "monthly-utilisation-data-of-voltage-contracted-units"
dataset_key: "voltage_units_utilisation"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Monthly Utilisation data of Voltage Contracted units

Monthly reactive-power utilisation of the units contracted under NESO's voltage service. For each
balancing unit (BMU) and calendar month, NESO reports how much reactive power the unit injected
and absorbed when the Control Room instructed it, plus the sum of the two. The vendor describes
the dataset as an overview of "the injection and absorption of reactive power utilised by the
unit based on the instructions provided by NESO's Control Room", with the unit identifier
(BMU ID), the geographical region of the unit and the monthly totals. The single resource covers
the **Voltage 2026** service. Use it as an outturn record of delivered voltage-support
utilisation per unit and month, for example to relate voltage-service cost reports to the units
that delivered them (see the sister outturn cost packages in this vendor folder). It is
delivered utilisation, not a forecast: there is no forecast column.

The vendor package note says updates to the dataset begin from 9 October 2026. That matches the
capture history: a sweep on 2026-10-08 found the file header-only (no data rows), and a probe on
2026-10-10 found one data row, with CKAN `last_modified` `2026-10-09T12:57:26.168291`
(gridflow `@.planning/phases/v0.22-K-SYS-1/LIVE-PROBE.md`). Because the family is not
`empty_allowed`, the header-only body failed the 2026-10-08 sweep and was captured on 2026-10-10
(RULINGS 639, data op class 2). The page reflects that one capture. Only one populated month
(Aug-26) has been seen so far.

- Publisher group: System
- Registry group: system · archetype: SER
- Vendor tags: Network Services, Reactive Power, Subscribable, Utilisation data, Voltage
- Package id: `f8386ee1-4e9c-474d-afbf-6339852c898b`

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Monthly Utilisation Data of Voltage 2026 Contracted Units | CSV | upload | `e13539d0-eed0-4561-82a4-4517c14253c1` |

- Monthly Utilisation Data of Voltage 2026 Contracted Units → `voltage_units_utilisation`.
  Download as captured: [utilisation-report.csv](https://api.neso.energy/dataset/f8386ee1-4e9c-474d-afbf-6339852c898b/resource/e13539d0-eed0-4561-82a4-4517c14253c1/download/utilisation-report.csv).
  The 2026-10-06 catalogue snapshot listed a different file name
  (`monthly_utilisation_data_of_voltage_2026_contracted_units.csv`) for the same resource id, so
  the file name has changed since the snapshot. The stable handle is the resource id, not the URL.
  CKAN datastore active. CKAN `last_modified` of the captured file: `2026-10-09T12:57:26.168291`.
- Captured: `raw_20261010T155055Z_e13539d0-eed0-4561-82a4-4517c14253c1_556901ab.csv`
  (bronze `2026/10/10`), 173 bytes, 1 data row, one header epoch.
- There is no DOC resource in this package. It has exactly one resource.

## Families

### `voltage_units_utilisation`

- Kind: tabular · archetype: SER · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| BMU ID | `bmu_id` | string | — | no | — | — |
| Month and Year | `month_and_year` | date | `%b-%y` | no | — | — |
| Location | `location` | string | — | yes | — | — |
| Total Injection MVAr | `total_injection_mvar` | float64 | — | yes | — | MVAr |
| Total Absorption MVAr | `total_absorption_mvar` | float64 | — | yes | — | MVAr |
| Total Injection and Absorption MVAr | `total_injection_and_absorption_mvar` | float64 | — | yes | — | MVAr |

- Entity key: `bmu_id`, `month_and_year`
- Latest: `whole_capture`
- Temporal recipe: month (`month_and_year`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource. For the one capture to date that is
   `2026-10-09T12:57:26.168291`, which CKAN emits without an offset. gridflow reads it as UTC
   (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). The file has **no
   issue column** (issue recipe `none`). There is no evidence the figures were public at an
   earlier instant or are immutable once issued, so the upload vintage is the only availability
   claim made.
2. **Event time (`month` on `month_and_year`).** `timestamp_utc` = `event_time` = the engine's
   month anchor: the start of the first UK settlement period of the labelled month, expressed in
   UTC. For the captured row (`Aug-26`, a BST month) this is `2026-07-31T23:00:00Z`. Event time is
   therefore **not** the capture time and **not** a vendor timestamp. It is a period label
   anchor. The row describes the whole utilisation month, not an instant. Do not join it to
   half-hourly data on the timestamp alone; aggregate the half-hourly side to the month first.

**Month parsing.** `Month and Year` arrives as `Aug-26`. The record parses it with `%b-%y` to the
first day of the month (`2026-08-01`). The vendor comment says the value is meant to be read by
people as month-year, for example `Jan-25`.

**Units (vendor dictionary only).** All three quantity columns carry the vendor unit **MVAr**
in the published field dictionary (snapshot
`@.planning/research/neso-snapshots/field-info/20261008T114228Z/voltage_units_utilisation.json`).
The vendor titles the columns "Total injection for the month (LAG MVAr)", "Total absorption for
the month (LEAD MVAr)" and "Total (combination of absorption and injection for the month)
(MVAr)". gridflow does not convert them. In particular they are not turned into MVArh or any
other derived monthly aggregate. `Location` is vendor free text ("The geolocation of the unit",
example `England`). `BMU ID` is the unit identifier. Neither carries a unit.

**Sentinels and missing values (FACTS g5).** The record declares no null token. The captured
body has no blanks, `-1`, `N/A`, `NA`, zeros, thousands separators, currency symbols or percent
signs in the value cells. **Negative quantities are real values and survive unchanged.** The one
row carries a negative absorption and a negative combined total. The combined column equals
injection plus absorption in that row (a measured check on one row, not a vendor guarantee).

**Identifiers stored as-is.** The BMU ID of the captured row is the composite label
`THURB-1,2 & 3`, quoted in the CSV because it contains commas and an ampersand. It is stored
unchanged and not split, trimmed or normalised.

**Identity and selection.** The entity key is `bmu_id` plus `month_and_year`. It has no
duplicates in the capture (1 row). `_latest` is `whole_capture`: the newest capture is served as a
whole, and older captures stay reachable through their vintages.

**Open vendor questions (TODOs).** None of these is a hold, and none blocks the retained rows:

- `TODO: verify` (SYS0-KEY) whether NESO guarantees one row per BMU and month. The dictionary
  names the unit and the utilisation month but states no primary-key guarantee.
- `TODO: verify` (SYS0-REPLACEMENT) whether a later monthly upload replaces the previous month
  or appends to it. One populated capture cannot show this. It needs vendor documentation of
  retention, or a second monthly capture.
- `TODO: verify` (SYS0-AGGREGATION) the sign and aggregation convention behind the monthly
  totals. The magnitudes in the captured row are large for a monthly MVAr sum and the vendor
  does not say how the month is aggregated. Preserve the supplied signed values and the vendor
  unit. Do not infer a different unit or aggregate.

**Activation (2026-10-10, master `4d06b9f`, PR #105).** Transformed over the window
2026-10-08..2026-10-10: **1 silver row**, equal to the planned count (no prior silver existed, so
nothing was overwritten). The window had to include 2026-10-10 because this capture is dated
then, while the other SYS-1 captures are dated 2026-10-08. Reconcile `--all --cutoff 2026-10-10`
exited 0 with 113 families and 0 gaps. This closes the header-only missing resource left by the
earlier sweep (gridflow `@.planning/v0.22-RESULTS.md` §SYS-1; RULINGS 639, 647).

Silver columns beyond the vendor columns: `timestamp_utc`, `published_at`, `bronze_capture_id`,
`capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version` (all
timestamps tz-aware UTC; `dataset_version` `1+e1` = record version 1, epoch 1).

## Cadence

- Registry refresh: monthly
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Monthly
- The vendor note says updates begin from 9 October 2026. Which day of the month later updates
  land on is not stated: `TODO: verify`.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

## Holds

- none

No output of this package is held. The two open questions above (replacement behaviour and
aggregation convention) do not change eligibility. The family stays `empty_allowed: no`, so a
future header-only upload would fail loudly rather than publish an empty month.
