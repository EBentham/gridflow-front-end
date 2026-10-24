---
source: "neso_data_portal"
package: "levelised-cost-of-green-hydrogen"
dataset_keys: ["lcoh_capex_opex_input_assumptions_pem", "lcoh_levelised_cost_blue_hydrogen", "lcoh_levelised_cost_green_hydrogen"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-16
layer_coverage: "bronze"
eligibility: "held"
---

# Levelised cost of green hydrogen

**This package is licence-held. Its files are captured to bronze and nothing is published from
them: no silver output exists, and this page carries no data values, previews, sample rows or
value statistics.** The page exists so the NESO Data Portal catalogue is complete (owner ruling
879).

The package is NESO's published set of levelised-cost-of-hydrogen modelling (geographic scope
is not stated in the package text; TODO: verify): a green-hydrogen modelling file and a blue-hydrogen modelling file, both covering 2025 to 2050
by their titles, plus a file of capex and opex input assumptions for PEM and alkaline
electrolyser systems. It belongs to the Future Energy Scenarios publications
(publisher group "FES: Pathways to Net Zero"). The vendor describes the package as an
aggregation of public and third-party data, and its source list names Bloomberg NEF, Aurora
Energy Research and the IEA, among others
(`@.planning/phases/v0.22-N-licence/N-FACTS.md`). The vendor's green-hydrogen resource
description carries the caveat that the modelling is not a forecast
(same file, section (c)). For the wider scenario context see the FES pages in this vendor's
dataset set; for the vendor index see @../README.md.

