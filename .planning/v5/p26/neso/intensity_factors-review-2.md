# neso/intensity_factors: re-check (review 2)

Checker: Sonnet 5.5 (high), 2026-10-06. Answers `intensity_factors-author-2.md`. Port 9889 (my static server stopped; 9670 untouched).

## Verdict: APPROVE

0 blockers, 0 majors, 1 nit (new, optional). All six findings from review 1 are fixed; nothing regressed.

## Review 1 findings

1. **major, `how_used[2]` revised-factor use: fixed.** The item is gone. `how_used` is now two items (inside the build's range). The only remaining "revised" is in `raw_feed.note` ("so a revised factor replaces the old row"), which stays true (`silver/neso/carbon_intensity.py:132-139`, `:248-251`; `storage/parquet.py:50-54`) and claims nothing silver cannot show.
2. **major, `how_used[0]` weighting: fixed.** Now "Approximate mix weighting; `generation` lumps gas and imports, so assume one factor each." Checked against silver: `neso/generation` (and `generation_current`, `generation_pt24h`) hold one `gas` and one `imports` share and no cycle or country split, so exactly one factor must be assumed for each; the other seven factor fuels (`biomass, coal, hydro, nuclear, other, solar, wind`) match by name. The wording says approximate and says what must be assumed. The chart beside it shows the spread (gas 394 or 651, imports 53 to 474).
3. **nit, `how_used[1]`: fixed.** Now "A per-fuel factor lookup for approximate carbon-intensity features", the note's own Modelling-notes framing. No unsupported merit-order or dispatch claim remains.
4. **nit, unit stated flat: fixed.** `summary` says "labelled gCO2/kWh by gridflow" and `facts.grain` "its factor labelled gCO2/kWh by gridflow". Consistent with `what_it_is` and `record.fields.factor_gco2_kwh` (bronze body is bare integers; label from `schemas/neso.py:52`, `docs/endpoints/neso.md:19`). The chart axis, caption and key still say gCO2/kWh plainly, which is fine next to the hedge in the hero.
5. **nit, `related[2]`: fixed.** `elexon/fuelhh`: "Splits gas by cycle and imports by interconnector, closer to these factors" (12 words). True: `fuelhh` silver `fuel_type` includes `CCGT`, `OCGT`, `INTNED`, `INTFR`, `INTIRL` (and other interconnectors). The "closer to" hedge is right, since `fuelhh` also carries interconnectors with no factor.
6. **nit, `facts.cadence`: fixed.** "One call returns the whole table; gridflow's schedule fetches it weekly", matching `config/sources.yaml:626-629` and attributed to gridflow, with no file name in the public row.

## Are the remaining uses deliverable from silver?

Yes, both.
- Mix weighting: `generation` shares (silver) times the factor table (silver) with one assumed gas and one assumed imports factor; the page says so.
- Factor lookup: the 14-row `neso/intensity_factors` table is exactly this; `data.sql` on `silver_neso_intensity_factors` returns it (notebook outputs, unchanged).

## No regression

- `gridflow-build --only neso/intensity_factors` writes the page, no errors, no out-of-scope sibling error this time.
- `detect.mjs --json site/hifi/data-sources/neso/intensity_factors.html` returns `[]`.
- Em dashes 0, arrows 0, middle dots 0. Leakage grep over the rendered text (`locally`, `held`, `our `, `since 20`, `% of`, `live`, `now`, `real-time`, `yet`, `soon`, `planned`, `coming`, `static`, `merit`): no hits other than the kept "revised" above.
- Mirror byte-equal to the canonical note (`cmp` clean). The vault diff against `origin/master` still has only the three evidenced body edits (`Write mode`, the two Known issues bullets, the relabelled gold link). The edit is confined to the `page:` block, as the writer states.
- Artefacts unchanged: the series values are still `[937, 935, 651, 474, 458, 394, 300, 120, 53, 0, 0, 0, 0, 0]`, `spec_origin: vault`, digests pass; notebook and sample untouched.
- Screenshots, own headless Chrome under `timeout 60` (`--timeout=15000 --virtual-time-budget=5000`; 390 as a true 390 px iframe), viewed at 1440 and 390 over the hero, scenery, facts rows, What it is, How it's used and the chart head: the longer summary and facts wrap cleanly, nothing clipped or overlapping. I did not re-shoot 1024, 768 or the lower strata; those sections are unchanged apart from the related note text, which is checked in the rendered HTML.

## Nit (optional, does not block)

7. **nit** `page.how_used[0]`: "Approximate mix weighting" does not say weighting into what. The second item names "carbon-intensity features", so a reader can infer it, but "Approximate carbon-intensity weighting of a mix" (within budget) would be plainer.
