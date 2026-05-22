from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Set


NORMAL_SELECTABLE_KINDS = {"item", "subitem", "paragraph", "statement"}

PRIVATE_USE_RE = re.compile(r"[\uE000-\uF8FF]")
DOT_LEADER_RE = re.compile(r"\.{8,}")
LONG_SPACE_RE = re.compile(r" {8,}")
REPEATED_COLUMN_SPACE_RE = re.compile(r"(?: {3,}\S+){2,}")
TABLE_CAPTION_RE = re.compile(r"\b(?:Table|Figure)\s+\d+[A-Za-z\-]*\b", re.IGNORECASE)
CHECKED_ITEM_RE = re.compile(r"\bCHECKED\s+ITEM\b")
CHECKLIST_TOKEN_RE = re.compile(r"(?<![A-Za-z])(?:YES|NO|N/A|COMMENTS)(?![A-Za-z])")
BULLET_RE = re.compile(r"(^|\s)[\u2022\uF0B7]\s+")


@dataclass
class ContaminationFinding:
    nid: str = ""
    kind: str = ""
    score: int = 0
    flags: List[str] = field(default_factory=list)
    severity: str = "none"
    preview: str = ""

    @property
    def severe(self) -> bool:
        return self.severity == "severe"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nid": self.nid,
            "kind": self.kind,
            "score": self.score,
            "flags": list(self.flags),
            "severity": self.severity,
            "preview": self.preview,
        }


def _preview(text: str, limit: int = 180) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def _checklist_tokens(text: str) -> Set[str]:
    tokens = set(CHECKLIST_TOKEN_RE.findall(text))
    if CHECKED_ITEM_RE.search(text):
        tokens.add("CHECKED ITEM")
    return tokens


def classify_text_contamination(
    text: str,
    *,
    kind: str,
    nid: str = "",
    selectable: bool = True,
) -> ContaminationFinding:
    value = text or ""
    flags: List[str] = []
    if PRIVATE_USE_RE.search(value):
        flags.append("private_use_char")
    if DOT_LEADER_RE.search(value):
        flags.append("dot_leader")
    checklist_tokens = _checklist_tokens(value)
    if len(checklist_tokens) >= 2 or "CHECKED ITEM" in checklist_tokens:
        flags.append("checklist_columns")
    if LONG_SPACE_RE.search(value) or REPEATED_COLUMN_SPACE_RE.search(value):
        flags.append("fixed_width_columns")
    if TABLE_CAPTION_RE.search(value):
        flags.append("table_caption")
    if BULLET_RE.search(value) and any(flag in flags for flag in ("dot_leader", "checklist_columns", "fixed_width_columns", "private_use_char")):
        flags.append("bullet_form_row")

    flag_set = set(flags)
    score = 0
    if "private_use_char" in flag_set:
        score += 3
    if "dot_leader" in flag_set:
        score += 3
    if "checklist_columns" in flag_set:
        score += 3
    if "fixed_width_columns" in flag_set:
        score += 2
    if "table_caption" in flag_set:
        score += 1
    if "bullet_form_row" in flag_set:
        score += 2

    severe = False
    if selectable and kind in NORMAL_SELECTABLE_KINDS:
        severe = (
            {"private_use_char", "dot_leader"}.issubset(flag_set)
            or {"private_use_char", "fixed_width_columns"}.issubset(flag_set)
            or {"checklist_columns", "fixed_width_columns"}.issubset(flag_set)
            or {"checklist_columns", "dot_leader"}.issubset(flag_set)
            or "bullet_form_row" in flag_set
        )

    if severe:
        severity = "severe"
    elif flags:
        severity = "warning"
    else:
        severity = "none"

    return ContaminationFinding(
        nid=nid,
        kind=kind,
        score=score,
        flags=flags,
        severity=severity,
        preview=_preview(value),
    )


def node_text_for_contamination(node: Any) -> str:
    if isinstance(node, dict):
        values = [node.get("heading"), node.get("text")]
    else:
        values = [getattr(node, "heading", None), getattr(node, "text", None)]
    return "\n".join(str(value) for value in values if value)


def node_kind(node: Any) -> str:
    if isinstance(node, dict):
        return str(node.get("kind") or "")
    return str(getattr(node, "kind", "") or "")


def node_nid(node: Any) -> str:
    if isinstance(node, dict):
        return str(node.get("nid") or "")
    return str(getattr(node, "nid", "") or "")


def detect_node_contamination(
    node: Any,
    *,
    selectable_kinds: Optional[Iterable[str]] = None,
) -> ContaminationFinding:
    kind = node_kind(node)
    selectable_set = set(selectable_kinds or [])
    selectable = kind in selectable_set if selectable_set else kind in NORMAL_SELECTABLE_KINDS
    return classify_text_contamination(
        node_text_for_contamination(node),
        kind=kind,
        nid=node_nid(node),
        selectable=selectable,
    )
