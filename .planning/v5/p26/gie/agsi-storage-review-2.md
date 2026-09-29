# agsi-storage: checker re-review 2

A focused re-check of `agsi-storage-author-2.md` against `agsi-storage-review.md` (1 major, 7 nits). Checker: Opus 5.5, 2026-09-29.
Seat ruling applied: the related link to the held `gie/unavailability` page stays (`netbsad` precedent), so it is not a finding.

## Verdict: APPROVE

No findings above nit, and no new findings.

## Checks

1. **Major, the plot cell at 390: fixed.** The 33-space hanging indent is gone. The cell is now four lines: the pivot, `colors = [...]`, `ax = net[["DE", "FR", "NL"]].plot(..., color=colors)` and `ax.legend(loc="upper left");`.
   - I measured the code block with the notebook opened, in a 390 px iframe (headless Chrome, `timeout 60`): 285 px wide, **226 px tall** (about 11 lines at 20.8 px), where it was 1,183 px before. `scrollWidth` 283 is within the box, and the page `scrollWidth` 375 is within 390.
   - The screenshot `chk9855/shots/r2_390_a.png` shows the cell wrapping at word boundaries, fully legible.
   - Other widths: 157 px at 768, and 134 px at 1024 and 1440.
2. **The nits.**
   - **TWh wording: fixed.** `what_it_is` now reads "Stock columns are TWh despite `_gwh` names, by our check against the flows and ENTSOG; compare countries by `storage_pct_full`." That is plain, and it is marked as a project check, not GIE's statement.
     - The guide lines for `gas_in_storage_gwh`, `working_gas_volume_gwh`, `consumption_gwh` and the contracted and available capacities say TWh "by our check". That is consistent with the 1,000x ratio and the ENTSOG cross-check, which the writer reproduced (ratio 0.96 to 1.02 on 14 gas days, matching mine).
     - "our check" is the rubric's sanctioned phrasing for a project measurement, not a local-data statistic.
   - **Vault bodies: fixed.** The flows bullet in Known issues cites the ENTSOG check (`silver/entsog/physical_flows.py:27-68`, within 4% on 14 gas days). The stock rows say TWh by our check. The mirror is `cmp` clean for both notes, and CRLF is kept.
   - **GB: fixed.** The caption says "GB sends placeholders, no storage values", and the family `differs` says "GB's storage values are null". Both match the bronze (`-` placeholders plus `consumptionFull` `0`).
   - **`related[2]` (`gie/lng`): fixed.** It now reads "LNG send-out feeds the same national gas balances as storage".
   - **`record.fields.gas_day`: fixed.** It now reads "AGSI's `gasDayStart` date; `event_time` gets a fixed 06:00 UTC project label, not the start". That matches `silver/base.py:383-400`.
   - **`related[0]`:** out of scope by the seat's ruling.
3. **Notebook colours and legend: fixed.** The plot shows DE petrol, FR olive and NL clay (the chart's own paints, three distinct hues). IT, the second teal, is dropped. The upper-left legend sits clear of every line in `storage-5.png`.
   - `plot_alt` now names DE, FR and NL, and its values (FR -759.2 on the 20th; DE -71.7, -711.1, -1.0; NL -429.5; every point below zero) still match silver.
   - The notebook JSON is from `scripts/run_notebooks.py`, source `gie_agsi`, and all cells are read-only with no errors.
   - The `.head()` rows come back in a different order after the rerun (AT, PL, NL, IT, GB). That is expected, because `query()` orders by `gas_day` only, and no page text cites those rows.
4. **No regressions.**
   - `gridflow-build --only gie/storage` wrote `data-sources/gie/agsi-storage.html`, with only the known warnings for other gie datasets.
   - `detect.mjs --json` (absolute path) returns `[]`.
   - A grep of the rendered text finds no em or en dashes, no `→` or `·`, and no "live", "now", "locally" or "held". The chart spec and sample are unchanged, and the series digest still passes the build.
   - My server on 9855 was started and stopped. Port 9670 was not touched.

Summary: APPROVE. The 390 notebook cell is now readable (226 px, from 1,183 px), all seven nits are fixed, build and detector are clean, and nothing regressed.
