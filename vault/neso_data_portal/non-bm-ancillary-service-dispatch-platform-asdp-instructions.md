---
source: "neso_data_portal"
package: "non-bm-ancillary-service-dispatch-platform-asdp-instructions"
dataset_key: "asdp_instructions"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-13
layer_coverage: "bronze, silver"
eligibility: "eligible"
page:
  title: ASDP dispatch instructions
  summary: >-
    Dispatch and cease instructions NESO sent to Non-BM Fast Reserve, STOR and RDP units through
    its dispatch platform, ASDP, in monthly files.
  facts:
    vendor: "NESO Data Portal: 70 datastore tables, one per month"
    cadence: "Not active (NESO's label); NESO is moving non-BM services to its Open Balancing Platform"
    grain: "One row per instruction entry, numbered by NESO's `EntryID`"
    history: "Monthly files from June 2020 to April 2026, with none for September 2020"
  landscape: market
  what_it_is: >-
    NESO's Ancillary Service Dispatch Platform (ASDP) instructed reserve units outside the
    Balancing Mechanism: Non-BM Fast Reserve, STOR and RDP curtailments. NESO publishes
    instructions once providers confirm them. Most rows give start and cease times, MW, an
    indicative price in £/MWh and, from November 2021, provider and asset. Times are text: ending
    in `Z` in 2020, no zone marker from 2021.
  how_used:
    - How often NESO called Non-BM Fast Reserve and STOR, by day and hour
    - Instructed MW and indicative price per asset and provider
    - Lead time from each dispatch message to the instructed start
  chart:
    type: stacked-area
    silver: neso_data_portal/asdp_instructions
    time: instruction_start_date_time
    time_text: {format: "%Y-%m-%dT%H:%M:%S"}
    filter:
      - {column: dispatch_date_time_stamp, op: ge, value: "2021-01-01"}
    group: service_type
    group_map: {"Non-BM Fast Reserve": fast, "Non-BM STOR": stor, RDP_NEGATIVE: rdp}
    series_order: [fast, stor, rdp]
    aggregation: count
    time_bucket: 1d
    window: {start: "2022-03-01", end: "2022-03-31"}
    unit: count
  chart_view:
    title: Instructions per day by service, March 2022
    caption: >-
      Silver `neso_data_portal/asdp_instructions`, instructions per start date as written, March 2022:
      picked as the month with most STOR instructions. That month, Fast Reserve has rows daily and
      STOR comes in bursts. Rows without a start are not counted.
    alt: >-
      Stacked area chart from neso_data_portal/asdp_instructions of instructions per start date as
      written, 1 to 31 March 2022: Non-BM Fast Reserve at the bottom, STOR on top. Fast Reserve runs
      every day, 5 to 57 a day, highest on the 3rd. STOR appears on nine days, the 1st and between
      the 8th and 17th, up to 108 on the 11th; the total is highest on the 8th, at 133.
    x_label: start date as written, March 2022
    key:
      - {series: stor, label: Non-BM STOR, codes: Non-BM STOR, paint: hatch-cross, note: "Nine days this month, up to 108 on the 11th."}
      - {series: fast, label: Non-BM Fast Reserve, codes: Non-BM Fast Reserve, paint: hatch-lines}
  raw_feed:
    note: >-
      From NESO's CKAN portal: one `package_show`, then each month's datastore dump (three of 70
      shown), kept only if its body changed. gridflow re-checks it at most weekly.
    requests:
      - "GET https://api.neso.energy/api/3/action/package_show?id=non-bm-ancillary-service-dispatch-platform-asdp-instructions"
      - "GET https://api.neso.energy/datastore/dump/6f037ebe-110d-4099-ab82-0ac3185e3f18"
      - "GET https://api.neso.energy/datastore/dump/90ba1625-d99b-4ec6-8356-ad69af4e6b20"
      - "GET https://api.neso.energy/datastore/dump/099bd868-d0af-4157-85c6-4508ddbd8a64"
    commands:
      - {run: gridflow ingest neso_data_portal asdp_instructions --last 24h, comment: "all 70 monthly dumps to bronze"}
      - {run: gridflow transform neso_data_portal asdp_instructions --last 24h, comment: "the capture's date to silver"}
  record:
    select:
      filter:
        - {column: resource_id, op: eq, value: "ba09543b-79e0-46c7-a229-089d83df6304"}
        - {column: entry_id, op: in, value: ["73427", "73429", "73430", "73433", "73436", "73437", "73441", "73447"]}
      order_by: [entry_id]
      columns: [entry_id, instruction_start_date_time, dispatch_date_time_stamp, mw, indicative_price,
                asset_id, party_id, service_type, instruction_cease_date_time, cease_date_time_stamp,
                tendered, resource_id]
    key: [resource_id, entry_id]
    caption: "Eight instructions, 29 March 2026; five start between 01:00 and 01:59, an hour UK clocks skipped."
    fields:
      entry_id: "NESO's sequential entry number, kept as text (its dictionary says integer)"
      instruction_start_date_time: "Ramp-up start (RDP: dispatch sent); no zone marker, and not UK local time here"
      dispatch_date_time_stamp: "When NESO sent the dispatch; its dictionary adds publish time to the portal"
      mw: "MW dispatched, as NESO states it; NESO states no sign"
      indicative_price: "Price as the instruction starts to ramp up, £/MWh (NESO); RDP: utilisation price"
      asset_id: "The Non-BM unit instructed, as NESO names it; files to October 2021 lack it"
      party_id: "The provider as NESO writes it, spaces kept; files to October 2021 lack it"
      service_type: "`Non-BM Fast Reserve`, `Non-BM STOR` or `RDP_NEGATIVE` (an RDP curtailment)"
      instruction_cease_date_time: "Cease ramp-down end (NESO; RDP: when the cease was sent), as written"
      cease_date_time_stamp: "When NESO sent the cease; its dictionary adds publish time to the portal"
      tendered: "`Tendered` or `Non-tendered`, case as NESO writes it; files to October 2021 lack it"
      resource_id: "The monthly file the row came from; with `entry_id`, the key"
      timestamp_utc: "gridflow's capture time, UTC; not the instruction time"
      published_at: "Null: when NESO first published each instruction is not recorded"
      bronze_capture_id: Path of the bronze capture the row was read from
      capture_written_at: When gridflow wrote that capture to bronze, UTC
  notebook:
    lead: >-
      `data.sql` reads the `_latest` view; `query()` would filter on `timestamp_utc`, the capture
      time. Years and hours are cut from the text as written. STOR falls from 776 in 2022 to 26,
      6, 1 and 1.
    cells:
      - |
        data.sql("""
            SELECT substr(instruction_start_date_time, 1, 4) AS year,
                count_if(service_type = 'Non-BM Fast Reserve') AS fast_res,
                count_if(service_type = 'Non-BM STOR') AS stor,
                count_if(service_type = 'RDP_NEGATIVE') AS rdp,
                round(avg(indicative_price), 2) AS mean_price_gbp_mwh
            FROM silver_neso_data_portal_asdp_instructions_latest
            WHERE instruction_start_date_time IS NOT NULL
            GROUP BY ALL ORDER BY year""")
      - |
        hours = data.sql("""
            SELECT substr(instruction_start_date_time, 12, 2)::INT AS hour,
                count(*) AS instructions
            FROM silver_neso_data_portal_asdp_instructions_latest
            WHERE service_type = 'Non-BM Fast Reserve'
              AND instruction_start_date_time LIKE '2025-%'
            GROUP BY ALL ORDER BY hour""")
        hours.head()
      - |
        hours.plot.bar(x="hour", y="instructions", legend=False,
                       color="#155A6E", figsize=(8, 3.5),
                       xlabel="hour of the start time as written, 2025",
                       ylabel="Fast Reserve instructions");
    needs: a capture of the 70 monthly files
    plot_alt: >-
      Bar chart of 2025's Non-BM Fast Reserve instructions by hour of the start time as written, 0 to
      23. The fewest start in hour 2 (372) and the most in hour 6 (1,318); a second, broader high runs
      from hour 15 to 18, at 943 to 1,024 each.
  related:
    - {dataset: neso_data_portal/non-bm-ancillary-service-dispatch-platform-asdp-window-prices, note: "Window prices providers sent through ASDP; `EntryID` points here"}
    - {dataset: neso_data_portal/obp-non-bm-reserve-instructions, note: "OBP, the platform NESO is moving non-BM services to; never join ids"}
    - {dataset: neso_data_portal/short-term-operating-reserve-stor-day-ahead-auction-results, note: The day-ahead STOR auctions behind the STOR service}
