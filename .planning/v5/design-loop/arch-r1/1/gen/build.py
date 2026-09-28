"""Designer 1, "The cross-section": the architecture board. Usage: python -B build.py [--reuse]

Pass 1 renders the page in flow with a probe (headless Chrome, own profile, port 9731) and records where every
index entry, stop and reader sits; pass 2 draws each section's own background layer to those numbers: the system
drawing (sky, strata, cables, labels) behind the drawing section, and the strata plus the row's cable behind the
journey. Text is always in flow; only the SVG layers are absolute.
"""
from __future__ import annotations

import html
import json
import math
import re
import sys

sys.dont_write_bytecode = True

import content as K  # noqa: E402
import frame  # noqa: E402
import hp  # noqa: E402
import scenery as sn  # noqa: E402
from frame import (BASE_CSS, BRONZE, CHART, CLAY, DAY, GOLD, HERE, HORIZON, INK, KHAKI, MUTED, OLIVE,  # noqa: E402
                   PETROL, SILVER, SOFT, T_BRONZE, T_GOLD, T_SILVER, T_TOP, W, cable, check, measure, shell, static)
from hp import f, smooth  # noqa: E402

NAME = "arch-1"
TITLE = "Architecture"
FAR = "#297382"
LIGHT = "#E4EFEC"
RULE_P = "rgba(207,224,220,.22)"

# ================================================================== helpers
KW = {
    "sql": r"\b(CREATE|OR|REPLACE|VIEW|AS|SELECT|FROM|WHERE|AND|ORDER|BY|QUALIFY|ROW_NUMBER|row_number|OVER|"
           r"PARTITION|DESC|NULLS|LAST|CASE|WHEN|THEN|ELSE|END|DATE|TIMESTAMPTZ|TABLE|IF|NOT|EXISTS|PRIMARY|KEY|"
           r"NULL|DEFAULT|VARCHAR|INTEGER|FLOAT|TIMESTAMP|WITH|TIME|ZONE)\b",
    "py": r"\b(from|import|with|as|print)\b",
    "sh": r"^(gridflow|GET)\b",
    "json": r"(?!x)x",
}


def hl(code: str, lang: str) -> str:
    """Tiny highlighter: keywords (petrol), strings (clay), comments (muted)."""
    out = []
    for line in code.split("\n"):
        pat = re.compile(r"(#.*$|--.*$)|('[^']*'|\"[^\"]*\")|" + KW[lang], re.M)
        pos, buf = 0, []
        for mt in pat.finditer(line):
            buf.append(html.escape(line[pos:mt.start()], quote=False))
            tok = html.escape(mt.group(0), quote=False)
            if mt.group(1) and lang in ("py", "sh"):
                buf.append(f'<span class="c">{tok}</span>')
            elif mt.group(1):
                buf.append(tok)
            elif mt.group(2):
                q = mt.group(2)
                is_key = lang == "json" and line[mt.end():].lstrip().startswith(":")
                ident = lang == "sql" and q.startswith('"')
                buf.append(tok if (is_key or ident) else f'<span class="s">{tok}</span>')
            else:
                buf.append(f'<span class="k">{tok}</span>')
            pos = mt.end()
        buf.append(html.escape(line[pos:], quote=False))
        out.append("".join(buf))
    return "\n".join(out)


def well(code: str, lang: str, cls: str = "", label: str = "") -> str:
    cap = f'<p class="wl">{label}</p>' if label else ""
    return f'<figure class="wf {cls}">{cap}<pre class="well"><code>{hl(code, lang)}</code></pre></figure>'


def table(head: list[str], rows: list[list[str]], label: str = "") -> str:
    th = "".join(f'<th scope="col" class="{"n" if h in K.NUMERIC else ""}">{h.replace("_", "_<wbr>")}</th>' for h in head)
    tr = "".join("<tr>" + "".join(f'<td class="{"n" if h in K.NUMERIC else ""}">{v}</td>' for h, v in zip(head, r))
                 + "</tr>" for r in rows)
    cap = f'<p class="wl">{label}</p>' if label else ""
    return f'<figure class="wf">{cap}<div class="df"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div></figure>'


def record(head: list[str], rows: list[list[str]]) -> str:
    """A one-row result shown as a record: column, value (as DuckDB's line mode prints it)."""
    tr = "".join(f'<tr><th scope="row">{h}</th><td class="{"n" if h in K.NUMERIC else ""}">{v}</td></tr>'
                 for h, v in zip(head, rows[0]))
    return f'<figure class="wf"><div class="df rec"><table><tbody>{tr}</tbody></table></div></figure>'


def links(pairs: list[tuple[str, str]], cls: str = "kl") -> str:
    return f'<p class="{cls}">' + " ".join(f'<a href="{u}"><code>{t}</code></a>' for u, t in pairs) + "</p>"


def short(t: str) -> str:
    return t.replace("src/gridflow_models/", "gridflow_models/").replace("src/gridflow/", "").replace("/", "/<wbr>")


def inline_links(pairs: list[tuple[str, str]]) -> str:
    return " ".join(f'<a class="il" href="{u}"><code>{short(t)}</code></a>' for u, t in pairs)


def curly(s: str) -> str:
    """Typographic apostrophes in prose (outside tags)."""
    return re.sub(r"(?<=[A-Za-z])'(?=[A-Za-z])", "’", s)


# ================================================================== drawn parts (sources)
def gas_point(x: float, base: float) -> str:
    """ENTSO-G: a gas pipeline point, two pipe loops out of the ground with handwheels, and a metering kiosk."""
    def pipe(d: str) -> str:
        return (f'<path d="{d}" stroke="{INK}" stroke-width="7.4" fill="none" stroke-linejoin="round"></path>'
                f'<path d="{d}" stroke="{CLAY}" stroke-width="4.6" fill="none" stroke-linejoin="round"></path>')
    out = [pipe(f"M{f(x + 6)} {f(base + 3)} V{f(base - 30)} H{f(x + 70)} V{f(base + 3)}"),
           pipe(f"M{f(x + 20)} {f(base + 3)} V{f(base - 17)} H{f(x + 56)} V{f(base + 3)}")]
    for wx, wy in ((x + 38, base - 30), (x + 38, base - 17)):
        out.append(f'<path d="M{f(wx)} {f(wy)} V{f(wy - 9)}" stroke="{INK}" stroke-width="1.4"></path>'
                   f'<circle cx="{f(wx)}" cy="{f(wy - 12)}" r="4.2" fill="{DAY}" stroke="{INK}" stroke-width="1.2"></circle>'
                   f'<path d="M{f(wx - 4.2)} {f(wy - 12)} H{f(wx + 4.2)} M{f(wx)} {f(wy - 16.2)} V{f(wy - 7.8)}" '
                   f'stroke="{INK}" stroke-width=".7"></path>')
    out.append(f'<rect x="{f(x + 82)}" y="{f(base - 24)}" width="26" height="24" fill="{DAY}" stroke="{INK}" '
               f'stroke-width="1"></rect><path d="M{f(x + 79)} {f(base - 24)} L{f(x + 95)} {f(base - 31)} '
               f'L{f(x + 111)} {f(base - 24)}" fill="{KHAKI}" stroke="{INK}" stroke-width="1" stroke-linejoin="round"></path>'
               f'<rect x="{f(x + 88)}" y="{f(base - 16)}" width="7" height="16" fill="{INK}" opacity=".75"></rect>')
    posts = " ".join(f"M{f(xp)} {f(base)} v-11" for xp in hp._frange(x - 4, x + 116, 12))
    out.append(f'<path d="{posts} M{f(x - 4)} {f(base - 10)} H{f(x + 116)}" stroke="{INK}" stroke-width=".6" '
               f'opacity=".6"></path>')
    return "\n".join(out)


