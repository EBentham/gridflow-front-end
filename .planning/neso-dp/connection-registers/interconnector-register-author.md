# Interconnector register: writer report (2026-10-24)

Page `neso_data_portal/interconnector-register`, one table `interconnector_register` (eligible). Full page: chart,
frame, notebook. Build `--only neso_data_portal/interconnector_register` clean; detector `[]`. Canonical note
`C:\gridflow-wt\vault-neso-cr\30-vendors\neso-data-portal\datasets\interconnector-register.md` (CRLF kept, no bare
LF); mirror `C:\gridflow-wt\fe-neso-cr\vault\neso_data_portal\interconnector-register.md`, `cmp` identical.

Files (mine only): the note and its mirror; `site/hifi/data/series/neso_data_portal/interconnector_register.json`,
`samples/neso_data_portal/interconnector_register.json`, `notebooks/neso_data_portal/interconnector_register.json`
and `-5.png`; the built page. No staged chart spec or authored override existed.

## Chart and window

Bar chart, `mw_import_total` (MW) summed by `project_status`, NESO's file of 16 October 2026 (filter `published_at`
>= 2026-10-16 and < 2026-10-17), Moyle's stage 1 row `PRO-001292-1` filtered out, `dedup` on `project_number` by
`published_at` as a guard. Series: Scoping 26,830; Built 10,791; Awaiting Consents 4,000; Construction 1,400
(34 rows used of 70 read, 0 duplicates dropped). `Under Construction/Commissioning` is mapped to the label
`Construction` because the long label clipped at 390 px; the key note says so.

## Evidence

| Claim | Evidence |
|---|---|
| Two captures, 35 rows each, same 35 `project_number`s, so every key repeats across captures | Polars over silver: captures with `published_at` 2026-10-06T10:47:52.001303 and 2026-10-16T18:06:23.602416, 35 rows and 35 unique keys each, 70 in all |
| Five rows differ between the files (gate filled on four, three effective dates moved); no MW, status or host TO change | anti-join of the two captures on all 15 vendor columns |
| One row is one project, or one stage of a staged project; key `project_number` within a capture | registry `interconnector-register.json` `entity_key: [project_number]`; field dictionary: a staged project number is "followed by a dash and the relevant stage number" |
| Import is power NESO accepts into the transmission system at the interconnector's connection site; export is power NESO transports to that site | package notes quoting CUSC 9.4 and 9.5 (catalogue snapshot 20261006T195819Z) |
| Total import is firm TEC; Moyle holds 500 MW TEC | package notes, same snapshot |
| MW for the six capacity columns; `mw_effective_from` is `yyyy-mm-dd`, no time of day | field dictionary `field-info/20261008T114228Z/interconnector_register.json` |
| Meanings of current, increase/decrease and total; 0 until built; effective date only for future connections or changes | field dictionary descriptions and comments |
| Status is "as far as we are aware"; Gate blank until countersigned, Gate 1 or 2 | field dictionary comments; package notes on Gate |
| Moyle stage rows overlap: stage 1 import 270 current + 205 = 475 total; stage 2 475 current + 25 = 500 total; export 500 on both | the two rows, both captures; 500 matches NESO's stated Moyle TEC |
| `current + increase_decrease = total` in all 35 rows, both captures, import and export | Polars check |
| Status sums (chart and notebook cell 4) | Polars and notebook agree: import 4,000 / 10,791 / 26,830 / 1,400; export 4,135 / 11,097 / 26,904 / 1,470; projects 3 / 11 / 19 / 1 |
| `published_at` is CKAN `last_modified` of the file, read as UTC; `timestamp_utc` and `capture_written_at` are the bronze write time | registry `vintage: ckan_last_modified`, `temporal: none`; silver values equal the sidecars' `ckan_last_modified` and `written_at` |
| gridflow downloads the upload file again only when CKAN `last_modified` differs from the newest capture's | gridflow `connectors/neso_data_portal/client.py` `iter_members`, upload-member skip (about lines 1748 to 1765) |
| Raw requests | `package_show` with `id=interconnector-register` (`client.py` `_package_show`); the download URL is the 16 October capture sidecar's `request_url` |
| Commands: `--last 24h` ingest and transform with the family key | the window is not a selector for portal captures (`client.py` fetch docstring, D-16); same form as the approved FFR page |
| `_latest` view returns the newest complete capture (16 October file, 35 rows) | `silver/latest_views.py` `whole_capture`; notebook cell 3 prints `published_at` 2026-10-16 19:06 UK time |
| Notebook uses `data.sql`: `query()` filters on capture time for a table with no event time | batch Checked facts; registry `temporal: none` |
| Plot values by contracted effective year (projects not built, Moyle stage 1 dropped) | notebook: 2027 1,400; 2028 750; 2029 4,400; 2030 6,600; 2031 1,900; 2032 6,380; 2033 1,800; 2034 0; 2035 3,600; 2036 1,000; 2037 4,400 |
| IFA 1,988 MW; BritNed written "Britned" | frame rows `PRO-000282`, `PRO-000280` |