---

# Non-BM ancillary service dispatch platform (ASDP) instructions

NESO's log of dispatch and cease instructions sent to **non-BM** reserve providers through its Ancillary Service
Dispatch Platform (ASDP). The vendor text says NESO publishes the instructions "once instructions have been
confirmed by Service Providers", and that a new monthly file is only created when a new set of instructions is
dispatched for **Non-BM Fast Reserve (FR)**, **Short Term Operating Reserve (STOR)** and **Regional Development
Programme (RDP) MW Dispatch** (CKAN package `notes`,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json; NESO
[ASDP instructions](https://www.neso.energy/data-portal/non-bm-ancillary-service-dispatch-platform-asdp-instructions)).
Each row is **one instruction entry**: the instruction start and cease times, the MW dispatched, an indicative
price, and the times NESO sent the dispatch and the cease messages. The later bodies add the provider name
(`party_id`), the asset (`asset_id`) and a `tendered` flag. Use it to see what NESO asked non-BM units to do, how
often, in what size and at what indicative price. It is an **event log, not a forecast**.

**NESO is moving non-BM services from ASDP to OBP, and the two overlap in time.** The vendor states that the non-BM services "that
used to be published on this page have now migrated to the OBP system" and links the successor datasets
(@./obp-non-bm-reserve-instructions.md, @./obp-non-bm-physical-notifications.md,
@./obp-reserve-availability-utilisation-price.md). The registry refresh is `frozen` and the vendor's own
"Update Frequency" label is `Not Active`. The captured ASDP rows have start labels from 2020-06-25 to 2026-04-17,
and the OBP instruction points captured in AS-3 span 2025-10-10 to 2026-10-02, so the **reporting periods overlap
from 2025-10-10**. That overlap does **not** mean the same instruction is published twice: the grain (an ASDP
entry versus an OBP instruction point) and the identifier systems differ. **Never union ASDP with OBP and never
match `entry_id` to an OBP instruction identifier**; gridflow defines no silver relation between them (K-AS-5-FACTS
ASDP section; K-AS-5b-SPEC seat ruling 3).

**What a model gets from it, and what it does not.**

- **Times are raw strings, and their clock is undocumented.** All four timestamp columns are kept exactly as
  published (`TODO: verify` the export clock, below), so the table has **no event time in the usual sense**: the
  silver `timestamp_utc` is the gridflow capture time, not the instruction time. See Two clocks.
- **MW is as published, with no sign convention.** `mw` is the vendor's "MWs dispatched" and is positive in every
  row (3 to 100 MW), including the `RDP_NEGATIVE` service rows. gridflow neither flips nor infers a sign.
- **No history before 2026-10-08 in the vintage clock.** Every row's `available_at` is the 2026-10-08 capture.

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| Non BM Dispatch Cease Instructions_Apr_2021 | CSV | dump | `02b3937a-4ba1-46a5-9082-bf7b4fd995cf` |
| Non BM Dispatch Cease Instructions_Apr_2022 | CSV | dump | `bf629b2f-b93b-4d4a-8dd7-c50156c3a8ab` |
| Non BM Dispatch Cease Instructions_Apr_2023 | CSV | dump | `1f8eb6f2-6c3f-41ae-bc47-9d546a564988` |
| Non BM Dispatch Cease Instructions_Apr_2024 | CSV | dump | `cbe93aea-a869-40a9-8115-ec32c690300c` |
| Non BM Dispatch Cease Instructions_Apr_2025 | CSV | dump | `302141a1-6c74-4c2f-a1dc-298e485d59d9` |
| Non BM Dispatch Cease Instructions_Apr_2026 | CSV | dump | `099bd868-d0af-4157-85c6-4508ddbd8a64` |
| Non BM Dispatch Cease Instructions_Aug_2020 | CSV | dump | `a16abb3c-36bd-448f-9263-b25d90ca08a0` |
| Non BM Dispatch Cease Instructions_Aug_2021 | CSV | dump | `b87d78c8-a961-4b6b-8f64-7e0ccb4156f2` |
| Non BM Dispatch Cease Instructions_Aug_2022 | CSV | dump | `1b02bcab-e050-4725-bfc1-b5d034aaef37` |
| Non BM Dispatch Cease Instructions_Aug_2023 | CSV | dump | `edd4f419-14d1-4f48-a9e6-1e0a87b99561` |
| Non BM Dispatch Cease Instructions_Aug_2024 | CSV | dump | `a5ce745a-8555-4c50-94fa-d7db3bd2b8af` |
| Non BM Dispatch Cease Instructions_Aug_2025 | CSV | dump | `0a4e2125-5e97-4c28-b707-056c7f295419` |
| Non BM Dispatch Cease Instructions_Dec_2020 | CSV | dump | `0acd8a9f-025b-4e4f-b69c-fda1bf9007ae` |
| Non BM Dispatch Cease Instructions_Dec_2021 | CSV | dump | `b2df172c-dbfe-4c96-9e33-7e2c0e64a0c4` |
| Non BM Dispatch Cease Instructions_Dec_2022 | CSV | dump | `e647c7e0-4ecf-4fcc-b177-5e6e2473e8ac` |
| Non BM Dispatch Cease Instructions_Dec_2023 | CSV | dump | `3050db3d-0930-4462-8275-47413788fc7f` |
| Non BM Dispatch Cease Instructions_Dec_2024 | CSV | dump | `57d05910-1b81-4eaa-b87d-46e6ad7a483a` |
| Non BM Dispatch Cease Instructions_Dec_2025 | CSV | dump | `bfbce47e-7ef8-4777-91cb-9b547d222829` |
| Non BM Dispatch Cease Instructions_Feb_2021 | CSV | dump | `98a05e0c-eb08-427c-a440-b084d30af78e` |
| Non BM Dispatch Cease Instructions_Feb_2022 | CSV | dump | `fb7bc149-2a9b-4b80-86e7-e2c5c1e37271` |
| Non BM Dispatch Cease Instructions_Feb_2023 | CSV | dump | `b3cd38dd-9d42-4a15-975a-f047b1452830` |
| Non BM Dispatch Cease Instructions_Feb_2024 | CSV | dump | `f393b6dd-a53e-479b-9487-ef6be9b54c7c` |
| Non BM Dispatch Cease Instructions_Feb_2025 | CSV | dump | `fa6aa4e7-9c1a-439b-8d56-bfb3dfff9568` |
| Non BM Dispatch Cease Instructions_Feb_2026 | CSV | dump | `2043a615-ad1c-44ed-9a36-11fbbcef5128` |
| Non BM Dispatch Cease Instructions_Jan_2021 | CSV | dump | `75acd396-3895-4538-998b-ed4c45574c40` |
| Non BM Dispatch Cease Instructions_Jan_2022 | CSV | dump | `3c9e6c70-5cff-42e6-8c9e-ca7f51111ba8` |
| Non BM Dispatch Cease Instructions_Jan_2023 | CSV | dump | `aa138e72-3e25-4787-8369-40f2b9abb980` |
| Non BM Dispatch Cease Instructions_Jan_2024 | CSV | dump | `f9de917d-9fc1-4ae6-9bfd-38f2c4e03ad7` |
| Non BM Dispatch Cease Instructions_Jan_2025 | CSV | dump | `6661b52e-89b7-4011-8900-e2ded58b215f` |
| Non BM Dispatch Cease Instructions_Jan_2026 | CSV | dump | `4c1e607e-d006-4d1a-a753-2c94d23b10c5` |
| Non BM Dispatch Cease Instructions_Jul_2020 | CSV | dump | `5d741b13-85c4-44bd-82ba-50dca68ff4f1` |
| Non BM Dispatch Cease Instructions_Jul_2021 | CSV | dump | `2522c3cd-9f5a-402a-8a0c-9410ad187bb8` |
| Non BM Dispatch Cease Instructions_Jul_2022 | CSV | dump | `d6aa3dd3-42d7-426d-905b-0f24afd26d60` |
| Non BM Dispatch Cease Instructions_Jul_2023 | CSV | dump | `b6de945d-deed-4181-a97c-ba795d41a550` |
| Non BM Dispatch Cease Instructions_Jul_2024 | CSV | dump | `8fbe008a-cbb7-4244-accd-52eb48484589` |
| Non BM Dispatch Cease Instructions_Jul_2025 | CSV | dump | `c2e53d15-8041-4ec3-9d55-69e15895ab49` |
| Non BM Dispatch Cease Instructions_Jun_2020 | CSV | dump | `6f037ebe-110d-4099-ab82-0ac3185e3f18` |
| Non BM Dispatch Cease Instructions_Jun_2021 | CSV | dump | `e843280c-7c36-44e5-97b8-b6403d338bbc` |
| Non BM Dispatch Cease Instructions_Jun_2022 | CSV | dump | `00936338-b75c-4ada-b812-6d84e03ae650` |
| Non BM Dispatch Cease Instructions_Jun_2023 | CSV | dump | `022b285b-99b5-4daf-984b-67af79d034a9` |
| Non BM Dispatch Cease Instructions_Jun_2024 | CSV | dump | `3d943305-737e-4da3-af80-d02da7ab89e7` |
| Non BM Dispatch Cease Instructions_Jun_2025 | CSV | dump | `51f4ada0-407e-49f4-bca8-ffe67c5beb9a` |
| Non BM Dispatch Cease Instructions_Mar_2021 | CSV | dump | `d1fce430-c387-413d-99c7-e3f0fc6f5458` |
| Non BM Dispatch Cease Instructions_Mar_2022 | CSV | dump | `6835dd89-6845-48ec-a8a2-041c6924dc02` |
| Non BM Dispatch Cease Instructions_Mar_2023 | CSV | dump | `f42d3568-e5d5-49ff-85fa-5307ef5a1a9e` |
| Non BM Dispatch Cease Instructions_Mar_2024 | CSV | dump | `634f9b03-e2e2-4d5a-a1b3-1eeae249dad3` |
| Non BM Dispatch Cease Instructions_Mar_2025 | CSV | dump | `ed60b6bf-b771-4eb5-8633-46d816f05703` |
| Non BM Dispatch Cease Instructions_Mar_2026 | CSV | dump | `ba09543b-79e0-46c7-a229-089d83df6304` |
| Non BM Dispatch Cease Instructions_May_2021 | CSV | dump | `47e35617-1df4-46d4-9900-874f034792b1` |
| Non BM Dispatch Cease Instructions_May_2022 | CSV | dump | `b97f5a01-96bb-46ec-80c5-62d5ba010fe7` |
| Non BM Dispatch Cease Instructions_May_2023 | CSV | dump | `7d42751b-69d7-4886-b323-348bc280ec70` |
| Non BM Dispatch Cease Instructions_May_2024 | CSV | dump | `c6ec4a0d-bf02-41fd-b31d-d341d183a281` |
| Non BM Dispatch Cease Instructions_May_2025 | CSV | dump | `fa096fbf-9e57-4e9e-bbc0-8371e8541bf9` |
| Non BM Dispatch Cease Instructions_Nov_2020 | CSV | dump | `568b4255-b66f-4aa8-a704-36a5e65b5563` |
| Non BM Dispatch Cease Instructions_Nov_2021 | CSV | dump | `90ba1625-d99b-4ec6-8356-ad69af4e6b20` |
| Non BM Dispatch Cease Instructions_Nov_2022 | CSV | dump | `8229a89a-77fe-44db-a0e6-a02aff2ad048` |
| Non BM Dispatch Cease Instructions_Nov_2023 | CSV | dump | `9d03620d-e526-4c2e-8917-0d990efe71c9` |
| Non BM Dispatch Cease Instructions_Nov_2024 | CSV | dump | `43a3ba39-6a69-4951-8f31-b36f24a752eb` |
| Non BM Dispatch Cease Instructions_Nov_2025 | CSV | dump | `cc57a85a-8f7e-4f45-9957-ae086d48b1c3` |
| Non BM Dispatch Cease Instructions_Oct_2020 | CSV | dump | `339bbc15-2e83-4928-a07f-e09b6d60edfc` |
| Non BM Dispatch Cease Instructions_Oct_2021 | CSV | dump | `4766f3e3-18ff-4703-8528-f4ea4606eeb1` |
| Non BM Dispatch Cease Instructions_Oct_2022 | CSV | dump | `33858909-ad26-4a3c-b1d1-af5b8df7cac2` |
| Non BM Dispatch Cease Instructions_Oct_2023 | CSV | dump | `2057abe9-465d-4ca0-84d1-ec67e9cdb7c8` |
| Non BM Dispatch Cease Instructions_Oct_2024 | CSV | dump | `6d3919d5-21be-4427-8757-e43fda9db4b6` |
| Non BM Dispatch Cease Instructions_Oct_2025 | CSV | dump | `35a4fac5-ee33-475a-adab-25ad14da60b0` |
| Non BM Dispatch Cease Instructions_Sep_2021 | CSV | dump | `15d4c539-f523-4406-957a-334ad15859ec` |
| Non BM Dispatch Cease Instructions_Sep_2022 | CSV | dump | `c3d32954-7b6b-472f-9d22-a96580a97fc2` |
| Non BM Dispatch Cease Instructions_Sep_2023 | CSV | dump | `f352265b-01c4-4f45-b0e4-bef889b74d23` |
| Non BM Dispatch Cease Instructions_Sep_2024 | CSV | dump | `9cec00cf-8ade-4a81-b2ef-f3ecf51e7c97` |
| Non BM Dispatch Cease Instructions_Sep_2025 | CSV | dump | `7b3a9ead-c041-4a62-97b1-6cb0587baf58` |

All 70 resources are dispositioned `SILVER` and are **CSV datastore dumps** (CKAN `url_type` `datastore`), one per
calendar month from June 2020 to April 2026. Each downloads from `https://api.neso.energy/datastore/dump/<Id>` (the
`url` the vendor publishes in the catalogue snapshot of 2026-10-06,
@.planning/research/neso-snapshots/20261006T195819Z/catalog-snapshot.json); gridflow holds **exactly one bronze
capture per resource** (70 CSV bodies, captured 2026-10-08 08:16 to 08:50 UTC, each with a hash-verified sidecar).
**September 2020 has no resource** (the series runs Jun, Jul, Aug, Oct, Nov, Dec 2020 and then every month from
January 2021); `TODO: verify` whether that month had no instructions or was never published (the vendor says a
monthly file exists only when instructions were dispatched, which would fit but is not stated for that month).

**Documentation (DOC) files: none are registry resources.** The catalogue lists no DOC resource for this package.
The resource descriptions point to a reference document for the `PartyID` and `AssetID` fields, in several
generations of link, and none is downloaded or parsed by gridflow:

- [Party ID and Asset ID reference (current NESO document)](https://www.neso.energy/document/294096/download) -
  linked from 19 resource descriptions.
- The same document at the older National Grid ESO site address (`nationalgrideso.com/document/294096/download`) -
  linked from 10 resource descriptions.
- Two older workbook links on the retired `datanationalgrideso.files.wordpress.com` host
  (`reference_document_for_party_id_and_asset_id-1.xlsx`, 8 resource descriptions, and
  `reference_document_for_party_id_and_asset_id-1-1-1.xlsx`, 17 resource descriptions); 16 further resource
  descriptions carry no link. `TODO: verify` whether the retired links still resolve; the contents of the
  party/asset reference were not read for this page, so the meaning of the party and asset codes is the vendor's
  field text only.

## Families

### `asdp_instructions`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

**Activation.** 74,137 silver rows from the 70 resources (activation 2026-10-08, window `2026-10-08..2026-10-08`, no
prior silver, 0 recorded failures; @.planning/v0.22-RESULTS.md section AS-5b; RULINGS 792). The reconcile of all
families afterwards exited 0 with 0 gaps. Nothing is held for this family and no resource is held.

**Header epochs.** The header is not the same in every body.

- **Epoch 1 (8 columns):** the first **16 resources** (June 2020 to October 2021), **12,441 rows**.
- **Epoch 2 (11 columns):** epoch 1 plus `PartyID`, `AssetID`, `Tendered`; the remaining **54 resources**
  (November 2021 to April 2026), **61,696 rows**. In epoch 1 rows the three extra silver columns are null; another
  **95** epoch 2 rows (all `Non-BM Fast Reserve`) are also blank in all three.

The header change is independent of the timestamp-spelling change below. A body whose header matches neither epoch
fails loudly. The silver column names are harmonised across both epochs (one dtype per name).

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| EntryID | `entry_id` | string | — | no | — | — |
| ServiceType | `service_type` | string | — | yes | — | — |
| InstructionStartDateTime | `instruction_start_date_time` | string | — | yes | — | — |
| MW | `mw` | float64 | — | yes | — | MW |
| IndicativePrice | `indicative_price` | float64 | — | yes | — | £/MWh |
| InstructionCeaseDateTime | `instruction_cease_date_time` | string | — | yes | — | — |
| DispatchDateTimeStamp | `dispatch_date_time_stamp` | string | — | yes | — | — |
| CeaseDateTimeStamp | `cease_date_time_stamp` | string | — | yes | — | — |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| EntryID | `entry_id` | string | — | no | — | — |
| ServiceType | `service_type` | string | — | yes | — | — |
| InstructionStartDateTime | `instruction_start_date_time` | string | — | yes | — | — |
| MW | `mw` | float64 | — | yes | — | MW |
| IndicativePrice | `indicative_price` | float64 | — | yes | — | £/MWh |
| InstructionCeaseDateTime | `instruction_cease_date_time` | string | — | yes | — | — |
| DispatchDateTimeStamp | `dispatch_date_time_stamp` | string | — | yes | — | — |
| CeaseDateTimeStamp | `cease_date_time_stamp` | string | — | yes | — | — |
| PartyID | `party_id` | string | — | yes | — | — |
| AssetID | `asset_id` | string | — | yes | — | — |
| Tendered | `tendered` | string | — | yes | — | — |

- Entity key: `resource_id`, `entry_id`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | null |
| `available_at` | gridflow capture time (sidecar `written_at`), labelled so |

**Silver also carries** the engine-stamped columns `resource_id` (the key partition), `timestamp_utc`, `published_at`
(null on every row), `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and
`dataset_version` (`1+e1` on every row, verified for all 74,137).

**Two clocks.**

- **Vintage (when it was known): `available_at` = gridflow capture time**, the `written_at` of the bronze sidecar,
  and not the CKAN `last_modified`. These are datastore dumps, not uploads; the record model forbids the CKAN
  `last_modified` vintage on a datastore family (check V-8), so the registry uses `capture_fallback`. The vendor's
  CKAN `last_modified` is null for 42 of the 70 resources in the catalogue snapshot, and for the other 28 it is not
  used. Every row carries an `available_at` between 2026-10-08 08:16:26 and 08:50:58 UTC. A point-in-time query
  (`WHERE available_at <= :as_of`) therefore sees **no ASDP history before 2026-10-08**, and the vendor's own
  publication time of an instruction is not recorded in the table (`published_at` is null).
- **Event time: none.** The temporal recipe is `none`, so `timestamp_utc` **is the capture time**, not an
  instruction time: `event_time`, `timestamp_utc` and `available_at` are equal on all 74,137 rows (verified). Do not
  use any of them as the time of an instruction. The instruction's own times are the four raw string columns
  (`instruction_start_date_time`, `instruction_cease_date_time`, `dispatch_date_time_stamp`,
  `cease_date_time_stamp`), which are **not typed and not converted to UTC**.

**The raw time columns, and why they stay raw.** The vendor dictionary types the four columns as DateTime and shows
the example `2019-01-30 07:26:16Z`. The captured spellings are two:

| Spelling | Rows (instruction start column) | Resources | Start-label range |
|---|---:|---|---|
| `YYYY-MM-DD HH:MM:SSZ` (space, literal `Z`) | 2,724 | the six June to December 2020 resources | 2020-06-25 01:49:00Z to 2020-12-31 20:13:00Z |
| `YYYY-MM-DDTHH:MM:SS` (ISO `T`, **no zone marker**) | 71,304 | the other 64 resources | 2021-01-01T03:04:00 to 2026-04-17T21:49:00 |
| blank | 109 | 26 resources | - |

The same two spellings occur in the other three time columns: the same 2,724 rows are space-and-`Z`, and the naive
counts are 71,304 for the dispatch stamp and 71,210 for the cease time and cease stamp (blank counts 109, 203 and
203; see Sentinels). The `Z` in the early rows does not authorise assigning UTC to the later naive cells.
ASDP protocol guidance uses UTC for message timestamps ([STOR ASDP guidance](https://www.neso.energy/document/186511/download)),
but no reviewed portal dictionary maps that specification onto every exported column and spelling in both epochs
(`TODO: ASDP-EXPORT-CLOCK`). One measured check narrows it for three files. On 29 March 2026, when UK clocks skip
01:00 to 01:59, the March 2026 body has 17 starts and 17 dispatch stamps in that hour, and in `EntryID` order (73427
to 73455) starts and stamps run on unbroken from 00:43 through 01:03, 01:08 and 01:33 to 02:03, so that body is not
written in UK local time (UTC or fixed GMT fit). Of the other five spring changes in the naive files, only the cease
columns have rows in the skipped hour: 28 March 2021 (entry 5574, cease 01:12:48, cease stamp 01:11:13) and 30 March
2025 (entries 54370 to 54375, ceases 01:20:00 to 01:28:36), so those two bodies' cease columns are not UK local time
either. 27 March 2022, 26 March 2023 and 31 March 2024 have no row in that hour in any column, so they test nothing
(front-end page writer, 2026-10-18, local silver; corrected after review the same day). No two resources'
start-label ranges overlap in the observed labels.

**Units (vendor dictionary only; nothing converted).** From NESO's saved field info
(@.planning/research/neso-snapshots/field-info/20261008T114228Z/asdp_instructions.json) as cited in K-AS-5-FACTS:

| Silver column | Vendor unit | Vendor meaning |
|---|---|---|
| `entry_id` | none | "Sequential Number" (an identifier; never cast to a number) |
| `service_type` | none | `Non-BM STOR`, `Non-BM Fast Reserve`; every RDP MW Dispatch instruction has `RDP_NEGATIVE` |
| `instruction_start_date_time` | none | when the dispatch starts to ramp up; for RDP, when the dispatch was sent to the DER unit via the DNO for curtailment down to 0 MW |
| `mw` | MW | "MWs dispatched" |
| `indicative_price` | £/MWh | the price of the instruction at the time it starts to ramp up; for RDP, the DER unit's latest Utilisation Price for that day |
| `instruction_cease_date_time` | none | when the cease instruction's ramp down ends; for RDP, when the cease was sent to restore generation |
| `dispatch_date_time_stamp` | none | "Timestamp Dispatch is sent (publish time to NESO data portal)" |
| `cease_date_time_stamp` | none | "Timestamp Cease is sent (publish time to NESO data portal)" |
| `party_id` | none | the service provider name for the instruction |
| `asset_id` | none | the Non-BMU ID; for RDP, the NESO-assigned unit ID of the DER |
| `tendered` | none | whether the service is Tendered or Non-tendered; for RDP, "always Non-Tendered" |

No unit is inferred from a column name. The registry record's columns carry no unit field, so these units are
documented here and in FACTS only.

**Sentinels and typing (K-AS-5-FACTS g5, g6).** No `NA`/`N/A` token, thousands separator or embedded quote, comma or
newline was found in a data cell; the production reader agreed with a strict second parse on every row and cell, and
every body is valid UTF-8. **No token is mapped to null, no trim is applied and no bound is applied.**

- **Blanks stay null.** `instruction_start_date_time`, `mw`, `indicative_price` and `dispatch_date_time_stamp` are
  blank in **109** rows each (the same 109 rows, in 26 resources, every one of which still has a cease time);
  `instruction_cease_date_time` and `cease_date_time_stamp` are blank in **203** rows each. `service_type` is never
  blank.
- **Zero stays zero.** `indicative_price` is exactly 0 in **4** rows (never two in a row within a resource). The
  captured price range is 0 to 7000 £/MWh; `TODO: verify` whether the largest values are real prices. No threshold
  or cap is applied.
- **Case and padding are preserved as published.** `tendered` is `Non-tendered` (61,370 rows), `Non-Tendered` (1),
  `Tendered` (230) or null (12,536). The case variants are the vendor's, not folded; provider-name padding is kept.

**Identity and selection.** The entity key is (`resource_id`, `entry_id`). `EntryID` is nonblank and unique within
every body and across all 74,137 rows (numerically 1 to 74,647, so 510 numbers in that span do not appear in the
captured data; 360 of them, 19 to 378, fall between the last August 2020 entry and the first October 2020 entry,
where the series has no September 2020 resource; `TODO: verify` why, for example instructions never confirmed by
the provider). A vendor guarantee
that an `EntryID` is permanent is not stated, so `resource_id` stays in the key and `latest` is the whole capture of
each resource: a later capture of a monthly file replaces that file's rows and no other month's. Row order inside a
body is not by `EntryID` (the November 2021 body begins 12810, 12809).

**Service vocabulary (rows).** `Non-BM Fast Reserve` 72,503 · `Non-BM STOR` 1,620 · `RDP_NEGATIVE` 14. By start
year (2020 to 2026, rows with a start), STOR is 122, 680, 776, 26, 6, 1 and 1. There is
**no instruction-status column** in either header, so a cancelled or rejected instruction cannot be told apart from
a delivered one.

**Bronze.** One CSV per resource under
`bronze/neso_data_portal/asdp_instructions/2026/10/08/raw_<capture time>_<resource id>_<hash prefix>.csv`, with a
`.meta.json` sidecar. Bronze is immutable raw bytes. Epoch 1 body (first rows of `6f037ebe-...`, June 2020):

```text
EntryID,ServiceType,InstructionStartDateTime,MW,IndicativePrice,InstructionCeaseDateTime,DispatchDateTimeStamp,CeaseDateTimeStamp
1,Non-BM STOR,2020-06-25 01:49:00Z,4,48.85,2020-06-25 02:45:00Z,2020-06-25 01:47:36Z,2020-06-25 02:40:08Z
2,Non-BM STOR,2020-06-25 01:49:00Z,4,48.85,2020-06-25 02:45:00Z,2020-06-25 01:47:36Z,2020-06-25 02:40:08Z
```

Epoch 2 body (first rows of `90ba1625-...`, November 2021; the three trailing fields are blank):

```text
EntryID,ServiceType,InstructionStartDateTime,MW,IndicativePrice,InstructionCeaseDateTime,DispatchDateTimeStamp,CeaseDateTimeStamp,PartyID,AssetID,Tendered
12810,Non-BM Fast Reserve,2021-11-01T12:11:00,80,221.75,2021-11-01T12:46:00,2021-11-01T12:09:11,2021-11-01T12:43:43,,,
12809,Non-BM Fast Reserve,2021-11-01T12:11:00,80,221.75,2021-11-01T12:42:00,2021-11-01T12:09:11,2021-11-01T12:40:13,,,
```

**Silver sample** (two rows of `90ba1625-...`; engine columns other than the key partition omitted):

```python
[
    {"entry_id": "12836", "service_type": "Non-BM Fast Reserve",
     "instruction_start_date_time": "2021-11-02T18:46:00", "mw": 65.0, "indicative_price": 200.0,
     "instruction_cease_date_time": "2021-11-02T18:53:05",
     "dispatch_date_time_stamp": "2021-11-02T18:43:48", "cease_date_time_stamp": "2021-11-02T18:51:49",
     "party_id": "ENWL", "asset_id": "OFR-ENWL-1", "tendered": "Non-tendered",
     "resource_id": "90ba1625-d99b-4ec6-8356-ad69af4e6b20"},
    {"entry_id": "12837", "service_type": "Non-BM Fast Reserve",
     "instruction_start_date_time": "2021-11-02T19:15:00", "mw": 60.0, "indicative_price": 200.0,
     "instruction_cease_date_time": "2021-11-02T19:22:00",
     "dispatch_date_time_stamp": "2021-11-02T19:13:19", "cease_date_time_stamp": "2021-11-02T19:21:20",
     "party_id": "ENWL", "asset_id": "OFR-ENWL-1", "tendered": "Non-tendered",
     "resource_id": "90ba1625-d99b-4ec6-8356-ad69af4e6b20"},
]
```

Silver path: `silver/neso_data_portal/asdp_instructions/year=2026/month=10/` (the partition is the capture month, because
`timestamp_utc` is the capture time).

## Cadence

- Registry refresh: frozen
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Not Active

The vendor text says the instructions are "continuously published throughout the day", which describes the service
before its migration to OBP; the `Not Active` label, the OBP successor note and the last start label (2026-04-17)
all point to a closed series. The package metadata in the catalogue snapshot was last modified 2026-05-11.
gridflow has one capture per resource, so whether past months were ever amended or re-published is unmeasured
(`TODO: verify` by comparing a later capture with the hash-pinned bodies).

## Licence and attribution

- Licence: NESO Open Data Licence
  ([licence text](https://www.neso.energy/data-portal/ngeso-open-licence))
- Attribution: Supported by National Energy SO Open Data

Any gridflow output derived from this package carries the attribution line "Supported by National Energy SO Open Data".

## Holds

- none

Nothing is held for this package: the resources and the family are eligible. The open `TODO:` items on this page are
documented uncertainties that do not block publication. The **sibling** package, ASDP window prices
(@./non-bm-ancillary-service-dispatch-platform-asdp-window-prices.md), **is** held on `ASDP-WINDOW-PRICE-UNIT`
(unit v0.22-K-AS-5b): the vendor calls its `WindowPrice` only an indicative price with no currency, energy or time
denominator, and the £/MWh of this table's `indicative_price` cannot be carried across. Do not read the window-price
column through this page's unit.

## Known issues and gotchas

- **`timestamp_utc` is the capture time, not the instruction time** (temporal `none`). A time series built on
  `timestamp_utc` or `event_time` is a plot of the 2026-10-08 download, not of the instructions.
- **The time columns are raw strings in two spellings, with no zone marker after December 2020.** Parse them only
  once the export clock is established (`TODO: ASDP-EXPORT-CLOCK`); a UTC reading of the naive cells is an
  assumption, and a local-time reading is equally unproven.
- **`TODO: ASDP-ISSUE-IMMUTABILITY`.** The dispatch and cease messages are separate publication stages, but a row
  holds both. A dispatch stamp does not prove a populated cease field was published at that time, so no per-row
  availability earlier than the capture is claimed (issue `none`, no backdating). Repeat captures, or a vendor
  guarantee of versioning, would settle it.
- **`TODO: ASDP-SIGN-CONVENTION`.** `mw` is positive in every row (3 to 100), including the 14 `RDP_NEGATIVE` rows
  (4 to 7 MW, the first with a start label of 2023-11-21T14:47:44). The vendor explains an RDP MW Dispatch as a
  curtailment down to 0 MW, so a positive quantity can mean a reduction in output. Do not treat every positive `mw`
  as positive reserve or as an increase in generation; keep `service_type` beside it. A vendor mapping of
  dispatched MW to an operational baseline would settle the sign.
- **109 rows are cease-only.** They have an `entry_id`, a service type and a cease time, but no start time, MW,
  price or dispatch stamp. They are kept (never dropped) and are not repaired from a neighbouring row.
- **No status column.** The vendor says only confirmed instructions are published; whether a cease row can follow
  a dispatch that never ran is not stated.
- **Migration to OBP.** Reporting periods overlap from 2025-10-10, with different grain and identifier systems; see
  the overview. The OBP instructions page's vendor text says OBP will incrementally master more non-BM services, with
  less published on ASDP, while this package's text says the services here have migrated; the two vendor statements
  are not reconciled (`TODO: verify`). The services differ: ASDP silver holds only `Non-BM STOR`,
  `Non-BM Fast Reserve` and `RDP_NEGATIVE` rows, while OBP's rows, from 2025-10-10, are Positive Quick Reserve,
  Positive Slow Reserve and MW Dispatch (@./obp-non-bm-reserve-instructions.md).
- **Resource wording.** The resource names say "Dispatch Cease Instructions" and the older descriptions say
  "published on NG website" (National Grid-era wording, retained by the vendor); the series has no September 2020
  resource.
- **Not settlement data.** There is no `run_type` and no settlement period, so the settlement-period rules (range
  1..50, 46 and 50 period days) do not apply, and no key involves a date.

## Implementation delta

The ratified record follows the vendor dictionary; the differences are deliberate typing choices.

- **`entry_id`**: the dictionary types `EntryID` as Integer, and the registry holds `string` (identifiers are kept
  byte-equal and never cast; K-AS-5b-SPEC seat ruling 2).
- **The four time columns**: the dictionary types them as DateTime, and the registry holds raw `string` (export
  clock undocumented, and a literal `Z` in one epoch does not license typing the naive cells; `ASDP-EXPORT-CLOCK`).
- **`mw`**: the dictionary says Integer; the registry holds `float64` (the batch rule for measured values). Every
  captured value is between 3 and 100. `TODO: verify` whether any captured value is non-integral.
- **Vintage**: the family is a datastore dump, so `capture_fallback` is used rather than the CKAN `last_modified`
  vintage used for upload families.
- **No silver relation to OBP**, although the vendor names OBP as the successor (seat ruling 3).
- No endpoint, query-parameter or authentication discrepancies apply: the data is read from the public datastore
  dump URLs, which need no key.

## Modelling notes

`TODO`: no gold view or models feed exists for this dataset (RULINGS 555), and its modelling use is not designed.
Cautions for anyone designing one:

- The silver table has no event time, so a time series of instructions needs the raw time columns parsed after the
  export clock is established.
- Keep `service_type` beside `mw` (see the sign note); `RDP_NEGATIVE` is a different mechanism from reserve
  instructions.
- Flag the 109 cease-only rows and the 203 rows with no cease time before computing durations.
- Do not join to OBP on `entry_id`; `TODO: verify` that asset identifiers correspond before joining on them.
- Related pages: @./obp-non-bm-reserve-instructions.md (successor) and
  @./short-term-operating-reserve-stor-day-ahead-auction-results.md (the STOR service context).

## Links

- [NESO Open Data Portal package](https://www.neso.energy/data-portal/non-bm-ancillary-service-dispatch-platform-asdp-instructions)
- [Party ID and Asset ID reference document](https://www.neso.energy/document/294096/download)
- [STOR ASDP guidance](https://www.neso.energy/document/186511/download)
- Registry record: gridflow `@src/gridflow/connectors/neso_data_portal/registry/non-bm-ancillary-service-dispatch-platform-asdp-instructions.json`
- Eligibility report: gridflow `@docs/neso_data_portal/eligibility.md`
- Batch facts: gridflow `@.planning/phases/v0.22-K-AS-5/K-AS-5-FACTS.md` (ASDP instructions section); spec
  `@.planning/phases/v0.22-K-AS-5/K-AS-5b-SPEC.md`; activation `@.planning/v0.22-RESULTS.md` section AS-5b
- Sibling pages: @./non-bm-ancillary-service-dispatch-platform-asdp-window-prices.md ·
  @./obp-non-bm-reserve-instructions.md · @./obp-non-bm-physical-notifications.md
