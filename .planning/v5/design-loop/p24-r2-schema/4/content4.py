"""Designer 4, "One record, then many": copy for the silver stratum of each specimen.

Facts only from pack/SPECIMENS.md and specimens.json. Meanings reuse A's content.py wording where it still holds;
the value now shown beside each meaning replaces A's "e.g." examples, and local row counts are removed.
Every meaning is 14 words or fewer.
"""
from __future__ import annotations

# Template copy (every page)
H2 = "Schema and sample rows"
H3_ONE = "One row, field by field"
H3_MANY = "Eight rows"
KEY_NOTE = "A square marks the columns that identify a row."
LINEAGE_LABEL = ("Added to every row by the silver base transformer; "
                 "<code>query()</code> leaves these out.")
MANY_NOTE = "Only the schema columns that differ between rows are shown. The marked row is the one above."
SAME = "Same on every row"

LINEAGE = {
    "event_time": "Event instant: the row’s time column, else the target date",
    "available_at": "When the row became knowable: <code>published_at</code>, else the ingest time",
    "source_run_id": "Id of the pipeline run that wrote the row",
    "dataset_version": "Transformer version stamped on the row",
    "vintage_policy": "Which rule produced <code>available_at</code>",
}

FUELHH = {
    "id": "elexon/fuelhh",
    "file": "4-fuelhh",
    "title": "Generation by fuel type",
    "relation": "silver_elexon_fuelhh",
    "schema_cls": "ElexonFuelHH",
    "schema_src": "gridflow/schemas/elexon.py",
    "version": "2.0.0",
    "keys": ["settlement_date", "settlement_period", "fuel_type"],
    "record": 6,  # PS, -1454.0: the signed row
    "meaning": {
        "settlement_date": "GB settlement date, taken from the vendor start time",
        "settlement_period": "Half-hour of the day, 1 to 50 (46 or 50 on clock-change days)",
        "timestamp_utc": "Start of the half-hour",
        "fuel_type": "Elexon fuel-type code, uppercase as sent",
        "generation_mw": "MW for the period. Interconnectors signed, positive is import; PS signed, meaning undocumented",
        "published_at": "Vendor publish time",
        "data_provider": SAME,
        "ingested_at": "When the silver transform ran",
    },
    "many_cap": "All eight rows are settlement date 2026-09-26, period 25: 8 of its 20 codes.",
    "side": True,  # a two-column table: its caption sits beside it
}

SYSTEM_PRICES = {
    "id": "elexon/system_prices",
    "file": "4-system-prices",
    "title": "System sell and buy prices",
    "relation": "silver_elexon_system_prices_latest",
    "schema_cls": "ElexonSystemPrice",
    "schema_src": "gridflow/schemas/elexon.py",
    "version": "2.0.0",
    "keys": ["settlement_date", "settlement_period", "published_at"],
    "record": 7,  # SP29, -49.9: a negative price
    "meaning": {
        "settlement_date": "GB settlement date",
        "settlement_period": "Half-hour of the day, 1 to 50",
        "timestamp_utc": "Start of the period",
        "system_sell_price": "SSP, GBP/MWh; can be negative",
        "system_buy_price": "SBP, GBP/MWh; equal to SSP on every row",
        "net_imbalance_volume": "NIV, MWh; signed, sign convention undocumented",
        "run_type": "Always null: this endpoint has no such field",
        "price_derivation_code": "Vendor code: N, P or K",
        "published_at": "Vendor created time; a new version adds a row",
        "data_provider": SAME,
        "ingested_at": "When the silver transform ran",
    },
    "many_cap": "Settlement date 2026-09-20, periods 22 to 29, one version each.",
}

PHYSICAL_FLOWS = {
    "id": "entsog/physical_flows",
    "file": "4-physical-flows",
    "title": "Physical gas flows",
    "relation": "silver_entsog_physical_flows",
    "schema_cls": "EntsogPhysicalFlow",
    "schema_src": "gridflow/schemas/entsog.py",
    "version": "1.0.0",
    "keys": ["timestamp_utc", "point_key", "operator_key", "direction_key"],
    "record": 0,  # Bacton (IUK), National Gas TSO, exit: its pair is the next row
    "meaning": {
        "timestamp_utc": "Start of the operator’s gas day; operators start at different hours",
        "point_key": "ENTSOG point id",
        "point_label": "Point name",
        "operator_key": "Reporting operator; both sides of a point report, so a flow can appear twice",
        "operator_label": "Operator name",
        "direction_key": "<code>entry</code> or <code>exit</code>",
        "flow_gwh_per_day": "GWh/d, normalised from the vendor unit; a missing flow stays null",
        "unit": "Same on every row, after normalisation",
        "data_provider": SAME,
        "ingested_at": "When the silver transform ran; not declared in the schema class",
    },
    "many_cap": "Gas day 2026-09-21 at GB points; every row starts at 04:00 UTC.",
}

BMUNITS = {
    "id": "elexon/bmunits_reference",
    "file": "4-bmunits-reference",
    "title": "Balancing Mechanism units",
    "relation": "silver_elexon_bmunits_reference",
    "schema_cls": "ElexonBMUnit",
    "schema_src": "gridflow/schemas/elexon.py",
    "version": "1.1.0",
    "keys": ["bm_unit_id"],
    "record": 0,  # E_ABERDARE: no fuel type, has a GSP group
    "meaning": {
        "bm_unit_id": "Elexon BM unit id",
        "bm_unit_name": "Vendor name; often repeats the id",
        "fuel_type": "Vendor fuel type; null for most units",
        "registered_capacity_mw": "MW per registration; not additive across rows",
        "company_name": "Lead party",
        "gsp_group_id": "GSP group; nullable",
        "national_grid_bm_unit": "National Grid unit id; not an ENTSO-E EIC",
        "data_provider": SAME,
        "ingested_at": "When the silver transform ran",
    },
    "many_cap": "Eight units, chosen across id prefixes.",
}

SPECIMENS = [FUELHH, SYSTEM_PRICES, PHYSICAL_FLOWS, BMUNITS]
