"""gridflow-build — render dataset pages from Obsidian Vault markdown.

Reads vault `.md` files under `<vault>/elexon/*.md`, parses YAML frontmatter
and the structured sections (Overview, API endpoint, Silver layer, Known
issues, etc.), and renders one HTML file per dataset using Jinja2 templates
under `templates/`. Also rebuilds the vendor hub (`site/hifi/data-sources/elexon.html`)
from the manifest at `site/hifi/data/elexon.json`.

Build inputs (single source of truth):
- vault/<vendor>/<slug>.md       — authored content (frontmatter + sections)
- site/hifi/data/<vendor>.json   — structural manifest (id/title/freq/lag/rows)

Build outputs (gitignored, regenerated on every run):
- site/hifi/data-sources/<vendor>/<slug>.html
- site/hifi/data-sources/<vendor>.html

The deployed artefact stays pure static HTML/CSS/JS — Jinja2 is a build-time
dependency only (declared in pyproject.toml's [build] extras).

Usage
-----
    gridflow-build                                  # build everything
    gridflow-build --vault-path /path/to/vault      # override vault location
    gridflow-build --check                          # build twice; non-zero on drift

Vault path resolution order:
    1. --vault-path CLI flag
    2. $GRIDFLOW_VAULT_PATH env var
    3. <repo>/vault/ (vendored fallback)

Snapshot-chart data is a separate, occasional step:

    gridflow-build --refresh-chart-data          # re-distil site/hifi/data/chart-series.json

That command reads a local gridflow extract and rewrites the committed
``site/hifi/data/chart-series.json``; ordinary builds only ever read that file.
See ``chart_data`` for why the read is split in two — CI builds from a bare
checkout and cannot see the extract.
"""

from __future__ import annotations

import argparse
import filecmp
import json
import os
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass, field
from html import escape as html_escape
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from gridflow_front_end import chart_data

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = REPO_ROOT / "templates"
SITE_DIR = REPO_ROOT / "site" / "hifi"
DEFAULT_VAULT = REPO_ROOT / "vault"
AUTHORED_DIR = REPO_ROOT / "authored-pages"


# ──────────────────────────────────────────────────────────────────────
# Vendor configuration — drives both real hubs and coming-soon stubs.
# ──────────────────────────────────────────────────────────────────────


REAL_VENDORS: dict[str, dict] = {
    "elexon": {
        "label": "Elexon BMRS",
        "vendor_doc_base": "https://bmrs.elexon.co.uk/api-documentation/endpoint/datasets/",
        "vendor_meta": {
            "region": "United Kingdom",
            "domain": "Electricity",
            "heading_prefix": "Elexon",
            "heading_italic": "BMRS.",
            "lede": (
                "The British electricity Balancing Mechanism Reporting Service. Settlement "
                "prices, generation by fuel, demand outturn, balancing actions, and BM unit "
                "metadata — documented as a static reference site over the gridflow ETL "
                "pipeline."
            ),
            "vendor_docs_url": "https://bmrs.elexon.co.uk/",
            "base_url": "data.elexon.co.uk/bmrs/api/v1",
            "auth": "Public · no key required",
            "rate_limit": "2 req/s · project default",
            "format": "JSON · ISO-8601 · UTC",
            "earliest": "2014-04-01",
            "timezone": "UTC · SP 1–50",
            "stat_three_value": "7",
            "stat_three_label": "Settlement runs · II → DF",
            "stat_four_value": "11y",
            "stat_four_label": "History",
        },
    },
    "entsoe": {
        "label": "ENTSO-E Transparency",
        "vendor_doc_base": "https://transparency.entsoe.eu/",
        "vendor_meta": {
            "region": "European Union",
            "domain": "Electricity",
            "heading_prefix": "ENTSO-E",
            "heading_italic": "Transparency.",
            "lede": (
                "The pan-European transmission system operators' Transparency Platform. "
                "Day-ahead prices, actual generation per production type, cross-border flows, "
                "forecasts, and outages across EU bidding zones — cross-vendor proof for the "
                "documentation template."
            ),
            "vendor_docs_url": "https://transparency.entsoe.eu/",
            "base_url": "web-api.tp.entsoe.eu",
            "auth": "API key · query param securityToken",
            "rate_limit": "~1 req/s · polite default",
            "format": "XML · GL_MarketDocument",
            "earliest": "2014-12-05",
            "timezone": "UTC · PT15M / PT30M / PT60M",
            "stat_three_value": "B25",
            "stat_three_label": "PSR types · production codes",
            "stat_four_value": "EU",
            "stat_four_label": "Bidding zones",
        },
    },
    "entsog": {
        "label": "ENTSO-G Transparency",
        "vendor_doc_base": "https://transparency.entsog.eu/",
        "vendor_meta": {
            "region": "European Union",
            "domain": "Gas",
            "heading_prefix": "ENTSO-G",
            "heading_italic": "Transparency.",
            "lede": (
                "The European Network of Transmission System Operators for Gas "
                "Transparency Platform. Point-level operational flows, nominations, "
                "capacities, CMP data, and network topology for European gas "
                "interconnections — public API, no authentication, 33 endpoints "
                "covering GB interconnection points (Bacton IUK/BBL, Moffat)."
            ),
            "vendor_docs_url": "https://transparency.entsog.eu/",
            "base_url": "transparency.entsog.eu/api/v1",
            "auth": "Public · no key required",
            "rate_limit": "5 req/s · project default",
            "format": "JSON · ISO-8601 · timeZone:UCT",
            "earliest": "2010",
            "timezone": "UCT · day periods",
            "stat_three_value": "9",
            "stat_three_label": "GB interconnection points",
            "stat_four_value": "1",
            "stat_four_label": "Typed schema · 32 dynamic",
        },
    },
    "gie": {
        "label": "GIE",
        "vendor_doc_base": "https://agsi.gie.eu/",
        "vendor_meta": {
            "region": "European Union",
            "domain": "Gas storage · LNG",
            "heading_prefix": "GIE",
            "heading_italic": "Storage.",
            "lede": (
                "Gas Infrastructure Europe — the trade association for European gas "
                "storage and LNG operators. AGSI+ publishes daily underground storage "
                "levels by country and facility from 2011; ALSI publishes daily LNG "
                "terminal inventories and send-out across the same footprint. Both "
                "share a single x-key authentication model on separate hosts."
            ),
            "vendor_docs_url": "https://agsi.gie.eu/",
            "base_url": "agsi.gie.eu · alsi.gie.eu",
            "auth": "API key · x-key request header",
            "rate_limit": "1 req/s · 60 req/min cap",
            "format": "JSON · gas day (06:00 UTC)",
            "earliest": "2011-01-01",
            "timezone": "UTC · daily gas-day grain",
            "stat_three_value": "9",
            "stat_three_label": "AGSI countries",
            "stat_four_value": "2011",
            "stat_four_label": "Storage depth",
        },
    },
    "neso": {
        "label": "NESO Carbon Intensity",
        "vendor_doc_base": "https://carbonintensity.org.uk/",
        "vendor_meta": {
            "region": "United Kingdom",
            "domain": "Carbon",
            "heading_prefix": "NESO",
            "heading_italic": "Carbon.",
            "lede": (
                "The National Energy System Operator's Carbon Intensity API (formerly "
                "National Grid ESO), built with the Environmental Defense Fund Europe "
                "and University of Oxford. Half-hourly forecast and actual carbon "
                "intensity of the GB grid in gCO₂/kWh, with national, statistical, "
                "generation-mix, and regional (DNO / postcode) breakdowns. Public, "
                "no key required."
            ),
            "vendor_docs_url": "https://carbonintensity.org.uk/",
            "base_url": "api.carbonintensity.org.uk",
            "auth": "Public · no key required",
            "rate_limit": "10 req/s · project default",
            "format": "JSON · ISO-8601 · UTC",
            "earliest": "2018-01",
            "timezone": "UTC · 30-min settlement periods",
            "stat_three_value": "48h",
            "stat_three_label": "Forecast horizon",
            "stat_four_value": "gCO₂/kWh",
            "stat_four_label": "Reporting unit",
        },
    },
    "openmeteo": {
        "label": "Open-Meteo",
        "vendor_doc_base": "https://open-meteo.com/en/docs",
        "vendor_meta": {
            "region": "Global",
            "domain": "Weather",
            "heading_prefix": "Open-Meteo",
            "heading_italic": "Weather.",
            "lede": (
                "An open-source weather API aggregating ECMWF, GFS, and ERA5 "
                "reanalysis into a single columnar JSON interface. No authentication "
                "required for non-commercial use. Six datasets covering hourly "
                "temperature, wind, and solar irradiance across GB population centres "
                "and capacity-weighted generation sites — 1–16-day forecasts and "
                "ERA5-backed archive to 1940."
            ),
            "vendor_docs_url": "https://open-meteo.com/en/docs",
            "base_url": "api.open-meteo.com/v1 · archive-api.open-meteo.com/v1",
            "auth": "Public · no key required",
            "rate_limit": "5 req/s · ~10 000 req/day",
            "format": "JSON · ISO-8601 · UTC",
            "earliest": "1940-01-01 · ERA5",
            "timezone": "UTC · hourly resolution",
            "stat_three_value": "1940",
            "stat_three_label": "ERA5 depth",
            "stat_four_value": "25",
            "stat_four_label": "GB sites",
        },
    },
    "neso_data_portal": {
        "label": "NESO Data Portal",
        "vendor_doc_base": "https://www.neso.energy/data-portal/api-guidance",
        "vendor_meta": {
            "region": "United Kingdom",
            "domain": "Electricity",
            "heading_prefix": "NESO",
            "heading_italic": "Data Portal.",
            "lede": (
                "The National Energy System Operator's general open-data catalogue — a "
                "CKAN file-download platform distinct from the existing NESO Carbon "
                "Intensity API. Per-BMU wind availability forecasts, embedded (sub-"
                "transmission) wind/solar generation forecasts, and a half-hourly GB "
                "generation-mix archive back to 2009. 129 catalogued packages; 3 implemented "
                "so far, 29 more eligible and queued as Planned."
            ),
            "vendor_docs_url": "https://www.neso.energy/data-portal/api-guidance",
            "base_url": "api.neso.energy/api/3/action",
            "auth": "Public · no key required",
            "rate_limit": "1 req/s · CKAN action API (IP-block enforced)",
            "format": "CKAN JSON metadata → CSV file download",
            "earliest": "2009-01-01 · historic_generation_mix",
            "timezone": "UTC · daily / half-hourly grain",
            "stat_three_value": "129",
            "stat_three_label": "CKAN packages catalogued",
            "stat_four_value": "3",
            "stat_four_label": "Implemented so far",
        },
    },
}


