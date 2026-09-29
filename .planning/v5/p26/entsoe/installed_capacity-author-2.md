# entsoe/installed_capacity: author round 2

This answers `installed_capacity-review.md` (REVISE: 1 major, 4 nits). Everything is fixed.

- The canonical note (`vault-p26-entsoe/30-vendors/entsoe/datasets/installed_capacity.md`) was edited with the Edit tool.
  - Line endings are still CRLF, with 0 LF-only lines.
  - The front matter has no `---`.
- The note was mirrored to `p26-entsoe/vault/entsoe/installed_capacity.md`; `cmp` shows them identical.

## Fixes

1. **Major, the notebook pivot output (now `page.notebook.cells[1]`).**
   - **Change:** the zone map moved into the pivot cell. The pivot now does `.rename(columns=zones).rename_axis(index=None, columns=None)`. This takes the reviewer's fuller fix: a one-row header with readable zone names instead of EIC codes.
   - **The cell** is a double-quoted YAML string, with the EIC dashes written as `\x2D` escapes (ruling #40).
   - **The plot cell** (`cells[2]`) now only maps the five PSR codes and plots. It holds no EIC code, so it is a plain block scalar.
   - **Rerun:** `scripts/run_notebooks.py --dataset entsoe/installed_capacity` gives 5 cells, 1 image and no errors.
   - **Result:**
     - Output `columns` is `['', 'DE-LU', 'BE', 'FR', 'NL']`.
     - Each body row has 4 values under the matching headers.
     - The rendered `<thead>` is `<th></th><th>DE-LU</th><th>BE</th><th>FR</th><th>NL</th>`.
     - The first row is `B01 | 8855.90 | 846.099 | 1434.93000 | 418.0`.
     - The DE-LU B14 cell reads NaN, which agrees with "no B14".
   - **Plot:** the new image is the same chart without the `area_code` x-label and the `production_type` legend title. `plot_alt` still holds: DE-LU solar about 104,000, DE-LU onshore wind about 68,000, FR nuclear about 63,000, no DE-LU nuclear bar, and every BE bar under 12,000.
2. **Nit, `page.facts.cadence`.**
   - Was: "One `P1Y` point per year, as sent; `sources.yaml` schedules weekly fetches".
   - Now: "One `P1Y` point per year, as sent in these responses". The weekly claim is gone.
3. **Nit, "a single annual snapshot".** `what_it_is` now opens "ENTSO-E's installed capacity per bidding zone and production type: a single annual snapshot, one MW figure per type."
4. **Nit, `page.notebook.lead`.** It now reads: "`query()` reads `silver_entsoe_installed_capacity` by whole UTC days of `timestamp_utc`, ends included, without lineage columns. The 2026 row is stamped 31 December 2025 whatever day you ingest, so query that day, then drop per-file duplicates." That is 34 words.
5. **Nit, scoping in `what_it_is`.**
   - The acknowledgements claim now reads "GB and IE-SEM return no-data acknowledgements in these responses".
   - The zero-versus-absent claim now reads "the 2026 document has DE-LU B07 at 0, no B14".
   - The paragraph is 60 words, within budget.

## Gates

- **Build:** `gridflow-build --only entsoe/installed_capacity` wrote the page with no errors.
- **Detector:** run at its absolute path, `detect.mjs --json` returns only the accepted `em-dash-overuse` advisory (`advisory: true`), which counts the EIC `--` padding.
- **Rendered text:**
  - 0 em dashes.
  - "weekly" is gone.
  - "single annual snapshot" appears once and "in these responses" three times: cadence, `what_it_is`, and the raw-feed note.
- **Unchanged:** the chart spec and `record.select` did not change, so the series and sample digests stand. No Chrome was run this round. The visible changes are prose of similar length, and the pivot output is narrower than before (4 value columns in place of a misaligned 9).

## On the review's note about the frame

The reviewer is right: the `…` header cell is a checkbox (`#fx`, "Show the folded columns"). My round-1 report was wrong to say the template has no unfold control. The reviewer checked the unfolded state and found it fine.

Summary: all five review findings are fixed. The notebook pivot is now a one-row header with DE-LU, BE, FR and NL columns; the prose nits are fixed; build green; detector advisory only.
