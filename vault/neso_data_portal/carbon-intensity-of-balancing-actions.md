---
source: "neso_data_portal"
package: "carbon-intensity-of-balancing-actions"
dataset_key: "ci_balancing_actions"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Carbon Intensity of Balancing Actions

This dataset shows how much the Balancing Mechanism (BM) changes the carbon intensity of GB
generation. Each half-hour row has two figures. The first, `FPN`, is the carbon intensity
the system would have had if every BM unit had followed its Final Physical Notification, the
schedule it submits at gate closure. The second, `BOA`, is the carbon intensity once the
control room's accepted bids and offers are applied. `Difference` is the gap between them;
the dictionary says it is positive when the BOA profile is the more carbon-intensive one.
The vendor methodology (the DOC resource below, issued April 2021) works out each profile by
weighting fuel-type emission factors by generation and dividing by national demand. It
excludes interconnectors and small BM units, and it says the figure tracks a change in
intensity, not emissions. A typical case is a constraint that forces the control room to
bid wind down and offer gas up, which pushes BOA above FPN. Models can use the series as a
half-hourly measure of the carbon cost of balancing actions and constraint management. See
@../../../20-domain/concepts/carbon-intensity.md,
@../../../20-domain/markets/gb-balancing-mechanism.md and
@../../../20-domain/concepts/bm-units.md.

The data comes from a CKAN upload-file package on the NESO Open Data Portal
(@../README.md). That is not the Carbon Intensity API (`neso` source,
@../../neso/README.md); the methodology cites that API, but the repo has no API counterpart
for this series (LIVE-PROBE).

> **Status: held.** The silver output is built but held from publication: it is not yet
> known whether `DATETIME` marks the start or the end of the half-hour (unit E-SEM,
> RULINGS 521). Row counts and schema appear on this page; data values do not.

- Publisher group: Carbon intensity
- Registry group: carbon-intensity1 · archetype: SER

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Carbon Intensity of Balancing Actions | CSV | upload | `0b7edf10-4328-4b85-a0af-e6daa6bb8428` |

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| Carbon Intensity Balancing Actions Methodology | PDF | upload | `86fb2746-4f5f-4a22-85bd-dbb63b75a791` |

### Resource download links

URLs from the catalogue snapshot `20261006T195819Z`, matching the `request_url` in each
capture's sidecar:

