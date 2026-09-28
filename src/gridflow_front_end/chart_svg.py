"""Draw a dataset page's chart as static inline SVG at build time.

The chart is drawn from the committed series (``gridflow-distil``) and the
note's ``page.chart_view``; it needs no script, so it is in the page for every
reader, crawler and screen reader. Two drawings are made: a wide one beside
its key (desktop) and a narrow one for phones, swapped in CSS.

Drawing rules (DESIGN.md "Charts" and the dataset page lock, Decision 2):
- the scenery is the palette; codes it does not cover are unpainted (daylight
  with an ink hatch); khaki is the vendor code OTHER only
- a stacked area stacks each series' positive part above zero and hangs its
  negative part below, so signed series (interconnectors, pumped storage) are
  never clipped
- minimal chrome: an ink axis, a few real ticks, no gridlines, no legend
  inside the plot (the key sits beside it)

Stdlib only; colours come from ``tokens.css`` so the drawing and the theme
cannot drift apart.
"""

from __future__ import annotations

import datetime as dt
import html
import itertools
import math
import re
from collections.abc import Sequence
from dataclasses import dataclass
from functools import cache
from typing import Any

from gridflow_front_end.page_fields import DEFAULT_PAINT, ChartView, KeyEntry
from gridflow_front_end.paths import SITE_DIR

PAINT_TOKEN = {
    "horizon": "--fuel-wind",
    "chartreuse": "--fuel-solar",
    "clay": "--fuel-gas",
    "petrol": "--fuel-nuclear",
    "olive": "--fuel-imports",
    "bronze": "--fuel-biomass",
    "khaki": "--fuel-other",
}
HATCHES = ("hatch-lines", "hatch-cross", "hatch-dots", "hatch-vertical")
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


@cache
def tokens() -> dict[str, str]:
    """``--name: #hex`` pairs from ``tokens.css``."""
    text = (SITE_DIR / "assets" / "tokens.css").read_text(encoding="utf-8")
    return dict(re.findall(r"(--[a-z0-9-]+):\s*(#[0-9A-Fa-f]{6})", text))


def colour(name: str) -> str:
    """A token's hex value (``ink``, ``daylight``, ``fuel-wind`` ...)."""
    return tokens()[f"--{name}"]


def paint_of(entry: KeyEntry) -> str:
    """The entry's paint: explicit, else its palette role's default."""
    return entry.paint or DEFAULT_PAINT.get(entry.series, "petrol")


def _f(v: float) -> str:
    s = f"{v:.1f}"
    return s.removesuffix(".0")


def fmt_num(v: float, step: float | None = None) -> str:
    """Tick labels: thousands separators and a true minus sign.

    With ``step`` (the axis's tick spacing) every label carries the decimals that spacing needs, so a
    tenth-of-a-hertz axis reads 49.9, 50.0, 50.1 rather than 50 three times.
    """
    if step:
        places = 0
        while places < 4 and abs(step * 10**places - round(step * 10**places)) > 1e-6:
            places += 1
        text = f"{v:,.{places}f}"
    else:
        text = f"{v:,.0f}" if abs(v) >= 10 or v == int(v) else f"{v:,.1f}"
    return text.replace("-", "−")


def nice_ticks(lo: float, hi: float, count: int) -> list[float]:
    """Round tick values covering ``lo..hi``, about ``count`` of them."""
    if hi <= lo:
        hi = lo + 1
    raw = (hi - lo) / max(count, 1)
    mag = 10 ** math.floor(math.log10(raw))
    step = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)
    start = math.floor(lo / step) * step
    ticks: list[float] = []
    v = start
    while v <= hi + step * 1e-9:
        ticks.append(round(v, 10))
        v += step
    if ticks[-1] < hi:
        ticks.append(round(ticks[-1] + step, 10))
    return ticks


def _hatch_defs(uid: str) -> str:
    ink = colour("ink")
    return (
        f'<pattern id="{uid}-hatch-lines" width="6" height="4" patternUnits="userSpaceOnUse">'
        f'<path d="M0 2 H6" stroke="{ink}" stroke-width=".7"/></pattern>'
        f'<pattern id="{uid}-hatch-cross" width="6" height="6" patternUnits="userSpaceOnUse">'
        f'<path d="M0 6 L6 0 M0 0 L6 6" stroke="{ink}" stroke-width=".55"/></pattern>'
        f'<pattern id="{uid}-hatch-dots" width="4" height="4" patternUnits="userSpaceOnUse">'
        f'<circle cx="2" cy="2" r=".75" fill="{ink}"/></pattern>'
        f'<pattern id="{uid}-hatch-vertical" width="4" height="6" patternUnits="userSpaceOnUse">'
        f'<path d="M2 0 V6" stroke="{ink}" stroke-width=".7"/></pattern>'
    )


