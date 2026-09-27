# v5 data matrix (Phase 22)

Generated 2026-09-27T06:16:06Z by `.planning/v5/scripts/build_data_matrix.py` (offline; no vendor API calls). Canonical vault = quant-vault `master` @ `e2a96e019`. Silver = `C:\gridflow-data\silver`. Machine-readable twin: `DATA-MATRIX.json` (full columns, schema diffs, sections).

## Headline

- Vault dataset notes: **165** (elexon 33, entsoe 49, entsog 33, gie 8, neso 33, neso_data_portal 3, openmeteo 6).
- Notes with local silver: **149/165** (elexon 33/33, entsoe 36/49, entsog 32/33, gie 6/8, neso 33/33, neso_data_portal 3/3, openmeteo 6/6).
- gridflow: 163 datasets in `config/sources.yaml`, 164 silver transformers.
- Registry vs vault: agree: 163; partial: not in sources.yaml: 1; site only (no vault note, not in gridflow): 29; vault only (gridflow has no config or transformer): 1.
- Vault silver-schema table vs gridflow pydantic schema: bitemporal_only: 74; differs: 25; match: 48; no_code_schema_or_silver: 2; no_silver_section: 1; no_vault_table: 14; range_notation: 1.
- Chart series: 85. Authored overrides: 130. Rendered pages: 194 (of which coming-soon stubs: 29).
- Mirror byte-identical to canonical `master`: 145; differs: 20.
- Vault validator last run: 2026-06-15T22:09:01.969587Z.

Columns: **cfg** in `sources.yaml` · **tr** silver transformer · **silver** rows / first / last (designated date column) · **lv** vault `last_verified` · **vs** vault schema table vs code (`=` match, `≈` differs only in published_at/ingested_at, `=*` range-notation table, `≠` differs, `–` no table, `?` nothing to compare) · **mir** mirror byte-identical · **ch** chart series · **ov** authored override · **stub** coming-soon stub · **agree** registry vs vault.

## elexon (33 rows)

