from __future__ import annotations

from pathlib import Path

from scripts.check_bidi_controls import _is_forbidden, _scan_file


def test_is_forbidden_detects_bidi_and_control_chars() -> None:
    assert _is_forbidden(0x202E) is True
    assert _is_forbidden(0x07) is True
    assert _is_forbidden(0x09) is False


def test_scan_file_reports_disallowed_control_char(tmp_path: Path) -> None:
    p = tmp_path / "sample.md"
    p.write_text("ok\nbad:\x07\n", encoding="utf-8", newline="\n")
    findings = _scan_file(p)

    assert len(findings) == 1
    line_no, col_no, codepoint, _ = findings[0]
    assert line_no == 2
    assert col_no == 5
    assert codepoint == 0x07
