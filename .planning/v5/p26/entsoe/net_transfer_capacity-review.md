# entsoe/net_transfer_capacity: checker review

Checker: Opus 5.5 · high, 2026-09-29. Inputs: the canonical note in `vault-p26-entsoe` (diffed against `origin/master`), the three artefacts and the built page in `p26-entsoe`, the writer's report, gridflow code, local bronze and silver (read only).

## Verdict: REVISE

Findings: 1 blocker, 1 major, 4 nits. The page's own facts, chart, rows, notebook and layout pass. The blocker is one related note. The major is the note body's corrected modelling line, which is still wrong for one of the four GB pairs.

## Findings

### 1. Blocker: `page.related[3].note` (entsoe/day_ahead_prices)

- **What is wrong.** "Prices in the zones at each end of these borders" is false for the four GB borders, which are the page's subject. `day_ahead_prices` has no GB price.
- **Evidence.**
  - `day_ahead_prices.md:177`: GB returns "Acknowledgement code 999 ('No matching data found for Data item ENERGY_PRICES [12.1.D]')".
  - Silver check: `pl.read_parquet(".../silver/entsoe/day_ahead_prices/**/*.parquet").group_by("area_code").len()` returns five zones: IE-SEM, DE-LU, BE, FR and NL. There is no `10YGB----------A`.
  - The approved `cross_border_flows` note words the same relation as "Prices at the continental and Irish ends; none for GB".
- **Fix.** Reuse that wording, or similar, within 12 words.

### 2. Major: note body, `## Modelling notes`, first bullet (a body correction under rubric section 7)

- **What is wrong.** The corrected line says:
  - "on the four GB pairs flow reaches at most 1.04 x NTC, bar one GB-BE hour at 1.11";
  - hours "where NTC is 0" occur only on NL-DE-LU;
  - so "`utilisation = flow / ntc` slightly above 1 is normal on the GB pairs".

  GB from NL breaks all three. It has 286 compared hours at NTC 0, and flow into GB is positive in 259 of them. Two of those hours carry real flow: 19 Sep 19:00 UTC at 373.5 MW and 19 Sep 13:00 at 86.5 MW. Utilisation is undefined in those hours, not "slightly above 1". The 19:00 hour falls inside the NTC-0 stretch that the page's own eight rows show. The 1.04 figure holds only for hours where NTC > 0.
- **Evidence.** I reproduced the writer's join: `cross_border_flows` quarter-hours truncated to the hour and averaged, then inner-joined to NTC on (hour, in, out). It gives 2,426 joined hours, 2026-08-01 to 2026-09-20.
  - The writer's figures reproduce:
    - NL from DE-LU: 141 of 432 hours with flow above NTC, max excess 2,559.8 MW;
    - GB-BE: max ratio 1.106 (889.3 against 804, 18 Sep 08:00);
    - GB-NL: max ratio 1.040 where NTC > 0.
  - Per pair, (flow > NTC) and (NTC = 0 with flow > 0):
    - GB-NL: 285 of 432, and 259;
    - GB-FR: 89 of 432, and 0;
    - GB-BE: 50 of 432, and 0.
  - GB-NL at NTC 0, `nl.filter(ntc_mw == 0, flow > 1)`: two rows, 2026-09-19 19:00 (373.5) and 13:00 (86.5).
  - The other 257 positive hours are 0.06 to 0.10 MW. The daily table shows flow about 0.06 MW on every hour from 8 to 18 Sep, while NTC is 0.
- **Fix.** Scope the 1.04 figure to hours with NTC above zero. Say that GB from NL also shows flow at NTC 0 (up to 374 MW on 19 Sep). Drop "normal on the GB pairs", or restrict it to hours with NTC > 0.
- **Not on the page.** The page quotes no count or ratio. Its only related wording, `how_used[1]` ("see how close physical flow runs to capacity"), is fine. This is a note-body finding only.
- **Optional.** The Overview still says "(NTC is the upper bound on commercial flow)". That is about commercial exchange, so it can stand, but it sits oddly beside the corrected bullet.

