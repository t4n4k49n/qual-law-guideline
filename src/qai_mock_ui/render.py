from __future__ import annotations

from dataclasses import dataclass
import re
import sys
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

from qai_mock_ui.ir_model import DocIndex, Node


@dataclass
class RenderBlock:
    nid: str
    kind: str
    header_lines: List[str]
    header_line_nids: List[str]
    item_lines: List[str]
    item_line_nids: List[str]
    header_omitted: bool


@dataclass
class _RuleOptions:
    include_ancestors_until_kind: Optional[str]
    include_ancestors_until_kinds: Optional[Set[str]]
    include_headings: bool
    include_chapeau_text: bool
    include_descendants: bool
    include_descendants_of: str
    include_descendants_kinds: Optional[Set[str]]
    include_descendants_max_depth: int
    force_article_p1_text: bool
    suppress_duplicate_headings: bool


@dataclass
class _SelectionPlan:
    selected: Node
    included_ancestors: List[Node]
    header_lines_full: List[str]
    header_line_nids_full: List[str]
    item_lines: List[str]
    item_line_nids: List[str]


@dataclass
class _RenderOptions:
    egov_merge_article_p1: bool = False


_ARTICLE_NID_RE = re.compile(r"^art\d+(?:_\d+)?$")


def _single_line(text: str) -> str:
    return " ".join(text.strip().split())


def _pick_rule(purpose_profile: Dict[str, Any], kind: str) -> Dict[str, Any]:
    policies = purpose_profile.get("context_display_policy")
    if not isinstance(policies, list):
        return {}
    for rule in policies:
        if isinstance(rule, dict) and str(rule.get("when_kind") or "") == kind:
            return rule
    return {}


def _resolve_render_options(
    purpose_profile: Dict[str, Any],
    render_options: Optional[Dict[str, Any]],
) -> _RenderOptions:
    templates = purpose_profile.get("render_templates")
    template_defaults = templates if isinstance(templates, dict) else {}
    default_merge = bool(template_defaults.get("egov_merge_article_p1"))

    if isinstance(render_options, dict) and "egov_merge_article_p1" in render_options:
        return _RenderOptions(egov_merge_article_p1=bool(render_options.get("egov_merge_article_p1")))
    return _RenderOptions(egov_merge_article_p1=default_merge)


def _suggest_fold_remap_to_p1(index: DocIndex, nid: str) -> Optional[str]:
    parts = nid.split(".")
    if len(parts) < 2:
        return None
    for i, part in enumerate(parts[:-1]):
        if not _ARTICLE_NID_RE.match(part):
            continue
        next_part = parts[i + 1]
        if next_part.startswith("p"):
            continue
        candidate = ".".join(parts[: i + 1] + ["p1"] + parts[i + 1 :])
        if candidate in index.by_nid:
            return candidate
        return None
    return None


def resolve_selected_nids(
    index: DocIndex,
    selected_nids: Sequence[str],
) -> Tuple[List[str], List[str], Dict[str, str]]:
    resolved_nids: List[str] = []
    missing_nids: List[str] = []
    suggested_remap: Dict[str, str] = {}

    for nid in selected_nids:
        if nid in index.by_nid:
            resolved_nids.append(nid)
            continue
        missing_nids.append(nid)
        suggestion = _suggest_fold_remap_to_p1(index, nid)
        if suggestion:
            suggested_remap[nid] = suggestion
    return resolved_nids, missing_nids, suggested_remap


def _missing_nids_message(missing_nids: Sequence[str], suggested_remap: Dict[str, str]) -> str:
    base = f"selected_nids に存在しない nid が含まれています: {', '.join(missing_nids)}"
    if not suggested_remap:
        return base
    suggestions = ", ".join([f"{src} -> {dst}" for src, dst in suggested_remap.items()])
    return f"{base} | 旧fold由来の候補: {suggestions}"


