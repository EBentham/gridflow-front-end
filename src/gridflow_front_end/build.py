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
import math
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
    },
    "entsoe": {"label": "ENTSO-E", "vendor_doc_base": "https://transparency.entsoe.eu/"},
    "entsog": {"label": "ENTSO-G", "vendor_doc_base": "https://transparency.entsog.eu/"},
    "gie": {"label": "GIE AGSI+ and ALSI", "vendor_doc_base": "https://agsi.gie.eu/"},
    "neso": {
        "label": "NESO Carbon Intensity",
        "vendor_doc_base": "https://carbonintensity.org.uk/",
    },
    "openmeteo": {"label": "Open-Meteo", "vendor_doc_base": "https://open-meteo.com/en/docs"},
    "neso_data_portal": {
        "label": "NESO Data Portal",
        "vendor_doc_base": "https://www.neso.energy/data-portal/api-guidance",
    },
}


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
            cache[vendor_id] = set(manifest_datasets(manifest))
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
    """A vendor's page set and hub content, ``site/hifi/data/<vendor>.json``.

    ``groups`` list the vendor's pages in hub order; a page is a dataset slug or a family slug.
    ``families`` name each family's members, the lead first; ``names`` give each single dataset
    the plain name its hub row and blank page carry. Datasets in ``dropped`` have no page.
    """
    path = SITE_DIR / "data" / f"{vendor_id}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_families(manifest: dict) -> dict[str, dict]:
    """Family slug → the family entry (``slug``, ``title``, ``members``, lead first)."""
    return {f["slug"]: f for f in manifest.get("families", [])}


def manifest_datasets(manifest: dict) -> list[str]:
    """Every dataset slug in the vendor's page set, in hub order (family members in family order)."""
    fams = manifest_families(manifest)
    out: list[str] = []
    for group in manifest["groups"]:
        for page in group["pages"]:
            out.extend(fams[page]["members"] if page in fams else [page])
    return out


def manifest_total_count(manifest: dict) -> int:
    """The number of datasets the vendor's pages document (ruling: computed, never hand-typed)."""
    return len(manifest_datasets(manifest))


def manifest_errors(vendor_id: str, manifest: dict) -> list[str]:
    """Structural checks on a vendor's page set."""
    errors: list[str] = []
    fams = manifest_families(manifest)
    pages = [p for g in manifest["groups"] for p in g["pages"]]
    if len(pages) != len(set(pages)):
        errors.append(f"{vendor_id}: a page is listed in two groups")
    for slug in fams:
        if slug not in pages:
            errors.append(f"{vendor_id}: family {slug!r} is in no group")
    datasets = manifest_datasets(manifest)
    if len(datasets) != len(set(datasets)):
        errors.append(f"{vendor_id}: a dataset is in two families or listed twice")
    clash = sorted(set(fams) & set(datasets))
    if clash:
        errors.append(f"{vendor_id}: family slug(s) {clash} are also dataset slugs")
    for page in pages:
        if page not in fams and page not in manifest.get("names", {}):
            errors.append(f"{vendor_id}: {page!r} has no plain name in `names`")
    dropped = sorted(set(manifest.get("dropped", {})) & set(datasets))
    if dropped:
        errors.append(f"{vendor_id}: {dropped} are both dropped and on a page")
    return errors


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


# ──────────────────────────────────────────────────────────────────────
# The dataset page template (locked anatomy, v5 Phase 25b)
# ──────────────────────────────────────────────────────────────────────

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


# Columns every silver table carries; the frame shows them, the guide gives them no line.
PIPELINE_COLUMNS = frozenset({"data_provider", "ingested_at", *artefacts.LINEAGE_COLUMNS})

