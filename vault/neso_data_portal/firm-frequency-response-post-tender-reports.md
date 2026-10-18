---
source: "neso_data_portal"
package: "firm-frequency-response-post-tender-reports"
dataset_keys: ["ffr_post_tender_reports_csv", "ffr_post_tender_reports_csv_ext", "ffr_post_tender_reports_ext", "ffr_post_tender_reports_workbook"]
vendor: "NESO Open Data Portal"
skeleton: false
layer_coverage: "bronze, silver"
updated: 2026-10-14
eligibility: "eligible"
---

# Firm Frequency Response (FFR) Post Tender Reports

Monthly post-tender reports for National Grid ESO's (now NESO) Firm Frequency Response (FFR) market. Each report covers one tender round (the `TR` number) and lists every tender submission with the decision NESO took: accepted or rejected, rejection reason codes, the company and unit that tendered, the tendered service period, the recurring daily availability windows, the tendered prices and the frequency-response volumes the unit offered at each deviation level. NESO describes the reports as showing which tenders were accepted and rejected and the information submitted for them. A row is therefore a tender submission, not a settled delivery or a payment. Service capabilities and weekday/weekend windows are wide columns on that row.

Use it to study how the FFR market priced availability over time and who offered what. It is not a delivery or settlement record: it says what was offered and decided at tender, not what was dispatched.

In gridflow the three NESO naming families (`CSV`, `CSV EXT`, `EXT` uploads) publish the same monthly table, so they are read as **one table** (`ffr_post_tender_reports_csv_ext`, with the other two as siblings). Dates and the recurring window clocks are **raw vendor strings** (calendar dates and Excel serial integers are mixed, so no date is parsed). Two CSV resources, TR147 and TR154, are **held** and not transformed.

The older Excel uploads (XLSX/XLSM, TR108 to TR166) are read into a **second table**, `ffr_post_tender_reports_workbook` (v0.22 AS-5c, 59 workbooks and 10,094 rows; TR123 and TR125 are held). Workbook dates are stored as Excel 1900-system serial numbers, not parsed. **The workbook table and the CSV table overlap on TR139-TR166 - never add them.**

Supported by National Energy SO Open Data