def _parse_rule_options(rule: Dict[str, Any]) -> _RuleOptions:
    include_until = rule.get("include_ancestors_until_kind")
    include_ancestors_until_kind = (
        str(include_until) if isinstance(include_until, str) and include_until else None
    )
    include_until_many = rule.get("include_ancestors_until_kinds")
    include_ancestors_until_kinds = (
        {str(v) for v in include_until_many if isinstance(v, str) and v}
        if isinstance(include_until_many, list)
        else None
    )
    include_headings = bool(rule.get("include_headings"))
    include_chapeau_text = bool(rule.get("include_chapeau_text"))
    include_descendants = bool(rule.get("include_descendants"))
    include_descendants_of = str(rule.get("include_descendants_of") or "selected")
    force_article_p1_text = bool(rule.get("force_article_p1_text"))
    suppress_duplicate_headings = bool(rule.get("suppress_duplicate_headings"))
    depth_raw = rule.get("include_descendants_max_depth")
    include_descendants_max_depth = depth_raw if isinstance(depth_raw, int) and depth_raw > 0 else 8
    kinds_raw = rule.get("include_descendants_kinds")
    include_descendants_kinds = (
        {str(v) for v in kinds_raw if isinstance(v, str) and v}
        if isinstance(kinds_raw, list)
        else None
    )
    return _RuleOptions(
        include_ancestors_until_kind=include_ancestors_until_kind,
        include_ancestors_until_kinds=include_ancestors_until_kinds,
        include_headings=include_headings,
        include_chapeau_text=include_chapeau_text,
        include_descendants=include_descendants,
        include_descendants_of=include_descendants_of,
        include_descendants_kinds=include_descendants_kinds,
        include_descendants_max_depth=include_descendants_max_depth,
        force_article_p1_text=force_article_p1_text,
        suppress_duplicate_headings=suppress_duplicate_headings,
    )


def _included_ancestors(
    index: DocIndex,
    selected_nid: str,
    include_until_kind: Optional[str],
    include_until_kinds: Optional[Set[str]] = None,
) -> List[Node]:
    ancestors = index.ancestors_of(selected_nid)
    if not ancestors:
        return []
    included_from_bottom: List[Node] = []
    for anc in reversed(ancestors):
        if anc.kind == "document" or anc.nid == "root":
            continue
        included_from_bottom.append(anc)
        if include_until_kinds and anc.kind in include_until_kinds:
            break
        if include_until_kind and anc.kind == include_until_kind:
            break
    included_from_bottom.reverse()
    return included_from_bottom


def _collect_descendants(
    index: DocIndex,
    base_nodes: Iterable[Node],
    *,
    include_kinds: Optional[Set[str]],
    max_depth: int,
) -> List[Node]:
    uniq: Dict[str, Node] = {}
    for base in base_nodes:
        for node in index.descendants_of(base.nid, max_depth=max_depth, include_kinds=include_kinds):
            uniq[node.nid] = node
    return sorted(uniq.values(), key=lambda n: (n.ord, n.nid))


def _line_head_from_num(node: Node) -> Optional[str]:
    if not node.num:
        return None
    num = _single_line(str(node.num))
    if not num:
        return None
    if node.kind == "chapter":
        return f"第{num}章"
    if node.kind == "article":
        return f"第{num}条"
    if node.kind == "paragraph":
        return str(num)
    if node.kind == "item":
        return str(num)
    if node.kind == "subitem":
        return str(num)
    return str(num)


def _resolve_line_head(index: DocIndex, node: Node) -> Optional[str]:
    display = index.display_name_by_nid.get(node.nid)
    if display:
        head = _single_line(str(display))
        if head:
            heading = _single_line(str(node.heading or ""))
            # display_name が「行頭 + heading」の合成表現なら、行頭部分だけ使う。
            # 例: "第一条 （薬局の構造設備）" -> "第一条"
            if heading and head.endswith(heading):
                prefix = head[: -len(heading)].strip()
                if prefix:
                    return prefix
            return head
    return _line_head_from_num(node)


def _build_common_line(index: DocIndex, node: Node) -> str:
    head = _resolve_line_head(index, node)
    text = _single_line(node.text or "")
    if head and text:
        return f"{head}\u3000{text}"
    if text:
        return text
    if head:
        return head
    return ""


def _as_row_cells(text: str) -> List[str]:
    return [_single_line(part) for part in text.split("|")]


