"""Explorer page, round 1, designer 1: "The window".

A quiet, direct page. A short opening and the repo link; one large app window in the homepage notebook's frame
style, with a tab strip of five real screens (screenshots from the explorer's own shoot tool, light or dark to match
the reader's system); below it, how it's built: front end and backend, one cable for the request's route, and one
real excerpt of the market index price view. The deep band holds only the links to Architecture and Models.

Every fact comes from ``explorer-pack`` or the screenshots; lines that are not pack wording go through ``N()`` and
are listed in ``copy-new.json``.

Usage: gen.py [desktop] [phone]   (needs the design-loop root served on 127.0.0.1:9711)
"""
from __future__ import annotations

import html
import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).parent
DL = HERE.parent.parent
sys.path.insert(0, str(DL / "p27-r1" / "A"))

import frame  # noqa: E402
import hp  # noqa: E402
import scenery as sn  # noqa: E402
from hp import f, smooth  # noqa: E402

NAME = "1-explorer"
PORT = 9711
URL = f"http://127.0.0.1:{PORT}/explorer-r1/1/"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
W, PW = 1440, 390

PETROL, HORIZON, CHART, OLIVE = "#155A6E", "#3E8C97", "#AFC64E", "#66793B"
INK, DAY = "#1C2B22", "#F6F4EC"
T_GOLD, T_SILVER, T_TOP = "#E9DDAF", "#DCE2DF", "#ECE8DA"
FAR = "#297382"

REPO = "https://github.com/EBentham/gridflow-explorer"
GH_REPO = "https://github.com/EBentham/gridflow"

NEW: list[str] = []


def N(s: str) -> str:
    """Register a line of copy that is not pack wording (for the notes)."""
    NEW.append(s)
    return s


def esc(s: str) -> str:
    return html.escape(s, quote=False)


# =============================================================== chrome (as the locked sibling pages, plus Explorer)
NAV = [("Home", "index.html"), ("Data sources", "data-sources.html"), ("Architecture", "architecture.html"),
       ("Models", "models.html"), ("Explorer", "explorer.html"), ("About", "index.html#about")]


def masthead() -> str:
    cur = ' aria-current="page"'
    li = "".join(f'<li><a href="{h}"{cur if n == "Explorer" else ""}>{n}</a></li>' for n, h in NAV)
    return (f'<header class="mast"><a class="brand" href="index.html">gridflow</a>'
            f'<nav aria-label="Primary"><ul>{li}</ul></nav></header>')


def footer() -> str:
    links = "".join(f'<li><a href="{h}">{n}</a></li>' for n, h in NAV[1:] + [("GitHub", GH_REPO)])
    return (f'<footer class="st st-deep"><div class="foot"><a class="brand" href="index.html">'
            f'gridflow</a><ul>{links}</ul></div></footer>')


# =============================================================== the five screens
SHOTS = [
    ("catalogue", "Catalogue", 1480,
     "The catalogue it opens on: eight public sources and gridflow gold, grouped Electricity, Gas and Weather.",
     "The explorer’s catalogue: a petrol band with the eight sources and gridflow gold, then Electricity, Gas and "
     "Weather columns listing each source with its datasets.",
     (100, 20)),
    ("generation-mix", "Generation mix", 1047,
     "Generation mix, pinned in the side rail: GB generation stacked by fuel.",
     "The Generation mix screen: GB generation per half-hour stacked by fuel over seven days, with the fuel key, "
     "the mean mix for one day and a table of the days.",
     (118, 14)),
    ("system-prices", "System prices", 1174,
     "System prices, pinned in the side rail: the imbalance price per half-hour, with net imbalance volume on the "
     "same clock.",
     "The System prices screen: the imbalance price per half-hour over seven days with net imbalance volume below "
     "it, a key, a table of the days and the runs below zero.",
     (118, 14)),
    ("historic-mix", "Historic mix", 1935,
     "Historic mix: NESO’s generation by fuel from 2009 to 2026, with carbon intensity and the mix by year.",
     "The Historic generation mix screen: NESO’s generation by fuel as monthly means from 2009 to 2026, carbon "
     "intensity below, and the mix by year as a bar and a table.",
     (118, 220)),
    ("demand-outturn", "Demand outturn", 1397,
     "Demand outturn: Elexon’s national and transmission system demand per half-hour.",
     "The Demand outturn screen: national demand per half-hour over seven days, transmission demand below it, and "
     "the gap between them with a table of the days.",
     (118, 30)),
]
for _k, _t, _h, cap, _a, _o in SHOTS:
    N(cap)

