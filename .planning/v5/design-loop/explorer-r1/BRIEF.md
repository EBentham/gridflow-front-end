# Explorer page, round 1 (shared brief for three designers)

You are one of three designers working in parallel on a new top-level page of the gridflow docs site: a
page about **gridflow explorer**, the owner's React app over his data platform. Your direction is in your
prompt. Read this brief fully, then the files it names.

Repo (READ ONLY except your own folder; never commit, branch or push):
`C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end` (`<repo>`). Design loop:
`<repo>\.planning\v5\design-loop\` (`<dl>`). Write ONLY inside `<dl>\explorer-r1\<N>\`.

## Read, in order

1. `<dl>\explorer-decisions.md`: Bobbo's asks and rulings (binding).
2. `<dl>\explorer-pack\EXPLORER-PACK.md`, the screenshots in `explorer-pack\shots\` (look at them) and
   `explorer-pack\code\`. Every fact comes from the pack or the screenshots. You may shorten; you may not add.
3. The locked sibling pages, so this one sits with them as one site: `<dl>\models-r2\models-r2.dc.html`
   (generator `models-r2\gen.py`) and `<dl>\arch-r2\arch-r2.dc.html` (`arch-r2\gen.py`). Reuse their
   masthead, nav, scenery and foot. Also the homepage notebook showcase Bobbo referred to: find the
   notebook window in the homepage source (`<repo>\site\hifi\index.html` on `origin/v5/site`, read with
   `git -C <repo> show origin/v5/site:site/hifi/index.html`) or the p23 homepage boards under `<dl>`.
4. `<repo>\DESIGN.md`, `<repo>\site\hifi\assets\tokens.css` (on `origin/v5/site` if absent locally), and
   `<repo>\.planning\v4\design-loop\SHARED.md` (board format and verification recipe).

## What Bobbo wants

- **Show the work.** Not detailed. Recruiters should come away knowing he is a full-stack developer who
  builds React front ends over a real Python data backend.
- **A brief section on the technologies**, front end and backend.
- **A screen demo in a window frame, like the homepage notebook**: real screenshots of the app (ruled:
  screenshots, not a rebuilt HTML copy, not a recording). Light screenshots in light mode and dark ones in
  dark mode (`<picture>` with a `prefers-color-scheme: dark` source). The shots are full-page tall: crop
  or scroll inside the frame as your direction needs; on the phone board make them legible (e.g. tap to
  enlarge, or a crop of the chart).
- A link to the public repo, and links to the Architecture and Models pages.

## Boards

`<N>-explorer.dc.html` at 1440 wide (whole page, masthead to foot) and `<N>-explorer-390.dc.html` (phone);
root height = `$preview` exactly. Wrap sections in `data-section="..."` (the picker crops by it).
Images: copy the shots you use (you may crop or re-encode them, e.g. to WebP or JPEG at sensible size)
into `<dl>\explorer-r1\<N>\explorer-shots\` and reference them as `explorer-shots/<file>` relative to the
board. Keep that folder under 6 MB.

## Rules

DESIGN.md is binding: no em dashes, eyebrows, middle dots, "→", italic headline words, stat strips, logo
walls, cards as the default container, planning words (planned, milestone, version numbers, wave, live,
coming, in progress), status badges, hire-me calls, licence line, local-data claims; AA contrast in both
themes; Red Hat Mono only for code, names and values. Describe only what exists (the pack). Tech names
are set as text, not brand logos.

## Verify, then report

Detector `node <repo>\.claude\skills\impeccable\scripts\detect.mjs --json <board>` returns `[]` on both
boards; no horizontal overflow at 390. Measure in your OWN browser tab (serve your folder on a port in
9700-9799, stop your server after); never kill or stop other processes. The harness blocks REPORT.md: your
report is your FINAL MESSAGE (under 200 words, first line your model ID), also saved as `<N>-notes.md`:
boards and heights, the idea in one sentence, which shots you used, new copy verbatim, detector results,
anything not done.
