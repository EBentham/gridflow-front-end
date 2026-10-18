"""The y axis floor (chart_view.y_min) and missing periods drawn as gaps."""

from __future__ import annotations

import datetime as dt
import re
from typing import Any

from gridflow_front_end import chart_svg
from gridflow_front_end.page_fields import ChartView, KeyEntry, parse_page_fields

DAY = 86400.0
INK = chart_svg.colour("ink")
PETROL = chart_svg.colour("fuel-nuclear")


def _days(n: int, skip: range = range(0)) -> list[str]:
    t0 = dt.datetime(2025, 4, 1, tzinfo=dt.UTC).timestamp()
    return [
        dt.datetime.fromtimestamp(t0 + i * DAY, dt.UTC).date().isoformat()
        for i in range(n)
        if i not in skip
    ]


def _view(*keys: str, y_min: float | None = None) -> ChartView:
    return ChartView(
        key=tuple(KeyEntry(series=k, label=k, paint="petrol") for k in keys), y_min=y_min
    )


def _y_labels(svg: str) -> list[str]:
    return re.findall(r'text-anchor="end">([−\d,.]+M?)</text>', svg)


def _zero_rule(svg: str, fr: chart_svg.Frame) -> bool:
    # the zero rule is the only ink path that runs across the plot at stroke-width 1.1 with no fill
    return bool(
        re.search(
            rf'<path d="M{chart_svg._f(fr.x0)} [\d.]+ H{chart_svg._f(fr.x1)}" stroke="{INK}"', svg
        )
    )


def _line_ys(svg: str) -> list[float]:
    """Every y coordinate of the petrol line's paths."""
    paths = re.findall(rf'<path d="M([^"]+)" fill="none" stroke="{PETROL}"', svg)
    return [float(y) for d in paths for y in re.findall(r"[\d.]+ ([\d.]+)", d)]


def _cost_chart() -> dict[str, Any]:
    # constraint breakdown's shape: tens of millions, a few dates a little below zero
    values = [5e6 + (i % 7) * 8e6 for i in range(60)]
    values[10] = -232_717.0
    return {"type": "line", "x": _days(60), "series": [{"key": "c", "values": values}], "unit": "£"}


def test_by_default_a_small_negative_floors_the_axis_a_whole_step_down() -> None:
    svg = chart_svg._lines(_cost_chart(), _view("c"), chart_svg.WIDE, "t", narrow=False)
    assert _y_labels(svg)[0] == "−20M"


def test_y_min_floors_the_axis_just_below_the_data() -> None:
    fr = chart_svg.WIDE
    svg = chart_svg._lines(_cost_chart(), _view("c", y_min=-2e6), fr, "t", narrow=False)
    labels = _y_labels(svg)
    # no tick below the floor; the floor itself is not a tick
    assert labels[0] == "0" and "−20M" not in labels
    # a value is below zero, so the zero rule is drawn, above the axis
    assert _zero_rule(svg, fr)
    plot = chart_svg._Plot(fr, [0.0, DAY], -2e6, 60e6, narrow=False, y_min=-2e6, negative=True)
    assert plot.v0 == -2e6 and plot.Y(-2e6) == fr.bottom and plot.Y(0) < fr.bottom


def test_y_min_must_not_cut_off_a_value() -> None:
    chart = _cost_chart()
    assert chart_svg.check_view(chart, _view("c", y_min=-2e6)) == []
    errors = chart_svg.check_view(chart, _view("c", y_min=0))
    assert any("above the lowest value drawn" in e for e in errors), errors
    assert chart_svg.check_view(chart, _view("c", y_min=1e9))
    bar = {"type": "bar", "x": ["a"], "series": [{"key": "c", "values": [1.0]}], "unit": "MW"}
    assert any("bar chart" in e for e in chart_svg.check_view(bar, _view("c", y_min=-1)))


def test_a_gap_in_a_line_at_zero_reads_as_a_gap_with_a_floor_below_zero() -> None:
    # aggregated BSAD's shape: zero on most days, a missing year, never below zero
    xs = _days(40, skip=range(15, 25))
    values = [0.0] * len(xs)
    values[3] = 150.0
    chart = {"type": "line", "x": xs, "series": [{"key": "bpa", "values": values}], "unit": "£/MWh"}
    fr = chart_svg.WIDE
    plain = chart_svg._lines(chart, _view("bpa"), fr, "t", narrow=False)
    lifted = chart_svg._lines(chart, _view("bpa", y_min=-10), fr, "t", narrow=False)
    for svg in (plain, lifted):
        # the line breaks at the missing days: two runs, neither crossing the gap
        assert len(re.findall(rf'stroke="{PETROL}" stroke-width="1.8"', svg)) == 2
    # without a floor the zero line lies on the axis; with one it sits above it
    assert max(_line_ys(plain)) == fr.bottom
    assert max(_line_ys(lifted)) < fr.bottom
    # nothing is below zero, so no zero rule is drawn to be mistaken for the line
    assert not _zero_rule(lifted, fr)
    assert "0" in _y_labels(lifted)


def test_a_stacked_area_breaks_where_a_period_is_absent() -> None:
    xs = _days(30, skip=range(10, 14))
    n = len(xs)
    chart = {
        "type": "stacked-area",
        "x": xs,
        "series": [{"key": "a", "values": [5.0] * n}, {"key": "b", "values": [3.0] * n}],
        "unit": "£",
    }
    view = ChartView(
        key=(
            KeyEntry(series="a", label="a", paint="petrol"),
            KeyEntry(series="b", label="b", paint="clay"),
        )
    )
    fr = chart_svg.WIDE
    svg = chart_svg._stacked(chart, view, fr, "t", narrow=False)
    fills = re.findall(rf'<path d="(M[^"]+Z)" fill="{PETROL}"/>', svg)
    assert len(fills) == 2
    first, second = ([float(x) for x in re.findall(r"([\d.]+) [\d.]+", d)] for d in fills)
    # the first run closes at the end of its last day, the second opens at the start of its first
    assert max(first) < min(second)
    assert min(first) == fr.x0 and max(second) == fr.x1


def test_a_stacked_period_with_every_series_null_is_a_gap() -> None:
    ts = [i * DAY for i in range(6)]
    series = [
        {"values": [1.0, 1.0, None, 1.0, 1.0, 1.0]},
        {"values": [2.0, 2.0, None, None, 2.0, 2.0]},
    ]
    assert chart_svg._periods(ts, series, DAY) == [range(0, 2), range(3, 6)]
    assert chart_svg._periods(ts[:2] + ts[4:], [{"values": [1.0] * 4}], DAY) == [
        range(0, 2),
        range(2, 4),
    ]


def test_the_note_carries_y_min_as_a_number() -> None:
    note = "---\npage:\n  chart_view:\n    y_min: -10\n---\n"
    fields, errors = parse_page_fields(note)
    assert errors == [] and fields.chart_view.y_min == -10.0
    _fields, errors = parse_page_fields(note.replace("-10", "low"))
    assert any("y_min" in e for e in errors)
