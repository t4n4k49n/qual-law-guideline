from __future__ import annotations

import re
from typing import Dict, Iterable, Iterator, List, Optional, Tuple


def _get(node, key: str):
    if isinstance(node, dict):
        return node.get(key)
    return getattr(node, key, None)


def _get_children(node) -> List:
    children = _get(node, "children")
    return children or []


def walk_nodes(root) -> Iterator:
    stack = [root]
    while stack:
        node = stack.pop()
        yield node
        children = _get_children(node)
        if children:
            stack.extend(reversed(children))


def collect_nids(root) -> List[str]:
    nids: List[str] = []
    for node in walk_nodes(root):
        nid = _get(node, "nid")
        if nid:
            nids.append(nid)
    return nids


def assert_unique_nids(root) -> None:
    seen = set()
    duplicates = []
    for nid in collect_nids(root):
        if nid in seen:
            duplicates.append(nid)
        else:
            seen.add(nid)
    if duplicates:
        raise AssertionError(f"Duplicate nids detected: {sorted(set(duplicates))}")


def summarize_kinds(root) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for node in walk_nodes(root):
        kind = _get(node, "kind")
        if kind:
            counts[kind] = counts.get(kind, 0) + 1
    return counts


def check_annex_article_nids(root) -> Tuple[List[str], List[str]]:
    main = []
    annex = []
    for node in walk_nodes(root):
        if _get(node, "kind") != "article":
            continue
        nid = _get(node, "nid")
        if not nid:
            continue
        if nid.startswith("annex"):
            annex.append(nid)
        else:
            main.append(nid)
    collisions = sorted(set(main).intersection(set(annex)))
    invalid_annex = [nid for nid in annex if ".art" not in nid]
    return collisions, invalid_annex


_APPDX_RE = re.compile(r"(appdx_(?:table|note|style|fig|format)|appdx)([0-9_]+)$")
def check_appendix_scoped_indices(root) -> List[str]:
    problems: List[str] = []
    for parent in walk_nodes(root):
        children = _get_children(parent)
        appdx_children = [c for c in children if _get(c, "kind") == "appendix"]
        if not appdx_children:
            continue
        by_key: Dict[str, List[int]] = {}
        for child in appdx_children:
            nid = _get(child, "nid") or ""
            m = _APPDX_RE.search(nid)
            if not m:
                continue
            key, num_str = m.group(1), m.group(2)
            head = num_str.split("_", 1)[0]
            try:
                num = int(head)
            except ValueError:
                continue
            by_key.setdefault(key, []).append(num)
        for key, nums in by_key.items():
            if not nums:
                continue
            count = len(nums)
            if any(num > count for num in nums):
                continue
            expected = list(range(1, count + 1))
            if sorted(nums) != expected:
                parent_nid = _get(parent, "nid")
                problems.append(
                    f"appendix index for {key} under {parent_nid} is not contiguous: {sorted(nums)}"
                )
    return problems


def check_ord_format_and_order(root) -> List[str]:
    problems: List[str] = []
    seen: set[int] = set()
    prev_ord: Optional[int] = None
    for node in walk_nodes(root):
        nid = _get(node, "nid")
        ord_val = _get(node, "ord")
        if nid != "root":
            if not isinstance(ord_val, int):
                problems.append(f"invalid ord type at {nid}: {ord_val!r}")
            else:
                if ord_val <= 0:
                    problems.append(f"invalid ord value at {nid}: {ord_val}")
                if ord_val in seen:
                    problems.append(f"duplicate ord value at {nid}: {ord_val}")
                else:
                    seen.add(ord_val)
                if prev_ord is not None and ord_val <= prev_ord:
                    problems.append(
                        f"ord is not strictly increasing at {nid}: {ord_val} <= {prev_ord}"
                    )
                prev_ord = ord_val
        children = _get_children(node)
        if not children:
            continue
        ords: List[int] = []
        has_invalid_child = False
        for child in children:
            child_nid = _get(child, "nid")
            child_ord = _get(child, "ord")
            if not isinstance(child_ord, int):
                problems.append(f"missing ord at {child_nid}")
                has_invalid_child = True
                continue
            ords.append(child_ord)
        if has_invalid_child:
            continue
        if ords != sorted(ords):
            parent_nid = _get(node, "nid")
            problems.append(f"children ord not sorted under {parent_nid}")
    return problems
