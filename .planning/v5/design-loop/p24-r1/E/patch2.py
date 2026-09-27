from __future__ import annotations

from pathlib import Path

p = Path(__file__).parent / "gen_e.py"
s = p.read_text(encoding="utf-8")


def rep(a: str, b: str, cnt: int = 1) -> None:
    global s
    n = s.count(a)
    assert n == cnt, (n, a[:90])
    s = s.replace(a, b)


# label placement that knows each label's height (lines x 15 px)
rep('''def declash(items: list[tuple[float, str]], lo: float, hi: float, gap: float) -> list[tuple[float, float, str]]:''',
    '''def spread(items: list[tuple[float, str]], lo: float, hi: float, line: float = 15, pad: float = 3
           ) -> list[tuple[float, float, str]]:
    """Place label centres near their wanted y, top to bottom, so no two overlap; a label's height is its lines."""
    items = sorted(items)
    hs = [line * (s.count("|") + 1) for _, s in items]
    ys = [y for y, _ in items]
    for i in range(1, len(ys)):
        ys[i] = max(ys[i], ys[i - 1] + (hs[i - 1] + hs[i]) / 2 + pad)
    over = ys[-1] + hs[-1] / 2 - hi if ys else 0
    if over > 0:
        ys[-1] -= over
        for i in range(len(ys) - 2, -1, -1):
            ys[i] = min(ys[i], ys[i + 1] - (hs[i] + hs[i + 1]) / 2 - pad)
    return [(want, y, s) for (want, s), y in zip(items, ys)]


def declash(items: list[tuple[float, str]], lo: float, hi: float, gap: float) -> list[tuple[float, float, str]]:''')
rep('''    placed = declash(mids, PT + 6, PB + 4, 16)''', '''    placed = spread(mids, PT, PB + 8)''')

# captions to two lines
rep('''        cap=(f'{code("elexon/fuelhh")} silver, MW, settlement dates 20 to 26 September 2026, hourly in UTC: each '
             'code’s two half-hours averaged, codes in one band summed first. Positive values stack up from zero, '
             'negative ones down from it; the PS sign is not documented.'),''',
    '''        cap=(f'{code("elexon/fuelhh")} silver, MW, settlement dates 20 to 26 September 2026. Hourly means, UTC; codes '
             'in one band are summed first. Positive values stack up from zero, negative ones down; the PS sign is '
             'not documented.'),''')
p.write_text(s, encoding="utf-8")
print("patched")
