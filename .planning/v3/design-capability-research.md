# v3 design-capability research — making Claude Code produce non-AI-slop design

**Written:** 2026-08-02. Requested by user ("revamp the aesthetics; research skills/connectors/workflows that improve Claude Code's front-end design"). Web research + repo-state audit. No decisions taken — feeds a user gate.

## Headline finding — the current look IS the documented AI default

Anthropic's official **frontend-design skill** (the one they ship to fix "AI slop") names
three generic default looks that Claude converges on regardless of subject, and instructs
Claude to avoid them. **Default #1 is: "warm cream (#F4F1EA) + high-contrast serif +
terracotta accent."** That is, to a first approximation, this site's locked identity
(cream paper + Fraunces display serif + accent). Default #3 ("broadsheet: hairline rules,
zero border-radius, dense columns") overlaps with the rest of it.

Implication: the site doesn't read AI-generated because it's badly executed — it reads
AI-generated because the *identity itself is on-distribution*. Claude produces this exact
look unprompted, at scale, for everyone. Polish inside the same identity (= Direction A as
chosen at the Phase 12 gate) cannot remove that tell. The user's 2026-08-02 instinct
("still clearly AI slop") is validated by Anthropic's own documentation.

This reopens **D-V3-1 / the Direction A gate decision** — a user call, flagged to them.

> **GATE OUTCOME 2026-08-02:** user chose **FULL REBRAND** (identity fully reopened) and
> will **curate inspiration references** (Pinterest et al.) to seed the direction work.
> Recorded in CONTROL.md + STATE.md.

## Tooling landscape (what people actually use, filtered for this stack)

Stack filter: static HTML + one shared CSS + vanilla JS. React-world tooling (shadcn,
Magic UI, tweakcn, v0) is off-target and excluded.

### 1. Official `frontend-design` plugin (Anthropic) — NOT currently installed
- The single highest-leverage install (~277k installs). Loads as a skill whenever Claude
  builds UI.
- Interactive session, one-time:
  - `/plugin marketplace add anthropics/claude-code`
  - `/plugin install frontend-design@claude-code-plugins`
- Alternative: vendor the raw SKILL.md into `.claude/skills/frontend-design/` in this repo
  so all subagents inherit it without the plugin system (it's plain markdown).
- What it encodes (the load-bearing content):
  - **Two-pass method:** Pass 1 = a compact design plan *before any code* — 4–6 named hex
    tokens with rationale, ≥2 type roles (display/body/utility), 1-sentence layout concept
    + ASCII wireframe, and **one signature element** ("what this design will be remembered
    by"). Pass 2 = self-critique against the brief: *"Would I produce the same thing for a
    similar prompt? If yes, revise."* Only then code.
  - **Ground design in the subject's world** (for gridflow: the grid, market microstructure,
    settlement periods, SVG chart language — not generic "docs site" tropes).
  - **One justified aesthetic risk**, everything else quiet ("spend boldness in one place").
  - Structure must encode truth (numbered markers only for sequences, etc.) — rhymes with
    the site's honesty rules.
  - Avoid-list of the three generic defaults (above).
  - Quality floor: responsive, visible focus, `prefers-reduced-motion`.
- A community fork (Justin Wetch) measured a 75% win rate over the official skill after
  clarity edits; optional, official skill first.

### 2. Claude Cookbook — "Prompting for frontend aesthetics"
- Three strategies: (a) guide specific dimensions (typography / color / motion /
  backgrounds), (b) reference design inspirations, (c) explicitly name the defaults to
  avoid.
- Ships a reusable `<frontend_aesthetics>` system-prompt block + isolated dimension
  prompts (e.g. typography: "use weight extremes 100/900 not 400/600; size jumps 3x+").
  Useful raw material for agent briefs in phases 14–15.

### 3. The community-consensus workflow: a project DESIGN.md (design-system file)
The strongest repeated pattern across sources: output stops looking AI when a
**single source-of-truth design doc** exists before generation and is pasted into every
prompt/agent brief. Sections: Typography / Color palette (named roles + hex) / Spacing &
shape / Component conventions / Layout rules / **Do-not-use list** (explicit
anti-patterns) / Personality (3–5 adjectives + anti-examples) / Changelog.
- Negative constraints matter as much as positive ones.
- Test on single components before full pages; iterate *within* the system, never "make
  it more premium."
- Perfect fit for the Phase 14/15 staggered fleet: every Stream-C agent gets DESIGN.md in
  its brief → cross-page consistency without cross-page sameness of prose.

### 4. Visual iteration loop (screenshot → critique → fix → verify)
- Community standard is Playwright MCP; **not needed here** — this session already has the
  in-app Claude browser pane + `gridflow-serve`. Loop: edit → reload → screenshot/read_page
  → self-critique against DESIGN.md → fix → re-verify.
- Repo gotchas that bit in June (12-HANDOFF): single-threaded dev server wedges on rapid
  reloads; old preview surface wedged on screenshots (fall back to numeric evals:
  scrollWidth vs clientWidth); browser caches theme.css — cache-bust the `<link>` when
  verifying CSS.

### 5. Inspiration connectors
- **User-curated references — best fit, free.** Cookbook explicitly endorses referencing
  inspirations. Pinterest boards are fine: drop screenshots directly into chat (Claude
  reads images). 10–20 refs sorted into 2–3 vibe buckets is the ideal input; Claude mines
  them into token systems per direction.
  - Galleries worth trawling: godly.website, siteinspire, minimal.gallery, httpster.net.
  - Editorial/data exemplars relevant to this site's job: The Pudding (data-journalism
    charts), Stripe Press (editorial craft), Our World in Data (honest data docs), FT/
    Bloomberg visual-journalism energy pieces, Tufte CSS / gwern.net (austere docs).
