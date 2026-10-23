# Review: ancillary-services-important-industry-notifications (lead as_industry_notifications_balancing)

Checker, 2026-10-18. Verdict: **REVISE** (0 blockers, 1 major, 3 nits).

Build `--only neso_data_portal/as_industry_notifications_balancing`: success. Detector on the page: `[]`. No em or en dashes,
middle dots or arrows in the built page. Mirror and canonical note `cmp` equal. Screenshots at 1440, 1024 and 768 (full page)
and 390 (390 px iframe): nothing clipped or overlapping. Server on 9991 stopped.

## Findings

1. **major** `page.notebook.cells[0]` (and its output) / `page.record.fields.notes`: the first notebook cell ends in
   `.head()`, so its output shows the first five Balancing Reserve rows: 2024-03-29, 2024-11-26, 2025-10-08, 2025-11-25,
   2025-11-30. The last three are exactly the three rows whose notes are shifted (vendor defect 20n): 2025-10-08 shows `NaN`,
   2025-11-25 shows "This is an enduring change for the EAC sandbox...", 2025-11-30 shows "...for the EAC PRODUCT...". The
   cell shows notes without descriptions, so a reader cannot see that the 25 November notice is the production outage and the
   30 November one is a forecast-upload notice. The page therefore excludes the three rows from the frame (true: the frame is
   the eight newest, 26 March to 4 September 2026, none affected) but puts them on screen in the notebook output with no
   warning, and the `notes` guide line ("NESO's free-text note, such as whether the change applies once; often null") presents
   the column as reliable. Evidence: `notebooks/.../as_industry_notifications_balancing.json` cell 3 rows 2 to 4; raw bronze CSV
   `raw_20261008T081601Z_13f8f6b1-...csv` (08/10/2025 note empty, 25/11/2025 sandbox note, 30/11/2025 production note); the same
   notices in DC/DM/DR and Quick Reserve carry the sandbox note on 2025-10-08 and the production note on 2025-11-25 (Polars over
   silver, notes differ at those two minutes). Fix, either: change what the cell prints so it does not display these rows (for
   example `df.groupby("file").tail(2)` style output, or select by date), or say it in the `notes` field line or the notebook
   lead in plain words (some older Balancing Reserve notes sit on the neighbouring notice). Re-run `run_notebooks.py` after any
   cell change.

2. **nit** `page.summary`, `page.what_it_is`: "one file per service" and "Each service has its own file" are not quite
   right. Dynamic Containment, Dynamic Moderation and Dynamic Regulation share one file (the chart itself counts combined
   labels). The six files are Balancing Reserve, DC/DM/DR, Quick Reserve, Slow Reserve, STOR and Static FFR. Suggest "one file
   per service group" or name the grouping.

3. **nit** `page.notebook.cells[2]`, `page.notebook.plot_alt`: the axis label and alt say "UK time". The query returns
   Europe/London-zoned times, but `mdates.DateFormatter("%b %Y")` is built with no `tz`, so matplotlib formats the tick labels
   in its default zone (UTC). At January and July month ticks the labels cannot differ, so nothing visible is wrong; the words
   "UK time" just describe the data, not the axis. Drop "UK time" from the label or pass `tz`.

