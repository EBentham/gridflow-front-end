# entsog/urgent_market_messages: review 1

Checker: Sonnet 5.5 · high, 2026-10-07. Inspection only; no file written except this one.

## Verdict: REVISE

0 blockers, 3 majors, 7 nits. The numbers are right and the chart is honest. The majors are all
wording: the page does not say plainly what silver can do with history (and "still serves" implies a
withdrawal nobody observed), the capacity guide omits placeholder and mis-scaled values, and
`last_update_date_time` is glossed with an unverified "not an edit".

## Reproduced and passing

- **Chart.** Silver (133 rows, 39 columns, one `id` per row, `(thread_id, version_number)` unique,
  `message_id` = `thread_id_version_number` on 133/133). Highest version per `thread_id`: 101
  messages. By `market_participant_key`: OGE 31, NaTran DE 21 (20 as `NaTran Deutschland` plus 1 as
  `GRTgaz Deutschland`, 2024-04-29), GASCADE 12, NaTran FR 5, Conexus 4, terranets 4, FGSZ 4,
  NET4GAS 3, and 12 others totalling 17 (BE 2, DE-0005 2, EE 2, HR 2, DE-0003 2, then seven singles).
  Committed series `x`/`values` equal this; alt text equal; key note names are the 12 others.
  `spec_origin: vault`; the build digest check passes; no staged spec or authored override.
- **No UK sender.** The 20 keys resolve in silver `operators`; `operator_country_key` is DE 11 and
  BE, CZ, DK, EE, FR, HR, HU, LV, SI 1 each. The register does hold UK keys (`UK-TSO-0001` to
  `-0004` are in `physical_flows`), so the observation is meaningful and the caption scopes it to
  the fetch.
- **Versions versus messages.** The page never calls a version a message: grain, key, caption
  ("Eight versions of four messages"), notebook lead ("every stored version") are right.
- **Request and commands.** Bronze sidecar `request_url` is `...urgentMarketMessages?limit=-1&timeZone=UCT`
  (`endpoints.py:263-281`); `meta.count` 133 = `meta.total` 133, so "whole list" holds for this response;
  fetched 2026-09-27T00:31:23Z. Commands match the shipped `operators` page. Reference endpoint,
  `NEWEST_VOUCHED`, one file overwritten (`generic.py:106-116,128-129,252-259,284`).
- **Guide facts.** `timestamp_utc` equals `publication_date_time` on 133/133; `Gas` rows carry
  `event_type`, `unit_measure`, capacities and `Planned`/`Unplanned` on 69/69, `Other` rows none of
  the capacity fields; technical = available + unavailable on all 69 `Gas` rows; `u_mm_type`
  Automatic 54, Feeds 44, null 35; `direction` blank on 31 `Gas` rows (all OGE); `balancing_zone_eic`
  present on 31 of the 76 null-key rows; `share_point_publication_id` begins with the sender EIC on
  89/89; every stamp in bronze carries a `+01:00`/`+02:00` offset; 15 `event_stop` values run to 2030
  or later; the sample rows are real (`gridflow-sample`) and tie to silver.
- **Six threads with no `Yes` version** (reproduced): Conexus `25063021X000000001379R006` (001 to 003
  all `No`), Conexus `25110321X000000001379R001` (001, 002), Fluxys Belgium `26062421X-BE-A-A0A0A-Y001`
  and `-Y002`, OGE `V0021586/1---------------`, NaTran DE `26032521X000000001008P001`. Two NaTran
  threads start at version 004. The flagged-latest version is always the highest served (0 exceptions).
- **Shared stamp.** 35 rows share `2026-09-27T02:28:56+02:00` (00:28:56 UTC), fetch at 00:31:23 UTC;
  all 35 have `u_mm_type` null (16 `Gas`, 19 `Other`); 44 rows null.
