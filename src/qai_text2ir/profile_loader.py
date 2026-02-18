from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

CONCAT_UNIQ_LIST_PATHS: set[Tuple[str, ...]] = {
    ("structural_kinds",),
    ("preprocess", "drop_line_regexes"),
    ("preprocess", "drop_line_exact"),
    ("preprocess", "strip_inline_regexes"),
    ("preprocess", "skip_blocks"),
    ("preprocess", "dedent_pop_kinds"),
}


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Invalid parser profile YAML: {path}")
    return data


def _merge_unique_list(base: List[Any], child: List[Any]) -> List[Any]:
    merged = list(base)
    for item in child:
        if item not in merged:
            merged.append(item)
    return merged


def _merge_marker_types(base: List[Any], child: List[Any]) -> List[Any]:
    # Keep base order; child can override existing marker id and append new ids.
    merged = [deepcopy(v) for v in base]
    index_by_id: Dict[str, int] = {}
    for idx, marker in enumerate(merged):
        if isinstance(marker, dict):
            marker_id = marker.get("id")
            if isinstance(marker_id, str) and marker_id:
                index_by_id[marker_id] = idx
    for marker in child:
        marker_cp = deepcopy(marker)
        if not isinstance(marker_cp, dict):
            merged.append(marker_cp)
            continue
        marker_id = marker_cp.get("id")
        if isinstance(marker_id, str) and marker_id and marker_id in index_by_id:
            merged[index_by_id[marker_id]] = marker_cp
        else:
            merged.append(marker_cp)
            if isinstance(marker_id, str) and marker_id:
                index_by_id[marker_id] = len(merged) - 1
    return merged


def _deep_merge(base: Any, child: Any, *, path: Tuple[str, ...] = ()) -> Any:
    if isinstance(base, dict) and isinstance(child, dict):
        merged: Dict[str, Any] = {k: deepcopy(v) for k, v in base.items()}
        for key, child_value in child.items():
            if key in merged:
                merged[key] = _deep_merge(merged[key], child_value, path=path + (str(key),))
            else:
                merged[key] = deepcopy(child_value)
        return merged
    if isinstance(base, list) and isinstance(child, list):
        if path == ("marker_types",):
            return _merge_marker_types(base, child)
        if path in CONCAT_UNIQ_LIST_PATHS:
            return _merge_unique_list(base, child)
        return deepcopy(child)
    return deepcopy(child)


def _resolve_extends_items(raw_extends: Any) -> List[str]:
    if isinstance(raw_extends, str):
        return [raw_extends]
    if isinstance(raw_extends, list):
        resolved: List[str] = []
        for item in raw_extends:
            if not isinstance(item, str) or not item.strip():
                raise ValueError(f"Invalid extends entry: {item!r}")
            resolved.append(item.strip())
        return resolved
    raise ValueError(f"Invalid extends value: {raw_extends!r}")


def _default_profile_path(*, family: str, profiles_dir: Path) -> Path:
    if family == "US_CFR":
        profile_path = profiles_dir / "us_cfr_default_v2.yaml"
        if not profile_path.exists():
            profile_path = profiles_dir / "us_cfr_default_v1.yaml"
        return profile_path
    if family == "EU_GMP":
        return profiles_dir / "eu_gmp_chap1_default_v2.yaml"
    if family == "PICS":
        profile_path = profiles_dir / "pics_part1_default_v3.yaml"
        if not profile_path.exists():
            profile_path = profiles_dir / "pics_part1_default_v2.yaml"
        if not profile_path.exists():
            profile_path = profiles_dir / "pics_part1_default_v1.yaml"
        return profile_path
    if family == "WHO_LBM":
        profile_path = profiles_dir / "who_lbm_3rd_default_v4.yaml"
        if not profile_path.exists():
            profile_path = profiles_dir / "who_lbm_3rd_default_v3.yaml"
        if not profile_path.exists():
            profile_path = profiles_dir / "who_lbm_3rd_default_v2.yaml"
        if not profile_path.exists():
            profile_path = profiles_dir / "who_lbm_3rd_default_v1.yaml"
        return profile_path
    return profiles_dir / "us_cfr_default_v1.yaml"


def load_parser_profile(
    *,
    profile_id: Optional[str] = None,
    path: Optional[Path] = None,
    family: str = "US_CFR",
    profiles_dir_override: Optional[Path] = None,
    _stack: Optional[list[str]] = None,
) -> Dict[str, Any]:
    profiles_dir = profiles_dir_override or (Path(__file__).resolve().parent / "profiles")
    stack = list(_stack or [])
    if path is not None:
        profile_path = path
    elif profile_id:
        profile_path = profiles_dir / f"{profile_id}.yaml"
    else:
        profile_path = _default_profile_path(family=family, profiles_dir=profiles_dir)
    profile_path = profile_path.resolve()
    if not profile_path.exists():
        raise ValueError(f"Parser profile not found: {profile_path}")

    path_key = str(profile_path)
    if path_key in stack:
        cycle = " -> ".join([*stack, path_key])
        raise ValueError(f"Cyclic profile extends detected: {cycle}")

    raw = _load_yaml(profile_path)
    extends_raw = raw.get("extends")
    if extends_raw is None:
        return raw

    extends_items = _resolve_extends_items(extends_raw)
    merged_base: Dict[str, Any] = {}
    next_stack = [*stack, path_key]
    for base_id in extends_items:
        base = load_parser_profile(
            profile_id=base_id,
            profiles_dir_override=profiles_dir,
            _stack=next_stack,
        )
        merged_base = _deep_merge(merged_base, base)

    child = deepcopy(raw)
    child.pop("extends", None)
    return _deep_merge(merged_base, child)
