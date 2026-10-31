"""`gridflow-build --check` fails when the vault mirror's sync stamp is missing or malformed."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import pytest

from gridflow_front_end import build
from gridflow_front_end.paths import DEFAULT_VAULT


def _check(vault: Path, monkeypatch: pytest.MonkeyPatch) -> int:
    """``gridflow-build --check`` against ``vault``, with the page build itself stubbed out."""
    monkeypatch.setattr(build, "build", lambda *args, **kwargs: (0, 0, 0))
    return build.main(["--check", "--vault-path", str(vault)])


def _stamp(vault: Path, text: str) -> None:
    (vault / ".last_synced_from_vault").write_text(text, encoding="utf-8")


def _synced(days_ago: int) -> str:
    when = dt.datetime.now(dt.UTC) - dt.timedelta(days=days_ago)
    return json.dumps({"synced_at_utc": when.strftime("%Y-%m-%dT%H:%M:%SZ")})


def test_a_missing_stamp_fails_the_check(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    assert _check(tmp_path, monkeypatch) == 1


@pytest.mark.parametrize(
    "text",
    ["not json", "{}", '{"synced_at_utc": "21 August 2026"}', '{"synced_at_utc": null}', "[1]"],
)
def test_a_malformed_stamp_fails_the_check(
    text: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _stamp(tmp_path, text)
    assert _check(tmp_path, monkeypatch) == 1


def test_a_valid_stamp_passes_and_an_old_one_only_warns(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _stamp(tmp_path, _synced(1))
    assert _check(tmp_path, monkeypatch) == 0
    assert "WARNING" not in capsys.readouterr().err
    _stamp(tmp_path, _synced(45))
    assert _check(tmp_path, monkeypatch) == 0
    assert "days old" in capsys.readouterr().err


def test_the_committed_mirror_carries_a_valid_stamp() -> None:
    assert build.check_stamp(DEFAULT_VAULT / build.STAMP_FILENAME)
