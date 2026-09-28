# v5 cutover: visual QA

Reviewer: Opus 5.5 (inspection only), 2026-09-28. Build: `scratchpad/integ/site/hifi`, served on 127.0.0.1:9722.
Captures: headless Chrome over DevTools. Widths 1280, 1440 and 1920 (first screen at 900 px tall, plus the full page) and 390 (full page). Each page was also measured for `scrollWidth`, rendered font size (SVG text scaled by its CTM), clipping, broken images and nav/footer text.

Paths: `S` = `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\a0012501-ff9a-440a-b654-cec67ac10bcf\scratchpad\qa`. First screens are in `S\shots\<page>_<w>_top.png`. Full pages are split into `S\slices\<page>_<w>_NN.png` (ignore `S\shots\*_full.png`: some of those came from a stalled load and are cut short).

**Checked and clean everywhere:** no sideways scroll on any page at any width (`scrollWidth` equals the viewport on all 56 page/width pairs); no broken images or missing assets (the only 404 is `/favicon.ico`); fonts load; the primary nav is the same on all 14 pages (Home, Data sources, Architecture, Models, Explorer, About), with the active page marked; no licence line in any footer; the content column centres at 1920 (it starts at 240 px and is 1440 px wide, so it runs from 240 to 1680).

Coverage: I looked at every first-screen shot at 1280, 1440 and 1920, every 390 slice, and every 1280 slice. At 1440 and 1920 I looked at the slices for all five top pages and all three hubs, and at a sample of the pilot-page slices (the hero, chart, raw feed, schema and footer bands of `system_prices`, `bmunits_reference`, `physical_flows`, `demand-outturn` and `fuelhh`). The measurements for the 1440/1920 slices I did not open show no overflow, clipping or small-text changes compared with the ones I did.

## Blocker

**B1. The hero drawing breaks on every hub and dataset page at phone width.** Affects `data-sources.html`, the three hubs, the five pilot pages and the blank page, and therefore every dataset page under 700 px. The drawing shrinks to a 76 px strip in the left half of the screen, with a blank petrol area to its right and labels at 4 to 9 px.
Cause: the home page's phone rule in `theme.css` (the `@media (max-width: 699.98px)` block, around line 218), `.landscape svg { … height: auto; aspect-ratio: 2240 / 434; margin-left: -45.35%; }`, also matches `figure.landscape.ds-land` and `figure.landscape.hub-land`. The `.ds-land`/`.hub-land` rules reset `width` but not `aspect-ratio` or `margin-left`. Measured at 390: svg 390×75.6 px, margin-left −176.9 px, aspect-ratio 2240/434 (at 740 the values are correct: 740×278, margin 0, aspect auto). The fix is to scope that phone rule to the home figure, or reset `aspect-ratio: auto; margin-left: 0` on `.ds-land svg` and `.hub-land svg`.
Shots: `S\slices\ds-elexon-system_prices_390_00.png`, `ds-elexon-fuelhh_390_00.png`, `ds-entsog-physical_flows_390_00.png`, `ds-elexon_390_00.png`, `data-sources_390_00.png`, `ds-elexon-freq_390_00.png`.

## Major

**M1. Data sources, "Find a dataset" chart: axis text too small at every desktop width.** The imbalance-price chart's tick and axis labels render at 8.9 px at 1280 and 10.1 px at 1440/1920 (14 ticks plus the axis note). The 900-unit wide chart is scaled into a 618 px column. Shot: `S\slices\data-sources_1280_01.png`.

**M2. Home and Data sources give different numbers for the same catalogue.** Home says "165 datasets"; Data sources says "149 datasets". Per vendor: ENTSO-E 49 (home) vs 36; GIE 8 vs 6; ENTSO-G 33 vs 32 (the ENTSO-G hub also says 32); Elexon "every 5 minutes" vs "half-hourly". Explorer says "eight public sources" where home and Data sources say "seven vendors". Home's silver/gold examples (`silver.fuelhh`, `silver.da_prices`, `gold.gb_dispatch`, `gold.daily_brief`) don't match the naming shown on Architecture and the hubs (`silver_elexon_system_prices`, `gold_uk_imbalance_context`). Shots: `S\shots\index_1280_top.png`, `S\slices\index_1280_02.png`, `S\slices\data-sources_1280_00.png`, `S\slices\explorer_1440_00.png`.

