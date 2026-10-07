# entsog/aggregated_physical_flows: author round 2

Writer: Opus 5.5 · high, 2026-10-07. Response to `aggregated_physical_flows-review.md` (REVISE, 0 blockers, 3 majors, 6 nits). Every finding is addressed; nit 6 is in another note, so it is passed to the seat.

## Status

- **Canonical note edited.** I used the same count-asserted scripts as round 1 (`scratchpad\apf\fix_note.py --replace-page` for the page block, `scratchpad\apf\fix2_body.py` for the body), with CRLF kept.
  - Mirrored with `cp`; `cmp` shows the files byte-equal, and the note is uniformly CRLF.
  - The front matter has no literal `---`, and its YAML parses.
- **Build:** `gridflow-build --only entsog/aggregated_physical_flows` passes. The only warnings are the generic "no Pydantic class" notices. Output: `wrote: data-sources/entsog/aggregated_physical_flows.html (dataset template)`.
- **Detector:** I ran it at its absolute path, `C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow-front-end/.claude/skills/impeccable/scripts/detect.mjs --json`. It returns only the accepted `em-dash-overuse` advisory ("98 em-dashes"), triggered by the `UK---------` codes and the `--start`/`--end` flags. Real em dashes: 0.
- **Rubric greps** on the rendered text found nothing.
  - My first revision wrote "the responses fetched held only", which tripped the `held` grep; it now reads "contained only".
  - The only "returned no record" is the scoped `raw_feed.note` sentence.
- **Artefacts:** the series, sample and notebook are unchanged. No chart spec, record select or notebook cell changed, only words. The build's digest checks pass.
- **Screenshots** at 1440, 1024 and 768, and at 390 in a true 390 px iframe:
  - Location: `scratchpad\apf\shots\s_<width>_<n>.png`; the top sections are in `sheet_r2_top.png`.
  - The longer title wraps to two lines at 1440, 1024 and 768 and to three at 390.
  - The new caption, `what_it_is` and raw-feed note fit.
  - Nothing is clipped or overlapping.
  - I removed the temporary 390 helper `site/hifi/w390-apf.html` again. The 9875 server stops itself under `timeout`; 9670 was not touched.

## Findings and fixes

1. **Major 1: the page read as total zone entry.**
   - `page.title`: "Physical gas flows by zone" becomes "Gas entry from production, storage, LNG" (6 words).
   - `page.summary`: adds "only" ("from production, storage and LNG terminals only").
   - `page.chart_view.title`: "Production, storage and LNG entry, 13 to 21 September 2026".
   - `page.chart_view.caption` (40 words): "Silver `entsog/aggregated_physical_flows`, kWh/d as sent and provisional, gas days 13 to 21 September 2026: National Gas Transmission's entry from three source types only. Entry from other transmission systems and every exit are not requested, so this is not total entry."
   - `page.what_it_is`: "ENTSOG's aggregate physical flow by zone, direction and adjacent system. Of five British-zone aggregates gridflow requests, the responses fetched contained only National Gas Transmission's entry from production, storage and LNG terminals. Entry from other transmission systems and all exits are not requested: this is not total entry. Values stay in kWh/d; the notebook matches each to its points in `physical_flows`."
   - No local numbers are on the page. The St. Fergus and Easington evidence is only in the vault body's Known issues, as an observation on 2026-08/09 `physical_flows`, with no figures.
2. **Major 2: unscoped vendor behaviour.**
   - `what_it_is` now reads "the responses fetched contained only …".
   - `raw_feed.note` now reads "in the responses fetched, the Northern Ireland pair returned no record". It asserts no cause and uses the plainer "Northern Ireland pair".
3. **Major 3: wrong counts.**
   - Canonical note "Zero storage entry": "7 of 14" becomes "6 of 14 gas days in 2026-08/09 (1 and 3 August, 15 and 18 to 20 September)". Reproduced: silver Storage `value == 0` on 2026-08-01, 08-03, 09-15, 09-18, 09-19 and 09-20.
   - In my round-1 report, "All 16 named points" becomes "All 13 named points (Production 4, Storage 7, LNG 2)", and the storage-zero count becomes 6 of 14. The count does not appear on the page or elsewhere in the note.
4. **Nit 4: Teesside is explained.** Bronze `physical_flows` for 2026-09-21 gives these exact `pointType` strings (the review quoted them without the suffix):
   - `LNG-00007` Teesside: "Aggregated production point - TP ExtEU" (`idPointType` 27);
   - `LNG-00053` Avonmouth LNG: "Storage point ExtEU" (29).

   The note's Teesside bullet now cites the `pointType` and says the `LNG-` prefix is only the key's prefix. The `countPointPresents` bullet adds Avonmouth's `pointType`, "consistent with its place under `Storage`". The Teesside defect is withdrawn in my round-1 report.
