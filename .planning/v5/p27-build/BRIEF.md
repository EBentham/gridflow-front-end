# Top-page builds for the v5 cutover (shared brief)

You are one of three Opus builders turning a locked design board into a real, responsive site page for
tonight's cutover (`.planning/v5/CUTOVER-PLAN.md`). Your page and extra duties are in your prompt.

## Setup

- Work in your own worktree. First run `git fetch origin`, then
  `git switch -c v5/p27-<page> origin/v5/site`. The local `v5/site` is stale; `origin/v5/site` is the base.
- The design-loop folder (`.planning/v5/design-loop/`) exists on `main`. Read it from the main checkout at
  `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\v5\design-loop\`, or with
  `git show main:<path>`.

## Inputs

- **Your locked boards.** Desktop (1440) and phone (390) `.dc.html`, plus the generator and notes beside
  them. These are the spec: same content, same copy, same drawing, same order.
- **The built pages on `origin/v5/site`.** `site/hifi/index.html` is the reference for how a v5 page is
  put together: `<body data-page=".." data-root=".." data-screen-label="..">`, chrome (masthead, nav,
  foot) injected by `assets/site.js`, `assets/theme.css`, `assets/tokens.css`, strata grounds and scenery.
- **Rules.** `DESIGN.md` and `CLAUDE.md` (a11y minimums, conventions) are binding.
- **Standing checks:**
  - no licence line anywhere;
  - no local-data wording in site prose;
  - no planning words;
  - drawings get real top room in the viewBox;
  - no object is cropped at any width;
  - nothing clips or overlaps.

## Build

1. **One page, `site/hifi/<page>.html`,** responsive from 360 to 1920. Fold the desktop and phone boards
   into one layout with media queries. No zoom or scale tricks, no fixed 1440 root, and no masthead of the
   board's own: `site.js` supplies the chrome.
2. **Page CSS in its own file, `site/hifi/assets/<page>.css`.** Do not edit `theme.css`, `tokens.css`,
   `site.js`, `index.html` or another unit's page. The Explorer builder is the one exception, per its prompt.
3. **Images in `site/hifi/assets/img/<page>/`,** at a sensible size.
4. **Links** are relative within the site. GitHub links stay as the boards have them (the private
   gridflow-models repo included, per Bobbo).

## Verify (all must pass before you open the PR)

- `uv run --system-certs --extra build gridflow-build --check` passes.
- `htmlhint --config .htmlhintrc` on your page.
- `lychee --offline --include-fragments` over `site/hifi/**/*.html`, as CI runs it.
- `node .claude/skills/impeccable/scripts/detect.mjs --json <your page>` returns `[]`.
- AA contrast.
- Screenshots at 1280, 1440, 1920 and 390 wide, light and dark, looked at by you: nothing clipped, no
  sideways page scroll, text legible.
  - Serve on your own port in 9700-9799. Use your own headless Chrome or Edge, not the shared browser pane.
  - Stop your server after.
  - Never kill or stop processes you did not start.

## Ship

- Conventional commits, one concern each.
- Push your branch and open a PR into `v5/site` (`gh pr create --base v5/site`). Never merge. Never touch
  `main`.
- Your FINAL MESSAGE, under 150 words, first line your model ID:
  - the PR URL;
  - the files changed;
  - the gate results;
  - anything you could not match from the board, and why.
