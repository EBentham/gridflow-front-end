# entsog/reference-data: writer report, round 2

Writer: Opus 5.5 · high, 2026-10-07. This round answers `reference-data-review.md` (4 majors, 9 nits) and the seat's
instructions on it.

## Status

- **Fixes:** all 13 findings are fixed.
- **Build:** `gridflow-build --only entsog/operators` passes.
- **Detector:** `detect.mjs --json` (run at its absolute path) returns `[]`. The page has 0 real em dashes, 0 `→` and
  0 `·`.
- **Mirrors:** `cmp` shows all six byte-equal.
- **Artefacts:**
  - The series was re-distilled; the spec is unchanged and the values are identical.
  - The sample and the notebook are unchanged. Their `select` and `cells` did not change; the build's digest check
    passes.
- **Screenshots** (light only; there is no dark theme): `...\scratchpad\refdata\shots2\` holds `w1440.png`,
  `w1024.png`, `w768.png`, `w390.png` (390 px iframe), and crops `m390_a.png`, `m390_b.png`, `g1.png`.
- **Cleanup:** the static server on 9878 is stopped, and the 390 harness file is removed.

## Majors

1. **`query()` on the non-lead members** (`what_it_is`, `notebook.lead`, `family.members[].differs`):
   - `what_it_is` now says: "Directions and interconnections have `timestamp_utc` null on every row, so `query()`
     returns nothing for them."
   - `operator_point_directions` differs line: "…; `query()` returns no rows; use `data.sql()`".
   - `interconnections` differs line: "UK-side links; `query()` finds nothing; its update stamp is local time labelled
     UTC".
   - `notebook.lead` now says that `query()` filters on `timestamp_utc` for operators, and on `ingested_at` (the silver
     write time) for zones, points and aggregates. Evidence: `schema_manifest.py:193,200,204`;
     `generic.py:201-205`.
2. **Naive stamps labelled UTC** (`record.fields.last_update_date_time`, interconnections differs line, operators note
   body):
   - Guide line: "ENTSOG's update stamp; offsets converted to UTC; the naive 2014 one only labelled UTC".
   - Reproduced from bronze: `TR-TSO-0003` is the only naive operator stamp (`Sep  1 2014 12:16AM`). The other stamps
     carry offsets.
   - The interconnections line says its stamp is local time labelled UTC.
   - The operators body point-in-time line adds the naive 2014 row with `datetime.py:43-44`.
   - The caption no longer headlines the 2014 stamp; it now opens the guide (see 4).
3. **Unscoped "what flow, capacity and tariff rows key on"** (`what_it_is`, related `physical_flows` note):
   - Page: "Flow, capacity and tariff rows carry the same operator, point and direction keys."
   - Related note: "Daily flows carrying the same operator, point and direction keys". There is no claim that every
     triple is in the register.
   - The counts stay off the page (no local-data rule) and are recorded as an observation in the
     `operator_point_directions` note body:
     - 39 of 986 `physical_flows` triples are absent, 546 of 13,764 rows;
     - examples `BE-TSO-0001 ITP-00065` and `DE-TSO-0003 ITP-00518`;
     - cause unknown; all other data tables resolve.
4. **Column guide** (seat ruling: one line per column, a plain opener, terse and true):
   - Opener: `record.caption` now reads "Eight operators by key. ENTSOG defines no response fields; guide meanings are
     read from names." It sits directly above the frame. `what_it_is` repeats "ENTSOG defines none of the response
     fields".
   - The template has no guide-introduction field, so the caption is the nearest place (template note below).
   - All 129 lines are rewritten (`scratchpad\refdata\fields2.yaml`). Lines that only restated a name now say what
     the values look like:
     - remark columns: "Free text, mostly empty";
     - profile booleans: "`true` or `false` with an operator profile, else null";
     - profile URLs: "… URL; null without a profile";
     - legal-citation columns name the citation;
     - unit columns: "spellings vary between operators";
     - examples taken from the rows (`2 C`, `02-337`, `Kassel`, `11.3`, `Range 3% - 20%`).
   - No padding. All lines are 14 words or fewer.
   - Checked by script: every column whose line says "null without a profile" or "else null" is null or blank on all
     500 non-profile rows. A profile row is one of the 57 that carry `gas_day_start_hour`.

## Nits

5. `operator_logo_url`: "Logo URL, usually on ENTSOG's site; blank for most operators" (369 of 557 blank).
6. `operator_label`: "Short name as sent, never over 20 characters; longer names arrive cut" (65 rows at exactly 20).
7. `gas_day_start_hour`: "Gas day start hour; no time zone field, though a few remarks name one". The
   `gas_day_start_hour_remarks` line cites `EET`.
8. `_is_information` lines describe the values as the operator wrote them:
   - daily: "The tolerance as the operator wrote it, such as `Range 3% - 20%`";
   - hourly: "flags, dashes, sentences or formulas" (it has no sizes);
   - cumulated: "flags, sizes or formulas";
   - additional daily: "flags, dashes, sizes or sentences";
   - additional cumulated: "such as `0%` or `-`".
9. Key note: "balance responsible parties".
10. Chart labels shortened to "Storage", "Hydrogen", "LNG" and "Production" (the key and bar labels). At 390 the
    longest label, "Energy transition", now starts about 25 px from the viewport edge, inside the gutter
    (`m390_a.png`).
11. Interconnections and the far-side operator:
    - The interconnections differs line is now "UK-side links" (no longer "exit system to entry system").
    - `how_used[2]`: "Finding the operator across a point, from directions' `adjacent_operator_key`."
    - Correction to my round-1 report: the interconnections key is not null-free. `from_operator_key` and
      `from_direction_key` are null on 16 rows; the vendor `id` is the unique key.
    - Also: `adjacent_operator_key` is never null but is blank on 527 of 1,225 rows. The use line names it as a route
      only.
12. `balancing_zones` and `connection_points` differs lines now say "meta shows ENTSOG's default `isDeactivated=0`"
    and "`IsInvalid=False`". This is worded as the response meta's default, not a documented rule.
13. `how_used[1]`: "Looking up `pointDirection` keys; gridflow's request lists are written by hand."

## Notes for the seat

- **Template:** there is no field for a sentence that opens the column guide. The "ENTSOG defines no response fields"
  statement lives in `record.caption`. A guide intro (or group lines) in the content model would fit wide vendor
  registers better.
- **Template:** the 1440 guide squeeze (`dataset.css:42`) is unchanged. Nothing overflows now (`g1.png`).

## Defects (unchanged from round 1, one addition)

- **[gridflow silver] Operators' only naive stamp labelled UTC.** `TR-TSO-0003` `lastUpdateDateTime` is sent as
  `Sep  1 2014 12:16AM` with no offset, and `silver/entsog/datetime.py:43-44` labels it UTC. This is the same defect as
  the interconnections stamp: naive ENTSOG timestamps are labelled UTC rather than read in ENTSOG's zone.
- All other round-1 defects stand as written in `reference-data-author.md`:
  - null `timestamp_utc` and an empty `query()` on two registers;
  - the interconnections stamp 2 h late;
  - `validto` and the date-shaped text columns;
  - `gridflow-sample` and `|`;
  - the guide `dt` width;
  - DATA-MATRIX range;
  - the physical_flows observation.

Summary: all 4 majors and 9 nits fixed; build clean, detector `[]`, mirrors byte-equal; ready for re-check.
