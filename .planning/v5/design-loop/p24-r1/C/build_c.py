"""Designer C, "The plate": page template and specimen content. Run this file to write the four boards.

Facts come from ../pack; prose lines (one-liner, what it is, how it's used, plate notes, captions) are NEW COPY.
"""
from __future__ import annotations

import json
import math
import re

from gen_c import (CHART, HERE, HORIZON, INK, OLIVE, PETROL, SPEC, T_BRONZE, T_GOLD, T_SILVER, T_TOP, W, esc, f,
                   patterns, plate_flows, plate_fuelhh, plate_prices, plate_units, smooth, wave)

HEIGHTS = {"fuelhh": 4000, "system-prices": 4000, "physical-flows": 4000, "bmunits-reference": 4000}
if (HERE / "heights.json").exists():
    HEIGHTS.update(json.loads((HERE / "heights.json").read_text(encoding="utf-8")))
SHOW_HORIZON = True


def nul() -> str:
    return '<span class="nul">null</span>'


def sample(spec: str, cols: list[str]) -> tuple[list[str], list[list[str]]]:
    out = []
    for r in SPEC[spec]["sample_rows"]["rows"]:
        line = []
        for c in cols:
            v = r[c]
            if v is None:
                line.append(nul())
            elif isinstance(v, float):
                line.append(repr(v))
            elif isinstance(v, str) and re.match(r"\d{4}-\d\d-\d\dT", v):
                line.append(v.replace("+00:00", "Z"))
            else:
                line.append(esc(str(v)))
        out.append(line)
    return cols, out


SETUP = ('<span class="k">from</span> gridflow_models <span class="k">import</span> setup_notebook\n'
         'data, models, common = setup_notebook()')


def hl(code: str) -> str:
    return re.sub(r'"[^"]*"', lambda m: f'<span class="s">{m.group(0)}</span>', esc(code))


