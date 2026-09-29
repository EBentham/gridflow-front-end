"""A literal ``---`` inside a note's front matter truncates it for the vault's scripts."""

from __future__ import annotations

from gridflow_front_end.page_fields import parse_page_fields

_GUARD = "front matter must not contain '---'"


def _note(key: str) -> str:
    return f"---\npage:\n  chart_view:\n    key:\n      {key}: fr\n---\nbody\n"


def test_a_literal_eic_key_is_rejected() -> None:
    errors = parse_page_fields(_note('"10YFR-RTE------C"'))[1]
    assert any(_GUARD in e for e in errors)


def test_escaped_dashes_pass_the_guard_and_decode_to_the_code() -> None:
    text = _note(r'"10YFR-RTE\x2D\x2D\x2D\x2D\x2D\x2DC"')
    assert "---" not in text.split("\n---", 1)[0][3:]
    assert not any(_GUARD in e for e in parse_page_fields(text)[1])


def test_an_escaped_code_in_a_string_value_passes() -> None:
    text = '---\npage:\n  name: "Load in 10YFR-RTE\\x2D\\x2D\\x2D\\x2D\\x2D\\x2DC"\n---\nbody\n'
    fields_errors = parse_page_fields(text)[1]
    assert not any("---" in e for e in fields_errors)


def test_a_note_without_a_page_block_is_not_checked() -> None:
    assert parse_page_fields("---\ntitle: a---b\n---\nbody\n")[1] == []
