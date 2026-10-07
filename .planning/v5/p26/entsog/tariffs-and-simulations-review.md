# entsog/tariffs-and-simulations: review

Checker: Sonnet 5.5 · high, 2026-10-07. Family `tariffs-and-simulations` (lead `tariffs`, member `tariff_simulations`). Rubric: `.planning/v5/review-rubric.md`; seat ruling on repeats applied.

## Verdict: REVISE

No blocker. The repeats ruling is met in full (copies identical, nothing lost, every surface dedups and the page says so). Four majors remain: two are on the page (the simulations member, the folded frame hiding every price), one is a missing caveat on a use the page invites (National Gas TSO; arguable, may be ruled a nit), and one is a false fact in the canonical vault notes and in the writer's defect list. All four are small edits. Findings: 0 blocker, 4 major, 6 nit.

## Seat ruling on repeats: met

| Check | Result (read-only, Polars and bronze JSON) |
|---|---|
| Silver rows | `tariffs` 61,220 = 12,244 ids x 5 daily files; `tariff_simulations` 13,910 = 2,782 x 5 |
| Copies identical | Day 2 to 5 compared with day 1, every column except `ingested_at`, `available_at`, `source_run_id`: 0 differing values, same ids, in both tables |
| Bronze identical | The five bronze bodies per dataset are equal record for record (`records identical across days: True`) |
| No loss | Bronze records per day 12,244 / 2,782 (`meta.count` = `meta.total`) = silver rows per day; 66 / 47 bronze fields all carried (73 / 54 silver columns = bronze + `timestamp_utc` + 6 lineage) |
| Dedup surfaces | Series provenance `rows_read` 61,220, `rows_matched` 40, `duplicates_dropped` 32, `rows_used` 8; sample `select.dedup` on `id`; notebook `.drop_duplicates("id")`; `what_it_is` and `raw_feed.note` say plainly that silver repeats the set per fetched day |
| Key | The 6-tuple is unique within a day (12,244 of 12,244); simulations 5-tuple + `period_from` unique (2,782 of 2,782) |

So the repeats are not a hold trigger. One reading caveat for the seat: bronze turns `N/A` price strings into nulls in silver (nit 5), which is not loss of records.

## Findings

### Major

**1. [major] `page.what_it_is`, `page.how_used[2]`, `page.family.members[1].differs`: the page never says what a simulated cost is or what silver keeps of it, and use 3 is not deliverable.**
- The page's whole treatment of the second member is the hero chip, `summary` ("plus simulated costs per product"), one `differs` line ("One simulated cost per product and tariff period, in local currency and euro") and how-used bullet 3 ("Reading an operator's simulated cost of a product beside its published tariff").
- Missing, all of which silver can and must be described by:
  - The two cost columns are **text** (`product_simulation_cost_in_euro` and `_local_currency` are String), with `N/A` on every record that has no cost (both columns at once). Evidence: `s[L].dtype` String, `N/A` in both columns on the same 799 of 2,782 records, 0 nulls.
  - The cost carries no capacity unit and its basis is set by each operator. Operator remarks quoted from silver: "Cost of flowing 1 GWh/day/year through the IP in EUR taking into account the quarterly multiplier" (22 records); "The simulation cost is calculated as the sum of the capacity charge ... and the commodity" (105); "Product Not Available" (159); BBL company sends 365000 EUR for every one of its 10 firm products, daily to yearly (confirmed).
  - What ENTSOG's simulation is. The writer reports "not verified". It is documented: ENTSOG's Transparency Platform standardised table carries "Simulation of costs for flowing 1 GWh/d/y at IP (in local currency and euro)" (ENTSOG TAR NC transparency workshop slides, Dec 2016, `.../publications/Transparency/2016/TAR0762_161208_TAR_NC_Transparency_for TRA_WS_Rev2.pdf`, slide "TRA PF Standardised Table: contents"). A silver remark cites Article 31(2) of Regulation (EU) 2017/460 (195 records). I could not retrieve the regulation text itself, so the slide is the only vendor quote.
