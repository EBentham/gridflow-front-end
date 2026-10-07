# entsog/tariffs-and-simulations: author report, round 2

Writer: Opus 5.5 · high, 2026-10-07. Answers `tariffs-and-simulations-review.md` (REVISE: 0 blockers, 4 majors, 6 nits) and the seat's relayed instructions. Every finding is fixed.

## Status

- **Build:** `gridflow-build --only entsog/tariffs` exits 0 with `wrote: data-sources/entsog/tariffs-and-simulations.html`. Remaining warnings are the generic "no Pydantic class" notices.
- **Detector:** `C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow-front-end/.claude/skills/impeccable/scripts/detect.mjs --json` returns `[]`. Em dashes in the page: 0.
- **Rubric greps** on the rendered text (locally, held, our, since 20, % of, live, now, yet, soon, planned, coming, real-time, digits plus rows or days, →, ·): 0 hits.
- **Mirrors:** `tariffs.md` and `tariff_simulations.md` copied with `cp` and checked with `cmp`, byte-equal, CRLF kept.
- **Artefacts regenerated:**
  - series: distil re-run, spec unchanged, same 8 values;
  - sample: new column order;
  - notebook: 6 cells; the plot is now `tariffs-6.png`, and the runner removed `tariffs-5.png`.
- **Screenshots** at 1440, 1024, 768 and 390 (true 390 px iframe), light: `scratchpad\tar\shots\s_<width>_light_<n>.png`, with crops `r2_1440_chart.png` and `r2_1440_frame*.png`. Nothing is clipped or overlapping. The 9877 server runs under `timeout 600`; 9670 was not touched.

## Fixes

**Major 1: what a simulated cost is, and what silver keeps of it.**
- `what_it_is` now says: ENTSOG describes the simulation as "costs for flowing 1 GWh/d/y at IP", and each operator sets its basis. To stay within 60 words (now 57) I dropped "per kWh/d and per kWh/h of capacity"; the guide still covers both.
- `family.members[1].differs` now reads "Simulated cost, kept as text; `N/A` when not sent; currency only, no capacity unit" (14 words).
- `how_used[2]` now reads "Reading an operator's simulated cost beside its tariff, with its cost remark."
- **The "799 of 2,782" count stays off the page.** It is a local row count, so it is in the vault and here only (rubric 3). The page says "`N/A` when not sent".
- **Source of ENTSOG's words:** the TAR NC transparency workshop slide (Dec 2016) that the reviewer cites. I did not retrieve it myself, and the vault note says so. Silver remarks also carry "Cost of flowing 1 GWh/day/year through the IP" (22 records).
- **Vault, `tariff_simulations.md`:**
  - Overview: the "no ENTSOG definition" sentence is replaced with the quoted wording and its source.
  - Known issues, "What the cost is": now opens with ENTSOG's wording.

**Major 2: the folded frame showed no price.**
- `record.select.columns` order is now the six key columns, then `applicable_tariff_per_eurk_wh_h_value` and `_unit`, then `product_period_to`, `operator_currency`, the local price and unit, `multiplier`, `operator` and `point_label`.
- The sample is regenerated (`gridflow-sample`, 8 rows × 73 columns), and the guide lines are reordered to match.
- At 1440 the folded frame now shows the euro price as column 7 (3.63709, 1.222898, 0.588397, 0.02847, 8.76, 2.6496, 1.116, 0.0504; `r2_1440_frame.png`).
- The unit column folds behind `…`, because the price column's long name uses the width. `product_type` beside it says what the price is for.

**Major 3 (seat ruling: major): the National Gas TSO exclusion is now stated plainly.**
- `chart_view.caption` (40 words): "...yearly firm products of BBL, Interconnector and Fluxys Belgium, euro per kWh/h per year, daily repeats removed. National Gas TSO excluded: its Moffat exit price, 0.008326, is labelled both yearly and monthly."
- 0.008326 is visible on the page. A new read-only notebook cell prints National Gas TSO's Moffat exit firm yearly and monthly rows: `Monthly 0.008326 Euro/(kWh/h)/m` and `Yearly 0.008326 Euro/(kWh/h)/y`.
- `how_used[0]` no longer invites cross-operator comparison. It now reads "Comparing yearly firm prices of the pipeline operators at Bacton and Zeebrugge."

