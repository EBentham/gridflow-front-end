# Embedded register: author report (writer, round 1)

Page `neso_data_portal/embedded-register`, one table `embedded_register` (eligible). Lead and member list in the
page set are right (`package_tables`: `embedded-register` -> `embedded_register`).

**Status:** `gridflow-build --only neso_data_portal/embedded_register` passes; detector `[]`; 0 em dashes in the
built page. Mirror `cmp` identical to the canonical note (CRLF throughout, 478 lines).

**Files (mine only):**
- Vault worktree: `C:\gridflow-wt\vault-neso-cr\30-vendors\neso-data-portal\datasets\embedded-register.md` (page
  block plus body corrections).
- Front-end worktree `C:\gridflow-wt\fe-neso-cr`: `vault\neso_data_portal\embedded-register.md` (mirror),
  `site\hifi\data\series\neso_data_portal\embedded_register.json`,
  `site\hifi\data\samples\neso_data_portal\embedded_register.json`,
  `site\hifi\data\notebooks\neso_data_portal\embedded_register.json` and `embedded_register-5.png`; built page
  `site\hifi\data-sources\neso_data_portal\embedded-register.html` (gitignored).

## What one row is

One project, or one stage of a staged project, in NESO's Embedded Register file: the project's name, the generator
(NESO's customer), the connection site (free text naming a substation or grid supply point, for example
`Glenfarclas GSP`, `BRORA 132/33KV GRID SUPPLY POINT SUBSTATION`), the host transmission owner, plant type, build
status, MW connected, MW contracted to connect or be removed, the cumulative contracted MW over stages, the date the
change is contracted from, the stage number and the Connections Reform Gate. There is **no DNO area column**; the
only location fields are `connection_site` (free text, no GSP id) and `host_to`.

Units: MW for the three capacity columns (dictionary `unit: MW`, field info 20261008T114228Z). `stage` and `gate`
are plain numbers typed `float64`. `mw_effective_from` is a calendar date, `%Y-%m-%d` in the body.

Dates, per NESO's dictionary:
- `mw_effective_from`: "Date on which Connection is contracted to be effective from"; comment: "will only include
  dates for future connections or increase/decreases to capacity, otherwise this field will be empty". In the
  rows it is a contracted date, not a forecast: 129 rows of the 16 October file are dated before that day (128 of
  them not `Built`), and `PRO-001297` has 40 MW contracted but no date.
- `published_at`: CKAN `last_modified` of the captured file, read as UTC (`ckan_last_modified` vintage);
  `available_at` = `coalesce(published_at, ...)` so equals it (checked in silver).
- `timestamp_utc` / `event_time`: the capture time (temporal recipe `none`, generic transformer `_date_column`
  returns `timestamp_utc`), so `query()` filters on capture time; the notebook uses `data.sql()`.

## Captures and repeats

| Capture (UTC) | NESO file | CKAN `last_modified` | Rows | Distinct `project_number` |
|---|---|---|---:|---:|
| 2026-10-08T10:36:47 | `embedded-register-05-october-2026.csv` | 2026-10-06T10:47:45 | 561 | 561 |
| 2026-10-16T20:18:02 | `embedded-register-16-october-2026.csv` | 2026-10-16T18:05:22 | 562 | 562 |

Same 14-column header, BOM and CRLF in both. 540 rows are identical in both captures, so silver repeats them.
The chart and the frame filter on `published_at` = the 16 October file and carry
`dedup: {on: [project_number], order_by: capture_written_at}` as a guard (0 duplicates dropped after the filter).
The notebook reads `_latest` (`whole_capture`), which returned the 16 October file's 562 rows.

## Chart

