---
source: "neso_data_portal"
package: "gb-system-inertia-bid-and-offer-costs"
dataset_key: "inertia_bid_offer_costs"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-10
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# Great Britain System Inertia Bid and Offer Costs

Supported by National Energy SO Open Data

## Overview

NESO publishes indicative daily prices for the cost of procuring system inertia in Great Britain. The package describes them as average daily prices for Balancing Mechanism accepted offers tagged as being for System Inertia, plus the cost of the bid actions needed to make room for those offers. Three variants are published as separate columns, one row per day:

- **Method A** is the cost of the inertia based on the average bid price.
- **Method B** is the cost of inertia assuming the units replace the energy taken off at the average wind bid price.
- **Method C** is the cost of inertia assuming the units replace the energy taken off at the highest bid price.

NESO states that these prices represent all bid prices in each category, not necessarily the accepted bid price, so they are indicative scenario costs and not settled outturn. The body covers 2019-04-01 to 2022-03-31 (1,096 distinct dates, one row each). The CKAN resource was last modified on 2022-10-19, so the package is operationally treated as frozen. NESO's catalogue says "Ad hoc" update frequency, not "will never update"; the registry's `frozen` refresh is a gridflow operating choice. TODO: verify whether NESO guarantees permanent non-update.

**This family is HELD.** Silver exists (row counts and schema below) but its values are not published or consumed until the hold question is answered. See [Holds](#holds).

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

The package stays `eligible` in the registry; only the family's outputs are held (RULINGS 653; held-exactly-as-ruled test in batch BAL-1). Row counts and schema are documented here, but no data values (samples, minima, maxima, aggregates or example values) are published for this family, and downstream models must not consume it until E-SEM rules on the three questions above.

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
