# entsoe/cross_border_flows: checker review

Checker: Opus 5.5 · high, 2026-09-29. Inputs: the canonical note in `vault-p26-entsoe` (diffed against `origin/master`), the artefacts and the built page in `p26-entsoe`, the writer's report, gridflow code, and local silver (read only).

## Verdict: REVISE

There is 1 blocker, 4 majors and 3 nits. The writer's hard findings stand: the direction, one direction per border, and the chart values. The fixes are small field edits and one re-distil.

## Findings

1. **blocker: `page.record.fields.timestamp_utc`**
   - **What is wrong.** The field reads "period start plus position times resolution". Positions are 1-based, so that formula gives the interval end: every row would sit one step late.
   - **Evidence.** The code is `timestamp = start_dt + (position - 1) * resolution` (`gridflow/connectors/entsoe/parsers.py:530`, and `:582` for the A03 forward-fill). The writer's own evidence table has the right form. The seat's note says other pages repeat this wording.
   - **Fix.** Something like "Interval start, UTC: period start plus (position minus one) resolutions".

2. **major: `page.raw_feed.requests[0]` and `page.raw_feed.note`**
   - **What is wrong.** The request shows the EIC dashes as `%2D`. gridflow sends literal dashes, so this is not the URL the connector builds. The `%2D` form was a workaround for the old guard, which checked parsed values. The guard now checks only the raw front-matter text (commit `e33083c`; `page_fields.py:592`; `tests/test_front_matter_fence.py::test_an_escaped_code_in_a_string_value_passes`), so the workaround is no longer needed.
   - **Evidence.**
     - The bronze sidecar `2026/09/16/raw_20260921T100929Z_a853457e.meta.json` records `request_url` as `...&in_Domain=10YGB----------A&out_Domain=10YFR-RTE------C&...`.
     - At 390 px, the `%2D` strings wrap into blank gaps in the middle of the `in_Domain` and `out_Domain` parameters (screenshot `scratchpad/cbf-review/q-390-open-c2.png`).
   - **Fix.**
     - Write the URL with plain codes, escaping each dash as `\x2D` inside the double-quoted string.
     - Drop "EIC dashes shown as `%2D`" from `raw_feed.note`. It describes the page's own workaround.

3. **major: `page.chart_view.caption` (and the same phrase in `chart_view.alt`)**
   - **What is wrong.** The caption says the chart shows "the hourly mean of each series with `in_area_code` GB". The spec also filters `out_area_code != 10Y1001A1001A59C`, so the GB to IE-SEM series, a fourth GB series, is not drawn. The caption does not state the filter the spec applies (rubric section 2).
   - **Evidence.**
     - `page.chart.filter[2]`.
     - Silver holds four `in_area_code` GB pairs in the window: FR 168, BE 672, NL 672 and IE-SEM 151 rows.
     - The committed series has 3 series and `rows_used` 1,512 (168 + 672 + 672).
   - **Fix.** Name the three borders in the caption ("series from France, Belgium and the Netherlands with `in_area_code` GB"). Give no reason for leaving IE-SEM out: its missing hours are a local-data fact. The alt goes on to list the three series, so there a light touch is enough.

4. **major: `page.related[2].note` (`entsoe/day_ahead_prices`)**
   - **What is wrong.** The note reads "Prices in the zones at each end of these borders". This is false for the GB end, which is the subject of the chart. ENTSO-E sends no GB day-ahead price, so four of the eight borders have no price at one end.
   - **Evidence.**
     - The `day_ahead_prices` canonical note, lines 177-179 and 275-278: GB returns Acknowledgement 999 after Brexit, and the transformer produces zero GB rows.
     - Local silver `day_ahead_prices` has no `10YGB----------A` rows. Its `area_code` values are 59C, 82H, BE, FR and NL.
   - **Fix.** For example "Prices at the continental and Irish ends; none for GB".

