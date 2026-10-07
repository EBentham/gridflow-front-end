# entsog/gas-quality: author revision 2

Writer: Opus 5.5 · high, 2026-10-07. Answers `gas-quality-review.md` (REVISE: 0 blockers, 2 majors, 7 nits). All edits are in the canonical `30-vendors/entsog/datasets/gcv.md`. The other four notes are unchanged.

## Status

- **Mirrors:** all five notes copied with `cp` and checked with `cmp`: byte-equal, CRLF on every line. Line counts: gcv 447, wobbe_index 285, methane_content 248, hydrogen_content 247, oxygen_content 247.
- **Build:** `gridflow-build --only entsog/gcv` passes.
  - All 28 warnings are the generic "no Pydantic class" notices.
  - No field is over budget.
  - `wrote: data-sources/entsog/gas-quality.html`.
- **Detector:** `detect.mjs --json`, run at its absolute path, returns `[]`. Em dashes: 0. The rubric greps on the rendered text find nothing.
- **Artefacts:** unchanged. The chart spec, select and notebook cells were not touched, so the series, sample and notebook digests still pass.
- **Screenshots:** retaken at 1440 and at 390 (true 390 px iframe) after the edits, in `scratchpad\gq\shots2\`.
  - The new summary, the key note, the three `differs` lines and the guide all wrap cleanly. Nothing is clipped.
  - The static server on 9874 was restarted under `timeout 600`, so it stops itself. Port 9670 was not touched.

## Findings and fixes

1. **Major, `record.fields.timestamp_utc`: placeholder stamps.** Fixed.
   - The field was "Start of the gas day, from the vendor `periodFrom`, in UTC". It is now "Gas-day start from `periodFrom`, in UTC; placeholders send an earlier one" (12 words).
   - Reproduced: gcv has 56 rows at 04:00 UTC (valued) and 42 at 03:00 UTC (all `is_na` 1).
2. **Major, `gcv.md` Known issues, "Repeated values".** Fixed.
   - Reproduced from silver: National Gas TSO has 11 distinct `last_update_date_time` values over 14 gas days, while Interconnector and GNI have 14 each.
   - Gas days 14 and 15 Sep share 2026-09-18 15:54:29 UTC. Gas days 18, 19 and 20 Sep share 2026-09-23 17:02:50 UTC, though the value changes from 11.6429 to 11.6927 and 11.6136.
   - The bullet now gives "own stamp" for Interconnector only, gives the shared stamps for National Gas TSO, and drops the "re-sent, not one record" inference for it. It says National Gas TSO's stamp reads as a batch time.
   - The same sentence is corrected in `gas-quality-author.md` (two places).
   - The Wobbe and methane notes' repeated-value bullets cover Interconnector only, so they stay correct.
3. **Nit, `key[bacton_iuk_entry].note`.** Now "Interconnector's report; within 0.02 of National Gas TSO's except 14.253 on the 20th, sent `Confirmed`." (16 words).
   - I put `Confirmed` on the 20th's value rather than on the whole report, because Interconnector's 15 Sep row is `Provisional`.
4. **Nit, overlapping lines.** No page change; it was already reported as a renderer matter for the seat.
5. **Nit, `family.members[].differs`.** "only" is removed and the exit zero is stated:
   - methane: "Methane in `% (mol/mol)`; Bacton (IUK) and Moffat (IE) entry; Interconnector's exit sends 0";
   - hydrogen: "Hydrogen in `% (mol/mol)`; Interconnector at Bacton (IUK) entry, its exit sends 0";
   - oxygen: the same as hydrogen, with Oxygen.

   All three are within 14 words (the build passes). Wobbe keeps its "only", which the operators' own remarks back.
6. **Nit, register GCV units.** Added a Known issues bullet to `gcv.md`.
   - Reproduced from `silver/entsog/operator_point_directions` (`tp_tso_gcv_unit`): `MJ/Sm3` for National Gas TSO at `ITP-00005` exit, `ITP-00207` exit and `ITP-00090`; `kWh/Nm3` for Interconnector and GNI (GNI's remark cites ISO 13443:1996); `kWh/m3(n)` for BBL company.
   - The bullet notes that the rows label every GCV `kWh/Nm3` and that the two Bacton reports agree, and advises checking the register before a cross-operator model. The page is unchanged, as suggested.
7. **Nit, frame fold at 390.** Template width tiers; no change (seat item).
8. **Nit, `summary`.** Now "Daily gross calorific value and methane content at Bacton and Moffat, plus Wobbe index, hydrogen and oxygen at Bacton, from ENTSOG." (21 words). Values at Moffat exist only for GCV and methane (GNI); Wobbe, hydrogen and oxygen values come only from Bacton (IUK).
9. **Nit, `record.fields.is_cmp_relevant`.** Now "Vendor congestion management procedure (CMP) relevance flag; text, as placeholders send it empty" (13 words).

## Defects (additions to the first report, pasteable)

- **[vendor data, observation] National Gas TSO's `lastUpdateDateTime` is shared across gas days.**
  - `entsog/gcv`, `UK-TSO-0001` `ITP-00005` exit: gas days 14 and 15 Sep 2026 are both stamped 2026-09-18 15:54:29 UTC.
  - Gas days 18, 19 and 20 Sep are all stamped 2026-09-23 17:02:50 UTC, though the value changes between the 18th and the 19th.
  - 11 distinct stamps over 14 gas days. The stamp behaves as a batch time, not a per-value revision time.
- **[vendor data, observation] The register declares GCV units that differ from the `operationalData` unit label.**
  - `silver/entsog/operator_point_directions` `tp_tso_gcv_unit` is `MJ/Sm3` for `UK-TSO-0001` at `ITP-00005` exit, `ITP-00207` exit and `ITP-00090`.
  - `entsog/gcv` rows for the same point direction are labelled `kWh/Nm3`, with values near 11.6.
  - BBL company declares `kWh/m3(n)`.
  - Worth a vendor or register check before any cross-operator model uses GCV.