**M3. Architecture at 1280: the section drawing's legend and labels shrink below readable size.** The legend's file links (`connectors/base.py`, `.meta.json`, CLI verbs; about 85 runs) render at 11.1 px, and the legend body text at 12 px. The drawing's SVG labels render at 10.2 px (`silver_{source}_{dataset}`) and 11.5 to 11.9 px (the timeline's `20260908T214403Z` and `system_sell_price 9.56`). At 1440/1920 the same text renders at 12.5 px, and one SVG label at 11.5 px. Shots: `S\slices\architecture_1280_00.png`, `architecture_1280_01.png`, `architecture_1280_04.png`.

## Minor

- **m1. Home at 390:** the landscape labels render at 10.9 px ("data centre", "gas-fired power station", "converter station"). Shot: `S\slices\index_390_00.png`.
- **m2. Footer differs within the dataset family.** The pilot pages end on the related-datasets band with no site footer (by design, DESIGN.md anatomy item 6). The blank page (`freq.html`, `main.ds-blank`) gets the full site footer, because `site.js` only drops the footer when `main` has class `ds`. Shots: `S\slices\ds-elexon-freq_1920_00.png` vs `ds-elexon-system_prices_1280_02.png`.
- **m3. Explorer, "Market index price" frame:** the crop starts part-way through a line of text, so the top line is sliced in half (1280: image 926 px wide in an 846×522 window). Live capture: `S\shots\live_explorer_1280.png`. (In the full-page slices this frame looks empty; that is a lazy-load artefact of off-screen capture. The image is served with a 200 and renders when scrolled to.)
- **m4. Physical flows chart x-axis (1280/1440):** the first tick has no label, and "21 Sep" and "22 Sep" crowd together, with "22 Sep" running past the end of the axis. Shot: `S\slices\ds-entsog-physical_flows_1280_01.png`.
- **m5. Sample tables treat extra columns in two ways.** `fuelhh` ends in a "…" column; `system_prices`, `physical_flows` and `bmunits_reference` run their last column into the box edge (`price_deri`, `data_provi`, `national_grid_bm_unit`) and scroll sideways. Shots: `S\slices\ds-elexon-fuelhh_1280_01.png`, `ds-elexon-system_prices_1280_01.png`.
- **m6. Command and code boxes cut their text at the right edge** at every desktop width, 1920 included (`system_prices` and `physical_flows` at 1920: `S\slices\ds-elexon-system_prices_1920_01.png`, `ds-entsog-physical_flows_1920_01.png`). Examples: the `# bronze; the end …` comments in each raw-feed box and the NESO hub's notebook line (`…historic_generation_mix", start`). They scroll sideways, but the screenshots were taken with scrollbars hidden and overlay-scrollbar browsers give no cue. Shots: `S\slices\ds-elexon-fuelhh_1280_01.png`, `ds-neso_data_portal_1280_01.png`.
- **m7. The Data sources headline at 1280 leaves "it" alone on the third line.** Shot: `S\shots\data-sources_1280_top.png`.
- **m8. Mono and table text sits at 12 to 12.5 px across desktop pages** (code chips, schema tables, legend codes: about 40 runs on Models, 70 on the Elexon hub, 370 on Architecture). This is below the 13 px bar but reads fine in the shots, so it is noted rather than ranked higher.
- **m9. Physical flows chart key at 1280:** "ITP-00090" breaks across two lines at the hyphen. Shot: `S\slices\ds-entsog-physical_flows_1280_00.png`.
- **m10. BM unit register chart:** the "BM units" axis title floats alone in the middle of the plot, far from the short bars and the value labels (1440/1920). Shot: `S\slices\ds-elexon-bmunits_reference_1920_00.png`.

## Per page

- `index.html`: clean apart from M2 (counts) and m1 (10.9 px labels at 390).
- `data-sources.html`: B1 at 390, M1 chart axis, M2 counts, m7 orphaned "it".
- `architecture.html`: clean apart from M3 at 1280 (and m8).
- `models.html`: clean.
- `explorer.html`: clean apart from m3 (crop through text) and M2 ("eight sources").
- `data-sources/elexon.html`: clean apart from B1 at 390.
- `data-sources/entsog.html`: clean apart from B1 at 390.
- `data-sources/neso_data_portal.html`: clean apart from B1 at 390 and m6.
- `data-sources/elexon/system_prices.html`: clean apart from B1 at 390, m5 and m6.
- `data-sources/elexon/fuelhh.html`: clean apart from B1 at 390 and m6.
- `data-sources/elexon/demand-outturn.html`: clean apart from B1 at 390 and m6.
- `data-sources/elexon/bmunits_reference.html`: clean apart from B1 at 390, m5 and m10.
- `data-sources/entsog/physical_flows.html`: clean apart from B1 at 390, m4, m5, m6 and m9.
- `data-sources/elexon/freq.html` (the blank page): clean apart from B1 at 390 and m2 (footer).
