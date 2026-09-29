# soso review 2 (SO-SO prices, Revision 1)

Checker: Opus 5.5, 2026-09-29. Re-check of the five findings in `soso-review.md` against Revision 1, looking for
anything the revision broke.

**Verdict: APPROVE** (0 blocker, 0 major, 1 nit).

## Earlier findings

1. **Fixed (was major), `notebook.cells[2]`.** `pivot_table(` and `.plot(` now break after the open parenthesis
   with a 4-space hanging indent. At 390 (390 px iframe, notebook opened) cell [5] wraps as ordinary lines with no
   one-letter columns. The notebook JSON was re-run (`generated_by: scripts/run_notebooks.py`, image output, no
   errors) and the plot is unchanged, so `plot_alt` still holds.
2. **Fixed (was major), `record.select`.** `columns: [trader_unit, trade_price, trade_direction,
   contract_identification, settlement_date, trade_quantity_mw]`. The regenerated sample (`gridflow-sample`, same
   eight rows) leads with `trader_unit` and `trade_price`. Both are in view at 390, the frame runs through
   `trade_quantity_mw` at 1024, and through `sender_identification` at 1440. Every `trade_price` value in the frame
   matches silver (492.51, -61.02, 89.07, 306.54, 492.51, -61.02, 854.31, -97.64). `record.fields` follows the new
   frame order. The rendered guide shows the three key columns under "Identifies a row", then the other columns in
   frame order (`trader_unit`, `trade_price`, `trade_quantity_mw`, `timestamp_utc`, ...).
3. **Fixed (was nit), `chart_view.caption`.** It now reads "the mean of each start hour's eight 25 MW `Bid`
   contracts, and of its eight `Offer` contracts". That matches silver: n = 8 and 25.0 MW in all 240
   hour-direction groups for `EWIC_EG`, settlement dates 14 to 18. "`GL1_EG` carries the same prices here" is
   scoped and true (1920 of 1920 prices equal). The series artefact is unchanged and the build's digest check
   passes.
4. **Fixed (was nit), `record.fields`.** The sender and receiver lines now name the vendor fields
   (`senderIdentification`, `receiverIdentification`), and `resource_provider` names `resourceProvider`. Nothing
   repeats the frame.
5. **Fixed (was nit), `notebook.cells[1]`.** The two-column `.head()` output fits its box at 390, price included.

## New finding

1. **nit** · `page.notebook.cells[1]` · `df[["trade_direction", "trade_price"]].head()` shows five prices with
   nothing saying whose they are. They are `EWIC_EG` contracts for the 13 Sep 23:00 hour, but no column shows that,
   and the brief asks for a `.head()` of the key columns. Adding `trader_unit` (for example
   `df[["trader_unit", "trade_direction", "trade_price"]]`, three narrow columns) would identify the rows, if it
   fits at 390. Not blocking.

## Regression checks

- `gridflow-build --only elexon/soso` is green, `detect.mjs --json` returns `[]`, and the mirror is byte-identical
  to the vault note (`cmp`).
- The page block was re-read in full. Outside the revised fields nothing changed, and no local-data words, em
  dashes, middle dots or arrows were added.
- Screenshots after the revision (headless Chrome, my own server on 9742, now stopped): 1440 and 1024 full page;
  390 frame and guide, and 390 with the notebook opened. The hero, chart and key, raw feed, frame, guide, notebook
  cells [1] to [5], plot and related list are all clean, with nothing clipped or overlapping.