# All seven vendors ship real documentation (Phase 10 closed the v2 milestone;
# T-23 added neso_data_portal): elexon, entsoe, entsog, gie, neso, openmeteo,
# neso_data_portal all live in REAL_VENDORS above. Six of them are documented at
# full fidelity — every dataset their landing page links to is implemented.
# neso_data_portal is the exception: it links 29 eligible-but-unbuilt CKAN
# packages, so build_dataset_stubs_from_landings is ACTIVE (see
# _PARTIAL_CONNECTOR_VENDORS below, which keeps those stubs from claiming the
# pipeline already ingests them). This list stays empty — the VENDOR-level
# coming-soon machinery (build_coming_soon_stubs) is retained, dormant,
# for any future vendor that ships ahead of its documentation.
COMING_SOON_VENDORS: list[dict] = []


# ──────────────────────────────────────────────────────────────────────
# Data classes
# ──────────────────────────────────────────────────────────────────────


@dataclass
class SchemaRow:
    name: str
    pk: bool
    type: str
    nullable: bool
    note: str


@dataclass
class Caveat:
    title: str
    text: str


@dataclass
class DatasetDoc:
    slug: str
    vendor_id: str  # "elexon"
    vendor_label: str  # "Elexon BMRS"
    last_verified: str  # "2026-05-08"
    title_line: str  # H1 of the vault doc
    api_code: str  # e.g. "FUELHH"
    overview_paragraphs: list[str] = field(default_factory=list)
    base_url: str = ""
    api_path: str = ""
    auth_note: str = ""
    silver_path: str = ""
    transformer_class: str = ""
    pydantic_schema: str = ""
    dedup_key: str = ""
    point_in_time_field: str = ""
    pydantic_schema_wired: bool = False
    schema_rows: list[SchemaRow] = field(default_factory=list)
    sample_columns: list[str] = field(default_factory=list)
    sample_rows: list[list[str]] = field(default_factory=list)
    sample_language: str = "json"
    sample_raw: str = ""
    caveats: list[Caveat] = field(default_factory=list)
    bronze_path: str = ""

    @property
    def vendor_doc_url(self) -> str:
        """Link to the canonical vendor endpoint reference, derived from vendor config."""
        base = REAL_VENDORS.get(self.vendor_id, {}).get("vendor_doc_base", "")
        if self.vendor_id == "elexon":
            return f"{base}{self.api_code}"
        if self.vendor_id == "entsoe":
            return base  # ENTSO-E TP doesn't have per-dataset URLs
        return base

    @property
    def silver_dir(self) -> str:
        """Directory glob root for the silver layer (drops trailing partition spec)."""
        if not self.silver_path:
            return f"data/silver/elexon/{self.slug}"
        # Truncate at the first `<` or `=` partition marker, or at the filename basename
        head = re.split(r"/[^/]*[=<]", self.silver_path)[0]
        return head.rstrip("/")

    @property
    def first_pk_column(self) -> str:
        """First PK column (for the DuckDB date-filter example)."""
        for row in self.schema_rows:
            if row.pk:
                return row.name
        return "settlement_date"


# ──────────────────────────────────────────────────────────────────────
# Vault parsing
# ──────────────────────────────────────────────────────────────────────


def _parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end].strip()
    body = text[end + 4 :].lstrip("\n")
    frontmatter: dict[str, str] = {}
    for line in fm_text.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            frontmatter[k.strip()] = v.strip()
    return frontmatter, body


_HEADING_RE = re.compile(r"^(#+)\s+(.*?)\s*$", re.MULTILINE)


def _split_sections(body: str) -> dict[str, str]:
    """Split a markdown body into sections keyed by lowercased heading text.

    Recognises any `## Heading` line. Sections include nested `### subheads`
    in their content. Returns ordered dict (insertion order = source order).
    """
    sections: dict[str, str] = {}
    matches = list(re.finditer(r"^##\s+(?P<title>.*?)\s*$", body, re.MULTILINE))
    for i, m in enumerate(matches):
        key = m.group("title").strip().lower()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        sections[key] = body[start:end].strip()
    return sections


def _strip_link(text: str) -> str:
    """Strip markdown links '[a](b)' → 'a'."""
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)


# Link-count telemetry from the most recent `_markdown_inline` pass, keyed by
# outcome. Populated as a module-level counter (rather than threaded through
# every call site) so `build()` can report resolved-vs-plain-text counts for
# vault-relative `.md` links without changing every caller's signature.
_MD_LINK_STATS: dict[str, int] = {"resolved": 0, "plain_text": 0, "fragment_dropped": 0}


def _reset_md_link_stats() -> None:
    _MD_LINK_STATS["resolved"] = 0
    _MD_LINK_STATS["plain_text"] = 0
    _MD_LINK_STATS["fragment_dropped"] = 0


