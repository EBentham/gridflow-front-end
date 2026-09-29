# agsi-storage: author revision 2

Answers `agsi-storage-review.md` (REVISE: 1 major, 7 nits). Writer: Opus 5.5, 2026-09-29.

## Gates

- Canonical notes edited in `vault-p26-gie` (CRLF kept: `storage.md` 414/414, `storage_reports.md` 304/304) and mirrored byte for byte into `p26-gie/vault/gie/` (`cmp` clean for both).
- `run_notebooks.py --dataset gie/storage`: 5 cells, no errors, the plot cell now has no text output (the `;` suppresses the legend repr).
- `gridflow-build --only gie/storage`: no errors (only the known WARNs for other gie datasets).
- `detect.mjs --json` (absolute path): `[]`.
- Notebook checked open at 390 (a 390 px iframe) and 1440. Method: a scratch copy of the built site under `scratchpad/agst-nb2`, with a one-line auto-click on the "Open the demo notebook" button appended to the copy only, served on my port 9851 and stopped after. The site worktree is unchanged. Port 9670 was not touched.

## Findings and what changed

1. **major, plot cell at 390.** The 33-space hanging indent is gone. The cell is now:
   ```
   net = df.pivot(index="gas_day", columns="entity_code", values="net_withdrawal_gwh")
   colors = ["#155A6E", "#66793B", "#C77E3C"]
   ax = net[["DE", "FR", "NL"]].plot(ylabel="net withdrawal, GWh", figsize=(8, 3.5), color=colors)
   ax.legend(loc="upper left");
   ```
   At 390 the cell wraps at word boundaries into 10 readable lines (screenshot `scratchpad/agst-shots2/390-light_t5.png`).
2. **nit, `what_it_is`, units.** First I reproduced the checker's ENTSOG cross-check: Italy's AGSI `injection_gwh - withdrawal_gwh` over ENTSOG `physical_flows` exits minus entries at `Italgasstorage (IT)`, `UGS - IT - Snam Rete Gas/STOGIT` and `.../Stogit Adriatica` gives a ratio of 0.960 to 1.020 on all 14 overlapping gas days (13 Sep: 522.04 vs 525.19; 20 Sep: 489.18 vs 481.14). The last sentence now reads: "Stock columns are TWh despite `_gwh` names, by our check against the flows and ENTSOG; compare countries by `storage_pct_full`." The guide lines for `gas_in_storage_gwh`, `working_gas_volume_gwh`, `consumption_gwh` and `contracted_`/`available_capacity_gwh_per_day` now say TWh "by our check". The page never presents TWh as GIE's statement.
3. **nit, vault bodies.** In both notes, the flows bullet in Known issues now cites the ENTSOG check (three Italian storage points, `silver/entsog/physical_flows.py:27-68`, within 4% on 14 gas days, ratio 0.96 to 1.02). The stock rows in the silver table say TWh by our check. Both notes say GIE's own unit statement is not in our sources, so the units are our check.
4. **nit, GB wording.** The caption now reads "GB sends placeholders, no storage values" (40 words, at budget). The family `differs` for `storage` is "Nine countries, one row each per gas day; GB's storage values are null".
5. **nit, `related[2]`.** `gie/lng`: "LNG send-out feeds the same national gas balances as storage".
6. **nit, `related[0]` held page.** Kept `gie/unavailability`, following the `netbsad` precedent. **Seat to rule:** keep it or swap it while the unavailability page stays blank.
7. **nit, notebook colours and legend.** The plot now shows DE, FR and NL in the chart's own paints: petrol, olive and clay, all distinct hues. IT (the second teal) is gone from the plot. The legend is fixed at upper left, which is clear of every line (DE starts at -512). `plot_alt` now names DE, FR and NL; its values are unchanged and still match silver.
8. **nit, `record.fields.gas_day`.** Now reads "AGSI's `gasDayStart` date; `event_time` gets a fixed 06:00 UTC project label, not the start" (14 words).

No change to the chart spec, so the series was not re-distilled. The sample is unchanged too.

## Defects

Unchanged from `agsi-storage-author.md`, with the unit defect now confirmed as the checker records: `injection_gwh`, `withdrawal_gwh` and `net_withdrawal_gwh` are GWh per gas day (ENTSOG cross-check, ratio 0.96 to 1.02 on 14 gas days). `gas_in_storage_gwh`, `working_gas_volume_gwh`, `consumption_gwh`, `contracted_capacity_gwh_per_day` and `available_capacity_gwh_per_day` are TWh. The vault GIE README ("stocks and flows are GWh") remains wrong and untouched.

Summary: all 8 review findings fixed; notes mirrored; build, detector `[]` and the 390 notebook check all pass; the seat still has to rule on the `gie/unavailability` link to a held page.
