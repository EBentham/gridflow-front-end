---
source: "neso_data_portal"
package: "disaggregated-bsad"
dataset_key: "disaggregated_bsad"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze"
eligibility: "eligible"
---

# Disaggregated Balancing Services Adjustment Data (BSAD)

Per-action **Balancing Services Adjustment Data**. BSAD is the cost and volume of the
adjustments National Energy System Operator (NESO) makes to balance the system outside the
Balancing Mechanism, submitted into settlement. The **disaggregated** file is the finest grain
of the three BSAD packages: one row is meant to be one adjustment *action* within a settlement
period, sometimes a vendor-defined roll-up of several underlying services. It carries only a
settlement date, a settlement period, a cost (£), a volume (MWh) and a one-letter flag that
separates **system** actions (`T`) from **energy** actions (`F`). The sibling packages are
@./aggregated-bsad.md (settlement-period totals by variable) and
@./balancing-services-adjustment-data-forward-contracts.md (forward-contract adjustments).

The vendor's methodology and the BSC (Section Q) require every action to carry a sequential
identity in the settlement submission. **The portal CSVs do not publish that identity.** They
also omit contract, trade, party, asset, run and revision identifiers. Several actions in the
same period can therefore be identical in every published column, and they are.

**Read this first.** This family is **captured in bronze but not loaded to silver**. It has
**no registry record**, so no transformer runs: there are no silver rows, no silver views and no
`_latest` view. The reason is RULINGS 538 (the same ruling as `demand_profile_dates` and
`contract_transfer_obligation`): every one of the 14 captured bodies repeats identical complete
rows, so no key built from vendor columns passes the duplicate guard, and gridflow forbids
silent deduplication, summing repeated actions, or inventing an occurrence index. The batch
that handled it (v0.22 AS-4a, RULINGS 749 and 759) left it **ingest-only**. The activation
receipt (RULINGS 760, `v0.22-RESULTS` section AS-4a) confirms it: "disaggregated_bsad not
transformed (no record)", and the registry file is byte-unchanged. This is a structural
blocker, not a unit or sign hold on a published output.

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT
- Attribution: Supported by National Energy SO Open Data

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Disaggregated BSAD 2013-14 | CSV | upload | `a01c3587-0e29-4e8b-81e6-37a32776fd8a` |
| Disaggregated BSAD 2014-15 | CSV | upload | `56b1346d-b0b7-4382-b1f6-8c20f614498e` |
| Disaggregated BSAD 2015-16 | CSV | upload | `d635d2b5-13ed-479b-ab84-1b62b0bf57c5` |
| Disaggregated BSAD 2016-17 | CSV | upload | `67b9dc17-9680-465c-8811-d0701608a9de` |
| Disaggregated BSAD 2017-18 | CSV | upload | `b6cb5312-ec16-4c4b-924b-9154f051e772` |
| Disaggregated BSAD 2018-19 | CSV | upload | `c64c285c-764b-4e95-9e04-a9379f8f84be` |
| Disaggregated BSAD 2019-20 | CSV | upload | `48fbc6ea-381e-40d6-9633-d1be09a89a0b` |
| Disaggregated BSAD 2020-21 | CSV | upload | `17325b59-ee73-4d7b-a05b-f2be04f1c2f8` |
| Disaggregated BSAD 2021-22 | CSV | dump | `cbf4e22a-d18e-4998-a7aa-da36261c4430` |
| Disaggregated BSAD 2022-23 | CSV | dump | `b1167b32-75e8-436b-8b04-f1e586ffe60b` |
| Disaggregated BSAD 2023-24 | CSV | dump | `aba2f13c-39ed-4991-a28b-288c94f1b800` |
| Disaggregated BSAD 2024-25 | CSV | dump | `bc7cf2a8-6e25-4dad-ac2d-b9a97e968317` |
| Disaggregated BSAD 2025-26 | CSV | dump | `f99c6391-507b-4eaa-beb8-a26fdfa809de` |
| Disaggregated BSAD 2026-27 | CSV | dump | `2be1a4d1-6b10-4c62-a01c-924942a3748f` |