def _format_table_row_lines(
    node: Node,
    *,
    header_text: Optional[str],
    header_nid: Optional[str],
) -> Tuple[List[str], List[str]]:
    row_cells = _as_row_cells(node.text or "")
    if not row_cells:
        line = _build_common_line_from_row_fallback(node)
        return ([line] if line else []), ([node.nid] if line else [])

    if header_text:
        header_cells = _as_row_cells(header_text)
        if len(header_cells) == len(row_cells):
            sep_cells = ["---"] * len(row_cells)
            src = header_nid or node.nid
            return (
                [
                    "| " + " | ".join(header_cells) + " |",
                    "| " + " | ".join(sep_cells) + " |",
                    "| " + " | ".join(row_cells) + " |",
                ],
                [src, src, node.nid],
            )
    return (["| " + " | ".join(row_cells) + " |"], [node.nid])


def _build_common_line_from_row_fallback(node: Node) -> str:
    text = _single_line(node.text or "")
    return text


def _build_header_lines(
    index: DocIndex,
    ancestors: Sequence[Node],
    options: _RuleOptions,
) -> Tuple[List[str], List[str]]:
    lines: List[str] = []
    nids: List[str] = []
    if options.include_headings:
        for anc in ancestors:
            heading = _single_line(str(anc.heading or ""))
            if heading:
                lines.append(heading)
                nids.append(anc.nid)
    if options.include_chapeau_text:
        for anc in ancestors:
            line = _build_common_line(index, anc)
            if line:
                lines.append(line)
                nids.append(anc.nid)
    dedup_lines: List[str] = []
    dedup_nids: List[str] = []
    for line, nid in zip(lines, nids):
        if dedup_lines and dedup_lines[-1] == line:
            if options.suppress_duplicate_headings or dedup_nids[-1] == nid:
                continue
        if options.suppress_duplicate_headings and line in dedup_lines:
            continue
        dedup_lines.append(line)
        dedup_nids.append(nid)
    return dedup_lines, dedup_nids


def _build_descendant_lines(
    index: DocIndex,
    descendants: Sequence[Node],
) -> Tuple[List[str], List[str]]:
    lines: List[str] = []
    nids: List[str] = []
    for node in descendants:
        line = _build_common_line(index, node)
        if line:
            lines.append(line)
            nids.append(node.nid)
    return lines, nids


def _first_paragraph_nid_for_article(index: DocIndex, article_nid: str) -> Optional[str]:
    article = index.by_nid.get(article_nid)
    if article is None or article.kind != "article":
        return None
    fallback: Optional[str] = None
    for child in article.children:
        if child.kind != "paragraph":
            continue
        if fallback is None:
            fallback = child.nid
        num = _single_line(str(child.num or ""))
        if num in {"1", "１"}:
            return child.nid
    return fallback


def _article_node_for_paragraph1(index: DocIndex, paragraph_nid: str) -> Optional[Node]:
    node = index.by_nid.get(paragraph_nid)
    if node is None or node.kind != "paragraph":
        return None
    num = _single_line(str(node.num or ""))
    if num not in {"1", "１"}:
        return None
    for anc in reversed(index.ancestors_of(paragraph_nid)):
        if anc.kind == "article":
            return anc
    return None


