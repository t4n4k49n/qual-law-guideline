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
            if nums and min(nums) != 1:
                parent_nid = _get(parent, "nid")
                problems.append(
                    f"appendix index for {key} under {parent_nid} starts at {min(nums)}"
                )
    return problems
