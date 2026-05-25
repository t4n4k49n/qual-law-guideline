from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


PROFILE_DIR = Path(__file__).resolve().parent / "candidate_visibility_profiles"


def _read_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Invalid candidate visibility profile YAML: {path}")
    return data


def load_candidate_visibility_profile(
    *,
    profile_id: Optional[str] = None,
    path: Optional[Path] = None,
) -> Dict[str, Any]:
    if path is not None:
        profile_path = path
    elif isinstance(profile_id, str) and profile_id.strip():
        profile_path = PROFILE_DIR / f"{profile_id.strip()}.yaml"
    else:
        raise ValueError("candidate visibility profile id or path is required")
    if not profile_path.exists():
        raise ValueError(f"Candidate visibility profile not found: {profile_path}")
    return _read_yaml(profile_path)


def extract_candidate_visibility(profile: Dict[str, Any]) -> Dict[str, Any]:
    direct = profile.get("candidate_visibility")
    if isinstance(direct, dict):
        return deepcopy(direct)

    purpose = ((profile.get("profiles") or {}).get("dq_gmp_checklist") or {})
    nested = purpose.get("candidate_visibility")
    if isinstance(nested, dict):
        return deepcopy(nested)

    raise ValueError("candidate visibility profile has no candidate_visibility block")


def apply_candidate_visibility_profile(
    regdoc_profile: Dict[str, Any],
    visibility_profile: Dict[str, Any],
    *,
    purpose_id: str = "dq_gmp_checklist",
) -> Dict[str, Any]:
    merged = deepcopy(regdoc_profile)
    profiles = merged.setdefault("profiles", {})
    if not isinstance(profiles, dict):
        raise ValueError("regdoc_profile.profiles must be a mapping")
    purpose = profiles.setdefault(purpose_id, {})
    if not isinstance(purpose, dict):
        raise ValueError(f"regdoc_profile.profiles.{purpose_id} must be a mapping")
    purpose["candidate_visibility"] = extract_candidate_visibility(visibility_profile)
    return merged
