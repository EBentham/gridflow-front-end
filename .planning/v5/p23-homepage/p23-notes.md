claude-opus-5-5

# Phase 23 build: v5 theme, strata, chrome and homepage

**Status:** built, gates green, pushed, PR open into v5/site, not merged.
**PR:** https://github.com/EBentham/gridflow-front-end/pull/41 (v5/p23-foundation → v5/site)

## Commits (on b3b4892)
- d0ffd9a feat(site): v5 theme on tokens, with the strata
- 6392d0c feat(site): v5 chrome: masthead, nav and footer
- a0d4c93 feat(site): homepage rebuilt from R3-final in reflowing HTML

## Files changed
- site/hifi/assets/theme.css: rewritten on @import tokens.css, with no token values duplicated; strata, contacts, textures, components, rotors
- site/hifi/assets/site.js: skip link, masthead and nav, deep-stratum footer; data-* contract kept
- site/hifi/index.html: R3-final as reflowing HTML (about 125 KB, inline SVG art)
- site/hifi/assets/home.js (new): cable overlay at 1100px and up, splice at 1380px and up

## Gates (actual output)
- detect.mjs --json site/hifi/index.html → `[]`, exit 0
- htmlhint --config .htmlhintrc site/hifi/index.html → "Scanned 1 files, no errors found (24 ms).", exit 0
- lychee --offline --no-progress site/hifi/index.html → "22 Total, 17 Unique, 18 OK, 0 Errors, 4 Excluded", exit 0. It needs the build to run first; before the build, 8 generated data-sources pages were missing.
- uv run --system-certs --extra build gridflow-build --check → "OK: idempotent across 165 pages + 7 hubs + 0 dataset stubs.", exit 0. Content warnings come from the vault only.
- AA contrast (contrast.py): every pair passes. The worst is 4.57 (ink on clay, the CCGT and OCGT labels); the sea label is 4.61.
- CDP overflow probe: scrollWidth equals innerWidth at 360, 390, 768, 1024, 1100, 1280, 1380, 1440 and 1920. Cable paths: 0 below 1100px, 14 from 1100px, 31 from 1380px. The nav takes 1 row at 390px and 2 rows at 360px.

## Decisions (made autonomously; the owner was asleep)
- Landscape widened to 2240 units and bottom-sliced. Edge labels hide below 1100px, far labels below 700px.
- The phone has its own core sample (below 760px) and merit drawing (below 900px). Biomass and Nuclear labels are stacked, and CCGT/OCGT use knockout rects.
- Keyed index is absolute only at 1440px and up; below that it is a list.
- Gold grid starts at 1380px and the notebook goes side by side at 1440px, to avoid collisions at 1100 to 1280px.
- Cables are JS-only and wide-screen only; the layout does not depend on them.
- Inline SVG art keeps its palette hex values (generated drawing, not theme).
- The footer is a continuation of the deep stratum; masthead and footer seams use 1px negative margins.
- The browser pane was left alone, because other agents' tabs share it. Both of my http.servers are stopped.

## Copy awaiting approval (listed in the PR)
The "means / the point" line, the price-forecast aim line, the notebook intro, the residual-demand labels and the 1,000-draws line. The About copy is unchanged and is due a rewrite.

## Open issues
- The matplotlib figure's text is tiny on phones.
- Nav takes 2 rows at 360px.
- Code wells scroll sideways on phones.
- Bronze copy says "Each cable below…", but there are no cables below 1100px (only the vendor markers).
- Contrast headroom is thin on the clay labels (4.57).
- The generator (gen_home.py plus theme.src.css) lives only in scratch. Future edits to index.html and theme.css are hand edits unless it moves into the repo.
- Other pages are unstyled on this branch, as expected.
- Needs Bobbo's look on a real phone before merge.

## Screenshots (scratchpad\p23\)
final-390.png, final-768.png, final-1440.png (full page, via CDP); parts\final-390-*.png (segments)
