# elexon/temp: review 2 (re-check of Revision 1)

Checker: Opus 5.5, 2026-09-28. Inputs: `temp-author.md` "Revision 1", the canonical note in `vault-p26-elexon`, its
mirror, the rebuilt page.

**Verdict: APPROVE** (0 blocker, 0 major, 1 nit)

## The Elexon quote

- **Verified word for word.** I rendered https://bmrs.elexon.co.uk/api-documentation/endpoint/datasets/TEMP in
  headless Chrome (`--dump-dom`, JavaScript on; a documentation page, not the data API). The page text reads: "This
  endpoint provides the average degree celsius value measured at midday deemed to be representative of the
  temperature for Great Britain. Data is gathered from 6 weather stations. Default output will be the last 31 days.
  Values are received from 5pm each day." The note's Overview quotes it exactly, with the URL and the date read.
- **Correction to review 1.** My "daily average GB temperature data (in Celsius)" was the search index's paraphrase
  and the Open Net Zero mirror, not Elexon's words. The writer was right to follow Elexon's wording: an average
  measured at midday, not a daily mean.
- **The page matches the quote.**
  - `summary`: "midday temperature for Great Britain, averaged over six weather stations".
  - `what_it_is`: "the average °C value measured at midday for Great Britain, gathered from six weather stations".
  - `facts.cadence`: "Measured at midday, per Elexon".
  - `record.fields.temperature`, and the caption's "°C (Elexon's unit)".

  Each is a close paraphrase of the quote. The chart unit, notebook `ylabel` and `plot_alt` °C now rest on a vendor
  fact.
- **Not on the page:** "Values are received from 5pm each day" sits oddly with the 15:45 UTC (16:45 BST) publish
  times in the rows. The page makes no schedule claim, so this is only a note.

## Review 1 findings

1. **major, °C sourced to gridflow's docs.** Fixed. There are 0 hits for "gridflow's docs" in the rendered page. The
   unit is attributed to Elexon, and the vendor quote is in the note body.
2. **major, "one reading per measurement date".** Fixed. There are 0 hits for "one reading per" in the rendered page.
   - The caption now says "one point per measurement date", which describes the chart and holds by the spec's dedup.
   - `facts.grain` is unchanged and still correct (`temp.py:25,96`).
3. **nit, wrong cause in `what_it_is`.** Fixed: "gridflow fetches and dates each row by its publish time, so ...".
   This matches the publish-window fetch and the per-bronze-date silver.
4. **nit, "generation data" in the scenery alt.** This is the seat's, per the coordinator's ruling. Not a finding.
5. **nit, related notes.** Fixed. Both Open-Meteo notes say how the datasets relate, within 12 words.
   - Forecasts for a day do exist before that day's midday value is published.
   - Seven cities against a six-station GB value is consistent with `vault/openmeteo/*_demand.md:12-14`.

## New finding

1. **nit: degree days from one midday reading are an approximation.**
   - **Field:** `page.how_used[1]`, "Heating and cooling degree days, from each measurement date's reading."
   - **What is wrong:** degree days are normally computed from a daily mean. Elexon now states this is a midday
     value, so degree days from it are a proxy.
   - **Fix (optional):** for example "Degree-day style heating and cooling measures, from the midday reading".

## Rebuild and regression

- **Build:** `gridflow-build --only elexon/temp` fails, but only on another writer's page:
  `ERROR: atl: page.what_it_is: 61 words, over its budget of 60`. The vendor-wide content audit runs on every Elexon
  note. Temp's own fields are clean: `parse_page_fields` plus `anatomy_errors` on `vault/elexon/temp.md` return `[]`
  and `[]`. The page on disk (written 22:07:46 by the writer's passing build) carries the revised text. This needs a
  green build once `atl` is fixed, before merge.
- **Detector:** `detect.mjs --json` returns `[]`.
- **Mirror:** byte-identical to the canonical note (`cmp` clean).
- **Artefacts:** series, sample and notebook are unchanged (all timestamped 21:46, before review 1). The spec,
  select and cells are unedited, so `alt`, `plot_alt`, the eight rows and the notebook outputs still match.
- **Wording:** grep of the rendered text finds no local-data words, em dashes, middle dots, "→", "live", "now" or
  planning labels.
- **Screenshots:** headless Chrome through a static server on 9717, at 1440 and at 390 (in an iframe). The
  lengthened summary and cadence in the hero, `what_it_is`, the caption and the longer related notes all wrap
  cleanly. Nothing is clipped or overlapping. The rest of the page is unchanged from review 1.

## For the seat

- The `atl` budget error blocks every `--only elexon/*` build until its writer trims one word.
- The note body's Overview still says "The dataset publishes one record per measurement date". That sentence is
  older than this writer's work and not on the page. It could be reworded from Elexon's quote at the next vault pass.
