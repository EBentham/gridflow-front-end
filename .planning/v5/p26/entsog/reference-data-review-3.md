# entsog/reference-data: checker re-review (round 3)

Checker: Sonnet 5.5 · high, 2026-10-07. Answers `reference-data-author-3.md`.

## Verdict: APPROVE

No findings above nit; no new nits.

## Regression gate

- `gridflow-build --only entsog/operators`: succeeds.
- `detect.mjs --json` (absolute path): `[]`. Page text has no em dash, `→` or `·`, and neither "never over" nor "local time".
- `cmp`, vault worktree against `vault/entsog/`: all six notes byte-equal.
- I did not retake screenshots. The round-3 edits are short text changes in lines that already wrap.

## The five points

1. **Operator-name line: fixed.** The page says "Short name as sent; many are cut at 20 characters, so join on `operator_key`".
   Silver `operator_label`: 65 labels are exactly 20 characters, and 49 of them are a strict prefix of a longer
   `operator_label_long` (for example `Aggregated Counterpa`). Three labels run past 20 (up to 28), which "many are cut at
   20" does not deny. The claim is supported and no cap is asserted.
2. **Null `timestamp_utc` cause: fixed.** The page says "For directions and interconnections ENTSOG sends `validFrom` null,
   which `timestamp_utc` copies, so `query()` returns nothing." This matches `generic.py:51-59,185-187` and the bronze
   (`validFrom` null on all 1,225 and 194 records). The sentence names the cause and no longer states a bare universal.
3. **Interconnections stamp: fixed.** The page says only "update stamp, labelled UTC, postdates the fetch". That is what the
   data shows (02:18 labelled UTC, fetch 00:30:35 UTC) and it carries no claim about the real zone. "Most likely local time
   (inferred: the directions stamp sent the same night is `+02:00`)" appears only in the `interconnections` note body
   (line 139), flagged as an inference.
4. **Adjacent-operator line: fixed.** The page says "from directions' `adjacent_operator_key`, blank for some points", with
   no count. The column is blank on 527 of 1,225 rows, so "some" is true. The line is honest about the gap and tells the
   reader how to read it.
5. **Imbalance-tolerance lines: fixed.** I compared each against the distinct silver values:
   - hourly: flags (`true`, `false`), dashes (`-`), a formula (`HIT(d) = ...`), placeholder text (`HOURLYIMBALANCETOLERANCE`);
   - additional daily: flags, dashes, sentences, placeholder (`ADDITIONALDAILYIMBALANCETOLERANCE`);
   - cumulated: flags, sizes (`24 MWh/d per Balance Group`, `2 %`), formulas (`CIT(d) = ...`), placeholder
     (`tsoInformation/balancingCumulated`);
   - additional cumulated: `0%`, `-`, placeholder (`ADDITIONALCUMULATEDIMBALANCETOLERANCE`);
   - daily (`Range 3% - 20%`) unchanged and still present in the values.

## The "527 of 1,225" question

The page does not carry it. A search of the rendered page text finds no `527`, `1,225` or `1225`, and none of the six canonical
notes contains `527` either. The figure is only in the writer's report (`reference-data-author-3.md`, nit 4) as evidence.
So there is nothing to flag against the author brief's numbers rule (no local row counts; a number only if it is a vendor fact,
a code fact, or visible in the chart or rows). Keep it out: "blank for some points" is the right wording.

Summary: the five round-2 items are fixed, "527 of 1,225" is not on the page, and the build, detector (`[]`) and mirrors are clean, so I approve.
