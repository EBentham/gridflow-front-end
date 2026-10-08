# gridflow-front-end — Backlog

Owner intents and deferred work for future milestones. Items leave this file when a milestone
roadmap takes them.

## OWNER 2026-10-08 — future milestone intents (recorded by the control room)

1. **Add the new NESO Data Portal datasets to the front-end catalogue, vault pages included.**
   The contract already exists in gridflow: `../gridflow/.planning/milestones/v0.22-ROADMAP.md`
   §Front-end track (batches FE-0…FE-8 by the portal's 16 Data Groups; page = package; a
   multi-table package is a family page). Input is the seat's per-package hand-off ledger
   `../gridflow/.planning/v0.22-FE-LEDGER.md` (activated silver, `_latest` names, row counts,
   vault page approved on master, eligibility report — only `eligible` outputs ship). Vault side:
   `quant-vault/30-vendors/neso-data-portal/` (v0.22 writes skeletons; the docs track writes
   prose), mirrored here by `/propagate-vault-mirror`. Lane: front-end lane rule (Opus 5.5
   one-shot, no plan/diff review, deterministic gates before merge). Starts after the paused
   v5 batch has closed.
2. **Notebooks + pipeline as one public deployable, without the models** — tracked in
   `../gridflow_models/.planning/BACKLOG.md` (same date); the site will need to link to it.
3. **Notebook info-card visual redesign** — tracked there too; a design change follows the
   UI-design rule (interactive chat with Bobbo, ~5 variants side by side, until `DESIGN.md` +
   tokens lock).
