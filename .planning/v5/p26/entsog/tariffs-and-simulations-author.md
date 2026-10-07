# entsog/tariffs-and-simulations: author report

Writer: Opus 5.5 · high, 2026-10-07. Family `tariffs-and-simulations`, lead `tariffs`, member `tariff_simulations`. Built with `--only entsog/tariffs`.

## Recommendation: SHIP (no hold)

The check the brief puts first passes: **silver loses no records.**

| Member | Bronze, per fetched day (1 to 5 Aug 2026) | Silver, per day | Silver total | Distinct `id` |
|---|---|---|---|---|
| `tariffs` (lead) | 12,244 (`meta.count` = `meta.total` = 12,244) | 12,244 | 61,220 | 12,244 |
| `tariff_simulations` | 2,782 (`meta.count` = `meta.total` = 2,782) | 2,782 | 13,910 | 2,782 |

The capacity writer was right: both are in `_DATE_WINDOW_EXEMPT` (`silver/entsog/generic.py:297-317`), so the gas-day filter (`:157-161,332`) does not run on them.

**What silver does get wrong is repetition, not loss.**
- Silver has no cross-day dedup (`generic.py:193-199` dedups on `id` within one day's read).
- Each fetched day's partition therefore holds the whole set again: five copies that are identical in every column except `ingested_at` and `available_at`.
- `data.entsog.query()` filters on `timestamp_utc` (`schema_manifest.py:222-223`), which is the tariff-period start. It keeps `ingested_at` (not in `BITEMPORAL_EXCLUDE`, `schema_manifest.py:77-85`), so it returns every copy.

I judged this not to mislead overall, and the advisor agreed. Nothing is lost or arbitrarily picked, the copies are byte-identical, and the page discharges the problem in every place a reader meets it:
- **Chart:** `dedup: {on: [id]}`. Distil provenance shows `rows_matched` 40, `duplicates_dropped` 32, `rows_used` 8.
- **Sample:** `select.dedup` on `id`.
- **Notebook:** `.drop_duplicates("id")` in the query cell, and `notebook.lead` says why.
- **Prose:** `what_it_is` and `raw_feed.note` both state the repetition.
- **Commands:** they fetch one day, so a reader who follows them gets no repeats.

The seat may still rule "repeated rows" a hold trigger; the numbers are above.

## Status

- **Build:** `uv run --system-certs --extra build gridflow-build --only entsog/tariffs` exits 0 with `wrote: data-sources/entsog/tariffs-and-simulations.html (dataset template)`. Remaining warnings are the generic "no Pydantic class" notices (`content warning(s)` for ENTSOG).
- **Detector:** `detect.mjs --json` returns `[]`, with no advisories. Em dashes, `→` and middle dots in the page: 0 each.
- **Rubric greps** on the rendered text (locally, held, our, since 20, % of, live, now, yet, soon, planned, coming, real-time, digits plus rows or days) find nothing.
- **Mirrors:** `vault/entsog/tariffs.md` and `vault/entsog/tariff_simulations.md` are copied with `cp` and checked with `cmp`, byte-equal with CRLF kept (567/567 and 308/308 CRLF lines).
- **Artefacts** (all from real silver):
  - `site/hifi/data/series/entsog/tariffs.json` (`spec_origin: vault`, bar, 1 series × 8 categories);
  - `site/hifi/data/samples/entsog/tariffs.json` (`gridflow-sample`, 8 rows × 73 columns);
  - `site/hifi/data/notebooks/entsog/tariffs.json` plus `tariffs-5.png` (`scripts/run_notebooks.py`, 5 cells, no errors).
  - No staged chart spec or authored override existed.
- **`|` in values:** none. I checked every String column in both tables, and `gridflow-sample` ran unmodified. The sampler's dtype-drift problem is already fixed on this branch (`sample.py:51-64`, `diagonal_relaxed`).
- **Screenshots** (light only; the site has no dark theme) at 1440, 1024, 768, and 390 in a true 390 px iframe: `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\5fec4a50-7518-4657-b815-ed1434a34580\scratchpad\tar\shots\s_<width>_light_<n>.png`. Crops: `z1024_chart.png`, `z390_bars2.png`.
  - The first 390 pass clipped the bar labels on the left ("nnector, Bacton exit"). I shortened the labels to 17 characters or fewer ("IUK, Bacton entry", "Fluxys, IZT entry") and moved the full names into the key notes. After that, nothing is clipped at any width.
  - At 390, long column names in the guide wrap mid-identifier (`applicable_tariff_per_local_currency_k_wh_h_` / `value`). This is legible and template-level.
  - The static server on 9877 runs under `timeout 900` and stops itself 15 minutes after launch. Port 9670 was not touched.
- **Member pointers:** `data-sources/entsog/tariffs.html` points to `tariffs-and-simulations.html#tariffs`, and `tariff_simulations.html` to `#tariff_simulations`.
- **Notebook cell 1 counts (3,351 / 8,715 / 178)** are not a local holding. After `drop_duplicates("id")` they split one response's 12,244 records (`meta.count`) by tariff period: the size of what ENTSOG returns for one day.

## What the data is (the "look hardest at" answers)

- **Request.** One call per covered UTC day with `from` = `to` = D (`connectors/entsog/client.py:78-102`; `utils/time.py:123-147`, end exclusive). The verbatim `request_url` from the sidecar is `https://transparency.entsog.eu/api/v1/tariffsFulls?limit=-1&timeZone=UCT&from=2026-08-01&to=2026-08-01&countryKey=UK`, and the same shape for `tariffsSimulations`.
- **`countryKey=UK` does not filter to the UK.**
  - The connector sends it (`endpoints.py:187,196`) and `meta.query` echoes it.
  - Yet the rows cover 21 country codes (AT to UK) and 8 currencies: 37 operators, 138 points and 321 operator-point-directions in `tariffs`.
  - The page says "rows cover operators across Europe". The notebook's currency count makes that visible. No country count appears on the page.
- **Coverage is not a window.** DATA-MATRIX's "2025-10-01 to 2026-04-01" is the min and max of `timestamp_utc`, which is three one-year **tariff periods**:

  | Tariff period start (UTC) | Tariffs | Simulations |
  |---|---|---|
  | 2025-10-01 04:00 | 3,351 | 538 |
  | 2026-01-01 05:00 | 8,715 | 2,170 |
  | 2026-04-01 04:00 | 178 | 74 |

  Each period runs one year. The fetch days are 1 to 5 August 2026 (ingested 2026-08-16).
- **What one row is.**
  - **Tariff:** one operator × point × direction × capacity type (Firm/Interruptible) × product (Yearly, Quarterly, Monthly, Daily, WithinDay) × product period. Products subdivide the tariff period: monthly products have one row per month, quarterly ones per quarter, and some daily or within-day products have one row per month (BBL) or one for the year (Interconnector).
  - **Key:** within a day the 6-tuple (`operator_key`, `point_key`, `direction_key`, `tariff_capacity_type`, `product_type`, `product_period_from`) is unique, 12,244 groups of 1. Repeated rows exist only across days.
  - **Simulation:** one row per operator × point × direction × capacity type × product × tariff period, also unique within a day (2,782 groups). It has no product period.
- **Currency and units (from the rows).** Each priced tariff row carries five numbers:
  - local currency per kWh/d, e.g. `GBP/(kWh/d)/y`;
  - local currency per kWh/h, e.g. `GBP/(kWh/h)/y`;
  - euro per kWh/d (`Euro/(kWh/d)/y`);
  - euro per kWh/h (`Euro/(kWh/h)/y`);
  - a "common unit" figure in `Euro/(kWh/h)/d` (`/h` for within-day).

  How they relate:
  - The kWh/h value is 24 × the kWh/d value on all priced rows (ratio 24.000 ± 0.004).
  - For euro operators the euro columns equal the local ones exactly.
  - The unit's last part follows the product (`/y`, `/q`, `/m`, `/d`, `/h`), except 72 within-day rows sent with `/d` (Snam Rete Gas 42, GASCADE 12 and five others).
  - 827 of 12,244 records carry no price at all.
  - The simulation cost is plain currency (local and `EUR`), kept as **text** with `N/A` on 799 of 2,782 records.
- **The common-unit column is not comparable across operators.** For yearly products, most operators send the yearly euro kWh/h price ÷ 365 (406 records). Fluxys Belgium divides by 8,760 (26, plus 1 bayernets record), Energinet by other factors, and Transgaz's common figure is 24 times its euro kWh/h price (corrected in round 2). I therefore charted the per-product euro column, not the common unit.
- **National Gas TSO.**
  - It prices 25 of its 70 records.
  - Moffat exit firm is 0.000299 GBP/(kWh/d) on the yearly product (unit `/y`) **and** on all 11 monthly products (unit `/m`).
  - Bacton IUK exit yearly is 0.005064 GBP/(kWh/h)/y, against Interconnector's 3.138445 on the other side of the same point.
  - Its unit suffixes do not follow its products. The chart is framed on the three pipeline operators (BBL company, Interconnector, Fluxys Belgium), so National Gas TSO does not appear. The page does not claim anything about it.
- **What a "simulation" is.** Neither note, nor the vendor README or `endpoints.md`, quotes an ENTSOG definition. Each note's Overview is an authored paraphrase. The page gives none, and `differs` says only "one simulated cost per product and tariff period, in local currency and euro".
  - Operator remarks in the rows differ: "Cost of flowing 1 GWh/day/year through the IP in EUR taking into account the quarterly multiplier." (22 records); "The simulation cost is calculated as the sum of the capacity charge ... and the commodity" (105).
  - Project check: for 204 yearly records the cost equals the yearly euro kWh/h tariff × 41,667 kWh/h (1 GWh/d); others differ.
  - BBL company sends 365000 EUR for every firm product, daily to yearly.
  - All of this is recorded in the vault, not on the page.
- **Time stamps** (`generic.py:181-187,201-206`):
  - `timestamp_utc` = `period_from` = tariff-period start, in UTC (06:00 CEST/CET as sent becomes 04:00/05:00 UTC). `event_time` is the same.
  - `product_period_from`/`_to` are parsed to UTC.
  - `exchange_rate_reference_date` stays text as sent (not in `_DATETIME_COLUMNS`, `:34-50`).
  - `last_update_date_time` is the vendor's stamp in UTC; `ingested_at` is the silver transform time.
  - No stamp is a fetch or publish time, and the fetch day lives only in the file name.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| No loss; per-day bronze = silver (report, vault Dedup/Bronze read filter) | `scratchpad\tar\t1.py`: bronze `tariffsFulls` 12,244 and `tariffsSimulations` 2,782 records per file, `meta.count` = `meta.total`; silver partitions 12,244 / 2,782 rows, all ids distinct |
| Exempt from the gas-day filter | `generic.py:297-317` (`_DATE_WINDOW_EXEMPT`) |
| Silver repeats each record once per fetched day (`what_it_is`, `raw_feed.note`, caption "Daily repeats removed", notebook lead) | `t2.py`/`t3.py`: day-1 vs day-5 partitions equal on all non-pipeline columns; 61,220 rows / 12,244 ids; only `ingested_at`/`available_at` differ |
| `query()` returns every copy (notebook lead) | `gridflow_models/research/handles/source.py:401-451`; `schema_manifest.py:77-85,222-223` |
| Request URL (`raw_feed.requests`, `family.members[].request`) | Bronze `.meta.json` `request_url` for 2026-08-01, verbatim; `endpoints.py:181-198,263-281` |
| Commands: ingest end exclusive, transform end inclusive | `client.py:78-102`, `utils/time.py:123-147`; same CLI shape as the approved nominations page |
| "rows cover operators across Europe" (`what_it_is`, `raw_feed.note`) | 21 `country_code` values, 8 currencies in silver; notebook cell 2 output lists EUR, HUF, RON, BGN, PLN, CZK, DKK, GBP |
| Grain and key (`facts.grain`, `record.key`) | `t13.py`: the 6-tuple is unique within a day (12,244 groups, max 1) |
| `facts.cadence` "One-year tariff periods" | `period_from`/`period_to` pairs one year apart on all rows (`t2.py`); notebook cell 1 prints the three starts |
| Chart values, alt text, key notes | Committed series: 19.32, 8.76, 8.76, 8.112, 3.637 × 4; sample rows show 3.138445 GBP → 3.63709 EUR |
| Fluxys tariff period from 1 January 2026; BBL from 1 October 2025 (key notes) | `t9.py`: `period_from` per operator-point-direction |
| Directions "From `X` to `Y` as sent" (key notes, `from_bz`/`to_bz` fields) | `from_bz`/`to_bz` on the charted rows (`t9.py`, `t7.py`) |
| "Interconnector sends one price for both points and both directions" | `t12.py`: 3.63709 on all four Interconnector yearly firm rows (Bacton and Zeebrugge, entry and exit) |
| Field "a 24th of the kWh/h price here" | Sample rows: 0.13076854 × 24 = 3.138445; 0.365 × 24 = 8.76 |
| Field "common unit ... how it is derived differs by operator" | `t10.py`: ratios 365 / 8,760 / other by operator |
| Fields "kept as text" (`multiplier`, `seasonal_factor`, commodity, `exchange_rate_reference_date`) | Silver dtypes String; `_looks_numeric` `generic.py:60-69,384-387`; `_DATETIME_COLUMNS` `:34-50` |
| `plot_alt` numbers | `tariffs-5.png` and silver: BBL Bacton exit firm monthly 1.116, 1.08, 1.116, 1.116, 1.008, 1.116 (Oct to Mar), then 1.44 to 1.488 (Apr to Sep) |
| `notebook.needs` "one day" | The commands fetch one day; the notebook output is identical whatever the number of days, after dedup |
| Related: firm_booked "at the Bacton and Moffat points" | `endpoints.py:24-34,118-125` |

## Body corrections (both canonical notes, applied by `scratchpad\tar\body_fix.py` with count-asserted replacements; CRLF kept)

1. **Query parameters, `countryKey` row:** "Filter to one country (recommended)" becomes "the connector sends `UK` (`endpoints.py:187,196`); it does not limit the response". Added one line after the table: one request per UTC day with `from` = `to` (`client.py:78-102`).
2. **Dedup key:** "`(id)` if present, else all non-`timestamp_utc` columns" becomes "vendor `id`, keep last, within one day's read (`generic.py:193-199`)", with no cross-day dedup and the five-copy counts. Added a **Bronze read filter** line (exempt, `generic.py:297-317`, bronze = silver per day).
3. **Point-in-time field:** "`last_update_date_time` or `publication_date_time` (UMM)" becomes "none used by the pipeline", with what `timestamp_utc`, `last_update_date_time` and `ingested_at` are.
4. **Silver schema table**, regenerated from the parquet schema in silver's column order:
   - fixed the broken `id | str | int` and `data_set | str | int` cells (they split the table);
   - added `timestamp_utc` and the four lineage columns;
   - corrected dtypes: `product_period_from/to` datetime (were str); `seasonal_factor` str (was float); `exchange_rate_reference_date` str (was datetime); `display_order` int; `data_set` int; Null dtype on all-null columns; `is_unlimited` Null (was bool).
5. **Silver sample:** each note showed a bronze-shaped record with `+02:00` stamps (tariffs: a Transgaz row with no prices). Each is replaced with a real silver row, BBL company Bacton exit firm yearly from the 2026-08-01 partition, in UTC.
6. **Known issues (tariffs):**
   - the `countryKey` bullet is corrected;
   - currencies listed;
   - the 827 no-price records;
   - the "evergreen" null product periods scoped to 11 Transgaz records;
   - new bullets on tariff periods and products, the cross-day repetition, units (×24, suffixes, the 72 exceptions), the common-unit inconsistency, National Gas TSO figures, and numbers kept as text.
7. **Known issues (simulations):**
   - the `countryKey` bullet is corrected;
   - the "Mixed currencies" bullet named tariff-only fields (`applicableTariffPerEURKWhDValue`) and now names the two cost fields;
   - "tariffs are sparse" becomes "799 of 2,782 records send `N/A`";
   - the "productPeriodFrom may be null" bullet was wrong (simulations have no product period) and is replaced;
   - new bullets on repetition and on what the cost is (no ENTSOG definition, operator remarks quoted, the 41,667 kWh/h project check).
8. **Overview (simulations):** one sentence says the notes quote no ENTSOG definition.
9. **Modelling notes:** `TODO` becomes dedup-first and like-with-like guidance (both notes).

Bronze samples, curl examples and the operational-data bullets copied into both notes (indicator case, `pointDirection`) are left alone. They are irrelevant here, but not wrong.

## Not verified

- **ENTSOG's definition of a tariff simulation** and of the common-unit figure. No vendor text is quoted in the vault, and I read no PDF.
- **What `countryKey` filters on in `tariffsFulls`/`tariffsSimulations`.** It is echoed in `meta.query`, but the response is Europe-wide.
- **Whether National Gas TSO's figures are per-day rates labelled per year or month.** They are consistent with that reading, but unconfirmed.
- **Whether ENTSOG's euro conversion uses the rate on `exchange_rate_reference_date`.** For Interconnector the ratio is 1.15888 EUR/GBP, against a stamp of 2025-07-03.
- **Whether a later fetch changes stored tariffs.** All five bodies are identical, and there is no re-fetch across a tariff update.
- **The unfolded frame** was not screenshotted. Same template as nominations.

## Open questions

1. **Hold or ship?** I recommend shipping (see top). The seat's "repeated rows" trigger is literally met, but no row is lost, every page surface dedups or states it, and the commands avoid it.
2. **Silver design after a fix.** Either treat tariffs as a register (newest body only, `reference=True`) or dedup across partitions on `id`. Both remove the repetition; the register route also drops the meaningless per-day partitioning. This decides whether the page later needs its dedup notes.
3. **Should `connectors/entsog/endpoints.py` keep `countryKey=UK`?** It does not restrict anything; dropping it changes nothing in the response.

## Template problems

1. **Bar-category labels are clipped at 390 when longer than about 17 characters** (the label column is fixed-width and overflows left). I worked around it with short labels. The renderer could wrap or truncate with a title. Cosmetic, but it bites any bar chart with long categories.
2. **Long column names wrap mid-identifier in the 390 guide.** Legible; cosmetic.
3. **Bar value labels are rounded to two significant figures** (19, 8.8, 8.1, 3.6), while the alt text and key notes carry the committed series values (19.32, 8.76, 8.112, 3.637). Both are correct; a checker reading the screenshot should compare against `series/entsog/tariffs.json`.
4. **Build warnings name the wrong module** ("no Pydantic class declared in gridflow.schemas.elexon" for ENTSOG), as earlier writers reported.

## Defects

- **[gridflow silver] `tariffs` and `tariff_simulations` repeat the full record set once per fetched day.**
  - Dedup is on `id` within one bronze day only (`silver/entsog/generic.py:193-199`), and both datasets are exempt from the gas-day filter (`:297-317`). So each daily partition holds every tariff in force: 2026-08-01 to 05 give 12,244 × 5 = 61,220 and 2,782 × 5 = 13,910 rows, identical apart from `ingested_at`/`available_at`.
  - `data.entsog.query()` filters on `timestamp_utc` (the tariff-period start) and keeps `ingested_at`, so it returns every copy, with no column naming the fetch day.
  - Candidate fix: treat both as registers (newest body, `reference=True`) or dedup across partitions on `id`.
- **[gridflow silver] Tariff and simulation numbers kept as text.** `multiplier`, `seasonal_factor`, `applicable_commodity_tariff_local_currency`, `applicable_commodity_tariff_euro`, `product_simulation_cost_in_local_currency` and `product_simulation_cost_in_euro` miss `_looks_numeric` (`generic.py:60-69,80-93,384-387`) and stay String, with `N/A` placeholders (799 of 2,782 simulation records). `exchange_rate_reference_date` is not in `_DATETIME_COLUMNS` (`:34-50`) and stays text with `N/A`.
- **[gridflow connector, observation] `countryKey=UK` does not restrict `tariffsFulls`/`tariffsSimulations`** (`connectors/entsog/endpoints.py:187,196`). The responses hold 21 country codes and 8 currencies; `meta.query` echoes `countryKey: UK`.
- **[vendor data] The common-unit tariff is derived differently by operator.** `applicableTariffInCommonUnitValue` (`Euro/(kWh/h)/d`) is the yearly euro kWh/h price ÷ 365 for most operators, ÷ 8,760 for Fluxys Belgium (e.g. 19.32 → 0.002205) and other factors for Energinet. Transgaz's common figure is 24 times its euro kWh/h price, not a zero-price case (corrected in round 2). It is not comparable across operators.
- **[vendor data] National Gas TSO unit suffixes do not follow its products.**
  - Moffat exit firm sends 0.000299 GBP/(kWh/d) labelled `/y` on the yearly product and `/m` on all 11 monthly products.
  - Bacton (IUK) exit yearly is 0.005064 GBP/(kWh/h)/y, against Interconnector's 3.138445 at the same point.
  - Only 25 of its 70 records carry a price. Unexplained.
- **[vendor data, observation] 72 within-day tariff records carry `/d` units instead of `/h`** (Snam Rete Gas 42, GASCADE 12, Enagas 6 and others).
- **[vault, fixed in this branch] Both notes were wrong in several places:**
  - the `countryKey` "filter to one country";
  - the dedup key and the point-in-time field;
  - broken `id`/`data_set` schema cells, a missing `timestamp_utc`, about six wrong dtypes;
  - bronze-shaped `+02:00` silver samples;
  - tariff-only fields and a "productPeriodFrom" bullet in the simulations note.

  All are corrected with code citations.
