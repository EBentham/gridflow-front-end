SELECT settlement_date, settlement_period,
       system_sell_price, system_buy_price, available_at
FROM silver_elexon_system_prices_latest
WHERE settlement_date = DATE '2026-09-08' AND settlement_period = 37;
