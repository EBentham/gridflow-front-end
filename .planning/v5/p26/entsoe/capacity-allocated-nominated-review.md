# capacity-allocated-nominated: review

Family page `capacity-allocated-nominated`: lead `total_capacity_allocated`, member `total_nominated_capacity`. Checker: Opus 5.5 · high, 2026-09-29. Rubric: `.planning/v5/review-rubric.md`. Seat ruling applied: the page ships with the contract-series loss stated; this review checks that statement for accuracy and plainness.

## Verdict: REVISE

0 blockers, 1 major, 7 nits.

The facts all hold: chart, alt, sample rows, notebook output, request, commands, point-time and direction. The one major is that the seat-ruled loss statement is accurate but not plain enough. It sits only in the member's `differs` line, and the notebook, the only place nominated values appear, never says which series its "nominated" line is.

## Findings

### 1. major: the contract-series loss is accurate but not plain enough

**Where:** `page.family.members[1].differs`, `page.notebook.lead`, `page.notebook.plot_alt` (and `page.what_it_is` as the natural home).

**What is wrong:**
- The only statement of the loss is "silver keeps only the last contract series, `A07`", in the member's differs line.
- A reader is never told that replies carry three contract series, or which two are dropped. "The last" means nothing without that.
- The notebook compares allocated against "nominated" and says nominations "can exceed allocated". It never says the plotted line is the `A07` series only.
- The choice of series changes that claim. In the notebook's window, Belgium into GB:
  - `A06` never exceeds the 725 MW allocated.
  - `A01` exceeds it in 27 hours.
  - `A07` exceeds it in 37 hours.
- `commercial_schedules`, the precedent the seat named, states its loss in `what_it_is`: which series a reply holds, which one gridflow keeps, and what is lost.

**Evidence** (reproduced from bronze with an independent XML parse, `can-review/a2.py` and `a3.py`, and from silver):
- **Three series per reply.** Every GB/FR, GB/NL and GB/BE nominated reply (14 of 14 files per pair) carries three TimeSeries in the order `A01`, `A06`, `A07` (`ts_i` 0, 1, 2). FR/DE-LU carries `A07` only, at `PT15M`.
- **Dedup key has no contract column.** The key at `h6_market.py:91-99` is `[timestamp_utc, in_area_code, out_area_code, business_type]`, `keep="last"`.
- **The parser never reads the contract type.** Its `market_agreement_type` matches only `Type_MarketAgreement.Type`, `type_MarketAgreement.Type`, `MarketAgreement.Type` and `marketAgreement.Type`, or a `Type_MarketAgreement`/`type_MarketAgreement` element (`parsers.py:320-328`). `contract_MarketAgreement.type` is none of these, so the field stays `""`, and the transformer's `output_cols` has no such column anyway (`h6_market.py:107-118`). The writer's description is right.
- **Silver is `A07`.** On each GB pair, silver `quantity_mw` equals `A07` in 336 of 336 hours. `A01` differs from `A07` in 148, 159 and 105 hours (GB/BE, GB/FR, GB/NL); `A06` differs in 272, 322 and 154 hours.
- **The series nest.** `A06 <= A01 <= A07` holds in 336 of 336 hours on each GB pair. So silver keeps the largest of the three.
- **Exceedance by series, GB/BE, 14 to 21 Sep.** Hours above 725 MW per day:

