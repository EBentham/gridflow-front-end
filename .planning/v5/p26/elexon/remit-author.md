# remit: author report

Writer, 2026-09-29. Canonical note: `vault-p26-elexon/30-vendors/elexon/datasets/remit.md` (CRLF, 360/360
lines); mirror `p26-elexon/vault/elexon/remit.md` is byte-identical (`cmp`). No staged spec and no
authored override existed.

**Status:** `gridflow-build --only elexon/remit` passes. The detector is **not `[]`**: it returns one
advisory finding, `em-dash-overuse` ("92 em-dashes in body text"). The page contains **0** em-dash
glyphs. Every hit is a `--` inside a vendor identifier in the eight-row frame (see Template problems 1).

Artefacts: `site/hifi/data/series/elexon/remit.json` (gridflow-distil, `spec_origin: vault`),
`site/hifi/data/samples/elexon/remit.json` (gridflow-sample), and
`site/hifi/data/notebooks/elexon/remit.json` plus `remit-5.png` (run_notebooks.py, 5 cells, no errors).

## Chart decision

- **Chart:** a bar chart counting unavailability messages by fuel type.
  - Each `mrid` with a revision published 13 to 21 September 2026 (UTC) is counted once, under the
    fuel type of its highest revision in that window.
  - Result: gas 246, no fuel type 99, biomass 79, wind 70, hydro 31, nuclear 8, other 8 (541).
- **Why not unavailable MW by fuel at an instant:** the distil engine cannot express it soundly.
  - `distil.py` applies `filter`, then `window`, then `dedup`. Any "active at T" filter (on status or
    on the event window) therefore runs before the latest revision is chosen. A message whose latest
    revision was dismissed, ended or moved falls back to an older `Active` revision.
  - Measured at T = cut-off = 2026-09-18 12:00 UTC:
    - correct method (latest revision first, then filter): 62 messages in force;
    - engine method (filter first, then latest): 76;
    - 14 `mrid`s differ.
  - Two further reasons a summed MW snapshot would mislead:
    - At that T, 5 assets have 2 or 3 active messages at once (`T_CRUA-2`, `T_FFES-3`, `E_LYNE3`,
      `E_THMRB-1`, `T_DINO-4`).
    - Every pumped-storage unit sends a production and a consumption message for the same window, so
      summing double counts.
- **Why a count is sound:** it is indifferent to which revision survives the dedup. It filters only
  on `message_type` and publish time, and `message_type` never varies within an `mrid`.
  - `fuel_type` varies within 2 `mrid`s (`Fossil Gas` against null). The caption says "the fuel type
    of its highest revision there".
- The caption states plainly that this counts messages, "not of outages in force or MW".
- **The trader reading lives in the notebook:** a timeline of the active nuclear messages returned
  by `query()`, one bar per message from event start to end.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Silver keeps every revision; no dedup in the transformer (what_it_is, grain) | `silver/elexon/remit.py:22-27` docstring ("every revision ... is preserved"), `:44` `APPEND_ONLY = True`, `:46-50` ("remit has NO unique(subset=...)"); no `unique()` in `transform()` |