Bar, silver `embedded_register`, the 16 October 2026 file only: `mw_increase_decrease` (MW contracted to connect or
be removed) summed per grouped plant type, at any contracted date. Bars: storage 4,853.48; mixed technologies
2,019.86; onshore wind 1,881.78 (net of `PRO-000902`'s -5.5); solar PV 1,106.14; biomass and waste 138.80; gas and
thermal 106.16; hydro, tidal and wave 85.25; total 10,191.47 MW. All 25 plant-type strings mapped explicitly; every
`;` string goes to "mixed". Additivity: `mw_connected` and `mw_increase_decrease` are per-row increments; the
cumulative column is a running total over stages (see evidence) and is never summed.

## Evidence table

| Claim (page) | Evidence |
|---|---|
| NESO's words "a list of connected or contracted to connect embedded generation projects in Scotland" | catalogue snapshot 20261006T195819Z, package `notes` |
| Twice weekly, Tuesdays and Fridays | resource description in the same snapshot; extras `Update Frequency: Twice weekly` |
| 562 rows in the file of 16 October 2026 | bronze body 563 lines (header + 562); silver capture 562 rows |
| File of 16 October lists one `NGET` project | silver: `host_to` counts SHET 352, SPT 209, NGET 1 (`PRO-001297`, Grimsby) |
| Dictionary lists `SHET` or `SPT` | field info, `HOST TO` comment "SHET or SPT" |
| NESO does not define "embedded" | package notes and resource description carry no definition |
| `project_number` key; staged numbers get a dash and stage | registry `entity_key: [project_number]`; dictionary comment on Project Number; unique within each capture (561/561, 562/562) |
| `project_id` case sensitive, shared by stages, to be phased out | resource description ("phase out the use of Project IDs"); dictionary comment; frame rows `PRO-000815-1/-2` share one id |
| `mw_connected` 0 until built and connected | dictionary comment "Field will state 0MW until the project is built and connected" |
| `mw_increase_decrease`: contracted to connect or be removed; negative is a removal | dictionary description; the sign reading is ours, from arithmetic: `PRO-000902` 70.0 + (-5.5) = 64.5 cumulative. NESO does not state the sign. |
| Cumulative "across all Stages"; each stage adds earlier ones | dictionary description; both captures: cumulative = running sum of connected + change over stages 1..k, 31 staged rows, 0 mismatches at 0.01 MW (Polars `cum_sum().over("project_id", order_by="stage")`) |
| Gate null until countersigned | dictionary comment on Gate |
| `project_status`: NESO holds no authority | dictionary comment on Project Status |
| Plant types joined by `;` | 25 distinct strings, 13 contain `;` |
| Raw request URLs | sidecar `request_url` of the 16 Oct capture; `package_show?id=embedded-register` from `client.py` `_package_show` |
| Skipped while `last_modified` unchanged | `client.py` `iter_members`: upload member yields `unchanged` when `capture.ckan_last_modified == live_modified` |
| `--last 24h` commands | `client.py` `_assert_window_admissible`: window end within 48 h of now, span at most 7 days, partition = `end.date()`; same form as approved NESO register-type pages |
| Notebook relation and `_latest` | `silver_neso_data_portal_embedded_register_latest` ran; status sums equal the Polars check on the 16 Oct file |
| Related: TEC register shares the columns plus `Agreement Type` | registry headers of both packages |
| Related: embedded forecast is GB embedded wind and solar | that page's own note summary |

## Body corrections (canonical note)

1. Opening paragraph: added that the 16 October 2026 file carries one `NGET` row (`PRO-001297`), outside the
   dictionary's `SHET or SPT`.
2. "gridflow holds a single capture" -> two captures; one project joined, none left; leaving behaviour still
   `TODO: verify`.
3. "As of the query time ... one capture ... 561 rows ... not row-level values" -> two captures, 561 + 562 = 1,123
   silver rows, 540 repeated; the page now shows rows of the 16 October file.
4. Files table: added the 16 October capture row; the bronze scan paragraph is scoped to the 2026-10-08 capture and
   a sentence describes the second body (BOM, CRLF, 563 lines, name date equals `last_modified` date).
5. Identity: 562/562 in the second capture; `project_number` unique within a capture only; every
   `project_id`+`stage` pair kept its number across the two captures (the stage-gain case is still `TODO`).
6. Profile: header scoped to the 2026-10-08 capture, plus a paragraph of the 16 October file's differences and counts
   (status, Gate, blanks, 13 date changes, 10 Gate changes blank to 2, 4 status changes Scoping to Consents
   Approved).
7. Silver layout: one Parquet file per capture (two).
8. Gotcha 1: the running-total arithmetic is now checked in both captures (0 mismatches); the vendor statement
   stays `TODO`.
9. Gotcha 5: the undated non-built row and the 129 past dates in the 16 October file, against the dictionary
   comment.
10. Cadence: the unchanged-file skip resolved from code (`iter_members`); the two captures listed; the 9 and 13
    October updates remain unknown.
11. Holds paragraph: open items reworded to match.
12. `updated:` 2026-10-16 -> 2026-10-24.

## Not verified

- What NESO means by "embedded"; whether the `NGET` row is intended (NESO's text says Scotland).
- Whether NESO published files on 9 and 13 October 2026; gridflow has no capture between 8 and 16 October.
- That a negative `mw_increase_decrease` is a removal is our reading of the arithmetic, worded on the page as
  "removed when negative ... (NESO)": the checker may prefer it marked as ours. NESO says "connect or be removed".
- The cumulative arithmetic is observed, not a vendor rule; the page says "here each stage adds the earlier ones".

## Open questions

- Related links: the build allows four. I used TEC register, interconnector register, GSP boundaries and the
  embedded wind and solar forecast (table key `neso_data_portal/embedded_wind_solar_forecast`; the package slug
  `embedded-wind-and-solar-forecasts` fails the build as "no page"). The DNO licence area boundaries page is left out:
  the register has no DNO column, so the link would rest on inference. Swap it for the interconnector register if
  the seat prefers.
- The notebook plot charts contracted MW by year of `mw_effective_from`; the axis and alt say these are contracted
  dates and that past years still carry MW (not history).

## Template problems (seat items)

- The site has no dark theme (no `prefers-color-scheme` in any stylesheet), so the dark screenshots equal the light
  ones.
- At 390 px the `units` scenery label "battery storage" sits at x = 0 in the hero (shared drawing, not page content).
- At 390 px the notebook code panel wraps long lines with uneven hanging indents (template wrapping).
- The build prints "37 line(s) in 'Known issues and gotchas' sections could not be placed" on every `--only` run;
  it is not specific to this page.

Screenshots (light and dark at 1440, 1024, 768, and 390 through a 390 px iframe) are in
`C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\da30dd44-cdfe-4d81-8e01-4b4045e0ad6b\scratchpad\er-writer\`;
nothing clipped in the page's own content. Server on 9842 started with a recorded PID and stopped by that PID.

## Defects

- **NESO data: register outside its stated scope.** NESO's Embedded Register file of 16 October 2026
  (`embedded-register-16-october-2026.csv`, `last_modified` 2026-10-16T18:05:22) carries `PRO-001297` (Grimsby,
  `Grimsby West 132kV Substation`, `HOST TO` = `NGET`), although the package notes describe the register as projects
  "in Scotland" and the dictionary comment allows `SHET or SPT`. gridflow loads it as is (string column). Logged in
  the vault note body.
- **NESO data: `MW Effective From` against its own dictionary.** In the same file 129 rows carry a date before
  16 October 2026 (128 of them not `Built`, for example `PRO-000815-2` Scoping dated 2024-10-30), and `PRO-001297`
  has 40 MW contracted with the date blank; the dictionary comment says the field holds only dates for future
  connections or changes and is otherwise empty. Treat it as a contracted date, never as a forecast.
- **gridflow coverage question (not a code defect).** The registry refresh is `daily` and the vendor cadence is
  Tuesdays and Fridays, but bronze holds captures of 2026-10-08 and 2026-10-16 only; files NESO may have published on
  9 and 13 October were not captured. Unknown whether NESO published them; the register keeps no history, so a
  missed file is lost.
- **Vault (fixed in this branch):** the note body said one capture, 561 rows, and left the unchanged-file skip and
  the staged arithmetic as open; corrected with evidence above.
