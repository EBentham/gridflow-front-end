"""Round 3, designer 1, "Clean frame, glossary beneath": the silver stratum of the dataset page.

The rows stand alone as a Polars frame (name over the real dtype over the 8 sample rows, cells from Polars' own
repr), unannotated except for a small square after each key column's name. Columns past the width budget fold
into Polars' `…` column. Beneath sits a two-column guide (name, one line of meaning): the key columns under
"Identifies a row", then the other columns, both in frame order, and the lineage columns folded into one line.
Hovering or focusing a guide entry highlights its column in the frame with CSS `:has()` only (the board format
allows no scripts, and the board reads the same without it).

Run with the gridflow venv's Python (it has Polars). Emits 1-<name>.dc.html + static/1-<name>.html.
"""
from __future__ import annotations

import html
import json
import math
import re
import sys
from datetime import date, datetime
from pathlib import Path

import polars as pl

HERE = Path(__file__).parent
PACK = json.loads((HERE.parent.parent / "pack" / "specimens.json").read_text(encoding="utf-8"))
DATA = {s["id"]: s for s in PACK["specimens"]}
HEIGHTS_F = HERE / "heights.json"
HEIGHTS = json.loads(HEIGHTS_F.read_text(encoding="utf-8")) if HEIGHTS_F.exists() else {}

INK = "#1C2B22"
BRONZE, SILVER, GOLD = "#A5713C", "#9FADAB", "#C2A14A"
T_GOLD, T_SILVER, T_BRONZE = "#E9DDAF", "#DCE2DF", "#E2CDB3"
TOP = 58          # y of the bronze/silver contact on the board
TAIL = 58         # gold shown below the silver/gold contact
CH = 7.8          # Red Hat Mono advance at 13 px, measured
PAD = 16          # cell padding, left + right (Polars' one space either side)
KEY_W = 14        # the key square and its gap
EL_W = 30         # Polars' elision column
BUDGET = 1280     # the frame never outgrows the content column at 1440