PAGES = {
    "fuelhh": dict(
        spec="elexon/fuelhh", vendor="Elexon BMRS", title="Generation by fuel type",
        idline='<code>elexon/fuelhh</code>, from Elexon’s <code>FUELHH</code>: “Half-hourly Generation Outturn by '
               'Fuel Type”',
        oneliner="GB generation outturn by fuel type: one MW value for every half-hour settlement period and every "
                 "Elexon fuel code, interconnectors included.",
        plate_title="Generation by fuel, 20 to 26 September 2026",
        plate_note='Source <code>elexon/fuelhh</code>, silver, MW. Settlement dates 20 to 26 September 2026, by '
                   'UTC hour: each code is the mean of its two half-hours, summed within a band, never averaged '
                   'across fuels. Signed codes split by sign, positive stacking up from zero and negative down; '
                   'for interconnectors, positive means import to GB.',
        plate=plate_fuelhh,
        what="Elexon publishes GB generation outturn for every settlement period, split by fuel type. gridflow keeps "
             "one row per settlement date, period and fuel code: twenty codes today, from <code>WIND</code>, "
             "<code>CCGT</code> and <code>NUCLEAR</code> to pumped storage and ten interconnectors. The interconnector "
             "codes are signed, positive for imports to GB. There is no solar code.",
        uses=["Wind and gas output by half-hour, as features for a GB price or imbalance model.",
              "Interconnector flows border by border, read from the signed <code>INT</code> codes.",
              "Outturn to score a wind generation forecast against, half-hour by half-hour."],
        facts=[("Grain", "One row per settlement period and fuel code"),
               ("Cadence", "Every 30 minutes, 17 to 20 codes per half-hour"),
               ("Unit", "MW"),
               ("Local history", "1 Sep 2021 to 26 Sep 2026; 7 to 9 Sep 2026 missing"),
               ("Publication lag", "At the period end (30 min after its start) on 99.82% of rows; at most 271 min"),
               ("Rows", "1,682,517; 29,760 in August 2026")],
        caveats=[("No solar.", "FUELHH has no solar code at all, so solar outturn has to come from another dataset."),
                 ("Eleven codes are signed.", "The ten <code>INT</code> codes (positive = import to GB) and "
                  "<code>PS</code>, whose sign is undocumented. Negatives are routine: "
                  "<code>INTIRL</code> is negative in 70.3% of half-hours, <code>PS</code> in 54.7%."),
                 ("The code set changes.", "<code>INTELEC</code> starts on 14 Sep 2021, <code>INTVKL</code> on 12 Jul "
                  "2023 and <code>INTGRNL</code> on 19 Mar 2024, so a half-hour holds 17 to 20 rows. A stray "
                  "<code>INTELE</code> has nine zero rows on 10 Sep 2021.")],
        endpoint=["GET https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH",
                  "    ?publishDateTimeFrom=<UTC Z>", "    &publishDateTimeTo=<UTC Z>", "    &page=<n>"],
        cli=[("gridflow ingest elexon fuelhh --start 2026-09-20 --end 2026-09-26", "bronze only"),
             ("gridflow pipeline elexon fuelhh --start 2026-09-20 --end 2026-09-26", "bronze to silver")],
        schema_class="ElexonFuelHH", version="2.0.0",
        schema=[("settlement_date", "Date", "GB settlement date, derived from the vendor start time"),
                ("settlement_period", "Int32", "Half-hour index 1 to 50 (46 or 50 on clock-change days)"),
                ("timestamp_utc", "Datetime(us, UTC)", "Start of the half-hour (vendor startTime)"),
                ("fuel_type", "String", "Elexon fuel-type code, uppercase as sent"),
                ("generation_mw", "Float64", "MW for the period. INT codes signed, positive = import to GB; PS signed, "
                                             "meaning undocumented"),
                ("published_at", "Datetime(us, UTC)", "Vendor publication time"),
                ("data_provider", "String", "Always <code>elexon</code>"),
                ("ingested_at", "Datetime(us, UTC)", "When the silver transform ran, not the bronze fetch")],
        lineage="<code>event_time</code>, <code>available_at</code>, <code>source_run_id</code> and "
                "<code>dataset_version</code> are added by the silver base class; <code>available_at</code> is "
                "<code>published_at</code>, else the ingest time.",
        sample=sample("elexon/fuelhh", ["settlement_date", "settlement_period", "timestamp_utc", "fuel_type",
                                        "generation_mw", "published_at"]),
        sample_cap="Settlement date 2026-09-26, period 25: 8 of the 20 codes. Every row also carries "
                   "<code>data_provider</code> elexon and <code>dataset_version</code> 2.0.0.",
        wb=['df = data.elexon.query("fuelhh", "2026-09-20", "2026-09-26")'],
        wb_note="Returns a pandas DataFrame: 6,720 rows for that range, with <code>event_time</code>, "
                "<code>available_at</code>, <code>source_run_id</code> and <code>dataset_version</code> left out. "
                "<code>\"fuel_generation\"</code> names the same table.",
        related=[("elexon/fuelinst", "Same connector: instantaneous generation outturn by fuel type."),
                 ("elexon/bmunits_reference", "The BM unit register, which uses the same fuel-type codes."),
                 ("elexon/indo", "The demand series the interconnector sign is checked against."),
                 ("neso_data_portal/historic_generation_mix", "Where solar outturn lives.")]),
    "system-prices": dict(
        spec="elexon/system_prices", vendor="Elexon BMRS", title="System sell and buy prices",
        idline='<code>elexon/system_prices</code>, from Elexon’s settlement system prices (response dataset '
               '<code>DISEBSP</code>)',
        oneliner="GB imbalance (cash-out) prices for every half-hour settlement period: the system sell and buy "
                 "price in £/MWh, with the net imbalance volume.",
        plate_title="System sell price, 19 to 22 September 2026",
        plate_note='Source <code>elexon/system_prices</code>, silver, latest vintage per period, £/MWh. '
                   'Settlement dates 19 to 22 September 2026, in UTC. Native half-hourly values, no aggregation. '
                   'The buy price is identical in every period, so one line carries both.',
        plate=plate_prices,
        what="For each settlement period Elexon publishes the system sell price (SSP) and system buy price (SBP), the "
             "prices imbalances are cashed out at, with the net imbalance volume (NIV) in MWh. The two prices are "
             "equal on every row gridflow holds. Silver keeps every vintage the vendor sends, so a period can "
             "appear more than once.",
        uses=["The target series for an imbalance price forecast.",
              "Valuing a position’s imbalance exposure, half-hour by half-hour.",
              "Finding and counting negative-price periods, which are routine."],
        facts=[("Grain", "One row per settlement period per vendor vintage"),
               ("Cadence", "Every 30 minutes"),
               ("Units", "£/MWh for prices; MWh for NIV"),
               ("Local history", "1 Sep 2021 to 22 Sep 2026, no missing dates"),
               ("Publication lag", "Median 52 min after period start in 2021 to 2023, about 24.7 h in 2024 to 2026; "
                                   "the cause is not established"),
               ("Rows", "96,793, covering 88,694 periods")],
        caveats=[("Silver is append-only.", "96,793 rows cover 88,694 periods. Read the latest view, as the workbench "
                  "does, or dedupe on <code>available_at</code> before plotting."),
                 ("SSP equals SBP.", "On every row since September 2021, so one line carries both."),
                 ("Negative prices are routine.", "4,052 periods since September 2021 and 34 of the 192 in the "
                  "chart above.")],
        endpoint=["GET https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/{YYYY-MM-DD}",
                  "    ?page=<n>"],
        cli=[("gridflow ingest elexon system_prices --start 2026-09-19 --end 2026-09-22", "bronze only"),
             ("gridflow pipeline elexon system_prices --start 2026-09-19 --end 2026-09-22", "bronze to silver")],
        schema_class="ElexonSystemPrice", version="2.0.0, append-only",
        schema=[("settlement_date", "Date", "GB settlement date"),
                ("settlement_period", "Int32", "Half-hour index 1 to 50"),
                ("timestamp_utc", "Datetime(us, UTC)", "Period start"),
                ("system_sell_price", "Float64", "SSP, £/MWh; schema bound −500 to 10,000"),
                ("system_buy_price", "Float64", "SBP, £/MWh; equal to SSP on every row"),
                ("net_imbalance_volume", "Float64", "NIV, MWh; sign convention not documented"),
                ("run_type", "String", "Settlement run; null on every row, as this endpoint has no such field"),
                ("price_derivation_code", "String", "Vendor priceDerivationCode: N, P and K observed"),
                ("published_at", "Datetime(us, UTC)", "Vendor createdDateTime: the vintage stamp"),
                ("data_provider", "String", "Always <code>elexon</code>"),
                ("ingested_at", "Datetime(us, UTC)", "When the silver transform ran")],
        lineage="<code>event_time</code>, <code>available_at</code>, <code>source_run_id</code>, "
                "<code>dataset_version</code> and <code>vintage_policy</code> (vendor, on every row) are added by the "
                "silver base class.",
        sample=sample("elexon/system_prices", ["settlement_period", "timestamp_utc", "system_sell_price",
                                               "system_buy_price", "net_imbalance_volume", "price_derivation_code",
                                               "published_at"]),
        sample_cap="Settlement date 2026-09-20, periods 22 to 29, one vintage each; <code>run_type</code> is null on "
                   "every row.",
        wb=['df = data.elexon.query("system_prices", "2026-09-19", "2026-09-22")'],
        wb_note="Reads <code>silver_elexon_system_prices_latest</code>, so vintages are already collapsed to one row "
                "per period; the raw parquet is not. <code>data.imbalance_context(start, end)</code> adds NESO carbon "
                "intensity.",
        related=[("neso/carbon_intensity", "Joined to these prices in the workbench’s imbalance context."),
                 ("elexon/mid", "The workbench’s GB day-ahead benchmark."),
                 ("system_marginal_price", "A gold view built over this table.")]),
    "physical-flows": dict(
        spec="entsog/physical_flows", vendor="ENTSO-G", title="Physical gas flows",
        idline='<code>entsog/physical_flows</code>, from the ENTSOG Transparency Platform’s operational data, '
               'indicator “Physical Flow”',
        oneliner="Daily physical gas flow in GWh/d for each operator, point and direction on Europe’s transmission "
                 "systems.",
        plate_title="Daily flow at two GB points, all 14 gas days held",
        plate_note='Source <code>entsog/physical_flows</code>, silver, GWh/d, National Gas TSO rows. Every gas '
                   'day in local silver: 1 to 5 August and 13 to 21 September 2026, one native value per day, '
                   'nothing averaged. The axis breaks where there are no rows.',
        plate=plate_flows,
        what="Each transmission operator reports the gas that physically crossed each of its points, per gas day and "
             "direction. gridflow keeps one row per point, operator, direction and gas day, normalised to GWh/d: "
             "about 983 rows a day across 620 points and 48 operators. Both sides of a point report, and "
             "some flows are null.",
        uses=["Supply by entry point, terminals and LNG included, for a gas balance model.",
              "Flows at the points joining GB to the continent.",
              "Checking physical flow against nominations and allocations at the same point."],
        facts=[("Grain", "One row per gas day, point, operator and direction"),
               ("Cadence", "Daily; the gas-day start varies by operator (04:00 UTC for most GB rows)"),
               ("Unit", "GWh/d"),
               ("Local history", "14 gas days: 1 to 5 Aug and 13 to 21 Sep 2026"),
               ("Publication lag", "Not established: silver keeps no vendor publication time"),
               ("Rows", "13,764; 2,499 with a null flow")],
        caveats=[("Fourteen gas days.", "Local history is 1 to 5 August and 13 to 21 September 2026, in two blocks."),
                 ("Both sides report.", "Summing every row double counts: at Bacton (IUK) on 2026-09-21, National Gas "
                  "TSO exit and Interconnector entry are both 175.165952 GWh/d."),
                 ("Flows can be null.", "2,499 rows, and every day for 176 series such as Avonmouth LNG entry. Do not "
                  "zero-fill.")],
        endpoint=["GET https://transparency.entsog.eu/api/v1/operationalData",
                  "    ?limit=-1&timeZone=UCT&from=YYYY-MM-DD&to=YYYY-MM-DD",
                  "    &indicator=Physical%20Flow&periodType=day"],
        endpoint_note="No <code>pointDirection</code> filter: one call fetches the whole system.",
        cli=[("gridflow ingest entsog physical_flows --start 2026-09-13 --end 2026-09-21", "bronze only"),
             ("gridflow pipeline entsog physical_flows --start 2026-09-13 --end 2026-09-21", "bronze to silver")],
        schema_class="EntsogPhysicalFlow", version="1.0.0",
        schema=[("timestamp_utc", "Datetime(us, UTC)", "Gas-day start (vendor periodFrom) in UTC"),
                ("point_key", "String", "ENTSOG point id, e.g. ITP-00005"),
                ("point_label", "String", "Point name, e.g. Bacton (IUK)"),
                ("operator_key", "String", "Reporting operator id, e.g. UK-TSO-0001"),
                ("operator_label", "String", "Operator name, e.g. National Gas TSO"),
                ("direction_key", "String", "entry or exit, relative to the reporting operator’s system (inferred, "
                                            "not documented)"),
                ("flow_gwh_per_day", "Float64", "Flow normalised to GWh/d; nullable"),
                ("unit", "String", "Always GWh/d after normalisation"),
                ("data_provider", "String", "Always <code>entsog</code>"),
                ("ingested_at", "Datetime(us, UTC)", "When the silver transform ran; not declared in the class")],
        lineage="<code>event_time</code>, <code>available_at</code> (the ingest time here), <code>source_run_id</code> "
                "and <code>dataset_version</code> are added by the silver base class.",
        sample=sample("entsog/physical_flows", ["point_key", "point_label", "operator_key", "operator_label",
                                                "direction_key", "flow_gwh_per_day"]),
        sample_cap="Gas day 2026-09-21, <code>timestamp_utc</code> 2026-09-21T04:00Z, GB-side points. Avonmouth LNG "
                   "shows a null flow.",
        wb=['df = data.entsog.query("physical_flows", "2026-09-13", "2026-09-21")'],
        wb_note="Filters <code>timestamp_utc</code> from 13 Sep 00:00 UTC to before 22 Sep 00:00 UTC, so operators "
                "whose gas day starts at 21:00 to 23:00 UTC the day before miss the first day.",
        related=[("entsog/aggregated_physical_flows", "The same indicator, aggregated to zone level."),
                 ("entsog/nominations", "Same endpoint, the Nomination indicator."),
                 ("entsog/allocations", "Same endpoint, the Allocation indicator.")]),
    "bmunits-reference": dict(
        spec="elexon/bmunits_reference", vendor="Elexon BMRS", title="BM unit reference data",
        idline='<code>elexon/bmunits_reference</code>, from Elexon’s “All BM Unit reference data”',
        oneliner="A snapshot of Balancing Mechanism unit registrations: id, name, fuel type, registered capacity, "
                 "lead party and GSP group.",
        plate_title="Registered BM units by fuel type",
        plate_note='Source <code>elexon/bmunits_reference</code>, silver snapshot ingested 26 September 2026. No '
                   'time axis: a count of units, one square per row, grouped by <code>fuel_type</code> with nulls '
                   'kept. Capacity is not drawn: it is per registration and does not add up.',
        plate=plate_units,
        what="Elexon’s register of Balancing Mechanism units, one row per unit id. gridflow fetches the whole list in "
             "one call and overwrites a single file each run, so silver holds the current snapshot only. Fuel type is "
             "filled for 499 of the 3,014 units, with the same codes as FUELHH.",
        uses=["Mapping per-unit datasets such as <code>boal</code> and <code>pn</code> to a fuel type and lead party.",
              "Selecting every unit of one technology, such as all <code>WIND</code> units.",
              "Linking unit registrations to FUELHH’s fuel codes."],
        facts=[("Grain", "One row per BM unit id"),
               ("Cadence", "A snapshot; the configured schedule is weekly"),
               ("Unit", "MW for registered capacity, per registration"),
               ("Local history", "The current snapshot only, ingested 26 Sep 2026"),
               ("Publication lag", "Not established"),
               ("Rows", "3,014 units from 379 companies")],
        caveats=[("Most units have no fuel type.", "2,515 of 3,014 (83%), so a fuel breakdown covers only 499 units."),
                 ("Capacity does not add up.", "It is per registration: the untyped rows alone sum to 727,551 MW, and "
                  "1,315 ids start <code>I_</code>, which the docs describe as per-party interconnector registrations."),
                 ("Counts drift between runs.", "One snapshot, overwritten each run, with keyless vendor rows dropped: "
                  "2,969 units on 2026-09-09, 3,014 now.")],
        endpoint=["GET https://data.elexon.co.uk/bmrs/api/v1/reference/bmunits/all"],
        endpoint_note="No parameters and no pagination.",
        cli=[("gridflow pipeline elexon bmunits_reference", "dates are ignored")],
        schema_class="ElexonBMUnit", version="1.1.0",
        schema=[("bm_unit_id", "String", "Elexon BM Unit id; the entity key"),
                ("bm_unit_name", "String", "Vendor bmUnitName; often repeats the id"),
                ("fuel_type", "String", "Vendor fuelType; null on 2,515 of 3,014 rows"),
                ("registered_capacity_mw", "Float64", "Vendor generationCapacity, MW; per registration, not additive"),
                ("company_name", "String", "Lead party name"),
                ("gsp_group_id", "String", "GSP group, e.g. _A; null on 1,822 rows"),
                ("national_grid_bm_unit", "String", "National Grid BM unit id, e.g. ABERU-1; not the ENTSO-E EIC"),
                ("data_provider", "String", "Always <code>elexon</code>"),
                ("ingested_at", "Datetime(us, UTC)", "When the silver transform ran")],
        lineage="<code>event_time</code> (2026-09-26T00:00Z, the target date), <code>available_at</code>, "
                "<code>source_run_id</code> and <code>dataset_version</code> are added by the silver base class.",
        sample=sample("elexon/bmunits_reference", ["bm_unit_id", "bm_unit_name", "fuel_type", "registered_capacity_mw",
                                                   "company_name", "gsp_group_id", "national_grid_bm_unit"]),
        sample_cap="Eight units from the 2026-09-26 snapshot, including one each of the <code>I_</code>, "
                   "<code>2__</code> and <code>V__</code> id patterns.",
        wb=['df = data.elexon.tail("bmunits_reference", n=3014)',
            'data.sql("SELECT * FROM silver_elexon_bmunits_reference")'],
        wb_note="Not <code>query()</code>: this table’s date column is <code>ingested_at</code>, so a date range such "
                "as January 2026 returns 0 rows. <code>tail()</code> reads the newest rows; <code>sql()</code> is "
                "read-only.",
        related=[("elexon/boal", "A per-unit dataset joined on <code>bm_unit_id</code>; the transformer measures this join’s coverage."),
                 ("elexon/pn", "A per-unit dataset joined on <code>bm_unit_id</code>."),
                 ("elexon/uou2t14d", "Per-unit availability."),
                 ("elexon/fuelhh", "Shares the fuel-type codes; interconnector flow lives there.")]),
}


