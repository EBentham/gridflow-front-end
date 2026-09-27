"""A compact landscape strip for the sky's lower edge (architecture and models), in the homepage's language:
a far ridge, a near ridge with turbines, the energised field, and a few assets standing on the cut."""
from __future__ import annotations

import math

from b_base import (CHART, DAY, HORIZON, INK, OLIVE, W, converter, f, frange, metmast, pylon, sc, smooth, solar_rows,
                    spans, substation, tank, tips, turbine)


def strip(S: float, assets: list[str], turbines: list[float] | None = None) -> tuple[str, dict[str, tuple[float, float]]]:
    """Draw the strip whose cut sits at S (in the caller's coordinates). Returns the SVG and, per asset, the
    point where a feed cable can leave it."""
    prof = lambda x: S + 3 * math.sin(x / 190 + .6) - 2 * math.sin(x / 83 + 1.3)  # noqa: E731
    g: list[str] = []
    far = [(-20, S - 150), (140, S - 176), (320, S - 160), (500, S - 186), (690, S - 166), (880, S - 150),
           (1060, S - 172), (1250, S - 156), (1460, S - 168)]
    g.append(f'<path d="{smooth(far)} L1460 {f(S + 4)} L-20 {f(S + 4)} Z" fill="{HORIZON}" opacity=".5"></path>')
    near = [(-20, S - 104), (110, S - 124), (260, S - 112), (420, S - 134), (600, S - 118), (780, S - 100),
            (960, S - 116), (1140, S - 108), (1300, S - 122), (1460, S - 110)]
    g.append(f'<path d="{smooth(near)} L1460 {f(S + 4)} L-20 {f(S + 4)} Z" fill="{HORIZON}"></path>')
    for i, tx in enumerate(turbines or [110, 260, 420, 600, 1140, 1300]):
        base = S - 116 + 6 * math.sin(tx / 70)
        g.append(turbine(tx, base, 64 + (i % 3) * 6, 33, ["sp1", "sp2", "sp3"][i % 3], 30 * i + 8))
    field = [(-20, S - 62), (200, S - 54), (420, S - 64), (640, S - 50), (860, S - 58), (1080, S - 46),
             (1280, S - 52), (1460, S - 48)]
    bottom = " ".join(f"L{f(x)} {f(prof(x))}" for x in range(1460, -21, -20))
    g.append(f'<path d="{smooth(field)} {bottom} Z" fill="{CHART}"></path>')
    g.append(f'<path d="{smooth([(-20, S - 30), (500, S - 26), (1000, S - 32), (1460, S - 28)])}" stroke="{OLIVE}" '
             f'stroke-width="1" fill="none" opacity=".45"></path>')
    ends: dict[str, tuple[float, float]] = {}
    for a in assets:
        kind, xs = a.split("@")
        x = float(xs)
        base = prof(x + 30) + 1
        if kind == "sub":
            g.append(sc(substation(x, base), x, base, 1.0))
            ends[a] = (x + 44, base)
        elif kind == "mast":
            g.append(metmast(x, prof(x), 132, prof))
            ends[a] = (x, prof(x))
        elif kind == "conv":
            g.append(sc(converter(x, base), x, base, .9))
            ends[a] = (x + 30, base)
        elif kind == "gas":
            g.append(tank(x, base, 40, 26) + tank(x + 46, base, 30, 20))
            ends[a] = (x + 38, base)
        elif kind == "solar":
            g.append(solar_rows(x, x + 150, lambda xx: prof(xx) - 4, rows=((0.7, 30), (0.85, 17), (1.0, 4))))
            ends[a] = (x + 75, prof(x + 75))
        elif kind == "town":
            out, xx = [], x
            for k, w in enumerate([46, 22, 40, 34, 20]):
                gy = prof(xx + w / 2) + 1
                if k in (1, 4):
                    h = 40 if k == 1 else 30
                    out.append(f'<rect x="{f(xx)}" y="{f(gy - h)}" width="{w}" height="{h}" fill="#A39A6A" '
                               f'stroke="{INK}" stroke-width=".9"></rect>')
                else:
                    h = 14
                    out.append(f'<path d="M{f(xx)} {f(gy)} V{f(gy - h)} L{f(xx + w / 2)} {f(gy - h - 9)} L{f(xx + w)} '
                               f'{f(gy - h)} V{f(gy)} Z" fill="{DAY}" stroke="{INK}" stroke-width=".9" '
                               f'stroke-linejoin="round"></path><path d="M{f(xx)} {f(gy - h)} L{f(xx + w / 2)} '
                               f'{f(gy - h - 9)} L{f(xx + w)} {f(gy - h)}" fill="#C77E3C" opacity=".75"></path>')
                xx += w + 3
            g.append("".join(out))
            ends[a] = (x + 80, prof(x + 80))
        elif kind == "pyl":
            g.append(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.35">'
                     f'{pylon(x, prof(x) + 2, .72)}</g>')
            ends[a] = (x, prof(x))
    return "".join(g), ends


def cable(d: str, core: str = "#A5713C", sheath: float = 4.4, corew: float = 1.5) -> str:
    return (f'<path d="{d}" stroke="{INK}" stroke-width="{sheath}" fill="none" stroke-linecap="round" '
            f'stroke-linejoin="round"></path><path d="{d}" stroke="{core}" stroke-width="{corew}" fill="none" '
            f'stroke-linecap="round" stroke-linejoin="round"></path>')


def ring(x: float, y: float) -> str:
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="5.2" fill="{DAY}" stroke="{INK}" stroke-width="1.6"></circle>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="1.8" fill="{INK}"></circle>')


_ = (frange, spans, tips)