SPECS = [
    {
        "file": "fuelhh", "id": "elexon/fuelhh", "title": "Generation by fuel type: schema",
        "relation": "silver_elexon_fuelhh", "cls": "ElexonFuelHH", "src": "gridflow/schemas/elexon.py",
        "version": "2.0.0",
        "keys": ["settlement_date", "settlement_period", "fuel_type"],
        "lineage": ["event_time", "available_at", "source_run_id", "dataset_version"],
        "caption": "Settlement date 2026-09-26, period 25: eight of that half-hour’s fuel-type codes.",
        "meanings": {
            "settlement_date": "GB settlement date, recomputed from the vendor start time",
            "settlement_period": "Half-hour of the day, 1 to 48; 46 or 50 on clock-change days",
            "timestamp_utc": "Start of the half-hour, from the vendor start time",
            "fuel_type": "Elexon fuel-type code, uppercase as sent",
            "generation_mw": "MW for the period; interconnectors (positive is import) and PS are signed",
            "published_at": "Vendor publish time",
            "data_provider": "Same on every row: <code>elexon</code>",
            "ingested_at": "When the silver transform ran",
        },
    },
    {
        "file": "system-prices", "id": "elexon/system_prices", "title": "System sell and buy prices: schema",
        "relation": "silver_elexon_system_prices", "cls": "ElexonSystemPrice",
        "src": "gridflow/schemas/elexon.py", "version": "2.0.0",
        "keys": ["settlement_date", "settlement_period", "published_at"],
        "lineage": ["event_time", "available_at", "source_run_id", "dataset_version", "vintage_policy"],
        "caption": "Settlement date 2026-09-20, periods 22 to 29: one published version of each.",
        "meanings": {
            "settlement_date": "GB settlement date, as Elexon labels it",
            "settlement_period": "Half-hour of the day, 1 to 48; 46 or 50 on clock-change days",
            "timestamp_utc": "Start of the half-hour, computed from settlement date and period",
            "system_sell_price": "System sell price (SSP), £/MWh, as sent",
            "system_buy_price": "System buy price (SBP), £/MWh, from its own API field",
            "net_imbalance_volume": "Net imbalance, MWh; positive means the system was short, negative long",
            "run_type": "Settlement run; null, because this endpoint sends no run field",
            "price_derivation_code": "Elexon’s code for how the price was derived, as sent",
            "published_at": "Vendor record time; each new version adds a row",
            "data_provider": "Same on every row: <code>elexon</code>",
            "ingested_at": "When the silver transform ran",
        },
    },
    {
        "file": "physical-flows", "id": "entsog/physical_flows", "title": "Physical gas flows: schema",
        "relation": "silver_entsog_physical_flows", "cls": "EntsogPhysicalFlow", "src": "gridflow/schemas/entsog.py",
        "version": "1.0.0",
        "keys": ["timestamp_utc", "point_key", "operator_key", "direction_key"],
        "lineage": ["event_time", "available_at", "source_run_id", "dataset_version"],
        "caption": "Gas day 2026-09-21 at GB points.",
        "meanings": {
            "timestamp_utc": "Start of the operator’s gas day, in UTC",
            "point_key": "ENTSOG point ID",
            "point_label": "Point name",
            "operator_key": "Reporting operator ID; both sides of a point report, so flows repeat",
            "operator_label": "Operator name",
            "direction_key": "<code>entry</code> or <code>exit</code>",
            "flow_gwh_per_day": "Flow in GWh/d, normalised from the vendor unit; can be null",
            "unit": "Same on every row: <code>GWh/d</code>",
            "data_provider": "Same on every row: <code>entsog</code>",
            "ingested_at": "When the silver transform ran",
        },
    },
    {
        "file": "bmunits-reference", "id": "elexon/bmunits_reference", "title": "Balancing Mechanism units: schema",
        "relation": "silver_elexon_bmunits_reference", "cls": "ElexonBMUnit", "src": "gridflow/schemas/elexon.py",
        "version": "1.1.0",
        "keys": ["bm_unit_id"],
        "lineage": ["event_time", "available_at", "source_run_id", "dataset_version"],
        "caption": "Eight units from the register, chosen across ID prefixes.",
        "meanings": {
            "bm_unit_id": "Elexon BM unit ID (<code>elexonBmUnit</code>); rows without one are dropped",
            "bm_unit_name": "The unit’s name as Elexon sends it",
            "fuel_type": "Elexon fuel-type code; null when Elexon sends none",
            "registered_capacity_mw": "MW for one registration; not additive across rows",
            "company_name": "Lead party name",
            "gsp_group_id": "Grid supply point group; may be null",
            "national_grid_bm_unit": "National Grid’s ID for the unit; not the EIC",
            "data_provider": "Same on every row: <code>elexon</code>",
            "ingested_at": "When the silver transform ran; the same on every row",
        },
    },
]


# ================================================================ Polars: the frame exactly as Polars prints it
PL_TYPES = {"Date": pl.Date, "Int32": pl.Int32, "String": pl.String, "Float64": pl.Float64}


def polars_frame(spec_id: str) -> tuple[tuple[int, int], list[str], list[str], list[list[str]]]:
    """Build the sample DataFrame with the silver dtypes and parse Polars' own repr into cells."""
    s = DATA[spec_id]
    schema = {c["column"]: PL_TYPES.get(c["dtype"], pl.Datetime("us", "UTC")) for c in s["schema"]["columns"]}
    rows = []
    for r in s["sample_rows"]["rows"]:
        o = {}
        for k, dt in schema.items():
            v = r.get(k)
            if v is not None and dt == pl.Date:
                v = date.fromisoformat(v)
            elif v is not None and isinstance(dt, pl.Datetime):
                v = datetime.fromisoformat(v)
            o[k] = v
        rows.append(o)
    df = pl.DataFrame(rows, schema=schema, orient="row")
    with pl.Config(tbl_cols=-1, tbl_rows=-1, tbl_width_chars=4000, fmt_str_lengths=200):
        text = repr(df)
    body = [ln for ln in text.splitlines() if ln.startswith("│")]

    def cells(line: str) -> list[str]:
        return [c.strip() for c in line.strip().strip("│").split("┆")]

    names, dtypes = cells(body[0]), cells(body[2])
    data = [cells(ln) for ln in body[3:]]
    assert names == list(schema), (names, list(schema))
    assert len(data) == 8
    return df.shape, names, dtypes, data


# ================================================================ drawing (strata pieces from A's generator)
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


def wave_y(x: float, y0: float, amp: float, seed: float) -> float:
    return y0 + amp * math.sin(x / 210 + seed) + amp * 0.45 * math.sin(x / 73 + seed * 2.3)


