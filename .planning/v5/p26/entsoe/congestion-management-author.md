# congestion-management: writer report

Family page `congestion-management`. The lead is `redispatching_internal`; the members are `redispatching_cross_border`, `countertrading` and `congestion_management_costs`. Writer: Opus 5.5 · high, 2026-09-29, with two advisor calls. Worktrees are as in `BATCH-entsoe.md`; screenshot port 9824.

## Status

- **Notes:**
  - The `page:` block is on the canonical lead note (`vault-p26-entsoe/30-vendors/entsoe/datasets/redispatching_internal.md`).
  - All four notes have body corrections.
  - All four are mirrored byte for byte, with CRLF kept: 304/304, 177/177, 171/171 and 210/210 lines. `cmp` shows them identical.
  - The copies bring in the canonical costs note's live-probe callout.
- **Artefacts, all from real data:**
  - `site/hifi/data/series/entsoe/redispatching_internal.json`: `spec_origin: vault`, 1 series × 672 points.
  - `site/hifi/data/samples/entsoe/redispatching_internal.json`: eight rows.
  - `site/hifi/data/notebooks/entsoe/redispatching_internal.json` and `-5.png`: 5 cells, 1 image, no errors.
  - No staged spec or authored override existed for any member.
- **Build:** `gridflow-build --only entsoe/redispatching_internal` passes.
  - The member pages are pointers to `congestion-management.html#<member>`.
  - It prints 3 content warnings: "silver schema rows empty". Two are for my members (`redispatching_cross_border`, `countertrading`); they come from the legacy schema-table parse and the members render as pointers. The third is `total_nominated_capacity`, not mine.
  - The one error it defers belongs to another writer (`water_reservoirs: page.chart_view.caption: 42 words`). I checked by wrapping `_scoped`: nothing names my family.
- **Detector** (absolute path): only `em-dash-overuse` (advisory, EIC padding).
  - The rendered page has 0 real em dashes, 0 `→`, 0 `·` and 0 literal backticks.
  - Grep for locally, held, our, "since 20", "N days", live, now and real-time: nothing. The only "rows" hit is the template's frame aria-label ("8 rows of 13 columns").
- **Screenshots, CDP headless Chrome** (`scratchpad/cm/cm_shot.mjs`, every call under `timeout 60`, profiles `%TEMP%\cdp-cm-*` left in place):
  - Full pages at 1440, 1024, 768 and 390: `scrollWidth` equals the width everywhere. I cropped each section and looked at it: hero scenery (turbine tops whole), chart, key, raw feed, frame and guide, notebook, related. Nothing is clipped or overlapping.
  - Dark captures are byte-identical to light: the site defines no `prefers-color-scheme` or `data-theme`.
  - The notebook drawer was opened at 1440 and 390. The plot image is 690/780 px of its container at 1440 and 300/300 at 390, and loads once scrolled into view (it is lazy).
  - At 390 the `.ipynb` tab clips the filename (seat ruling: template, leave it). Long `%2D` EIC parameters wrap inside their box.
  - Frame unfolded (the `#fx` toggle) at 390 and 1440: the box scrolls internally (2,311 px inside 390; 2,279 inside 1,280) and the document stays at 390 and 1440. Checked visually at 1440.
  - No server was started.
- **Late changes after the second advisor call:**
  - `what_it_is` now says "a TSO-ordered adjustment to relieve a constraint", not "change of output": `mktPSRType` `A04`/`A05` are not in the vault code list, so output versus load is unverified.
  - The chart `unit` is now `MWH`, matching caption, alt, guide and notebook. The series was re-distilled, and the build and detector were rerun (same results as above).

## Chart and window

- **Chart:** a line of silver `entsoe/redispatching_internal`, NL rows (`in_area_code` = `10YNL----------L`), quarter-hourly, `aggregation: last`, 15 to 21 September 2026. That is 672 points, 0 to 84.0 in `MWH` as sent.
- **Why this window:** it is the longest run of whole NL days. CET day 14 Sep is absent from the NL replies (13 Sep has 88 rows, 14 Sep 8). In the window every NL row equals the down (`A02`) series, so the chart can be labelled honestly as "Netherlands, down (A02)" with the loss stated.
- **Why not BE:** BE silver mixes up-only and down-only days with nothing to tell them apart, so it is not charted.

## What a row is, per member (code + bronze)

