# entsoe/wind_solar_forecast: review 1

Reviewer: Opus 5.5 · high, checker. Inputs: `BATCH-entsoe.md` (rulings #39, #40), `review-rubric.md`, `author-brief.md`, the author report, the vault note diffed against quant-vault `origin/master` (vault worktree `docs/v5-p26-entsoe`), the committed artefacts, the built page, gridflow code, local silver and bronze (read only).

## Verdict: REVISE

1 major, 3 nits. The page itself is correct: every fact, number, request and command on it checks out. The major is in the note body. Two sentences there still carry the scrambled production-type codes the writer set out to fix.

## Findings

1. **major**: note body, `## Known issues and gotchas` (bullet 2) and `### Silver sample`
   - **What is wrong:** two leftovers of the scrambled codes survive next to the corrected schema table, so the note still contradicts itself on the codes.
     - The gotcha reads "A69 only carries B16, B18, B19 — solar separation may merge B17 (solar thermal) historically; we observe only B19 for current periods."
       - "we observe only B19" is false. DE-LU, FR, NL and BE each send B16, B18 and B19. This is the load-bearing part of the finding.
       - The B17 label is also doubtful. The ENTSO-E PSR type list (the API guide's appendix, which the note links) names B17 as waste, and the sibling note `actual_generation.md:74` keys it as waste too. gridflow code has no B17 mapping, so this rests on the vendor list, not on code.
     - The silver sample (May 2026) shows `production_type: B19` at 0.0 at 22:00 and 31,250.4 at 11:00. That is a solar profile under the onshore code.
       - It also shows `"resolution": "0:15:00"`. The parser stores the ISO code string (`parsers.py:459`, `"resolution": resolution_code`), and silver holds `PT15M`/`PT60M`.
   - **Why major, not nit:** the note now contradicts itself on the exact codes the page rests on, and author-brief item 2 asks the writer to fix body facts that research shows are wrong. The author flagged both leftovers openly under "Unverified", so this is not concealment. The seat may downgrade it if it prefers to refresh the body separately.
   - **Fix (smallest spans):**
     - Gotcha: drop the B17 clause. Replace "we observe only B19 for current periods" with a true scoped fact, or delete the bullet.
     - Silver sample: replace it with two real rows (for example the DE-LU B16 and B19 rows at 22:00 on 14 Sep from the sample JSON), or delete it.
   - **Evidence:**
     - Polars over silver 14 to 20 Sep, `group_by(area_code, production_type, resolution)`. DE-LU, BE, FR and NL each have B16, B18 and B19. B16 has min 0.0 in every zone. B19 min is 569.7 for DE-LU.
     - DE-LU mean by UTC hour: B16 is 0 from 18:00 to 03:00 and 35,557 at 10:00. B19 ranges from 12,511 to 17,303.
     - Bronze `2026/09/14/raw_20260921T100800Z_9a638f3e.xml` has three TimeSeries: B16 (businessType A94), and B18 and B19 (A93).

2. **nit**: note body, silver schema table, `published_at` notes
   - **What is wrong:** it says `createdDateTime` "equals the sidecar `fetched_at` to within a second". Measured, the gap reaches about 2 s. Ruling #39 says "within seconds".
   - **Evidence** (`2026/09/14/*.meta.json` against `<createdDateTime>`):
     - NL: created 10:07:57, fetched 10:07:58.849.
     - FR: created 10:07:56, fetched 10:07:58.002.
     - IE-SEM: created 10:08:01, fetched 10:08:02.223.
   - **Fix:** "within seconds of". The page line ("a fetch-time stamp") is correct and needs no change.

3. **nit**: `page.raw_feed.note` (or `record.fields.timestamp_utc`)
   - **What is wrong:** the page does not say that silver fills the vendor's compressed curve. A69 series come as `curveType` A03, where omitted positions repeat the previous value. The parser forward-fills them (`parsers.py:533-600`).
     - For example, the DE-LU response for 14 Sep declares 248 `<position>`s across three series. Silver holds 288 rows (96 x 3).
     - A reader comparing bronze with silver will see missing points.
   - **Why only a nit:** nothing on the page is false. Each row is still one target interval and one point quantity.
   - **Optional fix:** a few words in `raw_feed.note`, for example "fills the vendor's A03 blocks".

4. **nit**: `page.facts.cadence` (and the body gotcha "DE-LU is published at PT15M; some smaller zones publish at PT60M only")
   - **What is wrong:** "each zone sends its own interval, such as PT15M or PT60M" reads as a vendor rule. No quoted vendor source backs it. It is what these responses carry.
     - Silver 14 to 20 Sep: DE-LU, FR and NL are PT15M; BE and IE-SEM are PT60M.
   - **Fix:** scope it, for example "Day-ahead; the interval is the response's `resolution`, PT15M or PT60M in these responses". The body gotcha is an unedited original, so it is optional to fix.
   - **Checked per the seat note:** no field says a point's time is "position times resolution".
     - The `timestamp_utc` guide ("from the period start and point position") is consistent with `parsers.py:530`, which computes `start + (position - 1) * resolution`.
     - The note body's "Period start + position" is loose but not one step late, and it is not a page field.

## What was checked and holds

- **Production-type codes: correct everywhere on the page.**
  - Code: `wind_solar_forecast.py:23-24` and `schemas/entsoe.py:127,132` give B16 Solar, B18 Wind Offshore, B19 Wind Onshore, which matches the ENTSO-E PSR list.
  - Silver: the diurnal profile above, and B16 = 0.0 each night on all 7 days.
  - The page uses the codes consistently in `what_it_is`, the `production_type` guide, key codes, `group_map` and the notebook rename.
  - The body Overview and schema-table corrections are correct and minimal. The other body edits (bronze path `raw_{ts}_{hash}` per `bronze/writer.py:57`, businessType A93, `psrType` in `optional_params` at `endpoints.py:49`) are also correct.
- **`published_at`.**
  - The guide ("Document `createdDateTime`: a fetch-time stamp, not the forecast's issue time") follows ruling #39.
  - "The document carries no forecast issue time" holds. The A69 header has mRID, `revisionNumber` (3), type, process type, sender, receiver, `createdDateTime` and `time_Period.timeInterval`, and nothing else time-like.
- **One value per target time, zone and code, the latest fetch.**
  - `unique(subset=[timestamp_utc, area_code, production_type], keep="last")` (`:75`) runs over rows read from `sorted(glob("raw_*.xml"))` (`:39`). Names are `raw_{fetched_at:%Y%m%dT%H%M%SZ}_{hash}`, so sorted order is fetch order. `APPEND_ONLY` is false, so each run rebuilds the partition.
  - Silver 14 to 20 Sep has 0 duplicate keys. 14 Sep has two fetches (15 Sep 19:57 and 21 Sep 10:07), and silver carries `published_at` 2026-09-21 10:07:59 for DE-LU, the later one.
  - Edge case: a later fetch that returns only an acknowledgement contributes no rows, so the earlier fetch's rows survive. The page does not say "latest fetch", so nothing to fix.
- **Chart.**
  - The committed series has `spec_origin: vault`, the build digest check passes, and no staged spec or override exists. It holds 672 x-points from 2026-09-14T00:00Z to 2026-09-20T23:45Z.
  - Each band equals silver DE-LU exactly (max abs diff 0.0005, from rounding).
  - Every alt number matches silver:
    - offshore 250.6 to 6,885.2;
    - onshore 569.7 at 14th 17:00 to 36,442.3 at 20th 15:45;
    - solar 0 every night, max 46,739.4 at 15th 10:30;
    - total 1,834.0 at 14th 17:45 to 63,664.1 at 17th 11:00.
  - The stack reads offshore, then onshore, then solar from zero. The key lists them top first.
  - The caption states dataset, MW, zone, 15-minute grain, window, one type per band, stacked, and "Day-ahead forecast values, not outturn". Stacking forecasts of different types is labelled as a forecast, and MW forecasts per type are additive.
  - No khaki is used. Offshore is `hatch-lines`, which is acceptable because the palette has one wind role.
- **Raw feed.**
  - The request URL is byte-identical to the sidecar `request_url` of `raw_20260921T100800Z_9a638f3e`, with the token shown as `$ENTSOE_API_KEY`. Parameter order follows `client.py:286-310`.
  - Ingest `--end 2026-09-21` is exclusive: `resolve_dates` gives midnight UTC and `day_subwindows` excludes it.
  - Transform `--end 2026-09-20` is inclusive (`runner.py:1138` `date_range`). There are no `PARTITION_SOURCE_OFFSETS`.
  - GB acknowledgement: bronze `raw_20260921T100756Z_ddc6771b.xml` has reason text "No matching data found ... (10YGB----------A)".
- **Record.**
  - The eight rows match silver exactly (Polars filter on 22:00, B16/B19) and are `generated_by: gridflow-sample`.
  - The guide has one line per non-pipeline column, key columns first.
  - The caption is accurate: four zones. IE-SEM sends an acknowledgement for 14 Sep, and B19 only on later days.
- **Notebook.**
  - The JSON was written by `scripts/run_notebooks.py`, cells are read-only, and there are no errors.
  - The relation is `silver_entsoe_wind_solar_forecast`, and the date column is `timestamp_utc` (`schema_manifest.py:192`).
  - `_date_range_predicate` covers whole UTC days with both ends included. `bitemporal_exclude()` = event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year, so `published_at` and `ingested_at` stay. The lead is accurate.
  - `plot_alt` matches `wind_solar_forecast-5.png`: solar at the bottom, peak near 64,000 on the 17th, low near 1,800 on the 14th.
- **Gates.**
  - `gridflow-build --only entsoe/wind_solar_forecast` passes. The mirror is byte-identical to the vault note.
  - `detect.mjs --json` returns only the advisory em-dash count, which is EIC padding and CLI flags (accepted, ruling #39). The page has 0 real em dashes, no "→", no middle dots, and no leakage words. The grep hits are "delivery", "acknowledgement" and template help-card text.
  - The front matter has no literal `---` (ruling #40).
- **Screenshots.**
  - Headless Chrome at 1440, 1024 and 768, plus 390 in a 390 px iframe. I also shot the unfolded frame and the opened notebook at 1440 and 768.
  - Nothing of this page's content is clipped or overlapping: turbines, scene edges, corner labels, chart tags and key, URL, commands, frame, guide, notebook output and related list.
  - The notebook filename clip at 390, and the notebook `.head()` table scrolling at 768, are template behaviour (ruling #39 seat item).
  - Light only: the site ships no dark theme (no `prefers-color-scheme` or `data-theme` in `site/hifi/assets`).