- The major rests on the omission above: the task's test is that the page states plainly what silver keeps, and for this member it states nothing (text type, `N/A`, no unit, operator-set basis).
- Wording note on use 3: the two tables do join on operator, point, direction, capacity type and product, so the cost can sit beside the tariff. What silver cannot give is a derivation of one from the other: for yearly firm records, cost divided by the operator's yearly euro kWh/h tariff is 41,667 (1 GWh/d in kWh/h) on 204 of 442 joinable records, and anything from 42 to 5.1e8 on the rest (19 records at 42, 9 at 95,685, 12 at 3.65e8, ...). Bullet 3 is acceptable once the basis caveat is on the page.
- Fix: one or two sentences in `what_it_is` (or `differs`): ENTSOG describes the simulation as the cost of flowing 1 GWh/d for a year at an interconnection point (cite as ENTSOG's own wording, not as a rule for every operator's figure); the cost is kept as text with `N/A` where not sent; each operator sets the basis, so read the cost remark before comparing. `what_it_is` is at its 60-word budget, so something has to go (for example the clause "per kWh/d and per kWh/h of capacity"); `differs` is at 13 of 14.

**2. [major] `page.record.select.columns`: the folded frame shows no price at 1440.**
- The print order is `operator_key, point_key, direction_key, tariff_capacity_type, product_type, product_period_from, product_period_to, operator_currency, applicable_tariff_per_local_currency_k_wh_h_value, ...`. The 1280 px budget (`shots/d_frame.png`, 1440 wide) ends at `operator_currency`, then `…`. The sample exists to show prices; none of the 12 value and unit columns is in view until the reader unfolds and scrolls the frame sideways (`shots/e_open_s1.png` shows 3.138445, 3.63709, 8.76 only after a 1,100 px scroll).
- At 390 the frame shows only `operator_key` and `point_key`: template behaviour, not charged, but it means the price must come first when the budget is tight.
- Brief: "Name the columns that matter ... so they stay in view when the frame folds."
- Fix: the frame fits eight columns. Keep the six key columns, then `applicable_tariff_per_eurk_wh_h_value` and `applicable_tariff_per_eurk_wh_h_unit` as columns 7 and 8; `product_period_to` and `operator_currency` follow. (`product_period_from` stays a key column, so nothing is displaced from the first six.) Then re-run `gridflow-sample` (the sample digest changes) and rebuild; the guide order follows.

**3. [major, arguable] `page.how_used[0]`, `page.chart_view.caption`: the page invites a cross-operator yearly comparison and says nothing of the one operator whose labels are wrong.**
- The chart itself does not overclaim: title and caption name its three operators. The issue is silence on a use the page recommends. How-used bullet 1 says "Comparing yearly firm capacity prices across operators and points in euro". A reader who follows it with the chart's own filter (Yearly, Firm, `Euro/(kWh/h)/y`) and without the 8-key list gets National Gas TSO, the UK-side operator at Bacton, at 0.005876 for Bacton (IUK) exit against Interconnector's 3.63709 on the same point, and Moffat exit at 0.008326: no error, just wrong numbers.
- Evidence: National Gas TSO's 25 priced records carry labels that contradict their products. Moffat exit firm is 0.000299 GBP/(kWh/d) labelled `/y` on the yearly product and on all 11 monthly products (labelled `/m`), euro 0.008326 on all twelve. Verified.
- The reason for leaving it out appears only in the vault note, not on the page.
- Fix: one clause where there is room. Caption is at 31 of 40 words (BUDGET `chart_caption`), so "National Gas TSO is left out: its unit labels contradict its products." (12 words) fits only if two words go (for example swap nit 8's wording in, "the euro column as ENTSOG sends it", for "ENTSOG converts Interconnector's GBP"). `what_it_is` is at 60 of 60, `raw_note` at 27 of 30.
- If the seat prefers, this can be downgraded to a nit: it is silence, not a false statement. I kept it major because it is a silent failure (plausible numbers, no warning).

**4. [major] Canonical notes (`30-vendors/entsog/datasets/tariffs.md` Known issues, "Common-unit column is not comparable across operators") and the author report's Defects list: "Transgaz sends zero capacity prices beside a non-zero common value" is false.**
- Transgaz has 913 records; 902 carry a euro kWh/h price (min 0.000232, max 0.084624), none is zero (`(eur == 0).sum()` = 0; none of the five tariff columns is zero for Transgaz). Example: Csanadpalota entry 0.0009357 euro kWh/h against common unit 0.022457. The common figure is exactly 24 times the euro kWh/h price on all Transgaz yearly rows (ratio 23.99996 to 23.99998), which is another derivation, not a zero price. The writer most likely read a rounded ratio of 0.
- The defect line is written to be pasted into the gridflow backlog as is, so the false claim would be logged. Fix both: say Transgaz's common figure is 24 times its euro kWh/h price (not 1/365), and rewrite the defect line.
- The rest of that bullet checks out: yearly common unit is the euro kWh/h price over 365 for 406 records, over 8,760 for Fluxys Belgium (26) and one bayernets record, other factors for Energinet (65,394 and 6,766), FGSZ and others.

### Nit

**5. [nit] `page.raw_feed.note` ("Values stay as sent") and vault `tariffs.md` Known issues, "827 of 12,244 records carry none of the five tariff values".** True (816 + 11), but 816 of them arrive from the vendor as the string `N/A` (bronze `applicableTariffPerEURKWhHValue` etc.) and silver casts them to null (`cast(Float64, strict=False)`), while the 11 evergreen Transgaz records are absent in bronze. Say so; the page's guide reads `N/A` as text only for `multiplier`.

**6. [nit] `page.notebook.plot_alt`.** "between 1.008 in February and 1.116 from October to March": November is 1.08 and February 1.008 (silver: 1.116, 1.08, 1.116, 1.116, 1.008, 1.116 for Oct to Mar; 1.44 to 1.488 Apr to Sep). Reword to "between 1.008 and 1.116 from October to March, then 1.44 to 1.488 from April".

**7. [nit] `page.chart_view.key[*].label` and notes: `IZT` and `IUK` are never expanded.** `IZT` is ENTSOG's point name "Zeebrugge IZT" and `IUK` a balancing-zone value as sent; both appear in every bar label and note. A reader in energy trading will know Interconnector but may not know IZT. One of the notes could say "Zeebrugge IZT (Interconnector's terminal)", if that is verified; I did not verify it.

