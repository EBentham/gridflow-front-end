from __future__ import annotations

from pathlib import Path

p = Path(__file__).parent / "gen_e.py"
s = p.read_text(encoding="utf-8")


def rep(a: str, b: str, cnt: int = 1) -> None:
    global s
    n = s.count(a)
    assert n == cnt, (n, a[:90])
    s = s.replace(a, b)


rep('LAND_H = 124', 'LAND_H = 114')
rep('FW, FH = 800, 330          # figure svg', 'FW, FH = 800, 272          # figure svg')
rep('PL, PR = 52, 652  ', 'PL, PR = 52, 620  ')
rep('    PT, PB = 16, 292\n', '    PT, PB = 14, 236\n', 3)
rep('PB + 26, ', 'PB + 24, ', 4)
rep('''        ("NUCLEAR", pg["nuclear"], "NUCLEAR"), ("BIOMASS", pg["biomass"], "BIOMASS"),
        ("OTHER", khaki, "OTHER, NPSHYD, COAL, OIL"), ("CCGT", pg["gas"], "CCGT, OCGT"),''',
    '''        ("BIOMASS", pg["biomass"], "BIOMASS"), ("NUCLEAR", pg["nuclear"], "NUCLEAR"),
        ("OTHER", khaki, "OTHER, NPSHYD,|COAL, OIL"), ("CCGT", pg["gas"], "CCGT, OCGT"),''')
rep('''    placed = declash(mids, PT + 6, PB + 4, 17)
    labs, leads = [], []
    for want, y, s in placed:
        main, _, rest = s.partition(" (")
        t = f'<tspan class="cd">{esc(main)}</tspan>'
        if rest:
            t += f'<tspan class="an" dx="5">{esc(rest[:-1])}</tspan>'
        labs.append(f'<text x="{LX + 12}" y="{f(y + 4.5)}">{t}</text>')''',
    '''    placed = declash(mids, PT + 6, PB + 4, 16)
    labs, leads = [], []
    for want, y, s in placed:
        main, _, rest = s.partition(" (")
        lines = main.split("|")
        t = "".join(f'<tspan class="cd" x="{LX + 12}" dy="{0 if j == 0 else 15}">{esc(ln)}</tspan>'
                    for j, ln in enumerate(lines))
        if rest:
            t += f'<tspan class="an" dx="5">{esc(rest[:-1])}</tspan>'
        yy = y + 4.5 - 7.5 * (len(lines) - 1)
        labs.append(f'<text x="{LX + 12}" y="{f(yy)}">{t}</text>')''')
rep('''    ann = t_text(PL + 8, Y(-5200), "below zero: INT* net export and negative PS", "start", "an")\n''',
    '    ann = ""\n')
rep('.deep{background:var(--petrol);color:var(--on-petrol);padding-top:70px;padding-bottom:30px}',
    '.deep{background:var(--petrol);color:var(--on-petrol);padding-top:70px;padding-bottom:0}\n'
    '.dfoot{padding-top:64px;padding-bottom:30px}')
rep('.foot{display:flex;justify-content:space-between;align-items:baseline;margin-top:64px;padding:22px 0 0;',
    '.foot{display:flex;justify-content:space-between;align-items:baseline;padding:22px 0 0;')
rep('.title{padding:40px 80px 0}', '.title{padding:30px 80px 0}')
rep('.land{margin:-58px -80px 0}', '.land{margin:-78px 0 0}')
rep('column-gap:64px;padding-top:22px}', 'column-gap:64px;padding-top:16px}')
rep('.fig figcaption{margin:10px 0 0;', '.fig figcaption{margin:8px 0 0;')
rep('grid-template-columns:136px minmax(0,1fr);border-bottom', 'grid-template-columns:128px minmax(0,1fr);border-bottom')
rep('.facts dt,.facts dd{margin:0;padding:9px 0 10px;', '.facts dt,.facts dd{margin:0;padding:8px 0 9px;')
rep('.get{padding:34px 0 40px}', '.get{padding:26px 0 34px}')
rep('grid-template-columns:30px 150px minmax(0,1fr);column-gap:16px;row-gap:14px;align-items:start}',
    'grid-template-columns:30px 140px minmax(0,1fr);column-gap:16px;row-gap:12px;align-items:start}')
rep('.ways dd{margin:0}', '.ways dd{margin:0;display:flex;align-items:flex-start;column-gap:24px}')
rep('.note{margin:4px 0 0;font-size:14px;line-height:1.45;color:var(--ink-2)}',
    '.note{margin:0;padding-top:4px;max-width:44ch;font-size:14px;line-height:1.45;color:var(--ink-2)}')

# shorter captions (two lines at 800 px)
rep('''        cap=(f'{code("elexon/fuelhh")} silver, MW, settlement dates 20 to 26 September 2026 (336 half-hours from 23:00 '
             'UTC on 19 September; hours in UTC). Each code’s two half-hours are averaged per hour; codes sharing a band '
             'are summed first. Positive values stack above zero, negative ones below it. What the PS sign means is not '
             'documented.'),''',
    '''        cap=(f'{code("elexon/fuelhh")} silver, MW, settlement dates 20 to 26 September 2026, hourly in UTC: each '
             'code’s two half-hours averaged, codes in one band summed first. Positive values stack up from zero, '
             'negative ones down from it; the PS sign is not documented.'),''')
rep('''        cap=(f'{code("elexon/system_prices")} silver, latest vintage per period, £/MWh, settlement dates 19 to 22 '
             'September 2026 (192 half-hours from 23:00 UTC on 18 September; times in UTC). Native half-hourly values, '
             'nothing averaged. SBP equals SSP in every period, so one line carries both.'),''',
    '''        cap=(f'{code("elexon/system_prices")} silver, latest vintage per period, £/MWh, settlement dates 19 to 22 '
             'September 2026, times in UTC. Native half-hourly values, 192 of them, nothing averaged; SBP equals SSP in '
             'every period, so one line carries both.'),''')
