import polars as pl

from gridflow.serving.client import GridflowClient

with GridflowClient() as gf:
    prices = gf.get_system_prices("2026-09-08", "2026-09-08")

print(
    prices.filter(pl.col("settlement_period") == 37).select(
        "settlement_date", "settlement_period", "system_sell_price", "system_buy_price",
        pl.col("available_at").dt.convert_time_zone("UTC"),
    )
)
