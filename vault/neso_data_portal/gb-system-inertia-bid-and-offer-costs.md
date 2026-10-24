---
source: "neso_data_portal"
package: "gb-system-inertia-bid-and-offer-costs"
dataset_key: "inertia_bid_offer_costs"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: System inertia bid and offer costs
  summary: >-
    NESO's indicative daily price of inertia bought through Balancing Mechanism offers, with the bids
    those offers need, costed three ways.
  facts:
    vendor: "NESO Data Portal, package `gb-system-inertia-bid-and-offer-costs`: one CSV file"
    cadence: Ad hoc, as NESO lists it
    grain: "Each row: one day, with the Method A, B and C prices"
  landscape: market
  what_it_is: >-
    Some accepted Balancing Mechanism offers are tagged for system inertia. This file gives that
    inertia's average daily price, including the bid actions the offers require: at the average bid
    price (A), or assuming displaced energy is replaced at the average wind bid price (B) or highest
    bid price (C). NESO calls them indicative: they use all bid prices.
  how_used:
    - An indicative daily cost of buying inertia through the Balancing Mechanism
    - How far that cost moves with the bid price assumed, Method A to C
  chart:
    type: line
    silver: neso_data_portal/inertia_bid_offer_costs
    time: date
    values:
      - {column: method_c_highest_bid_price, series: c}
      - {column: method_b_average_wind_price, series: b}
      - {column: method_a_average_bid_price, series: a}
    filter:
      - {column: method_a_average_bid_price, op: ne, value: 0}
      - {column: method_b_average_wind_price, op: ne, value: 0}
      - {column: method_c_highest_bid_price, op: ne, value: 0}
    dedup: {"on": [date], order_by: published_at}
    aggregation: last
    window: {start: "2022-02-01", end: "2022-02-28"}
    unit: "£/GVA or £ per GVAs"
  chart_view:
    title: Inertia cost by method, February 2022
    caption: >-
      Silver `neso_data_portal/inertia_bid_offer_costs`, daily, 1 to 28 February 2022. Days with a
      zero in any method are gaps, as NESO does not define a zero; most days outside this month are zero
      in every method. NESO gives the unit two ways.
    alt: >-
      Line chart from neso_data_portal/inertia_bid_offer_costs, in NESO's unit (£/GVA or £ per
      GVAs), one point per date and method, 1 to 27 February 2022, with gaps on 2, 10 and 26
      February. Method C runs from 13,171 on 14 February to 27,107 on 27 February, and Method B from
      7,867 to 17,359 on the same days; both climb after 16 February. Method A is lowest throughout,
      from 1,543 on 7 February to 5,234 on 25 February.
    x_label: NESO's date; day window not stated
    key:
      - {series: c, label: "Method C, highest bid", codes: "Method C: Highest bid price", paint: clay, note: "Displaced energy replaced at the highest bid price"}
      - {series: b, label: "Method B, wind bid", codes: "Method B: Average wind price", paint: olive, note: "Displaced energy replaced at the average wind bid price"}
      - {series: a, label: "Method A, average bid", codes: "Method A: Average bid price", paint: petrol, note: "At the average bid price"}
  caveat: "NESO's unit is £/GVA or £ per GVAs; its day window and its zeros are unexplained."
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then the file downloaded whole unless its
      `last_modified` is unchanged.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=gb-system-inertia-bid-and-offer-costs"
      - "GET https://api.neso.energy/dataset/23d66321-9c65-4825-9d62-94b6b24a1207/resource/8da765a1-004f-46a5-8b3f-0e5b1787fcb1/download/inertia_costs_methods.csv"
    commands:
      - {run: gridflow ingest neso_data_portal inertia_bid_offer_costs --last 24h, comment: whole file to bronze}
      - {run: gridflow transform neso_data_portal inertia_bid_offer_costs --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: date, op: in, value: ["2020-11-12", "2022-02-01", "2022-02-02", "2022-02-24", "2022-02-25", "2022-02-26", "2022-02-27", "2022-02-28"]}
      dedup: {"on": [date], order_by: published_at}
      order_by: [date]
      columns: [date, method_a_average_bid_price, method_b_average_wind_price, method_c_highest_bid_price, published_at, timestamp_utc]
    key: [date]
    caption: "12 November 2020, with a negative Method A, and seven February 2022 days, some zero."
    fields:
      date: "NESO's date of the price; NESO does not state the day's window or zone"
      method_a_average_bid_price: "Method A, at the average bid price; NESO's unit: £/GVA or £ per GVAs"
      method_b_average_wind_price: "Method B: displaced energy replaced at the average wind bid price; unit as A"
      method_c_highest_bid_price: "Method C: displaced energy replaced at the highest bid price; unit as A"
      published_at: "NESO's last-modified time for the whole file, read as UTC; one per capture"
      timestamp_utc: "Start of settlement period 1 of `date`, GB local midnight, as UTC; gridflow's anchor"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote the capture to bronze, UTC
  notebook:
    lead: >-
      Returns a pandas DataFrame from the DuckDB view
      `silver_neso_data_portal_inertia_bid_offer_costs_latest`, every row of the newest capture,
      filtered on `date` with both ends included; lineage columns dropped.
    cells:
      - |
        df = data.neso_data_portal.query("inertia_bid_offer_costs", "2019-04-01", "2022-03-31")
        m = ["method_a_average_bid_price", "method_b_average_wind_price", "method_c_highest_bid_price"]
        df[["date", *m]].tail()
      - |
        april_year = (df.date.dt.year - (df.date.dt.month < 4)).rename("april_year")
        zero = df[m].eq(0).rename(columns=lambda c: c[:8] + "_zero")
        zero.groupby(april_year).sum().assign(days=df.groupby(april_year).size()).rename_axis(None)
      - |
        no_zero = df[m].ne(0).all(axis=1).groupby(df.date.dt.strftime("%Y-%m")).sum()
        ax = no_zero.plot.bar(color="#155A6E", figsize=(8, 3.5), xlabel="month", ylabel="days with no zero")
        ax.set_xticks(range(0, len(no_zero), 6), no_zero.index[::6], rotation=0);
    needs: the inertia costs file
    plot_alt: >-
      Bar plot of the days in each month, April 2019 to March 2022, on which all three methods are
      non-zero. July 2019 and January 2020 have 1; May 2020 has 23 and February 2022 has 24; 31 of
      the 36 months have 2 to 15.
  related:
    - {dataset: neso_data_portal/constraint-breakdown, note: "Daily spend on increasing system inertia, in £, among four constraint costs"}