All four use the H6 transformer: output `timestamp_utc, in_area_code, out_area_code, <value>, business_type, resolution, published_at` plus lineage (`h6_market.py:107-117`). The dedup key is `(timestamp_utc, in_area_code, out_area_code, business_type)`, `keep="last"` (`h6_market.py:91-99`). The parser reads `flow_direction`, `reason_code`, `timeseries_mrid`, `currency_unit` and the measure unit is never read at all (`parsers.py:284-402`); none of these reach silver.

| Member | Area in row | Direction in reply | Unit in reply | Business type | Reason | Dedup effect |
|---|---|---|---|---|---|---|
| `redispatching_internal` | the zone itself in both domains (NL→NL, BE→BE), whatever pair was requested | `flowDirection.direction` `A01` and `A02`, separate TimeSeries | `MWH` | `A85` | `B24` | **Drops a direction.** 22,431 parsed rows give 2,101 keys but 4,021 key+direction pairs. NL: silver = `A02` in 1,728/1,728 quarter-hours, and `A01` differs in 1,013 (476 of the 672 in the chart window). BE: 119 rows are `A01`-only (8, 15, 17 Sep), 62 are `A02`-only (4, 5 Aug) |
| `redispatching_cross_border` | ordered pair NL→BE, line `HORTA DOEL` (`location.name`) | `A02` only | `MWH` | `A46` | `B24` | No loss seen: the duplicate keys carry identical values |
| `countertrading` | ordered pair FR→DE-LU, `connecting_MarketParticipant` `10XFR-RTE------Q` | `A02` only | `MAW` | `B03` | `B24` | No collisions: 12 parsed rows give 12 keys |
| `congestion_management_costs` | the zone in both domains | none | `currency_Unit.name` `EUR` | `A46`, `B03`, `B04` | none | Month rows copied into every daily partition (24 keys × 31 = 744 rows); 9 of the 24 keys are a false forward-filled point |

Every populated reply also carries `curveType` `A03`, so points hold until the next declared one (`parsers.py:533-600`).

## Coverage and usability (report only; none of this is on the page)

- **`redispatching_internal`:** usable for NL down-regulation only.
  - 1,909 silver rows, 19 UTC days (1 to 5 Aug, 8 to 21 Sep).
  - NL has 1,728 rows; BE has 181 on 4, 5 Aug and 8, 15, 17 Sep.
  - Bronze: 168 XML, 73 populated. The NL document came back under GB/NL, NL/DE-LU and NL/BE alike; BE under GB/BE and FR/BE (and NL/BE on 4 Aug).
  - The up series is not recoverable from silver.
- **`redispatching_cross_border`:** thin but sound.
  - 288 rows, NL→BE only, 6 Jul 22:00 to 9 Jul 21:45 UTC. Values are 0 to 1.25 `MWH` (sum 15).
  - Bronze: 624 XML; only NL/BE returned data, in 4 of 78 daily replies. Every other reply was an Acknowledgement.
- **`countertrading`:** thin but sound.
  - 12 rows, FR→DE-LU: 22 Sep 04:00 to 05:45 (300 then 150) and 25 Sep 05:00 to 05:45 UTC.
  - Bronze: 72 XML, 2 populated.
- **`congestion_management_costs`:** usable only after de-duplication, and after dropping the 30 Jul 22:00 rows.
  - 744 rows, 15 real month-zone-type values:
    - July (stamped 2026-06-30T22:00Z):
      - BE: `A46` 721,049; `B03` 0; `B04` 721,049.
      - FR: `A46` 0; `B03` 10,603,628; `B04` 10,603,628.
      - NL: `A46` 16,882,788.28; `B03` 0; `B04` 16,882,788.28.
    - August (2026-07-31T22:00Z):
      - FR: `A46` 0; `B03` 5,231,136; `B04` 5,231,136.
      - NL: `A46` 19,634,716.80; `B03` 0; `B04` 19,634,716.80.
    - BE August returned an Acknowledgement.
  - GB, DE-LU and IE-SEM returned only Acknowledgements (71 each).
  - `B04` = `A46` + `B03` in all 15 values (project observation).