def pylon_sub(cx: float, base: float) -> str:
    """Elexon: a lattice pylon feeding a substation."""
    sx = cx - 40
    sub, ends = hp.substation(sx, base)
    px = cx - 92
    wires = hp.spans(hp.tips(px, base, .52, 1), ends, 8) + " " + hp.spans(
        [(px - 64, base - 38), (px - 64, base - 52), (px - 64, base - 62)], hp.tips(px, base, .52, -1), 5)
    return (f'<g stroke="{INK}" fill="none" stroke-linecap="round" stroke-width="1.3">{hp.pylon(px, base, .52)}</g>'
            f'<path d="{wires}" stroke="{INK}" stroke-width=".8" fill="none" opacity=".85"></path>' + sub)


# (key, draw(cx, base) -> svg, cable x offset from cx, label dy above the base, crop box for the index mark)
def asset_svg(key: str, cx: float, base: float) -> str:
    if key == "elexon":
        return pylon_sub(cx, base)
    if key == "neso":
        return hp.ccgt(cx - 34, base, .8)
    if key == "neso_data_portal":
        return sn.solar_farm_at(cx - 64, cx + 64, lambda x: base + (hp.prof(x) - hp.Y["surf"]))
    if key == "open_meteo":
        return hp.metmast(cx, base, 124)
    if key == "gie_alsi":
        return hp.sc(sn.lng_terminal(cx - 64, base), cx - 64, base, .8)
    if key == "gie_agsi":
        return hp.sc(hp.gasterminal(cx - 56, base), cx - 56, base, .9)
    if key == "entsog":
        return gas_point(cx - 56, base)
    return hp.sc(hp.converter(cx - 30, base), cx - 30, base, .92)


ASSET_H = {"elexon": 74, "neso": 96, "neso_data_portal": 66, "open_meteo": 138, "gie_alsi": 48, "gie_agsi": 44,
           "entsog": 46, "entsoe": 60}
# crop boxes (relative to cx, base) for the index marks: x0, y0, w, h
ASSET_BOX = {"elexon": (-130, -80, 180, 90), "neso": (-60, -100, 124, 110), "neso_data_portal": (-70, -70, 140, 76),
             "open_meteo": (-58, -142, 110, 150), "gie_alsi": (-70, -56, 140, 64), "gie_agsi": (-62, -50, 124, 58),
             "entsog": (-64, -46, 128, 54), "entsoe": (-66, -66, 132, 72)}


def mark_asset(key: str) -> str:
    x0, y0, w, h = ASSET_BOX[key]
    save = hp.Y["surf"]
    hp.Y["surf"] = 0
    body = asset_svg(key, 0, 0)
    hp.Y["surf"] = save
    return (f'<svg class="mk" width="44" height="34" viewBox="{x0} {y0} {w} {h}" preserveAspectRatio="xMidYMax meet" '
            f'aria-hidden="true"><path d="M{x0} 0 H{x0 + w}" stroke="{OLIVE}" stroke-width="3"></path>{body}</svg>')


# ================================================================== drawn parts (below ground)
def pit(x: float, y: float) -> str:
    return (f'<rect x="{f(x - 11)}" y="{f(y - 16)}" width="22" height="32" rx="2" fill="#DFDACA" stroke="{INK}" '
            f'stroke-width="1.2"></rect><path d="M{f(x - 11)} {f(y - 10)} H{f(x + 11)}" stroke="{INK}" '
            f'stroke-width=".7" opacity=".45"></path>')


def splice(x: float, y: float, fill: str = DAY) -> str:
    return (f'<rect x="{f(x - 4.5)}" y="{f(y - 8)}" width="9" height="16" rx="4.5" fill="{fill}" stroke="{INK}" '
            f'stroke-width="1.2"></rect>')


def lens_pair(x: float, y: float) -> str:
    return (f'<rect x="{f(x)}" y="{f(y - 3.2)}" width="24" height="6.4" rx="3.2" fill="{BRONZE}" stroke="{INK}" '
            f'stroke-width=".8"></rect><rect x="{f(x + 27)}" y="{f(y - 3.2)}" width="9" height="6.4" rx="3.2" '
            f'fill="{DAY}" stroke="{INK}" stroke-width=".8"></rect>')


def transformer(x: float, y: float) -> str:
    fins = " ".join(f"M{f(x + s * 13)} {f(y - 9 + 3.6 * k)} h{f(s * 5)}" for s in (-1, 1) for k in range(6))
    bush = "".join(f'<rect x="{f(x + dx - 1.8)}" y="{f(y - 21)}" width="3.6" height="7" fill="{DAY}" stroke="{INK}" '
                   f'stroke-width=".8"></rect>' for dx in (-7, 0, 7))
    return (f'<path d="{fins}" stroke="{INK}" stroke-width="1.6"></path>{bush}'
            f'<rect x="{f(x - 13)}" y="{f(y - 14)}" width="26" height="28" rx="1.5" fill="{KHAKI}" stroke="{INK}" '
            f'stroke-width="1.2"></rect><path d="M{f(x - 13)} {f(y - 6)} H{f(x + 13)}" stroke="{INK}" '
            f'stroke-width=".6" opacity=".45"></path>')


def tapbox(x: float, y: float) -> str:
    return (f'<rect x="{f(x - 8)}" y="{f(y - 6)}" width="16" height="12" rx="1.5" fill="{DAY}" stroke="{INK}" '
            f'stroke-width="1.2"></rect><path d="M{f(x - 4)} {f(y)} H{f(x + 4)}" stroke="{INK}" stroke-width="1"></path>')


def busbar(x0: float, x1: float, y: float) -> str:
    posts = "".join(f'<rect x="{f(xp - 3)}" y="{f(y + 5)}" width="6" height="9" fill="{KHAKI}" stroke="{INK}" '
                    f'stroke-width=".8"></rect>' for xp in hp._frange(x0 + 26, x1 - 20, 92))
    return (posts + f'<rect x="{f(x0)}" y="{f(y - 5)}" width="{f(x1 - x0)}" height="10" rx="2" fill="{DAY}" '
            f'stroke="{INK}" stroke-width="1.6"></rect><path d="M{f(x0 + 4)} {f(y)} H{f(x1 - 4)}" stroke="{GOLD}" '
            f'stroke-width="2.4"></path>')


def builder(x: float, y: float) -> str:
    return (f'<rect x="{f(x - 16)}" y="{f(y - 12)}" width="32" height="24" rx="2" fill="{GOLD}" stroke="{INK}" '
            f'stroke-width="1.3"></rect><path d="M{f(x - 9)} {f(y - 5)} H{f(x + 9)} M{f(x - 9)} {f(y + 1)} H{f(x + 9)} '
            f'M{f(x - 9)} {f(y + 7)} H{f(x + 3)}" stroke="{INK}" stroke-width=".9"></path>')


def term(x: float, y: float, fill: str, r: float = 6.5) -> str:
    return (f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="2"></circle>'
            f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r / 3)}" fill="{INK}"></circle>')


def joint(x: float, y: float, r: float = 3.6) -> str:
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{INK}"></circle>'


def leader(x0: float, y0: float, x1: float, y1: float) -> str:
    """A thin annotation leader from a part (dot) to its label."""
    mx = x1 - 14
    return (f'<path d="M{f(x0)} {f(y0)} L{f(mx)} {f(y1)} H{f(x1 - 4)}" stroke="{INK}" stroke-width=".8" fill="none" '
            f'opacity=".7"></path><circle cx="{f(x0)}" cy="{f(y0)}" r="1.8" fill="{INK}"></circle>')


