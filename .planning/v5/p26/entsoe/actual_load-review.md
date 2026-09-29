# entsoe/actual_load: checker review

Checker: Opus 5.5 · high, 2026-09-29. Inputs: `BATCH-entsoe.md`, `review-rubric.md`, `author-brief.md`, the writer's report, the canonical note diffed against `origin/master` (vault worktree), the three artefacts, the page rebuilt with `gridflow-build --only entsoe/actual_load`, gridflow code, local silver and bronze (read only), and screenshots I took myself.

## Verdict: REVISE

One major (a GB claim stated as a standing ENTSO-E behaviour on evidence from our own raw files) and four nits. No blockers. The fix is a few words in two fields.

## Findings

### 1. major: `page.related[3].note` (`elexon/indo`), and the GB half of `page.what_it_is`

**What is wrong.** The `related` note reads "GB demand outturn; ENTSO-E answers GB with code 999". That is present tense, unscoped, and has ENTSO-E as its subject, so it reads as a standing vendor rule. `what_it_is` has the same problem in a milder form: "GB, and IE-SEM on the days charted, get ENTSO-E's 'no matching data' answer (code 999)". IE-SEM is scoped to the charted days, but GB is not.

**Evidence.** The only evidence is what gridflow received.
- Bronze scan over `C:\gridflow-data\bronze\entsoe\actual_load\**\raw_*.xml` and their sidecars: `10YGB----------A` returned `Acknowledgement_MarketDocument` code 999 in 26 of 26 files. The `periodStart` values run from 202608010000 to 202609200000, and every day from 14 to 20 Sep is included.
- The vault body's "GB empty post-Brexit" line is a vault author's observation, not a quoted vendor document.

This is the "measured on our copy, stated as universal" class that rubric section 1 forbids. The seat asked for the page to word it as what gridflow received.

**Fix.** Scope GB the way IE-SEM is scoped. For example:
- `what_it_is`: "GB and IE-SEM got ENTSO-E's 'no matching data' answer (code 999) on the days charted."
- `related` note (12 words or fewer): "GB demand outturn; gridflow's GB calls to ENTSO-E returned code 999."

### 2. nit: `page.chart_view.alt`, "DE-LU runs highest"

FR is above DE-LU in 2 of the 672 intervals:
- 18 Sep 22:00 UTC: DE-LU 41,278.7, FR 42,136.7.
- 18 Sep 22:15 UTC: DE-LU 41,103.8, FR 41,256.9.

Evidence: a Polars pivot of silver over 14 to 20 Sep, filtered on `fr > de`. "Runs highest almost throughout" or "highest on most intervals" would be exact.

### 3. nit: `page.what_it_is`, last sentence

"Whether the figure counts network losses is ENTSO-E's definition, not stated here."
- The sentence brings in "network losses", a concept no source on the page introduces.
- "Not stated here" is ambiguous.

The page does not overclaim what total load includes, which was the seat's point 3. The problem is clarity: it reads as a hint. Something plainer would do, such as "ENTSO-E defines what total load includes; that definition is not quoted here." Dropping the sentence would also work.

### 4. nit: note body, silver schema row `timestamp_utc` (body correction 4)

"Responses are `curveType` A03" cites `connectors/entsoe/parsers.py:533-596`. That code shows how the parser handles A03 (forward-fill); it does not show that the responses are A03. The evidence for that is bronze: all 104 GL documents carry `<curveType>A03`, from my scan. Either cite the bronze check or scope the claim to the responses held ("responses checked were A03"). This is an evidence-citation mismatch under rubric section 7.

### 5. nit: `page.chart_view.key[nl].note`, "Lows fall near midday on every day shown"

This is borderline. From silver, NL's daily minima fall at 11:45, 11:00, 11:15, 10:00, 09:45, 10:45 and 14:00 UTC on 14 to 20 Sep. On the 20th the trough is broad, from 12:00 to 14:00 UTC with hourly means 4,812, 4,596 and 5,031. "Near midday" is a fair reading of the chart, and "cause undocumented" does not guess a cause. Keeping it is acceptable. "Lows fall between late morning and early afternoon UTC" would be tighter.

## Seat checks, answered

1. **IE-SEM and GB, code 999.** Confirmed from bronze. Both return `Acknowledgement_MarketDocument` code 999 in 26 of 26 files, 1 Aug to 20 Sep, including every charted day. The vendor text reads "No matching data found for Data item ACTUAL_TOTAL_LOAD_R3 [6.1.A] (...)". IE-SEM is worded as received and scoped; GB is not (finding 1).
2. **The chart.** The committed series matches silver exactly for all four zones: 672 points each, from `2026-09-14T00:00Z` to `2026-09-20T23:45Z`, 2,688 rows used, no duplicate keys, `PT15M` only. Ranges:

   | Zone | Min (MW) | Max (MW) |
   |---|---|---|
   | DE-LU | 35,310.541 | 65,453.589 |
   | FR | 31,367.59 | 50,605.26 |
   | NL | 4,094.801 | 11,972.166 |
   | BE | 6,808.78 | 11,901.35 |

   `spec.group_map` decodes the `\x2D` keys to the real EICs.
   - **DE-LU 39.4 GW dip.** 39,435.41266 at 16 Sep 23:15 UTC. Bronze `2026/09/16/raw_20260921T100306Z_767d12fb.xml` has `<position>94</position><quantity>39435.41266`, and the neighbours are 46,282.37 and 45,556.62. It is the vendor's value: all 32 GL documents in the week declare 96 points, so nothing was forward-filled. The key note says "as sent" and "cause undocumented" and gives no cause.
   - **NL midday lows.** No cause is guessed (see nit 5).
   - **Alt numbers.** Weekday DE-LU peaks are 63.0 to 65.5 GW at 06:45 to 08:45 UTC. Weekend peaks are 52.4 and 50.9 GW. The Sunday low is 35.3 GW at 02:15 UTC on the 20th. FR runs from 31.4 to 50.6 GW. NL's low is 4,094.8 MW at 11:00 UTC on the 15th. All match silver, apart from nit 2.
