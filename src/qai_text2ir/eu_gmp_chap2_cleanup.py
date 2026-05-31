from __future__ import annotations

import re
from typing import Any


_SPACE_RE = re.compile(r"\s+")


def _walk(node: Any):
    if node is None:
        return
    yield node
    for child in getattr(node, "children", []) or []:
        yield from _walk(child)


def _clean_text(value: str) -> str:
    return _SPACE_RE.sub(" ", value).strip()


def normalize_eu_gmp_chap2_cleanup(root: Any) -> dict[str, int]:
    changed = 0
    for node in _walk(root):
        if getattr(node, "kind", None) in {"table", "table_header", "table_row", "preformatted"}:
            continue
        for field in ("heading", "text"):
            value = getattr(node, field, None)
            if not isinstance(value, str) or not value:
                continue
            cleaned = _clean_text(value)
            if cleaned != value:
                setattr(node, field, cleaned)
                changed += 1
    return {"changed_fields": changed}
