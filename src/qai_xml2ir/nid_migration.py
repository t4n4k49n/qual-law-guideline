from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

import yaml


PREFERRED_LIST_KEYS = ("selected_nids", "selected", "selections", "nids", "targets")
ARTICLE_SEGMENT_RE = re.compile(r"^art[0-9A-Za-z_]+$")
PARAGRAPH_SEGMENT_RE = re.compile(r"^p[0-9].*$")


@dataclass
class MappingRow:
    old: str
    new: Optional[str]
    status: str  # unchanged | changed | unresolved


@dataclass
class MigrationResult:
    resolved_nids: List[str]
    mappings: List[MappingRow]
    unresolved: List[str]
    invalid_after_migration: List[str]
    warnings: List[str]

    @property
    def total_in(self) -> int:
        return len(self.mappings)

    @property
    def total_out(self) -> int:
        return len(self.resolved_nids)

    @property
    def changed_count(self) -> int:
        return sum(1 for row in self.mappings if row.status == "changed")

    @property
    def unchanged_count(self) -> int:
        return sum(1 for row in self.mappings if row.status == "unchanged")

    @property
    def unresolved_count(self) -> int:
        return len(self.unresolved)


@dataclass
class LoadedNidList:
    source_type: str  # yaml | json | text
    original_data: Any
    nids: List[str]
    list_key: Optional[str] = None


def _walk_content_nodes(node: Dict[str, Any]) -> List[Dict[str, Any]]:
    stack = [node]
    nodes: List[Dict[str, Any]] = []
    while stack:
        current = stack.pop()
        nodes.append(current)
        children = current.get("children") or []
        if children:
            stack.extend(reversed(children))
    return nodes


def build_existing_nids(ir_data: Dict[str, Any]) -> Tuple[Set[str], Dict[str, str]]:
    content = ir_data.get("content")
    if not isinstance(content, dict):
        raise ValueError("regdoc_ir.yaml: content が見つからないか不正です")

    existing_nids: Set[str] = set()
    kind_by_nid: Dict[str, str] = {}
    for node in _walk_content_nodes(content):
        nid = node.get("nid")
        kind = node.get("kind")
        if isinstance(nid, str) and nid:
            existing_nids.add(nid)
            if isinstance(kind, str):
                kind_by_nid[nid] = kind
    return existing_nids, kind_by_nid


def _insert_p1_after_article_segment(old_nid: str) -> Optional[str]:
    segments = old_nid.split(".")
    article_idx: Optional[int] = None
    for i, seg in enumerate(segments):
        if ARTICLE_SEGMENT_RE.match(seg):
            article_idx = i
            break
    if article_idx is None:
        return None

    next_idx = article_idx + 1
    if next_idx < len(segments) and PARAGRAPH_SEGMENT_RE.match(segments[next_idx]):
        return None

    new_segments = list(segments[:next_idx]) + ["p1"] + list(segments[next_idx:])
    return ".".join(new_segments)


def generate_candidate_nids(old_nid: str) -> List[str]:
    candidate = _insert_p1_after_article_segment(old_nid)
    if not candidate or candidate == old_nid:
        return []
    return [candidate]


