SELECT settlement_date, settlement_period, system_sell_price, available_at
FROM silver_elexon_system_prices
WHERE settlement_date = DATE '2026-09-08' AND settlement_period = 37
  AND available_at <= TIMESTAMPTZ '2026-09-09 12:00:00+00'
QUALIFY row_number() OVER (
    PARTITION BY settlement_date, settlement_period
    ORDER BY available_at DESC
) = 1;
