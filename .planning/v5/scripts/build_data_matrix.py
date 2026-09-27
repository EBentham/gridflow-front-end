"""Build the v5 Phase 22 provenance matrix (DATA-MATRIX.json + DATA-MATRIX.md).

One row per dataset across four sources of truth: gridflow code (registry, connector,
silver schema), local silver data under C:\\gridflow-data\\silver, the canonical vault
note (quant-vault ``master`` blobs, never the working tree, whose Windows checkout
carries CRLF line endings), and the front-end artefacts (vault mirror, chart-series.json,
authored-pages overrides, rendered pages / coming-soon stubs).

Offline only: no vendor API is called. The gridflow registry is read by importing
gridflow inside its own venv (subprocess), so this script needs only stdlib + polars:

    uv run --with polars --with pyyaml python .planning/v5/scripts/build_data_matrix.py

Env overrides: GRIDFLOW_REPO, QUANT_VAULT, GRIDFLOW_DATA_DIR, VAULT_REF (default master),
MATRIX_OUT_DIR (default .planning/v5).
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import polars as pl

FE = Path(__file__).resolve().parents[3]
GRIDFLOW = Path(os.environ.get("GRIDFLOW_REPO", r"C:\Users\Bobbo\OneDrive\Desktop\Python\gridflow"))
VAULT = Path(os.environ.get("QUANT_VAULT", r"C:\Users\Bobbo\OneDrive\Desktop\Learning\AI\quant-vault"))
DATA = Path(os.environ.get("GRIDFLOW_DATA_DIR", r"C:\gridflow-data"))
VAULT_REF = os.environ.get("VAULT_REF", "master")
OUT = Path(os.environ.get("MATRIX_OUT_DIR", FE / ".planning" / "v5"))

# vault vendor folder -> site vendor folder (the mirror / authored-pages / data-sources name)
VAULT_TO_SITE = {
    "elexon": "elexon",
    "entsoe": "entsoe",
    "entsog": "entsog",
    "gie": "gie",
    "neso": "neso",
    "neso-data-portal": "neso_data_portal",
    "open-meteo": "openmeteo",
}
# gridflow source key -> site vendor folder
SOURCE_TO_SITE = {
    "elexon": "elexon",
    "entsoe": "entsoe",
    "entsog": "entsog",
    "gie_agsi": "gie",
    "gie_alsi": "gie",
    "neso": "neso",
    "neso_data_portal": "neso_data_portal",
    "open_meteo": "openmeteo",
}
# The NESO Data Portal vault notes use the portal's hyphenated slugs; gridflow and the
# site use their own underscore keys. The note frontmatter dataset_key confirms the map.
NDP_SLUG = {
    "daily-wind-availability": "daily_wind_availability",
    "embedded-wind-and-solar-forecasts": "embedded_wind_solar_forecast",
    "historic-generation-mix": "historic_generation_mix",
}

HEADER_CELLS = {"field", "column", "name", "silver column", "column name"}
# Infrastructure columns gridflow adds to every silver table (schema_manifest.BITEMPORAL_EXCLUDE
# plus the partition keys); the vault's validator also ignores them.
# Bitemporal columns added to the pydantic schemas after the vault validator's 2026-06-15 run;
# a table that differs only in these is reported separately from a substantive difference.
SOFT_BITEMPORAL = {"published_at", "ingested_at"}
INFRA_COLS = {"event_time", "available_at", "vintage_policy", "source_run_id", "dataset_version", "month", "year"}

REGISTRY_DUMP = r'''
import json, inspect, importlib, pkgutil, sys
from pathlib import Path
import yaml
from gridflow.silver import schema_manifest as sm
from gridflow.silver.registry import list_transformers, get_transformer_class
from gridflow.connectors import registry as creg
import gridflow.connectors as C
sm._ensure_silver_transformers_registered()
for m in pkgutil.walk_packages(C.__path__, "gridflow.connectors."):
    try:
        importlib.import_module(m.name)
    except Exception as e:  # noqa: BLE001 - report, never abort the dump
        print("IMPORTFAIL", m.name, e, file=sys.stderr)
def rel(p):
    p = str(p).replace("\\", "/")
    return p.split("/src/", 1)[-1] if "/src/" in p else p
out = {"transformers": [], "connectors": {}, "sources_yaml": {}}
for s, d in sorted(list_transformers()):
    cls = get_transformer_class(s, d)
    sc = None
    try:
        sc = cls(Path("__schema_manifest__")).schema_cls
    except Exception:
        sc = getattr(cls, "schema_cls", None)
    try:
        date_col = sm._date_col_for(s, d)
    except Exception as e:
        date_col = None
    out["transformers"].append({
        "source": s, "dataset": d,
        "transformer": f"{cls.__module__}.{cls.__name__}",
        "transformer_file": rel(inspect.getsourcefile(cls)),
        "schema": f"{sc.__module__}.{sc.__name__}" if sc else None,
        "schema_file": rel(inspect.getsourcefile(sc)) if sc else None,
        "columns": list(sc.model_fields) if sc else None,
        "date_col": date_col,
        "append_only": bool(getattr(cls, "APPEND_ONLY", False)),
        "reference_dataset": bool(getattr(cls, "reference_dataset", False)),
    })
for name in creg.list_sources():
    cls = creg._REGISTRY[name]
    out["connectors"][name] = {
        "class": f"{cls.__module__}.{cls.__name__}",
        "file": rel(inspect.getsourcefile(cls)),
        "snapshot_only": bool(getattr(cls, "SNAPSHOT_ONLY", False)),
    }
y = yaml.safe_load(open("config/sources.yaml", encoding="utf-8"))
for src, cfg in y["sources"].items():
    out["sources_yaml"][src] = {
        "api_key_env": cfg.get("api_key_env") or "",
        "datasets": {k: {kk: vv for kk, vv in (v or {}).items() if isinstance(vv, (str, int, float, bool))}
                     for k, v in (cfg.get("datasets") or {}).items()},
    }
print(json.dumps(out))
'''


def gridflow_registry() -> dict[str, Any]:
    """Import gridflow in its own venv and return its registries as JSON."""
    py = GRIDFLOW / ".venv" / "Scripts" / "python.exe"
    if not py.exists():
        py = GRIDFLOW / ".venv" / "bin" / "python"
    res = subprocess.run([str(py), "-c", REGISTRY_DUMP], cwd=GRIDFLOW, capture_output=True, text=True, check=True)
    return json.loads(res.stdout.strip().splitlines()[-1])


def git(*args: str) -> bytes:
    return subprocess.run(["git", "-C", str(VAULT), *args], capture_output=True, check=True).stdout


def vault_notes() -> dict[tuple[str, str], dict[str, Any]]:
    """Read every canonical dataset note from the vault ref (default master)."""
    sha = git("rev-parse", VAULT_REF).decode().strip()
    paths = git("ls-tree", "-r", "--name-only", VAULT_REF, "30-vendors/").decode().splitlines()
    notes: dict[tuple[str, str], dict[str, Any]] = {}
    for p in paths:
        m = re.fullmatch(r"30-vendors/([^/]+)/datasets/([^/]+)\.md", p)
        if not m or m.group(2) == "README":
            continue
        vendor, slug = m.groups()
        raw = git("show", f"{VAULT_REF}:{p}")
        notes[(vendor, slug)] = {"path": p, "raw": raw, **parse_note(raw.decode("utf-8", "replace"))}
    return {"_sha": sha, **{k: v for k, v in notes.items()}}  # type: ignore[dict-item]


def parse_note(text: str) -> dict[str, Any]:
    fm: dict[str, str] = {}
    body = text
    m = re.match(r"^---\n(.*?)\n---\n", text.replace("\r\n", "\n"), re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            mm = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
            if mm:
                fm[mm.group(1)] = mm.group(2).strip().strip('"')
        body = text.replace("\r\n", "\n")[m.end():]
    lines = body.split("\n")
    heads: list[str] = []
    in_code = False
    for ln in lines:
        if ln.startswith("```"):
            in_code = not in_code
            continue
        if not in_code and re.match(r"^#{2,3} ", ln):
            heads.append(ln.strip("# ").strip())
    schema_cols: list[str] | None = None
    range_notation = False
    for i, ln in enumerate(lines):
        if re.match(r"^###\s+Silver schema", ln):
            cols: list[str] = []
            j = i + 1
            while j < len(lines) and not lines[j].lstrip().startswith("|"):
                if lines[j].startswith("#"):
                    break
                j += 1
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                first = (cells[0] if cells else "").strip().strip("`").strip()
                if first and not set(first) <= set("-: ") and first.lower() not in HEADER_CELLS:
                    if "…" in first or "..." in first:
                        range_notation = True
                    cols.append(first.split()[0].strip("`*"))
                j += 1
            schema_cols = cols or None
            break
    overview = ""
    if "## Overview" in body:
        seg = body.split("## Overview", 1)[1].split("\n## ", 1)[0].strip()
        overview = re.sub(r"\s+", " ", seg)[:400]
    return {
        "frontmatter": fm,
        "sections": heads,
        "has_silver_section": any(h.startswith("Silver layer") for h in heads),
        "has_silver_schema_heading": any(h.startswith("Silver schema") for h in heads),
        "vault_schema_cols": schema_cols,
        "vault_schema_range_notation": range_notation,
        "overview": overview,
    }


def silver_stats(source: str, dataset: str, date_col: str | None) -> dict[str, Any] | None:
    root = DATA / "silver" / source / dataset
    if not root.is_dir():
        return None
    files = sorted(root.rglob("*.parquet"))
    if not files:
        return {"files": 0, "rows": 0}
    info: dict[str, Any] = {"files": len(files)}
    try:
        cols = list(pl.read_parquet_schema(files[-1]).keys())
    except Exception as e:  # noqa: BLE001
        return {"files": len(files), "error": f"schema read: {e}"}
    info["columns"] = cols
    dc = date_col if date_col in cols else next(
        (c for c in ("settlement_date", "gas_day", "timestamp_utc", "period_start_utc", "date") if c in cols), None
    )
    info["date_col"] = dc
    rows = 0
    lo = hi = None
    try:
        exprs = [pl.len().alias("n")]
        if dc:
            exprs += [pl.col(dc).min().cast(pl.String).alias("lo"), pl.col(dc).max().cast(pl.String).alias("hi")]
        r = pl.scan_parquet(files, hive_partitioning=False).select(exprs).collect().row(0, named=True)
        rows, lo, hi = r["n"], r.get("lo"), r.get("hi")
    except Exception:  # noqa: BLE001 - schema drift across files; fall back per file
        for f in files:
            try:
                sch = pl.read_parquet_schema(f)
                e2 = [pl.len().alias("n")]
                if dc and dc in sch:
                    e2 += [pl.col(dc).min().cast(pl.String).alias("lo"), pl.col(dc).max().cast(pl.String).alias("hi")]
                r = pl.scan_parquet(f, hive_partitioning=False).select(e2).collect().row(0, named=True)
                rows += r["n"]
                if r.get("lo") is not None:
                    lo = r["lo"] if lo is None else min(lo, r["lo"])
                    hi = r["hi"] if hi is None else max(hi, r["hi"])
            except Exception as e:  # noqa: BLE001
                info.setdefault("file_errors", []).append(f"{f.name}: {e}"[:200])
    info.update(rows=rows, first=lo, last=hi)
    info["newest_file_mtime"] = datetime.fromtimestamp(max(f.stat().st_mtime for f in files), UTC).strftime(
        "%Y-%m-%dT%H:%MZ"
    )
    return info


def validation_by_note() -> tuple[str | None, dict[str, dict[str, Any]]]:
    """Per-note curl and silver-schema status from the vault's last validator run."""
    try:
        d = json.loads(git("show", f"{VAULT_REF}:30-vendors/vault-curl-schema-validation.json"))
    except subprocess.CalledProcessError:
        return None, {}
    out: dict[str, dict[str, Any]] = defaultdict(lambda: {"curl": [], "schema": None})
    for c in d.get("curl_examples", []):
        out[c["relative_path"].replace("\\", "/")]["curl"].append(c["status"])
    for s in d.get("silver_schema_checks", []):
        out[s["relative_path"].replace("\\", "/")]["schema"] = s["status"]
    return d.get("generated_at"), dict(out)