# The frame's width budget, as silver prints it (the locked schema board): Red Hat Mono's advance at
# 13 px, cell padding, the key square and Polars' `…` column. Past 1280 px, columns fold into `…`.
_FRAME_BUDGET = 1280
_FRAME_CH = 7.8
_FRAME_PAD = 16
_FRAME_KEY_W = 14
_FRAME_EL_W = 30
_POLARS_DTYPES = {
    "Boolean": "bool",
    "Date": "date",
    "Float32": "f32",
    "Float64": "f64",
    "Int8": "i8",
    "Int16": "i16",
    "Int32": "i32",
    "Int64": "i64",
    "UInt8": "u8",
    "UInt16": "u16",
    "UInt32": "u32",
    "UInt64": "u64",
    "String": "str",
    "Time": "time",
}
_DATETIME_DTYPE = re.compile(r"^Datetime\((ns|us|ms)(?:, (.+))?\)$")
_NUMERIC_POLARS = re.compile(r"^[iuf]\d+$")


def polars_dtype(label: str) -> str:
    """A committed sample's dtype label as Polars prints it over a column (``datetime[μs, UTC]``)."""
    if label in _POLARS_DTYPES:
        return _POLARS_DTYPES[label]
    m = _DATETIME_DTYPE.match(label)
    if m:
        unit = "μs" if m.group(1) == "us" else m.group(1)
        return f"datetime[{unit}, {m.group(2)}]" if m.group(2) else f"datetime[{unit}]"
    return label.lower()


