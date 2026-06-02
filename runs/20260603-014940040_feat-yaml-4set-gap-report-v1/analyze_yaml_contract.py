from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path
from typing import Any

import yaml


SUFFIXES = {
    "ir": ".regdoc_ir.yaml",
    "parser_profile": ".parser_profile.yaml",
    "regdoc_profile": ".regdoc_profile.yaml",
    "meta": ".meta.yaml",
}


def parse_yaml(data: bytes) -> tuple[Any, str | None]:
    try:
        return yaml.safe_load(data.decode("utf-8-sig")), None
    except yaml.YAMLError as exc:
        return None, str(exc)


def key_paths(value: Any, prefix: str = "$") -> set[str]:
    paths = set()
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}"
            paths.add(path)
            paths.update(key_paths(child, path))
    elif isinstance(value, list):
        paths.add(f"{prefix}[]")
        for child in value:
            paths.update(key_paths(child, f"{prefix}[]"))
    return paths


def collect_nodes(value: Any) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    if isinstance(value, dict):
        if "kind" in value or "nid" in value or "children" in value:
            nodes.append(value)
        for child in value.values():
            nodes.extend(collect_nodes(child))
    elif isinstance(value, list):
        for child in value:
            nodes.extend(collect_nodes(child))
    return nodes


def load_current(root: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in root.rglob("*.yaml"):
        for kind, suffix in SUFFIXES.items():
            if path.name.endswith(suffix):
                doc_id = path.name[: -len(suffix)]
                data, error = parse_yaml(path.read_bytes())
                result.setdefault(doc_id, {})[kind] = {
                    "path": path.as_posix(),
                    "data": data,
                    "parse_error": error,
                }
    return result


def load_old(zip_path: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            normalized = info.filename.replace("\\", "/")
            if info.is_dir() or ("/data/normalized/" not in normalized and not normalized.startswith("data/normalized/")):
                continue
            name = Path(normalized).name
            for kind, suffix in SUFFIXES.items():
                if name.endswith(suffix):
                    doc_id = name[: -len(suffix)]
                    data, error = parse_yaml(zf.read(info.filename))
                    result.setdefault(doc_id, {})[kind] = {
                        "path": normalized,
                        "data": data,
                        "parse_error": error,
                    }
    return result


def summarize(label: str, sets: dict[str, dict[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {
        "label": label,
        "doc_count": len(sets),
        "file_contract": {},
        "ir_kinds": {},
        "ir_node_key_union": [],
        "profile_contract": {},
        "parse_errors": [],
    }
    all_node_keys = set()
    for doc_id, files in sets.items():
        for kind, file_info in files.items():
            if file_info["parse_error"]:
                out["parse_errors"].append({
                    "doc_id": doc_id,
                    "file_kind": kind,
                    "path": file_info["path"],
                    "error": file_info["parse_error"],
                })
                continue
            out["file_contract"].setdefault(kind, set()).update(key_paths(file_info["data"]))
            if kind == "ir":
                nodes = collect_nodes(file_info["data"])
                for node in nodes:
                    node_kind = str(node.get("kind", "<missing>"))
                    out["ir_kinds"].setdefault(node_kind, 0)
                    out["ir_kinds"][node_kind] += 1
                    all_node_keys.update(node.keys())
            if kind == "regdoc_profile":
                out["profile_contract"].setdefault("paths", set()).update(key_paths(file_info["data"]))
    out["ir_node_key_union"] = sorted(all_node_keys)
    out["ir_kinds"] = dict(sorted(out["ir_kinds"].items()))
    for kind, paths in out["file_contract"].items():
        out["file_contract"][kind] = sorted(paths)
    for key, paths in out["profile_contract"].items():
        out["profile_contract"][key] = sorted(paths)
    return out


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: analyze_yaml_contract.py <old_zip> <current_normalized_dir> <out_json>", file=sys.stderr)
        return 2
    old = load_old(Path(sys.argv[1]))
    current = load_current(Path(sys.argv[2]))
    report = {
        "old": summarize("old_zip", old),
        "current": summarize("current", current),
    }
    old_kinds = set(report["old"]["ir_kinds"])
    current_kinds = set(report["current"]["ir_kinds"])
    report["diff"] = {
        "current_only_ir_kinds": sorted(current_kinds - old_kinds),
        "old_only_ir_kinds": sorted(old_kinds - current_kinds),
        "common_ir_kinds": sorted(old_kinds & current_kinds),
        "current_only_file_paths": {
            kind: sorted(set(report["current"]["file_contract"].get(kind, [])) - set(report["old"]["file_contract"].get(kind, [])))
            for kind in SUFFIXES
        },
        "old_only_file_paths": {
            kind: sorted(set(report["old"]["file_contract"].get(kind, [])) - set(report["current"]["file_contract"].get(kind, [])))
            for kind in SUFFIXES
        },
    }
    out = Path(sys.argv[3])
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "old_doc_count": report["old"]["doc_count"],
        "current_doc_count": report["current"]["doc_count"],
        "current_only_ir_kinds": report["diff"]["current_only_ir_kinds"],
        "old_parse_error_count": len(report["old"]["parse_errors"]),
        "current_parse_error_count": len(report["current"]["parse_errors"]),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
