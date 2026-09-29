"""Explorer page, round 1, designer 3: "Above ground, below ground".

The app window stands on the site's land line, as the part a person sees: an ink tab bar in the homepage notebook's
style with four screens (real screenshots from the explorer's own screenshot tool, light or dark to match the
viewer). Below the ground the stack is drawn as strata, and that drawing is the technology section: the React front
end in the topsoil just under the window, then FastAPI, then GridflowClient over a read-only DuckDB, each a bed of
the topsoil; then gridflow's own silver and gold at depth. One chartreuse cable, the request's route, runs from the
window down through every bed. One real code excerpt from the market index price view sits beside the front end.

Every line comes from ``explorer-pack/EXPLORER-PACK.md`` or the screenshots (verbatim or shortened); lines that are
not pack wording are registered through ``N()`` and listed in ``copy-new.json``.

Usage: gen.py [desktop] [phone]   probes on 127.0.0.1:9763 (the design-loop root), then writes the boards.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # the shared modules below live outside this folder

import html  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).parent
DL = HERE.parent.parent
sys.path.insert(0, str(DL / "p27-r1" / "A"))

import frame  # noqa: E402
import hp  # noqa: E402
import scenery as sn  # noqa: E402
from hp import f, smooth  # noqa: E402

NAME = "3-explorer"
PORT = 9763
URL = f"http://127.0.0.1:{PORT}/explorer-r1/3/static/"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
W, PW = 1440, 390

PETROL, HORIZON, CHART, OLIVE = "#155A6E", "#3E8C97", "#AFC64E", "#66793B"
INK, DAY, KHAKI = "#1C2B22", "#F6F4EC", "#A39A6A"
SILVER, GOLD = "#9FADAB", "#C2A14A"
T_GOLD, T_SILVER, T_TOP = "#E9DDAF", "#DCE2DF", "#ECE8DA"
FAR = "#297382"

REPO = "https://github.com/EBentham/gridflow-explorer"
GH_GRIDFLOW = "https://github.com/EBentham/gridflow"

NEW: list[str] = []
ALL: list[str] = []


def N(s: str) -> str:
    """Register a line of copy that is not pack wording (for the notes)."""
    NEW.append(s)
    return s


# =============================================================== chrome (as the locked sibling pages, plus Explorer)
NAV = [("Home", "index.html"), ("Data sources", "data-sources.html"), ("Architecture", "architecture.html"),
       ("Models", "models.html"), ("Explorer", "explorer.html"), ("About", "index.html#about")]


def masthead() -> str:
    cur = ' aria-current="page"'
    li = "".join(f'<li><a href="{h}"{cur if n == "Explorer" else ""}>{n}</a></li>' for n, h in NAV)
    return (f'<header class="mast"><a class="brand" href="index.html">gridflow</a>'
            f'<nav aria-label="Primary"><ul>{li}</ul></nav></header>')


def footer() -> str:
    links = "".join(f'<li><a href="{h}">{n}</a></li>' for n, h in NAV[1:] + [("GitHub", GH_GRIDFLOW)])
    return (f'<footer class="st st-deep"><div class="foot"><a class="brand" href="index.html">'
            f'gridflow</a><ul>{links}</ul></div></footer>')


# =============================================================== the screens
SCREENS = [
    ("cat", "catalogue", "Catalogue", "Catalogue",
     "The explorer's catalogue: a petrol band with the eight sources plus gridflow gold, then the Electricity, Gas "
     "and Weather columns, each source with its count of datasets."),
    ("gen", "generation-mix", "Generation mix", "Generation",
     "The Generation mix screen: GB generation stacked by fuel for each half-hour over seven days, with the fuel "
     "key beside it."),
    ("mip", "market-index-price", "Market index price", "Market index",
     "The Market index price screen: price per half-hour over seven days, with its runs below zero banded, and a "
     "key of the latest half-hour and the window's range, extremes and mean."),
    ("hist", "historic-mix", "Historic generation mix", "Historic mix",
     "The Historic generation mix screen: NESO's generation by fuel as monthly means from 2009 to 2026, with "
     "carbon intensity beneath."),
]
ACTIVE = "mip"

WIN_X, WIN_TOP, WIN_W = 80, 50, 1104
BAR, BODY = 40, 620                  # body: 1101 x 620 css px shows the top 1440 x 811 of a screenshot
P_WIN_TOP, P_BAR, P_BODY = 74, 36, 420   # phone: a 440 x 520 crop at 355 x 420


def win_h(ph: bool) -> float:
    return 1.5 + (P_BAR + P_BODY if ph else BAR + BODY) + 1.5


def window(ph: bool) -> str:
    chk = ' checked=""'
    radios = "".join(f'<input class="tr" type="radio" name="scr" id="t-{k}"{chk if k == ACTIVE else ""}>'
                     for k, *_ in SCREENS)
    tabs = "".join(f'<label class="wt" for="t-{k}">{short if ph else name}</label>' for k, _s, name, short, _a in SCREENS)
    name = "" if ph else f'<span class="win-name">{N("gridflow explorer")}</span>'
    panes = []
    for k, stem, nm, _short, alt in SCREENS:
        if ph:
            img = (lambda th: f'<img src="explorer-shots/{stem}-{th}-crop.webp" alt="{html.escape(alt)}" width="355" '
                              f'height="420">')
            panes.append(f'<div class="pane p-{k}">'
                         f'<a class="enl enl-l" href="explorer-shots/{stem}-light.webp">{img("light")}</a>'
                         f'<a class="enl enl-d" href="explorer-shots/{stem}-dark.webp">{img("dark")}</a></div>')
        else:
            panes.append(f'<div class="pane p-{k}"><picture><source srcset="explorer-shots/{stem}-dark.webp" '
                         f'media="(prefers-color-scheme: dark)"><img src="explorer-shots/{stem}-light.webp" '
                         f'alt="{html.escape(alt)}" width="1101" height="620"></picture></div>')
    lab = N("Screens from gridflow explorer")
    return (f'<figure class="win" role="group" aria-label="{lab}">{radios}<div class="win-bar">{tabs}{name}</div>'
            f'<div class="win-body">{"".join(panes)}</div></figure>')


def tab_css() -> str:
    out = []
    for k, *_ in SCREENS:
        out.append(f'#t-{k}:checked~.win-bar label[for="t-{k}"]{{background:#F6F4EC;color:#1C2B22}}'
                   f'#t-{k}:checked~.win-body .p-{k}{{display:block}}'
                   f'#t-{k}:focus-visible~.win-bar label[for="t-{k}"]{{outline:2px solid #AFC64E;outline-offset:-4px}}')
    return "\n".join(out).replace("}}", "} }") + "\n"


# =============================================================== the ground in the screens section
def blend(x: float, a: float, b: float, ramp: float = 46) -> float:
    """0 under the window (a..b), rising smoothly to 1 outside it: the window stands on level ground."""
    d = a - x if x < a else (x - b if x > b else 0.0)
    t = max(0.0, min(1.0, d / ramp))
    return t * t * (3 - 2 * t)


def prof_for(S: float, a: float, b: float, w: int):
    k = 1.0 if w > 500 else .5

    def prof(x: float) -> float:
        wob = 4 * math.sin(x / 190 + .6) - 2.5 * math.sin(x / 83 + 1.3)
        return S + k * wob * blend(x, a, b)
    return prof


def screens_svg(ph: bool) -> tuple[str, float, float]:
    """Petrol sky, ridges and the energised field, the level land line the window stands on, a strip of topsoil,
    and the head of the cable. Returns (svg, surface y, section height)."""
    w = PW if ph else W
    top = P_WIN_TOP if ph else WIN_TOP
    x0 = 16 if ph else WIN_X
    x1 = (w - 16) if ph else WIN_X + WIN_W
    S = top + win_h(ph)
    SH = S + (26 if ph else 30)
    prof = prof_for(S, x0 - 8, x1 + 8, w)
    hp.Y["surf"] = S
    o = [f'<rect x="0" y="0" width="{w}" height="{f(SH)}" fill="{PETROL}"></rect>']
    if ph:
        far = [(-20, S - 476), (80, S - 492), (190, S - 480), (300, S - 494), (410, S - 482)]
        near = [(-20, S - 446), (90, S - 458), (200, S - 448), (310, S - 460), (410, S - 450)]
        o.append(sn.ridge(far, S - 60, FAR))
        o.append(sn.ridge(near, S - 60, HORIZON))
        for i, (tx, hh) in enumerate([(62, 26), (150, 22), (262, 24), (344, 20)]):
            o.append(hp.turbine(tx, S - 450, hh, hh * .5, ["sp2", "sp3", "sp1"][i % 3], 31 * i + 7))
        fld = [(-20, S - 120), (120, S - 126), (260, S - 118), (410, S - 124)]
        o.append(sn.field(fld, prof, -20, 410, [[(-20, S - 70), (200, S - 74), (410, S - 68)]]))
    else:
        far = [(-20, S - 262), (160, S - 290), (360, S - 270), (560, S - 292), (760, S - 266), (960, S - 284),
               (1160, S - 258), (1320, S - 280), (1460, S - 262)]
        near = [(-20, S - 214), (110, S - 236), (300, S - 222), (560, S - 246), (900, S - 226), (1180, S - 238),
                (1300, S - 214), (1460, S - 228)]
        o.append(sn.ridge(far, S - 60, FAR))
        o.append(sn.ridge(near, S - 60, HORIZON))
        o.append(hp.turbine(36, S - 234, 44, 22, "sp3", 20))
        for i, (tx, ty, hh) in enumerate([(1236, S - 234, 42), (1318, S - 216, 50), (1412, S - 224, 38)]):
            o.append(hp.turbine(tx, ty + 3, hh, hh * .5, ["sp2", "sp1", "sp3"][i], 37 * i + 11))
        fld = [(-20, S - 132), (200, S - 142), (600, S - 130), (1000, S - 140), (1220, S - 128), (1460, S - 136)]
        o.append(sn.field(fld, prof, -20, 1460, [[(-20, S - 96), (700, S - 102), (1460, S - 94)],
                                                 [(-20, S - 50), (800, S - 54), (1460, S - 46)]]))
        for i, (tx, hh) in enumerate([(1282, 150), (1384, 116)]):
            o.append(hp.turbine(tx, prof(tx), hh, hh * .5, ["sp1", "sp2"][i], 25 + 40 * i))
    step = 4 if ph else 8
    surf = [(x, prof(x)) for x in range(-40, w + 41, step)]
    surf_d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in surf)
    tail = f" L{w + 40} {f(SH + 10)} L-40 {f(SH + 10)} Z"
    o.append(f'<path d="{surf_d}{tail}" fill="{T_TOP}"></path><path d="{surf_d}{tail}" fill="url(#p-soil)" '
             f'opacity=".5"></path>')
    root = surf_d + " " + " ".join(f"L{f(x)} {f(y + (6 if ph else 8))}" for x, y in reversed(surf)) + " Z"
    o.append(f'<path d="{root}" fill="{OLIVE}"></path>')
    o.append(f'<path d="{surf_d}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    cx = CXP if ph else CX
    k = .8 if ph else 1
    o.append(hp.cable(f"M{cx} {f(S - 2)} V{f(SH + 4)}", CHART, 5.2 * k, 2.3 * k))
    aria = N("A landscape under a petrol sky: ridges with wind turbines and an energised field. The app window "
             "stands on the land line, and a cable runs from its foot into the ground.")
    svg = (f'<svg class="layer" width="{w}" height="{f(SH)}" viewBox="0 0 {w} {f(SH)}" role="img" '
           f'aria-label="{aria}"><defs>{hp.PATTERNS}</defs>' + "\n".join(o) + "</svg>")
    return svg, S, SH


# =============================================================== below ground: the stack as strata
CX, CXP = 128, 28          # the cable (desktop, phone)
TX, TXP = 176, 54          # text column left
TW, TWP = 468, 320         # text column width
CODE_X, CODE_W = 700, 660


def term(x: float, y: float, tint: str = T_TOP, r: float = 5.5) -> str:
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{tint}" stroke="{INK}" stroke-width="1.8"></circle>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r / 3)}" fill="{INK}"></circle>')


def joint(x: float, y: float, r: float = 4.6) -> str:
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{INK}"></circle>'


def drum(cx: float, cy: float, w: float, h: float, sw: float = 1.5) -> str:
    """DuckDB, drawn as the architecture page draws its file: a flat-lidded drum."""
    rx, ry = w / 2, h * .16
    t, b = cy - h / 2 + ry, cy + h / 2 - ry
    return (f'<path d="M{f(cx - rx)} {f(t)} V{f(b)} A{f(rx)} {f(ry)} 0 0 0 {f(cx + rx)} {f(b)} V{f(t)}" fill="{DAY}" '
            f'stroke="{INK}" stroke-width="{sw}"></path>'
            f'<ellipse cx="{f(cx)}" cy="{f(t)}" rx="{f(rx)}" ry="{f(ry)}" fill="{DAY}" stroke="{INK}" '
            f'stroke-width="{sw}"></ellipse>'
            f'<path d="M{f(cx - rx)} {f(t + (b - t) * .5)} A{f(rx)} {f(ry)} 0 0 0 {f(cx + rx)} {f(t + (b - t) * .5)}" '
            f'fill="none" stroke="{INK}" stroke-width=".8" opacity=".45"></path>')


def wave_d(y0: float, amp: float, seed: float, w: int) -> str:
    step = 120 if w > 500 else 60
    pts = [(x, wave_y(y0, amp, seed, x, w)) for x in range(-40, w + step + 41, step)]
    return smooth(pts)


def wave_y(y0: float, amp: float, seed: float, x: float, w: int) -> float:
    return (y0 + amp * math.sin(x / (210 if w > 500 else 90) + seed)
            + amp * .45 * math.sin(x / (73 if w > 500 else 37) + seed * 2.3))


def blocks() -> dict[str, tuple[str, str]]:
    """(heading html, body html) of every stratum, in descent order."""
    fe = ("React front end",
          f'<p class="kl">{N("React 19, TypeScript, Vite, Recharts and React Router.")}</p>'
          f'<p class="kl">{N("No component kit or CSS framework: its own design tokens, light and dark, and one shared chart theme.")}</p>')
    be = ("FastAPI backend",
          f'<p class="kl">{N("Python, FastAPI on uvicorn, and Polars.")}</p>'
          f'<p class="kl">{N("It serves the source manifest, a dataset’s rows and coverage, forecast runs from the gold forecast store, and a job that runs gridflow’s ingestion to fill a missing range.")}</p>')
    gc = ('<code>GridflowClient</code> and DuckDB, <span class="nw">read-only</span>',
          f'<p class="kl">{N("It reads gridflow only through gridflow’s own client, never raw file paths, with DuckDB opened read-only per request.")}</p>'
          f'<p class="kl">{N("The only thing it writes is gridflow’s catalogue, when it asks gridflow to fill a gap.")}</p>')
    sv = ("gridflow silver",
          f'<p class="kl">{N("GB and European energy-market data from eight public sources: Elexon BMRS, ENTSO-E, NESO Carbon Intensity, NESO Data Portal, ENTSO-G, GIE AGSI+, GIE ALSI and Open-Meteo.")}</p>')
    gd = ("gridflow gold",
          f'<p class="kl">{N("The tables gridflow builds from them, and its forecast store.")}</p>')
    return {"fe": fe, "be": be, "gc": gc, "sv": sv, "gd": gd}


CODE = [
    "  datasets: [",
    "    {",
    "      id: 'mid',",
    "      body: 'series',",
    "      label: 'Market index',",
    "      title: 'Price per half-hour',",
    "      values: [",
    "        { column: PRICE, label: 'Price', color: 'var(--chart-price)' },",
    "        { column: VOLUME, label: 'Volume', color: 'var(--chart-fan-soft)' },",
    "      ],",
]


def check_code() -> None:
    src = (DL / "explorer-pack" / "code" / "market-index-price.index.tsx").read_text(encoding="utf-8").splitlines()
    i = src.index(CODE[0])
    assert src[i:i + len(CODE)] == CODE, "code excerpt is not a contiguous run of real lines"


def code_block() -> str:
    lines = []
    for ln in CODE:
        e = html.escape(ln, quote=False)
        e = re.sub(r"'([^']*)'", r"<span class=\"s\">'\1'</span>", e)
        lines.append(e)
    cap = N("A dataset view is a small typed folder, found by a file glob: adding a view is adding a folder, with "
            "no central list to edit. <code>body: 'series'</code> picks one of the page template’s three bodies: a "
            "chart for series, a filterable table for events, a plain table for reference.")
    src = N("From the market index price view’s <code>index.tsx</code>, the screen above.")
    return (f'<figure class="code" data-h="code"><figcaption class="cap">{cap}</figcaption>'
            f'<pre class="well" tabindex="0" aria-label="{N("Code excerpt from the market index price view")}">'
            + "\n".join(lines) + f'</pre><p class="cap src">{src}</p></figure>')


def block_html(key: str, head: str, body: str, x: float, top: float, w: float) -> str:
    return (f'<div class="blk" data-h="{key}" style="left: {f(x)}px; top: {f(top)}px; width: {f(w)}px">'
            f'<h2 class="kn">{head}</h2>{body}</div>')


def layout(h: dict, ph: bool) -> dict:
    g = lambda k, d: h.get(k, d)  # noqa: E731
    Y: dict = {}
    if not ph:
        Y["fe"] = 44
        Y["code"] = 44
        Y["bed1"] = max(Y["fe"] + g("fe", 110), Y["code"] + g("code", 360)) + 48
        Y["be"] = Y["bed1"] + 48
        Y["bed2"] = Y["be"] + g("be", 120) + 48
        Y["gc"] = Y["bed2"] + 48
        Y["CS"] = Y["gc"] + g("gc", 120) + 58
        Y["sv"] = Y["CS"] + 50
        Y["CG"] = Y["sv"] + g("sv", 90) + 56
        Y["gd"] = Y["CG"] + 50
        Y["H"] = Y["gd"] + g("gd", 60) + 74
    else:
        Y["fe"] = 32
        Y["code"] = Y["fe"] + g("fe", 200) + 20
        Y["bed1"] = Y["code"] + g("code", 420) + 36
        Y["be"] = Y["bed1"] + 36
        Y["bed2"] = Y["be"] + g("be", 220) + 36
        Y["gc"] = Y["bed2"] + 36
        Y["CS"] = Y["gc"] + g("gc", 220) + 44
        Y["sv"] = Y["CS"] + 40
        Y["CG"] = Y["sv"] + g("sv", 160) + 44
        Y["gd"] = Y["CG"] + 40
        Y["H"] = Y["gd"] + g("gd", 80) + 60
    return Y


def stack_svg(Y: dict, ph: bool) -> str:
    w = PW if ph else W
    H = Y["H"]
    cx = CXP if ph else CX
    k = .8 if ph else 1.0
    amp = (5, 5) if ph else (8, 7)
    tail = f" L{w + 40} {f(H + 10)} L-40 {f(H + 10)} Z"
    o = [f'<rect x="0" y="0" width="{w}" height="{f(H)}" fill="{T_TOP}"></rect>',
         f'<rect x="0" y="0" width="{w}" height="{f(H)}" fill="url(#p-soil)" opacity=".5"></rect>']
    lines = []
    for y0, a, seed, fill, pid, op in ((Y["CS"], amp[0], 2.1, T_SILVER, "p-diag", ".22"),
                                       (Y["CG"], amp[1], 4.0, T_GOLD, "p-stip", ".26")):
        d = wave_d(y0, a, seed, w)
        o.append(f'<path d="{d}{tail}" fill="{fill}"></path><path d="{d}{tail}" fill="url(#{pid})" '
                 f'opacity="{op}"></path>')
        lines.append(d)
    o.append(f'<path d="{" ".join(lines)}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    for yb in (Y["bed1"], Y["bed2"]):
        pts = [(x, yb + (3 if ph else 4) * math.sin(x / (70 if ph else 160) + yb / 97)) for x in
               range(-40, w + 81, 40 if ph else 80)]
        o.append(f'<path d="{smooth(pts)}" stroke="{INK}" stroke-width="1" stroke-dasharray="2 6" fill="none" '
                 f'opacity=".55"></path>')
    hy = lambda key: Y[key] + (12 if ph else 14)  # noqa: E731  (level with a block's heading)
    end = hy("gd")
    o.append(hp.cable(f"M{cx} -4 V{f(end)}", CHART, 5.2 * k, 2.3 * k))
    parts = [term(cx, hy("fe"), T_TOP, 5.5 * k), term(cx, hy("be"), T_TOP, 5.5 * k),
             drum(cx, hy("gc") + (4 if ph else 6), 34 * k if ph else 44, 30 * k if ph else 38, 1.3 if ph else 1.5),
             joint(cx, hy("sv"), 4.6 * k), term(cx, end, T_GOLD, 5.5 * k)]
    for y0, a, seed, tint in ((Y["CS"], amp[0], 2.1, T_SILVER), (Y["CG"], amp[1], 4.0, T_GOLD)):
        cy = wave_y(y0, a, seed, cx, w)
        sl = frame.sleeve(cx, cy, tint)
        parts.append(hp.sc(sl, cx, cy, .7) if ph else sl)
    aria = N("The stack in section, under the app window: the React front end in the topsoil just below it, then "
             "the FastAPI backend, then GridflowClient over a read-only DuckDB; below them, gridflow's silver and "
             "gold. One cable runs from the window down through each of them.")
    return (f'<svg class="layer" width="{w}" height="{f(H)}" viewBox="0 0 {w} {f(H)}" role="img" '
            f'aria-label="{aria}"><defs>{hp.PATTERNS}</defs>' + "\n".join(o + parts) + "</svg>")


# =============================================================== page
def rough_edge(w: int) -> str:
    pts = [p for p in frame.rough(22) if p[0] <= w + 40]
    d = smooth(pts)
    return (f'<svg class="redge" width="{w}" height="44" viewBox="0 0 {w} 44" aria-hidden="true">'
            f'<defs>{hp.PATTERNS}</defs><path d="{d} L{w + 40} -4 L-40 -4 Z" fill="{T_GOLD}"></path>'
            f'<path d="{d} L{w + 40} -4 L-40 -4 Z" fill="url(#p-stip)" opacity=".26"></path>'
            f'<path d="{d}" stroke="{INK}" stroke-width="2" fill="none" stroke-linejoin="round"></path></svg>')


def body(h: dict, ph: bool = False) -> str:
    NEW.clear()
    check_code()
    Y = layout(h, ph)
    hint = f'<p class="hint">{N("Tap a screen to open it at full size.")}</p>' if ph else ""
    opening = (f'<section class="sky" data-section="opening">{masthead()}'
               f'<div class="hero"><h1>{N("A React app over gridflow’s data")}</h1><div class="lede">'
               f'<p class="lead">gridflow explorer is a web app for browsing everything gridflow collects: GB and '
               f'European energy-market data from eight public sources, plus the tables gridflow builds from them.</p>'
               f'<p>{N("It isn’t hosted, so the screens below are screenshots taken by its own screenshot tool.")}</p>'
               f'<p class="repo"><a class="alt" href="{REPO}">{N("gridflow-explorer on GitHub")}</a></p>{hint}'
               f'</div></div></section>')
    ssvg, S, SH = screens_svg(ph)
    screens = (f'<section class="screens" data-section="screens" style="height: {f(SH)}px">{ssvg}{window(ph)}'
               f'</section>')
    tx, tw = (TXP, TWP) if ph else (TX, TW)
    b = blocks()
    blks = [block_html(key, *b[key], tx, Y[key], tw) for key in ("fe", "be", "gc", "sv", "gd")]
    code = code_block().replace('<figure class="code"', f'<figure class="code" style="top: {f(Y["code"])}px"')
    stack = (f'<section class="stack" data-section="stack" aria-label="{N("How it is built")}" '
             f'style="height: {f(Y["H"])}px">{stack_svg(Y, ph)}{"".join(blks)}{code}</section>')
    gran = ('<svg class="gran" width="100%" height="100%" aria-hidden="true"><defs><pattern id="p-gran-d" width="46" '
            'height="40" patternUnits="userSpaceOnUse"><path d="M8 8 h8 M12 4 v8 M30 26 h8 M34 22 v8 M20 34 h6 M23 31 '
            f'v6 M40 6 h5 M42.5 3.5 v5" stroke="{HORIZON}" stroke-width="1.1"></path></pattern></defs>'
            '<rect width="100%" height="100%" fill="url(#p-gran-d)" opacity=".5"></rect></svg>')
    nxt = (f'<div class="st next"><p>{N("The pipeline under these tables, and the models that read them, have pages of their own.")}</p>'
           f'<ul><li><a class="out" href="architecture.html">Architecture</a></li>'
           f'<li><a class="out" href="models.html">Models</a></li></ul></div>')
    deep = f'<div class="deep" data-section="foot">{gran}{rough_edge(PW if ph else W)}{nxt}{footer()}</div>'
    return opening + screens + stack + deep


CSS = """.sky{position:relative;box-sizing:border-box;padding:0 80px 26px;background:#155A6E}
.hero{display:grid;grid-template-columns:780px 440px;column-gap:60px;margin-top:64px;align-items:start}
.lede{padding-top:10px}
.lede .repo{margin:4px 0 0}
.screens{position:relative;background:#155A6E}
.stack{position:relative;margin-top:-1px}
.layer{position:absolute;left:0;top:0;display:block}
.win{position:absolute;left:80px;top:50px;width:1104px;margin:0;box-sizing:border-box;background:#F6F4EC;border:1.5px solid #1C2B22;border-radius:4px;overflow:hidden}
.tr{position:absolute;opacity:0;width:1px;height:1px;margin:0;pointer-events:none}
.win-bar{display:flex;align-items:flex-end;gap:2px;height:40px;padding:0 18px 0 10px;background:#1C2B22;font:500 13.5px/1 "Hanken Grotesk",sans-serif}
.wt{padding:11px 16px 12px;border-radius:3px 3px 0 0;color:#CFE0DC;white-space:nowrap;cursor:pointer}
.wt:hover{color:#F6F4EC}
.win-name{margin-left:auto;align-self:center;color:#B4D0CD;white-space:nowrap}
.win-body{height:620px;overflow:hidden;background:#F6F4EC}
.pane{display:none}
.pane picture{display:block}
.pane img{display:block;width:1101px;height:620px}
.blk{position:absolute;margin:0}
.root .kn{font-family:"Bricolage Grotesque",sans-serif;font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.005em;margin:0 0 8px;color:#1C2B22}
.kn .nw{white-space:nowrap}
.kn code{font-size:.84em;font-weight:500;letter-spacing:0}
.kl{margin:0;font-size:15px;line-height:1.55;color:#3F4A3B;max-width:58ch}
.kl+.kl{margin-top:6px}
.code{position:absolute;left:700px;width:660px;margin:0}
.code .cap{margin:0 0 12px;font-size:14.5px;line-height:1.55;color:#3F4A3B;max-width:66ch}
.code .cap code,.code .src code{font-size:13.5px;color:#1C2B22}
.code .src{margin:10px 0 0}
.root .well{background:#F6F4EC;border:1px solid rgba(28,43,34,.22);padding:12px 16px;font-size:13.5px;line-height:1.7;overflow-x:auto}
.well:focus-visible{outline:2px solid #AFC64E;outline-offset:3px}
.deep{position:relative;background:#155A6E;color:#F6F4EC;margin-top:-2px}
.deep .gran{position:absolute;left:0;top:0;z-index:0}
.deep>*:not(.gran){position:relative;z-index:1}
.redge{display:block}
.next{display:flex;align-items:center;justify-content:space-between;column-gap:40px;padding-top:40px;padding-bottom:44px}
.next p{margin:0;font-size:17.5px;line-height:1.55;color:#CFE0DC;max-width:58ch}
.next ul{display:flex;gap:16px;list-style:none;margin:0;padding:0}
.root .out{display:inline-block;padding:11px 20px;border:1.5px solid rgba(207,224,220,.55);border-radius:3px;font-weight:600;font-size:16px;line-height:1.3;color:#F6F4EC;text-decoration:none}
.root .out:hover{border-color:#CFE0DC}
.foot{border-top:1px solid rgba(207,224,220,.22)}
"""

PH_CSS = """.ph .sky{padding:0 16px 24px}
.ph .mast{flex-wrap:wrap;row-gap:10px;padding-top:18px}
.ph .mast nav{flex:1 1 100%}
.ph .mast ul{flex-wrap:wrap;column-gap:18px;row-gap:2px}
.ph .hero{grid-template-columns:minmax(0,1fr);row-gap:18px;margin-top:34px}
.ph .hero h1{font-size:44px;line-height:.98}
.ph .lede{padding-top:0}
.ph .lede p{font-size:16.5px}
.ph .lede .hint{margin:18px 0 0;font-size:14.5px;color:#B4D0CD}
.ph .win{left:16px;top:74px;width:358px}
.ph .win-bar{height:36px;padding:0 6px;gap:0;font-size:12.5px}
.ph .wt{padding:10px 8px 10px}
.ph .win-body{height:420px}
.ph .pane img{width:355px;height:420px}
.ph .enl{display:block}
.ph .enl-d{display:none}
@media (prefers-color-scheme: dark){.ph .enl-l{display:none}.ph .enl-d{display:block} }
.ph .kn{font-size:20px;margin-bottom:6px}
.ph .kl{font-size:14.5px;line-height:1.5}
.ph .kl,.ph .kn{overflow-wrap:anywhere}
.ph .code{left:54px;width:320px}
.ph .code .cap{font-size:14px}
.ph .well{font-size:12px;padding:10px 12px}
.ph .st{padding:0 16px}
.ph .next{flex-direction:column;align-items:flex-start;row-gap:18px;padding-top:30px;padding-bottom:36px}
.ph .next p{font-size:16px}
.ph .foot{grid-template-columns:minmax(0,1fr);row-gap:14px;padding:36px 0 44px}
.ph .foot ul{flex-wrap:wrap;column-gap:18px;row-gap:6px}
"""

PROBE = """<pre id="m"></pre><script>
window.addEventListener('load',function(){Promise.all(['760 86px "Bricolage Grotesque"','720 23px "Bricolage Grotesque"','400 16px "Hanken Grotesk"','500 16px "Hanken Grotesk"','600 16px "Hanken Grotesk"','italic 400 14px "Hanken Grotesk"','400 14px "Red Hat Mono"','500 14px "Red Hat Mono"'].map(function(q){return document.fonts.load(q)})).then(function(){return document.fonts.ready}).then(function(){setTimeout(function(){
var root=document.querySelector('.root').getBoundingClientRect(),o={h:{},secs:{},H:0,over:[],hit:[],well:[],imgs:[]};
document.querySelectorAll('[data-h]').forEach(function(e){o.h[e.dataset.h]=Math.ceil(e.getBoundingClientRect().height);});
document.querySelectorAll('[data-section]').forEach(function(s){var r=s.getBoundingClientRect();o.secs[s.dataset.section]=[Math.round(r.top-root.top),Math.round(r.height)];});
o.H=Math.ceil(document.querySelector('main').getBoundingClientRect().bottom-root.top);
var LIM=__LIM__,RW=__RW__;
document.querySelectorAll('main p,main li,main h1,main h2,main h3,main a,main label,main figcaption').forEach(function(e){if(e.scrollWidth>e.clientWidth+1)o.over.push((e.className||e.tagName)+':'+(e.scrollWidth-e.clientWidth)+':'+e.textContent.slice(0,40));var r=e.getBoundingClientRect();if(r.width&&r.right-root.left>LIM+1&&!e.closest('.mast')&&!e.closest('.win'))o.over.push('WIDE '+(e.className||e.tagName)+':'+Math.round(r.right-root.left)+':'+e.textContent.slice(0,30));});
document.querySelectorAll('pre.well').forEach(function(e){o.well.push([e.scrollWidth,e.clientWidth]);});
var bar=document.querySelector('.win-bar');o.bar=[bar.scrollWidth,bar.clientWidth];
document.querySelectorAll('.pane img').forEach(function(e){if(e.offsetParent)o.imgs.push([e.currentSrc.split('/').pop(),e.naturalWidth,e.complete]);});
var ks=[].slice.call(document.querySelectorAll('.blk,.code'));for(var i=0;i<ks.length;i++)for(var j=i+1;j<ks.length;j++){var a=ks[i].getBoundingClientRect(),b=ks[j].getBoundingClientRect();if(a.left<b.right&&b.left<a.right&&a.top<b.bottom&&b.top<a.bottom)o.hit.push((ks[i].dataset.h)+'x'+(ks[j].dataset.h));}
var bad=[];document.querySelectorAll('.root *').forEach(function(e){if(e.closest('svg')&&e.tagName.toLowerCase()!=='svg')return;if(e.closest('pre.well')&&!e.matches('pre.well'))return;if(e.closest('.win-bar')&&!e.matches('.win-bar'))return;var r=e.getBoundingClientRect();if(r.width>0&&(r.right-root.left>RW+.5||r.left-root.left<-.5))bad.push((e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className||e.tagName)+':'+Math.round(r.left-root.left)+'..'+Math.round(r.right-root.left));});
o.outside=bad.slice(0,20);o.docW=document.documentElement.scrollWidth;
document.getElementById('m').textContent=JSON.stringify(o);},600);});});
</script>"""


def shell(inner: str, H: int, probe: bool, ph: bool = False) -> str:
    w = PW if ph else W
    css = CSS + tab_css() + (PH_CSS if ph else "")
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


def static(dc: str) -> str:
    return frame.static(dc).replace('"explorer-shots/', '"../explorer-shots/')


def measure(html_text: str, w: int) -> dict:
    (HERE / "static").mkdir(exist_ok=True)
    p = HERE / "static" / "_probe.html"
    p.write_text(static(html_text), encoding="utf-8")
    out = None
    for attempt in range(3):
        try:
            out = subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--window-size={w},4000",
                                  "--virtual-time-budget=9000", "--dump-dom", f"{URL}_probe.html?v={time.time_ns()}"],
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


def build(ph: bool) -> dict:
    """Probe the block heights, lay the strata out to them, probe again, then write at the measured height."""
    w = PW if ph else W
    name = f"{NAME}-{PW}" if ph else NAME
    m1 = measure(shell(body({}, ph), 20000, True, ph), w)
    m2 = measure(shell(body(m1["h"], ph), 20000, True, ph), w)
    H = m2["H"]
    out = shell(body(m1["h"], ph), H, False, ph)
    frame.check(out)
    ALL.extend(NEW)
    (HERE / f"{name}.dc.html").write_text(out, encoding="utf-8")
    (HERE / "static" / f"{name}.html").write_text(static(out), encoding="utf-8")
    print(name, "H", H, "h", m2["h"], "secs", m2["secs"])
    for k in ("over", "outside", "hit", "well", "bar", "imgs", "docW"):
        print(" ", k, m2.get(k))
    if m1["h"] != m2["h"]:
        print("  WARNING block heights moved between passes", m1["h"], m2["h"])
    return {"h": m2["h"], "H": H, "Y": layout(m1["h"], ph), "secs": m2["secs"]}


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