PH_SCALE = .69          # phone crop: the shot at 69 %, so the app's 14 px text reads at about 10 px
PH_FRAME = (358 - 3, 404)


def picture(key: str, h: int, alt: str, eager: bool, cls: str = "") -> str:
    lazy = "" if eager else ' loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="explorer-shots/{key}-dark.png">'
            f'<img{c} src="explorer-shots/{key}-light.png" alt="{esc(alt)}" width="1440" height="{h}"{lazy}>'
            f'</picture>')


def window(ph: bool) -> str:
    tabs, panels = [], []
    for i, (key, label, h, cap, alt, (ox, oy)) in enumerate(SHOTS):
        on = i == 0
        tabs.append(f'<button type="button" role="tab" id="t-{key}" aria-controls="p-{key}" '
                    f'aria-selected="{"true" if on else "false"}" tabindex="{0 if on else -1}">{label}</button>')
        hid = "" if on else " hidden"
        if ph:
            s = PH_SCALE
            pic = picture(key, h, alt, on, "crop")
            style = f"width: {f(1440 * s)}px; left: {f(-ox * s)}px; top: {f(-oy * s)}px"
            pic = pic.replace('class="crop"', f'class="crop" style="{style}"')
            view = (f'<a class="full" href="explorer-shots/{key}-light.png" data-light="explorer-shots/{key}-light.png" '
                    f'data-dark="explorer-shots/{key}-dark.png">{pic}</a>')
            tail = f'<p class="wcap">{esc(cap)} {N("Tap the screen to see it whole.")}</p>'
        else:
            view = f'<div class="vp" role="region" tabindex="0" aria-label="{esc(label)}, scrolls">{picture(key, h, alt, on)}</div>'
            tail = f'<p class="wcap">{esc(cap)}</p>'
        panels.append(f'<div class="pane" role="tabpanel" id="p-{key}" aria-labelledby="t-{key}"{hid}>'
                      f'<div class="view">{view}</div>{tail}</div>')
    return (f'<figure class="win"><div class="win-bar" role="tablist" aria-label="{N("Screens of gridflow explorer")}">'
            f'{"".join(tabs)}</div>{"".join(panels)}</figure>')


# =============================================================== landscape strip and ground
def strip_desk(S: float, Hs: float) -> str:
    """Petrol sky into ridges with turbines, the chartreuse field and the cut. The window stands on the field."""
    hp.Y["surf"] = S
    p = [f'<rect x="0" y="0" width="{W}" height="{f(S)}" fill="{PETROL}"></rect>']
    p.append(sn.ridge([(-20, S - 150), (180, S - 176), (400, S - 158), (620, S - 184), (840, S - 160),
                       (1060, S - 178), (1260, S - 154), (1460, S - 170)], S, FAR))
    near = [(-20, S - 112), (140, S - 132), (300, S - 140), (470, S - 122), (660, S - 146), (860, S - 128),
            (1040, S - 112), (1220, S - 134), (1460, S - 118)]
    p.append(sn.ridge(near, S, HORIZON))
    for i, (tx, ty) in enumerate([near[2], near[4], near[5], near[7]]):
        hgt = [58, 64, 52, 60][i]
        p.append(hp.turbine(tx, ty + 3, hgt, hgt * .5, ["sp2", "sp3", "sp1", "sp2"][i], 31 * i + 7))
    top = [(-20, S - 58), (220, S - 66), (460, S - 54), (700, S - 64), (940, S - 52), (1180, S - 62), (1460, S - 56)]
    p.append(sn.field(top, hp.prof, -20, 1460, [[(-20, S - 34), (500, S - 38), (1000, S - 30), (1460, S - 34)]]))
    pls = [(170, hp.prof(170) - 2, .62), (470, hp.prof(470) - 2, .62), (770, hp.prof(770) - 2, .62)]
    p.append("".join(f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.35">{hp.pylon(*pl)}</g>'
                     for pl in pls))
    wires = [hp.spans([(-20, S - 70), (-20, S - 84), (-20, S - 96)], hp.tips(*pls[0], -1), 6),
             hp.spans(hp.tips(*pls[0], 1), hp.tips(*pls[1], -1), 10),
             hp.spans(hp.tips(*pls[1], 1), hp.tips(*pls[2], -1), 10),
             hp.spans(hp.tips(*pls[2], 1), [(1460, S - 72), (1460, S - 86), (1460, S - 98)], 12)]
    p.append(f'<path d="{" ".join(wires)}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".85"></path>')
    for i, (tx, hh) in enumerate([(1040, 150), (1140, 136), (1232, 124)]):
        p.append(hp.turbine(tx, hp.prof(tx), hh, hh * .5, ["sp1", "sp2", "sp3"][i], 25 + 40 * i))
    surf = [(x, hp.prof(x)) for x in range(-40, W + 41, 8)]
    sd = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in surf)
    root = sd + " " + " ".join(f"L{f(x)} {f(y + 8)}" for x, y in reversed(surf)) + " Z"
    p.append(f'<path d="{root}" fill="{OLIVE}"></path><path d="{sd}" stroke="{INK}" stroke-width="1.5" '
             f'fill="none"></path>')
    return (f'<svg class="strip" width="{W}" height="{f(Hs)}" viewBox="0 0 {W} {f(Hs)}" aria-hidden="true">'
            + "\n".join(p) + "</svg>")


