"""Home is hand-written, but its catalogue counts come from the build's own source.

The ruling: the headline dataset count is computed, never hand-typed. gridflow-build counts each
vendor's datasets from ``site/hifi/data/<vendor>.json`` for Data sources; Home repeats those numbers,
so this test holds Home to the same files.
"""

from __future__ import annotations

import html
import re

from gridflow_front_end import build
from gridflow_front_end.paths import SITE_DIR

HOME = (SITE_DIR / "index.html").read_text(encoding="utf-8")
VENDOR = re.compile(
    r'<article class="vend[^"]*"[^>]*>.*?<h3 class="h-entry"><a href="data-sources/(\w+)\.html">'
    r"(.*?)</a></h3>.*?<p class=\"vend__m\">(.*?)</p>",
    re.S,
)


def _manifests() -> dict[str, dict]:
    return {v: build.load_manifest(v) for v in build.REAL_VENDORS}


def test_home_lists_every_vendor_with_the_builds_name_count_and_fact() -> None:
    manifests = _manifests()
    rows = {vid: (html.unescape(name), html.unescape(fact)) for vid, name, fact in VENDOR.findall(HOME)}
    assert set(rows) == set(manifests)
    for vid, m in manifests.items():
        name, fact = rows[vid]
        assert name == m["name"], vid
        assert fact == f"{build.manifest_total_count(m)} datasets, {m['landing']['fact']}", vid


def test_home_headline_count_is_the_builds_total() -> None:
    manifests = _manifests()
    total = sum(build.manifest_total_count(m) for m in manifests.values())
    vendors = build._count_word(len(manifests)).capitalize()
    assert f"{vendors} vendors, {total} datasets," in HOME
    assert f"{vendors} vendors across UK and EU power, gas, carbon and weather: {total} datasets" in HOME
    # no other dataset count anywhere on the page
    assert set(re.findall(r"(\d+) datasets", HOME)) <= {
        str(total),
        *(str(build.manifest_total_count(m)) for m in manifests.values()),
    }
