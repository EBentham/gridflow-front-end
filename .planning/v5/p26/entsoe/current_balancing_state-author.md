# current_balancing_state: author report

Writer, 2026-09-29. Dataset `entsoe/current_balancing_state` (A86 / B33, GL EB 12.3.A). Group 3, port 9821.

## Verdict: HOLD. Silver cannot build a truthful page

I wrote no `page:` block and produced no artefacts. Three gridflow defects compound, and any one of them is a
rubric §1/§2 blocker. Silver has no zone, no sign and wrong times for every point after the first in each
period. A chart, eight rows or a notebook built from it would show bug output under a factual caption. The
page stays blank (hero name and id). I made body corrections to the canonical note and mirrored them.

- Build: `gridflow-build --only entsoe/current_balancing_state` succeeded, printing `wrote: ... (blank)`.
- Detector: `[]`.
- Screenshots of the blank page at 1440, 1024, 768 and 390 (390 through an iframe): nothing clipped.
  They are in `scratchpad/cbs/shots/`.
- The server on 9821 is stopped.

## The three gridflow defects (for the seat; a gridflow fix and a re-transform are needed)

| # | Defect | Evidence |
|---|---|---|
| 1 | **`PT1M` is not mapped, so point times are spread over hours.** `_RESOLUTION_MAP` has no `PT1M`, and `_resolve_resolution` falls back to `timedelta(hours=1)`. Each point therefore lands at start + (position - 1) **hours**, not minutes. The A03 forward-fill is also skipped for an unmapped code. | `connectors/entsoe/parsers.py:35-43`, `:50-51`, `:530`, `:547-555`. Bronze holds 1 to 5 Aug only, yet silver `timestamp_utc` runs to 2026-08-25 08:15 UTC: FR's 5 Aug document, stretched sixty times. Silver's maximum equals the maximum from my bronze re-parse with gridflow's own parser, and the dedup simulation below reproduces silver's 9,414 rows exactly. |
| 2 | **Zone lost.** Real A86 responses carry `area_Domain.mRID` at document level. The parser reads it only from TimeSeries children, so `area_code` is `""` on every row. | `parsers.py:302`. Every bronze document header has it (for example `<area_Domain.mRID codingScheme="A01">10YFR-RTE------C</area_Domain.mRID>` directly under the root), as does ENTSO-E's own XML example. Polars: `df["area_code"].unique()` gives `['']` over 9,414 rows. |
| 3 | **Sign lost.** `flow_direction` is parsed but is not in `output_cols`, so silver holds magnitudes only. | `silver/entsoe/h8_balancing.py:36-45`. `(quantity_mw < 0).sum()` is 0; the minimum is 0.018 and the maximum 2361.76. |

**How they compound.** The dedup on `(timestamp_utc, area_code, business_type)` with `keep="last"`
(`h8_balancing.py:46`, `:104`) merges FR, NL, BE and both directions into one row per timestamp. I
re-parsed bronze with gridflow's own `parse_timeseries_xml` (read only) and got 14,880 points. Simulating
the per-day dedup gives **9,414 rows, exactly silver's count**. The survivors mix zones and directions: BE
A01 3,267, BE A02 2,856, NL A01 1,478, NL A02 1,489, FR A01 128, FR A02 196.

**Related stale code note.** `silver/entsoe/_event_window.py:889-908` classifies this dataset as "Never
observed populated". The bronze for 1 to 5 Aug 2026 has populated FR, NL and BE documents, so that
evidence string is out of date (a seat item for gridflow).

**Suggested fix, for gridflow, not done here.**
- Add `"PT1M": timedelta(minutes=1)` to `_RESOLUTION_MAP`.
- Fall back to the document-level `area_Domain.mRID` when the TimeSeries has none.
- Keep `flow_direction` (as `direction`) in `CurrentBalancingStateTransformer.output_cols` and add it to
  `unique_subset`, or sign the value once the Up/Down meaning is sourced (see open questions).
- Then re-transform 1 to 5 Aug.
- Reconsider the fallback: a silent one-hour default for any unknown resolution code is the root hazard.

## Answers to the three watch items

