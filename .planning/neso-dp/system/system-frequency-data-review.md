# System frequency (`system-frequency-data`): checker's review

**Verdict: REVISE.** 0 blockers, 2 majors, 7 nits. Every number on the chart, the clock claims, the member requests and
the held line reproduce from silver, bronze, gridflow code and NESO's catalogue text. The two majors are wording that
misleads a reader (a count that contradicts the list under it, and a sample frame that never says which table it is).
Both are one-line fixes.

Checked: build `--only neso_data_portal/system_frequency` runs clean (one unrelated warning about 35 dropped lines in the
note's "Known issues" sections); detector `[]`; mirror `cmp` clean; note CRLF 893/893; spec digest passes
(`spec_origin: vault`, no staged spec). Page text has no em or en dashes, arrows, middle dots, "live", "now", planning
words or local-data wording. Screenshots taken at 1440, 1024, 768 and a 390 px iframe (my server on 9891, PID found
from the listening port and stopped): nothing clipped or overlapping; hero, chart, folded and unfolded frame,
notebook panel (all six cells and the plot) and related list all read. At 390 the member headings and chips break
mid-word but fit. The site has no dark theme.

## What I reproduced (all lazy Polars, selected columns)

| Claim | Result |
|---|---|
| Chart window 13:00:00 to 13:29:59 UTC, 22 Dec 2023, `system_frequency_gmt_csv` | 1,800 rows, 1,800 distinct `dtm`, no nulls, one resource, one `published_at` (2026-04-17 09:30:07) |
| Low 49.275 Hz at 13:10:11 | Exact (also the committed series) |
| Below 49.5 Hz for 60 seconds, 13:10:03 to 13:11:02 | Exact, contiguous (13:10:03 = 49.498, 13:11:02 = 49.494, 13:11:03 = 49.510) |
| Alt text: 49.878 to 50.042 Hz to 13:09:51; 50 Hz again at 13:21:09; peak 50.134 at 13:26:07 | All exact. The two steps are real: 49.880 at 13:09:51, a shelf near 49.65 to 13:09:59, then 49.30 by 13:10:07 |
| Offset shape is UK clock time with its offset | All 157,766,400 bronze rows of 2015 to 2019 (48 CSVs, 12 ZIPs): offsets are only `+0000` or `+0100`, `+0100` exactly between the last-Sunday 01:00 UTC changes in every year, and the converted UTC seconds step by exactly 1 s throughout |
| GMT shape does not follow the UK clock | `fnew-2023-3.csv` carries every second through 26 March 2023 (the frame shows 00:59:59, 01:00:00, 01:59:59, 02:00:00); NESO's package notes say "Time values are all given in Greenwich Mean Time (GMT) starting January 2020" |
| Held 2014 table | Bronze `f-2014-10.csv` repeats `26/10/2014 01:00:00` to `01:59:59` (3,600 labels twice, 7,200 rows). NESO's resource descriptions say `YYYY-MM-DD` and name no zone |
| `timestamp_utc` equals `dtm`, and `event_time` equals `dtm` | 0 differences in all four typed silver tables (139.4M, 70.9M, 126.2M, 31.5M rows) |
| Request URLs | All ten first and last member URLs appear verbatim as `request_url` in the bronze sidecars; month ranges and ZIP/CSV split match (12 / 48 / 12 / 27 / 53 files) |
| Raw-feed note | `iter_members` (`client.py:1658-1790`): one `package_show`, then each member downloaded unless its `last_modified` matches the newest capture; the window is only checked for admissibility, so "dates select nothing" holds |
| Transform commands | `generic.py:250-340`: a typed family reads its own bronze and the sibling's bronze for the date partition and takes only the captures that belong to it; `--last 24h` after a same-day ingest covers them |
| Hz and Elexon cadence | NESO field information: `f`, title "System Frequency (Hz)", unit Hz; `elexon/freq` page: samples 15 seconds apart |

## Findings

1. **major** `page.family.members[0].differs`: "the four tables below read it". Five tables are listed below it, and all
   five read this bronze: `system_frequency_dmy_csv` is also sibling-fed from it (`siblings: ["system_frequency"]`; its
   silver exists, 11 files). Only four are shown with rows. A reader counting the member list finds five. Suggested:
   "every monthly file lands here, and the tables below read it", or say "four ... and the held 2014 one". The same
   fix settles the three-command question (finding 3): "the other three typed tables" is right only for the four
   shown tables, so say "the other three shown tables".

2. **major** `page.record.caption` (and the band that carries it): the page says "Schema and sample rows" under a lead
   that has no silver table, and the caption names no table. The frame is `system_frequency_gmt_csv`, which a reader
   learns only from the chart caption two sections up; the frame's own `bronze_capture_id` shows the lead's bronze path
   (`bronze/neso_data_portal/system_frequency/...`), which pulls the other way. The seat asked for the bronze-only lead to
   be stated plainly: it is stated once, inside the member list. Suggested caption: "Silver
   `system_frequency_gmt_csv`: seconds either side of 01:00 and 02:00 UTC on 26 March 2023." (15 words now, so there is
   room.)

