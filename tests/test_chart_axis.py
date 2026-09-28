"""The time axis: daily series name each day under its own point, and no label runs off the axis."""

from __future__ import annotations

import datetime as dt
import re

from gridflow_front_end import chart_svg

DAY = 86400.0


def _gas_days(n: int) -> list[float]:
    start = dt.datetime(2026, 9, 13, 4, tzinfo=dt.UTC).timestamp()
    return [start + i * DAY for i in range(n)]


def test_gas_days_are_labelled_under_their_points_with_ticks_on_their_edges() -> None:
    ts = _gas_days(9)
    ticks, lo, hi = chart_svg._time_axis(ts, chart_svg.WIDE, narrow=False)
    labelled = [(label, centre) for _t, label, centre in ticks if label]
    assert [label for label, _c in labelled] == [f"{d} Sep" for d in range(13, 22)]
    assert [centre for _l, centre in labelled] == [t + DAY / 2 for t in ts]
    assert [t for t, _l, _c in ticks] == [*ts, ts[-1] + DAY]
    assert (lo, hi) == (ts[0], ts[-1] + DAY)


def test_no_axis_label_passes_the_end_of_the_axis() -> None:
    ts = [dt.datetime(2026, 9, 15, 23, tzinfo=dt.UTC).timestamp() + i * 1800 for i in range(336)]
    plot = chart_svg._Plot(chart_svg.WIDE, ts, 0.0, 100.0, narrow=False)
    svg = plot.axes("£/MWh", "")
    for x, label in re.findall(r'<text x="([\d.]+)" y="[\d.]+" text-anchor="middle">([^<]+)</text>', svg):
        assert float(x) + len(label) * 3.6 <= chart_svg.WIDE.x1 + 8, label


def test_a_span_of_hours_is_labelled_by_the_clock() -> None:
    start = dt.datetime(2026, 9, 17, tzinfo=dt.UTC).timestamp()
    ts = [start + i * 15 for i in range(6 * 240)]
    ticks, _lo, _hi = chart_svg._time_axis(ts, chart_svg.WIDE, narrow=False)
    assert [label for _t, label, _c in ticks] == [f"{h:02d}:00" for h in range(7)]


def test_a_band_far_from_zero_is_drawn_to_its_own_range() -> None:
    start = dt.datetime(2026, 9, 17, tzinfo=dt.UTC).timestamp()
    chart = {
        "x": [dt.datetime.fromtimestamp(start + i * 15, dt.UTC).isoformat() for i in range(3)],
        "series": [{"key": "f", "values": [49.9, 50.0, 50.1]}],
        "unit": "Hz",
    }
    view = chart_svg.ChartView(key=[chart_svg.KeyEntry(series="f", label="Frequency")], x_label=None)
    svg = chart_svg._lines(chart, view, chart_svg.WIDE, "t", narrow=False)
    assert ">0<" not in svg


def test_axis_labels_carry_the_decimals_their_spacing_needs() -> None:
    assert [chart_svg.fmt_num(v, 0.1) for v in (49.9, 50.0, 50.1)] == ["49.9", "50.0", "50.1"]
    assert chart_svg.fmt_num(12.5, 2.5) == "12.5"
    assert chart_svg.fmt_num(-1500, 500) == "−1,500"


def test_settlement_dates_tick_on_uk_midnight() -> None:
    # settlement dates 15 to 21 September 2026 in BST: each opens at 23:00 UTC the evening before
    lo = dt.datetime(2026, 9, 14, 23, tzinfo=dt.UTC).timestamp()
    ts = [lo + i * 1800 for i in range(7 * 48)]
    ticks, _lo, _hi = chart_svg._time_axis(ts, chart_svg.WIDE, narrow=False, uk_days=True)
    assert [t for t, _l, _c in ticks] == [lo + i * DAY for i in range(8)]
    assert [label for _t, label, _c in ticks][:2] == ["15 Sep", "16 Sep"]


def test_winter_settlement_dates_tick_on_utc_midnight() -> None:
    lo = dt.datetime(2026, 12, 1, tzinfo=dt.UTC).timestamp()
    ts = [lo + i * 1800 for i in range(3 * 48)]
    ticks, _lo, _hi = chart_svg._time_axis(ts, chart_svg.WIDE, narrow=False, uk_days=True)
    assert ticks[0][0] == lo


def test_a_line_breaks_at_a_missing_half_hour_that_is_absent_not_null() -> None:
    t0 = dt.datetime(2026, 9, 14, tzinfo=dt.UTC).timestamp()
    ts = [t0 + i * 1800 for i in range(10) if i != 4]
    runs = chart_svg._runs(ts, [1.0] * len(ts), chart_svg._step(ts))
    assert [len(r) for r in runs] == [4, 5]


def test_the_midnight_closing_the_axis_carries_no_day_label() -> None:
    lo = dt.datetime(2026, 9, 14, 23, tzinfo=dt.UTC).timestamp()
    ts = [lo + i * 1800 for i in range(7 * 48)]
    for narrow in (False, True):
        ticks, _lo, hi = chart_svg._time_axis(ts, chart_svg.WIDE, narrow=narrow, uk_days=True)
        assert ticks[-1][0] == hi and ticks[-1][1] == ""