def migrate_nids(
    old_nids: Sequence[str],
    existing_nids: Set[str],
    *,
    dedup: bool = True,
) -> MigrationResult:
    mappings: List[MappingRow] = []
    unresolved: List[str] = []
    resolved_raw: List[str] = []
    warnings: List[str] = []

    for old_nid in old_nids:
        if old_nid in existing_nids:
            mappings.append(MappingRow(old=old_nid, new=old_nid, status="unchanged"))
            resolved_raw.append(old_nid)
            continue

        resolved: Optional[str] = None
        for cand in generate_candidate_nids(old_nid):
            if cand in existing_nids:
                resolved = cand
                break

        if resolved is None:
            mappings.append(MappingRow(old=old_nid, new=None, status="unresolved"))
            unresolved.append(old_nid)
            continue

        mappings.append(MappingRow(old=old_nid, new=resolved, status="changed"))
        resolved_raw.append(resolved)

    if dedup:
        seen: Set[str] = set()
        resolved_nids: List[str] = []
        for nid in resolved_raw:
            if nid in seen:
                continue
            seen.add(nid)
            resolved_nids.append(nid)
    else:
        resolved_nids = resolved_raw

    invalid_after_migration = [nid for nid in resolved_nids if nid not in existing_nids]

    return MigrationResult(
        resolved_nids=resolved_nids,
        mappings=mappings,
        unresolved=unresolved,
        invalid_after_migration=invalid_after_migration,
        warnings=warnings,
    )


def _extract_from_text(text: str) -> List[str]:
    nids: List[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("- "):
            line = line[2:].strip()
        elif line.startswith("* "):
            line = line[2:].strip()
        line = line.split("#", 1)[0].strip()
        if line:
            nids.append(line)
    return nids


def load_nids_file(path: Path) -> LoadedNidList:
    suffix = path.suffix.lower()
    raw = path.read_text(encoding="utf-8")
    if suffix in {".yaml", ".yml"}:
        data = yaml.safe_load(raw)
        return _extract_nids_from_structured(data, "yaml")
    if suffix == ".json":
        data = json.loads(raw)
        return _extract_nids_from_structured(data, "json")
    if suffix in {".txt", ".md"}:
        return LoadedNidList(source_type="text", original_data=raw, nids=_extract_from_text(raw))
    raise ValueError(f"未対応の入力拡張子です: {path}")


def _extract_nids_from_structured(data: Any, source_type: str) -> LoadedNidList:
    if isinstance(data, list):
        nids = [x for x in data if isinstance(x, str)]
        return LoadedNidList(source_type=source_type, original_data=data, nids=nids, list_key=None)
    if isinstance(data, dict):
        for key in PREFERRED_LIST_KEYS:
            value = data.get(key)
            if isinstance(value, list):
                nids = [x for x in value if isinstance(x, str)]
                return LoadedNidList(
                    source_type=source_type,
                    original_data=data,
                    nids=nids,
                    list_key=key,
                )
    raise ValueError("NID一覧を抽出できませんでした（listまたは既定キーのlistが必要）")


def render_output_data(loaded: LoadedNidList, new_nids: Sequence[str]) -> str:
    if loaded.source_type == "text":
        return "\n".join(new_nids) + ("\n" if new_nids else "")

    if isinstance(loaded.original_data, list):
        new_data = list(new_nids)
    elif isinstance(loaded.original_data, dict):
        new_data = dict(loaded.original_data)
        if not loaded.list_key:
            raise ValueError("内部エラー: dict入力なのにlist_keyがありません")
        new_data[loaded.list_key] = list(new_nids)
    else:
        raise ValueError("内部エラー: 未知の構造化データ")

    if loaded.source_type == "json":
        return json.dumps(new_data, ensure_ascii=False, indent=2) + "\n"
    return yaml.safe_dump(new_data, allow_unicode=True, sort_keys=False)


def build_report(
    *,
    input_path: Path,
    ir_path: Path,
    result: MigrationResult,
    purpose: Optional[str],
) -> Dict[str, Any]:
    return {
        "input_path": str(input_path),
        "ir_path": str(ir_path),
        "purpose": purpose,
        "total_in": result.total_in,
        "total_out": result.total_out,
        "changed_count": result.changed_count,
        "unchanged_count": result.unchanged_count,
        "unresolved_count": result.unresolved_count,
        "mappings": [
            {"old": row.old, "new": row.new, "status": row.status} for row in result.mappings
        ],
        "unresolved": list(result.unresolved),
        "invalid_after_migration": list(result.invalid_after_migration),
        "warnings": list(result.warnings),
    }

