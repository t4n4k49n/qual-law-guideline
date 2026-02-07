from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

_OVERWRITE_APPROVED: Optional[bool] = None


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _can_write(path: Path) -> bool:
    global _OVERWRITE_APPROVED
    if not path.exists():
        return True
    if _OVERWRITE_APPROVED is True:
        return True
    if _OVERWRITE_APPROVED is False:
        return False
    answer = input('Overwrite?"Yes" ')
    _OVERWRITE_APPROVED = answer == "Yes"
    return _OVERWRITE_APPROVED


def write_yaml(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not _can_write(path):
        raise FileExistsError(
            f"Refusing to overwrite existing file: {path} (type exact 'Yes' once to allow overwrite)"
        )
    with path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(
            data,
            f,
            allow_unicode=True,
            sort_keys=False,
            width=120,
        )
