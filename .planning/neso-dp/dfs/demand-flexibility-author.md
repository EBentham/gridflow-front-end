# Demand Flexibility Service page: writer's report

Writer, 2026-10-18. Page `neso_data_portal/demand-flexibility` (family, lead `demand_flexibility_utilisation_summary`).

## Status

- **Build:** `gridflow-build --only neso_data_portal/demand_flexibility_utilisation_summary` passes (no errors). The
  only warning is the pre-existing caveat-grammar note about the legacy "Known issues and gotchas" body section,
  which the new template does not render.
- **Detector:** `detect.mjs --json` on `demand-flexibility.html` returns `[]`.
- **Mirror:** canonical note copied byte for byte to `vault/neso_data_portal/demand-flexibility.md`; `cmp` clean after
  every edit. The note is all CRLF (checked: 663 lines, no bare LF).
- **Recommendation:** ship with the loss stated (seat ruling "ship or hold"). The chart and the eight rows come from the
  2026-10-06 summary file, which silver loaded cleanly, and `what_it_is` states the loss: the newest NESO summary file
  fails to load. **Caveat for the seat:** until gridflow's summary key gains `event_id`, a reader who ingests today gets
  a failed summary capture and an empty summary view, so the demo notebook cannot be reproduced from a fresh install.
  If that is unacceptable, hold until the key fix (Defects 1).

## Files written (mine only)

- Canonical note: `C:\gridflow-wt\vault-dfs\30-vendors\neso-data-portal\datasets\demand-flexibility.md` (`page:` block
  plus four small body corrections, listed below).
- Mirror: `<fe-neso>\vault\neso_data_portal\demand-flexibility.md`.
- Artefacts under the lead key: `site/hifi/data/series/neso_data_portal/demand_flexibility_utilisation_summary.json`
  (spec_origin vault, 3 series x 321 points), `site/hifi/data/samples/neso_data_portal/demand_flexibility_utilisation_summary.json`
  (generated_by gridflow-sample, 8 rows x 23 columns), `site/hifi/data/notebooks/neso_data_portal/demand_flexibility_utilisation_summary.json`
  and `-5.png` (scripts/run_notebooks.py, 5 cells, no errors).
- Built page: `site/hifi/data-sources/neso_data_portal/demand-flexibility.html` and the four member pointer pages,
  each landing on its `#<table key>` anchor (checked).
- No staged chart spec or authored override existed for the lead key.

## The page in one paragraph

Title "Demand Flexibility Service". Chart: accepted DFS cost in £ per delivery date, summed over each day's windows
(Live and Test), 29 November 2024 to 6 October 2026, split into three series: archive-file rows (no event type),
Downwards events and Upwards events. Rows: four windows (16:00, 16:30, 18:00, 18:30) of 27 March 2026 (archive file,
settled values present) and of 24 June 2026 (event 56, two negative settled values). Notebook: summary and report for
11 September 2026 (event 119), joined per window: summary MW equals the Accepted bids in every window, with the
Rejected bid volume beside it, then a stacked bar plot. The requirement table is listed with its current file and one
line: "Rows not shown: NESO does not say when each requirement was first published"; it has no chart, sample or notebook.

## Evidence table