# ================================================================ strata edges: each section draws its own top
E = 28


def edge_svg(kind: str, seed: float, label: str = "") -> str:
    p = f"e{kind[:2]}"
    fills = {"soil": (T_TOP, "soil", ".5"), "bronze": (T_BRONZE, "brick", ".15"), "silver": (T_SILVER, "diag", ".22"),
             "gold": (T_GOLD, "stip", ".26"), "deep": (PETROL, "granite", ".5")}
    fill, pat, op = fills[kind]
    root = ""
    if kind == "soil":
        pts = [(x, 14 + 3.5 * math.sin(x / 190 + .6) - 2.2 * math.sin(x / 83 + 1.3)) for x in range(-40, W + 41, 20)]
        top = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)
        root = top + " " + " ".join(f"L{f(x)} {f(y + 9)}" for x, y in reversed(pts)) + " Z"
    elif kind == "deep":
        pts = [(x, 15 + 5 * math.sin(x / 140 + 1) + 3.5 * math.sin(x / 53 + 2) + 2.2 * math.sin(x / 19))
               for x in range(-40, W + 41, 20)]
        top = smooth(pts)
    else:
        top = smooth(wave(14, 6, seed))
    body = f"{top} L{W + 40} 20000 L-40 20000 Z"
    out = [f'<svg class="st-bg" width="{W}" aria-hidden="true"><defs>{patterns(p)}</defs>',
           f'<path d="{body}" fill="{fill}"></path>', f'<path d="{body}" fill="url(#{p}-{pat})" opacity="{op}"></path>']
    if root:
        out.append(f'<path d="{root}" fill="{OLIVE}"></path>')
    out.append(f'<path d="{top}" stroke="{INK}" stroke-width="{2 if kind == "deep" else 1.5}" fill="none" '
               f'stroke-linejoin="round"></path>')
    if label:
        out.append(f'<text x="1360" y="{E + 36}" text-anchor="end" font-family="Hanken Grotesk" font-style="italic" '
                   f'font-size="14" fill="{INK}">{label}</text>')
    out.append("</svg>")
    return "".join(out)


