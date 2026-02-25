from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional


MARKER_RE = re.compile(r"<!--\s*PR_BODY_FILE:\s*([^\s].*?)\s*-->")
ALLOWED_CONTROLS = {9, 10, 13}  # tab, LF, CR


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def find_marker_path(text: str) -> Optional[str]:
    match = MARKER_RE.search(text)
    if not match:
        return None
    return match.group(1).strip()


def is_safe_relative_path(path_str: str) -> bool:
    p = Path(path_str)
    if p.is_absolute():
        return False
    if "\\" in path_str:
        return False
    parts = p.parts
    if any(part in ("..", "") for part in parts):
        return False
    return True


def validate_text_content(text: str) -> List[str]:
    issues: List[str] = []
    if "\\n" in text:
        issues.append(r"contains raw '\n' sequence")
    if "�" in text:
        issues.append("contains replacement character U+FFFD")
    for idx, ch in enumerate(text):
        code = ord(ch)
        if code < 32 and code not in ALLOWED_CONTROLS:
            issues.append(f"contains disallowed control char U+{code:04X} at offset {idx}")
            break
    return issues
