from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

import yaml


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Invalid parser profile YAML: {path}")
    return data


def load_parser_profile(
    *,
    profile_id: Optional[str] = None,
    path: Optional[Path] = None,
) -> Dict[str, Any]:
    profiles_dir = Path(__file__).resolve().parent / "profiles"
    if path is not None:
        profile_path = path
    elif profile_id:
        profile_path = profiles_dir / f"{profile_id}.yaml"
    else:
        profile_path = profiles_dir / "us_cfr_default_v1.yaml"
    return _load_yaml(profile_path)
