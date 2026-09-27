SELECT settlement_date, settlement_period,
       system_sell_price, system_buy_price,
       available_at, vintage_policy, source_run_id, dataset_version
FROM silver_elexon_system_prices
WHERE settlement_date = DATE '2026-09-08' AND settlement_period = 37
ORDER BY available_at;