5. **major: `page.facts.cadence`**
   - **What is wrong.** "Hourly or quarter-hourly points, as each border is sent" is a general rule measured on our copy. No vendor quote backs it. The seat asked checkers to flag cadence stated this way.
   - **Evidence.**
     - The only evidence is the responses we hold.
     - It is not even stable per border: silver `NL`→`BE` switches from `PT60M` (2026-08-01 to 08-03, 70 rows) to `PT15M` (from 2026-08-03). I checked this with Polars: `group_by(in_area_code, out_area_code, resolution)`.
     - The note's gotcha "PT15M post-2024" has no vendor quote.
   - **Fix.**
     - Scope the field to the rows shown, for example "Per series, as `resolution` states; `PT60M` or `PT15M` in these rows".
     - Scope the note body's Overview edit ("Hourly or quarter-hourly (`PT60M` / `PT15M`)") the same way.
   - **Already scoped.** The caption ("sent quarter-hourly here"), the key notes ("Hourly as sent") and `record.fields.resolution` ("for example") are scoped and need no change.

6. **nit: `page.chart.filter` and its YAML comment**
   - **What is wrong.** The GB string range (`ge "10YGB"`, `lt "10YGC"`) is correct: it selects exactly `10YGB----------A`, the only GB value in silver. But `{column: in_area_code, op: eq, value: "10YGB\x2D…\x2DA"}` reads more plainly. The comment "which front matter bans, so GB is picked by a string range" is now false for values.
   - **Fix.** Switch to `eq` and delete the comment. This changes `spec_sha256`, so re-distil. The output is identical.
   - **Optional.** The key `codes` (`out_Domain FR` and the others) could now carry the real EICs.
   - **Not a finding.** The notebook's `.str.startswith("10YGB")` and `.str[3:5]` are fine. A Python string would need `\x2D` too, which reads worse.

7. **nit: note body, the direction wording in the Overview and cross-zonal table**
   - **What is wrong.** The Overview labels Elexon's positive part as "(import to GB)". That sign is itself a project check (the fuelhh page: checked against demand; Elexon does not state it).
   - **IE-SEM.** IE-SEM is marked "checked" on the same footing as FR, BE and NL, but its evidence is weaker.
     - My hourly check against the positive part of `INTEW` + `INTIRL` + `INTGRNL` gives a correlation of 0.789. The writer's 0.94 does not reproduce at hourly grain. FR, BE and NL are all at or above 0.9998.
     - The direction still holds. In the 141 hours where the Elexon net is below -100 MW (GB exporting), the ENTSO-E series is at most 70.1 MW.
   - **Also in the body.** The modelling line "Net interconnector flow = GB→X − X→GB; consume both directions" is still there. gridflow cannot serve it, because it requests one direction per border. The writer flagged it, but a one-clause qualifier belongs in the body.

8. **nit: `page.chart_view.key[0].note` (France)**
   - **What is wrong.** "the positive part of Elexon's INTFR, INTIFA2 and INTELEC, summed" can be read as the positive part of the sum. The check that holds is the sum of each cable's positive part.
   - **Evidence.** Half-hourly correlation is 0.9999 against the sum of per-cable positive parts (median |d| 9.7 MW), and 0.9945 against the positive part of the net sum (median |d| 67 MW).
   - **Fix.** "the positive parts of … summed".

## What I verified and found correct

- **Direction.** Rows with `in_area_code` GB are the receiving side, reproduced against `silver/elexon/fuelhh` (latest `published_at` per key, 14 to 20 September).
  - BE against the positive part of `INTNEM`: correlation 1.000.
  - NL against the positive part of `INTNED`: 0.9998.
  - FR against the per-cable positive sum: 0.9999.
  - Against the net value, FR drops to 0.952.
  - BE is at most 9.97 MW in the 229 half-hours where `INTNEM` < 0 (key note 2 holds).
  - The parser takes `in_Domain.mRID` and `out_Domain.mRID` from the TimeSeries (`parsers.py:290-299`), and the bronze XML carries in=GB, out=FR for the GB-FR request.
  - The page attributes the direction as a project check in `what_it_is` and `record.fields.in_area_code`, and never as an ENTSO-E rule.
