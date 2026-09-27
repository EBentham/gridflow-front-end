from gridflow_models import setup_notebook

data, models, common = setup_notebook()
df = data.elexon.query("system_prices", "2026-09-08", "2026-09-08")
print(type(df), len(df))

p37 = df.loc[df["settlement_period"] == 37, ["settlement_date", "settlement_period",
             "system_sell_price", "system_buy_price", "published_at"]]
p37["published_at"] = p37["published_at"].dt.tz_convert("UTC")
print(p37.to_string(index=False))
