---
source: "neso_data_portal"
package: "obligatory-reactive-power-service-orps-utilisation"
dataset_keys: ["orps_utilisation_historic_reactive", "orps_utilisation_reactive", "orps_utilisation_reactive_default"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: ORPS reactive power utilisation
  summary: >-
    NESO's monthly record of how much reactive power each unit was asked to absorb or produce,
    with the default payment rates.
  facts:
    vendor: "NESO Data Portal, ORPS package: four CSV files, a workbook and two PDFs"
    cadence: Monthly, as NESO lists it; updated mid-month with data to two months earlier
    grain: "Utilisation: a row per unit, columns per month; rates: a row per month"
  landscape: market
  what_it_is: >-
    Grid Code generators must be able to absorb or produce reactive power, which NESO calls on to
    manage voltage near their connection. These files give each unit's monthly utilisation, lead
    (read as absorbed) and lag (read as produced) apart, in MVArh as NESO's package text states;
    the historic file's dictionary says MVAr. Another table holds default payment rate
    inputs.
  how_used:
    - Which units NESO calls on for reactive power, month by month
    - "The two default rates NESO pays for reactive power, in £/MVArh, by month"
  chart:
    type: bar
    silver: neso_data_portal/orps_utilisation_reactive_default
    filter:
      - {column: year_vendor, op: ge, value: 2008}
      - {column: year_vendor, op: le, value: 2025}
    group: year_vendor
    value: x_1
    aggregation: mean
    sort: label
    unit: £/MVArh
  chart_view:
    title: "Mean default rate at X = 1, 2008 to 2025"
    caption: >-
      Silver `orps_utilisation_reactive_default`, the third table here (the utilisation tables are too
      wide to show): mean of NESO's twelve monthly `X = 1` default rates in each full calendar year,
      2008 to 2025, £/MVArh as NESO's guidance labels it.
    alt: >-
      Horizontal bar chart from neso_data_portal/orps_utilisation_reactive_default of the mean monthly
      default rate at X = 1 in each year, £/MVArh, 2008 to 2025. From 2009 to 2020 every year sits
      between 2.417 (2010) and 3.355 (2018); 2008 is 3.783. The mean rises to 5.048 in 2021 and 11.883
      in 2022, then falls to 6.837, 4.462 and 4.911.
    key:
      - {series: x_1, label: Rate at X=1, paint: petrol}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then each file whole unless `last_modified` is
      unchanged. Bronze only: the workbook, PDFs and newer long file, which repeats a complete row.
    commands:
      - {run: gridflow ingest neso_data_portal orps_utilisation_reactive --last 24h, comment: "whole files; swap in any key"}
      - {run: gridflow transform neso_data_portal orps_utilisation_reactive --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      silver: neso_data_portal/orps_utilisation_reactive_default
      filter:
        - {column: year_vendor, op: eq, value: 2022}
        - {column: month_vendor, op: ge, value: 5}
      order_by: [month_vendor]
      columns: [year_vendor, month_vendor, x_1, x_0_2, hpim, papim, ppim, frpim, im]
    key: [year_vendor, month_vendor]
    caption: "May to December 2022; the `X = 1` rate peaks at 16.97 £/MVArh in October."
    fields:
      year_vendor: "Calendar year of the rate, NESO's `Year`"
      month_vendor: "Month of the year, 1 to 12, NESO's `Month`"
      x_1: "Default payment rate at utilisation factor X = 1, £/MVArh (NESO's guidance)"
      x_0_2: "Default payment rate at X = 0.2, £/MVArh (NESO's guidance)"
      hpim: "Heren power-price input, NESO's `HPIm`; labelled only £"
      papim: "Argus power-price input, NESO's `PAPIm`; labelled only £"
      ppim: "Platts power-price input, NESO's `PPIm`; labelled only £"
      frpim: "RPI index input, NESO's `FRPIm`: an index level, not pounds (NESO's guidance)"
      im: "Indexation factor, NESO's `Im`: dimensionless (NESO's guidance)"
      timestamp_utc: "gridflow's capture time, UTC; not the rate's month"
      published_at: "When NESO last changed the file (CKAN `last_modified`), not first publication"
      bronze_capture_id: Path of the bronze capture the row was read from
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `data.sql` reads the `_latest` view of the default-rate table: it has no date column for
      `query()`. In every month here, the rate at X = 0.2 is a fifth of that at X = 1.
    cells:
      - |
        rates = data.sql("""
            SELECT year_vendor, month_vendor, hpim, papim, ppim, x_1, x_0_2
            FROM silver_neso_data_portal_orps_utilisation_reactive_default_latest
            ORDER BY year_vendor, month_vendor""")
        rates.tail()
      - |
        (rates.x_0_2 / rates.x_1).round(6).value_counts()
      - |
        import pandas as pd
        rates["month"] = pd.to_datetime(dict(year=rates.year_vendor, month=rates.month_vendor, day=1))
        rates.plot(x="month", y=["x_1", "x_0_2"], color=["#155A6E", "#C77E3C"], figsize=(8, 3.5),
                   xlabel="rate month, from NESO's Year and Month",
                   ylabel="default rate, £/MVArh");
    needs: a capture of the default payment rate file
    plot_alt: >-
      Monthly default rates at X = 1 and X = 0.2, £/MVArh, November 2007 to October
      2026. X = 1 stays between about 2 and 4 from 2009 to 2020, then climbs to 16.97 in October
      2022, falls back to about 4 to 6 and ends at 7.39. X = 0.2 is a fifth of it in every month.
  family:
    slug: obligatory-reactive-power-service-orps-utilisation
    members:
      - dataset: orps_utilisation_reactive
        differs: "Lead, lag, total by month, April 2020 to December 2024; long file bronze only"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=obligatory-reactive-power-service-orps-utilisation"
          - "GET https://api.neso.energy/dataset/7e142b03-8650-4f46-8420-7ce1e84e1e5b/resource/a61c6c26-62ec-41e1-ae25-ed95f4562274/download/reactive-utilisation-data-apr-2020-dec-2024.csv"
          - "GET https://api.neso.energy/dataset/7e142b03-8650-4f46-8420-7ce1e84e1e5b/resource/528b03d2-4008-4b65-a732-a001cd835a3b/download/reactive-utilisation-data.csv"
        caveat: "A blank may mean zero or not reported, and NESO's newer long file changes some values."
      - dataset: orps_utilisation_historic_reactive
        differs: "Lead, lag and total by month, October 2013 to March 2020"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=obligatory-reactive-power-service-orps-utilisation"
          - "GET https://api.neso.energy/dataset/7e142b03-8650-4f46-8420-7ce1e84e1e5b/resource/3ee65326-3729-421d-b667-b2164501e4a5/download/reactive-historical-data-apr-2013-to-mar-2020.csv"
        caveat: "NESO does not say what a dash cell means; one unit appears twice, with different values."
      - dataset: orps_utilisation_reactive_default
        differs: "Monthly inputs to NESO's default payment rate, and the two rates in £/MVArh"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=obligatory-reactive-power-service-orps-utilisation"
          - "GET https://api.neso.energy/dataset/7e142b03-8650-4f46-8420-7ce1e84e1e5b/resource/b00df5b1-4179-44e3-b556-28a836ad619f/download/reactive-default-payment-rate-oct-2026.csv"
        caveat: "NESO gives `HPIm`, `PAPIm` and `PPIm` only a pound sign, with no denominator."
  related:
    - {dataset: neso_data_portal/constraint-breakdown, note: "Daily voltage constraint costs, which NESO ties to reactive-power balance"}
---

# Obligatory Reactive Power Service (ORPS)

NESO's data on the **Obligatory Reactive Power Service (ORPS)**. ORPS is the provision of varying
reactive power output: at any given output, generators covered by the Grid Code can be asked to
produce or absorb reactive power to help manage system voltages near their point of connection, and
all such generators must have that capability. The package publishes the **utilisation** of the
service in **MVARh per balancing mechanism unit per month**, with lead and lag reported separately
(the vendor's historical dictionary reads leading as absorption and lagging as generation/export).
The utilisation history is split across three CSV generations: a historic wide table, a later wide
archive, and a current long table (see Families). A fourth CSV, the **default payment rate** table,
carries the monthly inputs and outputs NESO uses to price default (non-market) ORPS payments. Two
PDFs and one legacy workbook complete the package.

The question this package answers is who was asked to absorb or generate reactive power, and how
much, month by month; the payment-rate table says what that default service is paid. For modelling
it is voltage-management and cost context for the GB balancing mechanism
(@../../../20-domain/markets/gb-balancing-mechanism.md), keyed on BM unit identifiers
(@../../../20-domain/concepts/bm-units.md).

**gridflow's registry holds all three silver families** on open vendor questions, so no model consumes
them (gridflow `@.planning/v0.22-RESULTS.md` section AS-3b; RULINGS 738, 751, 752). The site page still
shows rows (ruling 66): each family carries its question as a caveat, and the chart, eight sample rows
and notebook come from the default payment-rate table, whose two utilisation siblings are too wide for
the page's column guide. This note records structure, row counts, clocks and the open questions. The
hold unit for the open questions is E-SEM (the registry froze the questions in unit v0.22-K-AS-3b).

- Vendor page: [ORPS utilisation](https://www.neso.energy/data-portal/obligatory-reactive-power-service-orps-utilisation)
- Attribution: Supported by National Energy SO Open Data

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: SER

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Historic Reactive Utilisation Data - Apr-2013 - March 2020 | CSV | upload | `3ee65326-3729-421d-b667-b2164501e4a5` |
| Reactive Default Payment Rate - Oct - 2026 | CSV | upload | `b00df5b1-4179-44e3-b556-28a836ad619f` |
| Reactive Utilisation Data - Apr-2020 - Dec-2024 | CSV | upload | `a61c6c26-62ec-41e1-ae25-ed95f4562274` |

- Downloads (the CKAN `last_modified` of each is its vintage clock, see Families):
  - Historic Reactive Utilisation Data: [reactive-historical-data-apr-2013-to-mar-2020.csv](https://api.neso.energy/dataset/7e142b03-8650-4f46-8420-7ce1e84e1e5b/resource/3ee65326-3729-421d-b667-b2164501e4a5/download/reactive-historical-data-apr-2013-to-mar-2020.csv) (CKAN `last_modified` 2021-07-26T11:19:03.229125).
  - Reactive Utilisation Data - Apr-2020 - Dec-2024: [reactive-utilisation-data-apr-2020-dec-2024.csv](https://api.neso.energy/dataset/7e142b03-8650-4f46-8420-7ce1e84e1e5b/resource/a61c6c26-62ec-41e1-ae25-ed95f4562274/download/reactive-utilisation-data-apr-2020-dec-2024.csv) (CKAN `last_modified` 2025-02-14T13:27:21.557694).
  - Reactive Default Payment Rate - Oct - 2026: [reactive-default-payment-rate-oct-2026.csv](https://api.neso.energy/dataset/7e142b03-8650-4f46-8420-7ce1e84e1e5b/resource/b00df5b1-4179-44e3-b556-28a836ad619f/download/reactive-default-payment-rate-oct-2026.csv) (CKAN `last_modified` 2026-09-17T07:44:25.572388).
- Captures (bronze, all 2026-10-08, one capture per resource; names are `raw_<stamp>_<resource id>_<sha-256 prefix>.csv`):
  - `raw_20261008T111555Z_3ee65326-3729-421d-b667-b2164501e4a5_af98c88f.csv`, 319,481 bytes, 295 rows, family `orps_utilisation_historic_reactive`.
  - `raw_20261008T111558Z_a61c6c26-62ec-41e1-ae25-ed95f4562274_b9e76522.csv`, 259,336 bytes, 243 rows, family `orps_utilisation_reactive`.
  - `raw_20261008T111605Z_b00df5b1-4179-44e3-b556-28a836ad619f_2830307a.csv`, 13,032 bytes, 228 rows, family `orps_utilisation_reactive_default`.
- The titles are vendor labels, not coverage statements. The historic resource is titled "Apr-2013 - March 2020", but its earliest monthly column is **October 2013**, so April 2013 is not covered by the capture (gridflow `@.planning/phases/v0.22-K-AS-3/K-AS-3-FACTS.md` section 5.1). "Oct - 2026" in the payment-rate title is a rate-effective label, not an issue date.
- All three CSVs begin with a byte-order mark that the CSV reader removes.

### DOC

| Resource | Format | Capture | Id |
|---|---|---|---|
| Obligatory Reactive Power Guide | PDF | upload | `0a74a789-d9fc-46cc-9554-e4e04c1e8014` |
| Reactive Default Payment Rate - Oct - 2026 | PDF | upload | `e2e6f74c-ebca-48b3-b2ae-e4652d296dca` |

- Downloads:
  - Obligatory Reactive Power Guide: [obligatory-reactive-power-guide.pdf](https://api.neso.energy/dataset/7e142b03-8650-4f46-8420-7ce1e84e1e5b/resource/0a74a789-d9fc-46cc-9554-e4e04c1e8014/download/obligatory-reactive-power-guide.pdf) (CKAN `last_modified` 2019-12-13T14:09:44.843039). The vendor describes it as a summary of what ORPS is, how it is dispatched, the technical requirements to provide it, how it is procured and the payment arrangements.
  - Reactive Default Payment Rate - Oct - 2026: [reactive-default-payment-rate-oct-2026.pdf](https://api.neso.energy/dataset/7e142b03-8650-4f46-8420-7ce1e84e1e5b/resource/e2e6f74c-ebca-48b3-b2ae-e4652d296dca/download/reactive-default-payment-rate-oct-2026.pdf) (CKAN `last_modified` 2026-09-17T07:46:20.354202). The vendor describes it as the methodology used to calculate ORPS payment rates; it is the companion to the payment-rate CSV.
- Captured: `raw_20261008T111551Z_0a74a789-d9fc-46cc-9554-e4e04c1e8014_d1f392bf.pdf` (281,948 bytes) and `raw_20261008T111549Z_e2e6f74c-ebca-48b3-b2ae-e4652d296dca_7208ea34.pdf` (619,621 bytes), family `orps_utilisation_files`. Catalogue only: no silver output. NESO's default-payment guidance (document 84286) is the evidence behind the units of the rate columns (see `orps_utilisation_reactive_default`).

### HOLD

| Resource | Format | Capture | Id | Reason (unit) |
|---|---|---|---|---|
| Reactive Utilisation Data | CSV | upload | `528b03d2-4008-4b65-a732-a001cd835a3b` | TODO: ORPS-REACTIVE-LONG-DUPLICATE — the current long table repeats one complete row twice (one complete row is repeated twice; identity not named, as the long table is bronze only), so no key passes the duplicate guard (RULINGS 538); publication defect or two distinct utilisations? Re-disposition only after a corrected NESO upload (a new last_modified) or a vendor identity column (v0.22-K-AS-3b) |
| Reactive Utilisation-Nov-2021 | XLSX | upload | `d91e4fd2-1f27-4d0b-8473-b4b19af7f3dc` | TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) |
| ↳ Oct00-Mar05 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Apr05-Sep06 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Oct06-Mar07 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Apr07-Sep07 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Oct07-Mar08 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Apr08-Sep08 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Oct08-Mar09 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Apr09-Sep09 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Oct09-Mar10 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Apr10-Sep10 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Oct10-Mar11 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Apr11-Sep11 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Oct11-Mar12 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Apr12-Sep12 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Oct12-Mar13 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Apr13-Sep13 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Oct13-Mar14 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Apr14-Sep14 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Oct14-Mar15 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Apr15-Sep15 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Oct15-Mar16 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Apr16-Sep16 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Oct16-Mar17 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Apr17-Sep17 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Oct17-Mar18 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Apr18 - Sep 18 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Oct 18 - Mar19 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Apr 19 - Sep 19 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Oct 19 - Mar 20 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Apr 20 - Sep 20 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Oct 20 - Mar 21 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Apr 21 - Sep 21 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |
| ↳ Oct 21 - Mar 22 | — | — | HOLD: TODO: ORPS-WORKBOOK-LAYOUT — merged monthly headers, notes and totals; the ADR-037 single-block XLSX reader cannot read a sheet faithfully; re-disposition only after a reader unit with per-sheet flattened headers and verified table boundaries (v0.22-K-AS-3b) | — |

- Downloads:
  - Reactive Utilisation Data (current long table): [reactive-utilisation-data.csv](https://api.neso.energy/dataset/7e142b03-8650-4f46-8420-7ce1e84e1e5b/resource/528b03d2-4008-4b65-a732-a001cd835a3b/download/reactive-utilisation-data.csv) (CKAN `last_modified` 2026-10-07T15:58:09.723806 at capture). Captured as `raw_20261008T111602Z_528b03d2-4008-4b65-a732-a001cd835a3b_e6a485d3.csv`, 852,298 bytes, 19,130 data rows, header `Company,Unit,Default/Market,Location,Month-Year,LEAD,LAG,TOTAL`. It is a **resource-level HOLD inside the recorded family `orps_utilisation_reactive`**: it is bronze only, the record's single epoch is the wide archive header, and no silver row comes from it. The registry precedent is the GTMA trades resource (unit v0.22-K-TRD).
  - Reactive Utilisation-Nov-2021 (legacy workbook): [reactive-utilisation-nov-2021.xlsx](https://api.neso.energy/dataset/7e142b03-8650-4f46-8420-7ce1e84e1e5b/resource/d91e4fd2-1f27-4d0b-8473-b4b19af7f3dc/download/reactive-utilisation-nov-2021.xlsx) (CKAN `last_modified` 2022-01-11T10:51:29.866177). Captured as `raw_20261008T111546Z_d91e4fd2-1f27-4d0b-8473-b4b19af7f3dc_5a011509.xlsx`, 2,448,584 bytes, family `orps_utilisation_files`.
- The `↳` rows are the workbook's 33 sheets (named by period, running from `Oct00-Mar05` through `Oct 21 - Mar 22`; TODO: verify the per-sheet period granularity). Two sheet names carry trailing spaces in the vendor workbook (`Apr12-Sep12 ` and `Oct 20 - Mar 21 `) and are registered byte-equal. The workbook adds pre-CSV years from October 2000 and overlaps the CSV-era span. Its sheet labels do not prove the final populated month. The workbook's layout (merged monthly headers, notes and totals, unresolved table boundaries) is what the ADR-037 single-block reader cannot read faithfully, hence HOLD. No `orps_utilisation_workbook` family or record exists; a later reader unit would need per-sheet flattened headers and verified table boundaries.
- Both HOLD reasons are vendor-data or layout questions, not capture failures: no capture has failed and no ADR-040 adjudication applies.

## Families

### `orps_utilisation_files`

- Kind: files · archetype: SER · refresh: monthly · empty allowed: no
- files: catalogue only

This family captures the two PDFs (DOC) and the legacy workbook (HOLD) listed above. It has no
silver output and no clocks beyond each capture's CKAN `last_modified`.

### `orps_utilisation_historic_reactive`

- Kind: tabular · archetype: SER · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Company | `company` | string | — | no | — | — |
| Unit | `unit` | string | — | no | — | — |
| Default/Market | `default_market` | string | — | no | — | — |
| Location | `location` | string | — | no | — | — |
| Oct 13 - LEAD | `oct_13_lead` | string | — | yes | — | MVAr |
| Oct 13 - LAG | `oct_13_lag` | string | — | yes | — | MVAr |
| Oct 13 - TOTAL | `oct_13_total` | string | — | yes | — | MVAr |
| Nov 13 - LEAD | `nov_13_lead` | string | — | yes | — | MVAr |
| Nov 13 - LAG | `nov_13_lag` | string | — | yes | — | MVAr |
| Nov 13 - TOTAL | `nov_13_total` | string | — | yes | — | MVAr |
| Dec 13 - LEAD | `dec_13_lead` | string | — | yes | — | MVAr |
| Dec 13 -LAG | `dec_13_lag` | string | — | yes | — | MVAr |
| Dec 13 - TOTAL | `dec_13_total` | string | — | yes | — | MVAr |
| Jan 14 - LEAD | `jan_14_lead` | string | — | yes | — | MVAr |
| Jan 14 - LAG | `jan_14_lag` | string | — | yes | — | MVAr |
| Jan 14 - TOTAL | `jan_14_total` | string | — | yes | — | MVAr |
| Feb 14 - LEAD | `feb_14_lead` | string | — | yes | — | MVAr |
| Feb 14- LAG | `feb_14_lag` | string | — | yes | — | MVAr |
| Feb 14 - TOTAL | `feb_14_total` | string | — | yes | — | MVAr |
| Mar 14 - LEAD | `mar_14_lead` | string | — | yes | — | MVAr |
| Mar 14 - LAG | `mar_14_lag` | string | — | yes | — | MVAr |
| Mar 14 - TOTAL | `mar_14_total` | string | — | yes | — | MVAr |
| Apr 14 - LEAD | `apr_14_lead` | string | — | yes | — | MVAr |
| Apr 14 - LAG | `apr_14_lag` | string | — | yes | — | MVAr |
| Apr 14 - TOTAL | `apr_14_total` | string | — | yes | — | MVAr |
| May 14 - LEAD | `may_14_lead` | string | — | yes | — | MVAr |
| May 14 - LAG | `may_14_lag` | string | — | yes | — | MVAr |
| May 14 - TOTAL | `may_14_total` | string | — | yes | — | MVAr |
| Jun 14 - LEAD | `jun_14_lead` | string | — | yes | — | MVAr |
| Jun 14 -LAG | `jun_14_lag` | string | — | yes | — | MVAr |
| Jun 14 - TOTAL | `jun_14_total` | string | — | yes | — | MVAr |
| Jul 14 - LEAD | `jul_14_lead` | string | — | yes | — | MVAr |
| Jul 14 - LAG | `jul_14_lag` | string | — | yes | — | MVAr |
| Jul 14 - TOTAL | `jul_14_total` | string | — | yes | — | MVAr |
| Aug 14 - LEAD | `aug_14_lead` | string | — | yes | — | MVAr |
| Aug 14 - LAG | `aug_14_lag` | string | — | yes | — | MVAr |
| Aug 14 - TOTAL | `aug_14_total` | string | — | yes | — | MVAr |
| Sep 14- LEAD | `sep_14_lead` | string | — | yes | — | MVAr |
| Sep 14 - LAG | `sep_14_lag` | string | — | yes | — | MVAr |
| Sep 14- TOTAL | `sep_14_total` | string | — | yes | — | MVAr |
| Oct 14- LEAD | `oct_14_lead` | string | — | yes | — | MVAr |
| Oct 14- LAG | `oct_14_lag` | string | — | yes | — | MVAr |
| Oct 14 - TOTAL | `oct_14_total` | string | — | yes | — | MVAr |
| Nov 14 - LEAD | `nov_14_lead` | string | — | yes | — | MVAr |
| Nov 14- LAG | `nov_14_lag` | string | — | yes | — | MVAr |
| Nov 14- TOTAL | `nov_14_total` | string | — | yes | — | MVAr |
| Dec 14 - LEAD | `dec_14_lead` | string | — | yes | — | MVAr |
| Dec 14 -LAG | `dec_14_lag` | string | — | yes | — | MVAr |
| Dec 14 - TOTAL | `dec_14_total` | string | — | yes | — | MVAr |
| Jan 15 - LEAD | `jan_15_lead` | string | — | yes | — | MVAr |
| Jan 15 - LAG | `jan_15_lag` | string | — | yes | — | MVAr |
| Jan 15 - TOTAL | `jan_15_total` | string | — | yes | — | MVAr |
| Feb 15 - LEAD | `feb_15_lead` | string | — | yes | — | MVAr |
| Feb 15 - LAG | `feb_15_lag` | string | — | yes | — | MVAr |
| Feb 15 - TOTAL | `feb_15_total` | string | — | yes | — | MVAr |
| Mar 15- LEAD | `mar_15_lead` | string | — | yes | — | MVAr |
| Mar 15 - LAG | `mar_15_lag` | string | — | yes | — | MVAr |
| Mar 15- TOTAL | `mar_15_total` | string | — | yes | — | MVAr |
| Apr 15- LEAD | `apr_15_lead` | string | — | yes | — | MVAr |
| Apr 15- LAG | `apr_15_lag` | string | — | yes | — | MVAr |
| Apr 15 - TOTAL | `apr_15_total` | string | — | yes | — | MVAr |
| May 15 - LEAD | `may_15_lead` | string | — | yes | — | MVAr |
| May 15- LAG | `may_15_lag` | string | — | yes | — | MVAr |
| May 15- TOTAL | `may_15_total` | string | — | yes | — | MVAr |
| Jun 15 - LEAD | `jun_15_lead` | string | — | yes | — | MVAr |
| Jun 15 -LAG | `jun_15_lag` | string | — | yes | — | MVAr |
| Jun 15 - TOTAL | `jun_15_total` | string | — | yes | — | MVAr |
| Jul 15 - LEAD | `jul_15_lead` | string | — | yes | — | MVAr |
| Jul 15 - LAG | `jul_15_lag` | string | — | yes | — | MVAr |
| Jul 15 - TOTAL | `jul_15_total` | string | — | yes | — | MVAr |
| Aug 15 - LEAD | `aug_15_lead` | string | — | yes | — | MVAr |
| Aug 15 - LAG | `aug_15_lag` | string | — | yes | — | MVAr |
| Aug 15 - TOTAL | `aug_15_total` | string | — | yes | — | MVAr |
| Sep 15- LEAD | `sep_15_lead` | string | — | yes | — | MVAr |
| Sep 15 - LAG | `sep_15_lag` | string | — | yes | — | MVAr |
| Sep 15- TOTAL | `sep_15_total` | string | — | yes | — | MVAr |
| Oct 15- LEAD | `oct_15_lead` | string | — | yes | — | MVAr |
| Oct 15- LAG | `oct_15_lag` | string | — | yes | — | MVAr |
| Oct 15 - TOTAL | `oct_15_total` | string | — | yes | — | MVAr |
| Nov 15 - LEAD | `nov_15_lead` | string | — | yes | — | MVAr |
| Nov 15- LAG | `nov_15_lag` | string | — | yes | — | MVAr |
| Nov 15- TOTAL | `nov_15_total` | string | — | yes | — | MVAr |
| Dec 15 - LEAD | `dec_15_lead` | string | — | yes | — | MVAr |
| Dec 15 -LAG | `dec_15_lag` | string | — | yes | — | MVAr |
| Dec 15 - TOTAL | `dec_15_total` | string | — | yes | — | MVAr |
| Jan 16 - LEAD | `jan_16_lead` | string | — | yes | — | MVAr |
| Jan 16 - LAG | `jan_16_lag` | string | — | yes | — | MVAr |
| Jan 16 - TOTAL | `jan_16_total` | string | — | yes | — | MVAr |
| Feb 16 - LEAD | `feb_16_lead` | string | — | yes | — | MVAr |
| Feb 16- LAG | `feb_16_lag` | string | — | yes | — | MVAr |
| Feb 16 - TOTAL | `feb_16_total` | string | — | yes | — | MVAr |
| Mar 16 - LEAD | `mar_16_lead` | string | — | yes | — | MVAr |
| Mar 16 - LAG | `mar_16_lag` | string | — | yes | — | MVAr |
| Mar 16 - TOTAL | `mar_16_total` | string | — | yes | — | MVAr |
| Apr 16 - LEAD | `apr_16_lead` | string | — | yes | — | MVAr |
| Apr 16 - LAG | `apr_16_lag` | string | — | yes | — | MVAr |
| Apr 16- TOTAL | `apr_16_total` | string | — | yes | — | MVAr |
| May 16 - LEAD | `may_16_lead` | string | — | yes | — | MVAr |
| May 16 - LAG | `may_16_lag` | string | — | yes | — | MVAr |
| May 16 - TOTAL | `may_16_total` | string | — | yes | — | MVAr |
| Jun 16 - LEAD | `jun_16_lead` | string | — | yes | — | MVAr |
| Jun 16 -LAG | `jun_16_lag` | string | — | yes | — | MVAr |
| Jun 16- TOTAL | `jun_16_total` | string | — | yes | — | MVAr |
| Jul 16 - LEAD | `jul_16_lead` | string | — | yes | — | MVAr |
| Jul 16 - LAG | `jul_16_lag` | string | — | yes | — | MVAr |
| Jul 16 - TOTAL | `jul_16_total` | string | — | yes | — | MVAr |
| Aug 16 - LEAD | `aug_16_lead` | string | — | yes | — | MVAr |
| Aug 16- LAG | `aug_16_lag` | string | — | yes | — | MVAr |
| Aug 16 - TOTAL | `aug_16_total` | string | — | yes | — | MVAr |
| Sep 16 - LEAD | `sep_16_lead` | string | — | yes | — | MVAr |
| Sep 16 - LAG | `sep_16_lag` | string | — | yes | — | MVAr |
| Sep 16 - TOTAL | `sep_16_total` | string | — | yes | — | MVAr |
| Oct 16 - LEAD | `oct_16_lead` | string | — | yes | — | MVAr |
| Oct 16 - LAG | `oct_16_lag` | string | — | yes | — | MVAr |
| Oct 16 - TOTAL | `oct_16_total` | string | — | yes | — | MVAr |
| Nov 16 - LEAD | `nov_16_lead` | string | — | yes | — | MVAr |
| Nov 16 - LAG | `nov_16_lag` | string | — | yes | — | MVAr |
| Nov 16 - TOTAL | `nov_16_total` | string | — | yes | — | MVAr |
| Dec 16 - LEAD | `dec_16_lead` | string | — | yes | — | MVAr |
| Dec 16 -LAG | `dec_16_lag` | string | — | yes | — | MVAr |
| Dec 16 - TOTAL | `dec_16_total` | string | — | yes | — | MVAr |
| Jan 17 - LEAD | `jan_17_lead` | string | — | yes | — | MVAr |
| Jan 17 - LAG | `jan_17_lag` | string | — | yes | — | MVAr |
| Jan 17 - TOTAL | `jan_17_total` | string | — | yes | — | MVAr |
| Feb 17 - LEAD | `feb_17_lead` | string | — | yes | — | MVAr |
| Feb 17 - LAG | `feb_17_lag` | string | — | yes | — | MVAr |
| Feb 17 - TOTAL | `feb_17_total` | string | — | yes | — | MVAr |
| Mar 17- LEAD | `mar_17_lead` | string | — | yes | — | MVAr |
| Mar 17 - LAG | `mar_17_lag` | string | — | yes | — | MVAr |
| Mar 17 - TOTAL | `mar_17_total` | string | — | yes | — | MVAr |
| Apr 17 - LEAD | `apr_17_lead` | string | — | yes | — | MVAr |
| Apr 17 - LAG | `apr_17_lag` | string | — | yes | — | MVAr |
| Apr 17 - TOTAL | `apr_17_total` | string | — | yes | — | MVAr |
| May 17 - LEAD | `may_17_lead` | string | — | yes | — | MVAr |
| May 17 - LAG | `may_17_lag` | string | — | yes | — | MVAr |
| May 17 - TOTAL | `may_17_total` | string | — | yes | — | MVAr |
| Jun 17 - LEAD | `jun_17_lead` | string | — | yes | — | MVAr |
| Jun 17 -LAG | `jun_17_lag` | string | — | yes | — | MVAr |
| Jun 17 - TOTAL | `jun_17_total` | string | — | yes | — | MVAr |
| Jul 17 - LEAD | `jul_17_lead` | string | — | yes | — | MVAr |
| Jul 17 - LAG | `jul_17_lag` | string | — | yes | — | MVAr |
| Jul 17- TOTAL | `jul_17_total` | string | — | yes | — | MVAr |
| Aug 17 - LEAD | `aug_17_lead` | string | — | yes | — | MVAr |
| Aug 17 - LAG | `aug_17_lag` | string | — | yes | — | MVAr |
| Aug 17 - TOTAL | `aug_17_total` | string | — | yes | — | MVAr |
| Sep 17- LEAD | `sep_17_lead` | string | — | yes | — | MVAr |
| Sep 17 - LAG | `sep_17_lag` | string | — | yes | — | MVAr |
| Sep 17 - TOTAL | `sep_17_total` | string | — | yes | — | MVAr |
| Oct 17 - LEAD | `oct_17_lead` | string | — | yes | — | MVAr |
| Oct 17 - LAG | `oct_17_lag` | string | — | yes | — | MVAr |
| Oct 17 - TOTAL | `oct_17_total` | string | — | yes | — | MVAr |
| Nov 17 - LEAD | `nov_17_lead` | string | — | yes | — | MVAr |
| Nov 17 - LAG | `nov_17_lag` | string | — | yes | — | MVAr |
| Nov 17 - TOTAL | `nov_17_total` | string | — | yes | — | MVAr |
| Dec 17 - LEAD | `dec_17_lead` | string | — | yes | — | MVAr |
| Dec 17 -LAG | `dec_17_lag` | string | — | yes | — | MVAr |
| Dec 17 - TOTAL | `dec_17_total` | string | — | yes | — | MVAr |
| Jan 18 - LEAD | `jan_18_lead` | string | — | yes | — | MVAr |
| Jan 18 - LAG | `jan_18_lag` | string | — | yes | — | MVAr |
| Jan 18 - TOTAL | `jan_18_total` | string | — | yes | — | MVAr |
| Feb 18 - LEAD | `feb_18_lead` | string | — | yes | — | MVAr |
| Feb 18 - LAG | `feb_18_lag` | string | — | yes | — | MVAr |
| Feb 18 - TOTAL | `feb_18_total` | string | — | yes | — | MVAr |
| Mar 18 - LEAD | `mar_18_lead` | string | — | yes | — | MVAr |
| Mar 18 - LAG | `mar_18_lag` | string | — | yes | — | MVAr |
| Mar 18 - TOTAL | `mar_18_total` | string | — | yes | — | MVAr |
| Apr 18 - LEAD | `apr_18_lead` | string | — | yes | — | MVAr |
| Apr 18 - LAG | `apr_18_lag` | string | — | yes | — | MVAr |
| Apr 18 - TOTAL | `apr_18_total` | string | — | yes | — | MVAr |
| May 18 - LEAD | `may_18_lead` | string | — | yes | — | MVAr |
| May 18 - LAG | `may_18_lag` | string | — | yes | — | MVAr |
| May 18 - TOTAL | `may_18_total` | string | — | yes | — | MVAr |
| Jun 18 - LEAD | `jun_18_lead` | string | — | yes | — | MVAr |
| Jun 18 -LAG | `jun_18_lag` | string | — | yes | — | MVAr |
| Jun 18 - TOTAL | `jun_18_total` | string | — | yes | — | MVAr |
| Jul 18 - LEAD | `jul_18_lead` | string | — | yes | — | MVAr |
| Jul 18 - LAG | `jul_18_lag` | string | — | yes | — | MVAr |
| Jul 18 - TOTAL | `jul_18_total` | string | — | yes | — | MVAr |
| Aug 18 - LEAD | `aug_18_lead` | string | — | yes | — | MVAr |
| Aug 18 - LAG | `aug_18_lag` | string | — | yes | — | MVAr |
| Aug 18 - TOTAL | `aug_18_total` | string | — | yes | — | MVAr |
| Sep 18 - LEAD | `sep_18_lead` | string | — | yes | — | MVAr |
| Sep 18 - LAG | `sep_18_lag` | string | — | yes | — | MVAr |
| Sep 18 - TOTAL | `sep_18_total` | string | — | yes | — | MVAr |
| Oct 18 - LEAD | `oct_18_lead` | string | — | yes | — | MVAr |
| Oct 18 - LAG | `oct_18_lag` | string | — | yes | — | MVAr |
| Oct 18 - TOTAL | `oct_18_total` | string | — | yes | — | MVAr |
| Nov 18 - LEAD | `nov_18_lead` | string | — | yes | — | MVAr |
| Nov 18 - LAG | `nov_18_lag` | string | — | yes | — | MVAr |
| Nov 18 - TOTAL | `nov_18_total` | string | — | yes | — | MVAr |
| Dec 18 - LEAD | `dec_18_lead` | string | — | yes | — | MVAr |
| Dec 18 -LAG | `dec_18_lag` | string | — | yes | — | MVAr |
| Dec 18 - TOTAL | `dec_18_total` | string | — | yes | — | MVAr |
| Jan 19 - LEAD | `jan_19_lead` | string | — | yes | — | MVAr |
| Jan 19 - LAG | `jan_19_lag` | string | — | yes | — | MVAr |
| Jan 19 - TOTAL | `jan_19_total` | string | — | yes | — | MVAr |
| Feb 19 - LEAD | `feb_19_lead` | string | — | yes | — | MVAr |
| Feb 19 - LAG | `feb_19_lag` | string | — | yes | — | MVAr |
| Feb 19- TOTAL | `feb_19_total` | string | — | yes | — | MVAr |
| Mar 19 - LEAD | `mar_19_lead` | string | — | yes | — | MVAr |
| Mar 19 - LAG | `mar_19_lag` | string | — | yes | — | MVAr |
| Mar 19 - TOTAL | `mar_19_total` | string | — | yes | — | MVAr |
| Apr 19 - LEAD | `apr_19_lead` | string | — | yes | — | MVAr |
| Apr 19 -LAG | `apr_19_lag` | string | — | yes | — | MVAr |
| Apr 19- TOTAL | `apr_19_total` | string | — | yes | — | MVAr |
| May 19 - LEAD | `may_19_lead` | string | — | yes | — | MVAr |
| May 19 -LAG | `may_19_lag` | string | — | yes | — | MVAr |
| May 19- TOTAL | `may_19_total` | string | — | yes | — | MVAr |
| Jun 19 - LEAD | `jun_19_lead` | string | — | yes | — | MVAr |
| Jun 19 -LAG | `jun_19_lag` | string | — | yes | — | MVAr |
| Jun 19- TOTAL | `jun_19_total` | string | — | yes | — | MVAr |
| Jul 19 - LEAD | `jul_19_lead` | string | — | yes | — | MVAr |
| Jul 19 -LAG | `jul_19_lag` | string | — | yes | — | MVAr |
| Jul 19- TOTAL | `jul_19_total` | string | — | yes | — | MVAr |
| Aug 19 - LEAD | `aug_19_lead` | string | — | yes | — | MVAr |
| Aug 19 -LAG | `aug_19_lag` | string | — | yes | — | MVAr |
| Aug 19- TOTAL | `aug_19_total` | string | — | yes | — | MVAr |
| Sep 19 - LEAD | `sep_19_lead` | string | — | yes | — | MVAr |
| Sep 19 -LAG | `sep_19_lag` | string | — | yes | — | MVAr |
| Sep 19- TOTAL | `sep_19_total` | string | — | yes | — | MVAr |
| Oct 19 -LEAD | `oct_19_lead` | string | — | yes | — | MVAr |
| Oct 19 - LAG | `oct_19_lag` | string | — | yes | — | MVAr |
| Oct -19 TOTAL | `oct_19_total` | string | — | yes | — | MVAr |
| Nov 19 -LEAD | `nov_19_lead` | string | — | yes | — | MVAr |
| Nov 19 - LAG | `nov_19_lag` | string | — | yes | — | MVAr |
| Nov -19 TOTAL | `nov_19_total` | string | — | yes | — | MVAr |
| Dec 19 -LEAD | `dec_19_lead` | string | — | yes | — | MVAr |
| Dec 19 - LAG | `dec_19_lag` | string | — | yes | — | MVAr |
| Dec 19 - TOTAL | `dec_19_total` | string | — | yes | — | MVAr |
| Jan 20 -LEAD | `jan_20_lead` | string | — | yes | — | MVAr |
| Jan 20 - LAG | `jan_20_lag` | string | — | yes | — | MVAr |
| Jan 20 - TOTAL | `jan_20_total` | string | — | yes | — | MVAr |
| Feb 20 -LEAD | `feb_20_lead` | string | — | yes | — | MVAr |
| Feb 20 - LAG | `feb_20_lag` | string | — | yes | — | MVAr |
| Feb 20 - TOTAL | `feb_20_total` | string | — | yes | — | MVAr |
| Mar 20 -LEAD | `mar_20_lead` | string | — | yes | — | MVAr |
| Mar 20 - LAG | `mar_20_lag` | string | — | yes | — | MVAr |
| Mar 20 - TOTAL | `mar_20_total` | string | — | yes | — | MVAr |

- Entity key: `company`, `unit`, `default_market`, `location`, `oct_13_lead`, `oct_13_lag`, `oct_13_total`, `nov_13_lead`, `nov_13_lag`, `nov_13_total`, `dec_13_lead`, `dec_13_lag`, `dec_13_total`, `jan_14_lead`, `jan_14_lag`, `jan_14_total`, `feb_14_lead`, `feb_14_lag`, `feb_14_total`, `mar_14_lead`, `mar_14_lag`, `mar_14_total`, `apr_14_lead`, `apr_14_lag`, `apr_14_total`, `may_14_lead`, `may_14_lag`, `may_14_total`, `jun_14_lead`, `jun_14_lag`, `jun_14_total`, `jul_14_lead`, `jul_14_lag`, `jul_14_total`, `aug_14_lead`, `aug_14_lag`, `aug_14_total`, `sep_14_lead`, `sep_14_lag`, `sep_14_total`, `oct_14_lead`, `oct_14_lag`, `oct_14_total`, `nov_14_lead`, `nov_14_lag`, `nov_14_total`, `dec_14_lead`, `dec_14_lag`, `dec_14_total`, `jan_15_lead`, `jan_15_lag`, `jan_15_total`, `feb_15_lead`, `feb_15_lag`, `feb_15_total`, `mar_15_lead`, `mar_15_lag`, `mar_15_total`, `apr_15_lead`, `apr_15_lag`, `apr_15_total`, `may_15_lead`, `may_15_lag`, `may_15_total`, `jun_15_lead`, `jun_15_lag`, `jun_15_total`, `jul_15_lead`, `jul_15_lag`, `jul_15_total`, `aug_15_lead`, `aug_15_lag`, `aug_15_total`, `sep_15_lead`, `sep_15_lag`, `sep_15_total`, `oct_15_lead`, `oct_15_lag`, `oct_15_total`, `nov_15_lead`, `nov_15_lag`, `nov_15_total`, `dec_15_lead`, `dec_15_lag`, `dec_15_total`, `jan_16_lead`, `jan_16_lag`, `jan_16_total`, `feb_16_lead`, `feb_16_lag`, `feb_16_total`, `mar_16_lead`, `mar_16_lag`, `mar_16_total`, `apr_16_lead`, `apr_16_lag`, `apr_16_total`, `may_16_lead`, `may_16_lag`, `may_16_total`, `jun_16_lead`, `jun_16_lag`, `jun_16_total`, `jul_16_lead`, `jul_16_lag`, `jul_16_total`, `aug_16_lead`, `aug_16_lag`, `aug_16_total`, `sep_16_lead`, `sep_16_lag`, `sep_16_total`, `oct_16_lead`, `oct_16_lag`, `oct_16_total`, `nov_16_lead`, `nov_16_lag`, `nov_16_total`, `dec_16_lead`, `dec_16_lag`, `dec_16_total`, `jan_17_lead`, `jan_17_lag`, `jan_17_total`, `feb_17_lead`, `feb_17_lag`, `feb_17_total`, `mar_17_lead`, `mar_17_lag`, `mar_17_total`, `apr_17_lead`, `apr_17_lag`, `apr_17_total`, `may_17_lead`, `may_17_lag`, `may_17_total`, `jun_17_lead`, `jun_17_lag`, `jun_17_total`, `jul_17_lead`, `jul_17_lag`, `jul_17_total`, `aug_17_lead`, `aug_17_lag`, `aug_17_total`, `sep_17_lead`, `sep_17_lag`, `sep_17_total`, `oct_17_lead`, `oct_17_lag`, `oct_17_total`, `nov_17_lead`, `nov_17_lag`, `nov_17_total`, `dec_17_lead`, `dec_17_lag`, `dec_17_total`, `jan_18_lead`, `jan_18_lag`, `jan_18_total`, `feb_18_lead`, `feb_18_lag`, `feb_18_total`, `mar_18_lead`, `mar_18_lag`, `mar_18_total`, `apr_18_lead`, `apr_18_lag`, `apr_18_total`, `may_18_lead`, `may_18_lag`, `may_18_total`, `jun_18_lead`, `jun_18_lag`, `jun_18_total`, `jul_18_lead`, `jul_18_lag`, `jul_18_total`, `aug_18_lead`, `aug_18_lag`, `aug_18_total`, `sep_18_lead`, `sep_18_lag`, `sep_18_total`, `oct_18_lead`, `oct_18_lag`, `oct_18_total`, `nov_18_lead`, `nov_18_lag`, `nov_18_total`, `dec_18_lead`, `dec_18_lag`, `dec_18_total`, `jan_19_lead`, `jan_19_lag`, `jan_19_total`, `feb_19_lead`, `feb_19_lag`, `feb_19_total`, `mar_19_lead`, `mar_19_lag`, `mar_19_total`, `apr_19_lead`, `apr_19_lag`, `apr_19_total`, `may_19_lead`, `may_19_lag`, `may_19_total`, `jun_19_lead`, `jun_19_lag`, `jun_19_total`, `jul_19_lead`, `jul_19_lag`, `jul_19_total`, `aug_19_lead`, `aug_19_lag`, `aug_19_total`, `sep_19_lead`, `sep_19_lag`, `sep_19_total`, `oct_19_lead`, `oct_19_lag`, `oct_19_total`, `nov_19_lead`, `nov_19_lag`, `nov_19_total`, `dec_19_lead`, `dec_19_lag`, `dec_19_total`, `jan_20_lead`, `jan_20_lag`, `jan_20_total`, `feb_20_lead`, `feb_20_lag`, `feb_20_total`, `mar_20_lead`, `mar_20_lag`, `mar_20_total`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Status: held in gridflow (E-SEM). 295 silver rows, 238 vendor columns plus the eight lineage columns
below. The site page names its question as a caveat; it shows no rows of this table, which is too wide
for the column guide.**

One CSV (`Historic Reactive Utilisation Data`), one row per balancing mechanism unit, wide: four
identity columns (`Company`, `Unit`, `Default/Market`, `Location`) followed by **LEAD / LAG / TOTAL**
triplets for each month. There are 78 months, **Oct 2013 to Mar 2020** (234 value columns). The
vendor's headers are irregular (inconsistent spacing around the hyphen, forms such as
`Oct -19 TOTAL`); the record freezes the headers exactly as the CSV reader returns them (BOM removed,
header-edge whitespace stripped) and the silver names follow a lowercase-underscore rule.
`Default/Market` is the procurement route: `D` is ORPS/default procurement and `M` is the Enhanced
Reactive Power Service market route (vendor dictionary).

**Value columns are stored as `string`.** The CSV carries comma-grouped numerals (20,950 cells), blank
cells (11,418) and 32 padded `-` tokens, so a numeric cast is not faithful and no cleaning rule is
evidenced. gridflow applies no comma strip, no trim and no token map, and blanks stay null.

**Unit.** The package text states utilisation in **MVARh per BM unit per month**. This family's
vendor dictionary labels the value columns **MVAr**, which conflicts with that statement. The
conflict is recorded rather than resolved. `TODO: verify` with NESO which label is right; until
then read the columns as monthly accumulated utilisation (MVARh) only on the strength of the package
text, never as instantaneous power.

**Entity key.** The four natural identity columns repeat (one four-field identity appears at
physical rows 181 and 277 with 234 differing value columns; identity not named in this note), so the key above is **all 238 silver
columns**. That is a duplicate guard, not a vendor identity.

**Sentinels.** None established. The padded `-` is **not** treated as zero, missing or not
applicable (hold question in Holds). No `NA`/`N/A`, percent-bearing cells or `-1` sentinel cells
occur.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured file: `2021-07-26T11:19:03.229125Z` for the single capture. This
   is the portal's file-modification instant, not proof of when each month's figure was first
   available.
2. **Event time (temporal recipe `none`).** The month each value describes lives in the column
   header, not in a row date, so gridflow derives no event time. `timestamp_utc` (and `event_time`)
   is the **capture time**, `2026-10-08T11:15:55.409392Z`. It carries no market meaning; do not use
   it as an event clock.

Silver carries eight lineage columns beyond the vendor columns: `timestamp_utc`, `published_at`,
`bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`,
`dataset_version` (`1+e1`, record version 1 epoch 1; all timestamps tz-aware UTC).

### `orps_utilisation_reactive`

- Kind: tabular · archetype: SER · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| id | `id` | string | — | yes | — | — |
| Company | `company` | string | — | no | — | String |
| Unit | `unit` | string | — | no | — | String |
| Default/Market | `default_market` | string | — | no | — | String |
| Location | `location` | string | — | no | — | String |
| Apr 20 -LEAD | `apr_20_lead` | float64 | — | yes | — | — |
| Apr 20 - LAG | `apr_20_lag` | float64 | — | yes | — | — |
| Apr 20 - TOTAL | `apr_20_total` | float64 | — | yes | — | — |
| May 20 -LEAD | `may_20_lead` | float64 | — | yes | — | — |
| May 20 - LAG | `may_20_lag` | float64 | — | yes | — | — |
| May 20 - TOTAL | `may_20_total` | float64 | — | yes | — | — |
| Jun 20 -LEAD | `jun_20_lead` | float64 | — | yes | — | — |
| Jun 20 - LAG | `jun_20_lag` | float64 | — | yes | — | — |
| Jun 20 - TOTAL | `jun_20_total` | float64 | — | yes | — | — |
| Jul 20 -LEAD | `jul_20_lead` | float64 | — | yes | — | — |
| Jul 20 - LAG | `jul_20_lag` | float64 | — | yes | — | — |
| Jul 20 - TOTAL | `jul_20_total` | float64 | — | yes | — | — |
| Aug 20 -LEAD | `aug_20_lead` | float64 | — | yes | — | — |
| Aug 20 - LAG | `aug_20_lag` | float64 | — | yes | — | — |
| Aug 20 - TOTAL | `aug_20_total` | float64 | — | yes | — | — |
| Sep 20 -LEAD | `sep_20_lead` | float64 | — | yes | — | — |
| Sep 20 - LAG | `sep_20_lag` | float64 | — | yes | — | — |
| Sep 20 - TOTAL | `sep_20_total` | float64 | — | yes | — | — |
| Oct 20 -LEAD | `oct_20_lead` | float64 | — | yes | — | — |
| Oct 20 - LAG | `oct_20_lag` | float64 | — | yes | — | — |
| Oct 20 - TOTAL | `oct_20_total` | float64 | — | yes | — | — |
| Nov 20 -LEAD | `nov_20_lead` | float64 | — | yes | — | — |
| Nov 20 - LAG | `nov_20_lag` | float64 | — | yes | — | — |
| Nov 20 - TOTAL | `nov_20_total` | float64 | — | yes | — | — |
| Dec 20 -LEAD | `dec_20_lead` | float64 | — | yes | — | — |
| Dec 20 - LAG | `dec_20_lag` | float64 | — | yes | — | — |
| Dec 20 - TOTAL | `dec_20_total` | float64 | — | yes | — | — |
| Jan 21 -LEAD | `jan_21_lead` | float64 | — | yes | — | — |
| Jan 21 - LAG | `jan_21_lag` | float64 | — | yes | — | — |
| Jan 21 - TOTAL | `jan_21_total` | float64 | — | yes | — | — |
| Feb 21 -LEAD | `feb_21_lead` | float64 | — | yes | — | — |
| Feb 21 - LAG | `feb_21_lag` | float64 | — | yes | — | — |
| Feb 21 - TOTAL | `feb_21_total` | float64 | — | yes | — | — |
| Mar 21 -LEAD | `mar_21_lead` | float64 | — | yes | — | — |
| Mar 21 - LAG | `mar_21_lag` | float64 | — | yes | — | — |
| Mar 21 - TOTAL | `mar_21_total` | float64 | — | yes | — | — |
| Apr 21 -LEAD | `apr_21_lead` | float64 | — | yes | — | — |
| Apr 21 - LAG | `apr_21_lag` | float64 | — | yes | — | — |
| Apr 21 - TOTAL | `apr_21_total` | float64 | — | yes | — | — |
| May 21 -LEAD | `may_21_lead` | float64 | — | yes | — | — |
| May 21 - LAG | `may_21_lag` | float64 | — | yes | — | — |
| May 21 - TOTAL | `may_21_total` | float64 | — | yes | — | — |
| Jun 21 -LEAD | `jun_21_lead` | float64 | — | yes | — | — |
| Jun 21 - LAG | `jun_21_lag` | float64 | — | yes | — | — |
| Jun 21 - TOTAL | `jun_21_total` | float64 | — | yes | — | — |
| Jul 21 -LEAD | `jul_21_lead` | float64 | — | yes | — | — |
| Jul 21 - LAG | `jul_21_lag` | float64 | — | yes | — | — |
| Jul 21 - TOTAL | `jul_21_total` | float64 | — | yes | — | — |
| Aug 21 -LEAD | `aug_21_lead` | float64 | — | yes | — | — |
| Aug 21 - LAG | `aug_21_lag` | float64 | — | yes | — | — |
| Aug 21 - TOTAL | `aug_21_total` | float64 | — | yes | — | — |
| Sep 21 -LEAD | `sep_21_lead` | float64 | — | yes | — | — |
| Sep 21 - LAG | `sep_21_lag` | float64 | — | yes | — | — |
| Sep 21 - TOTAL | `sep_21_total` | float64 | — | yes | — | — |
| Oct 21 -LEAD | `oct_21_lead` | float64 | — | yes | — | — |
| Oct 21 - LAG | `oct_21_lag` | float64 | — | yes | — | — |
| Oct 21 - TOTAL | `oct_21_total` | float64 | — | yes | — | — |
| Nov 21 -LEAD | `nov_21_lead` | float64 | — | yes | — | — |
| Nov 21 - LAG | `nov_21_lag` | float64 | — | yes | — | — |
| Nov 21 - TOTAL | `nov_21_total` | float64 | — | yes | — | — |
| Dec 21 - LEAD | `dec_21_lead` | float64 | — | yes | — | — |
| Dec 21 - LAG | `dec_21_lag` | float64 | — | yes | — | — |
| Dec 21 - Total | `dec_21_total` | float64 | — | yes | — | — |
| Jan 22 - LEAD | `jan_22_lead` | float64 | — | yes | — | — |
| Jan 22 - LAG | `jan_22_lag` | float64 | — | yes | — | — |
| Jan 22 - Total | `jan_22_total` | float64 | — | yes | — | — |
| Feb 22 - LEAD | `feb_22_lead` | float64 | — | yes | — | — |
| Feb 22 - LAG | `feb_22_lag` | float64 | — | yes | — | — |
| Feb 22 - Total | `feb_22_total` | float64 | — | yes | — | — |
| Mar 22 - LEAD | `mar_22_lead` | float64 | — | yes | — | — |
| Mar 22 - LAG | `mar_22_lag` | float64 | — | yes | — | — |
| Mar 22 - Total | `mar_22_total` | float64 | — | yes | — | — |
| Apr 22 - LEAD | `apr_22_lead` | float64 | — | yes | — | — |
| Apr 22 - LAG | `apr_22_lag` | float64 | — | yes | — | — |
| Apr 22 - Total | `apr_22_total` | float64 | — | yes | — | — |
| May 22 - LEAD | `may_22_lead` | float64 | — | yes | — | — |
| May 22 - LAG | `may_22_lag` | float64 | — | yes | — | — |
| May 22 - Total | `may_22_total` | float64 | — | yes | — | — |
| Jun 22 - LEAD | `jun_22_lead` | float64 | — | yes | — | — |
| Jun 22 - LAG | `jun_22_lag` | float64 | — | yes | — | — |
| Jun 22 - Total | `jun_22_total` | float64 | — | yes | — | — |
| Jul 22 - LEAD | `jul_22_lead` | float64 | — | yes | — | — |
| Jul 22 - LAG | `jul_22_lag` | float64 | — | yes | — | — |
| Jul 22 - Total | `jul_22_total` | float64 | — | yes | — | — |
| Aug 22 - LEAD | `aug_22_lead` | float64 | — | yes | — | — |
| Aug 22 - LAG | `aug_22_lag` | float64 | — | yes | — | — |
| Aug 22 - Total | `aug_22_total` | float64 | — | yes | — | — |
| Sep 22 - LEAD | `sep_22_lead` | float64 | — | yes | — | — |
| Sep 22 - LAG | `sep_22_lag` | float64 | — | yes | — | — |
| Sep 22 - Total | `sep_22_total` | float64 | — | yes | — | — |
| Oct 22 - LEAD | `oct_22_lead` | float64 | — | yes | — | — |
| Oct 22 - LAG | `oct_22_lag` | float64 | — | yes | — | — |
| Oct 22 - Total | `oct_22_total` | float64 | — | yes | — | — |
| Nov 22 - LEAD | `nov_22_lead` | float64 | — | yes | — | — |
| Nov 22 - LAG | `nov_22_lag` | float64 | — | yes | — | — |
| Nov 22 - Total | `nov_22_total` | float64 | — | yes | — | — |
| Dec 22 - LEAD | `dec_22_lead` | float64 | — | yes | — | — |
| Dec 22 - LAG | `dec_22_lag` | float64 | — | yes | — | — |
| Dec 22 - Total | `dec_22_total` | float64 | — | yes | — | — |
| Jan 23 - LEAD | `jan_23_lead` | float64 | — | yes | — | — |
| Jan 23 - LAG | `jan_23_lag` | float64 | — | yes | — | — |
| Jan 23 - Total | `jan_23_total` | float64 | — | yes | — | — |
| Feb 23 - LEAD | `feb_23_lead` | float64 | — | yes | — | — |
| Feb 23 - LAG | `feb_23_lag` | float64 | — | yes | — | — |
| Feb 23 - Total | `feb_23_total` | float64 | — | yes | — | — |
| Mar 23 - LEAD | `mar_23_lead` | float64 | — | yes | — | — |
| Mar 23 - LAG | `mar_23_lag` | float64 | — | yes | — | — |
| Mar 23 - Total | `mar_23_total` | float64 | — | yes | — | — |
| Apr 23 - LEAD | `apr_23_lead` | float64 | — | yes | — | — |
| Apr 23 - LAG | `apr_23_lag` | float64 | — | yes | — | — |
| Apr 23 - Total | `apr_23_total` | float64 | — | yes | — | — |
| May 23 - LEAD | `may_23_lead` | float64 | — | yes | — | — |
| May 23 - LAG | `may_23_lag` | float64 | — | yes | — | — |
| May 23 - Total | `may_23_total` | float64 | — | yes | — | — |
| June 23 - LEAD | `june_23_lead` | float64 | — | yes | — | — |
| June 23 - LAG | `june_23_lag` | float64 | — | yes | — | — |
| June 23 - Total | `june_23_total` | float64 | — | yes | — | — |
| July 23 - LEAD | `july_23_lead` | float64 | — | yes | — | — |
| July 23 - LAG | `july_23_lag` | float64 | — | yes | — | — |
| July 23 - Total | `july_23_total` | float64 | — | yes | — | — |
| Aug 23 - LEAD | `aug_23_lead` | float64 | — | yes | — | — |
| Aug 23 - LAG | `aug_23_lag` | float64 | — | yes | — | — |
| Aug 23 - Total | `aug_23_total` | float64 | — | yes | — | — |
| Sep 23 - LEAD | `sep_23_lead` | float64 | — | yes | — | — |
| Sep 23 - LAG | `sep_23_lag` | float64 | — | yes | — | — |
| Sep 23 - Total | `sep_23_total` | float64 | — | yes | — | — |
| Oct 23 - LEAD | `oct_23_lead` | float64 | — | yes | — | — |
| Oct 23 - LAG | `oct_23_lag` | float64 | — | yes | — | — |
| Oct 23 - Total | `oct_23_total` | float64 | — | yes | — | — |
| Nov 23 - LEAD | `nov_23_lead` | float64 | — | yes | — | — |
| Nov 23 - LAG | `nov_23_lag` | float64 | — | yes | — | — |
| Nov 23 - Total | `nov_23_total` | float64 | — | yes | — | — |
| Dec 23 - LEAD | `dec_23_lead` | float64 | — | yes | — | — |
| Dec 23 - LAG | `dec_23_lag` | float64 | — | yes | — | — |
| Dec 23 - Total | `dec_23_total` | float64 | — | yes | — | — |
| Jan 24 - LEAD | `jan_24_lead` | float64 | — | yes | — | — |
| Jan 24 - LAG | `jan_24_lag` | float64 | — | yes | — | — |
| Jan 24 - Total | `jan_24_total` | float64 | — | yes | — | — |
| Feb 24 - LEAD | `feb_24_lead` | float64 | — | yes | — | — |
| Feb 24 - LAG | `feb_24_lag` | float64 | — | yes | — | — |
| Feb 24 - Total | `feb_24_total` | float64 | — | yes | — | — |
| Mar 24 - LEAD | `mar_24_lead` | float64 | — | yes | — | — |
| Mar 24 - LAG | `mar_24_lag` | float64 | — | yes | — | — |
| Mar 24 - Total | `mar_24_total` | float64 | — | yes | — | — |
| Apr 24 - LEAD | `apr_24_lead` | float64 | — | yes | — | — |
| Apr 24 - LAG | `apr_24_lag` | float64 | — | yes | — | — |
| Apr 24 - Total | `apr_24_total` | float64 | — | yes | — | — |
| May 24 - LEAD | `may_24_lead` | float64 | — | yes | — | — |
| May 24 - LAG | `may_24_lag` | float64 | — | yes | — | — |
| May 24 - Total | `may_24_total` | float64 | — | yes | — | — |
| June 24 - LEAD | `june_24_lead` | float64 | — | yes | — | — |
| June 24 - LAG | `june_24_lag` | float64 | — | yes | — | — |
| June 24 - Total | `june_24_total` | float64 | — | yes | — | — |
| July 24 - LEAD | `july_24_lead` | float64 | — | yes | — | — |
| July 24 - LAG | `july_24_lag` | float64 | — | yes | — | — |
| July 24 - Total | `july_24_total` | float64 | — | yes | — | — |
| Aug 24 - LEAD | `aug_24_lead` | float64 | — | yes | — | — |
| Aug 24 - LAG | `aug_24_lag` | float64 | — | yes | — | — |
| Aug 24 - Total | `aug_24_total` | float64 | — | yes | — | — |
| Sep 24 - LEAD | `sep_24_lead` | float64 | — | yes | — | — |
| Sep 24 - LAG | `sep_24_lag` | float64 | — | yes | — | — |
| Sep 24 - Total | `sep_24_total` | float64 | — | yes | — | — |
| Oct 24 - LEAD | `oct_24_lead` | float64 | — | yes | — | — |
| Oct 24 - LAG | `oct_24_lag` | float64 | — | yes | — | — |
| Oct 24 - Total | `oct_24_total` | float64 | — | yes | — | — |
| Nov 24 - LEAD | `nov_24_lead` | float64 | — | yes | — | — |
| Nov 24 - LAG | `nov_24_lag` | float64 | — | yes | — | — |
| Nov 24 - Total | `nov_24_total` | float64 | — | yes | — | — |
| Dec 24 - LEAD | `dec_24_lead` | float64 | — | yes | — | — |
| Dec 24 - LAG | `dec_24_lag` | float64 | — | yes | — | — |
| Dec 24 - Total | `dec_24_total` | float64 | — | yes | — | — |

- Entity key: `company`, `unit`, `default_market`, `location`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Status: held in gridflow (E-SEM). 243 silver rows, 176 vendor columns plus the eight lineage columns.
The site page names its question as a caveat; it shows no rows of this table, which is too wide for the
column guide.**

The record covers **only the wide archive** `Reactive Utilisation Data - Apr-2020 - Dec-2024` (one
epoch, 176 columns): an opaque `id`, the four identity columns, then LEAD / LAG / TOTAL for 57 months,
**Apr 2020 to Dec 2024** (171 value columns). Its 243 rows are unique on the four identity columns,
which are the entity key. `id` is stored as an opaque string; the vendor has not defined its role
(`TODO: verify`) and it is not the key. The monthly columns are `float64`; blank cells (2,895) are
null.

The **current long table** (`Reactive Utilisation Data`, 19,130 rows, columns `Company, Unit,
Default/Market, Location, Month-Year, LEAD, LAG, TOTAL`) is a different table shape and is a
resource-level HOLD with no record. It repeats one complete row, so no key, including all columns,
passes the duplicate guard (RULINGS 538). Its header is deliberately not frozen as a second epoch.

**Relationship between the two resources (structure only).** The long table restates all 57
overlapping months and every archive unit/month identity (13,851 unit/month keys in the archive, all
present in the long table, which adds 5,278 later or other identities). It is **not** a
value-identical replacement: it differs from the archive on 241 values and publishes 2,895 archive
blanks as 0. Neither silent overlap deduplication nor a coverage grant follows. The historic family
shares no months with either resource.

NESO's package note says a new version of the reactive utilisation data will have a fixed number of
columns with rows growing at each update, which matches the long-table shape. `TODO: verify` that the
long table is that new version and whether the archive is therefore superseded.

**Unit.** The package text states **MVARh** per unit per month. The "Vendor unit" values `String` in
the schema above (identity columns) and the generic label `Number` for LEAD/LAG/TOTAL come from the
vendor field-info for resource `528b03d2` (the held current long table), snapshot
`neso-snapshots/field-info/20261008T114228Z/orps_utilisation_reactive.json`, not from a dictionary for
the archive `a61c6c26` that this family's record covers. Neither is a physical unit for the
LEAD/LAG/TOTAL columns, so the unit rests on the package text alone.

**Sentinels.** Zeros are numeric zeros and are kept. No token or sentinel is mapped. The open question
is whether a blank means zero or not reported.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` equal the CKAN `last_modified`
   of the archive: `2025-02-14T13:27:21.557694Z`. The long table's `last_modified` was
   `2026-10-07T15:58:09.723806` at capture (it was `2026-09-04T15:21:37.532365` in the 2026-10-06
   catalogue snapshot). The actual refresh day is `TODO: verify`. That resource has no silver.
2. **Event time (temporal recipe `none`).** The month is in the column header, so no event time is
   derived. `timestamp_utc` (and `event_time`) is the **capture time**, `2026-10-08T11:15:58.937852Z`.
   It carries no market meaning. A `month(Month-Year)` recipe (`%b-%y`) would be possible for the long
   table alone, but that table has no silver (bronze only).

Silver carries the same eight lineage columns as the historic family (`dataset_version` `1+e1`).

### `orps_utilisation_reactive_default`

- Kind: tabular · archetype: SER · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Year | `year_vendor` | int64 | — | no | — | — |
| Month | `month_vendor` | int64 | — | no | — | — |
| HPIm | `hpim` | float64 | — | yes | — | £ |
| PAPIm | `papim` | float64 | — | yes | — | £ |
| PPIm | `ppim` | float64 | — | yes | — | £ |
| FRPIm | `frpim` | float64 | — | yes | — | £ |
| Im | `im` | float64 | — | yes | — | £ |
| X = 1 | `x_1` | float64 | — | yes | — | £ |
| X = 0.2 | `x_0_2` | float64 | — | yes | — | £ |

- Entity key: `year_vendor`, `month_vendor`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Status: held in gridflow (E-SEM). 228 silver rows (one per payment-rate month), 9 vendor columns plus
the eight lineage columns. The site page shows this table: a chart of the yearly mean `X = 1` rate, eight
sample rows and a notebook, with the price-input unit question as a caveat.**

The monthly inputs and outputs of the ORPS default payment-rate calculation: `Year` and `Month`
(stored as `year_vendor` and `month_vendor`, because `year` and `month` are reserved silver names),
five inputs or factors (`HPIm`, `PAPIm`, `PPIm`, `FRPIm`, `Im`) and two output rates (`X = 1`,
`X = 0.2`). The vendor dictionary describes `HPIm`, `PAPIm` and `PPIm` as the Heren, Argus and
Platts values respectively (power-price inputs) and `FRPIm` as the RPI indices input. "Default"
is the ORPS default-payment mechanism; the two `X` columns are payment rates under different
utilisation-factor conditions, not measured reactive-power quantities. The entity key is
`year_vendor` and `month_vendor`, unique in this resource. All 1,596 value cells cast to `float64`;
there are no blanks, tokens, commas or percent cells.

**Units** (vendor dictionary, refined by NESO's default-payment guidance,
[document 84286](https://www.neso.energy/document/84286/download)). The dictionary labels every
numeric column with a bare £, which is incomplete or unsuitable for most of them:

| Column | Unit | Source |
|---|---|---|
| `X = 1`, `X = 0.2` | £/MVArh | Guidance labels the rate outputs; the dictionary's bare £ is incomplete |
| `FRPIm` | dimensionless RPI index level | Guidance; the dictionary's £ is unsuitable |
| `Im` | dimensionless indexation factor | Guidance; the dictionary's £ is unsuitable |
| `HPIm`, `PAPIm`, `PPIm` | **£ (dictionary), denominator not established** | Hold question in Holds |

No unit is inferred from industry convention (for example £/MWh for the price inputs).

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` equal the CKAN `last_modified`
   of the capture, `2026-09-17T07:44:25.572388Z`. The file has no issue column, and the "Oct - 2026" in
   its title is a rate label, not evidenced issuance. It covers historical effective months and is
   not an issue-evidenced forecast archive.
2. **Event time (temporal recipe `none`).** `Year` and `Month` are separate columns and no recipe
   composes them into a date, so no event time is derived. `timestamp_utc` (and `event_time`) is the
   **capture time**, `2026-10-08T11:16:05.568105Z`, with no market meaning.

Silver carries the same eight lineage columns as the other families (`dataset_version` `1+e1`).

## Cadence

- Registry refresh: monthly
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Monthly
- Captures to date: one per resource, all on 2026-10-08. No scheduled refresh has run yet, so
  amendment, deletion and republication behaviour across captures is unmeasured (`TODO: verify`).
- NESO's resource descriptions say the utilisation files are updated in the middle of each month and
  hold data up to two months earlier (a month named in the description is an example, not a
  schedule). The current long table's `last_modified` was 2026-09-04T15:21:37.532365 in the 2026-10-06
  catalogue snapshot and 2026-10-07T15:58:09.723806 at the 2026-10-08 capture; the actual refresh day
  is `TODO: verify`. gridflow's refresh is
  monthly; later republications of the long table reach bronze only, until its hold lifts.
- The payment-rate CSV and PDF share a `last_modified` day (2026-09-17). How often NESO republishes
  them is `TODO: verify`.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `orps_utilisation_historic_reactive`: held: TODO: ORPS-HIST-DASH / ORPS-HIST-IDENTITY — what does the padded `-` cell mean (zero, not reported, not applicable)? And one repeated four-field identity (rows 181 and 277; identity withheld) carries 234 different values: are these two distinct entries, and what distinguishes them? (unit v0.22-K-AS-3b)
- `orps_utilisation_reactive`: held: TODO: ORPS-REACTIVE-ARCHIVE — the current long table restates every unit/month of this Apr-20 … Dec-24 archive but differs on 241 values and publishes 2,895 of its blanks as 0; is this archive superseded, and does a blank mean zero or not reported? (unit v0.22-K-AS-3b)
- `orps_utilisation_reactive_default`: held: TODO: ORPS-PRICE-INPUT-UNITS — the dictionary labels HPIm, PAPIm and PPIm only "£" and NESO's default-payment guidance calls them power-price inputs without a denominator; what unit are they in this export? (FRPIm is a dimensionless RPI index, Im a dimensionless indexation factor, X = 1 / X = 0.2 are £/MVArh rates.) (unit v0.22-K-AS-3b)

All three silver families are held in gridflow (unit E-SEM): no model consumes them. The package-level
`eligibility: eligible` in the front matter is the package registry entry; the holds are per family and
per resource. Silver holds 295, 243 and 228 rows. The site page shows rows anyway (ruling 66): each
family's question is a caveat, and the chart, sample rows and notebook come from the default payment-rate
table. The registry's hold text for the long table quotes the cells of the duplicated row; this note does
not repeat those cell values.

1. **`orps_utilisation_historic_reactive`.** Two vendor questions. (a) What does the padded `-` cell
   mean (zero, not reported, not applicable)? It occurs in 32 cells. (b) One four-field identity
   (identity withheld) appears twice, at rows 181 and 277, with 234 different value columns: are these two distinct
   entries, and what distinguishes them? Until both are answered the value columns stay strings and
   the key is the full row.
2. **`orps_utilisation_reactive`.** The long table restates every unit/month of the Apr-20 to Dec-24
   archive but differs on 241 values and publishes 2,895 archive blanks as 0. Is the archive
   superseded, and does a blank mean zero or not reported? Separately, the long table's own
   resource-level HOLD (ORPS-REACTIVE-LONG-DUPLICATE) asks whether its repeated complete row is a
   publication defect or two distinct utilisations; re-disposition needs a corrected NESO upload (a
   new `last_modified`) or a vendor identity column.
3. **`orps_utilisation_reactive_default`.** The dictionary labels `HPIm`, `PAPIm` and `PPIm` only "£"
   and NESO's guidance calls them power-price inputs without a denominator. What unit are they in
   this export? (`FRPIm` and `Im` are dimensionless; `X = 1` and `X = 0.2` are £/MVArh rates.) The raw
   numeric values are kept as published in the silver record.
4. **`Reactive Utilisation-Nov-2021` workbook (HOLD, not a family).** Layout, not semantics: see the
   HOLD disposition above.

Not held, and not a question: the two PDFs stay DOC.

Other open items, none of them holding anything:

- `TODO: verify` the unit conflict between the historic dictionary (MVAr) and the package text
  (MVARh).
- `TODO: verify` the vendor role of the `id` column in the wide archive.
- `TODO: verify` whether the long table is the "fixed number of columns" version NESO announced.
- `TODO: verify` the original publication instants of the historical months: `available_at` is the
  CKAN `last_modified` of the capture and never backdates to the month a figure was first released.
