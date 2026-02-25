from __future__ import annotations

from scripts import check_venv_runtime as mod


def test_is_venv_active_with_virtual_env(monkeypatch) -> None:
    monkeypatch.setenv("VIRTUAL_ENV", r"C:\repo\.venv")
    assert mod._is_venv_active() is True


def test_main_fails_when_not_in_venv(monkeypatch) -> None:
    monkeypatch.delenv("VIRTUAL_ENV", raising=False)
    monkeypatch.setattr(mod.sys, "executable", r"C:\Python311\python.exe")
    monkeypatch.setattr(mod.sys, "prefix", r"C:\Python311")
    assert mod.main() == 1
