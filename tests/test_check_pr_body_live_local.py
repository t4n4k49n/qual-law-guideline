from __future__ import annotations

from pathlib import Path

from scripts import check_pr_body_live_local as mod


def test_no_pr_returns_success(monkeypatch) -> None:
    monkeypatch.setattr(mod, "_load_current_pr", lambda: None)
    assert mod.main() == 0


def test_missing_marker_fails(monkeypatch) -> None:
    monkeypatch.setattr(mod, "_load_current_pr", lambda: {"body": "hello"})
    assert mod.main() == 1


def test_body_marker_and_file_must_match(tmp_path: Path, monkeypatch) -> None:
    marker = "docs/pr_bodies/pr-x.md"
    p = tmp_path / marker
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("## t\n\n<!-- PR_BODY_FILE: docs/pr_bodies/pr-x.md -->\n", encoding="utf-8", newline="\n")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(mod, "_load_current_pr", lambda: {"body": "## t\n\n<!-- PR_BODY_FILE: docs/pr_bodies/pr-x.md -->\n"})
    assert mod.main() == 0
