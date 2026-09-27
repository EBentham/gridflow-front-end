"""gridflow-build — render dataset pages from Obsidian Vault markdown.

Reads vault `.md` files under `<vault>/elexon/*.md`, parses YAML frontmatter
and the structured sections (Overview, API endpoint, Silver layer, Known
issues, etc.), and renders one HTML file per dataset using Jinja2 templates
under `templates/`. Also rebuilds the vendor hub (`site/hifi/data-sources/elexon.html`)
from the manifest at `site/hifi/data/elexon.json`.

Build inputs (single source of truth):
- vault/<vendor>/<slug>.md       — authored content (frontmatter + sections);
                                   the front matter's `page:` block carries the
                                   page fields and chart spec (see page_fields)
- site/hifi/data/<vendor>.json   — structural manifest (id/title/freq/lag/rows)
- site/hifi/data/series/<vendor>/<slug>.json — distilled chart series, written
                                   by `gridflow-distil` from local silver and
                                   committed (see chart_spec, distil)
- site/hifi/data/chart-specs/<vendor>/<slug>.json — staged chart specs, until
                                   Phase 26 moves them into the vault notes

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

Charts: a dataset page shows a chart only when its dataset has a chart spec
and a committed series distilled from exactly that spec. No spec, no chart:
there is no seeded or placeholder fallback (v5 decision D3).
"""

from __future__ import annotations

import argparse
import filecmp
import json
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass, field
from html import escape as html_escape
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup

from gridflow_front_end import artefacts, chart_spec, chart_svg
from gridflow_front_end.page_fields import PageFields, anatomy_errors, parse_page_fields
from gridflow_front_end.paths import DEFAULT_VAULT, REPO_ROOT, SITE_DIR, resolve_vault_path

TEMPLATES_DIR = REPO_ROOT / "templates"
AUTHORED_DIR = REPO_ROOT / "authored-pages"

__all__ = [
    "AUTHORED_DIR",
    "DEFAULT_VAULT",
    "REAL_VENDORS",
    "REPO_ROOT",
    "SITE_DIR",
    "parse_vault_file",
    "resolve_vault_path",
]


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
            # v5 D4: the site documents only what gridflow ingests, so the hub
            # names the three ingested packages and counts nothing else.
            "lede": (
                "The National Energy System Operator's general open-data catalogue, a "
                "CKAN file-download platform separate from the NESO Carbon Intensity "
                "API. gridflow ingests three of its packages: per-BMU wind availability "
                "forecasts, embedded (sub-transmission) wind and solar generation "
                "forecasts, and a half-hourly GB generation-mix archive back to 2009."
            ),
            "vendor_docs_url": "https://www.neso.energy/data-portal/api-guidance",
            "base_url": "api.neso.energy/api/3/action",
            "auth": "Public · no key required",
            "rate_limit": "1 req/s · CKAN action API (IP-block enforced)",
            "format": "CKAN JSON metadata → CSV file download",
            "earliest": "2009-01-01 · historic_generation_mix",
            "timezone": "UTC · daily / half-hourly grain",
            "stat_three_value": "CKAN",
            "stat_three_label": "File catalogue · CSV downloads",
            "stat_four_value": "3",
            "stat_four_label": "Packages ingested",
        },
    },
}


# Vendors whose authored `_landing.html` is NOT used, so the hub renders from
# the manifest instead. neso_data_portal's authored landing is a catalogue of
# 29 packages gridflow does not ingest, each linking a "Planned" stub page;
# v5 D4 drops those stubs, and the landing would otherwise link 29 dead pages.
_TEMPLATE_HUB_VENDORS = frozenset({"neso_data_portal"})


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
    page: PageFields = field(default_factory=PageFields)
    page_errors: list[str] = field(default_factory=list)

    @property
    def new_template(self) -> bool:
        """True when the note carries a ``page:`` block: it renders on the locked anatomy."""
        return self.page.present

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
        # Top-level scalars only. Nested YAML (v2_fix_history, the `page:`
        # block) is indented; letting it through would let a nested key
        # overwrite a top-level one. `page:` is read by page_fields with YAML.
        if line[:1].isspace() or line.lstrip().startswith("-"):
            continue
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