- Publisher group: FES: Pathways to Net Zero
- Registry group: future-energy-scenarios · archetype: SCN
- Vendor portal page (the only link this page gives to the files):
  [levelised-cost-green-hydrogen](https://www.neso.energy/data-portal/levelised-cost-green-hydrogen)
- Attribution: Supported by National Energy SO Open Data

## The hold

Held under unit N (RULINGS 477, class 3 workflow disposition; the registry hold text is
"third-party origin cited in package notes; licence carve-out"). Reasoning, from
`@.planning/phases/v0.22-N-licence/N-FACTS.md`:

- The package is labelled with the NESO Open Data Licence (CKAN `license_id` `ESO`, title
  "NESO Open Data Licence", measured from the ratified catalogue snapshot `20261006T195819Z`).
- The package notes and the capex/opex resource describe third-party data and name the sources
  above. No permission statement and no package-specific restriction was found in the package
  text.
- The licence excludes rights NESO is not authorised to license. Nothing found shows that NESO
  holds authority over these particular third-party inputs, so republication is unresolved.
  Provenance and the licence label do not answer that question.

**The exact question (packet section 4.1, group J, put to NESO):** the package cites
Bloomberg NEF, Aurora Energy Research and IEA among its sources and is labelled NESO Open Data
Licence; is NESO authorised to license those inputs, so that a third party may republish the
files under the Open Data Licence with the attribution "Supported by National Energy SO Open
Data"? (`@.planning/phases/v0.22-close/v0.22-NEEDS-BOBBO.md`, Ask 6.)

Lift condition: a NESO statement answering the question. Nothing is published until it
arrives; lifting would need a small promotion unit. The eligibility report
(`@docs/neso_data_portal/eligibility.md`) records only the hold label ("held: third-party origin
cited in package notes; licence carve-out (unit N)") and the three families as "ingest-only (no
silver output)"; the full group J question is in `@.planning/phases/v0.22-close/v0.22-NEEDS-BOBBO.md`
section 4.1 J (Ask 6), not in the eligibility report.

## Files by disposition

### SILVER (disposition only; no silver output exists)

| Resource | Format | Capture | Id |
|---|---|---|---|
| Capex and opex input assumptions for PEM and Alkaline electrolyser systems | CSV | upload | `88cfa584-db79-4573-a0c0-c14086257f8f` |
| Levelised cost of blue hydrogen modelling, 2025 to 2050 | CSV | upload | `3f3b1bf0-4664-494f-a501-a39adabecd0d` |
| Levelised cost of green hydrogen modelling, 2025 to 2050 | CSV | upload | `cc2dad0c-393c-4ae0-ae67-a98703169ad4` |

All three resources are registered to a silver family, but the package hold means no
transformer has run and no silver exists. The registry records `transformer: null` for each
family. There are no DOC resources in this package.

What bronze holds, from the capture sidecars (all three captured 2026-10-08, HTTP 200,
`text/csv`, one page, not empty captures). Bronze is the raw vendor bytes, held locally and
immutable; it is not republished.

| Family | Vendor file name | Bytes | `ckan_last_modified` (as recorded) | Captured (UTC) |
|---|---|---|---|---|
| `lcoh_capex_opex_input_assumptions_pem` | `electrolysers_capex_and_opex_inputs.csv` | 3,192 | 2026-09-24T13:44:23 | 2026-10-08T11:12:04 |
| `lcoh_levelised_cost_blue_hydrogen` | `blue_h2_lcoh_modelled_results_2025_to_2050.csv` | 15,513 | 2026-09-24T13:45:35 | 2026-10-08T11:12:08 |
| `lcoh_levelised_cost_green_hydrogen` | `green_h2_lcoh_modelled_results_2025_to_2050.csv` | 57,414,631 | 2026-06-17T11:38:34 | 2026-10-08T11:12:13 |

Vendor pages for the individual resources (portal pages, not gridflow-hosted files):

- [Capex and opex input assumptions](https://www.neso.energy/data-portal/levelised-cost-green-hydrogen/capex_and_opex_input_assumptions_for_pem_and_alkaline_electrolyser_systems)
- [Blue hydrogen modelling](https://www.neso.energy/data-portal/levelised-cost-green-hydrogen/levelised_cost_of_blue_hydrogen_modelling_2025_to_2050)
- [Green hydrogen modelling](https://www.neso.energy/data-portal/levelised-cost-green-hydrogen/levelised_cost_of_green_hydrogen_modelling_2025_to_2050)

## Families

All three are tabular, archetype SCN, refresh adhoc, `empty allowed: no`, ingest-only (no
silver yet). The registry download cap for each is 536,870,912 bytes.

### `lcoh_capex_opex_input_assumptions_pem`

- Resource `88cfa584-db79-4573-a0c0-c14086257f8f`, 1 capture, 3,192 bytes.
- Vintage clock: `ckan_last_modified`, recorded 2026-09-24T13:44:23. Under the portal archetype
  a capture's `available_at` is the CKAN `last_modified` of that capture.
- Event time: no temporal recipe is recorded in the registry and no silver exists, so no
  `timestamp_utc` column has been defined. If a silver output were ever released with recipe
  `none`, `timestamp_utc` would be the capture time. TODO: verify the event-time basis (if any)
  from the vendor's data dictionary before any silver is built.
- Schema, units, sentinels, row count: TODO: verify. No silver exists and no vendor data
  dictionary is cited in FACTS for this package. Units are never inferred from a column name.

### `lcoh_levelised_cost_blue_hydrogen`

- Resource `3f3b1bf0-4664-494f-a501-a39adabecd0d`, 1 capture, 15,513 bytes.
- Vintage clock: `ckan_last_modified`, recorded 2026-09-24T13:45:35.
- Event time: as for the capex/opex family. The title says 2025 to 2050, but the
  year-label convention (calendar, financial or other) is not established. TODO: verify.
- Schema, units, sentinels, row count: TODO: verify.

### `lcoh_levelised_cost_green_hydrogen`

- Resource `cc2dad0c-393c-4ae0-ae67-a98703169ad4`, 1 capture, 57,414,631 bytes (about 57 MB,
  by far the largest of the three).
- Vintage clock: `ckan_last_modified`, recorded 2026-06-17T11:38:34. This differs from the
  other two files in the same package, so the package does not share one vintage.
- Event time: as above; same TODO on the year-label convention.
- Schema, units, sentinels, row count: TODO: verify.

## Activation

None. The package was captured to bronze only (RULINGS 477). `@.planning/v0.22-RESULTS.md` has
no activation section for it (there is no "## N" section): its only mention is the last bullet
of the "## SCN-3" section, which records "LCOH HOLD(N) (477)". No transform ran, no silver
partition exists, there is no reconcile, and the eligibility report lists all three families as
ingest-only with no silver output. Consequently there is no results section on this page, and no
gold view consumes the package.

## Cadence

- Registry refresh: adhoc
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

## Licence and attribution

- Licence: NESO Open Data Licence (`license_id` `ESO`)
  ([licence text](https://www.neso.energy/data-portal/ngeso-open-licence)).
- Third-party carve-out: unresolved for this package (see The hold). The licence's general
  exclusion of third-party rights NESO is not authorised to license is confirmed; its
  application here is unclear.
- Own restriction found in the package text: none. Primary confirmation from the vendor's
  `package_show` JSON of the notes and resource descriptions was not obtained by the research
  run; the snapshot of record was used instead (see FACTS seat addendum).
- Attribution: Supported by National Energy SO Open Data

## Holds

- package: held: third-party origin cited in package notes; licence carve-out (unit N).
  Applies to every family above. Question: group J, as stated in The hold. Unit: N.
- No data values, previews, geometry or sample rows from this package are published on this
  page or on the site, until NESO answers.
