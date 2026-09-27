"""New drawn pieces for the top pages (same flat ink language as the homepage: 1.5 px-ish ink, flat palette fills,
no gradients). Everything takes page coordinates; ``hp.Y["surf"]`` must be set to the page's surface first."""
from __future__ import annotations

import math

import hp
from hp import _frange, f, smooth
from frame import CHART, CLAY, DAY, HORIZON, INK, KHAKI, MUTED, OLIVE, PETROL


def solar_farm_at(x0: float, x1: float, prof) -> str:
    """The homepage solar farm, re-laid on a plot from x0 to x1 (homepage plot: 52 to 414)."""
    k = (x1 - x0) / 362
    X = lambda hx: x0 + (hx - 52) * k  # noqa: E731
    parts = []
    plot = [(X(64), prof(X(64)) - 60), (X(398), prof(X(398)) - 64), (X(414), prof(X(414))), (X(52), prof(X(52)))]
    parts.append(f'<path d="M{f(plot[0][0])} {f(plot[0][1])} L{f(plot[1][0])} {f(plot[1][1])} '
                 f'L{f(plot[2][0])} {f(plot[2][1])} L{f(plot[3][0])} {f(plot[3][1])} Z" fill="{OLIVE}"></path>')
    for s, up in [(0.46, 58), (0.58, 45), (0.71, 32), (0.85, 18), (1.0, 4)]:
        a, b = X(78 + (1 - s) * 30), X(392 - (1 - s) * 20)
        base = prof((a + b) / 2) - up
        h, lean, fh = 10 * s, 6 * s, 4.2 * s
        yf, yb = base - fh, base - fh - h
        legs = " ".join(f"M{f(xl)} {f(base)} V{f(yf)}" for xl in _frange(a + 6, b, 30 * s))
        parts.append(f'<path d="{legs}" stroke="{INK}" stroke-width=".9"></path>')
        parts.append(f'<path d="M{f(a)} {f(yf)} L{f(b)} {f(yf)} L{f(b - lean)} {f(yb)} L{f(a - lean)} {f(yb)} Z" '
                     f'fill="{CHART}" stroke="{INK}" stroke-width=".9" stroke-linejoin="round"></path>')
        cells = " ".join(f"M{f(xc)} {f(yf)} L{f(xc - lean)} {f(yb)}" for xc in _frange(a + 9 * s, b - 2, 9 * s))
        parts.append(f'<path d="{cells} M{f(a - lean / 2)} {f((yf + yb) / 2)} H{f(b - lean / 2)}" '
                     f'stroke="{INK}" stroke-width=".55" opacity=".4"></path>')
    fence = " ".join(f"M{f(xp)} {f(prof(xp) + 0.5)} v-9" for xp in _frange(X(58), X(412), 16 * k))
    parts.append(f'<path d="{fence} M{f(X(52))} {f(prof(X(52)) - 6)} L{f(X(414))} {f(prof(X(414)) - 6)}" '
                 f'stroke="{INK}" stroke-width=".7" opacity=".7"></path>')
    return "\n".join(parts)


def lng_terminal(x: float, base: float) -> str:
    """Two full-containment LNG tanks (flat-domed cylinders), a stair tower and a pipe rack."""
    out = []
    for tx in (x, x + 70):
        w, h = 60, 40
        out.append(f'<path d="M{f(tx)} {f(base)} V{f(base - h)} Q{f(tx + w / 2)} {f(base - h - 13)} {f(tx + w)} '
                   f'{f(base - h)} V{f(base)} Z" fill="{DAY}" stroke="{INK}" stroke-width="1.1"></path>')
        out.append(f'<path d="M{f(tx)} {f(base - h + 11)} H{f(tx + w)} M{f(tx)} {f(base - h + 24)} H{f(tx + w)}" '
                   f'stroke="{INK}" stroke-width=".6" opacity=".25"></path>')
        out.append(f'<path d="M{f(tx + 8)} {f(base)} L{f(tx + 26)} {f(base - h - 4)}" stroke="{INK}" '
                   f'stroke-width=".8" opacity=".55"></path>')
        out.append(f'<rect x="{f(tx + w / 2 - 4)}" y="{f(base - h - 15)}" width="8" height="5" fill="{KHAKI}" '
                   f'stroke="{INK}" stroke-width=".7"></rect>')
    rack = (f"M{f(x + 60)} {f(base - 8)} H{f(x + 70)} M{f(x + 130)} {f(base - 8)} H{f(x + 160)} "
            f"M{f(x + 130)} {f(base - 13)} H{f(x + 160)} M{f(x + 144)} {f(base)} V{f(base - 15)} "
            f"M{f(x + 156)} {f(base)} V{f(base - 15)}")
    out.append(f'<path d="{rack}" stroke="{INK}" stroke-width="1.1" fill="none"></path>')
    return "\n".join(out)