### 3. Nit: note body, `### Cross-zonal parameters`, direction sentence

- **What is wrong.** "on the four GB pairs, hourly `cross_border_flows` flow into GB (same in/out) tops out at about these NTC values". This fits FR, BE and NL. It does not fit IE-SEM, where flow into GB reaches at most 153.4 MW against NTC of 400 to 1,413. The same join as finding 2 shows this: GB-IE-SEM has 266 joined hours and max flow 153.4.
- **Two smaller points in the same sentence.**
  - "(19 days, 2026-08-01 to 2026-09-21)" reads as one continuous range. The 19 bronze days are 1 to 5 August and 8 to 21 September.
  - The check shows that A61 and A11 share an in/out convention, and that flow saturates at NTC on FR, BE and NL. Because those links are near-symmetric in rating, the check cannot rule out the reverse reading on its own. The page labels it a project check, which is the right disposition.
- **Fix.** "on the GB-FR, GB-BE and GB-NL pairs", and give the day ranges.

### 4. Nit: `page.what_it_is`, second sentence

- **What is wrong.** "FR to BE and FR to DE-LU came back as no matching data". The facts are right, and it is correctly worded as what gridflow received:
  - all 42 of 42 FR-pair responses are `Acknowledgement_MarketDocument` with Reason `999`;
  - the text reads "No matching data found for Data item FORECASTED_TRANSFER_CAPACITIES_EXPLICIT [11.1] ...";
  - they cover each of the 19 bronze days, and both FR pairs on 13 and 14 Sep, which were fetched twice.

  The phrase is awkward and carries no scope, while `facts.cadence` scopes the same kind of observation with "in the responses received".
- **Suggested wording.** "In the responses received, FR to BE and FR to DE-LU returned ENTSO-E's 'No matching data found' acknowledgement."

### 5. Nit: the writer's report (not the page)

- **What is wrong.** "38 of 38 files" should be 42 of 42. Days 13 and 14 Sep have 16 files each, fetched on 15 and 26 Sep.
- **Evidence.** The bronze tally by (in, out, document root) gives 21 ACK files for each FR pair and 21 PUB files for each of the six other pairs, 168 XML files in all. The note and the page carry no count, so nothing else changes.

### 6. Nit: the note body links

- **What is wrong.** `../../../20-domain/markets/net-transfer-capacity.md` does not exist. The writer reported this and left it. It is not on the page. It is a vault item for the seat.

## What passes (evidence)

- **Direction.** It is labelled "(project check)" in `what_it_is` and in `record.fields.in_area_code`. This is the same pattern as the approved `cross_border_flows`, whose own direction is a labelled project check against FUELHH. The chart title "Capacity into GB" follows the approved `cross_border_flows` precedent ("Flows into GB").
- **No matching data.** See finding 4. The page states no count and no dates.
- **Corrected claim.** The page never calls NTC an upper bound. The caption says "Forecast capacity, not flow". No local counts appear on the page. A grep of the rendered text for `locally|held|our |since 20|rows|% of|live|now|→|·|—|–` finds only template strings and "GB rows read as...".
- **"Not what was allocated or nominated".** It matches the family lead `total_capacity_allocated` ("Neither is the forecast capacity in `net_transfer_capacity`"): A26/A29 is allocated in earlier rounds, A26/B08 is nominated.
- **Related pages.**
  - `total_capacity_allocated`: "on these pairs" is true, because it uses `zone_pair` and so `_FLOW_PAIRS`.
  - `dc_link_intraday_transfer_limits`: "same ordered pairs" is true (`endpoints.py:146-150`, `zone_pair`).
- **Chart.**
  - The committed series has 4 × 336 hourly points, 8 Sep 00:00 to 21 Sep 23:00, with `spec_origin: vault`. There is no staged spec or override for the dataset.
  - Checked against silver (filter `in_area_code == GB`, `group_map`, `last`), it has **0 mismatches**.
  - Every step in the alt text and key notes matches the run-length output:
    - FR goes to 3,028 at 09T06;
    - IE-SEM goes to 1,413 at 13T00, is 913 from 14T15 to 20, and is back to 1,413 at 14T23;
    - BE is 1,032 from 08 to 12 most days, 764 and 750 on the 8th, 834 and 804 on the 18th, and 0 from 21T05;
    - NL goes to 1,016 at 19T22.
  - The four NL pairs, NL-DE (max 2,774) and NL-BE (4,498), are excluded as the caption says.
