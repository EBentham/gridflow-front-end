# Agent prompt templates for dataset-page batches

These are the prompts that worked on the Elexon, ENTSO-E and GIE batches, as of 29 Sep.

**How to spawn:**
- Launch every agent with `subagent_type: claude`, `model: opus` and `run_in_background: true`.
- The Agent tool has no effort setting, so each prompt starts with "Effort: high".

**How to reuse:**
- Revisions and re-checks go back to the same agent via SendMessage with its ID; that is cheaper, and the agent keeps its context.
- Fill in the `{…}` placeholders.

**Batch conventions:**
- Ports are per batch: writers `98x1…`, checkers `+4`.
- Record every agent ID in the batch tracker.

## Writer (single page)

```
Effort: high. You are the dataset page WRITER for {VENDOR} dataset `{DS}` ({one-line plain description}) on the gridflow documentation site.

Read these first, in full, in the main repo `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end`:
1. `.planning\v5\p26\BATCH-{vendor}.md` (paths, shared-worktree rules, every seat ruling, known defects). Your screenshot port is {PORT}.
2. `.planning\v5\author-brief.md`.
3. `.planning\v5\review-rubric.md`.
Then study the worked examples the batch file names ({closest example, e.g. `remit` for an event register, `bmunits_reference` for a register}).

Do the whole job the brief describes for `{vendor}/{DS}`:
- Research from gridflow code and local silver, read only.
- Write the `page:` block and any note-body corrections in the canonical vault note.
- Mirror the note byte for byte.
- Generate the artefacts.
- Build with `--only {vendor}/{DS}`, with no errors and only accepted detector advisories.
- Take screenshots at 1440, 1024, 768 and 390.

Rules:
- Wrap every Chrome call in `timeout 60`.
- Never `rm -rf` a path built from a variable.
- Do not stop the owner's review server if one is running (port {REVIEW_PORT}).

Look hardest at:
- {Coverage: the row count and window from DATA-MATRIX; establish what one row is, which entities, and the key}
- {Units and time stamps: read from code or the vendor, never from memory}
- {Known defect to reproduce first, if any; if the rows can't support an honest page, recommend a hold with numbers}

Write your full report to `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\v5\p26\{vendor}\{page}-author.md`. It must cover:
- the evidence table;
- body corrections;
- anything unverified;
- open questions;
- template problems;
- a pasteable "Defects" section.

Your final message must be at most 8 lines, one line each: build and detector status (or HOLD recommended), chart and window, what the checker should look hardest at, any blocker, and any gridflow or data defect.
```

## Writer (family page)

Use the same prompt, with these changes:
- The opening line becomes: "the {VENDOR} family page `{page}` on the gridflow documentation site. The members, lead first, are `{lead}`, `{m2}`, …".
- Add "including 'Family pages'" after the author-brief line.
- The job becomes: "write the `page:` block on the lead's canonical note, plus body corrections on all N notes; mirror them byte for byte…".
- Build with `--only {vendor}/{lead}`. The family slug renders nothing.

## Checker

```
Effort: high. You are the dataset page CHECKER for {VENDOR} {dataset|family page} `{page}` ({lead/members if a family}) on the gridflow documentation site.

**Rules**
- Inspection only. Use Bash only to read code, read silver with Polars (read only), run `gridflow-build --only {vendor}/{lead}` and the detector (absolute path, see the batch file), and take screenshots.
- Wrap every Chrome call in `timeout 60 ...` with `--timeout=15000 --virtual-time-budget=5000`. A true 390 view needs a 390 px iframe. Stop any server you start. Do not stop the server on port {REVIEW_PORT}.
- Write no file except your review.
- Never commit, run ingest or any live API, or edit the notes, page or artefacts.
- Never `rm -rf` a path built from a variable.

**Read first, in full,** in the main repo `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end`:
1. `.planning\v5\p26\BATCH-{vendor}.md` (paths and every seat ruling). Your screenshot port is {PORT}.
2. `.planning\v5\review-rubric.md`.
3. `.planning\v5\author-brief.md` (including "Family pages" for a family).

**Then read:**
- the writer's report `.planning\v5\p26\{vendor}\{page}-author.md`;
- the vault note(s), diffed against `origin/master` in the vault worktree (use a literal path);
- the artefacts and the built page.

**Seat ruling(s):** {e.g. "the page ships with the X loss stated plainly; check the statement is accurate and plain", or the seat's answers to the writer's open questions: not findings unless inaccurate}.

Check everything in the rubric against gridflow code, local silver and the vendor docs the note quotes. Look hardest at:
1. {The writer's own "look hardest" items, each with the numbers to reproduce}
2. {Chart: values against silver, the window, point-time and cadence wording}
3. {Units, keys, and any use the page suggests that silver can't deliver (a major)}

Open the unfolded frame and the notebook output. The accepted detector advisory (EIC dash count) is not a finding.

**Output:** write your review to `C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow-front-end\.planning\v5\p26\{vendor}\{page}-review.md`. Give the verdict (APPROVE or REVISE), then numbered findings, each with severity (blocker, major, nit), field path, what is wrong, and the evidence.

Your final message must be at most 6 lines: the verdict, the count of findings by severity, and one line per blocker or major.
```

## Revise (SendMessage to the writer)

```
The {page} review is REVISE: {counts}. Read `...\{page}-review.md` and fix everything in it.

**{The major}:** {one or two sentences, plus the seat's ruling if one is needed}.
**Nits:** fix all of them, within budgets.

Then:
1. Edit the canonical note(s) and mirror them byte for byte.
2. Rebuild with `--only {vendor}/{lead}`.
3. Run the detector at its absolute path.

Wrap every Chrome call in `timeout 60`. Never delete a variable path. No git. Do not stop the server on port {REVIEW_PORT}.

Write `{page}-author-2.md` beside the review. End with a one-line summary.
```

## Re-check (SendMessage to the checker)

```
Please re-check the revised {page} page. The writer's response is in `...\{page}-author-2.md`.

1. Verify the major(s) first: {what must now be true, with numbers to reproduce}.
2. Then check the nits.
3. Check that nothing regressed: build with `--only {vendor}/{lead}` and run the detector at its absolute path.

This is a focused re-check. Wrap every Chrome call in `timeout 60`. Inspection only. Do not stop the server on port {REVIEW_PORT}.

Write `{page}-review-2.md` with APPROVE or REVISE. End with a one-line summary.
```

## Nit-fix after APPROVE (SendMessage to the writer)

```
{page} came back APPROVE with N nits. Please fix all of them before the owner's review. The review is `...\{page}-review.md`:
1. …

Then:
1. Edit the canonical note(s) and mirror them byte for byte.
2. Rebuild with `--only {vendor}/{lead}`.
3. Run the detector.

No git. Never delete a variable path. Do not stop the server on port {REVIEW_PORT}.

Append a "Nits fixed" section to your report, and end with a one-line summary.
```