| dataset | gridflow key | cfg | tr | schema class | silver rows | first | last | lv | vs | mir | ch | ov | stub | agree |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|
| agpt | elexon/agpt | y | y | ElexonAGPT | 7,392 | 2026-07-31 | 2026-09-21 | 2026-05-08 | = | y | y | n | n | agree |
| agws | elexon/agws | y | y | ElexonAGWS | 256,983 | 2021-08-31 | 2026-09-26 | 2026-05-08 | = | n | y | n | n | agree |
| atl | elexon/atl | y | y | ElexonATL | 403 | 2026-08-01 | 2026-09-21 | 2026-05-08 | = | y | y | n | n | agree |
| bmunits_reference | elexon/bmunits_reference | y | y | ElexonBMUnit | 3,014 | 2026-09-26 | 2026-09-26 | 2026-05-08 | = | y | n | y | n | agree |
| boal | elexon/boal | y | y | ElexonBOAL | 199,565 | 2026-08-01 | 2026-09-22 | 2026-05-21 | = | y | n | y | n | agree |
| disbsad | elexon/disbsad | y | y | ElexonDISBSAD | 8,116 | 2026-08-01 | 2026-09-22 | 2026-05-21 | = | y | y | y | n | agree |
| fou2t14d | elexon/fou2t14d | y | y | ElexonFOU2T14D | 83,239 | 2026-08-03 | 2026-10-06 | 2026-05-08 | = | y | n | n | n | agree |
| freq | elexon/freq | y | y | ElexonFrequency | 80,654 | 2026-08-01 | 2026-09-22 | 2026-05-09 | = | y | y | y | n | agree |
| fuelhh | elexon/fuelhh | y | y | ElexonFuelHH | 1,686,317 | 2021-09-01 | 2026-09-26 | 2026-09-07 | = | n | y | y | n | agree |
| fuelinst | elexon/fuelinst | y | y | ElexonFuelInst | 80,920 | 2026-08-01 | 2026-09-22 | 2026-05-08 | = | y | y | y | n | agree |
| imbalngc | elexon/imbalngc | y | y | ElexonImbalNGC | 1,442 | 2026-08-01 | 2026-09-23 | 2026-05-08 | = | y | y | n | n | agree |
| inddem | elexon/inddem | y | y | ElexonIndDem | 25,956 | 2026-08-01 | 2026-09-23 | 2026-05-08 | = | y | y | n | n | agree |
| indgen | elexon/indgen | y | y | ElexonIndGen | 25,956 | 2026-08-01 | 2026-09-23 | 2026-05-08 | = | y | y | n | n | agree |
| indo | elexon/indo | y | y | ElexonINDO | 88,315 | 2021-08-31 | 2026-09-22 | 2026-05-08 | = | n | y | n | n | agree |
| indod | elexon/indod | y | y | ElexonINDOD | 14 | 2026-08-01 | 2026-09-21 | 2026-05-08 | ≈ | y | y | y | n | agree |
| itsdo | elexon/itsdo | y | y | ElexonITSDO | 674 | 2026-08-01 | 2026-09-22 | 2026-07-30 | = | n | y | n | n | agree |
| lolpdrm | elexon/lolpdrm | y | y | ElexonLOLPDRM | 1,428 | 2026-08-01 | 2026-09-23 | 2026-07-30 | = | n | y | n | n | agree |
| market_depth | elexon/market_depth | y | y | ElexonMarketDepth | 768 | 2026-08-01 | 2026-09-22 | 2026-05-08 | = | y | y | n | n | agree |
| melngc | elexon/melngc | y | y | ElexonMelNGC | 1,442 | 2026-08-01 | 2026-09-23 | 2026-05-08 | = | y | y | n | n | agree |
| mid | elexon/mid | y | y | ElexonMID | 176,286 | 2021-09-01 | 2026-09-22 | 2026-09-07 | = | n | y | y | n | agree |
| ndf | elexon/ndf | y | y | ElexonDemandForecast | 39,424 | 2026-08-01 | 2026-09-23 | 2026-07-31 | = | n | y | n | n | agree |
| ndfd | elexon/ndfd | y | y | ElexonDemandForecast | 156 | 2026-08-03 | 2026-10-05 | 2026-05-08 | = | y | n | n | n | agree |
| netbsad | elexon/netbsad | y | y | ElexonNETBSAD | 686 | 2026-08-01 | 2026-09-22 | 2026-05-21 | = | y | n | n | n | agree |
| nonbm | elexon/nonbm | y | y | ElexonNonBM | 5 | 2026-04-01 | 2026-04-01 | 2026-05-08 | = | y | n | n | n | agree |
| pn | elexon/pn | y | y | ElexonPN | 1,850,886 | 2026-08-01 | 2026-09-22 | 2026-05-08 | = | y | y | y | n | agree |
| remit | elexon/remit | y | y | ElexonREMIT | 2,291 | 2026-08-01 | 2026-09-21 | 2026-05-09 | = | y | y | n | n | agree |
| soso | elexon/soso | y | y | ElexonSOSO | 20,256 | 2026-08-01 | 2026-09-22 | 2026-05-09 | ≈ | y | y | n | n | agree |
| system_prices | elexon/system_prices | y | y | ElexonSystemPrice | 96,793 | 2021-09-01 | 2026-09-22 | 2026-09-07 | ≈ | n | y | y | n | agree |
| temp | elexon/temp | y | y | ElexonTemp | 14 | 2026-08-01 | 2026-09-21 | 2026-05-21 | = | y | y | y | n | agree |
| tsdf | elexon/tsdf | y | y | ElexonTSDF | 25,956 | 2026-08-01 | 2026-09-23 | 2026-07-31 | ≈ | n | y | y | n | agree |
| tsdfd | elexon/tsdfd | y | y | ElexonTSDFD | 156 | 2026-08-03 | 2026-10-05 | 2026-05-08 | = | y | n | y | n | agree |
| uou2t14d | elexon/uou2t14d | y | y | ElexonUOU2T14D | 92,232 | 2026-08-03 | 2026-10-06 | 2026-05-21 | = | y | n | n | n | agree |
| windfor | elexon/windfor | y | y | ElexonWindForecast | 860,715 | 2021-09-01 | 2026-09-28 | 2026-05-08 | = | y | y | n | n | agree |

## entsoe (49 rows)

