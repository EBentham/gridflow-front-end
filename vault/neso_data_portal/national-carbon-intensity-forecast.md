---
source: "neso_data_portal"
package: "national-carbon-intensity-forecast"
dataset_key: "national_ci_forecast"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# National Carbon Intensity Forecast

GB national carbon intensity of electricity per half-hour, published by NESO as a single CSV on
the Open Data Portal. Each row carries a UTC half-hour label, a **forecast** intensity (the
vendor dictionary says it is predicted with machine-learning models), an **actual** intensity
(the dictionary says it is estimated from metered generation), and a categorical **index** of
the relative level of intensity. Intensity measures the CO2 emitted per kWh of electricity
consumed. It is the bulk file of the same series that the Carbon Intensity API's national
routes serve, which gridflow already ingests under the `neso` source
(@../../neso/datasets/carbon_intensity.md). Like the API, which sends no issue time either, the
CSV has **no issue column**: each target half-hour holds exactly one forecast/actual pair, with
no record of which forecast run produced it. The silver output is held because that issue clock
is missing (FACTS CI-1, g2; see Holds).

- Publisher group: Carbon intensity
- Registry group: carbon-intensity1 · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| National Carbon Intensity Forecast | CSV | upload | `0e5fde43-2de7-4fb4-833d-c7bca3b658b0` |