def _fill(uid: str, paint: str, d: str) -> str:
    """One filled shape in a paint: a palette colour, or daylight under an ink hatch."""
    if paint in PAINT_TOKEN:
        return f'<path d="{d}" fill="{colour(PAINT_TOKEN[paint][2:])}"/>'
    return f'<path d="{d}" fill="{colour("daylight")}"/><path d="{d}" fill="url(#{uid}-{paint})"/>'


def _stroke(paint: str) -> str:
    return colour(PAINT_TOKEN[paint][2:]) if paint in PAINT_TOKEN else colour("ink")


def key_mark(entry: KeyEntry, kind: str, uid: str) -> str:
    """The 30 x 18 key mark, copied from the chart part it names."""
    paint = paint_of(entry)
    ink = colour("ink")
    if kind == "line":
        dash = "" if paint in PAINT_TOKEN else ' stroke-dasharray="4 3"'
        body = (
            f'<path d="M1 12 L8 7 L15 10 L22 4 L29 8" fill="none" stroke="{_stroke(paint)}" '
            f'stroke-width="2" stroke-linejoin="round"{dash}/>'
        )
        defs = ""
    elif kind == "dots":
        body = (
            f'<path d="M3 12 L15 7 L27 9" fill="none" stroke="{_stroke(paint)}" stroke-width="1.8"/>'
            + "".join(
                f'<circle cx="{cx}" cy="{cy}" r="3" fill="{_stroke(paint)}" stroke="{ink}" stroke-width="1"/>'
                for cx, cy in ((3, 12), (15, 7), (27, 9))
            )
        )
        defs = ""
    else:
        rect = "M.75 3.75 H29.25 V14.25 H.75 Z"
        body = (
            _fill(uid, paint, rect)
            + f'<path d="{rect}" fill="none" stroke="{ink}" stroke-width="1.2"/>'
        )
        defs = f"<defs>{_hatch_defs(uid)}</defs>" if paint not in PAINT_TOKEN else ""
    return f'<svg class="mk" width="30" height="18" viewBox="0 0 30 18" aria-hidden="true">{defs}{body}</svg>'


@dataclass(frozen=True)
class Frame:
    """Geometry of one drawing."""

    w: int
    h: int
    x0: float
    x1: float
    top: float
    bottom: float
    y_ticks: int
    font_note: str


WIDE = Frame(w=900, h=470, x0=74, x1=884, top=26, bottom=410, y_ticks=5, font_note="")
NARROW = Frame(w=360, h=300, x0=50, x1=350, top=22, bottom=246, y_ticks=4, font_note=" narrow")
# The Data sources landing sets the chart in a 600 to 700 px column: drawn 600 wide, its 13 px text
# renders at 13 px or more there, where the 900-wide frame shrank it to 9 px.
LANDING = Frame(w=600, h=380, x0=64, x1=588, top=26, bottom=318, y_ticks=5, font_note="")


def _parse_time(value: str) -> float:
    text = value.replace("Z", "+00:00")
    if len(text) == 10:
        text += "T00:00:00+00:00"
    return dt.datetime.fromisoformat(text).timestamp()


def _day_label(ts: float, with_month: bool = True) -> str:
    d = dt.datetime.fromtimestamp(ts, dt.UTC)
    return f"{d.day} {MONTHS[d.month - 1]}" if with_month else str(d.day)


def _step(ts: Sequence[float]) -> float:
    """The series' own interval: its smallest spacing, not its average.

    A series whose missing periods are absent rather than null has a stretched average, and a line
    measured against it would bridge a missing half-hour instead of breaking there.
    """
    gaps = [b - a for a, b in itertools.pairwise(ts) if b > a]
    return min(gaps) if gaps else 86400


def _last_sunday(year: int, month: int) -> dt.date:
    d = dt.date(year, month + 1, 1) - dt.timedelta(days=1)
    return d - dt.timedelta(days=(d.weekday() + 1) % 7)


