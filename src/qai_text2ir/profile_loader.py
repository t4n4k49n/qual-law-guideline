from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

import yaml


def load_parser_profile(path: Optional[Path] = None) -> Dict[str, Any]:
    profile_path = path or (Path(__file__).resolve().parent / "profiles" / "us_cfr_default_v1.yaml")
    with profile_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Invalid parser profile YAML: {profile_path}")
    return data

