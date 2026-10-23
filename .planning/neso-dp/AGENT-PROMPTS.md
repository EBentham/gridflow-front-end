# NESO overnight batches: standing instructions for writers and checkers

The seat's launch prompt names your role, the batch file, the package, its members, your port and anything to look
hardest at. Everything else is here. Paths: main repo `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end`;
the batch file names the front-end and vault worktrees.

## Read first, in full

1. The batch file (`.planning\neso-dp\BATCH-<batch>.md`): paths, worktrees, shared-worktree rules, rulings, risks.
2. `.planning\v5\author-brief.md` as it stands IN THE FRONT-END WORKTREE (it documents the template options: `values`,
   `y_min`, related package slugs, the `needs` rule, several requests per member, held members and held pages),
   including "Family pages".
3. `.planning\v5\review-rubric.md`.
4. `.planning\neso-dp\template-pass\REPORT.md`.
5. Worked examples: the NESO showcase pages (`demand-flexibility`, `eac-br-auction-results`, `aggregated-bsad`,
   `constraint-breakdown`) and pages already approved in your batch (the batch tracker lists them).

## Writer

Do the whole job the author brief describes for your package:
- Research from gridflow code (`connectors/neso_data_portal/`, `silver/neso_data_portal/`, `schemas/`, the registry),
  local silver read only (Polars, lazy, select columns), the ledger row in
  `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow\.planning\v0.22-FE-LEDGER.md` (tables, eligible and held, the
  question that holds each), and the canonical note.
- Write the `page:` block on the canonical note in the vault worktree (Edit tool, CRLF), plus body corrections the code
  proves. Mirror byte for byte into the front-end worktree's `vault\neso_data_portal\` and `cmp`.
- Generate the artefacts under the lead key; build with `--only neso_data_portal/<lead>`, no errors, detector `[]`
  (`node C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow-front-end/.claude/skills/impeccable/scripts/detect.mjs --json <page>`).
- Screenshots at 1440, 1024, 768 and 390.
- If the lead or member list in the manifest is wrong, say so in the report; never edit the manifest.
- Held members: one plain line each on why rows are not shown, from the ledger's question, no codes, no planning words.
- If the rows cannot support an honest page, recommend a hold with numbers.

Report: `.planning\neso-dp\<batch>\<slug>-author.md` (if a Write to that path is refused, write it with a Bash
heredoc): the evidence table; body corrections; anything unverified; open questions; template problems; a pasteable
"Defects" section. Final message at most 8 lines: build and detector status (or HOLD recommended), chart and window,
what the checker should look hardest at, any blocker, any gridflow or data defect.

Revisions come back to you by message: fix everything in the review, re-mirror, rebuild, detector, write
`<slug>-author-2.md` (then `-3`), end with a one-line summary.

## Checker

Inspection only. Bash only to read code, read silver and bronze with Polars (read only, lazy), run the build
`--only neso_data_portal/<lead>` in the front-end worktree, the detector, and screenshots. Write no file except your
review. Never commit, run ingest or a live API, or edit notes, pages or artefacts.

Then read: the writer's report; the canonical note diffed against `origin/master` in the vault worktree
(`git -C <vault worktree> diff origin/master -- 30-vendors/neso-data-portal/datasets/<slug>.md`); `cmp` the mirror;
the artefacts `site\hifi\data\{series,samples,notebooks}\neso_data_portal\<lead>*`; the built page
`site\hifi\data-sources\neso_data_portal\<slug>.html`; the ledger row. Check everything in the rubric against gridflow
code, local silver and the NESO docs the note quotes. Open the unfolded frame and the notebook output. Seat rulings in
the launch prompt or batch file are not findings unless inaccurate. Template limits listed under the batch file's
"Template follow-ups" are seat items, not findings.

Review: `.planning\neso-dp\<batch>\<slug>-review.md` (Bash heredoc if a Write is refused): the verdict (APPROVE or
REVISE), then numbered findings, each with severity (blocker, major, nit), field path, what is wrong, the evidence.
Final message at most 6 lines: verdict, counts by severity, one line per blocker or major. Re-checks come back by
message: write `<slug>-review-2.md` (then `-3`).

## Both

- Wrap every Chrome call in `timeout 60 ...` with `--timeout=15000 --virtual-time-budget=5000`; a true 390 view needs
  a 390 px iframe. Use your own port. **Hard rule:** start a server only in a way that records its PID, and stop only that PID. Never kill processes by image name or pattern (no `taskkill /IM`, `Stop-Process -Name`, `pkill python`, `killall`): that kills other agents' and sessions' builds, kernels and servers. Never stop the server on port 9670.
- Never write `rm -rf` (a guard blocks it). No git writes in either repo. Never run `gridflow-drift-check`, ingest,
  transform or a live API. Keep strictly to your own package's files; several agents share the worktree. A DuckDB lock
  or busy kernel means another agent: wait a minute and retry.
- Public copy: no local-data references, no planning words, no em dashes, no bare codes, British spelling, plain
  English; units and time stamps from code or the vendor, never memory.
- Scratch files go in your own subfolder of the scratchpad, named for your role and package (for example
  `<scratchpad>\dr-checker\`): agents share the scratchpad and generic names overwrite each other.
- Do not end your turn until your report or review file is written and your final message is ready: a turn that ends mid-task ("Now the detector...") stalls the batch.
- Agents keep ending their turn right after starting a server: a server started without redirecting its output keeps
  the tool call's pipes open, the call is pushed to the background, and the agent waits for it to exit (it never does).
  Start it in the Bash tool so the call returns at once and prints the PID:
  `python -m http.server <port> --directory <worktree>/site/hifi >/dev/null 2>&1 & echo $!`
  (the PowerShell form must add `-RedirectStandardOutput` and `-RedirectStandardError` to files). Never use
  `run_in_background` for a server, never end a turn while waiting on a background task, and stop only that PID.