- **Build and detector.** `gridflow-build --only entsog/urgent_market_messages` succeeds and rewrites
  the HTML byte-identically. `detect.mjs --json` returns only `em-dash-overuse` (advisory, "49
  em-dashes", from `--` inside codes and CLI flags); real em dashes 0, en dashes 0, arrows 0, middle
  dots 0. Accepted under the ruling.
- **Mirror.** `cmp` canonical note against `vault/entsog/urgent_market_messages.md`: byte-equal.
- **Rendered page.** Headless Chrome at 1440, 1024, 768 and a true 390 px iframe: hero, chart, key,
  raw feed, folded frame, guide, notebook panel and related list all fully visible, nothing clipped
  or overlapping. Unfolded frame (opened in the browser pane, scrolled across all 39 columns) and the
  opened notebook (cells 1 to 6 and their outputs, including the plot image) render without error.
  The site has no dark theme. (One 1024 capture truncated after the frame header; a second capture
  of the same build was complete. A render-timing artefact, not the page.)
- **Local-data grep.** `locally`, `held`, `our `, `since 20`, `% of`, planning words: none on the
  page. The fetch date is on the page only as the capture the chart shows, which the rubric allows.
- **Related notes** are 8 to 10 words and the four pages resolve.

## Findings

### 1. major: `page.what_it_is`, `page.summary`, `page.raw_feed.note`, `page.how_used[1]`, `page.notebook`: the page never says what history silver can and cannot give, and "still serves" implies a withdrawal nobody observed

The page says "silver keeps only the newest fetch" once, in the last clause of `what_it_is`, and
"`transform` rewrites one silver file from the newest fetch" in `raw_feed.note`. It never says the
consequence: a message or version ENTSOG stops sending disappears from silver at the next transform
(bronze keeps it), silver cannot show what was visible on an earlier day, and `timestamp_utc` is the
message's publication stamp, not when gridflow saw it. Meanwhile `how_used[1]` ("Setting a flow drop
at a point against its operator's message") and a notebook that queries `2021-01-01` to `2026-09-30`
read as history uses. Silver can deliver "what ENTSOG sends today", not an event history or a
point-in-time view. Evidence: `endpoints.py:199-206` (`reference=True`), `generic.py:106-116,128-129,
252-259,284`; `silver/entsog/urgent_market_messages/` holds one parquet file; bronze holds one capture.
The consequence is stated only in the vault body (silver path paragraph), not on the page.

The same sentence, "ENTSOG returns the versions it still serves, some threads without their latest"
(and `summary`: "the versions ENTSOG still serves"), makes a present-tense claim about ENTSOG's
behaviour. "Still" says ENTSOG withdraws versions; the writer's own "could not verify" list says
whether the endpoint serves everything or a subset is unknown, and bronze holds one capture, so no
withdrawal was ever observed. What was observed: in the 27 September fetch, 6 of 101 threads have no
`Yes` version (reproduced above).

Fix: one plain sentence, for example "A message ENTSOG stops sending leaves silver at the next
transform, so silver is the list as last fetched, not a history; keep the bronze captures for that."
Drop "still" (summary: "with the versions ENTSOG sends"; `what_it_is`: scope the thread remark to
"in the fetch shown"). Tie `how_used[1]` to "messages ENTSOG currently sends".

### 2. major: `page.record.fields.unavailable_capacity` (and `available_capacity`, `technical_capacity`): placeholder and mis-scaled values are not stated

The page shows capacities and invites their use (`how_used[0]`), states mixed units
(`unit_measure ... never sum rows`, correct: `kWh/d` 61, `kWh/h` 8, null 64) but says nothing about
values that are not capacities. In the fetch: `unavailable_capacity` 1e10 kWh/d with 0 available on
four versions (`26032521X000000001008P001/P002`, VIP France - Germany); `unavailable_capacity` 1
kWh/d against 9.97e8 available on `25050221X-FR-A-A0A0A-S001` v004 and v005 (SPNS2U); RC Basel
`25090321X000000001163D001` v001 26.57 / 239.2 / 265.77 against v002 26,578 / 239,200 / 265,778
kWh/h (thousandfold); 10 `Gas` versions with all three capacities 0 (NaTran DE `26082121...`).
None is visible in the eight rows shown. Fix: a fetch-scoped warning on the capacity guide lines, no
counts needed, for example "Values are as sent: this fetch holds placeholders (such as 10000000000
or 1) and a version a thousand times too small, so check a value against its neighbours before use."
(The writer kept this off the page under the no-local-data rule; the page already makes fetch-scoped
statements, and the brief's own test is "stated if the page shows capacities".)

### 3. major: `page.record.fields.last_update_date_time`: "not an edit" asserts an unverified cause, and "several" understates

Text: "ENTSOG's update stamp; several rows here share one 27 September value, not an edit". ENTSOG
defines no UMM field (manual v2.1 lists only the path `/urgentMarketMessages`,
`scratchpad\entsog_api_manual.txt:192-194`), so nobody can say the shared value is not an edit; a bulk
touch of 35 records is exactly what a bulk edit looks like. The line also contradicts itself ("update
stamp ... not an edit"). Measured: 35 of 133 rows (five of the eight on the page) share
`2026-09-27 00:28:56 UTC`, 2 min 27 s before the 00:31:23 UTC fetch; all 35 have `u_mm_type` null;
44 rows are null. Fix, as an observation scoped to the fetch: "ENTSOG's update stamp as sent; in this
fetch many rows, five of these eight, share one value from 27 September, minutes before the fetch.
ENTSOG does not define it." Drop "not an edit".

### 4. nit: `page.notebook.plot_alt`, `page.notebook.cells[3]`: top bar is a thread whose latest version was not sent

The plot keeps OGE `Gas` messages whose highest version sent has `event_status == "Active"`, and the
alt says "15 active capacity messages ... highest version each". That is what silver holds, so the plot is
not wrong, but the top bar, "VIP Oberkappel, from 01 Oct 2025", is thread `V0021586/1---------------`:
version 001 only, flagged `is_latest_version = No`, one of the six threads without a `Yes`. Its three
sibling threads (`V0021584/1`, `V0021585/1`, `V0021587/1`, same asset, same start) each carry a version
002 that is `Dismissed`, so a reader will take this bar as in force when ENTSOG's own flag says a
later version exists. Reword `plot_alt` (and the cell comment if any) from "active" to "flagged
`Active` at the highest version sent". Do not filter on `is_latest_version == "Yes"`: the note's own
gotcha says that filter drops threads.

### 5. nit: `page.how_used[0]`: "cross-border point"

`what_it_is` says "point or facility", and the `Gas` messages' assets include storage connections
(`UGS-00355` Bierwang, `UGS-00357` Breitbrunn, `UGS-00416` Haiming 2 7F, `UGS-00476` Haiming 3),
the MND storage zone, `SPNS2U` and the virtual trading point THE-ZTP, not only interconnection
points (`ITP-*`: Kiemenai, VIP Oberkappel, VIP France - Germany, RC Lindau). Say "at a point or
facility".

### 6. nit: `page.how_used[1]` and `page.related[1]`: no direct key to flows

`physical_flows` silver carries `point_key` only (no EIC or asset name). The link runs through
`connection_points.point_eic_code`, and in this fetch 6 of 17 distinct `affected_asset_eic` values do
not resolve there (Emden EPT, Dornum, RC Basel, MND zone, SPNS2U, Värska). One short phrase on how to
join ("via the connection point register's EIC") would stop the bullet over-promising.

### 7. nit: `page.notebook.cells[0]`: hard-coded window

`query("urgent_market_messages", "2021-01-01", "2026-09-30")` filters on `timestamp_utc`
(publication). A reader who ingests after 30 September 2026 silently loses newer messages. A wide end
date (or `date.today()`) avoids it; the lead's "in the window" is correct as written.

### 8. nit: `page.record.caption`, `page.record.fields.u_mm_type`: the manual evidence is not in the note

"ENTSOG's manual defines no fields" is true of the v2.1 text (path listed at lines 192 to 194, no
UMM fields) but the vault body carries no line saying so. Add one body line citing the manual, as the
`hasData` gotcha does elsewhere in this vault.

### 9. nit: vault body, `Gotchas` bullets (ADDED/CORRECTED 2026-10-07)

- "one 65 days later": two `Automatic` rows are about 65 days after publication (93,820.7 and
  93,821.4 minutes, `26032521X000000001008P002` and `P001`).
- "three minutes before the 00:31:23 UTC fetch": 2 min 27 s.
- "RC Basel 265.77 kWh/h, corrected to 265,778": 265.77 is `technical_capacity`; the unavailable
  figures are 26.57 and 26,578. Say which column.

### 10. nit: `page.record.fields.message_id`

The column is called `message_id` but identifies a version (`thread_id` plus `version_number`), the
page's own distinction. Say "one per version" so the name does not undo the grain line.

## Not findings (checked, fine)

- Defects section is pasteable and accurate except the capacity/column ambiguity in finding 10.
- The chart label `Open Grid Europe` is right (silver has both `Open Grid Europe` and
  `Open Grid Europe GmbH` under one key; the guide's "it can change under one key" covers it).
- The `NaTran DE` note ("an older message names it GRTgaz Deutschland, under the same key") is
  true: one `Other` message, 2024-04-29.
- Em-dash advisory accepted.