4. **nit** `page.family.members[5].held`: "Its one row's dates could be day first or month first, and may be a placeholder."
   is true to the ledger (SFFR-NOTIFICATION-DATE-ORDER: `01/03/2024` is ambiguous; one row, blank description, note "Example
   note", same effective times as the first STOR row) and plain. It would be more concrete, and still brief, to say what
   makes it look like a placeholder: "The file's one row has a blank description and the note 'Example note', and its dates
   could be day first or month first." Optional.

## Checked and correct

- **Chart counts.** Polars over silver `as_industry_notifications_dc_dm_dr` (one capture, `published_at` 2026-08-19 15:12:17.130148 UTC,
  28 rows): `DC, DM, DR` 12, `DM` 11, `DC` 3, `DC, DM` 1, `DM, DR` 1. Matches the committed series, alt text and bars. Caption says
  it is one member and that a combined label is one value; "last modified 19 August 2026" matches the stamp. Series is
  `spec_origin: vault`, digest passes.
- **Key notes against NESO's full text.** DM (11): every notice raises the DM requirement (one auction or from a date), including
  the 24 Jan 2025 high-wind and 7 Aug 2026 eclipse notices. DC (3): two Data Portal maintenance notices (2 and 4 April 2024) and the
  19 to 20 Sep 2025 raise of the DCL forecast requirement (NESO says DCL; "raised DC requirement" is a fair summary). DC, DM:
  "additional 100 MW of DC (high and low) and DM (high and low)" for EFAs 3 to 5 in the 29 May 2026 auction. DM, DR: DML and DMH to
  300 MW, DRL and DRH to 480 MW, auction 2 Feb 2025 for delivery 3 Feb 2025. DC, DM, DR (12): 4 delay and all-clear notices, 2 new
  column notices, 2 EAC sandbox and production outage notices, 3 archive or restructure notices, 1 ABSVD clarification; "Mostly
  ..." holds (11 of 12).
- **Frame.** Eight newest of the 13 Balancing Reserve rows, 2026-03-26 to 2026-09-04, `published_at` 2026-09-04 10:50:39 UTC,
  all `BR`. Values match the raw CSV after the UK-to-UTC conversion (04/09/2026 12:00 is 11:00 UTC; 01/10/2026 17:00 is 16:00 UTC).
  "Can precede an issue time" is true on the newest row (10:50:39 against 11:00).
- **Notebook time-zone sentence.** `query()` builds `SELECT ... FROM silver_neso_data_portal_<table>_latest WHERE timestamp_utc >= ? AND
  timestamp_utc < ?` with half-open UTC days (end inclusive); date column `timestamp_utc`, `TIMESTAMPTZ`, from the schema manifest.
  No code in gridflow or gridflow_models sets a DuckDB `TimeZone`; `duckdb.connect()` here reports Europe/London; the committed
  output shows `+00:00` and `+01:00` offsets. "Times come back in the machine's zone, UK here" is accurate.
- **67 rows against 43 distinct issue times.** 13 + 28 + 13 + 4 + 9 = 67 rows; 43 distinct issue instants; 17 occur in 2 to 4 files
  (12 in 2, 3 in 3, 2 in 4); `description` differs at three instants (2024-03-28 14:00Z, 2026-03-26 14:45Z, 2026-08-07 14:35Z).
  The claim is in the vault body, not on the page; the page says "often posted to several, sometimes reworded", which holds.
  Notebook cell 4 output rows match (including the 4-file, 2-text row on 2026-03-26).
- **Plot alt.** STOR's last issue 2025-04-01, Slow Reserve's first 2026-03-26, DC/DM/DR with Quick Reserve is the most common pair
  (13 shared minutes, against 5 for the next).
- **SFFR held line.** Matches the ledger (`SFFR-NOTIFICATION-DATE-ORDER`) and K-AS-2-FACTS 4.4; raw CSV is one row, `01/03/2024 10:00`,
  blank description, "Example note"; header identical to the Balancing Reserve file.
- **Raw feed and commands.** Request URLs equal the capture sidecars' `request_url`; all six are uploads; window is not a selector
  and is screened to end recently, unchanged files skipped (`client.py` `fetch`, `iter_members`, `_assert_window_admissible`).
- **Defect 20n.** Reproduced against the raw CSV and the other two files; the vault bullets state it correctly. Not a vault
  body overreach: both new Known-quirks bullets cite measurements.
- **Copy greps.** No "live", "locally", "held", "our ", "since 20" or bare codes in the page copy; the one "live" is NESO's own
  text in a folded description. Related notes are 12 words or fewer. British spelling.
