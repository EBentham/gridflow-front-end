#!/usr/bin/env python3
"""Generate .planning/v3/page-manifest.json — the disjoint creative-pass backlog.

Tags every shippable page with type / vendor / slug / tier / flagship so the
Phase 14-15 staggered fleet can claim disjoint page sets. Tier 1 = recruiter
path (top-level + hubs + flagship datasets); tier 2 = the long tail.
Re-run any time; deterministic (sorted).
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
AUTHORED = ROOT / "authored-pages"
HIFI = ROOT / "site" / "hifi"

# Top-level hand-authored pages (live directly under site/hifi/).
TOP_LEVEL = [
    "site/hifi/index.html",
    "site/hifi/architecture.html",
    "site/hifi/data-sources.html",
    "site/hifi/models/demand-forecast.html",
]

# ~12 flagship datasets — widest domain spread, highest recruiter signal.
FLAGSHIP = {
    "elexon/fuelhh", "elexon/system_prices", "elexon/mid",
    "entsoe/day_ahead_prices", "entsoe/actual_generation",
    "entsoe/net_positions", "entsoe/imbalance_prices",
    "neso/carbon_intensity", "neso/generation",
    "entsog/physical_flows", "gie/storage", "openmeteo/forecast_wind",
}


def main() -> int:
    pages: list[dict] = []

    for rel in TOP_LEVEL:
        pages.append({
            "path": rel,
            "type": "top",
            "vendor": None,
            "slug": pathlib.Path(rel).stem,
            "tier": 1,
            "flagship": False,
            "mechanical": "done",
            "creative": "pending",
        })

    for page in sorted(AUTHORED.rglob("*.html")):
        vendor = page.parent.name
        slug = page.stem
        rel = page.relative_to(ROOT).as_posix()
        if slug == "_landing":
            pages.append({
                "path": rel, "type": "hub", "vendor": vendor, "slug": vendor,
                "tier": 1, "flagship": False, "mechanical": "done", "creative": "pending",
            })
            continue
        key = f"{vendor}/{slug}"
        flagship = key in FLAGSHIP
        pages.append({
            "path": rel, "type": "dataset", "vendor": vendor, "slug": slug,
            "tier": 1 if flagship else 2, "flagship": flagship,
            "mechanical": "done", "creative": "pending",
        })

    tier1 = [p for p in pages if p["tier"] == 1]
    manifest = {
        "note": "v3 creative-pass backlog. mechanical=Phase 13 (done). creative=Phase 14/15.",
        "counts": {
            "total": len(pages),
            "tier1_recruiter_path": len(tier1),
            "tier2_long_tail": len(pages) - len(tier1),
            "top": sum(p["type"] == "top" for p in pages),
            "hub": sum(p["type"] == "hub" for p in pages),
            "flagship": sum(p["flagship"] for p in pages),
        },
        "pages": pages,
    }
    out = ROOT / ".planning" / "v3" / "page-manifest.json"
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT).as_posix()}")
    print(json.dumps(manifest["counts"], indent=2))
    miss = sorted(FLAGSHIP - {f"{p['vendor']}/{p['slug']}" for p in pages if p["type"] == "dataset"})
    if miss:
        print(f"WARNING: flagship slugs not found on disk: {miss}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
