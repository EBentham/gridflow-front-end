# Imbalance volume sign: finding (2026-09-27)

**Positive NIV means the system is short** (demand exceeded generation; the SO accepted offers). Negative means long (the SO accepted bids). Confidence: **high**: two Elexon primary sources agree, gridflow stores the vendor value unchanged, and five years of stored rows fit the convention every month.

The vault note `20-domain/instruments/imbalance-volume.md` has the sign **inverted** (lines 10-11 and 15-17). Its price section (lines 19-24) and the forecasting formula (line 38) are correct and consistent with positive = short.

## Primary sources (Elexon)
- Imbalance Pricing page, https://www.elexon.co.uk/bsc/settlement/imbalance-pricing/ : "Where the NIV is positive, the system is short..." (continues: the SO normally accepts Offers).
- Open settlement data item descriptions, N0430, https://www.elexon.co.uk/bsc/documents/data/open-settlement-data/data-item-descriptions/ : "A positive Net Imbalance Volume indicates that the System is Short".
- Insights API spec (https://data.elexon.co.uk/swagger/v1/swagger.json), `SystemPriceResponse.netImbalanceVolume`: typed `number/double` only, no sign text.
- Imbalance Pricing Guidance V16.0 (effective 14/07/2025, https://bscdocs.elexon.co.uk/guidance-notes/imbalance-pricing-guidance) exists but its body did not render or extract here; not relied on.

## Pipeline: no sign flip
- `gridflow/src/gridflow/connectors/elexon/endpoints.py:58-59`: raw `/balancing/settlement/system-prices` (DISEBSP).
- `gridflow/src/gridflow/silver/elexon/system_prices.py:126` rename `netImbalanceVolume` -> `net_imbalance_volume`; `:204` Float64 cast only; `:244` selected as-is. No arithmetic anywhere.
- `gridflow/src/gridflow/schemas/elexon.py:47`: `net_imbalance_volume: float  # MWh`.
- Spot check, bronze `raw_20260926T182927Z_7ae6faf0.json` vs silver, 2026-09-22 SP1-3: 52.099..., -77.935..., 19.352... identical to the last digit.

## Data (read-only DuckDB over `C:\gridflow-data\silver\elexon\system_prices`, latest vintage per settlement period)
Window 2025-09-23 to 2026-09-22, 17,520 periods. SSP = SBP in 100% of rows (single imbalance price), so "system price" below.

| Sign | Periods | Mean price | Median | Mean NIV | Negative prices | Max price |
|---|---|---|---|---|---|---|
| NIV > 0 | 8,297 | 126.4 | 119.9 | +208 MWh | **6** | 800.0 |
| NIV <= 0 | 9,223 | 66.6 | 71.3 | -243 MWh | **763** | 226.7 |

corr(NIV, price) = 0.61. Top five prices of the year all at NIV > 0 (e.g. 800 GBP/MWh at +748 MWh, 23 Jun 2026 SP42; 750 at +1,197 MWh, 5 Jan 2026).

Every one of 13 months: mean price higher when NIV > 0 (gap 36-122 GBP/MWh), monthly corr 0.54-0.79. Every calendar year 2021 (from Sep) to 2026: mean price at NIV > 0 exceeds NIV <= 0 (e.g. 2022: 274.1 vs 118.2; 2024: 101.7 vs 43.5), corr 0.34-0.66.

## Proposed vault wording (not applied; seat relays)
Lines 9-11 replace with:
> The system-wide signed imbalance in MWh per settlement period, as balanced by BM actions. Positive = system was short (demand exceeded generation); negative = system was long.

Lines 15-17 replace with:
> Elexon's `netImbalanceVolume` follows the convention (data item N0430):
> - **Positive** = system short (SO accepted offers to buy energy upward)
> - **Negative** = system long (SO accepted bids to curtail / sell energy)

Leave "Relationship to prices" and "Forecasting NIV" as they are.

## Proposed site field description
`net_imbalance_volume` (MWh): The system's net shortfall or surplus in the half hour, as balanced by the system operator. Positive means the system was short (it bought energy by accepting offers); negative means it was long (it accepted bids).