---

# Great Britain System Inertia Bid and Offer Costs

Supported by National Energy SO Open Data

## Overview

NESO publishes indicative daily prices for the cost of procuring system inertia in Great Britain. The package describes them as average daily prices for Balancing Mechanism accepted offers tagged as being for System Inertia, plus the cost of the bid actions needed to make room for those offers. Three variants are published as separate columns, one row per day:

- **Method A** is the cost of the inertia based on the average bid price.
- **Method B** is the cost of inertia assuming the units replace the energy taken off at the average wind bid price.
- **Method C** is the cost of inertia assuming the units replace the energy taken off at the highest bid price.

NESO states that these prices represent all bid prices in each category, not necessarily the accepted bid price, so they are indicative scenario costs and not settled outturn. The body covers 2019-04-01 to 2022-03-31 (1,096 distinct dates, one row each). The CKAN resource was last modified on 2022-10-19, so the package is operationally treated as frozen. NESO's catalogue says "Ad hoc" update frequency, not "will never update"; the registry's `frozen` refresh is a gridflow operating choice. TODO: verify whether NESO guarantees permanent non-update.

**This family is HELD.** Silver exists (row counts and schema below) but its values are not consumed by gridflow's models until the hold question is answered; the site page shows the rows and a chart with a caveat naming the question (ruling 66). See [Holds](#holds).

- Publisher group: Balancing costs
- Registry group: balancing · archetype: SER
- Package id: `23d66321-9c65-4825-9d62-94b6b24a1207`

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| GB System Inertia Costs – combined bids and offers | CSV | upload | `8da765a1-004f-46a5-8b3f-0e5b1787fcb1` |