def _apply_line_templates_split(
    index: DocIndex,
    header_lines: List[str],
    header_nids: List[str],
    item_lines: List[str],
    item_nids: List[str],
    options: _RenderOptions,
) -> Tuple[List[str], List[str], List[str], List[str]]:
    if not options.egov_merge_article_p1:
        return header_lines, header_nids, item_lines, item_nids

    # 先に祖先+選択本体を1本の連鎖として扱い、テンプレ適用後に header/item へ再分配する。
    chain_lines = list(header_lines) + list(item_lines)
    chain_nids = list(header_nids) + list(item_nids)
    chain_bucket = (["H"] * len(header_lines)) + (["I"] * len(item_lines))

    # Pass1: paragraph(1) 行を「第一条 + 本文」に統一
    normalized_lines: List[str] = []
    normalized_nids: List[str] = []
    normalized_bucket: List[str] = []
    for line, nid, bucket in zip(chain_lines, chain_nids, chain_bucket):
        new_line = line
        article = _article_node_for_paragraph1(index, nid)
        if article is not None:
            article_num = _single_line(str(article.num or ""))
            para_text = _single_line(index.by_nid[nid].text or "")
            if article_num and para_text:
                new_line = f"{article_num}\u3000{para_text}"
        normalized_lines.append(new_line)
        normalized_nids.append(nid)
        normalized_bucket.append(bucket)

    # Pass2: article行 + paragraph(1)行の並びは article行を圧縮
    out_lines: List[str] = []
    out_nids: List[str] = []
    out_bucket: List[str] = []
    i = 0
    while i < len(normalized_lines):
        cur_nid = normalized_nids[i]
        cur_node = index.by_nid.get(cur_nid)
        if cur_node is not None and cur_node.kind == "article" and i + 1 < len(normalized_lines):
            next_nid = normalized_nids[i + 1]
            p1_nid = _first_paragraph_nid_for_article(index, cur_nid)
            if p1_nid is not None and next_nid == p1_nid:
                # articleの次がその第1項行なら article行を落とす
                out_lines.append(normalized_lines[i + 1])
                out_nids.append(next_nid)
                out_bucket.append(normalized_bucket[i + 1])
                i += 2
                continue
        out_lines.append(normalized_lines[i])
        out_nids.append(normalized_nids[i])
        out_bucket.append(normalized_bucket[i])
        i += 1

    new_header_lines: List[str] = []
    new_header_nids: List[str] = []
    new_item_lines: List[str] = []
    new_item_nids: List[str] = []
    for line, nid, bucket in zip(out_lines, out_nids, out_bucket):
        if bucket == "H":
            new_header_lines.append(line)
            new_header_nids.append(nid)
        else:
            new_item_lines.append(line)
            new_item_nids.append(nid)
    return new_header_lines, new_header_nids, new_item_lines, new_item_nids


def _extract_selection_plan(
    index: DocIndex,
    selected: Node,
    rule: Dict[str, Any],
    *,
    render_options: _RenderOptions,
) -> _SelectionPlan:
    options = _parse_rule_options(rule)
    included_ancestors = _included_ancestors(
        index,
        selected.nid,
        options.include_ancestors_until_kind,
        options.include_ancestors_until_kinds,
    )

    header_lines, header_nids = _build_header_lines(index, included_ancestors, options)
    if options.force_article_p1_text and selected.kind != "paragraph":
        article_nid: Optional[str] = None
        for anc in reversed(included_ancestors):
            if anc.kind == "article":
                article_nid = anc.nid
                break
        if article_nid is not None:
            article = index.by_nid.get(article_nid)
            if article is not None:
                p1_node: Optional[Node] = None
                for child in article.children:
                    if child.kind != "paragraph":
                        continue
                    num = _single_line(str(child.num or ""))
                    if num in {"1", "１"}:
                        p1_node = child
                        break
                    if p1_node is None:
                        p1_node = child
                if p1_node is not None:
                    p1_line = _build_common_line(index, p1_node)
                    if p1_line and p1_line not in header_lines:
                        insert_at = 0
                        for i, nid in enumerate(header_nids):
                            if nid == article_nid:
                                insert_at = i + 1
                        header_lines.insert(insert_at, p1_line)
                        header_nids.insert(insert_at, p1_node.nid)

    selected_desc_lines: List[str] = []
    selected_desc_nids: List[str] = []

    if options.include_descendants:
        if options.include_descendants_of in ("ancestors", "both"):
            anc_desc = _collect_descendants(
                index,
                included_ancestors,
                include_kinds=options.include_descendants_kinds,
                max_depth=options.include_descendants_max_depth,
            )
            anc_lines, anc_nids = _build_descendant_lines(index, anc_desc)
            header_lines.extend(anc_lines)
            header_nids.extend(anc_nids)
        if options.include_descendants_of in ("selected", "both"):
            sel_desc = _collect_descendants(
                index,
                [selected],
                include_kinds=options.include_descendants_kinds,
                max_depth=options.include_descendants_max_depth,
            )
            selected_desc_lines, selected_desc_nids = _build_descendant_lines(index, sel_desc)

    item_lines: List[str]
    item_nids: List[str]
    if selected.kind == "table_row":
        table_header_text = None
        table_header_nid = None
        for anc in reversed(included_ancestors):
            if anc.kind == "table_header" and anc.text:
                table_header_text = anc.text
                table_header_nid = anc.nid
                break
        item_lines, item_nids = _format_table_row_lines(
            selected,
            header_text=table_header_text,
            header_nid=table_header_nid,
        )
    else:
        line = _build_common_line(index, selected)
        item_lines = [line] if line else []
        item_nids = [selected.nid] if line else []

    item_lines.extend(selected_desc_lines)
    item_nids.extend(selected_desc_nids)

    (
        header_lines,
        header_nids,
        item_lines,
        item_nids,
    ) = _apply_line_templates_split(
        index,
        header_lines,
        header_nids,
        item_lines,
        item_nids,
        render_options,
    )

    return _SelectionPlan(
        selected=selected,
        included_ancestors=included_ancestors,
        header_lines_full=header_lines,
        header_line_nids_full=header_nids,
        item_lines=item_lines,
        item_line_nids=item_nids,
    )