def rendered_pages() -> dict[tuple[str, str], dict[str, Any]]:
    base = FE / "site" / "hifi" / "data-sources"
    pages: dict[tuple[str, str], dict[str, Any]] = {}
    for f in base.glob("*/*.html"):
        t = f.read_text(encoding="utf-8", errors="replace")
        stub = bool(re.search(r'data-screen-label="Dataset[^"]*· planned"', t))
        pages[(f.parent.name, f.stem)] = {
            "stub": stub,
            "seeded_chart": "seeded" in t.lower(),
            "illustrative": "illustrative" in t.lower(),
        }
    return pages


def main() -> None:
    reg = gridflow_registry()
    notes = vault_notes()
    vault_sha = notes.pop("_sha")  # type: ignore[arg-type]
    val_at, val = validation_by_note()
    pages = rendered_pages()
    chart = json.loads((FE / "site" / "hifi" / "data" / "chart-series.json").read_text(encoding="utf-8"))
    chart_keys = set(chart.get("series", {}))
    authored = {(p.parent.name, p.stem) for p in (FE / "authored-pages").glob("*/*.html") if not p.stem.startswith("_")}
    mirror_root = FE / "vault"

    yaml_ds = {(s, d): cfg for s, v in reg["sources_yaml"].items() for d, cfg in v["datasets"].items()}
    tr = {(t["source"], t["dataset"]): t for t in reg["transformers"]}

    # key every row by (site vendor, page slug)
    rows: dict[tuple[str, str], dict[str, Any]] = {}

    def row(site_vendor: str, slug: str) -> dict[str, Any]:
        return rows.setdefault((site_vendor, slug), {"vendor": site_vendor, "slug": slug})

    for (vv, vslug), n in notes.items():
        sv = VAULT_TO_SITE[vv]
        slug = NDP_SLUG.get(vslug, vslug) if vv == "neso-data-portal" else vslug
        r = row(sv, slug)
        fm = n["frontmatter"]
        mirror_path = mirror_root / sv / f"{slug}.md"
        mirror_bytes = mirror_path.read_bytes() if mirror_path.exists() else None
        v = val.get(f"{vv}/datasets/{vslug}.md", {})
        r["vault"] = {
            "path": n["path"],
            "source": fm.get("source"),
            "dataset_key": fm.get("dataset_key"),
            "last_verified": fm.get("last_verified"),
            "layer_coverage": fm.get("layer_coverage"),
            "sections": n["sections"],
            "has_silver_section": n["has_silver_section"],
            "has_silver_schema_table": bool(n["vault_schema_cols"]),
            "vault_schema_cols": n["vault_schema_cols"],
            "vault_schema_range_notation": n["vault_schema_range_notation"],
            "overview": n["overview"],
            "validator_2026_06_15": {"curl": v.get("curl", []), "schema": v.get("schema")} if v else None,
        }
        r["mirror"] = {
            "path": f"vault/{sv}/{slug}.md",
            "present": mirror_bytes is not None,
            "byte_identical": mirror_bytes == n["raw"] if mirror_bytes is not None else False,
        }
    for (s, d) in set(yaml_ds) | set(tr):
        row(SOURCE_TO_SITE[s], d).setdefault("gridflow_keys", []).append(f"{s}/{d}")
    for (sv, slug), p in pages.items():
        row(sv, slug)["page"] = {"path": f"site/hifi/data-sources/{sv}/{slug}.html", **p}

    for (sv, slug), r in rows.items():
        keys = r.get("gridflow_keys", [])
        gk = keys[0] if keys else None
        src, ds = gk.split("/") if gk else (None, None)
        t = tr.get((src, ds)) if gk else None
        y = yaml_ds.get((src, ds)) if gk else None
        conn = reg["connectors"].get(src) if src else None
        r["gridflow"] = {
            "key": gk,
            "in_sources_yaml": y is not None,
            "endpoint": (y or {}).get("endpoint") or (y or {}).get("document_type"),
            "connector": conn["file"] if conn else None,
            "connector_class": conn["class"] if conn else None,
            "snapshot_only_connector": conn["snapshot_only"] if conn else None,
            "api_key_env": reg["sources_yaml"].get(src, {}).get("api_key_env") if src else None,
            "has_transformer": t is not None,
            "transformer": t["transformer"] if t else None,
            "transformer_file": t["transformer_file"] if t else None,
            "schema": t["schema"] if t else None,
            "schema_file": t["schema_file"] if t else None,
            "schema_cols": t["columns"] if t else None,
            "date_col": t["date_col"] if t else None,
        }
        s = silver_stats(src, ds, t["date_col"] if t else None) if gk else None
        r["silver"] = s or {"files": 0, "rows": 0}
        r["silver_present"] = bool(s and s.get("rows", 0) > 0)
        # vault schema table vs gridflow pydantic schema (offline comparison)
        vcols = (r.get("vault") or {}).get("vault_schema_cols")
        n_range = (r.get("vault") or {}).get("vault_schema_range_notation", False)
        ccols = t["columns"] if t else None
        # Dynamic-schema transformers (no pydantic class) are compared against the actual
        # silver parquet columns instead; the basis is recorded.
        basis = "pydantic"
        if ccols is None and r["silver"].get("columns"):
            ccols, basis = r["silver"]["columns"], "silver_parquet"
        if not r.get("vault"):
            r["vault_vs_code_schema"] = {"status": "n/a"}
        elif vcols is None:
            r["vault_vs_code_schema"] = {"status": "no_vault_table" if r["vault"]["has_silver_section"] else "no_silver_section"}
        elif ccols is None:
            r["vault_vs_code_schema"] = {"status": "no_code_schema_or_silver"}
        else:
            miss = [c for c in ccols if c not in vcols and c not in INFRA_COLS]
            extra = [c for c in vcols if c not in ccols and c not in INFRA_COLS]
            if not miss and not extra:
                status = "match"
            elif set(miss) | set(extra) <= SOFT_BITEMPORAL:
                status = "bitemporal_only"
            elif n_range:
                status = "range_notation"
            else:
                status = "differs"
            r["vault_vs_code_schema"] = {"status": status, "basis": basis,
                                         "missing_in_vault": miss, "extra_in_vault": extra}
        # actual silver parquet columns vs code schema
        scols = r["silver"].get("columns")
        if scols and ccols:
            r["silver_vs_code_schema"] = {
                "missing_in_silver": [c for c in ccols if c not in scols],
                "extra_in_silver": [c for c in scols if c not in ccols],
            }
        r["chart_series"] = f"{sv}/{slug}" in chart_keys
        r["authored_override"] = (sv, slug) in authored
        r["stub"] = bool((r.get("page") or {}).get("stub"))
        # registry vs vault agreement
        has_note, in_code = bool(r.get("vault")), bool(gk)
        if has_note and in_code and r["gridflow"]["in_sources_yaml"] and r["gridflow"]["has_transformer"]:
            agree = "agree"
        elif has_note and in_code:
            agree = "partial: " + ", ".join(
                x for x, ok in (("not in sources.yaml", r["gridflow"]["in_sources_yaml"]),
                                ("no silver transformer", r["gridflow"]["has_transformer"])) if not ok
            )
        elif has_note:
            agree = "vault only (gridflow has no config or transformer)"
        elif in_code:
            agree = "gridflow only (no vault note)"
        else:
            agree = "site only (no vault note, not in gridflow)"
        r["registry_vs_vault"] = agree

    ordered = [rows[k] for k in sorted(rows)]
    vault_rows = [r for r in ordered if r.get("vault")]
    summary = {
        "generated_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "vault_ref": VAULT_REF,
        "vault_sha": vault_sha,
        "validator_last_run": val_at,
        "rows_total": len(ordered),
        "vault_notes": len(vault_rows),
        "vault_notes_by_vendor": dict(Counter(r["vendor"] for r in vault_rows)),
        "silver_present_of_vault": sum(r["silver_present"] for r in vault_rows),
        "silver_present_by_vendor": {
            v: f"{sum(r['silver_present'] for r in vault_rows if r['vendor'] == v)}/{c}"
            for v, c in Counter(r["vendor"] for r in vault_rows).items()
        },
        "gridflow_sources_yaml": len(yaml_ds),
        "gridflow_transformers": len(tr),
        "chart_series": sum(r["chart_series"] for r in ordered),
        "authored_overrides": sum(r["authored_override"] for r in ordered),
        "rendered_pages": sum(1 for r in ordered if r.get("page")),
        "stubs": sum(r["stub"] for r in ordered),
        "mirror_byte_identical": sum(1 for r in vault_rows if r["mirror"]["byte_identical"]),
        "mirror_differs": sum(1 for r in vault_rows if not r["mirror"]["byte_identical"]),
        "registry_vs_vault": dict(Counter(r["registry_vs_vault"] for r in ordered)),
        "vault_vs_code_schema": dict(Counter(r["vault_vs_code_schema"]["status"] for r in vault_rows)),
        "notes_without_silver_section": [f"{r['vendor']}/{r['slug']}" for r in vault_rows if not r["vault"]["has_silver_section"]],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "DATA-MATRIX.json").write_text(
        json.dumps({"summary": summary, "rows": ordered}, indent=1, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8",
    )
    (OUT / "DATA-MATRIX.md").write_text(render_md(summary, ordered), encoding="utf-8")
    print(json.dumps(summary, indent=1))


def yn(b: bool) -> str:
    return "y" if b else "n"


def render_md(s: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    out = [
        "# v5 data matrix (Phase 22)",
        "",
        f"Generated {s['generated_at']} by `.planning/v5/scripts/build_data_matrix.py` (offline; no vendor API "
        f"calls). Canonical vault = quant-vault `{s['vault_ref']}` @ `{s['vault_sha'][:9]}`. Silver = "
        f"`{DATA}\\silver`. Machine-readable twin: `DATA-MATRIX.json` (full columns, schema diffs, sections).",
        "",
        "## Headline",
        "",
        f"- Vault dataset notes: **{s['vault_notes']}** ({', '.join(f'{k} {v}' for k, v in sorted(s['vault_notes_by_vendor'].items()))}).",
        f"- Notes with local silver: **{s['silver_present_of_vault']}/{s['vault_notes']}** "
        f"({', '.join(f'{k} {v}' for k, v in sorted(s['silver_present_by_vendor'].items()))}).",
        f"- gridflow: {s['gridflow_sources_yaml']} datasets in `config/sources.yaml`, {s['gridflow_transformers']} silver transformers.",
        "- Registry vs vault: " + "; ".join(f"{k}: {v}" for k, v in sorted(s["registry_vs_vault"].items())) + ".",
        "- Vault silver-schema table vs gridflow pydantic schema: "
        + "; ".join(f"{k}: {v}" for k, v in sorted(s["vault_vs_code_schema"].items())) + ".",
        f"- Chart series: {s['chart_series']}. Authored overrides: {s['authored_overrides']}. Rendered pages: "
        f"{s['rendered_pages']} (of which coming-soon stubs: {s['stubs']}).",
        f"- Mirror byte-identical to canonical `{s['vault_ref']}`: {s['mirror_byte_identical']}; differs: {s['mirror_differs']}.",
        f"- Vault validator last run: {s['validator_last_run']}.",
        "",
        "Columns: **cfg** in `sources.yaml` · **tr** silver transformer · **silver** rows / first / last "
        "(designated date column) · **lv** vault `last_verified` · **vs** vault schema table vs code "
        "(`=` match, `≈` differs only in published_at/ingested_at, `=*` range-notation table, `≠` differs, "
        "`–` no table, `?` nothing to compare) · **mir** mirror byte-identical · **ch** chart series · "
        "**ov** authored override · **stub** coming-soon stub · **agree** registry vs vault.",
        "",
    ]
    vs_sym = {"match": "=", "differs": "≠", "bitemporal_only": "≈", "range_notation": "=*", "no_vault_table": "–", "no_silver_section": "–",
              "no_code_schema_or_silver": "?", "n/a": ""}
    for vendor in sorted({r["vendor"] for r in rows}):
        vr = [r for r in rows if r["vendor"] == vendor]
        out += [f"## {vendor} ({len(vr)} rows)", "",
                "| dataset | gridflow key | cfg | tr | schema class | silver rows | first | last | lv | vs | mir | ch | ov | stub | agree |",
                "|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|"]
        for r in vr:
            g, sv, v = r["gridflow"], r["silver"], r.get("vault") or {}
            schema = (g["schema"] or "").rsplit(".", 1)[-1] or ("dynamic" if g["has_transformer"] else "")
            out.append(
                f"| {r['slug']} | {g['key'] or ''} | {yn(g['in_sources_yaml'])} | {yn(g['has_transformer'])} | "
                f"{schema} | {sv.get('rows', 0):,} | {(sv.get('first') or '')[:10]} | {(sv.get('last') or '')[:10]} | "
                f"{v.get('last_verified', '') if v else 'no note'} | {vs_sym.get(r['vault_vs_code_schema']['status'], '')} | "
                f"{yn(r['mirror']['byte_identical']) if r.get('mirror') else ''} | {yn(r['chart_series'])} | "
                f"{yn(r['authored_override'])} | {yn(r['stub'])} | {r['registry_vs_vault']} |"
            )
        out.append("")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    sys.exit(main())