| `timestamp_utc` is the vendor `publishTime` (fields.timestamp_utc) | `remit.py:85` maps `publishTime` to `published_at`; `:118-123` parses it into `timestamp_utc`; `published_at` and `created_time` are absent from `output_cols` (`:149-175`). Silver: `event_time == timestamp_utc` on all 2,291 rows |
| Elexon can re-send a revision number with changed content (grain, what_it_is, fields.revision_number) | Polars: 62 extra rows over 42 `(mrid, revision_number)` pairs; 3 pairs mix `Active` and `Dismissed`; e.g. `0000000000000001-ELXP-RMT-00000011` rev 12 appears 3 times with different `event_start_time` |
| "the number alone does not order revisions" (what_it_is) | Follows from the re-sends above; also, within an `mrid` sorted by publish time, the number falls in 32 steps (e.g. PEMB-41 revs 6 and 7 at 15:18:05, rev 7 has the earlier end) |
| `mrid` is shared by every revision (fields.mrid) | `latest_views.py:100-103` keys the latest view on `mrid`; `ENTITY_KEY_COLUMNS = ("mrid",)` (`remit.py:50`) |
| Key `[mrid, revision_number, timestamp_utc]` | The tightest identifying set in silver. It is still not unique: 6 rows repeat on every business column. The grain fact states re-sends |
| Revisions arrive at irregular publish times (facts.cadence) | Visible in the eight rows' `timestamp_utc` (15:18:04, 15:18:05, 15:18:05, 15:18:06, then 05:06:53 and later). Elexon states no cadence in anything in the repo or vault |
| 23-hour publish windows; windows over a day rejected (raw_feed.note) | `connectors/elexon/endpoints.py:231-240` (`max_chunk_hours=23`, comment "Vendor enforces an undocumented max-1-day query window ... return HTTP 400"); vault Implementation delta (23h → 200, 25h → 400, live 2026-05-09). Worded as a project finding |
| Bronze filed by window start day; a silver file can span two dates (raw_feed.note) | `client.py:314` `data_date = start.date()`; `bronze/writer.py:39` partitions on `data_date`. Silver file 2026-09-14 runs 14 Sep 22:02:59 to 15 Sep 20:02:06 |
| Request URL (raw_feed.requests) | `client.py:91-97` chunk loop (`while current < end`, 23 h steps); `endpoints.py:300-313` `publishDateTimeFrom/To` via `_to_utc_z` (`%Y-%m-%dT%H:%M:%SZ`), plus `page`. With `--start 2026-09-13`, chunk 6 is 2026-09-18T18:00:00Z to 2026-09-19T17:00:00Z. Its silver partition (file 2026-09-18) holds revisions 9 to 12 |
| Ingest `--end` exclusive; transform `--end` inclusive (commands) | `runner.resolve_dates` (`runner.py:479-501`): a bare date is midnight UTC; chunk loop `while current < end`; transform iterates dates inclusive. Last chunk 21 Sep 15:00 to 22 Sep 00:00 lands in partition 21 (silver file 21 ends 23:13:04). `PARTITION_SOURCE_OFFSETS` is the default `(0,)` (base.py:417); remit does not override it |
| `query()` reads `silver_elexon_remit_latest`, one row per `mrid`, filtered on `timestamp_utc` with both dates included, lineage dropped (notebook.lead) | gridflow_models `_get_method_registry`: `_DATE_COLUMN_BY_DATASET['remit'] = timestamp_utc`, `_RELATION_NAME_BY_DATASET['remit'] = silver_elexon_remit_latest`, TIMESTAMPTZ → half-open `[start, end+1d)` (`_get_method_registry.py:62-97`); `_BITEMPORAL_EXCLUDE` = event_time, available_at, vintage_policy, source_run_id, dataset_version, month, year; run returned `mrid.is_unique == True` |
| "newest silver write then highest revision" (notebook.lead) | `latest_views.py:100-103` `order_columns=("available_at", "revision_number")`, both `DESC NULLS LAST` (`:261-270`); `available_at` has one value per silver file (Polars: 1 unique per file) |
| unavailable MW "need not equal normal minus available" (fields.unavailable_capacity_mw) | Visible in the eight rows: normal 465, available 0, unavailable 394 (revs 5 to 10) |
| End moves between these revisions (fields.event_end_time) | Visible in the rows: 18:14:33, 22:14:33, 18:14:33, 16:14:33, 00:14:33 (20th), 15:59:33 |
| `NO_ASSET` names no asset (fields.asset_id) | gridflow_models `plant_universe.py:200-207` (cites the Elexon REMIT XML Implementation Guide); 11 silver rows carry it |
| here a BM unit ID (fields.asset_id) | `T_PEMB-41` is the BM unit form; gridflow_models renames `asset_id` to `bm_unit_id` for the BMUNITS join (`plant_universe.py:223-236`) |
| `fuel_type` values like `Fossil Gas`, not FUELHH codes (fields.fuel_type) | Polars `value_counts`: Fossil Gas, Wind Offshore, Biomass, Hydro Pumped Storage, Nuclear, Other, Wind Onshore, Hydro Water Reservoir, null |
| Pumped units send generating and pumping sides separately (key note, hydro) | Polars: every pumped-storage asset in the window (CRUA-1/2, DINO-3/4/5, FFES-3, FOYE-2) has both `Production unavailability` and `Consumption unavailability` messages with the same window |
| `fuelType` sent as null (key note, no_fuel) | Measured: 455 null rows; the transformer only renames `fuelType` (`remit.py:98`) |
| how_used: merit-order stack, point-in-time, join on `asset_id` | gridflow_models `estimators/stack/plant_universe.py:820-900` (`_fetch_active_outages`: latest per `mrid` observable at `as_of`, `Active` + `UnavailabilitiesOfElectricityFacilities` covering the target, joined on `asset_id` → `bm_unit_id`) |
| Chart numbers and alt | `series/elexon/remit.json`: x = gas, no_fuel, biomass, wind, hydro, nuclear, other; values 246, 99, 79, 70, 31, 8, 8; provenance rows_matched 1353, duplicates_dropped 812, rows_used 541 |
| plot_alt | `remit-5.png` checked by eye; `query()` output: nuclear Active rows T_HRTL-1 (6 May to 23 Sep), T_HEYM11 (26 Aug to 2 Oct, then 2 Oct to 7 Jan 2027), T_TORN-1, T_HRTL-2 (to 8 Oct), T_SIZB-2, T_HEYM27 |
| ingested_at is the transform time (body fix) | `remit.py:141-146` `datetime.now(UTC)` |

