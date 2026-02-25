from __future__ import annotations

from pathlib import Path

from scripts import check_parent_root_notes_absent as mod


def test_main_passes_when_root_notes_absent(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    assert mod.main() == 0


def test_main_blocks_when_root_todo_exists(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "TODO.md").write_text("x", encoding="utf-8")
    assert mod.main() == 1