def _apply_header_dedup(
    *,
    mode: str,
    current_lines: List[str],
    current_nids: List[str],
    previous_lines: Optional[List[str]],
) -> Tuple[List[str], List[str], bool]:
    if previous_lines is None:
        return current_lines, current_nids, False

    if mode == "prefix":
        common_len = 0
        for prev_line, curr_line in zip(previous_lines, current_lines):
            if prev_line != curr_line:
                break
            common_len += 1
        shown_lines = current_lines[common_len:]
        shown_nids = current_nids[common_len:]
        omitted = bool(current_lines) and not shown_lines
        return shown_lines, shown_nids, omitted

    # exact
    omitted = bool(current_lines) and previous_lines == current_lines
    if omitted:
        return [], [], True
    return current_lines, current_nids, False


def render_selected_nodes(
    index: DocIndex,
    purpose_profile: Dict[str, Any],
    selected_nids: Sequence[str],
    header_dedup_mode: str = "exact",
    render_options: Optional[Dict[str, Any]] = None,
    on_missing_nids: str = "error",
) -> List[RenderBlock]:
    options = _resolve_render_options(purpose_profile, render_options)
    resolved_nids, missing_nids, suggested_remap = resolve_selected_nids(index, selected_nids)

    mode = on_missing_nids.lower().strip()
    if mode not in {"error", "warn", "ignore"}:
        raise ValueError(f"unknown on_missing_nids mode: {on_missing_nids}")
    if missing_nids:
        message = _missing_nids_message(missing_nids, suggested_remap)
        if mode == "error":
            raise ValueError(message)
        if mode == "warn":
            sys.stderr.write(message + "\n")

    selected_nodes = [index.by_nid[nid] for nid in resolved_nids]
    selected_nodes.sort(key=lambda n: (n.ord, n.nid))

    plans: List[_SelectionPlan] = []
    for selected in selected_nodes:
        rule = _pick_rule(purpose_profile, selected.kind)
        plans.append(_extract_selection_plan(index, selected, rule, render_options=options))

    blocks: List[RenderBlock] = []
    prev_header_full_lines: Optional[List[str]] = None
    prev_context_for_prefix: Optional[List[str]] = None
    for plan in plans:
        compare_lines = prev_header_full_lines
        if header_dedup_mode == "prefix":
            compare_lines = prev_context_for_prefix
        shown_header_lines, shown_header_nids, header_omitted = _apply_header_dedup(
            mode=header_dedup_mode,
            current_lines=plan.header_lines_full,
            current_nids=plan.header_line_nids_full,
            previous_lines=compare_lines,
        )

        blocks.append(
            RenderBlock(
                nid=plan.selected.nid,
                kind=plan.selected.kind,
                header_lines=shown_header_lines,
                header_line_nids=shown_header_nids,
                item_lines=plan.item_lines,
                item_line_nids=plan.item_line_nids,
                header_omitted=header_omitted,
            )
        )
        prev_header_full_lines = plan.header_lines_full
        prev_context_for_prefix = plan.header_lines_full + plan.item_lines
    return blocks


def render_text_preview(blocks: Sequence[RenderBlock]) -> str:
    lines: List[str] = []
    for block in blocks:
        if not block.header_omitted:
            lines.extend(block.header_lines)
        lines.extend(block.item_lines)
    return "\n".join(lines)


