from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

from .glyph_sanitizer import contains_private_use, sanitize_visible_text

DOT_LEADER_RE = re.compile(r"\.{5,}")
FORM_HEADER_RE = re.compile(r"\bYES\s+NO\s+N/?A(?:\s+COMMENTS?)?\b", re.IGNORECASE)
FORM_WORD_RE = re.compile(
    r"\b(?:CHECKED\s+ITEM|ENTER\s+DATE\s+OF\s+CHECK|COMMENTS?|Date\s+survey|Safety\s+surveyor|Biosafety\s+Level\s+Survey)\b",
    re.IGNORECASE,
)
FORM_CAPTION_RE = re.compile(r"\bTable\s+\d+[.:]\s+.*?\b(?:survey|form|checklist)\b", re.IGNORECASE | re.DOTALL)
CHECKBOX_CLUSTER_RE = re.compile(r"(?:\[[ xX]\]\s*){3,}|(?:[\uEC1E☐☑☒□■]\s*){3,}")
OPEN_CIRCLE_CLUSTER_RE = re.compile(r"(?:○\s*){3,}")


def has_form_signal(text: str) -> bool:
    value = text or ""
    return bool(FORM_WORD_RE.search(value) or FORM_HEADER_RE.search(value) or FORM_CAPTION_RE.search(value))


def looks_like_form_artifact(text: str) -> bool:
    value = text or ""
    if not value:
        return False
    if contains_private_use(value) and (DOT_LEADER_RE.search(value) or has_form_signal(value)):
        return True
    if CHECKBOX_CLUSTER_RE.search(value) and (DOT_LEADER_RE.search(value) or has_form_signal(value)):
        return True
    if OPEN_CIRCLE_CLUSTER_RE.search(value) and has_form_signal(value):
        return True
    if DOT_LEADER_RE.search(value) and has_form_signal(value):
        return True
    return bool(FORM_HEADER_RE.search(value) and "CHECKED ITEM" in value.upper())


def split_prose_and_form_artifact(text: str) -> Optional[Tuple[str, str]]:
    value = text or ""
    if not looks_like_form_artifact(value):
        return None
    starts = []
    for pattern in (r"\bTable\s+\d+[.:]\s+", r"\bCHECKED\s+ITEM\b", r"\bYES\s+NO\s+N/?A\b"):
        match = re.search(pattern, value, flags=re.IGNORECASE)
        if match:
            starts.append(match.start())
    if not starts:
        return None
    start = min(starts)
    if start <= 0:
        return None
    prose = value[:start].strip()
    artifact = value[start:].strip()
    if not prose or not artifact or not looks_like_form_artifact(artifact):
        return None
    return prose, artifact


def split_form_artifact_tail(text: str) -> Tuple[str, str]:
    """Split a captured form block from trailing normal prose when paragraph breaks make it clear."""
    value = text or ""
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", value) if part.strip()]
    if len(paragraphs) < 2:
        return value, ""

    artifact_parts: List[str] = []
    tail_parts: List[str] = []
    saw_strong_form = False
    for part in paragraphs:
        is_caption_fragment = bool(re.match(r"^Table\s+\d+\.?$", part.strip(), re.IGNORECASE))
        is_form_part = is_caption_fragment or looks_like_form_artifact(part) or has_form_signal(part)
        if is_form_part:
            artifact_parts.append(part)
            if looks_like_form_artifact(part) or has_form_signal(part):
                saw_strong_form = True
            continue
        if saw_strong_form:
            tail_parts.append(part)
        else:
            artifact_parts.append(part)

    if not tail_parts:
        return value, ""
    artifact = "\n\n".join(artifact_parts).strip()
    tail = "\n\n".join(tail_parts).strip()
    if not artifact or not looks_like_form_artifact(artifact):
        return value, ""
    return artifact, tail


def artifact_caption(text: str) -> str:
    value = sanitize_visible_text(text or "", context="artifact")
    value = CHECKBOX_CLUSTER_RE.sub(" ", value)
    value = DOT_LEADER_RE.sub(" ", value)
    value = OPEN_CIRCLE_CLUSTER_RE.sub(" ", value)
    value = " ".join(value.split())
    match = re.search(r"\bTable\s+\d+[.:]\s+(.{1,140}?)(?:\s+Location\b|\s+CHECKED\s+ITEM\b|$)", value, re.IGNORECASE)
    if match:
        return match.group(0).strip()
    if "CHECKED ITEM" in value.upper():
        return "Reference form artifact"
    return value[:120] or "Reference form artifact"


def summarize_form_artifact(text: str) -> Dict[str, object]:
    sanitized = sanitize_visible_text(text or "", context="artifact")
    columns = []
    if FORM_HEADER_RE.search(sanitized):
        columns = ["checked_item", "yes", "no", "na", "comments"]
    return {
        "caption": artifact_caption(sanitized),
        "has_checkboxes": bool(CHECKBOX_CLUSTER_RE.search(sanitized) or "[ ]" in sanitized),
        "has_open_circle_fields": bool(OPEN_CIRCLE_CLUSTER_RE.search(sanitized)),
        "has_dot_leaders": bool(DOT_LEADER_RE.search(sanitized)),
        "form_columns": columns,
        "estimated_lines": len([line for line in sanitized.splitlines() if line.strip()]),
        "raw_text_escaped": sanitize_visible_text(text or "", context="artifact"),
    }


def artifact_text_summary(text: str) -> str:
    summary = summarize_form_artifact(text)
    caption = str(summary.get("caption") or "Reference form artifact")
    caption = caption.rstrip(".")
    return f"Reference form artifact: {caption}. Hidden from default checklist/review display."


def visible_form_leakage(text: str) -> bool:
    value = text or ""
    if CHECKBOX_CLUSTER_RE.search(value):
        return True
    if FORM_HEADER_RE.search(value) and "CHECKED ITEM" in value.upper():
        return True
    if DOT_LEADER_RE.search(value) and has_form_signal(value):
        return True
    if "Information on sign accurate and current | [ ] [ ] [ ]" in value:
        return True
    if "Sign legible and not defaced | [ ] [ ] [ ]" in value:
        return True
    return False