def _midnights(lo: float, hi: float, uk: bool) -> list[tuple[float, dt.date]]:
    """Each midnight in ``lo..hi`` with the date it opens, on the UTC clock or the UK one.

    A GB settlement date is a UK calendar day, so in summer time it opens at 23:00 UTC the evening
    before. UK summer time runs from the last Sunday in March to the last Sunday in October, both
    changes at 01:00 UTC, so a local midnight is an hour early for the dates in between.
    """
    out: list[tuple[float, dt.date]] = []
    d = dt.datetime.fromtimestamp(lo, dt.UTC).date() - dt.timedelta(days=1)
    while True:
        t = dt.datetime(d.year, d.month, d.day, tzinfo=dt.UTC).timestamp()
        if uk and _last_sunday(d.year, 3) < d <= _last_sunday(d.year, 10):
            t -= 3600
        if t > hi + 1:
            return out
        if t >= lo - 1:
            out.append((t, d))
        d += dt.timedelta(days=1)


def _time_axis(
    ts: Sequence[float], fr: Frame, narrow: bool, uk_days: bool = False
) -> tuple[list[tuple[float, str, float]], float, float]:
    """Ticks as ``(tick_ts, label, label_ts)``, plus the axis span."""
    lo, hi = ts[0], ts[-1]
    step = _step(ts)
    hi_edge = hi + step  # each value covers its own interval
    day = 86400
    span_days = (hi_edge - lo) / day
    ticks: list[tuple[float, str, float]] = []
    if abs(step - day) < 60 and span_days <= 16:
        # one value per day (a gas day from 04:00, say): ticks on the days' edges, each day named
        # under its own point, by the date at its middle
        n = round((hi_edge - lo) / day)
        every = 1 if not narrow or n <= 8 else 2
        for k in range(n):
            t = lo + k * day
            if k % every == 0:
                ticks.append((t, _day_label(t + day / 2, with_month=not narrow or not ticks), t + day / 2))
            else:
                ticks.append((t, "", t + day / 2))
        ticks.append((hi_edge, "", hi_edge))
    elif span_days <= 2:
        # a span of hours (15-second frequency, say): ticks on whole hours, labelled by the clock; the
        # caption carries the date
        cap = 4 if narrow else 8
        hours = next(h for h in (1, 2, 3, 6, 12, 24) if (hi_edge - lo) / (h * 3600) <= cap)
        t = math.ceil(lo / (hours * 3600)) * hours * 3600
        while t <= hi_edge + 1:
            ticks.append((t, dt.datetime.fromtimestamp(t, dt.UTC).strftime("%H:%M"), t))
            t += hours * 3600
    elif span_days <= 16:
        every = 1 if not narrow or span_days <= 8 else 2
        for i, (t, d) in enumerate(_midnights(lo, hi_edge, uk_days)):
            if t >= hi_edge - 1:
                # the midnight that closes the axis opens a day the chart does not show
                ticks.append((t, "", t))
            elif i % every == 0:
                # a short span labels each day at the middle of its visible part
                centre = (t + min(t + day, hi_edge)) / 2 if span_days <= 9 else t
                label = f"{d.day} {MONTHS[d.month - 1]}" if not narrow or not ticks else str(d.day)
                ticks.append((t, label, centre))
    else:
        # weekly ticks on Mondays, or the 1st of each month for long spans
        for t, d in _midnights(lo, hi_edge, uk_days):
            if (span_days <= 120 and d.weekday() == 0) or (span_days > 120 and d.day == 1):
                ticks.append((t, f"{d.day} {MONTHS[d.month - 1]}", t))
        if narrow and len(ticks) > 4:
            ticks = ticks[:: math.ceil(len(ticks) / 4)]
    return ticks, lo, hi_edge


def _settlement_days(view: ChartView) -> bool:
    """An axis of GB settlement dates marks UK days, not UTC ones."""
    return (view.x_label or "").lower().startswith("settlement date")