- Download: [gb_carbon_intensity.csv](https://api.neso.energy/dataset/f406810a-1a36-48d2-b542-1dfb1348096e/resource/0e5fde43-2de7-4fb4-833d-c7bca3b658b0/download/gb_carbon_intensity.csv)
  (CKAN datastore active; datastore unique key `datetime`).
- Captured: `raw_20261008T111249Z_0e5fde43-2de7-4fb4-833d-c7bca3b658b0_8beca58c.csv`,
  5,874,687 bytes, 155,159 data rows, one header epoch.

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| National Carbon Intensity Forecast Methodology | PDF | upload | `36638178-e993-4d34-afdc-4ada83993585` |

- Download: [neso-ci-national-methodology_v2.pdf](https://api.neso.energy/dataset/f406810a-1a36-48d2-b542-1dfb1348096e/resource/36638178-e993-4d34-afdc-4ada83993585/download/neso-ci-national-methodology_v2.pdf)
  (CKAN `last_modified` 2024-10-01T03:16:37Z).
- Captured: `raw_20261008T111254Z_36638178-e993-4d34-afdc-4ada83993585_85da2e89.pdf`,
  359,920 bytes. Catalogue only: no silver output. It is still primary evidence for the
  methodology and is cited below.

## Families

### `national_ci_forecast`

- Kind: tabular · archetype: FC · refresh: intraday · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| datetime | `datetime` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | — |
| forecast | `forecast` | float64 | — | yes | — | gCO2/kWh |
| actual | `actual` | float64 | — | yes | — | gCO2/kWh |
| index | `index` | string | — | yes | — | — |

- Entity key: `datetime`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`datetime`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured resource. For the one capture to date that is
   `2026-10-08T11:11:23.285254`, which CKAN emits without an offset. gridflow reads it as UTC
   (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`, D-15). Every
   silver row of a capture shares this one vintage. It says when the file changed, not when
   any individual forecast was issued.
2. **Event time (`utc_instant` on `datetime`).** `event_time` = `timestamp_utc` = `datetime`.
   All three are equal on every silver row (checked 2026-10-09). `datetime` is the **UTC start**
   of the half-hour it labels. The vendor dictionary documents the column as UTC. The seat's live
   probe joined the captured CSV to the Carbon Intensity API silver, whose `from` is the
   period start: forecast and actual matched on all 675 overlapping periods when joined on
   period start, and on fewer than 1 in 10 when joined on period end
   (gridflow `@.planning/phases/v0.22-K-CI/LIVE-PROBE.md`). Event time is therefore **not** the
   capture time here. The "`none` = capture time" fallback applies to sibling families
   (regional, balancing actions), not this one.

DST check: London-local days 2024-03-31 / 2024-10-27 / 2025-03-30 / 2025-10-26 hold
46 / 50 / 46 / 50 periods after activation, as UTC labels should.

**Units (vendor dictionary only, [NESO data dictionary](https://www.neso.energy/data-portal/national-carbon-intensity-forecast/national_carbon_intensity_forecast)).**
`forecast` and `actual` are **gCO2/kWh**, as the dictionary
states for each field (`unit: gCO2/kWh`). `index` is a text category the dictionary describes as
"Index describing the relative level of the carbon intensity" (its example is `very low`). It
has no physical unit. `TODO: verify` the complete vendor list of index labels and their band
thresholds. The dictionary does not enumerate them.

**Sentinels and missing values (FACTS g5).** The vendor declares no sentinel spelling, and the
record's null-token map is empty.

- Empty `forecast`, `actual` and `index` cells are kept as **null**. The full-body census of the
  newest capture counted 2,901 blank `forecast`, 3,732 blank `actual` and 2,901 blank `index`
  cells. `TODO: verify` why particular observations are absent. Only the vendor can settle it.
- Numeric **zeros** in `actual` are preserved as values, not converted to null.
  `TODO: verify` whether a zero actual is a real estimate or an error marker.
- A small number of `forecast` values the vendor has not explained are preserved **unclipped**,
  and no upper bound is imposed. `TODO: verify` with a vendor correction or explanation.

**Identity and selection.** `datetime` was unique across the whole newest body (155,159
distinct, no duplicates or missing keys). It is kept as the entity key only as a **capture
uniqueness guard**. No vendor text guarantees that a `datetime` identifies one stable record
across revisions, so `_latest` is `whole_capture` (the newest capture wins as a whole) rather
than per-key selection.

**Activation (2026-10-09, master `1ceeaab`).** The family was transformed with cutoff
2026-10-08 (one capture). Silver has **155,159 rows**, equal to the planned count, with
`timestamp_utc` unique. Reconcile at cutoff 2026-10-08 found 0 gaps for this family. No prior
silver existed, so nothing was overwritten (gridflow `@.planning/v0.22-RESULTS.md` §CI;
RULINGS 523–525).

Silver columns beyond the four vendor columns: `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version` (all timestamps tz-aware UTC; `dataset_version` `1+e1` = record version 1,
epoch 1).

**Supersedes the research proposal.** The batch research (gridflow
`@.planning/phases/v0.22-K-CI/K-CI-FACTS.md` §2.1, T01/T02) proposed `temporal: none` with
`datetime` kept as a raw string, because it could not tell period start from period end. The
seat's live probe then established period start, and RULINGS 521 shipped the record as
`utc_instant` on a parsed UTC `datetime`. Where FACTS and this page disagree on the temporal
recipe, the registry record and this page are current.

### `national_ci_forecast_files`

- Kind: files · archetype: FC · refresh: intraday · empty allowed: no
- files: catalogue only

This family captures the methodology PDF (see DOC above). Its extracted text says estimated
data becomes available at the end of a settlement period and that forecasts are provided ahead
of real time. That is publication-timing evidence only. It does not on its own fix whether
the CSV's `datetime` labels the start or the end of the period. The live probe settled that
(see above).

## Cadence

- Registry refresh: intraday
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Hourly
- Intraday: captured once per refresh run — sampled, not complete

The vendor updates the file hourly. gridflow captures one snapshot per refresh run, so hourly
states between runs are not retained. `TODO: verify` whether each hourly update rewrites past
targets, appends new ones, or rolls the window. Only more captures of the same resource,
compared target by target, can show this. No scheduled gridflow refresh exists yet, so
captures are on demand (gridflow `@.planning/v0.22-RESULTS.md` §CI).

Observed (no inference drawn): the CKAN datastore reported a `total` of 155,163 records in a
field-info read at 2026-10-08T13:14Z, about two hours after the capture (written
2026-10-08T11:12:49Z), against 155,159 rows in the captured CSV.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `national_ci_forecast`: held: TODO: no issue column; which forecast issue a past target's value reflects, and whether values are revised after the period, is undocumented (unit E-SEM)

The silver output exists on disk, but it is **held**: it is not eligible for publication or for
point-in-time model use until unit E-SEM answers the question above (RULINGS 521). The
resource carries no forecast-issue clock. A past half-hour's `forecast` may come from any
earlier forecast run, and the vendor does not say whether the stored value is replaced after the
period closes. Without that, the CKAN vintage is the only availability clock. It bounds when
the file existed, not when each value was known. This page therefore publishes schema, units
and row counts only, not data values or ranges.

Partial evidence for E-SEM, recorded here without lifting the hold: the CKAN resource metadata
shows `datastore_unique_keys: ["datetime"]` and `datastore_append_or_update: true`.
`TODO: verify` whether the vendor's datastore append-or-update on `datetime` means past targets
are overwritten in place, and whether the downloadable CSV follows the datastore.

The package-level `eligibility: eligible` in the front matter refers to the package registry
entry. The hold is per family and sits on `national_ci_forecast`.

Related holds (gridflow `@docs/neso_data_portal/eligibility.md`): `country_ci_forecast` is
held on the same issue-clock question. `regional_ci_forecast` is held on it too, and also on
period position and on the meaning of negative intensities. `ci_balancing_actions` is held on
period position only. All are unit E-SEM.
