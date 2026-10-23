# Ancillary services industry notifications: author report, round 2

Writer, 2026-10-18. Answers `ancillary-services-important-industry-notifications-review.md` (1 major, 3 nits): all
four fixed.

## Status

- `gridflow-build --only neso_data_portal/as_industry_notifications_balancing`: success. Two intermediate budget
  failures (`what_it_is` 62/60, `summary` 24/22) fixed by trimming, as below.
- Detector `[]`; 0 em or en dashes in the built page.
- Canonical note: 648 lines, 648 CR; mirror copied, `cmp` equal.
- Notebook re-run with `run_notebooks.py`: 3 cells after setup and help card, no errors. Series and sample unchanged
  (chart spec and record select untouched; the build's digest checks pass).
- No new screenshots: every change is wrapping prose or code text in sections already checked at all four widths.

## Fixes

1. **Major, notebook cell 1 and `record.fields.notes`.** Both done.
   - Cell 1 now ends `df.groupby("file").tail(1)[["file", "notification_issued_date_time", "effective_from_date_time",
     "notes"]]`: the newest notice of each file (balancing 2026-09-04, DC/DM/DR, Quick and Slow Reserve 2026-08-19,
     STOR 2025-04-01). None of the three offset Balancing Reserve rows (2025-10-08, 2025-11-25, 2025-11-30) is printed.
   - `notes` field line: "NESO's free-text note; three 2025 notes in this file sit one row off" (13 words). Evidence
     as in round 1: raw CSV `raw_20261008T081601Z_13f8f6b1-...csv` against the DC/DM/DR and Quick Reserve files.
2. **Nit, `summary` and `what_it_is`.** Summary now ends "one file per service group" (and "platform outages"
   became "outages" to stay in 22 words). `what_it_is`: "Each service or group has a file" (and "when it takes
   effect" became "when it starts" to stay in 60 words).
3. **Nit, plot axis and alt.** Dropped "UK time" from the x label ("notice issued") and from `plot_alt`, since
   `DateFormatter` formats in UTC; at January and July ticks the labels are the same either way.
4. **Nit, SFFR held line.** Now: 'One row: blank description, note "Example note", dates that could be day or month
   first.' (15 words). Matches K-AS-2-FACTS 4.4 and the raw CSV.

## Defects

Unchanged from round 1 (Balancing Reserve notes offset, vendor; narrow bar labels clip at 390, template).