def lab(x: float, y: float, s: str, fill: str = INK, anchor: str = "start", cls: str = "") -> str:
    return f'<text x="{f(x)}" y="{f(y)}" fill="{fill}" text-anchor="{anchor}" class="{cls}">{s}</text>'


def sw(fill: str, pat: str, op: str) -> str:
    return (f'<svg class="mk" width="34" height="24" viewBox="0 0 34 24" aria-hidden="true">'
            f'<rect x=".75" y=".75" width="32.5" height="22.5" fill="{fill}"></rect>'
            f'<rect x=".75" y=".75" width="32.5" height="22.5" fill="url(#{pat})" opacity="{op}"></rect>'
            f'<rect x=".75" y=".75" width="32.5" height="22.5" fill="none" stroke="{INK}" stroke-width="1.3"></rect></svg>')


def mk(inner: str, vb: str = "0 0 34 24") -> str:
    return f'<svg class="mk" width="34" height="24" viewBox="{vb}" aria-hidden="true">{inner}</svg>'


def cab_v(x: float, y0: float, y1: float, core: str) -> str:
    return cable(f"M{f(x)} {f(y0)} V{f(y1)}", core)


UG_MARKS = {
    "boundary-vendor-connector": mk(cab_v(17, -2, 26, BRONZE) + pit(17, 12) + cab_v(17, -4, 28, BRONZE) + splice(17, 12)),
    "boundary-connector-bronze": mk(lens_pair(2, 12)),
    "stratum-bronze": sw(T_BRONZE, "p-brick", ".45"),
    "boundary-bronze-silver": mk(cab_v(17, -2, 27, SILVER) + transformer(17, 13), "0 -1 34 26"),
    "stratum-silver": sw(T_SILVER, "p-diag", ".5"),
    "boundary-silver-views": mk(cab_v(17, -2, 26, SILVER) + tapbox(17, 12)),
    "catalogue": mk(busbar(1, 33, 9), "0 0 34 24"),
    "stratum-gold": sw(T_GOLD, "p-stip", ".55"),
}

# ================================================================== layout constants
SRC_COL = [80 + 330 * k for k in range(4)]          # source index columns (290 wide, 40 gap)
SRC_CX = {}
for k in range(4):
    SRC_CX[K.SRC_ORDER[2 * k]] = SRC_COL[k] + 78
    SRC_CX[K.SRC_ORDER[2 * k + 1]] = SRC_COL[k] + 222
BX = [124 + 67 * i for i in range(8)]               # the bundle below ground, west to east
LANE = 676                                          # drawing labels
LAND_H = 250                                        # landscape band height (fixed)
FOOT_H = 112

# ================================================================== html
def opening() -> str:
    lk = " ".join(f'<a href="{u}"><code>{t}</code></a>' for u, t in K.OPEN_LINKS)
    return (f'<section class="sky open" data-section="opening" data-st="opening" aria-labelledby="h1">'
            f'{frame.masthead("Architecture")}<h1 id="h1">{K.H1}</h1>'
            f'<div class="open-g"><p class="lead">{curly(K.LEDE)}</p>'
            f'<div><p class="scope">{curly(K.SCOPE).replace("gridflow command", "<code>gridflow</code> command")}</p>'
            f'<p class="kl on">{lk}</p></div></div></section>')


def drawing_html() -> str:
    src = []
    for key in K.SRC_ORDER:
        s = K.src(key)
        src.append(f'<li class="ks" data-t="src-{key}">{mark_asset(key)}<h3>{s["human"]}</h3>'
                   f'<p><a href="{s["url"]}"><code>{key}</code></a> {s["line"]}</p></li>')
    ug = []
    for i, (pid, line, lks) in enumerate(K.UG):
        brk = " brk" if i in (0, 2, 5) else ""
        ug.append(f'<li class="ki{brk}" data-t="ug-{i}">{UG_MARKS[pid]}<p>{line} {inline_links(lks)}</p></li>')
    rd = []
    for j, (rid, title, line, lks, site) in enumerate(K.READERS):
        extra = (f' <a class="alt" href="{site[0]}">{site[1]}</a>' if site else "")
        rd.append(f'<li class="kr" data-t="rd-{j}"><h3 data-t="rh-{j}">{title}</h3><p>{line}</p>'
                  f'<p class="kl">{" ".join(f"<a href=\"{u}\"><code>{short(t)}</code></a>" for u, t in lks)}{extra}</p></li>')
    return (f'<section class="drw" data-section="drawing" data-st="drawing" aria-labelledby="drw-h">@@LAYER_DRAW@@'
            f'<div class="wrap"><div class="two head"><h2 class="sec-h" id="drw-h">{K.H2_DRAW}</h2>'
            f'<p>{K.DRAW_INTRO}</p></div>'
            f'<ul class="k-src" aria-label="Above ground: the sources">{"".join(src)}</ul>'
            f'<div class="k-land" data-t="land" style="height: {LAND_H}px"></div>'
            f'<div class="k-ug"><ol class="k-ul" aria-label="Below ground, top to bottom">{"".join(ug)}</ol></div>'
            f'<div class="k-foot" data-t="foot" style="height: {FOOT_H}px"></div>'
            f'<ul class="k-read" aria-label="At the foot: the readers">{"".join(rd)}</ul></div></section>')


def stop_text(n: int, h: str = "h3") -> str:
    s = K.stop(n)
    return (f'<{h} data-t="sh-{n}">{s["heading"]}</{h}><p>{curly(K.BODY[n])}</p>{links(K.links_of(n))}')


