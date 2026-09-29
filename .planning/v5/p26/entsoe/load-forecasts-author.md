# entsoe/load-forecasts (family, lead `load_forecast`): writer report

Writer: Opus 5.5 · high, 2026-09-29. Page built with `gridflow-build --only entsoe/load_forecast`. The build passes; the only warnings are for other datasets. `detect.mjs --json` returns only the accepted `em-dash-overuse` advisory (56, from EIC padding and CLI flags). The prose has no em dashes, arrows or middle dots.

## What was made

- **Notes.** A `page:` block on the canonical lead note `vault-p26-entsoe/30-vendors/entsoe/load_forecast.md`. Body corrections on all four notes (lead, `_weekly`, `_monthly`, `_yearly`). All four are CRLF and copied byte for byte to `p26-entsoe/vault/entsoe/` (`cmp` clean).
- **Artefacts.** These are new; none of these datasets had a staged spec or authored override.
  - `site/hifi/data/series/entsoe/load_forecast.json`: `spec_origin: vault`, 4 series × 672 points, 2,688 rows, 14 to 20 Sep 2026.
  - `site/hifi/data/samples/entsoe/load_forecast.json`: `generated_by: gridflow-sample`, 8 rows.
  - `site/hifi/data/notebooks/entsoe/load_forecast.json` and `load_forecast-6.png`: from `scripts/run_notebooks.py`, 6 cells, no errors.
- **Chart.** A line chart of silver `entsoe/load_forecast` (day-ahead only): four zones (DE-LU, FR, NL, BE), every 15-minute value, UTC days 14 to 20 Sep 2026, `aggregation: last`.
  - The window and zone paints match the approved `actual_load` page, so the two can be read side by side.
  - The caption carries the issue-time caveat: every value in the window was served on 21 Sep, after delivery, and the document carries no issue time. The frame shows `published_at` 2026-09-21 for 15 Sep intervals.
- **Frame.** All four zones at 11:00 and 11:15 UTC on 15 Sep, the same instants as the `actual_load` frame.
- **Notebook.** Joins `load_forecast` to `actual_load` over 14 to 20 Sep and computes forecast minus actual, the MAE per zone and a plot. The lead says the forecast is scored as fetched on 21 Sep, not as issued.
- **Screenshots.** Headless Chrome (`timeout 60`, own profile) at 1440, 1024 and 768, and 390 through a 390 px iframe; server on port 9835, since stopped. Nothing is clipped or overlapping: turbines, scene edges, corner labels, chart and key, four member request blocks, frame, guide, notebook, related.
  - The long URLs wrap inside their boxes at 390, and the frame folds to `timestamp_utc` plus `…`. Both are template behaviour, the same as on the approved `actual_load`.
  - Light only: the site has no dark theme.
  - I did not shoot the unfolded frame or the open notebook drawer.

## Coverage and keys (the two questions asked)

**What the rows are.** Scanned from bronze (208 data documents plus acknowledgements, with sidecars) and silver, read only.

| Table | Silver rows | Zones | Point times | Resolution in every response | Series per response | What silver keeps |
|---|---|---|---|---|---|---|
| `load_forecast` | 9,216 = 24 UTC days × 4 zones × 96 | DE-LU, FR, NL, BE | 2026-08-01 00:00 to 08-05 23:45 and 09-02 00:00 to 09-20 23:45 UTC | `PT15M`, curve `A03`, 90 to 96 declared points | 1 (`A04`) | Latest fetch per `(timestamp_utc, area_code)` |
| `load_forecast_weekly` | 48 = 12 days × 4 zones | same four | 22:00 UTC on D-1 for each request day D (2026-07-31 22:00 to 09-13 22:00) | `P1D`, 1 point | 2 (`A60`, `A61`) | `A61` only, 48 of 48 |
| `load_forecast_monthly` | 48, only 16 distinct keys | same four | Week starts: 2026-07-26, 08-02, 09-06 and 09-13, 22:00 UTC | `P7D`, 1 point | 2 (`A60`, `A61`) | `A61` only; one week repeated up to 6 times |
| `load_forecast_yearly` | 48, only 16 distinct keys | same four | as monthly | `P7D`, 1 point | 2 (`A60`, `A61`) | as monthly |

