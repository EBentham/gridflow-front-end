claude-opus-5-5

**Boards:** `1-explorer.dc.html` 1440x3076, `1-explorer-390.dc.html` 390x3454 (root = `$preview`).

**Idea:** one app window in the notebook frame rises out of the field with five working tabs, then two tech columns, one cable (browser, FastAPI, `GridflowClient`, DuckDB forking to silver and gold) and real lines of the market index price view.

**Shots:** catalogue, generation-mix, system-prices, historic-mix, demand-outturn, light and dark (PNGs as shot, 3.0 MB). The phone crops each at 69%, and a tap opens it full size.

**New copy:** all verbatim in `copy-new.json`; headline "Browsing everything gridflow collects". The Architecture and Models lines are shortened from those pages' ledes, not the pack.

**Checks:** detector `[]` on both boards. Tab clicks tested in headless Chrome.

**Not done:** the tab script may not run in the canvas (Catalogue is authored as the resting state). Headless Chrome can't go below 500 px wide, so the 390 no-overflow check is an element-rect sweep. Shots are not re-encoded (no image library). "Explorer" is added to the nav here only.
