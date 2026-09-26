# v4 design capability — delta since 2026-08-02, and the new loop

**Written:** 2026-09-25, control room (Opus 5.5). Builds on `../v3/design-capability-research.md`
(2026-08-02); read that for the base landscape. This file holds what changed, why output still reads
as AI, and the method Bobbo ruled for all UI design work.

## Ruling (Bobbo, 2026-09-25)

UI design (a new look, layout or design system) is made by **Opus 5.5 · high in an interactive chat
with Bobbo**: ~5 divergent variants on a Claude Design canvas → he audits, picks and mixes → iterate →
lock `DESIGN.md` + `tokens.css`. **No agents, no pipeline, no resourcing/tier ceremony until the lock.**
After the lock, the pipeline rolls the spec out (Sol executes, Opus reviews). Recorded in
`~/.claude/CLAUDE.md` §Cross-family split and `~/.claude/workflow-history.md`. This replaces the
v4-EFFORT-PLAN Phase 17/18 method.

## Where v4 actually stands (corrected 2026-09-25)

`main`'s STATE.md said Phase 17 was "waiting on user inspiration references"; the vault focus file and git
say otherwise, and the control room's first pass was misled by the stale STATE.md.

- **Phase 17 ran on 2026-08-02:**
  - five directions (electrified-landscape, ink-and-utility, night-grid, signal-white, the-descent);
  - **electrified-landscape, panorama composition (`landscape-v1.html`), picked and locked**;
  - Bricolage Grotesque + Hanken Grotesk + Red Hat Mono over petrol / chartreuse / olive;
  - signature: bronze/silver/gold drawn as geological strata.
- **Bobbo's verdict:** *"still does not look amazing and requires further refinement."*
- **Phase 18 (craft) never started.** Its scope is the 8-item refinement backlog in
  `DESIGN-electrified-landscape.md`: neutral drawing language, repeated section rhythm, conventional
  typography, cards as the default container, an under-used geology motif, no motion, nothing yet
  uniquely gridflow.
- **All of it sits on the UNMERGED branch `chore/v4-planning-wip`** (85c7b4f, 2026-08-15): five
  `DESIGN-*.md`, `INSPIRATION-HANDOFF.md`, `site/hifi/v4-tiles/` (8 HTML tiles).

The lesson: August did the "five directions and pick" half, then handed the craft half to a pipeline
phase that never ran. The loop below is the missing half, done interactively.

## The loop (how the design chat runs it)

- **Round 1 — start from August, not zero.** Put `landscape-v1` on the canvas as the baseline, plus five
  new homepage first screens (1440 wide, first screen + the next section).
  - Three work inside electrified-landscape, each attacking the refinement backlog a different way.
  - Two are wildcards that test whether the direction itself is the problem.
  - Bobbo's first reaction decides refine vs reopen.
  - Write each variant against its own brief. Five variants from one prompt collapse into five flavours
    of one idea. If round 1 still converges, the fallback is parallel Opus 5.5 spawns with independent
    briefs: still Claude and still Bobbo's loop, not the pipeline.
- **Content is real.** Current homepage copy and the real FUELHH numbers from `site/hifi/index.html`.
  Honesty rules hold: no invented stats, no fake-live, no KPIs, no hire-me CTAs.
- **Bobbo's input:** likes, dislikes and mixes, as canvas comments or chat. Dislikes are as valuable
  as likes; they become the do-not-use list.
- **Mix by system, not by pixel.** "B's type + D's palette" works; stitching B's header onto D's body
  makes Frankenstein pages. Flag clashes rather than forcing them.
- **Round 2 — blends.** 2–3 directions, each as home + one flagship dataset page + a 390 px phone view.
- **Round 3 — lock.** One direction →
  - `DESIGN.md`: palette roles + hex, type roles + scale, layout rules, component conventions, chart
    language, personality, do-not-use list;
  - `tokens.css`;
  - **the winning home + one flagship dataset page written as real repo HTML/CSS (the exemplar).**
    Canvas artboards are `.dc.html` mockups, not site code. Without a real exemplar, Phase 19's executor
    has to reproduce the look from prose and screenshots, which is exactly where fidelity leaks.
  - Mirror `DESIGN.md` as a Design System artifact (browsable). **The repo file is canonical, because
    Codex cannot read claude.ai.**
  - Update the repo `CLAUDE.md` "Locked decisions" line, which still names cream + Fraunces + Inter.
  - Then Phase 19 roll-out goes to the pipeline.