- **GB and IE-SEM** (`10YGB----------A` and `10Y1001A1001A59C`, both in `DEFAULT_ZONES`, `endpoints.py:395`) returned acknowledgement code 999 in every file for all four tables:
  - 26 day-ahead files each;
  - 12 files each for the three horizon tables.
- **Horizon.**
  - Day-ahead: the period returned is exactly the requested UTC day.
  - Weekly: the CEST day that ends on D (22:00 on D-1 to 22:00 on D).
  - Monthly and yearly: the whole CEST week containing D's 00:00 UTC start.
- **Monthly against yearly.** For the same week, zone and business type they are equal for FR and BE and differ for DE-LU and NL (16 of 32 pairs differ).

**Keys.** `(timestamp_utc, area_code)` overwrites; no publish is kept.
- The transformer reads bronze files in name order, which is fetch order (`load_forecast.py:38`), and runs `unique(keep="last")` (`:68`). `published_at` is not in the key.
- Proof: 2026-09-08 was fetched on 9 Sep 01:43 and again on 15 Sep 19:55. DE-LU differs on 8 of 96 intervals, by up to 11 MW. Silver holds the 15 Sep values on 384 of 384 rows, the earlier fetch on 376.
- Every day-ahead fetch in bronze came after its delivery day. The earliest gap is 8 Sep, fetched 9 Sep 01:43 UTC.
- `revisionNumber` is 1 in every response. So no forecast-vs-actual on this page may claim an issue time or "as issued". The page says "as fetched on 21 September, after delivery".

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Four processes A01, A31, A32, A33 on document A65, domain `outBiddingZone_Domain` (`facts.vendor`, `raw_feed`, `family`) | `connectors/entsoe/endpoints.py:34-36, 127-135`; `client.py:558-559` |
| Regulation 543/2013 Art. 6(1)(b) to (e): day-ahead per market time unit; week-ahead max and min per day; month- and year-ahead max and min per week (`what_it_is`, `facts.cadence`) | legislation.gov.uk retained copy, Art. 6 (fetched 2026-09-29; quoted in each note body). EUR-Lex returned an empty page. |
| Total load = generation plus imports, minus exports and storage use, losses included, Art. 2(27) (`what_it_is`) | legislation.gov.uk Art. 2(27), quoted verbatim in the lead note body |
| "Day-ahead `PT15M` in every response charted" (`facts.cadence`) | Bronze scan: all 104 day-ahead data responses are `PT15M` |
| One row per zone and interval start, from the latest fetch (`facts.grain`, `record.key`, `fields.published_at`) | `load_forecast.py:38,68`; the 8 Sep double-fetch proof above |
| GB and IE-SEM got code 999 on the days charted (`what_it_is`, `related[3]`) | Bronze acknowledgements, 26 of 26 files each, including 14 to 20 Sep |
| Chart: 672 points per zone, 14 to 20 Sep; alt values | Committed series: DE-LU min 37,214.2 (20th 01:45), max 63,444.6 (16th 09:45); weekday peaks 63.0, 62.7, 63.4, 63.4, 61.8 GW; weekend peaks 52.0 and 51.5. FR 31,300 to 51,801. NL 7,563.2 (19th 13:30) to 13,255.9. BE 6,778.5 to 11,339.9. DE-LU is above FR on all 672 intervals (Polars pivot, 0 intervals with FR > DE-LU). |
| Caption: values served on 21 Sep, after delivery; no issue time | Silver `published_at` over 14 to 20 Sep runs from 2026-09-21 10:04:43 to 10:06:17. The GL_MarketDocument header has mRID, revisionNumber, type, process, sender, receiver, `createdDateTime` and `time_Period.timeInterval`, and nothing issue-like. |
| `timestamp_utc` = period start + (position − 1) × resolution (`fields`) | `parsers.py:530` (and 582 for A03 forward-fill) |
| `load_forecast_mw` = point `quantity`, unit `MAW` (`fields`) | `load_forecast.py:61`; bronze `quantity_Measure_Unit.name` MAW |
| `published_at` = `createdDateTime`, a fetch-time stamp (`fields`, ruling #39) | `_published_at.py`. `createdDateTime` minus sidecar `fetched_at`: −2 to +1 s (day-ahead), 0 to +1 (weekly), −7 to +1 (monthly), −2 to +1 (yearly). |
| `forecast_horizon` constants (`fields`) | `load_forecast.py:26,79`; `load_forecast_weekly.py:79`; `_monthly.py:15`; `_yearly.py:15` |
| Request URL (`raw_feed.requests`, `family.members[].request`) | Sidecars `load_forecast/2026/09/14/*.meta.json` (DE-LU, 21 Sep fetch) and the A31/A32/A33 DE-LU sidecars for 14 Sep: parameter order matches byte for byte; token shown as `<your-entsoe-api-key>` as on `actual_load` |
| Ingest `--end 2026-09-21` exclusive; transform `--end 2026-09-20` inclusive; no offsets | `day_subwindows` (`client.py:162`); `PARTITION_SOURCE_OFFSETS = (0,)` (`base.py:417`); `EVENT_WINDOW_FILTER = True` (`load_forecast.py:27`). The same semantics were confirmed by the `actual_load` checker. |
| Weekly `P1D` one point per day, keeps `A61`, drops `A60`; own schema (`family.members[1].differs`) | Bronze scan; silver-to-bronze join 48/48 on `A61`; `EntsoeLoadForecastWeekly` (`schemas/entsoe.py:303`) and `LoadForecastWeeklyTransformer` |
| Monthly and yearly `P7D`; keep `A61`; each week repeats once per day fetched (`differs`) | Bronze scan; silver 48 rows / 16 keys, max 6 repeats, equal values; event-window exempt (`load_forecast_monthly.py:16`, `_yearly.py:16`) |
| Notebook lead: relations, whole UTC days, both ends, lineage dropped | `schema_manifest.py:171` (`timestamp_utc`); the same `query()` path the `actual_load` checker verified |
| Notebook outputs, `plot_alt` | MAE: DE-LU 1,257, BE 295, FR 595, NL 1,707 MW. Errors: NL daily max 6,602 (15th 10:15 UTC), 6,030 (18th 09:45), 6,698 (20th 11:00); DE-LU −4,186 (17th 03:00) to 4,157 (16th 23:15 UTC, 00:15 on the plot's UTC+1 clock); FR −1,893 to 2,234; BE −1,078 to 935. The plot is on the kernel's UTC+1 clock, as the head's `+01:00` shows. |
| Related pages resolve | The build resolves all four; `elexon/ndf` is the `demand-forecasts` lead |

## Body corrections (all four notes, smallest spans)

**Lead `load_forecast.md`**
1. Overview "Resolution typically PT15M" is now scoped to the 104 responses in bronze. Added the legal basis: Art. 6(1)(b) and Art. 2(27), quoted, with the source URL and the note that EUR-Lex returned an empty page.
2. Publication lag "Published D-1 ~12:00 CET, then revised" (unsourced) is replaced by a quote of Art. 6(2)(b).
3. Bronze path `raw_<uuid>.xml` becomes `raw_<ts>_<hash>.xml` plus sidecar (`bronze/writer.py:57`). Granularity "per query window" becomes per zone and UTC day (`client.py:162`).
4. Dedup key: added keep-last in fetch order (`load_forecast.py:38,68`) and the event-window filter (`:27`). Point-in-time field: fetch-time stamp.
5. Schema `timestamp_utc`: source formula, curve A03, and forward-fill (`parsers.py:533-596`).
6. Schema `published_at`: "leak-proof forecast issue time" becomes a fetch-time stamp, with the measured gap.
7. Gotchas:
   - "GB empty post-Brexit" is now scoped: GB and IE-SEM returned 999 in 26/26 files.
   - "latest revision wins by dedup" is replaced by: the latest *fetch* wins, with no issue time and `revisionNumber` 1. The 8 Sep double-fetch evidence is included, and every fetch was after delivery.

**`load_forecast_weekly.md`**
1. Overview "weekly resolution (`P7D`)" is wrong: responses carry two series (`A60`, `A61`), each one `P1D` point per day. Added a quote of Art. 6(1)(c).
2. Publication lag is now a quote of Art. 6(2)(c).
3. Bronze path and granularity as in the lead; the period runs 22:00 UTC on D-1 to 22:00 UTC on D.
4. Bronze sample: the invented `P7D`/60800 sample is replaced with the real DE-LU 10 Sep document (both series, abridged, file named).
5. Dedup key: the collision is validated (`A61` on 48/48) and the event-window exemption cited (`_event_window.py:159`).
6. Schema `timestamp_utc`: formula, and 22:00 UTC. `resolution`: "typically `P7D`" becomes `P1D`. `published_at` corrected.
7. Silver sample replaced with a real row (with a comment naming the dropped `A60` value).
8. Gotchas:
   - GB and IE-SEM scoped.
   - "Sparse output ... verify" is replaced by the validated finding, including that no source names which code is max or min.
   - The `P7D` gotcha becomes `P1D` (`parsers.py:39`).
9. Implementation delta: "Possible silver bug ... Not validated" becomes validated, logged as a defect.

**`load_forecast_monthly.md`**
1. Overview:
   - "typically published once per month" is replaced by `A60`/`A61`, one `P7D` point per week, and a quote of Art. 6(1)(d).
   - "Same schema and parser as week-ahead" is wrong: it subclasses the day-ahead transformer (`load_forecast_monthly.py:11`) and uses the day-ahead schema; weekly has its own.
2. Publication lag is now a quote of Art. 6(2)(d).
3. Bronze path and granularity: one file per zone and UTC day. The whole CEST week containing D's start is returned, so days repeat the week.
4. Bronze sample: the invented `P1M`/58000 sample is replaced with the real DE-LU 10 Sep document.
5. Dedup key: the collapse to `A61`, no event-window filter (`:16`), 48 rows for 16 keys.
6. Schema `timestamp_utc`: Sunday 22:00 UTC week start. `resolution`: `P1M` becomes `P7D`. `published_at` corrected.
7. Silver sample replaced with a real row.
8. Gotchas:
   - GB and IE-SEM scoped.
   - Two series, one kept.
   - Repeated weeks (dedup before use).
   - "`P1M` approximates 30 days" is stale: the parser uses calendar arithmetic (`parsers.py:76-93,523-528`), and responses are `P7D` anyway.
9. Implementation delta: "`timedelta(days=30)` ... known approximation" is stale for the same reason. Defects noted.

**`load_forecast_yearly.md`**
- The same set as monthly, with Art. 6(1)(e) and 6(2)(e), and `P1Y`/365-day claims corrected to `P7D` and calendar arithmetic.
- Overview "annual resolution" and "identical to day-/week-/month-ahead" corrected.
- Real DE-LU sample and row.
- Added a gotcha that yearly differs from monthly for DE-LU and NL.

Untouched (unverified, pre-existing): "Historical depth ~5 years", "Rate limit ... 1 req/s", `PT60M` for older windows, the Modelling notes, and the curl examples. The curl examples are the vendor's shape and not wrong.

## Could not verify

- **Which of `A60`/`A61` is the maximum.** No repo or vault source names them. The ENTSO-E code list is not quoted, and the Guide PDF was unfetchable in earlier batches. `A60` < `A61` in every response in bronze. The page never says which is max or min: it says only that silver keeps `A61` and drops `A60`.
- **The EU original text of Arts. 2(27), 6(1) and 6(2).** I quoted the UK retained copy on legislation.gov.uk because EUR-Lex returned an empty page. These points are very unlikely to differ, but a checker may want the EU text.
- **Week and day boundaries in winter.** Every response seen starts at 22:00 UTC (CEST), and the page does not state a boundary as a rule.
- **What the day-ahead forecast looked like when issued.** gridflow never fetched it before delivery, so any as-issued value is unknowable from bronze.

## Open questions for the seat

1. **Regulation as a source.** Is the legislation.gov.uk retained copy acceptable as the vendor-side document? If yes, its Art. 2(27) text also sources the `actual_load` total-load definition flagged as unsourced (BACKLOG 13g). I did not touch `actual_load`.
2. **The lossy horizon members.** The page describes the three horizon members only in `family.members[].differs`, and says plainly that each keeps `A61` of two series and that monthly and yearly repeat weeks. The chart, frame and notebook use the lead only. Is that enough, or should the family be held until the gridflow fix lands?
3. **The NL error pattern.** The notebook shows NL forecast minus actual peaking near 6.6 GW around midday on three days, a large error for a zone of 4 to 13 GW. The page states the numbers and gives no cause. It may be a definitional mismatch between the NL forecast and actual series, which is worth a research unit. It is not claimed anywhere.

## Template problems

None new. The notebook filename clip at 390 is a known seat item (ruling #39), and the URL wrap and frame fold at 390 behave as on the approved pages.

Environment note, not a template issue: the front-end `.venv` has no `tzdata`, so Polars cannot print UTC datetimes there. I ran the probes under the gridflow venv.

## Defects (pasteable)

- **gridflow: week-, month- and year-ahead load forecasts drop one of the two regulated values.**
  - What happens: `load_forecast_weekly`, `load_forecast_monthly` and `load_forecast_yearly` dedup on `(timestamp_utc, area_code)` (`silver/entsoe/load_forecast_weekly.py:68`, and `load_forecast.py:68` inherited by monthly and yearly).
  - Why it loses data: every A31/A32/A33 response carries two series, business types `A60` and `A61`. The regulation requires a maximum and a minimum per day or week (Reg. 543/2013 Art. 6(1)(c) to (e)). The parser keeps `business_type` (`connectors/entsoe/parsers.py:453`), but the transformers drop it.
  - Evidence: silver keeps only `A61`, 48 of 48 weekly rows and 16 of 16 distinct monthly and yearly keys (bronze and silver compared 2026-09-29).
  - Fix: add `business_type` to the output columns and the key (a `DATASET_VERSION` bump and backfill).
- **gridflow: month- and year-ahead tables repeat each week across daily partitions.**
  - What happens: requests are one per UTC day (`client.py:162`), and ENTSO-E returns the whole CEST week containing the day's start. Both tables are exempt from the event-window filter (`load_forecast_monthly.py:16`, `load_forecast_yearly.py:16`), and dedup runs per partition.
  - Evidence: silver holds 48 rows for 16 distinct `(timestamp_utc, area_code)` keys, and the week of 2026-09-06 22:00 appears 6 times.
  - Impact: `data.entsoe.query(...)` returns the duplicates.
  - Fix: request per week or month, or trim to the owning partition, or dedup across partitions at read.
- **gridflow: the day-ahead `load_forecast` keeps one fetch per interval and has never been captured before delivery.**
  - What happens: the key `(timestamp_utc, area_code)` with keep-last over fetch-ordered bronze (`load_forecast.py:38,68`) overwrites earlier fetches. On 2026-09-08, DE-LU changed on 8 intervals by up to 11 MW between the 9 Sep and 15 Sep fetches, and only the later survives.
  - Every fetch in bronze (1 Aug to 20 Sep) was after its delivery day, so the table holds no point-in-time day-ahead forecast.
  - Related seat item (ruling #39): the code calls `published_at` a "leak-proof forecast issue time" (`silver/entsoe/_published_at.py:1-8`, `schemas/entsoe.py:101-106`), but it is the fetch time.
  - Fix, if point-in-time is wanted: ingest before delivery (D-1) and add `published_at` to the key.
- **vault: the week-, month- and year-ahead notes claimed `P7D`, `P1M` and `P1Y` resolutions and invented bronze samples.**
  - Actual resolutions: weekly `P1D`, monthly and yearly `P7D`.
  - The monthly and yearly notes also described a 30-day/365-day parser approximation that `_advance_calendar` replaced.
  - Status: corrected in this batch's vault branch (all four notes).