3. **"Total load".** No field claims what the figure includes. The summary, facts and caption only name it (A65/A16, Article 6.1.A, "Realised"). See nit 3 for the one awkward sentence.

## Seat mid-task note (timestamp wording, cadence)

- The `timestamp_utc` guide line reads "period start plus (position minus 1) times resolution". That matches `parsers.py:530` and `582` (`start_dt + (position - 1) * resolution`), so it is not the one-step-late wording.
- `facts.cadence` is scoped: "Every 15 minutes (`PT15M`) in each zone shown". `record.fields.resolution` reads "as ENTSO-E sends it", and the caption is scoped to the window. No general cadence rule appears on the page.
- For the seat only, not a page finding: the body lines "15-minute resolution by default for continental zones. Some smaller zones still publish PT60M", "Publication lag ~1 hour", "Historical depth ~5 years" and "Revisions within ~24 hours" predate this batch and are unverified. The writer left them untouched and listed them.

## Verified, no finding

- **Request.** The URL matches `_fetch_document` parameter order: `documentType`, `periodStart`, `periodEnd`, `outBiddingZone_Domain` (`client.py:558`), `processType`, `securityToken`. The `yyyyMMddHHmm` format comes from `endpoints.py`. `DEFAULT_ZONES` holds six zones, with no override in `config/sources.yaml`.
- **Commands.**
  - Ingest `--end 2026-09-21` is exclusive: a bare date resolves to midnight UTC, and `day_subwindows` excludes an end at midnight.
  - Transform `--end 2026-09-20` is inclusive: `run_transform` uses `date_range(start.date(), end.date())`.
  - No offsets are needed: `PARTITION_SOURCE_OFFSETS` is `(0,)` and `EVENT_WINDOW_FILTER` is True.
- **Grain and key.** `actual_load.py:65` dedups with `unique(subset=["timestamp_utc","area_code"], keep="last")`. `area_code` is `outBiddingZone_Domain.mRID`, mapped to `in_domain` and then renamed. `load_mw` is `quantity` in unit `MAW`.
- **`published_at`.** It is the document `createdDateTime` (`actual_load.py:76`). Over 104 GL documents, `createdDateTime` minus the sidecar `fetched_at` runs from -3.48 s to +0.10 s, so "within seconds of the request" holds. It follows ruling #39.
- **Notebook lead.** `query()` reads `silver_entsoe_actual_load`. The TIMESTAMPTZ predicate is `>= start 00:00 UTC` and `< end+1 day`, so both ends are included. Lineage columns are excluded and rows are ordered by the date column. The head prints `+01:00`, which is kernel local time.
- **Notebook artefact.** Written by `scripts/run_notebooks.py`. All cells are read-only, there are no error outputs, and the PNG loads. `plot_alt` matches the plot. `needs` ("14 to 20 September 2026") matches the commands.
- **Samples.** `generated_by: gridflow-sample`. The eight rows are all four zones at 11:00 and 11:15 UTC on 15 Sep and match silver. The guide has a line for every non-pipeline column, with the key columns first.
- **Build and detector.** The build with `--only entsoe/actual_load` succeeds. `detect.mjs` reports only the accepted `em-dash-overuse` advisory (43), which comes from EIC padding and CLI flags. The rendered prose has no em dashes, middle dots, arrows, local-data words or "live" wording. No staged spec and no authored override exist.
- **Related pages.** All four resolve, and each note is 12 words or fewer.
- **Mirror.** Its content is identical to the canonical note. It differs only in line endings, which come from the repo's `.gitattributes` `*.md text eol=lf`. The canonical note keeps CRLF.
- **Body corrections 1, 2, 3 and 5.** Each is supported:
  - Bronze file names on disk match `raw_<ts>_<hash>.xml` with sidecars.
  - `day_subwindows` confirms one file per zone and UTC day.
  - The `published_at` probe above covers correction 3.
  - IE-SEM: 26 of 26 files returned 999 from 2026-08-01 to 2026-09-20.
- **Screenshots.**
  - I took full-page headless Chrome shots at 1440, 1024 and 768, and at 390 through a 390 px iframe.
  - I also took CDP shots of the unfolded frame (1440, 390) and the open notebook drawer (1440, 390).
  - Nothing is clipped or overlapping: hero scenery, turbine tops, chart, key notes, stratum corner labels, frame, guide and notebook.
  - The unfolded frame scrolls inside its box (`scrollWidth` 1990 against `clientWidth` 1280 at 1440). The page has no horizontal overflow at any width.
  - The site has no dark scheme (0 matches for `prefers-color-scheme` or `data-theme` in `tokens.css`, `theme.css` and `site.js`), so light only.
  - The port 9810 server was stopped.
