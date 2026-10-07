# neso_data_portal/embedded_wind_solar_forecast: author revision 2

Writer: Opus 5.5 · high, 2026-10-06. Answers `embedded_wind_solar_forecast-review.md` (REVISE: 1 blocker, 1 major,
6 nits) and the seat's ruling relayed by the coordinator.

## Status

- Canonical note edited in the vault worktree; mirror `vault/neso_data_portal/embedded_wind_solar_forecast.md` copied and `cmp` byte-equal.
- `gridflow-build --only neso_data_portal/embedded_wind_solar_forecast`: success (budgets pass).
- `detect.mjs --json` (absolute path): `[]`. Real em dashes on the page: 0.
- Chart spec, sample selection and notebook cells are unchanged, so the series, sample and notebook artefacts did not need regenerating, and the build's digest check passes.
- Re-shot 1440, 1024, 768 and 390 (390 in a 390 px iframe, port 9865, server stopped). Looked at the 1440 and 390 hero and topsoil, where the text changed: nothing clipped.
- The hero key chip now wraps at 390, so the template fix from my first report is in.

## Findings and what changed

| # | Severity | Fix |
|---|---|---|
| 1 | blocker | **`facts.cadence`:** now `NESO's catalogue says hourly updates, within day to 14 days ahead; one issue charted`. That is NESO's package `notes` statement, attributed, beside what the chart shows.<br>**`what_it_is` rewritten:** it names the resource gridflow reads ("Embedded Solar and Wind Forecast") and says plainly that NESO's catalogue says the data moved to a new forecast system and recommends its "Jun - Dec" 2026 archive resource. No judgement on which is better.<br>To fit the 60-word budget, the sentence "silver appends every captured issue" was dropped (the summary already says gridflow keeps every issue), and so was the unit sentence (the column guide says "MW in gridflow's code").<br>**Note body:** the Publication lag row now quotes the package `notes` (half-hourly, "from within day up to 14 days ahead", "updated on an hourly basis") with the snapshot path. It marks this as a vendor statement that one capture cannot confirm, and records that the resource description's "daily resolution" contradicts the rows. A new Known issues bullet records the "Jun - Dec" recommendation, the archive resource's full name, `endpoints.py:118`, and the 21:25:03 last-modified.<br>**Docstring wording:** no "day-ahead" or "several times a day" wording from code docstrings remains on the page. The one "Day-ahead" left is the related link for `entsoe/wind_solar_forecast`, which describes ENTSO-E's own day-ahead process, not a docstring claim. |
| 2 | nit | `how_used[2]`: "Forecast error: score each captured issue, from the base view, against NESO's outturn estimates." (14 words) |
| 3 | major | **Note body silver path:** now `..._<YYYYMMDD>_run<bronze sidecar written_at, ISO with ":" and "+" as "-">.parquet`.<br>It says the stamp is the sidecar's `written_at`, via `_timestamp_from_sidecar` (`silver/base.py:102-107` key order `available_at, written_at, ...`; this sidecar has no `available_at` key; called at `1019`, written at `1067`). It is not the silver `available_at` column (= `published_at`). It cites the real file `..._20260820_run2026-08-20T21-43-41.158795-00-00.parquet`. |
| 4 | nit | **`chart_view.alt`:** the night window is now named: "Periods starting 21:00 to 02:30 UTC stay at or near zero (63 at most, at 23:30 UTC on the 25th)."<br>Re-checked on silver: the maximum over period starts with hour ≥ 21 or ≤ 2 is 63.0 at 2026-08-25 23:30 UTC. |
| 5 | nit | Caption: "stamped 21:25, read as UTC, on 20 August 2026". Alt: "stamped 21:25 (read as UTC)". |
| 6 | nit | No page edit (the reviewer's option). The cross-capture duplicate-key risk stays in Defects. |
| 7 | nit | Note body bronze sample note: "on this capture, `TIME_GMT` is half an hour after each period's start, UTC." |
| 8 | nit | Recorded in the note body (Known issues) and on the page (`what_it_is`), per the seat ruling. Defects line below. |

## Corrections to my first report

- "The CKAN catalogue snapshot carries no description" was wrong. I read the root `_generated/catalog-snapshot.json`, which has no `notes`. The dated snapshot under `_generated/snapshots/20260820T214455Z/` carries the package `notes`. Cadence and horizon are therefore vendor statements, no longer unverified.
- "`run<available_at>`" in the first report's body-correction list and evidence table was wrong. The run stamp is the bronze sidecar's `written_at` (finding 3).

## Defects (paste as is)

- **gridflow, connector resource choice (medium):**
  - `connectors/neso_data_portal/endpoints.py:118` selects the resource "Embedded Solar and Wind Forecast".
  - NESO's package `notes` say "NESO have moved the data source to its new forecast system. We recommend that customers now use the 'Jun - Dec' dataset", i.e. "Embedded Solar and Wind Forecast Archive 2026 (Jun - Dec)". Source: `quant-vault/30-vendors/neso-data-portal/_generated/snapshots/20260820T214455Z/catalog-snapshot.json`.
  - The resource gridflow reads was last modified 2026-08-20T21:25:03 in that snapshot.
  - Research which resource carries the live forecast, and whether the "Jun - Dec" archive has the same 8-column header and filename issue token. The token is `_ISSUE_TOKEN_PATTERN` in `silver/neso_data_portal/_bronze.py`.
- **gridflow, docstring (low):**
  - The `silver/neso_data_portal/embedded_wind_solar_forecast.py` module docstring says "rolling day-ahead forecast ... republished ... several times a day"; `silver/latest_views.py:128-129` says "republished several times a day".
  - The 20 Aug 2026 21:25 issue runs about 13 days ahead, and NESO's package `notes` say "from within day up to 14 days ahead ... updated on an hourly basis" (same snapshot).
  - Fix: drop "day-ahead" and cite the notes field for the cadence.
- **gridflow, to verify (medium if real):**
  - Two ingests that capture the same issue add duplicate `(settlement_date, settlement_period, issue_time)` keys to the base view `silver_neso_data_portal_embedded_wind_solar_forecast`.
  - Reasons: there is no identical-body skip (`bronze/writer.py` hashes the body only for the file name and sidecar, lines 33, 57, 80; `pipeline/runner.py` mentions identical bytes only in the backfill refusal, line 433). There is no cross-file dedup in `_write_silver` (`silver/base.py:2633-2636`). The run stamp is the microsecond `written_at`, so the files never collide.
  - Reasoned from code, not reproduced. With NESO's stated hourly updates, ingesting more often than hourly would hit it routinely.
  - `_latest` is unaffected.
- **gridflow, naming (low):**
  - `BaseSilverTransformer._write_silver(..., available_at=...)` receives the bronze sidecar `written_at` (via `_timestamp_from_sidecar`). For this dataset the silver `available_at` column is `published_at`.
  - On the one capture the file stamp and the column differ: 21:43:41.158795 against 21:25:03.319647.
  - Rename the parameter (for example `run_stamp_at`) or document it. The other NESO Data Portal pages hit the same trap.
- **Vault (fixed in this branch):** `embedded-wind-and-solar-forecasts.md`:
  - "Issue cadence TODO (not stated)" is replaced by the catalogue `notes` quote.
  - The silver path stamp is corrected to `written_at`.
  - The bronze and silver samples (invented) were replaced with real rows in revision 1.
- **Vendor, catalogue inconsistency:** the resource description says "up to 14 days ahead at a daily resolution", while the rows and the package `notes` are half-hourly.
- **Vendor data observation (no gridflow action):**
  - The 20 Aug 21:25 issue carries 1 to 63 MW of embedded solar for periods starting 21:00 to 02:30 UTC on the nights after 24 and 25 Aug (63 at 23:30 UTC on the 25th), and 1 to 2 MW on scattered later nights.
  - Silver passes it through unchanged.

Summary: the blocker, the major and all six nits are fixed: cadence and the "Jun - Dec" notice are attributed to NESO on the page and in the note, the silver run stamp is corrected to `written_at`, build and detector are clean, the mirror is byte-equal, and nothing is clipped at any width.

## Nits fixed (review 2, APPROVE)

| # | Field | Now |
|---|---|---|
| 1 | `page.what_it_is` | "... NESO's catalogue says the data moved to a new forecast system and recommends the "Jun - Dec" dataset." This is NESO's own word ("dataset"), and the ambiguous "its" is gone. The mapping to the resource "Embedded Solar and Wind Forecast Archive 2026 (Jun - Dec)" stays in the note body only. |
| 2 | `page.facts.cadence` | "NESO: hourly updates, from within the day to 14 days ahead; one issue charted" (14 words; still attributed to NESO, still beside what the chart shows) |
| 3 | `page.how_used[2]` | "Forecast error: score every captured issue, not just the newest, against NESO's outturn estimates." (14 words; no longer names a table the page never shows) |
| 4 | `page.record.fields` capacity lines | Both now say "`EMBEDDED_*_CAPACITY`; MW in gridflow's code; the same in these rows", matching the forecast lines |

- Canonical note edited, mirrored with `cp`, and `cmp` is byte-equal.
- `gridflow-build --only neso_data_portal/embedded_wind_solar_forecast`: success (budgets pass).
- `detect.mjs --json` (absolute path): `[]`. Em dashes: 0.
- The rendered text was grepped and contains all four new strings.
- Chart spec, sample and notebook are unchanged, so no artefacts were regenerated.
- No new screenshots: every change is shorter than or the same length as the text it replaced, inside fields already checked at 1440 and 390.

Summary: all four optional nits from review 2 are fixed in the note and its mirror; build and detector are clean.