# Section ids that actually exist on a generated dataset page
# (templates/dataset.html.j2) — the only fragments a resolved `.md` link may
# carry, because the deploy gate link-checks fragments (`lychee
# --include-fragments`): an anchor to a heading that only exists in the vault
# source would 404 the fragment and block deployment.
_GENERATED_SECTION_IDS = frozenset(
    {"overview", "snapshot-chart", "schema", "sample", "api", "caveats", "related"}
)

# Vault heading slugs whose content demonstrably lands in a specific generated
# section. Anything not listed here (e.g. `#changelog`, ad-hoc subsection
# anchors) has no generated counterpart: the fragment is dropped and counted,
# and the link points at the page top.
_VAULT_FRAGMENT_TO_SECTION_ID = {
    "known-issues-and-gotchas": "caveats",
    "silver-schema": "schema",
    # Subsection of "Known issues and gotchas" (historical_wind) — its content
    # renders inside the caveats section.
    "archive-10m100m-limitation": "caveats",
}


def _map_fragment(frag: str) -> str | None:
    """Best generated-page anchor for a vault fragment slug, or None."""
    if frag in _GENERATED_SECTION_IDS:
        return frag
    return _VAULT_FRAGMENT_TO_SECTION_ID.get(frag)


# Caveat-extraction telemetry, same shape and lifecycle as `_MD_LINK_STATS`:
# any line inside a "Known issues and gotchas" section that the grammar cannot
# place is COUNTED here rather than silently discarded, and `build()` reports
# a nonzero count at the end of the run.
_CAVEAT_STATS: dict[str, int] = {"dropped_lines": 0}


def _reset_caveat_stats() -> None:
    _CAVEAT_STATS["dropped_lines"] = 0


_MANIFEST_SLUGS_CACHE: dict[str, set[str]] | None = None


def _all_manifest_slugs() -> dict[str, set[str]]:
    """Slug set per vendor, loaded from each vendor's manifest and cached.

    Used to decide whether a vault-relative `.md` link target actually has a
    published dataset page (`site/hifi/data-sources/<vendor>/<slug>.html`).
    """
    global _MANIFEST_SLUGS_CACHE
    if _MANIFEST_SLUGS_CACHE is None:
        cache: dict[str, set[str]] = {}
        for vendor_id in REAL_VENDORS:
            try:
                manifest = load_manifest(vendor_id)
            except FileNotFoundError:
                cache[vendor_id] = set()
                continue
            cache[vendor_id] = {d["id"] for g in manifest["groups"] for d in g["datasets"]}
        _MANIFEST_SLUGS_CACHE = cache
    return _MANIFEST_SLUGS_CACHE


_MD_LINK_TARGET_RE = re.compile(r"^(?P<path>[^#]*\.md)(?P<anchor>#.*)?$")


def _resolve_md_link(target: str, vendor_id: str) -> str | None:
    """Resolve a vault-relative `.md` link to its published dataset-page href.

    Routing shape (see module docstring / `build_vendor`): a vault file at
    `vault/<vendor>/<slug>.md` publishes to
    `site/hifi/data-sources/<vendor>/<slug>.html`, and dataset pages for the
    same vendor sit flat in that vendor's directory, so a same-vendor link
    resolves to `<slug>.html` and a cross-vendor link to
    `../<other-vendor>/<slug>.html` (matching the existing sibling-link and
    vendor-hub href shapes already used by the Jinja templates).

    Recognised shapes: bare `slug.md`, `./slug.md` (same vendor), and
    `../<vendor>/slug.md` (cross-vendor) — each with an optional `#anchor`
    suffix. A fragment survives only if it names a real generated section id,
    directly or via `_VAULT_FRAGMENT_TO_SECTION_ID`; otherwise it is dropped
    (counted in `_MD_LINK_STATS["fragment_dropped"]`) so the deploy gate's
    fragment-aware link check cannot fail on a vault-only heading anchor.
    Anything else (a domain-notes path
    like `../../../20-domain/...`, `../README.md`, or a same/cross-vendor
    slug that isn't in that vendor's manifest — i.e. has no published page)
    returns None so the caller renders plain text instead of a dead link.
    """
    m = _MD_LINK_TARGET_RE.match(target)
    if not m:
        return None
    path, anchor = m.group("path"), m.group("anchor") or ""
    parts = path.split("/")
    if len(parts) == 1 or (len(parts) == 2 and parts[0] == "."):
        target_vendor = vendor_id
        slug = Path(parts[-1]).stem
    elif len(parts) == 3 and parts[0] == ".." and parts[1] in REAL_VENDORS:
        target_vendor = parts[1]
        slug = Path(parts[2]).stem
    else:
        return None
    if slug not in _all_manifest_slugs().get(target_vendor, set()):
        return None
    if anchor:
        mapped = _map_fragment(anchor[1:])
        if mapped:
            anchor = f"#{mapped}"
        else:
            # Cross-page link stays useful without its fragment: keep the
            # page target, drop the vault-only anchor.
            _MD_LINK_STATS["fragment_dropped"] += 1
            anchor = ""
    if target_vendor == vendor_id:
        return f"{slug}.html{anchor}"
    return f"../{target_vendor}/{slug}.html{anchor}"


_URI_SCHEME_RE = re.compile(r"^([a-zA-Z][a-zA-Z0-9+.\-]*):")
_ALLOWED_URI_SCHEMES = frozenset({"http", "https", "mailto"})
# WHATWG URL parsing removes ASCII tab/newline anywhere in the input and trims
# leading/trailing C0 controls and space BEFORE the scheme is read — so the
# allowlist must see the same normalized string the browser will, or
# `java<TAB>script:` slips past `_URI_SCHEME_RE` as a "relative" URL and
# executes anyway.
_ASCII_TAB_NL_RE = re.compile(r"[\t\n\r]")
_C0_AND_SPACE = "".join(chr(c) for c in range(0x21))


def _sanitize_href(url: str, vendor_id: str) -> str | None:
    """Return a safe href for `url`, or None if it must render as plain text.

    The input is first normalized the way browsers normalize URLs (tab/newline
    removed anywhere, C0 controls and spaces trimmed at the ends), and the
    normalized form is both what gets checked and what gets returned.

    Allowlist: `http:`, `https:`, `mailto:`; scheme-less relative paths;
    `#anchor` fragments that map to a real generated section id (via
    `_map_fragment` — same-page anchors to vault-only headings render as
    plain text, counted); and vault-relative `.md` targets that resolve to a
    published dataset page (see `_resolve_md_link`). Everything else —
    `javascript:`, `data:`, `vbscript:`, any other unrecognised scheme,
    protocol-relative `//` links, and `.md` targets with no published page —
    is rejected so the caller can render inert plain text instead of a
    clickable href.
    """
    url = _ASCII_TAB_NL_RE.sub("", url).strip(_C0_AND_SPACE)
    scheme_match = _URI_SCHEME_RE.match(url)
    if scheme_match:
        return url if scheme_match.group(1).lower() in _ALLOWED_URI_SCHEMES else None
    if url.startswith("//"):
        return None
    if url.startswith("#"):
        frag = url[1:]
        if not frag:
            return url
        mapped = _map_fragment(frag)
        if mapped:
            return f"#{mapped}"
        # A same-page link whose anchor has no generated counterpart is a
        # dead link with no useful remainder — render plain text, counted.
        _MD_LINK_STATS["fragment_dropped"] += 1
        return None
    if re.search(r"\.md(#.*)?$", url):
        resolved = _resolve_md_link(url, vendor_id)
        _MD_LINK_STATS["resolved" if resolved else "plain_text"] += 1
        return resolved
    return url