def wave(W: int, y0: float, amp: float, seed: float, step: int = 60) -> list[tuple[float, float]]:
    return [(x, wave_y(x, y0, amp, seed)) for x in range(-40, W + step + 41, step)]


def cable(d: str, core: str) -> str:
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="4.4" stroke-linecap="round" '
            f'stroke-linejoin="round"></path>'
            f'<path d="{d}" fill="none" stroke="{core}" stroke-width="1.5" stroke-linecap="round" '
            f'stroke-linejoin="round"></path>')


PATTERNS = """<pattern id="p-stip" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="3" r="1" fill="#8A6F1E"></circle><circle cx="6.5" cy="7.5" r=".8" fill="#8A6F1E"></circle></pattern>
<pattern id="p-diag" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 8 L8 0" stroke="#5E6E6B" stroke-width=".8"></path></pattern>
<pattern id="p-brick" width="24" height="12" patternUnits="userSpaceOnUse"><path d="M0 11.5 H24 M12 0 V6 M0 6 H24 M0 6 V12" stroke="#7C5530" stroke-width=".8" fill="none"></path></pattern>"""


def strata_svg(W: int, y_bs: float, y_sg: float, H: int, label_x: int) -> str:
    """Bronze above, silver between the two contacts, gold below; A's seeds, amplitudes and hatches."""
    def band(pts: list[tuple[float, float]], fill: str, pat: str, op: str) -> str:
        d = smooth(pts) + f" L{W + 40} {H + 10} L-40 {H + 10} Z"
        return f'<path d="{d}" fill="{fill}"></path><path d="{d}" fill="url(#{pat})" opacity="{op}"></path>'

    bs, sg = wave(W, y_bs, 8, 2.1), wave(W, y_sg, 7, 4.0)
    return (f'<svg class="layer" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true"><defs>{PATTERNS}'
            '</defs>'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="{T_BRONZE}"></rect>'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#p-brick)" opacity=".15"></rect>'
            + band(bs, T_SILVER, "p-diag", ".22") + band(sg, T_GOLD, "p-stip", ".26")
            + f'<path d="{smooth(bs)} {smooth(sg)}" stroke="{INK}" stroke-width="1.5" fill="none"></path>'
            f'<text class="sl" x="{label_x}" y="{f(y_bs + 34)}" text-anchor="end" font-family="Hanken Grotesk" '
            f'font-style="italic" font-size="14" fill="{INK}">silver, typed and validated</text>'
            '</svg>')


def feed_cable(W: int, y_bs: float, y_sg: float, H: int) -> str:
    """A's feed riser in the right margin, with the silver tap landing at (1348, contact + 77) as in A."""
    XR = 1404

    def rx(y: float) -> float:
        return XR + 9 * math.sin(y / 95 + .4)

    c_bs, c_sg = wave_y(XR, y_bs, 8, 2.1), wave_y(XR, y_sg, 7, 4.0)
    ys = list(range(-12, H + 13, 16))

    def seg(a: float, b: float) -> list[tuple[float, float]]:
        return [(rx(a), a)] + [(rx(y), y) for y in ys if a < y < b] + [(rx(b), b)]

    out = [cable(smooth(seg(-12, c_bs)), BRONZE), cable(smooth(seg(c_bs, c_sg)), SILVER),
           cable(smooth(seg(c_sg, H + 12)), GOLD)]
    tx, ty, R = 1348, y_bs + 77, 14
    jy = ty - 22
    jx = rx(jy)
    out.append(cable(f"M{f(jx)} {f(jy)} H{f(tx + R)} Q{f(tx)} {f(jy)} {f(tx)} {f(jy + R)} V{f(ty)}", SILVER))
    for c, fill in ((c_bs, SILVER), (c_sg, GOLD)):
        x = rx(c)
        out.append(f'<rect x="{f(x - 7)}" y="{f(c - 17)}" width="14" height="34" rx="7" fill="{fill}" stroke="{INK}" '
                   f'stroke-width="1.6"></rect><path d="M{f(x - 7)} {f(c - 8)} H{f(x + 7)} M{f(x - 7)} {f(c + 8)} '
                   f'H{f(x + 7)}" stroke="{INK}" stroke-width="1" opacity=".5"></path>')
    out.append(f'<circle cx="{f(jx)}" cy="{f(jy)}" r="4.6" fill="{INK}"></circle>')
    out.append(f'<circle cx="{tx}" cy="{f(ty)}" r="6.5" fill="{T_SILVER}" stroke="{INK}" stroke-width="2"></circle>'
               f'<circle cx="{tx}" cy="{f(ty)}" r="2.2" fill="{INK}"></circle>')
    return f'<svg class="layer" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true">{"".join(out)}</svg>'