- Vendor dataset page: [NESO post-tender dataset](https://www.neso.energy/data-portal/firm-frequency-response-post-tender-reports)
- TODO: verify whether a vault domain note on frequency response exists to link from here (none checked for this page).

- Publisher group: Ancillary services
- Registry group: ancillary-services · archetype: EVT

## Files by disposition

### SILVER

26 CSV resources (`ffr_post_tender_reports_csv_ext`, AS-5a) and 59 workbook resources (`ffr_post_tender_reports_workbook`, AS-5c; one tender sheet each). The format column is the catalogue label, which is not reliable for the workbooks: the captured bodies are 22 plain `.xlsx` and 39 macro-enabled `.xlsm`, the reverse of the catalogue's 39 `XLSX` and 22 `XLSM`, so the reader dispatches on the body, never the label.

| Resource | Format | Capture | Id |
|---|---|---|---|
| Post Tender Report TR139 July 2021 CSV- EXT | CSV | upload | `9347c45d-bffd-40ee-aa1e-593b41bde9a4` |
| Post Tender Report TR140 August 2021 CSV- EXT | CSV | upload | `fe695206-4729-46f2-a82e-b05ed8552da8` |
| Post Tender Report TR141 September 2021 CSV- EXT | CSV | upload | `5e0afd6e-ab83-480a-938b-e0da0223fcbc` |
| Post Tender Report TR142 October 2021 EXT | CSV | upload | `1882b277-6349-4513-9939-b39e1992620b` |
| Post Tender Report TR143 November 2021 EXT | CSV | upload | `990dd811-e65a-4361-87fc-9d07d6c0af45` |
| Post Tender Report TR144 December 2021 CSV | CSV | upload | `ceefff8c-7f61-41dd-b567-42774ca487bc` |
| Post Tender Report TR145 January 2022 CSV EXT | CSV | upload | `61ee31ac-1f2d-4744-add3-bac7878c6010` |
| Post Tender Report TR146 February 2022 CSV- EXT | CSV | upload | `66e127dc-5e95-49b5-bc55-915269d09e1a` |
| Post Tender Report TR148 April 2022 CSV EXT | CSV | upload | `fc994d78-f7d0-4a29-9ea7-31121931d04c` |
| Post Tender Report TR149 May 2022 CSV EXT | CSV | upload | `a32e86a6-6bd3-422c-996a-7245dcb9b6ee` |
| Post Tender Report TR150 June 2022CSV EXT | CSV | upload | `36164e1d-c6d5-4a58-85b1-74c3a01b0a9b` |
| Post Tender Report TR151 July 2022 CSV EXT | CSV | upload | `fcc91d6f-e35a-4878-a77d-d2882d01c357` |
| Post Tender Report TR152 August 2022 CSV EXT | CSV | upload | `7ed768cf-aa45-4577-bc7f-c1b64e534812` |
| Post Tender Report TR153 September 2022 CSV- EXT | CSV | upload | `178b6c47-6b27-403e-9715-87f41b48a84b` |
| Post Tender Report TR155 November 2022 CSV- EXT | CSV | upload | `904d2bf0-8396-43c4-8b8a-cafe105fc47c` |
| Post Tender Report TR156 December 2022 CSV - EXT | CSV | upload | `fd84c085-4ff8-45b4-b2ee-43ad2b052d9f` |
| Post Tender Report TR157 January 2023 CSV EXT | CSV | upload | `bd7cbfb7-a8cb-4b84-bd69-42abff36af0d` |
| Post Tender Report TR158 February 2023 CSV EXT | CSV | upload | `e15891f5-fd65-437f-823f-2906f238d0af` |
| Post Tender Report TR159 March 2023 CSV EXT | CSV | upload | `41c9403d-9618-4eb9-be69-45b9923bcf3f` |
| Post Tender Report TR160 April 2023 CSV EXT | CSV | upload | `a99bc100-352b-433a-83fc-5514affbbc0e` |
| Post Tender Report TR161 May 2023 CSV EXT | CSV | upload | `3d71f7d1-3dd7-40b1-b5f4-708da72a4f67` |
| Post Tender Report TR162 JUNE 2023 CSV EXT | CSV | upload | `fd57201c-24f6-4d42-8be2-177dd4b36229` |
| Post Tender Report TR163 July 2023 CSV EXT | CSV | upload | `fbb1ce86-b2f7-405d-94ac-6cef6f14cceb` |
| Post Tender Report TR164 August 2023 CSV EXT | CSV | upload | `2bfa2ab3-7f4e-44d7-a9ab-7342c4b9cd34` |
| Post Tender Report TR165 September 2023 CSV EXT | CSV | upload | `bec39c50-563c-4ed6-8100-8b519dcbf1ef` |
| Post Tender Report TR166 October 2023 CSV EXT | CSV | upload | `59dfabd4-a395-4ddc-a261-2f546a8a3b52` |
| Post Tender Report - TR108 Dec-18 | XLSX | upload | `31854ad2-0e98-48ab-8893-dc9b9d473091` |
| Post Tender Report - TR109 Jan-19 | XLSX | upload | `27ad6287-1d56-493f-a45f-a6707dc02e14` |
| Post Tender Report - TR110 Feb-19 | XLSX | upload | `50488f63-b71b-4647-b2d9-95efbddddf17` |
| Post Tender Report - TR111 Mar-19 | XLSX | upload | `d16afe87-cce1-43f2-a36b-d7707ae648d7` |
| Post Tender Report - TR112 Apr-19 | XLSX | upload | `dbaa2bb4-ab77-4297-90f2-a7f27e96f7fb` |
| Post Tender Report - TR113 May-19 | XLSX | upload | `aa3c7d58-9ed5-460a-bcba-415567abf9fb` |
| Post Tender Report - TR114 Jun-19 | XLSX | upload | `93802a8f-19ee-4c6b-9fe4-3783085eb0f9` |
| Post Tender Report - TR115 Jul-19 | XLSX | upload | `1c1c7788-a0c0-40c9-97fc-03be099995e5` |
| Post Tender Report - TR116 Aug-19 | XLSX | upload | `1eb0314b-54dc-45f4-80f7-f32e7edda972` |
| Post Tender Report - TR117 Sep-19 | XLSX | upload | `8c1dc03e-1463-4a52-94d9-b659ff2127c5` |
| Post Tender Report - TR118 Oct-19 | XLSX | upload | `d397ffa6-2b7c-4b8f-8cc1-36b267ea6ac1` |
| Post Tender Report - TR119 Nov-19 | XLSX | upload | `0544683b-0d5e-41a3-ba42-270b2d689fdf` |
| Post Tender Report - TR120 Dec-19 | XLSX | upload | `653110b8-4311-4489-81d3-dd6c01043b4e` |
| Post Tender Report - TR121 Jan-20 | XLSX | upload | `e692dc29-e94c-4be7-8067-4fc6af8bab22` |
| Post Tender Report - TR122 Feb-20 | XLSX | upload | `bf1bbc9a-ace7-4ec0-a0d5-aa6313fade21` |
| Post Tender Report- TR124 Apr- 20 | XLSX | upload | `93dac57b-a373-4fed-ab9f-338336a685e6` |
| Post Tender Report - TR126 June 2020 | XLSX | upload | `9137187c-8626-4d28-a538-3dd9eb395644` |
| Post Tender Report - TR127 July 2020 | XLSX | upload | `68529290-7992-4891-90bc-68fa9bcb5aeb` |
| Post Tender Report - TR127 July 2020 - Amended | XLSX | upload | `16773f53-c0f9-4b8c-aaee-ad819e93d405` |
| Post Tender Report TR128 August 2020 | XLSX | upload | `6e6b47ea-afae-4366-bdce-d961bdcb21fe` |
| Post Tender Report TR129 September 2020 | XLSX | upload | `5a1f039a-c6c8-43a2-9ae4-069a0a0b32b2` |
| Post Tender Report TR130 October 2020 | XLSX | upload | `4b4a2e83-094c-4566-90c1-98366469b504` |
| Post Tender Report TR131 November 2020 - EXT | XLSX | upload | `c325243e-2a5d-4585-9d56-2207d781d7a2` |
| Post Tender Report TR132 December 2020 EXT | XLSX | upload | `ce75bd6e-5c16-41b5-bf7f-ebf3b44508f3` |
| Post Tender Report TR133 January 2021 - EXT | XLSX | upload | `0f72be2e-71d3-4a6e-a19d-c627dd25c3bb` |
| Post Tender Report TR134 February 2021- EXT | XLSX | upload | `36c2cf05-c72b-4d18-91bd-dc2104f6103e` |
| Post Tender Report TR135 March 2021- EXT | XLSX | upload | `eaddd8aa-6cd1-403c-943e-4ffa6ce9ec9b` |
| Post Tender Report TR136 April 2021- EXT | XLSX | upload | `7912d65a-451a-4dea-b8eb-4bc5c7af254b` |
| Post Tender Report TR136 April 2021 EXT- Amended | XLSX | upload | `a85e6149-3893-48f6-953a-0a10e796ce8e` |
| Post Tender Report TR137 May 2021 EXT | XLSX | upload | `6e4f83e8-28d8-42f3-8e95-52928e58fb20` |
| Post Tender Report TR138 June 2021 EXT | XLSX | upload | `bc47f2cb-695e-450e-a800-cad8cfecaaf1` |
| Post Tender Report TR139 July 2021 EXT | XLSX | upload | `a5b3f43d-35f9-4384-b35c-a2d78d7bb4ba` |
| Post Tender Report TR140 August 2021 EXT | XLSX | upload | `d96d15ed-8705-42f5-a65d-f63468516e08` |
| Post Tender Report TR141 September 2021 EXT | XLSX | upload | `4df9b9b7-db93-4c98-93e0-1b57b8c256c7` |
| Post Tender Report TR142 October 2021 EXT xlms | XLSX | upload | `89134181-f1f0-4605-894f-859e1d19eb7b` |
| Post Tender Report TR143 November 2021.xlms. EXT | XLSM | upload | `a2888ffb-f2bc-455c-8d2c-8e70b194914e` |
| Post Tender Report TR144 December 2021 EXT | XLSX | upload | `6cd10acf-2524-4c3f-8509-f657eeae73e5` |
| Post Tender Report TR145 January 2022 EXT | XLSM | upload | `29014d2b-7ae3-4689-8dba-9e3a181b26e9` |
| Post Tender Report TR146 February 2022 EXT | XLSM | upload | `85ec5689-e1ab-4d12-8268-a84bd579beac` |
| Post Tender Report TR147 March 2022 EXT | XLSM | upload | `8ec9b10f-01e2-44ca-a3cb-2e9557a46410` |
| Post Tender Report TR148 April 2022 EXT | XLSM | upload | `c72a9877-e718-4b98-a942-ec61d3891e05` |
| Post Tender Report TR149 May 2022 EXT | XLSM | upload | `46313224-61d2-4c48-b59c-5973328ad5c3` |
| Post Tender Report TR150 June 2022 EXT | XLSX | upload | `e5c028dd-265e-4684-a419-cee906617e11` |
| Post Tender Report TR151 July 2022 EXT | XLSM | upload | `0ad0f7f5-314e-4d7a-b6df-84a7b77c9908` |
| Post Tender Report TR152 August 2022 EXT | XLSM | upload | `08ac3a6c-6f9e-4b6b-8389-38af6c1c9a46` |
| Post Tender Report TR153 September 2022 EXT | XLSM | upload | `854e29a9-3b94-41e0-8bbc-24ec270ae6fd` |
| Post Tender Report TR154 October 2022 EXT | XLSM | upload | `e4da45cc-fb8f-41e4-81f8-e61b6f413ae6` |
| Post Tender Report TR155 November 2022-  EXT | XLSM | upload | `244c9023-a68d-4a28-a4f3-7f492905ad99` |
| Post Tender Report TR156 December 2022- EXT | XLSM | upload | `1d0def5b-18b4-4184-9896-db328a443df2` |
| Post Tender Report TR157 January 2023 EXT | XLSM | upload | `8540c6b2-75e6-4e16-8113-0723a4a642b5` |
| Post Tender Report TR158 February 2023 EXT | XLSM | upload | `987467c5-a5fe-4d4c-a2c6-7e59a458e7af` |
| Post Tender Report TR159 March 2023 EXT | XLSM | upload | `ed783d99-dc3c-4deb-a847-c9d96295dcd4` |
| Post Tender Report TR160 April 2023 EXT | XLSM | upload | `5aa12080-f439-42ab-a806-cf2781750a29` |
| Post Tender Report TR161 May 2023 EXT | XLSM | upload | `634c7528-e461-49cf-ba7b-0fe20702717f` |
| Post Tender Report TR162 June 2023  EXT | XLSM | upload | `9a707d8f-36dc-4caf-9dfb-5c620e729d75` |
| Post Tender Report TR163 July 2023 EXT | XLSM | upload | `c3526774-2055-4fe9-b657-e829c9d65939` |
| Post Tender Report TR164 August 2023 EXT | XLSM | upload | `152ba991-4299-4801-9100-a80d7a0a079a` |
| Post Tender Report TR165 September 2023 EXT | XLSM | upload | `2e561c2b-0d70-44e7-ac0b-c99b3fe6ccdb` |
| Post Tender Report TR166 October 2023 EXT | XLSM | upload | `8bb5bf74-8f5e-44c7-a231-42d1323bfa73` |

### HOLD

Four resources are held. The full hold question for each is under "Held outputs".

| Resource | Format | Capture | Id | Reason (unit) |
|---|---|---|---|---|
| Post Tender Report TR147 March 2022 CSV EXT | CSV | upload | `c99081fb-0211-4a1a-9eed-53497f64a6ea` | FFR-TR147-THOUSANDS-SEPARATOR (v0.22-K-AS-5a) |
| Post Tender Report TR154 October 2022 CSV- EXT | CSV | upload | `7e48c1ce-b4cf-43fa-afe9-4e6730474944` | FFR-TR154-ORPHAN-ROWS (v0.22-K-AS-5a) |
| Post Tender Report - TR123 Mar-20 | XLSX | upload | `2e49daa5-90eb-4157-bcef-6fcf29e75085` | FFR-TR123-COMMA-MW (v0.22-K-AS-5c) |
| ↳ TR123 (sheet) | — | — | HOLD with its resource | same reason |
| Post Tender Report- TR125 May 2020- EXT | XLSX | upload | `4bea886e-3aad-4a8d-9bec-1c8e770739b0` | FFR-TR125-UNHEADED-AQ (v0.22-K-AS-5c) |
| ↳ TR125 (sheet) | — | — | HOLD with its resource | same reason |

### DOC

| Resource | Child | Disposition |
|---|---|---|
| Post Tender Report - TR121 Jan-20 (`e692dc29-e94c-4be7-8067-4fc6af8bab22`) | `Sheet1` (empty sheet) | DOC; the resource itself is `SILVER` through its `TR121 ` tender sheet |

## Families

### `ffr_post_tender_reports_csv`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no
- ingest-only: no silver yet

### `ffr_post_tender_reports_csv_ext`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Tender Ref | `tender_ref` | string | — | no | — | — |
| Status | `status` | string | — | yes | — | — |
| Rejection Codes | `rejection_codes` | string | — | yes | — | — |
| Company Name | `company_name` | string | — | yes | — | — |
| Tendered Unit (BMU/Unit ID) | `tendered_unit` | string | — | yes | — | — |
| TO connection / DNO connection | `connection_type` | string | — | yes | — | — |
| Generation Type | `generation_type` | string | — | yes | — | — |
| Start Date | `start_date` | string | — | yes | — | — |
| End Date | `end_date` | string | — | yes | — | — |
| Tendered Period (dd.mm.yy - dd.mm.yy) | `tendered_period` | string | — | yes | — | — |
| Applicable FFR Capability Data Table | `capability_data_table` | string | — | yes | — | — |
| Tendered Frames per Service Day - From (Mon-Fri) | `frame_from_mon_fri` | string | — | yes | — | — |
| Tendered Frames per Service Day - To (Mon- Fri) | `frame_to_mon_fri` | string | — | yes | — | — |
| Tendered Frames per Service Day - Duration (Mon-Fri) | `frame_duration_mon_fri` | float64 | — | yes | — | hours |
| Tendered Frames per Service Day - From (Saturday) | `frame_from_sat` | string | — | yes | — | — |
| Tendered Frames per Service Day - To (Saturday) | `frame_to_sat` | string | — | yes | — | — |
| Tendered Frames per Service Day - Duration (Saturday) | `frame_duration_sat` | float64 | — | yes | — | — |
| Tendered Frames per Service Day - From (Sunday/Bank Holidays) | `frame_from_sun_bh` | string | — | yes | — | — |
| Tendered Frames per Service Day - To (Sunday/Bank Holidays) | `frame_to_sun_bh` | string | — | yes | — | — |
| Tendered Frames per Service Day - Duration (Sunday/Bank Hol) | `frame_duration_sun_bh` | float64 | — | yes | — | £ |
| Tendered Prices - Availability Fee (£/h) | `availability_fee` | float64 | — | yes | — | £/h |
| Tendered Prices - Nomination Fee (£/h) | `nomination_fee` | string | — | yes | — | £/h |
| Tendered Prices - Window Initiation Fee (£/window) | `window_initiation_fee` | string | — | yes | — | £/window |
| BMUs Only | `bmus_only` | string | — | yes | — | — |
| Maximum Part Load Point (MW) | `max_part_load_point` | string | — | yes | — | MW |
| Minimum Part Load Point (MW) | `min_part_load_point` | string | — | yes | — | MW |
| Minimum MEL (MW) | `min_mel` | string | — | yes | — | MW |
| Maximum SEL (MW) | `max_sel` | string | — | yes | — | MW |
| Primary Response (max.) @ 0.2Hz (MW) | `primary_response_0_2hz` | float64 | — | yes | — | MW |
| Primary Response (max.) @ 0.5Hz (MW) | `primary_response_0_5hz` | float64 | — | yes | — | MW |
| Primary Response (max.) @ 0.8Hz (MW) | `primary_response_0_8hz` | float64 | — | yes | — | MW |
| Secondary Response (max.) @ 0.2/0.2Hz (MW) | `secondary_response_0_2hz` | float64 | — | yes | — | MW |
| Secondary Response (max.) @ 0.5/0.5Hz (MW) | `secondary_response_0_5hz` | float64 | — | yes | — | MW |
| High Frequency Response (max.) @ 0.2Hz (MW) | `high_frequency_response_0_2hz` | float64 | — | yes | — | MW |
| High Frequency Response (max.) @ 0.5Hz (MW) | `high_frequency_response_0_5hz` | float64 | — | yes | — | MW |
| Are you adding volume as per detail change provision | `detail_change_volume` | string | — | yes | — | — |
| Please state the accepted tender that you are stacking onto | `stacked_onto_tender` | string | — | yes | — | — |
| Please state if this is an all or nothing bid. | `all_or_nothing_bid` | string | — | yes | — | — |
| Please indicate if this is a mutually exclusive tender | `mutually_exclusive_tender` | string | — | yes | — | — |
| Automatic Response Energy Deliverable by 10s (MW) | `auto_response_10s` | string | — | yes | — | MW |
| Automatic Response Energy Deliverable by 30s (MW) | `auto_response_30s` | string | — | yes | — | MW |
| Post code | `post_code` | string | — | yes | — | — |
| Comments | `comments` | string | — | yes | — | — |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Tender Ref | `tender_ref` | string | — | no | — | — |
| Status | `status` | string | — | yes | — | — |
| Rejection Codes | `rejection_codes` | string | — | yes | — | — |
| Company Name | `company_name` | string | — | yes | — | — |
| Tendered Unit (BMU/Unit ID) | `tendered_unit` | string | — | yes | — | — |
| TO connection / DNO connection | `connection_type` | string | — | yes | — | — |
| Generation Type | `generation_type` | string | — | yes | — | — |
| Start Date | `start_date` | string | — | yes | — | — |
| End Date | `end_date` | string | — | yes | — | — |
| Tendered Period (dd.mm.yy - dd.mm.yy) | `tendered_period` | string | — | yes | — | — |
| Applicable FFR Capability Data Table | `capability_data_table` | string | — | yes | — | — |
| Tendered Frames per Service Day - From (Mon-Fri) | `frame_from_mon_fri` | string | — | yes | — | — |
| Tendered Frames per Service Day - To (Mon- Fri) | `frame_to_mon_fri` | string | — | yes | — | — |
| Tendered Frames per Service Day - Duration (Mon-Fri) | `frame_duration_mon_fri` | float64 | — | yes | — | hours |
| Tendered Frames per Service Day - From (Saturday) | `frame_from_sat` | string | — | yes | — | — |
| Tendered Frames per Service Day - To (Saturday) | `frame_to_sat` | string | — | yes | — | — |
| Tendered Frames per Service Day - Duration (Saturday) | `frame_duration_sat` | float64 | — | yes | — | — |
| Tendered Frames per Service Day - From (Sunday/Bank Holidays) | `frame_from_sun_bh` | string | — | yes | — | — |
| Tendered Frames per Service Day - To (Sunday/Bank Holidays) | `frame_to_sun_bh` | string | — | yes | — | — |
| Tendered Frames per Service Day - Duration (Sunday/Bank Hol) | `frame_duration_sun_bh` | float64 | — | yes | — | £ |
| Tendered Prices - Availability Fee (£/h) | `availability_fee` | float64 | — | yes | — | £/h |
| Tendered Prices - Nomination Fee (£/h) | `nomination_fee` | string | — | yes | — | £/h |
| Tendered Prices - Window Initiation Fee (£/window) | `window_initiation_fee` | string | — | yes | — | £/window |
| BMUs Only | `bmus_only` | string | — | yes | — | — |
| Maximum Part Load Point (MW) | `max_part_load_point` | string | — | yes | — | MW |
| Minimum Part Load Point (MW) | `min_part_load_point` | string | — | yes | — | MW |
| Minimum MEL (MW) | `min_mel` | string | — | yes | — | MW |
| Maximum SEL (MW) | `max_sel` | string | — | yes | — | MW |
| Primary Response (max.) @ 0.2Hz (MW) | `primary_response_0_2hz` | float64 | — | yes | — | MW |
| Primary Response (max.) @ 0.5Hz (MW) | `primary_response_0_5hz` | float64 | — | yes | — | MW |
| Primary Response (max.) @ 0.8Hz (MW) | `primary_response_0_8hz` | float64 | — | yes | — | MW |
| Secondary Response (max.) @ 0.2/0.2Hz (MW) | `secondary_response_0_2hz` | float64 | — | yes | — | MW |
| Secondary Response (max.) @ 0.5/0.5Hz (MW) | `secondary_response_0_5hz` | float64 | — | yes | — | MW |
| High Frequency Response (max.) @ 0.2Hz (MW) | `high_frequency_response_0_2hz` | float64 | — | yes | — | MW |
| High Frequency Response (max.) @ 0.5Hz (MW) | `high_frequency_response_0_5hz` | float64 | — | yes | — | MW |
| Are you adding volume as per detail change provision | `detail_change_volume` | string | — | yes | — | — |
| Please state the accepted tender that you are stacking onto | `stacked_onto_tender` | string | — | yes | — | — |
| Please state if this is an all or nothing bid. | `all_or_nothing_bid` | string | — | yes | — | — |
| Please indicate if this is a mutually exclusive tender | `mutually_exclusive_tender` | string | — | yes | — | — |
| Automatic Response Energy Deliverable by 10s (MW) | `auto_response_10s` | string | — | yes | — | MW |
| Automatic Response Energy Deliverable by 30s (MW) | `auto_response_30s` | string | — | yes | — | MW |
| Comments | `comments` | string | — | yes | — | — |

- Entity key: `resource_id`, `tender_ref`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

### `ffr_post_tender_reports_ext`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no
- ingest-only: no silver yet

### `ffr_post_tender_reports_files`

- Kind: files · archetype: EVT · refresh: frozen · empty allowed: no
- files: catalogue only

### `ffr_post_tender_reports_workbook`

- Kind: tabular · archetype: EVT · refresh: frozen · empty allowed: no · sibling of `ffr_post_tender_reports_files`
- Reader: `xlsx` with a per-resource block map (v0.22-K-AS-5c; ADR-037 amendment 1). The workbooks have merged composite headers of three stacked rows, example rows ahead of the tender block and block ends that differ per workbook, so the record declares, for each of the 59 `SILVER` workbook resources (32 over columns A:AP, 27 over A:AQ), the sheet name (trailing spaces exact), the header rows, the data rows and the column range. The held TR123 and TR125 have no block entry. A `SILVER` resource missing from the map fails its capture; there is no fallback. Rows are selected by declared position only, never by value, so no example, note or footer row loads.
- Composite header: the non-empty stacked header cells of a column are joined with ` | ` into one label per column and frozen as the epoch header. The 59 loaded sheets produce **16 distinct header tuples** (epochs): 8 over columns A:AP (42 columns, no postcode) and 8 over A:AQ (43 columns, with `Post Code`). They differ only in the wording of the rejection-code heading, four instruction texts, the Mon-Fri `From` heading and the A:AQ tail. Every populated heading maps to a column of the CSV table, so the workbook table has the same 43 silver columns (`post_code` null where the workbook has no such column).
- Entity key: `resource_id`, `tender_ref` · Latest: `whole_capture` per `resource_id` · Temporal recipe: none: `timestamp_utc` is the capture time (2026-10-08) · issue: none · vintage: `ckan_last_modified`
- Silver: **10,094 rows over 59 resources**, each resource loading exactly its counted tender rows with 0 rows excluded. Two workbook resources are held (TR123, TR125) and load nothing.
- Eligibility: eligible. The table is separate from the CSV table and overlaps it (see Known issues).

Schema (the 43 silver columns; the dtype is the same in every epoch):

| Silver column | Dtype | Unit | Notes |
|---|---|---|---|
| `tender_ref` | string | — | Entity-key part; stored lexical form of the worksheet cell, so floating-point tails survive (see Known issues) |
| `status`, `rejection_codes`, `company_name`, `tendered_unit`, `connection_type`, `generation_type` | string | — | |
| `start_date`, `end_date` | string | — | Raw stored text; Excel 1900-system serial numbers for all but 12 cells (see Time and clock semantics) |
| `tendered_period`, `capability_data_table` | string | — | |
| `frame_from_mon_fri`, `frame_to_mon_fri`, `frame_from_sat`, `frame_to_sat`, `frame_from_sun_bh`, `frame_to_sun_bh` | string | none | Raw recurring window clock labels, never composed into a timestamp |
| `frame_duration_mon_fri`, `frame_duration_sat`, `frame_duration_sun_bh` | float64 | hours | The workbook headings say `Duration (h)` for all three |
| `availability_fee` | float64 | £/h | |
| `nomination_fee` | string | £/h | Kept as string (see Sentinels) |
| `window_initiation_fee` | string | £/window | Kept as string (see Sentinels) |
| `bmus_only` | string | — | |
| `max_part_load_point`, `min_part_load_point`, `min_mel`, `max_sel` | string | MW | Kept as string (see Sentinels) |
| `primary_response_0_2hz`, `primary_response_0_5hz`, `primary_response_0_8hz`, `secondary_response_0_2hz`, `secondary_response_0_5hz`, `high_frequency_response_0_2hz`, `high_frequency_response_0_5hz` | float64 | MW | |
| `detail_change_volume`, `stacked_onto_tender`, `all_or_nothing_bid`, `mutually_exclusive_tender` | string | — | |
| `auto_response_10s`, `auto_response_30s` | string | MW | Kept as string |
| `comments` | string | — | |
| `post_code` | string | — | Present in the 43-column layouts only; null for every row of a resource whose workbook has no postcode column |

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Reading the family list.** `ffr_post_tender_reports_csv_ext` and `ffr_post_tender_reports_workbook` are the only families that carry a silver record. The generated "ingest-only: no silver yet" lines under `ffr_post_tender_reports_csv` and `ffr_post_tender_reports_ext` describe the registry family listing: those two families are declared as siblings of the CSV owner, their resources (TR144 for `_csv`; TR142 and TR143 for `_ext`) are dispositioned `SILVER` with key `ffr_post_tender_reports_csv_ext`, and their rows are in the owner's silver (v0.22-K-AS-5a, ruling 766 call 1). `ffr_post_tender_reports_files` is the catalogue-only family that holds the 61 workbook uploads; their rows are read into `ffr_post_tender_reports_workbook`.

## Resources and download links (CSV tables)

The 26 transformed CSV resources plus the 2 held CSV resources. `Rows` is the silver row count (5,457 in total, the activation receipt figure). `Published at` is the CKAN `last_modified` of the captured file, which is the vintage clock `available_at` (see Clocks); for the two held resources it is the catalogue-snapshot value because nothing was transformed. The workbook resources are in the next section.

| Resource | Family (as published) | Rows | Published at (UTC) | File |
|---|---|---|---|---|
| Post Tender Report TR139 July 2021 CSV- EXT | `ffr_post_tender_reports_csv_ext` | 97 | 2021-07-22T11:52:10Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/9347c45d-bffd-40ee-aa1e-593b41bde9a4/download/tr139-post-tender-reports_v1-1.csv) |
| Post Tender Report TR140 August 2021 CSV- EXT | `ffr_post_tender_reports_csv_ext` | 90 | 2021-08-17T14:31:55Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/fe695206-4729-46f2-a82e-b05ed8552da8/download/post-tender-report-tr140-august-2021-csv-ext.csv) |
| Post Tender Report TR142 October 2021 EXT | `ffr_post_tender_reports_ext` | 164 | 2021-10-18T16:09:22Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/1882b277-6349-4513-9939-b39e1992620b/download/tr142-post-tender-reports_v1-1.csv) |
| Post Tender Report TR143 November 2021 EXT | `ffr_post_tender_reports_ext` | 201 | 2021-11-16T16:34:32Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/990dd811-e65a-4361-87fc-9d07d6c0af45/download/tr143-post-tender-reports_v1.1-1.csv) |
| Post Tender Report TR144 December 2021 CSV | `ffr_post_tender_reports_csv` | 240 | 2021-12-16T16:31:59Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/ceefff8c-7f61-41dd-b567-42774ca487bc/download/tr144-post-tender-reports_v11.csv) |
| Post Tender Report TR145 January 2022 CSV EXT | `ffr_post_tender_reports_csv_ext` | 229 | 2022-01-19T16:19:50Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/61ee31ac-1f2d-4744-add3-bac7878c6010/download/tr145-post-tender-reports_v11.csv) |
| Post Tender Report TR148 April 2022 CSV EXT | `ffr_post_tender_reports_csv_ext` | 203 | 2022-04-20T13:01:32Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/fc994d78-f7d0-4a29-9ea7-31121931d04c/download/tr148-post-tender-reports_v11ext.csv) |
| Post Tender Report TR146 February 2022 CSV- EXT | `ffr_post_tender_reports_csv_ext` | 196 | 2022-04-26T14:52:49Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/66e127dc-5e95-49b5-bc55-915269d09e1a/download/tr146-post-tender-reports_v11-csv-corrected-tender-ref.csv) |
| Post Tender Report TR149 May 2022 CSV EXT | `ffr_post_tender_reports_csv_ext` | 227 | 2022-05-18T12:36:31Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/a32e86a6-6bd3-422c-996a-7245dcb9b6ee/download/tr149-post-tender-reports_v11ext.csv) |
| Post Tender Report TR150  June 2022CSV  EXT | `ffr_post_tender_reports_csv_ext` | 259 | 2022-06-21T12:25:39Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/36164e1d-c6d5-4a58-85b1-74c3a01b0a9b/download/tr150-post-tender-reports_v11ext.csv) |
| Post Tender Report TR151 July 2022 CSV EXT | `ffr_post_tender_reports_csv_ext` | 252 | 2022-08-18T12:55:34Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/fcc91d6f-e35a-4878-a77d-d2882d01c357/download/tr151-post-tender-reports_v1-amended1ext.csv) |
| Post Tender Report TR152 August 2022 CSV EXT | `ffr_post_tender_reports_csv_ext` | 266 | 2022-08-19T15:46:57Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/7ed768cf-aa45-4577-bc7f-c1b64e534812/download/tr152-post-tender-reports_v11ext.csv) |
| Post Tender Report TR153 September 2022 CSV- EXT | `ffr_post_tender_reports_csv_ext` | 272 | 2022-09-16T14:24:54Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/178b6c47-6b27-403e-9715-87f41b48a84b/download/tr153-post-tender-reports_v11ext.csv) |
| Post Tender Report TR155 November 2022 CSV-  EXT | `ffr_post_tender_reports_csv_ext` | 281 | 2022-11-18T10:56:58Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/904d2bf0-8396-43c4-8b8a-cafe105fc47c/download/tr155-post-tender-reports_v11ext.csv) |
| Post Tender Report TR156 December 2022 CSV - EXT | `ffr_post_tender_reports_csv_ext` | 269 | 2022-12-16T15:10:11Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/fd84c085-4ff8-45b4-b2ee-43ad2b052d9f/download/tr156-post-tender-reports_v11ext.csv) |
| Post Tender Report TR157 January 2023 CSV EXT | `ffr_post_tender_reports_csv_ext` | 291 | 2023-01-18T15:49:00Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/bd7cbfb7-a8cb-4b84-bd69-42abff36af0d/download/tr157-post-tender-reports_v11ext.csv) |
| Post Tender Report TR158 February 2023 CSV EXT | `ffr_post_tender_reports_csv_ext` | 310 | 2023-02-15T14:32:23Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/e15891f5-fd65-437f-823f-2906f238d0af/download/tr158-post-tender-reports_v11ext.csv) |
| Post Tender Report TR159 March 2023 CSV EXT | `ffr_post_tender_reports_csv_ext` | 206 | 2023-03-16T14:14:06Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/41c9403d-9618-4eb9-be69-45b9923bcf3f/download/tr159-post-tender-reports_v11ext.csv) |
| Post Tender Report TR160 April 2023 CSV EXT | `ffr_post_tender_reports_csv_ext` | 203 | 2023-04-19T11:32:51Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/a99bc100-352b-433a-83fc-5514affbbc0e/download/tr160-post-tender-reports_v11ext.csv) |
| Post Tender Report TR161 May 2023 CSV EXT | `ffr_post_tender_reports_csv_ext` | 209 | 2023-05-17T13:46:48Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/3d71f7d1-3dd7-40b1-b5f4-708da72a4f67/download/tr161-post-tender-reports_v11ext.csv) |
| Post Tender Report TR162 JUNE 2023 CSV EXT | `ffr_post_tender_reports_csv_ext` | 194 | 2023-06-15T10:51:25Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/fd57201c-24f6-4d42-8be2-177dd4b36229/download/tr162-post-tender-reports_v11ext.csv) |
| Post Tender Report TR163 July 2023 CSV EXT | `ffr_post_tender_reports_csv_ext` | 189 | 2023-07-18T09:12:57Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/fbb1ce86-b2f7-405d-94ac-6cef6f14cceb/download/tr163-post-tender-reports_v11ext.csv) |
| Post Tender Report TR164 August 2023 CSV EXT | `ffr_post_tender_reports_csv_ext` | 187 | 2023-08-11T14:16:07Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/2bfa2ab3-7f4e-44d7-a9ab-7342c4b9cd34/download/tr164-post-tender-reports_v11ext.csv) |
| Post Tender Report TR165 September 2023 CSV EXT | `ffr_post_tender_reports_csv_ext` | 179 | 2023-09-18T08:43:37Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/bec39c50-563c-4ed6-8100-8b519dcbf1ef/download/tr165-post-tender-reports_v11ext.csv) |
| Post Tender Report TR166 October 2023 CSV EXT | `ffr_post_tender_reports_csv_ext` | 149 | 2023-10-16T10:33:04Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/59dfabd4-a395-4ddc-a261-2f546a8a3b52/download/tr166-post-tender-reports_v11ext.csv) |
| Post Tender Report TR141 September 2021 CSV-  EXT | `ffr_post_tender_reports_csv_ext` | 94 | 2026-05-29T12:28:29Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/5e0afd6e-ab83-480a-938b-e0da0223fcbc/download/tr141-post-tender-reports_v1-1.csv) |
| Post Tender Report TR147 March 2022 CSV EXT | held | — | 2022-03-16T16:39:04.706143 (catalogue snapshot) | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/c99081fb-0211-4a1a-9eed-53497f64a6ea/download/tr147-post-tender-reports-ext.csv) |
| Post Tender Report TR154 October 2022 CSV- EXT | held | — | 2022-10-24T12:46:53.505500 (catalogue snapshot) | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/7e48c1ce-b4cf-43fa-afe9-4e6730474944/download/tr154-post-tender-reports_v11ext.csv) |

