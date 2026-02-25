from __future__ import annotations

from scripts import run_guard_stage as mod


class _DummyProc:
    def __init__(self, returncode: int = 0, stdout: bytes = b"") -> None:
        self.returncode = returncode
        self.stdout = stdout


def test_staged_files_from_git_output(monkeypatch) -> None:
    def fake_run(*args, **kwargs):  # type: ignore[no-untyped-def]
        return _DummyProc(stdout=b"a.md\x00b.py\x00")

    monkeypatch.setattr(mod.subprocess, "run", fake_run)
    assert mod._staged_files() == ["a.md", "b.py"]


def test_python_exe_prefers_dot_venv(monkeypatch, tmp_path) -> None:
    monkeypatch.chdir(tmp_path)
    venv_py = tmp_path / ".venv" / "Scripts" / "python.exe"
    venv_py.parent.mkdir(parents=True)
    venv_py.write_text("", encoding="utf-8")
    actual = mod._python_exe().replace("\\", "/")
    assert actual.endswith(".venv/Scripts/python.exe")


def test_run_pre_commit_stops_on_first_failure(monkeypatch) -> None:
    monkeypatch.setattr(mod, "_staged_files", lambda: ["PR.md"])
    calls: list[list[str]] = []

    def fake_run(cmd, *, env=None, stdin_text=None):  # type: ignore[no-untyped-def]
        calls.append(cmd)
        if "scripts/check_venv_runtime.py" in cmd:
            return 1
        return 0

    monkeypatch.setattr(mod, "_run", fake_run)
    assert mod.run_pre_commit("python") == 1
    assert calls[0][1] == "scripts/check_venv_runtime.py"


def test_run_pre_commit_without_staged_files_skips_file_scans(monkeypatch) -> None:
    monkeypatch.setattr(mod, "_staged_files", lambda: [])
    calls: list[list[str]] = []

    def fake_run(cmd, *, env=None, stdin_text=None):  # type: ignore[no-untyped-def]
        calls.append(cmd)
        return 0

    monkeypatch.setattr(mod, "_run", fake_run)
    assert mod.run_pre_commit("python") == 0
    called_scripts = [c[1] for c in calls]
    assert "scripts/check_pr_body_content.py" not in called_scripts
    assert "scripts/check_bidi_controls.py" not in called_scripts
