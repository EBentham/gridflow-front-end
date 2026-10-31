---
source: "neso_data_portal"
package: "skip-rates"
dataset_keys: ["skip_rates_behind_constraints_bmu", "skip_rates_behind_constraints_cons", "skip_rates_exclusion_reasons", "skip_rates_in_merit_all_bm", "skip_rates_in_merit_psa", "skip_rates_in_merit_psa_dsf_unit", "skip_rates_stage5_dsf_technology", "skip_rates_stage5_psa_technology", "skip_rates_stage6_acceptance", "skip_rates_stage6_psa", "skip_rates_summary"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-12
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: Skip rates
  summary: >-
    NESO's measure of better-priced Balancing Mechanism volume it passed over, stage by stage, by
    unit and by technology.
  facts:
    vendor: "NESO Data Portal: 77 CSV files; three tables come as monthly files"
    cadence: "Daily, as NESO lists it; some files are uploaded monthly"
    grain: "Summary: one row per half hour and stage of exclusion"
    history: NESO lists monthly files from December 2024
  landscape: market
  what_it_is: >-
    A skip is Balancing Mechanism volume that was available and priced better than what NESO
    accepted, but was not taken. NESO computes skip rates with a method developed with LCP Delta,
    then removes units it could not realistically have used, stage by stage. Tables give the
    summary, five-minute unit detail, exclusion reasons, technology rates and skips behind thermal
    constraints.
  how_used:
    - How often NESO dispatched out of price order, by half hour and stage
    - Which units and technologies were skipped, and why units were excluded
  chart:
    type: line
    silver: neso_data_portal/skip_rates_summary
    time: settlement_period_start
    filter:
      - {column: stage, op: eq, value: 5}
    values:
      - {column: bm_total_volume_skipped_offers_mwh, series: offers}
      - {column: bm_total_volume_skipped_bids_mwh, series: bids}
    dedup: {"on": [settlement_period_start, stage], order_by: published_at}
    aggregation: sum
    time_bucket: 1d
    window: {start: "2026-07-01", end: "2026-09-30"}
    max_points: 100
    unit: MWh
  chart_view:
    title: Skipped volume at stage 5, July to September 2026
    caption: >-
      Silver `skip_rates_summary` at stage 5, the table's last stage, All Balancing Mechanism
      basis: skipped offer and bid volume summed per UTC day, MWh, 1 July to 30 September 2026.
      Blank half hours add nothing; 1 August 2026 has no rows.
    alt: >-
      Line chart from neso_data_portal/skip_rates_summary in MWh, stage 5, one point per UTC day,
      1 July to 30 September 2026. Skipped offers have a daily median of 2,171.6, from 114.1 on 23
      August to 16,884.8 on 2 July. Skipped bids have a median of 3,808.8, from 65.9 on 2 July to
      12,285.6 on 26 July. Bids run higher in July and August, offers in September (medians
      4,583.3 against 2,653.3). Both lines break at 1 August.
    x_label: UTC day, from each half hour's start
    key:
      - {series: offers, label: Skipped offers, codes: "bm_total_volume_skipped_offers_MWh", paint: petrol, note: "Cheaper offer volume passed over, stage 5, summed per day"}
      - {series: bids, label: Skipped bids, codes: "bm_total_volume_skipped_bids_MWh", paint: clay, note: "Better-priced bid volume passed over, stage 5, summed per day"}
  raw_feed:
    note: >-
      From NESO's CKAN portal: `package_show`, then each file whole unless `last_modified` is
      unchanged (a few shown). The two Demand Side Flexibility tables are bronze only.
    commands:
      - {run: gridflow ingest neso_data_portal skip_rates_summary --last 24h, comment: "whole files; swap in any key"}
      - {run: gridflow transform neso_data_portal skip_rates_summary --last 24h, comment: "the summary: chart and rows below"}
  record:
    select:
      filter:
        - {column: settlement_period_start, op: in, value: ["2026-07-07T09:30:00Z", "2026-07-07T10:00:00Z", "2026-07-07T11:30:00Z", "2026-07-07T12:00:00Z"]}
        - {column: stage, op: in, value: [0, 5]}
      dedup: {"on": [settlement_period_start, stage], order_by: published_at}
      order_by: [settlement_period_start, stage]
      columns: [settlement_period_start, stage, bm_skip_rate_offers_percent, post_system_action_skip_rate_offers_percent, bm_total_volume_skipped_offers_mwh, post_system_action_total_volume_skipped_offers_mwh, bm_skip_rate_bids_percent, post_system_action_skip_rate_bids_percent, bm_total_volume_skipped_bids_mwh, post_system_action_total_volume_skipped_bids_mwh]
    key: [settlement_period_start, stage]
    caption: "Stages 0 and 5 of four half hours on 7 July 2026; NESO left 10:00 blank."
    fields:
      settlement_period_start: "Start of the half hour, UTC, as NESO's dictionary and guide state"
      stage: "Exclusion stage, 0 to 5: successive stages of NESO's method"
      bm_skip_rate_offers_percent: "Skip rate on offers, percent, on NESO's All Balancing Mechanism basis"
      post_system_action_skip_rate_offers_percent: "The same offer skip rate on NESO's Post System Action basis, percent"
      bm_total_volume_skipped_offers_mwh: "Offer volume skipped, MWh, All Balancing Mechanism basis"
      post_system_action_total_volume_skipped_offers_mwh: "Offer volume skipped, MWh, Post System Action basis; equal to All BM here"
      bm_skip_rate_bids_percent: "Skip rate on bids, percent, on NESO's All Balancing Mechanism basis"
      post_system_action_skip_rate_bids_percent: "The same bid skip rate on the Post System Action basis, percent"
      bm_total_volume_skipped_bids_mwh: "Bid volume skipped, MWh, All Balancing Mechanism basis"
      post_system_action_total_volume_skipped_bids_mwh: "Bid volume skipped, MWh, Post System Action basis; equal to All BM here"
      timestamp_utc: "Equals the half hour's start; gridflow's time anchor"
      published_at: "NESO's last-modified time for the whole file, read as UTC; one per capture"
      bronze_capture_id: The bronze file the row was read from; one per capture
      capture_written_at: When gridflow wrote the capture to bronze, UTC
  notebook:
    lead: >-
      `query()` reads the `_latest` view, the newest capture of the summary, filtering
      `timestamp_utc` (each half hour's start) with both ends included; times come back in UK time,
      so the first cell converts to UTC.
    cells:
      - |
        df = data.neso_data_portal.query("skip_rates_summary", "2026-07-01", "2026-07-31")
        df["start_utc"] = df.timestamp_utc.dt.tz_convert("UTC")
        df = df.sort_values(["start_utc", "stage"], ignore_index=True)
        df[["start_utc", "stage", "bm_skip_rate_offers_percent", "bm_total_volume_skipped_offers_mwh", "bm_total_volume_skipped_bids_mwh"]].head(6)
      - |
        vol = ["bm_total_volume_skipped_offers_mwh", "bm_total_volume_skipped_bids_mwh"]
        df.groupby("stage")[vol].sum().round().astype(int)
      - |
        day = df[df.stage.isin([0, 5])].assign(day=lambda x: x.start_utc.dt.day)
        daily = day.pivot_table(index="day", columns="stage", values="bm_total_volume_skipped_offers_mwh", aggfunc="sum")
        ax = daily.plot(figsize=(8, 3.5), color=["#C77E3C", "#155A6E"], xticks=range(1, 32, 5),
                        xlabel="UTC day of July 2026", ylabel="skipped offer volume, MWh")
        ax.legend(["stage 0", "stage 5"]);
    needs: the skip rates summary file
    plot_alt: >-
      Line plot of skipped offer volume per UTC day in July 2026, MWh, All Balancing Mechanism
      basis. At stage 0 the daily median is 32,274, high 59,026 on 2 July. At stage 5 the median
      is 1,982, from 117.6 on 12 July to 16,884.8 on 2 July, 0.3 to 28.6 percent of stage 0.
  family:
    slug: skip-rates
    members:
      - dataset: skip_rates_summary
        differs: "Skip rate and skipped volume per half hour and stage, under both measures"
        request:
          - "GET https://api.neso.energy/api/3/action/package_show?id=skip-rates"
          - "GET https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/e4129210-ea22-4a36-aa2f-ff7bd6147675/download/1_skip_rates_summary.csv"
      - dataset: skip_rates_behind_constraints_bmu
        differs: "Monthly skips behind thermal constraints, per BM unit, bid or offer"
        request:
          - "GET https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/26f3a3de-e5fd-43e5-9d8a-d89a9c786812/download/skips_behind_constraints_in_merit_bmu_level.csv"
        caveat: NESO's dictionary and slides disagree on what the rate is a percentage of.
      - dataset: skip_rates_behind_constraints_cons
        differs: "The same monthly measure, per constraint"
        request: "GET https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/a88adc4c-d3a6-440d-946b-4e5a3e7ea1c5/download/skips_behind_constraints_in_merit_constraint_level.csv"
        caveat: NESO's dictionary and slides disagree on what the rate is a percentage of.
      - dataset: skip_rates_exclusion_reasons
        differs: "Units excluded from the merit stack, with stage and reason; monthly files"
        request:
          - "GET https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/c20e81a0-1c82-4e03-913e-9e73d6daca6b/download/4_exclusions_12_2024.csv"
          - "GET https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/f8110eb8-f4ad-4288-87d5-37ab434b55b5/download/4_exclusions_10_2026.csv"
        caveat: NESO does not say whether each five-minute time marks the start or end of its slice.
      - dataset: skip_rates_in_merit_all_bm
        differs: "Measured against all Balancing Mechanism actions: volumes per unit, five-minute, monthly files"
        request:
          - "GET https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/ec422c87-a316-47bf-95a2-4e0cd07114dc/download/2_in_merit_data_bm_skips_12_2024.csv"
          - "GET https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/fb15911f-ddda-4b87-8334-471430c0e70f/download/2_in_merit_data_bm_skips_10_2026.csv"
        caveat: NESO does not say if times mark slice start or end; some monthly files are partial.
      - dataset: skip_rates_in_merit_psa
        differs: "Post System Action (PSA) basis: a more targeted measure, same columns, monthly files"
        request:
          - "GET https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/f8ec048d-7cd8-4eef-9323-f34311dd913c/download/3_in_merit_data_post_system_actions_skips_12_2024.csv"
          - "GET https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/b9806162-b605-4502-ac44-a419d2b010e5/download/3_in_merit_data_post_system_actions_skips_10_2026.csv"
        caveat: NESO does not say if times mark slice start or end; some monthly files are partial.
      - dataset: skip_rates_in_merit_psa_dsf_unit
        differs: The PSA detail with Demand Side Flexibility units as their own technology
        request: "GET https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/d02ef4f9-b2cf-4d0c-b851-521ba6976d44/download/6_dsf_in_merit_data_psa_skips.csv"
        held: Identical rows repeat and no column tells them apart, so there is no silver table.
      - dataset: skip_rates_stage5_dsf_technology
        differs: "Stage 5 skip rate for Demand Side Flexibility, per half hour and unit"
        request: "GET https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/8de48b80-48d7-4648-b812-9f91c992f559/download/7_dsf_speicfic_skip_rate.csv"
        held: Identical rows repeat and no column tells them apart, so there is no silver table.
      - dataset: skip_rates_stage5_psa_technology
        differs: "Stage 5 skip rate by technology, per half hour, bid or offer"
        request: "GET https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/007c5786-bd34-4a09-8bdf-be5d63eda16a/download/5_fuel_type_skip_rate.csv"
      - dataset: skip_rates_stage6_acceptance
        differs: "Accepted volumes and prices per unit at stage 6, five-minute"
        request: "GET https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/235e5cf1-745a-46e3-9e64-f7c8532abdc1/download/9_s6_acceptances.csv"
        caveat: NESO does not say whether each five-minute time marks the start or end of its slice.
      - dataset: skip_rates_stage6_psa
        differs: "Units in merit at stage 6, PSA basis, five-minute; uploaded monthly"
        request: "GET https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/32072115-34bd-4838-92ab-96803e1b692d/download/8_in_merit_s6_data_post_system_actions_skips.csv"
        caveat: NESO does not say whether each five-minute time marks the start or end of its slice.
  related:
    - {dataset: elexon/boal, note: "Elexon's accepted bids and offers: the actions taken instead of skipped volume"}
    - {dataset: neso_data_portal/constraint-breakdown, note: "NESO's daily constraint costs; two tables here count skips behind constraints"}
---

# Skip Rates

This package is NESO's **Skip Rates** publication. A **skip** is balancing-mechanism (BM) volume that
was available, was economically preferable to what NESO actually took, and was not accepted. The CKAN
package notes say the rates use a methodology developed with LCP Delta and are reported per 30 minutes
after each stage of exclusions set out in NESO's methodology
(@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json, in the gridflow checkout;
NESO skip-rate methodology and implementation guide, document 350061). The question it answers is "how
much cheaper volume did the control room pass over, and how much of that survives once units that could
not realistically have been used are excluded?" For a model it is a **retrospective measure of dispatch
efficiency**: it can explain why bid and offer volumes were accepted out of price order, and how that
varies by technology and over time. It is analytical output computed after the fact, **not a
settlement-run publication**, so it has no settlement `run_type`, and its **stages are methodology stages,
not settlement runs**. Do not dedup or join on `(date, period)` as if they were. Background:
@../../../20-domain/markets/gb-balancing-mechanism.md, @../../../20-domain/concepts/bm-units.md and
@../../../20-domain/concepts/settlement-period.md.

**Vocabulary** (NESO methodology and dispatch-transparency Q&A, document 379301, as read in the batch
research, @.planning/phases/v0.22-K-BAL-2/K-BAL-2-FACTS.md section 5, in the gridflow checkout):

- **All BM** skip: avoidable skips measured against all balancing-mechanism actions NESO could have
  taken in the period. **PSA** means **Post System Actions**, a more targeted measure that is not in the
  context of all actions taken at the time. The vendor says PSA skips are far fewer than All BM skips.
- **DSF** means **Demand Side Flexibility**. NESO describes it as a subset of technology types, not a
  separate technology.
- **Stages** 0 to 5 are successive exclusion stages. Stage 5 applies the long-notice and
  technical-feasibility exclusions. **Stage 6** adds the exclusion of energy-flagged volume used to
  position units for Mandatory Frequency Response (MFR), after the existing exclusions. Stage 0 is a
  methodology stage, not a missing-value marker; `TODO: verify` its exact definition against NESO
  document 350061.
- **Pair ID** is a signed identifier: negative pairs sit below the unit's FPN and positive pairs above it
  (NESO definition). `-1` is an identifier, not a null sentinel.

**Where each family stands (2026-10-12).** The package has **77 resources, all CSV uploads**, in
**eleven tabular families**. gridflow captured every resource on 2026-10-08, as immutable bronze
bytes, and seven again on 2026-10-16 (see Cadence). Nine families have a record and a silver table (175,057,350 rows in all); two have no record. Only
two silver families are eligible. **Seven are held** in gridflow; the front-end site shows their rows with a caveat naming the open question (ruling 66, 2026-10-24).

| Family | Resources | Grain | Rows (bronze = silver) | Status |
|---|---:|---|---:|---|
| `skip_rates_summary` | 1 | half-hour x stage | 190,368 | **silver, eligible** |
| `skip_rates_stage5_psa_technology` | 1 | half-hour x bid/offer x technology | 132,139 | **silver, eligible** |
| `skip_rates_behind_constraints_bmu` | 1 | month x BMU x bid/offer | 5,871 | silver, **held** |
| `skip_rates_behind_constraints_cons` | 1 | month x constraint | 236 | silver, **held** |
| `skip_rates_exclusion_reasons` | 23 | five-minute x BMU x pair x stage x reason | 15,575,765 | silver, **held** |
| `skip_rates_in_merit_all_bm` | 23 | five-minute x BMU x bid/offer x stage x pair | 84,931,005 | silver, **held** |
| `skip_rates_in_merit_psa` | 23 | five-minute x BMU x bid/offer x stage x pair | 65,776,812 | silver, **held** |
| `skip_rates_stage6_acceptance` | 1 | five-minute x BMU x bid/offer x stage x pair | 2,909,408 | silver, **held** |
| `skip_rates_stage6_psa` | 1 | five-minute x BMU x bid/offer x stage x pair | 5,535,746 | silver, **held** |
| `skip_rates_in_merit_psa_dsf_unit` | 1 | five-minute, DSF units | 431,215 (bronze) | **no record**, ingest-only |
| `skip_rates_stage5_dsf_technology` | 1 | half-hour x BMU x bid/offer x technology | 7,202 (bronze) | **no record**, ingest-only |

Row counts are the activation receipt (@.planning/v0.22-RESULTS.md section "BAL-2b", RULINGS 695) and
the seat's full-body bronze check (@.planning/phases/v0.22-K-BAL-2/BAL-2b-BRONZE-CHECK.json, RULINGS 690),
both in the gridflow checkout. Every silver count equals the bronze count, and the later `reconcile --all`
found 0 gaps (RULINGS 696). The bronze check found every body valid UTF-8 (four carry a UTF-8 byte-order
mark), one header per file, and no padded or non-numeric measure cells, so no trim was needed. Registry
records: @src/gridflow/connectors/neso_data_portal/registry/skip-rates.json; eligibility report:
@docs/neso_data_portal/eligibility.md (both in the gridflow checkout).

**Gotchas.**

- **Held means no model use.** Seven silver tables exist on disk and are held. They may not be used for
  point-in-time models until the questions in Holds are answered; the site shows their rows with a caveat. No gold view reads anything
  in this package.
- **The two DSF families have no record** because their bodies contain exact repeated rows, so no column
  key is unique (RULINGS 538: no record without a valid key; 7,830 excess repeated rows in the PSA DSF unit
  file and 192 in the stage-5 DSF technology file). This is not a missing `run_type`, and rows must not be
  deduplicated or given a row ordinal to force a key.
- **Vendor reissues replace history.** The vendor says it reissued all published datasets on 2025-05-15
  (marginal-unit and accepted-above-feasible-volume handling) and on 2025-11-18 (a long-notice exclusion
  bug). The early months therefore carry a 2025-11-18 `last_modified`, not their first-publication time,
  and gridflow holds at most two captures of each file (see Cadence). The one pair compared so far shows
  no silent revision, but a week is short (`TODO: verify` with repeated captures).
- **Silver is partitioned by capture month, not by event time.** Every silver file is under
  `year=2026/month=10` (the 2026-10-08 capture), including rows whose event time is December 2024.
- **Coverage defects in the monthly files are vendor behaviour,** not gridflow loss: see the September 2026
  and March 2026 resources under Holds. Do not assume a month's resource is a complete month.
- **The package name says "rates" but most families carry volumes.** The five-minute in-merit, stage-6 and
  exclusion families have **no rate column**; only the summary, the two technology summaries and the two
  behind-constraints families carry one.
- **Resource count drift.** The vendor coverage page (@../coverage.md) counted 69 resources for this
  package; the 2026-10-06 catalogue snapshot lists 77, and the registry and this page follow the snapshot.

- Publisher group: Balancing costs
- Registry group: balancing · archetype: SER
- Package page: [skip-rates](https://www.neso.energy/data-portal/skip-rates)
- Attribution: Supported by National Energy SO Open Data

## Files by disposition

Every one of the 77 resources is an uploaded CSV (`url_type` upload). The registry assigns **all 77 to
SILVER**: **77 SILVER, 0 DOC, 0 HOLD**. SILVER here means each CSV is a candidate data file for its
family; it does **not** mean a silver table exists (the two DSF families have none). There are **no DOC
files in this package**, so there are no document downloads. A resource's file is served at
`https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/<Id>/download/<file name>`.

Resource counts by family:

| Family | SILVER | DOC | HOLD |
|---|---:|---:|---:|
| `skip_rates_behind_constraints_bmu` | 1 | 0 | 0 |
| `skip_rates_behind_constraints_cons` | 1 | 0 | 0 |
| `skip_rates_exclusion_reasons` | 23 | 0 | 0 |
| `skip_rates_in_merit_all_bm` | 23 | 0 | 0 |
| `skip_rates_in_merit_psa` | 23 | 0 | 0 |
| `skip_rates_in_merit_psa_dsf_unit` | 1 | 0 | 0 |
| `skip_rates_stage5_dsf_technology` | 1 | 0 | 0 |
| `skip_rates_stage5_psa_technology` | 1 | 0 | 0 |
| `skip_rates_stage6_acceptance` | 1 | 0 | 0 |
| `skip_rates_stage6_psa` | 1 | 0 | 0 |
| `skip_rates_summary` | 1 | 0 | 0 |

The three 23-resource families have **one resource per calendar month, December 2024 to October 2026**.
The vendor's file name carries the month as `MM_YYYY`; the resource name carries the month name. The
other families are each one cumulative file. Vendor file names, with the CKAN `last_modified` shown in the
2026-10-06 catalogue snapshot (the capture of 2026-10-08 can carry a later stamp, given in the family
sections):

| Family | Vendor file name | Snapshot `last_modified` |
|---|---|---|
| `skip_rates_summary` | [1_skip_rates_summary.csv](https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/e4129210-ea22-4a36-aa2f-ff7bd6147675/download/1_skip_rates_summary.csv) | 2026-10-06 |
| `skip_rates_in_merit_all_bm` | `2_in_merit_data_bm_skips_MM_YYYY.csv`, e.g. [2_in_merit_data_bm_skips_01_2025.csv](https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/70d39639-4504-46b2-bae9-37428e96063d/download/2_in_merit_data_bm_skips_01_2025.csv) | 2025-11-18 to 2026-10-06 (13 distinct dates) |
| `skip_rates_in_merit_psa` | `3_in_merit_data_post_system_actions_skips_MM_YYYY.csv`, e.g. [3_in_merit_data_post_system_actions_skips_01_2025.csv](https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/3a4863d1-220e-43e5-9049-94db1045d92c/download/3_in_merit_data_post_system_actions_skips_01_2025.csv) | 2025-11-18 to 2026-10-06 (13 distinct dates) |
| `skip_rates_exclusion_reasons` | `4_exclusions_MM_YYYY.csv`, e.g. [4_exclusions_08_2025.csv](https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/ea2951b0-79d7-4575-a7d9-7d522ca2422c/download/4_exclusions_08_2025.csv) | 2025-11-18 to 2026-10-06 (13 distinct dates) |
| `skip_rates_stage5_psa_technology` | [5_fuel_type_skip_rate.csv](https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/007c5786-bd34-4a09-8bdf-be5d63eda16a/download/5_fuel_type_skip_rate.csv) | 2026-10-06 |
| `skip_rates_in_merit_psa_dsf_unit` | [6_dsf_in_merit_data_psa_skips.csv](https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/d02ef4f9-b2cf-4d0c-b851-521ba6976d44/download/6_dsf_in_merit_data_psa_skips.csv) | 2026-10-06 |
| `skip_rates_stage5_dsf_technology` | [7_dsf_speicfic_skip_rate.csv](https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/8de48b80-48d7-4648-b812-9f91c992f559/download/7_dsf_speicfic_skip_rate.csv) (the vendor's spelling) | 2026-10-06 |
| `skip_rates_stage6_psa` | [8_in_merit_s6_data_post_system_actions_skips.csv](https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/32072115-34bd-4838-92ab-96803e1b692d/download/8_in_merit_s6_data_post_system_actions_skips.csv) | 2026-09-21 |
| `skip_rates_stage6_acceptance` | [9_s6_acceptances.csv](https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/235e5cf1-745a-46e3-9e64-f7c8532abdc1/download/9_s6_acceptances.csv) | 2026-02-04 |
| `skip_rates_behind_constraints_bmu` | [skips_behind_constraints_in_merit_bmu_level.csv](https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/26f3a3de-e5fd-43e5-9d8a-d89a9c786812/download/skips_behind_constraints_in_merit_bmu_level.csv) | 2026-09-28 |
| `skip_rates_behind_constraints_cons` | [skips_behind_constraints_in_merit_constraint_level.csv](https://api.neso.energy/dataset/c7f21d91-4e93-4162-9caa-ad9165db9c5e/resource/a88adc4c-d3a6-440d-946b-4e5a3e7ea1c5/download/skips_behind_constraints_in_merit_constraint_level.csv) | 2026-09-28 |

The CKAN resources declare no byte size or hash. Captured sizes and row counts are in the bronze check
named above.

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| In Merit PSA for Demand Side Flexibility Unit | CSV | upload | `d02ef4f9-b2cf-4d0c-b851-521ba6976d44` |
| Skip Rate - Exclusion Reasons - April 2025 | CSV | upload | `a3d3e2ea-f099-483c-a61c-a4fb883db52b` |
| Skip Rate - Exclusion Reasons - April 2026 | CSV | upload | `5fc6319d-0ceb-4bad-99d6-653ef23cbed0` |
| Skip Rate - Exclusion Reasons - August 2025 | CSV | upload | `ea2951b0-79d7-4575-a7d9-7d522ca2422c` |
| Skip Rate - Exclusion Reasons - August 2026 | CSV | upload | `a82a2a20-6f08-4d7d-a2ed-221527ba75c2` |
| Skip Rate - Exclusion Reasons - December 2024 | CSV | upload | `c20e81a0-1c82-4e03-913e-9e73d6daca6b` |
| Skip Rate - Exclusion Reasons - December 2025 | CSV | upload | `cba84b51-1a29-43a6-b643-73670a71bb7f` |
| Skip Rate - Exclusion Reasons - February 2025 | CSV | upload | `16e874cf-7b26-4fea-bf39-aa153f552e20` |
| Skip Rate - Exclusion Reasons - February 2026 | CSV | upload | `4da36ea5-ea48-45ef-ab50-29751bff476b` |
| Skip Rate - Exclusion Reasons - January 2025 | CSV | upload | `fa3df861-bbdd-4d60-8e84-9b7f9351ba48` |
| Skip Rate - Exclusion Reasons - January 2026 | CSV | upload | `c81b5b16-3650-45f5-8dce-2765c840f50a` |
| Skip Rate - Exclusion Reasons - July 2025 | CSV | upload | `5fed7209-7f33-4b19-9858-84a967df0351` |
| Skip Rate - Exclusion Reasons - July 2026 | CSV | upload | `db88ded4-bb64-4b5a-851d-bdd6eabb397d` |
| Skip Rate - Exclusion Reasons - June 2025 | CSV | upload | `f6a6beb1-1117-4798-b5c4-68e6d60ccb0b` |
| Skip Rate - Exclusion Reasons - June 2026 | CSV | upload | `f2879df1-32d2-4faf-b4e4-28d33059960b` |
| Skip Rate - Exclusion Reasons - March 2025 | CSV | upload | `1b310928-3800-4402-9ee2-29e6815fa5a9` |
| Skip Rate - Exclusion Reasons - March 2026 | CSV | upload | `be20790b-f860-4d8e-bdcc-8ec4311b2058` |
| Skip Rate - Exclusion Reasons - May 2025 | CSV | upload | `8eed92f7-5450-476e-bfce-06af1385d75a` |
| Skip Rate - Exclusion Reasons - May 2026 | CSV | upload | `6f4319a1-ee65-442a-8081-f6e71713ba7f` |
| Skip Rate - Exclusion Reasons - November 2025 | CSV | upload | `1db68aaf-7d1b-4041-8556-a71383159944` |
| Skip Rate - Exclusion Reasons - October 2025 | CSV | upload | `9a90687c-265b-4f58-820f-43870c9a5256` |
| Skip Rate - Exclusion Reasons - October 2026 | CSV | upload | `f8110eb8-f4ad-4288-87d5-37ab434b55b5` |
| Skip Rate - Exclusion Reasons - September 2025 | CSV | upload | `51ae34f6-10bb-409e-8feb-6d07e8c4fbed` |
| Skip Rate - Exclusion Reasons - September 2026 | CSV | upload | `1679aa42-0184-4564-8bf5-406f6b0bc594` |
| Skip Rate - In Merit All Balancing Mechanism - April 2025 | CSV | upload | `c66e6ad7-98c1-46a1-8f6f-376876d9f9ed` |
| Skip Rate - In Merit All Balancing Mechanism - April 2026 | CSV | upload | `61c8f88d-87d4-4dc8-8ff8-89e4cdfb226f` |
| Skip Rate - In Merit All Balancing Mechanism - August 2025 | CSV | upload | `d9fca2ec-54f1-4b8c-9a78-7c84617f0d9d` |
| Skip Rate - In Merit All Balancing Mechanism - August 2026 | CSV | upload | `ce31e61b-ebc5-4c6f-846f-d5a971e019a0` |
| Skip Rate - In Merit All Balancing Mechanism - December 2024 | CSV | upload | `ec422c87-a316-47bf-95a2-4e0cd07114dc` |
| Skip Rate - In Merit All Balancing Mechanism - December 2025 | CSV | upload | `be364fbd-9ac3-4dd9-a0fd-6d2a80c4251c` |
| Skip Rate - In Merit All Balancing Mechanism - February 2025 | CSV | upload | `dbc0479f-0606-47d4-98fe-49923378d9f6` |
| Skip Rate - In Merit All Balancing Mechanism - February 2026 | CSV | upload | `51371db9-ef87-487c-b97e-bcacc6856374` |
| Skip Rate - In Merit All Balancing Mechanism - January 2025 | CSV | upload | `70d39639-4504-46b2-bae9-37428e96063d` |
| Skip Rate - In Merit All Balancing Mechanism - January 2026 | CSV | upload | `98d84000-6639-440c-ae2c-4a9a6c86a865` |
| Skip Rate - In Merit All Balancing Mechanism - July 2025 | CSV | upload | `7337899d-1bda-4a50-a82d-49c2140b094a` |
| Skip Rate - In Merit All Balancing Mechanism - July 2026 | CSV | upload | `c12fdef0-0b18-439d-a16c-c97fbd93c45d` |
| Skip Rate - In Merit All Balancing Mechanism - June 2025 | CSV | upload | `d6fdf8bd-a2d5-4f91-81f9-2542e1fa7586` |
| Skip Rate - In Merit All Balancing Mechanism - June 2026 | CSV | upload | `83ad3fa4-5a79-4119-9511-4005b4f3c584` |
| Skip Rate - In Merit All Balancing Mechanism - March 2025 | CSV | upload | `19dcbf5b-2868-4cce-aeb4-068d42bc17d2` |
| Skip Rate - In Merit All Balancing Mechanism - March 2026 | CSV | upload | `bb251d50-126a-4fbc-a0b8-bf137a900801` |
| Skip Rate - In Merit All Balancing Mechanism - May 2025 | CSV | upload | `fd68196f-349e-4d6e-a4fc-fb8e538c600e` |
| Skip Rate - In Merit All Balancing Mechanism - May 2026 | CSV | upload | `0c358c48-72f6-4f65-a738-2fa4ce182692` |
| Skip Rate - In Merit All Balancing Mechanism - November 2025 | CSV | upload | `7c90cdbb-ce59-4ab9-b41a-d05a912fd587` |
| Skip Rate - In Merit All Balancing Mechanism - October 2025 | CSV | upload | `426f4ead-8d24-4196-9425-c42c6788f617` |
| Skip Rate - In Merit All Balancing Mechanism - October 2026 | CSV | upload | `fb15911f-ddda-4b87-8334-471430c0e70f` |
| Skip Rate - In Merit All Balancing Mechanism - September 2025 | CSV | upload | `413a8f68-855c-4cc2-95a2-916001753bf7` |
| Skip Rate - In Merit All Balancing Mechanism - September 2026 | CSV | upload | `ca3587a2-ae0d-47db-b0a1-4d681af8bced` |
| Skip Rate - In Merit Post System Action - April 2025 | CSV | upload | `e3c6852a-2814-4f03-9998-639e85881cf6` |
| Skip Rate - In Merit Post System Action - April 2026 | CSV | upload | `973563c8-295a-4d08-bd72-ef529b82bf9a` |
| Skip Rate - In Merit Post System Action - August 2025 | CSV | upload | `9884e31f-a513-4770-a0ae-d66e46d696dc` |
| Skip Rate - In Merit Post System Action - August 2026 | CSV | upload | `80f792cd-8985-4f94-b073-8756b0b4211c` |
| Skip Rate - In Merit Post System Action - December 2024 | CSV | upload | `f8ec048d-7cd8-4eef-9323-f34311dd913c` |
| Skip Rate - In Merit Post System Action - December 2025 | CSV | upload | `a4db6822-66cf-40f4-92a7-9712703b4575` |
| Skip Rate - In Merit Post System Action - February 2025 | CSV | upload | `9ba454f6-5b45-4e54-be41-a1e3a9ba3520` |
| Skip Rate - In Merit Post System Action - February 2026 | CSV | upload | `4b0599e1-5022-4335-9193-49b75dd85b21` |
| Skip Rate - In Merit Post System Action - January 2025 | CSV | upload | `3a4863d1-220e-43e5-9049-94db1045d92c` |
| Skip Rate - In Merit Post System Action - January 2026 | CSV | upload | `84868db8-cbd8-42d0-8972-b6b5da6187c8` |
| Skip Rate - In Merit Post System Action - July 2025 | CSV | upload | `ffb84e07-85ec-4c2e-a643-934cf6354b32` |
| Skip Rate - In Merit Post System Action - July 2026 | CSV | upload | `85a2af4e-d3de-4f11-80cf-309e39b94b59` |
| Skip Rate - In Merit Post System Action - June 2025 | CSV | upload | `a9105348-c2c4-4a16-8a11-b061747f5832` |
| Skip Rate - In Merit Post System Action - June 2026 | CSV | upload | `96a1a331-bd61-498b-8880-d9a02a58df0e` |
| Skip Rate - In Merit Post System Action - March 2025 | CSV | upload | `70531959-ccc0-4453-aebb-0fbbb7e4c308` |
| Skip Rate - In Merit Post System Action - March 2026 | CSV | upload | `a04c4c6e-0526-42b4-99d0-eb114beba8a2` |
| Skip Rate - In Merit Post System Action - May 2025 | CSV | upload | `c53434d5-9bd2-4702-8b64-bd111c43d3fe` |
| Skip Rate - In Merit Post System Action - May 2026 | CSV | upload | `f3a834c0-71c5-4efb-909e-5b7dd2f2c11f` |
| Skip Rate - In Merit Post System Action - November 2025 | CSV | upload | `f2f15724-8780-4ff4-904a-f36915a4f98e` |
| Skip Rate - In Merit Post System Action - October 2025 | CSV | upload | `eb166d7b-5a59-4bdf-9e38-b0ab4d530fe2` |
| Skip Rate - In Merit Post System Action - October 2026 | CSV | upload | `b9806162-b605-4502-ac44-a419d2b010e5` |
| Skip Rate - In Merit Post System Action - September 2025 | CSV | upload | `6549a9d8-d61c-4929-983e-dec122e8d13c` |
| Skip Rate - In Merit Post System Action - September 2026 | CSV | upload | `38421f3d-8949-4dcf-81cf-0295a8688086` |
| Skip Rate - Stage 6 Acceptance | CSV | upload | `235e5cf1-745a-46e3-9e64-f7c8532abdc1` |
| Skip Rate - Summary | CSV | upload | `e4129210-ea22-4a36-aa2f-ff7bd6147675` |
| Skips Behind Constraints - In Merit BMU-Level | CSV | upload | `26f3a3de-e5fd-43e5-9d8a-d89a9c786812` |
| Skips Behind Constraints - In Merit Constraint-Level | CSV | upload | `a88adc4c-d3a6-440d-946b-4e5a3e7ea1c5` |
| Stage 5 DSF Technology-Specific Skip Rate | CSV | upload | `8de48b80-48d7-4648-b812-9f91c992f559` |
| Stage 5 PSA Skip Rate by Technology | CSV | upload | `007c5786-bd34-4a09-8bdf-be5d63eda16a` |
| Stage 6 PSA Skip Rate | CSV | upload | `32072115-34bd-4838-92ab-96803e1b692d` |

## Families

### `skip_rates_behind_constraints_bmu`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| month | `month_vendor` | string | — | no | — | YearMonth UTC |
| bm_unit | `bm_unit` | string | — | no | — | — |
| bid_offer | `bid_offer` | string | — | no | — | — |
| fuel_type | `fuel_type` | string | — | yes | — | — |
| skipped_volume_mwh | `skipped_volume_mwh` | float64 | — | yes | — | MWh |
| in_merit_volume_mwh | `in_merit_volume_mwh` | float64 | — | yes | — | MWh |
| skip_rate | `skip_rate` | float64 | — | yes | — | Percentage |

- Entity key: `month_vendor`, `bm_unit`, `bid_offer`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What it is.** A **monthly BMU-level view of skips behind active thermal constraints**: the volume of
in-merit bid and offer actions that were skipped after accounting for accepted balancing actions taken for
constraint management (CKAN resource description; NESO constraint-skip publication, document 387436). One
resource, one cumulative file, **5,871 rows**, grain month x `bm_unit` x `bid_offer` (unique across all
rows; values are not part of the key). Coverage December 2024 to August 2026 (the resource's rows).
`fuel_type` is nullable. The body carries a UTF-8 byte-order mark.

**Units (vendor dictionary).** `skipped_volume_mwh` and `in_merit_volume_mwh` MWh; `skip_rate` Percentage;
`month` is documented as `YearMonth UTC`. The BMU identifier is stored as supplied.

**Clocks.** Vintage `ckan_last_modified` (capture value 2026-09-28T12:04:03.117796). Event time: `none`.
The vendor month is a UTC month, and the current month recipe anchors on London midnight, so the raw
`month_vendor` string is kept and `timestamp_utc` is the capture time.

**Held.** The silver table exists on disk but may not be used for point-in-time work; the site shows its rows with a caveat. The hold is the rate denominator (`TODO: CONSTRAINT-RATE-DENOMINATOR`, see Holds). Because the
denominator is open, do not recompute or reinterpret `skip_rate`.

### `skip_rates_behind_constraints_cons`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| month | `month_vendor` | string | — | no | — | YearMonth UTC |
| constraint | `constraint` | string | — | no | — | — |
| skipped_volume_mwh | `skipped_volume_mwh` | float64 | — | yes | — | MWh |
| in_merit_volume_mwh | `in_merit_volume_mwh` | float64 | — | yes | — | MWh |
| skip_rate | `skip_rate` | float64 | — | yes | — | Percentage |

- Entity key: `month_vendor`, `constraint`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What it is.** The **monthly constraint-level** companion to the BMU file: the same measure aggregated to
each constraint name. One resource, **236 rows**, grain month x `constraint` (unique). Coverage December
2024 to August 2026. The body carries a UTF-8 byte-order mark. Constraint identifiers are preserved as
supplied.

**Units (vendor dictionary).** Volumes MWh; `skip_rate` Percentage; `month` is `YearMonth UTC`.

**Clocks.** Vintage `ckan_last_modified` (capture value 2026-09-28T12:08:43.108251). Event time: `none`;
raw `month_vendor` kept, `timestamp_utc` is the capture time.

**Held.** The silver table exists on disk but may not be used for point-in-time work; the site shows its rows with a caveat. Same hold as the BMU file (`TODO: CONSTRAINT-RATE-DENOMINATOR`).

### `skip_rates_exclusion_reasons`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| date | `date_vendor` | string | — | no | — | DateTime UTC |
| bm_unit | `bm_unit` | string | — | no | — | — |
| fuel | `fuel` | string | — | yes | — | — |
| bid_offer | `bid_offer` | string | — | no | — | — |
| excluded_from_accepted_or_feasible_merit_stack | `excluded_from_accepted_or_feasible_merit_stack` | string | — | no | — | — |
| exclusion_stage | `exclusion_stage` | int64 | — | no | — | — |
| pair_id | `pair_id` | int64 | — | no | — | — |
| average_price_per_MWh | `average_price_per_mwh` | float64 | — | yes | — | £/MWh |
| excluded_volume_MWh | `excluded_volume_mwh` | float64 | — | yes | — | MWh |
| exclusion_reason | `exclusion_reason` | string | — | no | — | — |

- Entity key: `resource_id`, `date_vendor`, `bm_unit`, `bid_offer`, `excluded_from_accepted_or_feasible_merit_stack`, `exclusion_stage`, `pair_id`, `exclusion_reason`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What it is.** The list of **BM units that were excluded from the accepted or feasible merit stack, and
why**, at five-minute resolution, with the stack, the exclusion stage, the pair and the reason. One
resource per month, **23 resources, 15,575,765 rows**, December 2024 to October 2026. The 23 resource
month sets are disjoint and no key overlaps between them, so the family keeps `resource_id` in the key and
takes the latest capture per resource (`latest_partition` = `resource_id`). Several reasons can apply to
one unit and stage, so the stack and the reason are part of the key. Observed `exclusion_stage` runs from 1
to 5.

**Units (vendor dictionary, FACTS g4).** Volumes MWh; average price GBP per MWh (`£/MWh`); `stage`, `exclusion_stage` and `pair_id` are dimensionless identifiers. Blank cells are nulls (no `NA` or `N/A` text tokens, no thousands separators, currency or percent signs in any data cell); zeros are real zeros and stay zeros (FACTS g5). `fuel` is nullable and is kept as supplied; no technology code is invented for a blank.

**Clocks.** Vintage `ckan_last_modified`: `available_at` is the CKAN `last_modified` of the captured file (an upload stamp, not an issue time). Event time: `none`, so `timestamp_utc` is the **capture time**, not an observation time. The vendor's `date` is kept as the raw string `date_vendor`. The vendor dictionary says the column is UTC at five-minute resolution, but the support guide describes the stamp ambiguously as giving the start and end of the period, so whether it marks the slice start or end is open (`TODO: SKIP-DATE-ENDPOINT`). Observed spellings are naive or `Z`; no conflicting offset appears, so no clock correction applies.

**Held.** The silver table exists on disk but may not be used for point-in-time work; the site shows its rows with a caveat. The hold is the five-minute endpoint (`TODO: SKIP-DATE-ENDPOINT`).

### `skip_rates_in_merit_all_bm`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| date | `date_vendor` | string | — | no | — | DateTime UTC |
| bm_unit | `bm_unit` | string | — | no | — | — |
| fuel | `fuel` | string | — | yes | — | — |
| bid_offer | `bid_offer` | string | — | no | — | — |
| stage | `stage` | int64 | — | no | — | — |
| available_volume_MWh | `available_volume_mwh` | float64 | — | yes | — | MWh |
| average_price_per_MWh | `average_price_per_mwh` | float64 | — | yes | — | £/MWh |
| pair_id | `pair_id` | int64 | — | no | — | — |
| accepted_volume_MWh | `accepted_volume_mwh` | float64 | — | yes | — | MWh |
| in_merit_volume_MWh | `in_merit_volume_mwh` | float64 | — | yes | — | MWh |
| skipped_volume_MWh | `skipped_volume_mwh` | float64 | — | yes | — | MWh |

- Entity key: `resource_id`, `date_vendor`, `bm_unit`, `bid_offer`, `stage`, `pair_id`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What it is.** The **All Balancing Mechanism skip** detail: for each five-minute slice, BM unit,
bid/offer, stage and pair, the available volume, average price, accepted volume, in-merit volume and
skipped volume. One resource per month, **23 resources, 84,931,005 rows**, December 2024 to October 2026.
Resource month sets are disjoint (zero key overlaps) and every full-body key is unique. Observed `stage`
runs 0 to 5. There is **no rate column**; any rate derived from these volumes needs the vendor's formula
(`TODO: verify`).

**Units (vendor dictionary, FACTS g4).** Volumes MWh; average price GBP per MWh (`£/MWh`); `stage`, `exclusion_stage` and `pair_id` are dimensionless identifiers. Blank cells are nulls (no `NA` or `N/A` text tokens, no thousands separators, currency or percent signs in any data cell); zeros are real zeros and stay zeros (FACTS g5). `fuel` is nullable and is kept as supplied; no technology code is invented for a blank.

**Clocks.** Vintage `ckan_last_modified`: `available_at` is the CKAN `last_modified` of the captured file (an upload stamp, not an issue time). Event time: `none`, so `timestamp_utc` is the **capture time**, not an observation time. The vendor's `date` is kept as the raw string `date_vendor`. The vendor dictionary says the column is UTC at five-minute resolution, but the support guide describes the stamp ambiguously as giving the start and end of the period, so whether it marks the slice start or end is open (`TODO: SKIP-DATE-ENDPOINT`). Observed spellings are naive or `Z`; no conflicting offset appears, so no clock correction applies.

**Held.** The silver table exists on disk but may not be used for point-in-time work; the site shows its rows with a caveat. Two questions: the endpoint (`TODO: SKIP-DATE-ENDPOINT`) and the September 2026 resource
`ca3587a2-ae0d-47db-b0a1-4d681af8bced`, which holds **30 September 2026 only** (00:00:00Z to 23:55:00Z,
387,189 rows). Do not claim whole-month coverage for September 2026 (`TODO: ALL-BM-SEPTEMBER-COVERAGE`).
Peak memory to transform this family was 4,769.9 MiB (RULINGS 695), the heaviest in the package.

### `skip_rates_in_merit_psa`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| date | `date_vendor` | string | — | no | — | DateTime UTC |
| bm_unit | `bm_unit` | string | — | no | — | — |
| fuel | `fuel` | string | — | yes | — | — |
| bid_offer | `bid_offer` | string | — | no | — | — |
| stage | `stage` | int64 | — | no | — | — |
| available_volume_MWh | `available_volume_mwh` | float64 | — | yes | — | MWh |
| average_price_per_MWh | `average_price_per_mwh` | float64 | — | yes | — | £/MWh |
| pair_id | `pair_id` | int64 | — | no | — | — |
| accepted_volume_MWh | `accepted_volume_mwh` | float64 | — | yes | — | MWh |
| in_merit_volume_MWh | `in_merit_volume_mwh` | float64 | — | yes | — | MWh |
| skipped_volume_MWh | `skipped_volume_mwh` | float64 | — | yes | — | MWh |

- Entity key: `resource_id`, `date_vendor`, `bm_unit`, `bid_offer`, `stage`, `pair_id`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What it is.** The **Post System Actions** counterpart of the All BM detail, with the same columns and
grain: five-minute slice, BM unit, bid/offer, stage and pair. One resource per month, **23 resources,
65,776,812 rows**, December 2024 to October 2026, disjoint month sets, unique full-body keys. Observed
`stage` runs 0 to 5. No rate column.

**Units (vendor dictionary, FACTS g4).** Volumes MWh; average price GBP per MWh (`£/MWh`); `stage`, `exclusion_stage` and `pair_id` are dimensionless identifiers. Blank cells are nulls (no `NA` or `N/A` text tokens, no thousands separators, currency or percent signs in any data cell); zeros are real zeros and stay zeros (FACTS g5). `fuel` is nullable and is kept as supplied; no technology code is invented for a blank.

**Clocks.** Vintage `ckan_last_modified`: `available_at` is the CKAN `last_modified` of the captured file (an upload stamp, not an issue time). Event time: `none`, so `timestamp_utc` is the **capture time**, not an observation time. The vendor's `date` is kept as the raw string `date_vendor`. The vendor dictionary says the column is UTC at five-minute resolution, but the support guide describes the stamp ambiguously as giving the start and end of the period, so whether it marks the slice start or end is open (`TODO: SKIP-DATE-ENDPOINT`). Observed spellings are naive or `Z`; no conflicting offset appears, so no clock correction applies.

**Held.** The silver table exists on disk but may not be used for point-in-time work; the site shows its rows with a caveat. Two questions: the endpoint (`TODO: SKIP-DATE-ENDPOINT`) and two **coverage defects**:

- The March 2026 resource `a04c4c6e-0526-42b4-99d0-eb114beba8a2` holds **exactly 3,200,000 rows** and
  stops at `2026-03-24T15:45:00`. The round row count does not prove the cause.
- The September 2026 resource `38421f3d-8949-4dcf-81cf-0295a8688086` holds **30 September 2026 only**
  (273,888 rows, ending 23:55:00Z).

Both need a vendor explanation or corrected bodies (`TODO: PSA-MARCH/SEPTEMBER-COVERAGE`).

### `skip_rates_in_merit_psa_dsf_unit`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no
- ingest-only: no silver yet

**What it is.** A subset of the PSA in-merit data that identifies Demand Side Flexibility assets as a
unique technology type (CKAN resource description). One resource, **431,215 bronze rows**, with the same
eleven columns as the PSA in-merit detail (`date`, `bm_unit`, `fuel`, `bid_offer`, `stage`,
`available_volume_MWh`, `average_price_per_MWh`, `pair_id`, `accepted_volume_MWh`, `in_merit_volume_MWh`,
`skipped_volume_MWh`). Range `2024-12-15T00:00:00` to `2026-10-06T20:15:00`; capture `last_modified`
2026-10-07T10:42:44.918610.

**State.** Bronze only; **no record** (RULINGS 538, 690). The body contains **7,830 excess repeated full
rows** (431,215 rows, 423,385 distinct), so no column key is unique and adding value columns cannot help.
Do not deduplicate, add a row ordinal or treat this as a missing `run_type`. A record needs a corrected
vendor body or an applicable explicit adjudication.

**Units (vendor dictionary).** Volumes MWh; average price GBP per MWh. **Clocks if a record existed:** vintage
`ckan_last_modified`; the `date` would be kept raw with event time `none` (the same endpoint question,
`TODO: SKIP-DATE-ENDPOINT`).

### `skip_rates_stage5_dsf_technology`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no
- ingest-only: no silver yet

**What it is.** The skip rate **specific to Demand Side Flexibility as a technology type**, per 30-minute
period, calculated at stage 5 from the post-system-actions data (CKAN resource description). One
resource, **7,202 bronze rows**, columns `settlement_period_start`, `bm_unit`, `bid_offer`, `fuel`,
`in_merit_volume_MWh`, `skipped_volume_MWh` and `technology_specific_skip_rate`. Despite "technology" in
the name, **BMU is an explicit dimension**. Range through `2026-10-06T20:00:00`; capture `last_modified`
2026-10-07T10:42:49.846493.

**State.** Bronze only; **no record** (RULINGS 538, 690). The candidate key (period, `bm_unit`,
`bid_offer`, `fuel`) has duplicates, and full-row uniqueness also fails by **192 repeated rows**
(7,202 rows, 7,010 distinct). No row ordinal or deduplication is allowed.

**Units (vendor dictionary).** Volumes MWh; `technology_specific_skip_rate` Percentage. **Clocks if a
record existed:** `settlement_period_start` is the UTC period start (dictionary and technology-summary
guidance), so `utc_instant` would be appropriate; vintage `ckan_last_modified`.

### `skip_rates_stage5_psa_technology`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| settlement_period_start | `settlement_period_start` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | DateTime UTC |
| bid_offer | `bid_offer` | string | — | no | — | — |
| fuel | `fuel` | string | — | yes | — | — |
| relative_technology_skip_rate | `relative_technology_skip_rate` | float64 | — | yes | — | Percentage |
| technology_specific_skip_rate | `technology_specific_skip_rate` | float64 | — | yes | — | Percentage |
| fuel_in_merit_volume_MWh | `fuel_in_merit_volume_mwh` | float64 | — | yes | — | MWh |
| fuel_skipped_volume_MWh | `fuel_skipped_volume_mwh` | float64 | — | yes | — | MWh |

- Entity key: `settlement_period_start`, `bid_offer`, `fuel`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`settlement_period_start`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What it is.** A **summary of the skip rate by technology type for each 30-minute period**, calculated at
stage 5 from the post-system-actions data (CKAN resource description). One resource, **132,139 rows**,
grain `settlement_period_start` x `bid_offer` (`Bid` or `Offer`) x `fuel`, unique across all rows including
the blank-fuel group. 31,604 distinct half-hours from `2024-12-15T00:00:00Z` to `2026-10-07T23:30:00Z`.
Capture `last_modified` 2026-10-08T08:58:11.847497.

**Units (vendor dictionary).** `relative_technology_skip_rate` and `technology_specific_skip_rate` are
Percentage, taken as published (do not rescale); `fuel_in_merit_volume_mwh` and `fuel_skipped_volume_mwh`
are MWh. `TODO: verify` the formal difference between the two rates and each one's denominator in NESO
document 367966 ("Interpreting NESO skip rate datasets"); the two columns must not be treated as
interchangeable.

**Clocks.** Vintage `ckan_last_modified`: `available_at` is the CKAN `last_modified` of the captured file.
Event time: recipe `utc_instant` on `settlement_period_start`. The vendor dictionary says UTC and the
support guide expressly identifies the **settlement-period start**; the source spelling is naive, and UTC
is attached from that explicit clock. `timestamp_utc` equals the period start. The file carries no
settlement period number, so there is no 46/50-period day issue; map to settlement periods through the UTC
instant.

**Missingness and labels.** `fuel` is blank in 8,933 rows and is kept null (no technology invented). Fifteen
`fuel` values occur including null: `BATTERY`, `BIOMASS`, `CCGT`, `DIESEL`, `GAS`, `GAS REC ENGINE`,
`LOAD REPSONSE`, `LOAD RESPONSE`, `LOAD_RESPONSE`, `NPSHYD`, `OCGT`, `PS`, `SOLAR`, `WIND`. The vendor
spells load response three ways (one is a typo); they are stored as-is and are **not** merged, so a
technology filter must list all three. Skipped-volume zeros: 15,134 rows; the longest consecutive zero run
in the rate and volume columns is 5. Zeros are real values. 172 half-hours inside the range have no row at
all (scattered through the range); `TODO: verify` the cause. A half-hour with no row is not a zero.

**Eligible.** Silver is eligible: 132,139 rows from the 2026-10-08 capture, `dataset_version` `1+e1`; the
2026-10-16 capture adds a second silver file (see Cadence).

Silver sample (two rows, same half-hour):

```python
[
    {"settlement_period_start": "2024-12-15T00:00:00Z", "bid_offer": "Bid", "fuel": "PS",
     "relative_technology_skip_rate": 100.0, "technology_specific_skip_rate": 100.0,
     "fuel_in_merit_volume_mwh": 0.01, "fuel_skipped_volume_mwh": 0.01,
     "timestamp_utc": "2024-12-15T00:00:00Z", "published_at": "2026-10-08T08:58:11.847497Z"},
    {"settlement_period_start": "2024-12-15T00:00:00Z", "bid_offer": "Offer", "fuel": None,
     "relative_technology_skip_rate": 0.0, "technology_specific_skip_rate": 0.0,
     "fuel_in_merit_volume_mwh": 0.02, "fuel_skipped_volume_mwh": 0.0,
     "timestamp_utc": "2024-12-15T00:00:00Z", "published_at": "2026-10-08T08:58:11.847497Z"},
]
```

Silver lives at `C:/gridflow-data/silver/neso_data_portal/skip_rates_stage5_psa_technology/year=2026/month=10/`;
system columns as for the summary.

### `skip_rates_stage6_acceptance`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| date | `date_vendor` | string | — | no | — | DateTime UTC |
| stage | `stage` | int64 | — | no | — | — |
| bm_unit | `bm_unit` | string | — | no | — | — |
| fuel | `fuel` | string | — | yes | — | — |
| bid_offer | `bid_offer` | string | — | no | — | — |
| pair_id | `pair_id` | int64 | — | no | — | MWh |
| average_price_per_MWh | `average_price_per_mwh` | float64 | — | yes | — | £/MWh |
| accepted_volume_MWh | `accepted_volume_mwh` | float64 | — | yes | — | MWh |

- Entity key: `date_vendor`, `bm_unit`, `bid_offer`, `stage`, `pair_id`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What it is.** The **accepted bid and offer volumes with their prices for each unit at five-minute
intervals, at stage 6**, after excluding volumes such as 0-SEL volume for long-notice units and volumes
instructed to position units for Mandatory Frequency Response (CKAN resource description). One resource,
**2,909,408 rows**, columns `date`, `stage`, `bm_unit`, `fuel`, `bid_offer`, `pair_id`,
`average_price_per_MWh`, `accepted_volume_MWh`; the body contains stage 6 only. Range
`2025-01-01T00:00:00Z` to `2025-12-31T23:55:00Z` (calendar 2025 only); capture `last_modified`
2026-02-04T08:47:52.060966. This is **not the same coverage as the stage-6 PSA file**. The key is unique
across all rows. The body carries a UTF-8 byte-order mark.

**Dictionary conflict.** The vendor dictionary gives `pair_id` the unit **MWh** while describing a signed
identifier. It is an identifier, not an energy quantity, and is stored as an integer with no unit; the
conflict is recorded here and `TODO: verify` with the vendor. Accepted volume is MWh; average price
GBP per MWh.

**Clocks.** Vintage `ckan_last_modified`: `available_at` is the CKAN `last_modified` of the captured file (an upload stamp, not an issue time). Event time: `none`, so `timestamp_utc` is the **capture time**, not an observation time. The vendor's `date` is kept as the raw string `date_vendor`. The vendor dictionary says the column is UTC at five-minute resolution, but the support guide describes the stamp ambiguously as giving the start and end of the period, so whether it marks the slice start or end is open (`TODO: SKIP-DATE-ENDPOINT`). Observed spellings are naive or `Z`; no conflicting offset appears, so no clock correction applies.

**Held.** The silver table exists on disk but may not be used for point-in-time work; the site shows its rows with a caveat. The hold is the endpoint (`TODO: SKIP-DATE-ENDPOINT`).

### `skip_rates_stage6_psa`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| date | `date_vendor` | string | — | no | — | DateTime UTC |
| bm_unit | `bm_unit` | string | — | no | — | — |
| fuel | `fuel` | string | — | yes | — | — |
| bid_offer | `bid_offer` | string | — | no | — | — |
| stage | `stage` | int64 | — | no | — | — |
| available_volume_MWh | `available_volume_mwh` | float64 | — | yes | — | MWh |
| average_price_per_MWh | `average_price_per_mwh` | float64 | — | yes | — | £/MWh |
| pair_id | `pair_id` | int64 | — | no | — | — |
| accepted_volume_MWh | `accepted_volume_mwh` | float64 | — | yes | — | MWh |
| in_merit_volume_MWh | `in_merit_volume_mwh` | float64 | — | yes | — | MWh |
| skipped_volume_MWh | `skipped_volume_mwh` | float64 | — | yes | — | MWh |

- Entity key: `date_vendor`, `bm_unit`, `bid_offer`, `stage`, `pair_id`
- Latest: `whole_capture`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What it is.** A full list of units that were **in merit according to stage 6** of the methodology, with
available, accepted, in-merit and skipped volume, on a post-system-actions basis (CKAN resource
description, which says the file is uploaded monthly). One resource, **5,535,746 rows**, five-minute
grain, the eleven PSA in-merit columns with stage 6 only. Range `2024-12-15T00:00:00Z` to
`2026-08-31T23:55:00Z`; capture `last_modified` 2026-09-21T13:39:18.302571. The key is unique across all
rows. The body carries a UTF-8 byte-order mark.

**Units (vendor dictionary, FACTS g4).** Volumes MWh; average price GBP per MWh (`£/MWh`); `stage`, `exclusion_stage` and `pair_id` are dimensionless identifiers. Blank cells are nulls (no `NA` or `N/A` text tokens, no thousands separators, currency or percent signs in any data cell); zeros are real zeros and stay zeros (FACTS g5). `fuel` is nullable and is kept as supplied; no technology code is invented for a blank.

**Clocks.** Vintage `ckan_last_modified`: `available_at` is the CKAN `last_modified` of the captured file (an upload stamp, not an issue time). Event time: `none`, so `timestamp_utc` is the **capture time**, not an observation time. The vendor's `date` is kept as the raw string `date_vendor`. The vendor dictionary says the column is UTC at five-minute resolution, but the support guide describes the stamp ambiguously as giving the start and end of the period, so whether it marks the slice start or end is open (`TODO: SKIP-DATE-ENDPOINT`). Observed spellings are naive or `Z`; no conflicting offset appears, so no clock correction applies.

**Held.** The silver table exists on disk but may not be used for point-in-time work; the site shows its rows with a caveat. The hold is the endpoint (`TODO: SKIP-DATE-ENDPOINT`).

### `skip_rates_summary`

- Kind: tabular · archetype: SER · refresh: daily · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| settlement_period_start | `settlement_period_start` | datetime | `%Y-%m-%dT%H:%M:%S` | no | UTC | DateTime UTC |
| stage | `stage` | int64 | — | no | — | Number |
| bm_skip_rate_offers_percent | `bm_skip_rate_offers_percent` | float64 | — | yes | — | Percentage |
| bm_total_volume_skipped_offers_MWh | `bm_total_volume_skipped_offers_mwh` | float64 | — | yes | — | MWh |
| post_system_action_skip_rate_offers_percent | `post_system_action_skip_rate_offers_percent` | float64 | — | yes | — | Percentage |
| post_system_action_total_volume_skipped_offers_MWh | `post_system_action_total_volume_skipped_offers_mwh` | float64 | — | yes | — | MWh |
| bm_skip_rate_bids_percent | `bm_skip_rate_bids_percent` | float64 | — | yes | — | Percentage |
| bm_total_volume_skipped_bids_MWh | `bm_total_volume_skipped_bids_mwh` | float64 | — | yes | — | MWh |
| post_system_action_skip_rate_bids_percent | `post_system_action_skip_rate_bids_percent` | float64 | — | yes | — | Percentage |
| post_system_action_total_volume_skipped_bids_MWh | `post_system_action_total_volume_skipped_bids_mwh` | float64 | — | yes | — | MWh |

- Entity key: `settlement_period_start`, `stage`
- Latest: `whole_capture`
- Temporal recipe: utc_instant (`settlement_period_start`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**What it is.** The **summary skip rate and skipped volume for each 30-minute period and each stage of
exclusion** in the LCP methodology (CKAN resource description). One resource, **190,368 rows**: 31,728
half-hours x stages 0 to 5 (31,728 rows per stage). It has **no stage-6 rows**; the separate stage-6
resources do not extend it. Range `2024-12-15T00:00:00Z` to `2026-10-07T23:30:00Z`. Capture
`last_modified` 2026-10-08T08:51:21.367851.

**Columns.** Four rate columns (offers and bids, each under All BM and under PSA) and four skipped-volume
columns. `bm_` columns are on the All BM basis and `post_system_action_` columns on the PSA basis. The offer
and bid sides are separate columns, not separate rows.

**Units (vendor dictionary).** The four `_percent` columns are Percentage, taken as published (do not
rescale); the four `_total_volume_skipped_` columns are MWh; `stage` is a dimensionless number.

**Clocks.** Vintage `ckan_last_modified`: `available_at` is the CKAN `last_modified` of the captured file
(an upload stamp, not an issue time). Event time: recipe `utc_instant` on `settlement_period_start`. The
vendor documents this as the settlement-period **start**, in UTC; the source spelling is naive and UTC is
attached from that explicit clock. `timestamp_utc` equals the period start. The file carries no settlement
period number, so DST days raise no 46/50-period issue; map to settlement periods through the UTC instant.

**Missingness.** In 222 rows all eight value columns are blank (null), and only those rows are affected:
37 half-hours between `2025-03-11T10:30:00Z` and `2026-07-07T11:00:00Z`, each blank for all six stages
(37 x 6 = 222). Blank is null, not zero. Zero runs are real values: counted as consecutive **rows in file
order** (six stage rows per half-hour, interleaved), the longest run of zero offer-side rate or volume is
48 rows and of bid-side 24 rows. Counted in half-hours within one stage, the longest zero run is 24
half-hours offer-side and 23 bid-side (stages 3 to 5), taking the maximum over the four offer columns and
the four bid columns. Separately, **all 48 half-hours of
2026-08-01 have no rows** between the first and last period, although the file continues after it;
`TODO: verify` the cause with the vendor. A missing day must not be read as zero.

**Eligible.** Silver is eligible: 190,368 rows from the 2026-10-08 capture, `dataset_version` `1+e1`; the
2026-10-16 capture adds a second silver file (see Cadence). Silver column names
are the lower-cased vendor names.

Silver sample (two rows, same half-hour; system columns trimmed to `timestamp_utc`, `published_at`):

```python
[
    {"settlement_period_start": "2024-12-15T00:00:00Z", "stage": 0,
     "bm_skip_rate_offers_percent": 38.22, "bm_total_volume_skipped_offers_mwh": 398.97,
     "post_system_action_skip_rate_offers_percent": 38.22,
     "post_system_action_total_volume_skipped_offers_mwh": 398.97,
     "bm_skip_rate_bids_percent": 55.26, "bm_total_volume_skipped_bids_mwh": 644.01,
     "post_system_action_skip_rate_bids_percent": 55.26,
     "post_system_action_total_volume_skipped_bids_mwh": 644.01,
     "timestamp_utc": "2024-12-15T00:00:00Z", "published_at": "2026-10-08T08:51:21.367851Z"},
    {"settlement_period_start": "2024-12-15T00:00:00Z", "stage": 1,
     "bm_skip_rate_offers_percent": 36.93, "bm_total_volume_skipped_offers_mwh": 385.51,
     "post_system_action_skip_rate_offers_percent": 36.93,
     "post_system_action_total_volume_skipped_offers_mwh": 385.51,
     "bm_skip_rate_bids_percent": 55.26, "bm_total_volume_skipped_bids_mwh": 644.01,
     "post_system_action_skip_rate_bids_percent": 55.26,
     "post_system_action_total_volume_skipped_bids_mwh": 644.01,
     "timestamp_utc": "2024-12-15T00:00:00Z", "published_at": "2026-10-08T08:51:21.367851Z"},
]
```

Silver lives at `C:/gridflow-data/silver/neso_data_portal/skip_rates_summary/year=2026/month=10/`
(partitioned by capture month; see Gotchas). System columns: `timestamp_utc`, `published_at`,
`available_at`, `event_time`, `bronze_capture_id`, `capture_written_at`, `source_run_id`, `dataset_version`.

## Cadence

- Registry refresh: daily
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Daily

The registry refreshes the package daily and the vendor's catalogue extra says "Daily". The reality is
uneven, family by family:

- **Summary and the technology summaries** update daily: the summary's capture `last_modified` is
  2026-10-08T08:51:21 UTC and its last half-hour is 2026-10-07T23:30:00Z, i.e. data to the end of the
  previous day, uploaded the next morning. The vendor says it aims to publish by 17:00 on business working
  days (CKAN resource description). `TODO: verify` the weekend and bank-holiday behaviour.
- **The 23-resource monthly families** (All BM, PSA, exclusions) are uploaded per month; their CKAN
  `last_modified` dates in the 2026-10-06 snapshot take 13 distinct values, mostly the first day of the
  following month, with the oldest months carrying the 2025-11-18 reissue date. The current month's
  resource (October 2026) is partial, and the September 2026 resources of All BM and PSA hold only one
  day (see Holds).
- **Behind-constraints and stage-6 PSA** are described by the vendor as published or uploaded monthly;
  their capture stamps (2026-09-28 and 2026-09-21) are consistent with that. The stage-6 acceptance file
  was last modified on 2026-02-04 and covers calendar 2025 only; `TODO: verify` whether NESO will extend it.
- **The DSF families** carry `last_modified` 2026-10-07 in the capture (2026-10-06 in the snapshot), so
  they also update frequently.

Every resource was captured on 2026-10-08. Seven were captured again on 2026-10-16 (bronze
`2026/10/16/`, each also transformed to one more silver file): the October 2026 files of exclusion reasons
(850,060 rows), All BM (3,922,118) and PSA (3,169,439), each to 2026-10-15T23:55:00; the PSA DSF unit file
(435,526 rows, still 7,830 excess repeated rows); the stage-5 DSF technology file (7,223 rows, still 192
excess); the stage-5 PSA technology file (133,598 rows); and the summary (192,672 rows, to
2026-10-15T23:30:00Z). Compared pair by pair, the summary and the stage-5 PSA technology file only
append: every earlier key is kept with identical values (2,304 and 1,459 new rows). The other resources,
including the September 2026 and March 2026 files under Holds, have one capture. The reissue history in
Gotchas shows the vendor does replace files, so only further pairs can show whether an uploaded file is
revised in place. The row counts in the table at the top are the 2026-10-12 activation.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence). gridflow
outputs derived from this package carry the attribution line above. The vendor's methodology documents
(NESO skip-rate section and dashboard) are the authority on definitions; the NESO website page
[Skip Rates](https://www.neso.energy/industry-information/balancing-services/skip-rates) is cited by the
CKAN notes.

## Holds

- `skip_rates_behind_constraints_bmu`: held: TODO: CONSTRAINT-RATE-DENOMINATOR — the dictionary says percentage of in-merit volume skipped, the methodology presentation uses accepted volume; which denominator is the published rate? Also no month-boundary recipe for a UTC month. (unit v0.22-K-BAL-2b)
- `skip_rates_behind_constraints_cons`: held: TODO: CONSTRAINT-RATE-DENOMINATOR — the dictionary says percentage of in-merit volume skipped, the methodology presentation uses accepted volume; which denominator is the published rate? Also no month-boundary recipe for a UTC month. (unit v0.22-K-BAL-2b)
- `skip_rates_exclusion_reasons`: held: TODO: SKIP-DATE-ENDPOINT — does the five-minute `date` stamp mark the slice start or end? (unit v0.22-K-BAL-2b)
- `skip_rates_in_merit_all_bm`: held: TODO: SKIP-DATE-ENDPOINT — does the five-minute `date` stamp mark the slice start or end? TODO: ALL-BM-SEPTEMBER-COVERAGE — resource ca3587a2-ae0d-47db-b0a1-4d681af8bced holds 30 September 2026 only (387,189 rows). (unit v0.22-K-BAL-2b)
- `skip_rates_in_merit_psa`: held: TODO: SKIP-DATE-ENDPOINT — does the five-minute `date` stamp mark the slice start or end? TODO: PSA-MARCH/SEPTEMBER-COVERAGE — resource a04c4c6e-0526-42b4-99d0-eb114beba8a2 stops at exactly 3,200,000 rows on 2026-03-24T15:45:00, and resource 38421f3d-8949-4dcf-81cf-0295a8688086 holds 30 September 2026 only (273,888 rows). (unit v0.22-K-BAL-2b)
- `skip_rates_stage6_acceptance`: held: TODO: SKIP-DATE-ENDPOINT — does the five-minute `date` stamp mark the slice start or end? (unit v0.22-K-BAL-2b)
- `skip_rates_stage6_psa`: held: TODO: SKIP-DATE-ENDPOINT — does the five-minute `date` stamp mark the slice start or end? (unit v0.22-K-BAL-2b)

Seven silver outputs exist on disk and are **held**. They may not be used for point-in-time
models until the unit that settles the semantics questions (E-SEM) answers the questions
below. The registry records each hold against the unit that created it (`v0.22-K-BAL-2b`); the
eligibility report agrees with the registry.

**The hold questions, in plain terms.**

1. **Five-minute date endpoint (`TODO: SKIP-DATE-ENDPOINT`), five families.** The exclusion-reasons,
   All BM, PSA, stage-6 acceptance and stage-6 PSA files have one `date` column. The vendor dictionary says
   UTC at five-minute resolution, but the support guide describes the timestamp as giving both the start and
   the end of the period. Which end the stamp marks is unknown. The raw string is kept in `date_vendor` and the
   event-time recipe is `none` until the vendor says which. Choosing the wrong end would shift every row by
   five minutes. Unit: E-SEM.
2. **Constraint rate denominator (`TODO: CONSTRAINT-RATE-DENOMINATOR`), two families.** The behind-constraints
   dictionary says the skip rate is a percentage of in-merit volume skipped, whereas NESO's presentation
   formula uses accepted-volume terminology. Which denominator is the published rate? The raw value and the
   Percentage unit are preserved; no derived rate is published. There is also no month-boundary recipe for a
   UTC month, because the current month recipe anchors on London midnight. Unit: E-SEM.
3. **Coverage (`TODO: ALL-BM-SEPTEMBER-COVERAGE`, `TODO: PSA-MARCH/SEPTEMBER-COVERAGE`).** The All BM
   September 2026 resource holds 30 September only (387,189 rows); the PSA September 2026 resource holds 30
   September only (273,888 rows); the PSA March 2026 resource stops at exactly 3,200,000 rows on
   2026-03-24T15:45:00. A vendor explanation or corrected bodies are needed, and no completeness claim may
   be made for those months. Unit: E-SEM.

**Not held but without a record.** `skip_rates_in_merit_psa_dsf_unit` and `skip_rates_stage5_dsf_technology`
carry repeated full rows and have no record or silver (RULINGS 538). They are ingest-only: bronze exists.

**Rows on the site (ruling 66, 2026-10-24).** The front-end page shows rows for all nine silver tables:
the seven held ones carry a caveat naming their question, the summary and the stage-5 PSA technology
summary carry none. The two DSF tables have no silver table, so the page shows no rows for them. The
holds still bar point-in-time and model use.

**Activation receipt.** `gridflow transform --start/--end 2026-10-08` (RULINGS 695); no prior skip silver
existed, so no snapshot was needed. The reconcile `--all --cutoff 2026-10-12` ended with exit 0, 132 families,
0 gaps, 45 adjudicated and 0 stale (RULINGS 696), with a peak of 8,692.0 MiB, up from about 2 GiB, because of
the 175 million new rows.
