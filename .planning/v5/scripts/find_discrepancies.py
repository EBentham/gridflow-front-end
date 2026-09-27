"""Per-dataset discrepancy list (v5 Phase 22): what the site / mirror / vault says vs code and silver.

Reads .planning/v5/DATA-MATRIX.json (run build_data_matrix.py first), the rendered pages under
site/hifi/data-sources, chart-series.json, local silver, and the canonical vault (git blobs).
Writes .planning/v5/DISCREPANCIES.md and DISCREPANCIES.json. Offline; reports only, fixes nothing.

    uv run --with polars python .planning/v5/scripts/find_discrepancies.py
"""

from __future__ import annotations

import difflib
import html
import json
import os
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import polars as pl

FE = Path(__file__).resolve().parents[3]
V5 = Path(os.environ.get("MATRIX_OUT_DIR", FE / ".planning" / "v5"))
VAULT = Path(os.environ.get("QUANT_VAULT", r"C:\Users\Bobbo\OneDrive\Desktop\Learning\AI\quant-vault"))
DATA = Path(os.environ.get("GRIDFLOW_DATA_DIR", r"C:\gridflow-data"))
VAULT_REF = os.environ.get("VAULT_REF", "master")
INFRA = {"event_time", "available_at", "vintage_policy", "source_run_id", "dataset_version", "month", "year"}
MAX_CODES = 60


def cells(row_html: str) -> list[str]:
    return [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row_html, re.DOTALL)]


def page_tables(t: str) -> tuple[list[str], list[str], list[list[str]]]:
    schema_cols: list[str] = []
    m = re.search(r'<table class="schema-table">(.*?)</table>', t, re.DOTALL)
    if m:
        for c in re.findall(r'<td class="col-name">(.*?)</td>', m.group(1), re.DOTALL):
            name = html.unescape(re.sub(r"<[^>]+>", " ", c)).split()
            if name:
                schema_cols.append(name[0])
    head: list[str] = []
    rows: list[list[str]] = []
    m = re.search(r'<table class="data-table">(.*?)</table>', t, re.DOTALL)
    if m:
        th = re.search(r"<thead>(.*?)</thead>", m.group(1), re.DOTALL)
        head = cells(th.group(1)) if th else []
        tb = re.search(r"<tbody>(.*?)</tbody>", m.group(1), re.DOTALL)
        if tb:
            rows = [cells(r) for r in re.findall(r"<tr[^>]*>(.*?)</tr>", tb.group(1), re.DOTALL)]
    return schema_cols, head, rows


def silver_codes(src: str, ds: str, cols: list[str]) -> dict[str, set[str]]:
    """Distinct values of low-cardinality string columns across all silver files."""
    root = DATA / "silver" / src / ds
    files = sorted(root.rglob("*.parquet"))
    if not files:
        return {}
    try:
        sch = pl.read_parquet_schema(files[-1])
    except Exception:  # noqa: BLE001
        return {}
    str_cols = [c for c in cols if c in sch and sch[c] in (pl.String, pl.Categorical)]
    out: dict[str, set[str]] = {}
    for c in str_cols:
        try:
            vals = (pl.scan_parquet(files, hive_partitioning=False).select(pl.col(c).unique()).collect()
                    .get_column(c).drop_nulls().to_list())
        except Exception:  # noqa: BLE001
            continue
        if 0 < len(vals) <= MAX_CODES:
            out[c] = {str(v) for v in vals}
    return out