- **Point time and cadence.**
  - The wording is "period start plus (position minus one) times resolution" (`parsers.py:530`, and `:582` for the A03 fill).
  - Bronze confirms it. `2026/09/19/raw_20260926T175730Z_e019b71c.xml` (GB from NL, A03, `PT60M`) has positions 1 (0) and 23 (1,016), and silver shows 1,016 from 22:00.
  - Cadence is scoped to "in the responses received". Every silver row is `PT60M`.
- **Grain and key.** `net_transfer_capacity.py:78` `unique(subset=[timestamp_utc, in_area_code, out_area_code], keep="last")`, over files read in name order (`:42`). There are 0 duplicate keys, and 456 rows per pair across 19 days.
- **`published_at`.** It is worded as a fetch-time stamp (ruling #39). The eight rows show 17:57:30 and then 17:58:02 on 26 Sep, across the day boundary.
- **Raw feed.** The request URL matches the bronze sidecar `request_url` exactly: parameter order, formats and host. The commands match the approved sister pattern, `day_subwindows` (`utils/time.py:123-141`) and the chart window.
- **Artefacts.**
  - The samples are `generated_by: gridflow-sample`, 8 real rows.
  - The notebook is `scripts/run_notebooks.py`. Its cells are read-only and it has no error outputs.
  - The cell 4 summary matches silver: min, max and count 336 for six pairs.
  - The plot image matches `plot_alt`. I checked it scrolled into view at 1440 and 390.
- **Build and detector.**
  - `gridflow-build --only entsoe/net_transfer_capacity` passes: "wrote: data-sources/entsoe/net_transfer_capacity.html".
  - `detect.mjs --json` returns only `em-dash-overuse`, which is advisory ("142 em-dashes", the EIC padding and `--` flags), accepted under ruling #39.
  - The mirror `vault/entsoe/net_transfer_capacity.md` is byte-identical to the canonical note (`cmp`).
- **Layout (section 5).**
  - I used my own CDP shots: a static server on 9823, since stopped, with Chrome under `timeout 60`.
  - At 1440, 1024 and 768, folded and unfolded, `scrollWidth` equals `innerWidth` and no element sits outside the viewport.
  - At 390 I used a real 390 px same-origin iframe, where `scrollWidth` is 390.
  - I looked at the hero turbines, the chart with its key and notes, the frame and guide, the stratum corner labels, the notebook and the related list. Nothing is clipped or overlapping.

## Non-findings and template notes for the seat

- **Blank notebook plot in full-page captures.** The image is `loading="lazy"`. Once scrolled into view it has `complete: true` and `naturalWidth` 707, and it renders. Its absence from the full-page shots is a capture artefact.
- **Dark theme.** `tokens.css` and `theme.css` have no `prefers-color-scheme` or `data-theme` rule, so a dark check does not apply.
- **Notebook summary table at 390 (template).** It sits in `.df-wrap` with `overflow-x: auto` (clientWidth 300, scrollWidth 487), so `min`, `max` and `count` need a horizontal scroll. Unlike the Polars frame's `.fw`, that wrapper has no `tabindex` or `role`, so keyboard users cannot reach the scroll. This is template work.
- **Known template items.** Both were reported by the writer and left alone:
  - the `contract_MarketAgreement.Type=A01` wrap at 390;
  - the notebook tab label clip (ruling #39).
- **Scratch files.** The checker wrote `ntc_check*.py`, `ntc_chart.py`, `ntc_text.txt`, `ntcrev_*.mjs` and `ntcrev-shots/`, all in the scratchpad. The Chrome profiles `%TEMP%\cdp-ntcrev-*` are left in place.