def journey_html() -> str:
    s1 = (f'<article class="stop" data-t="st-1" data-band="top"><div class="stop-t">{stop_text(1)}</div>'
          f'<div class="stop-o">{well(K.snip("01-cli.sh"), "sh")}</div></article>')
    s2 = (f'<article class="stop gap-b" data-t="st-2" data-band="top"><div class="stop-t">{stop_text(2)}</div>'
          f'<div class="stop-o">{well(K.snip("02-connector-request.txt"), "sh")}'
          f'<figure class="wf"><pre class="well"><code>{hl(K.snip("02-connector-request.py"), "py")}</code>'
          f'<code class="out">{html.escape(K.OUT2, quote=False)}</code></pre></figure>'
          f'</div></article>')
    files3 = K.snip("03-bronze-files.txt")
    s3 = (f'<article class="stop gap-b" data-t="st-3" data-band="bronze"><div class="stop-t">{stop_text(3)}'
          f'{well(files3, "json", "files")}</div>'
          f'<div class="stop-o">{well(K.snip("03-bronze-body-excerpt.json"), "json", "", "<code>raw_20260908T214403Z_3a7fca58.json</code>, " + K.new("excerpt"))}</div>'
          f'<div class="full">{well(K.snip("03-bronze-sidecar.json"), "json", "fit", "<code>raw_20260908T214403Z_3a7fca58.meta.json</code>")}</div></article>')
    s4 = (f'<article class="stop" data-t="st-4" data-band="silver"><div class="stop-t">{stop_text(4)}</div>'
          f'<div class="stop-o">{well(K.snip("04-silver-files.txt"), "json")}{well(K.snip("04-silver-vintages.sql"), "sql")}</div>'
          f'<div class="full">{table(*K.OUT4)}</div></article>')
    ddl = K.snip("05-latest-view-ddl.sql").replace(
        "CASE \"run_type\" WHEN 'II' THEN 1 WHEN 'SF' THEN 2 WHEN 'R1' THEN 3 WHEN 'R2' THEN 4 WHEN 'R3' THEN 5 WHEN 'RF' THEN 6 WHEN 'DF' THEN 7 ELSE 0 END DESC",
        "CASE \"run_type\" WHEN 'II' THEN 1 WHEN 'SF' THEN 2\n"
        "                  WHEN 'R1' THEN 3 WHEN 'R2' THEN 4 WHEN 'R3' THEN 5\n"
        "                  WHEN 'RF' THEN 6 WHEN 'DF' THEN 7 ELSE 0 END DESC")
    reads = (f'<div class="reads">'
             f'<div data-t="read-asof">{well(K.snip("05-as-of.sql"), "sql", "", K.new("Read as of 2026-09-09 12:00"))}{record(*K.OUT5A)}</div>'
             f'<div data-t="read-latest">{well(ddl, "sql", "", K.new("The view, as gridflow registers it"))}'
             f'{well(K.snip("05-latest-view.sql"), "sql", "", K.new("Read the <code>_latest</code> view"))}{record(*K.OUT5L)}</div></div>')
    fig = (f'<figure class="fig5" data-t="fig5"><h4>{K.FIG5_H}</h4>{fig5()}'
           f'<figcaption class="cap">{K.FIG5_CAP.replace("system_prices", "<code>system_prices</code>").replace("system_sell_price", "<code>system_sell_price</code>").replace("available_at", "<code>available_at</code>")}</figcaption></figure>')
    s5 = (f'<article class="stop gap-b hero5" data-t="st-5" data-band="silver"><div class="stop-t">{stop_text(5, "h3")}'
          f'<p class="mech">{curly(K.MECH)}</p></div>'
          f'<div class="stop-o">{fig}</div>{reads}</article>')
    spread = well(K.snip("06-gold-spread.py"), "py")
    g6 = K.snip("06-gold-build.py").replace(
        "gold = builder.build(date(2026, 9, 8), date(2026, 9, 8))  # build() returns the frame; run() writes it",
        "# build() returns the frame; run() writes it\ngold = builder.build(date(2026, 9, 8), date(2026, 9, 8))")
    s6 = (f'<article class="stop gap-b" data-t="st-6" data-band="gold"><div class="stop-t">{stop_text(6)}</div>'
          f'<div class="stop-o">{well(K.snip("06-gold-build.sh"), "sh")}{spread}{well(g6, "py")}</div>'
          f'<div class="full">{table(*K.OUT6)}</div></article>')
    s7 = (f'<article class="stop on-deep" data-t="st-7" data-band="deep"><div class="stop-t">{stop_text(7)}</div>'
          f'<div class="stop-o">{well(K.snip("07-client.py"), "py")}{table(*K.OUT7)}</div></article>')
    head = (f'<div class="two head jr-head" data-t="jr-head"><h2 class="sec-h" id="jr-h">{K.H2_JOURNEY}</h2>'
            f'<p>{curly(K.EXAMPLE)}</p></div>')
    return (f'<section class="jr" data-section="journey" data-st="journey" aria-labelledby="jr-h">@@LAYER_JR@@'
            f'<div class="wrap">{head}<div class="stops">{s1}{s2}{s3}{s4}{s5}{s6}{s7}</div></div></section>')


def correct_html() -> str:
    rules = "".join(f'<li><p>{r.replace("available_at", "<code>available_at</code>")}</p>{links(lk)}</li>'
                    for r, lk in K.RULES)
    return (f'<section class="cor deep" data-section="correct" data-st="correct" aria-labelledby="cor-h">@@LAYER_COR@@'
            f'<div class="wrap two-c"><div><h2 class="sec-h" id="cor-h">{K.H2_CORRECT}</h2><ul class="rules">{rules}</ul></div>'
            f'<div class="cor-r"><h3>{K.RUN_H}</h3><p>{curly(K.RUN_TEXT)}</p>{links(K.RUN_LINKS)}'
            f'{well(K.snip("08-run-tracking.sql"), "sql")}'
            f'<h3>{K.CI_H}</h3><p>{curly(K.CI_TEXT)}</p>{links(K.CI_LINKS)}</div></div></section>')


def look_html() -> str:
    li = "".join(f'<li><p>{K.new("For") + " " + d}</p>{links(lk)}</li>' for d, lk in K.LOOK)
    return (f'<section class="look deep" data-section="look" data-st="look" aria-labelledby="look-h">@@LAYER_LOOK@@'
            f'<div class="wrap"><h2 class="sec-h" id="look-h">{K.H2_LOOK}</h2><ul class="lk">{li}</ul></div></section>')


def footer_html() -> str:
    lk = "".join(f'<li><a href="#">{n}</a></li>' for n in ["Data sources", "Architecture", "Models", "About", "GitHub"])
    return (f'<footer class="st st-deep deep" data-st="deep">@@LAYER_FOOT@@<div class="foot"><a class="brand" href="#">gridflow</a>'
            f'<ul>{lk}</ul><p>{K.new("This site is MIT-licensed. gridflow is Apache-2.0.")}</p></div></footer>')


# ================================================================== stop 5 figure
def fig5() -> str:
    Wd, Hd = 820, 218
    x0, x1 = 84, 776
    X = lambda h: x0 + (x1 - x0) * h / 48  # noqa: E731
    tA = 17 + 48 / 60 + 45 / 3600
    tB = 24 + 17 + 44 / 60 + 29 / 3600
    tC = 36
    ya, yb, yax = 84, 146, 188
    xe = x1 + 18
    g = []
    # rows: dotted before the version exists, then the version as a cable to the right edge (both are kept)
    for y, t, val in ((ya, tA, "9.56"), (yb, tB, "110.00")):
        g.append(f'<path d="M{x0} {y} H{f(X(t) - 9)}" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="1.5 5" '
                 f'stroke-linecap="round"></path>')
        g.append(cable(f"M{f(X(t))} {y} H{xe}", SILVER, 5, 1.8))
        g.append(term(X(t), y, T_SILVER))
        g.append(f'<text x="0" y="{y + 6}" class="val">{val}</text>')
    g.append(f'<text x="{f(X(tA) - 13)}" y="{ya - 12}" class="an" text-anchor="end"><tspan class="mo">available_at</tspan> '
             f'2026-09-08 17:48:45</text>')
    g.append(f'<text x="{xe - 2}" y="{yb - 35}" class="an" text-anchor="end"><tspan class="mo">available_at</tspan></text>'
             f'<text x="{xe - 2}" y="{yb - 15}" class="an" text-anchor="end">2026-09-09 17:44:29</text>')
    # the as-of read
    xc = X(tC)
    g.append(f'<path d="M{f(xc)} 34 V{yax}" stroke="{INK}" stroke-width="1.2" stroke-dasharray="4 4"></path>')
    g.append(f'<circle cx="{f(xc)}" cy="{ya}" r="6.5" fill="{CHART}" stroke="{INK}" stroke-width="1.6"></circle>')
    g.append(f'<text x="{f(xc - 10)}" y="24" class="an" text-anchor="end">{K.new("as of 2026-09-09 12:00, the read returns")} '
             f'<tspan class="mo b">9.56</tspan></text>')
    # the latest view
    g.append(f'<path d="M{xe} {yb - 15} v30" stroke="{INK}" stroke-width="1.8"></path>')
    g.append(f'<text x="{xe - 2}" y="{yb + 27}" class="an" text-anchor="end"><tspan class="mo">_latest</tspan> '
             f'{K.new("returns")} <tspan class="mo b">110.00</tspan></text>')
    # time axis, UTC
    g.append(f'<path d="M{x0} {yax} H{xe}" stroke="{INK}" stroke-width="1.2"></path>')
    for h, s_ in ((0, "8 Sep 00:00"), (12, "8 Sep 12:00"), (24, "9 Sep 00:00"), (36, "9 Sep 12:00"), (48, "10 Sep 00:00")):
        g.append(f'<path d="M{f(X(h))} {yax} v6" stroke="{INK}" stroke-width="1.2"></path>'
                 f'<text x="{f(X(h))}" y="{yax + 23}" text-anchor="middle" class="tk">{s_}</text>')
    aria = K.new("Timeline of the two versions of Elexon system_prices for settlement date 2026-09-08, period 37. "
                 "9.56 is available from 2026-09-08 17:48:45 UTC and 110.00 from 2026-09-09 17:44:29 UTC; both are "
                 "kept. A read as of 2026-09-09 12:00 returns 9.56; the _latest view returns 110.00.")
    return (f'<svg class="tl" width="{Wd}" height="{Hd}" viewBox="0 0 {Wd} {Hd}" role="img" aria-label="{aria}">'
            + "".join(g) + "</svg>")


