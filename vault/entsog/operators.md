---
source: entsog
dataset_key: operators
vendor: ENTSOG Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Gas operators, points and zones
  summary: >-
    ENTSOG's reference registers of operators, balancing zones, points, interconnections and operator point
    directions: the keys its flow, capacity and tariff tables carry.
  facts:
    vendor: ENTSOG Transparency Platform, referential data endpoints
    cadence: A whole-register snapshot per call; `sources.yaml` declares each weekly
    grain: "Operators: one row per `operator_key`; each member has its own key"
  landscape: gas
  what_it_is: >-
    ENTSOG's six referential registers, each fetched whole in one call with no dates; silver keeps the
    newest capture. Flow, capacity and tariff rows carry the same operator, point and direction keys.
    ENTSOG defines none of the response fields. For directions and interconnections ENTSOG sends
    `validFrom` null, which `timestamp_utc` copies, so `query()` returns nothing.
  how_used:
    - Naming the operator, point and direction behind a flow or nomination row.
    - "Looking up `pointDirection` keys; gridflow's request lists are written by hand."
    - "Finding the operator across a point, from directions' `adjacent_operator_key`, blank for some points."
  chart:
    type: bar
    silver: entsog/operators
    group: operator_type_label
    group_map:
      TSO: gas_tso
      SSO: storage
      H2FO: hydrogen
      ESO: power_tso
      LSO: lng
      ETO: transition
      PSO: production
    group_default: rest
    aggregation: count
    sort: value_desc
    unit: operators
  chart_view:
    title: ENTSOG operators by type, fetched 27 September 2026
    caption: >-
      Silver `entsog/operators` only, as fetched 27 September 2026 with `hasData=1`: operators counted by
      ENTSOG's `operatorTypeLabel`, one row per `operator_key`. ENTSOG documents `hasData` for point
      directions only.
    alt: >-
      Horizontal bar chart counting operators by type in entsog/operators as fetched 27 September 2026.
      Gas transmission system operators lead with 154. Then storage operators 108, hydrogen facility
      operators 104, electricity transmission operators 86, LNG operators 51, seven smaller types together
      32, energy transition operators 12 and production operators 10.
    key:
      - {series: gas_tso, label: Gas TSOs, codes: TSO, paint: petrol, note: "ENTSOG's Transmission System Operator for Gas, including BBL company and PTL."}
      - {series: storage, label: Storage, codes: SSO, paint: petrol}
      - {series: hydrogen, label: Hydrogen, codes: H2FO, paint: petrol}
      - {series: power_tso, label: Electricity TSOs, codes: ESO, paint: petrol, note: "ENTSOG's Transmission System Operator for Electricity."}
      - {series: lng, label: LNG, codes: LSO, paint: petrol}
      - {series: rest, label: 7 other types, codes: "DSO, ENA, UTI, BRP, NWO, ASO, USO", paint: hatch-dots, note: "Distribution, associations, utilities, balance responsible parties, news organisations, artificial and upstream operators."}
      - {series: transition, label: Energy transition, codes: ETO, paint: petrol}
      - {series: production, label: Production, codes: PSO, paint: petrol}
  raw_feed:
    note: >-
      One GET per register with `limit=-1` and no dates. Bronze is filed under the UTC fetch day;
      `transform` rewrites one silver file per register from the newest capture.
    requests:
      - "GET https://transparency.entsog.eu/api/v1/operators?limit=-1&timeZone=UCT&hasData=1"
    commands:
      - {run: gridflow ingest entsog operators, comment: "one call; no dates sent"}
      - {run: gridflow transform entsog operators --start 2026-09-27 --end 2026-09-27, comment: "newest capture to one file"}
  record:
    select:
      filter:
        - {column: operator_key, op: in, value: [UK-TSO-0001, UK-TSO-0002, UK-TSO-0003, UK-TSO-0004, UK-SSO-0010, UK-LSO-0004, UK-H2O-0001, TR-TSO-0003]}
      order_by: [operator_key]
      columns: [operator_key, operator_label, operator_type_label, operator_country_key, last_update_date_time, membership_label, tso_eic_code, gas_day_start_hour, participates, timestamp_utc]
    key: [operator_key]
    caption: "Eight operators by key. ENTSOG defines no response fields; guide meanings are read from names."
    fields:
      operator_key: "ENTSOG operator key; its country prefix can differ from the operator's country"
      operator_label: "Short name as sent; many are cut at 20 characters, so join on `operator_key`"
      operator_type_label: "ENTSOG's operator type code, such as `TSO`, `SSO`, `LSO` or `H2FO`"
      operator_country_key: "Country code as sent: ENTSOG's `UK`, not ISO `GB`; `--` for none"
      last_update_date_time: "ENTSOG's update stamp; offsets converted to UTC; the naive 2014 one only labelled UTC"
      membership_label: "ENTSOG membership status as sent, such as `Member`, `EUC` or `Unaffiliated`"
      tso_eic_code: "The operator's EIC, sent with its operator profile; null without one"
      gas_day_start_hour: Gas day start hour; no time zone field, though a few remarks name one
      participates: "`1` or `0`, as text"
      timestamp_utc: "gridflow's copy of the update stamp; not a date the operator joined"
      id: "Vendor `id`: register digit, then operator key; silver keeps the last per `id`"
      operator_logo_url: "Logo URL, usually on ENTSOG's site; blank for most operators"
      operator_label_long: "Full name, such as `National Gas Transmission`"
      operator_tooltip: "Long name and an EIC joined by `|`; the EIC part can be blank"
      operator_country_label: "Country name, such as `United Kingdom`"
      operator_country_flag: "Sent null, so Polars types it `Null`"
      operator_type_label_long: Type in full, such as Storage System Operator
      tso_display_name: "Sent null, so Polars types it `Null`"
      tso_short_name: "Sent null, so Polars types it `Null`"
      tso_long_name: "Sent null, so Polars types it `Null`"
      tso_street: Street name; null without an operator profile
      tso_building_number: "House number as text, such as `2 C`"
      tso_post_office_box: Post office box; almost always null
      tso_zip_code: "Postcode as text, such as `02-337`"
      tso_city: "City, such as `Kassel`"
      tso_contact_name: Contact person or department; null without a profile
      tso_contact_phone: Phone number as text, spaced as sent
      tso_contact_email: Email address, sometimes with a trailing space
      tso_contact_url: Contact page URL; null without a profile
      tso_contact_remarks: Free text, mostly empty
      tso_general_website_url: Website URL; null without a profile
      tso_general_website_url_remarks: Free text, mostly empty
      tso_tariff_information_url: Tariff information URL; null without a profile
      tso_tariff_information_url_remarks: "A legal citation: Regulation (EU) 2017/460, Articles 29 and 30"
      tso_tariff_calculator_url: Tariff calculator URL; null without a profile
      tso_tariff_calculator_url_remarks: "A legal citation: Regulation (EC) 715/2009, Annex I point 3.4(6)"
      tso_capacity_information_url: Capacity information URL; null without a profile
      tso_capacity_information_url_remarks: Free text, mostly empty
      tso_gas_quality_url: Gas quality page URL; null without a profile
      tso_gas_quality_url_remarks: "A legal citation: Regulation (EU) 2015/703, Article 16"
      tso_access_conditions_url: Access conditions URL; null without a profile
      tso_access_conditions_url_remarks: Free text, mostly empty
      tso_contract_documents_url: Contract documents URL; null without a profile
      tso_contract_documents_url_remarks: Free text, mostly empty
      tso_maintainance_url: "Maintenance page URL; ENTSOG's spelling kept"
      tso_maintainance_url_remarks: Free text, mostly empty
      gas_day_start_hour_remarks: "Free text, mostly empty; some name a time zone, such as `EET`"
      multi_annual_contracts_is_available: "`true` or `false` with an operator profile, else null"
      multi_annual_contracts_remarks: Free text, mostly empty
      annual_contracts_is_available: "`true` or `false` with an operator profile, else null"
      annual_contracts_remarks: Free text, mostly empty
      half_annual_contracts_is_available: "`true` or `false` with an operator profile, else null"
      half_annual_contracts_remarks: Free text, mostly empty
      quarterly_contracts_is_available: "`true` or `false` with an operator profile, else null"
      quarterly_contracts_remarks: Free text, mostly empty
      monthly_contracts_is_available: "`true` or `false` with an operator profile, else null"
      monthly_contracts_remarks: Free text, mostly empty
      daily_contracts_is_available: "`true` or `false` with an operator profile, else null"
      daily_contracts_remarks: Free text, mostly empty
      within_day_contracts_is_available: "`true` or `false` with an operator profile, else null"
      within_day_contracts_remarks: Free text, mostly empty
      available_contracts_remarks: Free text, mostly empty
      firm_capacity_tariff_is_applied: "`true` or `false` with an operator profile, else null"
      firm_capacity_tariff_unit: "Unit text such as `EUR/kWh/h/a`; spellings vary between operators"
      firm_capacity_tariff_remarks: Free text, mostly empty
      interruptible_capacity_tariff_is_applied: "`true` or `false` with an operator profile, else null"
      interruptible_capacity_tariff_unit: "Unit text such as `EUR/kWh/h/a`; spellings vary between operators"
      interruptible_capacity_tariff_remarks: Free text, mostly empty
      auction_is_applied: "`true` or `false` with an operator profile, else null"
      auction_tariff_is_applied: "`true` or `false` with an operator profile, else null"
      auction_capacity_tariff_unit: "Unit text such as `EUR/kWh/h/a`; spellings vary between operators"
      auction_remarks: Free text, mostly empty
      commodity_tariff_is_applied: "`true` or `false` with an operator profile, else null"
      commodity_tariff_unit: Unit text; it varies by operator, some send a percentage
      commodity_tariff_price: Commodity tariff cast to a float, in the commodity unit
      commodity_tariff_remarks: Free text, mostly empty
      others_tariff_is_applied: "`true` or `false` with an operator profile, else null"
      others_tariff_remarks: Free text, mostly empty
      general_tariff_information_remarks: Free text, mostly empty
      general_capacity_remark: Free text, mostly empty
      first_come_first_served_is_applied: "`true` or `false` with an operator profile, else null"
      first_come_first_served_remarks: Free text, mostly empty
      open_subscription_window_is_applied: "`true` or `false` with an operator profile, else null"
      open_subscription_window_remarks: Free text, mostly empty
      firm_technical_remark: "The operator's own definition, free text; mostly empty"
      firm_booked_remark: "The operator's own definition, free text; mostly empty"
      firm_available_remark: "The operator's own definition, free text; mostly empty"
      interruptible_total_remark: "The operator's own definition, free text; mostly empty"
      interruptible_booked_remark: "The operator's own definition, free text; mostly empty"
      interruptible_available_remark: "The operator's own definition, free text; mostly empty"
      tso_general_remarks: Free text, often a data disclaimer; mostly empty
      balancing_model: "Mostly `Daily`, `Hourly` or a daily-with-hourly-constraints code; some free text"
      b_m_hourly_imbalance_tolerance_is_applied: "`true` or `false` with an operator profile, else null"
      b_m_hourly_imbalance_tolerance_is_information: "As the operator wrote it, such as flags, dashes, formulas or placeholder text"
      b_m_hourly_imbalance_tolerance_is_remarks: Free text, mostly empty
      b_m_daily_imbalance_tolerance_is_applied: "`true` or `false` with an operator profile, else null"
      b_m_daily_imbalance_tolerance_is_information: "The tolerance as the operator wrote it, such as `Range 3% - 20%`"
      b_m_daily_imbalance_tolerance_is_remarks: Free text, mostly empty
      b_m_additional_daily_imbalance_tolerance_is_applied: "`true` or `false` with an operator profile, else null"
      b_m_additional_daily_imbalance_tolerance_is_information: "As the operator wrote it: flags, dashes, sentences or placeholder text"
      b_m_additional_daily_imbalance_tolerance_is_remarks: Free text, mostly empty
      b_m_cumulated_imbalance_tolerance_is_applied: "`true` or `false` with an operator profile, else null"
      b_m_cumulated_imbalance_tolerance_is_information: "As the operator wrote it, such as flags, sizes, formulas or placeholder text"
      b_m_cumulated_imbalance_tolerance_is_remarks: Free text, mostly empty
      b_m_additional_cumulated_imbalance_tolerance_is_applied: "`true` or `false` with an operator profile, else null"
      b_m_additional_cumulated_imbalance_tolerance_is_information: "As the operator wrote it, such as `0%`, `-` or placeholder text"
      b_m_additional_cumulated_imbalance_tolerance_is_remarks: Free text, mostly empty
      b_m_status_information: Free text on how shippers learn their balancing position
      b_m_status_information_frequency: "Free text, such as `Daily` or `Hourly`"
      b_m_penalties: Free text on imbalance penalties
      b_m_cash_out_regime: Free text, such as monthly cash-out on a daily basis
      b_m_remarks: Free text, mostly empty
      grid_transport_model_type: "Transport model as sent, such as `Entry-Exit` or `Point-to-Point`"
      grid_transport_model_type_remarks: Free text, mostly empty
      grid_conversion_factor_capacity_default: "A float with an operator profile; mostly `1.0`"
      grid_conversion_factor_capacity_default_remaks: "Free text; ENTSOG's spelling `Remaks` kept"
      grid_gross_calorific_value_default_value: "A float, such as `11.3`, in the unit column that follows"
      grid_gross_calorific_value_default_value_to: Upper end when the default calorific value is sent as a range
      grid_gross_calorific_value_default_unit: "Unit text as sent, such as `kWh/Nm3`; spellings vary"
      grid_gross_calorific_value_default_remarks: Free text, mostly empty
      grid_gas_source_default: "Country or `Other`, such as `Russia`; mostly null"
      transparency_information_url: URL; null without a profile
      transparency_information_url_remarks: Free text, mostly empty
      transparency_guidelines_information_url: URL; null without a profile
      transparency_guidelines_information_url_remarks: "A legal citation: Regulation (EC) 715/2009, Annex I Chapter 3"
      tso_umm_rss_feed_url_gas: Feed URL for the operator's gas messages; mostly null
      tso_umm_rss_feed_url_other: Feed URL for the operator's other messages; mostly null
      include_umm_in_acer_rss_feed: "`true` or `false` with an operator profile, else null"
      data_set: "Vendor `dataSet`, the register's number: `1` for operators, leading `id`"
  notebook:
    source: entsog
    lead: >-
      `query()` filters on a date column: here `timestamp_utc`, a copy of ENTSOG's update stamp;
      `ingested_at`, the silver write time, for zones, points and aggregates. So these cells use
      `data.sql()` on `silver_entsog_operators`.
    cells:
      - |
        df = data.sql("""
            SELECT operator_key, operator_label, operator_country_key, operator_type_label,
                   membership_label, tso_eic_code, gas_day_start_hour
            FROM silver_entsog_operators
            ORDER BY operator_key
        """)
      - df[df.operator_country_key == "UK"].head()
      - df["operator_type_label"].value_counts()
    needs: the ENTSOG operator register
  related:
    - {dataset: entsog/physical_flows, note: "Daily flows carrying the same operator, point and direction keys"}
    - {dataset: entsog/nominations, note: "Nominations at GB points, requested by operator, point and direction keys"}
    - {dataset: entsog/aggregated_physical_flows, note: "Zone flows requested by keys from `aggregate_interconnections`"}
    - {dataset: entsog/tariffs, note: Tariffs per operator and point; operator profiles carry the tariff units}
  family:
    slug: reference-data
    members:
      - dataset: operators
        differs: "Operators returned with `hasData=1`, gas TSOs to news organisations; one per `operator_key`"
        request: "GET https://transparency.entsog.eu/api/v1/operators?limit=-1&timeZone=UCT&hasData=1"
      - dataset: balancing_zones
        differs: "One per `bz_key`, with manager and successor; meta shows ENTSOG's default `isDeactivated=0`"
        request: "GET https://transparency.entsog.eu/api/v1/balancingZones?limit=-1&timeZone=UCT"
      - dataset: connection_points
        differs: "Main map points only, one per `point_key`; meta shows ENTSOG's default `IsInvalid=False`"
        request: "GET https://transparency.entsog.eu/api/v1/connectionPoints?limit=-1&timeZone=UCT"
      - dataset: interconnections
        differs: "UK-side links; `query()` finds nothing; update stamp, labelled UTC, postdates the fetch"
        request: "GET https://transparency.entsog.eu/api/v1/interconnections?limit=-1&timeZone=UCT&fromCountryKey=UK"
      - dataset: aggregate_interconnections
        differs: "UK zones' aggregates by operator, direction and adjacent system; `countryKey=UK` sent"
        request: "GET https://transparency.entsog.eu/api/v1/aggregateInterconnections?limit=-1&timeZone=UCT&countryKey=UK"
      - dataset: operator_point_directions
        differs: "Triples of TSOs that publish data (`hasData=1`); `query()` returns no rows; use `data.sql()`"
        request: "GET https://transparency.entsog.eu/api/v1/operatorPointDirections?limit=-1&timeZone=UCT&hasData=1"