def strip_phone(S: float, Hs: float) -> str:
    pprof = lambda x: S + 2 * __import__("math").sin(x / 60 + .6) - 1.2 * __import__("math").sin(x / 27 + 1.3)  # noqa: E731
    p = [f'<rect x="0" y="0" width="{PW}" height="{f(S)}" fill="{PETROL}"></rect>']
    p.append(sn.ridge([(-20, S - 84), (80, S - 96), (170, S - 86), (260, S - 98), (340, S - 88), (410, S - 94)],
                      S, FAR))
    near = [(-20, S - 64), (70, S - 74), (150, S - 80), (240, S - 68), (320, S - 78), (410, S - 70)]
    p.append(sn.ridge(near, S, HORIZON))
    for i, (tx, ty) in enumerate(near[1:5]):
        hgt = [28, 32, 26, 30][i]
        p.append(hp.turbine(tx, ty + 2, hgt, hgt * .5, ["sp2", "sp3", "sp1", "sp2"][i], 29 * i + 5))
    fld = [(-20, S - 34), (100, S - 38), (220, S - 32), (320, S - 38), (410, S - 34)]
    p.append(sn.field(fld, pprof, -20, 410, [[(-20, S - 18), (200, S - 20), (410, S - 16)]]))
    surf = [(x, pprof(x)) for x in range(-40, PW + 41, 4)]
    sd = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in surf)
    root = sd + " " + " ".join(f"L{f(x)} {f(y + 6)}" for x, y in reversed(surf)) + " Z"
    p.append(f'<path d="{root}" fill="{OLIVE}"></path><path d="{sd}" stroke="{INK}" stroke-width="1.5" '
             f'fill="none"></path>')
    return (f'<svg class="strip" width="{PW}" height="{f(Hs)}" viewBox="0 0 {PW} {f(Hs)}" aria-hidden="true">'
            + "\n".join(p) + "</svg>")


def soil_layer() -> str:
    return (f'<svg class="soil" width="100%" height="100%" aria-hidden="true"><defs>{hp.PATTERNS}</defs>'
            f'<rect width="100%" height="100%" fill="{T_TOP}"></rect>'
            f'<rect width="100%" height="100%" fill="url(#p-soil)" opacity=".5"></rect></svg>')


def rough_edge(w: int) -> str:
    pts = [p for p in frame.rough(22) if p[0] <= w + 40]
    d = smooth(pts)
    return (f'<svg class="redge" width="{w}" height="44" viewBox="0 0 {w} 44" aria-hidden="true">'
            f'<defs>{hp.PATTERNS}</defs><path d="{d} L{w + 40} -4 L-40 -4 Z" fill="{T_TOP}"></path>'
            f'<path d="{d} L{w + 40} -4 L-40 -4 Z" fill="url(#p-soil)" opacity=".5"></path>'
            f'<path d="{d}" stroke="{INK}" stroke-width="2" fill="none" stroke-linejoin="round"></path></svg>')


# =============================================================== how it's built
def term(x: float, y: float, tint: str, r: float = 6.5) -> str:
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{tint}" stroke="{INK}" stroke-width="2"></circle>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r / 3)}" fill="{INK}"></circle>')


def cab(d: str) -> str:
    return hp.cable(d, CHART, 5.2, 2.3)


FLOW_ARIA = ("The route of a request: from the browser running the React app, to FastAPI, to GridflowClient, to "
             "DuckDB, which reads gridflow's silver and gold tables.")