- **Figma MCP** — official, bidirectional with Claude Code since Feb 2026. Only worth it
  if the user wants to sketch in Figma first. Requires connector auth (claude.ai connector
  settings; the design plugin's Figma MCP is currently unauthenticated in this
  environment).
- **Mobbin MCP** (official, May 2026): 600k+ real shipped screens, searchable from Claude
  Code (`npx -y mobbin-mcp auth` → `claude mcp add mobbin -- npx -y mobbin-mcp`).
  **Requires paid Mobbin.** Library skews product-app/mobile — weak fit for an editorial
  docs site. Skip unless already subscribed.

### 6. Already installed in this environment (no action)
- **design plugin**: design-critique, accessibility-review, design-system, design-handoff,
  ux-copy skills — use design-critique as a formal pass on exemplar candidates.
- **dataviz skill** — chart design system; relevant to charts.js/seeded-SVG restyling.
- **prototype skill** — "several radically different UI variations toggleable from one
  route": purpose-built for the N-directions exemplar pattern.
- **artifact-design skill** — for any artifact-based mockup sharing.

## Implications for the v3 plan (proposal, pending user gate)

1. **Reopen the direction decision** (user call — D-V3-1 / Phase-12 gate). Options:
   keep-A-and-deepen / re-explore with new directions / full rebrand.
2. If re-exploring: **inspiration → DESIGN.md → re-exemplar** loop:
   - User curates references (2–3 vibe buckets).
   - Build one DESIGN.md per candidate direction (tokens, type roles, signature element,
     do-not-use list) using the frontend-design skill's Pass-1 format.
   - Rebuild the exemplar pair (homepage + one flagship dataset page) per direction with
     the visual iteration loop; run design-critique + a11y passes.
   - Gate: user picks; winning DESIGN.md becomes the locked spec.
3. **Phases 14/15 fleet upgrade:** every Stream-C agent brief = winning DESIGN.md +
   cookbook aesthetics block + the page's content facts. Consistency comes from tokens,
   distinctiveness from the signature system — while voice-diagnosis's anti-sameness rules
   handle prose.
4. **Phase 13 mechanical sweeps are direction-independent** (honesty cut, facade examples,
   overflow/viewport fixes) — continue regardless; batches 1–3 already on main.
5. Distinctiveness levers specific to this site (from the skill's "ground in subject
   matter"): the energy-grid visual world (settlement periods, merit order, grid
   frequency, day-night demand shape) as the signature system; seeded SVG charts as a
   first-class identity element; typography with real contrast (weight extremes, scale
   jumps) whatever faces are chosen.

## Sources
- https://claude.com/blog/improving-frontend-design-through-skills
- https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md
- https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics
- https://www.justinwetch.com/blog/improvingclaudefrontend
- https://www.mindstudio.ai/blog/claude-design-avoid-ai-slop-design-system
- https://www.toools.design/blog-posts/best-mcp-servers-for-designers
- https://mcp.directory/blog/best-mcp-servers-for-design-2026
- https://designproject.io/blog/mobbin-mcp-design-inspiration/
- https://www.threads.com/@boris_cherny/post/DRDDB19kUZ5 (install commands)
- https://thomas-wiegold.com/blog/claude-code-frontend-design-plugin/
