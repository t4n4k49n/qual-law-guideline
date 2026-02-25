from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path("scripts").resolve()))
from pr_body_guard_lib import (  # noqa: E402
    find_marker_path,
    is_safe_relative_path,
    validate_text_content,
)


def test_find_marker_path() -> None:
    text = "hello\n<!-- PR_BODY_FILE: runs/x/PR.md -->\n"
    assert find_marker_path(text) == "runs/x/PR.md"


def test_validate_text_content_detects_raw_newline_sequence() -> None:
    issues = validate_text_content(r"line1\nline2")
    assert any("raw '\\n' sequence" in x for x in issues)


def test_validate_text_content_detects_replacement_char() -> None:
    issues = validate_text_content("bad � text")
    assert any("replacement character" in x for x in issues)


def test_is_safe_relative_path() -> None:
    assert is_safe_relative_path("runs/20260101-000000000_x/PR.md")
    assert not is_safe_relative_path("../runs/x/PR.md")
    assert not is_safe_relative_path(r"runs\x\PR.md")
    assert not is_safe_relative_path("C:/abs/path.md")

