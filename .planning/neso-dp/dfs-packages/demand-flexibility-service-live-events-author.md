# Writer report: `demand-flexibility-service-live-events` (DFS 2022/23 live events)

Writer, 2026-10-23. Lead `dfs_live_events_utilisation_report_sum`; members as the page set lists them (lead first:
summary, report, service update to industry, requirement). Manifest lead and members are right.

## Status

- `page:` block written on the canonical note (vault worktree `C:\gridflow-wt\vault-neso-dfs`, CRLF kept), mirrored
  byte for byte to `vault\neso_data_portal\demand-flexibility-service-live-events.md` (`cmp` clean).
- Artefacts under the lead key: `site\hifi\data\series\neso_data_portal\dfs_live_events_utilisation_report_sum.json`,
  `samples\...\dfs_live_events_utilisation_report_sum.json`, `notebooks\...\dfs_live_events_utilisation_report_sum.json`
  and `-5.png`. No staged spec or authored override existed.
- `gridflow-build --only neso_data_portal/dfs_live_events_utilisation_report_sum`: no errors. Detector: `[]`.
  Em dashes in page: 0. The build prints a general warning ("37 line(s) in 'Known issues and gotchas' sections could
  not be placed by the caveat grammar"), which is not tied to the template page.
- Screenshots at 1440, 1024, 768 and a true 390 iframe, light. The site defines no dark scheme (no
  `prefers-color-scheme` in `theme.css`/`tokens.css`), so there is no dark view to check. Server on 9872 started with a
  recorded PID (7045) and stopped by that PID.

## The four answers the launch asked for

1. **What one row is** (NESO field info `20261008T114228Z` and gridflow registry
   `connectors/neso_data_portal/registry/demand-flexibility-service-live-events.json`):
   - Summary (lead): one row per event window (`date`, `window_from`): requirement, D-1 procured MW and £, D0 procured
     MW and £, settled MW and £. Units from NESO's dictionary: MW and £.
   - Report: one row per bid of one DFS unit in one window (`date`, `window_from`, `unit`), `Accepted` or `Rejected`,
     price £/MWh, D-1 volume and 15 regional D-1 volumes (14 named plus Other) and Total, MW; 16 D0 counterparts, MW.
   - Service update to industry: one notice NESO posted, keyed (`date`, `time_label`, `type`); `date` is the posting
     date. No unit.
   - Requirement: one window NESO asked for (`delivery_date`, `window_from`), `dfs_required_mw` (MW: NESO's description
     "DFS volume required (MWs)"; the unit cell is blank).
   - Live only: the page never adds test rows. What NESO says about the split is quoted only as "a separate package"
     (package notes: "updates regarding the use of the live service (not test events)"). The related link to the test
     page says "published separately: never add them". No other test/live difference is claimed.
2. **Times and clock.** NESO labels every window GMT: the requirement header is `From GMT`/`To GMT`; the report and
   summary dictionaries give `From`/`To` the comment "GMT". All five windows are 23 and 24 January 2023, when GMT is UK
   clock time, so the page says "GMT labels, also UK clock time in January" (scoped to these rows). gridflow keeps the
   labels as text; `timestamp_utc`/`event_time` are the UK midnight of `date` (recipe `date_sp1`), 00:00Z here.
   `published_at` is CKAN `last_modified` read as UTC (requirement 2023-01-23T14:59:08Z, notifications
   2023-03-07T14:29:05Z, report 2026-07-27T14:01:36Z, summary 2026-07-27T13:22:45Z). The D0 forecast time is NESO's:
   "on day of event 10:00GMT". Notebook: `query()` returns the session zone (Europe/London); cell 1 converts
   `published_at` to UTC (July, so it matters: BST).
3. **Captures, truncation, repeats.** One bronze capture and one silver file per member, all 2026-10-08; no 16 October
   recapture exists for this package (frozen, `last_modified` unchanged). Rows: requirement 5, notifications 7, report
   170, summary 5; each body is one page (`total_pages: 1`), byte size equals the declared length, row counts equal
   K-DFS-FACTS. No repeated keys. `dedup: {on: [date, window_from, unit], order_by: published_at}` is set on the chart
   and frame as a guard (drops 0).
4. **Related:** `neso_data_portal/demand-flexibility` (showcase), `neso_data_portal/demand-flexibility-service`
   (2023/24), `neso_data_portal/demand-flexibility-service-test-events` (2022/23 tests), plus `elexon/system_prices`.

## Chart decision

The lead summary has five rows on two dates, and the chart's time axis would collapse each date's windows onto its
midnight anchor. A `bar` on the summary can't keep date and window apart either (one category column). The honest
reading at this size is within one window: a bar of the **D-1 volume of Accepted bids per provider, 17:30 to 18:00 GMT
on 23 January 2023** (report member, `sum` of `dfs_volume`, 19 providers). MW of different units in the same
half-hour add: NESO's own summary `dfs_procured` for the window (336.89) is that sum to two decimals. The per-window
reading of the summary (requirement, D-1, D0, settled for all five windows) is in the notebook's grouped bar plot.
Provider labels use a `group_map` to short names because NESO's run-together names (`DraxEnergySolutionsLimited`)
were clipped at 390; the caption says so and the frame keeps NESO's spellings.

The frame reads the report (`record.select.silver`), since the lead has five rows and `gridflow-sample` needs eight:
eight bids of the same window, including the Rejected `DRAX-04` (null D0, zero volume), Octopus's three units (D0
well below D-1), Oaktree and Orange Power (D0 zero) and EDF at £6,000/MWh. Precedent:
`phase-2-ffr-auction-results-summary`.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Windows are GMT labels (`what_it_is`, `window_from`, `window_to`) | Registry header `From GMT`; field info report/summary `From`/`To` comment "GMT" |
| D0 at 10:00 GMT on the event day (`what_it_is`, `d0_total`) | Field info report D0 columns "on day of event 10:00GMT"; summary D0 "at 10:00 GMT" |
| D-1 volume, MW; price £/MWh; Total "for GSPs at D-1" (fields) | Field info report: `DFS Volume` "Submitted at D-1", unit MW; `Price` "per MWh", £/MWh; `Total` "Total volume submitted for GSPs at D-1" |
| `Accepted`/`Rejected` | Field info `Status` "either Accepted or Rejected" |
| Requirement in MW | Field info "DFS volume required (MWs)" |
| Cadence "Not Active; files last changed January 2023 to July 2026" | Catalogue snapshot extras `Update Frequency: Not Active`; resource `last_modified` 2023-01-23 to 2026-07-27 |
| History "23 and 24 January 2023: five half-hour windows" | Whole vendor files; all five summary rows shown in notebook output |
| Key `date, window_from, unit` | Registry `entity_key`; 170 distinct |
| `timestamp_utc` = UK midnight of `date` | Registry `temporal: date_sp1`; silver 2023-01-23T00:00Z |
| `published_at` = CKAN `last_modified` read as UTC | Silver vs sidecar `ckan_last_modified` (same digits, +00:00) |
| Chart values (191.029 ... 1.0; 19 providers) | Committed series, `rows_used` 33 |
| 336.89 = summary `dfs_procured` | Silver summary row 2023-01-23 17:30; series sum 336.8888 |
| Plot alt numbers | Notebook cell 3 output (all five summary rows) |
| Requirement file changed before any window (`differs`) | `last_modified` 2023-01-23T14:59:08Z; first window 17:00 GMT that day |
| Notifications have no key to the others | Columns `date`, `status`, `type`, `time_label` only |
| `query()` relation, date column, drops | `gridflow_models` manifest: `_latest` views, `date` (requirement `delivery_date`), DATE BETWEEN inclusive, excludes `event_time`, `available_at`, `source_run_id`, `dataset_version` |
| Ingest commands, `--last 24h` | `client.py` upload member re-downloaded only when `last_modified` changes; `_HISTORICAL_WINDOW_TOLERANCE` 48 h |