def horizon_svg() -> str:
    """The sky's lower edge: far and near ridges, then the energised land running down under the surface."""
    h = 58
    far = [(-20, 30), (160, 18), (360, 26), (560, 12), (760, 22), (980, 14), (1180, 24), (1460, 16)]
    near = [(-20, 40), (140, 30), (320, 36), (520, 26), (700, 34), (900, 28), (1100, 38), (1300, 30), (1460, 36)]
    land = [(-20, 48), (240, 44), (560, 49), (880, 45), (1180, 50), (1460, 46)]
    return (f'<svg class="horizon" width="{W}" height="{h}" viewBox="0 0 {W} {h}" aria-hidden="true">'
            f'<path d="{smooth(far)} L1460 {h} L-20 {h} Z" fill="{HORIZON}" opacity=".5"></path>'
            f'<path d="{smooth(near)} L1460 {h} L-20 {h} Z" fill="{HORIZON}"></path>'
            f'<path d="{smooth(land)} L1460 {h} L-20 {h} Z" fill="{CHART}"></path></svg>')


# ================================================================ page
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,200..800'
         '&amp;family=Hanken+Grotesk:ital,wght@0,400..700;1,400..600&amp;family=Red+Hat+Mono:wght@400;500'
         '&amp;display=swap" rel="stylesheet">')