# Section ids that exist on EVERY generated dataset page
# (templates/dataset.html.j2) — the only fragments a resolved `.md` link may
# carry, because the deploy gate link-checks fragments (`lychee
# --include-fragments`): an anchor to a heading that only exists in the vault
# source would 404 the fragment and block deployment. The chart section is
# not listed: a page without a chart spec has no chart section at all.
_GENERATED_SECTION_IDS = frozenset({"overview", "schema", "sample", "api", "caveats", "related"})

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

# (vendor, slug) of every note on the new dataset template, filled by build()
# before any page renders, so a legacy page's link into one drops its
# legacy-only fragment instead of failing the fragment-aware link check.
_NEW_TEMPLATE_PAGES: set[tuple[str, str]] = set()


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
    if anchor and (target_vendor, slug) in _NEW_TEMPLATE_PAGES:
        # the new template has none of the legacy section ids (no #caveats, no
        # #schema); keep the page target and drop the fragment
        _MD_LINK_STATS["fragment_dropped"] += 1
        anchor = ""
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
    page, page_errors = parse_page_fields(text)

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
        page=page,
        page_errors=page_errors,
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


def chart_opts_json(chart: dict[str, Any]) -> str:
    """The ``data-opts`` payload ``charts.js`` needs to draw one series file.

    Only what the renderer reads: identity, provenance and the spec stay in the
    committed JSON, not in every page.
    """
    return json.dumps(
        {
            "type": chart["type"],
            "unit": chart["unit"],
            "x_kind": chart["x_kind"],
            "x": chart["x"],
            "series": [{"key": s["key"], "values": s["values"]} for s in chart["series"]],
        },
        separators=(",", ":"),
        ensure_ascii=False,
    )


def render_dataset(
    env: Environment, doc: DatasetDoc, manifest: dict, chart: dict[str, Any] | None = None
) -> str:
    """Render one dataset page.

    ``chart`` is the committed series distilled from this dataset's chart
    spec, or ``None``. With ``None`` the page has no chart section at all:
    there is no seeded or placeholder chart.
    """
    template = env.get_template("dataset-legacy.html.j2")
    siblings = manifest_siblings(manifest, doc.slug)
    manifest_entry = manifest_index(manifest).get(doc.slug, {})
    return template.render(
        doc=doc,
        manifest=manifest_entry,
        siblings=siblings,
        all_groups=manifest["groups"],
        manifest_total=manifest_total_count(manifest),
        chart=chart,
        chart_opts=chart_opts_json(chart) if chart else "",
    )


# ──────────────────────────────────────────────────────────────────────
# The dataset page template (locked anatomy, v5 Phase 25b)
# ──────────────────────────────────────────────────────────────────────

# Template copy for the lineage columns (schema option 4, verbatim).
LINEAGE_MEANINGS = {
    "event_time": "The row’s time column; for a table without one, the transform’s target date",
    "available_at": "When the row became knowable: `published_at`, else the transform time",
    "source_run_id": "Id of the pipeline run that wrote the row",
    "dataset_version": "Transformer version stamped on the row",
    "vintage_policy": "Which rule produced `available_at`",
}
_NUMERIC_DTYPES = re.compile(r"^(U?Int\d+|Float\d+|Decimal.*|Date|Datetime.*|Duration.*|Time)$")
_CODE_VALUE = re.compile(r"^[A-Z0-9_\-/.]+$")
_KW = re.compile(
    r"\b(from|import|as|def|return|for|in|if|else|lambda|not|and|or|None|True|False)\b"
)


@dataclass
class PageArtefacts:
    """The committed files one new-template page renders from."""

    chart: dict[str, Any] | None = None
    sample: dict[str, Any] | None = None
    notebook: dict[str, Any] | None = None


def highlight(code: str) -> Markup:
    """Escape Python, then tint keywords and string literals (the homepage's two token colours)."""
    out: list[str] = []
    pos = 0
    for m in re.finditer(r'"[^"\n]*"|\'[^\'\n]*\'', code):
        out.append(
            _KW.sub(r'<span class="k">\1</span>', html_escape(code[pos : m.start()], quote=False))
        )
        out.append(f'<span class="s">{html_escape(m.group(0), quote=False)}</span>')
        pos = m.end()
    out.append(_KW.sub(r'<span class="k">\1</span>', html_escape(code[pos:], quote=False)))
    return Markup("".join(out))


def request_lines(request: str) -> Markup:
    """A raw vendor request, one query parameter per line, as it reads in a well."""
    text = html_escape(request, quote=False)
    head, _, query = text.partition("?")
    if not query:
        return Markup(text)
    params = query.split("&amp;")
    lines = [f"{head}"] + [f"    {'?' if i == 0 else '&amp;'}{p}" for i, p in enumerate(params)]
    return Markup("\n".join(lines))