5. **Nit 5: the "Not requested" bullet** now lists the 12 exactly, all National Gas TSO:
   - entry from `Transmission`, Ireland, Ireland and Northern Ireland combined, the Netherlands and IUK (5);
   - exit to `Distribution`, `Final Consumers`, `Storage`, Ireland, Ireland and Northern Ireland combined, the Netherlands and IUK (7).

   It adds that St. Fergus and Easington (vendor `pointType` cross-border transmission import points) carry National Gas TSO entry outside the three requested aggregates in 2026-08/09 `physical_flows`.
6. **Nit 6: the live `entsog/physical_flows` related note** is not my file, so I left it unedited. **Seat:** reword `page.related` in `30-vendors/entsog/datasets/physical_flows.md` from "Physical flow summed by balancing zone rather than by point" to, for example, "Physical flow summed by adjacent system for the British zone" (9 words). The same wording appears in `nominations.md` `page.related` and should be changed too.
7. **Nit 7: `notebook.needs`** now reads "gas days 13 to 21 September 2026, aggregates and `physical_flows`", so the reader knows the point table must be ingested too. The command list stays at the aggregate's two commands; adding the point table's two would exceed the 3-command cap.
8. **Nit 8: guide lines that restated the frame** now each say what the frame does not show:
   - `indicator`: "The indicator the connector requests, echoed back by the vendor";
   - `data_set_label`: "Vendor label for the `dataSet` code, as sent";
   - `direction_key`: "Flow direction relative to the zone, lowercase as sent";
   - `adjacent_systems_key`: "Vendor `adjacentSystemsKey`, the category the aggregate groups its points by". Each row's `points_names` lists the points of that adjacent system.
9. **Nit 9: provisional values.** The caption now says "kWh/d as sent and provisional". Every row is `Provisionnal`, which the frame and guide show.

## Evidence for round-2 claims

| Claim | Evidence |
|---|---|
| Storage 0 on 6 of 14 days | Silver: `adjacent_systems_key == "Storage"` and `value == 0` gives dates 2026-08-01, 08-03, 09-15, 09-18, 09-19, 09-20 |
| `pointType` of Teesside and Avonmouth LNG | Bronze `physical_flows/2026/09/21`, `operatorKey` UK-TSO-0001: `LNG-00007` "Aggregated production point - TP ExtEU"; `LNG-00053` "Storage point ExtEU" |
| "Entry from other transmission systems and every exit are not requested" | `endpoints.py:48-54` (five filters); `aggregate_interconnections` silver: 17 British-zone aggregates, 12 not requested (listed above) |
| "in the responses fetched … returned no record" | 14 bronze bodies, 3 records each, none from `IE-TSO-0001`; `meta.count` 3, `meta.total` 6 |
| "provisional" (caption) | Silver `flow_status` `Provisionnal` on 42/42 rows |

## Not changed

- Chart spec, series, sample and notebook. The sample still needs regenerating once `gridflow-sample` handles `|` (round-1 template problem 1).
- `how_used`, `facts` and the key notes. The storage key note already says "Storage exit is not requested", and the caption now states the wider loss.

## Defects (round 2 delta)

- **Withdrawn:** "Teesside listed under `Production`". Vendor `pointType` "Aggregated production point - TP ExtEU" explains it.
- **Corrected:** the storage-zero count is 6 of 14 gas days, not 7.
- **Amended, connector scope:** the 12 unrequested British-zone aggregates are entry `Transmission`, IE, IE+NI, NL and IUK, and exit `Distribution`, `Final Consumers`, `Storage`, IE, IE+NI, NL and IUK. In 2026-08/09 `physical_flows`, St. Fergus and Easington (the largest National Gas TSO entry points) sit outside the three requested aggregates, so no total-entry, zone-balance or net-storage figure can be built from this table.
- **Unchanged:** the `gridflow-sample` `|` failure, `countPointPresents` 6 against 7 names (Avonmouth LNG, `pointType` "Storage point ExtEU", null at point level), shared `lastUpdateDateTime` across gas days, and `Provisionnal` spelling.

Summary: all 3 majors and 6 nits addressed (nit 6 handed to the seat); the page now says plainly that it covers only production, storage and LNG entry and is not total entry; build passes, detector shows only the accepted advisory, mirror byte-equal.
