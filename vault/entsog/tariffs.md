---
source: entsog
dataset_key: tariffs
vendor: ENTSOG Transparency Platform
last_verified: 2026-05-08
layer_coverage: bronze, silver
page:
  title: Transmission tariffs and simulated costs
  summary: >-
    Capacity tariffs of European gas transmission operators per interconnection point, direction
    and product, plus simulated costs per product, from ENTSOG's Transparency Platform.
  facts:
    vendor: "ENTSOG Transparency Platform, endpoints `tariffsFulls` and `tariffsSimulations`"
    cadence: One-year tariff periods, requested one day at a time
    grain: One row per operator, point, direction, capacity type, product and product period
  landscape: gas
  what_it_is: >-
    Each operator's published capacity price per interconnection point, direction, firm or
    interruptible capacity and product, in its own currency and in euro. The connector sends
    `countryKey=UK`, but rows cover operators across Europe. ENTSOG describes the simulation as
    "costs for flowing 1 GWh/d/y at IP"; each operator sets its basis. Silver repeats every
    record once per fetched day.
  how_used:
    - Comparing yearly firm prices of the pipeline operators at Bacton and Zeebrugge.
    - Pricing a monthly or daily booking against the yearly product at one point.
    - Reading an operator's simulated cost beside its tariff, with its cost remark.
  chart:
    type: bar
    silver: entsog/tariffs
    value: applicable_tariff_per_eurk_wh_h_value
    filter:
      - {column: product_type, op: eq, value: Yearly}
      - {column: tariff_capacity_type, op: eq, value: Firm}
      - {column: applicable_tariff_per_eurk_wh_h_unit, op: eq, value: "Euro/(kWh/h)/y"}
      - column: operator_point_direction
        op: in
        value:
          - uk-tso-0004itp-00207exit
          - uk-tso-0004itp-00207entry
          - uk-tso-0003itp-00005entry
          - uk-tso-0003itp-00005exit
          - uk-tso-0003itp-00061entry
          - uk-tso-0003itp-00061exit
          - be-tso-0001itp-00061entry
          - be-tso-0001itp-00061exit
    dedup: {on: [id], order_by: id}
    group: operator_point_direction
    group_map:
      uk-tso-0004itp-00207exit: bbl_bacton_exit
      uk-tso-0004itp-00207entry: bbl_bacton_entry
      uk-tso-0003itp-00005entry: iuk_bacton_entry
      uk-tso-0003itp-00005exit: iuk_bacton_exit
      uk-tso-0003itp-00061entry: iuk_zeebrugge_entry
      uk-tso-0003itp-00061exit: iuk_zeebrugge_exit
      be-tso-0001itp-00061entry: fluxys_zeebrugge_entry
      be-tso-0001itp-00061exit: fluxys_zeebrugge_exit
    aggregation: max
    sort: value_desc
    unit: EUR/(kWh/h)/y
  chart_view:
    title: Pipeline operators' yearly firm tariffs, Bacton and Zeebrugge
    caption: >-
      Silver `entsog/tariffs`, requested for 1 to 5 August 2026: yearly firm products of BBL,
      Interconnector and Fluxys Belgium, euro per kWh/h per year, repeats removed. National
      Gas TSO excluded: its Moffat exit price, 0.008326, is labelled both yearly and monthly.
    alt: >-
      Horizontal bar chart of yearly firm capacity tariffs in euro per kWh/h per year, from
      entsog/tariffs, requested for 1 to 5 August 2026. Fluxys Belgium's Zeebrugge IZT entry is
      highest at 19.32. BBL company's Bacton entry and exit both read 8.76, Fluxys Belgium's
      Zeebrugge IZT exit 8.112, and Interconnector's four bars, Bacton and Zeebrugge in both
      directions, 3.637 each.
    key:
      - {series: fluxys_zeebrugge_entry, label: "Fluxys, IZT entry", codes: "ITP-00061 entry", paint: olive, note: "Fluxys Belgium at ENTSOG's point Zeebrugge IZT, from `IUK` to `BeLux`; period from 1 January 2026."}
      - {series: bbl_bacton_entry, label: "BBL, Bacton entry", codes: "ITP-00207 entry", paint: petrol, note: "BBL company, from `UK` to `Netherlands` as sent; tariff period from 1 October 2025."}
      - {series: bbl_bacton_exit, label: "BBL, Bacton exit", codes: "ITP-00207 exit", paint: petrol, note: "From `Netherlands` to `UK` as sent; the same price as the entry bar."}
      - {series: fluxys_zeebrugge_exit, label: "Fluxys, IZT exit", codes: "ITP-00061 exit", paint: olive, note: "Zeebrugge IZT, from `BeLux` to `IUK` as sent; tariff period from 1 January 2026."}
      - {series: iuk_bacton_entry, label: "IUK, Bacton entry", codes: "ITP-00005 entry", paint: horizon, note: "Operator Interconnector, whose zone ENTSOG labels `IUK`; 3.138445 GBP as sent, euro column 3.63709."}
      - {series: iuk_bacton_exit, label: "IUK, Bacton exit", codes: "ITP-00005 exit", paint: horizon}
      - {series: iuk_zeebrugge_entry, label: "IUK, IZT entry", codes: "ITP-00061 entry", paint: horizon}
      - {series: iuk_zeebrugge_exit, label: "IUK, IZT exit", codes: "ITP-00061 exit", paint: horizon, note: "Zeebrugge IZT; Interconnector sends one price for both points and both directions."}
  raw_feed:
    note: >-
      One request per day to `tariffsFulls`, with `countryKey=UK`; the response still holds
      operators across Europe. Silver turns `N/A` prices into nulls and repeats the records in
      every fetched day's file.
    requests:
      - "GET https://transparency.entsog.eu/api/v1/tariffsFulls?limit=-1&timeZone=UCT&from=2026-08-01&to=2026-08-01&countryKey=UK"
    commands:
      - {run: gridflow ingest entsog tariffs --start 2026-08-01 --end 2026-08-02, comment: "bronze, end exclusive; repeat per member"}
      - {run: gridflow transform entsog tariffs --start 2026-08-01 --end 2026-08-01, comment: "silver, one file per day"}
  record:
    select:
      filter:
        - {column: operator_point_direction, op: in, value: [uk-tso-0004itp-00207exit, uk-tso-0003itp-00005exit]}
        - {column: tariff_capacity_type, op: eq, value: Firm}
        - {column: product_type, op: in, value: [Yearly, Quarterly, Monthly, Daily]}
        - {column: product_period_from, op: eq, value: "2025-10-01T04:00:00"}
      dedup: {on: [id], order_by: id}
      order_by: [operator_key, display_order]
      columns: [operator_key, point_key, direction_key, tariff_capacity_type, product_type, product_period_from, applicable_tariff_per_eurk_wh_h_value, applicable_tariff_per_eurk_wh_h_unit, product_period_to, operator_currency, applicable_tariff_per_local_currency_k_wh_h_value, applicable_tariff_per_local_currency_k_wh_h_unit, multiplier, operator, point_label]
    key: [operator_key, point_key, direction_key, tariff_capacity_type, product_type, product_period_from]
    caption: "Firm daily, monthly, quarterly and yearly products from 1 October 2025, at two Bacton exits."
    fields:
      operator_key: ENTSOG key of the operator publishing the tariff
      point_key: "ENTSOG point key, such as `ITP-00207` for Bacton (BBL)"
      direction_key: "`entry` or `exit`, from the publishing operator's side, as sent"
      tariff_capacity_type: "`Firm` or `Interruptible` capacity, as sent"
      product_type: "Capacity product: `Yearly`, `Quarterly`, `Monthly`, `Daily` or `WithinDay`"
      product_period_from: "Start of the period this price applies to, from `productPeriodFrom`, in UTC"
      applicable_tariff_per_eurk_wh_h_value: "Price in euro per kWh/h of capacity, as ENTSOG sends it; null when `N/A`"
      applicable_tariff_per_eurk_wh_h_unit: "Unit of the euro price as sent, such as `Euro/(kWh/h)/y`"
      product_period_to: "End of that period, from `productPeriodTo`, in UTC"
      operator_currency: The operator's own currency, as sent
      applicable_tariff_per_local_currency_k_wh_h_value: "The price in the operator's currency; equal to euro for euro operators"
      applicable_tariff_per_local_currency_k_wh_h_unit: "Unit of that price as sent, such as `GBP/(kWh/h)/y`"
      multiplier: "The operator's multiplier for the product, kept as text; `N/A` when none"
      operator: Name of the operator publishing the tariff, as sent
      point_label: ENTSOG's name for the point, as sent
      timestamp_utc: "Start of the tariff period, copied from `period_from`; not a fetch time"
      period_from: "Tariff period start as sent in `periodFrom`, converted to UTC"
      period_to: "Tariff period end as sent in `periodTo`, converted to UTC"
      indicator: Field shared with operational data; null in these rows
      period_type: Field shared with operational data; null in these rows
      operator_label: "Operator label field; null in these rows, see `operator`"
      tso_eic_code: Energy Identification Code of the publishing operator, as sent
      unit: Field shared with operational data; null in these rows
      value: Field shared with operational data; null in these rows
      id: "Vendor record id, the deduplication key: item, capacity type, product, keys and dates"
      operator_point_direction: Operator, point and direction keys joined in lowercase, as sent
      country_code: "Country code as sent; BBL company's rows carry `NL`"
      connection: "The two operators either side of the point, as sent"
      connection_remarks: Remark on the connection; null in these rows
      from_bz: "Balancing zone on the from side, as sent, such as `Netherlands`"
      to_bz: "Balancing zone on the to side, as sent, such as `UK`"
      tariff_capacity_unit: "Capacity unit as sent, `kWh/h` here; prices come per kWh/h and kWh/d"
      multiplier_factor_remarks: Remark on the multiplier; empty in these rows
      discount_for_interruptible_capacity_value: Discount for interruptible capacity, as sent; null in these rows
      discount_for_interruptible_capacity_remarks: Remark on that discount; empty in these rows
      seasonal_factor: "The operator's seasonal factor, kept as text; `N/A` in these rows"
      seasonal_factor_remarks: Remark on the seasonal factor; empty in these rows
      applicable_tariff_per_local_currency_k_wh_d_value: Operator-currency price per kWh/d of capacity; a 24th of the kWh/h price here
      applicable_tariff_per_local_currency_k_wh_d_unit: "Unit of that price as sent, such as `EUR/(kWh/d)/y`"
      applicable_tariff_per_eurk_wh_d_value: The kWh/d price in euro, as ENTSOG sends it
      applicable_tariff_per_eurk_wh_d_unit: Unit of the euro kWh/d price, as sent
      applicable_tariff_remarks: Remark on the tariff; empty in these rows
      applicable_tariff_in_common_unit_value: "ENTSOG's figure in `Euro/(kWh/h)/d`; how it is derived differs by operator"
      applicable_tariff_in_common_unit_unit: Unit of that figure, as sent
      applicable_tariff_in_common_unit_remarks: Remark on that figure; null in these rows
      applicable_commodity_tariff_local_currency: "Commodity tariff in the operator's currency, kept as text; `N/A` here"
      applicable_commodity_tariff_euro: "Commodity tariff in euro, kept as text; `N/A` here"
      applicable_commodity_tariff_remarks: The operator's remark on the commodity tariff, as sent
      exchange_rate_reference_date: "Reference date of the euro exchange rate, kept as text; `N/A` for euro"
      remarks: General remark; null in these rows
      tariff_period_remarks: Remark on the tariff period; null in these rows
      display_order: Vendor display order of the product, as sent
      point_type: ENTSOG's point type; null in these rows
      id_point_type: ENTSOG's point type code; null in these rows
      is_archived: Vendor archive flag, as sent
      data_set: "Vendor `dataSet` code, as sent; ENTSOG's meaning for it is not documented here"
      tso_item_identifier: The operator's own identifier for the point, as sent
      direction: Field shared with operational data; null in these rows
      item_remarks: Field shared with operational data; null in these rows
      general_remarks: Field shared with operational data; null in these rows
      last_update_date_time: "The vendor's `lastUpdateDateTime` for this tariff, converted to UTC"
      is_unlimited: Field shared with operational data; null in these rows
      interruption_type: Field shared with operational data; null in these rows
      restoration_information: Field shared with operational data; null in these rows
      capacity_type: Field shared with operational data; null in these rows
      capacity_booking_status: Field shared with operational data; null in these rows
      flow_status: Field shared with operational data; null in these rows
  notebook:
    lead: >-
      Reads `silver_entsog_tariffs`, lineage columns dropped, where `timestamp_utc`, the tariff
      period start, falls between the dates given, ends included; widen them for later periods.
      The query cell keeps one row per `id`, dropping the daily copies.
    cells:
      - |
        tariffs = data.entsog.query("tariffs", "2025-10-01", "2026-04-01").drop_duplicates("id")
        tariffs["period_from"].dt.tz_convert("UTC").value_counts().sort_index()
      - |
        tariffs["operator_currency"].value_counts()
      - |
        ng = tariffs[(tariffs.operator_point_direction == "uk-tso-0001itp-00090exit")
                     & (tariffs.tariff_capacity_type == "Firm")
                     & tariffs.product_type.isin(["Yearly", "Monthly"])]
        ng[["product_type", "applicable_tariff_per_eurk_wh_h_value",
            "applicable_tariff_per_eurk_wh_h_unit"]].drop_duplicates()
      - |
        bbl = tariffs[(tariffs.operator_point_direction == "uk-tso-0004itp-00207exit")
                      & (tariffs.tariff_capacity_type == "Firm") & (tariffs.product_type == "Monthly")]
        bbl = bbl.assign(month=bbl.product_period_from.dt.tz_convert("UTC")).sort_values("month")
        bbl.plot(x="month", y="applicable_tariff_per_eurk_wh_h_value", drawstyle="steps-post",
                 color="#155A6E", legend=False, ylabel="EUR/(kWh/h)/m", figsize=(8, 3.5))
    needs: the tariffs fetched for one day, such as 1 August 2026
    plot_alt: >-
      Step plot of BBL company's firm monthly product at Bacton exit, in euro per kWh/h per month,
      for October 2025 to September 2026. It sits between 1.008 and 1.116 from October to March,
      then between 1.44 and 1.488 from April.
  related:
    - {dataset: entsog/physical_flows, note: Daily flows at the interconnection points these tariffs price}
    - {dataset: entsog/firm_booked, note: "Firm capacity booked at the Bacton and Moffat points"}
    - {dataset: entsog/operator_point_directions, note: "The register of the operator, point and direction keys"}
  family:
    slug: tariffs-and-simulations
    members:
      - dataset: tariffs
        differs: "Capacity prices per product and product period, in local currency and euro"
        request: "GET https://transparency.entsog.eu/api/v1/tariffsFulls?limit=-1&timeZone=UCT&from=2026-08-01&to=2026-08-01&countryKey=UK"
      - dataset: tariff_simulations
        differs: "Simulated cost, kept as text; `N/A` when not sent; currency only, no capacity unit"
        request: "GET https://transparency.entsog.eu/api/v1/tariffsSimulations?limit=-1&timeZone=UCT&from=2026-08-01&to=2026-08-01&countryKey=UK"