| Claim on the page | Evidence |
|---|---|
| Summary key `resource_id, delivery_date, window_from, service_requirement_type`; report adds `dfs_unit_id` | registry `connectors/neso_data_portal/registry/demand-flexibility.json` `entity_key` per family |
| One row of the summary = one window and requirement type; report = one bid of one DFS unit | registry keys above; NESO field-info: report `Status` "Accepted or Rejected", `DFS Unit ID` (`.planning/research/neso-snapshots/field-info/20261008T114228Z/demand_flexibility_utilisation_report.json`) |
| `window_from` is NESO's `HH:MM` label in UK local time, kept as text | registry: epoch 2 `From_Local` -> `window_from` dtype string; field-info "DFS service window start time in local time"; archive summary dictionary says local (note body) |
| `window_from_utc` / `window_to_utc` are NESO's UTC labels, null in archive rows | registry epoch 2 `From_UTC`/`To_UTC`; silver: null on all 1,130 archive rows |
| `timestamp_utc` is the start of the delivery date's first settlement period, not the window start | `silver/neso_data_portal/casting.py` `_with_timestamp_utc`: `date_sp1` -> `settlement_period_to_utc(date, 1)` |
| `published_at` is NESO's last-modified time for the whole file, read as UTC | `casting.py` stamps `ctx.published_at`; `completion.py` `vintage == "ckan_last_modified"`; `_bronze.py` `_parse_ckan_timestamp` (naive CKAN stamp read as UTC) |
| `bronze_capture_id` = path of the bronze capture; `capture_written_at` = when gridflow wrote it | `casting.py` lines ~573-574; `completion.py` `CaptureContext` docstring (`capture_id`: data-root-relative path; `capture_written_at`: sidecar `written_at`, UTC) |
| `resource_id` = CKAN id of the file (archive or current) | `casting.py` stamps `ctx.resource_id` when `latest_partition == "resource_id"` |
| `dfs_procured_mw` = total accepted volume, MW | NESO field-info summary: "Total volume of DFS accepted for service window", unit MW |
| ... equals the report's Accepted bids summed (checked) | Polars: every one of 1,230 current summary windows equals the sum of Accepted report MW for the same date, window and type, in both report captures (published 2026-10-06 and 2026-10-16); 0 mismatches over 0.05 MW. Also visible in the notebook output (summary_mw = accepted_mw in all 8 windows) |
| Cost is indicative, £; = accepted MW x price x half an hour (checked) | field-info: "Indicative total cost of accepted DFS bids for service window", unit £; Polars: sum(MW x `utilisation_price_gbp_per_mwh` x 0.5) of Accepted bids matches every current window within £0.005 |
| A Rejected bid's `dfs_procured_mw` is volume offered, not bought | Rejected rows have `dfs_procured_mw` >= 0.1 in both captures (3,890 and 4,378 rows); field-info "DFS volume procured for service window" plus `Status`; notebook shows 34.0 to 73.6 MW rejected per window |
| Settled volume and cost: delivered, once settlement data is received; can be negative; null until then | field-info: "visible once settlement data is received"; sample rows show -13.01 MW / -771.03 £ (2026-06-24 16:00) and -10.22 / -589.08 |
| `event_type` Upwards or Downwards flexibility, not defined further | field-info: "Indicate type of event (Upwards Flexibility or Downwards Flexibility)", no more |
| `event_tag` Energy or System | field-info: "Indicate if event is system or energy tagged" |
| `service_requirement_type` Live or Test | field-info: "Indicating a Live or Test DFS service requirement" |
| Summary has both seasons; archive rows null event columns | silver: archive resource `25698259-...` 1,130 rows, delivery 2024-11-29 to 2026-03-27, `event_id` null; current `705e573c-...` 1,230 rows, 2026-04-14 to 2026-10-06 |
| History fact (archive 29 Nov 2024 to 27 Mar 2026, current from 14 Apr 2026) | vendor files' delivery-date spans; also visible in the chart (first and last points of each series) and in the note body |
| Report: current season only; archive file repeats rows | silver report has no archive rows (`dfs_volume_mw` null on all 30,916); failure record `state/neso_data_portal/completion_failures/demand_flexibility_utilisation_report/2f29967450ce115549457243248dbcc6.json` (DuplicateEntityKeyError, 8 rows) |
| Notification: notices a requirement was published; archive only; no event id | silver: `notification_type` "Requirement Published" (190) / "Revised Requirement Published" (1); one resource `3d042450-...`; schema has no event column |
| Requirement rows not shown: no publication time | registry `eligibility.status: held`, question REQUIREMENT-ISSUE-AVAILABILITY; field-info `DFS Submission Time_Local` = "DFS auction close time" |
| Silver's summary key omits `event_id`, so a file with two events in one window fails to load | failure record `state/neso_data_portal/completion_failures/demand_flexibility_utilisation_summary/ce9d3de8bdfd69f558b7bb6cf4db8b61.json` (88 rows share the key); bronze 2026-10-16 file: events 151/152, 154/155, 157/158, 160/161, 162/163 share windows on 12 to 16 Oct 2026; 0 fully identical rows |
| Raw feed: one `package_show`, then each table's files downloaded whole, skipped when `last_modified` is unchanged; dates select nothing | `client.py` `iter_members` (one `_package_show`, per-member skip when the newest capture's `ckan_last_modified` equals the live one); `fetch` docstring "The window is not a selector (D-16)" |
| Member requests are the CKAN redirector URLs | bronze sidecars `request_url` for each resource, e.g. `.../resource/705e573c-.../download/dfs-utilisation-report-summary.csv` |
| Commands: `gridflow ingest/transform neso_data_portal <key> --last 24h`; window must end recently | `cli.py` passes the dataset key through `runner.resolve_datasets`; `client.py` `_assert_window_admissible` refuses an end more than 48 h old; config lists the four family keys in `config/sources.yaml` lines 856-859 |
| Notebook lead: `_latest` view, newest loaded capture per `resource_id`, filtered on `delivery_date`, both ends included, lineage dropped | gridflow_models probe: date column `delivery_date`, relation `silver_neso_data_portal_demand_flexibility_utilisation_summary_latest`; `_BITEMPORAL_EXCLUDE` = event_time, available_at, vintage_policy, source_run_id, dataset_version; `silver/latest_views.py` whole_capture = every row of the newest COMPLETE capture |
| Chart numbers (alt and key notes) | committed series: archive max £200,159 (2025-01-08), £197,660 (2025-01-22), monthly max after Jan 2025 £53,789; downwards max £139,293.06 (2026-06-24), £93,908.64 (2026-09-22); upwards £27,372.62 (2026-08-30, Test), £31.50 (2026-09-13, Test), Live max £10.00 (2026-05-24) |
| Plot alt numbers | notebook output: accepted 127.5 / 127.3 MW at 19:00 / 19:30, at most 2.4 elsewhere; rejected 34.0 to 73.6 MW |
| Cadence "Ad hoc" | note body: vendor metadata "Update frequency: Ad hoc" |