- **Coverage (1 to 25 Aug in the data matrix).** This is not coverage. Bronze holds only 1 to 5 Aug 2026:
  60 files (30 XML, 30 meta), six zones per UTC day, all fetched on 2026-08-16 between 14:10 and 14:12 UTC. The five daily
  silver files are dated 1 to 5 Aug. The timestamps after 5 Aug are an artefact of defect 1. The matrix's
  "last" date of 2026-08-25 should be read as a parser bug, not as a date the vendor published.
- **Sign and unit, from vendor docs.**
  - The TP knowledge base article "Current Balancing State [GL EB 12.3.A]" (Zendesk article
    12824861339924, updated 2025-08-26, read through its JSON API) defines the value:
    - It is the total imbalance volume ("open loop area control error"), averaged over each minute.
    - The unit is MW.
    - The state is "Excess, Deficit or Balanced": "deficit is equivalent to negative imbalance while
      excess is equivalent to positive imbalance" (GL EB 54.6).
    - Publication is due 30 minutes after the end of the minute, and updates are "Not foreseen".
  - ENTSO-E's XML example (gitlab.entsoe.eu transparency/xml-examples) labels `B33` "Area control error"
    and gives the direction codes `A01: Up, A02: Down, A03: Symmetric`, with unit `MAW`, `PT1M` and curve
    `A03`.
  - **Neither source maps Up/Down to excess/deficit.** The wire value is unsigned, with a direction code.
  - **Checked against the rows:** silver can't be checked because the direction is dropped. Bronze confirms
    every quantity is positive, with the direction in a separate code; no zone-minute is negative.
  - The old note's "positive = system short" is unsupported and contradicts the vendor's own wording
    (excess = positive).
- **Zones.** Silver holds **no identifiable zone** (`area_code` is empty). Bronze has data for **FR**
  (`10YFR-RTE------C`), **NL** (`10YNL----------L`) and **BE** (`10YBE----------2`). **GB**, **DE-LU**
  and **IE-SEM** got code-999 "No matching data found for Data item CURRENT_BALANCING_STATE_R3" on all five
  days.
  - Point density in bronze: BE and NL declare a point for every minute of the day, split between the Up
    and Down series. FR declares 96 points a day on A03 variable blocks.

## Evidence table (claims now in the note body)

| Claim | Evidence |
|---|---|
| The request is `GET https://web-api.tp.entsoe.eu/api?documentType=A86&periodStart=YYYYMMDD0000&periodEnd=<next day>0000&area_Domain=<EIC>&businessType=B33&securityToken=...` | `client.py:291-311` (parameter order); `endpoints.py:328-334`; bronze `.meta.json` `request_url` (for example `...documentType=A86&periodStart=202608010000&periodEnd=202608020000&area_Domain=10YFR-RTE------C&businessType=B33...`) |
| One call per zone and UTC day, over six zones | `client.py:161-167` (`day_subwindows`), `:249` (the `DEFAULT_ZONES` loop, since the doc type has no `domain_style`, so the "zone" default applies with `domain_params`); `endpoints.py:395` |
| Point time = start + (position - 1) × resolution | `parsers.py:530` |
| `PT1M` is unmapped and falls back to 1 h | `parsers.py:35-43`, `:50-51` |
| `area_Domain.mRID` is read only inside the TimeSeries | `parsers.py:302`; bronze document heads |
| Direction is dropped | `h8_balancing.py:36-45` |
| `published_at` = root `createdDateTime`, a fetch-time stamp | Every silver row falls between 2026-08-16 14:10:54 and 14:11:55 UTC, matching the `.meta.json` `fetched_at` values; ruling #39 |
| Definition, unit, excess/deficit, deadline, no updates | TP knowledge base article 12824861339924 |
| `B33` = Area control error; `A01` Up / `A02` Down / `A03` Symmetric; `MAW`; `PT1M`; A03 | ENTSO-E GitLab XML example |
| GB, DE-LU and IE-SEM return code 999; FR, NL and BE publish | Bronze 1 to 5 Aug 2026 (15 acknowledgements, 15 documents) |
| The TimeSeries `mRID` is a sequence number | Bronze (`<mRID>1</mRID>`, `2`, ...) and the vendor example |