def _markdown_inline(text: str, vendor_id: str = "") -> str:
    """Render a minimal markdown subset: backticks -> <code>, **bold**, *italic*/_italic_,
    [text](url) -> <a>.

    Escapes first (matching the pre-existing backtick/bold approach), then
    reconstructs tags from the escaped text via regex — so any `<`, `>`, `&`,
    or quote characters authored in link URLs or emphasised text stay inert;
    they are HTML-entity-escaped rather than passed through as raw markup.
    Bold is substituted before italic so a leftover single `*` from a
    consumed `**pair**` can never be mistaken for an italic delimiter.

    `[text](url)` links are passed through `_sanitize_href` (scoped to
    `vendor_id`, the current dataset page's vendor): an unsafe or dead link
    target renders as escaped plain text instead of an `<a href>` — see
    `_sanitize_href` and `_resolve_md_link` for the allowlist/resolution
    rules.
    """
    text = html_escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*\n]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"(?<!\w)_([^_\n]+)_(?!\w)", r"<em>\1</em>", text)

    def _link_repl(m: re.Match[str]) -> str:
        label, url = m.group(1), m.group(2)
        href = _sanitize_href(url, vendor_id)
        if href is None:
            return label
        return f'<a href="{href}">{label}</a>'

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _link_repl, text)
    return text


def _parse_overview(section: str) -> list[str]:
    """Split overview body into paragraphs; strip 'Link to relevant domain...' note."""
    text = section.strip()
    # Drop the "→ Link to relevant domain..." auto-inserted block (and its bullets)
    text = re.sub(
        r"→ Link to relevant domain concept notes.*?(?=\n\n|\Z)",
        "",
        text,
        flags=re.DOTALL,
    )
    paragraphs = []
    for p in re.split(r"\n\s*\n", text):
        p = p.strip()
        # Drop empty paragraphs and lone markdown horizontal rules
        if not p or re.fullmatch(r"-{3,}", p):
            continue
        paragraphs.append(p)
    return paragraphs


def _strip_title_backticks(line: str) -> str:
    """Strip backticks but keep ALLCAPS dataset code visible: 'X (`FOO`)' → 'X (FOO)'."""
    return line.replace("`", "")


def _parse_markdown_table(text: str) -> list[list[str]] | None:
    """Parse a single markdown table; return rows including header. None if not a table."""
    lines = [ln for ln in text.strip().splitlines() if ln.strip().startswith("|")]
    if len(lines) < 2:
        return None
    rows = []
    for ln in lines:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        rows.append(cells)
    # Detect alignment row (---|---|...) and drop it
    if len(rows) >= 2 and all(re.match(r"^:?-+:?$", c) for c in rows[1]):
        rows.pop(1)
    return rows


def _extract_api_table(section: str) -> dict[str, str]:
    """Parse the API endpoint key/value table from the 'API endpoint' section."""
    rows = _parse_markdown_table(section)
    if not rows:
        return {}
    out: dict[str, str] = {}
    for row in rows[1:]:
        if len(row) < 2:
            continue
        key = row[0].lower()
        value = row[1]
        out[key] = value
    return out


def _extract_silver_metadata(section: str) -> dict[str, str]:
    """Parse the bold key/value pairs at the top of the Silver layer section.

    Values may be backtick-quoted with an optional trailing note (e.g.
    `` `ingested_at` (no native PIT field) ``). Extract the first backtick value
    when present; otherwise return the raw value with surrounding backticks stripped.
    """
    meta: dict[str, str] = {}
    for line in section.splitlines():
        m = re.match(r"\*\*(?P<key>[^*]+)\*\*\s*:\s*(?P<val>.*?)\s*$", line)
        if not m:
            continue
        key = m.group("key").strip().lower()
        val = m.group("val").strip()
        # Prefer the first backtick-bounded value if present (the canonical code value)
        code_match = re.match(r"`([^`]+)`", val)
        if code_match:
            meta[key] = code_match.group(1)
        else:
            meta[key] = val.strip("`")
    return meta


def _parse_pk_columns(dedup_key: str) -> set[str]:
    """Extract PK column names from a dedup-key string like '(a, b, c)' or 'a, b'."""
    cleaned = dedup_key.strip().strip("()").strip()
    if not cleaned:
        return set()
    return {c.strip().strip("`") for c in cleaned.split(",") if c.strip()}


def _extract_silver_schema_rows(section: str, pk_columns: set[str]) -> list[SchemaRow]:
    """Parse the silver schema table under '### Silver schema'."""
    sub_match = re.search(r"###\s+Silver schema\s*\n(.*?)(?=\n###\s|\n##\s|\Z)", section, re.DOTALL)
    if not sub_match:
        return []
    table = _parse_markdown_table(sub_match.group(1))
    if not table or len(table) < 2:
        return []
    header = [c.lower() for c in table[0]]
    name_i = header.index("field") if "field" in header else 0
    type_i = header.index("python type") if "python type" in header else 1
    nullable_i = header.index("nullable") if "nullable" in header else 2
    rows: list[SchemaRow] = []
    for r in table[1:]:
        if len(r) < 3:
            continue
        raw_name = r[name_i].strip("`").strip()
        is_pk = raw_name in pk_columns
        nullable_raw = r[nullable_i].strip()
        nullable = nullable_raw.lower() in {"yes", "true"}
        notes = ""
        if len(r) >= 5:
            notes = r[4].strip()
        elif len(r) == 4:
            notes = r[3].strip()
        type_str = r[type_i].strip("`").strip()
        if "pk" in notes.lower() or "primary key" in notes.lower():
            is_pk = True
        rows.append(
            SchemaRow(
                name=raw_name,
                pk=is_pk,
                type=type_str,
                nullable=nullable,
                note=notes,
            )
        )
    return rows


def _extract_silver_sample(section: str) -> tuple[list[str], list[list[str]], str, str]:
    """Parse silver sample. Returns (columns, rows, language, raw_block).

    Vault format varies: sometimes a Python list of dicts, sometimes JSON, sometimes
    a markdown table. We render it as code-block sample (raw) on the page; columns/rows
    are used by the data-table when a structured form can be derived.
    """
    sub_match = re.search(r"###\s+Silver sample\s*\n(.*?)(?=\n###\s|\n##\s|\Z)", section, re.DOTALL)
    if not sub_match:
        return [], [], "json", ""
    sub_text = sub_match.group(1)
    # Find first fenced code block
    fence = re.search(r"```(\w*)\n(.*?)```", sub_text, re.DOTALL)
    if fence:
        lang = fence.group(1) or "json"
        raw = fence.group(2).strip()
        # Try to extract list[dict] into a structured table
        rows_struct, cols_struct = _try_parse_listdict(raw)
        return cols_struct, rows_struct, lang, raw
    # Else try a markdown table
    table = _parse_markdown_table(sub_text)
    if table:
        return table[0], table[1:], "table", ""
    return [], [], "json", sub_text.strip()


def _try_parse_listdict(raw: str) -> tuple[list[list[str]], list[str]]:
    """Best-effort: parse a python-list-of-dicts literal into rows+columns."""
    try:
        # Python dicts allow trailing commas and unquoted keys sometimes —
        # safer to do a coarse parse
        s = raw.strip()
        if not s.startswith("["):
            return [], []
        # Replace Python None/True/False with JSON nulls/bools
        s_json = (
            s.replace("'", '"')
            .replace("True", "true")
            .replace("False", "false")
            .replace("None", "null")
        )
        # Drop trailing commas before ] or }
        s_json = re.sub(r",(\s*[\]}])", r"\1", s_json)
        data = json.loads(s_json)
    except (ValueError, json.JSONDecodeError):
        return [], []
    if not isinstance(data, list) or not data:
        return [], []
    if not isinstance(data[0], dict):
        return [], []
    columns = list(data[0].keys())
    rows = [[str(d.get(c, "")) for c in columns] for d in data]
    return rows, columns


_CAVEAT_LEAD_RE = re.compile(r"^\*\*(?P<title>[^*]+?)\*\*\s*(?P<rest>.*)$")
_CAVEAT_SEP_RE = re.compile(r"^[—:\-–]\s*")