## Body corrections in the canonical note

Smallest spans only; all four concern the 2026-10-16 captures, which the note (written at the 2026-10-08 activation)
does not know about.

1. Files by disposition: "Every resource has exactly one observed capture (2026-10-08), so same-resource amendments
   cannot be measured yet" -> "At activation every resource had exactly one observed capture (2026-10-08). The current
   report, summary and requirement files were captured again on 2026-10-16 and only the report's second capture
   loaded; the summary and requirement captures failed (recorded under each family)." Evidence: bronze sidecars dated
   2026/10/16 for resources `3ebf77d7`, `705e573c`, `3635fd80`; silver report run `drain-e80c1052...`; the two failure records.
2. Summary Identity: added the recorded failure of the 2026-10-16 capture (88 rows share the key; events 151/152 to
   162/163 on 12 to 16 October 2026; the `_latest` view keeps the 2026-10-06 file). Evidence: failure record
   `ce9d3de8...json`; Polars on the bronze CSV.
3. Requirement Identity: added the 2026-10-16 parse failure (six rows give `Delivery Date` as `16-10-2026` against
   `%d/%m/%Y`). Evidence: failure record `4f251541...json`.
4. Cadence: "gridflow has one capture per resource (all on 2026-10-08)" -> "gridflow had one capture per resource at
   activation (all on 2026-10-08; the current files again on 2026-10-16)".

No other body text changed. The body's local row counts are vault material and are not on the page.

## Not verified

- Whether "Upwards" and "Downwards" mean demand turn-up and turn-down: NESO's dictionary does not say, so the page says
  the file does not define the direction.
- What a negative settled value means (vault TODO SIGNED-SETTLEMENT-SEMANTICS); the page says only that it can be negative.
- `--last 24h` for `transform` follows the approved `historic_generation_mix` page; I did not trace the transform's
  partition window for registry families line by line.
