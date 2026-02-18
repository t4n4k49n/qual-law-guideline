from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from qai_xml2ir.models_ir import Node


@dataclass
class _SearchResult:
    node: Node
    ancestors: List[Node]


def _find_with_ancestors(root: Node, nid: str) -> Optional[_SearchResult]:
    stack: List[Tuple[Node, List[Node]]] = [(root, [])]
    while stack:
        node, ancestors = stack.pop()
        if node.nid == nid:
            return _SearchResult(node=node, ancestors=ancestors)
        for child in reversed(node.children):
            stack.append((child, [*ancestors, node]))
    return None


def _resolve_rule(purpose_profile: Dict[str, object], selected_kind: str) -> Dict[str, object]:
    policies = purpose_profile.get("context_display_policy")
    if not isinstance(policies, list):
        return {}
    for policy in policies:
        if not isinstance(policy, dict):
            continue
        when_kind = policy.get("when_kind")
        if isinstance(when_kind, str) and when_kind == selected_kind:
            return policy
    return {}


def _collect_descendants(
    base_nodes: List[Node],
    *,
    max_depth: int,
    kinds: Optional[Set[str]],
) -> List[Node]:
    out: List[Node] = []
    for base in base_nodes:
        stack: List[Tuple[Node, int]] = [(base, 0)]
        while stack:
            node, depth = stack.pop()
            if depth >= max_depth:
                continue
            for child in node.children:
                next_depth = depth + 1
                if kinds is None or child.kind in kinds:
                    out.append(child)
                stack.append((child, next_depth))
    return out


def resolve_context_nodes(root: Node, selected_nid: str, purpose_profile: Dict[str, object]) -> List[Node]:
    found = _find_with_ancestors(root, selected_nid)
    if found is None:
        return []
    selected = found.node
    ancestors = found.ancestors
    rule = _resolve_rule(purpose_profile, selected.kind)

    include_until = rule.get("include_ancestors_until_kind")
    included_ancestors: List[Node] = []
    for anc in reversed(ancestors):
        if anc.kind == "document":
            continue
        included_ancestors.append(anc)
        if isinstance(include_until, str) and include_until and anc.kind == include_until:
            break
    included_ancestors.reverse()

    result: List[Node] = [*included_ancestors, selected]
    seen = {n.nid for n in result}

    if bool(rule.get("include_descendants")):
        include_of = str(rule.get("include_descendants_of") or "selected")
        if include_of == "ancestors":
            bases = included_ancestors
        elif include_of == "both":
            bases = [*included_ancestors, selected]
        else:
            bases = [selected]
        max_depth_raw = rule.get("include_descendants_max_depth")
        if isinstance(max_depth_raw, int) and max_depth_raw > 0:
            max_depth = max_depth_raw
        else:
            max_depth = 8
        kinds_raw = rule.get("include_descendants_kinds")
        kinds: Optional[Set[str]] = None
        if isinstance(kinds_raw, list):
            allowed = {str(v) for v in kinds_raw if isinstance(v, str) and v}
            kinds = allowed or None
        descendants = _collect_descendants(bases, max_depth=max_depth, kinds=kinds)
        for node in descendants:
            if node.nid in seen:
                continue
            seen.add(node.nid)
            result.append(node)

    return result