rep('''        cap=(f'{code("entsog/physical_flows")} silver, GWh/d, every gas day held locally: 1 to 5 August and 13 to 21 '
             'September 2026. One native value per gas day, reported by National Gas TSO; nothing is averaged or '
             'interpolated, and the line breaks where there are no rows.'),''',
    '''        cap=(f'{code("entsog/physical_flows")} silver, GWh/d, every gas day held locally (1 to 5 August, 13 to 21 '
             'September 2026). One native value a gas day as National Gas TSO reports it; nothing averaged or '
             'interpolated, and the line breaks where there are no rows.'),''')
rep('''        cap=(f'{code("elexon/bmunits_reference")} silver, count of BM units, snapshot of 26 September 2026. There is no '
             'time axis, so the figure shows what the registry holds: all 3,014 units to scale, then the 499 with a fuel '
             'type enlarged by code. Counts only; capacities are not additive.'),''',
    '''        cap=(f'{code("elexon/bmunits_reference")} silver, count of BM units, snapshot of 26 September 2026. No time '
             'axis, so the figure shows what the registry holds: all 3,014 units to scale, then the 499 with a fuel type '
             'by code. Counts only; capacities are not additive.'),''')

# one-line facts
FACTS = {
    "fuelhh": '''            ("Vendor dataset", f'{code("FUELHH")}, Elexon Insights API'),
            ("Grain", f'one row per settlement period and {code("fuel_type")}'),
            ("Cadence", "every 30 minutes; 17 to 20 codes a period"),
            ("History", "2021-09-01 to 2026-09-26 in local silver; 2026-09-07 to 09 missing"),
            ("Publication lag", "at the period end, 30 minutes after it starts, on 99.82% of rows"),
            ("Units", f'MW in {code("generation_mw")}; INT* and PS are signed'),
            ("Volume", "29,760 rows in August 2026; 1,682,517 in all"),''',
}
rep(FACTS["fuelhh"], '''            ("Vendor dataset", f'{code("FUELHH")}, Elexon Insights API'),
            ("Grain", f'settlement period × {code("fuel_type")}'),
            ("Cadence", "every 30 minutes"),
            ("History", "2021-09-01 to 2026-09-26, with gaps"),
            ("Publication lag", "period end (30 min) on 99.82% of rows"),
            ("Units", "MW; INT* and PS are signed"),
            ("Volume", "29,760 rows in August 2026"),''')
rep('''            ("Vendor dataset", f'{code("DISEBSP")}, Elexon Insights API'),
            ("Grain", "one row per settlement period per vendor publication (append-only)"),
            ("Cadence", "every 30 minutes"),
            ("History", "2021-09-01 to 2026-09-22 in local silver; no dates missing"),
            ("Publication lag", "median 52 minutes in 2021 to 2023; about 24.7 hours in 2024 to 2026"),
            ("Units", "£/MWh for prices; MWh for net imbalance volume"),
            ("Volume", "3,770 rows in August 2026; 96,793 in all"),''',
    '''            ("Vendor dataset", f'{code("DISEBSP")}, Elexon Insights API'),
            ("Grain", "settlement period × vendor publication"),
            ("Cadence", "every 30 minutes"),
            ("History", "2021-09-01 to 2026-09-22, no dates missing"),
            ("Publication lag", "median 52 min to 2023; about 24.7 h from 2024"),
            ("Units", "£/MWh; net imbalance volume in MWh"),
            ("Volume", "3,770 rows in August 2026"),''')
rep('''            ("Vendor dataset", f'{code("operationalData")}, indicator Physical Flow, ENTSOG Transparency Platform'),
            ("Grain", "one row per gas day, point, operator and direction"),
            ("Cadence", "daily; each operator’s gas day starts at its own UTC hour"),
            ("History", "14 gas days in local silver: 1 to 5 Aug and 13 to 21 Sep 2026"),
            ("Publication lag", f'not established; {code("available_at")} is the ingest time'),
            ("Units", "GWh/d after normalisation; flow can be null"),
            ("Volume", "about 983 rows a gas day; 13,764 in all"),''',
    '''            ("Vendor dataset", f'{code("operationalData")}, Physical Flow indicator'),
            ("Grain", "gas day × point × operator × direction"),
            ("Cadence", "daily, on each operator’s gas day"),
            ("History", "1 to 5 Aug and 13 to 21 Sep 2026"),
            ("Publication lag", "not established"),
            ("Units", "GWh/d; flow can be null"),
            ("Volume", "about 983 rows a gas day"),''')
rep('''            ("Vendor dataset", f'{code("reference/bmunits/all")}, Elexon Insights API'),
            ("Grain", f'one row per BM Unit ({code("bm_unit_id")})'),
            ("Cadence", "a weekly snapshot, overwritten on each run"),
            ("History", "the current snapshot only (2026-09-26); no history is kept"),
            ("Publication lag", "not established"),
            ("Units", f'MW in {code("registered_capacity_mw")}, per registration'),
            ("Volume", "3,014 rows"),''',
    '''            ("Vendor dataset", f'{code("reference/bmunits/all")}, Insights API'),
            ("Grain", f'BM Unit ({code("bm_unit_id")})'),
            ("Cadence", "weekly snapshot, overwritten"),
            ("History", "current snapshot only (2026-09-26)"),
            ("Publication lag", "not established"),
            ("Units", "MW, per registration"),
            ("Volume", "3,014 rows"),''')
p.write_text(s, encoding="utf-8")
print("patched")