def _extract_caveats(section: str) -> list[Caveat]:
    """Parse 'Known issues and gotchas' bullet list into numbered caveats.

    The vault format uses three observed bullet shapes: `- **Title** — body`,
    `- **Title**: body`, and `` - **Title.** body `` (a bold lead-in ending in
    its own sentence period, immediately followed by the body sentence with
    no separator character at all — e.g. ``**PSR types are human-readable
    labels.** Elexon's AGPT API returns...``). All three are handled by
    stripping the bold title, then optionally stripping a leading separator
    from what remains. A trailing period on the title is dropped since it
    belongs to the bold lead-in's own sentence, not the title text.

    A bullet's body may wrap onto subsequent physical lines: the vault's
    authored markdown indents continuation lines by two spaces (standard
    Obsidian bullet-wrap style) rather than repeating the leading `-`. Each
    indented, non-blank line immediately following an open bullet belongs to
    that bullet's body and is joined with a single space, UNTIL a terminator
    is seen. A blank line or a pure horizontal-rule (``---``) line genuinely
    resets the open-bullet state: any indented content that follows a
    terminator is non-caveat content — it does NOT get appended to the
    caveat that preceded the terminator, and it is counted in
    ``_CAVEAT_STATS["dropped_lines"]`` rather than silently discarded.

    An in-section subheading (``### Control-area vs cross-zonal``) opens a
    caveat of its own: the heading text is the title and the col-0 prose
    lines that follow are its body, joined across blank-separated paragraphs
    until the next bullet, subheading, or horizontal rule. Col-0 prose with
    no open subheading has nowhere to go and is counted as dropped.

    An indented nested `-` bullet (e.g. Obsidian sub-bullets under a caveat)
    is not itself a new top-level caveat — top-level bullets are only
    recognised at column 0. While a caveat is open, an indented nested
    bullet joins that caveat's body as plain text (its own leading `-`
    marker is stripped). A nested bullet encountered after a terminator has
    no open caveat to join, so — like any other post-terminator indented
    line — it is dropped and counted, not silently ignored.

    Pure horizontal-rule lines (``---``) can appear inside a section's body
    (a markdown ``---`` divider before the next ``##`` heading is not itself
    a heading, so `_split_sections` leaves it in-section) and must not be
    misread as an empty caveat bullet — they are skipped explicitly (and, as
    above, they close out any open caveat's continuation).
    """
    caveats: list[Caveat] = []
    caveat_open = False
    heading_open = False
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped:
            # Blank line terminates any open bullet's continuation. A
            # heading-opened caveat stays open: its prose paragraphs are
            # authored blank-separated at column 0.
            caveat_open = False
            continue
        if re.fullmatch(r"-{3,}", stripped):
            # Horizontal rule — not a bullet, and terminates continuation
            # of whatever bullet or subheading preceded it.
            caveat_open = False
            heading_open = False
            continue
        is_indented = line[:1].isspace()
        if not is_indented and stripped.startswith("#"):
            # An in-section subheading (`### Control-area vs cross-zonal`)
            # opens a caveat whose body is the col-0 prose that follows it.
            caveats.append(Caveat(title=stripped.lstrip("#").strip(), text=""))
            caveat_open = False
            heading_open = True
            continue
        if not is_indented and stripped.startswith("-"):
            heading_open = False
            content = stripped[1:].strip()
            m = _CAVEAT_LEAD_RE.match(content)
            if m:
                title = m.group("title").strip().rstrip(".").strip()
                rest = m.group("rest")
                sep_m = _CAVEAT_SEP_RE.match(rest)
                body = rest[sep_m.end() :].strip() if sep_m else rest.strip()
                if not sep_m and re.fullmatch(r"[.!?]*", body):
                    # Title-only bullet (e.g. `- **GB empty post-Brexit**.`) —
                    # the trailing punctuation belongs to the title's own
                    # sentence, not a separate body; don't render a stray "."
                    # as the caveat body.
                    body = ""
                caveats.append(Caveat(title=title, text=body))
            else:
                # Fallback: take the first sentence as title
                title = content.split(".", 1)[0]
                body = content[len(title) :].lstrip(". ").strip()
                caveats.append(Caveat(title=title, text=body))
            caveat_open = True
            continue
        if ((is_indented and caveat_open) or (not is_indented and heading_open)) and caveats:
            # Continuation content: an indented line under an open bullet
            # (including a nested `-` bullet, whose own marker is stripped),
            # or a col-0 prose line under an open subheading. Joins the open
            # caveat's body with a space.
            joined = stripped[1:].strip() if stripped.startswith("-") else stripped
            if caveats[-1].text:
                caveats[-1] = Caveat(title=caveats[-1].title, text=f"{caveats[-1].text} {joined}")
            else:
                caveats[-1] = Caveat(title=caveats[-1].title, text=joined)
            continue
        # Anything the grammar cannot place (indented content after a
        # terminator, col-0 prose with no open subheading) is counted, never
        # silently discarded — `build()` reports a nonzero count.
        _CAVEAT_STATS["dropped_lines"] += 1
    return caveats


def _extract_api_code_from_title(title_line: str, slug: str) -> str:
    """Extract '(FUELHH)' style code from the title line."""
    m = re.search(r"\(`?([A-Z][A-Z0-9_\-/]+)`?\)", title_line)
    if m:
        return m.group(1).replace("-", "_").replace("/", "_")
    return slug.upper()


def parse_vault_file(
    path: Path, vendor_id: str = "elexon", vendor_label: str = "Elexon BMRS"
) -> DatasetDoc:
    text = path.read_text(encoding="utf-8")
    fm, body = _parse_frontmatter(text)
    slug = fm.get("dataset_key", path.stem)
    # First H1 is the title; strip backticks so HTML escaping doesn't lose semantics
    h1_match = re.search(r"^#\s+(.*?)\s*$", body, re.MULTILINE)
    raw_title = h1_match.group(1).strip() if h1_match else slug
    # Strip leading "Elexon - " or "Vendor - " prefix; the vendor breadcrumb already shows it
    title_line = re.sub(r"^(Elexon|ENTSO-E|ENTSO-G|GIE|NESO|Open-Meteo)\s*-\s*", "", raw_title)
    title_line = _strip_title_backticks(title_line)
    api_code = _extract_api_code_from_title(title_line, slug)

    sections = _split_sections(body)
    overview = _parse_overview(sections.get("overview", ""))
    api_meta = _extract_api_table(sections.get("api endpoint", ""))
    silver_section = sections.get("silver layer", "")
    silver_meta = _extract_silver_metadata(silver_section)
    dedup_key_raw = silver_meta.get("dedup key", "").strip("`")
    pk_cols = _parse_pk_columns(dedup_key_raw)
    schema_rows = _extract_silver_schema_rows(silver_section, pk_cols)
    sample_cols, sample_rows, sample_lang, sample_raw = _extract_silver_sample(silver_section)
    caveats = _extract_caveats(sections.get("known issues and gotchas", ""))
    bronze_section = sections.get("bronze layer", "")
    bronze_meta = _extract_silver_metadata(bronze_section)  # same key/value shape

    # Detect whether the pydantic schema is wired: must look like a dotted module path
    raw_schema = silver_meta.get("pydantic schema", "").strip("`")
    pydantic_wired = bool(re.match(r"^[\w]+(\.[\w]+)+$", raw_schema))

    return DatasetDoc(
        slug=slug,
        vendor_id=vendor_id,
        vendor_label=vendor_label,
        last_verified=fm.get("last_verified", ""),
        title_line=title_line,
        api_code=api_code,
        overview_paragraphs=overview,
        base_url=api_meta.get("base url", "").strip("`"),
        api_path=api_meta.get("path", "").strip("`"),
        auth_note=api_meta.get("auth", ""),
        silver_path=silver_meta.get("path pattern", "").strip("`"),
        transformer_class=silver_meta.get("transformer class", "").strip("`"),
        pydantic_schema=raw_schema if pydantic_wired else "",
        pydantic_schema_wired=pydantic_wired,
        dedup_key=silver_meta.get("dedup key", "").strip("`"),
        point_in_time_field=silver_meta.get("point-in-time field", "").strip("`"),
        schema_rows=schema_rows,
        sample_columns=sample_cols,
        sample_rows=sample_rows,
        sample_language=sample_lang,
        sample_raw=sample_raw,
        caveats=caveats,
        bronze_path=bronze_meta.get("path pattern", "").strip("`"),
    )


