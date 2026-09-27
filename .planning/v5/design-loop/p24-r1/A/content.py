"""Designer A, "The section": per-specimen content. Every fact comes from pack/SPECIMENS.md or specimens.json.

Prose fields (oneliner, what, uses, caveats, related notes, gold notes, captions, index notes) are NEW COPY.
"""
from __future__ import annotations

FUELHH = {
    "file": "A-fuelhh",
    "slug": "fuelhh",
    "vendor": "Elexon BMRS",
    "key": "elexon/fuelhh",
    "title": "Generation by fuel type",
    "code": 'Elexon dataset <code>FUELHH</code>, “Half-hourly Generation Outturn by Fuel Type”',
    "oneliner": ("Great Britain’s generation outturn for every half-hour settlement period, one MW value per "
                 "Elexon fuel-type code."),
    "facts": [
        ("Grain", "One row per settlement period and fuel-type code"),
        ("Cadence", "Every 30 minutes"),
        ("Units", "MW"),
        ("History", "1 Sep 2021 to 26 Sep 2026 held locally; 7 to 9 Sep 2026 missing"),
        ("Publication lag", "Published at the period end on 99.82% of rows"),
    ],
    "chart_h2": "Generation by fuel, 20 to 26 September 2026",
    "chart_cap": ("Silver <code>elexon/fuelhh</code>, MW, hourly: each point is the mean of an hour’s two half-hours, "
                  "with a group’s codes summed first. Values stack above zero when positive and below it when "
                  "negative; nothing is clipped."),
    "what": ("Elexon’s outturn by fuel type for each GB settlement period: one MW figure per code, from CCGT and wind "
             "to each interconnector. Recent half-hours carry 20 codes. The ten interconnector codes are signed, "
             "positive for imports to GB, and pumped storage (PS) is signed too, with the sign’s meaning "
             "undocumented. There is no solar code."),
    "uses": [
        "Fuel-mix and residual-demand features for a GB power price model.",
        "Net interconnector flows by link, from ten signed codes.",
        "Checking a wind generation forecast against outturn.",
    ],
    "endpoint": ["GET https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH",
                 "    ?publishDateTimeFrom=&lt;UTC Z&gt;",
                 "    &amp;publishDateTimeTo=&lt;UTC Z&gt;",
                 "    &amp;page=&lt;n&gt;"],
    "cli": [("gridflow ingest elexon fuelhh --start 2026-09-20 --end 2026-09-26", "bronze only"),
            ("gridflow pipeline elexon fuelhh --start 2026-09-20 --end 2026-09-26", "bronze to silver")],
    "bronze_note": ("From the Elexon Insights API. <code>gridflow ingest</code> writes the raw response to bronze; "
                    "<code>gridflow pipeline</code> carries it on to silver."),
    "relation": "silver_elexon_fuelhh",
    "schema_cls": "ElexonFuelHH",
    "schema_src": "gridflow/schemas/elexon.py",
    "version": "2.0.0",
    "keys": ["settlement_date", "settlement_period", "fuel_type"],
    "schema": [
        ("settlement_date", "Date", "GB settlement date, taken from the vendor start time"),
        ("settlement_period", "Int32", "Half-hour of the day, 1 to 50 (46 or 50 on clock-change days)"),
        ("timestamp_utc", "Datetime(us, UTC)", "Start of the half-hour"),
        ("fuel_type", "String", "Elexon fuel-type code, uppercase as sent"),
        ("generation_mw", "Float64", "MW for the period. Interconnectors signed, positive is import; PS signed, "
                                     "meaning undocumented"),
        ("published_at", "Datetime(us, UTC)", "Vendor publish time"),
        ("data_provider", "String", "Always <code>elexon</code>"),
        ("ingested_at", "Datetime(us, UTC)", "When the silver transform ran"),
    ],
    "lineage": ("event_time, available_at, source_run_id, dataset_version",
                "Added to every row by the silver base transformer"),
    "df_cap": "Silver rows for settlement date 2026-09-26, period 25: 8 of its 20 codes.",
    "df": "elexon/fuelhh",
    "source": "elexon",
    "nb_cells": ['df = data.elexon.query("fuelhh", "2026-09-20", "2026-09-26")'],
    "gold_note": ("Returns a pandas DataFrame from the DuckDB relation <code>silver_elexon_fuelhh</code>, filtered on "
                  "<code>settlement_date</code> with both ends included: 6,720 rows for this week. Lineage columns "
                  "are dropped."),
    "caveats": [
        ("No solar.", "FUELHH has no solar code, so solar outturn has to come from another dataset."),
        ("Eleven codes are signed:", "ten interconnectors (positive is import to GB) and PS. Negatives are "
                                     "routine: INTIRL is negative in 70.3% of half-hours."),
        ("The code set changes.", "INTELEC arrives in 2021, INTVKL in 2023 and INTGRNL in 2024, so a half-hour "
                                  "holds 17 to 20 rows."),
    ],
    "related": [
        ("elexon/fuelinst", "Instantaneous outturn by fuel type, from the same connector"),
        ("neso_data_portal/historic_generation_mix", "Where solar outturn lives"),
        ("elexon/bmunits_reference", "Shares the fuel-type codes"),
        ("elexon/indo", "Demand, used to check the interconnector sign"),
    ],
}

