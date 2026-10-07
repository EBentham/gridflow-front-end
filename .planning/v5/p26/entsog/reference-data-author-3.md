# entsog/reference-data: writer report, round 3

Writer: Opus 5.5 · high, 2026-10-07. This round answers `reference-data-review-2.md` (1 major, 4 nits).

## Status

- **Build:** `gridflow-build --only entsog/operators` passes.
- **Detector:** `detect.mjs --json` (absolute path) returns `[]`. The page has 0 em dashes, 0 `→` and 0 `·`.
- **Old wording:** neither "never over 20" nor "local time labelled" remains on the page.
- **Mirrors:** `cmp` on all six notes shows byte-equal. The canonical notes are still CRLF.
- **Artefacts:** no series, sample or notebook change. Only words changed, and the digests still pass.
- **Screenshots:** none retaken. The edits are short text changes in lines that already wrap (a guide meaning, a
  `how_used` item, a `differs` line, a `what_it_is` sentence of the same length).
- **Script:** `scratchpad\refdata\revise3.py`.

## Major

1. **`record.fields.operator_label`.**
   - Was: "Short name as sent, never over 20 characters; longer names arrive cut".
   - Now: "Short name as sent; many are cut at 20 characters, so join on `operator_key`".
   - Evidence: labels run to 28 characters (`Infrastrutture Trasporto Gas`), and 65 sit at exactly 20 (`Aggregated Counterpa`).

## Nits

2. **`what_it_is`, null `timestamp_utc` tied to its cause.**
   - Now: "For directions and interconnections ENTSOG sends `validFrom` null, which `timestamp_utc` copies, so `query()`
     returns nothing." (53 words in total).
   - Evidence: `generic.py:51-59,185-187`; bronze `validFrom` is null on all 1,225 and 194 records.
3. **`family.members[interconnections].differs`, local time no longer asserted on the page.**
   - Now: "UK-side links; `query()` finds nothing; update stamp, labelled UTC, postdates the fetch". The page states only
     what is shown: 02:18 labelled UTC against a 00:30 UTC fetch.
   - The interconnections note body now reads "most likely local time (inferred: the directions stamp sent the same night
     is `+02:00`) stamped as UTC".
4. **`how_used[2]`.** Now: "Finding the operator across a point, from directions' `adjacent_operator_key`, blank for
   some points." (Blank on 527 of 1,225 rows.)
5. **`_is_information` lines**, rewritten for all four that listed value kinds, from the distinct values in silver:
   - hourly: "As the operator wrote it, such as flags, dashes, formulas or placeholder text"
     (`HOURLYIMBALANCETOLERANCE`, `HIT(d) = …`, `N/A`);
   - additional daily: "As the operator wrote it: flags, dashes, sentences or placeholder text"
     (`ADDITIONALDAILYIMBALANCETOLERANCE`, `0`, a penalties sentence);
   - cumulated: "As the operator wrote it, such as flags, sizes, formulas or placeholder text"
     (`24 MWh/d per Balance Group`, `CIT(d) = …`, `tsoInformation/balancingCumulated`);
   - additional cumulated: "As the operator wrote it, such as `0%`, `-` or placeholder text";
   - the daily line ("such as `Range 3% - 20%`") is unchanged.

## Defects

Unchanged from `reference-data-author.md` and `-author-2.md`.

Summary: the false 20-character cap is fixed, all four nits are fixed, and the build is clean with detector `[]` and
mirrors byte-equal; ready for re-check.
