---
source: "neso_data_portal"
package: "brit-ned"
dataset_key: "brit_ned"
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-09
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# BritNed - NESO's Intraday Trading Limit

This package holds the restrictions NESO applies to **BritNed**, the GB–Netherlands
interconnector. Each row is one hourly operational period with two directional maximums in
MW: the most power that may flow **to GB** (import) and **from GB** (export), plus a reason
text. The package notes say these are "the values submitted by NESO to the interconnector
capacity calculation processes which restrict the maximum GB import and export interconnector
flows", submitted "in MW per hourly time period". They are **limits NESO submits, not measured
flows and not the final capacity**. Final capacity is calculated from NESO's values, the
connected system operator's values and the interconnector's own capability, so it "may be
lower than the NESO values shown here". The final figures are on the interconnector's trading
facilitator's website. Values are published only where NESO applied a restriction: "If there
are no values, NESO has not applied a restriction." Resource descriptions call them
"Intraday Transfer Limit restrictions submitted to Day-ahead and Intraday auctions", and the
package title says "Intraday Trading Limit"; both expand ITL. Use this package to see when and
why the GB side constrained BritNed, for example as a feature for GB–Netherlands flow or price
models. Measured flows are in the `britned_flow` column of @./historic-demand-data.md. Planned
BritNed flows are in the `britned_temx` / `britned_teol` / `britned_temi` columns of
@./system-operating-plan-sop.md. Those are expected reference-programme flows, not these
directional limits. Sibling packages with the same role: @./nsl.md, @./nemolink.md,
@./eleclink.md, @./viking.md, @./ifa.md, @./ifa2.md. The link list is in
@./interconnector-register.md.

Unlike its IC-1 siblings, BritNed has no datastore dump. It is **187 separate weekly CSV
uploads** (2022-10 to 2026-09), all in one family, `brit_ned`, with five header epochs.
Silver holds **18,817 rows from 185 resources**. Two captures failed and are **not loaded**:
the oldest upload (a key collision, adjudicated) and one upload with invalid UTF-8 bytes
(still an open reconcile gap). Both directional flows are kept as **raw strings**
(`flow_to_gb_mw_raw`, `flow_from_gb_mw_raw`) because some cells carry thousands separators
and decimals. The silver output is **held** (unit E-SEM; see Holds), so this page gives
schema, row counts, clocks and missingness only, never data values or ranges of values.