SYSTEM_PRICES = {
    "file": "A-system-prices",
    "slug": "system_prices",
    "vendor": "Elexon BMRS",
    "key": "elexon/system_prices",
    "title": "System sell and buy prices",
    "code": ('Elexon dataset <code>DISEBSP</code>, “System Sell Price and System Buy Price per settlement '
             'period”'),
    "oneliner": ("The GB imbalance price for each half-hour settlement period, with the net imbalance volume, "
                 "in GBP/MWh."),
    "facts": [
        ("Grain", "One row per settlement period per published version (append-only)"),
        ("Cadence", "Every 30 minutes"),
        ("Units", "GBP/MWh; net imbalance volume in MWh"),
        ("History", "1 Sep 2021 to 22 Sep 2026 held locally, no missing dates"),
        ("Publication lag", "Median 52 min in 2021 to 2023, about 24.7 h in 2024 to 2026"),
    ],
    "chart_h2": "System sell price, 19 to 22 September 2026",
    "chart_cap": ("Silver <code>elexon/system_prices</code>, latest version of each period, GBP/MWh: 192 native "
                  "half-hours, no aggregation. The buy price is identical in this window, so one line carries "
                  "both."),
    "what": ("Elexon’s system sell price (SSP) and system buy price (SBP) are the cash-out prices that settle "
             "imbalances in each GB settlement period, in GBP/MWh. In every row held locally, from September 2021, "
             "the two are equal. Each row also carries the net imbalance volume in MWh and a price derivation code "
             "(N, P or K)."),
    "uses": [
        "The target for an imbalance price forecast.",
        "Pricing the cash-out exposure of a position left out of balance.",
        "Studying negative prices: 4,052 half-hours below zero since September 2021.",
    ],
    "endpoint": ["GET https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement",
                 "    /system-prices/{YYYY-MM-DD}",
                 "    ?page=&lt;n&gt;"],
    "cli": [("gridflow ingest elexon system_prices --start 2026-09-19 --end 2026-09-22", "bronze only"),
            ("gridflow pipeline elexon system_prices --start 2026-09-19 --end 2026-09-22", "bronze to silver")],
    "bronze_note": ("From the Elexon Insights API, one settlement date per request. <code>gridflow ingest</code> "
                    "writes the raw response to bronze; <code>gridflow pipeline</code> carries it on to silver."),
    "relation": "silver_elexon_system_prices_latest",
    "schema_cls": "ElexonSystemPrice",
    "schema_src": "gridflow/schemas/elexon.py",
    "version": "2.0.0",
    "keys": ["settlement_date", "settlement_period", "published_at"],
    "schema": [
        ("settlement_date", "Date", "GB settlement date"),
        ("settlement_period", "Int32", "Half-hour of the day, 1 to 50"),
        ("timestamp_utc", "Datetime(us, UTC)", "Start of the period"),
        ("system_sell_price", "Float64", "SSP, GBP/MWh"),
        ("system_buy_price", "Float64", "SBP, GBP/MWh; equal to SSP on every row"),
        ("net_imbalance_volume", "Float64", "NIV, MWh; sign convention undocumented"),
        ("run_type", "String", "Null on every row: this endpoint has no such field"),
        ("price_derivation_code", "String", "Vendor code: N, P or K"),
        ("published_at", "Datetime(us, UTC)", "Vendor created time; a new version adds a row"),
        ("data_provider", "String", "Always <code>elexon</code>"),
        ("ingested_at", "Datetime(us, UTC)", "When the silver transform ran"),
    ],
    "lineage": ("event_time, available_at, source_run_id, dataset_version, vintage_policy",
                "Added to every row by the silver base transformer"),
    "df_cap": "Silver rows for settlement date 2026-09-20, periods 22 to 29: one version each.",
    "df": "elexon/system_prices",
    "source": "elexon",
    "nb_cells": ['df = data.elexon.query("system_prices", "2026-09-19", "2026-09-22")'],
    "gold_note": ("Reads <code>silver_elexon_system_prices_latest</code>, so each period comes back once; the raw "
                  "parquet keeps every version. Filtered on <code>settlement_date</code>, both ends included."),
    "caveats": [
        ("Silver is append-only:", "96,793 rows cover 88,694 periods. Read the <code>_latest</code> view, as the "
                                   "workbench does, or dedupe on <code>available_at</code>."),
        ("SSP equals SBP", "on every row since September 2021, so one line carries both."),
        ("Negative prices are routine:", "4,052 periods since September 2021, and 34 of the 192 in the chart."),
    ],
    "related": [
        ("neso/carbon_intensity", "Joined in the workbench by <code>data.imbalance_context()</code>"),
        ("elexon/mid", "Read by the workbench’s day-ahead benchmark"),
        ("system_marginal_price", "A gold view built over this table"),
    ],
}

