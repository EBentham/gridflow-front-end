# gie/lng: author round 2 (fixes to lng-review.md)

Writer: Opus 5.5 · high, 2026-09-29. Screenshots on port 9853. The server there ran under `timeout 400` and stops by
itself. Port 9670 was not touched. No git.

## Findings addressed

1. **Major: vendor `status` caveat near the chart.** I added one key note each to `page.chart_view.key` for `fr` and
   `nl`, which render directly beside the chart:
   - France: "The 18 Sep value arrived with vendor status code `E`, which gridflow does not keep." (15 words, budget 18)
   - Netherlands: "The 17 Sep value arrived with vendor status code `E`, which gridflow does not keep."
   - **Wording choices:**
     - It never says "estimated" or "provisional"; a grep of the page and the note finds neither. No code, schema or
       vault page defines the codes.
     - It gives no count. The reviewer warned against counting `E` rows as a statistic about our copy. Each note names
       the specific point, which is visible in the chart, and so meets the seat's "two values" intent without a
       tally.
     - `raw_feed.note` still lists `status` among the fields silver drops.
   - **Evidence (from the review):**
     - Bronze `gie_alsi/lng/2026/09/13/*` holds NL 2026-09-17 `status: "E"` (`sendOut` 734.6) and FR 2026-09-18
       `status: "E"` (`sendOut` 1052.8).
     - Both are in the committed series (`nl[4]` = 734.6, `fr[5]` = 1052.8).
     - `status` is absent from `output_cols` (`silver/gie/alsi.py:167-181`).
2. **Nit: Overview opening line (note body).**
   - Before: "Country-level LNG terminal inventory and flow data from GIE ALSI."
   - After: "Country-level LNG terminal send-out data from GIE ALSI (the response also carries inventory, which silver does
     not keep yet)."
   - Evidence: `alsi.py:95-97` field map versus the bronze `inventory: {lng, gwh}`.
3. **Nit: `page.what_it_is`, "never per terminal".**
   - The phrase now reads "one row per country and gas day; gridflow asks for country figures, not terminals", which is
     scoped to the request (`endpoints.py:17`; `client.py` `_fetch_country` sends only `country`, `from`, `till`,
     `page`, `size`).
   - To stay within 60 words I also shortened "GB arrives as `-` placeholders, stored as nulls" to "GB's `-` placeholders
     become nulls", with the same meaning. The field is now 59 words.

## Gates

- **Mirror:** canonical `vault-p26-gie/30-vendors/gie/datasets/lng.md` copied to `p26-gie/vault/gie/lng.md`. `cmp`
  reports them identical; the file is CRLF throughout (202 CRLF out of 202 LF).
- **Build:** `uv run --system-certs --extra build gridflow-build --only gie/lng` wrote `data-sources/gie/lng.html`
  with no errors. Its warnings are only for other GIE datasets.
- **No re-distil needed:** the chart spec is unchanged, so the series digest still passes.
- **Detector:** `node C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow-front-end/.claude/skills/impeccable/scripts/detect.mjs --json site/hifi/data-sources/gie/lng.html`
  returns `[]`.
- **Screenshots:** chart and key checked at 1440, 1024, 768 and a true 390 (iframe). Every Chrome call was wrapped in
  `timeout 60`. Files are in `scratchpad/lng-shots/`.
  - Both key notes wrap under their entries at every width.
  - Nothing is clipped or overlapping.
  - The 1440 light and 1024 light full-page captures stopped short this run, after the chart. This is a headless
    render-budget artefact, as the reviewer also saw. The chart and key tiles at those widths are complete, and 1024
    dark at full height shows the rest.
  - Nothing below the chart changed except the `what_it_is` prose, which I checked in the 390 tile.

## Defects

Unchanged from `lng-author.md`. The reviewer's "vendor `status` codes are undefined and dropped" defect adds the named
unknown: what `C`, `E` and `N` mean in ALSI, and whether and when GIE revises `E` rows.

Summary: all three review findings are fixed (status `E` notes on FR 18 Sep and NL 17 Sep, inventory overclaim removed
from the Overview, "not terminals" scoped to what gridflow requests); the build is green and the detector returns `[]`.