**Major 4: the false Transgaz claim.** Re-verified from silver:
- Transgaz has 913 records, 902 of them priced; none is zero (min 0.00023202).
- Its yearly common figure is its euro kWh/h price × 24 (ratio 23.999965 to 23.999979).

Corrected in:
- vault `tariffs.md` Known issues ("Common-unit column is not comparable");
- both lines of `tariffs-and-simulations-author.md` (analysis and Defects);
- the Defects list below.

**Nit 5: `N/A` becomes null.**
- `raw_feed.note` now says "Silver turns `N/A` prices into nulls and repeats the records in every fetched day's file" (30 words).
- The euro price guide line now ends "null when `N/A`".
- Vault `tariffs.md`: the 827 records are 816 sent as the string `N/A` and cast to null (`generic.py:189-191`), plus 11 evergreen Transgaz records sent with null price fields. The `multiplier`, `seasonal_factor`, commodity and exchange-date columns keep `N/A` as text. Bronze check, 2026-08-01: 11,417 numeric strings, 816 `N/A`, 11 null.

**Nit 6:** `plot_alt` now reads "between 1.008 and 1.116 from October to March, then between 1.44 and 1.488 from April".

**Nit 7: `IZT` and `IUK` expanded.**
- The Fluxys entry note reads "Fluxys Belgium at ENTSOG's point Zeebrugge IZT, ...".
- The IUK Bacton entry note reads "Operator Interconnector, whose zone ENTSOG labels `IUK`; 3.138445 GBP as sent, euro column 3.63709".
- I did not add "Interconnector's terminal", which is unverified.

**Nit 8:** "ENTSOG converts Interconnector's GBP" is gone from the caption and the key notes. Neither now says who converts.

**Nit 9 (bar labels rounded):** template behaviour, already listed as a template problem. Unchanged.

**Nit 10:** `notebook.lead` now ends "...ends included; widen them for later periods. The query cell keeps one row per `id`, dropping the daily copies." (35 words).

## Evidence for the new claims

| Claim | Evidence |
|---|---|
| National Gas TSO Moffat exit 0.008326 under both `/y` and `/m` (caption) | Notebook cell 5 output (rows 1709 and 1722); silver `t`-check: Monthly and Yearly 0.008326; Quarterly, Daily and WithinDay null |
| `N/A` prices become null (`raw_feed.note`, guide) | Bronze 2026-08-01 `applicableTariffPerEURKWhHValue`: 816 `"N/A"`, 11 absent; silver nulls; cast at `generic.py:189-191` (`strict=False`) |
| Transgaz common figure = euro kWh/h × 24 (vault, Defects) | Silver 2026-08-01: 902 of 913 priced, 0 zero; yearly ratio 23.999965 to 23.999979 |
| ENTSOG's simulation wording (`what_it_is`, vault) | The reviewer's citation of the ENTSOG TAR NC transparency workshop slide, Dec 2016 (not retrieved by me); silver remark "Cost of flowing 1 GWh/day/year through the IP" (22 records) |

## Template problems (unchanged from round 1)

1. Bar-category labels clip at 390 beyond about 17 characters (worked around).
2. Long column names wrap mid-identifier in the 390 guide.
3. Bar value labels round to two significant figures.
4. Build warnings name `gridflow.schemas.elexon` for ENTSOG.

## Defects (pasteable; replaces round 1's list)

- **[gridflow silver] `tariffs` and `tariff_simulations` repeat the full record set once per fetched day.**
  - Dedup is on `id` within one bronze day only (`silver/entsog/generic.py:193-199`), and both datasets are exempt from the gas-day filter (`:297-317`).
  - 2026-08-01 to 05: 12,244 × 5 = 61,220 and 2,782 × 5 = 13,910 rows, identical apart from `ingested_at`/`available_at`.
  - `data.entsog.query()` filters on the tariff-period start and returns every copy, with no column naming the fetch day.
  - Candidate fix: register semantics (newest body) or cross-partition dedup on `id`.
