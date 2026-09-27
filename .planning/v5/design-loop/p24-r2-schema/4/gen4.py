"""Designer 4, "One record, then many": the silver stratum of A's dataset page, per specimen.

One real row is laid out field by field (name, value, dtype, meaning): that record IS the schema. Below it, the
eight sample rows as a DataFrame whose left edge sits on the same spine, carrying only the columns that differ
between rows; the record's row is marked. Values are Polars' own formatting (vals.json, from polars_vals.py).
Strata, contact waves, hatch and the feed cable are copied from A's gen_A.py so the section slots into A's page.
"""
from __future__ import annotations

import html
import json
import math
import re
from pathlib import Path

from content4 import (H2, H3_MANY, H3_ONE, KEY_NOTE, LINEAGE, LINEAGE_LABEL, MANY_NOTE, SPECIMENS)

HERE = Path(__file__).parent
PACK = json.loads((HERE.parent.parent / "pack" / "specimens.json").read_text(encoding="utf-8"))
DATA = {s["id"]: s for s in PACK["specimens"]}
VALS = json.loads((HERE / "vals.json").read_text(encoding="utf-8"))
HEIGHTS_F = HERE / "heights.json"
HEIGHTS = json.loads(HEIGHTS_F.read_text(encoding="utf-8")) if HEIGHTS_F.exists() else {}

INK, DAY = "#1C2B22", "#F6F4EC"
BRONZE, SILVER, GOLD = "#A5713C", "#9FADAB", "#C2A14A"
T_GOLD, T_SILVER, T_BRONZE = "#E9DDAF", "#DCE2DF", "#E2CDB3"
W = 1440
Y0 = 40          # bronze/silver contact
PAD_BOT = 40     # gold sliver under the silver/gold contact
NUMERIC = {"Int32", "Float64"}


def f(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".") if abs(v - round(v)) > 1e-9 else str(int(round(v)))


def smooth(pts: list[tuple[float, float]]) -> str:
    d = f"M{f(pts[0][0])} {f(pts[0][1])}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else pts[i + 1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d


def wy(x: float, y0: float, amp: float, seed: float) -> float:
    return y0 + amp * math.sin(x / 210 + seed) + amp * 0.45 * math.sin(x / 73 + seed * 2.3)


def wave(y0: float, amp: float, seed: float, step: int = 120) -> list[tuple[float, float]]:
    return [(x, wy(x, y0, amp, seed)) for x in range(-40, W + step + 41, step)]


def cable(d: str, core: str) -> str:
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="4.4" stroke-linecap="round" '
            f'stroke-linejoin="round"></path>'
            f'<path d="{d}" fill="none" stroke="{core}" stroke-width="1.5" stroke-linecap="round" '
            f'stroke-linejoin="round"></path>')


PATTERNS = ('<pattern id="p-stip" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="3" r="1" '
            'fill="#8A6F1E"></circle><circle cx="6.5" cy="7.5" r=".8" fill="#8A6F1E"></circle></pattern>'
            '<pattern id="p-diag" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 8 L8 0" '
            'stroke="#5E6E6B" stroke-width=".8"></path></pattern>'
            '<pattern id="p-brick" width="24" height="12" patternUnits="userSpaceOnUse"><path d="M0 11.5 H24 M12 0 '
            'V6 M0 6 H24 M0 6 V12" stroke="#7C5530" stroke-width=".8" fill="none"></path></pattern>')


def stratum_svg(H: int, yb: float) -> str:
    """Bronze sliver, silver band, gold sliver; contact waves as in A (silver seed 2.1, gold seed 4.0)."""
    def band(pts: list[tuple[float, float]], fill: str, pat: str, op: str) -> str:
        d = smooth(pts) + f" L{W + 40} {H + 10} L-40 {H + 10} Z"
        return f'<path d="{d}" fill="{fill}"></path><path d="{d}" fill="url(#{pat})" opacity="{op}"></path>'
    top, bot = wave(Y0, 8, 2.1), wave(yb, 7, 4.0)
    return (f'<svg class="layer" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true"><defs>{PATTERNS}'
            f'</defs><rect x="0" y="0" width="{W}" height="{H}" fill="{T_BRONZE}"></rect>'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#p-brick)" opacity=".15"></rect>'
            + band(top, T_SILVER, "p-diag", ".22") + band(bot, T_GOLD, "p-stip", ".26")
            + f'<path d="{smooth(top)} {smooth(bot)}" stroke="{INK}" stroke-width="1.5" fill="none"></path>'
            f'<text x="1360" y="{Y0 + 34}" text-anchor="end" font-family="Hanken Grotesk" font-style="italic" '
            f'font-size="14" fill="{INK}">silver, typed and validated</text></svg>')