---

# ENTSOG — Operators

## Overview

All transmission system operators (TSOs).

This is a reference / inventory dataset — no time dimension, but
inventory does change weekly when ENTSOG approves new operators or points.
The connector schedule is `weekly` in `config/sources.yaml`.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://transparency.entsog.eu/api/v1` |
| Path             | `/operators` |
| Method           | GET |
| Auth             | None (public) |
| Rate limit       | Not vendor-published; project default 5 req/s |
| Pagination       | `limit` + `offset` — pagination is REQUIRED for full inventory; iterate offsets until `count < limit` or fall back to `limit=-1` for a single all-records pull |
| Historical depth | n/a (snapshot) |
| Publication lag  | Vendor inventory updates daily |
| Response format  | JSON |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `limit` | int | Yes | Page size; `-1` returns all | `1000` |
| `offset` | int | No | Page offset (0-based) | `0` |
| `hasData` | bool / int | No | Sent by gridflow; ENTSOG's manual documents it for operator point directions only | `1` |

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://transparency.entsog.eu/api/v1/operators?limit=100&offset=0&hasData=1"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsog/operators/<year>/<month>/<day>/raw_<uuid>.json` (one snapshot per weekly schedule)
**Format**: Raw JSON, as-received. Immutable.
**Granularity**: One file per fetch call (full inventory).

