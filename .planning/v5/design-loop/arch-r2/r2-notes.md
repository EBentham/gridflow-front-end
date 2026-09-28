claude-opus-5-5

**Boards** (root = `$preview`): `arch-r2/arch-r2.dc.html` 1440×8847, `arch-r2/arch-r2-390.dc.html` 390×13517.

**Stop 7**, "A notebook reads it into pandas":
```python
from gridflow_models import setup_notebook
data, models, common = setup_notebook()
df = data.elexon.query("system_prices", "2026-09-08", "2026-09-08")
print(type(df), len(df))
p37 = df.loc[df["settlement_period"] == 37, ["settlement_date", "settlement_period",
             "system_sell_price", "system_buy_price", "published_at"]]
p37["published_at"] = p37["published_at"].dt.tz_convert("UTC")
print(p37.to_string(index=False))
```
Real output: `<class 'pandas.DataFrame'> 48`, then `2026-09-08 37 110.0 110.0 2026-09-09 17:44:29+00:00`. The read drops `available_at`, so that claim is gone. Bobbo's decision overrides the pack's cut of pandas.

**Scope line:** "drops into" is now "runs under", because `gridflow build` exits 0 on failure (cli.py:337-342). The other clauses are verified.

**Phone drawing:** redrawn, not scaled down. The sources stand in one labelled strip, the cables nest into lanes, and the index sits level beside its parts. The drum's view names and the gold and tap labels move to the index. The timeline runs vertically, and scroll boxes hide their scrollbars.

**Checks:** detector `[]` on both. No overlaps, no text outside the column, no horizontal scroll.

**Also changed:** removed "Nothing runs on a timer"; the notebook cable is chartreuse; moved the GIE ALSI label inside 1360; links are real.