def flow_desk() -> str:
    y = 40
    xs = [14, 400, 760, 1086]
    xe = 1196
    o = [cab(f"M{xs[0]} {y} H{xs[3]}"),
         cab(f"M{xs[3]} {y} C{xs[3] + 40} {y} {xs[3] + 40} {y - 22} {xs[3] + 84} {y - 22} H{xe}"),
         cab(f"M{xs[3]} {y} C{xs[3] + 40} {y} {xs[3] + 40} {y + 22} {xs[3] + 84} {y + 22} H{xe}")]
    o += [term(x, y, T_TOP) for x in xs[:3]]
    o.append(f'<circle cx="{xs[3]}" cy="{y}" r="5.2" fill="{INK}"></circle>')
    o += [term(xe, y - 22, T_SILVER, 6), term(xe, y + 22, T_GOLD, 6)]
    lab = [(xs[0] - 6, "browser (React)", "start", ""), (xs[1], "FastAPI", "middle", ""),
           (xs[2], "GridflowClient", "middle", "m"), (xs[3], "DuckDB", "middle", "")]
    t = "".join(f'<text x="{f(x)}" y="{y + 34}" text-anchor="{a}"{" class=" + chr(34) + c + chr(34) if c else ""}>'
                f'{s}</text>' for x, s, a, c in lab)
    t += (f'<text x="{xe + 16}" y="{y - 17}">silver</text>'
          f'<text x="{xe + 16}" y="{y + 27}">gold</text>')
    return (f'<svg class="flow" width="1280" height="92" viewBox="0 0 1280 92" role="img" aria-label="{FLOW_ARIA}">'
            + "".join(o) + f'<g class="lab">{t}</g></svg>')


def flow_phone() -> str:
    x = 14
    ys = [12, 58, 104, 150]
    o = [cab(f"M{x} {ys[0]} V{ys[3]}"),
         cab(f"M{x} {ys[3]} C{x} {ys[3] + 26} {x + 20} {ys[3] + 26} {x + 20} {ys[3] + 48} V{ys[3] + 58}"),
         cab(f"M{x} {ys[3]} V{ys[3] + 58}")]
    o += [term(x, y, T_TOP) for y in ys[:3]]
    o.append(f'<circle cx="{x}" cy="{ys[3]}" r="5.2" fill="{INK}"></circle>')
    o += [term(x, ys[3] + 58, T_SILVER, 6), term(x + 20, ys[3] + 58, T_GOLD, 6)]
    lab = [("browser (React)", ""), ("FastAPI", ""), ("GridflowClient", "m"), ("DuckDB", "")]
    t = "".join(f'<text x="{x + 22}" y="{y + 5}"{" class=" + chr(34) + c + chr(34) if c else ""}>{s}</text>'
                for (s, c), y in zip(lab, ys))
    t += f'<text x="{x + 36}" y="{ys[3] + 63}">silver and gold</text>'
    h = ys[3] + 72
    return (f'<svg class="flow" width="358" height="{h}" viewBox="0 0 358 {h}" role="img" aria-label="{FLOW_ARIA}">'
            + "".join(o) + f'<g class="lab">{t}</g></svg>')


SRC = (DL / "explorer-pack" / "code" / "market-index-price.index.tsx").read_text(encoding="utf-8").splitlines()
EXCERPT = [[13], [18, 19], list(range(25, 35)), [36]]


def hl(s: str) -> str:
    s = esc(s)
    s = re.sub(r"('[^']*')", r'<span class="s">\1</span>', s)
    s = re.sub(r"\b(import|from|const)\b", r'<span class="k">\1</span>', s)
    return s


def code_well() -> str:
    rows = []
    for g, grp in enumerate(EXCERPT):
        for i, n in enumerate(grp):
            line = SRC[n - 1]
            ind = len(line) - len(line.lstrip(" "))
            cut = ' class="cut"' if g and not i else ""
            rows.append(f'<span{cut}><span class="n">{n}</span><span class="t" style="--i: {ind}ch">'
                        f'{hl(line.lstrip(" "))}</span></span>')
    return (f'<pre class="well code" aria-label="{N("Lines 13 to 36 of the market index price view, index.tsx, with some lines left out")}">'
            + "".join(rows) + "</pre>")