CSS = (HERE / "c.css").read_text(encoding="utf-8")

NAV = [("Home", False), ("Data sources", True), ("Architecture", False), ("Models", False), ("About", False)]


def mast() -> str:
    li = "".join(f'<li><a href="#"{" aria-current=" + chr(34) + "page" + chr(34) if cur else ""}>{t}</a></li>'
                 for t, cur in NAV)
    return (f'<header class="mast"><a class="brand" href="#">gridflow</a>'
            f'<nav aria-label="Primary"><ul>{li}</ul></nav></header>')


def well(lines: list[str]) -> str:
    return '<pre class="well">' + "\n".join(esc(x) for x in lines) + "</pre>"


def cli_well(cli: list[tuple[str, str]]) -> str:
    wd = max(len(c) for c, _ in cli)
    body = "\n".join(f'{esc(c).ljust(wd)}   <span class="c"># {esc(m)}</span>' for c, m in cli)
    return f'<pre class="well">{body}</pre>'


def page(slug: str, height: int) -> str:
    P = PAGES[slug]
    svg, _ = P["plate"]()
    cols, rows = P["sample"]
    facts = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in P["facts"])
    uses = "".join(f"<li>{u}</li>" for u in P["uses"])
    cav = "".join(f"<li><strong>{a}</strong> {b}</li>" for a, b in P["caveats"])
    schema = "".join(f"<tr><td>{c}</td><td>{t}</td><td>{m}</td></tr>" for c, t, m in P["schema"])
    df = ('<table class="df"><thead><tr>' + "".join(f"<th>{c}</th>" for c in cols) + "</tr></thead><tbody>"
          + "".join("<tr>" + "".join(f"<td>{v}</td>" for v in r) + "</tr>" for r in rows) + "</tbody></table>")
    cells = [f'<div class="cell"><span class="pr">[1]:</span><pre class="in">{SETUP}</pre></div>']
    for k, code in enumerate(P["wb"], start=2):
        cells.append(f'<div class="cell"><span class="pr">[{k}]:</span><pre class="in">{hl(code)}</pre></div>')
    rel = "".join(f'<li><a href="#">{k}</a><p>{d}</p></li>' for k, d in P["related"])
    ep_note = f'<p class="note">{P["endpoint_note"]}</p>' if P.get("endpoint_note") else ""

    sky = (f'<div class="sky">{mast()}'
           f'<div class="intro"><nav class="crumbs" aria-label="Breadcrumb"><a href="#">Data sources</a>'
           f'<span aria-hidden="true">/</span><a href="#">{P["vendor"]}</a></nav>'
           f'<div><h1>{P["title"]}</h1><p class="idline">{P["idline"]}</p></div>'
           f'<p class="oneliner">{P["oneliner"]}</p></div>{horizon_svg() if SHOW_HORIZON else ""}</div>')
    soil = (f'<section class="st soil" aria-labelledby="plate-h">{edge_svg("soil", 0)}<div class="st-in">'
            f'<figure class="plate"><div class="plate-head"><h2 id="plate-h">{P["plate_title"]}</h2>'
            f'<p class="plate-note">{P["plate_note"]}</p></div>{svg}</figure>'
            f'<div class="row first"><h2>What it is</h2><div class="body"><p class="lead">{P["what"]}</p></div></div>'
            f'<div class="row"><h2>How it’s used</h2><div class="body"><ul class="uses">{uses}</ul></div></div>'
            f'<div class="row"><h2>Facts</h2><div class="body"><dl class="facts">{facts}</dl></div></div>'
            f'<div class="row"><h2>Caveats</h2><div class="body"><ul class="cav">{cav}</ul></div></div>'
            f'</div></section>')
    bronze = (f'<section class="st" aria-labelledby="v-h">{edge_svg("bronze", 0.4, "bronze")}<div class="st-in">'
              f'<div class="row"><div><h2 id="v-h">From the vendor</h2></div><div class="body">{well(P["endpoint"])}{ep_note}{cli_well(P["cli"])}</div></div>'
              f'</div></section>')
    silver = (f'<section class="st" aria-labelledby="s-h">{edge_svg("silver", 2.1, "silver")}<div class="st-in">'
              f'<div class="row"><div><h2 id="s-h">Silver schema</h2><p class="sub">Pydantic class '
              f'<code>{P["schema_class"]}</code>; transformer version {P["version"]}.</p></div><div class="body">'
              f'<table class="schema"><thead><tr><th>column</th><th>dtype</th><th>meaning</th></tr></thead>'
              f'<tbody>{schema}</tbody></table><p class="cap lin">{P["lineage"]}</p></div></div>'
              f'<div class="row wide"><h2>Sample rows</h2><div class="dfw">{df}</div><p class="cap">{P["sample_cap"]}'
              f'</p></div></div></section>')
    gold = (f'<section class="st" aria-labelledby="g-h">{edge_svg("gold", 4.0, "gold")}<div class="st-in">'
            f'<div class="row"><div><h2 id="g-h">In the workbench</h2><p class="sub">From <code>gridflow-models</code>.'
            f'</p></div><div class="body"><div class="nb">{"".join(cells)}</div><p class="note">{P["wb_note"]}</p>'
            f'</div></div></div></section>')
    deep = (f'<section class="st deep" aria-labelledby="r-h">{edge_svg("deep", 1.0)}<div class="st-in">'
            f'<div class="row"><h2 id="r-h">Related</h2><ul class="rel">{rel}</ul></div>'
            f'<footer class="foot"><a class="brand" href="#">gridflow</a><ul><li><a href="#">Data sources</a></li>'
            f'<li><a href="#">Architecture</a></li><li><a href="#">Models</a></li><li><a href="#">Code on GitHub</a>'
            f'</li></ul><span>MIT licence</span></footer></div></section>')
    body = "\n".join([sky, "<main>", soil, bronze, silver, gold, deep, "</main>"])
    head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{P["title"]}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS}
