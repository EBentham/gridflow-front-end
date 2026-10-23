---
source: "neso_data_portal"
package: "system-frequency-data"
dataset_keys: ["system_frequency", "system_frequency_dmy_csv", "system_frequency_gmt_csv", "system_frequency_gmt_zip", "system_frequency_offset_csv", "system_frequency_offset_zip"]
vendor: "NESO Open Data Portal"
skeleton: false
updated: 2026-10-16
layer_coverage: "bronze, silver"
eligibility: "eligible"
---

# System Frequency

This package is the historic GB system frequency at **1-second resolution**, in hertz (Hz),
published by NESO on the Open Data Portal as one CSV per calendar month from January 2014
to August 2026: 152 resources in all. Each row is one second: a timestamp `dtm` and the
frequency reading `f`. The package description says it is the role of the system operator
to keep the system frequency at 50 Hz, with a statutory limit of 0.5 Hz above or below that
value. A month holds one row for every second of the month, so the 152 months come to
**399,686,400** rows (the exact count of seconds in those UTC months). Use it for
frequency-event studies, for the statistical behaviour of frequency around the 50 Hz target,
and as the physical-system companion to the half-hourly balancing, inertia and ancillary
service datasets in this vendor folder (for example @./system-inertia.md). It is not a price
or a settlement series, so the settlement-period rules of
@../../../20-domain/concepts/settlement-period.md do not apply to it.

The series is not one uniform file format, and that shapes everything gridflow does with it.

- **Three renderings of `dtm` under one header (`dtm,f`).** 2014 is day-first and carries no
  zone (`31/01/2014 23:59:59`). 2015 to 2019 is ISO with a numeric offset on every row
  (`+0000` or `+0100`). From January 2020 it is ISO and naive, and NESO states that the times
  are GMT. The 31 midnights of August 2026 are date-only cells.
- **Two body formats.** 113 resources are plain CSV. 39 (January 2019 to March 2022) are
  deflated ZIPs that each hold exactly one CSV member.
- **Re-uploads are real.** NESO replaces old months (see Cadence), so a month can have more
  than one version over time.

gridflow therefore splits the package into **five silver families by rendering and body
format** (ADR-043, gridflow `@docs/DECISION_LOG/ADR-043-neso-system-frequency-renderings.md`).
**Four are eligible** (2015 onward, 368,150,400 rows). **One is held** (2014, day-first, zone
unstated). There is **no union view**: a consumer unions the four typed `_latest` relations
itself, and the reconcile check proves that the union serves no second twice (see Consuming
the series). Outputs derived from this package carry the line *Supported by National Energy
SO Open Data*.

- Publisher group: System
- Registry group: system · archetype: SER

## Files by disposition

### SILVER

