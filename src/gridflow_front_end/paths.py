"""Repository paths shared by the build and the silver distil.

Kept free of third-party imports so ``gridflow-distil`` (polars) and
``gridflow-build`` (Jinja2) can each run with only their own extra.
"""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SITE_DIR = REPO_ROOT / "site" / "hifi"
DEFAULT_VAULT = REPO_ROOT / "vault"
DEFAULT_SILVER = Path("C:/gridflow-data/silver")


def resolve_vault_path(cli_arg: str | None) -> Path:
    """Vault root: CLI flag, then ``$GRIDFLOW_VAULT_PATH``, then the repo mirror."""
    if cli_arg:
        return Path(cli_arg).expanduser().resolve()
    env_path = os.environ.get("GRIDFLOW_VAULT_PATH")
    if env_path:
        return Path(env_path).expanduser().resolve()
    return DEFAULT_VAULT


def resolve_silver_path(cli_arg: str | None) -> Path:
    """Silver root: CLI flag, then ``$GRIDFLOW_SILVER_PATH``, then ``C:/gridflow-data/silver``."""
    if cli_arg:
        return Path(cli_arg).expanduser().resolve()
    env_path = os.environ.get("GRIDFLOW_SILVER_PATH")
    if env_path:
        return Path(env_path).expanduser().resolve()
    return DEFAULT_SILVER
