claude-opus-5-5

**Board:** `arch-r1/1/arch-1.dc.html`, 1440 × 8518 (root = `$preview`). Static copy: `static/arch-1.html`. Generator: `gen/build.py`.

**Idea:** the page is the section. The drawing goes down once for the whole system, then a cable from its `gridflow` command goes down the same layers again for one row.

**Drawing:**
- Eight sources stand above ground as assets, with the eight-entry index above them.
- Below ground, each cable passes a joint bay (the connector), raw files with sidecars laid by date in bronze, a transformer at the silver boundary, and silver files. It ends on a view tap into a `gridflow.duckdb` busbar. The Elexon core also feeds the gold builder.
- Readers sit at the foot. gridflow_models taps silver directly and links to the Models page.
- The index sits level with each band.
- Two liberties with the pack: one transformer per source cable (the pack says one per dataset), and the gridflow_models tap draws from all eight cores (the pack names no datasets).

**Journey:** stops sit in their layers, with numbered joints on the cable. The cable splits into two versions after stop 4. Stop 5 pairs its claim with a timeline showing the as-of read (9.56) against `_latest` (110.00), plus the real SQL and results.

**Pack wording changed:**
- Labels lower-cased; curly apostrophes.
- DDL `CASE` rewrapped (whitespace only); stop 6's comment moved above its line.
- Outputs shown as tables.
- Index paths shortened.
- Where to look drops CI, run tracking and gridflow_models, which are linked elsewhere.

**New copy:** in `gen/new-copy.json`.

**Detector:** `[]`. In my browser tab at 1440: width 1440, 0 overlaps, 0 text outside 80–1360, nothing scrolls. Server stopped.

**Not done:** no 390 px CSS. Not rendered in the canvas.
