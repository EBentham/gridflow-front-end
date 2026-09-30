"""Append gridflow defect rows to the remediation list: gridflow BACKLOG (local) and the vault page (tracked).

Rows go in after the last row of their item, or at the end if the item is new (write the item's heading and table
header into the rows file in that case). The vault copy is committed and pushed on the vault worktree's current branch,
which must be a docs branch, never master.

Usage:
    python logdefects.py <item> <rows.md> <vault-worktree> "<commit message>"

Example:
    python logdefects.py 15 rows.md C:/.../scratchpad/vault-issues "docs(gridflow): remediation list, ENTSOG 15a-15c"
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BACKLOG = Path("C:/Users/Bobbo/OneDrive/Desktop/Python/gridflow/.planning/BACKLOG.md")
REL = "10-projects/gridflow/specs/remediation-from-site-batches.md"


def _insert(path: Path, item: str, rows: list[str]) -> None:
    raw = path.read_bytes()
    crlf = b"\r\n" in raw
    lines = raw.decode("utf-8").replace("\r\n", "\n").split("\n")
    hits = [n for n, line in enumerate(lines) if line.startswith(f"| {item}")]
    at = hits[-1] + 1 if hits else len(lines)
    lines[at:at] = rows
    text = "\n".join(lines)
    path.write_bytes((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))
    print(f"{path}: +{len(rows)} at line {at + 1}")


def main() -> None:
    item, rows_path, vault, message = sys.argv[1:5]
    rows = Path(rows_path).read_text(encoding="utf-8").strip("\n").split("\n")
    branch = subprocess.run(
        ["git", "branch", "--show-current"], cwd=vault, check=True, capture_output=True, text=True
    ).stdout.strip()
    if branch in {"master", "main"}:
        sys.exit(f"vault worktree is on {branch}; switch to a docs branch first")
    _insert(BACKLOG, item, rows)
    _insert(Path(vault) / REL, item, rows)
    subprocess.run(["git", "add", REL], cwd=vault, check=True)
    subprocess.run(["git", "commit", "-q", "-m", message], cwd=vault, check=True)
    subprocess.run(["git", "push", "-q", "-u", "origin", branch], cwd=vault, check=True)


if __name__ == "__main__":
    main()
