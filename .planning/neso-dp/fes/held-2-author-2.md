# Held FES pages, second batch, round 2: writer report (2026-10-24)

These are fixes for `held-2-review.md` (WS2 REVISE with one major; ED5 APPROVE; the other four APPROVE with nits), applied under the seat's three rulings. All edits were made with the Edit tool and the notes stay LF. Each changed note was copied to the mirror, and `cmp` is clean on all six. `gridflow-build --only` rebuilt ED3, WS1, WS2, the local authority page and the hydrogen page with no errors: the "errors on pages not rendered" line is gone. The detector returns `[]` on all six. ED5 is unchanged. I took no new screenshots: every change is a prose swap of equal or similar length in the same fields.

## Ruling 1: WS2 major

Checked on bronze `3aba22fd` (`10yo2026_ws2_v001.csv`):
- `Category` holds `Emissions (MtCO2e)` (11 rows) and `Carbon Captured (MtCO2e)` (7 rows).
- The 2023, 2024 and 2025 files have no `Category` column and no unit anywhere.

Changes:
- **`held`:** "NESO states no period for the year labels, or what blanks mean; 2023, 2024 lack units." (16 words.)
  - True for both kinds of source: the 2023 and 2024 files carry no unit, and their dictionaries give `N/A`.
  - The review's wording ("dictionary units for 2025 only") is 17 words, over the budget.
- **`what_it_is`:** "There is no unit column. NESO's dictionaries, as read in October 2026, give `MTCO2e` for 2025 and `N/A` for 2023 and 2024. The 2026 file, a Ten-Year Outlook output last modified September 2026, adds two category labels that read `MtCO2e`." Each edition is now covered and dated.

## Ruling 2: ED3

**The exception now names one item.** The held line for both gas tables reads: "NESO states no period for the year labels except total GB peak, or what blanks mean." (16 words.)
- NESO's ED4 item is "Total GB Peak 1-in-20 Demand". "Total" excludes the combined table's heat `Peak 1in20` rows with fuel gas in `GW`.
- "Except the GB gas peak" would be 17 words.

**The combined table's other questions:**
- They are part of gridflow's question (`uptake` scale, `number` basis, and the earlier peak unit), but neither fits beside the shared clause in 16 words.
- I carried them in the other fields instead:
  - **The combined member's description:** "2023 and 2024: gas and heat demand; `number` and `uptake` have no stated scale" (14 words).
  - **`what_it_is`:** it now says ED4 "puts total GB 1-in-20 peak demand in gas years starting in October; the files label it `GWh` in 2023 and `GWh/day` from 2024". Both labels are checked in silver.
  - **To make room,** I dropped the sentence "NESO calls the 2026 files Ten-Year Outlook outputs" from `what_it_is`. The 2026 file names still show `10yo2026`, and the resource descriptions say it.

## Ruling 3: the other nits

| Nit | Fix |
|---|---|
| 1 (ED3 "peak gas") | Done; see ruling 2 |
| 2 (ED3 `number`, `uptake`, peak unit) | Done in the member description and `what_it_is`; see ruling 2 |
| 3 (WS1 held grammar) | Done: "NESO states no period for the year labels, or what blanks and `N/A` mean." (14) |
| 4 (WS1 2025 repeats in the held line) | Not done. "; 2025 repeats rows" takes the line to 17 words. `what_it_is` still carries the four row pairs |
| 5 (WS1 oil) | Done: the summary is "...natural gas, hydrogen, bioenergy and oil: supply, demand and capacity, per edition." |
| 6 (WS1 transform comment) | Done: back to "the capture's date to silver" |
| 7 (local authority, do not stack or join) | Done: "Two separate tables, never stacked or joined." `what_it_is` is still within 60 words ("every five years" became "five-yearly") |
| 8 (local authority domestic held) | Done: "NESO states no count date for each year's stock, oil boiler's basis, or hydrogen blanks." (15). The dictionary sentence on oil boiler stock stays in `what_it_is` |
| 9 (local authority second use) | Done: replaced with "Map the heating technology mix across GB local authorities, edition by edition" (no modelling claim) |
| 10 (hydrogen capex member) | Done: "Three-scenario capital cost benchmarks, plus operating costs, for proton-exchange membrane and alkaline electrolysers" |
| 11 (hydrogen note body) | Done: "Vendor portal page (the site page also lists the three download URLs, as the raw feed):" |

## Defects

None new.