# ================================================================== css
CSS = """.root code{font-family:"Red Hat Mono",monospace}
.sec-h{font-size:42px;font-weight:720;font-stretch:88%;line-height:1.02;letter-spacing:-.018em;margin:0;color:#F6F4EC}
.two{display:grid;grid-template-columns:760px 420px;column-gap:100px;align-items:end}
.head p{margin:0;font-size:16px;line-height:1.62;color:#CFE0DC;max-width:58ch}
.head p code{color:#F6F4EC;font-size:.9em}
.kl{margin:6px 0 0;font-size:13px;line-height:1.5;display:flex;flex-wrap:wrap;column-gap:16px;row-gap:2px}
.kl code{font-size:13px}
.root .kl a{color:#1C2B22;text-decoration-color:#66793B}
.kl.on a,.kr .kl a,.deep .kl a,.on-deep .kl a{color:#F6F4EC;text-decoration-color:#AFC64E}
.root .alt{font-family:"Hanken Grotesk",sans-serif;font-size:14.5px}
/* opening */
.open{padding-bottom:88px}
.open h1{margin-top:68px;color:#F6F4EC;font-weight:760;font-stretch:84%;font-size:86px;line-height:.94;letter-spacing:-.022em}
.open-g{display:grid;grid-template-columns:760px 420px;column-gap:100px;margin-top:34px;align-items:start}
.open .lead{margin:0;font-size:21px;line-height:1.5;color:#F6F4EC;max-width:58ch}
.open .scope{margin:4px 0 0;font-size:16px;line-height:1.62;color:#CFE0DC}
.open .scope code{color:#F6F4EC;font-size:.9em}
/* drawing */
.drw,.jr,.deep{position:relative}
.open,.drw,.jr{background:#155A6E}
.drw .wrap,.jr .wrap{position:relative;padding:0 80px}
.drw .head{padding-top:6px}
.k-src{list-style:none;margin:40px 0 0;padding:0;display:grid;grid-template-columns:repeat(4,290px);grid-template-rows:auto auto;grid-auto-flow:column;column-gap:40px;row-gap:18px}
.ks{display:grid;grid-template-columns:44px minmax(0,1fr);column-gap:12px;align-items:start;padding-top:12px;border-top:1px solid rgba(207,224,220,.22)}
.ks .mk{grid-row:1 / 3;margin-top:2px}
.ks h3{margin:0;font-family:"Hanken Grotesk",sans-serif;font-size:15px;font-weight:600;line-height:1.35;color:#F6F4EC}
.ks p{margin:3px 0 0;font-size:14px;line-height:1.45;color:#CFE0DC}
.ks a{color:#F6F4EC;text-decoration-color:#AFC64E}
.ks code{font-size:13px}
.k-ug{display:grid;grid-template-columns:minmax(0,1fr) 420px;padding:100px 0 64px}
.k-ul{grid-column:2;list-style:none;margin:0;padding:0}
.ki{display:grid;grid-template-columns:34px minmax(0,1fr);column-gap:14px;margin-bottom:18px}
.ki.brk{margin-bottom:60px}
.ki:last-child{margin-bottom:0}
.ki p{margin:0;font-size:14px;line-height:1.5;color:#3F4A3B}
.ki .il{margin-left:2px;margin-right:6px;color:#1C2B22;text-decoration-color:#66793B;white-space:nowrap}
.ki .il code{font-size:12.5px}
.ki p code{font-size:13px;color:#1C2B22;overflow-wrap:anywhere}
.ki .kl{margin-top:5px}
.k-read{list-style:none;margin:0;padding:0 0 40px;display:grid;grid-template-columns:repeat(4,290px);column-gap:40px}
.kr h3{margin:0 0 6px;font-size:20px;font-weight:720;font-stretch:90%;line-height:1.15;letter-spacing:-.008em;color:#F6F4EC}
.kr p{margin:0;font-size:14.5px;line-height:1.5;color:#CFE0DC}
.kr p code{color:#F6F4EC;font-size:13px}
.kr .kl{margin-top:8px}

.mk{display:block;overflow:visible}
.lab text{font-family:"Hanken Grotesk",sans-serif;font-style:italic;font-size:13.5px}
.lab text.mo,.lab tspan.mo{font-family:"Red Hat Mono",monospace;font-style:normal;font-size:12.5px}
/* journey */
.jr-head{padding:18px 0 0}
.stops{padding:124px 0 0}
.stop{display:grid;grid-template-columns:400px 820px;column-gap:60px;align-items:start;margin-bottom:72px}
.stop.gap-b{margin-bottom:138px}
.stop h3{margin:0 0 10px;font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em;color:#1C2B22}
.stop p{margin:0 0 10px;font-size:16px;line-height:1.62;color:#3F4A3B}
.stop p code{font-size:.9em;color:#1C2B22}
.stop-t .kl{margin:2px 0 0}
.stop-t .wf{margin-top:20px}
.stop-o{display:flex;flex-direction:column;gap:14px;min-width:0}
.full{grid-column:1 / -1;margin-top:26px;min-width:0}
.wf{margin:0;min-width:0}
.wl{margin:0 0 6px;font-size:14px;line-height:1.4;color:#3F4A3B;font-style:italic}
.wl code{font-style:normal;font-size:13px;color:#1C2B22}
.root .well{margin:0;background:#F6F4EC;border:1px solid rgba(28,43,34,.24);border-radius:3px;padding:11px 14px;font:400 13.5px/1.6 "Red Hat Mono",monospace;color:#1C2B22;white-space:pre;overflow-x:auto;overflow-y:hidden}
.well code{font-size:13.5px}
.well code.out{display:block;margin:10px -14px 0;padding:8px 14px 0;border-top:1px solid rgba(28,43,34,.18);color:#3F4A3B}
.fit .well{width:max-content;max-width:100%;box-sizing:border-box}
.df{overflow-x:auto;border:1px solid rgba(28,43,34,.3);border-radius:3px;background:#F6F4EC}
.df table{border-collapse:collapse;font:400 13px/1.5 "Red Hat Mono",monospace;font-variant-numeric:tabular-nums;color:#1C2B22;min-width:100%}
.df th{font-weight:500;text-align:left;padding:7px 12px 6px;border-bottom:1.5px solid #1C2B22;vertical-align:bottom;line-height:1.3}
.df td{padding:6px 12px;white-space:nowrap}
.df .n{text-align:right}
.rec table{min-width:0;width:100%}
.rec th{border-bottom:0;border-right:1.5px solid #1C2B22;width:1%;font-weight:400;color:#3F4A3B}
.rec td{font-size:14px;font-weight:500}
.rec td.n{text-align:left}
.rec tbody tr:nth-child(even) th{background:#EFEBDF}
.df tbody tr:nth-child(even) td{background:#EFEBDF}
.hero5 .stop-t h3{font-size:30px;font-weight:700;font-stretch:90%;line-height:1.08;letter-spacing:-.012em;margin-bottom:14px}
.hero5 .mech{margin-top:16px;padding-top:12px;border-top:1px solid rgba(28,43,34,.22);font-size:14.5px;line-height:1.55}
.fig5{margin:6px 0 0}
.fig5 h4{margin:0 0 14px;font-family:"Bricolage Grotesque",sans-serif;font-size:23px;font-weight:720;font-stretch:90%;line-height:1.1;letter-spacing:-.01em}
.fig5 .cap code{font-size:.9em}
.tl{display:block;overflow:visible}
.tl text{font-family:"Hanken Grotesk",sans-serif;fill:#1C2B22}
.tl .an{font-style:italic;font-size:13.5px}
.tl .mo{font-family:"Red Hat Mono",monospace;font-style:normal;font-size:12.5px}
.tl .b{font-weight:500;font-size:14px}
.tl .val{font-family:"Red Hat Mono",monospace;font-size:17px;font-weight:500}
.tl .tk{font-size:13px;fill:#3F4A3B}
.reads{grid-column:1 / -1;display:grid;grid-template-columns:612px 608px;column-gap:60px;margin-top:40px;align-items:start}
.reads .well{font-size:13px}
.reads .well code{font-size:13px}
.reads > div{display:flex;flex-direction:column;gap:12px;min-width:0}
.on-deep h3{color:#F6F4EC}
.on-deep p{color:#CFE0DC}
.on-deep p code{color:#F6F4EC}
/* deep sections */
.deep{background:#155A6E}
.two-c{display:grid;grid-template-columns:600px 620px;column-gap:60px;align-items:start}
.cor .wrap{position:relative;padding:40px 80px 96px}
.rules{list-style:none;margin:30px 0 0;padding:0;border-top:1px solid rgba(207,224,220,.22)}
.rules li{padding:13px 0 14px;border-bottom:1px solid rgba(207,224,220,.22)}
.rules p{margin:0;font-size:16.5px;line-height:1.5;color:#F6F4EC;max-width:58ch}
.rules p code{font-size:.88em}
.cor-r{padding-top:6px}
.cor-r h3{margin:0 0 8px;font-size:20px;font-weight:720;font-stretch:90%;line-height:1.15;color:#F6F4EC}
.cor-r h3 + p{margin:0;font-size:15.5px;line-height:1.6;color:#CFE0DC}
.cor-r p code{color:#F6F4EC;font-size:.88em}
.cor-r .wf{margin:18px 0 34px}
.look .wrap{position:relative;padding:22px 80px 92px}
.lk{list-style:none;margin:28px 0 0;padding:0;display:grid;grid-template-columns:600px 620px;grid-template-rows:repeat(5,auto);grid-auto-flow:column;column-gap:60px}
.lk li{padding:11px 0 12px;border-top:1px solid rgba(207,224,220,.22)}
.lk p{margin:0;font-size:14.5px;line-height:1.45;color:#CFE0DC}
.lk .kl{margin-top:3px}
.lk .kl code{font-size:13.5px}
.st-deep{position:relative}
.st-deep .foot{position:relative}
"""

