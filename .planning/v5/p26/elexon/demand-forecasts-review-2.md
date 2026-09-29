# demand-forecasts: checker review 2

Re-check of Revision 1 in `demand-forecasts-author.md`, against `demand-forecasts-review.md`. Checker, 2026-09-29.

## Verdict: APPROVE

All four findings are fixed, and nothing else broke. There are no new findings.

## The four findings

1. **The major, `page.what_it_is` attribution: fixed.**
   - The text now reads "which NESO equates with `INDO`" and "which NESO equates with `ITSDO`".
   - This matches NESO's equivalences quoted in `indo.md` (#01:244, #01:268), and the `demand-outturn` page's "NESO
     defines" wording.
   - The rendered page carries the new text.
2. **The notebook lead: fixed.** It now reads "The query cell converts times to UTC".
3. **The boundary count: fixed.**
   - `what_it_is` says "beside other boundary codes (`B1`, `B2` and so on)".
   - `family.members[tsdf].differs` says "Transmission demand at `N` plus other boundary codes; one vintage per publish
     day".
   - Neither "17 transmission" nor `B17` appears anywhere in the built page.
4. **The grain line: fixed.**
   - `facts.grain` now reads "NDF: half-hour and publish; TSDF: half-hour, boundary, publish day; NDFD, TSDFD: date,
     publish".
   - It matches the code:
     - NDF and NDFD: key `demand_forecast.py:150-153`, which includes `published_at`;
     - TSDF: dedup within each daily transform, `tsdf.py:112-115`;
     - TSDFD: `tsdfd.py:99`, also per daily transform.
   - For TSDFD, "publish" equals "publish day" here: every local NDFD and TSDFD silver file holds exactly one
     `published_at`, and both datasets are published daily.
5. **Optional body note, taken:** `ndfd.md` and `tsdfd.md` now say "the fields do not say which daily statistic".

## Nothing else broke

- **Build:** `gridflow-build --only elexon/ndf` succeeds, with no digest failures. The chart, record selection and
  notebook cells are unchanged, so the series, sample and notebook artefacts still match.
- **Detector:** `detect.mjs --json` on `demand-forecasts.html` returns `[]`.
- **Mirrors:** all four mirror copies (`ndf`, `ndfd`, `tsdf`, `tsdfd`) are byte-identical to the vault notes.
- **Text:** the rendered page has no em dash and no "→".
- **Screenshots:** headless Chrome at 1440, 1024 and 768, and 390 through a same-origin 390 px iframe.
  - The longer grain line wraps to three lines at 1440 and 390, and to two at 1024 and 768.
  - Nothing is clipped or overlapping in the hero facts, the scenery or `What it is`.
- **Not re-checked:** the chart, raw feed, frame, notebook and related sections. Revision 1 did not change them, and they
  passed in review 1.
