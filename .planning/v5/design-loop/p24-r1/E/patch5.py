from __future__ import annotations

from pathlib import Path

p = Path(__file__).parent / "gen_e.py"
s = p.read_text(encoding="utf-8")


def rep(a: str, b: str, cnt: int = 1) -> None:
    global s
    n = s.count(a)
    assert n == cnt, (n, a[:90])
    s = s.replace(a, b)


rep('''2.1 and 15.9 GW, largely in opposition. Net''', '''2.1 and 15.9 GW. Net''')
rep('''("PS", pg["uncovered:PS"], "PS"),''', '''("PS", pg["uncovered:PS"], "PS (signed)"),''')
rep('''        cap=(f'{code("elexon/fuelhh")} silver, MW, settlement dates 20 to 26 September 2026. Hourly means, UTC; codes '
             'in one band are summed first. Positive values stack up from zero, negative ones down; the PS sign is '
             'not documented.'),''',
    '''        cap=(f'{code("elexon/fuelhh")} silver, MW (axis in GW), settlement dates 20 to 26 September 2026. Hourly means, '
             'UTC; codes in one band are summed first. Positive values stack up from zero, negative ones down; the PS '
             'sign is not documented.'),''')
rep('''            ("Day-ahead spread", f'Set beside {code("elexon/mid")}, the workbench’s day-ahead benchmark.'),''',
    '''            ("Day-ahead spread", f'Set beside {code("elexon/mid")}, which the workbench’s day-ahead benchmark reads.'),''')
rep('''terminals and other points on Europe’s transmission systems. Each operator reports its own side of a "
              "point as entry or exit, so a point appears once per reporting operator and direction. gridflow "
              "normalises every value to GWh/d."),''',
    '''terminals and other points on Europe’s transmission systems. Operators on both sides of a point "
              "report it, each as entry or exit, so one point can appear once per operator and direction. gridflow "
              "normalises every value to GWh/d."),''')
rep('''            ("Capacity is not additive:", f'{code("registered_capacity_mw")} is per registration. Null-fuel rows alone '
                                          "sum to 727,551 MW, and 1,315 ids start I_, which the vault describes as "
                                          "per-party interconnector registrations."),
            ("One snapshot, overwritten each run,", "and keyless vendor rows are dropped, so counts drift between runs: "
                                                    "2,969 on 2026-09-09 and 3,014 now."),''',
    '''            ("Capacity is not additive:", f'{code("registered_capacity_mw")} is per registration, and the null-fuel '
                                          "rows alone sum to 727,551 MW."),
            ("One snapshot, overwritten each run,", "and keyless vendor rows are dropped, so counts drift between runs: "
                                                    "2,969 on 2026-09-09, 3,014 on 2026-09-26."),''')
p.write_text(s, encoding="utf-8")
print("patched")