| Resource | Format | Capture | Id |
|---|---|---|---|
| April 2014 - Historic Frequency Data | CSV | upload | `8841fc25-5472-4d9b-b0f7-eba44e083042` |
| April 2015 - Historic Frequency Data | CSV | upload | `350b3c70-f66a-48ca-8656-7de25401c03f` |
| April 2016 - Historic Frequency Data | CSV | upload | `4e1e37f9-9ee8-4fcd-a9ac-a74fca270cbd` |
| April 2017 - Historic Frequency Data | CSV | upload | `5270855a-ae0d-4f66-828d-dddfed53f54f` |
| April 2018 - Historic Frequency Data | CSV | upload | `4ebc55c9-7ad6-41e9-9154-b5769dbc17b8` |
| April 2019 - Historic Frequency Data | CSV | upload | `5a511d6f-0cc4-4054-bb45-8ad3b81051ad` |
| ↳ f 2019 4.csv | — | — | SILVER `system_frequency_offset_zip` |
| April 2020 - Historic Frequency Data | CSV | upload | `8b974058-2494-4675-98af-0570c3a0b240` |
| ↳ fNew 2020 4.csv | — | — | SILVER `system_frequency_gmt_zip` |
| April 2021 - Historic Frequency Data | CSV | upload | `bd6e1b3f-1abb-452c-813c-397a41f7af8d` |
| ↳ fNew 2021 4.csv | — | — | SILVER `system_frequency_gmt_zip` |
| April 2022 - Historic Frequency Data | CSV | upload | `b3bbd2e7-50b1-49cb-8326-bc8f09003cde` |
| April 2023 – Historic Frequency Data | CSV | upload | `83fc86bb-50d6-4965-91fb-ddbdd02a5190` |
| April 2024 – Historic Frequency Data | CSV | upload | `d4e3ca9c-ef92-4337-8ac7-b7e8232a94f4` |
| April 2025 – Historic Frequency Data | CSV | upload | `f81823de-ac73-48d4-8b4f-d2c871e5702e` |
| April 2026 – Historic Frequency Data | CSV | upload | `41b25b04-a824-402e-a3eb-2a0eeb348293` |
| August 2014 - Historic Frequency Data | CSV | upload | `ead6ec3e-a7e3-4a51-bcc9-4387175c298b` |
| August 2015 - Historic Frequency Data | CSV | upload | `6f7c57ba-8c46-4b75-950b-3edaa5d6b1b5` |
| August 2016 - Historic Frequency Data | CSV | upload | `8ee38f39-e8b4-42b6-8634-62d847e06d84` |
| August 2017 - Historic Frequency Data | CSV | upload | `5f60b563-ad37-4aca-9aa1-557bdd283987` |
| August 2018 - Historic Frequency Data | CSV | upload | `c51be017-fa87-42c6-b818-1a192699d3eb` |
| August 2019 - Historic Frequency Data | CSV | upload | `819a0821-cc6d-4909-a1ea-7dba5cab0c33` |
| ↳ f 2019 8.csv | — | — | SILVER `system_frequency_offset_zip` |
| August 2020 - Historic Frequency Data | CSV | upload | `27d4d8b3-0cbe-4cb2-bd83-947f968671a1` |
| ↳ fNew 2020 8.csv | — | — | SILVER `system_frequency_gmt_zip` |
| August 2021 - Historic Frequency Data | CSV | upload | `ae40912b-de8f-43b1-8eeb-c58e469f2365` |
| ↳ fNew 2021 8.csv | — | — | SILVER `system_frequency_gmt_zip` |
| August 2022 – Historic Frequency Data | CSV | upload | `232121b1-d3ab-4d5a-9e57-4cfc23d62eba` |
| August 2023 – Historic Frequency Data | CSV | upload | `b530feae-96b1-4f4a-94e1-6c6dee681229` |
| August 2024 – Historic Frequency Data | CSV | upload | `e5a24d28-a344-4969-970a-ffda612931a7` |
| August 2025 – Historic Frequency Data | CSV | upload | `b511a71e-15dc-4bb4-a4e1-dcb881363a85` |
| August 2026 – Historic Frequency Data | CSV | upload | `758fa76d-b645-4532-a532-ab49335ee4c3` |
| December 2014 - Historic Frequency Data | CSV | upload | `c46f588c-0067-46fb-9b82-1e0cb71c920e` |
| December 2015 - Historic Frequency Data | CSV | upload | `da6bc05c-4bca-4f72-8485-71aa10d17ef4` |
| December 2016 - Historic Frequency Data | CSV | upload | `9a0bf4eb-3a7f-48cb-af65-b753dc0e79d0` |
| December 2017 - Historic Frequency Data | CSV | upload | `e9987ee0-38d2-4b22-9a2f-ec935d5574a7` |
| December 2018 - Historic Frequency Data | CSV | upload | `67f7a127-e352-4c09-b403-d44f2740e510` |
| December 2019 - Historic Frequency Data | CSV | upload | `f0933bdd-1b0e-4dd3-aa7f-5498df1ba5b9` |
| ↳ f 2019 12.csv | — | — | SILVER `system_frequency_offset_zip` |
| December 2020 - Historic Frequency Data | CSV | upload | `706ec5fe-777a-4a46-90de-b9089f93853c` |
| ↳ fNew 2020 12.csv | — | — | SILVER `system_frequency_gmt_zip` |
| December 2021 - Historic Frequency Data | CSV | upload | `afe9895c-5937-4e78-8949-f0f026643666` |
| ↳ fNew 2021 12.csv | — | — | SILVER `system_frequency_gmt_zip` |
| December 2022 – Historic Frequency Data | CSV | upload | `2dbcb246-5f7a-45c8-9d04-19fd3f1b1595` |
| December 2023 – Historic Frequency Data | CSV | upload | `146e3d50-6e53-48d9-a831-d7c25304d102` |
| December 2024 – Historic Frequency Data | CSV | upload | `ac188a3c-9e52-40ce-8795-874e951327cb` |
| December 2025 – Historic Frequency Data | CSV | upload | `5c408627-44a1-417d-9fc5-a26ad822c4e4` |
| February 2014 - Historic Frequency Data | CSV | upload | `69553694-f590-4a5a-8da0-9e4532298603` |
| February 2015 - Historic Frequency Data | CSV | upload | `2c5c2cb9-1fcd-45cc-8b13-e08e4b69e79b` |
| February 2016 - Historic Frequency Data | CSV | upload | `0925f06c-1fab-4af9-827b-8fe0bc9812ea` |
| February 2017 - Historic Frequency Data | CSV | upload | `6ff1c0ee-86cc-44b7-9902-e8fefd23b17c` |
| February 2018 - Historic Frequency Data | CSV | upload | `ac669df9-1928-4a8c-9109-2494678f6c87` |
| February 2019 - Historic Frequency Data | CSV | upload | `3343dbfb-58ac-478a-8aed-618a35b38475` |
| ↳ f 2019 2.csv | — | — | SILVER `system_frequency_offset_zip` |
| February 2020 - Historic Frequency Data | CSV | upload | `939590e1-2632-432b-b0d3-3f7e1def9d30` |
| ↳ fNew 2020 2.csv | — | — | SILVER `system_frequency_gmt_zip` |
| February 2021 - Historic Frequency Data | CSV | upload | `53e2be31-c68c-40b3-bb83-7ae12240107c` |
| ↳ fNew 2021 2.csv | — | — | SILVER `system_frequency_gmt_zip` |
| February 2022 - Historic Frequency Data | CSV | upload | `181e8958-bf78-4bd6-b6ca-b8376da8e1aa` |
| ↳ fNew 2022 2.csv | — | — | SILVER `system_frequency_gmt_zip` |
| February 2023 – Historic Frequency Data | CSV | upload | `7a9b6d47-b2fd-4efe-bb41-f6e227b0786a` |
| February 2024 – Historic Frequency Data | CSV | upload | `4e24d459-3688-4c8c-8323-f1d38a0564a2` |
| February 2025 – Historic Frequency Data | CSV | upload | `ec60c750-b4e4-4328-a693-7b562467b175` |
| February 2026 – Historic Frequency Data | CSV | upload | `7f5364d6-5a06-4d34-bd60-6c4348cd892e` |
| January 2014 - Historic Frequency Data | CSV | upload | `0cd6ff2e-62ca-4fbf-8417-18b3539530e6` |
| January 2015 - Historic Frequency Data | CSV | upload | `67b59ac0-b297-4f90-936e-30039d2cf2df` |
| January 2016 - Historic Frequency Data | CSV | upload | `8a7a0ec6-a304-4f6e-b722-2f595cfde45b` |
| January 2017 - Historic Frequency Data | CSV | upload | `e7b276d2-0188-4dd9-8c0f-2176340158b1` |
| January 2018 - Historic Frequency Data | CSV | upload | `eee0395e-7a8d-45c3-8f23-0e6c7e252c3e` |
| January 2019 - Historic Frequency Data | CSV | upload | `2a653f90-7948-4203-a49e-8763733debb2` |
| ↳ f 2019 1.csv | — | — | SILVER `system_frequency_offset_zip` |
| January 2020 - Historic Frequency Data | CSV | upload | `e1eb079f-abab-47c8-b59d-d558b3399796` |
| ↳ fNew 2020 1.csv | — | — | SILVER `system_frequency_gmt_zip` |
| January 2021 - Historic Frequency Data | CSV | upload | `fe2502b8-7fef-4027-8399-550a0c84f415` |
| ↳ fNew 2021 1.csv | — | — | SILVER `system_frequency_gmt_zip` |
| January 2022 - Historic Frequency Data | CSV | upload | `43000c20-1208-4ca7-a419-712c7a1d375c` |
| ↳ fNew 2022 1.csv | — | — | SILVER `system_frequency_gmt_zip` |
| January 2023 – Historic Frequency Data | CSV | upload | `5da35567-ca7f-4127-861c-cc07d488fd2d` |
| January 2024 – Historic Frequency Data | CSV | upload | `79c707ac-dcd6-4f08-80e3-10a6ba92647c` |
| January 2025 – Historic Frequency Data | CSV | upload | `7b01e945-0e5b-4b51-9a21-6dc0a6d422d7` |
| January 2026 – Historic Frequency Data | CSV | upload | `dbc3d95b-57f2-4e12-9281-44aad0667e6e` |
| July 2014 - Historic Frequency Data | CSV | upload | `e9ae9d2d-0019-42c0-aa16-defca2433208` |
| July 2015 - Historic Frequency Data | CSV | upload | `2d901bcf-8907-45b4-8c7d-5fc91fb16b8b` |
| July 2016 - Historic Frequency Data | CSV | upload | `22aff02a-7e1a-413f-afa1-4ca3e82ea426` |
| July 2017 - Historic Frequency Data | CSV | upload | `39ad9573-bbe1-406c-8ffc-10d7df65d9e6` |
| July 2018 - Historic Frequency Data | CSV | upload | `bf45c11d-c787-4f84-8896-b14381f534c7` |
| July 2019 - Historic Frequency Data | CSV | upload | `da48b1fe-8e54-48fc-87b9-f6b0362422e2` |
| ↳ f 2019 7.csv | — | — | SILVER `system_frequency_offset_zip` |
| July 2020 - Historic Frequency Data | CSV | upload | `7c9a488f-5070-4f8b-a3a1-0418ed4438a2` |
| ↳ fNew 2020 7.csv | — | — | SILVER `system_frequency_gmt_zip` |
| July 2021 - Historic Frequency Data | CSV | upload | `94d95251-ccbb-4187-ae54-1b90ebf12b9f` |
| ↳ fNew 2021 7.csv | — | — | SILVER `system_frequency_gmt_zip` |
| July 2022 – Historic Frequency Data | CSV | upload | `3c62eb13-0531-4b20-b1a3-b9ff5095e5ef` |
| July 2023 – Historic Frequency Data | CSV | upload | `7e38448c-e482-46fe-b30e-cde1da30cf8d` |
| July 2024 – Historic Frequency Data | CSV | upload | `5dd3bbc6-40d1-41d4-a8d0-cfefef11c099` |
| July 2025 – Historic Frequency Data | CSV | upload | `a3cbf8d1-8327-4c80-82ef-a7a31820ec72` |
| July 2026 – Historic Frequency Data | CSV | upload | `027227d0-7c70-4497-bdc4-a80cff7726f8` |
| June 2014 - Historic Frequency Data | CSV | upload | `b295bc6b-2f1a-4f05-8925-54e7540b9137` |
| June 2015 - Historic Frequency Data | CSV | upload | `b620b4ba-c243-47ea-9a0b-e08be7ad1cf6` |
| June 2016 - Historic Frequency Data | CSV | upload | `19e18e2c-9104-479b-b741-1ea6befc7c71` |
| June 2017 - Historic Frequency Data | CSV | upload | `1489d348-abda-47d3-a31d-a3bd09332840` |
| June 2018 - Historic Frequency Data | CSV | upload | `2779f782-5938-4857-86d8-25350c2d4162` |
| June 2019 - Historic Frequency Data | CSV | upload | `f967b00a-36b4-4979-920e-77fdb6be8a9c` |
| ↳ f 2019 6.csv | — | — | SILVER `system_frequency_offset_zip` |
| June 2020 - Historic Frequency Data | CSV | upload | `4a7f506b-dd04-4480-988b-dff0cc3f9ed4` |
| ↳ fNew 2020 6.csv | — | — | SILVER `system_frequency_gmt_zip` |
| June 2021 - Historic Frequency Data | CSV | upload | `bd754692-bce7-43b7-ba25-813921476391` |
| ↳ fNew 2021 6.csv | — | — | SILVER `system_frequency_gmt_zip` |
| June 2022 – Historic Frequency Data | CSV | upload | `15c16754-6ed4-491e-949f-a42c6145ff24` |
| June 2023 – Historic Frequency Data | CSV | upload | `2b881e0a-44b4-4957-9cc3-89bf0df6247a` |
| June 2024 – Historic Frequency Data | CSV | upload | `c19ba72b-64ee-41f8-ba2d-2fdb4f5c1550` |
| June 2025 – Historic Frequency Data | CSV | upload | `8ac51432-f0c0-42e7-836e-247a030c91b9` |
| June 2026 – Historic Frequency Data | CSV | upload | `dc7c5468-08a1-4586-bcdd-77ced39a5067` |
| March 2014 - Historic Frequency Data | CSV | upload | `189fc0cb-7af9-4c7c-b674-0544ecb4b308` |
| March 2015 - Historic Frequency Data | CSV | upload | `0f008751-3f0b-4353-9d4a-72f208221532` |
| March 2016 - Historic Frequency Data | CSV | upload | `c8e26834-7b2b-4ad5-b365-b7cae23ddbc7` |
| March 2017 - Historic Frequency Data | CSV | upload | `f2142cc5-19f0-4724-bf8e-f93bd3daba78` |
| March 2018 - Historic Frequency Data | CSV | upload | `8e84b78f-8078-4188-965f-41685fd316bc` |
| March 2019 - Historic Frequency Data | CSV | upload | `b4fc11ec-2f9b-465e-8974-37cc289f2aaa` |
| ↳ f 2019 3.csv | — | — | SILVER `system_frequency_offset_zip` |
| March 2020 - Historic Frequency Data | CSV | upload | `1b7609f1-5132-45fc-8962-89912eb2b682` |
| ↳ fNew 2020 3.csv | — | — | SILVER `system_frequency_gmt_zip` |
| March 2021 - Historic Frequency Data | CSV | upload | `ac4e4031-0f86-48ff-8ecd-147d51ffbb81` |
| ↳ fNew 2021 3.csv | — | — | SILVER `system_frequency_gmt_zip` |
| March 2022 - Historic Frequency Data | CSV | upload | `182081de-9773-4b5b-9c87-17adbd1576e6` |
| ↳ fNew 2022 3.csv | — | — | SILVER `system_frequency_gmt_zip` |
| March 2023 – Historic Frequency Data | CSV | upload | `69e906af-04f6-49b9-95e9-b02a64a46582` |
| March 2024 – Historic Frequency Data | CSV | upload | `f6df9f02-458e-476e-9e04-9f71ac577eeb` |
| March 2025 – Historic Frequency Data | CSV | upload | `6437cf1d-8517-42dc-9086-e386df5065d5` |
| March 2026 – Historic Frequency Data | CSV | upload | `e7023794-d9f8-43ed-bfee-31c6f36a87f2` |
| May 2014 - Historic Frequency Data | CSV | upload | `16371770-2102-405f-a3f8-6098d0d66ce0` |
| May 2015 - Historic Frequency Data | CSV | upload | `4248e877-0af0-4f6a-9e7d-ee5f7b13fcf3` |
| May 2016 - Historic Frequency Data | CSV | upload | `9ce83f3a-0d10-4f92-a8b4-5b6de71f66ef` |
| May 2017 - Historic Frequency Data | CSV | upload | `fa42b000-5d10-4a84-bbc4-6bf2a73b8696` |
| May 2018 - Historic Frequency Data | CSV | upload | `215f0a52-d0dd-40ee-a103-6d14a5361e41` |
| May 2019 - Historic Frequency Data | CSV | upload | `84a85749-18e1-4b6b-bb97-73888ccacfe0` |
| ↳ f 2019 5.csv | — | — | SILVER `system_frequency_offset_zip` |
| May 2020 - Historic Frequency Data | CSV | upload | `954de419-c4e4-4366-9711-6cc1f0fcaa48` |
| ↳ fNew 2020 5.csv | — | — | SILVER `system_frequency_gmt_zip` |
| May 2021 - Historic Frequency Data | CSV | upload | `625597eb-7364-4ba8-a306-a7f59dcdc2a7` |
| ↳ fNew 2021 5.csv | — | — | SILVER `system_frequency_gmt_zip` |
| May 2022 - Historic Frequency Data | CSV | upload | `0a32dbfc-89e2-447d-a867-b10d5dbf3192` |
| May 2023 – Historic Frequency Data | CSV | upload | `66c7be67-9689-4578-bc8d-684a2dea8248` |
| May 2024 – Historic Frequency Data | CSV | upload | `755fc810-1a55-4dc7-9692-84cc4a33fdcf` |
| May 2025 – Historic Frequency Data | CSV | upload | `2122c101-fad5-4989-9814-728572d510e0` |
| May 2026 – Historic Frequency Data | CSV | upload | `06315187-afcf-4fe2-8439-0eacc3f7bc35` |
| November 2014 - Historic Frequency Data | CSV | upload | `0958d0a4-f98c-4617-92ab-a0de1b6ba0c0` |
| November 2015 - Historic Frequency Data | CSV | upload | `160fb47a-da74-4026-a22a-a51e792d22f6` |
| November 2016 - Historic Frequency Data | CSV | upload | `93cee8bd-0fed-4408-b148-246861c19104` |
| November 2017 - Historic Frequency Data | CSV | upload | `56fcb63c-4cb4-4de1-8a1d-d8fde291dfaa` |
| November 2018 - Historic Frequency Data | CSV | upload | `b3a66b62-f791-4cb3-ba99-ba7bc9b05333` |
| November 2019 - Historic Frequency Data | CSV | upload | `3d1a42c0-5637-4702-b9c3-76a7c5d8f062` |
| ↳ f 2019 11.csv | — | — | SILVER `system_frequency_offset_zip` |
| November 2020 - Historic Frequency Data | CSV | upload | `bcfa7999-1b14-444b-8f8f-6402092a0e9d` |
| ↳ fNew 2020 11.csv | — | — | SILVER `system_frequency_gmt_zip` |
| November 2021 - Historic Frequency Data | CSV | upload | `9bc4746e-3152-4c6f-886e-58377ab88e0e` |
| ↳ fNew 2021 11.csv | — | — | SILVER `system_frequency_gmt_zip` |
| November 2022 – Historic Frequency Data | CSV | upload | `ff852ca5-1462-4ed6-ab77-886617719276` |
| November 2023 – Historic Frequency Data | CSV | upload | `1f17159a-df91-48ef-a3d5-02da75e4196a` |
| November 2024 – Historic Frequency Data | CSV | upload | `d83124cd-5f18-4bd3-b956-001914585d0f` |
| November 2025 – Historic Frequency Data | CSV | upload | `2ddaf963-191a-43c3-bb3b-286de31508ee` |
| October 2014 - Historic Frequency Data | CSV | upload | `32f82531-81ad-43b9-99a4-ca42b3d7aa59` |
| October 2015 - Historic Frequency Data | CSV | upload | `0bf8a3cf-d3b2-40bb-a203-58bcf0391b09` |
| October 2016 - Historic Frequency Data | CSV | upload | `74b30661-acd2-4280-a0cc-90315ae1c68b` |
| October 2017 - Historic Frequency Data | CSV | upload | `b8ce3808-8f72-46f0-98d8-2ed8befa91f5` |
| October 2018 - Historic Frequency Data | CSV | upload | `cec33870-6c5e-4594-a62c-d824625cf404` |
| October 2019 - Historic Frequency Data | CSV | upload | `65b4f284-4963-46c5-ae78-cab57fe5372f` |
| ↳ f 2019 10.csv | — | — | SILVER `system_frequency_offset_zip` |
| October 2020 - Historic Frequency Data | CSV | upload | `3617f1af-4d3c-45d3-a1f6-0d51a9c2167b` |
| ↳ fNew 2020 10.csv | — | — | SILVER `system_frequency_gmt_zip` |
| October 2021 - Historic Frequency Data | CSV | upload | `12291f14-95c3-4847-b2ef-3190eaa1193c` |
| ↳ fNew 2021 10.csv | — | — | SILVER `system_frequency_gmt_zip` |
| October 2022 – Historic Frequency Data | CSV | upload | `74a4fae6-11e6-4e3b-9c48-7263f581f5c2` |
| October 2023 – Historic Frequency Data | CSV | upload | `530d18c9-01bc-4620-9911-0d03c7152081` |
| October 2024 – Historic Frequency Data | CSV | upload | `0c45a551-bda2-450c-9f41-b3185e643824` |
| October 2025 – Historic Frequency Data | CSV | upload | `288eba29-3ea0-4a93-bc7f-995c98473294` |
| September 2014 - Historic Frequency Data | CSV | upload | `0ecdb5ea-4b26-4273-b1d8-d61dc94b3ceb` |
| September 2015 - Historic Frequency Data | CSV | upload | `3ac1a58b-3c1e-456d-a515-04a8c154b374` |
| September 2016 - Historic Frequency Data | CSV | upload | `fac03fe6-bc94-40aa-8882-311d5e93082b` |
| September 2017 - Historic Frequency Data | CSV | upload | `b0d623f6-381e-4c79-a1dd-a013f8eaaf98` |
| September 2018 - Historic Frequency Data | CSV | upload | `9fe022eb-976f-4a17-beab-539ab00c61ea` |
| September 2019 - Historic Frequency Data | CSV | upload | `9ffafdfb-cf42-46b3-802f-a6d9a45794aa` |
| ↳ f 2019 9.csv | — | — | SILVER `system_frequency_offset_zip` |
| September 2020 - Historic Frequency Data | CSV | upload | `cfc880fe-3d3d-4df4-bf4f-9294a4dbc901` |
| ↳ fNew 2020 9.csv | — | — | SILVER `system_frequency_gmt_zip` |
| September 2021 - Historic Frequency Data | CSV | upload | `5cea7516-cbc3-416e-8dbf-162327c16b17` |
| ↳ fNew 2021 9.csv | — | — | SILVER `system_frequency_gmt_zip` |
| September 2022 – Historic Frequency Data | CSV | upload | `a1ccd82c-e522-4b5d-a4da-57dafab9d6de` |
| September 2023 – Historic Frequency Data | CSV | upload | `66487376-67f5-46bd-a508-442e7761f51c` |
| September 2024 – Historic Frequency Data | CSV | upload | `894b8dee-ad54-4f89-9f95-3f90661c3547` |
| September 2025 – Historic Frequency Data | CSV | upload | `5b1ae652-c0d5-4853-b46f-6af414b487fd` |