def built(ph: bool) -> str:
    fe = [("kf", N("React 19, TypeScript, Vite, Recharts and React Router.")),
          ("kl", N("No component kit and no CSS framework: its own design tokens as CSS custom properties, light and "
                   "dark themes, and one shared chart theme.")),
          ("kl", N("One dataset page template with three bodies: series as a chart, event feeds as a filterable "
                   "table, reference tables as a plain table.")),
          ("kl", N("Its own screenshot tool, headless Chrome through puppeteer-core, takes every screen in light and "
                   "dark."))]
    be = [("kf", N("Python, FastAPI on uvicorn, Polars, and DuckDB opened read-only per request.")),
          ("kl", N("It reads gridflow only through gridflow’s own client, <code>GridflowClient</code>, never raw file "
                   "paths.")),
          ("kl", N("Endpoints serve the source manifest, a dataset’s rows and its coverage, forecast runs from the "
                   "gold forecast store, and a job that runs gridflow’s ingestion to fill a missing range."))]

    def col(h: str, lines: list[tuple[str, str]]) -> str:
        return (f'<div class="tcol"><h3 class="kn">{h}</h3>'
                + "".join(f'<p class="{c}">{t}</p>' for c, t in lines) + "</div>")

    return (f'<section class="st built" data-section="built" aria-labelledby="h-built">'
            f'<h2 class="big" id="h-built">{N("How it’s built")}</h2>'
            f'<div class="tcols">{col("Front end", fe)}{col("Backend", be)}</div>'
            f'<div class="route">{flow_phone() if ph else flow_desk()}</div>'
            f'<div class="viewx"><div class="vtext"><h3 class="kn">{N("A view is a small typed file")}</h3>'
            f'<p class="kl">{N("Each dataset view is its own folder, <code>src/views/&lt;source&gt;/&lt;family&gt;/</code>, and the app finds views by a file glob: adding a view is adding a folder, with no central list to edit.")}</p>'
            f'<p class="kl">{N("This is the market index price view. The line numbers are the file’s; the gaps are lines left out.")}</p>'
            f'</div>{code_well()}</div></section>')


# =============================================================== page
def body(ph: bool) -> str:
    NEW.clear()
    for _k, _t, _h, cap, _a, _o in SHOTS:
        N(cap)
    lead = N("gridflow explorer is a web app for browsing gridflow’s data: GB and European energy-market data from "
             "eight public sources, and the tables gridflow builds from them. A React and TypeScript front end sits "
             "on a FastAPI backend that reads gridflow through its own client.")
    opening = (f'<section class="sky" data-section="opening">{masthead()}'
               f'<div class="hero"><h1>{N("Browsing everything gridflow collects")}</h1><div class="lede">'
               f'<p class="lead">{lead}</p>'
               f'<p><a class="alt" href="{REPO}">{N("The code on GitHub")}</a> <code>EBentham/gridflow-explorer</code></p>'
               f'</div></div></section>')
    S, Hs = (104, 116) if ph else (262, 276)
    strip = strip_phone(S, Hs) if ph else strip_desk(S, Hs)
    note = N("It isn’t hosted, so these are screenshots from its own screenshot tool, light or dark to match your "
             "system.")
    screens = (f'<section class="screens" data-section="screens" aria-label="{N("The app, screen by screen")}">'
               f'{strip}<div class="st wrapw">{window(ph)}<p class="wnote">{note}</p></div></section>')
    rel = [("Architecture", "architecture.html",
            N("How gridflow is built, from raw responses in bronze to the DuckDB file over silver and gold.")),
           ("Models", "models.html",
            N("gridflow-models, a separate Python library that reads gridflow’s silver tables for forecasts and a "
              "day-ahead price."))]
    lis = "".join(f'<li><h3 class="rn"><a href="{h}">{n}</a></h3><p>{d}</p></li>' for n, h, d in rel)
    gran = ('<svg class="gran" width="100%" height="100%" aria-hidden="true"><defs><pattern id="p-gran-d" width="46" '
            'height="40" patternUnits="userSpaceOnUse"><path d="M8 8 h8 M12 4 v8 M30 26 h8 M34 22 v8 M20 34 h6 M23 31 '
            f'v6 M40 6 h5 M42.5 3.5 v5" stroke="{HORIZON}" stroke-width="1.1"></path></pattern></defs>'
            '<rect width="100%" height="100%" fill="url(#p-gran-d)" opacity=".5"></rect></svg>')
    deep = (f'<div class="deep" data-section="foot">{gran}{rough_edge(PW if ph else W)}'
            f'<section class="st related" aria-labelledby="h-rel"><h2 class="rh" id="h-rel">{N("The rest of gridflow")}</h2>'
            f'<ul>{lis}</ul></section>{footer()}</div>')
    ground = f'<div class="ground">{soil_layer()}{screens}{built(ph)}</div>'
    return opening + ground + deep


TABS_JS = """<script>
(function () {
  var tabs = [].slice.call(document.querySelectorAll('.win [role="tab"]'));
  function pick(t) {
    tabs.forEach(function (x) {
      var on = x === t;
      x.setAttribute('aria-selected', on ? 'true' : 'false');
      x.tabIndex = on ? 0 : -1;
      document.getElementById(x.getAttribute('aria-controls')).hidden = !on;
    });
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { pick(t); });
    t.addEventListener('keydown', function (e) {
      var k = e.key, j = k === 'ArrowRight' ? i + 1 : k === 'ArrowLeft' ? i - 1 : k === 'Home' ? 0 : k === 'End' ? tabs.length - 1 : null;
      if (j === null) return;
      e.preventDefault();
      var n = tabs[(j + tabs.length) % tabs.length];
      pick(n); n.focus();
    });
  });
  var mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  function hrefs() {
    [].forEach.call(document.querySelectorAll('.win a.full'), function (a) {
      a.href = mq && mq.matches ? a.getAttribute('data-dark') : a.getAttribute('data-light');
    });
  }
  hrefs();
  if (mq && mq.addEventListener) mq.addEventListener('change', hrefs);
})();
</script>"""

