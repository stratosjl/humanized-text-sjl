#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for the memory-index dash exemption (I-10).

The operator's no-dash rule is global. The one shape that cannot comply is
the harness's own memory-index line, which is specified as a markdown list
item made of a link, a separator dash, and a one-line hook. These tests pin
both halves of the exemption: an index line passes, and ordinary prose using
the same character still fails.

Run with pytest, or standalone:

    pytest tests/
    python3 tests/test_index_line_exemption.py
"""
from __future__ import annotations

import importlib.util
import io
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HOOK = REPO / "scripts" / "greek_text_check.py"

# The hook reconfigures (or re-wraps) the standard streams at import time, as
# it has to for Windows cp1252. Hand it throwaway streams for the duration of
# the import, so pytest's capture files are not wrapped and later closed.
_streams = (sys.stdin, sys.stdout, sys.stderr)
sys.stdin = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")
sys.stdout = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")
sys.stderr = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")
_spec = importlib.util.spec_from_file_location("greek_text_check", HOOK)
gtc = importlib.util.module_from_spec(_spec)
try:
    _spec.loader.exec_module(gtc)
finally:
    sys.stdin, sys.stdout, sys.stderr = _streams

EM = gtc.EM_DASH
EN = gtc.EN_DASH


def hard_kinds(text: str) -> list[str]:
    return [v["kind"] for v in gtc.find_violations(text) if v.get("severity") == "hard"]


def dash_kinds(text: str) -> list[str]:
    return [k for k in hard_kinds(text) if k in ("em_dash", "en_dash")]


# --- the exemption holds -------------------------------------------------

def test_index_line_passes():
    line = f"- [Wi-Fi DFS channel collapse](wifi-dfs-channel-collapse.md) {EM} 286 Mbps recurrence means the router wandered off DFS; fix is to pin a non-DFS channel"
    assert dash_kinds(line) == []


def test_index_line_with_en_dash_passes():
    line = f"- [GUI sudo persistent elevation](gui-sudo-persistent-elevation.md) {EN} root via GUI dialog, cached until revoked"
    assert dash_kinds(line) == []


def test_index_line_variants_pass():
    variants = [
        f"* [Alt bullet](file.md) {EM} star bullets are the same shape",
        f"+ [Plus bullet](file.md) {EM} so are plus bullets",
        f"  - [Indented entry](nested/file.md) {EM} nested index entries are still index entries",
        f"- [No space around it](file.md){EM}hook packed against the separator",
    ]
    for line in variants:
        assert dash_kinds(line) == [], line


def test_index_line_inside_a_larger_file_passes():
    text = "\n".join([
        "# deskmeet-setup memory index",
        "",
        f"- [First entry](first.md) {EM} what the first entry is about",
        f"- [Second entry](second.md) {EM} what the second entry is about",
        "",
    ])
    assert dash_kinds(text) == []


# --- and it does not leak ------------------------------------------------

def test_prose_with_the_same_character_still_fails():
    line = f"Το κείμενο αυτό {EM} με παύλα στη μέση {EM} παραμένει παραβίαση."
    assert "em_dash" in hard_kinds(line)


def test_english_prose_with_the_same_character_still_fails():
    line = f"This sentence uses the separator {EM} and it must still be blocked."
    assert "em_dash" in hard_kinds(line)


def test_bullet_prose_without_a_link_still_fails():
    line = f"- a bullet of ordinary prose {EM} which is not an index entry"
    assert "em_dash" in hard_kinds(line)


def test_link_without_a_bullet_still_fails():
    line = f"[Some title](some-file.md) {EM} a hook with no list bullet is not the index shape"
    assert "em_dash" in hard_kinds(line)


def test_second_dash_in_the_hook_still_fails():
    line = f"- [Some title](some-file.md) {EM} a hook that then uses {EM} a second dash"
    assert "em_dash" in hard_kinds(line)


def test_overlong_hook_still_fails():
    line = f"- [Some title](some-file.md) {EM} " + ("x" * (gtc.INDEX_HOOK_MAX_CHARS + 1))
    assert "em_dash" in hard_kinds(line)


def test_empty_hook_still_fails():
    line = f"- [Some title](some-file.md) {EM}"
    assert "em_dash" in hard_kinds(line)


def test_prose_line_next_to_an_index_line_still_fails():
    text = "\n".join([
        f"- [Real entry](real.md) {EM} exempt because it is an index entry",
        f"Και μετά μια πρόταση {EM} που δεν είναι.",
    ])
    kinds = hard_kinds(text)
    assert "em_dash" in kinds
    assert len([k for k in kinds if k == "em_dash"]) == 1


def test_other_rules_still_apply_to_an_exempt_line():
    """The exemption covers the dash only, never the rest of the line."""
    line = f"- [Καταχώριση](entry.md) {EM} κείμενο, και κάτι ακόμη"
    kinds = hard_kinds(line)
    assert "em_dash" not in kinds
    assert "comma_kai" in kinds


def test_helper_predicate_is_narrow():
    assert gtc.is_memory_index_line(f"- [t](f.md) {EM} hook") is True
    assert gtc.is_memory_index_line(f"just prose {EM} here") is False
    assert gtc.is_memory_index_line("- [t](f.md) plain hyphen - hook") is False


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if not name.startswith("test_") or not callable(fn):
            continue
        try:
            fn()
            print(f"PASS  {name}")
        except AssertionError as exc:
            failures += 1
            print(f"FAIL  {name}: {exc}")
    print(f"\n{failures} failure(s)")
    sys.exit(1 if failures else 0)
