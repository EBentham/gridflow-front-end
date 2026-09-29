# uou2t14d: review 2 (Revision 1)

**Verdict: APPROVE.** 0 blockers, 0 majors, 0 nits. All 7 findings from `uou2t14d-review.md` are fixed, and the
revision broke nothing.

How I checked:
- I read the revised `page:` block and body diff in the vault worktree.
- The mirror is byte-identical to the vault note.
- `gridflow-build --only elexon/uou2t14d` is green, and `detect.mjs --json` returns `[]`.
- The notebook JSON is from `scripts/run_notebooks.py`, and I viewed the new `uou2t14d-5.png`.
- I took screenshots at 1440, 1024, 768 and 390 (390 in an iframe). The site has no dark scheme, so light and dark are
  the same.

## Each finding, re-checked

1. **Key and `published_at`: fixed.** The key keeps its three columns. `record.fields.published_at` now reads "Publish
   time from `publishTime`, UTC; separates fetched days, not in gridflow's dedup key" (13 words). That is true to the
   code:
   - the dedup is `(settlement_date, bm_unit_id)` for each bronze day (`uou2t14d.py:26,133-136`);
   - each fetched day gets its own silver file;
   - the publication-window filter trims the boundary publish (`base.py:1638-1642`, `1786-1805`).

   The body's Dedup key paragraph now cites the filter correctly (this was nit 5).

2. **Null-id collapse: fixed everywhere it appears.**
   - `facts.grain`: "One row per delivery date, unit id and fetched day; null ids share one".
   - `what_it_is`: "one row per Elexon unit id and date per fetched day ...; units without an id collapse to one row".
   - `raw_feed.note`: "one row per Elexon unit id and delivery date from each fetched day".
   - `record.fields.bm_unit_id`: "null-id units collapse to one row per date and fetched day".

   No "per unit" universal is left. The summary and the chart and record captions describe the vendor's figure or the
   rows shown, not silver's grain. The page carries no counts (81 and 555 stay in the body). Frame row 8 (`null`,
   `"WTGRW-1"`, 10.0) is unchanged and real.

3. **Notebook publish selection: fixed.** The first cell converts `published_at` to UTC and keeps
   `dt.strftime("%Y-%m-%d") == "2026-09-21"`. The committed output is one publish, `2026-09-21 20:00:00+00:00`. In round
   1, local silver filtered the same way gave 6,175 rows, one publish, and no repeated `(settlement_date, bm_unit_id)`.
   Cells 4 and 5 are unchanged in what they compute; cell 4's printed rows match silver.

   The lead's "the 21 September fetch's publish" describes a filter on publish date. For delivery dates 23 September to
   5 October the two are the same set, so no finding:
   - 21 September's 23:00 publish adds only 6 October, outside the window;
   - the day before's boundary publish cannot win its day's dedup.

4. **Heysham zero run: fixed.** Cell 5 plots `wide[["T_PEHE-1", "T_SGRWO-6", "T_HEYM11"]]` with colours clay, horizon
   and petrol (Heysham drawn last, Seagreen dashed). The new PNG shows Heysham's petrol line along zero from 23 to 29
   September, and Seagreen is clearly dashed. Peterhead's zero now lies underneath, which "drawn on top" in `plot_alt`
   implies, and the Peterhead key note on the site chart states it. `plot_alt` values still match silver.

5. **Body, Dedup key: fixed.** One added sentence cites `base.py:1638-1642`, `1761-1805` and
   `_publication_window.py:94-117`, and it describes the filter correctly.

6. **Body, Publication lag: fixed.** It now reads "00:00 to 23:00 UTC, plus 00:00 on the 22nd (the publish windows
   include both ends)", which matches the first `publishTime` in `raw_20260926T183410Z_59ab15a1.json`.

7. **`settlement_date` field: fixed.** It now reads "Delivery date the forecast is for, from the vendor `forecastDate`".
   That is the sister page's wording, without "a London date".

## Anything broken by the revision

Nothing:
- the series and sample artefacts are unchanged (timestamps 12:56 and 12:58), and the chart spec and `record.select`
  are untouched;
- the new wording has no local data, planning labels, em dashes, middle dots or "live";
- nothing is clipped or overlapping at any of the four widths, including the longer grain in the hero at 390 and the
  wrapped guide lines;
- at 390 the notebook code wraps mid-token (`"UT` / `C"`); this is the shared template's wrap rule and was already so
  in round 1, so it is not a finding for this page.