Download: [inertia_costs_methods.csv](https://api.neso.energy/dataset/23d66321-9c65-4825-9d62-94b6b24a1207/resource/8da765a1-004f-46a5-8b3f-0e5b1787fcb1/download/inertia_costs_methods.csv)

Vendor resource description: "Cost per unit of inertia, accounting for both bid and offer costs." The package has one resource, so there are no DOC or HOLD files. The CKAN datastore is active for it (1,096 records).

## Families

### `inertia_bid_offer_costs`

- Kind: tabular · archetype: SER · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Date | `date` | date | `%Y-%m-%d` | no | — | ISO 8601 |
| Method A: Average bid price | `method_a_average_bid_price` | float64 | — | yes | — | £/GVA |
| Method B: Average wind price | `method_b_average_wind_price` | float64 | — | yes | — | £/GVA |
| Method C: Highest bid price | `method_c_highest_bid_price` | float64 | — | yes | — | £/GVA |

- Entity key: `date`
- Latest: `whole_capture`
- Temporal recipe: date_sp1 (`date`)

Measured on the full capture: all 1,096 `date` values are unique and the method columns cast cleanly to float64 with no failures. The CKAN datastore types the method fields as int4 while the record casts to float64; the cast is the wider type and no failure was measured. TODO: verify whether the vendor intends integer or fractional values.

### Silver output

Silver is at `C:/gridflow-data/silver/neso_data_portal/inertia_bid_offer_costs/` (Parquet, partitioned by year and month of the capture). The first activation (batch BAL-1, RULINGS 656, window 2026-10-08..2026-10-10) wrote **1,096 rows**, equal to the planned count and to the body row count, with no transform errors. Columns: the four vendor columns above plus the engine columns `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version`.

### The two clocks

| Clock | Column | Meaning |
|---|---|---|
| Vintage (when the row was knowable) | `published_at`, `available_at` | CKAN `last_modified` of the captured file (ADR-030). `available_at` = `published_at`. For this package it is 2022-10-19T17:16:40.960429 UTC for every row. The resource `url_type` is `upload`, so this is the vendor's upload time, not a capture-time fallback. |
| Event time (what the row describes) | `event_time`, `timestamp_utc` | Temporal recipe `date_sp1`: the UTC start of settlement period 1 of the row's `date` (23:00 UTC the previous evening during British Summer Time, 00:00 UTC in winter). This is an engine anchor for a calendar day, not a vendor-stated measurement instant. |

`capture_written_at` is when gridflow wrote the bronze file (2026-10-08) and is neither clock. Point-in-time queries use `available_at <= :as_of`; every row of this package becomes available at the same instant, because the whole file is one upload.

TODO: verify the exact averaging-day window and time zone behind `Date`. The column is a plain ISO date and does not evidence an instant; the `date_sp1` anchor is a convention.

### Units

Units come only from the vendor field dictionary (CKAN field-info snapshot 20261008T114228Z). Each of Method A, B and C carries the unit `£/GVA`; `Date` carries `ISO 8601`. The package description instead says "£ per GVAs". The two labels disagree on whether a time dimension is part of the denominator, so the unit is not settled. No conversion is applied and neither spelling is normalised into a column name (the silver columns are unit-free by design). See [Holds](#holds).

### Sentinels and missing values

- No numeric or lexical sentinel is mapped to null: the full body had no blanks, `NA`/`N/A` tokens or uncastable values in the method columns, and the nullable flag is a typing allowance only.
- `N/A` appears in the vendor dictionary's `comment` field for every column; it is not a body sentinel.
- Zero-valued method cells exist in the body and are preserved as numeric zeros. Their meaning (no inertia action that day, missing data, or a genuine zero cost) is undocumented and is part of the hold question.

## Cadence

- Registry refresh: frozen
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

## Holds

- `inertia_bid_offer_costs`: held: TODO: the unit denominator — every field dictionary says £/GVA while the package description says £ per GVAs; the exact averaging-day window; what a zero method value means. (unit E-SEM)

The package stays `eligible` in the registry; only the family's outputs are held (RULINGS 653; held-exactly-as-ruled test in batch BAL-1). The site page shows its rows with a caveat (ruling 66), but downstream models must not consume it until E-SEM rules on the three questions above.

## Known issues and gotchas

- The unit denominator is contradictory between the field dictionary (`£/GVA`) and the package description (`£ per GVAs`). Preserve both labels as stated; never add or remove the time dimension.
- The vendor describes the prices as indicative and covering all bid prices in each category, not necessarily the accepted bid price.
- Update frequency "Ad hoc" does not mean frozen; gridflow's `frozen` refresh will not pick up a later vendor re-upload until the registry is changed. TODO: verify.
- `Date` has no time zone or window; the `date_sp1` event time is a storage anchor only. On the 46- and 50-period clock-change days the anchor is still the start of SP1.
- The vendor does not declare a primary-key constraint; `date` is unique by measurement on the captured body only. Selection is `whole_capture`.

## Links

- Vendor page: https://www.neso.energy/data-portal/gb-system-inertia-bid-and-offer-costs
- Registry record: @src/gridflow/connectors/neso_data_portal/registry/gb-system-inertia-bid-and-offer-costs.json
- Eligibility report: @docs/neso_data_portal/eligibility.md
- Batch evidence: @.planning/phases/v0.22-K-BAL-1/K-BAL-1-FACTS.md and @.planning/phases/v0.22-K-BAL-1/VERIFICATION.md
- Activation receipt: @.planning/v0.22-RESULTS.md (section BAL-1)