- **Explorer round:** decoupled from the site lock; the explorer's stack and dashboard register are the
  tighter constraint.
  - 3–5 variants of the wind forecast view (quantile fan, actuals overlay, metrics).
  - Then lock the explorer's `DESIGN.md` + tokens + Recharts theme; solar reuses it.
  - It must land before the wind milestone's explorer unit, which comes after the model work.
  - Run it after the site loop rather than in parallel, so Bobbo's attention isn't split.
- Keep a short round log (tried / kept / rejected) so later rounds don't circle back.

## Why the output reads as AI

**1. The site's identity sits on the model default.** Anthropic's frontend-design skill (updated
2026-09-03) now names five default looks, up from three. Live site, checked 2026-09-25, hits look #1
(warm cream + high-contrast serif + accent) and nearly all of look #5, "template chrome". These are
the seed of the do-not-use list:
- one italic accent phrase in the headline ("*energy data.*");
- tracked ALL-CAPS eyebrows above headings ("A PERSONAL RESEARCH PLATFORM…", "WHAT'S HERE");
- middle-dot meta strings everywhere ("GB GRID · 1–5 AUGUST 2026", "01 · ARCHITECTURE",
  "EX · Elexon", "1 shipping · 4 planned");
- "→" appended to links and CTAs;
- a big-number stats strip (7 / 165 / 4 / 17y / 3);
- 01/02/03 numbered cards on content that isn't a sequence ("Three things to explore.");
- mono micro-labels;
- terse one-word period headlines ("Pipeline." "Vendors." "Forecasts.");
- Inter in the type stack (on both Anthropic's and OpenAI's avoid lists).

**2. The explorer has no design system.** It runs default Recharts on near-black, a cousin of look #2
(Aug 15 screenshot, `gridflow_explorer/docs/screenshots/generation-mix.png`):
- purple default accent underline;
- ISO-8601 tick labels ("2026-08-09T07:00:00Z");
- y-axis with no unit;
- 11 stacked series in similar-lightness, muddy hues (gas vs other barely separable);
- default radio inputs;
- dead space beside a fixed-width chart.

**3. The executor is the weaker designer.** Design Arena, read live 2026-09-25:
- **Website board:** Opus 5.5 #1, Fable 5.1 #7, GPT-6 Astra (xhigh) ~#16, GPT-6 Sol absent from the
  top 17.
- **Data-viz board:** Fable 5.1 1359, GPT-6 Sol 1356, Muse Spark 1.2 1356, Kimi K3 1355, Opus 5 1347.
  Effectively a tie at the top.
- Community A/Bs of the GPT-5.6 generation agree: Sol is the cheaper coder and the worse designer.
- Caveat: arenas score one-shot generation. That is a good proxy for identity work and a weak one for
  spec-driven roll-out, which is why the ruling hands identity to Opus and roll-out to the pipeline.

**4. Codex had no design guidance.**
- The design skills lived only in this repo's gitignored `.claude/skills/`.
- `~/.codex/skills` was 100% GSD.
- OpenAI added a curated `frontend-skill` to openai/skills on 2026-03-20 and removed it on 2026-04-23;
  only `figma-*` skills remain, so the install line in OpenAI's GPT-5.4 frontend blog is dead.

**5. Nobody looked at pixels.** Plan and diff reviews read code. Design QA was implicitly Bobbo's
eyeball, which on a busy weekend means nobody's.

**6. The craft half never ran.** A direction was picked on 2026-08-02, but Phase 18's refinement was
queued as pipeline work and never started. Its output also never reached `main`, so later sessions read
a stale "waiting on references" state. See "Where v4 actually stands" above.

## Setup done 2026-09-25 (control room)

- **frontend-design** re-vendored from anthropics/skills (2026-09-03 version, 71 lines + LICENSE.txt).
  The previous copy was the untouched June upstream (claude-code@423563cf).
  - Installed in this repo's `.claude/skills/`, `gridflow_explorer/.claude/skills/` and
    `~/.codex/skills/`, so Sol sees it.