def lng_carrier(x: float, wl: float, L: float = 128) -> str:
    """An LNG carrier with four spherical cargo tanks, at its waterline wl, bow to the left."""
    hull = (f"M{f(x)} {f(wl - 12)} L{f(x + L)} {f(wl - 12)} L{f(x + L - 6)} {f(wl + 3)} L{f(x + 9)} {f(wl + 3)} Z")
    out = [f'<path d="{hull}" fill="{PETROL}" stroke="{INK}" stroke-width="1"></path>',
           f'<path d="M{f(x + 3)} {f(wl - 7)} H{f(x + L - 2)}" stroke="{CLAY}" stroke-width="1.6" opacity=".9"></path>']
    for i in range(4):
        cx = x + 20 + i * 24
        out.append(f'<path d="M{f(cx - 10)} {f(wl - 12)} A10 10 0 0 1 {f(cx + 10)} {f(wl - 12)} Z" fill="{DAY}" '
                   f'stroke="{INK}" stroke-width=".9"></path>')
    out.append(f'<rect x="{f(x + L - 22)}" y="{f(wl - 27)}" width="16" height="15" fill="{DAY}" stroke="{INK}" '
               f'stroke-width=".9"></rect>'
               f'<rect x="{f(x + L - 16)}" y="{f(wl - 33)}" width="5" height="6" fill="{INK}"></rect>')
    out.append(f'<path d="M{f(x + 12)} {f(wl + 6)} h{f(L - 30)}" stroke="{DAY}" stroke-width="1" opacity=".4"></path>')
    return "\n".join(out)


def monopile_turbine(x: float, sea: float, bed: float, h: float, spin: str, ang: float) -> str:
    """An offshore turbine cut in section: yellow transition piece at the waterline, monopile to the seabed."""
    return (f'<path d="M{f(x - 2.4)} {f(sea - 6)} V{f(bed + 10)} H{f(x + 2.4)} V{f(sea - 6)} Z" fill="{INK}" '
            f'opacity=".85"></path>'
            f'<rect x="{f(x - 3.6)}" y="{f(sea - 14)}" width="7.2" height="12" fill="{CHART}" stroke="{INK}" '
            f'stroke-width=".8"></rect>'
            + hp.turbine(x, sea - 14, h, h * .5, spin, ang))


def nuclear(x: float, base: float) -> str:
    """A nuclear station: reactor building with a dome, turbine hall, a short stack."""
    return "\n".join([
        f'<rect x="{f(x + 50)}" y="{f(base - 30)}" width="70" height="30" fill="{DAY}" stroke="{INK}" '
        f'stroke-width="1"></rect>',
        f'<path d="M{f(x + 56)} {f(base - 22)} H{f(x + 114)} M{f(x + 56)} {f(base - 12)} H{f(x + 114)}" '
        f'stroke="{INK}" stroke-width=".6" opacity=".3"></path>',
        f'<path d="M{f(x)} {f(base)} V{f(base - 40)} Q{f(x + 25)} {f(base - 70)} {f(x + 50)} {f(base - 40)} '
        f'V{f(base)} Z" fill="{PETROL}" stroke="{INK}" stroke-width="1.1"></path>',
        f'<path d="M{f(x + 4)} {f(base - 40)} Q{f(x + 25)} {f(base - 64)} {f(x + 46)} {f(base - 40)}" '
        f'stroke="{DAY}" stroke-width=".8" opacity=".35" fill="none"></path>',
        f'<rect x="{f(x + 126)}" y="{f(base - 58)}" width="6" height="58" fill="{DAY}" stroke="{INK}" '
        f'stroke-width=".9"></rect>',
    ])


def ridge(pts: list[tuple[float, float]], bottom: float, fill: str, op: str = "1") -> str:
    x0, x1 = pts[0][0], pts[-1][0]
    return (f'<path d="{smooth(pts)} L{f(x1)} {f(bottom)} L{f(x0)} {f(bottom)} Z" fill="{fill}" '
            f'opacity="{op}"></path>')


def field(top: list[tuple[float, float]], prof, xa: float, xb: float, stripes: list[list[tuple[float, float]]]
          ) -> str:
    """Energised land: a chartreuse field from the top curve down to the cut, with faint field boundaries."""
    bottom = " ".join(f"L{f(x)} {f(prof(x))}" for x in _frange(xa, xb, 20)[::-1])
    out = [f'<path d="{smooth(top)} L{f(xb)} {f(prof(xb))} {bottom} Z" fill="{CHART}"></path>']
    if stripes:
        out.append(f'<path d="{" ".join(smooth(s) for s in stripes)}" stroke="{OLIVE}" stroke-width="1" '
                   f'fill="none" opacity=".45"></path>')
    return "\n".join(out)


def wavelets(items: list[tuple[float, float, float]], op: str = ".35") -> str:
    d = " ".join(f"M{f(x)} {f(y)} h{f(ln)}" for x, y, ln in items)
    return f'<path d="{d}" stroke="{DAY}" stroke-width="1" opacity="{op}"></path>'


_ = (math, MUTED, HORIZON)
