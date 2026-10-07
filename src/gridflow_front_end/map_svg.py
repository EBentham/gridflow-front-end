"""Draw a weather dataset's site map and its table at build time.

The map is a static inline SVG: the UK and Ireland outline (``site/hifi/data/geo/gb-ie.json``,
Natural Earth 1:50m) and one marker per configured site, read from the committed site file
(``locations``). Each marker is a link to its row in the table beneath, so the map works with no
script; ``site.js`` adds the card that opens on hover, focus or tap.

Projection: equirectangular with true scale at 55°N (x = longitude × cos 55°, y = latitude), which
keeps Great Britain's shape within a few per cent across the frame. The frame runs 49.75°N to
59.5°N: Shetland lies north of it, and no site is there.

Stdlib only, like ``chart_svg``: CI builds from a bare checkout.
"""

from __future__ import annotations

import datetime as dt
import html
import json
import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from gridflow_front_end.chart_svg import MONTHS, PAINT_TOKEN, colour, paint_of
from gridflow_front_end.page_fields import KeyEntry
from gridflow_front_end.paths import SITE_DIR

OUTLINE = SITE_DIR / "data" / "geo" / "gb-ie.json"
LAT_TRUE = 55.0
LON_MIN, LAT_MIN, LON_MAX, LAT_MAX = -10.75, 49.75, 3.05, 59.5
WIDTH = 500
_K = math.cos(math.radians(LAT_TRUE))
_S = WIDTH / ((LON_MAX - LON_MIN) * _K)
HEIGHT = round((LAT_MAX - LAT_MIN) * _S)

MONTH_NAMES = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)  # fmt: skip
STAT_KEYS = {
    "demand": ("mean_temp_c", "coldest_c", "coldest_at", "hdd_per_year"),
    "wind": ("mean_100m_mps", "p90_100m_mps"),
    "solar": (
        "mean_daily_kwh_m2",
        "sunniest_month",
        "sunniest_kwh_m2",
        "darkest_month",
        "darkest_kwh_m2",
    ),
}
_LABEL_CH = 7.0  # Hanken italic at 13.5 px, per character of a capitalised name
_DOT_R = 5.5
# 18 units is a 24 px tap target where the drawing is narrowest (343 px at a 390 px viewport); the
# closest two sites on any map are 32 units apart, so a hit circle never covers a neighbour's dot.
HIT_R = 18
_WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}


def project(lon: float, lat: float) -> tuple[float, float]:
    """Map units (``WIDTH`` across) for a longitude and latitude."""
    return (lon - LON_MIN) * _K * _S, (LAT_MAX - lat) * _S


def _f(v: float) -> str:
    s = f"{v:.1f}"
    s = s.removesuffix(".0")
    if s.startswith("0."):
        s = s[1:]
    elif s.startswith("-0."):
        s = "-" + s[2:]
    return "0" if s in ("", "-0", "-") else s


def _relative(points: Sequence[tuple[float, float]], close: bool) -> str:
    """One run as ``M x y l dx dy ...``, deltas taken between rounded points so nothing drifts."""
    pts = [(round(x, 1), round(y, 1)) for x, y in points]
    nums: list[str] = []
    prev = pts[0]
    for p in pts[1:]:
        dx, dy = round(p[0] - prev[0], 1), round(p[1] - prev[1], 1)
        if dx or dy:
            nums.extend((_f(dx), _f(dy)))
            prev = p
    # a minus sign separates two numbers on its own, so the space before it is dropped
    body = "".join(n if i == 0 or n.startswith("-") else " " + n for i, n in enumerate(nums))
    return f"M{_f(pts[0][0])} {_f(pts[0][1])}l{body}" + ("z" if close else "")


def outline_paths() -> tuple[str, str]:
    """The land (filled, inked coast) and the land border, as path data."""
    data = json.loads(OUTLINE.read_text(encoding="utf-8"))
    land = [
        _relative([project(lon, lat) for lon, lat in ring], close=True)
        for ring in data["land"]
        if any(lat <= LAT_MAX for _lon, lat in ring)
    ]
    border = [
        _relative([project(lon, lat) for lon, lat in run], close=False) for run in data["border"]
    ]
    return "".join(land), "".join(border)


def land_rings() -> list[list[tuple[float, float]]]:
    """The outline's land rings in lon/lat, for tests that ask whether a point is on land."""
    data = json.loads(OUTLINE.read_text(encoding="utf-8"))
    return [[(lon, lat) for lon, lat in ring] for ring in data["land"]]


