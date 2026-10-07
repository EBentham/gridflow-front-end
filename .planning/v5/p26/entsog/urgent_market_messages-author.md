# entsog/urgent_market_messages: writer report

Single page, no family. Writer: Opus 5.5 · high, 2026-10-07.

## Status

**Recommendation: ship. No hold.** Bronze 133 records = `meta.total` 133 = unique `id` 133 = silver 133 rows:
nothing is lost and nothing repeats.

- **Why the HELD pages' defect cannot touch this table.** The endpoint is `reference=True` with no `requires_dates`
  (`connectors/entsog/endpoints.py:199-206`), so `date_window_dataset=False` (`silver/entsog/generic.py:332`). The
  per-day validity filter (`generic.py:157-161`) never runs.
- **No cross-day repeats, by construction.** Silver reads the newest bronze capture only (`NEWEST_VOUCHED`,
  `paths[:1]`, `generic.py:106-116,128-129,252-259`) and overwrites one file (`:284`). Bronze holds one capture, so I
  could not compare fetched days; the code rules repeats out.
- **Build:** `gridflow-build --only entsog/urgent_market_messages` passes.
- **Detector:** `detect.mjs --json` returns one advisory, `em-dash-overuse` ("49 em-dashes"). It is the accepted case:
  - The count is triggered only by codes and CLI flags: balancing zone keys `EE-LV------` (3) and `FR----------` (2),
    the OGE thread id `V0025119/1---------------` (2, plus 2 in `message_id`), and `--start`/`--end`.
  - The page has 0 real em dashes and 0 en dashes; the prose uses no dashes.
- **Chart:** a bar chart counting messages by sending operator (`market_participant_key`), each thread once at its
  highest version, from the capture fetched 27 September 2026. There is no time axis.
- **Sample:** made by `gridflow-sample` directly; no workaround was needed.
  - No value contains `|`.
  - 16 `remarks` and 8 `unavailability_reason` values contain newlines, so the eight rows were chosen newline-free.
- **Mirror:** `cp` then `cmp`, byte-equal; the note keeps CRLF (385 CRLF, 0 bare LF).

## Files written

- **Canonical note** (vault worktree): `30-vendors/entsog/datasets/urgent_market_messages.md`, with the `page:` block
  and body corrections.
- **Mirror:** `vault/entsog/urgent_market_messages.md` (front-end worktree). Before my copy it was stale only in line
  endings.
- **Artefacts:**
  - `site/hifi/data/series/entsog/urgent_market_messages.json` (`spec_origin: vault`; 133 rows read, 32 versions dropped by the thread dedup, 101 used).
  - `site/hifi/data/samples/entsog/urgent_market_messages.json` (8 × 39).
  - `site/hifi/data/notebooks/entsog/urgent_market_messages.json` and `urgent_market_messages-6.png` (6 cells, no
    errors, 1 image).