3. **nit** `page.record.caption`: "UK clocks went forward" gives the date's event but not what the eight rows show. The
   point is that the GMT-shape labels carry every second through 01:00 to 02:00 (no skipped hour) and the label runs on
   in UTC. A reader who does not already know the 26 March 2023 change at 01:00 UTC sees ordinary rows. One clause fixes
   it: "no hour is skipped: the labels are GMT, not UK clock time". The claim itself is accurate and scoped to these rows.

4. **nit** `page.raw_feed.commands[1].comment` ("April 2022 onward"): describes what the table holds, not what the
   command does; sibling pages say "the capture's date to silver". Accurate, but a reader gets no hint that this
   transforms only the `_gmt_csv` captures of the date partition. Also, the ingest line hides its size: NESO's declared
   sizes for the 152 files sum to about 9.4 GB. A short "152 files, about 9 GB" in the ingest comment would be an
   honest vendor fact (declared content lengths), your call. On the three-command limit generally: the shown pair plus
   "the other three ... transform like the second line, by their own keys" is accurate; the three remaining commands
   are `gridflow transform neso_data_portal system_frequency_<offset_csv|offset_zip|gmt_zip> --last 24h`, same flags.

5. **nit** `page.related[2].note` ("Fast frequency response NESO bought before EAC"): the target page is Dynamic
   Containment, Regulation and Moderation results. "Fast frequency response" is not a NESO service name here and sits
   beside the portal's separate Firm Frequency Response packages (FFR); a reader will confuse them. Suggested: "NESO's
   frequency response auctions before EAC".

6. **nit** `page.related[0].note` ("sent daily"): Elexon does not send daily; gridflow asks for one 24-hour window per
   call (`elexon/freq` page). Suggested: "Elexon's GB frequency, one sample every 15 seconds".

7. **nit** `page.notebook.lead`: cell 5 (86,400 rows on a clock-change day in each of the four typed tables) is not
   mentioned anywhere on the page, so a reader sees four identical numbers with no reason. One clause in the lead
   ("the fifth cell counts one clock-change day in each table") closes it. The cell is read-only and its output is
   correct (checked against silver: each of those days is 86,400 rows, steps of 1 s).

8. **nit** `page.chart_view` (template, for the seat): the x axis carries one label, `13:00` at the left, and no
   `13:10` or `13:30`, so the dip's time can be read only from the key note. The x label line gives the range. Not
   fixable in the note.

9. **nit** `page.family.members` (optional content): two facts a reader parsing the raw CSVs will hit are on no page:
   the 31 midnights of August 2026 are date-only cells (`2026-08-01`, verified in `fnew-2026-8.csv`, 31 of 2,678,400
   rows), and the file behind the chart (December 2023) was re-uploaded by NESO (`last_modified` 2026-04-17), so the
   chart shows the latest copy. The first fits the `_gmt_csv` `differs` line; both are vendor facts. Nothing wrong
   as it stands.

## Items checked and found right (so the seat need not re-check)

- Hero facts, summary, history, key (`resource_id, dtm`), cadence (NESO's extras: Update Frequency "Monthly"), statutory
  limit wording, `what_it_is` three-format sentence, every `record.fields` line (`published_at` is the CKAN
  `last_modified` of the whole file; `timestamp_utc` equals `dtm`), `plot_alt` (the drop starts at 13:09:52 and is
  mostly done by 13:10:08; "drops sharply at 13:10" is loose but fair).
- Held 2014 line is one plain line, no codes, and both halves are true.
- `notebook.lead` matches `query()` (`_date_range_predicate`: half-open UTC instants, end day inclusive; reads
  `_latest`; the workbench returns session-zone times, so the first cell's `tz_convert` is needed).
- No local-data wording: the numbers on the page are NESO or code facts, the chart, the eight rows or notebook output.

## Defects for the record (not page findings; the author's report missed the first)

- **gridflow silver: the held 2014 table is missing October 2014.** `silver/neso_data_portal/system_frequency_dmy_csv`
  has 11 files (28,857,600 rows), not 12. The October capture fails with `DuplicateEntityKeyError` ("7200 row(s)
  sharing an entity key ['resource_id', 'dtm']", failure record
  `state/neso_data_portal/completion_failures/system_frequency_dmy_csv/45da2fdce0a2dbfa4c3e657f646457a5.json`).
  The note body says one family is held for 2014 and counts 399,686,400 rows over 152 months, which includes it. The
  page is unaffected (the table is held and the hold line is right), but the key `(resource_id, dtm)` is wrong for
  that month and the held table cannot serve the whole year.
- gridflow_models (author's report): the workbench serves the held 2014 table and `list_datasets()` names the bronze
  lead that `query()` rejects. Reproduced by reading `_get_method_registry.py` only (no hold check in `query()`); not
  run.