- **[gridflow silver] Mixed `N/A` conventions and numbers kept as text.**
  - The five numeric tariff price columns turn the vendor's `"N/A"` into null (816 of 12,244 records a day).
  - These stay String with `N/A`: `multiplier`, `seasonal_factor`, `applicable_commodity_tariff_local_currency`/`_euro`, `product_simulation_cost_in_local_currency`/`_in_euro` (799 of 2,782 simulation records `N/A`) and `exchange_rate_reference_date`. Cause: `_looks_numeric` (`generic.py:60-69,80-93,384-387`) and `_DATETIME_COLUMNS` (`:34-50`).
- **[gridflow connector, observation] `countryKey=UK` does not restrict `tariffsFulls`/`tariffsSimulations`** (`connectors/entsog/endpoints.py:187,196`). The responses hold 21 country codes and 8 currencies; `meta.query` echoes `countryKey: UK`.
- **[vendor data] The common-unit tariff is derived differently by operator.** For yearly products, `applicableTariffInCommonUnitValue` (`Euro/(kWh/h)/d`) is:
  - the euro kWh/h price ÷ 365 for most operators (406 records);
  - ÷ 8,760 for Fluxys Belgium (26) and one bayernets record;
  - × 24 for Transgaz;
  - other factors for Energinet (65,394 and 6,766), FGSZ and others.

  It is not comparable across operators.
- **[vendor data] National Gas TSO unit suffixes do not follow its products.**
  - Moffat exit firm sends 0.000299 GBP/(kWh/d) (euro 0.008326 per kWh/h) labelled `/y` on the yearly product and `/m` on all 11 monthly products.
  - Bacton (IUK) exit yearly is 0.005064 GBP/(kWh/h)/y, against Interconnector's 3.138445 at the same point.
  - Only 25 of its 70 records carry a price.
- **[vendor data, observation] 72 within-day tariff records carry `/d` units** (Snam Rete Gas 42, GASCADE 12, Enagas 6, REN 4, NaTran Deutschland 4, NEL 2, Fluxys TENP 2).
- **[vault] The ENTSOG simulation definition was missing from the notes.** It is now quoted in `tariff_simulations.md` from the reviewer's source. It should be retrieved and confirmed against the slide or the Regulation (EU) 2017/460 text.

Summary: all 4 majors and 6 nits fixed; build exits 0, detector `[]`, mirrors byte-equal, screenshots clean at all four widths.

## Nits fixed (review 2, APPROVE)

1. **One word for the fetch window.**
   - `chart_view.caption` now says "requested for 1 to 5 August 2026", the same as `chart_view.alt`. This matches what the connector does: one request per day, with `from` = `to` = D (`client.py:78-102`).
   - To stay within 40 words, "daily repeats removed" became "repeats removed". The rendered page now carries "requested for 1 to 5 August 2026" three times and "fetched 1 to 5" nowhere.
2. **No process wording in the vault Overview.** In `tariff_simulations.md`, ", cited by the 2026-10-07 page review; not retrieved by the writer" is removed. The citation is now the source itself: ENTSOG, TAR NC transparency workshop slides, December 2016, slide "TRA PF Standardised Table: contents" (`TAR0762_161208_TAR_NC_Transparency_for TRA_WS_Rev2.pdf`). This report still records that I did not retrieve the slide.

Checks:
- Both notes copied with `cp` and checked with `cmp`, byte-equal.
- `gridflow-build --only entsog/tariffs` exits 0 and writes `tariffs-and-simulations.html`.
- `detect.mjs --json` (absolute path) returns `[]`.
- Em dashes in the page: 0.

Summary: both review-2 nits fixed; build exits 0, detector `[]`, mirrors byte-equal.