### Bronze sample

```json
{
  "meta": {
    "limit": 100,
    "offset": 0,
    "count": 100,
    "total": 100
  },
  "operators": [
    {
      "operatorLogoUrl": "",
      "operatorKey": "---ASO-0001",
      "operatorLabel": "Aggregated Counterpa",
      "operatorLabelLong": "Aggregated Counterparties",
      "operatorTooltip": "Aggregated Counterparties|                ",
      "operatorCountryKey": "--",
      "operatorCountryLabel": "None",
      "operatorCountryFlag": null,
      "operatorTypeLabel": "ASO",
      "operatorTypeLabelLong": "Artificial Operator",
      "participates": "0",
      "membershipLabel": "Unaffiliated",
      "tsoEicCode": null,
      "tsoDisplayName": null,
      "tsoShortName": null,
      "tsoLongName": null,
      "tsoStreet": null,
      "tsoBuildingNumber": null,
      "tsoPostOfficeBox": null,
      "tsoZipCode": null,
      "tsoCity": null,
      "tsoContactName": null,
      "tsoContactPhone": null,
      "tsoContactEmail": null,
      "tsoContactUrl": null,
      "tsoContactRemarks": null,
      "tsoGeneralWebsiteUrl": null,
      "tsoGeneralWebsiteUrlRemarks": null,
      "tsoTariffInformationUrl": null,
      "tsoTariffInformationUrlRemarks": "Regulation (EU) 2017/460, Article 29&30 Information",
      "tsoTariffCalculatorUrl": null,
      "tsoTariffCalculatorUrlRemarks": "Regulation (EC) No 715/2009, Annex I Point 3.4.(6) information",
      "tsoCapacityInformationUrl": null,
      "tsoCapacityInformationUrlRemarks": null,
      "tsoGasQualityURL": null,
      "tsoGasQualityURLRemarks": "Regulation (EU) No 2015/703, Article 16 information",
      "tsoAccessConditionsUrl": null,
      "tsoAccessConditionsUrlRemarks": null,
      "tsoContractDocumentsUrl": null,
      "tsoContractDocumentsUrlRemarks": null,
      "tsoMaintainanceUrl": null,
      "tsoMaintainanceUrlRemarks": null,
      "gasDayStartHour": null,
      "gasDayStartHourRemarks": null,
      "multiAnnualContractsIsAvailable": null,
      "multiAnnualContractsRemarks": null,
      "annualContractsIsAvailable": null,
      "annualContractsRemarks": null,
      "halfAnnualContractsIsAvailable": null,
      "halfAnnualContractsRemarks": null,
      "quarterlyContractsIsAvailable": null,
      "quarterlyContractsRemarks": null,
      "monthlyContractsIsAvailable": null,
      "monthlyContractsRemarks": null,
      "dailyContractsIsAvailable": null,
      "dailyContractsRemarks": null,
      "withinDayContractsIsAvailable": null,
      "withinDayContractsRemarks": null,
      "availableContractsRemarks": null,
      "firmCapacityTariffIsApplied": null,
      "firmCapacityTariffUnit": null,
      "firmCapacityTariffRemarks": null,
      "interruptibleCapacityTariffIsApplied": null,
      "interruptibleCapacityTariffUnit": null,
      "interruptibleCapacityTariffRemarks": null,
      "auctionIsApplied": null,
      "auctionTariffIsApplied": null,
      "auctionCapacityTariffUnit": null,
      "auctionRemarks": null,
      "commodityTariffIsApplied": null,
      "commodityTariffUnit": null,
      "commodityTariffPrice": null,
      "commodityTariffRemarks": null,
      "othersTariffIsApplied": null,
      "othersTariffRemarks": null,
      "generalTariffInformationRemarks": null,
      "generalCapacityRemark": null,
      "firstComeFirstServedIsApplied": null,
      "firstComeFirstServedRemarks": null,
      "openSubscriptionWindowIsApplied": null,
      "openSubscriptionWindowRemarks": null,
      "firmTechnicalRemark": null,
      "firmBookedRemark": null,
      "fir
... [truncated]
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsog/operators/operators.parquet` (CORRECTED 2026-10-07: `silver/base.py:834` gives each dataset its own folder; `generic.py:284` writes the file there) (single-file overwrite — `reference_dataset=True`)
**Transformer class**: `gridflow.silver.entsog.generic.GenericEntsogJsonTransformer (subclass OperatorsTransformer)`
**Pydantic schema**: Generic — no Pydantic schema declared
**Dedup key** (CORRECTED 2026-10-07): vendor `id`, keep last (`silver/entsog/generic.py:193-199`); every record of this register carries one (the `dataSet` digit then the natural key). Without `id` the subset would be every column but `timestamp_utc`. Silver reads only the newest bronze capture (`generic.py:112-116,128-129,252-259`), so no capture is repeated.
**Point-in-time field** (CORRECTED 2026-10-07): `timestamp_utc` is a copy of `last_update_date_time`, the first match in `_TIMESTAMP_PRIORITY` (`generic.py:51-59,185-187`). ENTSOG's API manual does not define `lastUpdateDateTime`. In the 27 Sep 2026 capture 547 of 557 operators share one stamp (2026-09-26 22:13 UTC), so it is not a per-operator edit date, and its 2014 to 2026 range is not register history. Ten stamps carry an offset and convert correctly; `TR-TSO-0003` is sent naive (`Sep  1 2014 12:16AM`) and `silver/entsog/datetime.py:43-44` only labels it UTC (CORRECTED 2026-10-07, round 2).

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| operator_logo_url | str | Yes | operatorLogoUrl |  |
| operator_key | str | Yes | operatorKey |  |
| operator_label | str | Yes | operatorLabel |  |
| operator_label_long | str | Yes | operatorLabelLong |  |
| operator_tooltip | str | Yes | operatorTooltip |  |
| operator_country_key | str | Yes | operatorCountryKey |  |
| operator_country_label | str | Yes | operatorCountryLabel |  |
| operator_country_flag | null (sent null) | Yes | operatorCountryFlag |  |
| operator_type_label | str | Yes | operatorTypeLabel |  |
| operator_type_label_long | str | Yes | operatorTypeLabelLong |  |
| participates | str | Yes | participates |  |
| membership_label | str | Yes | membershipLabel |  |
| tso_eic_code | str | Yes | tsoEicCode |  |
| tso_display_name | null (sent null) | Yes | tsoDisplayName |  |
| tso_short_name | null (sent null) | Yes | tsoShortName |  |
| tso_long_name | null (sent null) | Yes | tsoLongName |  |
| tso_street | str | Yes | tsoStreet |  |
| tso_building_number | str | Yes | tsoBuildingNumber |  |
| tso_post_office_box | str | Yes | tsoPostOfficeBox |  |
| tso_zip_code | str | Yes | tsoZipCode |  |
| tso_city | str | Yes | tsoCity |  |
| tso_contact_name | str | Yes | tsoContactName |  |
| tso_contact_phone | str | Yes | tsoContactPhone |  |
| tso_contact_email | str | Yes | tsoContactEmail |  |
| tso_contact_url | str | Yes | tsoContactUrl |  |
| tso_contact_remarks | str | Yes | tsoContactRemarks |  |
| tso_general_website_url | str | Yes | tsoGeneralWebsiteUrl |  |
| tso_general_website_url_remarks | str | Yes | tsoGeneralWebsiteUrlRemarks |  |
| tso_tariff_information_url | str | Yes | tsoTariffInformationUrl |  |
| tso_tariff_information_url_remarks | str | Yes | tsoTariffInformationUrlRemarks |  |
| tso_tariff_calculator_url | str | Yes | tsoTariffCalculatorUrl |  |
| tso_tariff_calculator_url_remarks | str | Yes | tsoTariffCalculatorUrlRemarks |  |
| tso_capacity_information_url | str | Yes | tsoCapacityInformationUrl |  |
| tso_capacity_information_url_remarks | str | Yes | tsoCapacityInformationUrlRemarks |  |
| tso_gas_quality_url | str | Yes | tsoGasQualityURL |  |
| tso_gas_quality_url_remarks | str | Yes | tsoGasQualityURLRemarks |  |
| tso_access_conditions_url | str | Yes | tsoAccessConditionsUrl |  |
| tso_access_conditions_url_remarks | str | Yes | tsoAccessConditionsUrlRemarks |  |
| tso_contract_documents_url | str | Yes | tsoContractDocumentsUrl |  |
| tso_contract_documents_url_remarks | str | Yes | tsoContractDocumentsUrlRemarks |  |
| tso_maintainance_url | str | Yes | tsoMaintainanceUrl |  |
| tso_maintainance_url_remarks | str | Yes | tsoMaintainanceUrlRemarks |  |
| gas_day_start_hour | int | Yes | gasDayStartHour |  |
| gas_day_start_hour_remarks | str | Yes | gasDayStartHourRemarks |  |
| multi_annual_contracts_is_available | bool | Yes | multiAnnualContractsIsAvailable |  |
| multi_annual_contracts_remarks | str | Yes | multiAnnualContractsRemarks |  |
| annual_contracts_is_available | bool | Yes | annualContractsIsAvailable |  |
| annual_contracts_remarks | str | Yes | annualContractsRemarks |  |
| half_annual_contracts_is_available | bool | Yes | halfAnnualContractsIsAvailable |  |
| half_annual_contracts_remarks | str | Yes | halfAnnualContractsRemarks |  |
| quarterly_contracts_is_available | bool | Yes | quarterlyContractsIsAvailable |  |
| quarterly_contracts_remarks | str | Yes | quarterlyContractsRemarks |  |
| monthly_contracts_is_available | bool | Yes | monthlyContractsIsAvailable |  |
| monthly_contracts_remarks | str | Yes | monthlyContractsRemarks |  |
| daily_contracts_is_available | bool | Yes | dailyContractsIsAvailable |  |
| daily_contracts_remarks | str | Yes | dailyContractsRemarks |  |
| within_day_contracts_is_available | bool | Yes | withinDayContractsIsAvailable |  |
| within_day_contracts_remarks | str | Yes | withinDayContractsRemarks |  |
| available_contracts_remarks | str | Yes | availableContractsRemarks |  |
| firm_capacity_tariff_is_applied | bool | Yes | firmCapacityTariffIsApplied |  |
| firm_capacity_tariff_unit | str | Yes | firmCapacityTariffUnit |  |
| firm_capacity_tariff_remarks | str | Yes | firmCapacityTariffRemarks |  |
| interruptible_capacity_tariff_is_applied | bool | Yes | interruptibleCapacityTariffIsApplied |  |
| interruptible_capacity_tariff_unit | str | Yes | interruptibleCapacityTariffUnit |  |
| interruptible_capacity_tariff_remarks | str | Yes | interruptibleCapacityTariffRemarks |  |
| auction_is_applied | bool | Yes | auctionIsApplied |  |
| auction_tariff_is_applied | bool | Yes | auctionTariffIsApplied |  |
| auction_capacity_tariff_unit | str | Yes | auctionCapacityTariffUnit |  |
| auction_remarks | str | Yes | auctionRemarks |  |
| commodity_tariff_is_applied | bool | Yes | commodityTariffIsApplied |  |
| commodity_tariff_unit | str | Yes | commodityTariffUnit |  |
| commodity_tariff_price | float | Yes | commodityTariffPrice |  |
| commodity_tariff_remarks | str | Yes | commodityTariffRemarks |  |
| others_tariff_is_applied | bool | Yes | othersTariffIsApplied |  |
| others_tariff_remarks | str | Yes | othersTariffRemarks |  |
| general_tariff_information_remarks | str | Yes | generalTariffInformationRemarks |  |
| general_capacity_remark | str | Yes | generalCapacityRemark |  |
| first_come_first_served_is_applied | bool | Yes | firstComeFirstServedIsApplied |  |
| first_come_first_served_remarks | str | Yes | firstComeFirstServedRemarks |  |
| open_subscription_window_is_applied | bool | Yes | openSubscriptionWindowIsApplied |  |
| open_subscription_window_remarks | str | Yes | openSubscriptionWindowRemarks |  |
| firm_technical_remark | str | Yes | firmTechnicalRemark |  |
| firm_booked_remark | str | Yes | firmBookedRemark |  |
| firm_available_remark | str | Yes | firmAvailableRemark |  |
| interruptible_total_remark | str | Yes | interruptibleTotalRemark |  |
| interruptible_booked_remark | str | Yes | interruptibleBookedRemark |  |
| interruptible_available_remark | str | Yes | interruptibleAvailableRemark |  |
| tso_general_remarks | str | Yes | tsoGeneralRemarks |  |
| balancing_model | str | Yes | balancingModel |  |
| b_m_hourly_imbalance_tolerance_is_applied | bool | Yes | bMHourlyImbalanceToleranceIsApplied |  |
| b_m_hourly_imbalance_tolerance_is_information | str | Yes | bMHourlyImbalanceToleranceIsInformation |  |
| b_m_hourly_imbalance_tolerance_is_remarks | str | Yes | bMHourlyImbalanceToleranceIsRemarks |  |
| b_m_daily_imbalance_tolerance_is_applied | bool | Yes | bMDailyImbalanceToleranceIsApplied |  |
| b_m_daily_imbalance_tolerance_is_information | str | Yes | bMDailyImbalanceToleranceIsInformation |  |
| b_m_daily_imbalance_tolerance_is_remarks | str | Yes | bMDailyImbalanceToleranceIsRemarks |  |
| b_m_additional_daily_imbalance_tolerance_is_applied | bool | Yes | bMAdditionalDailyImbalanceToleranceIsApplied |  |
| b_m_additional_daily_imbalance_tolerance_is_information | str | Yes | bMAdditionalDailyImbalanceToleranceIsInformation |  |
| b_m_additional_daily_imbalance_tolerance_is_remarks | str | Yes | bMAdditionalDailyImbalanceToleranceIsRemarks |  |
| b_m_cumulated_imbalance_tolerance_is_applied | bool | Yes | bMCumulatedImbalanceToleranceIsApplied |  |
| b_m_cumulated_imbalance_tolerance_is_information | str | Yes | bMCumulatedImbalanceToleranceIsInformation |  |
| b_m_cumulated_imbalance_tolerance_is_remarks | str | Yes | bMCumulatedImbalanceToleranceIsRemarks |  |
| b_m_additional_cumulated_imbalance_tolerance_is_applied | bool | Yes | bMAdditionalCumulatedImbalanceToleranceIsApplied |  |
| b_m_additional_cumulated_imbalance_tolerance_is_information | str | Yes | bMAdditionalCumulatedImbalanceToleranceIsInformation |  |
| b_m_additional_cumulated_imbalance_tolerance_is_remarks | str | Yes | bMAdditionalCumulatedImbalanceToleranceIsRemarks |  |
| b_m_status_information | str | Yes | bMStatusInformation |  |
| b_m_status_information_frequency | str | Yes | bMStatusInformationFrequency |  |
| b_m_penalties | str | Yes | bMPenalties |  |
| b_m_cash_out_regime | str | Yes | bMCashOutRegime |  |
| b_m_remarks | str | Yes | bMRemarks |  |
| grid_transport_model_type | str | Yes | gridTransportModelType |  |
| grid_transport_model_type_remarks | str | Yes | gridTransportModelTypeRemarks |  |
| grid_conversion_factor_capacity_default | float | Yes | gridConversionFactorCapacityDefault |  |
| grid_conversion_factor_capacity_default_remaks | str | Yes | gridConversionFactorCapacityDefaultRemaks |  |
| grid_gross_calorific_value_default_value | float | Yes | gridGrossCalorificValueDefaultValue |  |
| grid_gross_calorific_value_default_value_to | float | Yes | gridGrossCalorificValueDefaultValueTo |  |
| grid_gross_calorific_value_default_unit | str | Yes | gridGrossCalorificValueDefaultUnit |  |
| grid_gross_calorific_value_default_remarks | str | Yes | gridGrossCalorificValueDefaultRemarks |  |
| grid_gas_source_default | str | Yes | gridGasSourceDefault |  |
| last_update_date_time | datetime[UTC] | Yes | lastUpdateDateTime |  |
| transparency_information_url | str | Yes | transparencyInformationURL |  |
| transparency_information_url_remarks | str | Yes | transparencyInformationUrlRemarks |  |
| transparency_guidelines_information_url | str | Yes | transparencyGuidelinesInformationURL |  |
| transparency_guidelines_information_url_remarks | str | Yes | transparencyGuidelinesInformationUrlRemarks |  |
| tso_umm_rss_feed_url_gas | str | Yes | tsoUmmRssFeedUrlGas |  |
| tso_umm_rss_feed_url_other | str | Yes | tsoUmmRssFeedUrlOther |  |
| include_umm_in_acer_rss_feed | bool | Yes | includeUmmInAcerRssFeed |  |
| id | str | int | Yes | id |  |
| data_set | str | int | Yes | dataSet |  |
| data_provider | str | No | derived | Always `entsog` |
| ingested_at | datetime[UTC] | No | derived | Wall-clock at silver write |
| timestamp_utc | datetime[UTC] | Yes | derived | Copy of `last_update_date_time` (`generic.py:185-187`); row added 2026-10-07 |
| event_time, available_at, source_run_id, dataset_version | lineage | No | derived | Pipeline lineage columns (`silver/base.py`); row added 2026-10-07 |

