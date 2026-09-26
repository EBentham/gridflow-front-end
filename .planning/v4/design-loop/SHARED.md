# Round 3 shared brief: redesign the gridflow homepage (read fully before designing)

You are one of three designers working in parallel on the same homepage, each from a different brief.
Your own brief is in your prompt. This file is the context all three share.

Paths:
- Repo: `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end` (READ ONLY for you; never edit, commit or push)
- Scratch root: `C:\Users\Bobbo\AppData\Local\Temp\claude\C--Users-Bobbo-OneDrive-Desktop-Python-gridflow-front-end\ac992240-285c-4da8-b171-cc11c165a9de\scratchpad`
  (below: `<scratch>`). Write ONLY inside your own folder `<scratch>\r3\<your-folder>\`.

## The site and the owner

gridflow is a documentation site for Elliot Bentham's (Bobbo's) open-source ETL pipeline for UK and
European power, gas, weather and carbon data, plus a probabilistic modelling repo. It is a portfolio
piece for recruiters in energy trading (power first). It must work as real documentation, not a showpiece.
Owner's steer: modern, tech-oriented, clean and elegant, very appealing visually. Not a SaaS product.

## Where the design loop is (what Bobbo has said)

- Round 1 (six directions): he picked **B, "Borehole"**: petrol sky hero with a drawn landscape strip
  (ridge, wind turbines, lattice pylons, catenary), then the page drawn as geological strata (gold, silver,
  bronze tinted bands with textures and wavy contact lines), content sitting in the layer it belongs to,
  the GB fuel mix drawn as a core sample. He did NOT like the literal borehole (a drill column down the
  left margin).
- Round 2 (five strata variants, B1 to B5): "None of those 5 designs look amazing, but I like the general
  colours, fonts, design style." So: keep the palette, type and the drawn-landscape + strata language; the
  execution must get markedly better. Treat this as the craft round.
- **New steer (this round):** lean into the energy theme: renewables, net zero, electrification, data
  centres, the emerging trends of electricity markets (storage and batteries, interconnectors, flexibility,
  offshore wind, solar, EV, negative prices, demand growth from compute). Work these themes into the design.
- He wants to see his **existing homepage** redesigned in this style: all of its content, not a teaser.

Reference files (look at them, and read the source of the ones you learn from):
- `<scratch>\canvas\project\B-borehole.dc.html` (the round-1 pick) and `B1-open`, `B2-block`, `B3-dipping`,
  `B4-quarry`, `B5-quiet` `.dc.html` in the same folder (round 2). `<scratch>\gen_r2.py` holds the reusable
  SVG pieces (landscape strip, pylon path, fuel-mix core sample, strata patterns).
- `<repo>\site\hifi\index.html`: the CURRENT homepage. This is your content source.
- `<repo>\.planning\v4\design-capability-research-2026-09-25.md` section "Why the output reads as AI".
- The frontend-design skill: `<repo>\.claude\skills\frontend-design\SKILL.md`. Read it and follow it.

## Design system you must keep

Colour (hex, roles):
- `#155A6E` petrol: sky, deep fields, footer. `#3E8C97` horizon: ridges, wind. `#AFC64E` chartreuse: the
  energised land, primary accent, solar. `#66793B` olive: links, deep land, imports. `#1C2B22` ink: text.
  `#F6F4EC` daylight: light reading ground. `#C77E3C` clay: gas / CCGT. `#A39A6A` khaki: other.
  `#5d6a55` muted text. `#DFDACA` rule. Medallion: bronze `#A5713C`, silver `#9FADAB`, gold `#C2A14A`
  (tints used in B: gold `#E9DDAF`, silver `#DCE2DF`, bronze `#E2CDB3`).
- The scenery IS the categorical palette: wind = horizon, solar = chartreuse, gas/CCGT = clay,
  nuclear = petrol, imports = olive, other = khaki. Pick biomass and any new series (storage, data centres)
  from the same world and state your choice.
- You may add at most one new colour, only if the theme demands it, and say why.

Type: Bricolage Grotesque (display; it has opsz 12..96 and wdth 75..100 axes, use them), Hanken Grotesk
(body), Red Hat Mono (code, table names and dataset codes only; not as decorative micro-labels).
Load from Google Fonts css2 only.

## Content: everything on the current homepage, real

Take the copy from `site/hifi/index.html`. Sections, in its order: hero (headline, lede, two CTAs), the GB
grid snapshot (FUELHH mix), scope facts, three pillars (Pipeline / Vendors / Forecasts), architecture
preview (bronze / silver / gold with their file and table names), catalogue preview (seven vendors with
dataset counts, cadences and a sparkline each), models (five rows: one shipped, four planned F6 to F9),
query examples (DuckDB SQL / Python client / Pandas, the exact code), About (bio, four contact links,
skills list). You may reorder, merge, restructure and re-present sections, and fix punctuation (the
current copy uses em-dashes; replace them with commas, colons or parentheses). You may NOT invent facts.

