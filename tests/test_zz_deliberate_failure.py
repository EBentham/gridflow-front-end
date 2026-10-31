"""Scratch branch only, never merged: a deliberately failing test.

It shows that a red check blocks the deploy job.
"""


def test_deliberate_failure() -> None:
    assert False, "deliberate failure: the deploy job must not run"