| dataset | gridflow key | cfg | tr | schema class | silver rows | first | last | lv | vs | mir | ch | ov | stub | agree |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|
| activated_balancing_prices | entsoe/activated_balancing_prices | y | y | EntsoeActivatedBalancingPrices | 0 |  |  | 2026-05-08 | ≈ | y | n | n | n | agree |
| activated_balancing_qty | entsoe/activated_balancing_qty | n | y | EntsoeActivatedBalancingQty | 0 |  |  | 2026-05-11 | ≈ | y | n | y | n | partial: not in sources.yaml |
| actual_generation | entsoe/actual_generation | y | y | EntsoeActualGeneration | 100,831 | 2026-08-01 | 2026-09-20 | 2026-05-08 | ≈ | y | y | y | n | agree |
| actual_generation_units | entsoe/actual_generation_units | y | y | EntsoeActualGenerationUnits | 229,612 | 2026-08-01 | 2026-09-21 | 2026-05-08 | ≈ | y | y | y | n | agree |
| actual_load | entsoe/actual_load | y | y | EntsoeActualLoad | 9,191 | 2026-08-01 | 2026-09-20 | 2026-05-08 | ≈ | y | y | y | n | agree |
| aggregated_balancing_energy_bids | entsoe/aggregated_balancing_energy_bids | y | y | EntsoeBalancingEnergyBid | 768 | 2026-09-22 | 2026-09-25 | 2026-05-08 | ≈ | n | n | y | n | agree |
| auction_revenue | entsoe/auction_revenue | y | y | EntsoeTransmissionMarketAmount | 1,296 | 2026-07-31 | 2026-09-22 | 2026-05-08 | ≈ | y | y | y | n | agree |
| balancing_energy_bids | entsoe/balancing_energy_bids | y | y | EntsoeBalancingEnergyBid | 81,563 | 2026-08-01 | 2026-09-21 | 2026-05-08 | ≈ | n | y | y | n | agree |
| balancing_financial_expenses_income | entsoe/balancing_financial_expenses_income | y | y | EntsoeBalancingFinancial | 0 |  |  | 2026-05-09 | ≈ | n | n | n | n | agree |
| commercial_schedules | entsoe/commercial_schedules | y | y | EntsoeTransmissionMarketQuantity | 9,110 | 2026-08-01 | 2026-09-21 | 2026-05-11 | ≈ | y | y | y | n | agree |
| commercial_schedules_net_positions |  | n | n |  | 0 |  |  | 2026-05-11 | – | y | n | y | n | vault only (gridflow has no config or transformer) |
| congestion_income | entsoe/congestion_income | y | y | EntsoeTransmissionMarketAmount | 0 |  |  | 2026-05-08 | ≈ | y | n | y | n | agree |
| congestion_management_costs | entsoe/congestion_management_costs | y | y | EntsoeTransmissionMarketAmount | 744 | 2026-06-30 | 2026-07-31 | 2026-05-08 | ≈ | n | n | y | n | agree |
| contracted_reserves | entsoe/contracted_reserves | y | y | EntsoeContractedReserves | 0 |  |  | 2026-05-08 | ≈ | y | n | y | n | agree |
| countertrading | entsoe/countertrading | y | y | EntsoeTransmissionMarketQuantity | 12 | 2026-09-22 | 2026-09-25 | 2026-05-08 | – | y | n | y | n | agree |
| cross_border_flows | entsoe/cross_border_flows | y | y | EntsoeCrossborderFlow | 10,855 | 2026-08-01 | 2026-09-20 | 2026-05-08 | ≈ | y | y | y | n | agree |
| cross_zonal_balancing_capacity | entsoe/cross_zonal_balancing_capacity | y | y | EntsoeCrossZonalBalancingCapacity | 0 |  |  | 2026-05-08 | ≈ | y | n | y | n | agree |
| current_balancing_state | entsoe/current_balancing_state | y | y | EntsoeBalancingState | 9,414 | 2026-08-01 | 2026-08-25 | 2026-05-08 | ≈ | y | y | y | n | agree |
| day_ahead_prices | entsoe/day_ahead_prices | y | y | EntsoeDayAheadPrice | 10,054 | 2026-08-01 | 2026-09-21 | 2026-05-08 | ≈ | y | y | n | n | agree |
| dc_link_intraday_transfer_limits | entsoe/dc_link_intraday_transfer_limits | y | y | EntsoeTransmissionMarketQuantity | 24 | 2026-08-01 | 2026-08-05 | 2026-05-08 | ≈ | y | y | y | n | agree |
| forecast_margin | entsoe/forecast_margin | y | y | EntsoeForecastMargin | 48 | 2025-12-31 | 2025-12-31 | 2026-05-08 | ≈ | y | n | y | n | agree |
| generation_forecast | entsoe/generation_forecast | y | y | EntsoeGenerationForecast | 5,830 | 2026-08-01 | 2026-09-21 | 2026-05-08 | = | y | y | y | n | agree |
| generation_units_master_data | entsoe/generation_units_master_data | y | y | EntsoeGenerationUnitsMasterData | 1,317 | 1960-01-01 | 2027-01-01 | 2026-05-08 | = | y | n | y | n | agree |
| imbalance_prices | entsoe/imbalance_prices | y | y | EntsoeImbalancePrices | 0 |  |  | 2026-05-08 | ≈ | y | n | n | n | agree |
| imbalance_volume | entsoe/imbalance_volume | y | y | EntsoeImbalanceVolume | 0 |  |  | 2026-05-08 | ≈ | y | n | y | n | agree |
| installed_capacity | entsoe/installed_capacity | y | y | EntsoeInstalledCapacity | 804 | 2025-12-31 | 2025-12-31 | 2026-05-08 | ≈ | y | n | y | n | agree |
| installed_capacity_units | entsoe/installed_capacity_units | y | y | EntsoeInstalledCapacityUnits | 7,668 | 2025-12-31 | 2025-12-31 | 2026-05-08 | ≈ | y | n | y | n | agree |
| load_forecast | entsoe/load_forecast | y | y | EntsoeLoadForecast | 9,216 | 2026-08-01 | 2026-09-20 | 2026-05-08 | ≈ | y | y | y | n | agree |
| load_forecast_monthly | entsoe/load_forecast_monthly | y | y | EntsoeLoadForecast | 48 | 2026-07-26 | 2026-09-13 | 2026-05-08 | ≈ | y | n | n | n | agree |
| load_forecast_weekly | entsoe/load_forecast_weekly | y | y | EntsoeLoadForecastWeekly | 48 | 2026-07-31 | 2026-09-13 | 2026-05-08 | ≈ | y | n | y | n | agree |
| load_forecast_yearly | entsoe/load_forecast_yearly | y | y | EntsoeLoadForecast | 48 | 2026-07-26 | 2026-09-13 | 2026-05-08 | ≈ | y | n | n | n | agree |
| net_positions | entsoe/net_positions | y | y | EntsoeTransmissionMarketQuantity | 5,376 | 2026-08-01 | 2026-09-21 | 2026-05-08 | – | y | y | y | n | agree |
| net_transfer_capacity | entsoe/net_transfer_capacity | y | y | EntsoeNetTransferCapacity | 2,736 | 2026-08-01 | 2026-09-21 | 2026-05-08 | ≈ | y | y | y | n | agree |
| offered_transfer_capacity_continuous | entsoe/offered_transfer_capacity_continuous | y | y | EntsoeTransmissionMarketQuantity | 0 |  |  | 2026-05-08 | – | y | n | y | n | agree |
| offered_transfer_capacity_explicit | entsoe/offered_transfer_capacity_explicit | y | y | EntsoeTransmissionMarketQuantity | 0 |  |  | 2026-05-08 | – | y | n | y | n | agree |
| offered_transfer_capacity_implicit | entsoe/offered_transfer_capacity_implicit | y | y | EntsoeTransmissionMarketQuantity | 0 |  |  | 2026-05-08 | – | y | n | y | n | agree |
| outages_consumption | entsoe/outages_consumption | y | y | EntsoeOutagesConsumption | 1,738 | 2026-08-01 | 2026-09-20 | 2026-05-08 | ≈ | y | n | y | n | agree |
| outages_generation | entsoe/outages_generation | y | y | EntsoeOutagesGeneration | 11,011 | 2015-11-15 | 2069-06-26 | 2026-05-08 | ≈ | y | n | y | n | agree |
| outages_offshore_grid | entsoe/outages_offshore_grid | y | y | EntsoeOutagesOffshoreGrid | 4 | 2026-09-16 | 2026-09-16 | 2026-05-08 | ≈ | y | n | y | n | agree |
| outages_production | entsoe/outages_production | y | y | EntsoeOutagesProduction | 3,551 | 2024-12-31 | 2077-01-02 | 2026-05-08 | ≈ | y | y | n | n | agree |
| outages_transmission | entsoe/outages_transmission | y | y | EntsoeOutagesTransmission | 3,981 | 2025-01-11 | 2052-10-08 | 2026-05-08 | ≈ | y | y | y | n | agree |
| procured_balancing_capacity | entsoe/procured_balancing_capacity | y | y | EntsoeBalancingCapacity | 440 | 2026-08-01 | 2026-08-05 | 2026-05-08 | ≈ | y | y | y | n | agree |
| redispatching_cross_border | entsoe/redispatching_cross_border | y | y | EntsoeTransmissionMarketQuantity | 288 | 2026-07-06 | 2026-07-09 | 2026-05-08 | – | y | n | y | n | agree |
| redispatching_internal | entsoe/redispatching_internal | y | y | EntsoeTransmissionMarketQuantity | 1,909 | 2026-08-01 | 2026-09-21 | 2026-05-08 | – | y | y | y | n | agree |
| total_capacity_allocated | entsoe/total_capacity_allocated | y | y | EntsoeTransmissionMarketQuantity | 1,922 | 2026-08-01 | 2026-09-21 | 2026-05-08 | – | y | y | y | n | agree |
| total_nominated_capacity | entsoe/total_nominated_capacity | y | y | EntsoeTransmissionMarketQuantity | 2,352 | 2026-08-01 | 2026-09-21 | 2026-05-08 | – | y | y | y | n | agree |
| transfer_capacity_use | entsoe/transfer_capacity_use | y | y | EntsoeTransmissionMarketQuantity | 0 |  |  | 2026-05-08 | – | y | n | y | n | agree |
| water_reservoirs | entsoe/water_reservoirs | y | y | EntsoeWaterReservoirs | 18 | 2026-07-26 | 2026-09-13 | 2026-05-08 | ≈ | y | n | y | n | agree |
| wind_solar_forecast | entsoe/wind_solar_forecast | y | y | EntsoeWindSolarForecast | 22,665 | 2026-08-01 | 2026-09-20 | 2026-05-08 | = | y | y | n | n | agree |