## Note-body corrections (canonical note; mirror copied)

1. **Dedup key.** Was "_inline in transformer_". Now: none in the transformer, plus the read-time
   `_latest` rule (`remit.py:22-27`, `:46-50`; `latest_views.py:100-103`).
2. **Point-in-time field.** Was `revision_number`. Now `timestamp_utc` (the vendor `publishTime`),
   with `revision_number` numbering revisions.
3. **`timestamp_utc` row.**
   - Was "Derived from (settlement_date, settlement_period) via settlement_period_to_utc"; the source
     field column said `_derived_`.
   - Now: source field `publishTime`, parsed to UTC (`remit.py:118-123`), with `published_at` and
     `created_time` noted as renamed but not written (`:149-177`).
4. **`fuel_type` row.** Was "(CCGT, COAL, NUCLEAR, WIND, etc.)". Now the vendor's values (`Fossil Gas`,
   `Wind Offshore`, `Nuclear`), not the FUELHH codes.
5. **`ingested_at` row.** Was "Time ingested into bronze". Now the silver transform time
   (`remit.py:141-146`).
6. **Silver sample.** `timestamp_utc` changed from `2026-05-06T00:00:00+00:00` to
   `2026-05-06T23:09:05+00:00`, the sample's own `publishTime`.
7. **Known issues, Revisions bullet.** Appended the measured re-send finding (62 extra rows over 42
   pairs, 3 mixing Active and Dismissed, 6 full repeats) and the 32 falling-number steps. Dated
   "measured on silver 2026-09-29".

Not changed, though stale or unverified:

- "Publication lag: Real-time as messages are raised" (no evidence either way).
- "Historical depth" (no vendor evidence).
- The Overview's "Regulation (EU) No 1227/2011 mandates ..." sentence.

## Unverified

- What `Active`, `Inactive` and `Dismissed` mean in Elexon's terms. The page lists only what the
  rows show.
- Why the 6 fully identical rows exist. A likely cause is an inclusive `publishDateTimeTo` at chunk
  boundaries; not checked against bronze.
- Whether the bidding zone `10YGB----------B` (15 rows) is GB. The page does not mention it.
- The vendor meaning of the fuel category `Other`. The key says undocumented.

## Open questions for the seat