### Silver sample

```python
[
    {
        "operator_logo_url": "",
        "operator_key": "---ASO-0001",
        "operator_label": "Aggregated Counterpa",
        "operator_label_long": "Aggregated Counterparties",
        "operator_tooltip": "Aggregated Counterparties|                ",
        "operator_country_key": "--",
        "operator_country_label": "None",
        "operator_country_flag": null,
        "operator_type_label": "ASO",
        "operator_type_label_long": "Artificial Operator",
        "participates": "0",
        "membership_label": "Unaffiliated",
        "tso_eic_code": null,
        "tso_display_name": null,
        "tso_short_name": null,
        "tso_long_name": null,
        "tso_street": null,
        "tso_building_number": null,
        "tso_post_office_box": null,
        "tso_zip_code": null,
        "tso_city": null,
        "tso_contact_name": null,
        "tso_contact_phone": null,
        "tso_contact_email": null,
        "tso_contact_url": null,
        "tso_contact_remarks": null,
        "tso_general_website_url": null,
        "tso_general_website_url_remarks": null,
        "tso_tariff_information_url": null,
        "tso_tariff_information_url_remarks": "Regulation (EU) 2017/460, Article 29&30 Information",
        "tso_tariff_calculator_url": null,
        "tso_tariff_calculator_url_remarks": "Regulation (EC) No 715/2009, Annex I Point 3.4.(6) information",
        "tso_capacity_information_url": null,
        "tso_capacity_information_url_remarks": null,
        "tso_gas_quality_url": null,
        "tso_gas_quality_url_remarks": "Regulation (EU) No 2015/703, Article 16 information",
        "tso_access_conditions_url": null,
        "tso_access_conditions_url_remarks": null,
        "tso_contract_documents_url": null,
        "tso_contract_documents_url_remarks": null,
        "tso_maintainance_url": null,
        "tso_maintainance_url_remarks": null,
        "gas_day_start_hour": null,
        "gas_day_start_hour_remarks": null,
        "multi_annual_contracts_is_available": null,
        "multi_annual_contracts_remarks": null,
        "annual_contracts_is_available": null,
        "annual_contracts_remarks": null,
        "half_annual_contracts_is_available": null,
        "half_annual_contracts_remarks": null,
        "quarterly_contracts_is_available": null,
        "quarterly_contracts_remarks": null,
        "monthly_contracts_is_available": null,
        "monthly_contracts_remarks": null,
        "daily_contracts_is_available": null,
        "daily_contracts_remarks": null,
        "within_day_contracts_is_available": null,
        "within_day_contracts_remarks": null,
        "available_contracts_remarks": null,
        "firm_capacity_tariff_is_applied": null,
        "firm_capacity_tariff_unit": null,
        "firm_capacity_tariff_remarks": null,
        "interruptible_capacity_tariff_is_applied": null,
        "interruptible_capacity_tariff_unit": null,
        "interruptible_capacity_tariff_remarks": null,
        "auction_is_applied": null,
        "auction_tariff_is_applied": null,
        "auction_capacity_tariff_unit": null,
        "auction_remarks": null,
        "commodity_tariff_is_applied": null,
        "commodity_tariff_unit": null,
        "commodity_tariff_price": null,
        "commodity_tariff_remarks": null,
        "others_tariff_is_applied": null,
        "others_tariff_remarks": null,
        "general_tariff_information_remarks": null,
        "general_capacity_remark": null,
        "first_come_first_served_is_applied": null,
        "first_come_first_served_remarks": null,
        "open_subscription_window_is_applied": null,
        "open_subscription_window_remarks": null,
        "firm_technical_remark": null,
        "firm_booked_remark": null,
        "firm_available_remark": null,
        "interruptible_total_remark": null,
        "interruptible_booked_remark": null,
        "interruptible_available_remark": null,
        "tso_general_remarks": null,
        "balancing_model": null,
        "b_m_hourly_imbalance_tolerance_is_applied": null,
        "b_m_hourly_imbalance_tolerance_is_information": null,
        "b_m_hourly_imbalance_tolerance_is_remarks": null,
        "b_m_daily_imbalance_tolerance_is_applied": null,
        "b_m_daily_imbalance_tolerance_is_information": null,
        "b_m_daily_imbalance_tolerance_is_remarks": null,
        "b_m_additional_daily_imbalance_tolerance_is_applied": null,
        "b_m_additional_daily_imbalance_tolerance_is_information": null,
        "b_m_additional_daily_imbalance_tolerance_is_remarks": null,
        "b_m_cumulated_imbalance_tolerance_is_applied": null,
        "b_m_cumulated_imbalance_tolerance_is_information": null,
        "b_m_cumulated_imbalance_tolerance_is_remarks": null,
        "b_m_additional_cumulated_imbalance_tolerance_is_applied": null,
        "b_m_additional_cumulated_imbalance_tolerance_is_information": null,
        "b_m_additional_cumulated_imbalance_tolerance_is_remarks": null,
        "b_m_status_information": null,
        "b_m_status_information_frequency": null,
        "b_m_penalties": null,
        "b_m_cash_out_regime": null,
        "b_m_remarks": null,
        "grid_transport_model_type": null,
        "grid_transport_model_type_remarks": null,
        "grid_conversion_factor_capacity_default": null,
        "grid_conversion_factor_capacity_default_remaks": null,
        "grid_gross_calorific_value_default_value": null,
        "grid_gross_calorific_value_default_value_to": null,
        "grid_gross_calorific_value_default_unit": null,
        "grid_gross_calorific_value_default_remarks": null,
        "grid_gas_source_default": null,
        "last_update_date_time": "2015-11-09T00:11:00+01:00",
        "transparency_information_url": null,
        "transparency_information_url_remarks": null,
        "transparency_guidelines_information_url": null,
        "transparency_guidelines_information_url_remarks": "Regulation (EC) No 715/2009, Annex I Chapter 3 information",
        "tso_umm_rss_feed_url_gas": null,
        "tso_umm_rss_feed_url_other": null,
        "include_umm_in_acer_rss_feed": null,
        "id": "1---ASO-0001",
        "data_set": "1",
        "data_provider": "entsog",
        "ingested_at": "2026-05-08T18:00:00+00:00"
    }
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **No date filter — pagination required**: reference endpoints accept `limit` + `offset`. Default `limit` is small; pass `limit=1000` (or the full inventory size) and iterate offset for full extracts.
- **`hasData=1`** (CORRECTED 2026-10-07): ENTSOG's API manual (v2.1, section 2.4.7) documents it for operator point directions only: it keeps the directions of TSOs that publish their REG715 data. gridflow also sends it to `/operators`, where the manual does not document it; the 27 Sep 2026 response still lists storage, LNG, hydrogen and electricity operators. The claim that it drops dormant validity-period rows is unverified.
- **Field-case duplicates**: `isCAMRelevant` (uppercase CAM) appears here while `isCamRelevant` appears in operationalData. Generic silver coalesces both into `is_cam_relevant`.
- **Reference data refresh schedule**: weekly in `config/sources.yaml`. Static-ish, but new points and operator changes do appear when ENTSOG approves them.
- **`bzKey` separators**: balancing zone keys often contain trailing dashes (`UK---------`) — preserve as-is, do not strip.


---

## Implementation delta

- **Pagination required**: full inventory may exceed default page size. Connector defaults to `limit=-1`; live validation used `limit=100` to demonstrate paging shape. For production fetches, prefer `limit=-1` or iterate `offset` in chunks.
- **`reference_dataset=True` write path**: silver writes directly to `<silver_dir>/<dataset>.parquet`, bypassing the date-partitioned layout used by operational datasets.

---

## Modelling notes

TODO — primarily used as join keys for operational datasets.

---

## Links

- [Official API docs (PDF)](https://transparency.entsog.eu/api/archiveDirectories/8/api-manual/TP_REG715_Documentation_TP_API%20-%20v2.1.pdf)
- `src/gridflow/connectors/entsog/endpoints.py`
- `src/gridflow/silver/entsog/generic.py`
- `src/gridflow/schemas/entsog.py`
- Gold view/builder