- **`query()`:** only the lead can be queried. The local catalogue `C:\gridflow-data\gridflow.duckdb` has no `silver_entsoe_redispatching_cross_border`, `_countertrading` or `_congestion_management_costs` view; `data.entsoe.query()` raises `CatalogException` for all three. The notebook therefore reads the lead only.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Article 13.1.A/B/C (`summary`, `what_it_is`) | Vendor acknowledgement texts quoted in the notes: `REDISPATCHING_INTERNAL_R3 [13.1.A]`, `COUNTERTRADING_R3 [13.1.B]`, `COSTS_OF_CONGESTION_MANAGEMENT_R3 [13.1.C]` |
| Document types A63, A91, A92 (`facts.vendor`) | `endpoints.py:164-189` |
| `A85` internal, `A46` redispatching (`what_it_is`, `business_type` line) | `endpoints.py:164-176`; `gridflow/.planning/audit/2026-05-31-vendor-truth-audit/vendor-docs/entsoe-codes.md:53-54` |
| Quarter-hourly `PT15M` as sent; costs `P1M` (`facts.cadence`) | `resolution` in all silver rows of the three MW tables is `PT15M`; costs `P1M` (bronze and silver); canonical costs callout (live probe 2026-08-04) |
| Grain = key (`facts.grain`) | `h6_market.py:91-99` |
| Up and down arrive as separate series; silver keeps no direction (`what_it_is`, caption, key note, `quantity_mw` line) | Bronze TimeSeries with `flowDirection.direction` `A01` and `A02`; parser `parsers.py:316-319`; output columns `h6_market.py:107-117`; up/down reading `activated_balancing_qty.py:25` |
| Every chart point is `A02` in the window (caption) | 672 of 672 NL rows, 15 to 21 Sep, equal the bronze `A02` value (Polars join of silver against gridflow-parsed bronze by key+direction) |
| The `A01` series for the same quarter-hours is not in silver (key note) | NL `A01` is present in all 672 window quarter-hours and differs from silver in 476 |
| `A92` monthly, copied into every daily partition (`what_it_is`) | P1M replies; exemption `_event_window.py:201-204`; per-partition dedup `h6_market.py:91-99`; 24 keys × 31 copies |
| Some months gain a false second point (costs `differs`) | `_add_months` `parsers.py:54-63`, `_advance_calendar` `76-93`, A03 fill `578-600`; July Period `[06-30T22:00Z, 07-31T22:00Z)` gives 07-30T22:00Z; silver has 9 such keys |
| Unit `MWH` as sent (chart unit, caption, alt, `quantity_mw` line, lead `differs`) | `quantity_Measurement_Unit.name` `MWH` in every A63 TimeSeries in bronze; the parser never reads it |
| `MAW`, `B03`, one point per quarter-hour (countertrading `differs`) | Bronze A91: each TimeSeries has one Period of one `PT15M` step with one Point, `B03`, `MAW` |
| "Mostly empty replies" (cross-border, countertrading `differs`) | Bronze: 4 of 624 and 2 of 72 files are `TransmissionNetwork_MarketDocument`; the rest are Acknowledgements ("No matching data found"); the notes' existing "EMPTY-by-design" |
| One GET per UTC day per pair (eight) or per zone (six) (`raw_feed.note`) | `_FLOW_PAIRS` `client.py:40-49`, dispatch `211-227`; `DEFAULT_ZONES` `endpoints.py:395`; per-day chunking `client.py` `fetch` via `day_subwindows` |
| Internal replies name one zone in both domains; NL under three pairs (`raw_feed.note`, `in_area_code` line) | Bronze meta `request_params` versus TimeSeries domains: GB/NL, NL/DE-LU and NL/BE all return NL→NL |
| Request URLs, parameter order | Bronze `.meta.json` `request_url` for each member (documentType, periodStart, periodEnd, in_Domain, out_Domain, extra params) |
| Ingest 15 to 22 excluded, transform 15 to 21 included (`commands`) | `day_subwindows` end exclusive (`utils/time.py:123-147`); a one-UTC-day request returns `period.timeInterval` 22:00Z to 22:00Z over two CET days, covering all of UTC day D; silver day D is trimmed to `[D, D+1)` (event-window filter); no `PARTITION_SOURCE_OFFSETS` |
| Point time = start + (position − 1) × resolution (`timestamp_utc` line) | `parsers.py:530` and `582` |
| `published_at` fetch-time stamp | Seat ruling #39; three fetch batches in this table (16 Aug, 15 Sep, 26 Sep) |
| Alt numbers (0 to 84.0, peak 19:00 to 19:45 on 18 Sep, zero stretches, ≥32.5 on 17 to 20 Sep) | The committed series JSON: min 0, max 84.0 at 2026-09-18T19:00Z and 19:15Z; zero runs 15 Sep 00:00 to 04:45, 07:00 to 07:45, 15:00 to 15:45, 18:00 to 22:45; 16 Sep 04:00 to 07:45, 15:00 to 22:45; 21 Sep from 15:00; minimum non-zero 17 to 20 Sep is 32.5 |
| `plot_alt` (62.5 to 84 on 18 and 19 Sep) | Minimum on 18 Sep 63.75, on 19 Sep 62.5; notebook output table peaks 80.00, 70.50, 82.75, 84.00, 71.50, 71.25, 66.25 |
| `notebook.lead` | `source.py:401-451`: relation `silver_entsoe_redispatching_internal`, date column `timestamp_utc` (`schema_manifest.py:187`), inclusive ends, lineage exclusion |
| Related pairs | `cross_border_flows`, `net_transfer_capacity` and `auction_revenue` are all `domain_style="zone_pair"` over `_FLOW_PAIRS` (`endpoints.py:51-52, 139-143, 233-237`) |