## entsog (33 rows)

| dataset | gridflow key | cfg | tr | schema class | silver rows | first | last | lv | vs | mir | ch | ov | stub | agree |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|
| aggregate_interconnections | entsog/aggregate_interconnections | y | y | dynamic | 27 | 2026-09-27 | 2026-09-27 | 2026-05-08 | = | n | n | y | n | agree |
| aggregated_physical_flows | entsog/aggregated_physical_flows | y | y | dynamic | 42 | 2026-08-01 | 2026-09-21 | 2026-05-08 | ≠ | y | y | y | n | agree |
| allocations | entsog/allocations | y | y | dynamic | 98 | 2026-08-01 | 2026-09-21 | 2026-05-08 | ≠ | y | y | y | n | agree |
| available_through_oversubscription | entsog/available_through_oversubscription | y | y | dynamic | 55 | 2026-07-31 | 2026-08-04 | 2026-05-08 | ≠ | y | n | y | n | agree |
| available_through_surrender | entsog/available_through_surrender | y | y | dynamic | 55 | 2026-07-31 | 2026-08-04 | 2026-05-08 | ≠ | y | n | y | n | agree |
| available_through_uioli_long_term | entsog/available_through_uioli_long_term | y | y | dynamic | 55 | 2026-07-31 | 2026-08-04 | 2026-05-08 | ≠ | y | n | y | n | agree |
| available_through_uioli_short_term | entsog/available_through_uioli_short_term | y | y | dynamic | 55 | 2026-07-31 | 2026-08-04 | 2026-05-08 | ≠ | y | n | y | n | agree |
| balancing_zones | entsog/balancing_zones | y | y | dynamic | 48 | 2026-09-27 | 2026-09-27 | 2026-05-08 | = | n | n | y | n | agree |
| cmp_auction_premiums | entsog/cmp_auction_premiums | y | y | dynamic | 5,035 | 2026-07-31 | 2026-08-04 | 2026-05-08 | ≠ | y | n | y | n | agree |
| cmp_unavailable_firm_capacity | entsog/cmp_unavailable_firm_capacity | y | y | dynamic | 2,920 | 2026-07-31 | 2026-08-04 | 2026-05-08 | ≠ | y | n | y | n | agree |
| cmp_unsuccessful_requests | entsog/cmp_unsuccessful_requests | y | y | dynamic | 5,197 |  |  | 2026-05-08 | ≠ | y | n | y | n | agree |
| connection_points | entsog/connection_points | y | y | dynamic | 788 | 2026-09-27 | 2026-09-27 | 2026-05-08 | = | n | n | y | n | agree |
| firm_available | entsog/firm_available | y | y | dynamic | 59 | 2026-08-01 | 2026-09-21 | 2026-05-08 | ≠ | y | y | y | n | agree |
| firm_booked | entsog/firm_booked | y | y | dynamic | 59 | 2026-08-01 | 2026-09-21 | 2026-05-08 | ≠ | y | y | y | n | agree |
| firm_technical | entsog/firm_technical | y | y | dynamic | 28 | 2026-08-01 | 2026-09-21 | 2026-05-08 | ≠ | y | n | y | n | agree |
| gcv | entsog/gcv | y | y | dynamic | 98 | 2026-08-01 | 2026-09-21 | 2026-05-08 | ≠ | y | y | y | n | agree |
| hydrogen_content | entsog/hydrogen_content | y | y | dynamic | 28 | 2026-08-01 | 2026-09-21 | 2026-06-04 | – | y | y | y | n | agree |
| interconnections | entsog/interconnections | y | y | dynamic | 194 |  |  | 2026-05-08 | ≠ | y | n | y | n | agree |
| interruptible_available | entsog/interruptible_available | y | y | dynamic | 21 | 2026-08-01 | 2026-09-21 | 2026-05-08 | ≠ | y | n | y | n | agree |
| interruptible_booked | entsog/interruptible_booked | y | y | dynamic | 20 | 2026-08-01 | 2026-09-21 | 2026-05-08 | ≠ | y | n | y | n | agree |
| interruptible_total | entsog/interruptible_total | y | y | dynamic | 21 | 2026-08-01 | 2026-09-21 | 2026-05-08 | ≠ | y | n | y | n | agree |
| interruptions | entsog/interruptions | y | y | dynamic | 0 |  |  | 2026-06-04 | – | y | n | y | n | agree |
| methane_content | entsog/methane_content | y | y | dynamic | 42 | 2026-08-01 | 2026-09-21 | 2026-06-04 | – | y | y | y | n | agree |
| nominations | entsog/nominations | y | y | dynamic | 98 | 2026-08-01 | 2026-09-21 | 2026-05-08 | ≠ | y | y | y | n | agree |
| operator_point_directions | entsog/operator_point_directions | y | y | dynamic | 1,225 |  |  | 2026-05-08 | ≠ | y | n | y | n | agree |
| operators | entsog/operators | y | y | dynamic | 557 | 2014-09-01 | 2026-09-26 | 2026-05-08 | ≠ | y | n | y | n | agree |
| oxygen_content | entsog/oxygen_content | y | y | dynamic | 28 | 2026-08-01 | 2026-09-21 | 2026-06-04 | – | y | n | y | n | agree |
| physical_flows | entsog/physical_flows | y | y | EntsogPhysicalFlow | 13,764 | 2026-07-31 | 2026-09-21 | 2026-05-08 | = | y | y | y | n | agree |
| renominations | entsog/renominations | y | y | dynamic | 98 | 2026-08-01 | 2026-09-21 | 2026-05-08 | ≠ | y | y | y | n | agree |
| tariff_simulations | entsog/tariff_simulations | y | y | dynamic | 13,910 | 2025-10-01 | 2026-04-01 | 2026-05-08 | ≠ | y | n | y | n | agree |
| tariffs | entsog/tariffs | y | y | dynamic | 61,220 | 2025-10-01 | 2026-04-01 | 2026-05-08 | ≠ | y | n | y | n | agree |
| urgent_market_messages | entsog/urgent_market_messages | y | y | dynamic | 133 | 2021-01-07 | 2026-09-22 | 2026-05-08 | ≠ | y | n | y | n | agree |
| wobbe_index | entsog/wobbe_index | y | y | dynamic | 126 | 2026-08-01 | 2026-09-21 | 2026-05-08 | ≠ | y | y | y | n | agree |