1. **gridflow latest view (not this repo's code).** The view orders by `available_at` then
   `revision_number`.
   - For re-sent revisions with the same number in the same silver file, the pick is arbitrary.
   - For the 2 `mrid`s where the higher number was published earlier, the rule contradicts publish
     order.
   - Worth a gridflow issue: add `timestamp_utc` as a tie-break, or rank publish time first.
2. **Row choice.** The eight rows come from `mrid 11XINNOGY------2-NGET-RMT-00218399`. The note never
   names it: `---` must not appear in front matter, because the vault tools split notes on it. The
   filter is `asset_id = T_PEMB-41` and publish time on or after 18 Sep, which picks exactly revisions
   5 to 12.

## Template problems

1. **Detector gate vs. vendor identifiers.**
   - `detect-text.mjs:310-321` counts every `--(?=\S)` in the page text, including table cells.
   - ENTSO-E EIC codes pad with dashes (`10YGB----------A`). Every REMIT unavailability row carries
     one (`bidding_zone` is non-null on all 2,201 unavailability rows), at 5 hits per row, so 40 per
     frame.
   - Page text is 14,663 characters, so the rule fires at 30 or more hits. No eight outage rows can
     pass.
   - The current rows score 92: the registration code and `mrid` add 48, the CLI flags 4.
   - Rows from a participant without `--` in its code would score 44 and still fire, so I kept the
     most illustrative message.
   - The finding is marked `advisory: true`. Fix options: exclude `<td>`/`<code>` text from the rule,
     or accept advisory findings for this page. Any future ENTSO-E page showing EICs will hit the same
     rule.
2. **Distil engine: no post-dedup filter.** An outage-in-force chart for REMIT (or any
   revision-keyed register) needs dedup before filter, or a separate `filter_after_dedup` step. Until
   then, the only sound REMIT charts are counts.
3. **No dark theme.** The site has no `prefers-color-scheme` or `data-theme` rules, so the light and
   dark screenshots are identical. Not specific to this page.

## Screenshots

Taken with headless Chrome through a same-origin iframe wrapper on port 9745 (server stopped).

- **Widths:** 1440, 1024, 768 and true 390, each light, dark and unfolded. Tiles are in
  `scratchpad/remit/shots/`.
- **Fixed during the pass:**
  - The hydro key codes (`Hydro Pumped Storage, Hydro Water Reservoir`) overran the key column at
    1440. Codes are now `Hydro *, 2 values`, and the note names both values.
  - `revision_number` was folded away at 1024 and below. It now comes second, so the frame shows
    asset and revision at 390, plus start and end at 768, and available MW at 1024.
- **Otherwise:** nothing clipped or overlapping in the hero scenery, chart, key, raw feed, frame,
  guide, notebook panel or related list.
- **Unfolded:** the frame becomes a horizontal scroller, as designed.

## Revision 1 (response to remit-review.md, REVISE: 1 major, 6 nits)

All fixes are in the canonical note. The mirror is `cmp`-identical and CRLF (0 bare LF).
`gridflow-build --only elexon/remit` passes. The detector returns only the accepted
`em-dash-overuse` advisory. No artefact changed digest: the spec, select and cells are untouched, so
there was no re-distil, re-sample or notebook run.

1. **major, body Revisions bullet.** My "32 steps" counted ties within the same second.
   - Recount with a strict inequality: a pairwise join on `mrid` filtered to
     `timestamp_utc < timestamp_utc_b & revision_number > revision_number_b` gives 5 pairs across
     4 messages. Three are 1 s apart; `48X000000000357G-ELXP-RMT-20000025` is about 6 h 30 m apart.
   - Pairs sharing a publish second with different numbers: 72, across 47 messages.
   - The sentence now reads: "in 4 messages a lower number was published after a higher one (3 of
     them one second later), and 47 messages carry two numbers in the same publish second." The
     re-send counts are kept.
   - Also withdrawn from this report: the "32 steps" row in the evidence table and the PEMB-41 revs
     6 and 7 example. Those two share 15:18:05, so they are a tie, not an inversion.
2. **nit, body `event_status` row.** Was "Active / Withdrawn etc.". Now "Status as sent, e.g.
   `Active`, `Inactive`, `Dismissed` (silver, 2026-09-29; no `Withdrawn`); meanings not documented
   here".
3. **nit, key note `no_fuel`.** Checked bronze (read only), the 1,401 September records: `fuelType`
   is absent 310 times and never sent as an explicit null. The note now reads "Elexon's record has no
   `fuelType` field: a missing value, not a fuel."
4. **nit, `facts.grain`.** Now "... Elexon can re-send a revision, sometimes identically" (13 words).
5. **nit, `fields.timestamp_utc`.** "not an event time" is now "not the outage's start or end". The
   lineage `event_time` equals this column.
6. **nit, `related` uou2t14d and fou2t14d.** These now say how they relate: "Forward availability for
   the units these messages name" and "Forward availability for the fuel types charted here".
7. **Found in the 1280 check, not in the review.** The wind key codes (`Wind Offshore, Wind Onshore`)
   overran the viewport at 1280. Codes are now `Wind *, 2 values`, with the note "`Wind Offshore` and
   `Wind Onshore` counted together." (Same pattern as hydro.)

A correction to my own report: the evidence line for the pumped-storage key note said "with the same
window". The review found that untrue for 10 of 33 windows. The page never said it; the report line
is withdrawn.

**Screenshots:** 1280 (direct) and true 390 (390 px same-origin iframe, port 9745, server stopped),
folded and unfolded. Nothing clipped or overlapping in the hero facts, chart key, frame, guide,
notebook or related list.

**Not changed:** the detector advisory (accepted by the coordinator), and the review's gridflow
latest-view ordering note (a seat and gridflow issue, as in open question 1).