- Publisher group: Interconnectors
- Registry group: interconnectors · archetype: FC

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| BritNed DA & ID Weekly ITLs 20221012 | CSV | upload | `10432bfd-2102-4eda-8c6d-bed2a4df676b` |
| BritNed DA & ID Weekly ITLs 20221019 | CSV | upload | `c5282013-ee05-4da6-ad46-ff59ff443bfe` |
| BritNed DA & ID Weekly ITLs 20221026 | CSV | upload | `2248834b-c822-494a-8f1c-ee3cf04705c7` |
| BritNed DA & ID Weekly ITLs 20221102 | CSV | upload | `eebd1509-b977-43cb-a37e-71ec597a71f0` |
| BritNed DA & ID Weekly ITLs 20221109 | CSV | upload | `ecda7923-78d7-4865-af9e-0121ebf5c2fb` |
| BritNed DA & ID Weekly ITLs 20221116 | CSV | upload | `2a4bc449-649d-4d28-b41e-616fc9fa9215` |
| BritNed DA & ID Weekly ITLs 20221123 | CSV | upload | `b51a8d55-62ff-4a47-bc14-a238b3048a25` |
| BritNed DA & ID Weekly ITLs 20221130 | CSV | upload | `aea7e92f-1e5a-48fb-9215-6716f4aab4e1` |
| BritNed DA & ID Weekly ITLs 20221207 | CSV | upload | `87ae5355-b450-453a-a8b2-2930cf0f2246` |
| BritNed DA & ID Weekly ITLs 20221214 | CSV | upload | `b9e7f19e-07dc-43af-a67a-68e9588616ee` |
| BritNed DA & ID Weekly ITLs 20221221 | CSV | upload | `171662b8-4ae0-44ea-8ffa-15d64e0f8562` |
| BritNed DA & ID Weekly ITLs 20221228 | CSV | upload | `6245d8d5-74a1-43bd-97b2-95d4b3d391c5` |
| BritNed DA & ID Weekly ITLs 20230104 | CSV | upload | `9206c32f-35cb-447f-aec9-8ebf25a4e704` |
| BritNed DA & ID Weekly ITLs 20230111 | CSV | upload | `ddd2abc9-3ef4-4859-bd28-b434bcc7f6ee` |
| BritNed DA & ID Weekly ITLs 20230118 | CSV | upload | `c6782dcf-1f83-4a21-8b5f-404f787a940d` |
| BritNed DA & ID Weekly ITLs 20230125 | CSV | upload | `8be33510-58f8-4a07-8128-827c6439552a` |
| BritNed DA & ID Weekly ITLs 20230201 | CSV | upload | `c36f5f3d-c396-4c77-91e0-b1b7b40eec3e` |
| BritNed DA & ID Weekly ITLs 20230208 | CSV | upload | `d6f1a8e4-1ea9-423c-a5a6-c20f33c59c06` |
| BritNed DA & ID Weekly ITLs 20230215 | CSV | upload | `885e6cb7-a000-48cc-a4b8-1028f0f4688e` |
| BritNed DA & ID Weekly ITLs 20230222 | CSV | upload | `d2f2f4f1-30cd-4261-8797-cd0391b2543e` |
| BritNed DA & ID Weekly ITLs 20230301 | CSV | upload | `3363713c-bae7-4e79-84e3-45bf48ac6410` |
| BritNed DA & ID Weekly ITLs 20230308 | CSV | upload | `8a53a413-22db-439c-ad64-7673871edce5` |
| BritNed DA & ID Weekly ITLs 20230315 | CSV | upload | `16c97f2d-26ec-47a0-b4fd-f8cc50d67d58` |
| BritNed DA & ID Weekly ITLs 20230322 | CSV | upload | `54df8302-2da2-42f9-b5ba-97b4d9d117d5` |
| BritNed DA & ID Weekly ITLs 20230329 | CSV | upload | `5580a4a3-3ab7-4a55-9c12-95f59668b489` |
| BritNed DA & ID Weekly ITLs 20230405 | CSV | upload | `bdbaada6-309f-4888-8c99-b3f14bd97eb6` |
| BritNed DA & ID Weekly ITLs 20230412 | CSV | upload | `d1355935-d61d-47ff-8d84-04f2fd903acf` |
| BritNed DA & ID Weekly ITLs 20230419 | CSV | upload | `b0738ef5-e0e6-4f93-a303-4b45f08a18ea` |
| BritNed DA & ID Weekly ITLs 20230426 | CSV | upload | `2cd81edd-7d8f-462c-a8e9-14dc8beff357` |
| BritNed DA & ID Weekly ITLs 20230503 | CSV | upload | `333b4f84-e23f-46c5-b47f-b2827d54353f` |
| BritNed DA & ID Weekly ITLs 20230510 | CSV | upload | `bd268477-8923-49fc-9d61-d41c164eb8a0` |
| BritNed DA & ID Weekly ITLs 20230517 | CSV | upload | `212d8723-3741-4aa4-8201-091f3fd90f26` |
| BritNed DA & ID Weekly ITLs 20230524 | CSV | upload | `f8a603c6-24e7-416e-8e71-a02b480e9d08` |
| BritNed DA & ID Weekly ITLs 20230531 | CSV | upload | `8992630e-28b0-430d-930a-c0b80bde2ade` |
| BritNed DA & ID Weekly ITLs 20230607 | CSV | upload | `513ca6a4-a53e-4996-9cff-a20ac8266bb7` |
| BritNed DA & ID Weekly ITLs 20230614 | CSV | upload | `e3559f12-f7a7-4d04-9b7b-3504648f1874` |
| BritNed DA & ID Weekly ITLs 20230621 | CSV | upload | `fb1ced15-5ffe-4d39-9cda-18ebac127399` |
| BritNed DA & ID Weekly ITLs 20230628 | CSV | upload | `4b5666f2-708e-4af2-a1c8-acfd618cbcd4` |
| BritNed DA & ID Weekly ITLs 20230705 | CSV | upload | `6b5a3135-0611-4a9e-946b-f770976eaec7` |
| BritNed DA & ID Weekly ITLs 20230712 | CSV | upload | `e305d44e-c6ae-488c-8828-8f1c887463fa` |
| BritNed DA & ID Weekly ITLs 20230719 | CSV | upload | `788b330c-6165-48d4-a870-8f2b1f55a5fe` |
| BritNed DA & ID Weekly ITLs 20230726 | CSV | upload | `c8063e95-057e-4f87-8aef-8b3bb7566e64` |
| BritNed DA & ID Weekly ITLs 20230802 | CSV | upload | `9ed998b2-0fc8-4cf0-8c4a-77bb7d8dc44f` |
| BritNed DA & ID Weekly ITLs 20230809 | CSV | upload | `669c7c73-6d66-475c-87f5-c7a64014b3bf` |
| BritNed DA & ID Weekly ITLs 20230816 | CSV | upload | `e211afc5-fd21-4091-984b-6da1423842d4` |
| BritNed DA & ID Weekly ITLs 20230823 | CSV | upload | `980dc005-ce8f-49eb-95c6-ec9642d85689` |
| BritNed DA & ID Weekly ITLs 20230830 | CSV | upload | `4f4d9df4-8db6-41e0-bcdc-b1a1f14e27fc` |
| BritNed DA & ID Weekly ITLs 20230906 | CSV | upload | `f328325d-ad71-43b8-993c-220fbe9d38bb` |
| BritNed DA & ID Weekly ITLs 20230913 | CSV | upload | `67fd41a6-3c5a-44e7-934d-83d72d81586f` |
| BritNed DA & ID Weekly ITLs 20230920 | CSV | upload | `1337e91d-d28b-4206-a343-df71a0922e03` |
| BritNed DA & ID Weekly ITLs 20230927 | CSV | upload | `3805fbe4-b62c-4c00-8984-e88a1d9cd37c` |
| BritNed DA & ID Weekly ITLs 20231004 | CSV | upload | `130ec3a1-dd67-4dac-9d00-df7fb5990b05` |
| BritNed DA & ID Weekly ITLs 20231011 | CSV | upload | `f1b7062f-7fb4-4464-aeeb-cc321481cc1e` |
| BritNed DA & ID Weekly ITLs 20231018 | CSV | upload | `374d496a-0312-438a-bfa2-294cf0c7c8de` |
| BritNed DA & ID Weekly ITLs 20231101 | CSV | upload | `abe4cee6-06ce-4557-95bf-f2581778c185` |
| BritNed DA & ID Weekly ITLs 20231108 | CSV | upload | `e06f5075-f129-4a9a-b7d6-529ef3ad3122` |
| BritNed DA & ID Weekly ITLs 20231115 | CSV | upload | `48f556c5-33bb-4ac1-bcf6-24d001aacada` |
| BritNed DA & ID Weekly ITLs 20231122 | CSV | upload | `e0d90a91-5cbe-47a2-9c55-dc8e531b2088` |
| BritNed DA & ID Weekly ITLs 20231129 | CSV | upload | `f8ad75af-f3d1-447c-8c49-e55ee3ec4f93` |
| BritNed DA & ID Weekly ITLs 20231206 | CSV | upload | `30d8a0d9-6ff3-4552-9204-65cd89eb5f65` |
| BritNed DA & ID Weekly ITLs 20231213 | CSV | upload | `08987582-d94e-42e3-8124-54b853c92944` |
| BritNed DA & ID Weekly ITLs 20231220 | CSV | upload | `88998f41-1ce7-4c7c-9781-4a6a0465ab5a` |
| BritNed DA & ID Weekly ITLs 20231227 | CSV | upload | `bcd4c323-d8d7-4c37-bcd4-4651cb062aa1` |
| BritNed DA & ID Weekly ITLs 20240103 | CSV | upload | `1a9363a1-d052-4faa-b69a-d1872c542fc1` |
| BritNed DA & ID Weekly ITLs 20240110 | CSV | upload | `aa06b618-91de-4596-afb6-8bb12137d86c` |
| BritNed DA & ID Weekly ITLs 20240117 | CSV | upload | `aa0477c1-c80c-4208-91fd-5bbc2b4a3d98` |
| BritNed DA & ID Weekly ITLs 20240124 | CSV | upload | `bbd48f9d-8a63-4fbf-9954-5185552b0520` |
| BritNed DA & ID Weekly ITLs 20240131 | CSV | upload | `1e67fdb3-31d4-421d-9fc9-c212b41a8ab0` |
| BritNed DA & ID Weekly ITLs 20240207 | CSV | upload | `8d286f18-3395-45ff-85da-aa7f8f66911c` |
| BritNed DA & ID Weekly ITLs 20240214 | CSV | upload | `b7c0daed-9e35-42ff-87aa-93b1fbd91cd7` |
| BritNed DA & ID Weekly ITLs 20240221 | CSV | upload | `fb901593-b6d6-4215-aabb-b60340cf7b1f` |
| BritNed DA & ID Weekly ITLs 20240228 | CSV | upload | `5b6bae77-3bef-4bec-9a8f-5762d3ad1b9b` |
| BritNed DA & ID Weekly ITLs 20240306 | CSV | upload | `95ebbde2-0f3b-4609-9435-769633c160f6` |
| BritNed DA & ID Weekly ITLs 20240313 | CSV | upload | `6c51f881-6b72-49e4-88ad-2fc4ee97ecb3` |
| BritNed DA & ID Weekly ITLs 20240320 | CSV | upload | `a38ba431-7670-4076-9a5a-82f142f11bdc` |
| BritNed DA & ID Weekly ITLs 20240327 | CSV | upload | `3d152205-5023-4a46-86a8-2b6b07a0fb9b` |
| BritNed DA & ID Weekly ITLs 20240403 | CSV | upload | `870495e8-8f95-4817-8615-c40ca5ebef4e` |
| BritNed DA & ID Weekly ITLs 20240417 | CSV | upload | `8b36e933-304a-44ad-9500-5792819db0d3` |
| BritNed DA & ID Weekly ITLs 20240424 | CSV | upload | `cf3dcf59-ab29-4630-ba6c-6b73dc769a62` |
| BritNed DA & ID Weekly ITLs 20240501 | CSV | upload | `32783822-9e65-4b27-abe5-6350262ec7b2` |
| BritNed DA & ID Weekly ITLs 20240508 | CSV | upload | `eb108e97-2d7b-4d38-8f62-7286cc94b549` |
| BritNed DA & ID Weekly ITLs 20240515 | CSV | upload | `9e78d6a3-1814-4db3-9a27-e604807c92e9` |
| BritNed DA & ID Weekly ITLs 20240522 | CSV | upload | `0c32f871-1a47-4378-a5fd-303d02d890b9` |
| BritNed DA & ID Weekly ITLs 20240529 | CSV | upload | `e7325260-c1f3-468c-96e8-4778893d3ce0` |
| BritNed DA & ID Weekly ITLs 20240605 | CSV | upload | `e946d60d-ae23-4990-a1a8-91cb36ee010a` |
| BritNed DA & ID Weekly ITLs 20240612 | CSV | upload | `3d9036a4-1459-4439-9db1-c4479f97901b` |
| BritNed DA & ID Weekly ITLs 20240619 | CSV | upload | `13a175f1-31ae-4126-b2d4-10ec8bc63a9a` |
| BritNed DA & ID Weekly ITLs 20240626 | CSV | upload | `2af98846-e08a-43e6-b1f0-326e30a4d470` |
| BritNed DA & ID Weekly ITLs 20240807 | CSV | upload | `4de159de-1aee-42e0-b00f-f4d3a128f5b3` |
| BritNed DA & ID Weekly ITLs 20240814 | CSV | upload | `51ff0c0e-c896-4774-aa6f-17b8835fe55f` |
| BritNed DA & ID Weekly ITLs 20240821 | CSV | upload | `5335579f-da7b-474e-b4ec-6fb826af040f` |
| BritNed DA & ID Weekly ITLs 20240828 | CSV | upload | `dc46e9bb-906b-49dc-8ac1-05e77a81ec6a` |
| BritNed DA & ID Weekly ITLs 20240904 | CSV | upload | `0a546c80-0d5b-4217-a2d8-44c3c391bb04` |
| BritNed DA & ID Weekly ITLs 20240911 | CSV | upload | `e89a9770-f1e5-43c2-92f8-3b090c059654` |
| BritNed DA & ID Weekly ITLs 20240918 | CSV | upload | `d7749448-914a-49fb-8641-ef1fde6e60f0` |
| BritNed DA & ID Weekly ITLs 20240925 | CSV | upload | `91df114c-6c0a-4217-a963-8608f0ec619e` |
| BritNed DA & ID Weekly ITLs 20241002 | CSV | upload | `037acebf-f343-4dce-b9da-1a537c15555f` |
| BritNed DA & ID Weekly ITLs 20241009 | CSV | upload | `d721fb6d-616c-4339-83be-dc8eb50ad286` |
| BritNed DA & ID Weekly ITLs 20241016 | CSV | upload | `811bec71-f099-4474-ba5e-2f9932b39cc2` |
| BritNed DA & ID Weekly ITLs 20241023 | CSV | upload | `7ac2608d-9878-46f2-a075-0b40a87e0a63` |
| BritNed DA & ID Weekly ITLs 20241030 | CSV | upload | `7c80487f-dc26-430b-abbf-8c2823ed3dcc` |
| BritNed DA & ID Weekly ITLs 20241106 | CSV | upload | `f3371462-fd35-426e-8652-dd0a5ad69d3b` |
| BritNed DA & ID Weekly ITLs 20241113 | CSV | upload | `105be229-893d-4a04-a3e4-2e97d9d15cd9` |
| BritNed DA & ID Weekly ITLs 20241120 | CSV | upload | `7de2143d-f0b5-4d9e-9a20-588a392ed060` |
| BritNed DA & ID Weekly ITLs 20241127 | CSV | upload | `dbc1d975-607e-4814-b29e-4701d8fa7b7f` |
| BritNed DA & ID Weekly ITLs 20241204 | CSV | upload | `f5b7cc82-86ca-4e21-bc20-6fee78d525df` |
| BritNed DA & ID Weekly ITLs 20250129 | CSV | upload | `3b0da3b7-595f-421b-a77e-92f289599905` |
| BritNed DA & ID Weekly ITLs 20250205 | CSV | upload | `7bbdc91f-9dad-40d9-8d6e-ac7c5ad9d05e` |
| BritNed DA & ID Weekly ITLs 20250212 | CSV | upload | `7f97b143-c569-4132-9ebf-e17b58585f9f` |
| BritNed DA & ID Weekly ITLs 20250219 | CSV | upload | `f44a333a-f36f-4f57-882a-e520fc067ef5` |
| BritNed DA & ID Weekly ITLs 20250226 | CSV | upload | `850f4805-a839-450c-bf2c-1b76090f637c` |
| BritNed DA & ID Weekly ITLs 20250305 | CSV | upload | `d8d0f00c-a9e6-400a-a1a1-0d4acec0cbcc` |
| BritNed DA & ID Weekly ITLs 20250312 | CSV | upload | `5c49a1ab-bed9-43e2-9e69-c9c37a16602b` |
| BritNed DA & ID Weekly ITLs 20250319 | CSV | upload | `25c5f049-8317-4add-b9c9-0e22b749b795` |
| BritNed DA & ID Weekly ITLs 20250326 | CSV | upload | `5909b052-12e3-4385-9c55-da30b3066968` |
| BritNed DA & ID Weekly ITLs 20250407 | CSV | upload | `95f31f4e-7465-4359-b135-bbec23a1cfe1` |
| BritNed DA & ID Weekly ITLs 20250411 | CSV | upload | `8db596d3-720c-414b-bb96-3dc9bbf16d24` |
| BritNed DA & ID Weekly ITLs 20250416 | CSV | upload | `9fcbabfc-7689-437b-99f2-86c05742e77a` |
| BritNed DA & ID Weekly ITLs 20250423 | CSV | upload | `b9bbedd1-6290-4242-bac7-17957a4f3ef0` |
| BritNed DA & ID Weekly ITLs 20250430 | CSV | upload | `04f0d266-ba9c-4e7c-8bdd-f3fe0b45cd7f` |
| BritNed DA & ID Weekly ITLs 20250507 | CSV | upload | `0cde599a-bc16-4486-80da-127c83c68e14` |
| BritNed DA & ID Weekly ITLs 20250514 | CSV | upload | `13c35840-4152-460d-b7f8-38d4fa303728` |
| BritNed DA & ID Weekly ITLs 20250524 | CSV | upload | `29ab02fe-8b4e-4def-ba86-2ae4fb5f26b0` |
| BritNed DA & ID Weekly ITLs 20250528 | CSV | upload | `59b7d9d1-4a71-4be3-ada0-437dbd4b2740` |
| BritNed DA & ID Weekly ITLs 20250604 | CSV | upload | `0c0f6a94-5cef-45d3-8ca7-0b7ce09e5e80` |
| BritNed DA & ID Weekly ITLs 20250611 | CSV | upload | `89e3ec54-aa42-44a6-a106-d0d298f2d835` |
| BritNed DA & ID Weekly ITLs 20250618 | CSV | upload | `ad4523df-6d1d-4974-9198-dcd1269188f8` |
| BritNed DA & ID Weekly ITLs 20250627 | CSV | upload | `6df4e87a-185e-494f-bab1-e204cf813313` |
| BritNed DA & ID Weekly ITLs 20250702 | CSV | upload | `35cf39bd-e393-4a76-9c2d-c084cd71ad7e` |
| BritNed DA & ID Weekly ITLs 20250709 | CSV | upload | `707022a4-a31f-4c74-9bd9-5b2a9e4bf26a` |
| BritNed DA & ID Weekly ITLs 20250716 | CSV | upload | `dabc55d0-c686-4ea9-9e1d-7bc0262a87e7` |
| BritNed DA & ID Weekly ITLs 20250723 | CSV | upload | `a99e3c5d-681c-4bcf-9af4-4dd049f25f38` |
| BritNed DA & ID Weekly ITLs 20250730 | CSV | upload | `68be7816-7bbb-4788-8884-25aaa9a26062` |
| BritNed DA & ID Weekly ITLs 20250806 | CSV | upload | `c17e88aa-8c74-49d4-90bb-679d6c7751f7` |
| BritNed DA & ID Weekly ITLs 20250813 | CSV | upload | `d3d6ab02-78b5-40d1-ace3-7f7b14caf453` |
| BritNed DA & ID Weekly ITLs 20250820 | CSV | upload | `ada92d9f-400c-40f9-a0f6-d4a6e49c6ad2` |
| BritNed DA & ID Weekly ITLs 20250903 | CSV | upload | `15faa1da-22b6-4506-922c-0b5cc988e145` |
| BritNed DA & ID Weekly ITLs 20250917 | CSV | upload | `993b15d3-0bf8-4c9a-851a-4966b0f46926` |
| BritNed DA & ID Weekly ITLs 20251001 | CSV | upload | `115d7d3a-8ba6-4e31-8223-f91ae4ecdc8b` |
| BritNed DA & ID Weekly ITLs 20251015 | CSV | upload | `8fe7d5aa-a3b5-4c7e-a703-74310bd91e2d` |
| BritNed DA & ID Weekly ITLs 20251022 | CSV | upload | `248a3ace-ac3c-4497-8987-8a976d31787f` |
| BritNed DA & ID Weekly ITLs 20251029 | CSV | upload | `675190fe-973f-402b-aeaf-5682aa8874c9` |
| BritNed DA & ID Weekly ITLs 20251105 | CSV | upload | `50ef90de-bcda-45bd-8cd8-b8f9bc0788ea` |
| BritNed DA & ID Weekly ITLs 20251112 | CSV | upload | `70389475-9452-4379-bf21-d3e4500be684` |
| BritNed DA & ID Weekly ITLs 20251119 | CSV | upload | `452837b6-afb5-41b5-847e-88c859cb44c3` |
| BritNed DA & ID Weekly ITLs 20251126 | CSV | upload | `309bd7ee-689b-488d-8263-e5113cae408e` |
| BritNed DA & ID Weekly ITLs 20251203 | CSV | upload | `5c0d23ce-1f82-48c9-9671-af159fbd1803` |
| BritNed DA & ID Weekly ITLs 20251210 | CSV | upload | `c2db2c5d-5278-477c-9a62-7e6e8371bbc7` |
| BritNed DA & ID Weekly ITLs 20251217 | CSV | upload | `91714ac5-147f-43f7-a155-e279fd20810d` |
| BritNed DA & ID Weekly ITLs 20251229 | CSV | upload | `f43260c8-c559-4415-a369-0eb4b9c4e6b2` |
| BritNed DA & ID Weekly ITLs 20251231 | CSV | upload | `3e546d9e-32fc-4cbd-bd51-214b106907e6` |
| BritNed DA & ID Weekly ITLs 20260107 | CSV | upload | `40c995da-2fd8-49d2-b1a1-c82902469299` |
| BritNed DA & ID Weekly ITLs 20260114 | CSV | upload | `e2a26c5b-51a3-427c-b28f-d336d8ba4192` |
| BritNed DA & ID Weekly ITLs 20260121 | CSV | upload | `1e8e15d5-6ca2-4b83-8f27-87c6f6fea446` |
| BritNed DA & ID Weekly ITLs 20260128 | CSV | upload | `d824d533-002f-4828-96d6-85de239f8536` |
| BritNed DA & ID Weekly ITLs 20260215 | CSV | upload | `b2494ee9-2a64-4a6d-ac90-7878f6fffde5` |
| BritNed DA & ID Weekly ITLs 20260218 | CSV | upload | `bfeb12dc-ab49-4dc2-b29b-995ae4f9df5e` |
| BritNed DA & ID Weekly ITLs 20260225 | CSV | upload | `7e524a5b-5e5e-4d88-b7ca-ab64e14a4f15` |
| BritNed DA & ID Weekly ITLs 20260304 | CSV | upload | `759eac2e-5c58-4ec0-990d-eb3f52e666b8` |
| BritNed DA & ID Weekly ITLs 20260311 | CSV | upload | `00c2173e-5d58-48f5-8541-5fbdac98c30c` |
| BritNed DA & ID Weekly ITLs 20260318 | CSV | upload | `9e0a2ae0-d386-4b0d-83c8-0ab129c1b52b` |
| BritNed DA & ID Weekly ITLs 20260325 | CSV | upload | `fdc1cfe6-f77f-496e-b866-d648cd35f26d` |
| BritNed DA & ID Weekly ITLs 20260331 | CSV | upload | `7dbb4e3c-8439-4f9c-a49d-7db2e0fa0235` |
| BritNed DA & ID Weekly ITLs 20260408 | CSV | upload | `774b8573-8e5b-4279-9d24-c33a76416163` |
| BritNed DA & ID Weekly ITLs 20260415 | CSV | upload | `14301751-92fa-4382-bbc7-2d9fe434e90a` |
| BritNed DA & ID Weekly ITLs 20260422 | CSV | upload | `9f7619c7-1893-4ffb-825c-b160f3cba6cc` |
| BritNed DA & ID Weekly ITLs 20260429 | CSV | upload | `a2394a00-5bee-4eb4-ba2e-f617e78961b0` |
| BritNed DA & ID Weekly ITLs 20260506 | CSV | upload | `43de6df5-c171-4a4f-a3f1-6d91816d34fe` |
| BritNed DA & ID Weekly ITLs 20260513 | CSV | upload | `977452d9-56d3-4921-b8b5-2f5c9a8a0445` |
| BritNed DA & ID Weekly ITLs 20260520 | CSV | upload | `bf82899e-34f4-44f1-a859-8f79641757ed` |
| BritNed DA & ID Weekly ITLs 20260527 | CSV | upload | `7cf3b007-4f9d-4213-b7c9-482c69acab00` |
| BritNed DA & ID Weekly ITLs 20260603 | CSV | upload | `30787e04-45aa-48fc-adcb-6d98ddb79077` |
| BritNed DA & ID Weekly ITLs 20260610 | CSV | upload | `92a3f59f-f436-4df7-8c50-7e1fa4c845fd` |
| BritNed DA & ID Weekly ITLs 20260617 | CSV | upload | `2f8723e7-1fd8-4231-911c-27058734b9c0` |
| BritNed DA & ID Weekly ITLs 20260624 | CSV | upload | `a6a6da9c-1138-4498-bae0-b5f8387fa2d9` |
| BritNed DA & ID Weekly ITLs 20260701 | CSV | upload | `1cfd3828-cead-4b64-abcb-875af2031f4b` |
| BritNed DA & ID Weekly ITLs 20260708 | CSV | upload | `a205cc2e-d30f-4054-a980-d5f49d567ad7` |
| BritNed DA & ID Weekly ITLs 20260715 | CSV | upload | `36b889bb-db21-4f65-8961-0813188fd730` |
| BritNed DA & ID Weekly ITLs 20260722 | CSV | upload | `dd34b346-0af1-4913-b31b-aa05abbbe5d5` |
| BritNed DA & ID Weekly ITLs 20260729 | CSV | upload | `bdb4a2ee-ee6e-4956-b7c0-c4fda3bd0e85` |
| BritNed DA & ID Weekly ITLs 20260805 | CSV | upload | `f2256391-5e7d-4895-80d5-d1faa61e270c` |
| BritNed DA & ID Weekly ITLs 20260812 | CSV | upload | `09680097-27b1-4de1-8418-56e1d5dce4ab` |
| BritNed DA & ID Weekly ITLs 20260819 | CSV | upload | `a3f3be57-dced-4282-8f42-94b341e18ff9` |
| BritNed DA & ID Weekly ITLs 20260826 | CSV | upload | `5f640ce3-67e4-4be9-898d-681f0c85d5a1` |
| BritNed DA & ID Weekly ITLs 20260902 | CSV | upload | `0c1d1ac5-09da-4519-b39b-19557989ee7e` |
| BritNed DA & ID Weekly ITLs 20260916 | CSV | upload | `261e6fb2-ccfa-4718-ba21-66e64e363339` |
| BritNed DA & ID Weekly ITLs 20260923 | CSV | upload | `27f2e375-5a0b-484e-938f-4d4c0206d9c0` |