## Body corrections (smallest spans, cited in the notes)

**`redispatching_internal.md`**
- Cross-zonal parameters: "`in_Domain == out_Domain` (e.g. GB→GB)… `(GB, GB)`, `(FR, FR)`" is now the eight `_FLOW_PAIRS` (`client.py:40-49`, `211-227`), with replies naming the zone in both domains. The curl-example footnote now says the same.
- Bronze sample: added the populated reply envelope, covering the two-CET-day period, the `A01`/`A02` series, `MWH`, `A03`, `PT15M`, `B24`, the NL `A05` and BE `A04`/`B21`/`location.name` differences.
- Silver schema: added `published_at` (`h6_market.py:107-117`). The silver sample is now a real row (NL 2026-09-18T19:00Z, 84.0, `PT15M`), replacing a synthetic GB 400.0 `PT60M`.
- Known issues: added the direction loss and the unit (`MWH` in a column named `quantity_mw`).

**`redispatching_cross_border.md`**
- Bronze sample: added a correction note. The root is `TransmissionNetwork_MarketDocument`, not `Publication_MarketDocument`, with `flowDirection.direction`, `MWH`, `A04`, `B21`, `location.name` `HORTA DOEL`, `A03`, `PT15M`, `B24`; only NL/BE returned data.
- Silver schema: added `published_at`. The sample is now a real NL→BE row (1.25, `PT15M`), replacing a synthetic GB→FR 250.0 `PT60M`.
- Known issues: silver keeps neither `flowDirection` nor `location.name`.

**`countertrading.md`**
- Bronze sample: added a correction note. `businessType` is `B03` and does not carry direction; direction is `flowDirection.direction`. Also: one quarter-hour per TimeSeries, `MAW`, connecting participant, `B24`.
- Silver sample: now a real FR→DE-LU row with `business_type` `B03`, replacing the empty `business_type` and synthetic GB→FR 200.0 `PT60M`. Added `published_at` to the schema line.
- Known issues: added what silver drops.

**`congestion_management_costs.md`**
- Overview: "Daily" is now "Monthly (`P1M`…)", which the note's own callout already said.
- Bronze sample: `quantity_Measure_Unit.name` and `<quantity>` are now `currency_Unit.name` and `congestionCost_Price.amount`. Added the three business types and the `B04` = `A46` + `B03` observation, scoped.
- Schema table:
  - `amount_eur` source is now `congestionCost_Price.amount` (suffix match `parsers.py:148-153`).
  - `business_type` and `resolution` now give the values sent.
  - Added a `published_at` row.
- Silver sample: now a real NL July row (`P1M`), replacing the synthetic `P1D`.
- Known issues: added the partition copies, the false second point, and the UTC stamp of a month's row (with the missing view noted).

## Not verified

- **Meanings:**
  - `B03` and `B04`: not in the vault code list (the page prints codes only).
  - `mktPSRType` `A04`/`A05` and `pSRType` `B21`: not needed on the page.
  - Reason `B24`.
- **Magnitude:** what `MWH` per `PT15M` point means (energy per quarter-hour or a rate). The page says "as sent" only.
- **Whether up-and-down in one quarter-hour means two actions or a netting convention.** This is undocumented; the page makes no claim.
- **Why NL CET day 14 Sep is absent** (no reply, or no redispatch). The chart window avoids it.
- **Why the catalogue lacks three views:** the stale `gridflow.duckdb` was written at 01:23 BST on 27 Sep, and the cost and cross-border silver directories are later (01:44 and 02:14 BST). `gridflow transform` refreshes views (`cli.py:293`), so either a different path wrote them or the refresh failed silently.