# ──────────────────────────────────────────────────────────────────────
# Manifest loading
# ──────────────────────────────────────────────────────────────────────


def load_manifest(vendor_id: str = "elexon") -> dict:
    path = SITE_DIR / "data" / f"{vendor_id}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_index(manifest: dict) -> dict[str, dict]:
    """Map slug → manifest entry (with group injected)."""
    index = {}
    for group in manifest["groups"]:
        for ds in group["datasets"]:
            entry = dict(ds)
            entry["group"] = group["name"]
            entry["group_blurb"] = group["blurb"]
            index[ds["id"]] = entry
    return index


def manifest_siblings(manifest: dict, slug: str) -> list[dict]:
    """Return sibling dataset entries in the same group as slug (incl. slug itself)."""
    for group in manifest["groups"]:
        ids = [d["id"] for d in group["datasets"]]
        if slug in ids:
            return list(group["datasets"])
    return []


def manifest_total_count(manifest: dict) -> int:
    return sum(len(g["datasets"]) for g in manifest["groups"])


# ──────────────────────────────────────────────────────────────────────
# Rendering
# ──────────────────────────────────────────────────────────────────────


def make_env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=True,
        undefined=StrictUndefined,
        trim_blocks=False,
        lstrip_blocks=False,
        keep_trailing_newline=True,
    )
    env.filters["md_inline"] = _markdown_inline
    return env


def render_dataset(
    env: Environment, doc: DatasetDoc, manifest: dict, chart: dict | None = None
) -> str:
    """Render one dataset page.

    ``chart`` is the distilled real series for this page, or ``None`` when the
    page has no extracted data — in which case the template renders its seeded
    snapshot and the "illustrative, seeded" caption that goes with it.
    """
    template = env.get_template("dataset.html.j2")
    siblings = manifest_siblings(manifest, doc.slug)
    manifest_entry = manifest_index(manifest).get(doc.slug, {})
    return template.render(
        doc=doc,
        manifest=manifest_entry,
        siblings=siblings,
        all_groups=manifest["groups"],
        manifest_total=manifest_total_count(manifest),
        chart=chart,
        chart_opts=json.dumps(
            {"width": 900, "height": 280, "n": chart["points"], "values": chart["values"]},
            separators=(",", ":"),
        )
        if chart
        else "",
    )


def render_vendor_hub(
    env: Environment, manifest: dict, vendor_id: str, vendor_label: str, vendor_meta: dict
) -> str:
    template = env.get_template("vendor-hub.html.j2")
    return template.render(
        vendor_id=vendor_id,
        vendor_label=vendor_label,
        vendor_meta=vendor_meta,
        manifest=manifest,
        manifest_total=manifest_total_count(manifest),
    )


def render_coming_soon_stub(env: Environment, vendor_cfg: dict) -> str:
    template = env.get_template("vendor-coming-soon.html.j2")
    return template.render(
        vendor_id=vendor_cfg["vendor_id"],
        vendor_label=vendor_cfg["vendor_label"],
        region=vendor_cfg["region"],
        domain=vendor_cfg["domain"],
        stage_chip=vendor_cfg["stage_chip"],
        connector_state=vendor_cfg["connector_state"],
        vendor_docs_url=vendor_cfg.get("vendor_docs_url"),
        planned_items=vendor_cfg["planned_items"],
    )


# ──────────────────────────────────────────────────────────────────────
# Driver
# ──────────────────────────────────────────────────────────────────────


def resolve_vault_path(cli_arg: str | None) -> Path:
    if cli_arg:
        return Path(cli_arg).expanduser().resolve()
    env_path = os.environ.get("GRIDFLOW_VAULT_PATH")
    if env_path:
        return Path(env_path).expanduser().resolve()
    return DEFAULT_VAULT


def audit_vault_content(docs: list[DatasetDoc]) -> tuple[list[str], list[str]]:
    """Per-dataset content audit (VAULT-03).

    Returns (warnings, errors). Errors fail the build; warnings are surfaced
    on stderr but don't block. Critical-vs-soft thresholds:
      ERROR (build-blocking): no overview, no api endpoint base URL, no slug
      WARN  (surfaced):       schema rows empty, sample empty, caveats empty,
                              pydantic class not declared
    """
    warnings: list[str] = []
    errors: list[str] = []
    for d in docs:
        if not d.overview_paragraphs:
            errors.append(f"{d.slug}: vault file has no Overview content")
        if not d.base_url and not d.api_path:
            errors.append(f"{d.slug}: vault file declares no API endpoint")
        if not d.schema_rows:
            warnings.append(f"{d.slug}: silver schema rows empty (table will render placeholder)")
        if not (d.sample_rows or d.sample_raw):
            warnings.append(f"{d.slug}: silver sample empty (section will render placeholder)")
        if not d.caveats:
            warnings.append(f"{d.slug}: no caveats captured in vault")
        if not d.pydantic_schema_wired:
            warnings.append(
                f"{d.slug}: no Pydantic class declared in gridflow.schemas.elexon "
                f"(drift surface — flagged in schema description)"
            )
    return warnings, errors


