"""A notebook DataFrame with a named index keeps each header over its own column.

pandas gives a frame whose index (or columns axis) has a name a second header row. The HTML below
is pandas 3.0 ``to_html()`` output, turned into the stored ``df`` dict the way
``scripts/run_notebooks.py`` does (that script imports nbclient, so its three parsing lines are
repeated here rather than imported).
"""

from __future__ import annotations

import html
import re
from typing import Any

import pytest

from gridflow_front_end import build

_BODY = """  <tbody>
    <tr>
      <th>2024-01-01</th>
      <td>1.5</td>
      <td>2.00</td>
    </tr>
    <tr>
      <th>2024-01-02</th>
      <td>3.0</td>
      <td>4.25</td>
    </tr>
  </tbody>
</table>"""

# long.pivot(index="ts", columns="zone", values="mw")
PIVOT = (
    """<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>zone</th>
      <th>DE</th>
      <th>FR</th>
    </tr>
    <tr>
      <th>ts</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
"""
    + _BODY
)

# the same frame with columns.name = None: the set_index / groupby shape
INDEX_NAMED = (
    """<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DE</th>
      <th>FR</th>
    </tr>
    <tr>
      <th>ts</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
"""
    + _BODY
)

# columns.name only: one header row, the axis name in the corner
COLUMNS_NAMED = (
    """<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>zone</th>
      <th>DE</th>
      <th>FR</th>
    </tr>
  </thead>
"""
    + _BODY
)

PLAIN = (
    """<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DE</th>
      <th>FR</th>
    </tr>
  </thead>
"""
    + _BODY
)


def _stored(raw: str) -> dict[str, Any]:
    head = re.findall(r"<th>(.*?)</th>", raw.split("</thead>")[0])
    body = raw.split("<tbody>")[1]
    index: list[str] = []
    cells: list[list[str]] = []
    for row in re.findall(r"<tr>(.*?)</tr>", body, flags=re.DOTALL):
        index.append(html.unescape(re.findall(r"<th>(.*?)</th>", row)[0]))
        cells.append([html.unescape(c) for c in re.findall(r"<td>(.*?)</td>", row)])
    return {
        "kind": "df",
        "columns": [html.unescape(h) for h in head],
        "index": index,
        "rows": cells,
    }


def _render(raw: str) -> str:
    return str(build._output_html(_stored(raw), "entsoe", "data.entsoe", ""))


def _grid(fragment: str) -> list[list[str]]:
    return [
        re.findall(r"<t[hd]>(.*?)</t[hd]>", tr) for tr in re.findall(r"<tr>(.*?)</tr>", fragment)
    ]


@pytest.mark.parametrize("raw", [PIVOT, INDEX_NAMED, COLUMNS_NAMED, PLAIN])
def test_each_header_sits_over_its_own_values(raw: str) -> None:
    out = _render(raw)
    head = _grid(re.search(r"<thead>(.*)</thead>", out).group(1))
    body = _grid(re.search(r"<tbody>(.*)</tbody>", out).group(1))
    assert all(len(r) == 3 for r in head + body)
    top = head[0]
    assert top.index("DE") == body[0].index("1.5")
    assert top.index("FR") == body[0].index("2.00")


def test_the_named_index_keeps_both_header_rows() -> None:
    head = _grid(re.search(r"<thead>(.*)</thead>", _render(PIVOT)).group(1))
    assert head == [["zone", "DE", "FR"], ["ts", "", ""]]


def test_a_plain_frame_renders_as_before() -> None:
    assert _render(PLAIN) == (
        '<div class="df-wrap"><table class="df"><thead><tr><th></th><th>DE</th><th>FR</th></tr>'
        "</thead><tbody><tr><th>2024-01-01</th><td>1.5</td><td>2.00</td></tr>"
        "<tr><th>2024-01-02</th><td>3.0</td><td>4.25</td></tr></tbody></table></div>"
    )