def on_land(lon: float, lat: float, rings: list[list[tuple[float, float]]]) -> bool:
    """Even-odd point in polygon over every land ring."""
    inside = False
    for ring in rings:
        for (x1, y1), (x2, y2) in zip(ring, ring[1:]):
            if (y1 > lat) != (y2 > lat) and lon < x1 + (lat - y1) * (x2 - x1) / (y2 - y1):
                inside = not inside
    return inside


@dataclass(frozen=True)
class _Box:
    x0: float
    y0: float
    x1: float
    y1: float

    def hits(self, o: _Box) -> bool:
        return self.x0 < o.x1 and o.x0 < self.x1 and self.y0 < o.y1 and o.y0 < self.y1


# Display names. gridflow's code holds only slugs, so the names live here. A wind farm takes its
# operator's own spelling (RWE's Gwynt y Môr, Vattenfall's Pen y Cymoedd, Fred. Olsen Renewables'
# Crystal Rig; the other farm slugs already are the farms' names), a city its name, and a site that
# is a regional centre rather than one farm (the solar sites, the central Highland wind site) its region.
SITE_NAMES = {
    "london": "London",
    "birmingham": "Birmingham",
    "manchester": "Manchester",
    "leeds": "Leeds",
    "glasgow": "Glasgow",
    "cardiff": "Cardiff",
    "belfast": "Belfast",
    "dogger_bank": "Dogger Bank",
    "hornsea": "Hornsea",
    "east_anglia": "East Anglia",
    "triton_knoll": "Triton Knoll",
    "walney": "Walney",
    "gwynt_y_mor": "Gwynt y Môr",
    "beatrice": "Beatrice",
    "seagreen": "Seagreen",
    "highland_central": "Central Highlands",
    "borders_crystalrig": "Crystal Rig",
    "whitelee": "Whitelee",
    "pen_y_cymoedd": "Pen y Cymoedd",
    "east_anglia_norfolk": "Norfolk",
    "wiltshire_somerset": "Wiltshire and Somerset",
    "kent": "Kent",
    "cornwall": "Cornwall",
    "sussex": "Sussex",
    "oxfordshire": "Oxfordshire",
}
_NOUNS = {"demand": "cities", "wind": "wind-farm sites", "solar": "solar sites"}


def label_text(name: str) -> str:
    """A site's display name (``SITE_NAMES``); ``check`` fails a site that has none."""
    return SITE_NAMES.get(name, name)


def accessible_name(data: dict[str, Any]) -> str:
    """The map's accessible name, in words: no dataset code."""
    n = len(data["sites"])
    return (
        f"Map of the UK and Ireland with the {n} {_NOUNS[data['kind']]} where the weather is "
        "taken; each links to its row in the table."
    )


def place_labels(sites: Sequence[tuple[str, float, float]]) -> dict[str, tuple[float, float, str]]:
    """Put each label beside its marker where it overlaps no other label or marker.

    Returns ``{name: (x, y, anchor)}``; a site with no free place gets no label (its card and table
    row still name it). Crowded sites choose first.
    """
    marks = {n: _Box(x - 8, y - 8, x + 8, y + 8) for n, x, y in sites}

    def crowd(s: tuple[str, float, float]) -> tuple[int, str]:
        near = sum(1 for _n, x, y in sites if 0 < math.hypot(x - s[1], y - s[2]) < 70)
        return (-near, s[0])

    placed: dict[str, tuple[float, float, str]] = {}
    boxes: list[_Box] = []
    for name, x, y in sorted(sites, key=crowd):
        w = len(label_text(name)) * _LABEL_CH
        candidates = [
            (x + 10, y + 4.5, "start"),
            (x - 10, y + 4.5, "end"),
            (x + 8, y - 9, "start"),
            (x + 8, y + 17, "start"),
            (x - 8, y - 9, "end"),
            (x - 8, y + 17, "end"),
            (x, y - 12, "middle"),
            (x, y + 21, "middle"),
        ]
        for lx, ly, anchor in candidates:
            left = {"start": lx, "end": lx - w, "middle": lx - w / 2}[anchor]
            box = _Box(left - 2, ly - 11, left + w + 2, ly + 3)
            if box.x0 < 2 or box.x1 > WIDTH - 2 or box.y0 < 2 or box.y1 > HEIGHT - 2:
                continue
            if any(box.hits(b) for b in boxes) or any(
                box.hits(m) for n, m in marks.items() if n != name
            ):
                continue
            placed[name] = (lx, ly, anchor)
            boxes.append(box)
            break
    return placed


def _num(v: float, places: int) -> str:
    return f"{v:,.{places}f}".replace("-", "−")


def _coords(lat: float | str, lon: float | str, places: int | None = None) -> str:
    if places is None:
        return f"{lat}, {lon}"
    return f"{float(lat):.{places}f}, {float(lon):.{places}f}"