PROBE_EXTRA = ""


def page_body(layers: dict[str, str]) -> str:
    body = "\n".join([opening(), drawing_html(), journey_html(), correct_html(), look_html(), footer_html()])
    for k in ("DRAW", "JR", "COR", "LOOK", "FOOT"):
        body = body.replace(f"@@LAYER_{k}@@", layers.get(k, ""))
    return body


# ================================================================== pass 2: layers
def rel(m: dict, key: str, top: float) -> tuple[float, float, float, float]:
    l, t, r, b = m["t"][key]
    return l, t - top, r, b - top


def wave(y: float, amp: float, seed: float) -> str:
    return smooth(hp.wave(y, amp, seed))


def band_layer(Hs: float, surf_y: float | None, contacts: list[tuple[str, float]], deep_y: float | None,
               extra: str, aria: str = "", surface: bool = True, prof=None, pre: str = "") -> str:
    """One section's own ground: optional surface (olive root), wavy contacts, then the deep (granite)."""
    tail = f" L{W + 40} {f(Hs + 10)} L-40 {f(Hs + 10)} Z"
    out, lines = [pre], []
    if surf_y is not None:
        pf = prof or (lambda x: surf_y + 3 * math.sin(x / 190 + .6) - 2 * math.sin(x / 83 + 1.3))
        pts = [(x, pf(x)) for x in range(-40, W + 41, 10)]
        sd = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)
        root = sd + " " + " ".join(f"L{f(x)} {f(y + 9)}" for x, y in reversed(pts)) + " Z"
        out.append(f'<path d="{sd}{tail}" fill="{T_TOP}"></path><path d="{sd}{tail}" fill="url(#p-soil)" opacity=".5"></path>')
    fills = {"bronze": (T_BRONZE, "p-brick", ".15"), "silver": (T_SILVER, "p-diag", ".22"), "gold": (T_GOLD, "p-stip", ".26")}
    seeds = {"bronze": (7, .4), "silver": (8, 2.1), "gold": (7, 4.0)}
    for name, y in contacts:
        amp, seed = seeds[name]
        d = wave(y, amp, seed)
        fl, pid, op = fills[name]
        out.append(f'<path d="{d}{tail}" fill="{fl}"></path><path d="{d}{tail}" fill="url(#{pid})" opacity="{op}"></path>')
        lines.append(d)
    if deep_y is not None:
        gd = smooth(frame.rough(deep_y))
        out.append(f'<path d="{gd}{tail}" fill="{PETROL}"></path><path d="{gd}{tail}" fill="url(#p-granite)" opacity=".5"></path>')
    if surf_y is not None and surface:
        out.append(f'<path d="{root}" fill="{OLIVE}"></path><path d="{sd}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    if lines:
        out.append(f'<path d="{" ".join(lines)}" stroke="{INK}" stroke-width="1.5" fill="none"></path>')
    if deep_y is not None:
        out.append(f'<path d="{smooth(frame.rough(deep_y))}" stroke="{INK}" stroke-width="2" fill="none" stroke-linejoin="round"></path>')
    role = f'role="img" aria-label="{aria}"' if aria else 'aria-hidden="true"'
    return (f'<svg class="layer" width="{W}" height="{f(Hs)}" viewBox="0 0 {W} {f(Hs)}" {role}>'
            f'<defs>{frame.PATTERNS}</defs>' + "\n".join(out) + extra + "</svg>")


def granite(Hs: float) -> str:
    return (f'<svg class="layer" width="{W}" height="{f(Hs)}" viewBox="0 0 {W} {f(Hs)}" aria-hidden="true">'
            f'<defs>{frame.PATTERNS}</defs><rect x="0" y="0" width="{W}" height="{f(Hs)}" fill="url(#p-granite)" '
            f'opacity=".5"></rect></svg>')


def draw_drawing(m: dict) -> str:
    top, Hs = m["secs"]["drawing"]
    R = lambda k: rel(m, k, top)  # noqa: E731
    S = R("land")[3]
    hp.Y["surf"] = S
    prof = hp.prof
    e = [R(f"ug-{i}") for i in range(8)]
    mid = lambda r: (r[1] + r[3]) / 2  # noqa: E731
    c_tb = (e[0][3] + e[1][1]) / 2
    c_bs = (e[2][3] + e[3][1]) / 2
    c_sg = (e[5][3] + e[6][1]) / 2
    c_gd = e[7][3] + 46
    src_bottom = max(R(f"src-{k}")[3] for k in K.SRC_ORDER)
    g: list[str] = []
    labs: list[str] = []
    # ---- sky: ridges, turbines, energised field
    g.append(sn.ridge([(-20, S - 176), (160, S - 196), (360, S - 184), (560, S - 204), (760, S - 186),
                       (980, S - 198), (1200, S - 180), (1460, S - 194)], S - 40, FAR))
    near = [(-20, S - 158), (120, S - 172), (300, S - 164), (470, S - 180), (660, S - 162), (850, S - 176),
            (1040, S - 160), (1250, S - 174), (1460, S - 164)]
    g.append(sn.ridge(near, S - 40, HORIZON))
    tur = [(380, S - 170, 54), (560, S - 178, 58), (700, S - 164, 50), (1010, S - 162, 52), (1180, S - 168, 56),
           (1400, S - 166, 52)]
    for i, (tx, ty, th) in enumerate(tur):
        g.append(hp.turbine(tx, ty + 2, th, th * .5, ["sp1", "sp2", "sp3"][i % 3], 31 * i + 12))
    field_top = [(-20, S - 124), (200, S - 132), (420, S - 122), (640, S - 130), (860, S - 120), (1080, S - 128),
                 (1300, S - 122), (1460, S - 126)]
    g.append(sn.field(field_top, prof, -20, 1460,
                      [[(-20, S - 92), (400, S - 97), (900, S - 88), (1460, S - 95)],
                       [(-20, S - 50), (600, S - 54), (1460, S - 48)]]))
    for key in K.SRC_ORDER:
        cx = SRC_CX[key]
        g.append(asset_svg(key, cx, prof(cx)))
    # vendor labels above each asset
    for key in K.SRC_ORDER:
        cx = SRC_CX[key]
        if key == "open_meteo":
            labs.append(lab(cx + 24, prof(cx) - 100, K.src(key)["label"], INK, "start"))
            continue
        labs.append(lab(cx, prof(cx) - ASSET_H[key] - 10, K.src(key)["label"], INK, "middle"))
    # ---- ground
    # ---- cables: topsoil tray, nested so none cross
    cab: list[str] = []
    fix: list[str] = []
    y_bay = mid(e[0])
    rows = [c_tb + 30 + k * (c_bs - 70 - c_tb - 30) / 3 for k in range(4)]
    y_view = mid(e[5])
    y_bus = mid(e[6])
    y_b = mid(e[7])
    y_col = (e[4][3] + e[5][1]) / 2
    s_rows = [c_bs + 52 + k * 30 for k in range(4) if c_bs + 52 + k * 30 < y_col - 26]
    for i, key in enumerate(K.SRC_ORDER):
        x, t = SRC_CX[key], BX[i]
        L = S + 20 + 9 * i
        r = 10
        d = (f"M{f(x)} {f(prof(x) - 2)} V{f(L - r)} Q{f(x)} {f(L)} {f(x - r)} {f(L)} H{f(t + r)} "
             f"Q{f(t)} {f(L)} {f(t)} {f(L + r)} V{f(c_bs)}")
        cab.append(cable(d, BRONZE))
        fix.append(pit(t, y_bay) + cab_v(t, y_bay - 16, y_bay + 16, BRONZE) + splice(t, y_bay))
        fix.append(splice(t, c_tb, T_BRONZE))
        for y in rows:
            fix.append(lens_pair(t + 9, y))
        fix.append(transformer(t, c_bs))
        for y in s_rows:
            fix.append(f'<rect x="{f(t + 9)}" y="{f(y - 3.2)}" width="28" height="6.4" rx="1.5" fill="{SILVER}" '
                       f'stroke="{INK}" stroke-width=".8"></rect>')
        end = y_bus - 5 if i else y_b - 12
        cab.append(cable(f"M{f(t)} {f(c_bs + 14)} V{f(end)}", SILVER))
        fix.append(tapbox(t, y_view))
    # elexon: its _latest view, its link to the catalogue, on down to the builder
    fix.append(tapbox(BX[0], y_view + 20))
    labs.append(lab(BX[0] - 13, y_view + 24, "_latest", INK, "end", "mo"))
    fix.append(f'<path d="M{BX[0]} {f(y_bus)} H{f(BX[0] + 26)}" stroke="{INK}" stroke-width="2.4"></path>' + joint(BX[0], y_bus))
    # the collector: gridflow_models reads the silver files directly
    xm = BX[-1] + 56
    col_d = f"M{BX[0] - 10} {f(y_col)} H{f(xm - 10)} Q{f(xm)} {f(y_col)} {f(xm)} {f(y_col + 10)}"
    # catalogue busbar, builder, gold core and its view
    bus_x0, bus_x1 = BX[0] + 26, BX[-1] + 30
    fix.append(busbar(bus_x0, bus_x1, y_bus))
    fix.append(builder(BX[0], y_b))
    gcore = f"M{BX[0] + 16} {f(y_b)} H{BX[0] + 50} Q{BX[0] + 62} {f(y_b)} {BX[0] + 62} {f(y_b - 12)} V{f(y_bus + 5)}"
    cab.append(cable(gcore, GOLD))
    labs.append(lab(BX[0] - 18, y_b + 32, "system_marginal_price", INK, "start", "mo"))
    # ---- readers
    rd = [R(f"rd-{j}") for j in range(4)]
    rh = [R(f"rh-{j}") for j in range(4)]
    T = [(rd[j][0] - 16, mid(rh[j])) for j in range(4)]
    yf = {"models": c_gd + 40, "cli": c_gd + 56, "client": c_gd + 56, "nb": c_gd + 80}
    xcli, xcl = BX[3] - 36, BX[5] - 36
    r = 12

    def route(xa: float, ya: float, yh: float, xb: float, yb: float) -> str:
        s = -1 if xb < xa else 1
        return (f"M{f(xa)} {f(ya)} V{f(yh - r)} Q{f(xa)} {f(yh)} {f(xa + s * r)} {f(yh)} H{f(xb - s * r)} "
                f"Q{f(xb)} {f(yh)} {f(xb)} {f(yh + r)} V{f(yb)}")
    cab.append(cable(route(xcli, y_bus + 5, yf["cli"], T[0][0], Hs + 4), GOLD))
    cab.append(cable(route(xcl, y_bus + 5, yf["client"], T[1][0], T[1][1]), GOLD))
    cab.append(cable(route(T[1][0], yf["nb"] - 12, yf["nb"], T[2][0], T[2][1]), GOLD))
    cab.append(cable(col_d + f" V{f(yf['models'] - r)} Q{f(xm)} {f(yf['models'])} {f(xm + r)} {f(yf['models'])} "
                     f"H{f(T[3][0] - r)} Q{f(T[3][0])} {f(yf['models'])} {f(T[3][0])} {f(yf['models'] + r)} V{f(T[3][1])}",
                     SILVER, 3.8, 1.3))
    for i in range(8):
        fix.append(joint(BX[i], y_col, 3.2))
    fix.append(joint(T[1][0], yf["nb"]))
    for j in range(4):
        fix.append(term(T[j][0], T[j][1], T_GOLD if j < 3 else T_SILVER))
    # ---- labels in the lane, with leaders
    L0 = LANE
    lx = BX[-1]
    labs.append(lab(L0, mid(e[0]) + 4, K.LAB["boundary-vendor-connector"]))
    fix.append(leader(lx + 12, y_bay, L0, mid(e[0])))
    labs.append(lab(L0, mid(e[1]) + 4, K.LAB["boundary-connector-bronze"]))
    fix.append(leader(lx + 45, rows[0], L0, mid(e[1])))
    br_x = lx + 52
    fix.append(f'<path d="M{f(br_x)} {f(rows[0] - 6)} h5 V{f(rows[-1] + 6)} h-5" stroke="{INK}" stroke-width="1" fill="none"></path>')
    labs.append(lab(L0, mid(e[2]) + 4, K.LAB["stratum-bronze"]))
    fix.append(leader(br_x + 5, mid(e[2]) if rows[0] < mid(e[2]) < rows[-1] else (rows[1] + rows[2]) / 2, L0, mid(e[2])))
    labs.append(lab(L0, mid(e[3]) + 4, K.LAB["boundary-bronze-silver"]))
    fix.append(leader(lx + 18, c_bs + 6, L0, mid(e[3])))
    labs.append(lab(L0, mid(e[4]) + 4, K.LAB["stratum-silver"]))
    fix.append(leader(lx + 38, s_rows[min(1, len(s_rows) - 1)], L0, mid(e[4])))
    labs.append(lab(L0, mid(e[5]) + 4, K.LAB["boundary-silver-views"]))
    fix.append(leader(lx + 9, y_view, L0, mid(e[5])))
    labs.append(lab(L0, mid(e[6]) + 4, "one file: <tspan class=\"mo\">gridflow.duckdb</tspan>"))
    fix.append(leader(bus_x1 + 2, y_bus, L0, mid(e[6])))
    labs.append(lab(L0, mid(e[7]) + 4, K.LAB["stratum-gold"]))
    labs.append(lab(xm + 16, yf["models"] - 10, K.new("training and backtests read silver directly"), LIGHT))
    aria = K.new(
        "A section through gridflow. Above ground, eight sources stand on the grid: Elexon (a substation), NESO carbon "
        "intensity (a gas-fired power station), the NESO Data Portal (a solar farm), Open-Meteo (a met mast), GIE ALSI "
        "(an LNG terminal), GIE AGSI (gas storage), ENTSO-G (a gas pipeline point) and ENTSO-E (an interconnector "
        "converter station). A cable runs down from each, through a joint bay in the topsoil (the connector), into "
        "bronze, where raw responses lie with their sidecars by date; through a transformer into silver; to a view on "
        "the gridflow.duckdb busbar. The Elexon cable also feeds the system_marginal_price builder in gold. From the "
        "busbar, cables run to the gridflow command and GridflowClient, and on to notebooks; gridflow_models taps the "
        "silver cables directly.")
    extra = "".join(cab) + "".join(fix) + f'<g class="lab">{"".join(labs)}</g>'
    return band_layer(Hs, S, [("bronze", c_tb), ("silver", c_bs), ("gold", c_sg)], c_gd, extra, aria=aria,
                      prof=prof, pre="".join(g)), src_bottom


def draw_journey(m: dict) -> str:
    top, Hs = m["secs"]["journey"]
    R = lambda k: rel(m, k, top)  # noqa: E731
    st = {n: R(f"st-{n}") for n in range(1, 8)}
    sh = {n: R(f"sh-{n}") for n in range(1, 8)}
    head = R("jr-head")
    surf = (head[3] + st[1][1]) / 2 - 10
    c_tb = (st[2][3] + st[3][1]) / 2
    c_bs = (st[3][3] + st[4][1]) / 2
    c_sg = (st[5][3] + st[6][1]) / 2
    c_gd = (st[6][3] + st[7][1]) / 2
    X = 48
    mid = lambda r: (r[1] + r[3]) / 2  # noqa: E731
    ty = {n: mid(sh[n]) for n in range(1, 8)}
    c = []
    # the thread, continued from the gridflow command at the foot of the drawing
    c.append(cable(f"M64 -2 V{f(surf - 70)} C64 {f(surf - 40)} {X} {f(surf - 50)} {X} {f(surf - 20)} V{f(c_bs)}", BRONZE))
    c.append(cable(f"M{X} {f(c_bs)} V{f(ty[4])}", SILVER))
    # two versions between stop 4 and stop 5
    for dx in (-8, 8):
        c.append(cable(f"M{X} {f(ty[4])} C{X} {f(ty[4] + 40)} {X + dx} {f(ty[4] + 30)} {X + dx} {f(ty[4] + 70)} "
                       f"V{f(ty[5] - 70)} C{X + dx} {f(ty[5] - 30)} {X} {f(ty[5] - 40)} {X} {f(ty[5])}", SILVER, 4, 1.4))
    c.append(cable(f"M{X} {f(ty[5])} V{f(c_sg)}", SILVER))
    c.append(cable(f"M{X} {f(c_sg)} V{f(ty[7])}", GOLD))
    fx = [frame.sleeve(X, c_tb, T_BRONZE), frame.sleeve(X, c_bs, T_SILVER), frame.sleeve(X, c_sg, T_GOLD),
          frame.sleeve(X, c_gd, T_GOLD)]
    tint = {1: T_TOP, 2: T_TOP, 3: T_BRONZE, 4: T_SILVER, 5: T_SILVER, 6: T_GOLD, 7: T_GOLD}
    for n in range(1, 8):
        rr = 13 if n == 5 else 11
        fx.append(f'<path d="M{X + rr} {f(ty[n])} H72" stroke="{INK}" stroke-width="1.6"></path>')
        if n == 5:
            fx.append(f'<circle cx="{X}" cy="{f(ty[n])}" r="18" fill="{CHART}" stroke="{INK}" stroke-width="1.6"></circle>')
        fx.append(f'<circle cx="{X}" cy="{f(ty[n])}" r="{rr}" fill="{tint[n]}" stroke="{INK}" stroke-width="2"></circle>'
                  f'<text x="{X}" y="{f(ty[n] + 4.5)}" text-anchor="middle" class="num">{n}</text>')
    labs = "".join(lab(1360, y + 30, n, INK, "end") for n, y in (("bronze", c_tb), ("silver", c_bs), ("gold", c_sg)))
    labs += lab(1360, surf + 34, K.new("topsoil"), INK, "end")
    extra = "".join(c) + "".join(fx) + f'<g class="lab">{labs}</g>'
    return band_layer(Hs, surf, [("bronze", c_tb), ("silver", c_bs), ("gold", c_sg)], c_gd, extra)


def build(reuse: bool) -> None:
    css = CSS + ".num{font-family:'Hanken Grotesk',sans-serif;font-weight:700;font-size:12.5px;fill:#1C2B22}"
    mf = frame.MEAS_F
    meas = json.loads(mf.read_text(encoding="utf-8")) if (reuse and mf.exists()) else None
    if meas is None:
        probe_html = shell(TITLE, BASE_CSS_FIX + css, "<main>" + page_body({}) + "</main>", 9000, probe=True)
        meas = measure(NAME, probe_html)
        mf.write_text(json.dumps(meas, indent=1), encoding="utf-8")
    H = int(math.ceil(meas["H"]))
    lay_d, _ = draw_drawing(meas)
    layers = {"DRAW": lay_d, "JR": draw_journey(meas),
              "COR": granite(meas["secs"]["correct"][1]), "LOOK": granite(meas["secs"]["look"][1]),
              "FOOT": granite(meas["secs"]["deep"][1])}
    out = shell(TITLE, BASE_CSS_FIX + css, "<main>\n" + page_body(layers) + "\n</main>", H)
    check(out)
    (HERE / f"{NAME}.dc.html").write_text(out, encoding="utf-8")
    (HERE / "static" / f"{NAME}.html").write_text(static(out), encoding="utf-8")
    print(NAME, "H =", H, {k: [round(a), round(b)] for k, (a, b) in meas["secs"].items()}, "over", meas.get("over"))
    (HERE / "gen" / "new-copy.json").write_text(json.dumps(K.NEW, ensure_ascii=False, indent=1), encoding="utf-8")


BASE_CSS_FIX = BASE_CSS.replace(".root{background:#155A6E;", ".root{background:#155A6E;")

if __name__ == "__main__":
    build("--reuse" in sys.argv)