Far-end countries: none named anywhere on the page (seat ruling). Project names are as NESO writes them.

## Body corrections (canonical note)

- `updated:` 2026-10-16 to 2026-10-24.
- The two clocks: "For the one capture so far" now gives both captures' `last_modified` and `timestamp_utc`.
- "stores a new capture only when the body changed" was wrong: corrected to a re-download only when CKAN
  `last_modified` changes (client.py `iter_members`); same fix in Cadence ("an unchanged body is not stored again").
- "One capture" wording in MW sign, Arithmetic, Duplicate-looking rows and Missing values now covers both captures;
  blank counts restated per file (`gate` blank in 29, then 25).
- Gate: "Observed values are 1 or blank" corrected to 1, 2 or blank (Gate 2 first on NeuConnect, 16 October file).
- Moyle stage TODO kept, with the evidence that the stage values read as cumulative (stage 2's total equals NESO's
  500 MW); NESO does not state the rule.
- New subsection "Second capture (checked 2026-10-24)" under the dated 2026-10-16 silver section: the second capture,
  70 rows with every key repeated, the five changed rows, and NeuConnect's effective date moving from 2026-08-01 to
  2027-07-07 (which supersedes the 2026-10-16 section's past-effective-date example for it).

## Unverified

- Whether a contracted reduction would show as a negative increase/decrease (none in either file).
- How and when NESO moves capacity from increase/decrease into current: Moyle's 2022 dates still carry 205 and 25 MW
  increases on Built rows.
- The full status vocabulary (NESO defines Scoping, Awaiting Consents, Consents Approved; the files also show Built
  and Under Construction/Commissioning).

## Open questions and template problems

- **Related links cap of 4:** the launch prompt lists nine related pages (seven interconnector packages plus the TEC
  and embedded registers); `RELATED_MAX = 4`. Chosen: TEC register, embedded register, `ifa` (largest built link in
  the file) and `brit-ned`. Not linked: `eleclink`, `ifa2`, `nemolink`, `nsl`, `viking`. Seat to rule if a different
  four is wanted.
- **Bar category labels clip at 390 px** instead of wrapping (`Under Construction/Commissioning` lost its left part).
  Worked around with a `group_map` label and a key note; a template fix would let NESO's own label stand.
- The site has no dark theme (no `prefers-color-scheme` rules), so screenshots are light only, at 1440, 1024, 768 and
  390 (390 through a 390 px iframe). Nothing clipped or overlapping. At 390 the frame folds after `project_number` and
  the notebook tab name truncates with an ellipsis: template behaviour.
- The manifest's lead and member list are right (one member, `interconnector_register`).

## Defects

- **NESO interconnector register: past effective dates still carry increases.** In both captured files (5 and 16
  October 2026) Moyle's stage rows `PRO-001292-1` and `-2` (status Built) carry `mw_effective_from` 2022-04-01 and
  2022-08-01 with `mw_import_increase_decrease` 205 and 25 MW, although NESO's dictionary says the date is filled
  only for future connections or changes. Vendor data quirk; gridflow keeps it as sent. Documented in the note.
- **NESO interconnector register: stage rows overlap.** NESO's package note warns staged capacity may produce
  duplicate entries; Moyle's two stage rows are cumulative, so summing `mw_import_total` over rows double counts Moyle
  (11,266 instead of 10,791 MW for Built). Vendor shape; consumers must drop stage 1 or keep the highest stage.
  Candidate for a gridflow gold helper or a documented caveat on the `_latest` view.
- **Vault note was stale on the capture rule** (said body change; code keys on CKAN `last_modified`). Fixed in this
  note on the vault branch; sibling register notes may carry the same sentence.
