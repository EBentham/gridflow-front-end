---
source: "neso_data_portal"
package: "balancing-services-use-of-system-bsuos-daily-forecast"
dataset_key: "bsuos_daily_forecast"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-12
layer_coverage: "bronze"
eligibility: "eligible"
page:
  held: "Rows give no settlement run or issue time; the header's £ byte is not valid UTF-8."
  title: Daily BSUoS forecast
  summary: >-
    NESO's half-hourly forecast of the Balancing Services Use of System (BSUoS) charge in £/MWh,
    with the cost and volume behind it.
  facts:
    vendor: "NESO Data Portal: five CSV files, one per financial year"
    cadence: "Not active, as NESO lists it: not updated from April 2023 onward"
    grain: "Each row: settlement date and period, charge, cost and volume"
    history: "NESO lists files for 2018-19 to 2022-23, with data from December 2018"
  landscape: market
  what_it_is: >-
    The Balancing Services Use of System (BSUoS) charge recovers the cost of day-to-day operation of
    the transmission system. NESO forecast it per half hour: forecast cost (£) over forecast volume
    (MWh). Each file mixes historic and future values, with no column telling them apart. NESO warns
    it may bear no relation to later tariffs; it ended with modification CMP361.
  how_used:
    - A benchmark for half-hourly BSUoS charge forecasts, up to March 2023
    - Read beside NESO's settled charges, taking care that those come per settlement run
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each financial-year file whole unless its
      `last_modified` is unchanged (first and last shown). Ingest only: no silver table.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=balancing-services-use-of-system-bsuos-daily-forecast"
      - "GET https://api.neso.energy/dataset/a8368560-87ac-4d31-85b7-625322430456/resource/ac191a63-a67a-4b3b-ac8c-fdfcea79d042/download/daily-bsuos-forecast-2018-19.csv"
      - "GET https://api.neso.energy/dataset/a8368560-87ac-4d31-85b7-625322430456/resource/b98095a8-310a-4fee-8d51-e20531c49465/download/daily-bsuos-forecast-2022-23.csv"
    commands:
      - {run: gridflow ingest neso_data_portal bsuos_daily_forecast --last 24h, comment: "all five files, bronze only"}
  related:
    - {dataset: neso_data_portal/current-balancing-services-use-of-system-bsuos-data, note: "The settled half-hourly BSUoS charges, one file per settlement run"}
    - {dataset: neso_data_portal/daily-balancing-costs-balancing-services-use-of-system, note: "NESO's balancing cost per settlement period, in six categories"}
    - {dataset: neso_data_portal/daily-balancing-volume-balancing-services-use-of-system, note: "NESO's balancing volume per settlement period, in MWh"}
    - {dataset: neso_data_portal/bsuos-monthly-forecast, note: "NESO's rolling monthly forecast of BSUoS costs, 24 months ahead"}
---

# Daily Balancing Services Use of System (BSUoS) Forecast

Five annual CSVs of the system operator's **half-hourly forecast of the BSUoS charge**, one file
per financial year from 2018-19 to 2022-23. Each row is one settlement date and settlement
period with three measures: the estimated BSUoS charge, the forecast balancing cost for that
half hour, and the forecast BSUoS volume. The vendor describes the charge as the forecast
half-hourly balancing costs divided by the forecast BSUoS volume, published "without
prejudice" and possibly bearing no relation to the indicative or actual tariffs published later
(vendor catalogue note). BSUoS is the charge that recovers the cost of day-to-day operation of
the transmission system from generators and suppliers; this package is the forward-looking
estimate of it at settlement-period grain, so it answers "what did NESO expect the per-MWh
balancing charge to be for this half hour" rather than "what was it". Next to the realised
charge (@current-balancing-services-use-of-system-bsuos-data.md) and the realised cost and
volume packages (@daily-balancing-costs-balancing-services-use-of-system.md,
@daily-balancing-volume-balancing-services-use-of-system.md) it would let a model compare the
forecast with the outcome. The monthly forecast package is a separate, coarser series
(@bsuos-monthly-forecast.md).