- **Built page:** `site/hifi/data-sources/entsog/urgent_market_messages.html`.
- **Retired:** nothing; no staged chart spec or authored override existed.
- **Screenshots** in `...\scratchpad\umm\shots\` (light only; the site has no dark theme):
  - full pages: `w1440.png`, `w1024.png`, `w768.png`;
  - `w390.png`, a true 390 px iframe (harness `...\umm\f390.html`, kept out of `site/hifi`);
  - crops: `w1440_frame.png`, `w1440_chart.png`, `w390_chart.png`, `s390_0..2.png`, `w1024_0..3.png`, `w768_0..3.png`.
  - Every crop is re-cut from the final build (after the label change); every section was viewed at all four widths.
  - Nothing clips or overlaps at any width.
  - At 390 the long chart labels first sat 8 to 10 px from the viewport edge. I shortened them (`NaTran DE`,
    `NaTran FR`, `Conexus`, `12 others`, with full names in key notes); the leftmost ink is now at 16 px.
- **Server:** my static server on 9879 is stopped.

## Coverage, grain and key (the asked-for checks)

- **One row = one message version**, not one message.
  - 133 versions in 101 threads. `message_id` = `thread_id` + `_` + `version_number` on all 133, and
    `(thread_id, version_number)` is unique.
  - Silver dedups on the vendor `id`, which is unique per version (`generic.py:193-199`), so every version served is
    kept. `id` is ENTSOG's opaque id of varying length, not a plain concatenation.
- **Page key:** `[thread_id, version_number]` (readable, equivalent). The guide says silver keeps one row per `id`.
- **What gridflow requests:** one call, `GET /urgentMarketMessages?limit=-1&timeZone=UCT`, with no operator, point or
  date filter (`build_params` `endpoints.py:263-281`; `client.py:75-76`). The bronze sidecar `request_url` matches
  verbatim.
  - So this is everything ENTSOG serves, not a GB selection.
  - Senders: 20 operators, all continental. None is UK. Counted by thread: OGE 31, NaTran Deutschland 21,
    GASCADE 12, NaTran 5, then the rest.
  - All 20 `market_participant_key` values resolve in `operators`, with matching EICs, and all 20 appear in
    `physical_flows`.
- **Completeness:** silver holds what the endpoint still serves at the newest fetch, not the history of what was
  published.
  - **Missing latest versions:** 6 of 101 threads have no `Yes` version. Examples are Conexus Kiemenai `...R006`
    (001 to 003, all `No`), two Fluxys Belgium threads, OGE `V0021586/1`, NaTran DE `...P001`, and LV `...R001`.
  - **Missing early versions:** two NaTran threads start at version 004.
  - **No archive in silver:** a message ENTSOG stops serving disappears from silver at the next transform, though
    bronze keeps it.
  - `is_archived` is never `true` (89 `false`, 44 null). That fits archived messages not being served, but nothing
    proves it.
- **DATA-MATRIX "133 messages, 2021-01-07 to 2026-09-22":**
  - 133 is versions; there are 101 messages.
  - The dates are the publication range of one night's capture, not coverage.
  - The page states neither.

## Time stamps (what each truly is)

ENTSOG's API manual (v2.1) defines no UMM response fields. It lists only the path "UMM Data Urgent Market Messages
Data" (`scratchpad\entsog_api_manual.txt:192-194`). Every guide meaning is therefore "as sent" or read from names and
values, and the record caption says so.

| Column | What it is | Evidence |
|---|---|---|
| `publication_date_time` | ENTSOG's publication stamp of this version. All 133 carry `+01:00`/`+02:00`, converted to UTC exactly. | bronze offset count 133/133; `parse_entsog_datetime_expr` (`generic.py:181-183`) |
| `timestamp_utc` | gridflow's copy of `publication_date_time` (equal on 133/133). `period_from` is absent, so `publication_date_time` is the first `_TIMESTAMP_PRIORITY` hit. `query()` filters on it. | `generic.py:51-59,185-187`; `schema_manifest.py:224` |
| `event_start` / `event_stop` | The event window as sent, converted from its offset (133/133 and 132/132 have offsets). One `event_stop` is null; 15 run to 2030 to 2099 (open-ended notices). Versions can move the window (Kiemenai v001 starts 2026-04-01 06:00 UTC, v002 2026-04-04 04:00 UTC). | bronze; sample rows |
| `last_update_date_time` | ENTSOG's update stamp, **not an edit time**. Details below the table. | silver; sidecar `fetched_at` 2026-09-27T00:31:23Z |
| `ingested_at`, `available_at` | Silver transform wall clock (00:31:28 UTC), not shown on the page. | `generic.py:201-206` |

Detail on `last_update_date_time`:

- 35 of 133 rows share 2026-09-27 00:28:56 UTC, three minutes before the 00:31:23 UTC fetch. All 35 have `u_mm_type`
  null.
- `Automatic` rows usually sit minutes after publication (median about 7 minutes; one is earlier than publication,
  one is 65 days later).
- 44 rows are null.
- It is never used for `timestamp_utc`.

## Evidence table

| Claim (page field) | Evidence |
|---|---|
| Single page, `gas` landscape; title "Gas urgent market messages" | `site/hifi/data/entsog.json` (no family; group "Reference and messages") |
| `facts.vendor` ENTSOG, `/urgentMarketMessages` | `endpoints.py:199-206`; `config/sources.yaml:461-462,573-576` |
| `facts.cadence` one call, `sources.yaml` daily | `client.py:75-76` (single request); `sources.yaml:575` `schedule: "daily"` |
| `facts.grain` and key | uniqueness checks above; `generic.py:193-199` |
| `what_it_is`: `Gas` = capacity unavailability; `Other` = other notices such as auction, tariff or outage-plan news | `Gas` rows carry `event_type`, `unavailability_type`, capacities and unit (69/69). `Other` rows carry none (64/64). Their remarks include OGE yearly auction capacity, terranets network fees, the NET4GAS 2026 outage plan and NET4GAS storage capacity changes. |
| `what_it_is`: versions under one `thread_id`; some threads lack their latest; silver keeps the newest fetch | 6 of 101 threads without `Yes` (sample shows Kiemenai); `generic.py:128-129,252-259,284` |
| `how_used` capacity at cross-border points | `affected_asset_name` values such as VIP France - Germany, VIP Oberkappel, VIP THE-ZTP, RC Basel |
| `how_used` join to the operator register | 20/20 keys resolve in silver `operators`, with EICs equal |
| Chart counts 31, 21, 17, 12, 5, 4, 4, 4, 3 (alt) | committed series `x`/`values`; `duplicates_dropped` 32, `rows_used` 101 |
| Caption "none of the 20 operators is from the UK" | 8 named bars plus the "12 others" key note listing 12 names = 20. The register's `operator_country_key` for all 20: DE 11; BE, CZ, DK, EE, FR, HR, HU, LV and SI 1 each; no `UK`, `GB` or `--`. |
| Key note: NaTran DE was GRTgaz Deutschland, same key | `DE-TSO-0004` named `GRTgaz Deutschland` on 1 row (2024-04-29) and `NaTran Deutschland` on 22; the name also appears in the notebook head output |
| Key notes: NaTran FR separate key; Conexus = Conexus Baltic Grid, Latvia | `operators`: `FR-TSO-0003` NaTran, FR; `LV-TSO-0001` Conexus Baltic Grid JSC, LV |
| `raw_feed.requests` | bronze sidecar `request_url` verbatim |
| `raw_feed.commands`: ingest with no dates; transform 27 Sep to 27 Sep | `cli.py:186-258` (dates optional; reference endpoints ignore them); the reference family rescans the whole tree on each target date (`runner.py:1153`; `generic.py:252-259`); same as the shipped `operators` page |
| `raw_feed.note`: bronze under the UTC fetch day | `data_date=None` for reference (`client.py:76`); bronze folder `2026/09/27`, `fetched_at` 2026-09-27T00:31:23Z |
| Guide: capacities sent as text, cast to float | bronze `"42000000.00"`; `generic.py:189-191` (`_NUMERIC_NAMES`) |
| Guide: `unit_measure` varies, never sum | 61 rows `kWh/d`, 8 rows `kWh/h`, 64 null |
| Guide: technical = available + unavailable "here" | true on all 8 sample rows (and within float error on all 69 `Gas` rows; not claimed beyond the rows) |
| Guide: `event_status` values, OGE v002 `Dismissed` | values Active 117, Inactive 8, Dismissed 8; sample row |
| Guide: `balancing_zone_eic` present when key null | OGE rows: key null, EIC `37Y701125MH0000I` (sample) |
| Guide: `unavailability_reason` sometimes only a reference number | OGE sample `21032049` |
| Guide: `share_point_publication_id` begins with the sender's EIC | `21X000000001379RManual1384`, `21X000000001304LAutomatic886` |
| Guide: `direction` blank on some `Gas` messages | 31 `Gas` rows `''` (OGE), visible in the sample |
| Guide: `is_archived` `false` or null on these rows | sample rows |
| Notebook lead: relation, `timestamp_utc`, inclusive, lineage dropped | `_relation_name_for_dataset` returns `silver_entsog_urgent_market_messages`; `source.py:401-451`; 39 columns in, 35 returned (`event_time`, `available_at`, `source_run_id`, `dataset_version` excluded) |
| Notebook outputs: event types 48 / 47 / 5 / 1 | cell 5 output, matching my Polars count on the thread-deduped frame |
| `plot_alt`: 15 OGE active `Gas` messages, all ending 1 Oct 2026; starts 2 in Oct 2025, 2 in Apr, 3 in Jul, 8 on 1 Sep 2026 | the rendered PNG and the deduped silver |
| Related: `entsog/operators`, `entsog/physical_flows`, `gie/unavailability` (blank page, allowed), `elexon/remit` | joins above; all four in vendor page sets; the build resolves them |

## Body corrections (canonical note, CRLF kept, tagged CORRECTED/ADDED 2026-10-07)

1. **Silver path:**
   - Was: `.../year=YYYY/month=MM/urgent_market_messages_YYYYMMDD.parquet`.
   - Now: one file, `.../urgent_market_messages/urgent_market_messages.parquet`, rewritten from the newest capture.
   - The note now says messages ENTSOG drops leave silver.
   - Evidence: `endpoints.py:199-206`, `generic.py:106-116,128-129,252-259,284`; on disk.
2. **Dedup key:**
   - Was: "`(id)` if present, else all non-`timestamp_utc` columns".
   - Now: vendor `id`, keep last; one row per version; `(thread_id, version_number)` unique; `message_id` structure.
3. **Point-in-time field:**
   - Was: "`last_update_date_time` or `publication_date_time`".
   - Now: `timestamp_utc` copies `publication_date_time` (`generic.py:51-59,185-187`).
4. **Silver schema table:**
   - Removed the stray `| int` cell in the `id` row (it shifted the columns).
   - `is_latest_version` bool becomes str (`Yes`/`No`); `share_point_point_id` str becomes int.
   - Added a `timestamp_utc` row and one lineage row.
5. **`messageType` gotcha:**
   - Was: "`'unavailability'` dominant, `news` appears".
   - Now: the values are `Gas` (69) and `Other` (64), with what each carries.
6. **`isLatestVersion` gotcha:**
   - Was: "keep only `isLatestVersion=true`".
   - Now: the flag is text. 6 of 101 threads have no `Yes`, so take the highest `versionNumber` per `threadId`.
7. **Added gotchas:**
   - `lastUpdateDateTime` is a shared stamp, not an edit time.
   - Capacities are strings in mixed units, with placeholders and a version-001 thousandfold error.
   - All stamps carry offsets; there are open-ended stops.
   - Senders: 20 continental TSOs, no filter sent.
8. **Implementation delta:** the exact request (`limit=-1&timeZone=UCT`, one call, no paging).

Not changed: the overview, the curl example (`limit=100` is valid for the vendor; the page uses the connector's
URL), the bronze and silver samples, the operationalData gotchas, and the TODO rows.

## Could not verify

- ENTSOG's meaning of `uMMType` (`Automatic`, `Feeds`, null), `sharePointPointId`, `sharePointPublicationId`,
  `isArchived` and `eventStatus` `Inactive` versus `Dismissed`. The manual defines no fields, and I cannot call the
  API. The page says "as sent" or "ENTSOG does not define it".
- Whether the endpoint serves every message ever published or only a recent or active subset. The 2021 to 2026 spread
  and the missing versions suggest a subset, with no vendor statement either way. The page claims no history.
- Whether the 27 September shared `lastUpdateDateTime` is a nightly platform refresh. It is likely; I have only one
  capture.
- Whether `10000000000` kWh/d (NaTran DE, VIP France - Germany) and `1` kWh/d (NaTran `SPNS2U`) are operator
  placeholders. They look like it; the page shows neither.
- Whether these are REMIT disclosures. The page avoids the term; ENTSOG's manual does not use it.

## Open questions

1. Should urgent market messages stay a "reference" register in gridflow? A replace-whole snapshot cannot keep the
   history of an event stream. See Defects.
2. Should the chart count by event type instead (47 transmission system, 48 `Other`, 5 other unavailability,
   1 compressor station)? I chose operator because it shows that no UK operator posts here, which matters on a GB
   site. The event-type split appears in the notebook output.
3. Should gridflow_models offer a "latest version per thread" view (as `silver_elexon_remit_latest` does for REMIT)?
   It would need to handle threads with no `Yes`.

## Template problems

1. **`em-dash-overuse` advisory from vendor codes.** The detector counts `--` inside codes (balancing zone keys, OGE
   thread ids, CLI flags) as em dashes. It is accepted under the seat ruling, but it will recur on any ENTSOG page that
   prints zone keys.
2. **No dark theme.** "Light and dark" cannot be checked, as other writers reported.
3. **`gridflow-sample` and newlines.** Values with newlines would split rows (same root as the `|` issue,
   `sample.py:67-87`). I avoided it by choosing rows; no workaround file was needed.

## Defects (pasteable)

- **[gridflow silver, design] ENTSOG urgent market messages are modelled as a replace-whole reference snapshot, so
  silver keeps no message history.**
  - `endpoints.py:199-206` sets `reference=True`. Silver then reads only the newest bronze capture
    (`generic.py:106-116,128-129,252-259`) and overwrites one file (`:284`).
  - A message or version ENTSOG stops serving disappears from silver at the next transform. Bronze keeps it.
  - This is an event register: point-in-time use needs the union of captures, deduped on `id`.
  - Fix: treat it as an append dataset (union of all bronze captures, dedup on `id`), or add a "latest per thread"
    view built from that union.
- **[vendor data, observation] ENTSOG's UMM response omits versions.** 27 Sep 2026 capture:
  - 6 of 101 threads carry no `isLatestVersion = Yes` version. Examples: Conexus `25063021X000000001379R006`
    v001 to v003, Fluxys Belgium `26062421X-BE-A-A0A0A-Y001`/`Y002`, OGE `V0021586/1`, NaTran DE
    `26032521X000000001008P001`, Conexus `25110321X000000001379R001`.
  - Two NaTran threads (`25050221X-FR-A-A0A0A-S001`, `25102721X-FR-A-A0A0A-S001`) start at version 004.
  - Any consumer filtering on `isLatestVersion = Yes` silently drops those messages.
- **[vendor data, observation] `lastUpdateDateTime` is a platform stamp on many records.** 35 of 133 records (all
  `uMMType` null) share `2026-09-27T02:28:56+02:00`, three minutes before gridflow's 00:31:23 UTC fetch. It is not a
  per-message edit time.
- **[vendor data, observation] Suspect capacity values.**
  - `unavailableCapacity` `10000000000` kWh/d with 0 available (NaTran Deutschland, VIP France - Germany, threads
    `26032521X000000001008P002` and `26032521X000000001008P001`).
  - `1` kWh/d unavailable at NaTran `SPNS2U`.
  - terranets RC Basel version 001 is 265.77 kWh/h against 265,778 in version 002.
  - The units mix `kWh/d` (61) and `kWh/h` (8).
- **[DATA-MATRIX] `entsog/urgent_market_messages` "133 messages, 2021-01-07 to 2026-09-22".**
  - 133 is message versions; there are 101 messages (threads).
  - The dates are the publication range of the one capture, not coverage.
- **[vault, fixed in this branch] `urgent_market_messages.md` errors:**
  - wrong silver path, dedup wording and point-in-time field;
  - `is_latest_version`/`share_point_point_id` types and a broken `id` row;
  - `messageType` values wrong (`unavailability`/`news` versus actual `Gas`/`Other`);
  - an `isLatestVersion` filter advice that drops messages.

## What the checker should look hardest at

1. The completeness wording in `what_it_is` ("the versions it still serves, some threads without their latest").
   Check it against the 6 threads and the code path.
2. The caption's "none of the 20 operators is from the UK": 8 named bars plus the 12-name key note.
3. The `last_update_date_time` guide line, "not an edit", against the 35 shared stamps.