---

# ENTSOG — Tariffs

## Overview

Full tariff data per operator and point — unit prices, multipliers, currency.

---

## API endpoint

| Property         | Value |
|------------------|-------|
| Base URL         | `https://transparency.entsog.eu/api/v1` |
| Path             | `/tariffsFulls` |
| Method           | GET |
| Auth             | None (public) |
| Rate limit       | Not vendor-published; project default 5 req/s |
| Pagination       | `limit` + `offset` |
| Historical depth | TODO |
| Publication lag  | TODO |
| Response format  | JSON |
| Time zone | `timeZone=UCT` (ENTSOG's spelling) |

### Query parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `from` | date | Yes | Window start | `2026-05-06` |
| `to` | date | Yes | Window end | `2026-05-06` |
| `timeZone` | str | Yes | `UCT` | `UCT` |
| `countryKey` | str | No | The connector sends `UK` (`connectors/entsog/endpoints.py:187,196`); it does not limit the response to UK operators (see Known issues) | `UK` |
| `limit` | int | No | `-1` returns all | `-1` |

The connector sends one request per covered UTC day with `from` = `to` = that day (`connectors/entsog/client.py:78-102`), so `--end` on `gridflow ingest` is exclusive.

### Working curl example

```bash
curl --ssl-no-revoke -fsS \
  -H "Accept: application/json" \
  "https://transparency.entsog.eu/api/v1/tariffsFulls?from=2026-05-06&to=2026-05-06&timeZone=UCT&countryKey=UK&forceDownload=true&limit=1000"
```

---

## Bronze layer

**Path pattern**: `{data_root}/bronze/entsog/tariffs/<year>/<month>/<day>/raw_<uuid>.json`
**Format**: Raw JSON, as-received. Immutable.
**Granularity**: One file per fetch call.

### Bronze sample

```json
{
  "meta": {
    "limit": 1000,
    "offset": 0,
    "count": 1,
    "total": 1000
  },
  "tariffsFulls": [
    {
      "directionKey": "exit",
      "operator": "Transgaz",
      "operatorPointDirection": "ro-tso-0001itp-00153exit",
      "countryCode": null,
      "connection": null,
      "connectionRemarks": null,
      "fromBZ": null,
      "toBZ": null,
      "productPeriodFrom": null,
      "productPeriodTo": null,
      "tariffCapacityType": null,
      "tariffCapacityUnit": "kWh/h",
      "productType": "Yearly",
      "multiplier": null,
      "multiplierFactorRemarks": null,
      "discountForInterruptibleCapacityValue": null,
      "discountForInterruptibleCapacityRemarks": null,
      "seasonalFactor": null,
      "seasonalFactorRemarks": null,
      "operatorCurrency": "RON",
      "applicableTariffPerLocalCurrencyKWhDValue": null,
      "applicableTariffPerLocalCurrencyKWhDUnit": null,
      "applicableTariffPerLocalCurrencyKWhHValue": null,
      "applicableTariffPerLocalCurrencyKWhHUnit": null,
      "applicableTariffPerEURKWhDValue": null,
      "applicableTariffPerEURKWhDUnit": null,
      "applicableTariffPerEURKWhHValue": null,
      "applicableTariffPerEURKWhHUnit": null,
      "applicableTariffRemarks": null,
      "applicableTariffInCommonUnitValue": null,
      "applicableTariffInCommonUnitUnit": null,
      "applicableTariffInCommonUnitRemarks": null,
      "applicableCommodityTariffLocalCurrency": "0.0018",
      "applicableCommodityTariffEURO": "0.00035677",
      "applicableCommodityTariffRemarks": null,
      "exchangeRateReferenceDate": "2025-06-06T22:25:29+02:00",
      "remarks": null,
      "tariffPeriodRemarks": null,
      "displayOrder": null,
      "pointType": null,
      "idPointType": null,
      "isArchived": null,
      "id": "121Z0000000002798RO-TSO-0001ITP-00153exit2025-10-01T04:00:00+00:00__2026-10-01T04:00:00+00:00",
      "dataSet": 1,
      "indicator": null,
      "periodType": null,
      "periodFrom": "2025-10-01T06:00:00+02:00",
      "periodTo": "2026-10-01T06:00:00+02:00",
      "operatorKey": "RO-TSO-0001",
      "tsoEicCode": "21X-RO-A-A0A0A-S",
      "operatorLabel": null,
      "pointKey": "ITP-00153",
      "pointLabel": "Ruse (BG) / Giurgiu (RO)",
      "tsoItemIdentifier": "21Z0000000002798",
      "direction": null,
      "unit": null,
      "itemRemarks": null,
      "generalRemarks": null,
      "value": null,
      "lastUpdateDateTime": "2025-06-07T06:56:45+02:00",
      "isUnlimited": null,
      "interruptionType": null,
      "restorationInformation": null,
      "capacityType": null,
      "capacityBookingStatus": null,
      "flowStatus": null
    }
  ]
}
```

---

## Silver layer

**Path pattern**: `{data_root}/silver/entsog/tariffs/year=YYYY/month=MM/tariffs_YYYYMMDD.parquet`
**Transformer class**: `gridflow.silver.entsog.generic.GenericEntsogJsonTransformer (subclass TariffsTransformer)`
**Pydantic schema**: Generic — no Pydantic schema declared
**Dedup key**: the vendor `id`, `keep="last"`, within one bronze day's read (`silver/entsog/generic.py:193-199`). There is no dedup across days, so every fetched day's partition holds the full set again: 2026-08-01 to 05 hold 12,244 ids a day and 61,220 silver rows, five copies identical apart from `ingested_at` and `available_at`. Within one day the key (`operator_key`, `point_key`, `direction_key`, `tariff_capacity_type`, `product_type`, `product_period_from`) is unique (project check).
**Bronze read filter**: none. `tariffs` and `tariff_simulations` are exempt from the gas-day filter the other generic ENTSOG datasets apply (`generic.py:297-317`, VTA-ENTSOG-TARIFF-01), so silver keeps every bronze record: 12,244 bronze records and 12,244 silver rows on each of 2026-08-01 to 05.
**Point-in-time field**: none used by the pipeline. `timestamp_utc` is a copy of `period_from`, the start of the one-year tariff period, not a fetch or publication time (`silver/entsog/generic.py:181-187`). `last_update_date_time` is the vendor's `lastUpdateDateTime` in UTC; `ingested_at` is the silver transform time (`generic.py:201-206`). The fetched day appears only in the partition file name.

### Silver schema

| Field | Python type | Nullable | Source field | Notes |
|-------|-------------|----------|--------------|-------|
| timestamp_utc | datetime[UTC] | Yes | derived | Copy of `period_from`, the tariff period start (`generic.py:185-187`) |
| period_from | datetime[UTC] | Yes | periodFrom | Tariff period start, UTC |
| period_to | datetime[UTC] | Yes | periodTo |  |
| indicator | null (no values) | Yes | indicator |  |
| period_type | null (no values) | Yes | periodType |  |
| operator_key | str | Yes | operatorKey |  |
| operator_label | null (no values) | Yes | operatorLabel |  |
| tso_eic_code | str | Yes | tsoEicCode |  |
| point_key | str | Yes | pointKey |  |
| point_label | str | Yes | pointLabel |  |
| direction_key | str | Yes | directionKey |  |
| unit | null (no values) | Yes | unit |  |
| value | float | Yes | value |  |
| id | str | Yes | id | Dedup key within a day |
| operator | str | Yes | operator |  |
| operator_point_direction | str | Yes | operatorPointDirection |  |
| country_code | str | Yes | countryCode |  |
| connection | str | Yes | connection |  |
| connection_remarks | null (no values) | Yes | connectionRemarks |  |
| from_bz | str | Yes | fromBZ |  |
| to_bz | str | Yes | toBZ |  |
| product_period_from | datetime[UTC] | Yes | productPeriodFrom | Parsed to UTC (`_DATETIME_COLUMNS`) |
| product_period_to | datetime[UTC] | Yes | productPeriodTo | Parsed to UTC (`_DATETIME_COLUMNS`) |
| tariff_capacity_type | str | Yes | tariffCapacityType |  |
| tariff_capacity_unit | str | Yes | tariffCapacityUnit |  |
| product_type | str | Yes | productType |  |
| multiplier | str | Yes | multiplier | Text; `N/A` placeholders |
| multiplier_factor_remarks | str | Yes | multiplierFactorRemarks |  |
| discount_for_interruptible_capacity_value | float | Yes | discountForInterruptibleCapacityValue |  |
| discount_for_interruptible_capacity_remarks | str | Yes | discountForInterruptibleCapacityRemarks |  |
| seasonal_factor | str | Yes | seasonalFactor | Text; `N/A` placeholders |
| seasonal_factor_remarks | str | Yes | seasonalFactorRemarks |  |
| operator_currency | str | Yes | operatorCurrency |  |
| applicable_tariff_per_local_currency_k_wh_d_value | float | Yes | applicableTariffPerLocalCurrencyKWhDValue |  |
| applicable_tariff_per_local_currency_k_wh_d_unit | str | Yes | applicableTariffPerLocalCurrencyKWhDUnit |  |
| applicable_tariff_per_local_currency_k_wh_h_value | float | Yes | applicableTariffPerLocalCurrencyKWhHValue |  |
| applicable_tariff_per_local_currency_k_wh_h_unit | str | Yes | applicableTariffPerLocalCurrencyKWhHUnit |  |
| applicable_tariff_per_eurk_wh_d_value | float | Yes | applicableTariffPerEURKWhDValue |  |
| applicable_tariff_per_eurk_wh_d_unit | str | Yes | applicableTariffPerEURKWhDUnit |  |
| applicable_tariff_per_eurk_wh_h_value | float | Yes | applicableTariffPerEURKWhHValue |  |
| applicable_tariff_per_eurk_wh_h_unit | str | Yes | applicableTariffPerEURKWhHUnit |  |
| applicable_tariff_remarks | str | Yes | applicableTariffRemarks |  |
| applicable_tariff_in_common_unit_value | float | Yes | applicableTariffInCommonUnitValue | Basis differs by operator; see Known issues |
| applicable_tariff_in_common_unit_unit | str | Yes | applicableTariffInCommonUnitUnit |  |
| applicable_tariff_in_common_unit_remarks | str | Yes | applicableTariffInCommonUnitRemarks |  |
| applicable_commodity_tariff_local_currency | str | Yes | applicableCommodityTariffLocalCurrency | Text; `N/A` placeholders |
| applicable_commodity_tariff_euro | str | Yes | applicableCommodityTariffEURO | Text; `N/A` placeholders |
| applicable_commodity_tariff_remarks | str | Yes | applicableCommodityTariffRemarks |  |
| exchange_rate_reference_date | str | Yes | exchangeRateReferenceDate | Kept as text, as sent (`N/A` for euro operators) |
| remarks | str | Yes | remarks |  |
| tariff_period_remarks | str | Yes | tariffPeriodRemarks |  |
| display_order | int | Yes | displayOrder |  |
| point_type | null (no values) | Yes | pointType |  |
| id_point_type | null (no values) | Yes | idPointType |  |
| is_archived | bool | Yes | isArchived |  |
| data_set | int | Yes | dataSet |  |
| tso_item_identifier | str | Yes | tsoItemIdentifier |  |
| direction | null (no values) | Yes | direction |  |
| item_remarks | null (no values) | Yes | itemRemarks |  |
| general_remarks | null (no values) | Yes | generalRemarks |  |
| last_update_date_time | datetime[UTC] | Yes | lastUpdateDateTime |  |
| is_unlimited | null (no values) | Yes | isUnlimited |  |
| interruption_type | null (no values) | Yes | interruptionType |  |
| restoration_information | null (no values) | Yes | restorationInformation |  |
| capacity_type | null (no values) | Yes | capacityType |  |
| capacity_booking_status | null (no values) | Yes | capacityBookingStatus |  |
| flow_status | null (no values) | Yes | flowStatus |  |
| data_provider | str | No | derived | Always `entsog` |
| ingested_at | datetime[UTC] | No | derived | Wall-clock at silver write (`generic.py:201-206`) |
| event_time | datetime[UTC] | No | derived | Lineage; equals `period_from` here |
| available_at | datetime[UTC] | No | derived | Lineage |
| source_run_id | str | No | derived | Lineage |
| dataset_version | str | No | derived | Lineage, `1.0.0` |

### Silver sample

Real silver row (BBL company, Bacton (BBL) exit, firm yearly; 2026-08-01 partition), stamps in UTC.

```python
[
    {
        "timestamp_utc": "2025-10-01T04:00:00+00:00",
        "period_from": "2025-10-01T04:00:00+00:00",
        "period_to": "2026-10-01T04:00:00+00:00",
        "indicator": null,
        "period_type": null,
        "operator_key": "UK-TSO-0004",
        "operator_label": null,
        "tso_eic_code": "21X-NL-B-A0A0A-Q",
        "point_key": "ITP-00207",
        "point_label": "Bacton (BBL)",
        "direction_key": "exit",
        "unit": null,
        "value": null,
        "id": "121Z000000000088FFirmYearlyUK-TSO-0004ITP-00207exit2025-10-01T04:00:00+00:00__2025-10-01T04:00:00+00:00__2026-10-01T04:00:00+00:00",
        "operator": "BBL company",
        "operator_point_direction": "uk-tso-0004itp-00207exit",
        "country_code": "NL",
        "connection": " BBL company -> National Gas TSO",
        "connection_remarks": null,
        "from_bz": "Netherlands",
        "to_bz": "UK",
        "product_period_from": "2025-10-01T04:00:00+00:00",
        "product_period_to": "2026-10-01T04:00:00+00:00",
        "tariff_capacity_type": "Firm",
        "tariff_capacity_unit": "kWh/h",
        "product_type": "Yearly",
        "multiplier": "N/A",
        "multiplier_factor_remarks": "",
        "discount_for_interruptible_capacity_value": null,
        "discount_for_interruptible_capacity_remarks": "",
        "seasonal_factor": "N/A",
        "seasonal_factor_remarks": "",
        "operator_currency": "EUR",
        "applicable_tariff_per_local_currency_k_wh_d_value": 0.365,
        "applicable_tariff_per_local_currency_k_wh_d_unit": "EUR/(kWh/d)/y",
        "applicable_tariff_per_local_currency_k_wh_h_value": 8.76,
        "applicable_tariff_per_local_currency_k_wh_h_unit": "EUR/(kWh/h)/y",
        "applicable_tariff_per_eurk_wh_d_value": 0.365,
        "applicable_tariff_per_eurk_wh_d_unit": "Euro/(kWh/d)/y",
        "applicable_tariff_per_eurk_wh_h_value": 8.76,
        "applicable_tariff_per_eurk_wh_h_unit": "Euro/(kWh/h)/y",
        "applicable_tariff_remarks": "",
        "applicable_tariff_in_common_unit_value": 0.024,
        "applicable_tariff_in_common_unit_unit": "Euro/(kWh/h)/d",
        "applicable_tariff_in_common_unit_remarks": null,
        "applicable_commodity_tariff_local_currency": "N/A",
        "applicable_commodity_tariff_euro": "N/A",
        "applicable_commodity_tariff_remarks": "Commodity charge is calculated on a daily basis (see BBL website).",
        "exchange_rate_reference_date": "N/A",
        "remarks": null,
        "tariff_period_remarks": null,
        "display_order": 1,
        "point_type": null,
        "id_point_type": null,
        "is_archived": false,
        "data_set": 1,
        "tso_item_identifier": "21Z000000000088F",
        "direction": null,
        "item_remarks": null,
        "general_remarks": null,
        "last_update_date_time": "2025-07-01T12:08:36+00:00",
        "is_unlimited": null,
        "interruption_type": null,
        "restoration_information": null,
        "capacity_type": null,
        "capacity_booking_status": null,
        "flow_status": null,
        "data_provider": "entsog",
        "ingested_at": "2026-08-16T14:21:42.074899+00:00",
        "event_time": "2025-10-01T04:00:00+00:00",
        "available_at": "2026-08-16T14:21:39.925099+00:00",
        "source_run_id": "6bb01195-8d19-421c-9fa2-8380c9b83102",
        "dataset_version": "1.0.0"
    }
]
```

---

## Gold layer

None implemented.

---

## Known issues and gotchas

- **`countryKey=UK` does not limit the response**: the connector sends `countryKey=UK` (`connectors/entsog/endpoints.py:187,196`) and the response's `meta.query` echoes it, yet each 2026-08-01 to 05 body holds 12,244 records (`meta.count` = `meta.total`) for operators in 21 country codes, AT to UK. What the parameter filters on is not documented here.
- **Mixed currencies and units**: `operatorCurrency` varies (RON, EUR, GBP, etc.). Both local-currency and EUR-converted columns are present (`applicableTariffPerEURKWhDValue` etc.). `exchangeRateReferenceDate` records when the EUR conversion was sampled. Currencies in 2026-08 responses: EUR, HUF, RON, BGN, PLN, CZK, DKK, GBP. For euro operators the euro columns equal the local ones and `exchangeRateReferenceDate` is `N/A`; silver keeps that column as text (it is not in `_DATETIME_COLUMNS`, `generic.py:34-50`).
- **Most rows have many null fields**: tariffs are sparse — different tariff lines populate different cost columns. Don't drop nulls. In 2026-08, 827 of 12,244 records carry none of the five tariff values: 816 arrive with the five prices as the string `N/A`, which silver casts to null (`cast(pl.Float64, strict=False)`, `generic.py:189-191`), and 11 evergreen Transgaz records send the price fields as null. `multiplier`, `seasonal_factor`, the commodity columns and `exchangeRateReferenceDate` keep `N/A` as text, so one table mixes both conventions.
- **Periods**: each record belongs to a one-year tariff period (`periodFrom`/`periodTo`); in 2026-08 responses these start 1 October 2025 (3,351 records), 1 January 2026 (8,715) or 1 April 2026 (178). Products subdivide it with `productPeriodFrom`/`productPeriodTo` (monthly products one record per month, quarterly per quarter). `productPeriodFrom`/`productPeriodTo` may be null for "evergreen" tariff entries (2026-08: 11 Transgaz yearly records).
- **Silver repeats the tariff set once per fetched day**: see Dedup key. `data.entsog.query()` filters on `timestamp_utc` (the tariff period start, `schema_manifest.py:222-223`) and keeps `ingested_at`, so it returns every copy. Deduplicate on `id` before counting or aggregating.
- **Units**: every priced record gives the tariff per kWh/d and per kWh/h of capacity, in local currency and in euro; the kWh/h figure is 24 times the kWh/d figure on the priced 2026-08 records (project check). The unit's last part follows the product (`/y`, `/q`, `/m`, `/d`; `/h` for within-day), except 72 within-day records sent with `/d` (Snam Rete Gas, GASCADE and five others).
- **Common-unit column is not comparable across operators**: `applicableTariffInCommonUnitValue` (`Euro/(kWh/h)/d`, `/h` for within-day) is derived differently by operator. For yearly products most send the yearly euro kWh/h price divided by 365; Fluxys Belgium divides by 8,760; Energinet and a few others use other factors; Transgaz's common figure is 24 times its euro kWh/h price on its yearly records (ratio 23.99996 to 23.99998; none of its 902 prices is zero) (project check, 2026-08).
- **National Gas TSO figures**: 25 of its 70 records carry a price. Its Moffat exit firm price is 0.000299 GBP/(kWh/d) on the yearly product (unit `/y`) and on every monthly product (unit `/m`), so its unit suffixes do not follow its products. Unexplained; the front-end chart leaves National Gas TSO out.
- **Numbers kept as text**: `multiplier`, `seasonal_factor`, `applicable_commodity_tariff_local_currency` and `applicable_commodity_tariff_euro` miss `_looks_numeric` (`generic.py:60-69,384-387`) and stay strings, with `N/A` placeholders.

- **Indicator string is exact-case**: the connector sends the exact human-readable form (`Physical Flow`, `Nomination`, `Available through UIOLI long-term`). Sending lowercase or hyphen variants returns 404.
- **`timeZone=UCT` (note typo)**: ENTSOG documents the parameter as `timeZone=UCT` rather than `UTC`. The connector spells it the vendor's way. The response `meta.timezone` echoes back `CET` regardless of the request value.
- **`pointDirection` filter**: built as `operatorKey + pointKey + directionKey` concatenated with no separator (e.g. `UK-TSO-0001ITP-00005exit`). Multi-value lists are comma-joined.
- **Missing data returns HTTP 404**: ENTSOG returns `HTTP 404` with body `{"message":"No result found"}` when an indicator/window/point combination has no rows. This is the vendor's empty convention, not a true failure. The connector's retry policy must let 404 surface.
- **Field-case duplicates**: live records may carry both `isCamRelevant` and `isCAMRelevant` shape (or `isCmpRelevant`/`isCMPRelevant`) depending on indicator. The generic silver transformer `_normalise_column_names` collapses these via `pl.coalesce` into one snake_case column.
- **Datetime placeholders**: `lastUpdateDateTime` and `originalPeriodFrom` may be empty strings, `"-"`, `"N/A"`, or human-formatted strings (`"Jan 15 2024 06:00AM"`). `parse_entsog_datetime` returns `None` for unparseable values rather than raising.
- **`directionKey` casing varies**: lowercase (`entry`/`exit`) in `/operationalData`; capitalised (`Exit`) in `/cmpUnsuccessfulRequests`. Don't compare with `==` across families.
- **Period offset is +02:00 (CET)**: even with `timeZone=UCT`, `periodFrom` carries `+02:00` (CEST in summer / `+01:00` in winter). The silver transformer's `parse_entsog_datetime` converts to UTC.


---

## Implementation delta

- **Vendor empty convention**: HTTP 404 + `{"message":"No result found"}`.
- **Generic transformer**: dynamic schema; columns derived from live response.


---

## Modelling notes

Deduplicate on `id` first. Compare like with like: one `product_type`, one `tariff_capacity_type`, one price column and its unit, and the euro columns only when currencies differ (ENTSOG's conversion, dated by `exchange_rate_reference_date`). Do not compare operators on the common-unit column. Within one fetched day the key is (`operator_key`, `point_key`, `direction_key`, `tariff_capacity_type`, `product_type`, `product_period_from`).

---

## Links

- [Official API docs (PDF)](https://transparency.entsog.eu/api/archiveDirectories/8/api-manual/TP_REG715_Documentation_TP_API%20-%20v2.1.pdf)
- `src/gridflow/connectors/entsog/endpoints.py`
- `src/gridflow/silver/entsog/generic.py`
- `src/gridflow/schemas/entsog.py`
- Gold view/builder
