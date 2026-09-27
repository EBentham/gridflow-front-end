# Dataset page design loop: decisions with Bobbo (2026-09-27)

Picker: https://claude.ai/artifact/MpySKZLbpbe6VmCz4pcuzV · round-1 canvas https://claude.ai/artifact/7tkS1ydY8QWLvhC8LXbcsT

## Decision 1: overall layout (OWNER)

- **Base: A, "The section".** The page descends through the strata: chart and prose in topsoil, raw endpoint
  in bronze, schema and sample in silver, workbench call in gold.
- **Demo notebook:** a button at the bottom reveals a hidden notebook in D's style. The cells must paste
  into Jupyter and run as-is. Verify every cell before shipping.
- **No local-data references anywhere:** no "held locally", no local row counts, no local date ranges.
  History means what the vendor's API provides (e.g. "Elexon publishes from 2015"), only where evidenced.
  The same rule applies to "What it is".
- **Keep the raw vendor URL** in "how to get it".
- **Schema and sample rows: redesign.** Bobbo is not a fan of the round-1 formatting.
- **Foot:** the deep petrol band holds only related datasets. Remove the "Source on GitHub" and "MIT
  license" footer line.
- **Remove the caveats section** (A's "What to watch for"). Any caveat that matters for reading the chart
  goes in the chart caption instead.

## Decision 2: chart (OWNER)

- **A's chart:** in the topsoil with a key beside it. Signed series (interconnectors, pumped storage) stack
  above zero when positive and hang below when negative. Fuel codes the palette doesn't cover are drawn
  unpainted with distinct ink hatches, and khaki means only the vendor code OTHER.

## Decision 2b: facts and how to get it (OWNER)

- Keep A's for both: quick facts in the petrol hero under the one-liner; the raw feed and CLI in bronze and
  the workbench call in gold, plus the demo-notebook button.