## gie (8 rows)

| dataset | gridflow key | cfg | tr | schema class | silver rows | first | last | lv | vs | mir | ch | ov | stub | agree |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|
| about_listing | gie_agsi/about_listing | y | y | dynamic | 1,665 | 2026-09-27 | 2026-09-27 | 2026-05-08 | = | y | n | y | n | agree |
| about_summary | gie_agsi/about_summary | y | y | dynamic | 1,665 | 2026-09-27 | 2026-09-27 | 2026-05-08 | = | y | n | y | n | agree |
| lng | gie_alsi/lng | y | y | LNGTerminal | 120 | 2026-08-01 | 2026-09-22 | 2026-05-11 | ≈ | y | y | y | n | agree |
| news | gie_agsi/news | y | y | dynamic | 0 |  |  | 2026-05-08 | ? | y | n | y | n | agree |
| news_item | gie_agsi/news_item | y | y | dynamic | 0 |  |  | 2026-05-08 | ? | y | n | y | n | agree |
| storage | gie_agsi/storage | y | y | GasStorage | 135 | 2026-08-01 | 2026-09-22 | 2026-07-25 | ≈ | y | y | y | n | agree |
| storage_reports | gie_agsi/storage_reports | y | y | dynamic | 15 | 2026-08-01 | 2026-09-22 | 2026-05-08 | = | y | y | y | n | agree |
| unavailability | gie_agsi/unavailability | y | y | dynamic | 1,705 | 2026-08-16 | 2026-08-16 | 2026-05-08 | = | y | n | y | n | agree |

