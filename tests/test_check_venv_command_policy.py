from __future__ import annotations

from pathlib import Path

from scripts import check_venv_command_policy as mod


def test_main_blocks_plain_python_command(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(mod, "TARGET_FILES", ("README.md",))
    (tmp_path / "README.md").write_text("python -m pytest\n", encoding="utf-8")
    assert mod.main() == 1


def test_main_allows_dot_venv_command(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(mod, "TARGET_FILES", ("README.md",))
    (tmp_path / "README.md").write_text(
        ".\\.venv\\Scripts\\python.exe -m pytest\n",
        encoding="utf-8",
    )
    assert mod.main() == 0