- **impeccable kept at 4.0.4** in this repo and added to the explorer (4.0.4).
  - 4.3.1 (2026-09-09) was installed, then rolled back the same hour. It replaces the Node scripts,
    including `scripts/detect.mjs`, with an engine binary.
  - The vault's standing rule runs `node .claude/skills/impeccable/scripts/detect.mjs --json <files>`
    before showing any UI. 4.3.1 would break that gate.
  - 4.3.1's SKILL.md runs `scripts/impeccable context` (the engine, downloaded on first run) at the start
    of every session. Its Windows launcher says it is untested on real Windows, and Avast sandboxes new
    executables here.
  - Its hooks, four unpinned agents and `settings.json` were never installed.
  - 4.0.4's detector smoke-tested OK on 2026-09-25: it flags `overused-font: Fraunces` on the current
    homepage.
- **taste-skill:** unchanged. Site only; its own header excludes dashboards.
- Nothing committed; `.claude/` is gitignored in both repos.

## Named unknowns (roll-out phase, not the design loop)

1. **Pipeline eyes.** Can Sol under `codex exec` use Codex's bundled `browser` plugin to screenshot
   pages? If not, fall back to a small Playwright script: Node 22 is installed, Playwright browsers are
   not, and Avast TLS may need `NODE_EXTRA_CA_CERTS`. This gates the proposed **design-fidelity lens**:
   diff review of UI units gets screenshots at 1440/768/390 + `DESIGN.md` + the `design:design-critique`
   rubric. Proposed as a zone unit; not built.
2. **GPT-6 Sol website quality.** Not yet on the Website board. It matters only for roll-out, where the
   locked spec carries the taste.
3. **OpenAI's "low/medium reasoning gives better frontends"** was a GPT-5.4 claim. Test it on Sol at
   roll-out; don't adopt it as a rule.
4. **impeccable 4.3.1 upgrade.** Take it only after its Windows engine is shown to run here and an
   engine-based `detect` replaces the `detect.mjs` gate.

## Tool verdicts

- **Claude Design** (claude.ai/design; launched 2026-04-17 on Opus 4.7; research preview on Max):
  **use it** for the variant canvas and the Design System mirror. It adds canvas, comments and handoff,
  not better generation than the Opus 5.5 seat. This account has the Design + Design System types and
  no design systems yet.
- **In-app browser pane:** the design chat's eyes. No Playwright MCP needed for the loop.
- **Figma MCP:** skip unless Bobbo sketches in Figma. It is also unauthenticated here (claude.ai
  connector settings).
- **Mobbin MCP:** skip (paid, app-skewed).
- **shadcn / Tailwind:** skip by default. The explorer stack is locked; a CSS-custom-property token layer
  plus a Recharts theme covers the gap. Unlocking it is Bobbo's call.
- **21st.dev Magic / v0 / Stitch:** skip. React-only or marketing-component heavy; wrong for a quiet
  docs site.
- **`Enixes/astra-frontend-design`** (community Codex skill): optional, unvetted.
- **OpenAI hard rules worth borrowing** for the do-not-use list:
  - no cards by default;
  - no generic SaaS card grid as the first impression;
  - ≤2 typefaces and ≤1 accent without a reason;
  - no default stacks (Inter, Roboto, Arial, system).
  - **Don't borrow** their "use gradients, not flat backgrounds" or "ship 2–3 motions". Both conflict
    with Anthropic's guidance and this site's quiet values.

## Sources

- https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md (2026-09-03)
- https://www.anthropic.com/news/claude-design-anthropic-labs
- https://www.designarena.ai/leaderboard/website · https://www.designarena.ai/leaderboard/data-viz (read 2026-09-25)
- https://botmonster.com/ai/gpt-5-6-sol-reddit-reaction/ · https://expo.dev/blog/fable-5-vs-gpt-5-6-sol-expo-apps
- https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4
- https://github.com/openai/skills (commits 2026-03-20 add / 2026-04-23 remove curated frontend-skill)
- https://github.com/pbakaus/impeccable/releases (skill-v4.3.1, 2026-09-09)
- https://github.com/Leonxlnx/taste-skill · https://github.com/Enixes/astra-frontend-design
