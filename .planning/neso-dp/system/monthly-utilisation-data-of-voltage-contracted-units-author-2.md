# Writer report, round 2: Monthly utilisation data of voltage contracted units

Fixes for the checker's four nits (`monthly-utilisation-data-of-voltage-contracted-units-review.md`, APPROVE). The
seat's hold stands. All edits are in the canonical note
`C:\gridflow-wt\vault-neso-sys\30-vendors\neso-data-portal\datasets\monthly-utilisation-data-of-voltage-contracted-units.md`
(Edit tool, CRLF kept), mirrored to `C:\gridflow-wt\fe-neso-sys\vault\neso_data_portal\` with `cp`. `cmp` shows the
two files are identical.

## Fixes

1. **Outturn voltage costs pairing** (`page.how_used[1]`, `page.related[0].note`). These now say the costs are by
   constraint group, not by unit, so they no longer suggest a close pairing:
   - how_used: "Read beside NESO's monthly voltage costs, which are by constraint group, not by unit"
   - related: "Monthly voltage costs in £m by constraint group, not by unit" (11 words)
2. **Composite BMU ID** (`page.facts.grain`, `page.what_it_is`). A row is no longer called one unit:
   - grain: "One row per BMU ID and month; NESO states no key"
   - what_it_is: "Each row is one BMU ID's month". "BMU ID's" counts as two words, which put the field at 61 words against
     its 60-word budget, so the same sentence now reads "a unit of power, not energy" instead of "a unit of power
     rather than energy". The field is back to 60 words, with the meaning unchanged.
3. **Summary** (`page.summary`): "each unit contracted in its Voltage 2026 service" is now "each unit contracted to
   NESO's Voltage 2026 service". Still 22 words.
4. **Body, "Sentinels and missing values"**: "NESO explains neither" is replaced with "NESO does not explain the negative
   absorption, and its example total of `4512` is not the sum of its examples `198` and `4312`". The dictionary does
   say the total sums absorption and injection; only the sign is left unstated.

## Gates

- `parse_page_fields` and `anatomy_errors` on the note: both `[]`. Summary 22, what_it_is 60 and held reason 16
  words, all within budget.
- `gridflow-build --only neso_data_portal/voltage_units_utilisation`: the page is written with no errors.
- Detector `[]`; 0 em dashes on the page. The rendered page carries each new phrase.
- No series, sample or notebook artefacts, as a held page requires.
- Screenshots: not retaken, because this round's instructions forbade starting a server. The changes are word swaps
  of the same or similar length in fields that rendered cleanly at all four widths in round 1.

## Not mine

The `outturn-voltage-costs` related link renders blank on this branch because the branches were stacked before that
page was approved. The seat will fix this when it merges.

## Defects

None new. The two from round 1 stand (sign convention and unit unclear; one row only). The checker adds a related
fact: the ORPS package text gives that package's utilisation in MVArh, while this file's dictionary says MVAr.