**The package is closed.** The vendor note says that after modification CMP361 came into force
on 1 April 2023 this dataset is not updated from April 2023 onward; the vendor update frequency
is `Not Active`, the registry refresh is `frozen`, and the newest resource was last modified
2023-04-02 (gridflow
`@.planning/phases/v0.22-K-BAL-2/K-BAL-2-FACTS.md` section 4; vendor extras below).

**There is no silver output for this package.** The bodies carry no settlement-run column
and no issue column, so a settlement key that includes `run_type` cannot be built, and gridflow's
record model cannot generate a constant run column. The family stays ingest-only (RULINGS 667,
the same no-record disposition as RULINGS 538 and 653). A second, independent blocker is an
unresolved encoding (see Known issues). This page therefore describes the bronze files and the
reason silver is absent. Nothing here is held and no output of this package is published; no
data values appear on this page.

- Publisher group: Balancing costs
- Registry group: balancing · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Daily BSUoS Forecast 2018-19 | CSV | upload | `ac191a63-a67a-4b3b-ac8c-fdfcea79d042` |
| Daily BSUoS Forecast 2019-20 | CSV | upload | `c1be6c7c-c36d-46cb-8038-098075599bb0` |
| Daily BSUoS Forecast 2020-21 | CSV | upload | `586d0e6b-cc03-4312-9df3-407438715eb2` |
| Daily BSUoS Forecast 2021-22 | CSV | upload | `25e4acc4-e1b3-48f5-af8c-8d6f84291791` |
| Daily BSUoS Forecast 2022-23 | CSV | upload | `b98095a8-310a-4fee-8d51-e20531c49465` |

The registry routes all five CSVs to the `bsuos_daily_forecast` family, but that family has
`transformer: null`, so the SILVER label records the intended routing and **no silver rows
exist** (nothing under `C:/gridflow-data/silver/neso_data_portal/` for this family; the
eligibility report lists it as ingest-only; the batch reconcile exits 0 with no gap for it).
There is no DOC, HOLD or other disposition in this package: all five resources are data files.
Each resource is captured in bronze as `raw_<stamp>_<resource_id>_<hash>.csv` with a
`.meta.json` sidecar under
`C:/gridflow-data/bronze/neso_data_portal/bsuos_daily_forecast/2026/10/08/` (one capture per
resource, 2026-10-08). All are `url_type: upload`. Row counts are body rows excluding the
header and sum to 89,886 (no blank record rows; each file ends with CRLF).