| Resource | Disposition | Download |
|---|---|---|
| Carbon Intensity of Balancing Actions (CSV) | SILVER → `ci_balancing_actions` (held) | [balancing_actions_carbon_intensity_ckan.csv](https://api.neso.energy/dataset/5d3a7f30-020b-4bf2-9f56-1a7522ece994/resource/0b7edf10-4328-4b85-a0af-e6daa6bb8428/download/balancing_actions_carbon_intensity_ckan.csv) |
| Carbon Intensity Balancing Actions Methodology (PDF) | DOC → `ci_balancing_actions_files` (catalogue only) | [eso-ci-balancing-actions-methodology_neso.pdf](https://api.neso.energy/dataset/5d3a7f30-020b-4bf2-9f56-1a7522ece994/resource/86fb2746-4f5f-4a22-85bd-dbb63b75a791/download/eso-ci-balancing-actions-methodology_neso.pdf) |

The package has these 2 resources and no others (`num_resources: 2`, CKAN package id
`5d3a7f30-020b-4bf2-9f56-1a7522ece994`). The CSV is also loaded into the CKAN Datastore
(`datastore_active: true`), and its field dictionary is the source of the units below.
gridflow downloads the uploaded file; it does not read the Datastore.

## Families

### `ci_balancing_actions`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| DATETIME | `datetime` | string | — | yes | — | UTC ISO 8601 |
| FPN | `fpn` | float64 | — | yes | — | gCO2/kWh |
| BOA | `boa` | float64 | — | yes | — | gCO2/kWh |
| Difference | `difference` | float64 | — | yes | — | gCO2/kWh |

- Entity key: `datetime`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Column meanings (vendor field dictionary).** `DATETIME` ("Date & Time") is the record
timestamp, with the unit given as `UTC ISO 8601`. `FPN` is the carbon intensity had every BM
unit followed its FPN profile. `BOA` is the carbon intensity of the FPNs with accepted
bid/offer profiles applied. `Difference` ("FPN BOA Difference") is positive when the BOA
profile is higher than the FPN profile and negative when it is lower. Across the full
captured body, `Difference = BOA − FPN` held on every row (96,163 rows, 0 mismatches;
K-CI-FACTS §2.4, check C6).

**Units.** `FPN`, `BOA` and `Difference` are all **gCO2/kWh**, as stated in each field's
`unit` in the vendor dictionary (`field-info/20261008T114228Z/ci_balancing_actions.json`,
lines 34, 46 and 58; K-CI-FACTS §2.4 g4). The silver values are not rescaled. `DATETIME`
has no physical unit; the dictionary gives its unit as UTC ISO 8601.

**Two clocks.**

1. **Vintage: `ckan_last_modified`.** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the resource at capture time. CKAN gives this value without an offset;
   gridflow reads it as UTC (ADR-030 D-15, corroborated rather than vendor-documented). For
   the one capture so far, `published_at` = `available_at` = 2026-10-07T11:38:19.659640Z.
   The resource is `url_type=upload`, so this is the file's upload time and not a release
   time for any one row.
2. **Event time: temporal recipe `none`.** gridflow does **not** derive the half-hour from
   the data. `timestamp_utc`, and `event_time` copied from it, hold the **capture time** (the
   bronze write instant, 2026-10-08T09:14:50.052577Z on every row of the current output).
   They are not the time the measurement refers to. The vendor's half-hour stays in
   `datetime` as the raw string, for example `YYYY-MM-DDTHH:MM:SS` with no `Z` suffix. The
   value is UTC by the dictionary, and UTC-date DST-day checks support that (K-CI-FACTS
   §2.1/§2.4 g1). It is not converted to a timestamp because it is not established whether
   the label is the start or the end of the period. The seat probe settled that question
   for the national and country forecasts (period start) by joining them to Carbon
   Intensity API silver. It **could not** be tested for this family because the repo has
   no API counterpart (LIVE-PROBE, "Not measurable").
   - TODO: verify whether `DATETIME` labels the start or the end of the half-hour. The
     vendor methodology PDF does not say. This blocks a `utc_instant` recipe and lifting
     the hold.

**Identity and `_latest`.** `datetime` is a uniqueness guard on each capture. In the
current capture it is unique and never missing (96,163 distinct, 0 duplicates, 0 nulls),
but the vendor does not guarantee that a timestamp keeps the same identity when values are
corrected. `whole_capture` makes the newest capture the latest view, so rows the vendor
drops are not carried forward.
- TODO: verify whether the vendor rewrites, appends or rolls the file between uploads.
  This needs a second authorised capture of the same resource to compare (K-CI-FACTS §3.1
  CI-1).
- TODO: verify whether past half-hours are revised after first publication. Nothing in
  the dictionary, resource description or methodology says either way.

**No issue clock.** The epoch's issue is `{"kind": "none"}`. The file has no issue or
forecast-run column, so it is not a forecast archive. Each target timestamp appears once
in the capture (multiplicity `{1: 96163}`).

**Sentinels and nulls (K-CI-FACTS g5).** The record declares no null tokens.
- A `Difference` of `-1.0` is **valid signed arithmetic, not a null sentinel**. It matches
  `BOA − FPN` on those rows. Keep it.
- Numeric zeros are values and are kept.
- No blank values were found in `FPN`, `BOA` or `Difference` in the captured body. Silver
  confirms 0 nulls in each. The columns stay nullable, so a future blank would load as
  null, not as zero.
- Signs are kept: a negative `Difference` means balancing lowered carbon intensity.

**Silver output (activation 2026-10-08, RULINGS 524/525).**
- Path: `C:/gridflow-data/silver/neso_data_portal/ci_balancing_actions/year=2026/month=10/`,
  one Parquet file from the 2026-10-08 capture.
- Rows: **96,163**, equal to the planned count and the bronze body
  (`raw_20261008T091450Z_0b7edf10-…_1ae8306e.csv`, 4,755,075 bytes, one header epoch).
- Reconcile `--cutoff 2026-10-08`: 0 gaps.
- Columns: `datetime` (String), `fpn`, `boa`, `difference` (Float64), and the engine columns
  `timestamp_utc`, `published_at`, `capture_written_at`, `event_time`, `available_at`
  (Datetime µs, UTC), `bronze_capture_id`, `source_run_id`, `dataset_version` (String).
- TODO: verify why the Datastore's `datastore_search` total (96,211 at
  2026-10-08T12:01Z) differs from the uploaded CSV body captured at 09:14Z (96,163 rows).
  A later Datastore refresh is plausible but has not been measured.
- Coverage span: not published while the family is held.

### `ci_balancing_actions_files`

- Kind: files · archetype: SER · refresh: daily · empty allowed: no
- files: catalogue only

This family holds the methodology PDF only: one capture,
`raw_20261008T091453Z_86fb2746-…_e1bf14fc.pdf`, 225,625 bytes, CKAN `last_modified`
2024-10-01T03:19:45.417470 (read as UTC). There is no silver record and no temporal recipe;
the PDF is kept as vendor evidence. It describes the method (fuel-type emission factors,
FPN against BOA profiles, demand-normalised) but says nothing about where the CSV
timestamp sits in the period.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Daily

The CSV's CKAN `last_modified` was 2026-10-06T11:41:19 in the catalogue snapshot and
2026-10-07T11:38:19 at capture, which fits a roughly daily re-upload. TODO: verify the
vendor's upload time of day and how far behind real time the latest row is (publication
lag). One capture cannot establish either. No scheduled gridflow refresh exists yet (OWNER
457–460), so new captures need a manual sweep.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence URL from the catalogue: https://www.neso.energy/data-portal/ngeso-open-licence
(`license_id: ESO`). The CKAN author is "National Grid Electricity System Operator"; the
methodology predates the NESO rename.

