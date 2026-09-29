# entsoe/forecast_margin: author round 2

This answers `forecast_margin-review.md` (REVISE: 2 majors, 2 nits). All four are fixed.

- **The canonical note** (`vault-p26-entsoe/30-vendors/entsoe/datasets/forecast_margin.md`) was edited with the Edit tool.
  - Line endings are still CRLF, with 0 LF-only lines.
  - The front matter has no `---`.
- **The mirror** is `p26-entsoe/vault/entsoe/forecast_margin.md`; `cmp` shows it identical to the canonical note.

## Fixes

1. **Major, `page.how_used`.** Per the seat ruling, no use may need the sign.
   - **Removed:** `how_used[0]`, "Comparing neighbouring zones' expected adequacy...", and `how_used[2]`, "Flagging a zone whose TSO sends a negative margin (A92)...".
   - **New `[0]`:** "Reading the 2026 margin in MW for FR, NL and BE, sent positive (A91)."
     - This is 14 words, within budget.
     - It needs no sign from silver: the three zones are named, and bronze sends each as A91 in all 36 of their replies (review §"What I checked").
   - **Kept:** `[1]`, "A slow-moving input to year-ahead price and interconnector spread models". The review cleared it.
   - There are now two uses, which is within `HOW_USED_COUNT` (2, 3).
2. **Major, the notebook (`cells[1]`, the fourth cell in the run, and `notebook.lead`).**
   - **The cell** now drops DE-LU before display, with a comment saying why: `# DE-LU is sent negative (A92); silver keeps only 4126, unsigned, so drop it.` followed by `df = df[df['zone'] != 'DE-LU']`.
   - **The plot cell** (`cells[2]`) no longer filters, since `df` is already clean.
   - **The lead** now reads: "`query()` reads `silver_entsoe_forecast_margin` by whole UTC days of `timestamp_utc`, ends included, without lineage columns. The 2026 figure is stamped 31 December 2025. Drop per-file duplicates, and DE-LU: silver loses its negative (A92) sign." That is 33 words.
   - **Rerun:** `scripts/run_notebooks.py --dataset entsoe/forecast_margin` gives 5 cells, 1 image and no errors.
     - The fourth cell's output is FR 1500.000, BE 180.000 and NL 41891.044. DE-LU is gone.
     - The fifth cell has only the image. The plot is unchanged, so `plot_alt` still holds (NL 41,891, FR 1,500, BE 180, DE-LU left out).
   - **Comment wording:** the first wording said "sent as a negative margin". The template's code highlighter colours the Python keyword `as` inside a `#` comment. I reworded the comment to avoid it (see "Template observation").
3. **Nit, `page.what_it_is`.** It now reads "defines it as, in part, "the difference ... maximum total load"", so the cut is marked. The note body keeps the full Art. 2(30) text.
4. **Nit, `page.chart_view.caption`.** "Each silver file repeats it" is now "These silver files each repeat it". To stay within 40 words, "it is sent as a negative margin (A92)" became "it is sent negative (A92)". The meaning is unchanged.

## Gates

- **Build:** `gridflow-build --only entsoe/forecast_margin` rendered the page with no errors (budgets, digests and related all pass).
- **Detector:** run at its absolute path, `detect.mjs --json` returns only the accepted `em-dash-overuse` advisory (`advisory: true`), which counts the EIC `--` padding.
- **Rendered page:**
  - 0 em dashes.
  - "Flagging" and "Comparing neighbouring" are gone.
  - "in part", "These silver files" and "silver loses its negative" each appear once.
- **`4126` in the page:** it appears only in the two sample-frame rows (flagged by `record.caption`, which the review accepts) and in the notebook comment that states the sign loss.
- **Unchanged:** the chart spec and `record.select` did not change, so the series and sample digests stand.

## Screenshots

- **How taken:** headless Chrome under `timeout 60` with `--timeout=15000 --virtual-time-budget=5000`, at 1440, 1024 and 768. The 390 check used a 390 px iframe in a 500 px window.
- **Notebook panel:** I also opened "Open the demo notebook" in the Browser pane at 390, all served on 127.0.0.1:9834. The server was stopped afterwards and the pane viewport reset.
- **What I checked:**
  - the topsoil (what_it_is, the two uses);
  - the chart caption;
  - the notebook lead;
  - the opened notebook's fourth cell, its comment and its three-row output, which scrolls inside `.df-wrap` at 390.
- **Result:** nothing is clipped or overlapping.
- **Files:** in the scratchpad at `fm-shots2/`.

## Template observation (for the seat, not fixed here)

- The notebook code highlighter colours Python keywords (for example `as`) inside `#` comments.
  - It is cosmetic. I avoided it here by rewording.

## On the review's note about the code-list PDF

- The review says the v29r0 PDF URL now returns 404. My fetch this session succeeded, and the PDF is saved at `C:\Users\Bobbo\.claude\projects\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\a0012501-ff9a-440a-b654-cec67ac10bcf\tool-results\webfetch-1790713983691-xpg5si.pdf`.
  - A91 and A92 are on p. 16, section 3.4 BusinessTypeList.
  - They agree with the entsoe-py `BSNTYPE` mapping that the reviewer used.

Summary: both majors and both nits are fixed. The two uses no longer need the sign, the notebook drops DE-LU with a stated reason, and the lead says why. The build is green, the detector gives the advisory only, and the screenshots are clean.