def vault_diff(canon_path: str, mirror: Path) -> dict[str, Any]:
    canon = subprocess.run(["git", "-C", str(VAULT), "show", f"{VAULT_REF}:{canon_path}"], capture_output=True).stdout
    a = mirror.read_text(encoding="utf-8", errors="replace").splitlines() if mirror.exists() else []
    b = canon.decode("utf-8", "replace").splitlines()
    added = removed = 0
    changed: list[str] = []
    for ln in difflib.unified_diff(a, b, lineterm="", n=0):
        if ln.startswith("+++") or ln.startswith("---") or ln.startswith("@@"):
            continue
        if ln.startswith("+"):
            added += 1
            body = ln[1:].strip()
            if (len(changed) < 3 and len(body) > 60 and not re.match(r"^[A-Za-z_]+:\s", body)
                    and not body.startswith(("|", "-", "`", "#", "{", "}", "\"")) and " " in body):
                changed.append(body[:260])
        elif ln.startswith("-"):
            removed += 1
    fm = re.search(r"last_verified:\s*(\S+)", "\n".join(a))
    return {"mirror_last_verified": fm.group(1) if fm else None, "lines_added_in_canonical": added,
            "lines_removed_from_mirror": removed, "canonical_new_lines": changed}


def main() -> None:
    mx = json.loads((V5 / "DATA-MATRIX.json").read_text(encoding="utf-8"))
    chart = json.loads((FE / "site/hifi/data/chart-series.json").read_text(encoding="utf-8"))["series"]
    out: list[dict[str, Any]] = []
    systemic: dict[str, list[str]] = defaultdict(list)
    for r in mx["rows"]:
        key = f"{r['vendor']}/{r['slug']}"
        g, silver, vault = r["gridflow"], r["silver"], r.get("vault")
        items: list[dict[str, str]] = []

        def add(kind: str, where: str, text: str) -> None:
            items.append({"kind": kind, "where": where, "text": text})

        scols = [c for c in (silver.get("columns") or []) if c not in INFRA]
        page = r.get("page")
        src = "authored override" if r["authored_override"] else "template (from mirror)"
        if page and not r["stub"]:
            t = (FE / page["path"]).read_text(encoding="utf-8", errors="replace")
            sch_cols, head, rows = page_tables(t)
            if scols and sch_cols:
                miss = [c for c in scols if c not in sch_cols]
                extra = [c for c in sch_cols if c not in scols]
                if extra:
                    add("page-schema", src, f"page schema lists columns silver does not have: {', '.join(extra)}")
                if miss:
                    add("page-schema", src, f"silver columns missing from the page schema: {', '.join(miss)}")
            if scols and head:
                extra = [c for c in head if c not in scols and c not in INFRA]
                if extra:
                    add("page-sample", src, f"sample-row columns not in silver: {', '.join(extra)}")
            if rows and head and g["key"] and r["silver_present"]:
                s_src, s_ds = g["key"].split("/")
                codes = silver_codes(s_src, s_ds, head)
                for c, allowed in codes.items():
                    i = head.index(c)
                    bad = sorted({row[i] for row in rows if i < len(row) and row[i]
                                  and row[i].split(" (")[0].strip('"') not in allowed
                                  and row[i] not in ("—", "-", "null", "None", "…", '""')})
                    if bad:
                        add("page-sample-value", src,
                            f"sample `{c}` values never seen in silver ({silver.get('rows', 0):,} rows, "
                            f"{(silver.get('first') or '')[:10]}..{(silver.get('last') or '')[:10]}): {', '.join(bad[:8])}; "
                            f"silver has {len(allowed)} distinct")
            mcount = re.search(r"All (\d+) codes", t)
            if mcount and g["key"] and r["silver_present"]:
                s_src, s_ds = g["key"].split("/")
                codes_all = silver_codes(s_src, s_ds, scols)
                if codes_all:
                    col, vals = max(codes_all.items(), key=lambda kv: len(kv[1]))
                    if int(mcount.group(1)) != len(vals):
                        add("page-code-list", src, f"page says 'All {mcount.group(1)} codes'; silver `{col}` has "
                            f"{len(vals)} distinct values: {', '.join(sorted(vals))}")
            low = t.lower()
            if "seeded" in low:
                add("chart", src, "page carries a seeded (synthetic) chart")
            elif "illustrative" in low:
                add("chart", src, "page labels its chart or sample 'illustrative'")
            ep = g.get("endpoint")
            if ep and isinstance(ep, str) and ep.startswith("/") and "{" not in ep and ep not in t:
                add("endpoint", src, f"gridflow endpoint `{ep}` does not appear on the page")
            if not r["silver_present"]:
                if re.search(r"\b(silver sample|what a row looks like)\b", low):
                    add("no-silver", src, "page shows sample rows but there is no local silver for this dataset")
        ch = chart.get(key)
        if ch:
            if silver.get("columns") and any(c in (silver.get("columns") or []) for c in
                                               ("fuel_type", "psr_type", "production_type", "area_code", "region_id",
                                                "bm_unit", "point_key", "indicator")):
                add("chart", "chart-series.json",
                    f"series is '{ch['aggregation']}' from a one-off extract ({ch['start']}..{ch['end']}), "
                    "averaging across a categorical dimension; not from silver")
            else:
                add("chart", "chart-series.json",
                    f"series is '{ch['aggregation']}' from a one-off extract ({ch['start']}..{ch['end']}), not from silver")
        if r.get("mirror") and not r["mirror"]["byte_identical"] and vault:
            d = vault_diff(vault["path"], FE / r["mirror"]["path"])
            add("mirror-stale", r["mirror"]["path"],
                f"mirror is behind canonical (+{d['lines_added_in_canonical']}/-{d['lines_removed_from_mirror']} lines; "
                f"mirror last_verified {d['mirror_last_verified']} vs canonical {vault.get('last_verified')}). "
                + (f"Canonical now says: \"{d['canonical_new_lines'][0]}\"" if d["canonical_new_lines"] else ""))
        if vault:
            vs = r["vault_vs_code_schema"]
            if vs["status"] == "differs":
                add("vault-schema", vault["path"],
                    f"vault silver-schema table vs {vs['basis']}: missing {vs['missing_in_vault']}, extra {vs['extra_in_vault']}")
            elif vs["status"] == "bitemporal_only":
                systemic["vault silver-schema table omits `published_at`/`ingested_at` (bitemporal columns added to code after 2026-06-15)"].append(key)
            elif vs["status"] == "no_vault_table":
                systemic["vault note has a Silver layer section but no silver-schema table"].append(key)
            elif vs["status"] == "no_silver_section":
                systemic["vault note has no Silver layer section"].append(key)
            lc = (vault.get("layer_coverage") or "").lower()
            if "silver" in lc and not g["has_transformer"]:
                add("vault-coverage", vault["path"], f"note claims layer_coverage '{vault.get('layer_coverage')}' but gridflow has no silver transformer")
            if "silver" in lc and g["has_transformer"] and not r["silver_present"]:
                add("no-silver", vault["path"], "note claims silver coverage; no local silver rows exist")
            val = vault.get("validator_2026_06_15") or {}
            if any(s != "passed" for s in val.get("curl", [])):
                systemic["curl example not passing at the 2026-06-15 validator run"].append(
                    f"{key} ({', '.join(s for s in val.get('curl', []) if s != 'passed')})")
        if r["registry_vs_vault"] != "agree":
            add("registry", "gridflow vs vault", r["registry_vs_vault"])
        if r.get("silver_vs_code_schema"):
            m, e = r["silver_vs_code_schema"]["missing_in_silver"], [
                c for c in r["silver_vs_code_schema"]["extra_in_silver"] if c not in INFRA]
            if m:
                add("silver-vs-code", "local silver", f"pydantic columns absent from local silver parquet (stale silver?): {', '.join(m)}")
        if items:
            out.append({"dataset": key, "stub": r["stub"], "items": items})
    (V5 / "DISCREPANCIES.json").write_text(json.dumps({"datasets": out, "systemic": systemic}, indent=1) + "\n", encoding="utf-8")
    kinds = Counter(i["kind"] for d in out for i in d["items"])
    md = ["# v5 discrepancy list (Phase 22)", "",
          "Per dataset: what the site, the vault mirror or the canonical vault says that disagrees with gridflow code "
          "or local silver. Input to Phase 26; nothing is fixed here. Generated by "
          "`.planning/v5/scripts/find_discrepancies.py` from `DATA-MATRIX.json`. Sample-value checks compare the "
          "page's sample rows with the distinct values of low-cardinality string columns across ALL local silver.",
          "", "Counts by kind: " + ", ".join(f"{k} {v}" for k, v in kinds.most_common()) + ".", "",
          "Kinds: `page-sample-value` a value in the page's sample rows that silver never contains (the FUELHH SOLAR "
          "class) · `page-code-list` the page's 'All N codes' count vs silver's distinct codes · `page-schema` / `page-sample` page columns vs silver columns · `mirror-stale` the rendered source "
          "is behind the canonical vault · `vault-schema` substantive vault-table vs code difference · `chart` "
          "provenance of the current chart · `endpoint` gridflow's endpoint absent from the page · `no-silver` · "
          "`registry` · `vault-coverage` · `silver-vs-code`.", ""]
    stubs = [d for d in out if d["stub"]]
    gb = sorted({d["dataset"] for d in out for i in d["items"]
                 if i["kind"] == "page-sample-value" and "10YGB" in i["text"] and d["dataset"].startswith("entsoe/")})
    seeded = sum(1 for d in out for i in d["items"] if i["kind"] == "chart" and i["where"] != "chart-series.json")
    cat_mean = sorted(d["dataset"] for d in out for i in d["items"]
                      if i["where"] == "chart-series.json" and "categorical" in i["text"])
    md += ["## Cross-cutting findings", "",
           f"- **ENTSO-E pages show GB rows that silver never has ({len(gb)} pages).** Local ENTSO-E silver holds "
           "no `10YGB----------A` area rows for load, generation or prices (zones present: DE-LU, BE, FR, NL, "
           "IE-SEM); GB appears only as one side of a border (e.g. `cross_border_flows.in_area_code`). The pages' sample rows put "
           "GB codes in columns where silver has none: " + ", ".join(gb) + ".",
           f"- **Charts:** {seeded} rendered pages carry a seeded or 'illustrative' chart; every chart-series.json "
           "entry comes from the 2026-08 one-off extract, and "
           f"{len(cat_mean)} of them average across a categorical dimension (fuel, zone, unit): "
           + ", ".join(cat_mean) + ".", ""]
    md += ["## Headline items (Phase 26 must fix these first)", ""]
    for d in out:
        for i in d["items"]:
            if i["kind"] in ("page-sample-value", "page-code-list", "mirror-stale", "vault-schema", "registry", "vault-coverage"):
                md.append(f"- **{d['dataset']}** [{i['kind']}] {i['text']}")
    md += ["", "## Per dataset (full list)", ""]
    for d in out:
        if d["stub"]:
            continue
        md.append(f"### {d['dataset']}")
        for i in d["items"]:
            md.append(f"- [{i['kind']}] ({i['where']}) {i['text']}")
        md.append("")
    md += [f"## Coming-soon stubs ({len(stubs)})", "",
           "All are NESO Data Portal landing links with no vault note and no gridflow connector: "
           + ", ".join(d["dataset"].split("/")[1] for d in stubs) + ".", "",
           "## Systemic vault gaps (candidate vault units, not per-dataset fixes)", ""]
    for k, v in systemic.items():
        md.append(f"- **{k}** ({len(v)}): " + ", ".join(v))
    (V5 / "DISCREPANCIES.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps({"datasets_with_items": len(out), "kinds": kinds, "systemic": {k: len(v) for k, v in systemic.items()}}, indent=1))


if __name__ == "__main__":
    main()
