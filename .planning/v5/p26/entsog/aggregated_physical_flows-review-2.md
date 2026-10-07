# entsog/aggregated_physical_flows: re-check

Checker: Sonnet 5.5 · high, 2026-10-07. Re-check of the writer's round 2 (`aggregated_physical_flows-author-2.md`) against `aggregated_physical_flows-review.md`. Words-only revision: series, sample and notebook files are unchanged.

## Verdict: REVISE

One new major (a sentence that is literally false against the connector), one nit. All three original majors are fixed in substance; the nits are fixed.

## Findings

1. **major** · `page.what_it_is`, `page.chart_view.caption` (and the body's "Not requested" bullet, which is correct and is the model for the fix) · "Entry from other transmission systems and all exits are not requested" / "every exit are not requested" is false for the Northern Ireland pair.
   - The connector requests two aggregates at the Northern Ireland boundary (`connectors/entsog/endpoints.py:48-54`): `IE-TSO-0001` entry from `TransmissionUK-NI------` (entry from another transmission system) and `IE-TSO-0001` exit to it (an exit). The page itself says so in `raw_feed.note` ("five zone filters ... the Northern Ireland pair returned no record") and the request URL carries both. So "entry from other transmission systems ... not requested" and "every exit not requested" each contradict the page's own raw feed. This is an "every" claim, which the rubric requires to be true.
   - The substance (this is not total entry) is right and should stay. Fix by stating what is requested: for example "Entry from other transmission systems and all exits are not returned: the only other aggregates requested, for Northern Ireland, returned no record in the responses fetched" or "... not requested apart from the Northern Ireland pair". The body's bullet already lists the 12 unrequested aggregates exactly.

2. **nit** · `page.notebook.needs` · The text is plain, but the new wording carries literal backticks: the rendered page reads "with gas days 13 to 21 September 2026, aggregates and `physical_flows` ingested." Drop the backticks (the field is not rendered as markdown), for example "gas days 13 to 21 September 2026 of both the aggregates and the point table".

## Original findings, verified

- **Major 1 (total entry impression): fixed apart from finding 1 above.**
  - `title` "Gas entry from production, storage, LNG" (6 words), `summary` ends "terminals only", `chart_view.title` "Production, storage and LNG entry, 13 to 21 September 2026".
  - `caption`: "National Gas Transmission's entry from three source types only ... so this is not total entry." `what_it_is` says the same.
  - No local numbers on the page (St. Fergus and Easington appear only in the vault body, no figures).
  - Title wraps to two lines at 1440, 1024 and 768 and three at 390; nothing clipped.
- **Major 2 (unscoped): fixed.** `raw_feed.note`: "in the responses fetched, the Northern Ireland pair returned no record" (no cause). `what_it_is`: "the responses fetched contained only National Gas Transmission's entry from production, storage and LNG terminals". Matches the bronze (14 bodies, 3 records each, none from `IE-TSO-0001`; `meta.count` 3, `meta.total` 6).
- **Major 3 (counts): fixed.** The note now says storage is 0 on "6 of 14 gas days in 2026-08/09 (1 and 3 August, 15 and 18 to 20 September)", which matches silver (I reproduced the six dates in round 1). The author's report now says 13 named points. Confirmed: 13 distinct names (4, 7 and 2).
- **Nit 4 (`pointType`): fixed.** The Teesside bullet and the Avonmouth part of the `countPointPresents` bullet quote the vendor `pointType` "Aggregated production point - TP ExtEU" (`LNG-00007`) and "Storage point ExtEU" (`LNG-00053`); I re-read these strings in the 2026-09-21 `physical_flows` bronze in round 1. The Teesside defect is withdrawn in the report.
- **Nit 5 (12 unrequested aggregates): fixed.** The body lists entry from `Transmission`, Ireland, Ireland and Northern Ireland combined, the Netherlands, IUK (5) and exit to `Distribution`, `Final Consumers`, `Storage`, Ireland, Ireland and Northern Ireland combined, the Netherlands, IUK (7), all `UK-TSO-0001`. This equals the 12 ids I derived from `aggregate_interconnections` (17 British-zone ids minus the 5 requested). The St. Fergus and Easington sentence is an observation scoped to 2026-08/09 `physical_flows` with their vendor `pointType` ("Cross-Border Transmission IP ... (import)").
- **Nit 6** (seat's, the sibling "summed by balancing zone" lines): not a finding here, as instructed.
- **Nit 7 (`needs`):** content fixed (names both tables); formatting is finding 2.
- **Nit 8 (guide lines):** `indicator`, `data_set_label`, `direction_key`, `adjacent_systems_key` now say what the frame does not show. "Flow direction relative to the zone" and "the category the aggregate groups its points by" are consistent with the code and register.
- **Nit 9 (provisional):** the caption says "kWh/d as sent and provisional"; `flow_status` is `Provisionnal` on all 42 rows.

## No regression

- Mirror: `cmp` of the canonical note and `vault/entsog/aggregated_physical_flows.md` is byte-equal.
- `gridflow-build --only entsog/aggregated_physical_flows`: succeeds (only the generic "no Pydantic class" warnings). Artefact digests pass; series, sample and notebook JSON unchanged.
- Detector (absolute path): only the accepted `em-dash-overuse` advisory ("98 em-dashes", from `UK---------` and `--start`/`--end`). Real em dashes, arrows, middle dots on the page: 0.
- Rubric greps on the rendered text (`locally`, `held`, `our`, `since 20`, `% of`, `live`, `now`, `yet`, `soon`, `planned`, `coming`, `real-time`, `local`): no hits.
- Front matter has no literal `---` (checked earlier; the new page block is only words and `\x2D` escapes in the same places).
- Screenshots (own Chrome profile, port 9895 started and stopped, required flags; 390 in a true 390 px iframe) at 1440, 768 and 390 for the top sections, `what_it_is`, chart title and caption, raw feed, commands and the frame head: nothing clipped or overlapping. Lower sections are unchanged from the first review (words-only revision).