## Body corrections (note body)

- Two `TODO: verify` the D0 submission time: NESO's dictionary states it (10:00 GMT on the event day). Replaced the TODO
  with the dictionary quote and the field-info snapshot id, in the "Things a reader must know" bullet and the report's
  "D-1 and D0" paragraph. Nothing else in the body changed; every other body fact I relied on was reproduced from
  silver (5 Rejected rows all `DRAX-04`, zero volume, D0 blank; regional sums equal `total` in 130 of 170 rows, `total`
  equals `dfs_volume` in 140; the test package shares no delivery date, and its 22 January notice points readers to the
  live dataset).

## Unverified

- Why NESO re-saved the report and summary files on 27 July 2026 (unchanged question in the note's TODO list). The
  page states only the dates.
- The session-zone claim rests on the batch's checked fact; the converted output shows `+00:00`.

## Open questions

- None that block the page.

## Template problems

- In the column guide at 1024, the 38-character key `d0_north_wales_merseyside_and_cheshire` wraps mid-word inside its
  cell (not clipped).
- The `bar` type has one category column, so a table whose rows are told apart by date plus window (the summary)
  can't be charted per window without merging dates. A two-column category (or a `values` bar) would let the lead's
  own five windows be charted.
- A first headless capture at 1440 x 9000 rendered blank below the chart; at 1440 x 6600 the page is complete. A
  capture artefact, not a page fault.

## Defects

- None new in gridflow or the data. Known and already recorded on the note (non-holding): the summary's D0 and settled
  values can't be rebuilt from the report (D0 matches for 1 of 5 windows); regional columns sum to `total` in 130 of
  170 report rows; the report and summary files carry a 2026-07-27 `last_modified` for January 2023 data, so a
  point-in-time filter excludes them before that date.
