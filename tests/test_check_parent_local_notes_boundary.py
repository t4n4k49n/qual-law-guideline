from __future__ import annotations

from pathlib import Path

from scripts import check_parent_local_notes_boundary as mod


def test_main_passes_without_forbidden_paths(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(mod, "_collect_paths", lambda: ["docs/a.md", "src/x.py"])
    assert mod.main() == 0


def test_main_blocks_forbidden_paths(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        mod,
        "_collect_paths",
        lambda: ["TODO.md", "local_notes/TODO.md", "docs/ok.md"],
    )
    assert mod.main() == 1
