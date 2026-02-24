from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import streamlit as st
import yaml

from qai_mock_ui.ir_model import DocIndex, build_doc_index
from qai_mock_ui.render import build_render_debug_trace, render_selected_nodes
from qai_mock_ui.txtconcat_loader import (
    load_regdoc_bundle_from_txtconcat,
)

DEFAULT_TXTCONCAT = Path("txtconcat_20260222-040007081.txt")
FALLBACK_IR = Path(
    "data/normalized/jp_egov_336M50000100002_20260501_507M60000100117/"
    "jp_egov_336M50000100002_20260501_507M60000100117.regdoc_ir.yaml"
)
FALLBACK_PROFILE = Path(
    "data/normalized/jp_egov_336M50000100002_20260501_507M60000100117/"
    "jp_egov_336M50000100002_20260501_507M60000100117.regdoc_profile.yaml"
)
FALLBACK_META = Path(
    "data/normalized/jp_egov_336M50000100002_20260501_507M60000100117/"
    "jp_egov_336M50000100002_20260501_507M60000100117.meta.yaml"
)
OUT_DIR = Path("out")


def _load_default_yaml_pair() -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any] | None]:
    regdoc_ir = yaml.safe_load(FALLBACK_IR.read_text(encoding="utf-8"))
    regdoc_profile = yaml.safe_load(FALLBACK_PROFILE.read_text(encoding="utf-8"))
    regdoc_meta: Dict[str, Any] | None = None
    if FALLBACK_META.exists():
        try:
            parsed_meta = yaml.safe_load(FALLBACK_META.read_text(encoding="utf-8"))
            if isinstance(parsed_meta, dict):
                regdoc_meta = parsed_meta
        except yaml.YAMLError:
            # meta は表示補助用途。fallback meta が壊れていても起動は継続する。
            regdoc_meta = None
    if not isinstance(regdoc_ir, dict) or not isinstance(regdoc_profile, dict):
        raise ValueError("既定YAMLの読み込みに失敗しました。")
    return regdoc_ir, regdoc_profile, regdoc_meta if isinstance(regdoc_meta, dict) else None


def _load_bundle_from_yaml_files(
    ir_path: Path,
    profile_path: Path,
    meta_path: Path | None,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any] | None]:
    regdoc_ir = yaml.safe_load(ir_path.read_text(encoding="utf-8"))
    regdoc_profile = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
    regdoc_meta: Dict[str, Any] | None = None
    if meta_path is not None and meta_path.exists():
        parsed = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
        if isinstance(parsed, dict):
            regdoc_meta = parsed
    if not isinstance(regdoc_ir, dict) or not isinstance(regdoc_profile, dict):
        raise ValueError("YAMLペアの読み込みに失敗しました。")
    return regdoc_ir, regdoc_profile, regdoc_meta


def _latest_out_bundle(doc_prefix: str) -> Tuple[Path, Path, Path] | None:
    candidates = sorted(OUT_DIR.glob(f"*/*{doc_prefix}*.regdoc_ir.yaml"))
    if not candidates:
        return None
    latest_ir = max(candidates, key=lambda p: p.parent.name)
    base = latest_ir.name.replace(".regdoc_ir.yaml", "")
    profile = latest_ir.with_name(f"{base}.regdoc_profile.yaml")
    meta = latest_ir.with_name(f"{base}.meta.yaml")
    if not profile.exists():
        return None
    return latest_ir, profile, meta


def _load_from_uploaded_or_local(
    uploaded,
    source_mode: str,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any] | None, str]:
    if source_mode == "eGov固定":
        ir, profile, meta = _load_default_yaml_pair()
        return ir, profile, meta, "fixed:eGov(data/normalized)"
    if source_mode == "海外固定(WHO LBM 3rd)":
        bundle = _latest_out_bundle("who_lbm_3rd")
        if bundle is None:
            raise ValueError("WHO LBM 3rd の out バンドルが見つかりません。")
        ir, profile, meta = _load_bundle_from_yaml_files(bundle[0], bundle[1], bundle[2])
        return ir, profile, meta, f"fixed:{bundle[0].parent.as_posix()}"
    if uploaded is not None:
        raw = uploaded.getvalue().decode("utf-8")
        temp = Path(".streamlit_tmp_txtconcat.txt")
        temp.write_text(raw, encoding="utf-8")
        try:
            ir, profile, meta = load_regdoc_bundle_from_txtconcat(temp)
            return ir, profile, meta, f"uploaded:{uploaded.name}"
        finally:
            if temp.exists():
                temp.unlink()
    if DEFAULT_TXTCONCAT.exists():
        ir, profile, meta = load_regdoc_bundle_from_txtconcat(DEFAULT_TXTCONCAT)
        return ir, profile, meta, str(DEFAULT_TXTCONCAT)
    ir, profile, meta = _load_default_yaml_pair()
    return ir, profile, meta, "fallback:data/normalized/*"