PHYSICAL_FLOWS = {
    "file": "A-physical-flows",
    "slug": "physical_flows",
    "vendor": "ENTSO-G",
    "key": "entsog/physical_flows",
    "title": "Physical gas flows",
    "code": 'ENTSOG Transparency Platform, <code>operationalData</code> indicator “Physical Flow”',
    "oneliner": ("Daily gas flow at each European transmission point, per operator and direction, in GWh/d."),
    "facts": [
        ("Grain", "One row per gas day, point, operator and direction"),
        ("Cadence", "Daily; each operator’s gas day starts at its own hour"),
        ("Units", "GWh/d"),
        ("History", "14 gas days held locally: 1 to 5 Aug and 13 to 21 Sep 2026"),
        ("Publication lag", "Not established; available_at is the ingest time"),
    ],
    "chart_h2": "Daily flow at two GB points, August and September 2026",
    "chart_cap": ("Silver <code>entsog/physical_flows</code>, National Gas TSO, GWh/d: one native value per gas day, "
                  "nothing averaged. These are all the gas days held locally; the gap has no rows and is not "
                  "interpolated."),
    "what": ("ENTSOG’s Physical Flow indicator: for each gas day, the flow that each transmission operator reports "
             "at each point, marked entry or exit. gridflow normalises every value to GWh/d. Both sides of a "
             "cross-border point report, so one physical flow can appear twice. About 983 rows arrive per gas day."),
    "uses": [
        "GB supply features for a gas price model: terminal and LNG entries.",
        "Tracking pipeline flows between GB and the continent, such as Bacton to Zeebrugge.",
    ],
    "endpoint": ["GET https://transparency.entsog.eu/api/v1/operationalData",
                 "    ?limit=-1&amp;timeZone=UCT",
                 "    &amp;from=YYYY-MM-DD&amp;to=YYYY-MM-DD",
                 "    &amp;indicator=Physical%20Flow&amp;periodType=day"],
    "cli": [("gridflow ingest entsog physical_flows --start 2026-09-13 --end 2026-09-21", "bronze only"),
            ("gridflow pipeline entsog physical_flows --start 2026-09-13 --end 2026-09-21", "bronze to silver")],
    "bronze_note": ("From the ENTSOG Transparency Platform, the whole system in one fetch. <code>gridflow ingest"
                    "</code> writes the raw response to bronze; <code>gridflow pipeline</code> carries it on to "
                    "silver."),
    "relation": "silver_entsog_physical_flows",
    "schema_cls": "EntsogPhysicalFlow",
    "schema_src": "gridflow/schemas/entsog.py",
    "version": "1.0.0",
    "keys": ["timestamp_utc", "point_key", "operator_key", "direction_key"],
    "schema": [
        ("timestamp_utc", "Datetime(us, UTC)", "Start of the operator’s gas day"),
        ("point_key", "String", "ENTSOG point id, e.g. ITP-00005"),
        ("point_label", "String", "Point name, e.g. Bacton (IUK)"),
        ("operator_key", "String", "Reporting operator id, e.g. UK-TSO-0001"),
        ("operator_label", "String", "Operator name, e.g. National Gas TSO"),
        ("direction_key", "String", "<code>entry</code> or <code>exit</code>"),
        ("flow_gwh_per_day", "Float64", "Flow in GWh/d, normalised from the vendor unit; nullable"),
        ("unit", "String", "Always <code>GWh/d</code>"),
        ("data_provider", "String", "Always <code>entsog</code>"),
        ("ingested_at", "Datetime(us, UTC)", "When the silver transform ran; added by the transformer, not in the "
                                             "schema class"),
    ],
    "lineage": ("event_time, available_at, source_run_id, dataset_version",
                "Added to every row by the silver base transformer"),
    "df_cap": "Silver rows for gas day 2026-09-21 at GB points (04:00 UTC).",
    "df": "entsog/physical_flows",
    "source": "entsog",
    "nb_cells": ['df = data.entsog.query("physical_flows", "2026-09-13", "2026-09-21")'],
    "gold_note": ("Filters <code>timestamp_utc</code> from 00:00 UTC on the start date to 00:00 UTC after the end "
                  "date. Operators whose gas day starts at 21:00 to 23:00 UTC the day before miss the first day."),
    "caveats": [
        ("Local history is 14 gas days", "in two blocks: 1 to 5 August and 13 to 21 September 2026."),
        ("Both sides of a point report,", "so summing every row double counts: at Bacton (IUK) on 21 September, "
                                          "both sides read 175.165952 GWh/d."),
        ("Flows can be null:", "2,499 rows, and every day for 176 series such as Avonmouth LNG. Do not zero-fill."),
    ],
    "related": [
        ("entsog/aggregated_physical_flows", "The same indicator at zone level"),
        ("entsog/nominations", "Same endpoint, Nomination indicator"),
        ("entsog/allocations", "Same endpoint, Allocation indicator"),
    ],
}