| Series | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | Total |
|---|---|---|---|---|---|---|---|---|---|
| `A07` (silver) | 5 | 7 | 9 | 0 | 6 | 2 | 6 | 2 | 37 |
| `A01` | 3 | 7 | 9 | 0 | 6 | 0 | 2 | 0 | 27 |
| `A06` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**Fix (writer's choice of words, within budgets):**
- **Name the three series and the loss** once, in `what_it_is` or the notebook lead. For example: "GB replies carry three contract series, `A01`, `A06` and `A07`; gridflow drops the contract type and keeps `A07`, listed last." `what_it_is` is near its 60-word budget, so something must give. Either the direction sentence can shorten, or "gridflow requests contract type `A01` (daily)" can move to the lead's `differs` line.
- **Label the notebook line.** In the notebook lead or `plot_alt`, say the nominated line is the `A07` series.
- **Plainer `differs` wording.** For example "`B08`, hourly or quarter-hourly; silver keeps `A07` of three contract series (`A01`, `A06`, `A07`)". Check the 14-word budget.
- **Leave out the meanings** of `A06` and `A07`, or attribute them to entsoe-py. The writer's report says no ENTSO-E code list confirmed them. The existing "contract type `A01` (daily)" in `what_it_is` can stand: it has a code source (the `A01=daily products` comment, `endpoints.py:324`). Don't add "(intraday)" to `A07`.

### 2. nit: the notebook lead states a cause as fact

**Where:** `page.notebook.lead`, "Nominations follow later rounds too, so they can exceed allocated."

**What is wrong:**
- "Can exceed" is visible in the notebook output (859 and 851 MW against 725 MW), so it is fine.
- "Nominations follow later rounds too" is the writer's reading of Art. 12(1)(c), but the page doesn't attribute it.

**Evidence:**
- The data are consistent with the reading. The long-term-looking `A06` stays at or below the allocated 725 MW, and drops to 0 at 20 Sep 22:00, in the same hour allocated does (a3/a7 output). That is support, not proof.
- The regulation defines allocated as capacity "already allocated through previous allocation procedures" (quoted in the allocated note body). It says nothing about nominations.

**Fix:** tie the cause to the source. For example: "Allocated counts only earlier allocation rounds (Art. 12(1)(c)), so nominated can exceed it." Fold this into the rewrite for finding 1.

### 3. nit: "echo" is the wrong verb in the Netherlands key note, and the codes are unexplained

**Where:** `page.chart_view.key[0].note`, "replies echo auction category `A04`, not `A01`."

**What is wrong:**
- The fact is right. Every GB/NL allocated Period (28 of 28) carries `auction.category` `A04`. The other five populated pairs carry `A01` (a2 output).
- But the replies do not echo the request; they return a different code.
- The reader also gets no meaning for either code. The ENTSO-E code list gives `auction.Category` `A01` Base and `A04` Hourly (`gridflow/.planning/audit/2026-05-31-vendor-truth-audit/vendor-docs/entsoe-codes.md` §5, built from the official code list v36r0).

**Fix:** for example "replies carry auction category `A04` (hourly), though the request asks for `A01` (base)". Check the 18-word budget.

### 4. nit: the record caption says "step" where Belgium has none on 19 September

**Where:** `page.record.caption`, "Both GB pairs either side of the 22:00 UTC step, 19 and 20 September 2026."

**What is wrong:** on 19 September, GB/BE is 725 MW at both 21:00 and 22:00 (sample rows 1 and 2). There is no step there. Netherlands steps on both days; Belgium only on the 20th.

**Fix:** "either side of 22:00 UTC", or "the 22:00 UTC Period boundary".

### 5. nit: the chart caption credits the reply with gridflow's hourly fill

**Where:** `page.chart_view.caption`, "Each reply sends one value per 22:00 to 22:00 UTC period, repeated hourly."

**What is wrong:**
- The first half is right. All 161 allocated Periods in bronze have exactly one Point, and every Period starts at 22:00Z.
- The hourly repeat, though, is gridflow's A03 forward-fill (`parsers.py:578-601`), not something the reply sends.

**Fix:** for example "one value per 22:00 to 22:00 UTC Period, which gridflow repeats hourly (curve type `A03`)".

### 6. nit: the notebook plot legend covers the nominated trace

**Where:** `page.notebook.cells[2]` (the plot).

**What is wrong:** matplotlib's automatic legend sits over the nominated trace around 20 and 21 September, over the drop from about 840 MW to 0. See `can-review/shots/open_w1440_nb1.png`.

**Fix:** place the legend outside the axes, for example `.legend(loc="upper left", bbox_to_anchor=(1, 1))`, or in a clear corner. Then rerun `scripts/run_notebooks.py`.

### 7. nit: the suggested comparison with schedules returns identical numbers in silver

**Where:** `page.how_used[2]` ("set beside allocated capacity and schedules") and `page.related[1].note` ("set beside nominations").

**What is wrong:**
- On the three GB pairs, silver nominated equals `commercial_schedules` in every hour (336 of 336 per pair, `can-review/a9.py`). Both tables keep a last-listed series.
- A reader who follows this suggestion gets two identical lines.
- Not false, and the page must not state the equality (it is a measured-on-our-copy universal). But the suggested use is weak.

**Fix:** writer's call. Drop "and schedules", or relate `commercial_schedules` another way.

### 8. nit: stale spans left in the vault bodies

These are not on the page, but they contradict the writer's own corrections.

**`total_nominated_capacity.md`:**
- **Line 42:** the tuple table still says "(not in request — server returns `A01` on TS)". This contradicts the new Known-issues bullet (lines 168-172): the replies carry three series.
- **Lines 129-151:** the silver sample still shows GB→FR 3028 and 2928 MW. These match the `A01` TimeSeries in the note's own bronze sample (lines 93-104), and the new defect bullet (lines 173-178) says silver drops that series. No May bronze or silver is held to check them against directly.
- **Line 188:** the writer edited this dated record of the 2026-05-08 live probe to name `A01`, `A06` and `A07`. The evidence is the August and September bronze, not the May reply. Scope it ("as in the 2026-08 and 2026-09 replies") or leave the original wording.

**`total_capacity_allocated.md`:**
- **Line 272:** Implementation delta still gives the cause "post-Brexit GB borders publish no long-term allocation". This is contradicted by the writer's new line 258-261 and by bronze: GB/NL and GB/BE return `Publication_MarketDocument` in 14 of 14 files each.

## Checked, no finding

**Chart**
- **Series against silver:** 2 × 192 hourly points, 0 mismatches against silver (`can-review/b1.py`).
  - Netherlands: 0, then 850 MW from 19 Sep 22:00, then 900 MW from 20 Sep 22:00.
  - Belgium: 725 MW, then 0 from 20 Sep 22:00.
  - This matches the alt text, the key note and the `x_label`.
- **Provenance:** `spec_origin: vault`. No staged spec or authored override remains.
- **Build:** `gridflow-build --only entsoe/total_capacity_allocated` succeeds.
- **Detector:** only the accepted `em-dash-overuse` advisory (EIC dashes).

**Frame, notebook and request**
- **Sample rows:** the 8 rows are real (`gridflow-sample`) and show both steps. Every field line is true against code.
  - Point time: period start + (position − 1) × resolution, per `parsers.py:530`.
  - Cadence "as received": allocated has one Point per Period; nominated is `PT60M` on GB pairs and `PT15M` on FR/DE-LU.
  - `published_at`: the response `createdDateTime`, between −1 s and 27 s from the bronze file's fetch stamp across all files.
- **Notebook output:** matches silver (859, 851, 36, 65, 255 and 842 MW nominated around the step).
  - `plot_alt` values are right: maximum 1,055 MW at 14 Sep 10:00; above 725 MW on 7 of 8 days; 0 from 21 Sep 04:00 to 23:00.
  - The plot colours are `--petrol` and the clay `--fuel-gas` token.
  - The notebook JSON comes from `run_notebooks.py`, has read-only cells and no errors.
- **Request and commands:**
  - The request matches the bronze `request_url`: parameter order and `auction.Category`/`contract_MarketAgreement.Type` casing (`endpoints.py:263-274`).
  - "Eight pairs" matches `_FLOW_PAIRS` (`client.py:39-48`).
  - Ingest end is excluded (`day_subwindows`); transform end is included. `EVENT_WINDOW_FILTER` (`h6_market.py:228`) means silver day D reads bronze day D.

**Direction**
- "GB rows read as capacity into GB (project check)" is labelled correctly.
- Nominated GB rows correlate with `cross_border_flows` on the same ordered pair: r = 0.929 (GB/FR), 0.933 (GB/NL) and 0.878 (GB/BE), reproduced.
  - `cross_border_flows`' own direction is a project check against Elexon.
  - Only one direction is requested, so no reverse-pair control exists.
- The allocated table cannot be correlated, because its values are flat per day. It relies on the same `in_Domain` parameter, and its vault note points to the nominated check. That is acceptable.

**Other rubric checks**
- **Local-data grep:** clean. The only "rows" hits are generic wording. No em dashes, arrows, middle dots, or "live"/"now".
- **Screenshots:** 1440, 1024, 768 and 390, light only (the site has no dark theme: no `prefers-color-scheme` or `data-theme` in `assets/`). I checked the hero scenery, chart, raw feed, folded and unfolded frame, guide, open notebook, related section and corner labels.
  - Nothing is clipped or overlapping, except finding 6.
  - The known notebook filename clip at 390 (ruling #39) and the df table's sideways scroll at 390 are template behaviour.
- **Mirrors:** both notes are byte-identical to the vault worktree.

## Scratch evidence

Scripts and shots are in `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\a0012501-ff9a-440a-b654-cec67ac10bcf\scratchpad\can-review\`:
- `a1.py` to `a9.py`, `b1.py` and `b2.py`;
- `shots/`: `w<width>_<offset>.png` for the static page, and `open_w<width>_{frame,nb0,nb1,nb2}.png` for the open states.

Both servers on port 9826 are stopped.