def _ensure_mock_nodes(regdoc_ir: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(regdoc_ir)
    index = build_doc_index(data)
    by_nid = index.by_nid
    display = data.setdefault("index", {}).setdefault("display_name_by_nid", {})

    table = by_nid.get("appdx_table1.tbl1")
    header = by_nid.get("appdx_table1.tbl1.tblh")
    row1 = by_nid.get("appdx_table1.tbl1.tblh.tblr1")
    if table is not None and header is not None and row1 is not None:
        table_raw = _find_raw_node(data["content"], table.nid)
        header_raw = _find_raw_node(data["content"], header.nid)
        if table_raw is not None and header_raw is not None:
            children = table_raw.setdefault("children", [])
            if not any(c.get("nid") == "appdx_table1.tbl1.note1" for c in children):
                children.append(
                    {
                        "nid": "appdx_table1.tbl1.note1",
                        "kind": "note",
                        "kind_raw": "note",
                        "num": None,
                        "ord": row1.ord + 2.0,
                        "heading": None,
                        "text": "※ 表の注記（デモ用）",
                        "role": "informative",
                        "normativity": None,
                        "tags": [],
                        "refs": [],
                        "source_spans": [],
                        "children": [],
                    }
                )
            h_children = header_raw.setdefault("children", [])
            row_specs = [
                ("appdx_table1.tbl1.tblh.tblr2", 1.0, "【2行目デモ】標識の補足説明 | 【2行目デモ】大きさの補足 | 【2行目デモ】設置箇所の補足"),
                ("appdx_table1.tbl1.tblh.tblr3", 2.0, "【3行目デモ】標識の補足説明 | 【3行目デモ】大きさの補足 | 【3行目デモ】設置箇所の補足"),
                ("appdx_table1.tbl1.tblh.tblr4", 3.0, "【4行目デモ】標識の補足説明 | 【4行目デモ】大きさの補足 | 【4行目デモ】設置箇所の補足"),
                ("appdx_table1.tbl1.tblh.tblr5", 4.0, "【5行目デモ】標識の補足説明 | 【5行目デモ】大きさの補足 | 【5行目デモ】設置箇所の補足"),
            ]
            existing = {c.get("nid") for c in h_children}
            for nid, ord_delta, text in row_specs:
                if nid in existing:
                    continue
                h_children.append(
                    {
                        "nid": nid,
                        "kind": "table_row",
                        "kind_raw": "table_row",
                        "num": None,
                        "ord": row1.ord + ord_delta,
                        "heading": None,
                        "text": text,
                        "role": "normative",
                        "normativity": None,
                        "tags": [],
                        "refs": [],
                        "source_spans": [],
                        "children": [],
                    }
                )
    display.setdefault("appdx_table1.tbl1.note1", "注記")
    display.setdefault("appdx_table1.tbl1.tblh.tblr2", "2行目")
    display.setdefault("appdx_table1.tbl1.tblh.tblr3", "3行目")
    display.setdefault("appdx_table1.tbl1.tblh.tblr4", "4行目")
    display.setdefault("appdx_table1.tbl1.tblh.tblr5", "5行目")
    return data


def _find_raw_node(node: Dict[str, Any], nid: str) -> Dict[str, Any] | None:
    if node.get("nid") == nid:
        return node
    for child in node.get("children") or []:
        found = _find_raw_node(child, nid)
        if found is not None:
            return found
    return None


def _purpose(profile: Dict[str, Any]) -> Dict[str, Any]:
    return deepcopy(profile.get("profiles", {}).get("dq_gmp_checklist", {}))


def _mock_purpose(original: Dict[str, Any]) -> Dict[str, Any]:
    patched = deepcopy(original)
    for rule in patched.get("context_display_policy", []):
        if rule.get("when_kind") == "subitem":
            rule["include_chapeau_text"] = False
        if rule.get("when_kind") == "table_row":
            rule["include_ancestors_until_kind"] = "table"
        if rule.get("when_kind") in {"paragraph", "item", "subitem", "statement"}:
            rule["force_article_p1_text"] = True
    return patched


def _node_options(index: DocIndex, selectable_kinds: List[str], query: str) -> List[Tuple[str, str]]:
    q = query.strip().lower()
    options: List[Tuple[str, str]] = []
    for node in index.by_nid.values():
        if node.kind not in selectable_kinds:
            continue
        text = " ".join((node.text or "").split())
        display = index.display_name_by_nid.get(node.nid) or node.nid
        if text:
            label = f"{display}：{text[:80]}"
        else:
            label = str(display)
        if q and q not in label.lower() and q not in node.nid.lower():
            continue
        options.append((node.nid, label))
    options.sort(key=lambda x: (index.by_nid[x[0]].ord, x[0]))
    return options


def _node_depth(index: DocIndex, nid: str) -> int:
    depth = 0
    node = index.by_nid.get(nid)
    while node is not None and node.parent_nid:
        parent = index.by_nid.get(node.parent_nid)
        if parent is None:
            break
        if parent.kind != "document" and parent.nid != "root":
            depth += 1
        node = parent
    return depth


def _single_line(text: str) -> str:
    return " ".join(text.strip().split())


def _row_index_label(index: DocIndex, nid: str) -> str:
    node = index.by_nid.get(nid)
    if node is None or node.kind != "table_row" or not node.parent_nid:
        return "行"
    parent = index.by_nid.get(node.parent_nid)
    if parent is None:
        return "行"
    rows = [child for child in parent.children if child.kind == "table_row"]
    rows.sort(key=lambda n: (n.ord, n.nid))
    for i, row in enumerate(rows, start=1):
        if row.nid == nid:
            return f"{i}行目"
    return "行"


def _human_node_label(index: DocIndex, nid: str) -> str:
    node = index.by_nid[nid]
    display = index.display_name_by_nid.get(nid)
    if display:
        return _single_line(str(display))
    if node.heading:
        return _single_line(str(node.heading))
    if node.kind == "table_row":
        return _row_index_label(index, nid)
    if node.kind == "table_header":
        return "表ヘッダ"
    if node.kind == "table":
        return "表"
    if node.kind == "paragraph" and node.num:
        return f"{node.num}項"
    if node.kind == "article" and node.num:
        return f"第{node.num}条"
    if node.kind == "item" and node.num:
        return str(node.num)
    if node.kind == "subitem" and node.num:
        return str(node.num)
    if node.kind == "appendix":
        return "別表"
    if node.text:
        return _single_line(str(node.text))[:24]
    return f"[{node.kind}]"


def _human_path(index: DocIndex, nid: str) -> str:
    if nid not in index.by_nid:
        return nid
    labels: List[str] = []
    for anc in index.ancestors_of(nid):
        if anc.kind == "document" or anc.nid == "root":
            continue
        labels.append(_human_node_label(index, anc.nid))
    labels.append(_human_node_label(index, nid))
    return " > ".join([v for v in labels if v]) or nid


def _table_row_compact_label(index: DocIndex, nid: str) -> str:
    node = index.by_nid.get(nid)
    if node is None or node.kind != "table_row":
        return _build_node_label(index, nid)
    row_cells = [c.strip() for c in _single_line(node.text or "").split("|")]
    parent = index.by_nid.get(node.parent_nid or "")
    header_cells: List[str] = []
    if parent and parent.kind == "table_header":
        header_cells = [c.strip() for c in _single_line(parent.text or "").split("|")]
    row_label = _row_index_label(index, nid)
    if len(row_cells) >= 2 and len(header_cells) >= 2:
        left = row_cells[0][:24]
        mid = row_cells[1][:18]
        return f"{row_label}：{header_cells[0]}={left} / {header_cells[1]}={mid}"
    if row_cells:
        return f"{row_label}：{row_cells[0][:46]}"
    return row_label


def _build_node_label(index: DocIndex, nid: str) -> str:
    node = index.by_nid[nid]
    if node.kind == "table_row":
        return _table_row_compact_label(index, nid)
    display = _human_node_label(index, nid)
    text = _single_line(node.text or "")
    if text:
        return f"{display}：{text[:110]}"
    return display


def _all_rows(index: DocIndex, selectable_kinds: List[str], query: str) -> List[Tuple[str, str, bool, int]]:
    q = query.strip().lower()
    rows: List[Tuple[str, str, bool, int]] = []
    selectable_set = set(selectable_kinds)
    nodes = sorted(index.by_nid.values(), key=lambda n: (n.ord, n.nid))
    for node in nodes:
        if node.kind == "document" or node.nid == "root":
            continue
        label = _build_node_label(index, node.nid)
        if q:
            searchable = f"{label} {node.nid} {node.kind}".lower()
            if q not in searchable:
                continue
        rows.append(
            (
                node.nid,
                label,
                node.kind in selectable_set,
                _node_depth(index, node.nid),
            )
        )
    return rows


def _law_overview_lines(regdoc_ir: Dict[str, Any], regdoc_meta: Dict[str, Any] | None) -> List[str]:
    lines: List[str] = []
    doc = regdoc_meta.get("doc", {}) if isinstance(regdoc_meta, dict) else {}
    identifiers = doc.get("identifiers", {}) if isinstance(doc, dict) else {}
    title = doc.get("title")
    doc_id = doc.get("id")
    egov_law_id = identifiers.get("e_gov_law_id") if isinstance(identifiers, dict) else None
    if title:
        lines.append(f"法令名: {title}")
    else:
        lines.append("法令名: (meta未取得)")
    if egov_law_id:
        lines.append(f"法令ID: {egov_law_id}")
    elif doc_id:
        lines.append(f"法令ID: {doc_id}")
    else:
        lines.append("法令ID: (meta未取得)")
    return lines


def _checkbox_key(nid: str) -> str:
    return f"candidate_{nid}"


def _sync_checkbox_defaults(option_ids: List[str], draft_selected_nids: Set[str], *, force: bool = False) -> None:
    for nid in option_ids:
        key = _checkbox_key(nid)
        if force or key not in st.session_state:
            st.session_state[key] = nid in draft_selected_nids


def _find_demo_subitem_siblings(index: DocIndex) -> List[str]:
    for node in sorted(index.by_nid.values(), key=lambda n: (n.ord, n.nid)):
        if node.kind != "item":
            continue
        subs = [c for c in node.children if c.kind == "subitem"]
        if len(subs) >= 2:
            return [subs[0].nid, subs[1].nid]
    return []


def _find_demo_table_rows(index: DocIndex, count: int) -> List[str]:
    rows = [n for n in index.by_nid.values() if n.kind == "table_row"]
    rows.sort(key=lambda n: (n.ord, n.nid))
    return [n.nid for n in rows[:count]]


def _apply_demo(index: DocIndex, name: str) -> List[str]:
    if name == "demo1":
        sub_pair = _find_demo_subitem_siblings(index)
        if sub_pair:
            return [sub_pair[0]]
        item_case = _find_demo_egov_item_case(index)
        return item_case[:1]
    if name == "demo2":
        sub_pair = _find_demo_subitem_siblings(index)
        if sub_pair:
            return sub_pair
        item_case = _find_demo_egov_item_case(index)
        return item_case[:2]
    if name == "demo3":
        return _find_demo_table_rows(index, 1)
    if name == "demo4":
        return _find_demo_table_rows(index, 2)
    return []


def _find_demo_egov_item_case(index: DocIndex) -> List[str]:
    for node in sorted(index.by_nid.values(), key=lambda n: (n.ord, n.nid)):
        if node.kind != "article":
            continue
        paras = [c for c in node.children if c.kind == "paragraph"]
        if not paras:
            continue
        p1 = paras[0]
        items = [c for c in p1.children if c.kind == "item"]
        if not items:
            continue
        nids = [p1.nid, items[0].nid]
        if len(items) > 1:
            nids.append(items[1].nid)
        return nids
    return []


def _find_demo_egov_paragraph_case(index: DocIndex) -> List[str]:
    for node in sorted(index.by_nid.values(), key=lambda n: (n.ord, n.nid)):
        if node.kind != "article":
            continue
        paras = [c for c in node.children if c.kind == "paragraph"]
        if len(paras) >= 3:
            return [paras[0].nid, paras[1].nid, paras[2].nid]
    return []


def _find_demo_non_article_case(index: DocIndex, selectable_kinds: List[str]) -> List[str]:
    if any(n.kind == "article" for n in index.by_nid.values()):
        return []
    selectable_set = set(selectable_kinds)
    hits: List[str] = []
    for node in sorted(index.by_nid.values(), key=lambda n: (n.ord, n.nid)):
        if node.kind in selectable_set:
            hits.append(node.nid)
        if len(hits) >= 3:
            break
    return hits


def _ts_compact() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S%f")[:-3]


def _render_preview(
    index: DocIndex,
    purpose: Dict[str, Any],
    selected_nids: List[str],
    *,
    header_dedup_mode: str,
    egov_merge_article_p1: bool = False,
) -> None:
    try:
        blocks = render_selected_nodes(
            index,
            purpose,
            selected_nids,
            header_dedup_mode=header_dedup_mode,
            render_options={"egov_merge_article_p1": egov_merge_article_p1},
        )
    except ValueError as exc:
        st.error(str(exc))
        return
    if not blocks:
        st.info("左から候補を選択してください。")
        return

    def _tooltip_path(nid: str) -> str:
        return _human_path(index, nid)

    def _line_with_help(line: str, source_nid: str, *, emphasized: bool = False) -> str:
        tooltip = escape(_tooltip_path(source_nid))
        safe_line = escape(line)
        icon = (
            f"<span title='{tooltip}' "
            "style='margin-left:6px;display:inline-flex;align-items:center;justify-content:center;"
            "width:14px;height:14px;border:1px solid #9ca3af;border-radius:50%;"
            "font-size:10px;line-height:1;color:#6b7280;vertical-align:middle;'>?</span>"
        )
        style = "font-weight:600;" if emphasized else ""
        return f"<div style='margin:2px 0;{style}'>{safe_line}{icon}</div>"

    def _table_row_checkbox_label(nid: str) -> str:
        node = index.by_nid.get(nid)
        if node is None:
            return nid
        cells = [c.strip() for c in _single_line(node.text or "").split("|")]
        if cells and cells[0]:
            return cells[0][:80]
        return _human_node_label(index, nid)

    def _add_help_to_table_right_cell(line: str, source_nid: str) -> str:
        raw = line.strip()
        if not (raw.startswith("|") and raw.endswith("|")):
            return line
        inner = raw[1:-1]
        cells = inner.split("|")
        if not cells:
            return line
        # markdown 区切り行は除外
        if all(set(c.strip()) <= {"-", ":"} and c.strip() for c in cells):
            return line
        tooltip = escape(_tooltip_path(source_nid))
        icon = (
            f"<span title='{tooltip}' "
            "style='margin-left:6px;display:inline-flex;align-items:center;justify-content:center;"
            "width:14px;height:14px;border:1px solid #9ca3af;border-radius:50%;"
            "font-size:10px;line-height:1;color:#6b7280;vertical-align:middle;'>?</span>"
        )
        cells[-1] = cells[-1].rstrip() + " " + icon
        return "| " + " | ".join(c.strip() for c in cells) + " |"

    def _add_checkbox_to_table_left_cell(line: str) -> str:
        raw = line.strip()
        if not (raw.startswith("|") and raw.endswith("|")):
            return line
        inner = raw[1:-1]
        cells = inner.split("|")
        if not cells:
            return line
        if all(set(c.strip()) <= {"-", ":"} and c.strip() for c in cells):
            return line
        checkbox_html = (
            "<input type='checkbox' "
            "style='vertical-align:middle;margin-right:6px;transform:scale(1.0);' />"
        )
        cells[0] = checkbox_html + cells[0].lstrip()
        return "| " + " | ".join(c.strip() for c in cells) + " |"

    def _render_lines_with_markdown(
        lines: List[str],
        nids: List[str],
        *,
        emphasized: bool = False,
    ) -> None:
        table_buf: List[str] = []
        for line, nid in zip(lines, nids):
            if line.lstrip().startswith("|"):
                table_buf.append(line)
                continue
            if table_buf:
                st.markdown("\n".join(table_buf))
                table_buf = []
            st.markdown(_line_with_help(line, nid, emphasized=emphasized), unsafe_allow_html=True)
        if table_buf:
            st.markdown("\n".join(table_buf))

    def _render_header_lines(lines: List[str], nids: List[str]) -> None:
        if not lines:
            return
        st.markdown("<div style='background:#f4f4f4;padding:8px;border-radius:6px;margin:4px 0;'>", unsafe_allow_html=True)
        for line, nid in zip(lines, nids):
            st.markdown(_line_with_help(line, nid, emphasized=True), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    table_markdown_buffer: List[str] = []
    for block in blocks:
        block_header_lines = list(block.header_lines)
        block_header_nids = list(block.header_line_nids)
        block_item_lines = list(block.item_lines)
        block_item_nids = list(block.item_line_nids)

        # non-table block が来たら、溜めていた table markdown を確定描画する
        if block.kind != "table_row" and table_markdown_buffer:
            st.markdown("\n".join(table_markdown_buffer), unsafe_allow_html=True)
            table_markdown_buffer = []

        if block_header_lines and not block.header_omitted:
            _render_header_lines(block_header_lines, block_header_nids)
        checkbox_key = f"checksheet_item_{block.nid}"
        if block.kind == "table_row":
            for line, nid in zip(block_item_lines, block_item_nids):
                if line.lstrip().startswith("|"):
                    line_work = line
                    if nid == block.nid:
                        line_work = _add_checkbox_to_table_left_cell(line_work)
                    table_markdown_buffer.append(_add_help_to_table_right_cell(line_work, nid))
                else:
                    table_markdown_buffer.append(line)
        else:
            if checkbox_key not in st.session_state:
                st.session_state[checkbox_key] = False
            c1, c2 = st.columns([1, 30])
            with c1:
                st.checkbox(
                    f"{block.nid}",
                    key=checkbox_key,
                    label_visibility="collapsed",
                )
            with c2:
                _render_lines_with_markdown(block_item_lines, block_item_nids)

    if table_markdown_buffer:
        st.markdown("\n".join(table_markdown_buffer), unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(page_title="GMPチェックシート生成UI（モック）", layout="wide")
    st.title("GMPチェックシート生成UI（モック）")

    source_mode = st.radio(
        "データソース切替",
        ["自動(アップロード/txtconcat/fallback)", "eGov固定", "海外固定(WHO LBM 3rd)"],
        horizontal=True,
    )
    uploaded = st.file_uploader("txtconcat (*.txt) を選択", type=["txt"])
    try:
        regdoc_ir, regdoc_profile, regdoc_meta, source_label = _load_from_uploaded_or_local(uploaded, source_mode)
    except Exception as exc:
        st.error(f"YAML抽出/パースに失敗しました: {exc}")
        return

    regdoc_ir = _ensure_mock_nodes(regdoc_ir)
    index = build_doc_index(regdoc_ir)
    is_egov_doc = str(regdoc_ir.get("doc_id") or "").startswith("jp_egov_")
    base_purpose = _purpose(regdoc_profile)
    purpose_mode = st.radio("プロファイル切替", ["オリジナル設定", "モック用設定"], horizontal=True)
    current = base_purpose if purpose_mode == "オリジナル設定" else _mock_purpose(base_purpose)

    if "editable_purpose_yaml" not in st.session_state:
        st.session_state["editable_purpose_yaml"] = yaml.safe_dump(
            current, allow_unicode=True, sort_keys=False
        )
    if st.button("現在設定を編集欄に反映"):
        st.session_state["editable_purpose_yaml"] = yaml.safe_dump(
            current, allow_unicode=True, sort_keys=False
        )

    edited = st.text_area(
        "selectable_kinds / context_display_policy 編集（YAML）",
        key="editable_purpose_yaml",
        height=260,
    )
    if st.button("YAML編集を適用"):
        try:
            loaded = yaml.safe_load(edited)
            if not isinstance(loaded, dict):
                raise ValueError("YAMLのトップレベルは辞書である必要があります。")
            current = loaded
            st.success("編集内容を適用しました。")
        except Exception as exc:
            st.error(f"YAML適用に失敗しました: {exc}")

    selectable_kinds = [str(v) for v in current.get("selectable_kinds", []) if isinstance(v, str)]
    dedup_mode_label = st.radio(
        "文脈省略モード",
        ["完全一致省略（現行）", "ord差分省略（新）"],
        horizontal=True,
    )
    dedup_mode = "exact" if dedup_mode_label.startswith("完全一致") else "prefix"
    egov_merge_article_p1 = st.checkbox(
        "eGov専用: 第1項(1項)を条名と統合表示（□ 第一条 本文）",
        value=False,
        disabled=not is_egov_doc,
        help="通常はOFF（ノーマル表示）。ONにすると eGov 文書で第1項のみ条名と1行統合表示します。",
    )
    if "selected_nids" not in st.session_state:
        st.session_state["selected_nids"] = []
    if "draft_selected_nids" not in st.session_state:
        st.session_state["draft_selected_nids"] = list(st.session_state["selected_nids"])

    left, right = st.columns(2)
    with left:
        st.subheader("選択パネル")
        st.caption(f"データソース: `{source_label}`")
        st.caption("法令表示（参照のみ）")
        with st.container(height=110, border=True):
            for line in _law_overview_lines(regdoc_ir, regdoc_meta):
                st.write(line)

        query = st.text_input("検索（nid/表示ラベル/本文）", "")
        rows = _all_rows(index, selectable_kinds, query)
        selectable_row_ids = [nid for nid, _, selectable, _ in rows if selectable]
        label_by_id = {nid: label for nid, label, _, _ in rows}

        demo_cols = st.columns(5)
        if demo_cols[0].button("デモ1：ロだけ"):
            demo_nids = _apply_demo(index, "demo1")
            st.session_state["draft_selected_nids"] = demo_nids
            st.session_state["selected_nids"] = demo_nids
            _sync_checkbox_defaults(selectable_row_ids, set(demo_nids), force=True)
        if demo_cols[1].button("デモ2：ロ＋ハ"):
            demo_nids = _apply_demo(index, "demo2")
            st.session_state["draft_selected_nids"] = demo_nids
            st.session_state["selected_nids"] = demo_nids
            _sync_checkbox_defaults(selectable_row_ids, set(demo_nids), force=True)
        if demo_cols[4].button("デモ5：3ケース確認"):
            if source_mode == "海外固定(WHO LBM 3rd)":
                demo_nids = _find_demo_non_article_case(index, selectable_kinds)
            else:
                demo_nids = _find_demo_egov_item_case(index)
                if not demo_nids:
                    demo_nids = _find_demo_egov_paragraph_case(index)
            if not demo_nids:
                st.warning("このデータセットでは該当デモを組めません。")
            else:
                st.session_state["draft_selected_nids"] = demo_nids
                st.session_state["selected_nids"] = demo_nids
                _sync_checkbox_defaults(selectable_row_ids, set(demo_nids), force=True)

        case_cols = st.columns(3)
        if case_cols[0].button("Case A: 条→1項→号"):
            demo_nids = _find_demo_egov_item_case(index)
            if not demo_nids:
                st.warning("このデータセットに Article/Paragraph/Item ケースがありません。")
            else:
                st.session_state["draft_selected_nids"] = demo_nids
                st.session_state["selected_nids"] = demo_nids
                _sync_checkbox_defaults(selectable_row_ids, set(demo_nids), force=True)
        if case_cols[1].button("Case B: 条→1項/2項/3項"):
            demo_nids = _find_demo_egov_paragraph_case(index)
            if not demo_nids:
                st.warning("このデータセットに複数Paragraphケースがありません。")
            else:
                st.session_state["draft_selected_nids"] = demo_nids
                st.session_state["selected_nids"] = demo_nids
                _sync_checkbox_defaults(selectable_row_ids, set(demo_nids), force=True)
        if case_cols[2].button("Case C: 海外(Articleなし)"):
            demo_nids = _find_demo_non_article_case(index, selectable_kinds)
            if not demo_nids:
                st.warning("このデータセットは Article を持つため海外ケースになりません。")
            else:
                st.session_state["draft_selected_nids"] = demo_nids
                st.session_state["selected_nids"] = demo_nids
                _sync_checkbox_defaults(selectable_row_ids, set(demo_nids), force=True)
        if demo_cols[2].button("デモ3：表1行"):
            demo_nids = _apply_demo(index, "demo3")
            st.session_state["draft_selected_nids"] = demo_nids
            st.session_state["selected_nids"] = demo_nids
            _sync_checkbox_defaults(selectable_row_ids, set(demo_nids), force=True)
        if demo_cols[3].button("デモ4：表2行"):
            demo_nids = _apply_demo(index, "demo4")
            st.session_state["draft_selected_nids"] = demo_nids
            st.session_state["selected_nids"] = demo_nids
            _sync_checkbox_defaults(selectable_row_ids, set(demo_nids), force=True)

        st.caption("ord順の全ノードを表示中。選択可能ノードのみチェックできます。")
        draft_set = set(st.session_state.get("draft_selected_nids", []))
        _sync_checkbox_defaults(selectable_row_ids, draft_set)

        with st.form("candidate_form"):
            with st.container(height=560, border=True):
                for nid, label, selectable, depth in rows:
                    indent = "&nbsp;" * (depth * 4)
                    if selectable:
                        checkbox_label = f"{'  ' * depth}{label}"
                        st.checkbox(
                            checkbox_label,
                            key=_checkbox_key(nid),
                            help=_human_path(index, nid),
                        )
                    else:
                        kind = index.by_nid[nid].kind
                        st.markdown(
                            f"{indent}<span style='color:#6b7280;'>[{kind}] {label}</span>",
                            unsafe_allow_html=True,
                        )
            apply_selection = st.form_submit_button("選択を確定")

        if apply_selection:
            selected_visible = {
                nid for nid in selectable_row_ids if bool(st.session_state.get(_checkbox_key(nid), False))
            }
            still_selected = draft_set - set(selectable_row_ids)
            merged = sorted(selected_visible | still_selected, key=lambda x: (index.by_nid[x].ord, x))
            st.session_state["draft_selected_nids"] = merged
            st.session_state["selected_nids"] = merged
            st.success(f"{len(merged)}件を確定しました。")

        st.caption(f"確定済み: {len(st.session_state.get('selected_nids', []))}件")

    with right:
        st.subheader("チェックシートプレビュー")
        _render_preview(
            index,
            current,
            st.session_state.get("selected_nids", []),
            header_dedup_mode=dedup_mode,
            egov_merge_article_p1=egov_merge_article_p1,
        )

    st.markdown("---")
    st.subheader("設定（YAML）確認")
    st.markdown("`selectable_kinds`")
    st.code(yaml.safe_dump({"selectable_kinds": selectable_kinds}, allow_unicode=True, sort_keys=False), "yaml")
    st.markdown("`context_display_policy`")
    st.code(
        yaml.safe_dump(
            {"context_display_policy": current.get("context_display_policy", [])},
            allow_unicode=True,
            sort_keys=False,
        ),
        "yaml",
    )
    st.markdown("`header_dedup_mode`")
    st.code(dedup_mode, "text")

    with st.expander("デバッグ: 抽出/省略の中間トレース", expanded=False):
        selected_for_debug = st.session_state.get("selected_nids", [])
        try:
            trace_rows = build_render_debug_trace(
                index=index,
                purpose_profile=current,
                selected_nids=selected_for_debug,
                header_dedup_mode=dedup_mode,
                render_options={"egov_merge_article_p1": egov_merge_article_p1},
            )
        except ValueError as exc:
            st.error(str(exc))
            return
        debug_payload = {
            "meta": {
                "generated_at": _ts_compact(),
                "source_label": source_label,
                "purpose_mode": purpose_mode,
                "header_dedup_mode": dedup_mode,
                "selected_nids": selected_for_debug,
            },
            "trace_rows": trace_rows,
        }
        st.caption("表示の根拠となる中間データ（祖先抽出・省略前後・最終行）を表示します。")
        st.code(yaml.safe_dump(debug_payload, allow_unicode=True, sort_keys=False), "yaml")
        if st.button("デバッグログを out/ に保存"):
            try:
                OUT_DIR.mkdir(parents=True, exist_ok=True)
                out_path = OUT_DIR / f"{_ts_compact()}_mock_ui_debug_trace.yaml"
                out_path.write_text(
                    yaml.safe_dump(debug_payload, allow_unicode=True, sort_keys=False),
                    encoding="utf-8",
                )
                st.success(f"保存しました: {out_path}")
            except Exception as exc:
                st.error(f"保存に失敗しました: {exc}")


if __name__ == "__main__":
    main()