BMUNITS = {
    "file": "A-bmunits-reference",
    "slug": "bmunits_reference",
    "vendor": "Elexon BMRS",
    "key": "elexon/bmunits_reference",
    "title": "Balancing Mechanism units",
    "code": 'Elexon reference endpoint <code>/reference/bmunits/all</code>, “All BM Unit reference data”',
    "oneliner": ("The register of Balancing Mechanism units: id, name, fuel type, registered capacity, lead party "
                 "and GSP group."),
    "facts": [
        ("Grain", "One row per BM unit"),
        ("Cadence", "Snapshot, scheduled weekly, overwritten each run"),
        ("Units", "Registered capacity in MW, per registration"),
        ("History", "Current snapshot only (26 Sep 2026)"),
        ("Publication lag", "Not established"),
    ],
    "chart_h2": "3,014 BM units by fuel type, snapshot of 26 September 2026",
    "chart_cap": ("Silver <code>elexon/bmunits_reference</code>, count of BM units in one snapshot; null is kept as "
                  "its own group. Counts only: registered capacity is not additive, so it is not summed."),
    "what": ("Elexon’s reference list of registered BM units, fetched whole in one call and overwritten on every run. "
             "It is the lookup that turns a <code>bm_unit_id</code> in unit-level balancing data into a name, a lead "
             "party and, for 499 of 3,014 units, a fuel type. Registered capacity is per registration and does not "
             "add up."),
    "uses": [
        "Joining BOAL or PN data to a unit’s lead party and fuel type.",
        "Grouping units by lead party or GSP group.",
    ],
    "endpoint": ["GET https://data.elexon.co.uk/bmrs/api/v1/reference/bmunits/all"],
    "cli": [("gridflow pipeline elexon bmunits_reference", "no dates: one fetch of the whole list")],
    "bronze_note": ("From the Elexon Insights API: no parameters and no pages. <code>gridflow pipeline</code> writes "
                    "the raw response to bronze and carries it on to silver."),
    "relation": "silver_elexon_bmunits_reference",
    "schema_cls": "ElexonBMUnit",
    "schema_src": "gridflow/schemas/elexon.py",
    "version": "1.1.0",
    "keys": ["bm_unit_id"],
    "schema": [
        ("bm_unit_id", "String", "Elexon BM unit id, e.g. T_DRAXX-1"),
        ("bm_unit_name", "String", "Vendor name; often repeats the id"),
        ("fuel_type", "String", "Vendor fuel type; null on 2,515 of 3,014 rows"),
        ("registered_capacity_mw", "Float64", "MW per registration; not additive across rows"),
        ("company_name", "String", "Lead party"),
        ("gsp_group_id", "String", "GSP group, e.g. _A; null on 1,822 rows"),
        ("national_grid_bm_unit", "String", "National Grid unit id, e.g. ABERU-1; not an ENTSO-E EIC"),
        ("data_provider", "String", "Always <code>elexon</code>"),
        ("ingested_at", "Datetime(us, UTC)", "When the silver transform ran"),
    ],
    "lineage": ("event_time, available_at, source_run_id, dataset_version",
                "Added to every row by the silver base transformer"),
    "df_cap": "Silver rows from the snapshot of 2026-09-26, chosen across id prefixes.",
    "df": "elexon/bmunits_reference",
    "source": "elexon",
    "nb_cells": ['df = data.elexon.tail("bmunits_reference", n=3014)',
                 'data.sql("SELECT * FROM silver_elexon_bmunits_reference")'],
    "gold_note": ("Use <code>tail()</code> or <code>data.sql()</code>. A <code>query()</code> date range filters "
                  "this table on <code>ingested_at</code>, so it returns 0 rows."),
    "caveats": [
        ("83% of units have no fuel type", "(2,515 of 3,014), so any fuel breakdown covers 499 units."),
        ("Capacity does not add up:", "it is per registration, and the null-fuel rows alone sum to 727,551 MW."),
        ("One snapshot, overwritten each run,", "with keyless vendor rows dropped, so counts drift: 2,969 units on "
                                                "9 September, 3,014 on 26 September."),
    ],
    "related": [
        ("elexon/boal", "Bid-offer acceptances, joined on <code>bm_unit_id</code>"),
        ("elexon/pn", "Physical notifications, joined on <code>bm_unit_id</code>"),
        ("elexon/uou2t14d", "Availability per unit"),
        ("elexon/fuelhh", "Shares the fuel-type codes; interconnector flow lives there"),
    ],
}

SPECIMENS = [FUELHH, SYSTEM_PRICES, PHYSICAL_FLOWS, BMUNITS]