There is no resource classified as documentation (`DOC`) at resource level in this package. The one `DOC` entry is a child sheet (`Sheet1`, empty) inside the TR121 workbook, whose tender sheet `TR121 ` is loaded; it is not a separately downloadable document. The CKAN package notes and the per-column dictionary (field info) are the only vendor documentation captured.

## Workbook resources (`ffr_post_tender_reports_workbook`)

The 61 workbook uploads, in tender-round order (the two editions of TR127 and of TR136 are adjacent). `Rows` is the silver row count (59 resources, **10,094 rows** in total, the activation receipt figure). `Published at` is the CKAN `last_modified` of the captured file, which is the vintage clock `available_at`. The `Format` column is the catalogue label; the file extension in the link shows how NESO named the upload, and neither says reliably whether the body holds macros. For the two held resources nothing was transformed, so there is no row count or vintage value.

| Resource | Format (catalogue) | Sheet read | Rows | Published at (UTC) | File |
|---|---|---|---|---|---|
| Post Tender Report - TR108 Dec-18 | XLSX | `Sheet1` | 422 | 2019-12-03T20:26:08Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/31854ad2-0e98-48ab-8893-dc9b9d473091/download/post-tender-report-tr108-dec-18.xlsx) |
| Post Tender Report - TR109 Jan-19 | XLSX | `Sheet1` | 71 | 2019-12-03T20:25:39Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/27ad6287-1d56-493f-a45f-a6707dc02e14/download/post-tender-report-tr109-jan-19.xlsx) |
| Post Tender Report - TR110 Feb-19 | XLSX | `Sheet1` | 90 | 2019-12-03T20:25:04Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/50488f63-b71b-4647-b2d9-95efbddddf17/download/post-tender-report-tr110-feb-19.xlsx) |
| Post Tender Report - TR111 Mar-19 | XLSX | `Sheet1` | 71 | 2019-12-03T20:24:40Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/d16afe87-cce1-43f2-a36b-d7707ae648d7/download/post-tender-report-tr111-mar-19.xlsx) |
| Post Tender Report - TR112 Apr-19 | XLSX | `Sheet1` | 91 | 2019-12-03T20:24:16Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/dbaa2bb4-ab77-4297-90f2-a7f27e96f7fb/download/post-tender-report-tr112-apr-19.xlsx) |
| Post Tender Report - TR113 May-19 | XLSX | `Sheet1` | 91 | 2019-12-03T20:23:53Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/aa3c7d58-9ed5-460a-bcba-415567abf9fb/download/post-tender-report-tr113-may-19.xlsx) |
| Post Tender Report - TR114 Jun-19 | XLSX | `Sheet1` | 105 | 2019-12-03T20:23:30Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/93802a8f-19ee-4c6b-9fe4-3783085eb0f9/download/post-tender-report-tr114-jun-19.xlsx) |
| Post Tender Report - TR115 Jul-19 | XLSX | `TR115 ` | 107 | 2019-12-03T20:23:09Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/1c1c7788-a0c0-40c9-97fc-03be099995e5/download/post-tender-report-tr115-jul-19.xlsx) |
| Post Tender Report - TR116 Aug-19 | XLSX | `Sheet1` | 109 | 2019-12-03T20:22:46Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/1eb0314b-54dc-45f4-80f7-f32e7edda972/download/post-tender-report-tr116-aug-19.xlsx) |
| Post Tender Report - TR117 Sep-19 | XLSX | `TR117` | 128 | 2019-12-03T20:22:17Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/8c1dc03e-1463-4a52-94d9-b659ff2127c5/download/post-tender-report-tr117-sep-19.xlsx) |
| Post Tender Report - TR118 Oct-19 | XLSX | `Sheet1` | 121 | 2019-12-03T20:21:56Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/d397ffa6-2b7c-4b8f-8cc1-36b267ea6ac1/download/post-tender-report-tr118-oct-19.xlsx) |
| Post Tender Report - TR119 Nov-19 | XLSX | `TR119` | 108 | 2019-12-03T20:21:35Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/0544683b-0d5e-41a3-ba42-270b2d689fdf/download/post-tender-report-tr119-nov-19.xlsx) |
| Post Tender Report - TR120 Dec-19 | XLSX | `TR120` | 115 | 2020-01-06T09:12:18Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/653110b8-4311-4489-81d3-dd6c01043b4e/download/post-tender-report-tr120-dec-19.xlsx) |
| Post Tender Report - TR121 Jan-20 | XLSX | `TR121 ` | 115 | 2020-01-20T08:22:50Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/e692dc29-e94c-4be7-8067-4fc6af8bab22/download/post-tender-report-tr121-jan-20.xlsx) |
| Post Tender Report - TR122 Feb-20 | XLSX | `TR122` | 159 | 2020-02-14T14:42:28Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/bf1bbc9a-ace7-4ec0-a0d5-aa6313fade21/download/post-tender-report-tr122-feb-20.xlsx) |
| Post Tender Report- TR124 Apr- 20 | XLSX | `TR124` | 161 | 2020-05-20T14:33:29Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/93dac57b-a373-4fed-ab9f-338336a685e6/download/post-tender-report-tr124-april-2020-ext.xlsx) |
| Post Tender Report - TR126 June 2020 | XLSX | `TR126` | 182 | 2020-07-06T13:28:44Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/9137187c-8626-4d28-a538-3dd9eb395644/download/post-tender-report-tr126-jun-2020-ext-amended.xlsx) |
| Post Tender Report - TR127 July 2020 | XLSX | `TR127` | 175 | 2020-07-16T13:27:24Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/68529290-7992-4891-90bc-68fa9bcb5aeb/download/post-tender-report-tr127-july-2020-ext.xlsx) |
| Post Tender Report - TR127 July 2020 - Amended | XLSX | `TR127` | 175 | 2020-07-30T13:26:29Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/16773f53-c0f9-4b8c-aaee-ad819e93d405/download/post-tender-report-tr127-july-2020-amended-ext.xlsx) |
| Post Tender Report TR128 August 2020 | XLSX | `TR128` | 171 | 2020-08-18T19:03:05Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/6e6b47ea-afae-4366-bdce-d961bdcb21fe/download/post-tender-report-tr128-august-2020-ext.xlsx) |
| Post Tender Report TR129 September 2020 | XLSX | `TR129` | 156 | 2020-10-21T07:51:24Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/5a1f039a-c6c8-43a2-9ae4-069a0a0b32b2/download/post-tender-report-tr129-september-2020-ext.xlsm) |
| Post Tender Report TR130 October 2020 | XLSX | `TR130` | 128 | 2020-10-21T07:52:55Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/4b4a2e83-094c-4566-90c1-98366469b504/download/post-tender-report-tr130-october-2020-ext.xlsx) |
| Post Tender Report TR131 November 2020 - EXT | XLSX | `TR131` | 133 | 2020-11-17T13:41:19Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/c325243e-2a5d-4585-9d56-2207d781d7a2/download/post-tender-report-tr131-november-2020-ext.xlsm) |
| Post Tender Report TR132 December 2020 EXT | XLSX | `TR132` | 123 | 2020-12-16T15:58:04Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/ce75bd6e-5c16-41b5-bf7f-ebf3b44508f3/download/post-tender-report-tr132-december-2020-ext..xlsm) |
| Post Tender Report TR133 January 2021 - EXT | XLSX | `TR133` | 114 | 2021-01-19T12:28:18Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/0f72be2e-71d3-4a6e-a19d-c627dd25c3bb/download/post-tender-report-tr133-january-2021-ext..xlsm) |
| Post Tender Report TR134 February 2021- EXT | XLSX | `TR134` | 106 | 2021-02-16T15:23:13Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/36c2cf05-c72b-4d18-91bd-dc2104f6103e/download/post-tender-report-tr134-february-2021-ext..xlsm) |
| Post Tender Report TR135 March 2021- EXT | XLSX | `TR135` | 118 | 2021-04-20T14:41:07Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/eaddd8aa-6cd1-403c-943e-4ffa6ce9ec9b/download/post-tender-report-tr135-march-2021-ext.xlsm) |
| Post Tender Report TR136 April 2021- EXT | XLSX | `TR136` | 132 | 2021-04-20T14:39:58Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/7912d65a-451a-4dea-b8eb-4bc5c7af254b/download/post-tender-report-tr136-april-2021-ext.xlsm) |
| Post Tender Report TR136 April 2021 EXT- Amended | XLSX | `TR136` | 132 | 2021-05-07T10:08:46Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/a85e6149-3893-48f6-953a-0a10e796ce8e/download/post-tender-report-tr136-april-2021-ext-amended.xlsm) |
| Post Tender Report TR137 May 2021 EXT | XLSX | `TR137` | 125 | 2021-05-19T14:28:15Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/6e4f83e8-28d8-42f3-8e95-52928e58fb20/download/post-tender-report-tr137-may-2021-ext.xlsm) |
| Post Tender Report TR138 June 2021 EXT | XLSX | `TR138` | 131 | 2021-06-16T13:55:18Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/bc47f2cb-695e-450e-a800-cad8cfecaaf1/download/post-tender-report-tr138-june-2021-ext.xlsm) |
| Post Tender Report TR139 July 2021 EXT | XLSX | `TR139` | 97 | 2021-07-16T13:48:30Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/a5b3f43d-35f9-4384-b35c-a2d78d7bb4ba/download/post-tender-report-tr139-july-2021-ext.xlsm) |
| Post Tender Report TR140 August 2021 EXT | XLSX | `TR140` | 90 | 2021-08-17T14:47:47Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/d96d15ed-8705-42f5-a65d-f63468516e08/download/post-tender-report-tr140-august-2021-ext.xlsm) |
| Post Tender Report TR141 September 2021 EXT | XLSX | `TR141` | 94 | 2021-09-16T13:08:27Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/4df9b9b7-db93-4c98-93e0-1b57b8c256c7/download/post-tender-report-tr141-september-2021-ext.xlsm) |
| Post Tender Report TR142 October 2021 EXT xlms | XLSX | `TR142` | 164 | 2021-10-18T16:12:04Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/89134181-f1f0-4605-894f-859e1d19eb7b/download/post-tender-report-tr142-october-2021-ext.xlsm) |
| Post Tender Report TR143 November 2021.xlms. EXT | XLSM | `TR143 ` | 201 | 2021-11-16T16:32:58Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/a2888ffb-f2bc-455c-8d2c-8e70b194914e/download/post-tender-report-tr143-november-2021-ext-v1.1.xlsm) |
| Post Tender Report TR144 December 2021 EXT | XLSX | `TR144` | 240 | 2021-12-16T16:32:53Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/6cd10acf-2524-4c3f-8509-f657eeae73e5/download/post-tender-report-tr144-december-2021-ext.xlsm) |
| Post Tender Report TR145 January 2022 EXT | XLSM | `TR145` | 229 | 2022-01-19T16:23:31Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/29014d2b-7ae3-4689-8dba-9e3a181b26e9/download/post-tender-report-tr145-january-2022-ext.xlsm) |
| Post Tender Report TR146 February 2022 EXT | XLSM | `TR146` | 196 | 2022-02-16T15:10:50Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/85ec5689-e1ab-4d12-8268-a84bd579beac/download/post-tender-report-tr146-february-2022-ext.xlsm) |
| Post Tender Report TR147 March 2022 EXT | XLSM | `TR147` | 212 | 2022-03-16T16:42:19Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/8ec9b10f-01e2-44ca-a3cb-2e9557a46410/download/post-tender-report-tr147-march-2022-ext.xlsm) |
| Post Tender Report TR148 April 2022 EXT | XLSM | `TR148` | 203 | 2022-04-20T13:03:16Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/c72a9877-e718-4b98-a942-ec61d3891e05/download/post-tender-report-tr148-april-2022-ext.xlsm) |
| Post Tender Report TR149 May 2022 EXT | XLSM | `TR149` | 227 | 2022-05-18T12:37:47Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/46313224-61d2-4c48-b59c-5973328ad5c3/download/post-tender-report-tr149-may-2022-ext.xlsm) |
| Post Tender Report TR150 June 2022 EXT | XLSX | `TR150` | 259 | 2022-06-20T15:27:12Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/e5c028dd-265e-4684-a419-cee906617e11/download/post-tender-report-tr150-june-2022-ext.xlsm) |
| Post Tender Report TR151 July 2022 EXT | XLSM | `TR151` | 252 | 2022-07-18T14:53:32Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/0ad0f7f5-314e-4d7a-b6df-84a7b77c9908/download/post-tender-report-tr151-july-2022-ext.xlsm) |
| Post Tender Report TR152 August 2022 EXT | XLSM | `TR152` | 266 | 2022-08-19T15:48:04Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/08ac3a6c-6f9e-4b6b-8389-38af6c1c9a46/download/post-tender-report-tr152-august-2022-v2-ext.xlsm) |
| Post Tender Report TR153 September 2022 EXT | XLSM | `TR153` | 272 | 2022-09-16T14:23:10Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/854e29a9-3b94-41e0-8bbc-24ec270ae6fd/download/post-tender-report-tr153-september-2022-ext.xlsm) |
| Post Tender Report TR154 October 2022 EXT | XLSM | `TR154` | 262 | 2022-10-18T15:30:48Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/e4da45cc-fb8f-41e4-81f8-e61b6f413ae6/download/post-tender-report-tr154-october-2022-ext.xlsm) |
| Post Tender Report TR155 November 2022-  EXT | XLSM | `TR155` | 281 | 2022-11-16T15:55:05Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/244c9023-a68d-4a28-a4f3-7f492905ad99/download/post-tender-report-tr155-november-2022-ext.xlsm) |
| Post Tender Report TR156 December 2022- EXT | XLSM | `TR156` | 269 | 2022-12-16T15:12:54Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/1d0def5b-18b4-4184-9896-db328a443df2/download/post-tender-report-tr156-december-2022-ext.xlsm) |
| Post Tender Report TR157 January 2023 EXT | XLSM | `TR157` | 291 | 2023-01-18T16:01:14Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/8540c6b2-75e6-4e16-8113-0723a4a642b5/download/post-tender-report-tr157-january-2023-ext.xlsm) |
| Post Tender Report TR158 February 2023 EXT | XLSM | `TR158` | 310 | 2023-02-15T14:34:05Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/987467c5-a5fe-4d4c-a2c6-7e59a458e7af/download/post-tender-report-tr158-february-2023-ext.xlsm) |
| Post Tender Report TR159 March 2023 EXT | XLSM | `TR159` | 206 | 2023-03-16T14:18:18Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/ed783d99-dc3c-4deb-a847-c9d96295dcd4/download/post-tender-report-tr159-march-2023-ext.xlsm) |
| Post Tender Report TR160 April 2023 EXT | XLSM | `TR160` | 203 | 2023-04-19T11:31:58Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/5aa12080-f439-42ab-a806-cf2781750a29/download/post-tender-report-tr160-april-2023-ext.xlsm) |
| Post Tender Report TR161 May 2023 EXT | XLSM | `TR161` | 209 | 2023-05-17T13:48:43Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/634c7528-e461-49cf-ba7b-0fe20702717f/download/post-tender-report-tr161-may-2023-ext.xlsm) |
| Post Tender Report TR162 June 2023  EXT | XLSM | `TR162` | 194 | 2023-06-15T10:50:00Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/9a707d8f-36dc-4caf-9dfb-5c620e729d75/download/post-tender-report-tr162-june-2023-ext.xlsm) |
| Post Tender Report TR163 July 2023 EXT | XLSM | `TR163` | 188 | 2023-07-18T09:11:17Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/c3526774-2055-4fe9-b657-e829c9d65939/download/post-tender-report-tr163-july-2023-ext.xlsm) |
| Post Tender Report TR164 August 2023 EXT | XLSM | `TR164` | 186 | 2023-08-11T14:18:08Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/152ba991-4299-4801-9100-a80d7a0a079a/download/post-tender-report-tr164-august-2023-ext.xlsm) |
| Post Tender Report TR165 September 2023 EXT | XLSM | `TR165` | 179 | 2023-09-18T08:45:09Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/2e561c2b-0d70-44e7-ac0b-c99b3fe6ccdb/download/post-tender-report-tr165-september-2023-ext.xlsm) |
| Post Tender Report TR166 October 2023 EXT | XLSM | `TR166` | 149 | 2023-10-16T10:35:19Z | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/8bb5bf74-8f5e-44c7-a231-42d1323bfa73/download/post-tender-report-tr166-october-2023-ext.xlsm) |
| Post Tender Report - TR123 Mar-20 | XLSX | `TR123` | held | — | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/2e49daa5-90eb-4157-bcef-6fcf29e75085/download/ffr-post-tender-report-tr123-march-2020-ext.xlsx) |
| Post Tender Report- TR125 May 2020- EXT | XLSX | `TR125` | held | — | [download](https://api.neso.energy/dataset/1162a519-b66d-48f6-96ae-1a69ff17951f/resource/4bea886e-3aad-4a8d-9bec-1c8e770739b0/download/post-tender-report-tr125-may-2020-ext.xlsm) |

## Clocks

The family has two time axes and they do not coincide.

| Clock | Value in this family | Source |
|---|---|---|
| Vintage: `published_at` = `available_at` (CSV table) | CKAN `last_modified` of the captured file (ADR-030). For the 26 transformed CSV resources it ranges from 2021-07-22 to 2026-05-29. | `vintage: ckan_last_modified`; checked in silver that `available_at` equals `published_at` on every row |
| Vintage: `published_at` = `available_at` (workbook table) | CKAN `last_modified` of the captured file (ADR-030). For the 59 loaded workbook resources it ranges from 2019-12-03 to 2023-10-16. | `vintage: ckan_last_modified`; checked in silver that `available_at` equals `published_at` on every row, with one value per resource |
| Event time: `timestamp_utc` (both tables) | **`none`** (temporal recipe none): `timestamp_utc` is the **capture time** (bronze capture, 2026-10-08), not the service period. `event_time` equals `timestamp_utc` on every row. | `temporal: none` |

Consequences:

- Do not read `timestamp_utc` as the tender date, the decision date or the service date. The service dates are the raw strings `start_date` and `end_date`; the tender round is encoded in the resource and in the first three digits of `tender_ref`.
- Point-in-time queries use `available_at` (`WHERE available_at <= :as_of`). NESO publishes no issue-time column, and the monthly publication guidance does not establish the original availability of any later amendment, so a re-upload shows up with a later `last_modified`. There is one capture per resource in the current bronze, so amendment history within a resource cannot be observed.
- No issue clock exists (`issue: none`).
- The two editions of a tender report (TR127 and TR136 in the workbook table) are separated only by `available_at`; see Known issues.

## Units

Units come only from the vendor per-column dictionary (field info, snapshot `20261008T114228Z`), as cited in the batch evidence file (`K-AS-5-FACTS.md`, g4). Column names are not used to infer units.

| Group | Silver columns | Unit | Note |
|---|---|---|---|
| Availability fee | `availability_fee` | £/h | float64 |
| Nomination fee | `nomination_fee` | £/h | kept as string (see Sentinels) |
| Window initiation fee | `window_initiation_fee` | £/window | kept as string (see Sentinels) |
| Daily frame durations (Mon-Fri, Saturday, Sunday/bank holidays) | `frame_duration_mon_fri`, `frame_duration_sat`, `frame_duration_sun_bh` | hours | float64. The Saturday dictionary entry has a blank unit field but its description and comment say hours; see the Sunday conflict below |
| Frequency response volumes | `primary_response_0_2hz`, `primary_response_0_5hz`, `primary_response_0_8hz`, `secondary_response_0_2hz`, `secondary_response_0_5hz`, `high_frequency_response_0_2hz`, `high_frequency_response_0_5hz` | MW | float64, fractional MW permitted |
| Part-load and limit points | `max_part_load_point`, `min_part_load_point`, `min_mel`, `max_sel` | MW | string |
| Automatic response energy | `auto_response_10s`, `auto_response_30s` | MW | string (the 30 s column carries prose in one resource) |
| Window clock labels | `frame_from_*`, `frame_to_*` | none | raw clock labels such as `300` or `2300`; the dictionary says they must be consistent with EFA block boundaries; not a physical quantity |
| Tender reference, status, codes, names, units, comments, postcode | various | none | strings |

**Sunday/bank-holiday duration conflict.** For `Tendered Frames per Service Day - Duration (Sunday/Bank Hol)` the vendor dictionary's unit field says `£` while its title, description and comment say hours. The silver column is treated as hours (a duration), not a payment. This is a vendor defect that does not hold the family. TODO: verify with NESO which is intended; a vendor correction would settle it. The generated schema tables above show the vendor unit field verbatim, so they display `£` for this column.

**Workbook table.** The workbook columns reuse the CSV table's silver names, dtypes and units (a seat ruling, AS-5c): the workbook headings carry the same unit text for fees (`£/h`, `£/window`), frequency-response and limit points (`MW`) and the three frame durations (`Duration (h)`, hours, including the Sunday/bank-holiday one). No heading is workbook-only, so no workbook column needs its own unit `TODO`. The Sunday/bank-holiday dictionary conflict above applies to the dictionary, not to the workbook heading.

## Time and clock semantics

- `start_date` and `end_date` are the service dates (first and final date FFR would be provided if accepted), **not** issue or publication dates. The dictionary's example format is `dd/mm/yyyy`. In the captured bodies they are a mixture of slash dates and Excel serial integers, and in several resources the mixture is within one file, so they are stored as raw strings for the whole record. Do not parse only the slash-date subset. Admitted resources with serials or a mixture: TR144, TR145, TR152, TR153, TR157, TR158, TR161 (held TR154 also contains serials).
- The `From` and `To` window columns are recurring daily availability clock labels. Their export clock (local or UTC) and endpoint convention are not documented. TODO: verify the clock and whether `To` is inclusive. They are raw strings and are never composed into a UTC timestamp.
- `tendered_period` is a text label of the form `dd.mm.yy - dd.mm.yy (n months)`.
- No settlement-period or gas-day semantics apply to this family.

**Workbook dates are Excel 1900-system serial numbers.** In the 59 loaded sheets the `Start Date` and `End Date` cells are numeric serials that are date-styled in every loaded sheet except TR121, where they are `General` format (230 of the 20,188 cells, all on the TR121 sheet); the 12 TR164 cells are text. Of the 20,188 cells, 19,846 carry the built-in date format 14, 76 the custom format `d/m/yyyy` and 24 the custom format `dd/mm/yyyy;@`. Every loaded workbook uses the 1900 date system (none uses the 1904 system). `ffr_post_tender_reports_workbook` therefore stores `start_date` and `end_date` as the stored serial text, with no conversion and no `date` column (I-4 raw route, AS-5c plan K-2): 10,091 of 10,094 `start_date` cells and 10,085 of 10,094 `end_date` cells are all-digit serials. The remaining 12 cells are **text cells in the TR164 workbook** (`dd/mm/yyyy` text, 3 in `start_date` and 9 in `end_date`, on 9 rows; they carry date format 14 but hold text), so a reader must handle both spellings per resource and must not parse only one. The recurring `From`/`To` window labels are raw strings here too (the Mon-Fri `From` heading is spelled `From`, `L`, `l` or `,` across header epochs; each spelling is its own epoch and maps to the same silver column). `timestamp_utc` is the capture time, as for the CSV table.

## Sentinels and non-numeric tokens

Policy: zero is a value; no token is converted to null without vendor evidence (batch evidence g5).

- `NA`, `N/A` and `n/a` all appear in rejection-code fields (alongside numeric-looking codes such as `1.2`) and the exact token `N/A` in postcode fields (242 rows; no other case or spacing variant): kept byte-equal as strings.
- `nomination_fee` holds null (blank cells), a literal `0`, `-` and a single-space string (9 rows); `window_initiation_fee` holds null (blank cells), a literal `0` and `-`. Both are strings because there is no vendor evidence that `-` or the single space means null, and zero is a value. `availability_fee` has no nulls or tokens and is float64.
- `max_part_load_point`, `min_part_load_point`, `min_mel` and `max_sel` hold only `-` where published, so they are strings.
- `auto_response_30s` carries prose in the TR139 resource (a text qualifier instead of a number) and is kept as a string; no value is fabricated or nulled. `auto_response_10s` is also a string: TR144 and TR145 publish a single-space cell and TR146 one `1`, which a strict numeric cast rejects (ruling 773: string, no trim, no hold).
- Fractional response volumes are real, so the response columns are float64 and are never cast to integer.
- TR139 predates the postcode column (header epoch 2): its `post_code` is null for every row of that resource.
- Embedded newlines occur in postcode cells and in some header cells; they are kept (the reader cuts on CSV record boundaries, not raw lines).

**Workbook table** (same policy; counts are silver rows over the 59 loaded resources):

- `rejection_codes` has no nulls and holds `NA` (4,042 rows), `N/A` (772) and `n/a` (803) beside numeric-looking codes, all kept byte-equal as strings. `post_code` holds the exact token `N/A` on 263 rows.
- `nomination_fee` is null on 8,750 rows, `-` on 586 and a single space on 9; `window_initiation_fee` is null on 8,977 rows and `-` on 818. They stay strings: there is no vendor evidence that `-` or whitespace means null, and a zero is a value. `availability_fee` has no nulls and no tokens and is float64.
- `max_part_load_point`, `min_part_load_point`, `min_mel` and `max_sel` hold `-` on 156 rows each and whitespace-only cells (a single space, plus one double-space cell in `min_mel`) on 11 to 13 rows; `auto_response_10s` holds `-` on 103 rows and a single space on 3; `auto_response_30s` holds non-numeric text on 109 rows. All are kept as strings and none is nulled.
- Whitespace-only cells occur only in string columns. Fractional response volumes are real and the response columns are float64.
- `post_code` is null on every row of the 32 resources whose workbook layout (A:AP, 42 columns) has no postcode column.
- The one cast failure found across the 61 workbooks is a text cell in a float64 column of the held TR123 workbook (see Held outputs); a single bad numeric cell fails the whole capture, so that workbook is held, never partially loaded.

## Held outputs

Four resources are held and **not transformed**: two CSV resources (hold unit v0.22-K-AS-5a) and two workbook resources (hold unit v0.22-K-AS-5c). Both tables are eligible and carry no table-level hold. No data values from the held resources appear on this page; row counts and schema only.

| Resource | Id | Bronze rows | Hold question (E-SEM) |
|---|---|---|---|
| Post Tender Report TR147 March 2022 CSV EXT | `c99081fb-0211-4a1a-9eed-53497f64a6ea` | 212 | FFR-TR147-THOUSANDS-SEPARATOR: one availability fee is written with an internal thousands separator, which fails the strict float64 cast and which the lexical trim does not remove. Re-disposition needs a declared lexical-number mechanism or a corrected NESO upload (a new `last_modified`). |
| Post Tender Report TR154 October 2022 CSV EXT | `7e48c1ce-b4cf-43fa-afe9-4e6730474944` | 272 | FFR-TR154-ORPHAN-ROWS: 10 nonblank rows carry no Tender Ref, so the `(resource_id, tender_ref)` key could not hold every row and a non-nullable key would silently exclude them. Are they continuations of another tender, or a publication defect NESO can correct? |
| Post Tender Report - TR123 Mar-20 (workbook) | `2e49daa5-90eb-4157-bcef-6fcf29e75085` | 175 (tender block) | FFR-TR123-COMMA-MW: one High Frequency Response (max.) @ 0.2Hz (MW) cell (AH85, one tender row) holds text written with a decimal comma instead of a number, which fails the record's strict float64 type for `high_frequency_response_0_2hz`; is it a value written with a decimal comma, and can NESO correct the upload? Re-disposition needs a declared lexical-number mechanism or a corrected upload (a new `last_modified`). |
| Post Tender Report- TR125 May 2020- EXT (workbook) | `4bea886e-3aad-4a8d-9bec-1c8e770739b0` | 180 (tender block) | FFR-TR125-UNHEADED-AQ: the workbook has text in column AQ for 15 tender rows (63-68, 125-127, 133, 154-156, 170-171) under a blank composite header (AQ2:AQ4), so the column has no heading to name it from; what does NESO call this column? Re-disposition needs a vendor heading or an approved positional raw-column contract. |

A single bad numeric cell fails the whole capture, so TR123 is held rather than partially loaded, and the held TR125 workbook is the only one of the 61 with a populated column that has no heading. Two is below the scope stop of six unreadable workbooks. The other 59 workbooks are loaded as `SILVER`.

**No workbook is `COVERED`.** A workbook can be dropped as covered by its CSV only when the equivalence harness passes every leg (clean typing, equal projections, complete row multisets, vintage). For the 16 workbooks whose CSV passes the vintage screen (TR140, TR142, TR144, TR145, TR147, TR148, TR149, TR152, TR156, TR157, TR158, TR159, TR161, TR164, TR165, TR166) every nomination fails the row-multiset leg: the two tables hold different `resource_id`s and the workbook keeps the stored tender-reference text (floating-point tails included). TR147's CSV is itself held. The 33 workbooks with no CSV (TR108-TR138) and the 12 workbooks that fail the vintage leg were never candidates. Every workbook is therefore `SILVER`, and **the workbook table and the CSV table overlap on TR139-TR166 - never add them.**

## Known issues and gotchas

- **Tender `162.198` overlap (adjudicated, not deduplicated).** The same tender reference appears in TR162, TR163 and TR164, identical in every business column, in three consecutive monthly resources (published 2023-06-15, 2023-07-18 and 2023-08-11). At AS-5a time the activation reconcile (`--all --cutoff 2026-10-13`) exited 1 with 3 `overlap` gaps on this family, all for tender `162.198`. The three gaps were adjudicated under ADR-040 in AS-5b (PR #119; rulings 789 and 792), and the reconcile now exits 0 with 0 gaps on this family (adjudicated 55, +3). Silver still keeps all three rows because `resource_id` is part of the key `(resource_id, tender_ref)`; nothing is deduplicated and no amendment equivalence is assumed. Do not sum across resources by tender reference.
- **The workbook table and the CSV table overlap on TR139-TR166 - never add them.** The CSV table (5,457 rows, TR139-TR166 minus the held TR147 and TR154) and the workbook table (10,094 rows, TR108-TR166 minus the held TR123 and TR125) are two readings of the same published tender rounds for TR139-TR166 (28 workbook resources there, including TR147 and TR154, whose CSVs are held). They are separate tables because they are different uploads with different `resource_id`s and different stored tender-reference text, and no equivalence has been proven (see Held outputs). Never add rows from the two tables together; for TR108-TR138 only the workbook table exists. Do not join them on `tender_ref` text: the workbook keeps the worksheet's stored text, and 10,032 of its 10,094 tender references carry a floating-point serialization tail (for example `122.16500000000073`) that is deliberately not rounded to the CSV spelling.
- **TR127 and TR136 each have two editions (reconcile gaps, unadjudicated).** The activation reconcile (`--all --cutoff 2026-10-13`, RESULTS AS-5c) exited 1 with 4 `overlap` gaps, all on `ffr_post_tender_reports_workbook`, all from two pairs of workbooks that publish the same tender report twice: TR127 (`68529290-7992-4891-90bc-68fa9bcb5aeb`, available 2020-07-16, and `16773f53-c0f9-4b8c-aaee-ad819e93d405`, available 2020-07-30; 175 tender references) and TR136 (`7912d65a-451a-4dea-b8eb-4bc5c7af254b`, available 2021-04-20, and `a85e6149-3893-48f6-953a-0a10e796ce8e`, available 2021-05-07; 132 tender references). The editions are not identical: in each pair the later edition changes `status` and `rejection_codes` on 9 rows. Silver keeps **both** editions (`resource_id` is part of the key) and `available_at` separates them, so a point-in-time query `WHERE available_at <= :as_of` sees the earlier edition until the later one is published. The catalogue titles the later upload of each pair "Amended", but NESO states no precedence rule. TODO: verify that the later edition supersedes the earlier. Until then neither edition is dropped, deduplicated or preferred, and tender references must not be summed across a pair (ruling 798; ADR-040 adjudication entries are folded into the DFS spec).
- **Workbook layout.** Each workbook carries merged composite headers (three stacked rows starting on row 2, 3, 4 or 6), example rows before the tender block and a block end that differs per workbook; the record's per-resource block map loads the tender block only. The captured bodies are 22 plain `.xlsx` and 39 macro-enabled `.xlsm` (the catalogue labels are the reverse), and macros are never executed. The sheet names are kept exactly, including the trailing space in `TR121 `, `TR115 ` and `TR143 `.
- **Row counts.** 5,457 CSV silver rows in 26 resources (TR144 240; the 23 admitted `_csv_ext` resources 4,852; TR142 164; TR143 201). The reader removes and counts 145 wholly blank rows from nine `_csv_ext` resources, so bronze row totals exceed silver for those.
- **Mixed date spellings** in `start_date`/`end_date` (see Time and clock semantics). A typed date column is not offered until a faithful Excel-serial contract exists.
- **EXT suffix unexplained.** NESO's description and dictionaries do not expand `EXT` or establish a difference between the `CSV`, `CSV EXT` and `EXT` naming; no business dimension is derived from it. TODO: verify with NESO what `EXT` means.
- **Two header epochs.** Epoch 1 has 43 columns including `Post code`; epoch 2 (TR139) has 42 columns without it. Columns map by source name.
- **Dictionary quirks.** `Tender Ref` is typed numeric in the vendor dictionary but is an identifier in the data (example `122.001`) and is stored as a string, never cast.
- **Cadence.** The vendor update frequency is `Not Active` and the registry refresh is frozen; the latest captured report is TR166 (October 2023). TODO: verify whether NESO has stopped publishing these reports.
- **No gold or models consumer.** No gold view or models feed reads this family at present.

## Implementation delta

- The generated family listing shows `ingest-only: no silver yet` for `ffr_post_tender_reports_csv` and `ffr_post_tender_reports_ext`; in the shipped design they are siblings of `ffr_post_tender_reports_csv_ext` and their rows live in its silver, not in separate silver tables.
- The dispositions of TR144, TR142 and TR143 changed from their own family key to `SILVER` key `ffr_post_tender_reports_csv_ext` (v0.22-K-AS-5a). The upstream research proposal to type dates on clean resources (`date_sp1(start_date)`) was set aside in favour of raw strings and temporal `none` for the whole record (ruling 766 call 2), because one column has one dtype across all resources.
- **Workbooks (v0.22-K-AS-5c).** The 61 workbook resources and their sheet children changed from `HOLD` (data container, records pending) to `SILVER` key `ffr_post_tender_reports_workbook` for 59 resources and `HOLD` for TR123 and TR125; TR121's empty `Sheet1` stays `DOC`. The registry's proposed workbook family name was kept. The reader needed work beyond ADR-037's single-header `xlsx` spec (a per-resource block map keyed by `resource_id`, composite header labels, stored-text strings), recorded as ADR-037 amendment 1.
- **Set aside from the spec.** The spec's `date_sp1(start_date)` temporal for the workbook family was not used: workbook date cells are numeric serials (General format on the TR121 sheet, date-styled elsewhere) and TR164 holds 12 text cells, so no single declared date rule types every resource, and the record uses temporal `none` with raw strings (the same as the CSV table). The research expectation of 10,449 workbook rows (61 workbooks) became 10,094 after the TR123 (175 rows) and TR125 (180 rows) holds.
- **No COVERED grant.** The registry carries no `COVERED` workbook; see Held outputs.

## Cadence

- Registry refresh: frozen
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Not Active

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

## Holds

- none at table level. The four resource-level holds (CSV TR147 and TR154; workbook TR123 and TR125) are described under "Held outputs" and in the disposition tables above, each with its question for NESO (E-SEM).
- Open `TODO: verify` items: whether the later edition of TR127 and TR136 supersedes the earlier (NESO states no precedence); the export clock and `To` endpoint convention of the window labels; the meaning of `EXT`; whether NESO has stopped publishing these reports.