def check_artefacts(doc: DatasetDoc) -> tuple[PageArtefacts, list[str]]:
    """Load a new-template page's sample and notebook files and check their digests."""
    key = f"{doc.vendor_id}/{doc.slug}"
    errors: list[str] = []
    fields = doc.page
    arts = PageArtefacts()
    silver = artefacts.sample_silver(doc.vendor_id, doc.slug, fields.record.select, fields.chart)
    try:
        sample = artefacts.load_json(artefacts.sample_path(SITE_DIR, doc.vendor_id, doc.slug))
        notebook = artefacts.load_json(artefacts.notebook_path(SITE_DIR, doc.vendor_id, doc.slug))
    except (ValueError, json.JSONDecodeError) as exc:
        return arts, [f"{key}: {exc}"]
    if sample is None:
        errors.append(f"{key}: no sample rows (run gridflow-sample and commit them)")
    elif sample.get("select_sha256") != artefacts.select_digest(silver, fields.record.select):
        errors.append(
            f"{key}: sample rows were picked by a different page.record.select; rerun gridflow-sample"
        )
    else:
        arts.sample = sample
    source = artefacts.notebook_source(doc.vendor_id, fields.notebook.source)
    cells = artefacts.notebook_cells(source, fields.notebook.cells)
    if notebook is None:
        errors.append(f"{key}: no executed notebook (run scripts/run_notebooks.py and commit it)")
    elif notebook.get("cells_sha256") != artefacts.cells_digest(cells):
        errors.append(
            f"{key}: the notebook was executed from different cells; rerun scripts/run_notebooks.py"
        )
    else:
        arts.notebook = notebook
        for cell in notebook["cells"]:
            for out in cell["outputs"]:
                if out["kind"] == "image":
                    img = artefacts.notebooks_dir(SITE_DIR) / doc.vendor_id / out["src"]
                    if not img.is_file():
                        errors.append(f"{key}: notebook image {out['src']} is missing")
                    if not fields.notebook.plot_alt:
                        errors.append(
                            f"{key}: page.notebook.plot_alt is required for the plot output"
                        )
    return arts, errors