<style>
{CSS}</style>
</helmet>
<div class="root" style="width: {W}px; height: {height}px; overflow: hidden; position: relative">
"""
    tail = ("\n</div>\n</x-dc>\n<script type=\"text/x-dc\" data-dc-script data-props='{\"$preview\":{\"width\":"
            f"{W},\"height\":{height}" "}}'>\nclass Component extends DCLogic {\nrenderVals() { return {}; }\n}\n"
            "</script>\n</body>\n</html>\n")
    return head + body + tail


def static(dc: str) -> str:
    s = dc.replace('<script src="./support.js"></script>', "")
    s = re.sub(r"</?x-dc>", "", s)
    s = re.sub(r"</?helmet>", "", s)
    s = re.sub(r"<script type=\"text/x-dc\".*?</script>\n", "", s, flags=re.S)
    return s


if __name__ == "__main__":
    (HERE / "static").mkdir(exist_ok=True)
    for slug in PAGES:
        out = page(slug, HEIGHTS[slug])
        body_only = out.split('<script type="text/x-dc"')[0]
        assert "{{" not in body_only and "}}" not in body_only, "template-hole syntax in markup"
        assert "/>" not in re.sub(r"<(meta|link|br)[^>]*>", "", body_only), "self-closing tag"
        assert "<UTC" not in body_only and "<n>" not in body_only, "unescaped angle text"
        (HERE / f"C-{slug}.dc.html").write_text(out, encoding="utf-8")
        (HERE / "static" / f"C-{slug}.html").write_text(static(out), encoding="utf-8")
        print(slug, HEIGHTS[slug], len(out))