def _frame_view(doc: DatasetDoc, sample: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """The silver section: the sample rows as a Polars frame, then the column guide beneath.

    Every column is in the frame. Columns past the width budget (from ``ingested_at`` on, then more
    while the frame is wider than 1280 px) fold behind Polars' ``…`` column, which a visually hidden
    checkbox opens in place. The guide has one line per column that is not a pipeline column, key
    columns first, each group in frame order.
    """
    key = f"{doc.vendor_id}/{doc.slug}"
    rec = doc.page.record
    errors: list[str] = []
    cols = sample["columns"]
    names = [c["name"] for c in cols]
    pipeline = {c["name"] for c in cols if c["lineage"]} | (PIPELINE_COLUMNS & set(names))
    guided = [n for n in names if n not in pipeline]
    missing = [n for n in guided if n not in rec.fields]
    if missing:
        errors.append(f"{key}: page.record.fields has no meaning for {missing}")
    extra = sorted(set(rec.fields) - set(names))
    if extra:
        errors.append(f"{key}: page.record.fields names columns silver does not have: {extra}")
    bad_key = [k for k in rec.key if k not in names]
    if bad_key:
        errors.append(f"{key}: page.record.key names columns silver does not have: {bad_key}")

    dtypes = [polars_dtype(c["dtype"]) for c in cols]

    def cell(i: int, value: str | None) -> str | None:
        if value is None:
            return None
        return f'"{value}"' if dtypes[i] == "str" else value

    rows = [[cell(i, v) for i, v in enumerate(row)] for row in sample["rows"]]

    def width(i: int) -> int:
        chars = max(len(names[i]), len(dtypes[i]), *(len(r[i] or "null") for r in rows))
        w = math.ceil(chars * _FRAME_CH) + _FRAME_PAD + 1
        if names[i] in rec.key:
            w = max(w, math.ceil(len(names[i]) * _FRAME_CH) + _FRAME_KEY_W + _FRAME_PAD + 1)
        return w

    cut = names.index("ingested_at") if "ingested_at" in names else len(names)
    while cut > 1 and sum(width(i) for i in range(cut)) + _FRAME_EL_W + 3 > _FRAME_BUDGET:
        cut -= 1
    folded = names[cut:]
    columns = [
        {
            "name": n,
            "dtype": dtypes[i],
            "key": n in rec.key,
            "folded": i >= cut,
            "num": bool(_NUMERIC_POLARS.match(dtypes[i])),
        }
        for i, n in enumerate(names)
    ]

    def entry(n: str) -> dict[str, Any]:
        return {
            "name": n,
            "k": names.index(n) + 1,
            "folded": n in folded,
            "meaning": rec.fields.get(n, ""),
        }

    relation = f"silver_{sample['silver'].replace('/', '_')}"
    view = {
        "shape": f"({len(rows)}, {len(names)})",
        "caption": rec.caption,
        "columns": columns,
        "rows": rows,
        "n_folded": len(folded),
        "aria": (
            f"Sample rows from {relation}: {len(rows)} rows of {len(names)} columns"
            + (f", the last {len(folded)} folded." if folded else ".")
        ),
        "keyed": [entry(n) for n in guided if n in rec.key],
        "others": [entry(n) for n in guided if n not in rec.key],
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
        record_v, rec_errors = _frame_view(doc, arts.sample)
        errors.extend(rec_errors)

    related = []
    slugs = _all_manifest_slugs()
    for rel in p.related:
        vendor, _, slug = rel.dataset.partition("/")
        if slug not in slugs.get(vendor, set()):
            errors.append(f"{key}: related {rel.dataset} has no page on the site")
            continue
        href = f"{slug}.html" if vendor == doc.vendor_id else f"../{vendor}/{slug}.html"
        related.append({"href": href, "key": _breakable(rel.dataset), "note": rel.note})

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
        "blank": False,
        "chips": [{"key": v["key"], "id": None} for v in variants] or [{"key": key, "id": None}],
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


def blank_view(
    vendor_id: str, vendor_label: str, page: str, title: str, members: list[str]
) -> dict[str, Any]:
    """A page in the page set whose note has no ``page:`` block yet: the hero's name and id only.

    A family's blank page carries one chip per member, each with the member's id, so the members'
    old addresses (``<member>.html`` → ``<family>.html#<member>``) land on their own chip.
    """
    chips = (
        [{"key": f"{vendor_id}/{m}", "id": m} for m in members]
        if members
        else [{"key": f"{vendor_id}/{page}", "id": None}]
    )
    return {
        "blank": True,
        "vendor_id": vendor_id,
        "vendor_label": vendor_label,
        "key": f"{vendor_id}/{page}",
        "chips": chips,
        "title": title,
        "summary_plain": f"{title}, from {vendor_label}: {', '.join(c['key'] for c in chips)}.",
        "landscape": _DEFAULT_LANDSCAPE.get(vendor_id, "power"),
    }


_COUNT_WORDS = ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def _count_word(n: int) -> str:
    return _COUNT_WORDS[n] if n < len(_COUNT_WORDS) else str(n)


_CODE_SPAN = re.compile(r"(<code>)([^<]*)(</code>)")


def _wbr(escaped: str) -> str:
    """Offer a line break after each underscore and slash of an escaped code, never inside a word."""
    return escaped.replace("_", "_<wbr>").replace("/", "/<wbr>")


def _breakable(code: str) -> Markup:
    """A dataset key or path that may wrap at its underscores and slashes in a narrow column."""
    if code.startswith("<code>"):
        m = _CODE_SPAN.fullmatch(code)
        return Markup(f"{m.group(1)}{_wbr(m.group(2))}{m.group(3)}") if m else Markup(code)
    return Markup(_wbr(html_escape(code, quote=False)))


def _hub_rows(
    vendor_id: str, manifest: dict, docs: dict[str, DatasetDoc], pages: list[str]
) -> list[dict[str, Any]]:
    fams = manifest_families(manifest)
    rows = []
    for page in pages:
        fam = fams.get(page)
        if fam:
            lead = docs[fam["members"][0]]
            rows.append(
                {
                    "href": f"{vendor_id}/{page}.html",
                    "codes": [_breakable(m) for m in fam["members"]],
                    "title": lead.page.title
                    if lead.new_template and lead.page.title
                    else fam["title"],
                    "path": "",
                }
            )
        else:
            doc = docs[page]
            rows.append(
                {
                    "href": f"{vendor_id}/{page}.html",
                    "codes": [_breakable(page)],
                    "title": manifest["names"][page],
                    "path": _breakable(doc.api_path) if doc.api_path.startswith("/") else "",
                }
            )
    return rows


def hub_view(vendor_id: str, manifest: dict, docs: dict[str, DatasetDoc]) -> dict[str, Any]:
    """The vendor hub (direction A, "Sections"): hero and facts, the grouped datasets, silver, gold."""
    n = manifest_total_count(manifest)
    facts = [
        (
            k,
            Markup(
                _CODE_SPAN.sub(
                    lambda m: str(_breakable(m.group(0))), _markdown_inline(v, vendor_id)
                )
            ),
        )
        for k, v in manifest["facts"]
    ]
    facts.append(("Datasets", Markup(str(n))))
    groups = []
    for i, g in enumerate(manifest["groups"]):
        groups.append(
            {
                "id": f"g{i + 1}",
                "name": g["name"],
                "blurb": g["blurb"],
                "rows": _hub_rows(vendor_id, manifest, docs, g["pages"]),
            }
        )
    keys = manifest["source_keys"]
    views = " or ".join(f"<code>silver_{k}_{{dataset}}</code>" for k in keys)
    latest = manifest.get("latest_views", [])
    if latest:
        how_many = (
            f"All {_count_word(n)}" if len(latest) == n else _count_word(len(latest)).capitalize()
        )
        silver = {
            "title": "In silver, every capture is kept",
            "text": Markup(
                f"Each dataset is one DuckDB view, {views}. {how_many} are append-only: a later "
                "publication never overwrites an earlier one, each capture is its own "
                "<code>_run{available_at}</code> file, and a <code>_latest</code> view returns the "
                "newest capture for each key."
            ),
            "views": [f"silver_{keys[0]}_{d}_latest" for d in latest],
        }
    else:
        silver = {
            "title": "In silver, one view per dataset",
            "text": Markup(
                f"Each dataset is one DuckDB view, {views}: typed, validated and deduplicated on "
                "the dataset’s key."
            ),
            "views": [],
        }
    nb = manifest["notebook"]
    well = Markup(
        highlight(
            f"data.{nb['source']}.list_datasets()\n"
            f'df = data.{nb["source"]}.query("{nb["dataset"]}", start, end)'
        )
    )
    return {
        "vendor_id": vendor_id,
        "name": manifest["name"],
        "intro": manifest["intro"],
        "facts": facts,
        "landscape": manifest["landscape"],
        "land_class": "hub-land" if manifest["landscape"] == "elexon" else "ds-land",
        "n": n,
        "groups": groups,
        "groups_title": (
            f"The datasets, in {_count_word(len(groups))} groups"
            if len(groups) > 1
            else "The datasets"
        ),
        "groups_note": manifest.get("groups_note", ""),
        "silver": silver,
        "well": well,
    }


def render_hub(env: Environment, view: dict[str, Any]) -> str:
    """Render one vendor hub."""
    return env.get_template("hub.html.j2").render(v=view)


# The names of one dataset through the layers (direction A board, verbatim).
_LANDING_NAMES = [
    ("vendor endpoint", "/balancing/settlement/system-prices/{date}"),
    ("raw responses", "bronze/elexon/system_prices/"),
    ("typed Parquet", "silver/elexon/system_prices/"),
    ("DuckDB view", "silver_elexon_system_prices_latest"),
    ("notebook", 'data.elexon.query("system_prices", start, end)'),
]
# Where each vendor sits on the landing's grid (column, row), in cable order west to east.
_LANDING_GRID = {
    "elexon": (1, 1),
    "neso": (2, 2),
    "neso_data_portal": (2, 1),
    "openmeteo": (3, 2),
    "gie": (3, 1),
    "entsog": (4, 2),
    "entsoe": (4, 1),
}


def _page_href(vendor_id: str, manifest: dict, slug: str) -> str:
    """The address of a dataset's page from the site root's data-sources/ directory."""
    for fam in manifest_families(manifest).values():
        if slug in fam["members"]:
            return f"data-sources/{vendor_id}/{fam['slug']}.html#{slug}"
    return f"data-sources/{vendor_id}/{slug}.html"


def landing_view(manifests: dict[str, dict], chart: dict[str, Any] | None) -> dict[str, Any]:
    """The Data sources landing: every vendor, a few datasets to start with, one dataset's names."""
    vendors = []
    for vendor_id, m in manifests.items():
        land = m["landing"]
        col, row = _LANDING_GRID[vendor_id]
        vendors.append(
            {
                "id": vendor_id,
                "order": land["order"],
                "name": m["name"],
                "bronze": land["bronze"],
                "desc": land["desc"],
                "fact": f"{manifest_total_count(m)} datasets, {land['fact']}",
                "col": col,
                "row": row,
                "start": [
                    {"href": _page_href(vendor_id, m, k), "code": k, "gloss": g}
                    for k, g in land["start"]
                ],
            }
        )
    vendors.sort(key=lambda v: v["order"])
    n = sum(manifest_total_count(m) for m in manifests.values())
    return {
        "n": n,
        "vendors": vendors,
        "names": [(label, _breakable(name)) for label, name in _LANDING_NAMES],
        "chart": chart,
    }


def landing_chart(vault_path: Path) -> dict[str, Any] | None:
    """The system_prices page's own chart, drawn again beside its names on the landing."""
    note = vault_path / "elexon" / "system_prices.md"
    if not note.is_file():
        return None
    doc = parse_vault_file(note, vendor_id="elexon", vendor_label=REAL_VENDORS["elexon"]["label"])
    chart, errors, _ = resolve_chart(doc)
    if chart is None or errors or not doc.new_template:
        return None
    if chart_svg.check_view(chart, doc.page.chart_view):
        return None
    wide, narrow = chart_svg.render(chart, doc.page.chart_view, "lc", wide=chart_svg.LANDING)
    return {
        "title": doc.page.chart_view.title,
        "caption": doc.page.chart_view.caption,
        "wide": Markup(wide),
        "narrow": Markup(narrow),
    }


def render_landing(env: Environment, view: dict[str, Any]) -> str:
    """Render the Data sources landing."""
    return env.get_template("data-sources.html.j2").render(v=view)


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
) -> tuple[int, int, int]:
    """Render one vendor's pages, family pointers and hub.

    Every page in the vendor's page set renders: on the dataset template when its note (a family's
    lead note) has a ``page:`` block, else blank (the hero's name and id only). ``only``
    (``<vendor>/<dataset>`` keys) renders just those pages: no hub, no pruning.

    Returns ``(datasets_documented, pages_written, chart_pages)``.
    """
    manifest = load_manifest(vendor_id)
    vendor_label = manifest["name"]
    vendor_dir = vault_path / vendor_id
    if not vendor_dir.is_dir():
        sys.exit(
            f"[gridflow-build] ERROR: vault directory not found: {vendor_dir}\n"
            f"  Set --vault-path or $GRIDFLOW_VAULT_PATH, or vendor vault content into "
            f"{DEFAULT_VAULT.relative_to(REPO_ROOT)}/."
        )
    errors = manifest_errors(vendor_id, manifest)
    if errors:
        _fail(vendor_id, "page set", errors)
    out_dataset_dir = out_root / "data-sources" / vendor_id
    out_dataset_dir.mkdir(parents=True, exist_ok=True)
    fams = manifest_families(manifest)
    datasets = manifest_datasets(manifest)
    vault_slugs = {p.stem for p in vendor_dir.glob("*.md")}
    missing_in_vault = sorted(set(datasets) - vault_slugs)
    if missing_in_vault:
        sys.exit(
            f"[gridflow-build] ERROR: the page set names datasets without vault notes: {missing_in_vault}"
        )
    for slug in sorted(vault_slugs - set(datasets)):
        print(f"  skip (not in the page set): {vendor_id}/{slug}")
    docs = {
        slug: parse_vault_file(
            vendor_dir / f"{slug}.md", vendor_id=vendor_id, vendor_label=vendor_label
        )
        for slug in datasets
    }

    # VAULT-03 audit
    warnings, errors = audit_vault_content(list(docs.values()))
    if warnings:
        print(f"[gridflow-build] {vendor_id}: {len(warnings)} content warning(s):", file=sys.stderr)
        for w in warnings:
            print(f"  WARN: {w}", file=sys.stderr)
    if errors:
        _fail(vendor_id, "content", errors)

    charts: dict[str, dict[str, Any]] = {}
    chart_errors: list[str] = []
    for doc in docs.values():
        chart, errs, notes = resolve_chart(doc)
        chart_errors.extend(errs)
        for note in notes:
            print(f"  NOTE: {note}", file=sys.stderr)
        if chart is not None:
            charts[doc.slug] = chart
    if chart_errors:
        _fail(vendor_id, "chart", chart_errors)

    # Families (ruling: each family is one page): the page set names them; a lead note's
    # page.family, once written, must agree with it.
    family_of = {m: fam for fam in fams.values() for m in fam["members"]}
    page_errors: list[str] = []
    for doc in docs.values():
        if not doc.new_template:
            continue
        fam = family_of.get(doc.slug)
        declared = doc.page.family
        if fam is None:
            if declared is not None:
                page_errors.append(
                    f"{doc.slug}: page.family names a family the page set does not have"
                )
        elif doc.slug != fam["members"][0]:
            page_errors.append(
                f"{doc.slug}: only the lead note of family {fam['slug']!r} "
                f"({fam['members'][0]}) carries a page block"
            )
        elif declared is None:
            page_errors.append(
                f"{doc.slug}: leads family {fam['slug']!r}; its page block needs page.family"
            )
        elif declared.slug != fam["slug"] or {m.dataset for m in declared.members} != set(
            fam["members"]
        ):
            page_errors.append(
                f"{doc.slug}: page.family must match the page set: slug {fam['slug']!r}, "
                f"members {fam['members']}"
            )
    if page_errors:
        _fail(vendor_id, "dataset page", page_errors)

    pages = [p for g in manifest["groups"] for p in g["pages"]]
    views: dict[str, dict[str, Any]] = {}
    for page in pages:
        fam = fams.get(page)
        members = fam["members"] if fam else [page]
        if only and not any(f"{vendor_id}/{m}" in only for m in members):
            continue
        lead = docs[members[0]]
        if not lead.new_template:
            title = fam["title"] if fam else manifest["names"][page]
            views[page] = blank_view(vendor_id, vendor_label, page, title, members if fam else [])
            continue
        arts, errs = check_artefacts(lead)
        arts.chart = charts.get(lead.slug)
        if lead.page.chart and lead.page.chart.get("type") != "none" and arts.chart is None:
            errs.append(f"{lead.slug}: page.chart has no committed series")
        if not errs:
            view, errs = page_view(lead, arts, [docs[m] for m in members] if fam else [])
            views[page] = view
        page_errors.extend(errs)
    if page_errors:
        _fail(vendor_id, "dataset page", page_errors)

    written: set[str] = set()
    n_charts = 0
    for page, view in views.items():
        out_name = f"{page}.html"
        (out_dataset_dir / out_name).write_text(render_page(env, view), encoding="utf-8")
        written.add(out_name)
        n_charts += 1 if view.get("chart") else 0
        kind = "blank" if view.get("blank") else "dataset template"
        print(f"  wrote: data-sources/{vendor_id}/{out_name} ({kind})")
        fam = fams.get(page)
        for member in fam["members"] if fam else []:
            href = f"{page}.html#{member}"
            (out_dataset_dir / f"{member}.html").write_text(
                render_redirect(env, f"{vendor_id}/{member}", href, view["title"]), encoding="utf-8"
            )
            written.add(f"{member}.html")

    if only:
        return len(datasets), len(views), n_charts

    # The vendor directory is wholly generated (gitignored), so any page this
    # run did not write is left over from an earlier build: a dropped dataset
    # or a retired stub. Removing it keeps local output equal to a CI build.
    for stale in sorted(out_dataset_dir.glob("*.html")):
        if stale.name not in written:
            stale.unlink()
            print(f"  removed stale: data-sources/{vendor_id}/{stale.name}")

    hub_path = out_root / "data-sources" / f"{vendor_id}.html"
    hub_path.write_text(render_hub(env, hub_view(vendor_id, manifest, docs)), encoding="utf-8")
    print(f"  wrote: data-sources/{vendor_id}.html (hub)")
    return len(datasets), len(views), n_charts


def orphan_chart_files(vault_path: Path) -> list[str]:
    """Staged specs and series files naming a dataset the site does not build.

    ``build_vendor`` only checks datasets in a manifest, so a spec or series
    left behind after a dataset is dropped would otherwise sit unnoticed.
    """
    known = {
        (vendor_id, d)
        for vendor_id in REAL_VENDORS
        if (vault_path / vendor_id).is_dir()
        for d in manifest_datasets(load_manifest(vendor_id))
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
    """Render every vendor's pages and hub, then the Data sources landing.

    Returns ``(n_datasets, n_pages, n_hubs)``: the datasets the pages document, the pages
    written (family pointers not counted) and the hubs.
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

    n_datasets = 0
    n_pages = 0
    n_hubs = 0
    n_charts = 0
    manifests: dict[str, dict] = {}
    for vendor_id in REAL_VENDORS:
        if not (vault_path / vendor_id).is_dir():
            print(f"  skip vendor (no vault dir): {vendor_id}")
            continue
        if only and not any(k.startswith(f"{vendor_id}/") for k in only):
            continue
        datasets, pages, chart_pages = build_vendor(env, vendor_id, vault_path, out_root, only)
        manifests[vendor_id] = load_manifest(vendor_id)
        n_datasets += datasets
        n_pages += pages
        n_charts += chart_pages
        n_hubs += 0 if only else 1

    if not only and len(manifests) == len(REAL_VENDORS):
        landing = landing_view(manifests, landing_chart(vault_path))
        (out_root / "data-sources.html").write_text(render_landing(env, landing), encoding="utf-8")
        print(f"  wrote: data-sources.html (landing: {landing['n']} datasets)")

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
    return n_datasets, n_pages, n_hubs


def _generated(root: Path) -> list[Path]:
    """Every file the build writes under ``root`` (a site root or a snapshot of one)."""
    out = sorted((root / "data-sources").rglob("*.html"))
    landing = root / "data-sources.html"
    return [*out, landing] if landing.exists() else out


def _snapshot_outputs(temp_dir: Path) -> None:
    """Copy current generated outputs into temp_dir for diff comparison."""
    if (temp_dir / "data-sources").exists():
        shutil.rmtree(temp_dir / "data-sources")
    for path in _generated(SITE_DIR):
        out = temp_dir / path.relative_to(SITE_DIR)
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, out)


def _diff_outputs(temp_dir: Path) -> list[str]:
    """Compare the snapshot in temp_dir against current outputs. Return list of differing paths."""
    differing: list[str] = []
    for path in _generated(SITE_DIR):
        rel = path.relative_to(SITE_DIR)
        snap_path = temp_dir / rel
        if not snap_path.exists() or not filecmp.cmp(str(path), str(snap_path), shallow=False):
            differing.append(str(rel))
    for path in _generated(temp_dir):
        if not (SITE_DIR / path.relative_to(temp_dir)).exists():
            differing.append(f"{path.relative_to(temp_dir)} (removed by the second build)")
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

    n_datasets, n_pages, n_hubs = build(vault_path)
    print(
        f"[gridflow-build] wrote {n_pages} dataset pages ({n_datasets} datasets) "
        f"+ {n_hubs} vendor hub(s) + the landing"
    )

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