Real numbers you can use:
- FUELHH mix, 1 to 5 Aug 2026, mean of 240 settlement periods: Wind 6,408.2 MW (29%), CCGT 5,639.3 (26%),
  Nuclear 3,589.4 (16%), Imports 3,174.4 (14%), Biomass 2,350.2 (11%), Other 929.2 (4%). The slices sum to
  22.09 GW; show 22.1 GW (the live page's "22.0" is a rounding slip).
- Scope: 7 vendors, 165 datasets, 4 markets, 17 years of history, 3 pipeline layers.
- Vendor rows: Elexon BMRS 33 datasets 5 min; ENTSO-E 49, 15 min; ENTSO-G 33, daily; GIE AGSI and ALSI 8,
  daily; Open-Meteo 6, hourly; NESO 33, 30 min; NESO Data Portal 3, 30 min (sum 165).
- Any curve: `<repo>\site\hifi\data\chart-series.json` (`series[<vendor>/<dataset>].values`, 120 points,
  mostly 1 to 5 Aug 2026). Good ones for this theme: `neso_data_portal/historic_generation_mix` (gas_pct,
  Jan 2009 to Aug 2026, 120 sampled half-hours, 18% to 55%: the transition in one line),
  `neso/carbon_intensity` (gCO2/kWh, 35 to 179), `elexon/system_prices` (system sell price, GBP/MWh,
  -39 to 179: real negative prices), `elexon/ndf` (national demand forecast MW, 15.3 to 28.2 GW),
  `entsoe/wind_solar_forecast`, `openmeteo/historical_wind`. Every chart states dataset, unit, window.
  Caveats: each series is the MEAN across the rows a dataset returns per timestamp; never label
  `elexon/fuelhh` as total output (it is a per-row mean). Downsampled: timings are approximate; describe
  only what the drawn line shows, never a cause you have not verified.

## Honesty rules (hard)

- No invented stats, no fake-live framing (no "live", "now", timestamps, pulsing dots, "X min ago"),
  no KPIs or uptime badges, no hire-me CTAs, no testimonials, no author photo.
- The energy-trend themes (data centres, batteries, EVs, interconnectors, net zero) may appear as
  DRAWING and as framing, but gridflow holds no data-centre, battery or EV dataset: never imply it does,
  and never quote a trend number that is not in the repo. If you want a sentence of framing copy, keep it
  factual and generic, and list it in your report as NEW COPY for Bobbo to approve.
- Nothing internal: no tier codes, "scope", "milestone", "queued", "eligible", "v4", "branch" in visible copy.

## Do-not-use (AI tells and Bobbo's dislikes)

Tracked all-caps eyebrow labels above headings; middle-dot meta strings ("A · B · C"); "→" appended to
links or buttons; a big-number stats strip; 01/02/03 numbering on things that are not a sequence;
one-word period headlines ("Pipeline."); an italic or coloured single word in a headline; Inter, Roboto,
Arial, Fraunces, system stacks; cards as the default container, identical rounded cards, soft grey shadows;
gradient washes; glow/bloom; leaves, foliage, globes, hands, cartoon people; hexagons; purple;
colored border-left callouts; cream + serif; the literal borehole / drill column.

## The .dc.html artboard format (the canvas renders exactly this; rules fail silently)

Write ONE file: `<scratch>\r3\<your-folder>\<Name>.dc.html`, the whole homepage, 1440 px wide, height
whatever the page needs (keep it at most 7800 px). Skeleton:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Short name</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="https://fonts.googleapis.com/css2?family=...&amp;display=swap" rel="stylesheet">
<style>
body{margin:0}
/* your classes */
</style>
</helmet>
<div class="root" style="width: 1440px; height: 6200px; overflow: hidden; position: relative">
... the page ...
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{"$preview":{"width":1440,"height":6200}}'>
class Component extends DCLogic {
renderVals() { return {}; }
}
</script>
</body>
</html>
```

Rules: keep the `support.js` line exactly; root element has a FIXED width/height equal to `$preview`;
close every non-void element and quote every attribute; in SVG write `<path ...></path>`, never `<path/>`;
no `{{` anywhere in your markup or CSS (it is the template-hole syntax), and avoid `}}` (write `} }`);
no other scripts, no `<iframe>`, no `data:` URIs, no external images (draw everything as inline SVG);
fonts only via the Google Fonts `<link>`. `&` in URLs is `&amp;`. SVG `<pattern>`, `<clipPath>`,
`vector-effect`, `pathLength`, CSS `@keyframes` all work. Use real `<a href="#">`, `<nav aria-label>`,
`<main>`, headings in order, `role="img"` + `aria-label` on meaningful SVG, `aria-hidden` on decorative.
The query tabs can be static (show the SQL panel selected, the other two as tab labels).
One authored motion moment is allowed (CSS only, respect `prefers-reduced-motion`).

## Verify before you report

1. Detector (must return `[]`): make a plain copy
   `sed -e 's#<script src="./support.js"></script>##' -e 's#</\?x-dc>##g' -e 's#</\?helmet>##g' -e '/data-dc-script/,/<\/script>/d' in.dc.html > <your-folder>\static\<Name>.html`
   then from the repo root: `node .claude/skills/impeccable/scripts/detect.mjs --json <that .html>`.
   Fix every finding.
2. Layout: if you have browser tools, serve `<your-folder>\static` with
   `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.venv\Scripts\python.exe -m http.server <free port 9500-9599> --directory <folder>`
   in the background, load the page at 1440 wide and check for overlaps and clipping, measuring element
   rects with JavaScript (screenshots can stall; numeric checks are more reliable), then stop the server.
   If you have no browser tools, check your absolute-positioning arithmetic by hand and say so.
3. Self-critique against the frontend-design skill's list of default looks and this file's do-not-use
   list; remove one accessory before you finish.

## Report back (under 250 words)

File path and page height; the one memorable idea; how the energy theme shows up; every NEW COPY line
(verbatim) for approval; any data series used (dataset, unit, window); detector result; how layout was
verified; anything you could not do.