CSS = """.sky{position:relative;box-sizing:border-box;padding:0 80px 8px;background:#155A6E}
.hero{display:grid;grid-template-columns:720px 500px;column-gap:60px;margin-top:64px;align-items:start}
.lede{padding-top:10px}
.lede p{max-width:none}
.lede code{font-size:14.5px;color:#CFE0DC;margin-left:10px}
.ground{position:relative}
.ground .soil{position:absolute;left:0;top:0;z-index:0}
.ground>section{position:relative;z-index:1}
.strip{display:block}
.screens{position:relative}
.wrapw{margin-top:12px}
.win{margin:0;background:#F6F4EC;border:1.5px solid #1C2B22;border-radius:4px;overflow:hidden}
.win-bar{display:flex;align-items:flex-end;gap:2px;height:44px;padding:0 12px;background:#1C2B22}
.win-bar button{appearance:none;border:0;margin:0;cursor:pointer;padding:12px 18px 13px;border-radius:3px 3px 0 0;background:transparent;color:#CFE0DC;font:500 14.5px/1 "Hanken Grotesk",sans-serif;white-space:nowrap}
.win-bar button:hover{color:#F6F4EC}
.win-bar button[aria-selected="true"]{background:#F6F4EC;color:#1C2B22}
.win-bar button:focus-visible{outline:2px solid #AFC64E;outline-offset:-4px}
.pane[hidden]{display:none}
.view{position:relative;border-bottom:1.5px solid #1C2B22}
.vp{height:780px;overflow-y:auto;overflow-x:hidden;scrollbar-width:thin;scrollbar-color:#5d6a55 #ECE8DA}
.vp:focus-visible{outline:2px solid #AFC64E;outline-offset:-3px}
.vp img{display:block;width:100%;height:auto}
.wcap{margin:0;padding:12px 18px 14px;font-size:14.5px;line-height:1.5;color:#3F4A3B}
.wnote{margin:14px 0 0;font-size:14.5px;line-height:1.5;color:#3F4A3B;max-width:66ch}
.built{padding-top:104px;padding-bottom:112px}
.built h2.big{margin-bottom:34px}
.tcols{display:grid;grid-template-columns:560px 560px;column-gap:160px}
.root .kn{font-family:"Bricolage Grotesque",sans-serif;font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.005em;margin:0 0 9px}
.kf{margin:0 0 6px;font-size:15.5px;line-height:1.5;font-weight:600;color:#1C2B22;max-width:58ch}
.kl{margin:6px 0 0;font-size:14.5px;line-height:1.55;color:#3F4A3B;max-width:58ch}
.kl code{font-size:13.5px;color:#1C2B22}
.route{margin:58px 0 0}
.flow{display:block;overflow:visible}
.flow .lab text{font-family:"Hanken Grotesk",sans-serif;font-style:italic;font-size:14px;fill:#1C2B22}
.flow .lab text.m{font-family:"Red Hat Mono",monospace;font-style:normal;font-size:13.5px}
.viewx{display:grid;grid-template-columns:330px 890px;column-gap:60px;margin-top:70px;align-items:start}
.vtext .kl{max-width:none}
.well.code{padding:12px 16px 12px 8px;font-size:13.5px;line-height:1.7;white-space:normal}
.well.code>span{display:grid;grid-template-columns:30px minmax(0,1fr);column-gap:14px}
.well.code>span.cut{margin-top:.85em}
.well.code .n{color:#5d6a55;text-align:right;user-select:none}
.well.code .t{white-space:pre-wrap;padding-left:calc(var(--i) + 2ch);text-indent:-2ch}
.deep{position:relative;background:#155A6E;color:#F6F4EC;margin-top:-2px}
.deep .gran{position:absolute;left:0;top:0;z-index:0}
.deep>*:not(.gran){position:relative;z-index:1}
.redge{display:block}
.related{padding-top:52px;padding-bottom:40px}
.root .rh{font-size:30px;font-weight:700;font-stretch:90%;line-height:1.1;letter-spacing:-.012em;margin:0 0 22px;color:#F6F4EC}
.related ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:560px 560px;column-gap:160px}
.root .rn{font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;margin:0 0 8px}
.rn a{color:#F6F4EC;text-decoration-color:#AFC64E}
.related p{margin:0;font-size:15px;line-height:1.55;color:#CFE0DC;max-width:52ch}
.foot{border-top:1px solid rgba(207,224,220,.22)}
"""

