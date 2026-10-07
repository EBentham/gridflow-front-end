# neso/regional-carbon-intensity: re-review

Checker: Sonnet 5.5 (high), 2026-10-06. Re-check of the writer's response (`regional-carbon-intensity-author-2.md`) against `regional-carbon-intensity-review.md`.

## Verdict: APPROVE

Both majors and all five nits are resolved. No regressions. One optional wording nit below; it does not block.

## Majors

1. **GB key note: fixed.** It now reads "GB as a whole; a project check found it nearer the national `actual` than its `forecast`." It is an observation, flagged as a project check, with no categorical negative and no claim about what NESO does.
   - Reproduced: the GB (region 18) to national mean gap is 3.85 against `actual` and 9.23 against `forecast`, over the 674 shared half-hours. The figures stay in the lead note body, which the coordinator accepted.
   - It renders without clipping at 1440 and in a true 390 px iframe.
2. **Notebook legend: fixed.** Cell 4 now ends `ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.3), frameon=False)`.
   - I viewed the re-run `regional_intensity-6.png` (Oct 6 20:37). The legend is on one row below the axes and covers no line, including the South Wales 98.9 peak on 20 Sep.
   - The notebook JSON was written by `scripts/run_notebooks.py`: 6 cells, no error outputs. The build's digest check passes.

## Nits

3. **North Scotland line under the axis:** accepted as a template item for the seat, not a finding.
4. **fw/pt `differs` lines: fixed and verified against silver.**
   - fw24h is 49 half-hours with the first ending at `from`. fw48h is 97, first ending at `from`. pt24h is 49, last ending at `from`. The postcode and region id variants of all three have the same counts, 49, 97 and 49.
   - Silver coverage was checked again: fw24h runs 31 Jul 23:30 to 1 Aug 23:30, fw48h to 2 Aug 23:30, pt24h 30 Jul 23:30 to 31 Jul 23:30, all with `from` 2026-08-01T00:00Z.
   - All 18 `differs` lines are 14 words or fewer (longest 13).
5. **Forecast vintage: fixed.** The caption ends "NESO does not say whether a past half-hour's forecast is revised." It is 35 words, within the 40-word budget. Dropping the "repeats on every fuel row" clause is fine: the guide line for `forecast_gco2_kwh` still carries it, and the caption keeps "one value per region and half-hour".
6. **Postcode member `dnoregion`: fixed.** The line reads "One postcode, default `RG10` (region 12), over a window; the response lacks `dnoregion`" (13 words). It matches silver, where `dnoregion` is `""` on all rows of `regional_intensity_postcode`.
7. **Vault body: fixed.**
   - The `actual_gco2_kwh` schema row on all 18 notes now reads "Regional responses carry no `actual` (see Known issues), so it is null on every regional row." Grep: 18 of 18 identical lines.
   - "The sample below comes from an earlier request (`RG41`) and does carry `dnoregion`" is accurate. The bronze sample directly below has `"postcode":"RG41"` with `dnoregion` "SSE South".

## Regression checks

- `gridflow-build --only neso/regional_intensity` succeeds (budgets, digests, related pages).
- `detect.mjs --json` at its absolute path returns `[]`.
- All 18 mirrors under `vault/neso/` are `cmp`-equal to the canonical notes (18 of 18). Every line of every note is CRLF.
- Rendered page text: 0 em dashes, 0 arrows, 0 middle dots. No `locally`, `held`, `our`, `since 20`, `% of`, `live`, `now`, `yet`, `soon`, `planned` or `coming`. No planning words introduced.
- Chart series and artefacts are unchanged and still valid (the series equalled my recompute in review 1). No layout change at 1440 or 390.
- Servers: my server on 9890 is stopped, and port 9670 was left alone.

## Optional wording nit (not blocking)

- `page.chart_view.key[gb].note`: "nearer the national `actual` than its `forecast`" is true on average (mean gap 3.9 against 9.2). Half-hour by half-hour GB is nearer the `actual` in 397 of 674, nearer the `forecast` in 230, and tied in 47. If the seat wants it airtight, "on average nearer" costs two words. The coordinator has accepted the current wording.

Summary: APPROVE; both majors and all five nits are resolved, with the build, detector, 18 of 18 mirror `cmp`, and the notebook re-run all clean.