| Resource | Download | Bytes | Rows | Dates covered | Vintage `ckan_last_modified` | Date text |
|---|---|---:|---:|---|---|---|
| 2018-19 | [daily-bsuos-forecast-2018-19.csv](https://api.neso.energy/dataset/a8368560-87ac-4d31-85b7-625322430456/resource/ac191a63-a67a-4b3b-ac8c-fdfcea79d042/download/daily-bsuos-forecast-2018-19.csv) | 180,453 | 6,045 | 2018-12-01 to 2019-04-05 | 2019-12-11T14:46:49.740950 | `%d-%b-%y` |
| 2019-20 | [daily-bsuos-forecast-2019-20.csv](https://api.neso.energy/dataset/a8368560-87ac-4d31-85b7-625322430456/resource/c1be6c7c-c36d-46cb-8038-098075599bb0/download/daily-bsuos-forecast-2019-20.csv) | 559,494 | 18,329 | 2019-04-01 to 2020-04-18 | 2020-08-11T10:42:51.974667 | `%d-%b-%y` |
| 2020-21 | [daily-bsuos-forecast-2020-21.csv](https://api.neso.energy/dataset/a8368560-87ac-4d31-85b7-625322430456/resource/586d0e6b-cc03-4312-9df3-407438715eb2/download/daily-bsuos-forecast-2020-21.csv) | 949,489 | 30,622 | 2020-04-01 to 2022-01-11 | 2022-01-09T16:00:22.506568 | `%d-%b-%y`, day not always zero-padded (`1-Apr-20`) |
| 2021-22 | [daily-bsuos-forecast-2021-22.csv](https://api.neso.energy/dataset/a8368560-87ac-4d31-85b7-625322430456/resource/25e4acc4-e1b3-48f5-af8c-8d6f84291791/download/daily-bsuos-forecast-2021-22.csv) | 550,458 | 17,374 | 2021-04-04 to 2022-03-31 | 2022-04-21T12:34:50.046758 | `%d-%b-%y` |
| 2022-23 | [daily-bsuos-forecast-2022-23.csv](https://api.neso.energy/dataset/a8368560-87ac-4d31-85b7-625322430456/resource/b98095a8-310a-4fee-8d51-e20531c49465/download/daily-bsuos-forecast-2022-23.csv) | 581,306 | 17,516 | 2022-04-01 to 2023-03-31 | 2023-04-02T15:00:16.562043 | `%Y-%m-%d` |

Row counts, bytes and hashes reproduce FACTS section 2 (`bsuos_daily_forecast`); the date
ranges and date text were measured from the captured bytes for this page. The resource labels
are financial years, but the bodies are not disjoint year files: the 2018-19 file runs into
April 2019, the 2019-20 and 2020-21 files both cover April 2020, and the 2020-21 file runs to
11 January 2022 and overlaps the 2021-22 file from April 2021. See Known issues.

## Families

### `bsuos_daily_forecast`

- Kind: tabular · archetype: FC · refresh: frozen · empty allowed: no
- ingest-only: no silver yet

**No silver record, and why.**

1. **No run or issue column.** The five bodies have only `Date`, `SP` and three measures. A
   BSUoS family key follows the settlement convention `(date, period, run_type)`, and
   `run_type_column` must reference an existing string column; the record model has no constant
   or source-generation field (`record.py:524` and `record.py:690` per FACTS). `(Date, SP)` alone
   would break the settlement-key rule. Neither the filename (a financial year) nor a generated
   constant is run-type evidence. The frozen daily proposal must not become a record
   (FACTS BAL-2a-2; RULINGS 667, 538, 653).
2. **Unresolved encoding.** All five headers contain the single byte `0xA3`, which is not valid
   UTF-8. It sits where the pound sign belongs in `BSUoS £/MWh` and `Half hourly cost £`
   (the encoding is unresolved; FACTS T05 records only that the byte is not valid UTF-8), and no
   vendor encoding declaration was found. A record would need that declaration or an explicitly adjudicated faithful decoding
   (FACTS T05). `TODO: verify` the vendor encoding.
3. **Not wholly forward.** The 2020-21 resource includes 96 rows (two days) dated after its own
   last-modified instant (2022-01-09T16:00), while 89,790 rows are dated on or before their
   resource's last-modified (FACTS g2). The package mixes later-uploaded history with
   forecast rows in the same file, and no body column says which is which.

Measured within each body: `(Date, SP)` is unique, and across resources the 14,685
overlapping `(Date, SP)` keys agree on all three shared measure columns (0 differ; FACTS g3,
command C14). This measures the five captured bodies and is no guarantee of future uniqueness.
Merge and activation confirm the disposition: PR #107 squash `eeaac8d` (RULINGS 681) and
activation (RULINGS 682) left the family record-less; the later BAL-2aH unit (RULINGS 686, 687)
did not touch it (`@.planning/v0.22-RESULTS.md`, sections BAL-2a and BAL-2aH). What would unblock
a record: a vendor run or issue identifier plus an approved constant-column mechanism, or a
ruling that changes the run-key requirement for this publication, plus the encoding
declaration. `TODO: verify` which of these NESO or the project chooses.

Bronze columns (vendor header, as captured, identical in all five bodies):

`Date,SP,BSUoS ?/MWh,Half hourly cost ?,Half hourly volume MWh` (`?` = byte `0xA3`)

| Vendor column | Unit (vendor field title / dictionary) | Notes |
|---|---|---|
| `Date` | date | Settlement date; see Two clocks. Text format differs by resource (table above) |
| `SP` | Number (vendor dictionary unit); settlement-period index | Observed 1 to 48 only; see Known issues |
| `BSUoS £/MWh` | £/MWh | Estimated BSUoS charge for the half hour |
| `Half hourly cost £` | £ | Forecast balancing cost for the half hour |
| `Half hourly volume MWh` | MWh | Forecast BSUoS volume for the half hour |

Units are the vendor's own (header text and the vendor dictionary, FACTS g4 and T02 to T04);
they are not inferred from column names or magnitudes.

## Cadence

- Registry refresh: frozen
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Not Active

The vendor note states that this dataset is not updated from April 2023 onward, and the last
resource modification is 2023-04-02. Treat all five files as static. A new capture is a new
vintage only if NESO re-uploads a file, which would change that resource's `ckan_last_modified`.
Package created 2019-12-11 and metadata last modified 2023-04-12 in the catalogue snapshot
of 2026-10-06.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

## Holds

- none

The generated list reports no package-level holds and no resource has a HOLD disposition. The
absence of a silver record is a no-record disposition, not a hold on a published output: there
is no held question or unit for this package.

## Two clocks

Bronze-only package, so no silver `timestamp_utc` or `available_at` exists. The clocks a record
would carry are:

1. **Vintage (`ckan_last_modified`).** Every resource is `url_type: upload`, so the vintage for
   a capture is that resource's CKAN `last_modified` (sidecar field `ckan_last_modified`), not
   the capture-time fallback. `available_at` would equal it. CKAN emits it without an offset;
   gridflow reads it as UTC (`@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`).
   Per-resource values are in the table above. There is no issue column in the body, so the
   issue recipe would be `none`. Because the vintage is the upload time, it can be far later
   than the periods it covers: the 2018-19 file starts 2018-12-01 but was last modified
   2019-12-11, and its description says the data are "present from December 18". Do not treat
   the file's financial-year label as the date a forecast was made.
2. **Event time.** No temporal recipe is frozen, because there is no record. The candidate is
   `sp_pair(Date, SP)`, the start of the settlement period on the London settlement clock:
   the vendor `Date` description uses UTC in winter and UTC+1 in summer, and `SP` identifies
   the half-hour settlement interval (FACTS g1, T06). That candidate is not a `none` recipe.
   (Under `none`, `timestamp_utc` would be the capture time rather than a market time; that
   would be wrong for this package and is not proposed.) Since no silver exists, no
   `timestamp_utc` is published for this family at all.

## Units and sentinels

Units (vendor header and dictionary, FACTS g4): the charge is **£/MWh**, the half-hourly cost
is **£**, the half-hourly volume is **MWh**. `SP` carries the vendor dictionary unit "Number" and is a settlement-period index.

Sentinel handling (FACTS g5): the five bodies contain no `NA` or `N/A` tokens, no thousands
separators, currency symbols or percent signs in the numeric cells, and (measured again for this
page) no dash and no blank value cell in any of the 89,886 rows; every row has five fields.
Zero values do occur: 1,226 zero charge cells and 1,202 zero cost cells across the package, with
a longest consecutive zero run of 12 rows in source order. Zeros are numbers. No primary source
establishes that a zero (or any other value) is a missing-data marker, so nothing is mapped to
null. `TODO: verify` the vendor's meaning for zero where no definition exists.

The dash null token that gridflow now supports through the opt-in numeric trim (ADR-034
amendment 1, BAL-2aH) applies to a different package, its forecast-summary family `bsuos_monthly_forecast_fc_summary`
(@bsuos-monthly-forecast.md). It does not arise here, because no dash cell exists in these
bodies. `TODO: verify` whether a dash means zero or not-available; this is an open vendor question
and is not decided on this page.

## Known issues and gotchas

- **No run or issue column.** Rows are not labelled with a settlement run (II, SF or RF), unlike
  the BSUoS charge packages. Do not assume `II`, and do not key on `(Date, SP)` alone.
- **Header byte `0xA3`.** The pound-sign byte is not UTF-8, so a strict UTF-8 reader fails
  on the header of every file. Encoding is unresolved (`TODO: verify`); do not silently
  re-encode.
- **Date text differs.** Four files use day-month-year with an abbreviated month and a two-digit
  year (`%d-%b-%y`; the 2020-21 file has unpadded days such as `1-Apr-20`); the 2022-23 file
  uses ISO `%Y-%m-%d`. Parse per resource.
- **Resource years overlap.** The files are labelled by financial year but extend past it or
  start inside the previous one (table above). The 14,685 keys present in more than one file
  agree on the shared measures, so a union is consistent for the captured bytes.
- **Package coverage gaps (measured on the captured bytes, whole days absent from the files
  that carry the neighbouring dates):** 2020-03-15 to 2020-03-16, 2020-08-10 to 2020-08-12,
  2020-10-06, 2020-10-20, and 2021-03-27 to 2021-04-03 (eight days, not covered by the 2021-22
  file, which starts 2021-04-04). `TODO: verify` whether the vendor intended these gaps.
- **Settlement-period counts per day** (measured; `Date` and `SP` only): the four spring
  clock-change days (2019-03-31, 2020-03-29, 2022-03-27, 2023-03-26) have 46 periods as
  expected. The four autumn clock-change days (2019-10-27, 2020-10-25, 2021-10-31, 2022-10-30)
  have 48 and `SP` never exceeds 48 anywhere, so the 50-period day is not represented.
  2019-04-04 has 47 periods in both files that carry it (period 48 absent), and 2019-04-07,
  2020-04-05 (twice, in two files) and 2022-04-03 have 46 periods although they are not
  clock-change days. `TODO: verify` the cause of each; a record would have to carry the
  settlement-calendar rule (periods `1..50`, DST days 46 and 50), not assume 48.
- **Historic and future rows are mixed.** The resource descriptions say the vendor publishes
  "historic and future" forecast values; there is no column separating them (see item 3 under
  the no-record reasons).
- **Not the realised charge.** The vendor says the forecast may bear no relation to the
  indicative or actual tariffs; do not join it to realised data as if it were an outcome.

## Implementation delta

- **`run_type`**: sibling BSUoS records declare `run_type_column`; this family cannot, because
  the body has no run column and the record model has no constant-column mechanism. No record
  exists by ruling (RULINGS 667, 538, 653).
- **Registry disposition vs silver**: the registry labels the five CSVs `SILVER`, but the
  family has `transformer: null`. The label is a routing statement, not evidence of silver
  data. Reality: no silver exists.
- **Encoding**: bytes include `0xA3` and no vendor declaration exists; no decoding has been
  adjudicated for this family (FACTS T05).
- **Vendor catalogue vs bodies**: the catalogue says the data are "present from December 18"
  (2018-12-01, matches the first row of the 2018-19 file) and the dataset is not updated after
  April 2023 (last date 2023-03-31, matches).

## Modelling notes

TODO. No model consumes this package, and no silver exists to feed one. Candidate use once a
run-bearing key and an encoding declaration exist: the forecast BSUoS charge per settlement
period as a feature or benchmark for charge forecasting, compared with the realised charge
(@current-balancing-services-use-of-system-bsuos-data.md) by the settlement coordinates.
Because the vintage is the upload time and not a forecast issue time, it must not be used as an
as-of-safe feature for dates before its `ckan_last_modified`. The series ends 2023-03-31. Do not
join to settlement-run data on `(date, period)` alone.

## Links

- [Official dataset page](https://www.neso.energy/data-portal/balancing-services-use-of-system-bsuos-daily-forecast) (`TODO: verify` the URL resolves; derived from the package name)
- Registry record: `@src/gridflow/connectors/neso_data_portal/registry/balancing-services-use-of-system-bsuos-daily-forecast.json`
- Eligibility report: `@docs/neso_data_portal/eligibility.md`
- Batch evidence: `@.planning/phases/v0.22-K-BAL-2/K-BAL-2-FACTS.md`, `@.planning/phases/v0.22-K-BAL-2aH/VERIFICATION.md`
- Activation receipt: `@.planning/v0.22-RESULTS.md` (sections BAL-2a and BAL-2aH); rulings 538, 653, 667, 678, 680, 681, 682, 683, 686, 687 in `@.planning/RULINGS.md`
- ADRs: `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`, `@docs/DECISION_LOG/ADR-034-neso-generic-silver-engine.md`, `@docs/DECISION_LOG/ADR-040-neso-reconcile-adjudication.md`
- Domain: @../../../20-domain/concepts/settlement-period.md, @../../../20-domain/concepts/settlement-runs.md
- Sibling pages: @bsuos-monthly-forecast.md, @current-balancing-services-use-of-system-bsuos-data.md, @daily-balancing-costs-balancing-services-use-of-system.md, @daily-balancing-volume-balancing-services-use-of-system.md

Supported by National Energy SO Open Data