class _Plot:
    """Shared plotting state for one time drawing."""

    def __init__(
        self,
        fr: Frame,
        ts: Sequence[float],
        lo_v: float,
        hi_v: float,
        narrow: bool,
        uk_days: bool = False,
    ) -> None:
        self.fr = fr
        self.narrow = narrow
        self.ticks, self.t0, self.t1 = _time_axis(ts, fr, narrow, uk_days)
        self.yt = nice_ticks(lo_v, hi_v, fr.y_ticks)
        self.v0, self.v1 = self.yt[0], self.yt[-1]
        self.step = _step(ts)

    def X(self, t: float) -> float:
        return self.fr.x0 + (t - self.t0) / (self.t1 - self.t0) * (self.fr.x1 - self.fr.x0)

    def Y(self, v: float) -> float:
        return self.fr.bottom - (v - self.v0) / (self.v1 - self.v0) * (self.fr.bottom - self.fr.top)

    def axes(self, unit: str, x_label: str) -> str:
        fr, ink = self.fr, colour("ink")
        frame = (
            f'<path d="M{_f(fr.x0)} {_f(fr.top - 8)} V{_f(fr.bottom)} H{_f(fr.x1)}" fill="none" '
            f'stroke="{ink}" stroke-width="1.5"/>'
        )
        out = [frame]
        if self.v0 < 0 < self.v1:
            out.append(
                f'<path d="M{_f(fr.x0)} {_f(self.Y(0))} H{_f(fr.x1)}" stroke="{ink}" stroke-width="1.1"/>'
            )
        tk = " ".join(f"M{_f(self.X(t))} {_f(fr.bottom)} v6" for t, _, _ in self.ticks)
        ytk = " ".join(f"M{_f(fr.x0 - 6)} {_f(self.Y(v))} H{_f(fr.x0)}" for v in self.yt)
        out.append(f'<path d="{tk} {ytk}" stroke="{ink}" stroke-width="1.1"/>')
        txt = [
            f'<text x="{_f(fr.x0 - 10)}" y="{_f(self.Y(v) + 4.5)}" text-anchor="end">{fmt_num(v, self.yt[1] - self.yt[0])}</text>'
            for v in self.yt
        ]
        txt.append(
            f'<text x="{_f(fr.x0 - 10)}" y="{_f(fr.top - 12)}" text-anchor="end">{html.escape(unit)}</text>'
        )
        prev_right = -math.inf
        for _t, label, centre in self.ticks:
            x = self.X(centre)
            half = len(label) * 3.6  # about half the label's width at 13 px
            # a label that would run past the axis end or into its neighbour is left off
            if label and fr.x0 - 4 <= x and x + half <= fr.x1 + 8 and x - half >= prev_right + 6:
                txt.append(
                    f'<text x="{_f(x)}" y="{_f(fr.bottom + 22)}" text-anchor="middle">{label}</text>'
                )
                prev_right = x + half
        if x_label:
            txt.append(
                f'<text class="ax-i" x="{_f(fr.x1)}" y="{_f(fr.bottom + 44)}" text-anchor="end">'
                f"{html.escape(x_label)}</text>"
            )
        return "".join(out) + f'<g class="ax">{"".join(txt)}</g>'


def _runs(
    ts: Sequence[float], values: Sequence[float | None], step: float
) -> list[list[tuple[float, float]]]:
    """Consecutive non-null points, split where a value is missing or the time gap is too long."""
    runs: list[list[tuple[float, float]]] = []
    cur: list[tuple[float, float]] = []
    prev_t: float | None = None
    for t, v in zip(ts, values):
        gap = prev_t is not None and t - prev_t > step * 1.5
        if v is None or gap:
            if cur:
                runs.append(cur)
            cur = []
        if v is not None:
            cur.append((t, float(v)))
        prev_t = t
    if cur:
        runs.append(cur)
    return runs


