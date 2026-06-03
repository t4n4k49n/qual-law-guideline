from __future__ import annotations

import hashlib
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


SUFFIXES = {
    "ir": ".regdoc_ir.yaml",
    "parser_profile": ".parser_profile.yaml",
    "regdoc_profile": ".regdoc_profile.yaml",
    "meta": ".meta.yaml",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_yaml_bytes(data: bytes) -> Any:
    text = data.decode("utf-8-sig")
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as exc:
        return {"__parse_error__": str(exc)}


def doc_id_from_name(name: str, suffix: str) -> str:
    return name[: -len(suffix)]


def read_zip_sets(zip_path: Path) -> dict[str, dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            normalized = info.filename.replace("\\", "/")
            if "/data/normalized/" not in normalized and not normalized.startswith("data/normalized/"):
                continue
            leaf = Path(info.filename).name
            for kind, suffix in SUFFIXES.items():
                if leaf.endswith(suffix):
                    doc_id = doc_id_from_name(leaf, suffix)
                    data = zf.read(info.filename)
                    grouped.setdefault(doc_id, {"files": {}})["files"][kind] = {
                        "path": info.filename,
                        "sha256": sha256_bytes(data),
                        "bytes": len(data),
                        "yaml": parse_yaml_bytes(data),
                    }
                    break
    return enrich_sets(grouped)


def read_current_sets(root: Path) -> dict[str, dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for path in root.rglob("*.yaml"):
        leaf = path.name
        for kind, suffix in SUFFIXES.items():
            if leaf.endswith(suffix):
                doc_id = doc_id_from_name(leaf, suffix)
                data = path.read_bytes()
                grouped.setdefault(doc_id, {"files": {}})["files"][kind] = {
                    "path": str(path.as_posix()),
                    "sha256": sha256_bytes(data),
                    "bytes": len(data),
                    "yaml": parse_yaml_bytes(data),
                }
                break
    return enrich_sets(grouped)


def text_len(value: Any) -> int:
    if value is None:
        return 0
    return len(str(value))


def walk_nodes(value: Any, depth: int = 0):
    if isinstance(value, dict):
        if "nid" in value or "kind" in value or "children" in value:
            yield value, depth
        for child in value.get("children") or []:
            yield from walk_nodes(child, depth + 1)
        for key, child in value.items():
            if key != "children" and isinstance(child, (dict, list)):
                yield from walk_nodes(child, depth)
    elif isinstance(value, list):
        for item in value:
            yield from walk_nodes(item, depth)


def ir_stats(ir: Any) -> dict[str, Any]:
    nodes = list(walk_nodes(ir))
    kinds = Counter(str(node.get("kind", "<missing>")) for node, _ in nodes if isinstance(node, dict))
    nid_count = sum(1 for node, _ in nodes if isinstance(node, dict) and node.get("nid"))
    text_nodes = sum(1 for node, _ in nodes if isinstance(node, dict) and text_len(node.get("text")) > 0)
    heading_nodes = sum(1 for node, _ in nodes if isinstance(node, dict) and text_len(node.get("heading")) > 0)
    max_depth = max((depth for _, depth in nodes), default=0)
    return {
        "node_count": len(nodes),
        "nid_count": nid_count,
        "text_node_count": text_nodes,
        "heading_node_count": heading_nodes,
        "max_depth": max_depth,
        "kind_counts": dict(sorted(kinds.items())),
    }


def get_path(obj: Any, dotted: str, default: Any = None) -> Any:
    cur = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def profile_summary(profile: Any) -> dict[str, Any]:
    return {
        "selectable_kinds": get_path(profile, "selection.selectable_kinds", []),
        "include_ancestors": get_path(profile, "render_context.include_ancestors", None),
        "include_descendants": get_path(profile, "render_context.include_descendants", None),
        "ancestor_suppression": get_path(profile, "render_context.ancestor_suppression", None),
        "first_paragraph_merge": get_path(profile, "render.article_first_paragraph_merge", None),
        "top_keys": sorted(profile.keys()) if isinstance(profile, dict) else [],
    }


def meta_summary(meta: Any) -> dict[str, Any]:
    title = (
        get_path(meta, "document.title")
        or get_path(meta, "doc.title")
        or get_path(meta, "title")
        or ""
    )
    jurisdiction = (
        get_path(meta, "document.jurisdiction")
        or get_path(meta, "doc.jurisdiction")
        or get_path(meta, "jurisdiction")
        or ""
    )
    source_url = (
        get_path(meta, "source.url")
        or get_path(meta, "document.source_url")
        or get_path(meta, "doc.source_url")
        or ""
    )
    return {
        "title": title,
        "jurisdiction": jurisdiction,
        "source_url": source_url,
        "top_keys": sorted(meta.keys()) if isinstance(meta, dict) else [],
    }


def parser_summary(parser_profile: Any) -> dict[str, Any]:
    return {
        "parser_family": get_path(parser_profile, "parser.family", ""),
        "parser_name": get_path(parser_profile, "parser.name", ""),
        "source_format": get_path(parser_profile, "source.format", ""),
        "top_keys": sorted(parser_profile.keys()) if isinstance(parser_profile, dict) else [],
    }


def clean_for_json(item: dict[str, Any]) -> dict[str, Any]:
    cleaned = {"files": {}}
    for kind, file_info in item["files"].items():
        cleaned["files"][kind] = {
            "path": file_info["path"],
            "sha256": file_info["sha256"],
            "bytes": file_info["bytes"],
            "parse_error": get_path(file_info["yaml"], "__parse_error__", None),
        }
    for key in ["complete", "missing", "ir_stats", "meta", "profile", "parser"]:
        cleaned[key] = item.get(key)
    return cleaned


def enrich_sets(grouped: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    for doc_id, item in grouped.items():
        item["complete"] = all(kind in item["files"] for kind in SUFFIXES)
        item["missing"] = [kind for kind in SUFFIXES if kind not in item["files"]]
        if "ir" in item["files"]:
            item["ir_stats"] = ir_stats(item["files"]["ir"]["yaml"])
        if "meta" in item["files"]:
            item["meta"] = meta_summary(item["files"]["meta"]["yaml"])
        if "regdoc_profile" in item["files"]:
            item["profile"] = profile_summary(item["files"]["regdoc_profile"]["yaml"])
        if "parser_profile" in item["files"]:
            item["parser"] = parser_summary(item["files"]["parser_profile"]["yaml"])
    return grouped


def similarity_key(doc_id: str) -> str:
    return re.sub(r"_(20\d{6}|undated)$", "", doc_id)


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: compare_yaml_4sets.py <zip> <current_normalized_dir> <out_json>", file=sys.stderr)
        return 2
    zip_path = Path(sys.argv[1])
    current_root = Path(sys.argv[2])
    out_json = Path(sys.argv[3])

    old_sets = read_zip_sets(zip_path)
    current_sets = read_current_sets(current_root)

    old_ids = set(old_sets)
    current_ids = set(current_sets)
    common = sorted(old_ids & current_ids)
    old_only = sorted(old_ids - current_ids)
    current_only = sorted(current_ids - old_ids)

    changed = []
    unchanged = []
    for doc_id in common:
        per_file = {}
        for kind in SUFFIXES:
            old_file = old_sets[doc_id]["files"].get(kind)
            cur_file = current_sets[doc_id]["files"].get(kind)
            per_file[kind] = {
                "same": bool(old_file and cur_file and old_file["sha256"] == cur_file["sha256"]),
                "old_parse_error": get_path(old_file["yaml"], "__parse_error__", None) if old_file else None,
                "current_parse_error": get_path(cur_file["yaml"], "__parse_error__", None) if cur_file else None,
            }
        row = {
            "doc_id": doc_id,
            "same_files": per_file,
            "changed_files": [kind for kind, info in per_file.items() if not info["same"]],
            "old_ir_stats": old_sets[doc_id].get("ir_stats"),
            "current_ir_stats": current_sets[doc_id].get("ir_stats"),
            "old_meta": old_sets[doc_id].get("meta"),
            "current_meta": current_sets[doc_id].get("meta"),
            "old_profile": old_sets[doc_id].get("profile"),
            "current_profile": current_sets[doc_id].get("profile"),
            "old_parser": old_sets[doc_id].get("parser"),
            "current_parser": current_sets[doc_id].get("parser"),
        }
        if row["changed_files"]:
            changed.append(row)
        else:
            unchanged.append(row)

    old_by_base: dict[str, list[str]] = {}
    cur_by_base: dict[str, list[str]] = {}
    for doc_id in old_ids:
        old_by_base.setdefault(similarity_key(doc_id), []).append(doc_id)
    for doc_id in current_ids:
        cur_by_base.setdefault(similarity_key(doc_id), []).append(doc_id)

    likely_renamed_or_versioned = []
    for base in sorted(set(old_by_base) & set(cur_by_base)):
        pairs = sorted(old_by_base[base])
        cur = sorted(cur_by_base[base])
        if set(pairs) != set(cur):
            likely_renamed_or_versioned.append({"base": base, "old_ids": pairs, "current_ids": cur})

    result = {
        "inputs": {
            "old_zip": str(zip_path),
            "current_normalized_dir": str(current_root),
        },
        "summary": {
            "old_total": len(old_sets),
            "old_complete": sum(1 for item in old_sets.values() if item["complete"]),
            "current_total": len(current_sets),
            "current_complete": sum(1 for item in current_sets.values() if item["complete"]),
            "common": len(common),
            "current_only": len(current_only),
            "old_only": len(old_only),
            "changed_common": len(changed),
            "unchanged_common": len(unchanged),
        },
        "old_only": [{"doc_id": doc_id, **clean_for_json(old_sets[doc_id])} for doc_id in old_only],
        "current_only": [{"doc_id": doc_id, **clean_for_json(current_sets[doc_id])} for doc_id in current_only],
        "changed_common": changed,
        "unchanged_common": [{"doc_id": row["doc_id"]} for row in unchanged],
        "likely_renamed_or_versioned": likely_renamed_or_versioned,
    }

    out_json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
