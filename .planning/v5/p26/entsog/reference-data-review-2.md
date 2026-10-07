# entsog/reference-data: checker re-review (round 2)

Checker: Sonnet 5.5 · high, 2026-10-07. Answers `reference-data-author-2.md`.

## Verdict: REVISE

0 blockers, 1 major, 4 nits. All four round-1 majors are fixed. One of the nit fixes introduced a new false statement.

## Regression gate

- `gridflow-build --only entsog/operators`: succeeds, wrote `data-sources/entsog/reference-data.html`.
- `detect.mjs --json` (absolute path): `[]`. Page text has 0 em dashes, 0 `→`, 0 `·`, and none of the words `locally`,
  `held`, `our `, `since 20`, `coming`, `planned`, `soon`, `real-time`, `live`.
- `cmp` on all six notes, vault worktree against `vault/entsog/`: byte-equal.
- Rendered check at 390 (numeric): document width 390, no element outside a scroll box, and no chart label inside the 16 px
  gutter. At 768 and 1440 the hero, chart, frame and raw-feed lines look as before; no clipping.
- The 1440 guide squeeze is unchanged (the seat's call).

## Round-1 majors

1. **`query()` on the non-lead members: fixed.** `what_it_is` now says directions and interconnections have `timestamp_utc`
   null on every row so `query()` returns nothing; the two `differs` lines say it; `notebook.lead` names `timestamp_utc` for
   operators and `ingested_at` ("the silver write time") for zones, points and aggregates. `ingested_at` is the column in
   `schema_manifest.py:193,200,204`, and silver `ingested_at` is 00:31:03 UTC against a 00:30:59 bronze fetch, so "silver
   write time" is right.
2. **Naive stamps: fixed.** The guide says offsets are converted and "the naive 2014 one only labelled UTC". Bronze has
   exactly one naive operators stamp (`TR-TSO-0003`, `Sep  1 2014 12:16AM`); the other ten non-shared stamps carry offsets.
   The interconnections line says its stamp is local time labelled UTC (see nit 3). The caption no longer headlines the
   2014 stamp.
3. **Key scope: fixed.** The page says "Flow, capacity and tariff rows carry the same operator, point and direction keys"
   and the related note "Daily flows carrying the same operator, point and direction keys". Neither claims every triple
   resolves. The counts (39 of 986, 546 of 13,764 rows) are in the `operator_point_directions` note body only, scoped to
   the 27 Sep 2026 capture; I reproduced them last round.
4. **Guide: fixed in substance.** The caption now says "ENTSOG defines no response fields; guide meanings are read from
   names", and `what_it_is` repeats it. The lines now give the form of the values. I checked against silver:
   - "null without a profile" and "else null": all 500 non-profile rows are null or blank in every such column; the 57
     profile rows have no null bool.
   - Legal-citation lines match the constant strings on all 557 rows (2017/460 Art 29&30; 715/2009 Annex I 3.4(6);
     2015/703 Art 16; 715/2009 Annex I Chapter 3).
   - "Free text, mostly empty": no remark column is non-blank on more than 60% of the 57 profile rows.
   - Examples exist in the rows (`2 C`, `02-337`, `Kassel`, `11.3`, `Range 3% - 20%`, `0%`, `-`, `EET`).
   - The lines are not padding. The "Free text, mostly empty" repeats are the true description of those columns.

## Finding

1. **major** `page.record.fields.operator_label`: "Short name as sent, never over 20 characters; longer names arrive cut".
   This is false. In the 27 Sep 2026 capture, `operator_label` runs to 28 characters:
   `ONTRAS Gastransport GmbH` (24), `Infrastrutture Trasporto Gas` (28), `Conexus Baltic Grid JSC` (23). Command:
   `df['operator_label'].str.len_chars().max()` gives 28 and `(L > 20).sum()` gives 3. Sixty-five labels are exactly 20
   characters (for example `Power2MethanolAnvers`, `Aggregated Counterpa`), which is what suggested a cap. The "never"
   comes from my round-1 nit; the evidence supports "often cut at 20 characters", not a cap. Fix: "Short name as sent; many are
   cut at 20 characters, so use `operator_key` to join".

## Nits

2. **nit** `page.what_it_is`: "have `timestamp_utc` null on every row" is a statement about what ENTSOG sent on 27 Sep 2026
   (`validFrom` null on all 1,225 and 194 records). Tie it to the cause ("ENTSOG sends `validFrom` null, and `timestamp_utc`
   copies it") so it stays true if ENTSOG fills the field.
3. **nit** `page.family.members[interconnections].differs`: "its update stamp is local time labelled UTC". The evidence is
   that the stamp (02:18) is later than the fetch (00:30 UTC) and has no offset; that it is local time is inferred (the
   directions stamp sent the same night is `+02:00`). "Reads two hours ahead of the fetch" would state only what is shown.
4. **nit** `page.how_used[2]`: `adjacent_operator_key` is blank on 527 of 1,225 rows, mostly distribution, final-consumer and
   in-country points, and also on 77 of 396 EU to EU cross-border rows. The page names it as the route without saying it can
   be blank. Add "blank for some points".
5. **nit** `page.record.fields.b_m_additional_daily_imbalance_tolerance_is_information`: "flags, dashes, sizes or sentences".
   The sizes are only `0`; most values are placeholder tokens (`ADDITIONALDAILYIMBALANCETOLERANCE`, `tsoInformation/...`)
   that also appear in the cumulated columns. "Flags, dashes, sentences or placeholder text" is closer. Low value, take or
   leave.

## Round-1 nits

5 to 13 of round 1, status: logo (ok), label (broken, see finding 1), gas day hour (ok), `_is_information` lines (ok, see nit
5), "balance responsible parties" (ok), chart labels (ok: nothing inside the gutter at 390), interconnections and far-side
operator (ok, see nit 4), balancing zones and connection points defaults worded as response meta (ok), `how_used[1]` (ok).

Summary: one new false "never over 20 characters" line to fix; the four majors and the other eight nits are resolved, with
build clean, detector `[]` and mirrors byte-equal.