## neso (33 rows)

| dataset | gridflow key | cfg | tr | schema class | silver rows | first | last | lv | vs | mir | ch | ov | stub | agree |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|
| carbon_intensity | neso/carbon_intensity | y | y | CarbonIntensity | 674 | 2026-07-31 | 2026-09-21 | 2026-05-08 | ≈ | n | y | y | n | agree |
| generation | neso/generation | y | y | GenerationMix | 6,066 | 2026-07-31 | 2026-09-21 | 2026-05-08 | ≈ | y | y | y | n | agree |
| generation_current | neso/generation_current | y | y | GenerationMix | 9 | 2026-09-27 | 2026-09-27 | 2026-05-08 | ≈ | y | n | y | n | agree |
| generation_pt24h | neso/generation_pt24h | y | y | GenerationMix | 441 | 2026-07-30 | 2026-07-31 | 2026-05-08 | ≈ | y | n | y | n | agree |
| intensity_at | neso/intensity_at | y | y | CarbonIntensity | 1 | 2026-07-31 | 2026-07-31 | 2026-05-08 | ≈ | y | n | y | n | agree |
| intensity_current | neso/intensity_current | y | y | CarbonIntensity | 1 | 2026-09-26 | 2026-09-26 | 2026-05-08 | ≈ | y | n | y | n | agree |
| intensity_date | neso/intensity_date | y | y | CarbonIntensity | 240 | 2026-07-31 | 2026-08-05 | 2026-05-08 | ≈ | y | y | y | n | agree |
| intensity_factors | neso/intensity_factors | y | y | CarbonIntensityFactor | 14 | 2026-09-26 | 2026-09-26 | 2026-05-08 | ≈ | y | n | y | n | agree |
| intensity_fw24h | neso/intensity_fw24h | y | y | CarbonIntensity | 49 | 2026-07-31 | 2026-08-01 | 2026-05-08 | ≈ | y | y | y | n | agree |
| intensity_fw48h | neso/intensity_fw48h | y | y | CarbonIntensity | 97 | 2026-07-31 | 2026-08-02 | 2026-05-08 | ≈ | y | y | y | n | agree |
| intensity_period | neso/intensity_period | y | y | CarbonIntensity | 240 | 2026-07-31 | 2026-08-05 | 2026-05-08 | ≈ | y | y | y | n | agree |
| intensity_pt24h | neso/intensity_pt24h | y | y | CarbonIntensity | 49 | 2026-07-30 | 2026-07-31 | 2026-05-08 | ≈ | y | n | y | n | agree |
| intensity_stats | neso/intensity_stats | y | y | CarbonIntensityStats | 1 | 2026-08-01 | 2026-08-01 | 2026-05-08 | ≈ | y | n | y | n | agree |
| intensity_stats_block | neso/intensity_stats_block | y | y | CarbonIntensityStats | 14 | 2026-08-01 | 2026-09-21 | 2026-05-08 | ≈ | y | y | y | n | agree |
| intensity_today | neso/intensity_today | y | y | CarbonIntensity | 48 | 2026-09-26 | 2026-09-27 | 2026-05-08 | ≈ | y | n | y | n | agree |
| regional_current | neso/regional_current | y | y | RegionalIntensity | 162 | 2026-09-27 | 2026-09-27 | 2026-05-09 | ≈ | y | n | y | n | agree |
| regional_england | neso/regional_england | y | y | RegionalIntensity | 9 | 2026-09-27 | 2026-09-27 | 2026-05-08 | ≈ | y | n | y | n | agree |
| regional_intensity | neso/regional_intensity | y | y | RegionalIntensity | 109,188 | 2026-07-31 | 2026-09-21 | 2026-05-09 | ≈ | y | y | y | n | agree |
| regional_intensity_fw24h | neso/regional_intensity_fw24h | y | y | RegionalIntensity | 7,938 | 2026-07-31 | 2026-08-01 | 2026-05-09 | ≈ | y | y | y | n | agree |
| regional_intensity_fw24h_postcode | neso/regional_intensity_fw24h_postcode | y | y | RegionalIntensity | 441 | 2026-07-31 | 2026-08-01 | 2026-05-08 | ≈ | y | y | y | n | agree |
| regional_intensity_fw24h_regionid | neso/regional_intensity_fw24h_regionid | y | y | RegionalIntensity | 441 | 2026-07-31 | 2026-08-01 | 2026-05-08 | ≈ | y | y | y | n | agree |
| regional_intensity_fw48h | neso/regional_intensity_fw48h | y | y | RegionalIntensity | 15,714 | 2026-07-31 | 2026-08-02 | 2026-05-09 | ≈ | y | y | y | n | agree |
| regional_intensity_fw48h_postcode | neso/regional_intensity_fw48h_postcode | y | y | RegionalIntensity | 873 | 2026-07-31 | 2026-08-02 | 2026-05-08 | ≈ | y | y | y | n | agree |
| regional_intensity_fw48h_regionid | neso/regional_intensity_fw48h_regionid | y | y | RegionalIntensity | 873 | 2026-07-31 | 2026-08-02 | 2026-05-08 | ≈ | y | y | y | n | agree |
| regional_intensity_postcode | neso/regional_intensity_postcode | y | y | RegionalIntensity | 2,169 | 2026-07-31 | 2026-08-05 | 2026-05-08 | ≈ | y | y | y | n | agree |
| regional_intensity_pt24h | neso/regional_intensity_pt24h | y | y | RegionalIntensity | 7,938 | 2026-07-30 | 2026-07-31 | 2026-05-09 | ≈ | y | n | y | n | agree |
| regional_intensity_pt24h_postcode | neso/regional_intensity_pt24h_postcode | y | y | RegionalIntensity | 441 | 2026-07-30 | 2026-07-31 | 2026-05-08 | ≈ | y | n | y | n | agree |
| regional_intensity_pt24h_regionid | neso/regional_intensity_pt24h_regionid | y | y | RegionalIntensity | 441 | 2026-07-30 | 2026-07-31 | 2026-05-08 | ≈ | y | n | y | n | agree |
| regional_intensity_regionid | neso/regional_intensity_regionid | y | y | RegionalIntensity | 2,169 | 2026-07-31 | 2026-08-05 | 2026-05-08 | ≈ | y | y | y | n | agree |
| regional_postcode | neso/regional_postcode | y | y | RegionalIntensity | 9 | 2026-09-27 | 2026-09-27 | 2026-05-08 | ≈ | y | n | y | n | agree |
| regional_regionid | neso/regional_regionid | y | y | RegionalIntensity | 9 | 2026-09-27 | 2026-09-27 | 2026-05-08 | ≈ | y | n | y | n | agree |
| regional_scotland | neso/regional_scotland | y | y | RegionalIntensity | 9 | 2026-09-27 | 2026-09-27 | 2026-05-08 | ≈ | y | n | y | n | agree |
| regional_wales | neso/regional_wales | y | y | RegionalIntensity | 9 | 2026-09-27 | 2026-09-27 | 2026-05-08 | ≈ | y | n | y | n | agree |