def _stacked(chart: dict[str, Any], view: ChartView, fr: Frame, uid: str, narrow: bool) -> str:
    ts = [_parse_time(x) for x in chart["x"]]
    by_key = {e.series: e for e in view.key}
    series = chart["series"]
    n = len(ts)
    pos = [0.0] * n
    neg = [0.0] * n
    layers: list[tuple[KeyEntry, list[float], list[float], bool]] = []
    for s in series:
        vals = [float(v) if v is not None else 0.0 for v in s["values"]]
        entry = by_key[s["key"]]
        if any(v > 0 for v in vals):
            lower = pos[:]
            pos = [a + max(0.0, v) for a, v in zip(pos, vals)]
            layers.append((entry, lower, pos[:], True))
        if any(v < 0 for v in vals):
            upper = neg[:]
            neg = [a + min(0.0, v) for a, v in zip(neg, vals)]
            layers.append((entry, neg[:], upper, False))
    plot = _Plot(fr, ts, min(0.0, min(neg)), max(pos), narrow, _settlement_days(view))
    half = plot.step / 2
    body: list[str] = []
    labels: list[str] = []
    for entry, lower, upper, up in layers:
        top_pts = [(plot.X(t + half), plot.Y(u)) for t, u in zip(ts, upper)]
        bot_pts = [(plot.X(t + half), plot.Y(v)) for t, v in zip(ts, lower)]
        top_pts = [(fr.x0, top_pts[0][1]), *top_pts, (fr.x1, top_pts[-1][1])]
        bot_pts = [(fr.x0, bot_pts[0][1]), *bot_pts, (fr.x1, bot_pts[-1][1])]
        d = (
            "M"
            + " L".join(f"{_f(x)} {_f(y)}" for x, y in top_pts)
            + " L"
            + " L".join(f"{_f(x)} {_f(y)}" for x, y in reversed(bot_pts))
            + " Z"
        )
        body.append(_fill(uid, paint_of(entry), d))
        edge = top_pts if up else bot_pts
        body.append(
            '<path d="M'
            + " L".join(f"{_f(x)} {_f(y)}" for x, y in edge)
            + f'" fill="none" stroke="{colour("ink")}" stroke-width=".6" opacity=".55"/>'
        )
        if entry.tag and up and not narrow:
            best, bi = 0.0, -1
            for i in range(4, n - 4):
                th = abs(plot.Y(lower[i]) - plot.Y(upper[i]))
                score = th - abs(i - n / 2) * 0.02
                if score > best:
                    best, bi = score, i
            if bi >= 0 and abs(plot.Y(lower[bi]) - plot.Y(upper[bi])) >= 18:
                x = max(fr.x0 + 46, min(fr.x1 - 46, plot.X(ts[bi] + half)))
                y = (plot.Y(lower[bi]) + plot.Y(upper[bi])) / 2 + 4.5
                on_dark = paint_of(entry) in ("petrol", "olive")
                cls = ' class="on"' if on_dark else ""
                labels.append(
                    f'<text{cls} x="{_f(x)}" y="{_f(y)}" text-anchor="middle">{html.escape(entry.tag)}</text>'
                )
    return (
        "".join(body)
        + plot.axes(chart["unit"], view.x_label)
        + f'<g class="dl">{"".join(labels)}</g>'
    )


def _lines(chart: dict[str, Any], view: ChartView, fr: Frame, uid: str, narrow: bool) -> str:
    ts = [_parse_time(x) for x in chart["x"]]
    by_key = {e.series: e for e in view.key}
    values = [v for s in chart["series"] for v in s["values"] if v is not None]
    lo, hi = min(values), max(values)
    pad = (hi - lo) * 0.04 or 1
    # A line keeps a zero baseline while zero is close to the data; a band far from zero (a temperature,
    # a frequency near 50 Hz) is drawn to its own range, or it flattens into a strip at the top.
    floor = lo - pad if lo < 0 or lo > hi / 2 else 0.0
    plot = _Plot(fr, ts, floor, hi + pad, narrow, _settlement_days(view))
    half = plot.step / 2
    body: list[str] = []
    for s in chart["series"]:
        entry = by_key[s["key"]]
        paint = paint_of(entry)
        stroke = _stroke(paint)
        dash = "" if paint in PAINT_TOKEN else ' stroke-dasharray="5 3"'
        runs = _runs(ts, s["values"], plot.step)
        n_points = sum(len(r) for r in runs)
        for run in runs:
            pts = [(plot.X(t + half), plot.Y(v)) for t, v in run]
            if len(pts) > 1:
                body.append(
                    '<path d="M'
                    + " L".join(f"{_f(x)} {_f(y)}" for x, y in pts)
                    + f'" fill="none" stroke="{stroke}" stroke-width="1.8" stroke-linejoin="round"{dash}/>'
                )
            if n_points <= 60 or len(pts) == 1:
                body.extend(
                    f'<circle cx="{_f(x)}" cy="{_f(y)}" r="3.2" fill="{stroke}" stroke="{colour("ink")}" '
                    f'stroke-width="1"/>'
                    for x, y in pts
                )
    return "".join(body) + plot.axes(chart["unit"], view.x_label)


