# Dynamic Moderation requirements: review (checker, 2026-10-18)

Verdict: **APPROVE** (no blocker or major; 6 nits, all optional wording).

Counts: blockers 0, majors 0, nits 6.

## What was checked and held up

- Build `--only neso_data_portal/dm_requirements` succeeds (the 3 dropped-caveat-lines warning is the known one). Detector `[]`.
  Mirror `cmp` equal to the vault note. Vault diff against `origin/master` is the `page:` block, `updated`, and two body spans, each
  with evidence (EFA boundaries from K-AS-1-FACTS section 5.1; one-profile sentence reproduced below).
- Silver (read only, Polars): 78 rows, 78 distinct (efa_date, service), 39 EFA dates 2026-09-23 to 2026-10-31, one `published_at`
  (2026-09-22 14:48:12.082389 UTC). Exactly two distinct block profiles: DMH 570/510/510/510/510/570, DML 530/500/500/530/500/530.
  So "570 MW and 530 MW on all 39 dates" is true. Series JSON matches (39 points per series, one value each); alt, key notes and
  notebook plot_alt agree. Bronze CSV header `EFA_DATE,Service,EFA1..EFA6`, 1 capture, resource name "Indicative DM Requirements".
- Flat-chart wording (focus 1): title says "EFA block 1", caption says block 1 and the file's last-modified date, key notes say "on all
  39 dates here". No trend implied, no vendor rule drawn from one file. Seat ruling satisfied for block 1 (see nit 1 for the other blocks).
- `timestamp_utc` (focus 2): silver 2026-10-25 -> 2026-10-24 23:00 UTC, 2026-10-26 -> 2026-10-26 00:00 UTC, 2026-09-23 -> 2026-09-22
  23:00 UTC. Block 1 opens 23:00 UK time the evening before, so it is always one local hour before UK midnight; "block 1 starts an hour
  earlier" is true on both sides of the change (FACTS table: autumn EFA 1 2026-10-24 22:00 to 2026-10-25 03:00 UTC, 5 h; spring 3 h).
  `published_at` is described only as "NESO's last-modified time for the whole file, read as UTC" and "the file NESO last modified";
  the word "issue/issued" appears nowhere on the page. Correct (note: no per-row issue column; bronze sidecar `ckan_last_modified`
  is naive, read as UTC).
- Join advice (focus 3): `eac_results_summary` columns are `auction_product`, `delivery_start`, `delivery_end` (UTC, tz-aware). Its
  DMH and DML rows start at 23:00, 03:00, 07:00, 11:00, 15:00, 19:00 Europe/London, each 4 h, 400 each. So converting the requirement's
  UK block start to UTC before joining is the right direction and true. (The data stop at 17 October, in BST, so the clock change is not
  exercised; the advice does not depend on it.)
- `service` line (focus 4): the vendor dictionary (`field-info/20261008T114228Z/dm_requirements.json`) gives title "Service Type",
  description "DR-L = Dynamic Regulation Low / DR-H = Dynamic Regulation High", example `DR-L`; the file holds `DML`, `DMH`. The
  statement is accurate (wording: nit 2).
- Units and meaning: MW, "before overholding" from the dictionary. `raw_feed` URLs match the sidecar `request_url` and the usual
  `package_show`. Commands and the "dates select nothing" line match the approved BR page. Notebook: `_latest` view via `data.sql`,
  five cells, outputs real, no errors; plot PNG matches `plot_alt` (DMH petrol, DML clay).
- Banned text: no em or en dashes, middle dots, arrows, "locally", "our", "now", "live", planning words, F-codes. No local counts beyond
  what the chart, the eight rows and the notebook show.
- Screenshots (1440, 1024 via full page, 768 and a true 390 px iframe): nothing clipped or overlapping in hero, chart, frame, guide,
  notebook panel. At 390 the folded frame shows only efa1 and efa2, so the `timestamp_utc` rows that demonstrate the clock change need
  unfolding (known template item, not a finding).

## Findings

1. **nit** `page.chart_view.key[0].note` and `chart_view.caption`. The seat ruling asks the page to say plainly that the values are
   the same on every date in the file. The page says it for block 1 only; that blocks 2 to 6 also repeat on every date is stated
   nowhere outside the notebook output (cell 4 shows two distinct profiles). The eight sample rows show four dates only. Suggest a
   clause such as "every block repeats on all 39 dates in this file" in the DMH note. Evidence: Polars group_by of service plus
   efa1..efa6 gives 2 groups of 39.
2. **nit** `page.record.fields.service`. "NESO's dictionary text describes Dynamic Regulation instead" leaves "instead" dangling
   and does not name the codes. Suggest: "`DML` (low) or `DMH` (high); NESO's column dictionary lists the Dynamic Regulation codes
   `DR-L` and `DR-H` for this column". Facts are right.
3. **nit** `page.record.fields.efa1`. "spring change 3 hours, autumn 5" is terse; a reader can take "change" as a change of the
   requirement. Suggest "3 hours on the spring clock-change date, 5 on the autumn one". It also omits "before overholding" that
   efa2 to efa6 carry (the caption and `what_it_is` do say it).
4. **nit** `page.record.fields.timestamp_utc`. "UK midnight opening the EFA date" can be read as the start of the EFA day, which the
   page elsewhere puts at 23:00 the evening before. Suggest "UK midnight at the start of the calendar date `efa_date`, in UTC;
   block 1 starts an hour earlier". Silver agrees with either; this is about reader clarity. Likewise `record.caption` could say
   what to look at ("UK clocks go back on 25 October: `timestamp_utc` moves from 23:00 to 00:00 UTC").
5. **nit** `page.what_it_is` / `page.summary`. NESO's own title for this file is "Indicative DM Requirements" (resource name in the
   sidecar and note, also the note's Modelling notes). The page calls the values "requirement" and "latest view" but never says
   NESO labels them indicative, which matters to anyone reading 570 MW as a firm figure. Suggest naming the file's title once.
6. **nit** `page.how_used[2]`. "Requirement per product and block as a feature for response price models" goes beyond the note,
   whose Modelling notes say comparison with procured volumes. It is a plausible use, not a fact, and unsourced. Consider rewording
   to the compare-with-procured-volumes use or dropping it.

## Not findings

- Open question in the report about charting the six blocks: the template cannot; the notebook carries the profile. Within the seat
  ruling.
- Folded-frame and notebook name-wrapping behaviour at 768 and 390: seat items listed in the batch file.
- Gridflow or data defects: none found on this package. (The 2026-10-16 EAC summary capture has fewer rows than the 2026-10-08 one,
  61,884 against 64,800, which matches the known truncation defect and does not touch this page; the DM table has a single capture.)
