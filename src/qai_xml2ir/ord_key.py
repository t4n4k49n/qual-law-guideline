from __future__ import annotations

import re
from typing import List, Optional

SEG_WIDTH = 6
ORD_WIDTH = 8


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


def format_segments(segs: List[int]) -> str:
    return ".".join(f"{seg:0{SEG_WIDTH}d}" for seg in segs)


def build_ord(parent_ord: Optional[str], local_segs: List[int]) -> str:
    local_part = format_segments([*local_segs, 0])
    if parent_ord:
        return f"{parent_ord}.{local_part}"
    return local_part


def assign_document_order(root) -> int:
    counter = 0
    stack = [root]
    while stack:
        node = stack.pop()
        nid = getattr(node, "nid", None)
        if nid != "root":
            counter += 1
            node.ord = f"{counter:0{ORD_WIDTH}d}"
        children = getattr(node, "children", None) or []
        if children:
            stack.extend(reversed(children))
    return counter
