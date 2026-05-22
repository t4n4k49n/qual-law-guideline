from __future__ import annotations

from typing import Any, Dict, List, Sequence, Tuple

from qai_mock_ui.ir_model import DocIndex, Node


Rule = Dict[str, Any]


def resolve_candidate_visibility_rules(purpose_profile: Dict[str, Any]) -> Tuple[List[Rule], List[Rule]]:
    cfg = purpose_profile.get("candidate_visibility")
    if not isinstance(cfg, dict):
        return [], []
    allow_raw = cfg.get("allow_rules")
    deny_raw = cfg.get("deny_rules")
    allow_rules = [rule for rule in allow_raw if isinstance(rule, dict)] if isinstance(allow_raw, list) else []
    deny_rules = [rule for rule in deny_raw if isinstance(rule, dict)] if isinstance(deny_raw, list) else []
    return allow_rules, deny_rules


def build_candidate_visibility_map(index: DocIndex, purpose_profile: Dict[str, Any]) -> Dict[str, bool]:
    allow_rules, deny_rules = resolve_candidate_visibility_rules(purpose_profile)
    visible: Dict[str, bool] = {}
    for node in index.by_nid.values():
        if node.kind == "document" or node.nid == "root":
            visible[node.nid] = True
            continue
        visible[node.nid] = _is_node_visible(index, node, allow_rules=allow_rules, deny_rules=deny_rules)
    return visible


def _is_node_visible(
    index: DocIndex,
    node: Node,
    *,
    allow_rules: Sequence[Rule],
    deny_rules: Sequence[Rule],
) -> bool:
    if allow_rules and not any(_rule_matches(index, node, rule) for rule in allow_rules):
        return False
    if any(_rule_matches(index, node, rule) for rule in deny_rules):
        return False
    return True


def _rule_matches(index: DocIndex, node: Node, rule: Rule) -> bool:
    known = False
    ancestors = index.ancestors_of(node.nid)

    kind = rule.get("kind")
    if isinstance(kind, str) and kind:
        known = True
        if node.kind != kind:
            return False

    kind_in = rule.get("kind_in")
    if isinstance(kind_in, list):
        kinds = {str(v) for v in kind_in if isinstance(v, str) and v}
        if kinds:
            known = True
            if node.kind not in kinds:
                return False

    nid_prefix = rule.get("nid_prefix")
    if isinstance(nid_prefix, str) and nid_prefix:
        known = True
        if not node.nid.startswith(nid_prefix):
            return False

    under_kind = rule.get("under_kind")
    if isinstance(under_kind, str) and under_kind:
        known = True
        if not any(anc.kind == under_kind for anc in ancestors):
            return False

    under_nid_prefix = rule.get("under_nid_prefix")
    if isinstance(under_nid_prefix, str) and under_nid_prefix:
        known = True
        if not any(anc.nid.startswith(under_nid_prefix) for anc in ancestors):
            return False

    return known
