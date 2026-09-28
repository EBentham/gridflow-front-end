(pl.col("system_buy_price") - pl.col("system_sell_price")).alias("spread")
