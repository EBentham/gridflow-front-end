# entsoe/forecast_margin: checker re-check (round 2)

**Verdict: APPROVE.** Both majors and both nits from `forecast_margin-review.md` are fixed, with nothing regressed. One optional nit is below; it doesn't block.

## The two majors

1. **Suggested uses: fixed.** `page.how_used` is now two items:
   - "Reading the 2026 margin in MW for FR, NL and BE, sent positive (A91)."
   - "A slow-moving input to year-ahead price and interconnector spread models."

   Neither needs the sign from silver. The first names only zones that bronze sends as A91: all 36 FR, NL and BE replies are A91, re-counted in round 1. "Flagging" and "Comparing neighbouring" no longer appear in the rendered text.
2. **Notebook: fixed.**
   - **Cell 4** now drops DE-LU before display. The comment is visible in the rendered cell: "# DE-LU is sent negative (A92); silver keeps only 4126, unsigned, so drop it."
   - **Rerun output** (notebook artefact, `generated_by: scripts/run_notebooks.py`, cell n=4): three rows only, FR 1500.000, BE 180.000 and NL 41891.044.
   - **Cell 5** no longer filters. The new `forecast_margin-5.png` shows NL 41,891, FR 1,500 and BE 180 only, so `plot_alt` still holds.
   - **The lead** ends "Drop per-file duplicates, and DE-LU: silver loses its negative (A92) sign."
   - **On the page:** the only unsigned 4126 left is in the two sample-frame rows, which `record.caption` flags (accepted in round 1), and in the comment that states the loss.

## The two nits

3. **`page.what_it_is`: fixed.** It now reads "defines it as, in part, "the difference ... maximum total load"". The quoted words are verbatim from Art. 2(30).
4. **`page.chart_view.caption`: fixed.** "These silver files each repeat it; one copy is kept." DE-LU "is sent negative (A92), and silver drops the sign" keeps its meaning.

## Code-list PDF

- The page carries no link to the code list. Its only external links are the Google Fonts links and the gridflow and gridflow-models GitHub repositories. The note body cites "ENTSO-E Code Lists v29r0, section 3.4 BusinessTypeList (p. 16)" by name, with no URL.
- The 404 in round 1 came from a URL I guessed myself. The writer fetched the PDF successfully this session. **No finding.**

## Regression checks

- **Build:** `gridflow-build --only entsoe/forecast_margin` is green: it rendered the page, and budgets, digests and related all pass.
- **Detector:** `detect.mjs --json` at its absolute path returns only the accepted `em-dash-overuse` advisory (`advisory: true`, from EIC padding).
- **Canonical note:** CRLF with 294 CRLF line endings and 0 LF-only. The front matter has no `---`. The mirror is byte-identical (`cmp`).
- **Rendered text:** 0 em dashes, 0 middle dots, 0 arrows. No local-data wording.
- **Unchanged:** the chart spec and `record.select`, so the series and sample digests stand, as the build confirms.
- **Screenshots:** headless Chrome under `timeout 60` with `--timeout=15000 --virtual-time-budget=5000`, served on 127.0.0.1:9860 (server stopped).
  - **Widths:** 1440, 1024, 768, and 390 through a 390 px iframe, with the frame unfolded and the notebook open.
  - **Checked:** the topsoil (what_it_is, the two uses), the chart caption, the notebook lead, the cell 4 comment and its three-row output, and the plot.
  - **Result:** nothing is clipped or overlapping. The cell 4 output scrolls inside `.df-wrap` at 390.
  - **Retake:** one 1440 capture broke off mid-page, a paint-timing artefact; the retake was complete and clean.
  - **Files:** `scratchpad/fmrev/shots2/`.

## Optional nit (non-blocking)

5. **nit, `page.how_used[0]`.** "Reading the 2026 margin in MW for FR, NL and BE, sent positive (A91)" is true, and it doesn't need the sign. It is thin as a use, though: close to restating what the chart shows. A reader-facing use for these three zones would be stronger, for example "Comparing FR, NL and BE's year-ahead adequacy; all three are sent positive (A91)". Taste is Bobbo's; no change required.

Summary: APPROVE. Both majors and both nits are fixed, the build is green, the detector shows only the accepted advisory, the page has no code-list link, and screenshots are clean at all four widths.