def _when(stamp: str) -> str:
    t = dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%MZ")
    return f"{t:%H:%M} UTC, {t.day} {MONTHS[t.month - 1]} {t.year}"


def _columns(kind: str) -> list[dict[str, Any]]:
    """The table's headers, units included; ``num`` columns hold numbers and align right."""
    stats = {
        "demand": [
            ("Mean at 2 m, °C", True),
            ("Coldest hour, °C", True),
            ("Degree-days a year", True),
        ],
        "wind": [("Mean wind at 100 m, m/s", True), ("90th percentile, m/s", True)],
        "solar": [
            ("Mean day, kWh/m²", True),
            ("Sunniest month, kWh/m²", False),
            ("Darkest month, kWh/m²", False),
        ],
    }[kind]
    head = [("Site", False), ("Requested", False), ("Answered", False), ("Apart", True)]
    return [{"text": text, "num": num} for text, num in head + stats]


def _cells(kind: str, st: dict[str, Any]) -> list[dict[str, Any]]:
    """A row's statistic cells: ``text``, an optional second line ``sub``, and ``num`` to align right."""
    if kind == "demand":
        cells = [
            (_num(st["mean_temp_c"], 1), "", True),
            (_num(st["coldest_c"], 1), f"at {_when(st['coldest_at'])}", True),
            (_num(st["hdd_per_year"], 0), "", True),
        ]
    elif kind == "wind":
        cells = [
            (_num(st["mean_100m_mps"], 1), "", True),
            (_num(st["p90_100m_mps"], 1), "", True),
        ]
    else:
        cells = [
            (_num(st["mean_daily_kwh_m2"], 2), "", True),
            (
                MONTH_NAMES[st["sunniest_month"] - 1],
                f"{_num(st['sunniest_kwh_m2'], 2)} a day",
                False,
            ),
            (MONTH_NAMES[st["darkest_month"] - 1], f"{_num(st['darkest_kwh_m2'], 2)} a day", False),
        ]
    return [{"text": text, "sub": sub, "num": num} for text, sub, num in cells]


def _years(window: dict[str, Any]) -> tuple[int, int]:
    return int(window["start"][:4]), int(window["end"][:4])


def notes(data: dict[str, Any]) -> list[str]:
    """How every column was made, scoped to its window (inline markdown)."""
    first, last = _years(data["window"])
    n = last - first + 1
    silver_ds = data["silver"].split("/", 1)[1]
    out = [
        "Requested: the point gridflow sends (`endpoints.py`), a dot on the map. Answered: the "
        "archive grid point Open-Meteo returned, a small square. Apart: the great-circle distance.",
        f"Statistics: silver `{silver_ds}` at the answered point, every hour of {first} to {last}, UTC.",
    ]
    if data["kind"] == "demand":
        base = _num(data["hdd_base_c"], 1)
        out.append(
            f"Heating degree-days: each hour's degrees below {base} °C (gridflow's base, a project choice), "
            f"summed, divided by 24 and by the {_WORDS.get(n, str(n))} years."
        )
    elif data["kind"] == "wind":
        out.append("90th percentile: one hour in ten blows harder.")
    else:
        out.append(
            "A day's irradiation: the vendor's hourly global horizontal means, each over the hour "
            "ending at its stamp, summed over the day the hour began. A month: its mean day."
        )
    return out


def check(data: dict[str, Any], key: str) -> list[str]:
    """What the build can verify of a committed site file without silver or gridflow."""
    errors: list[str] = []
    if data.get("dataset") != key:
        errors.append(f"{key}: locations file names {data.get('dataset')!r}")
    kind = data.get("kind")
    if kind not in STAT_KEYS:
        return [*errors, f"{key}: locations kind {kind!r} is not one of {sorted(STAT_KEYS)}"]
    window = data.get("window") or {}
    if not window.get("start") or not window.get("end"):
        errors.append(f"{key}: locations file has no window")
    if kind == "demand" and not isinstance(data.get("hdd_base_c"), (int, float)):
        errors.append(f"{key}: locations file has no hdd_base_c")
    sites = data.get("sites") or []
    if not sites:
        errors.append(f"{key}: locations file has no sites")
    names = [s.get("name") for s in sites]
    if len(set(names)) != len(names):
        errors.append(f"{key}: locations file lists a site twice")
    for s in sites:
        where = f"{key}: site {s.get('name')!r}"
        if s.get("name") not in SITE_NAMES:
            errors.append(f"{where}: no display name; add it to map_svg.SITE_NAMES")
        try:
            lat, lon = float(s["configured"]["lat"]), float(s["configured"]["lon"])
            alat, alon = float(s["answered"]["lat"]), float(s["answered"]["lon"])
            float(s["offset_km"])
        except (KeyError, TypeError, ValueError):
            errors.append(f"{where}: needs configured and answered lat/lon and offset_km")
            continue
        for la, lo in ((lat, lon), (alat, alon)):
            if not (LAT_MIN <= la <= LAT_MAX and LON_MIN <= lo <= LON_MAX):
                errors.append(f"{where}: {la}, {lo} is outside the map")
        missing = [k for k in STAT_KEYS[kind] if (s.get("stats") or {}).get(k) is None]
        if missing:
            errors.append(f"{where}: no {missing}")
    return errors