All 187 resources are CSV `upload`s with the SILVER disposition. 185 produce silver. There
are no DOC, GIS or COVERED resources, so there is no document to download. The vendor's
package page is [brit-ned](https://www.neso.energy/data-portal/brit-ned). The oldest
upload's dictionary page is
[britned_da__id_weekly_itls_20221012](https://www.neso.energy/data-portal/brit-ned/britned_da__id_weekly_itls_20221012).

Each resource was captured once, on 2026-10-08 between 08:52:15Z and 09:01:05Z. Sizes,
download URLs and CKAN `last_modified` come from each sidecar under
`C:/gridflow-data/bronze/neso_data_portal/brit_ned/2026/10/08/`. "Data rows" excludes wholly
blank rows. "Epoch" uses this page's numbering (the schema tables below). "Silver" is the
measured row count per `resource_id` in silver on 2026-10-09.

| Resource | Download | Epoch | Bytes | Data rows | CKAN `last_modified` | Silver |
|---|---|---|---:|---:|---|---:|
| BritNed DA & ID Weekly ITLs 20221012 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/10432bfd-2102-4eda-8c6d-bed2a4df676b/download/britned-da-id-weekly-itls-20221012.csv) | 1 | 8,012 | 168 | 2022-10-19T15:36:13.309223 | 0 — failed, adjudicated (`DuplicateEntityKeyError`) |
| BritNed DA & ID Weekly ITLs 20221019 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/c5282013-ee05-4da6-ad46-ff59ff443bfe/download/britned-da-id-weekly-itls-20221019.csv) | 2 | 5,475 | 120 | 2022-10-26T12:34:38.464816 | 120 |
| BritNed DA & ID Weekly ITLs 20221026 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/2248834b-c822-494a-8f1c-ee3cf04705c7/download/britned-da-id-weekly-itls-20221026.csv) | 3 | 6,449 | 144 | 2022-11-02T13:07:23.272437 | 144 |
| BritNed DA & ID Weekly ITLs 20221102 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/eebd1509-b977-43cb-a37e-71ec597a71f0/download/britned-da-id-weekly-itls-20221102.csv) | 2 | 7,237 | 168 | 2022-11-09T14:07:43.174509 | 168 |
| BritNed DA & ID Weekly ITLs 20221109 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/ecda7923-78d7-4865-af9e-0121ebf5c2fb/download/britned-da-id-weekly-itls-20221109.csv) | 2 | 7,256 | 168 | 2022-11-16T17:48:51.967321 | 168 |
| BritNed DA & ID Weekly ITLs 20221116 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/2a4bc449-649d-4d28-b41e-616fc9fa9215/download/britned-da-id-weekly-itls-20221116.csv) | 4 (BOM) | 3,182 | 72 | 2022-11-23T15:28:40.435030 | 72 |
| BritNed DA & ID Weekly ITLs 20221123 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/b51a8d55-62ff-4a47-bc14-a238b3048a25/download/britned-da-id-weekly-itls-20221123.csv) | 4 (BOM) | 6,533 | 144 | 2022-11-30T18:18:16.899119 | 144 |
| BritNed DA & ID Weekly ITLs 20221130 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/aea7e92f-1e5a-48fb-9215-6716f4aab4e1/download/britned-da-id-weekly-itls-20221130.csv) | 4 | 7,879 | 168 | 2022-12-07T14:40:07.402656 | 168 |
| BritNed DA & ID Weekly ITLs 20221207 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/87ae5355-b450-453a-a8b2-2930cf0f2246/download/britned-da-id-weekly-itls-20221207.csv) | 4 | 7,750 | 168 | 2022-12-14T17:35:24.679491 | 168 |
| BritNed DA & ID Weekly ITLs 20221214 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/b9e7f19e-07dc-43af-a67a-68e9588616ee/download/britned-da-id-weekly-itls-20221214.csv) | 4 | 6,952 | 144 | 2022-12-22T11:56:06.285329 | 144 |
| BritNed DA & ID Weekly ITLs 20221221 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/171662b8-4ae0-44ea-8ffa-15d64e0f8562/download/britned-da-id-weekly-itls-20221221.csv) | 4 (BOM) | 1,303 | 24 | 2023-01-04T15:58:12.099411 | 24 |
| BritNed DA & ID Weekly ITLs 20221228 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/6245d8d5-74a1-43bd-97b2-95d4b3d391c5/download/britned-da-id-weekly-itls-20221228.csv) | 4 (BOM) | 1,303 | 24 | 2023-01-04T16:01:44.571069 | 24 |
| BritNed DA & ID Weekly ITLs 20230104 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/9206c32f-35cb-447f-aec9-8ebf25a4e704/download/britned-da-id-weekly-itls-20230104.csv) | 4 | 3,368 | 72 | 2023-01-11T10:05:20.347025 | 72 |
| BritNed DA & ID Weekly ITLs 20230111 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/ddd2abc9-3ef4-4859-bd28-b434bcc7f6ee/download/britned-da-id-weekly-itls-20230111.csv) | 4 | 4,177 | 96 | 2023-01-18T10:34:04.264076 | 96 |
| BritNed DA & ID Weekly ITLs 20230118 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/c6782dcf-1f83-4a21-8b5f-404f787a940d/download/ifa2-da-id-weekly-itls-20230118.csv) | 4 | 5,072 | 120 | 2023-01-25T11:08:43.281064 | 120 |
| BritNed DA & ID Weekly ITLs 20230125 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/8be33510-58f8-4a07-8128-827c6439552a/download/britned-da-id-weekly-itls-20230125.csv) | 4 | 4,334 | 96 | 2023-02-01T09:27:26.141001 | 96 |
| BritNed DA & ID Weekly ITLs 20230201 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/c36f5f3d-c396-4c77-91e0-b1b7b40eec3e/download/britned-da-id-weekly-itls-20230201.csv) | 4 | 5,533 | 120 | 2023-02-08T10:18:48.961027 | 120 |
| BritNed DA & ID Weekly ITLs 20230208 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/d6f1a8e4-1ea9-423c-a5a6-c20f33c59c06/download/britned-da-id-weekly-itls-20230208.csv) | 4 | 7,922 | 168 | 2023-02-15T10:54:36.785216 | 168 |
| BritNed DA & ID Weekly ITLs 20230215 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/885e6cb7-a000-48cc-a4b8-1028f0f4688e/download/britned-da-id-weekly-itls-20230215.csv) | 4 | 6,823 | 144 | 2023-02-22T10:31:54.936745 | 144 |
| BritNed DA & ID Weekly ITLs 20230222 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/d2f2f4f1-30cd-4261-8797-cd0391b2543e/download/britned-da-id-weekly-itls-20230222.csv) | 4 | 1,190 | 24 | 2023-03-01T09:24:10.220451 | 24 |
| BritNed DA & ID Weekly ITLs 20230301 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/3363713c-bae7-4e79-84e3-45bf48ac6410/download/britned-da-id-weekly-itls-20230301.csv) | 4 | 6,434 | 144 | 2023-03-08T09:26:37.579592 | 144 |
| BritNed DA & ID Weekly ITLs 20230308 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/8a53a413-22db-439c-ad64-7673871edce5/download/britned-da-id-weekly-itls-20230308.csv) | 4 | 3,204 | 72 | 2023-03-15T09:44:33.648401 | 72 |
| BritNed DA & ID Weekly ITLs 20230315 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/16c97f2d-26ec-47a0-b4fd-f8cc50d67d58/download/britned-da-id-weekly-itls-20230315.csv) | 4 | 7,692 | 168 | 2023-03-22T10:47:00.628150 | 168 |
| BritNed DA & ID Weekly ITLs 20230322 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/54df8302-2da2-42f9-b5ba-97b4d9d117d5/download/britned-da-id-weekly-itls-20230322.csv) | 4 | 3,028 | 72 | 2023-03-29T08:49:40.081509 | 72 |
| BritNed DA & ID Weekly ITLs 20230329 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/5580a4a3-3ab7-4a55-9c12-95f59668b489/download/britned-da-id-weekly-itls-20230329.csv) | 4 | 4,169 | 96 | 2023-04-05T09:15:13.336607 | 96 |
| BritNed DA & ID Weekly ITLs 20230405 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/bdbaada6-309f-4888-8c99-b3f14bd97eb6/download/britned-da-id-weekly-itls-20230405.csv) | 4 | 4,959 | 120 | 2023-04-12T09:23:29.505469 | 120 |
| BritNed DA & ID Weekly ITLs 20230412 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/d1355935-d61d-47ff-8d84-04f2fd903acf/download/britned-da-id-weekly-itls-20230412.csv) | 4 | 5,643 | 120 | 2023-04-19T09:56:02.439968 | 120 |
| BritNed DA & ID Weekly ITLs 20230419 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/b0738ef5-e0e6-4f93-a303-4b45f08a18ea/download/britned-da-id-weekly-itls-20230419.csv) | 4 | 7,674 | 168 | 2023-04-26T08:02:31.438924 | 168 |
| BritNed DA & ID Weekly ITLs 20230426 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/2cd81edd-7d8f-462c-a8e9-14dc8beff357/download/britned-da-id-weekly-itls-20230426.csv) | 4 | 4,447 | 96 | 2023-05-03T08:58:12.108949 | 96 |
| BritNed DA & ID Weekly ITLs 20230503 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/333b4f84-e23f-46c5-b47f-b2827d54353f/download/britned-da-id-weekly-itls-20230503.csv) | 4 | 5,372 | 120 | 2023-05-10T09:21:02.847171 | 120 |
| BritNed DA & ID Weekly ITLs 20230510 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/bd268477-8923-49fc-9d61-d41c164eb8a0/download/britned-da-id-weekly-itls-20230510.csv) | 4 | 6,047 | 144 | 2023-05-17T09:49:59.502131 | 144 |
| BritNed DA & ID Weekly ITLs 20230517 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/212d8723-3741-4aa4-8201-091f3fd90f26/download/britned-da-id-weekly-itls-20230517.csv) | 4 | 1,252 | 24 | 2023-05-24T09:21:35.424980 | 24 |
| BritNed DA & ID Weekly ITLs 20230524 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/f8a603c6-24e7-416e-8e71-a02b480e9d08/download/britned-da-id-weekly-itls-20230524.csv) | 4 | 3,257 | 72 | 2023-05-31T09:23:42.279070 | 72 |
| BritNed DA & ID Weekly ITLs 20230531 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/8992630e-28b0-430d-930a-c0b80bde2ade/download/britned-da-id-weekly-itls-20230531.csv) | 4 | 3,387 | 72 | 2023-06-07T08:51:32.748910 | 72 |
| BritNed DA & ID Weekly ITLs 20230607 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/513ca6a4-a53e-4996-9cff-a20ac8266bb7/download/britned-da-id-weekly-itls-20230607.csv) | 4 | 4,336 | 96 | 2023-06-14T09:05:39.557366 | 96 |
| BritNed DA & ID Weekly ITLs 20230614 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/e3559f12-f7a7-4d04-9b7b-3504648f1874/download/britned-da-id-weekly-itls-20230614.csv) | 4 | 5,954 | 144 | 2023-06-21T09:12:47.018539 | 144 |
| BritNed DA & ID Weekly ITLs 20230621 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/fb1ced15-5ffe-4d39-9cda-18ebac127399/download/britned-da-id-weekly-itls-20230621.csv) | 4 | 6,359 | 144 | 2023-06-28T09:14:42.064104 | 144 |
| BritNed DA & ID Weekly ITLs 20230628 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/4b5666f2-708e-4af2-a1c8-acfd618cbcd4/download/britned-da-id-weekly-itls-20230628.csv) | 4 | 7,598 | 168 | 2023-07-05T07:51:38.815152 | 168 |
| BritNed DA & ID Weekly ITLs 20230705 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/6b5a3135-0611-4a9e-946b-f770976eaec7/download/britned-da-id-weekly-itls-20230705.csv) | 4 | 4,918 | 120 | 2023-07-12T09:40:58.418356 | 120 |
| BritNed DA & ID Weekly ITLs 20230712 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/e305d44e-c6ae-488c-8828-8f1c887463fa/download/britned-da-id-weekly-itls-20230712.csv) | 4 | 5,349 | 120 | 2023-07-19T07:20:09.385742 | 120 |
| BritNed DA & ID Weekly ITLs 20230719 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/788b330c-6165-48d4-a870-8f2b1f55a5fe/download/britned-da-id-weekly-itls-20230719.csv) | 4 | 1,150 | 24 | 2023-07-26T09:50:08.556035 | 24 |
| BritNed DA & ID Weekly ITLs 20230726 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/c8063e95-057e-4f87-8aef-8b3bb7566e64/download/britned-da-id-weekly-itls-20230726.csv) | 4 | 2,706 | 72 | 2023-08-02T09:13:39.700953 | 72 |
| BritNed DA & ID Weekly ITLs 20230802 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/9ed998b2-0fc8-4cf0-8c4a-77bb7d8dc44f/download/britned-da-id-weekly-itls-20230802.csv) | 4 | 1,038 | 24 | 2023-08-09T08:47:03.176889 | 24 |
| BritNed DA & ID Weekly ITLs 20230809 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/669c7c73-6d66-475c-87f5-c7a64014b3bf/download/britned-da-id-weekly-itls-20230809.csv) | 4 | 5,482 | 144 | 2023-08-16T07:37:28.434173 | 144 |
| BritNed DA & ID Weekly ITLs 20230816 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/e211afc5-fd21-4091-984b-6da1423842d4/download/britned-da-id-weekly-itls-20230816.csv) | 4 | 7,043 | 168 | 2023-08-23T09:24:32.166058 | 168 |
| BritNed DA & ID Weekly ITLs 20230823 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/980dc005-ce8f-49eb-95c6-ec9642d85689/download/britned-da-id-weekly-itls-20230823.csv) | 4 | 5,137 | 120 | 2023-08-30T09:48:49.772507 | 120 |
| BritNed DA & ID Weekly ITLs 20230830 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/4f4d9df4-8db6-41e0-bcdc-b1a1f14e27fc/download/britned-da-id-weekly-itls-20230830.csv) | 4 | 2,753 | 72 | 2023-09-06T09:11:24.974727 | 72 |
| BritNed DA & ID Weekly ITLs 20230906 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/f328325d-ad71-43b8-993c-220fbe9d38bb/download/britned-da-id-weekly-itls-20230906.csv) | 4 | 5,723 | 144 | 2023-09-13T07:49:37.457069 | 144 |
| BritNed DA & ID Weekly ITLs 20230913 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/67fd41a6-3c5a-44e7-934d-83d72d81586f/download/britned-da-id-weekly-itls-20230913.csv) | 4 | 3,851 | 96 | 2023-09-20T08:52:51.524818 | 96 |
| BritNed DA & ID Weekly ITLs 20230920 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/1337e91d-d28b-4206-a343-df71a0922e03/download/britned-da-id-weekly-itls-20230920.csv) | 4 | 3,094 | 72 | 2023-09-27T08:01:40.409394 | 72 |
| BritNed DA & ID Weekly ITLs 20230927 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/3805fbe4-b62c-4c00-8984-e88a1d9cd37c/download/britned-da-id-weekly-itls-20230927.csv) | 4 | 4,539 | 120 | 2023-10-04T10:17:22.745946 | 120 |
| BritNed DA & ID Weekly ITLs 20231004 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/130ec3a1-dd67-4dac-9d00-df7fb5990b05/download/britned-da-id-weekly-itls-20231004.csv) | 4 | 5,716 | 144 | 2023-10-11T07:27:49.005689 | 144 |
| BritNed DA & ID Weekly ITLs 20231011 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/f1b7062f-7fb4-4464-aeeb-cc321481cc1e/download/britned-da-id-weekly-itls-20231011.csv) | 4 | 1,976 | 48 | 2023-10-18T09:50:43.769601 | 48 |
| BritNed DA & ID Weekly ITLs 20231018 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/374d496a-0312-438a-bfa2-294cf0c7c8de/download/britned-da-id-weekly-itls-20231018.csv) | 4 | 3,243 | 72 | 2023-10-25T08:44:59.855192 | 72 |
| BritNed DA & ID Weekly ITLs 20231101 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/abe4cee6-06ce-4557-95bf-f2581778c185/download/britned-da-id-weekly-itls-20231101.csv) | 4 | 1,238 | 24 | 2023-11-08T09:20:01.565640 | 24 |
| BritNed DA & ID Weekly ITLs 20231108 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/e06f5075-f129-4a9a-b7d6-529ef3ad3122/download/britned-da-id-weekly-itls-20231108.csv) | 4 | 1,815 | 48 | 2023-11-15T09:42:57.462877 | 48 |
| BritNed DA & ID Weekly ITLs 20231115 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/48f556c5-33bb-4ac1-bcf6-24d001aacada/download/britned-da-id-weekly-itls-20231115.csv) | 4 | 2,827 | 72 | 2023-11-22T11:23:34.689363 | 72 |
| BritNed DA & ID Weekly ITLs 20231122 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/e0d90a91-5cbe-47a2-9c55-dc8e531b2088/download/britned-da-id-weekly-itls-20231122.csv) | 4 | 4,648 | 120 | 2023-11-29T09:33:37.791322 | 120 |
| BritNed DA & ID Weekly ITLs 20231129 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/f8ad75af-f3d1-447c-8c49-e55ee3ec4f93/download/britned-da-id-weekly-itls-20231129.csv) | 4 | 3,715 | 96 | 2023-12-06T10:00:39.519659 | 96 |
| BritNed DA & ID Weekly ITLs 20231206 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/30d8a0d9-6ff3-4552-9204-65cd89eb5f65/download/britned-da-id-weekly-itls-20231206.csv) | 4 | 3,505 | 72 | 2023-12-13T10:04:13.514680 | 72 |
| BritNed DA & ID Weekly ITLs 20231213 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/08987582-d94e-42e3-8124-54b853c92944/download/britned-da-id-weekly-itls-20231213.csv) | 4 | 5,375 | 120 | 2023-12-20T08:49:11.669324 | 120 |
| BritNed DA & ID Weekly ITLs 20231220 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/88998f41-1ce7-4c7c-9781-4a6a0465ab5a/download/britned-da-id-weekly-itls-20231220.csv) | 4 | 1,229 | 24 | 2023-12-27T09:25:21.627612 | 24 |
| BritNed DA & ID Weekly ITLs 20231227 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/bcd4c323-d8d7-4c37-bcd4-4651cb062aa1/download/britned-da-id-weekly-itls-20231227.csv) | 4 | 965 | 24 | 2024-01-03T10:13:54.348783 | 24 |
| BritNed DA & ID Weekly ITLs 20240103 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/1a9363a1-d052-4faa-b69a-d1872c542fc1/download/britned-da-id-weekly-itls-20240103.csv) | 4 | 1,091 | 24 | 2024-01-10T09:37:57.259693 | 24 |
| BritNed DA & ID Weekly ITLs 20240110 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/aa06b618-91de-4596-afb6-8bb12137d86c/download/britned-da-id-weekly-itls-20240110.csv) | 4 | 7,119 | 168 | 2024-01-17T09:33:14.981862 | 168 |
| BritNed DA & ID Weekly ITLs 20240117 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/aa0477c1-c80c-4208-91fd-5bbc2b4a3d98/download/britned-da-id-weekly-itls-20240117.csv) | 4 | 4,684 | 120 | 2024-01-24T10:09:26.985924 | 120 |
| BritNed DA & ID Weekly ITLs 20240124 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/bbd48f9d-8a63-4fbf-9954-5185552b0520/download/britned-da-id-weekly-itls-20240124.csv) | 4 | 3,802 | 96 | 2024-01-31T08:27:21.994110 | 96 |
| BritNed DA & ID Weekly ITLs 20240131 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/1e67fdb3-31d4-421d-9fc9-c212b41a8ab0/download/britned-da-id-weekly-itls-20240131.csv) | 4 | 4,937 | 120 | 2024-02-07T09:41:42.308019 | 120 |
| BritNed DA & ID Weekly ITLs 20240207 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/8d286f18-3395-45ff-85da-aa7f8f66911c/download/britned-da-id-weekly-itls-20240207.csv) | 4 | 1,824 | 48 | 2024-02-14T08:54:13.865050 | 48 |
| BritNed DA & ID Weekly ITLs 20240214 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/b7c0daed-9e35-42ff-87aa-93b1fbd91cd7/download/britned-da-id-weekly-itls-20240214.csv) | 4 | 1,771 | 48 | 2024-02-21T08:55:43.172342 | 48 |
| BritNed DA & ID Weekly ITLs 20240221 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/fb901593-b6d6-4215-aabb-b60340cf7b1f/download/britned-da-id-weekly-itls-20240221.csv) | 4 | 2,986 | 72 | 2024-02-28T09:45:41.422645 | 72 |
| BritNed DA & ID Weekly ITLs 20240228 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/5b6bae77-3bef-4bec-9a8f-5762d3ad1b9b/download/britned-da-id-weekly-itls-20240228.csv) | 4 | 3,328 | 72 | 2024-03-06T09:40:56.272230 | 72 |
| BritNed DA & ID Weekly ITLs 20240306 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/95ebbde2-0f3b-4609-9435-769633c160f6/download/britned-da-id-weekly-itls-20240306.csv) | 4 | 3,065 | 72 | 2024-03-13T10:04:32.877596 | 72 |
| BritNed DA & ID Weekly ITLs 20240313 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/6c51f881-6b72-49e4-88ad-2fc4ee97ecb3/download/britned-da-id-weekly-itls-20240313.csv) | 4 | 3,555 | 96 | 2024-03-20T10:00:23.549388 | 96 |
| BritNed DA & ID Weekly ITLs 20240320 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/a38ba431-7670-4076-9a5a-82f142f11bdc/download/britned-da-id-weekly-itls-20240320.csv) | 4 | 2,703 | 72 | 2024-03-27T10:02:02.797837 | 72 |
| BritNed DA & ID Weekly ITLs 20240327 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/3d152205-5023-4a46-86a8-2b6b07a0fb9b/download/britned-da-id-weekly-itls-20240327.csv) | 4 | 1,168 | 24 | 2024-04-03T08:28:21.715088 | 24 |
| BritNed DA & ID Weekly ITLs 20240403 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/870495e8-8f95-4817-8615-c40ca5ebef4e/download/britned-da-id-weekly-itls-20240403.csv) | 4 | 1,025 | 24 | 2024-04-10T07:12:07.595265 | 24 |
| BritNed DA & ID Weekly ITLs 20240417 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/8b36e933-304a-44ad-9500-5792819db0d3/download/britned-da-id-weekly-itls-20240417.csv) | 4 | 2,551 | 72 | 2024-04-24T08:30:33.388835 | 72 |
| BritNed DA & ID Weekly ITLs 20240424 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/cf3dcf59-ab29-4630-ba6c-6b73dc769a62/download/britned-da-id-weekly-itls-20240424.csv) | 4 | 1,910 | 48 | 2024-05-01T08:32:30.675842 | 48 |
| BritNed DA & ID Weekly ITLs 20240501 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/32783822-9e65-4b27-abe5-6350262ec7b2/download/britned-da-id-weekly-itls-20240501.csv) | 4 | 1,023 | 24 | 2024-05-08T08:46:43.912242 | 24 |
| BritNed DA & ID Weekly ITLs 20240508 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/eb108e97-2d7b-4d38-8f62-7286cc94b549/download/britned-da-id-weekly-itls-20240508.csv) | 4 | 4,717 | 120 | 2024-05-15T08:12:46.288280 | 120 |
| BritNed DA & ID Weekly ITLs 20240515 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/9e78d6a3-1814-4db3-9a27-e604807c92e9/download/britned-da-id-weekly-itls-20240515.csv) | 4 | 6,925 | 168 | 2024-05-22T09:11:07.008031 | 168 |
| BritNed DA & ID Weekly ITLs 20240522 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/0c32f871-1a47-4378-a5fd-303d02d890b9/download/britned-da-id-weekly-itls-20240522.csv) | 4 | 5,844 | 144 | 2024-05-29T08:44:30.978634 | 144 |
| BritNed DA & ID Weekly ITLs 20240529 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/e7325260-c1f3-468c-96e8-4778893d3ce0/download/britned-da-id-weekly-itls-20240529.csv) | 4 | 3,984 | 96 | 2024-06-05T09:11:52.015413 | 96 |
| BritNed DA & ID Weekly ITLs 20240605 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/e946d60d-ae23-4990-a1a8-91cb36ee010a/download/britned-da-id-weekly-itls-20240605.csv) | 4 | 5,979 | 144 | 2024-06-12T09:19:13.436998 | 144 |
| BritNed DA & ID Weekly ITLs 20240612 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/3d9036a4-1459-4439-9db1-c4479f97901b/download/britned-da-id-weekly-itls-20240612.csv) | 4 | 5,045 | 120 | 2024-06-19T08:32:56.667152 | 120 |
| BritNed DA & ID Weekly ITLs 20240619 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/13a175f1-31ae-4126-b2d4-10ec8bc63a9a/download/britned-da-id-weekly-itls-20240619.csv) | 4 | 4,033 | 96 | 2024-06-26T09:26:45.269750 | 96 |
| BritNed DA & ID Weekly ITLs 20240626 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/2af98846-e08a-43e6-b1f0-326e30a4d470/download/britned-da-id-weekly-itls-20240626.csv) | 4 | 4,033 | 96 | 2024-07-03T09:18:42.706415 | 96 |
| BritNed DA & ID Weekly ITLs 20240807 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/4de159de-1aee-42e0-b00f-f4d3a128f5b3/download/britned-da-id-weekly-itls-20240807.csv) | 4 | 1,079 | 24 | 2024-08-14T07:57:40.198183 | 24 |
| BritNed DA & ID Weekly ITLs 20240814 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/51ff0c0e-c896-4774-aa6f-17b8835fe55f/download/britned-da-id-weekly-itls-20240814.csv) | 4 | 3,603 | 96 | 2024-08-21T09:27:12.570889 | 96 |
| BritNed DA & ID Weekly ITLs 20240821 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/5335579f-da7b-474e-b4ec-6fb826af040f/download/britned-da-id-weekly-itls-20240821.csv) | 4 | 6,382 | 168 | 2024-08-28T08:34:34.388516 | 168 |
| BritNed DA & ID Weekly ITLs 20240828 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/dc46e9bb-906b-49dc-8ac1-05e77a81ec6a/download/britned-da-id-weekly-itls-20240828.csv) | 4 | 6,900 | 168 | 2024-09-04T09:38:20.900564 | 168 |
| BritNed DA & ID Weekly ITLs 20240904 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/0a546c80-0d5b-4217-a2d8-44c3c391bb04/download/britned-da-id-weekly-itls-20240904.csv) | 4 | 6,411 | 168 | 2024-09-11T09:00:48.919313 | 168 |
| BritNed DA & ID Weekly ITLs 20240911 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/e89a9770-f1e5-43c2-92f8-3b090c059654/download/britned-da-id-weekly-itls-20240911.csv) | 4 | 2,852 | 72 | 2024-09-18T10:33:19.053028 | 72 |
| BritNed DA & ID Weekly ITLs 20240918 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/d7749448-914a-49fb-8641-ef1fde6e60f0/download/britned-da-id-weekly-itls-20240918.csv) | 4 | 6,608 | 168 | 2024-09-25T08:54:53.123416 | 168 |
| BritNed DA & ID Weekly ITLs 20240925 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/91df114c-6c0a-4217-a963-8608f0ec619e/download/britned-da-id-weekly-itls-20240925.csv) | 4 | 6,367 | 144 | 2024-10-02T11:20:45.013711 | 144 |
| BritNed DA & ID Weekly ITLs 20241002 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/037acebf-f343-4dce-b9da-1a537c15555f/download/britned-da-id-weekly-itls-20241002.csv) | 4 | 6,336 | 144 | 2024-10-09T07:22:24.451435 | 144 |
| BritNed DA & ID Weekly ITLs 20241009 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/d721fb6d-616c-4339-83be-dc8eb50ad286/download/britned-da-id-weekly-itls-20241009.csv) | 4 | 5,490 | 144 | 2024-10-16T09:34:16.270520 | 144 |
| BritNed DA & ID Weekly ITLs 20241016 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/811bec71-f099-4474-ba5e-2f9932b39cc2/download/britned-da-id-weekly-itls-20241016.csv) | 4 (not UTF-8) | 6,085 | 144 | 2024-10-23T08:37:35.939132 | 0 — failed, open gap (`ComputeError`; IC-2H) |
| BritNed DA & ID Weekly ITLs 20241023 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/7ac2608d-9878-46f2-a075-0b40a87e0a63/download/britned-da-id-weekly-itls-20241023.csv) | 4 | 6,711 | 169 | 2024-10-30T10:13:58.278979 | 169 |
| BritNed DA & ID Weekly ITLs 20241030 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/7c80487f-dc26-430b-abbf-8c2823ed3dcc/download/britned-da-id-weekly-itls-20241030.csv) | 4 | 5,558 | 144 | 2024-11-06T09:22:55.819781 | 144 |
| BritNed DA & ID Weekly ITLs 20241106 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/f3371462-fd35-426e-8652-dd0a5ad69d3b/download/britned-da-id-weekly-itls-20241106.csv) | 4 | 5,695 | 144 | 2024-11-13T09:33:42.951384 | 144 |
| BritNed DA & ID Weekly ITLs 20241113 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/105be229-893d-4a04-a3e4-2e97d9d15cd9/download/britned-da-id-weekly-itls-20241113.csv) | 4 | 6,701 | 168 | 2024-11-20T10:13:31.045088 | 168 |
| BritNed DA & ID Weekly ITLs 20241120 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/7de2143d-f0b5-4d9e-9a20-588a392ed060/download/britned-da-id-weekly-itls-20241120.csv) | 4 | 6,707 | 168 | 2024-11-27T11:01:38.752073 | 168 |
| BritNed DA & ID Weekly ITLs 20241127 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/dbc1d975-607e-4814-b29e-4701d8fa7b7f/download/britned-da-id-weekly-itls-20241127.csv) | 4 | 6,150 | 144 | 2024-12-04T10:23:03.138075 | 144 |
| BritNed DA & ID Weekly ITLs 20241204 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/f5b7cc82-86ca-4e21-bc20-6fee78d525df/download/britned-da-id-weekly-itls-20241204.csv) | 4 | 1,785 | 48 | 2024-12-11T09:08:54.251745 | 48 |
| BritNed DA & ID Weekly ITLs 20250129 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/3b0da3b7-595f-421b-a77e-92f289599905/download/britned-da-id-weekly-itls-20250129.csv) | 4 | 1,734 | 48 | 2025-02-05T13:14:26.208495 | 48 |
| BritNed DA & ID Weekly ITLs 20250205 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/7bbdc91f-9dad-40d9-8d6e-ac7c5ad9d05e/download/britned-da-id-weekly-itls-20250205.csv) | 4 | 6,007 | 144 | 2025-02-12T10:00:00.351349 | 144 |
| BritNed DA & ID Weekly ITLs 20250212 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/7f97b143-c569-4132-9ebf-e17b58585f9f/download/britned-da-id-weekly-itls-20250212.csv) | 4 | 6,773 | 168 | 2025-02-19T09:08:54.218225 | 168 |
| BritNed DA & ID Weekly ITLs 20250219 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/f44a333a-f36f-4f57-882a-e520fc067ef5/download/britned-da-id-weekly-itls-20250219.csv) | 4 | 6,788 | 168 | 2025-02-26T08:33:43.234334 | 168 |
| BritNed DA & ID Weekly ITLs 20250226 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/850f4805-a839-450c-bf2c-1b76090f637c/download/britned-da-id-weekly-itls-20250226.csv) | 4 | 7,055 | 168 | 2025-03-05T08:43:22.160094 | 168 |
| BritNed DA & ID Weekly ITLs 20250305 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/d8d0f00c-a9e6-400a-a1a1-0d4acec0cbcc/download/britned-da-id-weekly-itls-20250305.csv) | 4 | 5,079 | 120 | 2025-03-12T08:57:42.014291 | 120 |
| BritNed DA & ID Weekly ITLs 20250312 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/5c49a1ab-bed9-43e2-9e69-c9c37a16602b/download/britned-da-id-weekly-itls-20250312.csv) | 4 | 1,773 | 48 | 2025-03-19T10:25:23.444246 | 48 |
| BritNed DA & ID Weekly ITLs 20250319 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/25c5f049-8317-4add-b9c9-0e22b749b795/download/britned-da-id-weekly-itls-20250319.csv) | 4 | 1,773 | 48 | 2025-03-26T10:19:23.356902 | 48 |
| BritNed DA & ID Weekly ITLs 20250326 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/5909b052-12e3-4385-9c55-da30b3066968/download/britned-da-id-weekly-itls-20250326.csv) | 4 | 5,392 | 144 | 2025-04-02T14:34:36.897383 | 144 |
| BritNed DA & ID Weekly ITLs 20250407 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/95f31f4e-7465-4359-b135-bbec23a1cfe1/download/britned-da-id-weekly-itls-20250407.csv) | 4 | 1,105 | 24 | 2025-04-09T09:05:06.573571 | 24 |
| BritNed DA & ID Weekly ITLs 20250411 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/8db596d3-720c-414b-bb96-3dc9bbf16d24/download/britned-da-id-weekly-itls-20250411.csv) | 4 | 1,785 | 48 | 2025-04-16T10:16:38.635754 | 48 |
| BritNed DA & ID Weekly ITLs 20250416 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/9fcbabfc-7689-437b-99f2-86c05742e77a/download/britned-da-id-weekly-itls-20250416.csv) | 4 | 4,959 | 120 | 2025-04-23T08:21:11.919585 | 120 |
| BritNed DA & ID Weekly ITLs 20250423 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/b9bbedd1-6290-4242-bac7-17957a4f3ef0/download/britned-da-id-weekly-itls-20250423.csv) | 4 | 2,635 | 72 | 2025-04-30T10:48:27.963325 | 72 |
| BritNed DA & ID Weekly ITLs 20250430 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/04f0d266-ba9c-4e7c-8bdd-f3fe0b45cd7f/download/britned-da-id-weekly-itls-20250430.csv) | 4 | 1,926 | 48 | 2025-05-07T09:38:36.121150 | 48 |
| BritNed DA & ID Weekly ITLs 20250507 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/0cde599a-bc16-4486-80da-127c83c68e14/download/britned-da-id-weekly-itls-20250507.csv) | 4 | 4,059 | 96 | 2025-05-14T08:31:32.005212 | 96 |
| BritNed DA & ID Weekly ITLs 20250514 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/13c35840-4152-460d-b7f8-38d4fa303728/download/britned-da-id-weekly-itls-20250514.csv) | 4 | 2,037 | 48 | 2025-05-21T09:09:11.296841 | 48 |
| BritNed DA & ID Weekly ITLs 20250524 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/29ab02fe-8b4e-4def-ba86-2ae4fb5f26b0/download/britned-da-id-weekly-itls-20250524.csv) | 4 | 3,991 | 96 | 2025-05-28T07:17:09.335972 | 96 |
| BritNed DA & ID Weekly ITLs 20250528 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/59b7d9d1-4a71-4be3-ada0-437dbd4b2740/download/britned-da-id-weekly-itls-20250528.csv) | 4 | 1,979 | 48 | 2025-06-04T08:00:40.584117 | 48 |
| BritNed DA & ID Weekly ITLs 20250604 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/0c0f6a94-5cef-45d3-8ca7-0b7ce09e5e80/download/britned-da-id-weekly-itls-20250604.csv) | 4 | 1,787 | 48 | 2025-06-11T07:25:06.379493 | 48 |
| BritNed DA & ID Weekly ITLs 20250611 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/89e3ec54-aa42-44a6-a106-d0d298f2d835/download/britned-da-id-weekly-itls-20250611.csv) | 4 | 937 | 24 | 2025-06-18T08:24:05.730949 | 24 |
| BritNed DA & ID Weekly ITLs 20250618 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/ad4523df-6d1d-4974-9198-dcd1269188f8/download/britned-da-id-weekly-itls-20250618.csv) | 4 | 3,635 | 96 | 2025-06-25T07:16:14.024120 | 96 |
| BritNed DA & ID Weekly ITLs 20250627 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/6df4e87a-185e-494f-bab1-e204cf813313/download/britned-da-id-weekly-itls-20250627.csv) | 4 | 5,073 | 120 | 2025-07-02T07:42:35.792359 | 120 |
| BritNed DA & ID Weekly ITLs 20250702 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/35cf39bd-e393-4a76-9c2d-c084cd71ad7e/download/britned-da-id-weekly-itls-20250702.csv) | 4 | 5,516 | 144 | 2025-07-09T07:42:11.995996 | 144 |
| BritNed DA & ID Weekly ITLs 20250709 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/707022a4-a31f-4c74-9bd9-5b2a9e4bf26a/download/britned-da-id-weekly-itls-20250709.csv) | 4 | 5,628 | 144 | 2025-07-16T08:31:13.443881 | 144 |
| BritNed DA & ID Weekly ITLs 20250716 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/dabc55d0-c686-4ea9-9e1d-7bc0262a87e7/download/britned-da-id-weekly-itls-20250716.csv) | 4 | 4,683 | 120 | 2025-07-23T08:58:13.113205 | 120 |
| BritNed DA & ID Weekly ITLs 20250723 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/a99e3c5d-681c-4bcf-9af4-4dd049f25f38/download/britned-da-id-weekly-itls-20250723.csv) | 4 | 3,563 | 96 | 2025-07-30T07:08:04.155779 | 96 |
| BritNed DA & ID Weekly ITLs 20250730 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/68be7816-7bbb-4788-8884-25aaa9a26062/download/britned-da-id-weekly-itls-20250730.csv) | 4 | 3,652 | 96 | 2025-08-06T09:26:34.713990 | 96 |
| BritNed DA & ID Weekly ITLs 20250806 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/c17e88aa-8c74-49d4-90bb-679d6c7751f7/download/britned-da-id-weekly-itls-20250806.csv) | 4 | 3,561 | 96 | 2025-08-13T08:08:42.293446 | 96 |
| BritNed DA & ID Weekly ITLs 20250813 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/d3d6ab02-78b5-40d1-ace3-7f7b14caf453/download/britned-da-id-weekly-itls-20250814.csv) | 4 | 4,962 | 120 | 2025-08-20T09:12:52.400138 | 120 |
| BritNed DA & ID Weekly ITLs 20250820 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/ada92d9f-400c-40f9-a0f6-d4a6e49c6ad2/download/britned-da-id-weekly-itls-20250824.csv) | 4 | 985 | 24 | 2025-08-27T09:57:25.691629 | 24 |
| BritNed DA & ID Weekly ITLs 20250903 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/15faa1da-22b6-4506-922c-0b5cc988e145/download/britned-da-id-weekly-itls-20250903.csv) | 4 | 1,941 | 48 | 2025-09-10T09:37:35.128669 | 48 |
| BritNed DA & ID Weekly ITLs 20250917 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/993b15d3-0bf8-4c9a-851a-4966b0f46926/download/britned-da-id-weekly-itls-20250911.csv) | 4 | 1,972 | 48 | 2025-09-24T09:00:23.518526 | 48 |
| BritNed DA & ID Weekly ITLs 20251001 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/115d7d3a-8ba6-4e31-8223-f91ae4ecdc8b/download/britned-da-id-weekly-itls-20251001.csv) | 4 | 4,543 | 120 | 2025-10-08T12:56:34.711394 | 120 |
| BritNed DA & ID Weekly ITLs 20251015 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/8fe7d5aa-a3b5-4c7e-a703-74310bd91e2d/download/britned-da-id-weekly-itls-20251015.csv) | 4 | 3,035 | 72 | 2025-10-22T08:18:43.245399 | 72 |
| BritNed DA & ID Weekly ITLs 20251022 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/248a3ace-ac3c-4497-8987-8a976d31787f/download/britned-da-id-weekly-itls-20251022.csv) | 4 | 1,969 | 48 | 2025-10-29T09:51:11.257542 | 48 |
| BritNed DA & ID Weekly ITLs 20251029 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/675190fe-973f-402b-aeaf-5682aa8874c9/download/britned-da-id-weekly-itls-20251029.csv) | 4 | 3,773 | 96 | 2025-11-07T09:17:14.854585 | 96 |
| BritNed DA & ID Weekly ITLs 20251105 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/50ef90de-bcda-45bd-8cd8-b8f9bc0788ea/download/britned-da-id-weekly-itls-20251105.csv) | 4 | 1,995 | 48 | 2025-11-12T09:05:26.841772 | 48 |
| BritNed DA & ID Weekly ITLs 20251112 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/70389475-9452-4379-bf21-d3e4500be684/download/britned-da-id-weekly-itls-20251112.csv) | 4 | 7,165 | 168 | 2025-11-24T14:43:25.363094 | 168 |
| BritNed DA & ID Weekly ITLs 20251119 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/452837b6-afb5-41b5-847e-88c859cb44c3/download/britned-da-id-weekly-itls-20251119.csv) | 4 | 3,865 | 96 | 2025-11-26T08:19:03.540610 | 96 |
| BritNed DA & ID Weekly ITLs 20251126 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/309bd7ee-689b-488d-8263-e5113cae408e/download/britned-da-id-weekly-itls-20251126.csv) | 4 | 3,859 | 96 | 2025-12-03T09:32:35.644183 | 96 |
| BritNed DA & ID Weekly ITLs 20251203 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/5c0d23ce-1f82-48c9-9671-af159fbd1803/download/britned-da-id-weekly-itls-20251203.csv) | 4 | 3,747 | 96 | 2025-12-10T09:07:24.175370 | 96 |
| BritNed DA & ID Weekly ITLs 20251210 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/c2db2c5d-5278-477c-9a62-7e6e8371bbc7/download/britned-da-id-weekly-itls-20251210.csv) | 4 | 5,979 | 144 | 2025-12-17T08:36:58.357555 | 144 |
| BritNed DA & ID Weekly ITLs 20251217 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/91714ac5-147f-43f7-a155-e279fd20810d/download/britned-da-id-weekly-itls-20251217.csv) | 4 | 4,859 | 120 | 2025-12-24T10:21:18.145976 | 120 |
| BritNed DA & ID Weekly ITLs 20251229 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/f43260c8-c559-4415-a369-0eb4b9c4e6b2/download/britned-da-id-weekly-itls-20251229.csv) | 4 | 2,187 | 48 | 2025-12-31T10:08:15.411920 | 48 |
| BritNed DA & ID Weekly ITLs 20251231 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/3e546d9e-32fc-4cbd-bd51-214b106907e6/download/britned-da-id-weekly-itls-20251231.csv) | 4 | 6,848 | 168 | 2026-01-07T09:20:36.998256 | 168 |
| BritNed DA & ID Weekly ITLs 20260107 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/40c995da-2fd8-49d2-b1a1-c82902469299/download/britned-da-id-weekly-itls-20260107.csv) | 4 | 3,951 | 96 | 2026-01-14T08:43:54.612747 | 96 |
| BritNed DA & ID Weekly ITLs 20260114 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/e2a26c5b-51a3-427c-b28f-d336d8ba4192/download/britned-da-id-weekly-itls-20260114.csv) | 4 | 5,213 | 120 | 2026-01-21T11:16:30.408526 | 120 |
| BritNed DA & ID Weekly ITLs 20260121 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/1e8e15d5-6ca2-4b83-8f27-87c6f6fea446/download/britned-da-id-weekly-itls-20260121.csv) | 4 | 5,226 | 120 | 2026-01-28T09:06:39.905780 | 120 |
| BritNed DA & ID Weekly ITLs 20260128 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/d824d533-002f-4828-96d6-85de239f8536/download/britned-da-id-weekly-itls-20260128.csv) | 4 | 4,286 | 96 | 2026-02-10T08:07:50.351487 | 96 |
| BritNed DA & ID Weekly ITLs 20260215 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/b2494ee9-2a64-4a6d-ac90-7878f6fffde5/download/britned-da-id-weekly-itls-20260215.csv) | 4 | 961 | 24 | 2026-02-18T08:05:11.846174 | 24 |
| BritNed DA & ID Weekly ITLs 20260218 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/bfeb12dc-ab49-4dc2-b29b-995ae4f9df5e/download/britned-da-id-weekly-itls-20260218.csv) | 4 | 6,940 | 168 | 2026-02-25T08:05:53.739632 | 168 |
| BritNed DA & ID Weekly ITLs 20260225 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/7e524a5b-5e5e-4d88-b7ca-ab64e14a4f15/download/britned-da-id-weekly-itls-20260225.csv) | 4 | 4,776 | 120 | 2026-03-04T08:01:40.679726 | 120 |
| BritNed DA & ID Weekly ITLs 20260304 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/759eac2e-5c58-4ec0-990d-eb3f52e666b8/download/britned-da-id-weekly-itls-20260304.csv) | 4 | 2,846 | 72 | 2026-03-11T08:12:31.184737 | 72 |
| BritNed DA & ID Weekly ITLs 20260311 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/00c2173e-5d58-48f5-8541-5fbdac98c30c/download/britned-da-id-weekly-itls-20260311.csv) | 4 | 3,917 | 96 | 2026-03-18T09:05:40.319584 | 96 |
| BritNed DA & ID Weekly ITLs 20260318 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/9e0a2ae0-d386-4b0d-83c8-0ab129c1b52b/download/britned-da-id-weekly-itls-20260318.csv) | 4 | 3,953 | 96 | 2026-03-25T09:13:21.721282 | 96 |
| BritNed DA & ID Weekly ITLs 20260325 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/fdc1cfe6-f77f-496e-b866-d648cd35f26d/download/britned-da-id-weekly-itls-20260325.csv) | 4 | 2,097 | 48 | 2026-04-01T08:17:33.816806 | 48 |
| BritNed DA & ID Weekly ITLs 20260331 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/7dbb4e3c-8439-4f9c-a49d-7db2e0fa0235/download/britned-da-id-weekly-itls-20260331.csv) | 4 | 2,705 | 72 | 2026-04-08T08:30:53.142082 | 72 |
| BritNed DA & ID Weekly ITLs 20260408 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/774b8573-8e5b-4279-9d24-c33a76416163/download/britned-da-id-weekly-itls-20260408.csv) | 4 | 4,296 | 96 | 2026-04-15T07:02:46.759706 | 96 |
| BritNed DA & ID Weekly ITLs 20260415 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/14301751-92fa-4382-bbc7-2d9fe434e90a/download/britned-da-id-weekly-itls-20260415.csv) | 4 | 3,001 | 72 | 2026-04-22T07:09:08.295329 | 72 |
| BritNed DA & ID Weekly ITLs 20260422 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/9f7619c7-1893-4ffb-825c-b160f3cba6cc/download/britned-da-id-weekly-itls-20260422.csv) | 4 | 2,811 | 72 | 2026-04-29T08:42:57.368901 | 72 |
| BritNed DA & ID Weekly ITLs 20260429 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/a2394a00-5bee-4eb4-ba2e-f617e78961b0/download/britned-da-id-weekly-itls-20260429.csv) | 4 | 2,692 | 72 | 2026-05-06T08:22:40.009723 | 72 |
| BritNed DA & ID Weekly ITLs 20260506 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/43de6df5-c171-4a4f-a3f1-6d91816d34fe/download/britned-da-id-weekly-itls-20260506.csv) | 4 | 1,899 | 48 | 2026-05-13T07:13:03.696317 | 48 |
| BritNed DA & ID Weekly ITLs 20260513 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/977452d9-56d3-4921-b8b5-2f5c9a8a0445/download/britned-da-id-weekly-itls-20260513.csv) | 4 | 1,023 | 24 | 2026-05-20T08:59:09.503819 | 24 |
| BritNed DA & ID Weekly ITLs 20260520 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/bf82899e-34f4-44f1-a859-8f79641757ed/download/britned-da-id-weekly-itls-20260520.csv) | 4 | 2,680 | 72 | 2026-05-27T07:09:11.497618 | 72 |
| BritNed DA & ID Weekly ITLs 20260527 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/7cf3b007-4f9d-4213-b7c9-482c69acab00/download/britned-da-id-weekly-itls-20260527.csv) | 4 | 4,941 | 120 | 2026-06-03T07:45:03.489599 | 120 |
| BritNed DA & ID Weekly ITLs 20260603 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/30787e04-45aa-48fc-adcb-6d98ddb79077/download/britned-da-id-weekly-itls-20260603.csv) | 4 | 5,443 | 144 | 2026-06-10T07:26:03.710671 | 144 |
| BritNed DA & ID Weekly ITLs 20260610 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/92a3f59f-f436-4df7-8c50-7e1fa4c845fd/download/britned-da-id-weekly-itls-20260610.csv) | 4 | 1,757 | 48 | 2026-06-17T08:27:33.882197 | 48 |
| BritNed DA & ID Weekly ITLs 20260617 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/2f8723e7-1fd8-4231-911c-27058734b9c0/download/britned-da-id-weekly-itls-20260617.csv) | 4 | 4,877 | 120 | 2026-06-24T10:24:48.236054 | 120 |
| BritNed DA & ID Weekly ITLs 20260624 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/a6a6da9c-1138-4498-bae0-b5f8387fa2d9/download/britned-da-id-weekly-itls-20260624.csv) | 4 | 6,082 | 168 | 2026-07-01T08:14:24.413395 | 168 |
| BritNed DA & ID Weekly ITLs 20260701 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/1cfd3828-cead-4b64-abcb-875af2031f4b/download/britned-da-id-weekly-itls-20260701.csv) | 4 | 4,964 | 120 | 2026-07-08T08:58:01.989186 | 120 |
| BritNed DA & ID Weekly ITLs 20260708 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/a205cc2e-d30f-4054-a980-d5f49d567ad7/download/britned-da-id-weekly-itls-20260708.csv) | 4 | 3,705 | 96 | 2026-07-16T09:11:27.989094 | 96 |
| BritNed DA & ID Weekly ITLs 20260715 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/36b889bb-db21-4f65-8961-0813188fd730/download/britned-da-id-weekly-itls-20260715.csv) | 4 | 6,395 | 168 | 2026-07-22T08:56:11.254463 | 168 |
| BritNed DA & ID Weekly ITLs 20260722 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/dd34b346-0af1-4913-b31b-aa05abbbe5d5/download/britned-da-id-weekly-itls-20260722.csv) | 4 | 6,471 | 168 | 2026-07-29T12:39:51.143692 | 168 |
| BritNed DA & ID Weekly ITLs 20260729 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/bdb4a2ee-ee6e-4956-b7c0-c4fda3bd0e85/download/britned-da-id-weekly-itls-20260729.csv) | 4 | 3,261 | 72 | 2026-08-06T08:00:22.941165 | 72 |
| BritNed DA & ID Weekly ITLs 20260805 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/f2256391-5e7d-4895-80d5-d1faa61e270c/download/britned-da-id-weekly-itls-20260805.csv) | 4 | 6,958 | 168 | 2026-08-12T07:29:56.535235 | 168 |
| BritNed DA & ID Weekly ITLs 20260812 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/09680097-27b1-4de1-8418-56e1d5dce4ab/download/britned-da-id-weekly-itls-20260812.csv) | 4 | 7,465 | 168 | 2026-08-19T09:12:25.377688 | 168 |
| BritNed DA & ID Weekly ITLs 20260819 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/a3f3be57-dced-4282-8f42-94b341e18ff9/download/britned-da-id-weekly-itls-20260819.csv) | 4 | 7,374 | 168 | 2026-08-26T08:52:55.338227 | 168 |
| BritNed DA & ID Weekly ITLs 20260826 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/5f640ce3-67e4-4be9-898d-681f0c85d5a1/download/britned-da-id-weekly-itls-20260826.csv) | 4 | 5,759 | 144 | 2026-09-02T08:34:59.906060 | 144 |
| BritNed DA & ID Weekly ITLs 20260902 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/0c1d1ac5-09da-4519-b39b-19557989ee7e/download/britned-da-id-weekly-itls-20260902.csv) | 4 | 2,888 | 72 | 2026-09-09T08:02:53.840723 | 72 |
| BritNed DA & ID Weekly ITLs 20260916 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/261e6fb2-ccfa-4718-ba21-66e64e363339/download/britned-da-id-weekly-itls-20260916.csv) | 5 | 2,845 | 72 | 2026-09-23T08:04:13.828896 | 72 |
| BritNed DA & ID Weekly ITLs 20260923 | [download](https://api.neso.energy/dataset/1a9fa49a-dea1-4468-9a8c-7800db9d3ff4/resource/27f2e375-5a0b-484e-938f-4d4c0206d9c0/download/britned-da-id-weekly-itls-20260923.csv) | 5 | 7,165 | 168 | 2026-09-30T09:13:52.503781 | 168 |

Totals: 796,311 bytes, 19,153 parsed rows, of which 24 are wholly blank and 19,129 are
non-blank. Silver has 18,817 rows: 19,129 less 168 (20221012) less 144 (20241016). Notes on
individual resources:

- **20221012 (`10432bfd…`, FACTS alias B-OLD): failed, adjudicated.** The label
  `20221012 04:00 - 05:00` appears twice, at CSV lines 7 and 31, with two different From GB
  values. No row is an exact duplicate. The family key cannot identify these rows
  losslessly, so the transform fails the capture with `DuplicateEntityKeyError` and writes
  nothing. gridflow never deduplicates, and never adds a value or a row index to the key to
  hide a collision. The failure is in the ADR-040 ledger, gridflow
  `@src/gridflow/connectors/neso_data_portal/registry/_reconcile_adjudications.json`, as
  `family: brit_ned`, `category: failed`, `cause: DuplicateEntityKeyError`, ruling 571. The
  open question asks which of the two rows is the published limit, and whether the
  repeated label is a publication defect. Reconcile reports it **adjudicated**, not an open
  gap. Because this is the only page-epoch-1 body, epoch 1 has no silver rows.
- **20241016 (`811bec71…`, FACTS alias B-ENC): failed, open gap.** Physical lines 72–73
  (labels `20241018 21:00-22:00` and `20241018 22:00-23:00`) each carry a standalone `0xA0`
  byte in the export cell. That is a cp1252/Latin-1 non-breaking space, which is invalid
  UTF-8. CP1252 and Latin-1 decode it identically, so the bytes do not identify the
  producer's charset. The record reads `utf-8`, so the engine fails the capture at header
  pre-parse with a polars `ComputeError: invalid utf-8 sequence`. That cause is outside the
  ADR-040 allowlist, so the capture has **no ledger entry** and reconcile reports it as
  **brit_ned's one open gap**. Unit **IC-2H** retires it: strict UTF-8 detection before
  pre-parse, an allowlist entry and a ledger entry (RULINGS 575, 576). The gap is pinned by
  the test `test_the_0xa0_capture_is_the_one_open_reconcile_gap`. Bronze is never re-encoded
  or repaired.
- **Four UTF-8-BOM bodies** (20221116, 20221123, 20221221, 20221228) load normally. The
  reader strips the BOM before header matching. 182 other bodies are BOM-less UTF-8.
- **20251229 and 20251231 (`f43260c8…`, `3e546d9e…`, FACTS B-O1/B-O2): overlap,
  adjudicated.** Both publish all 24 hourly labels of 2025-12-31, and all 24 To GB / From GB
  pairs are equal. NESO states no precedence, so **both are served** (ADR-039). The ledger
  `overlap` entry (ruling 571) asks which upload is authoritative for those labels. No other
  pair of resources shares a label (FACTS all-pairs check). A plain concatenation of silver
  therefore has 24 repeated labels for 2025-12-31, one per resource.
- **20230118 (`c6782dcf…`)**: the vendor's download filename is
  `ifa2-da-id-weekly-itls-20230118.csv`, although the resource is in the BritNed package
  and its header matches BritNed epoch 4. Its content was not checked against the IFA2
  package. `TODO: verify` with NESO that this body is BritNed data.
- **20250917 (`993b15d3…`)**: the catalogue name carries a trailing space
  (`BritNed DA & ID Weekly ITLs 20250917 `), trimmed in the tables above. It also contains
  a label dated `20250911`, outside its named week. **20260225** contains a `20260203`
  label. **20240515** (`9e78d6a3…`) contains the malformed label `202405210 17:00-18:00`.
  All are preserved byte-identical. No date is corrected.
- **20241023** has 169 data rows: its 2024-10-27 day has 25 rows, with
  `01:00-02:00 (a)` and `(b)` labels (see Holds).

## Families

### `brit_ned`

- Kind: tabular · archetype: FC · refresh: weekly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Operational Date (YYYY-MM-DD) & Time GMT/BST (HH:MM - HH:MM) | `operational_date_and_hour` | string | — | yes | — | — |
| Flow (MW) From GB | `flow_from_gb_mw_raw` | string | — | yes | — | — |
| Flow (MW) To GB | `flow_to_gb_mw_raw` | string | — | yes | — | — |
| Reason For Restiction | `reason_for_restriction` | string | — | yes | — | — |

Schema, epoch 2:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Operational Date (YYYY-MM-DD) & Time GMT/BST (HH:MM - HH:MM) | `operational_date_and_hour` | string | — | yes | — | — |
| Flow (MW) to GB | `flow_to_gb_mw_raw` | string | — | yes | — | — |
| Flow (MW) from GB | `flow_from_gb_mw_raw` | string | — | yes | — | — |
| Reason For Restriction | `reason_for_restriction` | string | — | yes | — | — |

Schema, epoch 3:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Operational Date (YYYY-MM-DD) & Time GMT/BST (HH:MM - HH:MM) | `operational_date_and_hour` | string | — | yes | — | — |
| Flow (MW) To GB | `flow_to_gb_mw_raw` | string | — | yes | — | — |
| Flow (MW) From GB | `flow_from_gb_mw_raw` | string | — | yes | — | — |
| Reason For Restriction | `reason_for_restriction` | string | — | yes | — | — |

Schema, epoch 4:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Operational Date (YYYY-MM-DD) & Time GMT/BST (HH:MM - HH:MM) | `operational_date_and_hour` | string | — | yes | — | — |
| Flow (MW) to GB | `flow_to_gb_mw_raw` | string | — | yes | — | — |
| Flow (MW) from GB | `flow_from_gb_mw_raw` | string | — | yes | — | — |
| Reason for restriction | `reason_for_restriction` | string | — | yes | — | — |

Schema, epoch 5:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| Operational Period Start Date and Time GMT | `operational_date_and_hour` | string | — | yes | — | — |
| Flow in MW To GB | `flow_to_gb_mw_raw` | string | — | yes | — | MW |
| Flow in MW From GB | `flow_from_gb_mw_raw` | string | — | yes | — | MW |
| Reason for restriction | `reason_for_restriction` | string | — | yes | — | — |

- Entity key: `resource_id`, `operational_date_and_hour`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**Epochs and resources.** Page epoch *n* is FACTS epoch E*n−1* (FACTS §2 "IC2-1: headers and
encodings"). The five headers differ only in spelling, case, column order and the time
header. A BOM is removed before comparison; nothing else is normalised.

| Page epoch | FACTS | Resources | Data rows | Silver rows | Distinguishing header |
|---:|---|---:|---:|---:|---|
| 1 | E0 | 1 (20221012) | 168 | 0 (failed capture) | From before To; vendor typo `Reason For Restiction` |
| 2 | E1 | 3 (20221019, 20221102, 20221109) | 456 | 456 | lower-case `to GB` / `from GB` |
| 3 | E2 | 1 (20221026) | 144 | 144 | upper-case `To GB` / `From GB` |
| 4 | E3 | 180 (20221116 → 20260902) | 18,121 | 17,977 | lower-case `Reason for restriction` |
| 5 | E4 | 2 (20260916, 20260923) | 240 | 240 | renamed time and flow headers |

(FACTS reports 457 rows for E1 and 18,144 for E3 because it counts parsed rows, including
the 24 wholly blank rows. The table above counts non-blank rows.)

Epoch 5 follows a package notice that new BritNed files "from 17 September 2026 onwards"
use new column IDs: `Operational Period Start Date & Time (GMT)` →
`Operational Period Start Date and Time GMT`, `Flow (MW) To GB` → `Flow in MW To GB`,
`Flow (MW) From GB` → `Flow in MW From GB`, plus a `Data Upload Time GMT` rename. **No
captured BritNed body has a `Data Upload Time` column, in any epoch.** Despite its new
name, the epoch-5 time column **still holds the combined date-and-interval label**
(`20260923 23:00-00:00`), not a start datetime. Every epoch therefore maps its time column
to one raw string, `operational_date_and_hour`, preserved byte-identical. Two format quirks
matter for joins across resources:

- The epoch 1–4 header promises `YYYY-MM-DD`, but every body writes the date as
  `YYYYMMDD`.
- Interval spacing varies by epoch: `20221012 04:00 - 05:00` (epoch 1) against
  `20260923 23:00-00:00` (epoch 5). Fold markers appear as a suffix, `01:00-02:00 (a)`.
  Never whitespace-compact a label to make keys line up. FACTS found that compacting would
  not change the overlap result.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured upload. CKAN emits it without an offset, and gridflow
   reads it as UTC (gridflow `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`).
   The vintage is **per resource**: every row of one weekly file shares that file's vintage.
   Checked against silver on 2026-10-09: 185 distinct vintages, from 2022-10-26T12:34:38Z
   (20221019) to 2026-09-30T09:13:52Z (20260923), with `published_at = available_at` on
   every row. The oldest sidecar vintage, 2022-10-19T15:36:13 (20221012), is not in silver
   because that capture failed.
   - **These are after-the-fact publications.** Taking the first eight characters of each
     label as its date, 18,793 silver rows are dated before their file's vintage date, 24
     on the same date, and 0 after. Each upload lands about a week after its filename token
     (for example 20260923 → 2026-09-30). The resource name's date token is **not** an
     issue time. 20260916 covers labels for 2026-09-20 to 2026-09-22 only. Do not treat a
     file as a forecast that was available before its operational days.
   - **There is no issue time.** No body has an issue or publication column
     (`issue: none` in every epoch), so silver has no `issue_time` column. The CKAN vintage
     is when the captured file was last modified, not when NESO issued each limit to the
     auctions.
2. **Event time (temporal `none`).** The record has no temporal recipe, so **`timestamp_utc`
   is the capture time, not the hour the limit applies to**. `timestamp_utc` and
   `event_time` both equal `capture_written_at`, the time gridflow wrote that resource's
   capture. There are 185 distinct values, one per loaded resource, from
   2026-10-08T08:52:17Z to 2026-10-08T09:01:05Z. The hour the limit applies to exists only
   in the raw label `operational_date_and_hour`. Its calendar is the subject of the hold
   (see Holds), so **gridflow does not compose an instant from it, and neither should a
   consumer** until NESO defines the rollover and the GMT/BST mapping. Even once it does, no
   generic temporal recipe yet composes a date with an hourly interval label. Whether one is
   added is an open follow-up (RULINGS 572). Silver label dates run from 20221020 to
   20260929.

**Units (vendor dictionary only).** The frozen dictionary in the snapshot is the **newest**
upload's (`27f2e375…`, 20260923, epoch 5; gridflow
`@.planning/research/neso-snapshots/field-info/20261008T114228Z/brit_ned.json`). Both
directional flows have unit `MW`, described as "Maximum flow in this direction". The time
and reason columns have unit `N/A`. That is why only epoch 5 shows `MW` in the generated
tables. Epochs 1–4 show "—" because the snapshot holds no dictionary for those uploads. MW
for them comes from the vendor sources FACTS T01–T06 cite: the oldest upload's dictionary
page linked above, and the package notes ("submitted in MW per hourly time period"). The
header text `Flow (MW)` is consistent with that but is not the basis. The dictionary types
the flows as integer, but silver keeps them as **strings** (see Implementation delta below).

**Direction (FACTS T01–T06).** `flow_to_gb_mw_raw` is the **import** limit
(Netherlands → GB) and `flow_from_gb_mw_raw` the **export** limit (GB → Netherlands). Each is
a directional maximum, not one signed net-flow series. gridflow never signs or nets them.
Columns are mapped **by name, not position**: epoch 1 puts From before To. FACTS compared
the labels against local ENTSO-E GB–NL series (net transfer capacity, physical flow,
DC-link intraday limit; @../../entsoe/datasets/dc_link_intraday_transfer_limits.md) under
two candidate calendars. Agreement was only partial and does not establish the calendar,
or that NESO's restriction equals another source's final capacity or flow.

**Sentinels and missing values (FACTS g4–g5).** The vendor declares no sentinel, and the
record has no null-token map.

- **Raw strings, no cast.** Export cells include tokens with thousands separators and with
  decimal notation (FACTS counts 33 comma-containing export tokens, 12 also with decimals,
  across all bodies). NESO does not document the numeric format, so both flows stay raw
  strings exactly as published. A downstream cast must handle separators deliberately.
  Never parse a comma-thousands token as two fields or as a decimal comma.
- **Blank cells → null.** Silver nulls (2026-10-09, 18,817 rows): `flow_to_gb_mw_raw` 570,
  `flow_from_gb_mw_raw` 434, `reason_for_restriction` 8,382; `operational_date_and_hour`
  0. `TODO: verify` the vendor meaning of a blank directional cell. Never read it as zero,
  as "unrestricted" or as nameplate capacity.
- **Zeros stay the string `"0"`.** Literal zeros occur in both directions. No vendor source
  defines zero as missing, so a zero is never nulled or filled.
- No cell holds a literal `-1`, `NA` or `N/A`. The dictionary's `N/A` units are metadata,
  not CSV tokens.
- **24 wholly blank rows** across the bodies are dropped by the reader's logged blank-row
  path, never by a silent filter.
- **Absent rows mean "no NESO restriction"**, per the package notes. Many files cover fewer
  than seven days: FACTS counts 19 bodies with one labelled day and 32 with seven. Do not
  fill the gaps with zero, a nameplate capacity or a reconstructed limit.
- Reasons are free categorical text with no unit, kept as published.

**Identity and selection (ADR-039).** The key is `(resource_id, operational_date_and_hour)`.
`resource_id` is **not a vendor column**: the engine stamps each row with its capture's
sidecar resource UUID. The label is unique within each loaded resource, and the key is
measured unique on all 18,817 silver rows. `_latest` is `whole_capture` **per
`resource_id`** (`latest_partition: resource_id`), so a new capture of one weekly upload
replaces only that upload's rows. A family-wide `whole_capture` would keep a single weekly
file. Do not dedup on the label alone: the 2025-12-31 overlap is two resources serving the
same labels. No vendor identity guarantee exists (FACTS T09); `TODO: verify` with NESO.

**Activation (2026-10-09, master `2d72b83`, PR #96).** The frozen record merged
triple-green (RULINGS 579) and was activated with cutoff 2026-10-08 and no prior silver
(RULINGS 580). `brit_ned` silver has **18,817 rows over 185 resources**, equal to the plan.
The transform exits 1 by design (two failed captures). Reconcile `--all --cutoff 2026-10-08`
exited 1 with **1 open gap** (the 20241016 B-ENC capture, `ComputeError`, to be retired by
IC-2H), **9 adjudicated** (6 prior, plus this family's B-OLD failure and B-O1/B-O2
overlap) and 0 stale. Every other family had 0 gaps (gridflow `@.planning/v0.22-RESULTS.md`
§IC-2).

Silver layout: 185 Parquet files, one per loaded capture, under
`C:/gridflow-data/silver/neso_data_portal/brit_ned/year=2026/month=10/`. The
`year=`/`month=` partition is the **capture** date, not the operational date. Columns (13):
the four vendor columns (`operational_date_and_hour`, `flow_from_gb_mw_raw`,
`flow_to_gb_mw_raw`, `reason_for_restriction`), then `resource_id`, `timestamp_utc`,
`published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`,
`source_run_id` and `dataset_version` (`1+e1`). There is no `issue_time` column. All
timestamps are tz-aware UTC.

**Implementation delta.**

- *Dictionary type vs silver type.* The vendor dictionary types both flows as integer
  (`int4`). Silver keeps them as strings because the published bodies carry thousands
  separators and decimals. IC-1's float64 names (`flow_to_gb_mw` / `flow_from_gb_mw`)
  are deliberately **not** reused. The cast is deferred until NESO's numeric format is
  evidenced (G-3; gridflow `@.planning/v0.22-RESULTS.md` §IC-2).
- *Header promises vs bodies.* The epoch 1–4 header says `YYYY-MM-DD`, but bodies write
  `YYYYMMDD`. The epoch-5 header says "Start Date and Time", but bodies keep the
  date-and-interval label. The package rename notice lists a `Data Upload Time` column that
  no BritNed body contains.
- *Encoding.* The record declares `utf-8`. One body is not UTF-8 (20241016, above). The
  reader has no per-resource charset mechanism. `TODO: verify` the producer's charset with
  NESO (FACTS T07). IC-2H handles the failure path; it does not re-encode.
- *Refresh.* Vendor metadata says "Ad hoc"; the registry classifies the family as weekly,
  matching the observed weekly uploads.

## Cadence

- Registry refresh: weekly
- Vendor metadata (snapshot extras, verbatim):
  - Update frequency: Ad hoc

Uploads are roughly weekly, with gaps. Resource name tokens skip some weeks, for example
between 20240626 and 20240807, and between 20241204 and 20250129. Some weeks have two
uploads (20250407 and 20250411; 20251229 and 20251231). Each upload's CKAN `last_modified`
usually falls about a week after its name token. The newest captured upload is 20260923
(`last_modified` 2026-09-30T09:13:52). Package `metadata_modified` in the 2026-10-06
snapshot is 2026-09-30T09:13:53. Each resource was captured once (2026-10-08). The vendor
does not say whether a published weekly file is ever replaced. `TODO: verify` whether an
upload is revised in place; only a changed `last_modified` across successive captures can
show it.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `brit_ned`: held: TODO: NESO does not define the operational-date rollover, the GMT/BST mapping or the `(a)`/`(b)` fold markers of the hourly labels, and the bodies carry no issue time, so no label can be dated as an issued limit. (unit E-SEM)

The silver output exists on disk, but it is **held**. It is not eligible for publication or
for point-in-time model use until unit E-SEM answers the question above (RULINGS 571; held
at activation, RULINGS 580). The registry carries `eligible` at package level and `held`
at family level (gridflow `@docs/neso_data_portal/eligibility.md`). The family status
governs the silver output. The hold has three parts:

1. **Operational-day rollover (FACTS T08, IC2-1).** Files usually open with
   `23:00-00:00` before `00:00-01:00` under the same date. Whether the `23:00` interval
   belongs to the labelled date or the evening before is undefined. Under the second
   reading each operational day would start at 23:00 of the previous civil date.
2. **GMT/BST mapping and fold markers.** The epoch 1–4 header says "GMT/BST"; the epoch-5
   header says "GMT". The DST days are inconsistent with any single UK-local-day model
   (labels and row counts only; FACTS C-BRIT, C-DETAIL):

   | Labelled day | Rows | Observation |
   |---|---:|---|
   | `20221030` (autumn) | 24 | No repeated-hour marker |
   | `20241027` (autumn) | 25 | Separate `01:00-02:00 (a)` and `(b)` labels |
   | `20250330` (spring) | 24 | Includes `01:00-02:00` |
   | `20260329` (spring) | 24 | Includes `01:00-02:00` |

   A UK-local day would have 25 hours in autumn and 23 in spring, with the 01:00 hour
   missing. A UTC day would have 24 hours and no fold marker. These bodies follow neither
   consistently.
3. **No issue time.** No body records when a limit was issued, and the CKAN vintage
   follows the operational days (see Clocks), so no row can be dated as a limit known
   before delivery.

Settles it: a NESO statement of the label calendar per epoch (date attachment, rollover,
GMT vs BST, the meaning of `(a)`/`(b)`) and of when each limit was issued. Separately
from the hold, the 20221012 capture stays out of silver until NESO answers its
adjudication question, and the 20241016 capture stays out until IC-2H. Lifting the hold
would load neither.

References: gridflow `@.planning/phases/v0.22-K-IC-2/K-IC-2-FACTS.md` (§1, §2, IC2-1,
g2–g5, T01–T10), `@.planning/phases/v0.22-K-IC-2/K-IC-2-SPEC.md` (§1),
`@.planning/v0.22-RESULTS.md` (§IC-2), `@.planning/RULINGS.md` (569, 571, 575, 576, 579,
580), `@src/gridflow/connectors/neso_data_portal/registry/brit-ned.json`,
`@src/gridflow/connectors/neso_data_portal/registry/_reconcile_adjudications.json`,
`@docs/neso_data_portal/eligibility.md`,
`@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`,
`@docs/DECISION_LOG/ADR-039-neso-multi-resource-selection.md`,
`@docs/DECISION_LOG/ADR-040-neso-reconcile-adjudication.md`.