def build_render_debug_trace(
    index: DocIndex,
    purpose_profile: Dict[str, Any],
    selected_nids: Sequence[str],
    header_dedup_mode: str = "exact",
    render_options: Optional[Dict[str, Any]] = None,
    on_missing_nids: str = "error",
) -> List[Dict[str, Any]]:
    render_opts = _resolve_render_options(purpose_profile, render_options)
    resolved_nids, missing_nids, suggested_remap = resolve_selected_nids(index, selected_nids)

    mode = on_missing_nids.lower().strip()
    if mode not in {"error", "warn", "ignore"}:
        raise ValueError(f"unknown on_missing_nids mode: {on_missing_nids}")
    if missing_nids:
        message = _missing_nids_message(missing_nids, suggested_remap)
        if mode == "error":
            raise ValueError(message)
        if mode == "warn":
            sys.stderr.write(message + "\n")

    selected_pairs = [(nid, index.by_nid[nid]) for nid in resolved_nids]
    selected_pairs.sort(key=lambda pair: (pair[1].ord, pair[1].nid))

    trace_rows: List[Dict[str, Any]] = []
    prev_header_full_lines: Optional[List[str]] = None
    prev_context_for_prefix: Optional[List[str]] = None

    for nid_input, selected in selected_pairs:
        rule = _pick_rule(purpose_profile, selected.kind)
        rule_opts = _parse_rule_options(rule)
        plan = _extract_selection_plan(index, selected, rule, render_options=render_opts)
        compare_lines = prev_header_full_lines
        if header_dedup_mode == "prefix":
            compare_lines = prev_context_for_prefix
        shown_header_lines, shown_header_nids, header_omitted = _apply_header_dedup(
            mode=header_dedup_mode,
            current_lines=plan.header_lines_full,
            current_nids=plan.header_line_nids_full,
            previous_lines=compare_lines,
        )
        ancestors = []
        for anc in plan.included_ancestors:
            ancestors.append(
                {
                    "nid": anc.nid,
                    "kind": anc.kind,
                    "num": anc.num,
                    "display": index.display_name_by_nid.get(anc.nid),
                    "heading": anc.heading,
                    "text": anc.text,
                }
            )
        trace_rows.append(
            {
                "selected_nid": selected.nid,
                "nid_input": nid_input,
                "nid_resolved": selected.nid,
                "selected_kind": selected.kind,
                "selected_num": selected.num,
                "selected_display": index.display_name_by_nid.get(selected.nid),
                "selected_heading": selected.heading,
                "selected_text": selected.text,
                "rule": {
                    "when_kind": rule.get("when_kind"),
                    "include_ancestors_until_kind": rule_opts.include_ancestors_until_kind,
                    "include_ancestors_until_kinds": sorted(rule_opts.include_ancestors_until_kinds)
                    if rule_opts.include_ancestors_until_kinds
                    else [],
                    "include_headings": rule_opts.include_headings,
                    "include_chapeau_text": rule_opts.include_chapeau_text,
                    "include_descendants": rule_opts.include_descendants,
                    "include_descendants_of": rule_opts.include_descendants_of,
                    "include_descendants_kinds": sorted(rule_opts.include_descendants_kinds)
                    if rule_opts.include_descendants_kinds
                    else [],
                    "include_descendants_max_depth": rule_opts.include_descendants_max_depth,
                    "suppress_duplicate_headings": rule_opts.suppress_duplicate_headings,
                },
                "render_templates": {
                    "egov_merge_article_p1": render_opts.egov_merge_article_p1,
                },
                "included_ancestors": ancestors,
                "header_lines_full_before_dedup": plan.header_lines_full,
                "header_line_nids_full_before_dedup": plan.header_line_nids_full,
                "previous_header_lines_for_compare": compare_lines or [],
                "header_lines_after_dedup": shown_header_lines,
                "header_line_nids_after_dedup": shown_header_nids,
                "header_omitted": header_omitted,
                "item_lines": plan.item_lines,
                "item_line_nids": plan.item_line_nids,
            }
        )
        prev_header_full_lines = plan.header_lines_full
        prev_context_for_prefix = plan.header_lines_full + plan.item_lines

    return trace_rows