## Open questions for the seat

1. **Is charting only the NL `A02` series acceptable while silver drops `A01`?** The precedent is capacity-allocated-nominated (`A07` of three). The alternative is holding the family until the transformer keeps `flow_direction`.
2. **Costs member:** the page says only "some months gain a false second point" and "silver copies into every daily partition". Should it instead be held off the family until the two defects are fixed?

## Template problems

- The member headings in the raw feed print the note's H1 code in capitals ("REDISPATCHING_INTERNAL", "A91", "A92"), inconsistently across members. It is cosmetic and template-side.
- At 390 the notebook tab clips the filename (known, seat ruling).
- Lazy-loaded notebook images don't render in full-page headless captures unless scrolled into view. This is a capture artefact, not a page fault; useful for other writers.

## Defects (pasteable, for gridflow BACKLOG 12+ and the vault remediation page)

1. **ENTSO-E A63 redispatching (`redispatching_internal`, `redispatching_cross_border`): silver drops flow direction.**
   - The parser reads `flowDirection.direction` (`parsers.py:316-319`), but `_H6ZonePairTransformer` neither outputs it (`h6_market.py:107-117`) nor keys on it (`h6_market.py:91-99`, `keep="last"`).
   - Replies carry separate `A01` (up) and `A02` (down) TimeSeries per zone and CET day.
   - Measured on `redispatching_internal`: 2,101 silver keys against 4,021 key+direction pairs. NL silver equals `A02` in 1,728/1,728 quarter-hours, and the `A01` value differs in 1,013. BE silver mixes 119 `A01`-only and 62 `A02`-only rows with nothing to tell them apart.
   - Fix: add `flow_direction` (and, for A46, `location.name`) to the output and the key; bump `DATASET_VERSION`.
2. **ENTSO-E H6 quantity tables: the unit is not parsed and the column name asserts MW.**
   - A63 replies send `quantity_Measurement_Unit.name` `MWH` and A91 replies `MAW`; the parser never reads the tag.
   - The value lands in `quantity_mw` for both.
   - Fix: parse and store the unit, or rename or document the column per dataset.
3. **ENTSO-E `congestion_management_costs` (A92): each monthly row is copied into every daily partition.**
   - The transformer is exempt from the event-window filter (`_event_window.py:201-204`) and dedups only within a partition.
   - Silver has 744 rows = 24 keys × 31. Any read over the partitions multiplies every month by the number of days fetched.
   - Fix: write the month once (partition by Period start) or dedup across partitions.
4. **ENTSO-E parser: `A03` forward-fill over a `P1M` Period invents a second point.**
   - `_advance_calendar` steps a calendar month from the UTC Period start (`parsers.py:54-63, 76-93`), and the A03 loop fills until the Period end (`parsers.py:578-600`).
   - July 2026 (`[06-30T22:00Z, 07-31T22:00Z)`): position 2 = 07-30T22:00Z < end, so a false July row appears at 30 Jul 22:00 UTC (9 of 24 costs keys).
   - Any month after a shorter month is affected. The same code path serves `balancing_financial_expenses_income` and any `P1M`/`P1Y` A03 series.
   - Fix: for calendar resolutions, step in the zone's local calendar or stop at the Period end when the declared point count is 1.
5. **ENTSO-E A63 internal is requested over the eight cross-border `_FLOW_PAIRS`** (`endpoints.py:171-176` `domain_style="zone_pair"`).
   - The same zone document comes back under up to three pairs (NL under GB/NL, NL/DE-LU and NL/BE), tripling bronze and requests.
   - Silver dedup hides it, but a revision arriving under one pair only would be resolved by file order.
   - Fix: a per-zone `in_Domain == out_Domain` request, as the vault note claimed.
6. **RESOLVED by the seat's view refresh (see `congestion-management-author-2.md`); do not log as open.** Was: **Local catalogue: `C:\gridflow-data\gridflow.duckdb` has no view for `silver_entsoe_redispatching_cross_border`, `silver_entsoe_countertrading` or `silver_entsoe_congestion_management_costs`.**
   - The file was written at 01:23 BST on 27 Sep; the silver directories came later.
   - `data.entsoe.query()` raises `CatalogException` for all three.
   - Fix: refresh views (any `gridflow transform` or `build`), and find out why the 27 Sep transforms did not.
7. **Observation, not a defect:** in every populated A92 reply seen (FR, NL, BE; July and August 2026), `B04` = `A46` + `B03`.
