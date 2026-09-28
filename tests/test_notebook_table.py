"""A notebook table's header lines up with its columns."""

from __future__ import annotations

import re

from gridflow_front_end import build


def test_the_pandas_index_heading_is_not_doubled() -> None:
    out = {"kind": "df", "columns": ["", "a", "b"], "index": ["0"], "rows": [["1", "2"]]}
    html = str(build._output_html(out, "elexon", "data.elexon", ""))
    head = re.search(r"<thead>(.*)</thead>", html).group(1)
    assert head.count("<th>") == 3
