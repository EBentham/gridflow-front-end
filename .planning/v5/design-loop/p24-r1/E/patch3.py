from __future__ import annotations

from pathlib import Path

p = Path(__file__).parent / "gen_e.py"
s = p.read_text(encoding="utf-8")


def rep(a: str, b: str, cnt: int = 1) -> None:
    global s
    n = s.count(a)
    assert n == cnt, (n, a[:90])
    s = s.replace(a, b)


rep('    top, bot = 640.0, -80.0\n', '    top, bot = 650.0, -150.0\n')
rep('''    ticks.append(f"M{PL - 5} {f(Y(-50))} H{PL}")
    labs.append(t_text(PL - 9, Y(-50) + 4.5, f"{MINUS}50", "end"))''',
    '''    ticks.append(f"M{PL - 5} {f(Y(-100))} H{PL}")
    labs.append(t_text(PL - 9, Y(-100) + 4.5, f"{MINUS}100", "end"))''')
rep('''    labs.append(t_text(X(imin) + 8, Y(vals[imin]) + 16, f"{MINUS}50.00 at 13:30 UTC, 20 Sep", "start", "an"))
    labs.append(t_text(PL + 8, PB - 2, "34 of 192 periods below zero, in clay", "start", "an"))''',
    '''    labs.append(t_text(X(imin) + 9, Y(vals[imin]) + 5, f"{MINUS}50.00 at 13:30 UTC, 20 Sep", "start", "an"))
    labs.append(t_text(PL + 8, Y(-118), "34 of 192 periods below zero", "start", "an"))''')
p.write_text(s, encoding="utf-8")
print("patched")
