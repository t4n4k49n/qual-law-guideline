from __future__ import annotations

import re
from typing import List, Optional


def normalize_num_attr(num: Optional[str]) -> Optional[str]:
    if not num:
        return None
    normalized = num.translate(str.maketrans("０１２３４５６７８９", "0123456789"))
    cleaned = re.sub(r"[^0-9_]", "", normalized)
    return cleaned or None


def num_attr_to_segments(num_attr: Optional[str]) -> List[int]:
    normalized = normalize_num_attr(num_attr)
    if not normalized:
        return []
    return [int(part) for part in normalized.split("_") if part != ""]


def assign_document_order(root) -> int:
    counter = 0
    stack = [root]
    while stack:
        node = stack.pop()
        if getattr(node, "nid", None) != "root":
            counter += 1
            node.ord = counter
        children = getattr(node, "children", None) or []
        if children:
            stack.extend(reversed(children))
    return counter