def build_vendor(
    env: Environment,
    vendor_id: str,
    vault_path: Path,
    out_root: Path,
    chart_series: dict[str, dict] | None = None,
) -> tuple[int, int, int]:
    """Render one vendor's dataset pages + hub.

    Returns ``(dataset_page_count, template_page_count, real_chart_count)``.
    ``chart_series`` is the committed distilled series keyed
    ``"<vendor>/<slug>"``; a page with no entry renders its seeded chart. Only
    template-rendered pages can receive an injected series, so the second count
    is the denominator for the third.
    """
    chart_series = chart_series or {}
    vendor_cfg = REAL_VENDORS[vendor_id]
    vendor_label = vendor_cfg["label"]
    vendor_dir = vault_path / vendor_id
    if not vendor_dir.is_dir():
        sys.exit(
            f"[gridflow-build] ERROR: vault directory not found: {vendor_dir}\n"
            f"  Set --vault-path or $GRIDFLOW_VAULT_PATH, or vendor vault content into "
            f"{DEFAULT_VAULT.relative_to(REPO_ROOT)}/."
        )
    out_dataset_dir = out_root / "data-sources" / vendor_id
    out_dataset_dir.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest(vendor_id)
    manifest_slugs = {d["id"] for g in manifest["groups"] for d in g["datasets"]}

    vault_files = sorted(vendor_dir.glob("*.md"))
    vault_slugs = {p.stem for p in vault_files}

    missing_in_vault = manifest_slugs - vault_slugs
    if missing_in_vault:
        sys.exit(
            f"[gridflow-build] ERROR: manifest declares datasets without vault files: {sorted(missing_in_vault)}"
        )

    docs: list[tuple[Path, DatasetDoc]] = []
    for path in vault_files:
        slug = path.stem
        if slug not in manifest_slugs:
            print(f"  skip (not in manifest): {vendor_id}/{slug}")
            continue
        docs.append((path, parse_vault_file(path, vendor_id=vendor_id, vendor_label=vendor_label)))

    # VAULT-03 audit
    warnings, errors = audit_vault_content([d for _, d in docs])
    if warnings:
        print(f"[gridflow-build] {vendor_id}: {len(warnings)} content warning(s):", file=sys.stderr)
        for w in warnings:
            print(f"  WARN: {w}", file=sys.stderr)
    if errors:
        print(
            f"[gridflow-build] {vendor_id}: {len(errors)} content error(s) - failing build:",
            file=sys.stderr,
        )
        for e in errors:
            print(f"  ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    n_pages = 0
    n_template_pages = 0
    n_real_charts = 0
    for _path, doc in docs:
        out_path = out_dataset_dir / f"{doc.slug}.html"
        authored = AUTHORED_DIR / vendor_id / f"{doc.slug}.html"
        if authored.exists():
            # Authored pages carry their own markup verbatim, charts included —
            # they are not template-rendered, so chart injection does not reach
            # them. Subsuming their baked-in values is a separate change.
            shutil.copy(authored, out_path)
            print(f"  wrote: data-sources/{vendor_id}/{doc.slug}.html (authored)")
        else:
            chart = chart_series.get(f"{vendor_id}/{doc.slug}")
            html = render_dataset(env, doc, manifest, chart=chart)
            out_path.write_text(html, encoding="utf-8")
            suffix = f" (real: {chart['column']})" if chart else ""
            print(f"  wrote: data-sources/{vendor_id}/{doc.slug}.html{suffix}")
            n_template_pages += 1
            if chart:
                n_real_charts += 1
        n_pages += 1

    hub_path = out_root / "data-sources" / f"{vendor_id}.html"
    authored_hub = AUTHORED_DIR / vendor_id / "_landing.html"
    if authored_hub.exists():
        shutil.copy(authored_hub, hub_path)
        print(f"  wrote: data-sources/{vendor_id}.html (authored hub)")
    else:
        hub_html = render_vendor_hub(
            env, manifest, vendor_id, vendor_label, vendor_cfg["vendor_meta"]
        )
        hub_path.write_text(hub_html, encoding="utf-8")
        print(f"  wrote: data-sources/{vendor_id}.html")
    return n_pages, n_template_pages, n_real_charts


def build_coming_soon_stubs(env: Environment, out_root: Path) -> int:
    """Render coming-soon vendor hub stubs for any deferred vendors.

    For each entry in ``COMING_SOON_VENDORS`` (currently empty — every one of the
    seven vendors ships a real landing page), copies
    ``authored-pages/<vendor_id>/_landing.html`` verbatim if present, else renders
    ``vendor-coming-soon.html.j2``. Dormant after v2; retained for any future
    vendor that ships ahead of its documentation.
    """
    n = 0
    for cfg in COMING_SOON_VENDORS:
        vendor_id = cfg["vendor_id"]
        out_path = out_root / "data-sources" / f"{vendor_id}.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        authored_hub = AUTHORED_DIR / vendor_id / "_landing.html"
        if authored_hub.exists():
            shutil.copy(authored_hub, out_path)
            print(f"  wrote: data-sources/{vendor_id}.html (authored hub)")
        else:
            html = render_coming_soon_stub(env, cfg)
            out_path.write_text(html, encoding="utf-8")
            print(f"  wrote: data-sources/{vendor_id}.html (stub)")
        n += 1
    return n


def copy_authored_dataset_pages_for_coming_soon(out_root: Path) -> int:
    """Copy authored per-dataset HTML files for COMING_SOON vendor folders.

    REAL_VENDORS (including ``gie`` since the v2 close-out) get their per-dataset
    authored pages via ``build_vendor`` (manifest-driven). This covers only the
    manifest-less COMING_SOON vendors — currently none, so this is a no-op after
    v2. ``_landing.html`` is excluded (it's the hub, handled by
    ``build_coming_soon_stubs``). Retained for future coming-soon vendors.
    """
    n = 0
    coming_soon_folders = {cfg["vendor_id"] for cfg in COMING_SOON_VENDORS}
    for vendor_folder in sorted(coming_soon_folders):
        src_dir = AUTHORED_DIR / vendor_folder
        if not src_dir.is_dir():
            continue
        dst_dir = out_root / "data-sources" / vendor_folder
        for src in sorted(src_dir.glob("*.html")):
            if src.name == "_landing.html":
                continue
            dst_dir.mkdir(parents=True, exist_ok=True)
            dst = dst_dir / src.name
            shutil.copy(src, dst)
            n += 1
            print(f"  wrote: data-sources/{vendor_folder}/{src.name} (authored dataset)")
    return n


# REAL_VENDORS whose gridflow connector does NOT cover every dataset the
# vendor's landing page links to. Every other REAL_VENDOR is documented at
# full fidelity — every linked dataset is already ingested, so its Planned
# stubs (if any) may truthfully say so. neso_data_portal links its full
# implemented + eligible-but-not-yet-built catalogue from one landing page
# (T-23): the "shipping" stub copy ("the gridflow ETL pipeline already
# ingests it") would be false for the ~29 not-yet-implemented packages —
# exactly the "Shipping badge on unfinished work" front-end CLAUDE.md bans.
_PARTIAL_CONNECTOR_VENDORS = frozenset({"neso_data_portal"})


def _vendor_stub_metadata() -> dict[str, dict[str, str | None]]:
    """Lookup table: vendor folder → {label, docs_url, connector_state}.

    Drives ``build_dataset_stubs_from_landings``. Covers all REAL_VENDORS (the
    seven documented vendors, including the unified ``gie``) plus any
    COMING_SOON_VENDORS (currently none). Vendors in
    ``_PARTIAL_CONNECTOR_VENDORS`` report ``connector_state="planned"`` so their
    stubs never claim the pipeline already ingests them.
    """
    meta: dict[str, dict[str, str | None]] = {}
    for vendor_id, cfg in REAL_VENDORS.items():
        meta[vendor_id] = {
            "label": cfg["label"],
            "docs_url": cfg["vendor_meta"].get("vendor_docs_url"),
            "connector_state": (
                "planned" if vendor_id in _PARTIAL_CONNECTOR_VENDORS else "shipping"
            ),
        }
    for cfg in COMING_SOON_VENDORS:
        meta[cfg["vendor_id"]] = {
            "label": cfg["vendor_label"],
            "docs_url": cfg.get("vendor_docs_url"),
            "connector_state": cfg.get("connector_state", "planned"),
        }
    return meta


_LANDING_DATASET_LINK_RE = re.compile(r'href="([a-z][a-z0-9_]*)/([a-z][a-z0-9_]*)\.html"')


def build_dataset_stubs_from_landings(env: Environment, out_root: Path) -> int:
    """Render per-dataset coming-soon stubs for landing links with no real page.

    Scans every ``authored-pages/<vendor>/_landing.html`` for outgoing links of
    the form ``href="<vendor>/<slug>.html"``. For each target that does not yet
    exist under ``data-sources/<vendor>/<slug>.html`` after the manifest-driven
    and authored-copy passes have run, renders a depth-2 stub from
    ``dataset-coming-soon.html.j2``. Skips Elexon (full per-dataset coverage
    already authored).

    Must run AFTER ``build_vendor`` and ``copy_authored_dataset_pages_for_coming_soon``
    so the existence check correctly identifies real pages. Idempotent: a second
    invocation finds the stubs already on disk and skips them; ``filecmp`` in
    ``--check`` sees identical content because the template has no time-varying
    fields.
    """
    template = env.get_template("dataset-coming-soon.html.j2")
    vendor_meta = _vendor_stub_metadata()
    n = 0
    for landing in sorted(AUTHORED_DIR.glob("*/_landing.html")):
        vendor_folder = landing.parent.name
        if vendor_folder == "elexon":
            continue
        meta = vendor_meta.get(vendor_folder)
        if not meta:
            print(f"  skip stubs for {vendor_folder} (no vendor metadata)")
            continue
        text = landing.read_text(encoding="utf-8")
        targets = {
            slug
            for vendor, slug in _LANDING_DATASET_LINK_RE.findall(text)
            if vendor == vendor_folder
        }
        out_dir = out_root / "data-sources" / vendor_folder
        for slug in sorted(targets):
            out_path = out_dir / f"{slug}.html"
            if out_path.exists():
                continue
            out_dir.mkdir(parents=True, exist_ok=True)
            html = template.render(
                vendor_id=vendor_folder,
                vendor_label=meta["label"],
                vendor_docs_url=meta["docs_url"],
                connector_state=meta["connector_state"],
                slug=slug,
            )
            out_path.write_text(html, encoding="utf-8")
            n += 1
            print(f"  wrote: data-sources/{vendor_folder}/{slug}.html (coming-soon stub)")
    return n


def build(vault_path: Path, output_dir: Path | None = None) -> tuple[int, int, int, int]:
    """Render all vendor pages.

    Returns ``(n_dataset_pages, n_real_hubs, n_hub_stubs, n_dataset_stubs)``.
    ``n_dataset_pages`` covers manifest-rendered + authored-copied dataset pages;
    ``n_dataset_stubs`` is the coming-soon fallback for unfinished slugs linked
    from a vendor landing.
    """
    env = make_env()
    out_root = output_dir or SITE_DIR
    _reset_md_link_stats()
    _reset_caveat_stats()

    chart_series = chart_data.load_series(SITE_DIR)

    n_pages = 0
    n_hubs = 0
    n_template_pages = 0
    n_real_charts = 0
    for vendor_id in REAL_VENDORS:
        if not (vault_path / vendor_id).is_dir():
            print(f"  skip vendor (no vault dir): {vendor_id}")
            continue
        pages, template_pages, real_charts = build_vendor(
            env, vendor_id, vault_path, out_root, chart_series
        )
        n_pages += pages
        n_template_pages += template_pages
        n_real_charts += real_charts
        n_hubs += 1

    n_hub_stubs = build_coming_soon_stubs(env, out_root)
    n_pages += copy_authored_dataset_pages_for_coming_soon(out_root)
    n_dataset_stubs = build_dataset_stubs_from_landings(env, out_root)
    if chart_series:
        print(
            f"[gridflow-build] snapshot charts: {n_real_charts} real series injected from "
            f"{chart_data.series_path(SITE_DIR).name}, "
            f"{n_template_pages - n_real_charts} template page(s) seeded"
        )
    else:
        print(
            "[gridflow-build] snapshot charts: no chart-series.json — all template pages "
            "seeded (run --refresh-chart-data against a local gridflow extract)"
        )
    print(
        f"[gridflow-build] vault-relative .md links: {_MD_LINK_STATS['resolved']} resolved, "
        f"{_MD_LINK_STATS['plain_text']} rendered as plain text (no published page), "
        f"{_MD_LINK_STATS['fragment_dropped']} fragment(s) dropped (no generated anchor)"
    )
    if _CAVEAT_STATS["dropped_lines"]:
        print(
            f"[gridflow-build] WARNING: {_CAVEAT_STATS['dropped_lines']} line(s) in "
            "'Known issues and gotchas' sections could not be placed by the caveat "
            "grammar and were dropped from rendered output",
            file=sys.stderr,
        )
    return n_pages, n_hubs, n_hub_stubs, n_dataset_stubs


def _snapshot_outputs(temp_dir: Path) -> None:
    """Copy current generated outputs into temp_dir for diff comparison."""
    src = SITE_DIR / "data-sources"
    dst = temp_dir / "data-sources"
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True, exist_ok=True)
    for path in src.rglob("*.html"):
        rel = path.relative_to(src)
        out = dst / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, out)