The package has 14 resources, all one family (`disaggregated_bsad`), all `SILVER` in the
registry. It has **no DOC, GIS, COVERED or other ingest-only files**, so there are no
documentation downloads to list. `SILVER` is the *intended* target; it is **not realised**
because the family has no record (`transformer: null`). Each resource is one financial year
(1 April to 31 March); 2026-27 is the current, partial year.

Download links as captured (package id `4878d09f-8938-4e8f-8f3e-538b3355861a`). Uploads are
fetched from the file URL; dumps are fetched from the datastore dump endpoint.

| Financial year | Capture type | Download | Bytes · rows (bronze) |
|---|---|---|---|
| 2013-14 | upload | [bs_disbsd_01-04-2013_31-03-2014.csv](https://api.neso.energy/dataset/4878d09f-8938-4e8f-8f3e-538b3355861a/resource/a01c3587-0e29-4e8b-81e6-37a32776fd8a/download/bs_disbsd_01-04-2013_31-03-2014.csv) | 590,838 · 23,016 |
| 2014-15 | upload | [bs_disbsd_01-04-2014_31-03-2015.csv](https://api.neso.energy/dataset/4878d09f-8938-4e8f-8f3e-538b3355861a/resource/56b1346d-b0b7-4382-b1f6-8c20f614498e/download/bs_disbsd_01-04-2014_31-03-2015.csv) | 984,260 · 38,420 |
| 2015-16 | upload | [bs_disbsd_01-04-2015_31-03-2016.csv](https://api.neso.energy/dataset/4878d09f-8938-4e8f-8f3e-538b3355861a/resource/d635d2b5-13ed-479b-ab84-1b62b0bf57c5/download/bs_disbsd_01-04-2015_31-03-2016.csv) | 1,150,407 · 43,760 |
| 2016-17 | upload | [bs_disbsd_01-04-2016_31-03-2017.csv](https://api.neso.energy/dataset/4878d09f-8938-4e8f-8f3e-538b3355861a/resource/67b9dc17-9680-465c-8811-d0701608a9de/download/bs_disbsd_01-04-2016_31-03-2017.csv) | 2,626,737 · 99,658 |
| 2017-18 | upload | [bs_disbsd_01-04-2017_31-03-2018.csv](https://api.neso.energy/dataset/4878d09f-8938-4e8f-8f3e-538b3355861a/resource/b6cb5312-ec16-4c4b-924b-9154f051e772/download/bs_disbsd_01-04-2017_31-03-2018.csv) | 4,549,292 · 172,558 |
| 2018-19 | upload | [bs_disbsd_01-04-2018_31-03-2019.csv](https://api.neso.energy/dataset/4878d09f-8938-4e8f-8f3e-538b3355861a/resource/c64c285c-764b-4e95-9e04-a9379f8f84be/download/bs_disbsd_01-04-2018_31-03-2019.csv) | 4,573,629 · 173,633 |
| 2019-20 | upload | [bs_disbsd_01-04-2019_31-03-2020.csv](https://api.neso.energy/dataset/4878d09f-8938-4e8f-8f3e-538b3355861a/resource/48fbc6ea-381e-40d6-9633-d1be09a89a0b/download/bs_disbsd_01-04-2019_31-03-2020.csv) | 4,235,976 · 158,084 |
| 2020-21 | upload | [data.csv](https://api.neso.energy/dataset/4878d09f-8938-4e8f-8f3e-538b3355861a/resource/17325b59-ee73-4d7b-a05b-f2be04f1c2f8/download/data.csv) | 4,610,505 · 167,785 |
| 2021-22 | dump | [datastore dump](https://api.neso.energy/datastore/dump/cbf4e22a-d18e-4998-a7aa-da36261c4430) | 4,126,910 · 152,652 |
| 2022-23 | dump | [datastore dump](https://api.neso.energy/datastore/dump/b1167b32-75e8-436b-8b04-f1e586ffe60b) | 6,305,113 · 175,863 |
| 2023-24 | dump | [datastore dump](https://api.neso.energy/datastore/dump/aba2f13c-39ed-4991-a28b-288c94f1b800) | 3,665,566 · 138,353 |
| 2024-25 | dump | [datastore dump](https://api.neso.energy/datastore/dump/bc7cf2a8-6e25-4dad-ac2d-b9a97e968317) | 3,755,549 · 139,311 |
| 2025-26 | dump | [datastore dump](https://api.neso.energy/datastore/dump/f99c6391-507b-4eaa-beb8-a26fdfa809de) | 4,020,186 · 149,372 |
| 2026-27 | dump | [datastore dump](https://api.neso.energy/datastore/dump/2be1a4d1-6b10-4c62-a01c-924942a3748f) | 1,900,104 · 71,517 |

All 14 resources were captured once, on 2026-10-08 (stamps 10:07Z to 10:10Z). Total bronze rows
**1,703,982**. Each sidecar SHA-256 matches the body (FACTS section 2). Only one capture per
resource exists, so how NESO amends a published year between captures is unmeasured.

- Vendor dataset page: <https://www.neso.energy/data-portal/disaggregated-bsad>.
- Vendor dictionary (2026-27 resource): <https://www.neso.energy/data-portal/disaggregated-bsad/disaggregated_bsad_2026-27>.
- Vendor methodology: <https://www.neso.energy/document/110891/download>.
- **Implementation delta, reconciled.** The registry JSON gives the package `eligibility:
  eligible` and every resource a `SILVER` disposition. The eligibility report
  (`docs/neso_data_portal/eligibility.md`) lists the family as "ingest-only (no silver
  output)" and counts 14 eligible resources. The code has no record (pinned by
  `tests/unit/test_neso_as4a_records.py::test_disaggregated_bsad_has_no_record_and_its_file_is_byte_unchanged`).
  The three agree once you read RULINGS 538: the licence and format make the package eligible,
  the `SILVER` disposition shows the intended target, and the repeated rows alone keep a record
  from being written.

## Families

### `disaggregated_bsad`

- Kind: tabular · archetype: EVT · refresh: daily · empty allowed: no
- ingest-only: no silver yet

#### Bronze schema, three header epochs

All cells are text in bronze. The date column and the period column are in the same position in
every epoch, but the modern epoch reverses the order of cost and volume.

| Epoch | Resources | Exact header |
|---|---|---|
| D-H0 | 2013-14 to 2019-20 | `Date, Settlement Period, Disaggregated BSAD Volume (MWh), Disaggregated BSAD Cost (£), Trade Flag System (T) / Energy (F)` |
| D-H1 | 2020-21 | `Date, Settlement Period, Disaggregated BSAD Volume (MWh), Disaggregated BSAD Cost (£), Trade Flag`, with a standalone `£` byte that is not valid UTF-8 (see Encoding) |
| D-H2 | 2021-22 to 2026-27 | `Date, SettlementPeriod, DisaggregatedBSADCost, DisaggregatedBSADVolume, TradeFlag` |

| Vendor column | Meaning | Vendor unit |
|---|---|---|
| `Date` | UK settlement-day calendar label | none (date label) |
| `Settlement Period` / `SettlementPeriod` | Half-hour of the settlement day, beginning with midnight to the following half-hour (ordinal) | none (ordinal) |
| `Disaggregated BSAD Volume (MWh)` / `DisaggregatedBSADVolume` | Adjustment volume of the action | MWh |
| `Disaggregated BSAD Cost (£)` / `DisaggregatedBSADCost` | Adjustment cost of the action | £ |
| `Trade Flag …` / `TradeFlag` | `T` system action, `F` energy action | none (string flag) |

Units are taken from the vendor dictionary and methodology as cited in the FACTS research
(FACTS section 5; g4). No unit was inferred from a column name or from magnitudes. No silver
column names exist, because there is no record.

#### The two clocks (proposed, not applied)

No record exists, so neither clock is stamped on any row.

- **Vintage clock (`ckan_last_modified`).** `available_at` = the CKAN `last_modified` of the
  capture (ADR-030). The eight uploads record one in their sidecars: 2019-12-13 for the six
  uploads 2013-14 to 2018-19, 2020-04-02 for 2019-20 and 2022-02-25 for 2020-21, read as UTC. The
  2021-22 and 2022-23 dumps record 2022-03-31 and 2023-01-23. **The four newest dumps
  (2023-24 to 2026-27) record no `ckan_last_modified` at all**, so a future record would
  need `capture_fallback` (available_at = capture time) for the mixed family. In every case
  this marks when NESO last replaced the file, not when an action was submitted or settled.
  The files carry no issue-time column. Original availability cannot be reconstructed from these
  revised archive bytes.
- **Event clock (`sp_pair(settlement_date, settlement_period)`).** The dictionary states the
  UK winter/summer clock, so the supported temporal recipe is the Europe/London
  settlement-period *start* of the date and period. The date is a settlement-day label, not an
  issue instant. Both DST period ranges (46 and 50) occur in the historical captures. The partial
  2026-27 year reaches ordinary periods only. This recipe is **proposed**; it cannot be applied
  until the identity question below is settled.

At the capture instants (2026-10-08), 1,703,942 populated targets fall on or before capture and
**25 after**. That does not meet an all-targets-forward exemption.

#### Sentinels and missing values

- **625 literal `-1` cells** appear across the cost and volume columns. Signed action volumes are
  documented (negative = sell action), so `-1` cannot be treated generically as missing. **No
  null-token map is justified** (FACTS g5).
- No populated padded cells, separators, percent signs, `NA`, `N/A`, embedded quotes, commas or
  newlines were found.
- Wholly blank rows exist in three bodies (2016-17, 2017-18, 2018-19: 5 each in the profiler's
  count). They are blank repetitions of each other, included in the excess counts under
  Identity, and removing them does not fix any body.
- The 2022-23 date column is timestamp-shaped (`%Y-%m-%dT%H:%M:%S`) with a midnight time
  throughout the measured labels. Do not read it as an issue time or a UTC instant.

#### Date formats by resource

| Resources | Populated date format |
|---|---|
| 2013-14 to 2020-21 | `%d/%m/%Y` |
| 2021-22 | `%Y-%m-%d` |
| 2022-23 | `%Y-%m-%dT%H:%M:%S` |
| 2023-24 to 2026-27 | `%Y-%m-%d` |

If the identity question is ever settled, the modern epoch needs a per-resource date format
(`formats_by_filename` on the date output): the 2022-23 resource gets the full timestamp-shaped
format and the other datastore resources get `%Y-%m-%d`. No shared date and period pair was found
between any two resources, so the blocker is within-body action identity, not financial-year
overlap (FACTS C03).

#### Encoding

The 2020-21 body is **invalid UTF-8** because of its standalone pound-sign header byte, and it
carries no byte-order mark. A diagnostic cp1252 decode reads it, but that is not an
authoritative declaration of the encoding. TODO: verify the encoding of the 2020-21 resource
with NESO. This is the D08 encoding question. The other 13 bodies are valid UTF-8; the seven
oldest uploads carry a byte-order mark and CRLF line ends, and the datastore dumps use LF with no
mark. This does not decide the disposition (no record exists to fail), but any future record
must not freeze a per-resource encoding without a vendor statement.

#### Identity and the blocker

Every full body repeats identical complete rows. Complete-row excess, counted over the whole
body (blank repetitions included where present):

| Resource | Body rows | Excess |
|---|---:|---:|
| 2013-14 | 23,016 | 488 |
| 2014-15 | 38,420 | 3,342 |
| 2015-16 | 43,760 | 3,208 |
| 2016-17 | 99,658 | 22,423 |
| 2017-18 | 172,558 | 77,697 |
| 2018-19 | 173,633 | 76,564 |
| 2019-20 | 158,084 | 41,366 |
| 2020-21 | 167,785 | 12,835 |
| 2021-22 | 152,652 | 7,796 |
| 2022-23 | 175,863 | 4,086 |
| 2023-24 | 138,353 | 8,196 |
| 2024-25 | 139,311 | 10,586 |
| 2025-26 | 149,372 | 14,442 |
| 2026-27 | 71,517 | 9,673 |
| **Total** | **1,703,982** | **292,702** |

- **Every possible key drawn from vendor columns fails.** The profiler's candidate list is empty
  and its worst full-row repeat count is 77,697. Dropping the wholly blank rows rescues no body,
  because the duplicate examples in the three blank-bearing bodies also include populated action
  rows. Example: the 2026-27 body repeats one complete action (2026-04-01, period 15, flag `F`,
  cost 8609, volume 50).
- **No row can be told from its repeat.** There is no action id, no occurrence index, no run or
  revision column. The repeats may be genuine separate actions of equal size, or a publishing
  defect: the file cannot say.
- Do not deduplicate, sum repeated actions, add value columns to the key, or add a row ordinal.
  This follows RULINGS 538 and the `demand_profile_dates` and `contract_transfer_obligation`
  precedents. The engine's duplicate-key guard would reject every capture.
- **TODO: DISAGGREGATED-BSAD-ACTION-ID.** Does NESO publish a stable action identity, or a rule
  that distinguishes these repeated actions? What settles it: a vendor republication carrying a
  stable action identifier, or an explicit vendor rule that separates the repeated actions and
  supports a lossless representation. Consequence: until then the family is ingest-only, not a
  knowingly unusable generic record.
- **TODO: DISAGGREGATED-BSAD-COST-SIGN.** Cost sign semantics are not settled. BSC definitions
  say positive adjustment volume is a buy action and negative volume a sell action (BSC
  technical glossary). That does not establish that a cost's sign alone shows cash paid or
  received. What settles it: a vendor cashflow-sign definition. Retain costs unchanged and
  impose no sign bound, flip or net.
- **2015-16 and early-year coverage.** The aggregated package has no 2015-16 resource and a
  partly populated 2014-15 one (see @./aggregated-bsad.md). This package *does* list a 2015-16
  resource (43,760 rows). TODO: verify with NESO that the disaggregated 2013-14 to 2015-16 uploads
  cover their full financial years; this page measured row counts only, not per-year date
  coverage.

#### Bronze at activation

| Property | Value |
|---|---|
| Captures | 14 (one per resource, all 2026-10-08) |
| Location | `C:/gridflow-data/bronze/neso_data_portal/disaggregated_bsad/2026/10/08/` |
| Bytes · rows | 47,095,072 · 1,703,982 (sum of the table above) |
| Silver | **none.** No silver directory and no row count for this family. The AS-4a transform covered the other 7 families |
| Reconcile | `--all --cutoff 2026-10-12`: exit 0, 198 families, 0 gaps, 52 adjudicated (+5 captures), 0 stale. This family stays ingest-only (`v0.22-RESULTS` section AS-4a, RULINGS 760) |

The reader is faithful: the profiler found no parse errors and no duplicate headers. Encoding
(one body) and parsing are not the blocker. Identity is.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Status: Live

The vendor update frequency is not stated in the snapshot. TODO: verify with NESO how often the
current-year (2026-27) resource is rewritten, and whether an update replaces the whole file or
appends rows. Only one capture per resource exists, so gridflow cannot tell. The registry
refresh is daily.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: <https://www.neso.energy/data-portal/ngeso-open-licence>. Any derived output must
carry the attribution line above verbatim.

## Holds

- none

There is no held silver output because there is **no silver output at all**. The family is
blocked structurally (class 3, RULINGS 538) by the identical-row repeats described under
Identity. It is not an E-SEM semantics hold: no unit or sign question holds a *published*
value, because nothing is published. The cost-sign and action-identity TODOs above are the open
questions. Until the identity question is settled, the data exists only as immutable bronze
captures.

## References

- @../README.md: NESO Data Portal vendor page (CKAN, file-download model)
- @./aggregated-bsad.md · @./balancing-services-adjustment-data-forward-contracts.md: the two sibling BSAD packages that do have records
- @./demand-profile-dates.md · @./contract-transfer-of-obligation.md: the other ingest-only families (same RULINGS 538 blocker)
- gridflow `docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md` (vintage clock), `ADR-034-neso-generic-silver-engine.md` (generic engine, duplicate guard), `ADR-040-neso-reconcile-adjudication.md` (recorded failures)
- gridflow `.planning/phases/v0.22-K-AS-4/K-AS-4-FACTS.md` section 5 and g1 to g6; `K-AS-4a-SPEC.md` item 3 and seat ruling 1
- gridflow `.planning/v0.22-RESULTS.md` section AS-4a; RULINGS 538, 747, 748, 749, 759, 760
- gridflow registry `src/gridflow/connectors/neso_data_portal/registry/disaggregated-bsad.json`; eligibility report `docs/neso_data_portal/eligibility.md`; profiler output `docs/neso_data_portal/profile/families/disaggregated_bsad.json`
- gridflow `tests/unit/test_neso_as4a_records.py` (no-record pin), `tests/unit/test_neso_ingest_only.py`
