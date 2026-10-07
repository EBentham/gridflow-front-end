"""Write the UK and Ireland outline the weather-location maps are drawn on.

Reads Natural Earth's 1:50m Admin 0 countries GeoJSON (public domain; download it yourself, it is
not committed) and writes ``site/hifi/data/geo/gb-ie.json``: the land of the United Kingdom,
Ireland and the Isle of Man as lon/lat rings rounded to 3 decimals, plus the land border between
Northern Ireland and Ireland as its own run, so the build can draw it fainter than the coast. The build projects
the rings itself (``map_svg``), so the outline and the site markers share one projection.

Usage::

    uv run python scripts/make_outline.py path/to/ne_50m_admin_0_countries.geojson

The Isle of Man is its own Natural Earth feature (IMN); it is kept because two Irish Sea wind
sites sit beside it, and leaving it out would draw open sea where it stands.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT = REPO_ROOT / "site" / "hifi" / "data" / "geo" / "gb-ie.json"
KEEP = ("GBR", "IRL", "IMN")
PLACES = 3

Point = tuple[float, float]


def _rings(feature: dict) -> list[list[Point]]:
    geom = feature["geometry"]
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    out: list[list[Point]] = []
    for poly in polys:
        for ring in poly:
            pts: list[Point] = []
            for lon, lat in ring:
                p = (round(lon, PLACES), round(lat, PLACES))
                if not pts or pts[-1] != p:
                    pts.append(p)
            if len(pts) >= 4:
                out.append(pts)
    return out


def _segments(rings: list[list[Point]]) -> set[frozenset[Point]]:
    return {frozenset((a, b)) for r in rings for a, b in zip(r, r[1:]) if a != b}


def _runs(ring: list[Point], keep: set[frozenset[Point]], want: bool) -> list[list[Point]]:
    """Maximal runs of a closed ring's segments that are (``want``) or are not in ``keep``."""
    segs = list(zip(ring, ring[1:]))
    flags = [frozenset(s) in keep for s in segs]
    if all(f == want for f in flags):
        return [ring]
    # start the walk just after a segment of the other kind, so no run wraps the ring's seam
    start = next(i for i, f in enumerate(flags) if f != want) + 1
    order = [(i + start) % len(segs) for i in range(len(segs))]
    runs: list[list[Point]] = []
    cur: list[Point] = []
    for i in order:
        a, b = segs[i]
        if flags[i] == want:
            if not cur:
                cur = [a]
            cur.append(b)
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    return runs


def main(argv: list[str] | None = None) -> int:
    """Read the GeoJSON and write the committed outline."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("geojson", type=Path)
    args = parser.parse_args(argv)
    data = json.loads(args.geojson.read_text(encoding="utf-8"))
    by_code = {
        f["properties"]["ADM0_A3"]: _rings(f)
        for f in data["features"]
        if f["properties"].get("ADM0_A3") in KEEP
    }
    missing = set(KEEP) - set(by_code)
    if missing:
        raise SystemExit(f"features not found: {sorted(missing)}")
    shared = _segments(by_code["GBR"]) & _segments(by_code["IRL"])
    land = [r for code in KEEP for r in by_code[code]]
    border = [run for r in by_code["IRL"] for run in _runs(r, shared, want=True) if len(run) > 1]
    border = [run for run in border if all(frozenset(s) in shared for s in zip(run, run[1:]))]
    payload = {
        "_about": (
            "Natural Earth 1:50m Admin 0 countries (ne_50m_admin_0_countries, public domain): "
            "United Kingdom, Ireland and the Isle of Man, lon/lat rounded to 3 decimals; "
            "written by scripts/make_outline.py."
        ),
        "land": [[list(p) for p in r] for r in land],
        "border": [[list(p) for p in r] for r in border],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, separators=(",", ":"))
    OUT.write_text(text + "\n", encoding="utf-8", newline="\n")
    n = sum(len(r) for r in land)
    print(f"wrote {OUT.relative_to(REPO_ROOT)}: {len(land)} rings, {n} points, {len(text)} bytes")
    print(f"  border runs {len(border)}, shared segments {len(shared)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