**8. [nit] `page.chart_view.caption`: "ENTSOG converts Interconnector's GBP".** Silver shows the euro columns and an `exchange_rate_reference_date` of 2025-07-03 and a ratio of 1.15888 EUR/GBP, but who converts is not documented (the writer lists it as unverified). Say "the euro column as ENTSOG sends it", matching the guide line.

**9. [nit] Bar value labels are rounded to two significant figures** (19, 8.8, 8.1, 3.6) while the alt text and the notes carry 19.32, 8.76, 8.112, 3.637 and 3.63709. Template behaviour, already reported by the writer; the series JSON is right (19.32, 8.76 x 2, 8.112, 3.637 x 4), recomputed from silver (matches to 1e-9 after dedup).

**10. [nit] `page.notebook.cells[0]` window.** `data.entsog.query("tariffs", "2025-10-01", "2026-04-01")` filters on `timestamp_utc`, the tariff-period start, and hard-codes the three period starts in force in August 2026. A reader who fetches a day after a new tariff period starts (a new October period) would not see it. The lead explains the date column but not this; consider a single sentence, or a wider end date.

## What was checked and found correct

- Facts (rubric 1): every sentence in `what_it_is`, `how_used[1:3]` (except finding 1/3 above), `raw_feed.note`, `record.fields` and `family.members[].differs` holds. In particular: euro columns equal local ones for euro operators (0 of 8,083 differ); the kWh/h value is 24 times the kWh/d value (23.99999 to 24.00001 where the kWh/d value is at least 0.01); 72 within-day records carry `/d` (Snam Rete Gas 42, GASCADE 12, Enagas 6, REN 4, NaTran Deutschland 4, NEL 2, Fluxys TENP 2); 21 country codes (plus 11 null) and 8 currencies in `tariffs`, 21 country codes in `tariff_simulations`, 37 operators, 138 points, 321 operator-point-directions; the three tariff-period starts hold 3,351 / 8,715 / 178 tariffs and 538 / 2,170 / 74 simulations.
- `countryKey=UK`: the connector sends it (`connectors/entsog/endpoints.py:187,196`), `meta.query` echoes it, and the response covers 21 countries. The page says "rows cover operators across Europe", with no count: correct and plain.
- Request URLs: verbatim from the bronze sidecar (`request_url` for 2026-08-01); `limit=-1&timeZone=UCT&from=&to=&countryKey=UK`.
- Commands: `ingest --start 2026-08-01 --end 2026-08-02` fetches exactly 1 August (`client.py` `day_subwindows`, half-open; `utils/time.py`); `transform --end` is inclusive; one transform per day is right because bronze and silver are per day.
- Time stamps: `timestamp_utc` = `period_from` (`generic.py:181-187`), UTC conversion of the +02:00 stamps (06:00 CEST becomes 04:00 UTC) matches the frame; `last_update_date_time` is the vendor stamp; `ingested_at` is the transform time. No stamp is called a fetch or publish time.
- Chart: 8 bars, 1 series, one unit on the axis (`Euro/(kWh/h)/y`, enforced by the filter, the euro value column); recomputed 19.32, 8.76, 8.76, 8.112, 3.637 x 4 from silver. Writer's reason for the per-product euro column over the "common unit" column holds: yearly common figure is price/365 for most operators, /8,760 for Fluxys Belgium (19.32 gives 0.002205 against BBL's 0.024), other factors for Energinet. National Gas TSO's unit labels do contradict its products (finding 3). Bar labels at 390 are not clipped; all 8 labels, the unit line and the key are fully visible.
- Provenance: `spec_origin: vault`, build digest check passes, no staged spec or authored override; sample is `gridflow-sample`, 8 real rows x 73 columns; notebook JSON written by `run_notebooks.py`, no error outputs, read-only cells, `tariffs-5.png` matches the data; `plot_alt` apart from nit 6.
- Checks run: `gridflow-build --only entsog/tariffs` exits 0 (only the generic "no Pydantic class" warnings); `detect.mjs --json` returns `[]`; mirrors `cmp` byte-equal for `tariffs.md` and `tariff_simulations.md`; member pointers resolve (`#tariffs`, `#tariff_simulations` exist on the page).
- Greps on the rendered text (`locally`, `held`, `our`, `since 20`, `% of`, digits plus `rows` or `days`, `live`, `now`, `yet`, `soon`, `planned`, `coming`, `real-time`, em dash, arrow, middle dot): 0 hits. No local row counts on the page (the notebook's 3,351 / 8,715 / 178 and currency counts are notebook outputs after dedup, allowed by the rubric).
- Screenshots (mine, 1440, 1024, 768 and 390 in a true 390 px iframe; light only, the site has no dark theme): hero scenery, chart, key, raw feed, folded and unfolded frame, guide and notebook panel show nothing clipped or overlapping. Unfolded frame at 1440 scrolls sideways inside its box as designed; the unfolded price columns are right (3.138445 GBP, 3.63709 EUR, 8.76).
- Body edits (rubric 7), read from `git diff origin/master` in the vault worktree (both notes): the removed lines in `tariffs.md` are the old `countryKey` "filter to one country" row, the old dedup-key and point-in-time lines, the old silver schema rows (wrong dtypes, the broken `id | str | int` and `data_set | str | int` rows), the bronze-shaped Transgaz sample with `+02:00` stamps, four stale Known-issues bullets (`countryKey` recommended, mixed currencies, sparse rows, evergreen periods) and a `TODO` modelling note. Nothing unrelated is removed; the curl examples, bronze samples and operational-data bullets are untouched. Each replacement cites code or silver. The only wrong fact I found is finding 4.

## Defects to log (beyond the writer's list)

- **[vendor data / vault] Transgaz common-unit figure is 24 times its euro kWh/h price**, not the price over 365 and not zero (902 priced Transgaz records, ratio 23.99996 to 23.99998). Replaces the "zero capacity prices" wording in the writer's defect list.
- **[gridflow silver] Bronze `N/A` price strings become nulls** for the five numeric tariff columns (816 of 12,244 records in a fetched day), while `multiplier`, `seasonal_factor`, the two commodity columns and `exchange_rate_reference_date` keep `N/A` as text; the same table mixes both conventions.
- **[vault] Tariff simulation definition not in the vendor notes.** ENTSOG's TAR NC transparency workshop (Dec 2016) gives "Simulation of costs for flowing 1 GWh/d/y at IP (in local currency and euro)"; add it to `30-vendors/entsog/` with its source.
