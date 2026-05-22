from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

from .glyph_sanitizer import contains_private_use, sanitize_visible_text

DOT_LEADER_RE = re.compile(r"\.{5,}")
FIXED_WIDTH_RE = re.compile(r"\S\s{8,}\S")
FORM_WORD_RE = re.compile(
    r"\b(?:CHECKED\s+ITEM|ENTER\s+DATE\s+OF\s+CHECK|COMMENTS?|Date\s+survey|Safety\s+surveyor|Biosafety\s+Level\s+Survey)\b",
    re.IGNORECASE,
)
FORM_HEADER_RE = re.compile(r"\bYES\s+NO\s+N/?A\b|\bYES\s+NO\s+N/?A\s+COMMENTS?\b", re.IGNORECASE)
TABLE_FORM_START_RE = re.compile(
    r"\bTable\s+\d+[.:]\s+.*?(?:survey|checklist|form)\b",
    re.IGNORECASE | re.DOTALL,
)
CHECKBOX_RE = re.compile(r"(?:\[[ xX]\]|☐|☑|☒|□|■|✓|✔|○|●)")


def has_dot_leader(text: str) -> bool:
    return bool(DOT_LEADER_RE.search(text or ""))


def has_fixed_width_clue(text: str) -> bool:
    return bool(FIXED_WIDTH_RE.search(text or ""))


def has_form_word(text: str) -> bool:
    return bool(FORM_WORD_RE.search(text or "") or FORM_HEADER_RE.search(text or ""))


def looks_like_form_artifact(text: str) -> bool:
    if not text:
        return False
    has_form_marker = has_form_word(text)
    if contains_private_use(text) and has_dot_leader(text):
        return True
    if has_dot_leader(text) and (has_form_marker or CHECKBOX_RE.search(text)):
        return True
    if has_form_marker and has_fixed_width_clue(text):
        return True
    if TABLE_FORM_START_RE.search(text) and (has_fixed_width_clue(text) or has_form_marker):
        return True
    return False


def split_prose_and_form_artifact(text: str) -> Optional[Tuple[str, str]]:
    if not text or not looks_like_form_artifact(text):
        return None
    candidates = [
        r"\bTable\s+\d+[.:]\s+",
        r"\bCHECKED\s+ITEM\b",
        r"\bYES\s+NO\s+N/?A\b",
    ]
    earliest: Optional[int] = None
    for pattern in candidates:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match and (earliest is None or match.start() < earliest):
            earliest = match.start()
    if earliest is None or earliest <= 0:
        return None
    prose = text[:earliest].strip()
    artifact = text[earliest:].strip()
    if not prose or not artifact:
        return None
    if not looks_like_form_artifact(artifact):
        return None
    return prose, artifact


def sanitize_form_artifact_text(text: str) -> str:
    cleaned = sanitize_visible_text(text or "", context="form")
    cleaned = DOT_LEADER_RE.sub(" | ", cleaned)
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
    cleaned = re.sub(r"\s+\|", " |", cleaned)
    cleaned = re.sub(r"\|\s+", "| ", cleaned)
    return cleaned.strip()


def artifact_flags(text: str) -> List[str]:
    flags: List[str] = []
    if contains_private_use(text or ""):
        flags.append("literal_pua")
    if has_dot_leader(text or ""):
        flags.append("dot_leader")
    if has_form_word(text or ""):
        flags.append("form_words")
    if has_fixed_width_clue(text or ""):
        flags.append("fixed_width")
    if CHECKBOX_RE.search(text or ""):
        flags.append("checkbox")
    return flags


def artifact_summary(text: str) -> Dict[str, object]:
    return {
        "flags": artifact_flags(text),
        "looks_like_form_artifact": looks_like_form_artifact(text),
    }
