from datetime import date

import polars as pl

from gridflow.config.settings import load_settings
from gridflow.gold.system_marginal_price import SystemMarginalPriceBuilder

builder = SystemMarginalPriceBuilder(load_settings().pipeline.data_dir)
gold = builder.build(date(2026, 9, 8), date(2026, 9, 8))  # build() returns the frame; run() writes it
print(
    gold.filter(pl.col("settlement_period") == 37).select(
        "settlement_date", "settlement_period", "system_buy_price", "system_sell_price",
        "spread", "abs_imbalance", "hour_of_day", "day_of_week",
    )
)
