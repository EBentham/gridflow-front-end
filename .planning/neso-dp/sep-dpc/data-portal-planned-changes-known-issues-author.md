# Data Portal changes and known issues: author report

One-table page `data-portal-planned-changes-known-issues`, lead `portal_known_issues`. Writer, 2026-10-24.

## Status

- `gridflow-build --only neso_data_portal/portal_known_issues`: success. One intermediate failure (`what_it_is` 61/60)
  was fixed by trimming. The "37 lines in Known issues and gotchas" warning is the build-wide caveat-grammar notice.
- Detector on `site/hifi/data-sources/neso_data_portal/data-portal-planned-changes-known-issues.html`: `[]`. 0 em
  dashes, 0 en dashes, 0 middle dots. The page has 51 "→" and some "our " and "planned" hits. They are all NESO's own
  text inside the frame's `description` cells (column-rename lists, "As part of our ongoing efforts"), or NESO's
  status values.
- Canonical note (vault worktree, Edit tool): 526 lines, 526 CR. The diff is +136/-2: the `page:` block, `updated`
  moved to 2026-10-24, one line-number fix and two Known-issues bullets. Mirror copied; `cmp` equal.
- Artefacts, all from real data:
  - `series/.../portal_known_issues.json`: `spec_origin` vault, bar, 5 categories, 246 rows used, 487 read.
  - `samples/.../portal_known_issues.json`: from gridflow-sample, 8 rows, 18 columns.
  - `notebooks/.../portal_known_issues.json` and `-6.png`: from run_notebooks.py, 4 cells after setup and the help
    card, no errors.
  - No staged spec or authored override existed.
