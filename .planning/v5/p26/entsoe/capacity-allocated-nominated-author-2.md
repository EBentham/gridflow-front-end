# capacity-allocated-nominated: author response to review 1

Writer: Opus 5.5 · high, 2026-09-29. Answers `capacity-allocated-nominated-review.md`, which found 0 blockers, 1 major and 7 nits. All eight findings are fixed.

## Status

- **Notes:** edited the canonical lead note (`vault-p26-entsoe/30-vendors/entsoe/datasets/total_capacity_allocated.md`) and the nominated note, then mirrored both byte for byte (CRLF kept: 293/293 and 215/215 lines).
- **Notebook:** reran `scripts/run_notebooks.py`, because the cells changed. 5 cells, no errors, 1 image. The df header is now `["", "timestamp_utc", "allocated", "nominated_A07"]`.
- **Series and sample:** not rerun. The chart spec and `record.select` are unchanged, so their digests still match and the build passes.
- **Build:** `gridflow-build --only entsoe/total_capacity_allocated` passes.
- **Detector** (absolute path): only `em-dash-overuse`, the accepted advisory. The page has 0 real em dashes, and no literal backticks leak into alt text.
- **Screenshots, all Chrome calls under `timeout 60`:**
  - Retook the changed prose (what it is, how it's used, chart caption, key note, raw feed) at 1440 and 390.
  - Opened the notebook drawer in the Browser pane on port 9815 and measured it. The plot image is 799/799 px of its container at 1024 and 300/300 at 390; the page has no horizontal overflow (document width 390 at 390).
  - Nothing is clipped. The server is stopped and the viewport reset.

## Findings and fixes

| # | Severity | Fix (field: new text) | Words |
|---|---|---|---|
| 1 | major | `what_it_is`: "…Total nominated capacity (12.1.b) is what was nominated per market time unit; GB replies carry three contract series, `A01`, `A06` and `A07`, and silver keeps only `A07`. Rows with `in_area_code` GB read as capacity into GB (project check)." To make room, "Neither is the forecast capacity in `net_transfer_capacity`" was dropped (the NTC related note still says "not allocated or nominated"), and "gridflow requests contract type `A01` (daily)" moved to the lead's `differs` line. | 59/60 |
| 1 | major | Member `differs`: "`B08`, hourly or quarter-hourly; silver keeps `A07` of three contract series (`A01`, `A06`, `A07`)". | 14/14 |
| 1 | major | `notebook.lead`: "…Cells: Belgium into GB, nominated as the `A07` series. Allocated counts only earlier rounds (Art. 12(1)(c)), so `A07` can exceed it." The claim is now scoped to `A07`; the review's counts are 0 hours above 725 MW for `A06`, 27 for `A01` and 37 for `A07`. | 35/35 |
| 1 | major | Notebook cell: the column is renamed `nominated_A07`, so the df header and the plot legend name the series. `plot_alt`: "Nominated A07 (clay)…". No meanings for `A06` or `A07` are given anywhere on the page. | plot_alt 57/60 |
| 1 | major | Lead `differs`: "Business type `A29`, contract type `A01` (daily): one value per Period, as sent". The `A01` = daily source is `endpoints.py:324`. | 13/14 |
| 2 | nit | Cause tied to its source: "Allocated counts only earlier rounds (Art. 12(1)(c)), so `A07` can exceed it." (the review's wording). | in the lead |
| 3 | nit | Key note: "On the axis until 22:00 UTC, 19 September; replies carry auction category `A04` (hourly), not `A01` (base)." Meanings are from `entsoe-codes.md` §5 (code list v36r0). | 17/18 |
| 4 | nit | `record.caption`: "Both GB pairs either side of 22:00 UTC, 19 and 20 September 2026." | 12/16 |
| 5 | nit | `chart_view.caption`: "…Replies send one value per 22:00 to 22:00 UTC Period, which gridflow repeats hourly (curve type `A03`)…" | 38/40 |
| 6 | nit | Plot cell: `ax = both.plot(...)` then `ax.legend(loc="upper left", bbox_to_anchor=(1, 1));`. The legend now sits right of the axes and covers no trace (checked in the new PNG, 877×369). | none |
| 7 | nit | `how_used[2]`: "Hourly `A07` nominations on GB borders, set beside allocated capacity." ("and schedules" dropped). `related[1]` (`commercial_schedules`): "Scheduled exchanges (document type A09) on the same ordered pairs". `A09` is from `endpoints.py:152-153`. | 10/14, 10/12 |
| 8 | nit | Vault bodies, see the next section. | none |

## Body edits (finding 8)

**`total_nominated_capacity.md`**
- **Tuple table:** "(not in request — server returns `A01` on TS)" is now "(not in request; GB replies carry three TimeSeries, `A01`, `A06`, `A07`: see Known issues)".
- **Silver sample:** added a line marking the 3028 and 2928 MW rows as unverified. They are the first TimeSeries of the May bronze sample, while silver keeps the last-listed series, and no May bronze or silver is held.
- **Implementation delta (the 2026-05-08 probe record):** restored the original wording, "one per nominated MarketAgreement / direction split", and appended the observation scoped to its evidence: "in the 2026-08 and 2026-09 replies the three are contract types `A01`, `A06`, `A07`, same direction".

**`total_capacity_allocated.md`**
- **Implementation delta:** the old cause ("post-Brexit GB borders publish no long-term allocation") is now marked as contradicted by bronze. GB/NL and GB/BE return `Publication_MarketDocument` in 14 of 14 files each. The cause of the empty GB/FR border is undocumented.

## Defects for the seat to log

Per the remediation convention (gridflow BACKLOG item 13 and the vault spec page); I did not edit those files myself.

1. **ENTSO-E `total_nominated_capacity`:**
   - Silver keeps one of three contract series. GB replies carry `A01`, `A06` and `A07`.
   - The parser never reads `contract_MarketAgreement.type`: `parsers.py:320-328` matches only the `*MarketAgreement.Type` variants.
   - The dedup key has no contract column (`h6_market.py:91-99`, `keep="last"`), so silver equals `A07` in every hour.
   - Fix: parse the contract type and add it to the column set and the key.
2. **ENTSO-E `total_capacity_allocated`:** GB/NL replies carry `auction.category` `A04` (hourly) although the request sends `auction.Category=A01` (base). The filter's effect for this border is unverified. Silver stores no auction or contract column.
3. **Front-end runner:** `scripts/run_notebooks.py` flattens a named-index pandas header into a misaligned header. Avoided on this page with `reset_index()`.

## Not verified (unchanged from the first report)

- The meanings of `A06` and `A07` (only entsoe-py maps them). The page prints codes only.
- The cause of the allocation steps and of the zero values.
- Direction on continental pairs; the page makes no claim there.