## neso_data_portal (32 rows)

| dataset | gridflow key | cfg | tr | schema class | silver rows | first | last | lv | vs | mir | ch | ov | stub | agree |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|
| aahedc_tariffs |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| bsuos_fixed_tariffs |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| constraint_cost_forecast_24_months_ahead |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| contract_transfer_of_obligation |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| country_carbon_intensity_forecast |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| daily_opmr |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| daily_wind_availability | neso_data_portal/daily_wind_availability | y | y | NesoDailyWindAvailability | 3,589 | 2026-08-22 | 2026-09-03 | 2026-08-19 | = | y | y | n | n | agree |
| day_ahead_half_hourly_demand_forecast_performance |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| demand_profile_dates |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| dynamic_moderation_requirements |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| dynamic_regulation_requirements |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| embedded_register |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| embedded_wind_solar_forecast | neso_data_portal/embedded_wind_solar_forecast | y | y | NesoEmbeddedWindSolarForecast | 628 | 2026-08-20 | 2026-09-02 | 2026-08-19 | = | y | y | n | n | agree |
| gb_system_inertia_bid_and_offer_costs |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| historic_generation_mix | neso_data_portal/historic_generation_mix | y | y | NesoHistoricGenerationMix | 930,023 | 2009-01-01 | 2026-09-26 | 2026-08-19 | =* | y | y | n | n | agree |
| interconnector_register |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| long_term_2_52_weeks_ahead_national_demand_forecast |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| long_term_forecasts_for_dc_dm_dr_requirements |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| obp_non_bm_physical_notifications |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| obp_non_bm_reserve_instructions |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| obp_reserve_availability_utilisation_price |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| operational_transparency_forum_network_congestion_data |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| quick_reserve_auction_requirement_forecast |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| short_term_operating_reserve_stor_day_ahead_auction_results |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| slow_reserve_requirement_forecast |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| stability_midterm_y_1_utilisation_report |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| static_firm_frequency_response_requirement |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| stor_windows |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| transmission_entry_capacity_tec_register |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| upcoming_trades |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| weekly_opmr |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |
| weekly_wind_availability |  | n | n |  | 0 |  |  | no note |  |  | n | n | y | site only (no vault note, not in gridflow) |

