# entsog/aggregated_physical_flows: author round 3

Writer: Opus 5.5 · high, 2026-10-07. Response to `aggregated_physical_flows-review-2.md` (REVISE, 1 major, 1 nit). Both are fixed.

## Fixes

1. **Major: the round-2 wording said "all exits are not requested", which is false for the Northern Ireland pair.** `endpoints.py:48-54` requests GNI (UK) entry and exit at the British zone's Northern Ireland transmission boundary.
   - `page.what_it_is` now reads: "ENTSOG's aggregate flow by zone, direction and adjacent system. For the British zone gridflow requests only production, storage and LNG entry, plus Northern Ireland entry and exit, which returned no records in the responses fetched. Entry from other systems and the remaining exits are not requested: this is not total entry. The notebook matches each to its points in `physical_flows`." (60 words)
   - `page.chart_view.caption` now reads: "Silver `entsog/aggregated_physical_flows`, kWh/d as sent and provisional, gas days 13 to 21 September 2026: entry from production, storage and LNG. Northern Ireland entry and exit returned nothing when fetched; other entry and exits are not requested. Not total entry." (39 words)
   - What changed: both fields now name the Northern Ireland entry and exit as requested but empty, scoped to the fetched responses with no cause asserted. They say "other entry and exits" or "the remaining exits" rather than "all exits".
   - To fit the 60-word budget, I dropped two phrases from `what_it_is`: "Values stay in kWh/d" (the summary and caption carry the unit) and the operator name (the alt text and frame carry it).
   - Evidence: `endpoints.py:48-54`. In the 14 bronze bodies, no record has `operatorKey` `IE-TSO-0001`. The `aggregate_interconnections` register lists 12 British-zone aggregates outside the five filters (round-2 report).
2. **Nit: `notebook.needs` rendered literal backticks.** It is now plain text: "gas days 13 to 21 September 2026, aggregate and point-level flows". It renders as "…with gas days 13 to 21 September 2026, aggregate and point-level flows ingested."

The raw-feed note, the title, the summary and the vault body are unchanged from round 2; the raw-feed note already says "the Northern Ireland pair returned no record" in the responses fetched. The artefacts are unchanged.

## Checks

- **Canonical note and mirror.** Page block re-inserted with `scratchpad\apf\fix_note.py --replace-page`, with CRLF kept and the round-2 body edits intact. Mirrored with `cp`; `cmp` shows the files byte-equal, and the note is uniformly CRLF. No literal `---` in the front matter.
- **Build:** `gridflow-build --only entsog/aggregated_physical_flows` passes with the generic "no Pydantic class" warnings only. Budgets pass. Output: `wrote: data-sources/entsog/aggregated_physical_flows.html`.
- **Detector:** run at `C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow-front-end/.claude/skills/impeccable/scripts/detect.mjs --json`. Only the accepted `em-dash-overuse` advisory ("98 em-dashes", from zone codes and CLI flags). Real em dashes: 0.
- **Rubric greps** on the rendered text (locally, held, our, since 20, % of, live, now, yet, soon, planned, coming, real-time, digits followed by rows or days, →, middle dot, em dash, literal backtick): no hits.
- **Screenshots** at 1440, 1024 and 768, and at 390 in a true 390 px iframe:
  - Location: `scratchpad\apf\shots\s_<width>_<n>.png`, contact sheet `sheet_r3.png`.
  - The new `what_it_is` and caption fit at every width, as does the rest of the page; nothing is clipped or overlapping.
  - I removed the temporary `site/hifi/w390-apf.html` helper. The 9875 server stops itself under `timeout`; 9670 was not touched.

## Open items carried from earlier rounds

- The sample must be regenerated once `gridflow-sample` handles `|` in values.
- The `physical_flows` and `nominations` related lines ("summed by balancing zone") are for the seat to reword.

Summary: the Northern Ireland entry and exit are now described as requested but empty in the fetched responses, other entry and the remaining exits as not requested, and `needs` is plain text; build passes, detector shows only the accepted advisory, mirror byte-equal.