def feed_cable(H: int, yb: float) -> str:
    """A's feed cable passing through: bronze core above the top contact, silver inside, gold below, a splice
    sleeve on each contact, and the silver tap landing where A lands it (1348, contact + 77)."""
    XR = 1404

    def rx(y: float) -> float:
        return XR + 9 * math.sin(y / 95 + .4)
    pts = [(rx(y), float(y)) for y in range(-12, H + 13, 16)]
    c_top, c_bot = wy(XR, Y0, 8, 2.1), wy(XR, yb, 7, 4.0)
    s0 = [p for p in pts if p[1] <= c_top] + [(rx(c_top), c_top)]
    s1 = [(rx(c_top), c_top)] + [p for p in pts if c_top < p[1] < c_bot] + [(rx(c_bot), c_bot)]
    s2 = [(rx(c_bot), c_bot)] + [p for p in pts if p[1] >= c_bot]
    out = [cable(smooth(s0), BRONZE), cable(smooth(s1), SILVER), cable(smooth(s2), GOLD)]
    tx, ty, R = 1348, Y0 + 77, 14
    jy = ty - 22
    jx = rx(jy)
    out.append(cable(f"M{f(jx)} {f(jy)} H{f(tx + R)} Q{f(tx)} {f(jy)} {f(tx)} {f(jy + R)} V{f(ty)}", SILVER))
    for c, fill in ((c_top, SILVER), (c_bot, GOLD)):
        x = rx(c)
        out.append(f'<rect x="{f(x - 7)}" y="{f(c - 17)}" width="14" height="34" rx="7" fill="{fill}" stroke="{INK}" '
                   f'stroke-width="1.6"></rect><path d="M{f(x - 7)} {f(c - 8)} H{f(x + 7)} M{f(x - 7)} {f(c + 8)} '
                   f'H{f(x + 7)}" stroke="{INK}" stroke-width="1" opacity=".5"></path>')
    out.append(f'<circle cx="{f(jx)}" cy="{f(jy)}" r="4.6" fill="{INK}"></circle>')
    out.append(f'<circle cx="{tx}" cy="{ty}" r="6.5" fill="{T_SILVER}" stroke="{INK}" stroke-width="2"></circle>'
               f'<circle cx="{tx}" cy="{ty}" r="2.2" fill="{INK}"></circle>')
    return f'<svg class="layer" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true">{"".join(out)}</svg>'


def cell(v: str, raw: object) -> str:
    return '<span class="nl">null</span>' if raw is None else html.escape(v)


def record(spec: dict) -> str:
    d = DATA[spec["id"]]
    vals = VALS[spec["id"]]
    i = spec["record"]
    raw = d["sample_rows"]["rows"][i]
    idx = {c: n for n, c in enumerate(vals["columns"])}
    rows, lin = [], []
    for c in d["schema"]["columns"]:
        name, dt = c["column"], c["dtype"]
        v = cell(vals["rows"][i][idx[name]], raw.get(name))
        if c["origin"] == "lineage":
            lin.append(f'<div class="f"><dt><code>{name}</code></dt><dd class="v"><code>{v}</code></dd>'
                       f'<dd class="t"><code>{dt}</code></dd><dd class="m">{LINEAGE[name]}</dd></div>')
            continue
        key = name in spec["keys"]
        kq = '<span class="kq" aria-hidden="true"></span><span class="sr"> (identifies a row)</span>' if key else ""
        rows.append(f'<div class="f{" key" if key else ""}"><dt><code>{name}</code>{kq}</dt>'
                    f'<dd class="v"><code>{v}</code></dd><dd class="t"><code>{dt}</code></dd>'
                    f'<dd class="m">{spec["meaning"][name]}</dd></div>')
    return (f'<div class="one"><div class="one-h"><h3 id="one-h">{H3_ONE}</h3><p class="kn">{KEY_NOTE}</p></div>'
            f'<dl class="rec" aria-labelledby="one-h">{"".join(rows)}</dl>'
            f'<p class="lin-l">{LINEAGE_LABEL}</p>'
            f'<dl class="rec lin" aria-label="Lineage columns of the same row">{"".join(lin)}</dl></div>')


