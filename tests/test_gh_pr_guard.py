from __future__ import annotations

from pathlib import Path

import pytest

from scripts import gh_pr_guard as mod


def _write_body(path: Path, marker_path: str, extra: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "## t\n\n"
        f"{extra}"
        f"<!-- PR_BODY_FILE: {marker_path} -->\n",
        encoding="utf-8",
        newline="\n",
    )


def test_extract_body_file_rejects_body_option() -> None:
    with pytest.raises(ValueError):
        mod._extract_body_file(["--body", "x"])


def test_validate_body_file_requires_marker_match(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    p = Path("docs/pr_bodies/pr-1.md")
    _write_body(p, "docs/pr_bodies/other.md")
    with pytest.raises(ValueError):
        mod._validate_body_file(p.as_posix())


def test_validate_body_file_passes(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    p = Path("docs/pr_bodies/pr-1.md")
    _write_body(p, p.as_posix())
    mod._validate_body_file(p.as_posix())