def _record_view(doc: DatasetDoc, sample: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    key = f"{doc.vendor_id}/{doc.slug}"
    rec = doc.page.record
    errors: list[str] = []
    cols = sample["columns"]
    names = [c["name"] for c in cols]
    mark = sample["rows"][sample["mark"]]
    schema_cols = [c for c in cols if not c["lineage"]]
    missing = [c["name"] for c in schema_cols if c["name"] not in rec.fields]
    if missing:
        errors.append(f"{key}: page.record.fields has no meaning for {missing}")
    extra = sorted(set(rec.fields) - {c["name"] for c in schema_cols})
    if extra:
        errors.append(f"{key}: page.record.fields names columns silver does not have: {extra}")
    bad_key = [k for k in rec.key if k not in names]
    if bad_key:
        errors.append(f"{key}: page.record.key names columns silver does not have: {bad_key}")
    fields_v = []
    lineage_v = []
    for i, c in enumerate(cols):
        item = {
            "name": c["name"],
            "value": mark[i],
            "dtype": c["dtype"],
            "key": c["name"] in rec.key,
        }
        if c["lineage"]:
            lineage_v.append({**item, "meaning": LINEAGE_MEANINGS.get(c["name"], "")})
        else:
            fields_v.append({**item, "meaning": rec.fields.get(c["name"], "")})
    differ = [
        i
        for i, c in enumerate(cols)
        # ingested_at differs only by transform batch: pipeline noise, not data the reader compares.
        if not c["lineage"]
        and c["name"] != "ingested_at"
        and len({row[i] for row in sample["rows"]}) > 1
    ]
    if not differ:
        differ = [names.index(k) for k in rec.key if k in names]

    def cls(i: int) -> str:
        if _NUMERIC_DTYPES.match(cols[i]["dtype"]):
            return "n"
        vals = [row[i] for row in sample["rows"] if row[i] is not None]
        return "c" if vals and all(_CODE_VALUE.match(v) for v in vals) else "s"

    table = {
        "columns": [{"name": names[i], "align": cls(i)} for i in differ],
        "rows": [
            {"me": r == sample["mark"], "cells": [{"value": row[i], "cls": cls(i)} for i in differ]}
            for r, row in enumerate(sample["rows"])
        ],
    }
    relation = f"silver_{sample['silver'].replace('/', '_')}"
    line = f"Relation <code>{html_escape(relation)}</code>"
    if doc.pydantic_schema_wired:
        module, _, cls_name = doc.pydantic_schema.rpartition(".")
        line += (
            f", typed by <code>{html_escape(cls_name)}</code> in "
            f"<code>{html_escape(module.replace('.', '/'))}.py</code>"
        )
    if "dataset_version" in names and mark[names.index("dataset_version")]:
        line += f"; transformer version {html_escape(mark[names.index('dataset_version')])}"
    view = {
        "relation_line": Markup(line + "."),
        "fields": fields_v,
        "lineage": lineage_v,
        "caption": rec.caption,
        "table": table,
        "narrow": len(differ) <= 3,
    }
    return view, errors


_LOCAL_STORAGE = re.compile(r"\blocally\b|\blocal (copy|store|storage|disk)\b", re.IGNORECASE)


def _output_html(out: dict[str, Any], vendor_id: str, handle: str, alt: str) -> Markup:
    kind = out["kind"]
    if kind == "card":
        # The site never describes local storage (DESIGN.md), and the gridflow_models help text
        # for `backfill` does; the row is left out rather than reworded, so every shown word is real.
        dl = "".join(
            f"<div><dt>{html_escape(n)}</dt><dd>{html_escape(d)}</dd></div>"
            for n, d in out["rows"]
            if not _LOCAL_STORAGE.search(d)
        )
        foot = out["foot"]
        return Markup(
            f'<div class="card"><p class="card-h">{html_escape(handle)}</p><dl>{dl}</dl>'
            f'<p class="card-f">{html_escape(foot[0])} <code>{html_escape(foot[1])}</code></p></div>'
        )
    if kind == "df":
        head = (
            "<tr><th></th>"
            + "".join(f"<th>{html_escape(c)}</th>" for c in out["columns"])
            + "</tr>"
        )
        body = "".join(
            f"<tr><th>{html_escape(idx)}</th>"
            + "".join(f"<td>{html_escape(v)}</td>" for v in row)
            + "</tr>"
            for idx, row in zip(out["index"], out["rows"])
        )
        return Markup(
            f'<div class="df-wrap"><table class="df"><thead>{head}</thead><tbody>{body}</tbody></table></div>'
        )
    if kind == "image":
        return Markup(
            f'<div class="fig"><img src="../../data/notebooks/{vendor_id}/{html_escape(out["src"])}" '
            f'width="{out["width"]}" height="{out["height"]}" alt="{html_escape(alt, quote=True)}" '
            f'loading="lazy"></div>'
        )
    return Markup(
        f'<div class="fig"><pre class="txt">{html_escape(out["text"], quote=False)}</pre></div>'
    )


def _notebook_view(doc: DatasetDoc, nb: dict[str, Any]) -> dict[str, Any]:
    fields = doc.page.notebook
    source = nb["source"]
    cells = nb["cells"]
    rendered = [
        {
            "n": c["n"],
            "html": highlight(c["source"]),
            "outputs": [
                _output_html(o, doc.vendor_id, f"data.{source}", fields.plot_alt)
                for o in c["outputs"]
            ],
        }
        for c in cells
    ]
    call = [
        {"n": 1, "html": highlight(cells[0]["source"])},
        {"n": 2, "html": highlight(cells[2]["source"])},
    ]
    return {
        "lead": fields.lead,
        "needs": fields.needs,
        "tab": f"{doc.slug}.ipynb",
        "call": call,
        "cells": rendered,
        "source": "\n\n".join(c["source"] for c in cells) + "\n",
        "aria": (
            f"A demo notebook on the gridflow_models kernel: setup, the data.{source} help card, "
            f"then {len(cells) - 2} cells on {doc.vendor_id}/{doc.slug}, every output real."
        ),
    }


def page_view(
    doc: DatasetDoc,
    arts: PageArtefacts,
    members: list[DatasetDoc],
) -> tuple[dict[str, Any], list[str]]:
    """The view model ``dataset.html.j2`` renders, and the errors that stop it rendering.

    Args:
        doc: A note on the new template (``doc.new_template``).
        arts: Its committed chart series, sample rows and executed notebook.
        members: For a family page, the member notes in the family's order.
    """
    key = f"{doc.vendor_id}/{doc.slug}"
    p = doc.page
    errors: list[str] = []
    facts: list[tuple[str, Markup]] = [
        ("Vendor", Markup(_markdown_inline(p.facts.vendor, doc.vendor_id))),
        ("Cadence", Markup(_markdown_inline(p.facts.cadence, doc.vendor_id))),
        ("Grain", Markup(_markdown_inline(p.facts.grain, doc.vendor_id))),
        ("Key", Markup(", ".join(f"<code>{html_escape(k)}</code>" for k in p.record.key))),
    ]
    if p.facts.history:
        facts.append(("History", Markup(_markdown_inline(p.facts.history, doc.vendor_id))))

    chart_v = None
    if arts.chart is not None:
        errors.extend(f"{key}: {e}" for e in chart_svg.check_view(arts.chart, p.chart_view))
        if not errors:
            wide, narrow = chart_svg.render(arts.chart, p.chart_view, "c")
            kind = chart_svg.key_kind(arts.chart)
            chart_v = {
                "title": p.chart_view.title,
                "caption": p.chart_view.caption,
                "wide": Markup(wide),
                "narrow": Markup(narrow),
                "key": [
                    {
                        "mark": Markup(chart_svg.key_mark(e, kind, f"k{i}")),
                        "label": e.label,
                        "codes": e.codes,
                        "note": e.note,
                    }
                    for i, e in enumerate(p.chart_view.key)
                ],
            }

    record_v: dict[str, Any] = {}
    if arts.sample is not None:
        record_v, rec_errors = _record_view(doc, arts.sample)
        errors.extend(rec_errors)

    related = []
    slugs = _all_manifest_slugs()
    for rel in p.related:
        vendor, _, slug = rel.dataset.partition("/")
        if slug not in slugs.get(vendor, set()):
            errors.append(f"{key}: related {rel.dataset} has no page on the site")
            continue
        href = f"{slug}.html" if vendor == doc.vendor_id else f"../{vendor}/{slug}.html"
        related.append({"href": href, "key": rel.dataset, "note": rel.note})

    variants = []
    if p.family is not None:
        by_slug = {m.slug: m for m in members}
        for mem in p.family.members:
            m = by_slug.get(mem.dataset)
            variants.append(
                {
                    "slug": mem.dataset,
                    "key": f"{doc.vendor_id}/{mem.dataset}",
                    "code": m.api_code if m else mem.dataset.upper(),
                    "differs": mem.differs,
                    "request": request_lines(mem.request),
                }
            )

    view = {
        "vendor_id": doc.vendor_id,
        "vendor_label": doc.vendor_label,
        "key": key,
        "chips": [v["key"] for v in variants] or [key],
        "title": p.title,
        "summary": p.summary,
        "summary_plain": (p.summary or "").replace("`", ""),
        "facts": facts,
        "landscape": p.landscape or _DEFAULT_LANDSCAPE.get(doc.vendor_id, "power"),
        "what_it_is": p.what_it_is,
        "how_used": p.how_used,
        "chart": chart_v,
        "raw": {
            "note": p.raw_feed.note,
            "requests": [request_lines(r) for r in p.raw_feed.requests],
            "commands": p.raw_feed.commands,
        },
        "variants": variants,
        "record": record_v,
        "notebook": _notebook_view(doc, arts.notebook) if arts.notebook else {},
        "related": related,
    }
    return view, errors


_DEFAULT_LANDSCAPE = {"entsog": "gas", "gie": "gas"}


def render_page(env: Environment, view: dict[str, Any]) -> str:
    """Render one page on the dataset template."""
    return env.get_template("dataset.html.j2").render(v=view)


def render_redirect(env: Environment, key: str, href: str, family_title: str) -> str:
    """A family member's old address, pointing at its section of the family page."""
    return env.get_template("redirect.html.j2").render(
        key=key, href=href, family_title=family_title
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


# ──────────────────────────────────────────────────────────────────────
# Driver
# ──────────────────────────────────────────────────────────────────────


def audit_vault_content(docs: list[DatasetDoc]) -> tuple[list[str], list[str]]:
    """Per-dataset content audit (VAULT-03).

    Returns (warnings, errors). Errors fail the build; warnings are surfaced
    on stderr but don't block. Critical-vs-soft thresholds:
      ERROR (build-blocking): no overview, no api endpoint base URL, no slug,
                              a malformed `page:` block in the front matter
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
        errors.extend(f"{d.slug}: {e}" for e in d.page_errors)
        if d.new_template:
            errors.extend(f"{d.slug}: {e}" for e in anatomy_errors(d.page))
            continue
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


def resolve_chart(doc: DatasetDoc) -> tuple[dict[str, Any] | None, list[str], list[str]]:
    """The committed series for one dataset, after checking it against its spec.

    Returns:
        ``(chart, errors, notes)``. ``chart`` is ``None`` when the dataset has
        no spec, a ``none`` spec, or any error. Errors fail the build: an
        invalid spec, a spec without a series, a series without a spec, or a
        series distilled from a different spec than the one found today.
    """
    key = f"{doc.vendor_id}/{doc.slug}"
    try:
        spec, _origin, notes = chart_spec.resolve_spec(
            SITE_DIR, doc.vendor_id, doc.slug, doc.page.chart
        )
        series = chart_spec.load_series(SITE_DIR, doc.vendor_id, doc.slug)
    except (ValueError, TypeError) as exc:
        return None, [str(exc)], []
    if spec is not None:
        problems = chart_spec.validate_spec(spec)
        if problems:
            return None, [f"{key}: chart spec: {p}" for p in problems], notes
    errors = chart_spec.check_series(series, spec, key)
    if errors or spec is None or spec.get("type") == "none":
        return None, errors, notes
    return series, [], notes


def _fail(vendor_id: str, kind: str, errors: list[str]) -> None:
    print(
        f"[gridflow-build] {vendor_id}: {len(errors)} {kind} error(s) - failing build:",
        file=sys.stderr,
    )
    for e in errors:
        print(f"  ERROR: {e}", file=sys.stderr)
    sys.exit(1)


def build_vendor(
    env: Environment,
    vendor_id: str,
    vault_path: Path,
    out_root: Path,
    only: frozenset[str] = frozenset(),
) -> tuple[int, int]:
    """Render one vendor's dataset pages + hub.

    ``only`` (``<vendor>/<dataset>`` keys) renders just those pages, for a
    fast look at one page: no hub, no pruning, and every other page untouched.

    Returns ``(dataset_page_count, chart_page_count)``. Chart specs and series
    are checked for every dataset, authored overrides included, so a stale
    series fails the build even while an override hides the template.
    """
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
        _fail(vendor_id, "content", errors)

    charts: dict[str, dict[str, Any]] = {}
    chart_errors: list[str] = []
    for _path, doc in docs:
        chart, errs, notes = resolve_chart(doc)
        chart_errors.extend(errs)
        for note in notes:
            print(f"  NOTE: {note}", file=sys.stderr)
        if chart is not None:
            charts[doc.slug] = chart
    if chart_errors:
        _fail(vendor_id, "chart", chart_errors)

    # Family pages (v5 D5): the lead note's page lists every member; each
    # member's own address becomes a pointer to its section there.
    by_slug = {doc.slug: doc for _, doc in docs}
    family_of: dict[str, tuple[DatasetDoc, str]] = {}
    page_errors: list[str] = []
    for _path, doc in docs:
        fam = doc.page.family if doc.new_template else None
        if fam is None:
            continue
        if fam.slug in by_slug:
            page_errors.append(f"{doc.slug}: family slug {fam.slug!r} is also a dataset slug")
        for mem in fam.members:
            if mem.dataset not in by_slug:
                page_errors.append(f"{doc.slug}: family member {mem.dataset!r} has no vault note")
            elif mem.dataset in family_of:
                page_errors.append(f"{doc.slug}: {mem.dataset!r} is in two families")
            elif by_slug[mem.dataset].new_template and mem.dataset != doc.slug:
                page_errors.append(f"{mem.dataset}: a family member cannot have its own page block")
            else:
                family_of[mem.dataset] = (doc, fam.slug)
        if doc.slug not in {m.dataset for m in fam.members}:
            page_errors.append(f"{doc.slug}: a family's lead note must list itself as a member")
    if only:
        # Rendering a family lead also rewrites its members' pointers.
        only = only | {
            f"{vendor_id}/{member}"
            for member, (lead, _) in family_of.items()
            if f"{vendor_id}/{lead.slug}" in only
        }

    written: set[str] = set()
    n_charts = 0
    views: dict[str, tuple[DatasetDoc, dict[str, Any]]] = {}
    for _path, doc in docs:
        if not doc.new_template or (only and f"{vendor_id}/{doc.slug}" not in only):
            continue
        if (AUTHORED_DIR / vendor_id / f"{doc.slug}.html").exists():
            page_errors.append(
                f"{doc.slug}: the note is on the dataset template; delete its authored override"
            )
        arts, errs = check_artefacts(doc)
        arts.chart = charts.get(doc.slug)
        if doc.page.chart and doc.page.chart.get("type") != "none" and arts.chart is None:
            errs.append(f"{doc.slug}: page.chart has no committed series")
        members = []
        if doc.page.family is not None:
            members = [by_slug[m.dataset] for m in doc.page.family.members if m.dataset in by_slug]
        if not errs:
            view, errs = page_view(doc, arts, members)
            views[doc.slug] = (doc, view)
        page_errors.extend(errs)
    if page_errors:
        _fail(vendor_id, "dataset page", page_errors)

    for slug, (doc, view) in views.items():
        fam = doc.page.family
        out_name = f"{fam.slug}.html" if fam else f"{slug}.html"
        (out_dataset_dir / out_name).write_text(render_page(env, view), encoding="utf-8")
        written.add(out_name)
        n_charts += 1 if view["chart"] else 0
        print(f"  wrote: data-sources/{vendor_id}/{out_name} (dataset template)")

    for _path, doc in docs:
        if only and f"{vendor_id}/{doc.slug}" not in only:
            continue
        out_path = out_dataset_dir / f"{doc.slug}.html"
        authored = AUTHORED_DIR / vendor_id / f"{doc.slug}.html"
        if doc.slug in family_of:
            lead, fam_slug = family_of[doc.slug]
            href = f"{fam_slug}.html#{doc.slug}"
            out_path.write_text(
                render_redirect(env, f"{vendor_id}/{doc.slug}", href, lead.page.title or fam_slug),
                encoding="utf-8",
            )
            print(f"  wrote: data-sources/{vendor_id}/{doc.slug}.html (points to {href})")
        elif doc.new_template:
            continue
        elif authored.exists():
            # Authored pages carry their own markup verbatim, charts included;
            # they retire in Phase 25b, when the new template renders them.
            shutil.copy(authored, out_path)
            print(f"  wrote: data-sources/{vendor_id}/{doc.slug}.html (authored)")
        else:
            chart = charts.get(doc.slug)
            out_path.write_text(render_dataset(env, doc, manifest, chart=chart), encoding="utf-8")
            suffix = f" (chart: {chart['type']}, {len(chart['series'])} series)" if chart else ""
            print(f"  wrote: data-sources/{vendor_id}/{doc.slug}.html{suffix}")
            if chart:
                n_charts += 1
        written.add(out_path.name)

    if only:
        return len(docs), n_charts

    # The vendor directory is wholly generated (gitignored), so any page this
    # run did not write is left over from an earlier build: a dropped dataset
    # or a retired stub. Removing it keeps local output equal to a CI build.
    for stale in sorted(out_dataset_dir.glob("*.html")):
        if stale.name not in written:
            stale.unlink()
            print(f"  removed stale: data-sources/{vendor_id}/{stale.name}")

    hub_path = out_root / "data-sources" / f"{vendor_id}.html"
    authored_hub = AUTHORED_DIR / vendor_id / "_landing.html"
    if authored_hub.exists() and vendor_id not in _TEMPLATE_HUB_VENDORS:
        shutil.copy(authored_hub, hub_path)
        print(f"  wrote: data-sources/{vendor_id}.html (authored hub)")
    else:
        hub_html = render_vendor_hub(
            env, manifest, vendor_id, vendor_label, vendor_cfg["vendor_meta"]
        )
        hub_path.write_text(hub_html, encoding="utf-8")
        print(f"  wrote: data-sources/{vendor_id}.html")
    return len(docs), n_charts


def orphan_chart_files(vault_path: Path) -> list[str]:
    """Staged specs and series files naming a dataset the site does not build.

    ``build_vendor`` only checks datasets in a manifest, so a spec or series
    left behind after a dataset is dropped would otherwise sit unnoticed.
    """
    known = {
        (vendor_id, d["id"])
        for vendor_id in REAL_VENDORS
        if (vault_path / vendor_id).is_dir()
        for g in load_manifest(vendor_id)["groups"]
        for d in g["datasets"]
    }
    orphans: list[str] = []
    for root in (chart_spec.staging_dir(SITE_DIR), chart_spec.series_dir(SITE_DIR)):
        if not root.is_dir():
            continue
        for path in sorted(root.glob("*/*.json")):
            if (path.parent.name, path.stem) not in known:
                orphans.append(str(path.relative_to(REPO_ROOT)).replace("\\", "/"))
    return orphans


def new_template_pages(vault_path: Path) -> set[tuple[str, str]]:
    """``(vendor, slug)`` of every note with a ``page:`` block."""
    found: set[tuple[str, str]] = set()
    for vendor_id in REAL_VENDORS:
        for note in sorted((vault_path / vendor_id).glob("*.md")):
            if parse_page_fields(note.read_text(encoding="utf-8"))[0].present:
                found.add((vendor_id, note.stem))
    return found


def orphan_artefacts(pages: set[tuple[str, str]]) -> list[str]:
    """Committed sample or notebook files for a dataset that is not on the dataset template."""
    orphans: list[str] = []
    for root in (artefacts.samples_dir(SITE_DIR), artefacts.notebooks_dir(SITE_DIR)):
        if not root.is_dir():
            continue
        for path in sorted(root.glob("*/*.json")):
            if (path.parent.name, path.stem) not in pages:
                orphans.append(str(path.relative_to(REPO_ROOT)).replace("\\", "/"))
    return orphans


def build(
    vault_path: Path, output_dir: Path | None = None, only: frozenset[str] = frozenset()
) -> tuple[int, int, int]:
    """Render all vendor pages.

    Returns ``(n_dataset_pages, n_hubs, n_chart_pages)``; the last counts
    template-rendered pages that carry a distilled chart.
    """
    env = make_env()
    out_root = output_dir or SITE_DIR
    _reset_md_link_stats()
    _reset_caveat_stats()

    orphans = orphan_chart_files(vault_path)
    if orphans:
        _fail("charts", "orphan chart file", [f"{o}: no such dataset page" for o in orphans])
    _NEW_TEMPLATE_PAGES.clear()
    _NEW_TEMPLATE_PAGES.update(new_template_pages(vault_path))
    orphans = orphan_artefacts(_NEW_TEMPLATE_PAGES)
    if orphans:
        _fail("pages", "orphan artefact", [f"{o}: no dataset-template page" for o in orphans])

    n_pages = 0
    n_hubs = 0
    n_charts = 0
    for vendor_id in REAL_VENDORS:
        if not (vault_path / vendor_id).is_dir():
            print(f"  skip vendor (no vault dir): {vendor_id}")
            continue
        if only and not any(k.startswith(f"{vendor_id}/") for k in only):
            continue
        pages, chart_pages = build_vendor(env, vendor_id, vault_path, out_root, only)
        n_pages += pages
        n_charts += chart_pages
        n_hubs += 1

    print(
        f"[gridflow-build] charts: {n_charts} template page(s) carry a distilled series; "
        "every other page has no chart section"
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
    return n_pages, n_hubs, n_charts


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
    for path in snap.rglob("*.html"):
        if not (src / path.relative_to(snap)).exists():
            differing.append(f"{path.relative_to(snap)} (removed by the second build)")
    return differing


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
        "--only",
        action="append",
        default=[],
        metavar="VENDOR/DATASET",
        help="Render just this page (repeatable): no hubs, no pruning, no --check.",
    )
    args = parser.parse_args(argv)

    vault_path = resolve_vault_path(args.vault_path)
    print(f"[gridflow-build] vault: {vault_path}")

    if args.only:
        if args.check:
            parser.error("--only renders a subset; it cannot be combined with --check")
        build(vault_path, only=frozenset(args.only))
        print(f"[gridflow-build] rendered only {sorted(args.only)}")
        return 0

    n_pages, n_hubs, _ = build(vault_path)
    print(f"[gridflow-build] wrote {n_pages} dataset pages + {n_hubs} vendor hub(s)")

    if args.check:
        with tempfile.TemporaryDirectory(prefix="gridflow-build-check-") as tmp:
            tmp_path = Path(tmp)
            _snapshot_outputs(tmp_path)
            build(vault_path)
            differing = _diff_outputs(tmp_path)
            if differing:
                print(
                    f"[gridflow-build] FAIL: {len(differing)} file(s) differ between builds (non-idempotent):"
                )
                for p in differing:
                    print(f"    {p}")
                return 1
            print(f"[gridflow-build] OK: idempotent across {n_pages} pages + {n_hubs} hubs.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