def _bars(chart: dict[str, Any], view: ChartView, fr: Frame, uid: str, narrow: bool) -> str:
    cats = chart["x"]
    vals = [float(v or 0) for v in chart["series"][0]["values"]]
    by_key = {e.series: e for e in view.key}
    fallback = by_key.get(chart["series"][0]["key"])
    label_w = 150 if not narrow else 110
    x0, x1 = fr.x0 + label_w, fr.x1 - (70 if not narrow else 56)
    top = fr.top
    row = min(34.0, (fr.bottom - top) / max(len(cats), 1))
    bar_h = row * 0.62
    ticks = nice_ticks(0, max(vals), 4)
    vmax = ticks[-1]
    ink = colour("ink")
    out: list[str] = []
    txt: list[str] = []
    for i, (cat, v) in enumerate(zip(cats, vals)):
        entry = by_key.get(cat) or fallback
        paint = paint_of(entry) if entry else "petrol"
        y = top + i * row + (row - bar_h) / 2
        w = (x1 - x0) * v / vmax
        rect = f"M{_f(x0)} {_f(y)} H{_f(x0 + w)} V{_f(y + bar_h)} H{_f(x0)} Z"
        out.append(_fill(uid, paint, rect))
        out.append(f'<path d="{rect}" fill="none" stroke="{ink}" stroke-width="1"/>')
        name = entry.label if entry and entry.series == cat else cat
        txt.append(
            f'<text x="{_f(x0 - 10)}" y="{_f(y + bar_h / 2 + 4.5)}" text-anchor="end">{html.escape(name)}</text>'
        )
        txt.append(f'<text x="{_f(x0 + w + 8)}" y="{_f(y + bar_h / 2 + 4.5)}">{fmt_num(v)}</text>')
    base = top + len(cats) * row + 4
    out.append(f'<path d="M{_f(x0)} {_f(top - 4)} V{_f(base)}" stroke="{ink}" stroke-width="1.5"/>')
    # the unit sits at the foot of the bars' axis, beside the bars it measures, not out at the far end
    out.append(
        f'<text class="ax-i" x="{_f(x0)}" y="{_f(base + 22)}" text-anchor="start">{html.escape(chart["unit"])}</text>'
    )
    return "".join(out) + f'<g class="ax">{"".join(txt)}</g>'


def _height_for_bars(chart: dict[str, Any], fr: Frame) -> Frame:
    n = len(chart["x"])
    h = int(fr.top + n * 34 + 40)
    return Frame(fr.w, h, fr.x0 - 50, fr.x1, fr.top, h - 40, fr.y_ticks, fr.font_note)


def key_kind(chart: dict[str, Any]) -> str:
    """How the key marks are drawn: blocks for areas and bars, lines or dots for lines."""
    if chart["type"] != "line":
        return "block"
    few = all(sum(v is not None for v in s["values"]) <= 60 for s in chart["series"])
    return "dots" if few else "line"


def render(
    chart: dict[str, Any], view: ChartView, uid: str, wide: Frame = WIDE
) -> tuple[str, str]:
    """The wide and the narrow drawing of one chart.

    Args:
        chart: The committed series payload.
        view: The note's ``chart_view`` (every series has a key entry).
        uid: A page-unique prefix for pattern ids.
        wide: The frame of the wide drawing (the narrow one is fixed).

    Returns:
        ``(wide_svg, narrow_svg)``.
    """
    drawers = {"stacked-area": _stacked, "line": _lines, "bar": _bars}
    draw = drawers[chart["type"]]
    out = []
    for fr, narrow in ((wide, False), (NARROW, True)):
        if chart["type"] == "bar":
            fr = _height_for_bars(chart, fr)
        sid = f"{uid}{'n' if narrow else 'w'}"
        body = draw(chart, view, fr, sid, narrow)
        cls = "chart chart--narrow" if narrow else "chart chart--wide"
        out.append(
            f'<svg class="{cls}" viewBox="0 0 {fr.w} {fr.h}" width="{fr.w}" height="{fr.h}" role="img" '
            f'aria-label="{html.escape(view.alt, quote=True)}"><defs>{_hatch_defs(sid)}</defs>{body}</svg>'
        )
    return out[0], out[1]


def check_view(chart: dict[str, Any], view: ChartView) -> list[str]:
    """Every series (or bar category) has exactly one key entry, and no entry is orphaned."""
    errors: list[str] = []
    if chart["type"] == "bar":
        names = set(chart["x"]) | {chart["series"][0]["key"]}
        needed: set[str] = set()
    else:
        names = {s["key"] for s in chart["series"]}
        needed = names
    keys = [e.series for e in view.key]
    dup = sorted({k for k in keys if keys.count(k) > 1})
    if dup:
        errors.append(f"chart_view.key: series listed twice {dup}")
    missing = sorted(needed - set(keys))
    if missing:
        errors.append(f"chart_view.key: no entry for series {missing}")
    orphan = sorted(set(keys) - names)
    if orphan:
        errors.append(f"chart_view.key: entries for series the chart does not draw {orphan}")
    if chart["type"] == "line":
        hatched = [e.series for e in view.key if paint_of(e) in HATCHES]
        if len(hatched) > 1:
            errors.append(
                "chart_view.key: a line chart draws at most one unpainted (dashed) series"
            )
    return errors
