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
