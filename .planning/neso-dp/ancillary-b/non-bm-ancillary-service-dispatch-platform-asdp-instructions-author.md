# ASDP dispatch instructions: writer report (2026-10-18)

Page `non-bm-ancillary-service-dispatch-platform-asdp-instructions`, one table, lead `asdp_instructions`. The manifest's
lead and member are right.

| Gate | Result |
|---|---|
| `gridflow-build --only neso_data_portal/asdp_instructions` | ok (only the vault-wide "22 Known issues lines dropped" warning, which predates this work) |
| Detector | `[]` |
| Canonical note vs mirror | `cmp` clean; 564 lines, all CRLF |
| Rendered page | 0 em or en dashes, arrows or middle dots; none of live, now, yet, soon, pending, coming, planned, shipped, real-time, locally, held, ledger, TODO, "since 20", "% of" |
| Screenshots | `.planning\neso-dp\ancillary-b\asdp-instructions-shots\` at 1440, 1024, 768, and 390 in six 1,500 px slices through a 390 px iframe. Nothing clipped or overlapping. The site has no dark theme (no `prefers-color-scheme` or `data-theme` in `tokens.css`, `theme.css` or `site.js`), so light is the only mode |
| Server | my 9983 server is stopped; 9670 not touched |

Artefacts: `site\hifi\data\series\neso_data_portal\asdp_instructions.json` (`spec_origin: vault`, 2 series x 31 points,
1,027 rows used), `samples\neso_data_portal\asdp_instructions.json` (`gridflow-sample`, 8 rows, 20 columns),
`notebooks\neso_data_portal\asdp_instructions.json` and `-5.png` (`run_notebooks.py`, 5 cells, no errors). No staged
spec or authored override existed.

## Truncated captures (batch risk)

Not present here. Bronze has exactly one capture per resource (70 CSVs, all `2026/10/08`), so no later capture can have
fallen. Each body is also complete: for all 70, silver rows equal the bronze body's data lines (lines minus the header),
0 mismatches, and every body ends with a newline. `_latest` (whole capture per `resource_id`) is therefore all 74,137
rows. Nothing about this goes on the page.

## Chart choice

First draft: daily count by service over 1 January 2021 to 17 April 2026 (1,922 points). It rendered as a dark,
unreadable mass at every width and STOR could not be seen, so I narrowed it to **March 2022**, daily count by service
(stacked area, Fast Reserve below, STOR above). Both services show: Fast Reserve every day (5 to 57), STOR in bursts on
nine days (up to 108 on the 11th). The long view moved into the notebook as a per-year table.

Two spec details for the checker:

- **The filter `dispatch_date_time_stamp ge "2021-01-01"` is load-bearing.** `distil.py` `_scan` parses the `time_text`
  column with `strict=True` before any filter (`_time_from_text`, line 152; filters applied after at 283). The 2,724
  rows from 2020 write `YYYY-MM-DD HH:MM:SSZ`, which fail `%Y-%m-%dT%H:%M:%S`. A filter on another column is pushed down
  ahead of the parse, so those rows never reach it (tested: with the filter, 71,304 rows parse; without one that
  removes them, Polars raises on the 2020 values). Inside the March 2022 window it removes nothing: no March 2022 start
  has a 2021 or earlier dispatch stamp, and the rows it drops for a null stamp (the 109 cease-only rows) also have no
  start.
- **No clock is applied.** No `day` option, so `time_bucket: 1d` truncates the parsed text to its date as written. The
  x axis is "start date as written". 1,027 = the March 2022 file's 1,031 rows less its 4 rows with no start; the
  February file ends 2022-02-28T23:38 and the April file starts 2022-04-01T16:07, so no other file adds March rows.

## Evidence

| Claim (page field) | Evidence |
|---|---|
| Dispatch and cease instructions to Non-BM Fast Reserve, STOR and RDP (summary, `what_it_is`) | CKAN package notes quoted in the note's opening; `service_type` values `Non-BM Fast Reserve`, `Non-BM STOR`, `RDP_NEGATIVE` in silver |
| "NESO publishes an instruction once its provider confirms it" | vendor text "once instructions have been confirmed by Service Providers" (note, opening) |
| "70 datastore tables, one per month" | registry `resources` (70), all `url_type` `datastore` (note, Files by disposition) |
| Cadence: not active, moved to the Open Balancing Platform | vendor "Update Frequency: Not Active"; vendor migration text (note, overview and Cadence) |
| Grain: one row per instruction entry, numbered by `EntryID` | vendor dictionary "Sequential Number"; registry entity key `resource_id, entry_id`; key line comes from `record.key` |
| History: monthly files June 2020 to April 2026, none for September 2020 | catalogue resource names (note's table: Jun to Dec 2020 without Sep, then every month to Apr 2026) |
| "from November 2021, provider and asset" | registry epoch 2 header adds `PartyID`, `AssetID`, `Tendered`; the note dates epoch 2 to the November 2021 resource onward |
| Indicative price in £/MWh; MW "NESO's unit"; no sign | vendor field info table in the note (Units); `mw` "MWs dispatched", no sign convention stated |
| "Times are text with no zone marker" | registry dtype `string` for all four time columns; naive `T` spelling in every file from January 2021 |
| Caption: count, not MW, per start date as written, March 2022; rows with no start not counted; Fast Reserve every day, STOR in bursts | spec (`aggregation: count`, `time_bucket: 1d`, window 2022-03-01 to 2022-03-31); series: `fast` 31 of 31 days, `stor` 9 days |
| Alt: Fast Reserve 5 to 57, highest on the 3rd; STOR on the 1st and 8th to 17th, up to 108 on the 11th; total highest on the 8th at 133 | committed series: fast min 5 (6th, also 25th), max 57 (3rd); stor 1st 9, 8th 85, 9th 41, 10th 55, 11th 108, 12th 40, 13th 14, 15th 41, 17th 10; total 8th 48 + 85 = 133 |
| Key note "Nine days this month, up to 108 on the 11th" | same series |
| Raw requests | `endpoints.py` `build_dump_path` (`/datastore/dump/<id>`, line 275) on `api.neso.energy`; ids are June 2020 (first, epoch 1), November 2021 (first epoch 2) and April 2026 (last) |
| "kept only if its body changed", "re-checks it at most weekly" | `client.py` `_dump_member` (1874) hash suppression; `_FROZEN_CADENCE = timedelta(days=7)` (107), `_frozen_not_due` (2409); registry `refresh: frozen`. Same wording the checker accepted on the window-prices page |
| Commands `ingest` / `transform` with `--last 24h` | same CLI form as the approved part 1 and window-prices pages (`cli.py` ingest and transform take `--last`); temporal `none`, so silver partitions by capture date |
| Frame: 29 March 2026; five start between 01:00 and 01:59, an hour UK clocks skipped | rows 73430, 73433 (01:03), 73436, 73437 (01:08), 73441 (01:33); UK clocks went from 01:00 GMT to 02:00 BST on 29 March 2026 |
| Field `instruction_start_date_time`: "not UK local time here" | the same rows: in `EntryID` order the March 2026 file's starts and stamps run unbroken 00:37, 00:43, 01:03, 01:08, 01:33, 02:03 (entries 73421 to 73455), and 17 dispatch stamps fall in 01:00 to 01:59. Scoped to "here" (these rows) |
| Field `dispatch_date_time_stamp` / `cease_date_time_stamp` | vendor "Timestamp Dispatch is sent (publish time to NESO data portal)" and the cease equivalent (note, Units) |
| Field `indicative_price` "RDP: utilisation price" | vendor: for RDP, the DER unit's latest Utilisation Price for that day (note, Units) |
| Field `asset_id`, `party_id`, `tendered` "files to October 2021 lack it" | epoch 1 header (8 columns) covers June 2020 to October 2021 (note, Header epochs). Worded so as not to claim those are the only nulls (95 later Fast Reserve rows are also blank) |
| Field `party_id` "spaces kept" | silver values such as `"ABBEY POWER GENERATION "`, `"FIRST ENERGY(REDDITCH)  "`; note: provider-name padding kept |
| Field `tendered` "case as NESO writes it" | silver: `Non-tendered`, `Non-Tendered`, `Tendered` (note, Sentinels) |
| Field `timestamp_utc`, `published_at` | temporal `none` (capture time); `published_at` null on every row (note, Two clocks) |
| Notebook lead: `query()` would filter on `timestamp_utc`, the capture time | `get_silver_schema_manifest()` entry: relation `silver_neso_data_portal_asdp_instructions_latest`, `designated_date_col='timestamp_utc'` |
| Notebook outputs | per-year table (2020 to 2026: Fast Reserve 2,602 / 10,798 / 9,900 / 8,927 / 15,537 / 18,330 / 6,308; STOR 122 / 680 / 776 / 26 / 6 / 1 / 1; RDP 0 / 0 / 0 / 1 / 2 / 11 / 0); 2025 Fast Reserve starts by hour |
| `plot_alt`: fewest in hour 2 (372), most in hour 6 (1,318), 943 to 1,024 in hours 15 to 18 | Polars over silver: hours 2 = 372, 6 = 1,318, 15 = 943, 16 = 1,024, 17 = 1,009, 18 = 992 (sum 18,330, matching the table's 2025 Fast Reserve) |
| Related: window prices ("`EntryID` points here"), OBP reserve instructions ("never join ids"), STOR day-ahead auction results | vendor dictionary "EntryID from Instruction Dispatches" (window-prices note); note's own "never match `entry_id` to an OBP identifier"; note's Modelling notes list the STOR auction page. All three slugs are in the page set |

## Body corrections (canonical note, smallest spans)

1. **The raw time columns** (after the `ASDP-EXPORT-CLOCK` TODO): added the one measured check. On 29 March 2026, when
   UK clocks skip 01:00 to 01:59, the March 2026 body has 17 dispatch stamps in that hour and its times run unbroken
   through it in `EntryID` order (73427 to 73455), so that body is not UK local time (UTC or fixed GMT fit). The other
   five spring changes in the naive files have no row in that hour, so they test nothing. The TODO stays open.
2. **Identity and selection:** of the 510 missing `EntryID` numbers, 360 (19 to 378) fall between the last August 2020
   entry (18) and the first October 2020 entry (379), exactly where there is no September 2020 resource. The TODO
   stays open; this fits a month that had instructions but no published file, which NESO does not state.

## Unverified

- Whether the export clock is UTC in every file. Only the March 2026 file is tested (above). The page scopes the claim
  to the rows shown ("here") and keeps "no zone marker" elsewhere.
- What `RDP_NEGATIVE` MW means as a sign (the note's `ASDP-SIGN-CONVENTION`); the page says only "NESO states no sign"
  and "an RDP curtailment".
- The 4 rows with an `indicative_price` of exactly 0 (one is a January 2026 STOR row). They are inside the notebook's
  per-year mean, and the page says nothing about them.

## Open questions

- None blocking. A reviewer may prefer the chart window to be a recent month; March 2026 has Fast Reserve only, so the
  stacked view would lose STOR. I picked March 2022 so both services show.

## Template problems (seat items)

1. **`time_text` parses before filters, strictly.** A text time column in two spellings (here `...Z` in 2020 and naive
   `T` after) can be charted only if some filter on another column happens to be pushed down by Polars ahead of the
   parse. That works here, but it depends on query-plan behaviour. A non-strict parse, or applying `filter` before
   `time_text`, would make it robust.
2. **No bucket coarser than a day.** `time_bucket` is `30m`, `1h` or `1d`. A multi-year event log at one point per day
   (1,922 points here) draws as an unreadable mass. A `1w` or `1mo` bucket would let pages like this show their whole
   span.

## Defects

- **NESO: no September 2020 ASDP instructions file, but `EntryID` skips 360 numbers there.** Package
  `non-bm-ancillary-service-dispatch-platform-asdp-instructions`: `EntryID` runs to 18 in the August 2020 file and
  restarts at 379 in the October 2020 file; there is no September 2020 resource. This fits instructions that were sent
  but never published. Vendor data gap, nothing for gridflow to fix; recorded in the vault note's Identity paragraph.
- **ASDP export clock, evidence for the open question (not a defect):** the March 2026 body has times in 01:00 to 01:59
  on 29 March 2026, an hour UK clocks skipped, so that file is not UK local time. Recorded in the vault note under The
  raw time columns.
- **Front-end template (seat):** `distil.py` `_time_from_text` parses `time_text` with `strict=True` in the scan, before
  spec filters, so mixed text spellings need a filter that Polars pushes down ahead of the parse. Proposed fix: parse
  non-strictly, or apply filters first.
- **Front-end template (seat):** no weekly or monthly `time_bucket`, so multi-year daily event counts are unreadable.