## openmeteo (6 rows)

| dataset | gridflow key | cfg | tr | schema class | silver rows | first | last | lv | vs | mir | ch | ov | stub | agree |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|
| forecast_demand | open_meteo/forecast_demand | y | y | DemandWeather | 6,048 | 2026-08-01 | 2026-09-22 | 2026-06-03 | = | y | y | y | n | agree |
| forecast_solar | open_meteo/forecast_solar | y | y | SolarWeather | 2,160 | 2026-08-01 | 2026-09-22 | 2026-06-04 | = | y | y | n | n | agree |
| forecast_wind | open_meteo/forecast_wind | y | y | WindWeather | 4,320 | 2026-08-01 | 2026-09-22 | 2026-06-03 | = | y | y | n | n | agree |
| historical_demand | open_meteo/historical_demand | y | y | DemandWeather | 308,784 | 2021-09-01 | 2026-09-22 | 2026-06-03 | = | n | y | y | n | agree |
| historical_solar | open_meteo/historical_solar | y | y | SolarWeather | 266,688 | 2021-09-01 | 2026-09-26 | 2026-06-04 | = | n | y | n | n | agree |
| historical_wind | open_meteo/historical_wind | y | y | WindWeather | 533,376 | 2021-09-01 | 2026-09-26 | 2026-06-03 | = | n | y | n | n | agree |