- Screenshots in `<scratchpad>\dpc-writer\shots\`. Full pages at 1440 (`w1440b.png`), 1024 and 768. 390 through a
  390 px iframe at four offsets (`mpair0.png`, `mpair2.png`). Nothing is clipped or overlapping; long related slugs
  and request URLs wrap at 390. The first 1440 capture (`w1440.png`) was cut off after one frame row by a headless
  timing glitch; the retake is complete. The server on 9961 (PID 64568) was started with a recorded PID and stopped
  by that PID. The site has no dark scheme to check.

## The captures (checked; `dedup:` set)

Silver holds two captures. Both are whole and neither is truncated:

| File (CKAN `last_modified`, UTC) | Captured | Rows | Items |
|---|---|---|---|
| 2026-10-08 09:43:34 | 2026-10-08 11:16:49 | 241 | 1..241 |
| 2026-10-16 13:34:40 | 2026-10-16 20:43:02 | 246 | 1..244, 255, 256 (no 245..254) |

Every 8 October item is in the 16 October file. Items 1..238 are identical in every column. These items changed:
- 239 and 240: `Planned` became `Deployed`, with a new `last_updated`.
- 241: moved from 15 to 19 October 2026, with the note "Has been rescheduled for 19/10/2026". Its `description` still
  says 15th October.
- 242, 243, 244, 255 and 256 are new.

The launch prompt's "241 rows" is the 8 October file. The newest file, which `_latest` serves, has 246 rows. The
manifest member is correct.

The chart and the frame filter `published_at` to 16 October 2026 and set `dedup: {on: [po], order_by: published_at}`.
With the filter, dedup dropped 0 rows; it guards against a later capture.

## The chart, and how I reproduced it

I chose items by `status` in NESO's 16 October 2026 file (bar, count). Status is NESO's own categorical column with
five values, so no binning of mine is involved. "Type" would mean binning 72 free-text titles myself. "Month raised"
does not exist: there is no raise date, and `last_updated` is a mutable edit time. A chart over time would need a
year bucket, which the bar spec cannot derive.

The values are Deployed 214, Cancelled 25, Planned 4, Postponed 2, and Deployed on the test link provided 1 (shown
as the bar label "Test link", with NESO's full value as the key's code). I reproduced them with Polars over silver
(`value_counts` on `status` where `published_at` = 2026-10-16 13:34:40.735778). They match the committed series, the
alt text and notebook cell 2's output. The caption dates the counts to that file and says NESO edits statuses in
place.

Key notes, from silver:
- Planned is items 189, 241, 255 and 256. Item 189's `change_datetime_from` is 2026-01-09 11:00Z. It is still
  "Planned"; the page does not say why.
- Postponed is item 14 (window from 2021-04-16) and item 48 (2022-01-22).
- Test link is item 72, "Prototype testing", from 2022-01-16.
- Item 31 ("SOP dataset is being updated manually", an issue item) is `Deployed`.

## What one row is

One numbered item (`po`) as it reads in one NESO file (one capture). The key on the page is `[po, published_at]`.
The registry entity key is `po` within a capture, and `_latest` is `whole_capture`. NESO does not say whether item
numbers are permanent (TODO in the note), so the page never claims they are. The table has no event time:
`timestamp_utc` is the capture time (registry `temporal: none`). That is why the notebook uses `data.sql()` on
`silver_neso_data_portal_portal_known_issues_latest`.

## Evidence table

| Claim (field) | Evidence |
|---|---|
| Quote "upcoming changes to the NESO Data Portal along with any known issues" | Package description, quoted in the note body |
| History: package created 19 November 2020 | Note body: CKAN `metadata_created` and resource `created` 2020-11-19 |
| Cadence: ad hoc (NESO); gridflow checks daily | Package extras "Update Frequency: Ad hoc"; `config/sources.yaml:1025` `schedule: "daily"` |
| Change windows and last-updated are UTC | Registry `zone: UTC`; vendor unit "IS0 8601 - UTC" |
| From and to meanings: "will occur" and "will be fixed" | Vendor dictionary, quoted in the note |
| 239 and 240 Planned on 8 Oct, Deployed on 16 Oct | Polars join of the two captures on `po` |
| Frame: items 239..244, 255, 256; no items 245..254 | Silver 16 Oct capture; notebook cell 3 output `[245, ..., 254]` |
| Item 241 note and unchanged description | Silver rows of both captures |
| Related: 239 and 243 CMIS arming files; 241 AAHEDC, rescheduled 19 Oct; 256, seven TNUoS files; 255, two stability midterm column IDs | `dataset_specific`, `file_specific` (256 lists 7 files) and descriptions (255: "Inertia (in MVA.s)" and "Month & Year") |
| Requests | 16 Oct sidecar `request_url`; `package_show?id=` as on the approved NESO pages |
| Commands `--last 24h` | Same as the approved interconnector register and FES ED6 pages (same connector) |
| Notebook lead: `query()` filters `timestamp_utc`; times print in UK time | gridflow_models `_date_range_predicate` (cited on approved pages); cell 3 output shows `+01:00` offsets |
| Plot alt: 5/36/26/33/44/38/59 by start year; 5 with no start | Polars `change_datetime_from.dt.year` on the 16 Oct capture; committed PNG |

## Body corrections (canonical note)

- `config/sources.yaml:1021` is now `:1025` (checked with grep).
- New Known-issues bullet, "Edited in place, numbers not contiguous (2026-10-16 capture)". It covers the gap, the
  three edits and the 16 October status counts.
- New Known-issues bullet, "Mojibake in NESO's text (item 256)". The raw CSV has `Â£` (bytes `C3 82 C2 A3`), and
  silver keeps it byte for byte.

## Unverified

- Whether NESO will ever fill items 245..254, or reuse or renumber items: there is no vendor statement.
- Why item 189 is still Planned with a January 2026 window. The page states only the row.
- Whether `Deployed` on an issue item means the issue is fixed. The page never says resolved; it gives NESO's word.

## Template problems (report only)

- The unfolded frame prints NESO's multi-line `description` and `dataset_specific` cells in full (item 240 lists 20
  datasets; `data-w` up to 17,825 px). Polars itself would truncate them. The cells are behind the fold, so nothing
  overlaps, but the unfolded frame is very wide. I did not screenshot it unfolded.
- The page's notebook panel shows only the setup cell and the query. The other cells and the plot are in the demo
  notebook. This is the same as other pages.

## Checker: look hardest at

1. The phrase "items 239 and 240 read Planned in its 8 October 2026 file and Deployed on 16 October" in `what_it_is`.
   It is dated to NESO's files, as the batch asks, but the 8 October file can no longer be fetched from NESO. Is this
   acceptable, or a local-capture reference?
2. The key notes against silver, especially item 189 and the claim that "issue items" are Deployed (item 31).
3. The 51 "→" in the built page: all of them are NESO's verbatim text in the frame. Rubric 6 lists "→".
4. Whether the related notes ("renames") should be in the past tense for 239 and 243, which NESO marks Deployed.

## Defects

- **Vendor data, Data Portal changes log** (`23021dfa-a3b8-4f62-93bc-b60186c53fa4`, file last modified 2026-10-16):
  item 256's description has a double-encoded pound sign, `TDR Tariff in Â£/(Site Day)` (bytes `C3 82 C2 A3`).
  It is kept byte-equal in silver and recorded in the vault note. No gridflow change is needed.
- **Vendor data, same file:** item 241 was rescheduled by a note ("Has been rescheduled for 19/10/2026") while its
  `description` still says 15th October. Item numbers jump from 244 to 255. Both are recorded in the vault note; no
  gridflow change is needed.
- **Planning record:** the batch file and ledger give 241 rows. That count is the 8 October file; the newest
  capture (16 October) has 246.
- No gridflow code defect found.