def _diff_outputs(temp_dir: Path) -> list[str]:
    """Compare the snapshot in temp_dir against current outputs. Return list of differing paths."""
    src = SITE_DIR / "data-sources"
    snap = temp_dir / "data-sources"
    differing: list[str] = []
    for path in src.rglob("*.html"):
        rel = path.relative_to(src)
        snap_path = snap / rel
        if not snap_path.exists():
            differing.append(str(rel))
            continue
        if not filecmp.cmp(str(path), str(snap_path), shallow=False):
            differing.append(str(rel))
    return differing


def refresh_chart_data(cli_path: str | None) -> int:
    """Re-distil the committed chart-series file from a local gridflow extract.

    Local-only: the extract lives outside the repo, so this is run by hand after
    a re-extract and the resulting JSON is committed. Every dataset that did NOT
    become a chart is reported with its reason — a silently short list would read
    as "the extract had nothing", which is exactly the failure this guards.
    """
    extract_root = chart_data.resolve_extract_path(cli_path)
    print(f"[gridflow-build] chart extract: {extract_root}")
    try:
        payload, notes, problems = chart_data.distil(extract_root)
    except FileNotFoundError as exc:
        print(f"[gridflow-build] ERROR: {exc}", file=sys.stderr)
        return 1
    out_path = chart_data.write_series(payload, SITE_DIR)
    for note in notes:
        print(f"  seeded: {note}")
    if problems:
        print(
            f"[gridflow-build] {len(problems)} column-choice divergence(s) from the extract's "
            "charts-manifest:",
            file=sys.stderr,
        )
        for problem in problems:
            print(f"  NOTE: {problem}", file=sys.stderr)
    print(
        f"[gridflow-build] wrote {out_path.relative_to(REPO_ROOT)}: "
        f"{payload['count']} real series over {payload['window_label']}, "
        f"{len(notes)} dataset(s) left seeded"
    )
    print("[gridflow-build] commit that file — CI builds from a bare checkout and cannot")
    print("                 see the extract, so an uncommitted refresh never reaches the site.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="gridflow-build", description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--vault-path",
        default=None,
        help="Path to the Obsidian vault root (containing elexon/). "
        "Defaults to $GRIDFLOW_VAULT_PATH, then the vendored ./vault/ directory.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Build twice and exit non-zero if any output changes between builds (idempotence check).",
    )
    parser.add_argument(
        "--refresh-chart-data",
        action="store_true",
        help="Re-distil site/hifi/data/chart-series.json from a local gridflow extract "
        "and exit without building. Run this after a re-extract, then commit the file.",
    )
    parser.add_argument(
        "--chart-extract-path",
        default=None,
        help="Path to the gridflow chart-data extract (containing manifest.json). "
        "Defaults to $GRIDFLOW_CHART_EXTRACT_PATH, then "
        f"{chart_data.DEFAULT_EXTRACT}. Only used by --refresh-chart-data.",
    )
    args = parser.parse_args(argv)

    if args.refresh_chart_data:
        return refresh_chart_data(args.chart_extract_path)

    vault_path = resolve_vault_path(args.vault_path)
    print(f"[gridflow-build] vault: {vault_path}")

    n_pages, n_hubs, n_hub_stubs, n_dataset_stubs = build(vault_path)
    print(
        f"[gridflow-build] wrote {n_pages} dataset pages + {n_hubs} vendor hub(s) + "
        f"{n_hub_stubs} coming-soon hub(s) + {n_dataset_stubs} coming-soon dataset stub(s)"
    )

    if args.check:
        with tempfile.TemporaryDirectory(prefix="gridflow-build-check-") as tmp:
            tmp_path = Path(tmp)
            _snapshot_outputs(tmp_path)
            _, _, _, _ = build(vault_path)
            differing = _diff_outputs(tmp_path)
            if differing:
                print(
                    f"[gridflow-build] FAIL: {len(differing)} file(s) differ between builds (non-idempotent):"
                )
                for p in differing:
                    print(f"    {p}")
                return 1
            print(
                f"[gridflow-build] OK: idempotent across {n_pages} pages + "
                f"{n_hubs + n_hub_stubs} hubs + {n_dataset_stubs} dataset stubs."
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
