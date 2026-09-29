"""Explorer page, round 1, designer 2: "The tour".

The page shows how the app is navigated. After the opening and the repo link, three app windows follow in the
homepage notebook frame: the catalogue, the Elexon source page, the market index price page. Each is cropped to the
part that tells its step, and a chartreuse ring sits on the control the reader clicks. A chartreuse cable (the
click trail) runs from that ring, out of the window and round the margin to the next window. Below, the technology
section: front end in topsoil, backend in silver, and the request drawn as one cable descending through the strata
(browser, FastAPI, GridflowClient, DuckDB at the silver and gold contact). Then Architecture and Models in gold, and
the deep foot.

Every fact comes from explorer-pack/ or the screenshots; lines that are not pack wording go through ``N()`` and are
listed in copy-new.json. Chrome and scenery are the locked models page's (models-r2/gen.py).

Usage: gen.py [desktop] [phone]   probes on 127.0.0.1:9772 (this folder), then writes the boards.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import html  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).parent
DL = HERE.parent.parent
sys.path.insert(0, str(DL / "p27-r1" / "A"))

import frame  # noqa: E402
import hp  # noqa: E402
from hp import f  # noqa: E402

_spec = importlib.util.spec_from_file_location("models_gen", DL / "models-r2" / "gen.py")
mg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mg)  # type: ignore[union-attr]

NAME = "2-explorer"
PORT = 9772
BASE = f"http://127.0.0.1:{PORT}/"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
W, PW = 1440, 390

PETROL, HORIZON, CHART, OLIVE = "#155A6E", "#3E8C97", "#AFC64E", "#66793B"
INK, DAY, CLAY, KHAKI = "#1C2B22", "#F6F4EC", "#C77E3C", "#A39A6A"
BRONZE, SILVER, GOLD = "#A5713C", "#9FADAB", "#C2A14A"
T_GOLD, T_SILVER, T_TOP = "#E9DDAF", "#DCE2DF", "#ECE8DA"

REPO = "https://github.com/EBentham/gridflow-explorer"
GH_REPO = "https://github.com/EBentham/gridflow"
NAV = [("Home", "index.html"), ("Data sources", "data-sources.html"), ("Architecture", "architecture.html"),
       ("Models", "models.html"), ("Explorer", "explorer.html"), ("About", "index.html#about")]

NEW: list[str] = []
ALL: list[str] = []


def N(s: str) -> str:
    """Register a line of copy that is not pack wording (for the notes)."""
    NEW.append(s)
    return s


def esc(s: str) -> str:
    return html.escape(s, quote=False)


# =============================================================== chrome (the locked pages', plus Explorer)
def masthead() -> str:
    li = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if n == "Explorer" else ""}>{n}</a></li>'
                 for n, h in NAV)
    return (f'<header class="mast"><a class="brand" href="index.html">gridflow</a>'
            f'<nav aria-label="Primary"><ul>{li}</ul></nav></header>')


def footer() -> str:
    links = "".join(f'<li><a href="{h}">{n}</a></li>' for n, h in NAV[1:] + [("GitHub", GH_REPO)])
    return (f'<footer class="st st-deep"><div class="foot"><a class="brand" href="index.html">'
            f'gridflow</a><ul>{links}</ul></div></footer>')


# =============================================================== the three windows
# crop = (x0, y0, x1, y1, shown width) in screenshot pixels; ring = (x0, y0, x1, y1) in screenshot pixels
SHOTS = {
    "cat": {
        "stem": "catalogue", "h": 1480, "tab": "All sources",
        "alt": ("The gridflow explorer catalogue: a petrol band naming the eight sources and gridflow gold, then "
                "columns for Electricity, Gas and Weather, with Elexon BMRS first under Electricity."),
        "desk": (96, 0, 1440, 660, 1000), "phone": (120, 334, 546, 646, 355),
        "ring": (186, 481, 312, 513),
    },
    "elx": {
        "stem": "source-elexon", "h": 1401, "tab": "Elexon BMRS",
        "alt": ("The Elexon BMRS page in gridflow explorer: its time series in groups, how often gridflow fetches "
                "each, and the Explorer screens that read them, Market index price among them."),
        "desk": (96, 0, 1100, 559, 880), "phone": (120, 160, 600, 566, 355),
        "ring": (851, 503, 982, 530), "ring_ph": (128, 498, 604, 556),
    },
    "mip": {
        "stem": "market-index-price", "h": 1401, "tab": "Market index price",
        "alt": ("The Market index price page in gridflow explorer: the price per half-hour from 16 to 22 September "
                "2026 in pounds per MWh, highest 207.07 on Mon 21 at 18:00, lowest minus 19.03 on Sun 20 at 16:00, "
                "the runs below zero banded, and a key of the latest half-hour and the window's range beside it."),
        "desk": (104, 0, 1420, 812, 960), "phone": (572, 394, 1106, 798, 355),
    },
}


def crop_box(key: str, ph: bool) -> tuple[float, float, float, int]:
    x0, y0, x1, y1, w = SHOTS[key]["phone" if ph else "desk"]
    s = w / (x1 - x0)
    return s, x0, y0, round((y1 - y0) * s)


def window(key: str, ph: bool) -> str:
    c = SHOTS[key]
    s, x0, y0, h = crop_box(key, ph)
    w = c["phone" if ph else "desk"][4]
    iw, ih = 1440 * s, c["h"] * s
    stem = c["stem"]
    ring = ""
    rk = "ring_ph" if ph and "ring_ph" in c else "ring"
    if rk in c:
        a, b, cc, d = c[rk]
        ring = (f'<span class="ring" data-t="ring-{key}" aria-hidden="true" style="left: {f((a - x0) * s)}px; '
                f'top: {f((b - y0) * s)}px; width: {f((cc - a) * s)}px; height: {f((d - b) * s)}px"></span>')
    return (f'<div class="win" data-t="win-{key}" style="width: {w}px">'
            f'<div class="wbar"><span class="wtab">{c["tab"]}</span><span class="wname">gridflow explorer</span></div>'
            f'<div class="wbody" style="height: {h}px"><picture>'
            f'<source srcset="explorer-shots/{stem}-dark.png" media="(prefers-color-scheme: dark)">'
            f'<img src="explorer-shots/{stem}-light.png" alt="{c["alt"]}" width="{round(iw)}" height="{round(ih)}" '
            f'style="width: {f(iw)}px; height: {f(ih)}px; left: {f(-x0 * s)}px; top: {f(-y0 * s)}px"></picture>'
            f'{ring}</div></div>')


def whole(key: str) -> str:
    stem = SHOTS[key]["stem"]
    t = N("See the whole screen")
    return (f'<p class="open"><a class="lt" href="explorer-shots/{stem}-light.png">{t}</a>'
            f'<a class="dk" href="explorer-shots/{stem}-dark.png">{t}</a></p>')


STEPS = [
    ("cat", "All sources",
     "The app opens on the catalogue: the eight sources and gridflow gold, grouped Electricity, Gas and Weather."),
    ("elx", "Elexon BMRS",
     "One click on Elexon BMRS: its datasets, how often gridflow fetches each, and the screens that read them."),
    ("mip", "Market index price",
     "From the Elexon page, Market index price: each half-hour’s price over seven days, its extremes labelled "
     "and the runs below zero banded."),
]


def step(i: int, ph: bool) -> str:
    key, head, line = STEPS[i]
    cap = (f'<figcaption class="scap" data-t="cap-{key}"><span class="jn" aria-hidden="true">{i + 1}</span>'
           f'<h3>{head}</h3><p>{N(line)}</p>{whole(key)}</figcaption>')
    win = window(key, ph)
    inner = cap + win if (ph or i == 1) else win + cap
    return f'<figure class="step s{i + 1}" data-t="step-{key}">{inner}</figure>'


def tour(ph: bool) -> str:
    intro = ("Each source has a page; each dataset family has a page. Time series get charts; event feeds and "
             "reference tables get tables.")
    return (f'<section class="tour" data-section="tour" aria-labelledby="h-tour">'
            f'<div class="thead"><h2 id="h-tour">{N("From the catalogue to a chart in two clicks")}</h2>'
            f'<p>{intro}</p></div>{"".join(step(i, ph) for i in range(3))}</section>')


# =============================================================== how it's built
CODE_FILE = DL / "explorer-pack" / "code" / "market-index-price.index.tsx"
CODE_PATH = "src/views/elexon/market-index-price/index.tsx"


def code_excerpt() -> str:
    lines = CODE_FILE.read_text(encoding="utf-8").splitlines()
    i = next(k for k, s in enumerate(lines) if s.strip() == "datasets: [")
    j = next(k for k in range(i, len(lines)) if lines[k].strip() == "],")
    part = [s[2:] for s in lines[i:j + 1]]
    assert len(part) <= 15, len(part)
    out = []
    for s in part:
        e = esc(s)
        e = re.sub(r"(&#x27;|')([^'&]*?)(&#x27;|')", r'<span class="s">\1\2\3</span>', e)
        e = re.sub(r"\b(id|body|label|title|values|column|color|datasets)(:)", r'<span class="k">\1</span>\2', e)
        out.append(e)
    return "\n".join(out)


B_LINES = [
    ("Draws every dataset as charts and tables, in light and dark", "React and TypeScript"),
    ("Serves each dataset’s rows to the page", "a Python API built with FastAPI"),
    ("Reads gridflow’s silver and gold tables, read-only", "DuckDB, through gridflow’s own client"),
]


def built(ph: bool) -> str:
    """The "What it does" section (Bobbo's pick): three verb-led lines, each level with its part of the drawing."""
    li = "".join(f'<li data-t="i{k}"><p>{N(w)}: <span class="tech">{N(t)}</span>.</p></li>'
                 for k, (w, t) in enumerate(B_LINES))
    sec = (f'<section class="built" data-section="built" aria-labelledby="h-built">'
           f'<h2 id="h-built" data-t="bh">{N("How it’s built")}</h2><ul class="does">{li}</ul>'
           f'<div class="bspace" data-t="bspace"></div></section>')
    return sec.replace("read-only", '<span class="nw">read-only</span>')


def rest(ph: bool) -> str:
    arch = ("Raw API responses land in bronze, cleaned and typed tables settle in silver, and cross-source joins and "
            "derived columns sit in gold.")
    mod = "gridflow-models is a separate Python library that reads gridflow’s silver tables."
    return (f'<section class="rest" data-section="links" data-t="rest" aria-labelledby="h-rest">'
            f'<h2 id="h-rest">{N("The rest of gridflow")}</h2>'
            f'<div class="re"><h3><a href="architecture.html">Architecture</a></h3><p>{arch}</p></div>'
            f'<div class="re"><h3><a href="models.html">Models</a></h3><p>{mod}</p></div></section>')


# =============================================================== drawing parts
def terminal(x: float, y: float, tint: str = T_GOLD, r: float = 5.5) -> str:
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{tint}" stroke="{INK}" stroke-width="1.8"></circle>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r / 3)}" fill="{INK}"></circle>')


def cab(d: str, core: str = CHART, k: float = 1.0) -> str:
    if core == CHART:
        return hp.cable(d, core, 5.2 * k, 2.3 * k)
    return hp.cable(d, core, 4.4 * k, 1.5 * k)


def g_browser(x: float, y: float, w: float, h: float) -> str:
    """A browser window with a chart in it: ink bar, daylight body, a price line."""
    bar = max(8.0, h * .14)
    ax, ay, aw, ah = x + w * .12, y + bar + h * .14, w * .78, h * .56
    pts = [.55, .35, .5, .2, .62, .82, .78, .4, .25, .3, .45, .38]
    line = "M" + " L".join(f"{f(ax + aw * i / (len(pts) - 1))} {f(ay + ah * v)}" for i, v in enumerate(pts))
    return (f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="3" fill="{DAY}" stroke="{INK}" '
            f'stroke-width="1.5"></rect><rect x="{f(x + .75)}" y="{f(y + .75)}" width="{f(w - 1.5)}" height="{f(bar)}" '
            f'rx="2" fill="{INK}"></rect><rect x="{f(x + w * .07)}" y="{f(y + bar * .35)}" width="{f(w * .26)}" '
            f'height="{f(bar * .65 + .75)}" fill="{DAY}"></rect>'
            f'<path d="M{f(ax)} {f(ay + ah * .72)} H{f(ax + aw)}" stroke="{INK}" stroke-width=".7" opacity=".4"></path>'
            f'<path d="{line}" stroke="{HORIZON}" stroke-width="1.6" fill="none" stroke-linejoin="round"></path>'
            f'<path d="M{f(ax - 3)} {f(ay - 4)} V{f(ay + ah + 3)} H{f(ax + aw + 2)}" stroke="{INK}" stroke-width="1" '
            f'fill="none"></path>')


def g_api(x: float, y: float, w: float, h: float) -> str:
    """The FastAPI app: a server plate with its routes, one row each."""
    rows = 4
    out = [f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="3" fill="{DAY}" stroke="{INK}" '
           f'stroke-width="1.5"></rect>']
    for k in range(rows):
        yy = y + h * (k + .5) / rows
        out.append(f'<circle cx="{f(x + w * .13)}" cy="{f(yy)}" r="{f(h * .045 + 1)}" fill="{CHART}" stroke="{INK}" '
                   f'stroke-width=".9"></circle>')
        out.append(f'<path d="M{f(x + w * .24)} {f(yy)} H{f(x + w * (.62 + .1 * (k % 2)))}" stroke="{INK}" '
                   f'stroke-width="1.4" opacity=".7"></path>')
        if k:
            out.append(f'<path d="M{f(x + 1)} {f(y + h * k / rows)} H{f(x + w - 1)}" stroke="{INK}" '
                       f'stroke-width=".6" opacity=".35"></path>')
    return "".join(out)


def g_client(x: float, y: float, w: float, h: float) -> str:
    """GridflowClient as the architecture page draws it: a returned table (Polars)."""
    hd = h * .24
    out = [f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="3" fill="{DAY}" stroke="{INK}" '
           f'stroke-width="1.5"></rect>',
           f'<rect x="{f(x + 1)}" y="{f(y + 1)}" width="{f(w - 2)}" height="{f(hd - 1)}" fill="{T_TOP}"></rect>',
           f'<path d="M{f(x)} {f(y + hd)} H{f(x + w)}" stroke="{INK}" stroke-width="1.2"></path>']
    rh = (h - hd) / 3
    for k in range(3):
        if k % 2 == 0:
            out.append(f'<rect x="{f(x + 1)}" y="{f(y + hd + k * rh + .5)}" width="{f(w - 2)}" height="{f(rh - 1)}" '
                       f'fill="#EFEBDF"></rect>')
    out.append(f'<path d="M{f(x + w / 3)} {f(y + 1)} V{f(y + h - 1)} M{f(x + 2 * w / 3)} {f(y + 1)} V{f(y + h - 1)}" '
               f'stroke="{INK}" stroke-width=".7" opacity=".4"></path>')
    ticks = " ".join(f"M{f(x + w * c)} {f(y + (hd / 2 if r == 0 else hd + (r - 1) * rh + rh / 2))} h{f(w * .17)}"
                     for c in (.09, .42, .76) for r in range(4))
    out.append(f'<path d="{ticks}" stroke="{INK}" stroke-width="1.5" opacity=".7"></path>')
    return "".join(out)


def g_drum(cx: float, top: float, bot: float, rx: float, ry: float) -> str:
    l, r = cx - rx, cx + rx
    body = (f'<path d="M{f(l)} {f(top)} V{f(bot)} A{f(rx)} {f(ry)} 0 0 0 {f(r)} {f(bot)} V{f(top)} Z" fill="{DAY}" '
            f'stroke="{INK}" stroke-width="1.5"></path>')
    lid = (f'<ellipse cx="{f(cx)}" cy="{f(top)}" rx="{f(rx)}" ry="{f(ry)}" fill="{DAY}" stroke="{INK}" '
           f'stroke-width="1.5"></ellipse>')
    bands = "".join(f'<path d="M{f(l)} {f(y)} A{f(rx)} {f(ry)} 0 0 0 {f(r)} {f(y)}" stroke="{INK}" '
                    f'stroke-width=".8" fill="none" opacity=".45"></path>'
                    for y in (top + (bot - top) * .38, top + (bot - top) * .72))
    return body + lid + bands


def slab(x: float, y: float, fill: str, w: float = 44, n: int = 2) -> str:
    out = []
    for k in range(n):
        yy = y + k * 11
        out.append(f'<rect x="{f(x - w / 2)}" y="{f(yy)}" width="{f(w)}" height="9" fill="{fill}" stroke="{INK}" '
                   f'stroke-width=".9"></rect>')
        out.append(f'<path d="{" ".join(f"M{f(x + c)} {f(yy + 1)} V{f(yy + 8)}" for c in (-w / 4, 0, w / 4))}" '
                   f'stroke="{INK}" stroke-width=".6" opacity=".38"></path>')
    return "".join(out)


def rpath(pts: list[tuple[float, float]], r: float = 12) -> str:
    """An orthogonal polyline with rounded corners."""
    d = f"M{f(pts[0][0])} {f(pts[0][1])}"
    for i in range(1, len(pts) - 1):
        (ax, ay), (bx, by), (cx, cy) = pts[i - 1], pts[i], pts[i + 1]
        la = max(abs(bx - ax), abs(by - ay))
        lb = max(abs(cx - bx), abs(cy - by))
        rr = min(r, la / 2, lb / 2)
        ux, uy = (bx - ax) / (la or 1), (by - ay) / (la or 1)
        vx, vy = (cx - bx) / (lb or 1), (cy - by) / (lb or 1)
        d += f" L{f(bx - ux * rr)} {f(by - uy * rr)} Q{f(bx)} {f(by)} {f(bx + vx * rr)} {f(by + vy * rr)}"
    d += f" L{f(pts[-1][0])} {f(pts[-1][1])}"
    return d


# =============================================================== the ground and its drawing
def R(t: dict, k: str) -> tuple[float, float, float, float]:
    return tuple(t[k])  # type: ignore[return-value]


def layout(m: dict, ph: bool) -> dict:
    """Contacts and part positions (ground-relative) from the measured anchors."""
    t = m["t"]
    Y: dict = {"S": 176 if ph else 300}
    i0, i1, i2 = R(t, "i0"), R(t, "i1"), R(t, "i2")
    if not ph:
        Y["fe"] = i0[1] - 4
        Y["CS"] = i1[1] - 56
        Y["api"] = i1[1] + 2
        Y["cli"] = Y["api"] + 64 + 44
        Y["CG"] = i2[1] - 22
        Y["dtop"] = Y["CG"] - 40
        Y["dbot"] = Y["CG"] + 52
        Y["need"] = max(Y["dbot"] + 14 + 84, i2[3] + 90)
    else:
        Y["fe"] = i0[1] - 2
        Y["CS"] = i1[1] - 40
        Y["api"] = i1[1] + 2
        Y["cli"] = Y["api"] + 44 + 30
        Y["CG"] = i2[1] - 18
        Y["dtop"] = Y["CG"] - 26
        Y["dbot"] = Y["CG"] + 34
        Y["need"] = max(Y["dbot"] + 10 + 60, i2[3] + 56)
    Y["Hd"] = m["G"]
    return Y


def tour_cable(m: dict, ph: bool) -> str:
    """The click trail: out of the ringed control, round the margin, into the next window's tab bar."""
    if ph:
        return ""
    t = m["t"]
    r1, r2 = R(t, "ring-cat"), R(t, "ring-elx")
    w1, w2, w3 = R(t, "win-cat"), R(t, "win-elx"), R(t, "win-mip")
    y1 = (r1[1] + r1[3]) / 2
    b2 = w2[1] + 21
    p1 = rpath([(r1[0], y1), (40, y1), (40, b2), (w2[0], b2)], 14)
    y2 = (r2[1] + r2[3]) / 2
    b3 = w3[1] + 21
    p2 = rpath([(r2[2], y2), (1400, y2), (1400, b3), (w3[2], b3)], 14)
    return (cab(p1) + cab(p2) + terminal(w2[0], b2, T_TOP) + terminal(w3[2], b3, T_TOP)
            + f'<circle cx="{f(r1[0])}" cy="{f(y1)}" r="3.2" fill="{INK}"></circle>'
            + f'<circle cx="{f(r2[2])}" cy="{f(y2)}" r="3.2" fill="{INK}"></circle>')


def flow(Y: dict, ph: bool) -> tuple[str, str]:
    """The request, drawn: browser, FastAPI, GridflowClient, DuckDB over silver and gold. Returns (svg, labels)."""
    o: list[str] = []
    lab: list[str] = []
    if not ph:
        cx, bw, bh, aw, ah, cw, ch, rx, ry = 860, 132, 86, 120, 64, 96, 58, 68, 13
        lx = cx + 92
    else:
        cx, bw, bh, aw, ah, cw, ch, rx, ry = 56, 78, 52, 72, 44, 64, 40, 36, 8
        lx = 0
    yb = Y["fe"] + (6 if not ph else 4)
    ya, yc, dt, db = Y["api"], Y["cli"], Y["dtop"], Y["dbot"]
    # the request cable, top to bottom
    o.append(cab(f"M{cx} {f(yb + bh)} V{f(ya)}"))
    o.append(cab(f"M{cx} {f(ya + ah)} V{f(yc)}"))
    o.append(cab(f"M{cx} {f(yc + ch)} V{f(dt - ry)}"))
    # DuckDB reads silver and gold: thin ink lines out to the tables either side of the contact
    sx = 190 if not ph else 0
    if not ph:
        for side in (-1, 1):
            o.append(f'<path d="M{f(cx + side * rx * .8)} {f(dt + 6)} L{f(cx + side * sx)} {f(Y["CG"] - 44)} '
                     f'M{f(cx + side * rx * .8)} {f(db - 4)} L{f(cx + side * sx)} {f(Y["CG"] + 38)}" stroke="{INK}" '
                     f'stroke-width=".9" opacity=".6"></path>')
            o.append(slab(cx + side * sx, Y["CG"] - 56, T_SILVER))
            o.append(slab(cx + side * sx, Y["CG"] + 34, T_GOLD))
    parts = [g_browser(cx - bw / 2, yb, bw, bh), g_api(cx - aw / 2, ya, aw, ah), g_client(cx - cw / 2, yc, cw, ch),
             g_drum(cx, dt, db, rx, ry)]
    parts += [terminal(cx, yb + bh, T_TOP, 5 if not ph else 4), terminal(cx, ya, T_SILVER, 5 if not ph else 4),
              terminal(cx, ya + ah, T_SILVER, 5 if not ph else 4), terminal(cx, yc, T_SILVER, 5 if not ph else 4),
              terminal(cx, yc + ch, T_SILVER, 5 if not ph else 4)]
    cy = mg.wave_y(Y["CS"], 5 if ph else 8, 2.1, cx, PW if ph else W)
    parts.append(hp.sc(frame.sleeve(cx, cy, T_SILVER), cx, cy, .6) if ph else frame.sleeve(cx, cy, T_SILVER))
    if not ph:
        lab += [f'<text x="{lx}" y="{f(yb + bh / 2 + 5)}">{N("browser (React)")}</text>',
                f'<text x="{lx}" y="{f(ya + ah / 2 + 5)}">FastAPI</text>',
                f'<text x="{lx}" y="{f(yc + ch / 2 + 5)}" class="m">GridflowClient</text>',
                f'<text x="{cx}" y="{f(db + ry + 26)}" text-anchor="middle">{N("DuckDB over silver and gold")}</text>',
                f'<text x="{cx - sx}" y="{f(Y["CG"] - 66)}" text-anchor="middle">silver</text>',
                f'<text x="{cx + sx}" y="{f(Y["CG"] + 74)}" text-anchor="middle">gold</text>']
    else:
        lab += [f'<text x="{cx}" y="{f(yb - 8)}" text-anchor="middle" class="ht">browser</text>',
                f'<text x="{cx}" y="{f(ya - 9)}" text-anchor="middle" class="hs">FastAPI</text>',
                f'<text x="{cx}" y="{f(yc - 9)}" text-anchor="middle" class="m hs">GridflowClient</text>',
                f'<text x="{cx}" y="{f(db + ry + 18)}" text-anchor="middle">DuckDB</text>']
    return "".join(o + parts), "".join(lab)


def flow_aria() -> str:
    return N("Drawing of a request: the browser running the React app calls FastAPI, FastAPI reads through "
             "GridflowClient, and GridflowClient reads DuckDB over gridflow's silver and gold tables.")


def ground_svg(m: dict, ph: bool) -> tuple[str, str]:
    """(background svg below the content, overlay svg above it)."""
    w = PW if ph else W
    Y = layout(m, ph)
    S = Y["S"]
    if ph:
        land, _lab = mg.landscape_phone(S)
        land = re.sub(r'<path d="[^"]*" stroke="#F6F4EC" stroke-width="\.8" opacity="\.75"></path>', "", land)
        prof = mg.pprof_for(S)
        amp = (5, 5)
    else:
        land, _lab = mg.landscape_desk(S)
        prof = mg.dprof
        amp = (8, 7)
    top, ink = mg.ground(Y, w, prof, amp)
    fl, fl_lab = flow(Y, ph)
    Hd = Y["Hd"]
    bg = (f'<svg class="gnd" width="{w}" height="{f(Hd)}" viewBox="0 0 {w} {f(Hd)}" aria-hidden="true">'
          f'<defs>{hp.PATTERNS}</defs>{top}{land}{ink}</svg>'
          f'<svg class="flow" width="{w}" height="{f(Hd)}" viewBox="0 0 {w} {f(Hd)}" role="img" '
          f'aria-label="{flow_aria()}">{fl}<g class="lab">{fl_lab}</g></svg>')
    ov = (f'<svg class="trail" width="{w}" height="{f(Hd)}" viewBox="0 0 {w} {f(Hd)}" aria-hidden="true">'
          f'{tour_cable(m, ph)}</svg>')
    return bg, ov


# =============================================================== page
def body(m: dict | None, ph: bool = False) -> str:
    NEW.clear()
    lede = ("gridflow explorer is a web app for browsing everything gridflow collects: GB and European energy-market "
            "data from eight public sources, plus the tables gridflow builds from them.")
    second = N("A React and TypeScript front end over a Python backend that reads gridflow through its own client.")
    third = N("It is not hosted, so it is shown here in screenshots from its own screenshot tool, in light and dark.")
    repo = (f'<p class="repo">{N("Source on GitHub:")} <a class="alt" href="{REPO}"><code>EBentham/'
            f'<wbr>gridflow-explorer</code></a></p>')
    opening = (f'<section class="sky" data-section="opening">{masthead()}<div class="hero">'
               f'<h1>{N("A React front end over gridflow’s data")}</h1><div class="lede">'
               f'<p class="lead">{lede}</p><p>{second}</p><p>{third}</p>{repo}</div></div></section>')
    spacer = 0
    if m is not None:
        Y = layout(m, ph)
        bs = m["t"]["bspace"]
        spacer = max(0, round(Y["need"] - (m["t"]["rest"][1] - (bs[3] - bs[1]))))
        bg, ov = ground_svg(m, ph)
    else:
        bg = ov = ""
    inner = tour(ph) + built(ph).replace('<div class="bspace" data-t="bspace"></div>',
                                         f'<div class="bspace" data-t="bspace" style="height: {spacer}px"></div>') + rest(ph)
    ground = f'<div class="ground" data-t="ground">{bg}<div class="gin">{inner}</div>{ov}</div>'
    gran = ('<svg class="gran" width="100%" height="100%" aria-hidden="true"><defs><pattern id="p-gran-d" width="46" '
            'height="40" patternUnits="userSpaceOnUse"><path d="M8 8 h8 M12 4 v8 M30 26 h8 M34 22 v8 M20 34 h6 M23 31 '
            f'v6 M40 6 h5 M42.5 3.5 v5" stroke="{HORIZON}" stroke-width="1.1"></path></pattern></defs>'
            '<rect width="100%" height="100%" fill="url(#p-gran-d)" opacity=".5"></rect></svg>')
    deep = f'<div class="deep" data-section="foot">{gran}{mg.rough_edge(PW if ph else W)}{footer()}</div>'
    out = opening + ground + deep
    if ph:
        def brk(mm: re.Match[str]) -> str:
            inner_ = mm.group(1)
            if len(inner_.replace("<wbr>", "")) < 16 or "<wbr>" in inner_:
                return mm.group(0)
            return "<code>" + re.sub(r"([_/.])", r"\1<wbr>", inner_) + "</code>"
        out = re.sub(r"<code>((?:[^<]|<wbr>)+)</code>", brk, out)
    return out


CSS = """.sky{position:relative;box-sizing:border-box;padding:0 80px 40px;background:#155A6E}
.hero{display:grid;grid-template-columns:780px 440px;column-gap:60px;margin-top:64px;align-items:start}
.lede{padding-top:10px}
.lede .repo{margin-top:22px;color:#F6F4EC}
.lede .repo code{font-size:15px}
.ground{position:relative;background:#155A6E}
.gnd,.flow,.trail{position:absolute;left:0;top:0;display:block;overflow:visible}
.gnd{z-index:0}
.flow{z-index:1}
.trail{z-index:3;pointer-events:none}
.gin{position:relative;z-index:2;padding:370px 80px 0}
.flow .lab text{font-family:"Hanken Grotesk",sans-serif;font-style:italic;font-size:14px;fill:#1C2B22}
.flow .lab text.m{font-family:"Red Hat Mono",monospace;font-style:normal;font-size:13px}
.flow .lab text.hs{paint-order:stroke;stroke:#DCE2DF;stroke-width:5px;stroke-linejoin:round}
.flow .lab text.ht{paint-order:stroke;stroke:#ECE8DA;stroke-width:5px;stroke-linejoin:round}
.root h2{font-size:42px;font-weight:720;font-stretch:88%;line-height:1.02;letter-spacing:-.018em;color:#1C2B22}
.root h3{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.005em;color:#1C2B22;margin:0 0 8px}
.thead{display:grid;grid-template-columns:520px 560px;column-gap:80px;align-items:end}
.thead p,.built p,.re p{margin:0;font-size:16px;line-height:1.62;color:#3F4A3B;max-width:58ch}
.step{margin:0;display:grid;column-gap:40px;align-items:start}
.step.s1{margin-top:64px;grid-template-columns:1003px minmax(0,1fr)}
.step.s2{margin-top:84px;grid-template-columns:minmax(0,1fr) 883px}
.step.s3{margin-top:84px;grid-template-columns:963px minmax(0,1fr)}
.scap{padding-top:66px;max-width:320px}
.s2 .scap{padding-top:76px;max-width:340px}
.scap h3{margin-top:14px}
.scap p{margin:0;font-size:15px;line-height:1.55;color:#3F4A3B}
.scap p.open{margin-top:10px;font-size:14px}
.scap .open a{color:#1C2B22;font-weight:600}
.open .dk{display:none}
.jn{display:block;box-sizing:content-box;width:24px;height:24px;border:2px solid #1C2B22;border-radius:50%;background:#F6F4EC;font:700 13px/24px "Hanken Grotesk",sans-serif;text-align:center;color:#1C2B22;font-variant-numeric:tabular-nums}
.win{box-sizing:content-box;border:1.5px solid #1C2B22;border-radius:4px;overflow:hidden;background:#F6F4EC}
.wbar{display:flex;justify-content:space-between;align-items:flex-end;height:40px;background:#1C2B22;padding:0 18px 0 12px}
.wtab{background:#F6F4EC;color:#1C2B22;padding:11px 18px 12px;border-radius:3px 3px 0 0;font:600 14px/1 "Hanken Grotesk",sans-serif;white-space:nowrap}
.wname{align-self:center;color:#CFE0DC;font:400 13.5px/1 "Red Hat Mono",monospace;white-space:nowrap}
.wbody{position:relative;overflow:hidden}
.wbody picture{display:block}
.wbody img{position:absolute;display:block;max-width:none}
.ring{position:absolute;box-sizing:border-box;border:3px solid #AFC64E;outline:1.5px solid #1C2B22;border-radius:5px}
.built{margin-top:120px}
.built h2{margin:0 0 30px}
.bcol{width:660px}
.fe p+p{margin-top:12px}
.be{margin-top:120px}
.wt{margin:22px 0 8px;font-size:13.5px;line-height:1.4;color:#3F4A3B}
.wt code{font-size:12.5px;color:#1C2B22}
.root .well{font-size:13px;line-height:1.7;overflow-x:auto;scrollbar-width:none}
.built p code{color:#1C2B22}
.bspace{height:0}
.nw{white-space:nowrap}
.does{list-style:none;margin:0;padding:0;width:560px}
.does li{margin:0}
.does li+li{margin-top:150px}
.does li:nth-child(3){margin-top:230px}
.built .does p{margin:0;font-size:19px;line-height:1.45;color:#1C2B22;max-width:38ch}
.does .tech{color:#3F4A3B}
.rest{display:grid;grid-template-columns:420px minmax(0,1fr) minmax(0,1fr);column-gap:60px;align-items:start;padding-bottom:110px}
.rest h2{margin:0}
.re h3{margin:4px 0 8px}
.re h3 a{text-decoration-color:#66793B}
.deep{position:relative;background:#155A6E;color:#F6F4EC;margin-top:-2px}
.deep .gran{position:absolute;left:0;top:0;z-index:0}
.deep>*:not(.gran){position:relative;z-index:1}
.redge{display:block}
.foot{border-top:0}
@media (prefers-color-scheme: dark){
.wtab{background:transparent;color:#F6F4EC;box-shadow:inset 0 -2px 0 #AFC64E}
.open .lt{display:none}
.open .dk{display:inline}
}
"""

PH_CSS = """.ph .sky{padding:0 16px 26px}
.ph .mast{flex-wrap:wrap;row-gap:10px;padding-top:18px}
.ph .mast nav{flex:1 1 100%}
.ph .mast ul{flex-wrap:wrap;column-gap:18px;row-gap:2px}
.ph .hero{grid-template-columns:minmax(0,1fr);row-gap:18px;margin-top:34px}
.ph .hero h1{font-size:44px;line-height:.98}
.ph .lede{padding-top:0}
.ph .lede p{font-size:16.5px}
.ph .gin{padding:224px 16px 0}
.ph h2{font-size:31px}
.ph h3{font-size:20px}
.ph .thead{grid-template-columns:minmax(0,1fr);row-gap:12px}
.ph .thead p{font-size:15.5px}
.ph .step,.ph .step.s1,.ph .step.s2,.ph .step.s3{grid-template-columns:minmax(0,1fr);row-gap:14px;margin-top:40px}
.ph .step.s1{margin-top:30px}
.ph .scap,.ph .s2 .scap{padding-top:0;max-width:none}
.ph .scap h3{margin-top:10px}
.ph .wbar{height:34px;padding:0 10px 0 6px}
.ph .wtab{padding:9px 12px 10px;font-size:13px}
.ph .wname{font-size:12px}
.ph .built{margin-top:64px}
.ph .built h2{margin-bottom:22px}
.ph .bcol{width:auto;padding-left:116px}
.ph .be{margin-top:84px}
.ph .built p{font-size:15px;line-height:1.55}
.ph .wt code{font-size:11.5px}
.ph .root .well,.ph .well{font-size:12px;line-height:1.65;padding:8px 10px}
.ph .does{width:auto;padding-left:116px}
.ph .built .does p{font-size:16px;line-height:1.45}
.ph .does li+li{margin-top:96px}
.ph .does li:nth-child(3){margin-top:140px}
.ph .rest{grid-template-columns:minmax(0,1fr);row-gap:22px;padding-bottom:70px}
.ph .flow .lab text{font-size:12.5px}
.ph .flow .lab text.m{font-size:11px}
.ph .st{padding:0 16px}
.ph .foot{grid-template-columns:minmax(0,1fr);row-gap:14px;padding:36px 0 44px}
.ph .foot ul{flex-wrap:wrap;column-gap:18px;row-gap:6px}
"""

PROBE = """<pre id="m"></pre><script>
window.addEventListener('load',function(){Promise.all(['760 86px "Bricolage Grotesque"','720 42px "Bricolage Grotesque"','720 23px "Bricolage Grotesque"','400 16px "Hanken Grotesk"','600 16px "Hanken Grotesk"','italic 400 14px "Hanken Grotesk"','400 14px "Red Hat Mono"','500 14px "Red Hat Mono"'].map(function(q){return document.fonts.load(q)})).then(function(){return document.fonts.ready}).then(function(){setTimeout(function(){
var root=document.querySelector('.root').getBoundingClientRect(),g=document.querySelector('.ground').getBoundingClientRect(),o={t:{},secs:{},H:0,over:[],outside:[]};
document.querySelectorAll('[data-t]').forEach(function(e){var r=e.getBoundingClientRect();o.t[e.dataset.t]=[r.left-g.left,r.top-g.top,r.right-g.left,r.bottom-g.top];});
document.querySelectorAll('[data-section]').forEach(function(s){var r=s.getBoundingClientRect();o.secs[s.dataset.section]=[Math.round(r.top-root.top),Math.round(r.height)];});
o.G=Math.ceil(g.height);
o.H=Math.ceil(document.querySelector('main').getBoundingClientRect().bottom-root.top);
var LIM=__LIM__,RW=__RW__;
document.querySelectorAll('main p,main li,main h1,main h2,main h3,main a,main figcaption').forEach(function(e){if(e.scrollWidth>e.clientWidth+1)o.over.push((e.className||e.tagName)+':'+(e.scrollWidth-e.clientWidth)+':'+e.textContent.slice(0,40));var r=e.getBoundingClientRect();if(r.right-root.left>LIM+1&&!e.closest('.mast'))o.over.push('WIDE '+(e.className||e.tagName)+':'+Math.round(r.right-root.left)+':'+e.textContent.slice(0,30));});
document.querySelectorAll('.root *').forEach(function(e){if(e.closest('svg')&&e.tagName.toLowerCase()!=='svg')return;if(e.closest('.wbody')&&!e.matches('.wbody'))return;if(e.closest('pre.well')&&!e.matches('pre.well'))return;var r=e.getBoundingClientRect();if(r.width>0&&(r.right-root.left>RW+.5||r.left-root.left<-.5))o.outside.push((e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className||e.tagName)+':'+Math.round(r.left-root.left)+'..'+Math.round(r.right-root.left));});
o.outside=o.outside.slice(0,20);o.docW=document.documentElement.scrollWidth;
o.imgs=[].map.call(document.images,function(i){return i.naturalWidth});
var lab=[].slice.call(document.querySelectorAll('.flow .lab text')),tx=[].slice.call(document.querySelectorAll('.gin h2,.gin h3,.gin p,.gin pre'));o.hit=[];lab.forEach(function(a){var ra=a.getBoundingClientRect();tx.forEach(function(b){var rb=b.getBoundingClientRect();if(ra.left<rb.right&&rb.left<ra.right&&ra.top<rb.bottom&&rb.top<ra.bottom)o.hit.push(a.textContent+' x '+b.textContent.slice(0,20));});});
document.getElementById('m').textContent=JSON.stringify(o);},600);});});
</script>"""


def shell(inner: str, H: int, probe: bool, ph: bool = False) -> str:
    w = PW if ph else W
    css = CSS + PH_CSS if ph else CSS
    cls = "root ph" if ph else "root"
    pr = PROBE.replace("__LIM__", str(w - (16 if ph else 80))).replace("__RW__", str(w)) if probe else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Explorer</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{hp.FONTS}
<style>
{frame.BASE_CSS}{css}</style>
</helmet>
<div class="{cls}" style="width: {w}px; height: {H}px; overflow: hidden; position: relative">
<main>
{inner}
</main>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{H}}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
{pr}</body>
</html>
"""


def measure(html_text: str, w: int) -> dict:
    p = HERE / "_probe.html"
    p.write_text(frame.static(html_text), encoding="utf-8")
    out = None
    for attempt in range(3):
        try:
            out = subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--window-size={w},4000",
                                  "--virtual-time-budget=9000", "--dump-dom", f"{BASE}_probe.html?v={time.time_ns()}"],
                                 capture_output=True, text=True, encoding="utf-8", timeout=120)
            break
        except subprocess.TimeoutExpired:
            if attempt == 2:
                raise
    assert out is not None
    mm = re.search(r'<pre id="m">(.*?)</pre>', out.stdout, re.S)
    if not mm or not mm.group(1).strip():
        raise RuntimeError(f"probe failed: {out.stderr[-400:]}")
    p.unlink()
    return json.loads(html.unescape(mm.group(1)))


def to_static(dc: str) -> str:
    return frame.static(dc).replace('"explorer-shots/', '"../explorer-shots/').replace(
        'srcset="explorer-shots/', 'srcset="../explorer-shots/')


def build(ph: bool) -> dict:
    w = PW if ph else W
    name = f"{NAME}-{PW}" if ph else NAME
    m1 = measure(shell(body(None, ph), 30000, True, ph), w)
    m2 = measure(shell(body(m1, ph), 30000, True, ph), w)
    m3 = measure(shell(body(m2, ph), 30000, True, ph), w)
    H = m3["H"]
    out = shell(body(m2, ph), H, False, ph)
    frame.check(out)
    ALL.extend(NEW)
    (HERE / f"{name}.dc.html").write_text(out, encoding="utf-8")
    (HERE / "static").mkdir(exist_ok=True)
    (HERE / "static" / f"{name}.html").write_text(to_static(out), encoding="utf-8")
    print(name, "H", H, "secs", m3["secs"])
    for k in ("over", "outside", "hit", "imgs"):
        print(" ", k, m3.get(k))
    print("  docW", m3.get("docW"), "G", m2["G"], m3["G"])
    if m2["t"].get("rest") != m3["t"].get("rest"):
        print("  WARNING rest moved between passes", m2["t"].get("rest"), m3["t"].get("rest"))
    return {"H": H, "secs": m3["secs"], "Y": layout(m2, ph)}


def main() -> None:
    which = sys.argv[1:] or ["desktop", "phone"]
    meas = {}
    for k in which:
        meas[k] = build(k == "phone")
    (HERE / "copy-new.json").write_text(json.dumps(list(dict.fromkeys(ALL)), ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    (HERE / "measure.json").write_text(json.dumps(meas, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