def brk(name: str) -> str:
    """One optional break in a long column name, at the underscore nearest its middle."""
    if len(name) < 16:
        return name
    cuts = [i for i, ch in enumerate(name) if ch == "_"]
    i = min(cuts, key=lambda k: abs(k + 1 - len(name) / 2))
    return name[:i + 1] + "<wbr>" + name[i + 1:]


def many(spec: dict) -> str:
    d = DATA[spec["id"]]
    vals = VALS[spec["id"]]
    cols = [c for c in d["schema"]["columns"]]
    raws = d["sample_rows"]["rows"]
    vary = [c for c in cols if c["origin"] != "lineage"
            and len({json.dumps(r.get(c["column"])) for r in raws}) > 1]
    idx = {c: n for n, c in enumerate(vals["columns"])}
    def kind(c: dict) -> str:
        if c["dtype"] in NUMERIC:
            return "n"
        vs = [r.get(c["column"]) for r in raws]
        # codes and ids (no spaces anywhere) read in mono, so "2__AANGE001" keeps both underscores
        return "s c" if c["dtype"] == "String" and all(" " not in v for v in vs if v is not None) else "s"
    th = "".join(f'<th scope="col" class="{kind(c)}">{brk(c["column"])}</th>' for c in vary)
    body = []
    for i, (r, raw) in enumerate(zip(vals["rows"], raws)):
        tds = "".join(f'<td class="{kind(c)}">{cell(r[idx[c["column"]]], raw.get(c["column"]))}'
                      f'</td>' for c in vary)
        me = ' class="me"' if i == spec["record"] else ""
        body.append(f"<tr{me}>{tds}</tr>")
    side = " side" if spec.get("side") else ""
    return (f'<div class="many{side}"><h3 id="many-h">{H3_MANY}</h3>'
            f'<p class="mc" id="many-c">{spec["many_cap"]} {MANY_NOTE}</p>'
            f'<div class="dfs"><div class="dfw"><table class="df" aria-labelledby="many-h" aria-describedby="many-c">'
            f'<thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table></div></div></div>')


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,200..800'
         '&amp;family=Hanken+Grotesk:ital,wght@0,400..700;1,400..600&amp;family=Red+Hat+Mono:wght@400;500'
         '&amp;display=swap" rel="stylesheet">')

CSS = (HERE / "s4.css").read_text(encoding="utf-8")


def board(spec: dict) -> tuple[str, int]:
    hs = HEIGHTS.get(spec["file"], 1200)
    yb = Y0 + hs
    H = int(yb + PAD_BOT)
    section = (f'<section class="st st-silver" aria-labelledby="sv-h" style="height: {hs}px"><div class="inner">'
               f'<div class="head"><h2 id="sv-h">{H2}</h2>'
               f'<p>Relation <code>{spec["relation"]}</code>, typed by <code>{spec["schema_cls"]}</code> in '
               f'<code>{spec["schema_src"]}</code>; transformer version {spec["version"]}.</p></div>'
               f'{record(spec)}{many(spec)}</div></section>')
    body = "\n".join([stratum_svg(H, yb), feed_cable(H, yb), "<main>", section, "</main>"])
    out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{spec["title"]}: schema</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS}
<style>
{CSS}</style>
</helmet>
<div class="root" style="width: {W}px; height: {H}px; overflow: hidden; position: relative">
{body}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{W},"height":{H}}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
"""
    return out, H


def static(dc: str) -> str:
    s = dc.replace('<script src="./support.js"></script>', "")
    s = re.sub(r"</?x-dc>", "", s)
    s = re.sub(r"</?helmet>", "", s)
    s = re.sub(r"<script type=\"text/x-dc\".*?</script>\n", "", s, flags=re.S)
    return s


if __name__ == "__main__":
    (HERE / "static").mkdir(exist_ok=True)
    for spec in SPECIMENS:
        out, H = board(spec)
        body_only = out.split('<script type="text/x-dc"')[0]
        assert "{{" not in body_only and "}}" not in body_only, "template-hole syntax in markup"
        assert "/>" not in re.sub(r"<(meta|link|br)[^>]*>", "", body_only), "self-closing tag"
        assert "—" not in out, "em dash"
        (HERE / f'{spec["file"]}.dc.html').write_text(out, encoding="utf-8")
        (HERE / "static" / f'{spec["file"]}.html').write_text(static(out), encoding="utf-8")
        print(spec["file"], H)