PH_CSS = """.ph .sky{padding:0 16px 40px}
.ph .mast{flex-wrap:wrap;row-gap:10px;padding-top:18px}
.ph .mast nav{flex:1 1 100%}
.ph .mast ul{flex-wrap:wrap;column-gap:18px;row-gap:2px}
.ph .hero{grid-template-columns:minmax(0,1fr);row-gap:18px;margin-top:34px}
.ph .hero h1{font-size:44px;line-height:.98}
.ph .lede{padding-top:0}
.ph .lede p{font-size:16.5px}
.ph .lede code{display:block;margin:4px 0 0;font-size:13.5px}
.ph .st{padding:0 16px}
.ph .wrapw{margin-top:8px}
.ph .win-bar{flex-wrap:wrap;height:auto;padding:6px;gap:4px}
.ph .win-bar button{padding:8px 11px;border-radius:3px;font-size:14px}
.ph .view{height:404px;overflow:hidden}
.ph .full{display:block;position:relative;width:100%;height:100%}
.ph .full:focus-visible{outline:2px solid #AFC64E;outline-offset:-3px}
.ph img.crop{position:absolute;display:block;max-width:none;height:auto}
.ph .wcap{padding:10px 12px 12px;font-size:14px}
.ph .wnote{font-size:14px}
.ph .built{padding-top:64px;padding-bottom:72px}
.ph .built h2.big{font-size:32px;margin-bottom:24px}
.ph .tcols{grid-template-columns:minmax(0,1fr);row-gap:30px}
.ph .route{margin-top:36px}
.ph .viewx{grid-template-columns:minmax(0,1fr);row-gap:18px;margin-top:40px}
.ph .well.code{font-size:12px;line-height:1.6;padding:10px 10px 10px 4px}
.ph .well.code>span{grid-template-columns:22px minmax(0,1fr);column-gap:10px}
.ph .kl,.ph .kf{overflow-wrap:anywhere}
.ph .related{padding-top:36px;padding-bottom:28px}
.ph .related ul{grid-template-columns:minmax(0,1fr);row-gap:24px}
.ph .foot{grid-template-columns:minmax(0,1fr);row-gap:14px;padding:36px 0 44px}
.ph .foot ul{flex-wrap:wrap;column-gap:18px;row-gap:6px}
"""

PROBE = """<pre id="m"></pre><script>
window.addEventListener('load',function(){Promise.all(['760 86px "Bricolage Grotesque"','720 23px "Bricolage Grotesque"','400 16px "Hanken Grotesk"','500 16px "Hanken Grotesk"','600 16px "Hanken Grotesk"','italic 400 14px "Hanken Grotesk"','400 14px "Red Hat Mono"','500 14px "Red Hat Mono"'].map(function(q){return document.fonts.load(q)})).then(function(){return document.fonts.ready}).then(function(){setTimeout(function(){
var root=document.querySelector('.root').getBoundingClientRect(),o={secs:{},H:0,over:[],tabs:[]};
document.querySelectorAll('[data-section]').forEach(function(s){var r=s.getBoundingClientRect();o.secs[s.dataset.section]=[Math.round(r.top-root.top),Math.round(r.height)];});
o.H=Math.ceil(document.querySelector('main').getBoundingClientRect().bottom-root.top);
var RW=__RW__,LIM=__LIM__;
document.querySelectorAll('main p,main li,main h1,main h2,main h3,main pre,main a,main button,main code').forEach(function(e){if(e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).display!=='inline')o.over.push((e.className||e.tagName)+':'+(e.scrollWidth-e.clientWidth)+':'+e.textContent.slice(0,40));var r=e.getBoundingClientRect();if(r.width>0&&!e.closest('.mast')&&!e.closest('.view')&&(r.right-root.left>LIM+1||r.left-root.left<RW-LIM-1))o.over.push('EDGE '+(e.className||e.tagName)+':'+Math.round(r.left-root.left)+'..'+Math.round(r.right-root.left)+':'+e.textContent.slice(0,30));});
var bad=[];document.querySelectorAll('.root *').forEach(function(e){if(e.closest('svg')&&e.tagName.toLowerCase()!=='svg')return;if(e.closest('.view'))return;var r=e.getBoundingClientRect();if(r.width>0&&(r.right-root.left>RW+.5||r.left-root.left<-.5))bad.push((e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className||e.tagName)+':'+Math.round(r.left-root.left)+'..'+Math.round(r.right-root.left));});
o.outside=bad.slice(0,20);o.docW=document.documentElement.scrollWidth;
var w=document.querySelector('.win').getBoundingClientRect(),bar=document.querySelector('.win-bar').getBoundingClientRect(),view=document.querySelector('.pane:not([hidden]) .view').getBoundingClientRect();o.win=[Math.round(w.left-root.left),Math.round(w.top-root.top),Math.round(w.width),Math.round(w.height),Math.round(bar.height),Math.round(view.height)];
var well=document.querySelector('.well.code');o.well=[well.clientWidth,well.scrollWidth,Math.round(well.getBoundingClientRect().height)];
o.wrapped=[].slice.call(document.querySelectorAll('.well.code .t')).filter(function(t){return t.getClientRects().length>1||t.getBoundingClientRect().height>parseFloat(getComputedStyle(t).lineHeight)*1.5}).map(function(t){return t.parentNode.firstChild.textContent});
[].forEach.call(document.querySelectorAll('.win [role="tab"]'),function(t){t.click();var vis=[].filter.call(document.querySelectorAll('.pane'),function(p){return !p.hidden}).map(function(p){return p.id});var img=document.querySelector('.pane:not([hidden]) img');o.tabs.push(t.textContent+'>'+vis.join(',')+'|'+t.getAttribute('aria-selected')+'|'+(img?img.getAttribute('src'):''));});
document.querySelector('.win [role="tab"]').click();
document.getElementById('m').textContent=JSON.stringify(o);},600);});});
</script>"""