**Disposition summary.** All 152 resources are SILVER. There is no DOC, reference or
catalogue-only resource in this package, so there is no document to link. Each resource is a
CSV in the CKAN sense (`format: CSV`, `url_type: upload`), including the 39 whose body is a
ZIP. A ZIP resource has one child, the inner CSV, shown as a `↳` row above, and the child
shares the parent's family.

| Family | Rendering | Body / reader | Resources | Rows | Status |
|---|---|---|---:|---:|---|
| `system_frequency_dmy_csv` | R1: day-first, naive (2014) | CSV / `csv` | 12 | 28,857,600 (11 members served) | **held** (zone unstated); October 2014 fails its key |
| `system_frequency_offset_csv` | R2: ISO + `%z` offset (2015-01 to 2018-12) | CSV / `csv` | 48 | 126,230,400 | eligible |
| `system_frequency_offset_zip` | R2 (2019-01 to 2019-12) | ZIP / `zip_member`, inner `f 2019 M.csv` | 12 | 31,536,000 | eligible |
| `system_frequency_gmt_zip` | R3: ISO, GMT-stated (2020-01 to 2022-03) | ZIP / `zip_member`, inner `fNew YYYY M.csv` | 27 | 70,934,400 | eligible |
| `system_frequency_gmt_csv` | R3 (2022-04 to 2026-08) | CSV / `csv` | 53 | 139,449,600 | eligible |