## Holds

- `ci_balancing_actions`: held: TODO: whether DATETIME marks period start or end (unit E-SEM)

Detail:
- **What is held.** The `ci_balancing_actions` silver output. The package-level eligibility
  is `eligible`, but the record-level hold wins (ADR-036 P-8), so
  `docs/neso_data_portal/eligibility.md` lists this family as held.
- **Hold question.** Does `DATETIME` mark the start or the end of the settlement half-hour?
- **Unit.** E-SEM.
- **Ruling.** RULINGS 521 (PROXY-SOURCED seat, 2026-10-09). Regional and balancing-actions
  keep temporal `none` and stay held. National and country moved to `utc_instant` (period
  start) but stay held on the separate issue-clock question. The balancing-actions hold
  has no issue-clock part, because this is a measurement series, not a forecast.
- **What lifts it.** Vendor confirmation of the label position, or a measured join against
  an independent half-hourly source with known period boundaries. Then the record can move
  to `utc_instant` and be reviewed for eligibility.
- **Activation.** Merge PR #88 (`1ceeaab`) under RULINGS 523. Activation, reconcile and
  coverage under RULINGS 524 to 526 (`.planning/v0.22-RESULTS.md` §CI).

## Evidence

All paths are in the gridflow checkout unless noted.
- `.planning/phases/v0.22-K-CI/K-CI-FACTS.md`: §1 inventory, §2.4 family facts, §2.14 PDF
  families, §3.1 CI-1, §3.5 g1–g5, commands C1/C2/C5/C6.
- `.planning/phases/v0.22-K-CI/LIVE-PROBE.md`: period position settled for national and
  country; not measurable here.
- `.planning/v0.22-RESULTS.md` §CI: activation receipt.
- `.planning/RULINGS.md`: 521 and 523–526.
- `src/gridflow/connectors/neso_data_portal/registry/carbon-intensity-of-balancing-actions.json`:
  the registry record.
- `docs/neso_data_portal/eligibility.md`: generated eligibility report.
- `docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`: D-15, naive CKAN time read
  as UTC.
- Vendor field dictionary: `.planning/research/neso-snapshots/field-info/20261008T114228Z/ci_balancing_actions.json`.
- Sibling pages: @./national-carbon-intensity-forecast.md,
  @./regional-carbon-intensity-forecast.md and @./country-carbon-intensity-forecast.md.