- **One direction per border.**
  - `_FLOW_PAIRS` (`client.py:40-49`) has eight ordered pairs. Silver holds exactly those 8 combinations, none the reverse of another, with 0 duplicate keys.
  - The summary, `what_it_is` ("no border can be netted from this table"), the caption and the frame caption all say so, and nothing on the page implies netting.
- **Chart.**
  - The spec has `spec_origin: vault`, the build digest passes and there is no staged spec. The title and caption say "hourly mean", matching `aggregation: mean` and `time_bucket: 1h`.
  - My own Polars aggregation matches every number in the alt:
    - FR daily maxima of 3,054 to 3,059 MW, except 944.6 on the 19th; FR daily minima 12.0, 3.4, 2.0, 12.4, 0.8, 0.8, 0.8;
    - BE 0 to 1,042.3 MW, with a maximum of 63.4 on the 17th;
    - NL at most 0.1 MW to the 18th, 373.5 on the 19th and 1,016.7 on the 20th.
  - `plot_alt` matches the notebook PNG.
- **Raw feed and commands.** Host, path and parameter order match the bronze sidecar, and there is one GET per pair per UTC day (`day_subwindows`). Ingest `--end 2026-09-21` is excluded (`utils/time.py` `day_subwindows`, a bare date is midnight UTC). The transform end is inclusive. There are no `PARTITION_SOURCE_OFFSETS` overrides.
- **Frame.** The eight rows are real (`generated_by: gridflow-sample`), one per ordered pair at 21:00 UTC on 16 September.
  - `published_at` is 1 s before each fetch-time file name, for example `10:09:28` against `raw_20260921T100929Z`, which fits ruling #39.
  - The guide has a line per non-pipeline column, key columns first.
  - `flow_mw` (`MAW`, A03 forward-fill) and `resolution` are correct against the bronze XML and the probe (one `<Point>`, `PT15M`, `A03`).
- **Notebook.** Every cell is read-only and the outputs have no errors. The lead matches `source.py` `query()`: `timestamp_utc`, inclusive-end predicate, lineage excluded, `ORDER BY` the date column. `needs` matches the commands' window.
- **Local data and leakage.** None: grep of the page finds no `locally`, `held`, `since 20`, em dash, `→` or `·`. The one "our " hit is "half-hour" in the fuelhh related card.
- **Budgets and gates.** `gridflow-build --only entsoe/cross_border_flows` is OK. `detect.mjs` returns only the accepted `em-dash-overuse` advisory (EIC padding).
- **Screenshots.**
  - Taken at 1440, 1024, 768 and 390, with 390 as a true 390 CDP viewport and also in an iframe. The frame was captured both folded and unfolded, and the notebook opened. Nothing is clipped or overlapping, and `scrollWidth` equals `innerWidth` at every width.
  - The CSS has no dark theme, so light and dark are identical. The notebook tab clip at 390 is the seat's template item.
  - The files are in `scratchpad/cbf-review/`. I used port 9817 and stopped the server.
- **Body corrections.** The seven body corrections each cite a `file:line` that I confirmed:
  - the Overview, `client.py:40-49`;
  - the bronze path, `bronze/writer.py:33-34,56`;
  - the `published_at` row, `cross_border_flows.py:84` and `schemas/entsoe.py:88`;
  - the A03 fill, `parsers.py:533-600`, plus the one-point probe;
  - the implementation delta;
  - the quality filter, `cross_border_flows.py:37,73`.
  The curl example is unchanged.
- **Mirror.** `vault/entsoe/cross_border_flows.md` is LF while the canonical note is CRLF, so the writer's "cmp clean" no longer holds byte for byte. The content is identical once CRs are ignored, and the committed mirror on `main` is LF. This is not a finding.