## Body corrections made (canonical `30-vendors/entsoe/datasets/current_balancing_state.md`, mirrored byte for byte, CRLF kept)

1. **Overview.** Replaced the "positive = system short ... minute / quarter-hour" paragraph with the vendor
   definition and a paragraph on unsigned quantity plus direction code, marked as a correction.
2. **Overview.** The `B33` gloss "regulating reserve / balancing state" became "Area control error" (vendor
   code list, per the example XML).
3. **API table.** Publication lag: from "near real-time ... minute-to-quarter-hour" to the vendor deadline of
   30 minutes after the minute.
4. **Query parameters.** The `periodEnd` description changed from "Plan recommends ≤ 14h" to "exclusive;
   gridflow sends one whole UTC day" (with `client.py` lines). I left the curl example alone: a 14-hour
   window is valid for the vendor.
5. **Bronze granularity.** Changed to one file per zone and UTC day, over six zones including the code-999
   acknowledgements.
6. **Bronze sample.** Added a caveat that the fixture is hand-made and that real responses differ (document-
   level area, direction, `MAW`, A03, `PT1M`, unsigned). The fixture itself is unchanged.
7. **Point-in-time field.** From "none" to `published_at` as a fetch-time stamp.
8. **Silver schema.**
   - `timestamp_utc`: the formula changed to `(position - 1)`, and I noted the `PT1M` fallback defect.
   - `area_code`: noted that it is empty because of the parse location.
   - `quantity_mw`: from "positive = system short" to "unsigned magnitude; direction dropped".
   - `resolution`: `PT1M` as held.
   - Added the missing `published_at` row.
9. **Known issues.**
   - The GB bullet now adds that DE-LU and IE-SEM also return code 999, while FR, NL and BE publish.
   - The "Intra-day window required" bullet is corrected: whole-day calls return full days.
   - The "No DocStatus / mRID on TimeSeries" bullet is corrected: a sequence `mRID` exists.
   - The "Sign convention is TSO-local" bullet is replaced with the vendor wording and a warning not to
     borrow `imbalance_volume`'s long/short mapping.
   - **Added** a bullet naming the three gridflow defects and the 14,880 → 9,414 collapse.
10. **Modelling notes.** "(e.g. DE-LU, FR)" became "FR, NL, BE; DE-LU returned 999".
11. **Links.** Added the two vendor sources.

The front matter is untouched: no `page:` block and no `---` inside it. `last_verified` is left at
2026-05-08 for the seat to decide.

## Could not verify

- **Up/Down to excess/deficit.** No vendor text held here states the mapping. ENTSO-E's old static
  data-view page returns `URI_FORMAT_ERROR`, and newtransparency.entsoe.eu is JavaScript-only. The general
  ACE convention (positive ACE = over-generation) is not ENTSO-E's statement for this data item, so I did
  not use it.
- **History depth.** No vendor evidence was found, so the `TODO` stays.
- **Whether FR's 96 points a day is a TSO choice or A03 compression.** It looks like variable blocks, but
  this is unverified until `PT1M` forward-fill works.

## Open questions for the seat

1. Hold the page (recommended: **yes**) until gridflow fixes the three defects and silver is re-transformed.
   Then a writer can chart FR, NL and BE as minute lines by direction.
2. Should the direction mapping be a research unit (named unknown: does `A01` Up mean deficit, needing
   upward regulation, or excess)? Until it is answered, a fixed page should show direction as a code and
   not sign the value.
3. The data matrix's "last 2026-08-25" for this row, and possibly other `PT1M` datasets, is a parser
   artefact. Any other ENTSO-E dataset sending `PT1M` (or any unmapped code) has the same one-hour
   fallback. Worth a sweep: `grep` silver for `resolution` values outside `_RESOLUTION_MAP`.

## Template problems

None found. The blank page renders cleanly at all four widths.

## Process note

One `sed -i` (fixing a line citation) stripped the note's CRLF endings. I restored them with a uniform
LF→CRLF pass: 216/216 lines are CRLF, and the vault diff is 36+/24−, not a whole-file rewrite. The mirror
is byte-identical to the canonical note (`cmp`).