Silver rows total **397,008,000**: the nominal 399,686,400 less October 2014's 2,678,400,
which is not served (see Holds). The 152 bodies are 9.38 GB on disk (113 CSV bodies,
9,038,109,955 bytes; 39 ZIP bodies, 343,551,845 bytes, 3,045,943,575 bytes uncompressed),
about 12.1 GB of CSV text. The largest member is December 2019 (`f 2019 12.csv`,
90,757,307 bytes).

**Download links.** NESO serves each resource at

`https://api.neso.energy/dataset/cb1cc925-ecd8-4406-b021-3a3f368196e1/resource/<Id>/download/<filename>`

where `<Id>` is the resource id in the table above and the filename follows the month and
body: `f-YYYY-M.csv` (2014 to 2018), `f-2019-M.zip` (2019), `fnew-YYYY-M.zip` (2020-01 to
2022-03) and `fnew-YYYY-M.csv` (2022-04 on); `M` is the month number without a leading zero.
Examples:

- [January 2014 CSV](https://api.neso.energy/dataset/cb1cc925-ecd8-4406-b021-3a3f368196e1/resource/0cd6ff2e-62ca-4fbf-8417-18b3539530e6/download/f-2014-1.csv)
  (R1, held)
- [December 2019 ZIP](https://api.neso.energy/dataset/cb1cc925-ecd8-4406-b021-3a3f368196e1/resource/f0933bdd-1b0e-4dd3-aa7f-5498df1ba5b9/download/f-2019-12.zip)
  (R2 in a ZIP; the largest member)
- [August 2026 CSV](https://api.neso.energy/dataset/cb1cc925-ecd8-4406-b021-3a3f368196e1/resource/758fa76d-b645-4532-a532-ab49335ee4c3/download/fnew-2026-8.csv)
  (R3 with date-only midnights)

Resource names read "<Month> <YYYY> - Historic Frequency Data". From June 2022 the separator is
an en dash, and February 2024 has a trailing space. Neither matters to the registry, which
keys on the resource id. CKAN's `format` says `CSV` for all 152, ZIP bodies included.

**Capture.** One capture of each resource exists, all in the partition
`C:/gridflow-data/bronze/neso_data_portal/system_frequency/2026/10/08/` (written
2026-10-08, 11:27 to 11:37 UTC), plus one sidecar each (152 sidecars). Every body and ZIP
member has the header `dtm,f`, CRLF line ends, no BOM and strict UTF-8 content. Each ZIP holds
exactly one deflated CSV member. The registry family `system_frequency` is the **bronze
home**: every resource keeps `family: system_frequency`, so ingest, the frozen key and
coverage are unchanged. It has no record of its own, and each silver family is sibling-fed
from it (ADR-043 C-1).

## Families

### `system_frequency`

- Kind: tabular · archetype: SER · refresh: monthly · empty allowed: no
- ingest-only: no silver yet

This is the bronze home. It carries the 152 resources, their captures and the frozen key, but
it has **no schema record, so it produces no silver of its own**. Silver lives in the five
families below, at `C:/gridflow-data/silver/neso_data_portal/<family>/year=2026/month=10/`
(one Parquet file per resource). The `year=`/`month=` partition is the **capture** date
(2026-10-08), not the measurement date, so do not partition-prune by measurement year.

### `system_frequency_dmy_csv`

- Kind: tabular · archetype: SER · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| dtm | `dtm` | string | — | no | — | — |
| f | `f` | float64 | — | yes | — | — |

- Entity key: `resource_id`, `dtm`
- Latest: `whole_capture` per `resource_id`
- Temporal recipe: none: `timestamp_utc` is the capture time

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**R1, day-first and naive. HELD.** 12 resources (January to December 2014); 11 members are
served, with **28,857,600** rows. October 2014 (2,678,400 nominal rows) fails its key and is
not served. `dtm` is kept as the **raw vendor string** (dtype `string`), not as a timestamp.
Silver columns (11): `dtm`, `f`, `resource_id`, then `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version`. `f` is `float64`, nullable, with no bounds. The data values of this
family are **not published on this page**: it gives schema, row counts, clocks and label
shapes only. The 2014 resource descriptions specify a date-and-time layout with no zone, and
the captured bytes are day-first, so even the layout statement does not match the data.
NESO's GMT statement starts in January 2020, and no NESO statement of the 2014 zone was found
(see Holds).

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured file, read as UTC (gridflow
   `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). All 12 resources were last
   modified on **2023-03-24**. The vintage says when the **file** last changed, not when any
   second was measured.
2. **Event time: none.** The temporal recipe is `none`, because no instant in this family is
   evidenced. `timestamp_utc` (and `event_time`) is the **capture time** of the file, not a
   measurement time. Checked on silver (2026-10-16): each member has exactly one
   `timestamp_utc`, equal to its `capture_written_at` (2026-10-08). Do not use it as a time
   axis.

**Shape of the raw labels (structure only, no values).** The 2014 labels behave like a local
wall clock, but that is an inference from the label shapes and not a vendor statement.

- Members from March to September carry the first local hour of the following calendar month
  (March ends `01/04/2014 00:59:59`, and April starts `01/04/2014 01:00:00`).
- The labels `30/03/2014 01:00:00` to `01:59:59` are **absent** (3,600 labels).
- October starts `01/10/2014 01:00:00`, and the labels `26/10/2014 01:00:00` to `01:59:59`
  **occur twice** (3,600 excess rows; 7,200 rows take part in duplicate groups).

gridflow does not infer a zone from these shapes (`local_instant` is forbidden until
evidenced) and never resolves the repeated hour by file order. The family's selection and
key are the same as the other four (see Identity, selection and revisions), and the held
relation never joins the typed ones.

### `system_frequency_gmt_csv`

- Kind: tabular · archetype: SER · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| dtm | `dtm` | datetime | `%Y-%m-%d %H:%M:%S` or `%Y-%m-%d` | no | UTC | — |
| f | `f` | float64 | — | yes | — | — |

- Entity key: `resource_id`, `dtm`
- Latest: `whole_capture` per `resource_id`
- Overlap group: `system_frequency`
- Temporal recipe: utc_instant (`dtm`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**R3, ISO and naive, GMT-stated; eligible.** 53 resources (April 2022 to August 2026), CSV
bodies, **139,449,600** rows, 53 members. `dtm` is typed `datetime` in UTC (zone `UTC`), read
with `%Y-%m-%d %H:%M:%S` and, for any cell that is a bare date, the alternative `%Y-%m-%d`
(midnight). Silver columns (11): `dtm`, `f`, `resource_id`, then `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version`. `f` is `float64` Hz, nullable, no bounds. `dtm` spans
2022-04-01T00:00:00Z to 2026-08-31T23:59:59Z, and every month is complete.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured file, read as UTC (gridflow
   `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). The vintage is **per
   resource**: every second of one monthly file shares that file's vintage. The 53 vintages run from 2022-05-11 (April 2022) to 2026-09-09 (August 2026).
   Most are within about two weeks of month end; several are late uploads or re-uploads (see Cadence).
2. **Event time (`utc_instant` on `dtm`).** `timestamp_utc` equals `event_time` equals `dtm`,
   the measurement second in UTC (checked on every row of the silver, 2026-10-16). It is not
   the capture time. The package states the times are GMT from January 2020, so no London
   conversion applies and BST months begin at `00:00:00` UTC.

**August 2026 date-only midnights.** The August 2026 body renders each of its 31 midnights
as a bare date (`2026-08-01`) and every other second in full. The record's alternative
format reads them as midnight, so no row is dropped, and the family holds all 2,678,400
seconds of the month.

### `system_frequency_gmt_zip`

- Kind: tabular · archetype: SER · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| dtm | `dtm` | datetime | `%Y-%m-%d %H:%M:%S` or `%Y-%m-%d` | no | UTC | — |
| f | `f` | float64 | — | yes | — | — |

- Entity key: `resource_id`, `dtm`
- Latest: `whole_capture` per `resource_id`
- Overlap group: `system_frequency`
- Temporal recipe: utc_instant (`dtm`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**R3, ISO and naive, GMT-stated, inside ZIPs; eligible.** 27 resources (January 2020 to March
2022), each a deflated ZIP with one inner CSV named `fNew YYYY M.csv` (for example
`fNew 2020 4.csv`; see the `↳` rows above). Read through the `zip_member` reader (ADR-037). The
member must match the pattern and there must be exactly one. **70,934,400** rows, 27 members.
Same typing as `system_frequency_gmt_csv` (UTC, same two accepted formats). Silver columns
(13): `dtm`, `f`, `child_id`, `child_crc32`, `resource_id`, `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id`, `dataset_version`. `child_id` (string) and `child_crc32` (int64) are added by the ZIP container reader and identify the inner member (its name and CRC32). They are the two columns the CSV families lack. `dtm` spans 2020-01-01T00:00:00Z to 2022-03-31T23:59:59Z. The ZIP and CSV paths
read the same bytes to the same rows (tested with a ZIP rebuilt from a CSV member cut).

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured file, read as UTC (gridflow
   `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). The vintage is **per
   resource**: every second of one monthly file shares that file's vintage. The 27 vintages run from 2020-06-11 to 2022-04-06. January, March, April and May 2020 share the single
   upload date 2020-06-11, and February 2020 was uploaded on 2020-08-27, so the first
   2020 months became visible long after the measurements: an as-of query before 2020-06-11
   sees none of this family.
2. **Event time (`utc_instant` on `dtm`).** `timestamp_utc` equals `event_time` equals `dtm`,
   the measurement second in UTC. It is not the capture time.

### `system_frequency_offset_csv`

- Kind: tabular · archetype: SER · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| dtm | `dtm` | datetime | `%Y-%m-%d %H:%M:%S %z` | no | — | — |
| f | `f` | float64 | — | yes | — | — |

- Entity key: `resource_id`, `dtm`
- Latest: `whole_capture` per `resource_id`
- Overlap group: `system_frequency`
- Temporal recipe: utc_instant (`dtm`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**R2, ISO with a numeric offset on every row; eligible.** 48 resources (January 2015 to
December 2018), CSV bodies, **126,230,400** rows, 48 members. `dtm` is typed `datetime` from
`%Y-%m-%d %H:%M:%S %z` (zone not set; the offset carried in the cell is the zone evidence)
and converted to UTC. Silver columns (11): `dtm`, `f`, `resource_id`, then `timestamp_utc`, `published_at`, `bronze_capture_id`, `capture_written_at`, `event_time`, `available_at`, `source_run_id` and `dataset_version`. `f` is `float64` Hz, nullable, no bounds. `dtm` spans 2015-01-01T00:00:00Z to
2018-12-31T23:59:59Z. Every one of the 157,766,400 rows in the R2 months (this family and the
2019 ZIP family) carries an offset, which is why the family is eligible.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured file, read as UTC (gridflow
   `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). The vintage is **per
   resource**: every second of one monthly file shares that file's vintage. All 48 vintages are the single upload date 2023-03-24 (`available_at` between
   09:45 and 13:46 UTC that day), so an as-of query before 2023-03-24 sees none of this
   family, although its measurements date from 2015 to 2018.
2. **Event time (`utc_instant` on `dtm`).** `timestamp_utc` equals `event_time` equals `dtm`,
   the measurement second **converted from its own offset to UTC**. The displayed local date
   of a row can fall in the next month (a March row can read `... +0100` on 1 April), but the
   offset moves it back, and each member covers exactly its UTC month with no repeated or
   missing second. It is not the capture time.

### `system_frequency_offset_zip`

- Kind: tabular · archetype: SER · refresh: monthly · empty allowed: no

Schema, epoch 1:

| Vendor column | Silver column | Dtype | Format | Nullable | Zone | Vendor unit |
|---|---|---|---|---|---|---|
| dtm | `dtm` | datetime | `%Y-%m-%d %H:%M:%S %z` | no | — | — |
| f | `f` | float64 | — | yes | — | — |

- Entity key: `resource_id`, `dtm`
- Latest: `whole_capture` per `resource_id`
- Overlap group: `system_frequency`
- Temporal recipe: utc_instant (`dtm`)

| Clock | Meaning |
|---|---|
| `published_at` | CKAN `last_modified` of the captured file (ADR-030) |
| `available_at` | = `published_at` |

**R2 inside ZIPs; eligible.** 12 resources (January to December 2019), each a deflated ZIP with
one inner CSV named `f 2019 M.csv` (see the `↳` rows above), read through `zip_member`.
**31,536,000** rows, 12 members. Same typing as `system_frequency_offset_csv`; silver columns
(13): the 11 `system_frequency_offset_csv` columns plus `child_id` (string) and `child_crc32`
(int64), added by the ZIP container reader and identifying the inner member (placed after `f`:
`dtm`, `f`, `child_id`, `child_crc32`, `resource_id`, then the capture-stamp columns). `dtm` spans 2019-01-01T00:00:00Z to 2019-12-31T23:59:59Z.

**The two clocks for this family:**

1. **Vintage (`ckan_last_modified`).** `published_at` and `available_at` both equal the CKAN
   `last_modified` of the captured file, read as UTC (gridflow
   `@docs/DECISION_LOG/ADR-030-neso-data-portal-ckan-source.md`). The vintage is **per
   resource**: every second of one monthly file shares that file's vintage. All 12 vintages are the single upload date 2020-02-14, so an as-of query before
   2020-02-14 sees none of this family.
2. **Event time (`utc_instant` on `dtm`).** `timestamp_utc` equals `event_time` equals `dtm`,
   the offset-converted measurement second in UTC. It is not the capture time.

## Time semantics

| Rendering | Example of the shape | Zone evidence | gridflow treatment |
|---|---|---|---|
| R1 (2014) | `31/01/2014 23:59:59` | none in NESO's descriptions | raw string, `temporal: none`, **held** |
| R2 (2015 to 2019) | `2015-03-29 02:00:00 +0100` | the offset in every row | typed from `%z`, converted to UTC |
| R3 (2020-01 on) | `2023-10-01 00:00:00` | package statement of GMT from January 2020 | typed as UTC |

- **R2.** The offset is read for every row and the instant converted, never relabelled. At the
  2015 spring change the rows read `+0000` up to `00:59:59` and `+0100` from `02:00:00`. The
  January 2019 resource's field information describes the appended numeric zone, and the
  prose of all twelve 2019 resources says "given in Coordinated Universal Time (UTC)"; the `+0100` rows are nevertheless interpreted through their
  offsets, not relabelled as UTC.
- **R3.** The package page says the time values are all given in Greenwich Mean Time (GMT)
  starting January 2020 (<https://www.neso.energy/data-portal/system-frequency-data>). gridflow
  types the column as UTC on that statement. GMT is fixed all year, so there is no summer
  shift: months in British Summer Time still start at `00:00:00`. UTC-consistent month
  boundaries and row counts are measurements; the vendor statement is the evidence.
- **R1.** No NESO statement of the zone or of a repeated-hour rule was found in the checked
  descriptions and package page. That is a documented search outcome, not proof that no
  statement exists anywhere.
- **What `dtm` marks within the second.** NESO says `f` is the system frequency as measured at
  that second. Whether a reading is an instantaneous sample or a one-second aggregate, and
  whether `dtm` labels the start, end or instant of the second, is not documented.
  `TODO: verify` with NESO before using the series for sub-second or aggregation-sensitive
  work (ADR-043 residual).
- **Coverage.** Every R2 and R3 member covers exactly its UTC month, first second
  `YYYY-MM-01 00:00:00 UTC`, last second `23:59:59` of the last day, with no repeated and no
  missing second. A UTC day always has 86,400 rows (no 23- or 25-hour day, and not a
  settlement-period calendar). All 139 adjacent month edges from January 2015 to August 2026
  are contiguous (one second apart) with zero overlap, including the three format boundaries
  inside the typed range (December 2018 to January 2019, December 2019 to January 2020,
  March 2022 to April 2022).
- **The R1 to R2 edge** (December 2014 to January 2015) cannot be overlap-checked until R1's
  zone is documented. The raw labels are contiguous, but the physical instants are not known.

## Units and missing values

- **Unit: Hz** for `f`, from NESO's datastore field information (title "System Frequency
  (Hz)", unit `Hz`, type numeric), as captured by the profiler on the 2026-10-08 bodies. `dtm`
  carries no unit. The unit is the vendor's, not inferred from the column name `f`.
- **No vendor range.** NESO publishes no valid range for `f`, so the record applies no
  minimum or maximum and excludes no row (an invented bound would drop readings). The values
  observed in the four eligible families on 2026-10-16 are below. They are observations, not
  validation limits.

| Family | Rows | Null `f` | Zero or negative `f` | Lowest observed | Highest observed |
|---|---:|---:|---:|---:|---:|
| `system_frequency_offset_csv` | 126,230,400 | 0 | 0 | 49.569 | 50.410 |
| `system_frequency_offset_zip` | 31,536,000 | 0 | 0 | 48.787 | 50.380 |
| `system_frequency_gmt_zip` | 70,934,400 | 0 | 0 | 49.574 | 50.397 |
| `system_frequency_gmt_csv` | 139,449,600 | 0 | 0 | 49.275 | 50.352 |

- **Sentinels (FACTS g5).** None observed. The profiler's pass over the CSV bodies found no
  blank, no null and no non-numeric token in `f`; only decimal and integer-shaped cells. A
  whole-number cell is an ordinary number, not a code. No `-1`, `0`, `N/A` or blank run
  appears in the four typed families (no null and no zero or negative `f` over 368,150,400
  rows). The record declares no null token, so a future blank would stay a null and never
  exclude a row. `TODO: verify` that NESO defines no undocumented reading code, for example
  for an instrument outage; the series has no missing seconds, so a gap is not how an outage
  would show.
- The held R1 family's `f` values are not described here.

## Identity, selection and revisions

- **Entity key**: `(resource_id, dtm)` in every family. `resource_id` is **not a vendor
  column**: the engine stamps it from the capture's sidecar (ADR-039 P-2). For R2 and R3 `dtm`
  is the typed UTC instant, and for R1 it is the raw label string. A repeated key inside one
  member raises `DuplicateEntityKeyError` and fails the capture loudly; nothing is merged
  silently.
- **`_latest` selection** is `whole_capture` **per `resource_id`** (ADR-039). It serves each
  month's newest complete capture, ranked by `available_at`, then `capture_written_at`, then
  the capture id. A re-uploaded month **replaces its whole month**. A second that a
  re-upload drops is **absent from `_latest`** and still present at an as-of before the
  re-upload, because the as-of bound `available_at <= as_of` applies before ranking
  (`select_latest_vintage(as_of=...)`; the static views take no parameter, RULINGS 466). A
  key-based selection on the instant would resurrect a dropped second and is not used
  (ADR-043 C-2).
- **Base keeps every vintage** (RULINGS 466, 538). Nothing is deduplicated, on month edges or
  anywhere else. Until a second capture of any month exists, `_latest` equals the base in
  every family (one capture per resource at 2026-10-16).
- **Same instant in two members.** Both rows are kept and an `overlap` gap is reported by
  reconcile, never a silent dedup. At activation there were none (overlap 0).
- **A month re-uploaded under a new resource UUID** would be two resources serving the same
  seconds: both are served and reconcile reports `overlap` (ADR-043 FM-14). No vendor
  precedence is invented.
- **A new month needs a registry edit.** The bronze family has no name pattern, so only
  registered resources are fetched. A new month is reported missing by coverage until a
  registry entry adds it under the bronze home with `SILVER(system_frequency_gmt_csv)`
  (ADR-043 FM-15). That family's alternative format types any date-only midnight it carries.
- **Vintage caution (ADR-039 FM-12).** Each body's `ckan_last_modified` predates its capture, so
  `available_at <= as_of` does not prove the captured bytes were the ones published at that
  instant. An earlier version of the file may have been overwritten before capture.
  `available_at` is the upload time of the file, never a measurement time: as-of 2022-12-31 a
  2015 second is invisible, because its file was uploaded on 2023-03-24.

## Consuming the series

- **Union the four typed `_latest` relations** (`system_frequency_offset_csv`,
  `system_frequency_offset_zip`, `system_frequency_gmt_zip`, `system_frequency_gmt_csv`) to
  get 2015-01-01T00:00:00Z onward. They share the same columns. The overlap group
  `system_frequency` is checked at every reconcile: a second served by two families fails
  the reconcile and names it. At activation: 0 overlap.
- **The held R1 relation never joins the union.** Its `dtm` is a string and its
  `timestamp_utc` is a capture time. No consumer path presents it as eligible.
- **Never sum, average or resample across members without selecting through `_latest`** (or
  `select_latest_vintage(as_of=...)`). The base holds every vintage, so a re-uploaded month
  counted from the base would be counted twice (and a month served by two UUIDs, also).
- **No gold view.** Gold contracts are out of scope for this package (ruling 10, unit G). A
  continuous series is the consumer's union of the typed relations.
- **Volume.** A day is 86,400 rows, a month 2.4 to 2.7 million. Silver is 3.55 GB for the
  five families (see Activation). Query `_latest` over a bounded `dtm` range, not the whole
  relation.

## Activation (2026-10-16)

Merged as PR #127 (master `1c50e96`, RULINGS 864, ADR-043) and activated on the 2026-10-08
captures (RULINGS 866, 867; gridflow `@.planning/v0.22-RESULTS.md` section H).

| Family | Rows | Silver | Wall | Peak RSS |
|---|---:|---:|---:|---:|
| `system_frequency_dmy_csv` | 28,857,600 | 48.2 MB | 77 s | 1,863.5 MiB |
| `system_frequency_offset_csv` | 126,230,400 | 1,190.2 MB | 99 s | 1,800.1 MiB |
| `system_frequency_offset_zip` | 31,536,000 | 300.4 MB | 82 s | 1,673.4 MiB |
| `system_frequency_gmt_zip` | 70,934,400 | 677.9 MB | 95 s | 1,641.0 MiB |
| `system_frequency_gmt_csv` | 139,449,600 | 1,330.8 MB | 109 s | 1,563.1 MiB |

- Total 397,008,000 rows, equal to the plan; silver 3.55 GB.
- Coverage CLEAN (1,385 captured, 0 missing). `reconcile --all --cutoff 2026-10-13 --drain`
  exited 0 over 261 families with 0 gaps and `overlap` 0; adjudicated 62 (one new, October
  2014), stale 0.
- `_latest` equals the base for every family. DuckDB `count(*)` took 0.28 to 0.74 s per
  family, and a one-day range (86,400 rows) 0.21 to 0.44 s.
- Memory pilot on scratch copies (RULINGS 866): the largest member (December 2019 ZIP) alone
  peaked at 1,108.6 MiB. Twenty members cold peaked at 1,580.0 MiB (a cold ratio of 1.425,
  recorded, not hidden). The warmed comparison (8 + 5 against 8 + 20 members) was 1.068,
  within the 10 percent gate, and every peak was below 4 GiB. The gate was set on the warmed
  ratio (RULINGS 863).

## Implementation delta

- **ZIP bodies are not malformed CSV.** The earlier draft profile flagged `not_utf8` and
  `parse_error` for this package. Those were the 39 ZIP bodies read as CSV. All 152 bodies
  and members are strict UTF-8, and the `zip_member` reader reads the ZIPs.
- **The 2014 descriptions disagree with the bytes.** The resource descriptions give an ISO
  date-and-time layout; the 2014 bodies are day-first. The captured bytes are ground truth.
- **The generated schema tables show the vendor unit of `f` as "—".** The record carries no
  unit annotation, while NESO's field information says Hz. The unit on this page is the
  field information's.
- **The 2019 resource prose (all twelve) says UTC but summer rows carry `+0100`.** The offsets
  are read, not the prose (R2 above).
- **The vault's `coverage.md` row for this package is stale.** It lists 151 resources and
  "not started". The registry and the 2026-10-06 catalogue snapshot hold 152, and all 152 are
  now SILVER.
- **No gold layer and no union view** are implemented for this package (see Consuming the
  series).
## Cadence

- Registry refresh: monthly
- Vendor metadata (snapshot extras, verbatim):
  - Update Frequency: Monthly

The resource descriptions give no update time of day. For the months from January 2020
the catalogue shows a CKAN `last_modified` within 10 days of month end for 63 of 80 months
(69 within 14 days; a median of about 5 days; August 2026 was uploaded on 2026-09-09). That is an observation of
upload dates in the 2026-10-06 catalogue snapshot, not a vendor-stated publication lag.
Backfills and re-uploads are visible in the same dates:

- 2014 to 2018 (60 months) share the upload date 2023-03-24, and 2019 (12 months) shares
  2020-02-14.
- January to May 2020 were uploaded months after the measurements: January, March, April
  and May 2020 on 2020-06-11, and February 2020 on 2020-08-27.
- Individual later months carry much later dates than their neighbours: May 2022 on
  2024-06-07, April 2023 on 2023-06-07, August 2024 on 2024-10-31 and December 2023 on
  2026-04-17. They are late uploads or re-uploads of existing months.

`TODO: verify` whether any re-upload changed values, and the intended update time and
revision policy. Only more captures, compared pair by pair, can show a change: one capture of
each resource exists to date (2026-10-08). Whatever the capture schedule, the per-resource
`_latest` keeps each month's newest complete capture, and a month vanishing from the
catalogue would leave its last capture in `_latest`.

## Licence and attribution

- Licence: NESO Open Data Licence
- Attribution: Supported by National Energy SO Open Data

Licence text: [NESO Open Data Licence](https://www.neso.energy/data-portal/ngeso-open-licence).
gridflow outputs derived from this package carry the attribution line above.

## Holds

- `system_frequency_dmy_csv`: held: TODO: dtm: the zone, period start/end and clock of these datetimes are undocumented (local_instant is forbidden until evidenced). The 2014 day-first labels carry no offset and NESO's GMT statement starts January 2020; the labels 26/10/2014 01:00:00-01:59:59 repeat, so October 2014 fails its duplicate key (adjudicated, ADR-040), and the December 2014 to January 2015 edge cannot be overlap-checked until the zone is documented. (unit H-R1)

The silver output of `system_frequency_dmy_csv` exists on disk, but it is **held**: it is not
eligible for publication or for point-in-time model use until the question above is
answered. The record carries the hold (ADR-039 P-6, unit H-R1). Its schema, row counts and
clocks are described above, and this page does not publish its data values.

- **The question.** The zone, period start/end and clock of the 2014 day-first datetimes are
  undocumented. The 2014 labels carry no offset, NESO's GMT statement starts in January 2020,
  and the label shapes (March gap, October repeat) are not a zone declaration, so
  `local_instant` is forbidden until NESO evidences it.
- **What settles it.** A NESO statement of the 2014 zone and of the rule for the repeated
  October hour. If NESO is silent, the family stays held and is labelled "undocumented by
  NESO"; an assumed zone is never substituted.
- **October 2014 is adjudicated `failed`** (ADR-040, ruling 861), independently of the hold.
  Its labels `26/10/2014 01:00:00` to `01:59:59` each occur twice, so the member fails
  `(resource_id, dtm)` with `DuplicateEntityKeyError` and is not served. The adjudication's
  question to NESO: which of the two October 2014 rows of each repeated 01:00-01:59 label is
  the first (BST) hour? No file-order or `ambiguous=` resolution is applied.
- **Consequence for the series.** The served typed series begins 2015-01-01T00:00:00Z. The
  December 2014 to January 2015 edge cannot be overlap-checked, so the R1 to R2 boundary
  stays unproven.

The package-level `eligibility: eligible` in the front matter refers to the package registry
entry. The hold is per family and sits on `system_frequency_dmy_csv`. The other four
families are eligible with no hold (gridflow `@docs/neso_data_portal/eligibility.md`).