- Whether the archive summary's `From`/`To` labels are local (summary dictionary) or GMT (requirement dictionary): the
  guide line says UK local per the summary dictionary; on the archive rows shown (27 March 2026, before the clock
  change) local and UTC agree anyway.

## Open questions for the seat

1. Ship with the loss stated, or hold until gridflow's summary key includes `event_id`? (Recommendation above: ship;
   the notebook is not reproducible from a fresh ingest until the fix.)
2. The batch file's fact about event 141 is slightly off: in the summary it has **eight** windows, 17:00 to 21:00 local
   (16:00 to 20:00 UTC), not six to 20:00; the extra two accepted 8.8 and 10.3 MW. The page does not use event 141.
3. The member wells show only the current file for the summary, report and requirement (see template problem 1);
   the raw-feed note says "archive and current". Is one URL per member acceptable, or should the template list both?

## Template problems (not worked around)

1. **One raw URL per family member.** `page.family.members[].request` is one string, and `request_lines` /
   `_url_row` handle one URL (a second line would bypass the URL wrapping, since `_url_row`'s regex does not cross a
   newline). Package tables with two files (current and archive) can show only one, so the requirement member is
   "listed with" its current file only, not both raw files as Bobbo's ruling says.
2. **Long table keys overflow at 390 px.** The variant heading `<p class="ds-variants__h"><code>{{ m.key }}</code>`
   does not use the `breakable` filter (the hero chips do), so `neso_data_portal/demand_flexibility_utilisation_summary`
   and the other three keys are cut at the right edge of the raw-feed column at 390. The command well keeps each
   argument whole (`.ds-well .nw { white-space: nowrap }`, `command_row`), so the 38-character key in `gridflow ingest
   neso_data_portal demand_flexibility_utilisation_summary --last 24h` is cut at "summar" at 390. Fine at 768 and up.
   Suggested fix: `| breakable` on `m.key`, and a `<wbr>` after underscores inside long `.nw` tokens.
3. Minor, not clipping: the column guide breaks `dfs_provider_bids_accepted_total_cost_gbp` mid-name at 1440
   (`..._total_c` / `ost_gbp`); the notebook's call cell breaks a long string mid-word at 390; the notebook's df output
   scrolls sideways inside its panel at 390; the unfolded silver frame runs past the box edge at 1440 (open state).
   These are the template's existing behaviours.
4. The site has no dark colour scheme (no `prefers-color-scheme` in `tokens.css` or `theme.css`), so "light and dark"
   is one render.

## Screenshots

