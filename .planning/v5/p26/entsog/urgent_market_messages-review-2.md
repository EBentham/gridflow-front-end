# entsog/urgent_market_messages: review 2

Checker: Sonnet 5.5 · high, 2026-10-07. Focused re-check of the writer's round 2
(`urgent_market_messages-author-2.md`). Inspection only; no file written except this one.

## Verdict: APPROVE

0 blockers, 0 majors, 2 new nits. All three majors and all seven round-1 nits are resolved.

## Round-1 majors

1. **Snapshot statement: resolved.** `what_it_is` now says "Silver holds only the newest fetch: a message
   ENTSOG stops sending leaves silver at the next transform, so silver is not a history; bronze keeps each
   fetch." True against code and disk: `reference=True` (`endpoints.py:199-206`), `NEWEST_VOUCHED` and one
   overwritten file (`generic.py:106-116,128-129,252-259,284`), one parquet file in silver, one raw file
   per fetch in bronze. "Still serves" and the unscoped "some threads without their latest" are gone from
   `summary` and `what_it_is`; the observation is now fetch-scoped in `is_latest_version` ("some threads in
   this fetch, Kiemenai here, lack `Yes`", true: six threads). `how_used[1]` now reads "Matching current
   messages to flows through connection point EICs; some do not resolve" (true: 6 of 17 distinct
   `affected_asset_eic` values are absent from `connection_points.point_eic_code`). `raw_feed.note`,
   `notebook.lead` ("the newest fetch only") and `timestamp_utc` ("not when gridflow fetched it") agree.
2. **Capacity values: resolved.** `unavailable_capacity` names the placeholders 10000000000 and 1
   (reproduced: four versions at 1e10 kWh/d with 0 available; two at 1 kWh/d against 9.97e8 available).
   `available_capacity` says some versions send all three as 0 (reproduced: ten NaTran Deutschland
   `26082121X...` versions). `technical_capacity` says one version reads a thousandth of its successor
   (reproduced: RC Basel `25090321X000000001163D001`, technical 265.77 then 265,778 kWh/h). The mixed-unit
   warning on `unit_measure` remains. See nit A.
3. **Update-stamp line: resolved.** "Update stamp as sent; five rows here, about a quarter overall, share one
   value": no cause asserted, "not an edit" gone. Five of the eight shown rows and 35 of 133 (26 percent)
   share `2026-09-27 00:28:56 UTC`. See nit B.

## Round-1 nits

4. Plot wording: fixed. `plot_alt` says "15 capacity messages flagged Active at the highest version sent" and
   names VIP Oberkappel as "a thread sent without its latest version" (true: `V0021586/1`, version 001 flagged
   `No`); the cell carries the comment and no `Yes` filter. The 15 bars and their start dates still match
   silver.
5. `how_used[0]`: "at a point or facility". Fixed.
6. Flows join: `how_used[1]` and the `physical_flows` related note (11 words) name the connection-point EIC
   route. Fixed.
7. Notebook window: `query("urgent_market_messages", "2000-01-01", date.today())`. Fixed; the notebook re-ran
   (`generated_by: scripts/run_notebooks.py`, 6 cells, no error outputs), event types 48 / 47 / 5 / 1 unchanged,
   same plot image.
8. Manual citation: body gotcha "No field definitions" added and accurate (manual v2.1 text lists the path only).
   Fixed.
9. Body numbers: "2 min 27 s", "two about 65 days later", RC Basel columns named, ten all-zero versions added,
   gotcha heading and text no longer assert a cause. Fixed.
10. `message_id`: "One per version: ...". Fixed.

## Regression checks

- `gridflow-build --only entsog/urgent_market_messages` succeeds (digest checks pass, so series, sample and
  notebook artefacts match the note).
- `detect.mjs --json` returns only the accepted advisory `em-dash-overuse` ("49 em-dashes", codes and CLI flags).
- `cmp` canonical note against `vault/entsog/urgent_market_messages.md`: byte-equal.
- Chart, series and sample untouched; the chart still recomputes to 31, 21, 17, 12, 5, 4, 4, 4, 3 (101 messages).
- Rendered with headless Chrome (`timeout 60`) at 1440 and a true 390 px iframe: the new `what_it_is`, `how_used`,
  and the longer guide lines wrap cleanly; nothing clipped or overlapping. My server on 9899 is stopped; 9670
  untouched.

## New nits (not blocking)

- **A. `page.record.fields.unavailable_capacity`:** "this fetch includes placeholders 10000000000 and 1" states as
  fact what is an inference (the vault body says "apparent placeholders"; the writer's own report says "look like
  it"). 10000000000 with 0 available is near-certain; `1` is a judgement. "values that look like placeholders,
  such as 10000000000 and 1" is safer.
- **B. `page.record.fields.last_update_date_time`:** "about a quarter overall" is unscoped; say "in this fetch" so
  it is not read as a share of ENTSOG's data.

Summary: APPROVE, the three majors and seven nits are fixed and nothing regressed; two optional wording nits remain.