def render(data: dict[str, Any], key_entries: Sequence[KeyEntry]) -> dict[str, Any]:
    """The map's SVG and its table rows.

    Args:
        data: A committed site file that ``check`` passes.
        key_entries: The page's chart key; a site the chart draws keeps its paint on the map.
    """
    label = accessible_name(data)
    kind = data["kind"]
    paints = {e.series: paint_of(e) for e in key_entries}
    ink, daylight = colour("ink"), colour("daylight")
    land, border = outline_paths()
    sites = data["sites"]
    pos = {
        s["name"]: project(float(s["configured"]["lon"]), float(s["configured"]["lat"]))
        for s in sites
    }
    labels = place_labels([(n, x, y) for n, (x, y) in pos.items()])

    under: list[str] = []
    marks: list[str] = []
    for s in sites:
        name = s["name"]
        x, y = pos[name]
        ax, ay = project(float(s["answered"]["lon"]), float(s["answered"]["lat"]))
        under.append(
            f'<g class="wm-a" data-site="{name}"><path d="M{_f(x)} {_f(y)}L{_f(ax)} {_f(ay)}"/>'
            f'<rect x="{_f(ax - 2.5)}" y="{_f(ay - 2.5)}" width="5" height="5"/></g>'
        )
        paint = paints.get(name)
        fill = colour(PAINT_TOKEN[paint][2:]) if paint in PAINT_TOKEN else daylight
        marks.append(
            f'<a class="wm-s" href="#site-{name}" data-site="{name}" aria-label="{html.escape(label_text(name))}" '
            f'aria-describedby="site-{name}" tabindex="0">'
            f'<circle class="wm-halo" cx="{_f(x)}" cy="{_f(y)}" r="10.5"/>'
            f'<circle class="wm-dot" cx="{_f(x)}" cy="{_f(y)}" r="{_DOT_R}" fill="{fill}" stroke="{ink}" stroke-width="1.5"/>'
            f'<circle class="wm-hit" cx="{_f(x)}" cy="{_f(y)}" r="{HIT_R}"/></a>'
        )
    texts = [
        f'<text x="{_f(lx)}" y="{_f(ly)}" text-anchor="{anchor}" data-site="{name}">{html.escape(label_text(name))}</text>'
        for name, (lx, ly, anchor) in sorted(labels.items(), key=lambda kv: list(pos).index(kv[0]))
    ]
    svg = (
        f'<svg class="wm-svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}" '
        f'role="group" aria-label="{html.escape(label, quote=True)}">'
        f'<path class="wm-land" d="{land}" fill="{daylight}" stroke="{ink}" stroke-width="1.1" '
        f'stroke-linejoin="round" aria-hidden="true"/>'
        f'<g aria-hidden="true"><path d="{border}" fill="none" stroke="{daylight}" stroke-width="2.6"/>'
        f'<path d="{border}" fill="none" stroke="{ink}" stroke-width=".7" stroke-dasharray="3 2.5" opacity=".55"/></g>'
        f'<g class="wm-under" aria-hidden="true">{"".join(under)}</g>'
        f'<g class="wm-labs" aria-hidden="true">{"".join(texts)}</g>'
        f"{''.join(marks)}</svg>"
    )

    groups: list[dict[str, Any]] = []
    for s in sites:
        if not groups or groups[-1]["name"] != s.get("group"):
            groups.append({"name": s.get("group"), "rows": []})
        paint = paints.get(s["name"])
        groups[-1]["rows"].append(
            {
                "name": s["name"],
                "label": label_text(s["name"]),
                "paint": colour(PAINT_TOKEN[paint][2:]) if paint in PAINT_TOKEN else "",
                "requested": _coords(s["configured"]["lat"], s["configured"]["lon"]),
                "answered": _coords(s["answered"]["lat"], s["answered"]["lon"], 3),
                "apart": f"{s['offset_km']:.1f} km",
                "stats": _cells(kind, s["stats"]),
            }
        )
    return {
        "svg": svg,
        "columns": _columns(kind),
        "groups": groups,
        "grouped": any(g["name"] for g in groups),
        "notes": notes(data),
        "count": len(sites),
    }
