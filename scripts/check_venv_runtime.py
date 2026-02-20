from __future__ import annotations

import os
import sys
from pathlib import Path


def _is_venv_active() -> bool:
    virtual_env = os.environ.get("VIRTUAL_ENV", "")
    if virtual_env and Path(virtual_env).name == ".venv":
        return True

    exe = Path(sys.executable).as_posix().lower()
    if "/.venv/" in exe:
        return True

    prefix = Path(sys.prefix).name
    return prefix == ".venv"


def main() -> int:
    if _is_venv_active():
        return 0

    message = (
        "ERROR: .venv 以外の Python 実行を検出しました。\n"
        f"Detected executable: {sys.executable}\n"
        "Reason: 依存解決の不一致によりテスト/実行結果が不安定になります。\n"
        "Use one of:\n"
        "  Windows: .\\.venv\\Scripts\\python.exe -m pytest\n"
        "  Linux/macOS: ./.venv/bin/python -m pytest\n"
    )
    print(message, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
