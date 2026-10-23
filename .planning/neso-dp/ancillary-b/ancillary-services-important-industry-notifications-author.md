# Ancillary services industry notifications: author report

Family page `ancillary-services-important-industry-notifications`, lead `as_industry_notifications_balancing`. Writer,
2026-10-18.

## Status

- `gridflow-build --only neso_data_portal/as_industry_notifications_balancing`: success (the "22 lines in Known issues
  and gotchas" warning comes from other notes; this note has no such section).
- Detector on `site/hifi/data-sources/neso_data_portal/ancillary-services-important-industry-notifications.html`: `[]`.
  0 em or en dashes, middle dots or arrows in the built page. Copy grep: the only "live" is NESO's own notice text in
  the unfolded frame; "rows" hits are the template, the held line and the `service` field line.
- Canonical note (vault worktree) edited with Edit and a byte-safe CRLF script: 648 lines, 648 CR; diff +148 / -1
  (the `page:` block, `updated` 2026-10-13 to 2026-10-18, two Known-quirks bullets). Mirror copied, `cmp` equal.
- Artefacts: `site/hifi/data/series/neso_data_portal/as_industry_notifications_balancing.json` (spec_origin vault,
  bar, 5 categories, 28 rows used, silver `as_industry_notifications_dc_dm_dr`),
  `samples/.../as_industry_notifications_balancing.json` (gridflow-sample, 8 rows, silver
  `as_industry_notifications_balancing`), `notebooks/.../as_industry_notifications_balancing.json` and `-5.png`
  (run_notebooks.py, 3 cells after setup and help card, no errors). No staged spec or authored override existed.
- Screenshots 1440, 1024, 768 full page, 390 through a 390 px iframe in offset windows (scratchpad
  `asn-writer\shots\`): nothing clipped or overlapping after shortening two bar labels (below). No dark scheme on the
  site. Server on 9981 stopped.

## The page in one paragraph

Five text registers, one capture each (2026-10-08), so no truncation question. Chart: a bar count by `service` of the
DC/DM/DR member (the one file whose `service` varies), pinned to NESO's 19 August 2026 file by `published_at`:
`DC, DM, DR` 12, DM 11, DC 3, `DC, DM` 1, `DM, DR` 1; combined labels hatched, single services petrol; the caption says
it is one member and that a combined label is one value. Frame: the eight newest Balancing Reserve notices (26 March to
4 September 2026), pinned by `published_at`, showing the issue and effective times, the one effective-to, `BR`, notes,
and the newest row's issue label after the file's `published_at`. Notebook: queries all five eligible tables, concats
with a `file` column, lists issue minutes shared by several files (with a count of distinct texts), and draws a strip
plot of issue times per file. SFFR is listed with its file and one line on why its row is not shown.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Key `notification_issued_date_time`; no vendor id | registry `connectors/neso_data_portal/registry/ancillary-services-important-industry-notifications.json` `entity_key`; `K-AS-2-FACTS.md` §3 "No notification CSV has a notification-id column"; silver: 13/28/13/4/9 distinct issue times |
| Issue, effective-from, effective-to are UK local time; their meanings | NESO dictionary `.planning/research/neso-snapshots/field-info/20261008T114228Z/<family>.json`: comment "UK local time"; "The date and time of the notification", "...will become effective", "...is expected to become inactive" |
| Parsed `%d/%m/%Y %H:%M`, Europe/London, to UTC | registry epoch columns `format`, `zone`, `ambiguous: raise` |
| `timestamp_utc` = the issue time in UTC | registry `temporal: local_instant(notification_issued_date_time)`; silver: equal on all 13 balancing rows |
| `published_at` = file last-modified, read as UTC; can precede an issue time | registry `vintage: ckan_last_modified`; sidecar `ckan_last_modified` 2026-09-04T10:50:39.380805 equals silver; frame row 2026-09-04 11:00 UTC against `published_at` 10:50:39 UTC |
| Ad hoc cadence | package metadata "Update frequency: Ad hoc", quoted in the note body |
| History "from March 2024 in STOR and DC/DM/DR files" | vendor file content: STOR first issue 2024-03-01 10:00 UTC, DC/DM/DR 2024-03-11 10:00 UTC |
| One notice often posted to several files, sometimes reworded | Polars over the five tables: 67 rows, 43 distinct issue times; 17 in 2 to 4 files; description `n_unique` 2, 2 and 3 at 2024-03-28 14:00Z, 2026-03-26 14:45Z, 2026-08-07 14:35Z; notebook cell 4 output |
| Chart counts 12/11/3/1/1 | committed series; Polars `value_counts` on silver `service` |
| Key notes (DM: each raises the requirement; DC: two maintenance notices and one DCL raise; DM 300 and DR 480 MW from 3 Feb 2025 delivery; extra 100 MW DC and DM on 29 May 2026; combined label mostly delays, new columns, EAC outages, archiving) | full descriptions read from silver (scratch `asn-writer\full.py`, `read2.py`) |
| Requests | sidecar `request_url` of each 2026-10-08 capture; `package_show?id=` as on the approved NESO pages |
| `--last 24h`, whole file, unchanged skip | same commands as the approved Static FFR and DR pages (client.py window admissibility and `last_modified` skip, cited there) |
| `query()` reads `silver_neso_data_portal_<table>_latest`, filters `timestamp_utc` by half-open UTC days, end inclusive | gridflow_models `_validate_dataset_for_source` gives `timestamp_utc`; `_relation_name_for_dataset`; `_get_method_registry.py:62-96` `_date_range_predicate` (TIMESTAMPTZ) |
| "times come back in the machine's zone, UK here" | notebook output offsets `+01:00`/`+00:00`; `duckdb.connect()` `TimeZone` = Europe/London; gridflow_models never sets TimeZone (grep) |
| Plot alt (STOR ends April 2025, Slow Reserve from March 2026, ticks line up, most often DC/DM/DR with Quick Reserve) | silver issue times; 13 minutes shared by DC/DM/DR and Quick Reserve; committed PNG |
| SFFR held line | ledger row (SFFR-NOTIFICATION-DATE-ORDER); FACTS §4.4: one row `01/03/2024 10:00`, Notes "Example note", date order unresolved, placeholder question |
| Related: PBR and NBR on the Balancing Reserve requirement page | that page's approved block ("cleared `PBR` and `NBR` MW") |

## Body corrections (canonical note)

The body checked out against code and silver (row counts, ranges, blanks, the newest-row offsets such as 560.6 s).
Added two Known-quirks bullets, both measured on the 2026-10-08 captures:
- One notice, several files: 67 rows, 43 distinct issue labels, 17 shared, three reworded per service.
- Balancing Reserve notes sit one row off (raw CSV checked): the 2025-11-25 production-outage notice carries the
  sandbox note, the 2025-11-30 forecast-upload notice carries the production note, and the 2025-10-08 sandbox notice
  has none; DC/DM/DR and Quick Reserve put those notes on the sandbox and production notices.

## Lead choice

The lead is workable but not the strongest member. DC/DM/DR has the most rows (28) and the only `service` column with
more than one value, so the chart reads from it (`chart.silver`) and the caption says so. Balancing Reserve has clean
dates and a usable frame, so the frame stays on the lead. If the seat ever reorders the family, DC/DM/DR would carry
chart and frame from one table. No manifest change requested.

## Unverified

- Whether NESO appends, amends or removes notices: one capture per file.
- Whether effective-to is inclusive or exclusive, and whether a blank means open-ended (vendor silent); the page says
  only "expected to stop applying" and "blank cells kept null".
- Why the Balancing Reserve notes are offset (a data-entry slip is likely, not verified); not on the page.

## Open questions

1. The frame avoids the offset-notes rows. Should the `notes` field line warn about it? I left it off the page as an
   unexplained vendor quirk; it is in the vault body.

## Template problems (report only)

- Bar charts at 390 give category labels 110 px (`chart_svg.py` `_bars`, `label_w`), so "Dynamic Moderation" and
  "Dynamic Containment" were clipped at the left edge. I shortened the labels to "DM alone" and "DC alone" (full names
  in the key notes); the renderer does not wrap or shrink long labels.
- Known: the 390 frame shows only the key column until unfolded; the notebook tab name truncates at 390.

## Checker: look hardest at

- The chart reads a non-lead member (`chart.silver` = DC/DM/DR) while the frame and notebook use the lead; confirm the
  caption makes that plain.
- Key notes against the full descriptions (each summarises NESO's text).
- "can precede an issue time" (`published_at`) and the notebook lead's time-zone sentence.

## Defects

- **Vendor data, Balancing Reserve notifications file** (`13f8f6b1-690b-4695-993e-dbc26f9bbe54`, capture
  2026-10-08): the Notes of three notices appear shifted by one row against the same notices in the DC/DM/DR and
  Quick Reserve files (25 Nov 2025 production outage carries the sandbox note; 30 Nov 2025 forecast upload carries the
  production note; 8 Oct 2025 sandbox notice has none). Kept byte-equal in silver; recorded in the vault note's Known
  quirks. No gridflow change needed.
- **Template:** narrow bar charts clip category labels longer than about 16 characters at 390 px (110 px label
  column, no wrap).
- No gridflow code defect found.