# ================================================================ the section
NUM = {"i32", "f64"}


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def slug(spec: dict, name: str) -> str:
    return f"c-{spec['file']}-{name}"


def section(spec: dict) -> tuple[str, str, dict]:
    """Return the section markup, its highlight and toggle CSS, and the frame geometry.

    Every column is in the markup. Columns past the width budget carry class `fc` and stay hidden until the
    reader checks the `…` toggle (a visually hidden checkbox whose labels fill the `…` column), which sits last.
    """
    shape, names, dtypes, data = polars_frame(spec["id"])
    lin = spec["lineage"]
    assert names[-len(lin):] == lin, (names, lin)
    schema_cols = names[:-len(lin)]
    pipeline = set(lin) | {"data_provider", "ingested_at"}   # stamped on every dataset's rows; no guide line

    def width(i: int) -> int:
        n = names[i]
        chars = max(len(n), *(len(r[i]) for r in data))
        w = math.ceil(max(chars * CH, len(dtypes[i]) * CH)) + PAD + 1
        if n in spec["keys"]:
            w = max(w, math.ceil(len(n) * CH) + KEY_W + PAD + 1)
        return w

    cut = schema_cols.index("ingested_at")
    while sum(width(i) for i in range(cut)) + EL_W + 3 > BUDGET:
        cut -= 1
    shown, folded = names[:cut], names[cut:]
    expanded_w = sum(width(i) for i in range(len(names))) + EL_W + 3
    tog_k = len(names) + 1          # nth-child index of the `…` column, always last
    fid = spec["file"]
    fx = f"fx-{fid}"
    n_f = len(folded)

    def cls(i: int, extra: str = "") -> str:
        c = " ".join(x for x in (extra, "fc" if i >= cut else "") if x)
        return f' class="{c}"' if c else ""

    nm = []
    for i, n in enumerate(names):
        key = ('<span class="k" aria-hidden="true"></span><span class="sr"> (identifies a row)</span>'
               if n in spec["keys"] else "")
        nm.append(f'<th scope="col"{cls(i)} id="{slug(spec, n)}">{n}{key}</th>')
    nm.append(f'<th scope="col" class="el" id="{slug(spec, "more")}">'
              f'<input type="checkbox" class="fx sr" id="{fx}">'
              f'<label for="{fx}"><span aria-hidden="true">…</span>'
              f'<span class="sr">Show {n_f} more columns</span></label></th>')
    dt = "".join(f"<td{cls(i)}>{esc(dtypes[i])}</td>" for i in range(len(names)))
    dt += f'<td class="el"><label for="{fx}" aria-hidden="true"></label></td>'
    body = []
    for r in data:
        tds = []
        for i in range(len(names)):
            v = r[i]
            c = cls(i, "num" if dtypes[i] in NUM else "")
            tds.append(f'<td{c}><span class="nl">null</span></td>' if v == "null" else f"<td{c}>{esc(v)}</td>")
        body.append("<tr>" + "".join(tds) + f'<td class="el"><label for="{fx}" aria-hidden="true">…</label></td></tr>')
    aria = f"Sample rows from {spec['relation']}: {shape[0]} rows of {shape[1]} columns, the last {n_f} folded."
    frame = (f'<div class="fw" role="region" tabindex="0" aria-label="{html.escape(aria)}">'
             f'<table class="pl"><thead><tr class="nm">{"".join(nm)}</tr><tr class="dt">{dt}</tr></thead>'
             f'<tbody>{"".join(body)}</tbody></table></div>')

    # the guide: key columns, then the rest, each in frame order; pipeline columns need no line
    def entry(n: str) -> str:
        f_attr = ' data-f=""' if n in folded else ""
        return (f'<div class="g-r" data-k="{names.index(n) + 1}"{f_attr}><dt><a href="#{slug(spec, n)}">{n}</a>'
                f'</dt><dd>{spec["meanings"][n]}</dd></div>')

    keyed = [n for n in schema_cols if n in spec["keys"]]
    others = [n for n in schema_cols if n not in spec["keys"] and n not in pipeline]
    guide = (f'<div class="guide" role="group" aria-label="Column guide">'
             f'<div class="g-grp g-key"><p class="g-h" id="gk-{fid}"><span class="k" aria-hidden="true"></span>'
             f'Identifies a row</p><dl aria-labelledby="gk-{fid}">{"".join(entry(n) for n in keyed)}</dl></div>'
             f'<div class="g-grp"><p class="g-h" id="go-{fid}">Other columns</p>'
             f'<dl aria-labelledby="go-{fid}">{"".join(entry(n) for n in others)}</dl></div>'
             f'</div>')

    cap = (f'<p class="cap"><code class="shape">shape: ({shape[0]}, {shape[1]})</code> '
           f'<span>{spec["caption"]}</span></p>')
    html_s = (f'<h2 id="sv-h">Schema and sample rows</h2>'
              f'<div class="spec">{cap}{frame}{guide}</div>')

    # a guide entry lights its column; a folded one lights `…` until the frame is unfolded
    hl = []
    for k in range(1, len(names) + 1):
        hl.append(f'.spec:has([data-k="{k}"]:is(:hover,:focus-within)) .pl tr > :nth-child({k}),'
                  f'.spec:has(.pl th:nth-child({k}):target) .pl tr > :nth-child({k})'
                  '{background:var(--lit)}')
    hl.append('.spec:not(:has(.fx:checked)):has([data-f]:is(:hover,:focus-within)) .pl .el,'
              '.pl:has(.el label:hover) .el{background:var(--lit)}')
    geo = {"shown": shown, "folded": folded, "expanded_w": expanded_w}
    return html_s, "\n".join(hl), geo

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,200..800'
         '&amp;family=Hanken+Grotesk:ital,wght@0,400..700;1,400..600&amp;family=Red+Hat+Mono:wght@400;500'
         '&amp;display=swap" rel="stylesheet">')
