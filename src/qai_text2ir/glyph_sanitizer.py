from __future__ import annotations

import re
from typing import Any, Dict, List

PRIVATE_USE_RE = re.compile(r"[\uE000-\uF8FF]")
REPLACEMENT_CHAR = "\uFFFD"

PUA_MARKER_MAP: Dict[str, str] = {
    "\uF0B7": "•",
    "\uF0D8": "•",
}

PUA_CHECKBOX_MAP: Dict[str, str] = {
    "\uEC1E": "[ ]",
}


def contains_private_use(text: str) -> bool:
    return bool(PRIVATE_USE_RE.search(text))


def pua_codepoints(text: str) -> List[str]:
    return sorted({f"U+{ord(ch):04X}" for ch in PRIVATE_USE_RE.findall(text)})


def escape_private_use(text: str) -> str:
    return PRIVATE_USE_RE.sub(lambda m: f"<PUA-U+{ord(m.group(0)):04X}>", text)


def normalize_marker_glyph(text: str) -> str:
    if not text:
        return text
    return "".join(PUA_MARKER_MAP.get(ch, ch) for ch in text)


def sanitize_visible_text(text: str, *, context: str = "prose") -> str:
    if not text:
        return text

    def replace(match: re.Match[str]) -> str:
        ch = match.group(0)
        if context in {"form", "table", "artifact"} and ch in PUA_CHECKBOX_MAP:
            return PUA_CHECKBOX_MAP[ch]
        if ch in PUA_MARKER_MAP:
            return PUA_MARKER_MAP[ch]
        return f"<PUA-U+{ord(ch):04X}>"

    return PRIVATE_USE_RE.sub(replace, text)


def sanitize_payload(value: Any, *, context: str = "prose") -> Any:
    if isinstance(value, str):
        return sanitize_visible_text(value, context=context)
    if isinstance(value, list):
        return [sanitize_payload(item, context=context) for item in value]
    if isinstance(value, dict):
        return {key: sanitize_payload(item, context=context) for key, item in value.items()}
    return value
