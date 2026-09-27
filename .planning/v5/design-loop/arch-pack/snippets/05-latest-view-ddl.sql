CREATE OR REPLACE VIEW "silver_elexon_system_prices_latest" AS
SELECT * FROM "silver_elexon_system_prices"
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY "settlement_date", "settlement_period"
    ORDER BY "available_at" DESC NULLS LAST,
             CASE "run_type" WHEN 'II' THEN 1 WHEN 'SF' THEN 2 WHEN 'R1' THEN 3 WHEN 'R2' THEN 4 WHEN 'R3' THEN 5 WHEN 'RF' THEN 6 WHEN 'DF' THEN 7 ELSE 0 END DESC
) = 1
