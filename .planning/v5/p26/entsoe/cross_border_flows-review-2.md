# entsoe/cross_border_flows: checker re-review (Revision 1)

Checker: Opus 5.5 · high, 2026-09-29. This re-checks the canonical note in `vault-p26-entsoe` and the rebuilt page and re-distilled series in `p26-entsoe` against `cross_border_flows-review.md`.

## Verdict: APPROVE

All 8 findings are fixed, and nothing the revision touched broke. One new nit is left; it does not block.

## Findings from review 1

1. **Blocker, `record.fields.timestamp_utc`: fixed.** It now reads "period start plus (position minus one) resolutions", which matches `parsers.py:530,582`.
2. **Major, `raw_feed.requests[0]` and `raw_feed.note`: fixed.**
   - The request escapes the dashes as `\x2D` in the front matter and renders as `in_Domain=10YGB----------A&out_Domain=10YFR-RTE------C`. This is identical to the bronze sidecar's `request_url`.
   - The page has no `%2D` (grep count 0), and the note no longer mentions it.
   - The URL no longer wraps into blank gaps at 390 (`scratchpad/cbf-review/r2-390-open-c2.png`).
3. **Major, `chart_view.caption` and `alt`: fixed.**
   - The caption names "the France, Belgium and Netherlands series with `in_area_code` GB", and the alt says "three series".
   - No reason is given for leaving out IE-SEM, as intended.
4. **Major, `related[2].note`: fixed.** It now reads "Prices at the continental and Irish ends; none for GB". This matches the `day_ahead_prices` note (GB returns Acknowledgement 999) and silver (59C, 82H, BE, FR and NL present, no GB). It is 9 words.
5. **Major, `facts.cadence`: fixed.**
   - It now reads "Per series, as `resolution` states; `PT60M` or `PT15M` in these rows", which is scoped to the rows shown.
   - The body Overview is scoped the same way and says one border switched.
6. **Nit, `chart.filter`: fixed.**
   - The filter is now `in_area_code eq "10YGB…A"` plus `out_area_code in [FR, BE, NL]`, and the stale comment is gone. `in` is a supported op (`chart_spec.py:65`).
   - Re-distilled: `spec_origin: vault`, the build digest passes and `rows_used` is 1,512 as before.
   - The series equals my own Polars hourly mean of silver for all 3 × 168 points (max |diff| 0.0005 MW, which is rounding). The chart data is unchanged.
7. **Nit, note-body direction wording: fixed.**
   - The Overview now says "positive as import to GB is itself a project check, not an Elexon rule".
   - The IE-SEM row reads "checked, weaker: hourly correlation about 0.79…; at most 70 MW while GB exported", which matches my figures.
   - The netting line now adds "gridflow cannot serve this yet: it requests one direction per border (`client.py:40-49`)".
8. **Nit, `chart_view.key[0].note`: fixed.** It now reads "positive parts of … summed".

## New findings

1. **nit, note body, Bronze layer path cite `bronze/writer.py:32-33,56`**
   - **What is wrong.** The name parts sit on lines 33-34: `body_hash = …[:8]` is `:33` and `ts = response.fetched_at.strftime(...)` is `:34`. Line 56 (`filename = …`) is right.
   - **Correction to review 1.** My first review listed this cite as confirmed. It is off by one.

## Regression checks

- **Gates.** `gridflow-build --only entsoe/cross_border_flows` is OK. `detect.mjs` returns only the accepted `em-dash-overuse` advisory (EIC padding).
- **Page text.** The rendered page has no em dash, `→`, `·`, `locally` or `held`.
- **Mirror.** `vault/entsoe/cross_border_flows.md` has the same content as the canonical note, ignoring CRs; the mirror is LF, as committed on `main`.
- **Unchanged artefacts.** The sample and notebook artefacts are unchanged (19:06 and 19:09), and their `select` and `cells` blocks did not change, so their digests stand.
- **Unchanged fields.** `summary`, `what_it_is`, `how_used`, `commands`, `record`, `notebook` and the other related notes are unchanged from review 1.
- **Screenshots.** Taken with the CDP script on port 9817, with the frame unfolded and the notebook open, at 1440, 768 and 390 (a true 390 viewport).
  - `scrollWidth` equals `innerWidth` at every width.
  - The hero facts, caption, raw feed, guide and notebook plot are fully visible, with nothing clipped or overlapping.
  - I stopped the server afterwards.