def shell(inner: str, H: int, probe: bool, ph: bool) -> str:
    w = PW if ph else W
    css = CSS + PH_CSS if ph else CSS
    cls = "root ph" if ph else "root"
    pr = PROBE.replace("__RW__", str(w)).replace("__LIM__", str(w - (16 if ph else 80))) if probe else ""
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
{TABS_JS}
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{H}}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
{pr}</body>
</html>
"""


def static(dc: str) -> str:
    return frame.static(dc)


def measure(text: str, w: int) -> dict:
    p = HERE / "_probe.html"
    p.write_text(static(text), encoding="utf-8")
    out = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},4000",
                          "--virtual-time-budget=9000", "--dump-dom", f"{URL}_probe.html?v={time.time_ns()}"],
                         capture_output=True, text=True, encoding="utf-8", timeout=120)
    mm = re.search(r'<pre id="m">(.*?)</pre>', out.stdout, re.S)
    p.unlink()
    if not mm or not mm.group(1).strip():
        raise RuntimeError(f"probe failed: {out.stderr[-400:]}")
    return json.loads(html.unescape(mm.group(1)))


def check(out: str) -> None:
    frame.check(out)
    for bad in ("{{", "}}"):
        assert bad not in out.split('<script type="text/x-dc"')[0], bad
    body_txt = out.split("<main>")[1].split("</main>")[0]
    assert "\u00b7" not in body_txt, "middle dot"
    for word in ("planned", "milestone", "v0.", "coming", "in progress", "held locally", "local data", "live"):
        assert not re.search(rf"\b{re.escape(word)}\b", re.sub(r"<[^>]+>", " ", body_txt).lower()), word


def build(ph: bool) -> dict:
    w = PW if ph else W
    name = f"{NAME}-{PW}" if ph else NAME
    m = measure(shell(body(ph), 20000, True, ph), w)
    H = m["H"]
    out = shell(body(ph), H, False, ph)
    check(out)
    (HERE / f"{name}.dc.html").write_text(out, encoding="utf-8")
    (HERE / "static").mkdir(exist_ok=True)
    (HERE / "static" / f"{name}.html").write_text(static(out).replace('"explorer-shots/', '"../explorer-shots/'),
                                                  encoding="utf-8")
    print(name, "H", H, "secs", m["secs"])
    for k in ("win", "well", "wrapped", "over", "outside", "docW", "tabs"):
        print(" ", k, m.get(k))
    return {"H": H, "secs": m["secs"], "win": m["win"], "copy": list(dict.fromkeys(NEW))}


def main() -> None:
    which = sys.argv[1:] or ["desktop", "phone"]
    meas = {k: build(k == "phone") for k in which}
    allc: list[str] = []
    for v in meas.values():
        allc += v.pop("copy")
    (HERE / "copy-new.json").write_text(json.dumps(list(dict.fromkeys(allc)), ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    (HERE / "measure.json").write_text(json.dumps(meas, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