CSS = (HERE / "s1.css").read_text(encoding="utf-8")


def page(spec: dict, W: int) -> tuple[str, int, dict]:
    phone = W < 700
    name = f"1-{spec['file']}" + ("-390" if phone else "")
    hs = HEIGHTS.get(name, 1000)
    y_bs, y_sg = TOP, TOP + hs
    H = y_sg + TAIL
    inner, hl, geo = section(spec)
    sec = (f'<section class="st" aria-labelledby="sv-h" style="height: {hs}px"><div class="inner">'
           f'{inner}</div></section>')
    layers = [strata_svg(W, y_bs, y_sg, H, W - 16 if phone else 1360)]
    if not phone:
        layers.append(feed_cable(W, y_bs, y_sg, H))
    body = "\n".join(layers + [f'<main style="padding-top: {TOP}px">', sec, "</main>"])
    out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{spec["title"]}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS}
<style>
{CSS}
{hl}
</style>
</helmet>
<div class="root{' ph' if phone else ''}" style="width: {W}px; height: {H}px; overflow: hidden; position: relative">
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
    return out, H, geo


def static(dc: str) -> str:
    s = dc.replace('<script src="./support.js"></script>', "")
    s = re.sub(r"</?x-dc>", "", s)
    s = re.sub(r"</?helmet>", "", s)
    s = re.sub(r"<script type=\"text/x-dc\".*?</script>\n", "", s, flags=re.S)
    return s


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    (HERE / "static").mkdir(exist_ok=True)
    geos = {}
    boards = [(s, 1440) for s in SPECS] + [(SPECS[0], 390)]
    for spec, W in boards:
        out, H, geo = page(spec, W)
        name = f"1-{spec['file']}" + ("-390" if W < 700 else "")
        body_only = out.split('<script type="text/x-dc"')[0]
        assert "{{" not in body_only and "}}" not in body_only, "template-hole syntax in markup"
        assert "/>" not in re.sub(r"<(meta|link|br|col)[^>]*>", "", body_only), "self-closing tag"
        assert "—" not in body_only, "em dash"
        (HERE / f"{name}.dc.html").write_text(out, encoding="utf-8")
        (HERE / "static" / f"{name}.html").write_text(static(out), encoding="utf-8")
        geos[name] = geo
        print(name, "H =", H, "expanded_w =", geo["expanded_w"], "shown =", len(geo["shown"]), "folded =", len(geo["folded"]))
    (HERE / "geo.json").write_text(json.dumps(geos, indent=1, ensure_ascii=False), encoding="utf-8")