Headless Chrome over `file://` (no server started), profile `scratchpad/chrome-dfs-9911`, every call under
`timeout 60` with `--timeout=15000 --virtual-time-budget=5000`. 390 through a 390 px iframe wrapper. Closed state and
an opened state (demo notebook open, frame unfolded via the wrapper clicking `.ds-open` and `#fx`) at 1440, 1024, 768
and 390: `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\a46469c2-19b0-4f57-b2d5-81c7c1abca22\scratchpad\dfs-shots\`
(`light-<w>.png`, `open-<w>.png`, sliced as `s-*.png`). Nothing of mine is clipped after fixing the chart caption
(the full silver path overflowed at 390; it now names the table only). Remaining clipping at 390 is template problem 2.

## Defects

Pasteable for the gridflow BACKLOG and the vault remediation page.

1. **DFS summary key cannot hold two events in one window (summary capture of 2026-10-16 failed).**
   `demand_flexibility_utilisation_summary` entity key is `resource_id, delivery_date, window_from,
   service_requirement_type`. From delivery date 12 October 2026 NESO's current summary file runs an Upwards and a
   Downwards event in the same windows (event pairs 151/152, 154/155, 157/158, 160/161, 162/163; 88 rows share a key;
   no row is a full duplicate). The 2026-10-16 capture (`bronze/neso_data_portal/demand_flexibility_utilisation_summary/2026/10/16/raw_20261016T200207Z_705e573c-ddac-4675-b410-82916b35c4fe_5e57a28e.csv`)
   failed `DuplicateEntityKeyError` (failure record `state/neso_data_portal/completion_failures/demand_flexibility_utilisation_summary/ce9d3de8bdfd69f558b7bb6cf4db8b61.json`),
   so `_latest` stays on the 2026-10-06 file and every later NESO summary will fail the same way. A fresh install
   gets no summary rows at all. Likely fix: add `event_id` to the summary key (and check the requirement key, which
   has the same shape; the report key already includes `dfs_unit_id` and loaded). Registry change plus re-transform.
2. **DFS requirement capture of 2026-10-16 failed on a date format change.** Six rows of the current requirement file
   give `Delivery Date` as `16-10-2026` (dd-mm-yyyy) against the registry format `%d/%m/%Y`
   (failure record `state/neso_data_portal/completion_failures/demand_flexibility_service_requirement/4f251541bc6cd8d5480886eb1ce1dccb.json`).
   The family is held, so nothing is published, but silver is stuck on the 2026-10-08 capture. Vendor format drift:
   accept both formats or raise with NESO.
3. **Known, unchanged: archive utilisation report repeats four whole rows** (AXLE-01 and AXLE-03, 2025-01-05 16:00
   and 16:30, all Rejected), so the archive capture fails its key guard and the report has no 2024-11-29 to 2026-03-27
   rows (ADR-040, RULINGS 804). Recorded here only because the page states it.

## Revision 1 (2026-10-18, after the checker's review)

1. **Seasons (major).** Every "(checked)" is gone. The summary member line now reads "Window totals for both seasons;
   current-season MW and cost sum the report's Accepted bids". The two guide lines are scoped to current windows:
   `dfs_procured_mw` "Total accepted MW; in current windows, the report's Accepted bids summed: never add both" and the
   cost "Indicative accepted cost, £ (NESO); current windows: accepted MW × price × 0.5 h". I did not reproduce the
   bronze archive sums myself, so the page claims nothing about the archive report.
2. **The loss, as a fact (major).** `what_it_is` now ends: "NESO's newest summary file puts two events in one window,
   which silver's key (no `event_id`) cannot hold, so this page stops at the 6 October 2026 file" (60 words; the
   requirement clause was cut to fit). `notebook.needs` is "summary capture of 6 October 2026, and report; newer summary
   files fail", so it no longer suggests a fresh ingest reproduces the notebook.
3. **Raw-feed note (nit).** "(archive and current)" dropped: "each of the table's files downloaded whole".
4. **Zeros (nit).** Caption: "Days with no windows are absent; a day with nothing accepted is drawn at zero."
   `x_label`: "delivery date; days with no windows absent". The alt's "one point per event day" became "one point per
   day with windows", since archive days carry no event.
5. **History fact (nit).** "Archive 29 Nov 2024 to 27 Mar 2026; current file starts 14 Apr 2026" (14 words).

Checks: mirror `cmp` clean in the `fe-neso` worktree; note still all CRLF; `--only` build wrote the page with no new
warnings and no stale-artefact error (no artefact needed regenerating); `detect.mjs --json` returns `[]`; no em
dashes, "→" or middle dots in the page. build.py untouched. One slip, undone: I first copied the mirror into the main
checkout's `vault/` and deleted that stray file straight away; main's `git status` shows only the four untracked
`.planning/neso-dp/` folders it had before.

## Revision 2 (2026-10-18, after the second review)

- **Notebook line (major).** The template puts `notebook.needs` inside "with {needs} ingested", so Revision 1's value
  read as garbled copy and asked for a capture nobody can fetch. It is now the noun phrase "the summary and report
  tables for 11 September 2026", in the same form as other pages' values; the page renders "Needs gridflow and
  gridflow-models installed, with the summary and report tables for 11 September 2026 ingested." The loss stays stated
  once, in `what_it_is`.
- **Command lines cut at 390 px (nit).** Left alone, as the seat ruled.
- Checks: mirror `cmp` clean in `fe-neso`; note all CRLF; `--only` build wrote the page with only the old caveat-grammar
  warning; `detect.mjs --json` returns `[]`.
