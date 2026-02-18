from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml
from qai_xml2ir.serialize import sha256_file

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


def _provenance_path(profile_path: Path, profiles_dir: Path) -> str:
    try:
        return str(profile_path.relative_to(Path.cwd().resolve()))
    except ValueError:
        pass
    try:
        return str(Path("profiles") / profile_path.relative_to(profiles_dir.resolve()))
    except ValueError:
        return str(profile_path)


def _dedupe_provenance(entries: List[Dict[str, str]]) -> List[Dict[str, str]]:
    seen: set[str] = set()
    deduped: List[Dict[str, str]] = []
    for entry in entries:
        key = entry.get("path", "")
        if key in seen:
            continue
        seen.add(key)
        deduped.append(entry)
    return deduped


def _load_parser_profile_core(
    *,
    profile_id: Optional[str] = None,
    path: Optional[Path] = None,
    family: str = "US_CFR",
    profiles_dir_override: Optional[Path] = None,
    _stack: Optional[list[str]] = None,
) -> Tuple[Dict[str, Any], List[Dict[str, str]]]:
    profiles_dir = profiles_dir_override or (Path(__file__).resolve().parent / "profiles")
    stack = list(_stack or [])
    if path is not None:
        profile_path = path
        current_profile_id = path.stem
    elif profile_id:
        profile_path = profiles_dir / f"{profile_id}.yaml"
        current_profile_id = profile_id
    else:
        profile_path = _default_profile_path(family=family, profiles_dir=profiles_dir)
        current_profile_id = profile_path.stem
    profile_path = profile_path.resolve()
    if not profile_path.exists():
        raise ValueError(f"Parser profile not found: {profile_path}")

    path_key = str(profile_path)
    if path_key in stack:
        cycle = " -> ".join([*stack, path_key])
        raise ValueError(f"Cyclic profile extends detected: {cycle}")

    raw = _load_yaml(profile_path)
    extends_raw = raw.get("extends")
    provenance_entry = {
        "profile_id": str(current_profile_id),
        "internal_id": str(raw.get("id") or ""),
        "path": _provenance_path(profile_path, profiles_dir),
        "sha256": sha256_file(profile_path),
        "extends": str(extends_raw) if extends_raw is not None else "",
    }

    if extends_raw is None:
        return raw, [provenance_entry]

    extends_items = _resolve_extends_items(extends_raw)
    merged_base: Dict[str, Any] = {}
    provenance: List[Dict[str, str]] = []
    next_stack = [*stack, path_key]
    for base_id in extends_items:
        base, base_prov = _load_parser_profile_core(
            profile_id=base_id,
            profiles_dir_override=profiles_dir,
            _stack=next_stack,
        )
        merged_base = _deep_merge(merged_base, base)
        provenance.extend(base_prov)

    child = deepcopy(raw)
    child.pop("extends", None)
    provenance.append(provenance_entry)
    return _deep_merge(merged_base, child), _dedupe_provenance(provenance)


def load_parser_profile_with_provenance(
    *,
    profile_id: Optional[str] = None,
    path: Optional[Path] = None,
    family: str = "US_CFR",
    profiles_dir_override: Optional[Path] = None,
) -> Tuple[Dict[str, Any], List[Dict[str, str]]]:
    profile, provenance = _load_parser_profile_core(
        profile_id=profile_id,
        path=path,
        family=family,
        profiles_dir_override=profiles_dir_override,
        _stack=None,
    )
    return profile, provenance


def load_parser_profile(
    *,
    profile_id: Optional[str] = None,
    path: Optional[Path] = None,
    family: str = "US_CFR",
    profiles_dir_override: Optional[Path] = None,
    _stack: Optional[list[str]] = None,
) -> Dict[str, Any]:
    # _stack is kept for backwards compatibility with existing internal callers.
    if _stack:
        profile, _ = _load_parser_profile_core(
            profile_id=profile_id,
            path=path,
            family=family,
            profiles_dir_override=profiles_dir_override,
            _stack=_stack,
        )
        return profile
    profile, _ = load_parser_profile_with_provenance(
        profile_id=profile_id,
        path=path,
        family=family,
        profiles_dir_override=profiles_dir_override,
    )
    return profile
