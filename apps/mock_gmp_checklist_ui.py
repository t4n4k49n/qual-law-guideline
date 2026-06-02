from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from html import escape
from pathlib import Path
import re
from typing import Any, Dict, List, Set, Tuple

import streamlit as st
import streamlit.components.v1 as components
import yaml

from qai_mock_ui.ir_model import DocIndex, build_doc_index
from qai_mock_ui.candidate_visibility import build_candidate_visibility_map
from qai_mock_ui.render import build_render_debug_trace, render_selected_nodes

NORMALIZED_ROOT = Path("data/normalized")
DISPLAY_EXAMPLES_CONFIG = Path("data/mock_ui/display_examples.yaml")
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
DEFAULT_NORMALIZED_FOLDER = "jp_egov_336M50000100002_20260501_507M60000100117"
SOURCE_MODE_FOLDER = "フォルダ選択"
SOURCE_MODE_YAML_FOLDER = "4yaml内包フォルダ指定"


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
        try:
            parsed = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
            if isinstance(parsed, dict):
                regdoc_meta = parsed
        except yaml.YAMLError:
            # meta は表示補助用途。壊れていてもUI利用は継続する。
            regdoc_meta = None
    if not isinstance(regdoc_ir, dict) or not isinstance(regdoc_profile, dict):
        raise ValueError("YAMLペアの読み込みに失敗しました。")
    return regdoc_ir, regdoc_profile, regdoc_meta


def _meta_title(meta_path: Path | None) -> str | None:
    if meta_path is None or not meta_path.exists():
        return None
    raw = meta_path.read_text(encoding="utf-8")
    try:
        parsed = yaml.safe_load(raw)
    except Exception:
        # 一部の meta.yaml は generation.inputs.path の未クォート '%' で壊れる。
        # doc.title だけは行ベースで回収してUI表示に使う。
        m = re.search(r"^\s{2}title:\s*(.+)\s*$", raw, flags=re.MULTILINE)
        if not m:
            return None
        value = m.group(1).strip()
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        return value or None
    if not isinstance(parsed, dict):
        return None
    doc = parsed.get("doc")
    if not isinstance(doc, dict):
        return None
    title = doc.get("title")
    return str(title).strip() if isinstance(title, str) and title.strip() else None


def _extract_source_urls(meta: Dict[str, Any] | None) -> List[str]:
    if not isinstance(meta, dict):
        return []
    doc = meta.get("doc")
    if not isinstance(doc, dict):
        return []
    sources = doc.get("sources")
    if not isinstance(sources, list):
        return []
    urls: List[str] = []
    seen: Set[str] = set()
    for source in sources:
        if not isinstance(source, dict):
            continue
        raw_url = source.get("url")
        if not isinstance(raw_url, str):
            continue
        url = raw_url.strip()
        if not url or url in seen:
            continue
        urls.append(url)
        seen.add(url)
    return urls


def _meta_source_urls(meta_path: Path | None) -> List[str]:
    if meta_path is None or not meta_path.exists():
        return []
    raw = meta_path.read_text(encoding="utf-8")
    try:
        parsed = yaml.safe_load(raw)
    except Exception:
        urls: List[str] = []
        seen: Set[str] = set()
        for match in re.finditer(r"^\s*(?:-\s*)?url:\s*(.+)\s*$", raw, flags=re.MULTILINE):
            url = match.group(1).strip().strip("\"'")
            if url and url not in seen:
                urls.append(url)
                seen.add(url)
        return urls
    if not isinstance(parsed, dict):
        return []
    return _extract_source_urls(parsed)


def _source_url_display(url: str) -> str:
    max_chars = 96
    if len(url) <= max_chars:
        return url
    return f"{url[:72]}...{url[-21:]}"


def _discover_normalized_bundles() -> List[Tuple[str, Path, Path, Path | None, str | None]]:
    if not NORMALIZED_ROOT.exists():
        return []
    bundles: List[Tuple[str, Path, Path, Path | None, str | None]] = []
    for child in sorted(NORMALIZED_ROOT.iterdir(), key=lambda p: p.name):
        if not child.is_dir():
            continue
        if child.name.startswith("ARCHIVE_"):
            continue
        ir_files = sorted(child.glob("*.regdoc_ir.yaml"))
        profile_files = sorted(child.glob("*.regdoc_profile.yaml"))
        meta_files = sorted(child.glob("*.meta.yaml"))
        if not ir_files or not profile_files:
            continue
        ir_path = ir_files[0]
        profile_path = profile_files[0]
        meta_path = meta_files[0] if meta_files else None
        bundles.append((child.name, ir_path, profile_path, meta_path, _meta_title(meta_path)))
    return bundles


def _discover_out_bundles() -> List[Tuple[str, Path, Path, Path | None, str | None]]:
    if not OUT_DIR.exists():
        return []
    bundles: List[Tuple[str, Path, Path, Path | None, str | None]] = []
    for child in sorted(OUT_DIR.iterdir(), key=lambda p: p.name):
        if not child.is_dir():
            continue
        ir_files = sorted(child.glob("*.regdoc_ir.yaml"))
        profile_files = sorted(child.glob("*.regdoc_profile.yaml"))
        meta_files = sorted(child.glob("*.meta.yaml"))
        if not ir_files or not profile_files:
            continue
        ir_path = ir_files[0]
        profile_path = profile_files[0]
        meta_path = meta_files[0] if meta_files else None
        bundles.append((f"out/{child.name}", ir_path, profile_path, meta_path, _meta_title(meta_path)))
    return bundles


def _discover_selectable_bundles() -> List[Tuple[str, Path, Path, Path | None, str | None]]:
    merged: List[Tuple[str, Path, Path, Path | None, str | None]] = []
    merged.extend(_discover_normalized_bundles())
    merged.extend(_discover_out_bundles())
    return merged


def _single_yaml_bundle_in_folder(folder: Path) -> Tuple[Path, Path, Path, Path]:
    if not folder.exists() or not folder.is_dir():
        raise ValueError("フォルダが見つかりません。")

    suffixes = {
        ".regdoc_ir.yaml": "IR",
        ".parser_profile.yaml": "parser profile",
        ".regdoc_profile.yaml": "regdoc profile",
        ".meta.yaml": "meta",
    }
    matches: Dict[str, List[Path]] = {suffix: [] for suffix in suffixes}
    for child in sorted(folder.iterdir(), key=lambda p: p.name):
        if not child.is_file():
            continue
        for suffix in suffixes:
            if child.name.endswith(suffix):
                matches[suffix].append(child)
                break

    missing = [label for suffix, label in suffixes.items() if not matches[suffix]]
    if missing:
        raise ValueError(f"4yamlセットが揃っていません: {', '.join(missing)} がありません。")

    duplicated = [label for suffix, label in suffixes.items() if len(matches[suffix]) > 1]
    if duplicated:
        raise ValueError(f"4yamlセットが複数見つかりました: {', '.join(duplicated)} が複数あります。")

    prefixes = {
        suffix: matches[suffix][0].name[: -len(suffix)]
        for suffix in suffixes
    }
    if len(set(prefixes.values())) != 1:
        raise ValueError("4yamlのファイル名prefixが一致していません。")

    return (
        matches[".regdoc_ir.yaml"][0],
        matches[".parser_profile.yaml"][0],
        matches[".regdoc_profile.yaml"][0],
        matches[".meta.yaml"][0],
    )


def _pick_directory_with_dialog(initial_dir: str | None = None) -> str | None:
    try:
        import tkinter as tk
        from tkinter import filedialog
    except Exception as exc:
        raise RuntimeError(f"フォルダ選択ダイアログを開けません: {exc}") from exc

    root = tk.Tk()
    root.withdraw()
    try:
        root.attributes("-topmost", True)
        selected = filedialog.askdirectory(
            parent=root,
            initialdir=initial_dir or str(Path.cwd()),
            title="4yaml内包フォルダを選択",
            mustexist=True,
        )
    finally:
        root.destroy()
    selected = selected.strip()
    return selected or None


def _restore_source_selection_state(mode: str, yaml_folder_path: str | None) -> None:
    st.session_state["source_mode_key"] = mode
    st.session_state["confirmed_source_mode_key"] = mode
    st.session_state["source_mode_radio_nonce"] = (
        int(st.session_state.get("source_mode_radio_nonce", 0)) + 1
    )
    if yaml_folder_path:
        st.session_state["yaml_folder_source_selected_path"] = yaml_folder_path
    else:
        st.session_state.pop("yaml_folder_source_selected_path", None)


def _validate_and_store_yaml_folder_selection(
    selected_path: str | None,
    previous_mode: str,
    previous_yaml_folder_path: str | None,
) -> bool:
    if not selected_path:
        _restore_source_selection_state(previous_mode, previous_yaml_folder_path)
        st.session_state["yaml_folder_source_warning"] = (
            "4yaml内包フォルダが選択されなかったため、法令選択は変更していません。"
        )
        return False
    try:
        _single_yaml_bundle_in_folder(Path(selected_path))
    except Exception as exc:
        _restore_source_selection_state(previous_mode, previous_yaml_folder_path)
        st.session_state["yaml_folder_source_warning"] = (
            f"4yaml内包フォルダが上手く選択されませんでした: {exc}"
        )
        return False
    st.session_state["source_mode_key"] = SOURCE_MODE_YAML_FOLDER
    st.session_state["confirmed_source_mode_key"] = SOURCE_MODE_YAML_FOLDER
    st.session_state["yaml_folder_source_selected_path"] = selected_path
    st.session_state["source_mode_radio_nonce"] = (
        int(st.session_state.get("source_mode_radio_nonce", 0)) + 1
    )
    return True


def _load_display_examples() -> List[Dict[str, Any]]:
    if not DISPLAY_EXAMPLES_CONFIG.exists():
        return []
    parsed = yaml.safe_load(DISPLAY_EXAMPLES_CONFIG.read_text(encoding="utf-8"))
    if not isinstance(parsed, dict):
        return []
    raw_examples = parsed.get("examples")
    if not isinstance(raw_examples, list):
        return []
    examples: List[Dict[str, Any]] = []
    for raw in raw_examples:
        if not isinstance(raw, dict):
            continue
        ex_id = str(raw.get("id", "")).strip()
        if not ex_id:
            continue
        examples.append(raw)
    return examples


def _example_tooltip(
    example: Dict[str, Any],
    bundles: List[Tuple[str, Path, Path, Path | None, str | None]],
) -> str:
    source_mode = str(example.get("source_mode", ""))
    profile = str(example.get("profile", {}).get("mode", "original"))
    selection_nids = example.get("selection_nids", [])
    selection_desc = f"{len(selection_nids)}件" if isinstance(selection_nids, list) else "未設定"
    law_name = "（未設定）"
    if source_mode in {"data/normalized選択", "フォルダ選択"}:
        folder = str(example.get("law_folder", ""))
        for bundle in bundles:
            if bundle[0] == folder:
                law_name = bundle[4] or folder
                break
        if law_name == "（未設定）":
            law_name = folder or "（未設定）"
    return f"法令名: {law_name} | プロファイル: {profile} | 選択: {selection_desc}"

def _load_from_selected_source(
    source_mode: str,
    selected_normalized_folder: str | None = None,
    selected_yaml_folder_path: str | None = None,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any] | None, str]:
    if source_mode in {"data/normalized選択", SOURCE_MODE_FOLDER}:
        bundles = _discover_selectable_bundles()
        if not bundles:
            raise ValueError("選択可能なフォルダ（data/normalized, out/*）が見つかりません。")
        selected = selected_normalized_folder or bundles[0][0]
        matched = next((b for b in bundles if b[0] == selected), None)
        if matched is None:
            raise ValueError(f"選択フォルダが見つかりません: {selected}")
        ir, profile, meta = _load_bundle_from_yaml_files(matched[1], matched[2], matched[3])
        return ir, profile, meta, f"normalized:{matched[0]}"
    if source_mode == SOURCE_MODE_YAML_FOLDER and selected_yaml_folder_path:
        ir_path, _parser_path, profile_path, meta_path = _single_yaml_bundle_in_folder(
            Path(selected_yaml_folder_path)
        )
        ir, profile, meta = _load_bundle_from_yaml_files(ir_path, profile_path, meta_path)
        return ir, profile, meta, f"yaml-folder:{Path(selected_yaml_folder_path).as_posix()}"
    ir, profile, meta = _load_default_yaml_pair()
    return ir, profile, meta, "fallback:data/normalized/*"


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


def _split_table_cells(text: str) -> List[str]:
    line = _single_line(text)
    if not line:
        return []
    cells = [part.strip() for part in re.split(r"\s*[|｜]\s*", line)]
    return [cell for cell in cells if cell]


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
    row_cells = _split_table_cells(node.text or "")
    parent = index.by_nid.get(node.parent_nid or "")
    header_cells: List[str] = []
    if parent and parent.kind == "table_header":
        header_cells = _split_table_cells(parent.text or "")
    row_label = _row_index_label(index, nid)
    if len(row_cells) >= 2 and len(header_cells) >= 2:
        pairs: List[str] = []
        for header, value in zip(header_cells, row_cells):
            pairs.append(f"{header}={value}")
        return f"{row_label}：{' | '.join(pairs)}"
    if row_cells:
        return f"{row_label}：{' | '.join(row_cells)}"
    return row_label


def _build_node_label(index: DocIndex, nid: str) -> str:
    node = index.by_nid[nid]
    if node.kind == "table_row":
        return _table_row_compact_label(index, nid)
    display = _human_node_label(index, nid)
    text = _single_line(node.text or "")
    if text:
        return f"{display}：{text}"
    return display


def _all_rows(
    index: DocIndex,
    selectable_kinds: List[str],
    query: str,
    visible_by_nid: Dict[str, bool] | None = None,
) -> List[Tuple[str, str, bool, int]]:
    q = query.strip().lower()
    rows: List[Tuple[str, str, bool, int]] = []
    selectable_set = set(selectable_kinds)
    nodes = sorted(index.by_nid.values(), key=lambda n: (n.ord, n.nid))
    for node in nodes:
        if node.kind == "document" or node.nid == "root":
            continue
        if visible_by_nid is not None and not visible_by_nid.get(node.nid, True):
            continue
        label = _build_node_label(index, node.nid)
        if q:
            searchable_parts = [label, node.nid, node.kind, _single_line(node.text or "")]
            if node.kind == "table_row":
                parent = index.by_nid.get(node.parent_nid or "")
                if parent is not None:
                    searchable_parts.append(_single_line(parent.text or ""))
                searchable_parts.append(_single_line(node.text or "").replace("|", " ").replace("｜", " "))
            searchable = " ".join([part for part in searchable_parts if part]).lower()
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


def _nid_copy_icon_html(nid: str) -> str:
    title = escape(f"nid: {nid}", quote=True)
    data_nid = escape(nid, quote=True)
    return (
        "<span "
        "role='button' "
        "tabindex='0' "
        "class='candidate-icon candidate-icon-btn' "
        f"data-nid='{data_nid}' "
        f"title='{title}' "
        ">🆔</span>"
    )


def _inject_nid_copy_hook() -> None:
    components.html(
        """
        <script>
        (function () {
          const w = window.parent;
          if (!w || !w.document || w.__nidCopyHookInstalled) return;
          w.__nidCopyHookInstalled = true;
          w.document.addEventListener(
            "click",
            async function (event) {
              const target = event.target;
              if (!target) return;
              const btn = target.closest(".candidate-icon-btn[data-nid]");
              if (!btn) return;
              event.preventDefault();
              event.stopPropagation();
              const nid = btn.getAttribute("data-nid") || "";
              if (!nid) return;
              try {
                await w.navigator.clipboard.writeText(nid);
                return;
              } catch (e) {}
              try {
                const ta = w.document.createElement("textarea");
                ta.value = nid;
                ta.style.position = "fixed";
                ta.style.opacity = "0";
                ta.style.pointerEvents = "none";
                w.document.body.appendChild(ta);
                ta.focus();
                ta.select();
                w.document.execCommand("copy");
                w.document.body.removeChild(ta);
              } catch (e) {}
            },
            true
          );
        })();
        </script>
        """,
        height=0,
        width=0,
    )


def _sync_checkbox_defaults(option_ids: List[str], draft_selected_nids: Set[str], *, force: bool = False) -> None:
    for nid in option_ids:
        key = _checkbox_key(nid)
        if force or key not in st.session_state:
            st.session_state[key] = nid in draft_selected_nids


def _clear_selection_state() -> None:
    st.session_state["selected_nids"] = []
    st.session_state["draft_selected_nids"] = []
    for key in list(st.session_state.keys()):
        if key.startswith("candidate_"):
            del st.session_state[key]


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

    def _normalize_table_row_markdown(line: str) -> str | None:
        raw = _single_line(line.replace("｜", "|"))
        if "|" not in raw:
            return None
        if raw.startswith("|") and raw.endswith("|"):
            return raw
        parts = [part.strip() for part in raw.split("|")]
        cells = [part for part in parts if part]
        if len(cells) < 2:
            return None
        return "| " + " | ".join(cells) + " |"

    def _is_md_separator_row(line: str) -> bool:
        raw = line.strip()
        if not (raw.startswith("|") and raw.endswith("|")):
            return False
        cells = [c.strip() for c in raw[1:-1].split("|")]
        if not cells:
            return False
        return all(cell and set(cell) <= {"-", ":"} for cell in cells)

    def _make_table_header_for_row(row_line: str) -> tuple[str, str] | None:
        raw = row_line.strip()
        if not (raw.startswith("|") and raw.endswith("|")):
            return None
        cells = [c.strip() for c in raw[1:-1].split("|")]
        cols = max(1, len(cells))
        # 法令原文にヘッダ行がない table_row 群でも Markdown 表として成立させるため、
        # 最小限のダミーヘッダ（列1..N）を補完する。
        header = "| " + " | ".join([f"列{i}" for i in range(1, cols + 1)]) + " |"
        sep = "| " + " | ".join(["---"] * cols) + " |"
        return header, sep

    def _table_group_key(nid: str) -> str:
        node = index.by_nid.get(nid)
        if node is None:
            return nid
        cur = node
        while cur.parent_nid:
            parent = index.by_nid.get(cur.parent_nid)
            if parent is None:
                break
            if parent.kind in {"table", "table_header"}:
                return parent.nid
            cur = parent
        return node.parent_nid or nid

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
    table_has_separator = False
    active_table_group_key: str | None = None
    active_table_header_line: str | None = None
    for block in blocks:
        block_header_lines = list(block.header_lines)
        block_header_nids = list(block.header_line_nids)
        block_item_lines = list(block.item_lines)
        block_item_nids = list(block.item_line_nids)

        if block.kind == "table_row" and block_header_lines:
            filtered_header_lines: List[str] = []
            filtered_header_nids: List[str] = []
            for line, nid in zip(block_header_lines, block_header_nids):
                node = index.by_nid.get(nid)
                if node is not None and node.kind == "table_header":
                    continue
                filtered_header_lines.append(line)
                filtered_header_nids.append(nid)
            block_header_lines = filtered_header_lines
            block_header_nids = filtered_header_nids

        block_group_key: str | None = None
        if block.kind == "table_row":
            block_group_key = _table_group_key(block.nid)
            if active_table_group_key is not None and block_group_key != active_table_group_key:
                if table_markdown_buffer:
                    st.markdown("\n".join(table_markdown_buffer), unsafe_allow_html=True)
                    # 表グループ切替時は 1 行空けて、隣接 table が 1 つに連結される見え方を防ぐ。
                    st.markdown("")  # table と table の見切り回避
                table_markdown_buffer = []
                table_has_separator = False
                active_table_header_line = None
            if active_table_group_key is None or block_group_key != active_table_group_key:
                active_table_group_key = block_group_key
        elif table_markdown_buffer:
            # non-table block が来たら、溜めていた table markdown を確定描画する
            st.markdown("\n".join(table_markdown_buffer), unsafe_allow_html=True)
            table_markdown_buffer = []
            table_has_separator = False
            active_table_group_key = None
            active_table_header_line = None

        if block_header_lines and not block.header_omitted:
            _render_header_lines(block_header_lines, block_header_nids)
        checkbox_key = f"checksheet_item_{block.nid}"
        if block.kind == "table_row":
            normalized_rows: List[tuple[str, str]] = []
            for line, nid in zip(block_item_lines, block_item_nids):
                row_line = _normalize_table_row_markdown(line)
                if row_line is None:
                    if table_markdown_buffer:
                        st.markdown("\n".join(table_markdown_buffer), unsafe_allow_html=True)
                        table_markdown_buffer = []
                        table_has_separator = False
                        active_table_group_key = None
                        active_table_header_line = None
                    st.markdown(_line_with_help(line, nid), unsafe_allow_html=True)
                    continue
                normalized_rows.append((row_line, nid))
            if not normalized_rows:
                continue

            separator_indexes = [
                i for i, (row_line, _) in enumerate(normalized_rows) if _is_md_separator_row(row_line)
            ]
            has_explicit_separator = len(separator_indexes) > 0

            if has_explicit_separator:
                sep_idx = separator_indexes[0]
                header_row: tuple[str, str] | None = normalized_rows[sep_idx - 1] if sep_idx > 0 else None
                data_rows = normalized_rows[sep_idx + 1 :]

                if not table_has_separator:
                    if header_row is not None:
                        # 明示ヘッダ付き（header + |---|）はこの表グループで 1 回だけ採用する。
                        table_markdown_buffer.append(header_row[0])
                        active_table_header_line = header_row[0]
                    table_markdown_buffer.append(normalized_rows[sep_idx][0])
                    table_has_separator = True
                elif header_row is not None and active_table_header_line and header_row[0] != active_table_header_line:
                    if table_markdown_buffer:
                        st.markdown("\n".join(table_markdown_buffer), unsafe_allow_html=True)
                        st.markdown("")
                    # 同じ選択内に別ヘッダ表が来たら、ここで表を切って新しい表を開始する。
                    table_markdown_buffer = [header_row[0], normalized_rows[sep_idx][0]]
                    active_table_header_line = header_row[0]
                    table_has_separator = True

                for row_line, nid in data_rows:
                    line_work = _add_checkbox_to_table_left_cell(row_line) if nid == block.nid else row_line
                    table_markdown_buffer.append(_add_help_to_table_right_cell(line_work, nid))
                continue

            for i, (row_line, nid) in enumerate(normalized_rows):
                if not table_has_separator and i == 0:
                    # 明示ヘッダが無い table_row 群はダミーヘッダを先頭に差し込む。
                    header_and_sep = _make_table_header_for_row(row_line)
                    if header_and_sep is not None:
                        table_markdown_buffer.extend([header_and_sep[0], header_and_sep[1]])
                        active_table_header_line = header_and_sep[0]
                        table_has_separator = True
                line_work = _add_checkbox_to_table_left_cell(row_line) if nid == block.nid else row_line
                table_markdown_buffer.append(_add_help_to_table_right_cell(line_work, nid))
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

    source_options = [SOURCE_MODE_FOLDER, SOURCE_MODE_YAML_FOLDER]
    profile_options = ["オリジナル", "カスタマイズ"]
    dedup_mode_options = ["共通先祖省略", "兄弟のみ先祖省略"]
    selectable_bundles = _discover_selectable_bundles()
    display_examples = _load_display_examples()
    example_by_id = {str(ex.get("id")): ex for ex in display_examples}
    folder_names = [b[0] for b in selectable_bundles]
    label_map = {
        b[0]: f"{b[0]} | {(b[4] or '(meta.yaml から法令名を取得できません)')}"
        for b in selectable_bundles
    }
    source_url_map = {b[0]: _meta_source_urls(b[3]) for b in selectable_bundles}

    if "source_mode_key" not in st.session_state:
        st.session_state["source_mode_key"] = source_options[0]
    if st.session_state.get("source_mode_key") not in source_options:
        st.session_state["source_mode_key"] = source_options[0]
    if "confirmed_source_mode_key" not in st.session_state:
        st.session_state["confirmed_source_mode_key"] = st.session_state["source_mode_key"]
    if st.session_state.get("confirmed_source_mode_key") not in source_options:
        st.session_state["confirmed_source_mode_key"] = source_options[0]
    if "purpose_mode_key" not in st.session_state:
        st.session_state["purpose_mode_key"] = profile_options[0]
    pending_purpose_mode = st.session_state.pop("pending_purpose_mode_key", None)
    if pending_purpose_mode in profile_options:
        st.session_state["purpose_mode_key"] = pending_purpose_mode
    if "normalized_folder_key" not in st.session_state and folder_names:
        st.session_state["normalized_folder_key"] = folder_names[0]
    if "dedup_mode_label_key" not in st.session_state:
        st.session_state["dedup_mode_label_key"] = dedup_mode_options[0]
    if "egov_merge_article_p1_key" not in st.session_state:
        st.session_state["egov_merge_article_p1_key"] = True
    if "active_demo_preset_key" not in st.session_state:
        st.session_state["active_demo_preset_key"] = ""
    if "shortcut_preset_key" not in st.session_state:
        st.session_state["shortcut_preset_key"] = ""
    if st.session_state.pop("pending_clear_shortcut_preset_key", False):
        st.session_state["shortcut_preset_key"] = ""

    def _queue_example(example_id: str) -> None:
        ex = example_by_id.get(example_id)
        if not isinstance(ex, dict):
            return
        st.session_state["source_mode_key"] = str(ex.get("source_mode", "フォルダ選択"))
        profile = ex.get("profile") if isinstance(ex.get("profile"), dict) else {}
        profile_mode = str(profile.get("mode", "original")).lower()
        st.session_state["purpose_mode_key"] = "カスタマイズ" if profile_mode == "custom" else "オリジナル"
        ex_display = ex.get("display") if isinstance(ex.get("display"), dict) else {}
        st.session_state["dedup_mode_label_key"] = str(
            ex_display.get("dedup_mode_label", dedup_mode_options[0])
        )
        st.session_state["egov_merge_article_p1_key"] = str(
            ex_display.get("egov_merge_article_p1", True)
        ).lower() == "true"
        folder = str(ex.get("law_folder", ""))
        if folder and folder in folder_names:
            st.session_state["normalized_folder_key"] = folder
        if profile_mode == "custom":
            custom_yaml_path = str(profile.get("custom_yaml_path", "")).strip()
            if custom_yaml_path:
                st.session_state["pending_custom_profile_path"] = custom_yaml_path
        selection_nids = ex.get("selection_nids")
        st.session_state["pending_demo_selection_nids"] = (
            [str(nid) for nid in selection_nids if isinstance(nid, str)]
            if isinstance(selection_nids, list)
            else []
        )
        st.session_state["active_demo_preset_key"] = example_id
        st.session_state["pending_clear_shortcut_preset_key"] = True
        st.rerun()

    st.subheader("モック用設定項目")
    st.markdown("#### 表示例へのショートカット（幾つかの典型例（自動設定）をご用意しました）")
    preset_order = [("", "（表示例を選択）")]
    for ex in display_examples:
        ex_id = str(ex.get("id", "")).strip()
        if not ex_id:
            continue
        display_name = str(ex.get("display_name", ex_id)).strip() or ex_id
        display_title = str(ex.get("display_title", "")).strip()
        label = f"{display_name}：{display_title}" if display_title else display_name
        preset_order.append((ex_id, label))
    preset_keys = [key for key, _ in preset_order]
    preset_label_map = {key: label for key, label in preset_order}

    def _format_preset_option(key: str) -> str:
        if not key:
            return preset_label_map[key]
        ex = example_by_id.get(key, {})
        return f"{preset_label_map[key]} | {_example_tooltip(ex, selectable_bundles)}"

    chosen_preset = st.selectbox(
        "表示例（法令・プロファイル・選択を一括適用）",
        preset_keys,
        key="shortcut_preset_key",
        format_func=_format_preset_option,
    )
    if chosen_preset:
        _queue_example(chosen_preset)

    current_source_mode = str(st.session_state.get("source_mode_key", source_options[0]))
    current_folder = str(st.session_state.get("normalized_folder_key", "")) if folder_names else ""
    confirmed_source_mode = str(st.session_state.get("confirmed_source_mode_key", SOURCE_MODE_FOLDER))
    confirmed_yaml_folder_path = str(
        st.session_state.get("yaml_folder_source_selected_path", "")
    ).strip()
    if current_source_mode == SOURCE_MODE_FOLDER:
        law_display_for_header = label_map.get(current_folder, current_folder or "（未選択）")
    else:
        law_display_for_header = "4yamlフォルダ指定"

    with st.expander(f"法令選択：[{law_display_for_header}]", expanded=True):
        pending_folder_warning = st.session_state.pop("yaml_folder_source_warning", "")
        if pending_folder_warning:
            st.warning(pending_folder_warning)
        source_mode_radio_key = f"source_mode_radio_key_{int(st.session_state.get('source_mode_radio_nonce', 0))}"
        source_mode_index = (
            source_options.index(current_source_mode)
            if current_source_mode in source_options
            else 0
        )
        source_mode = st.radio(
            "データソース切替",
            source_options,
            horizontal=True,
            index=source_mode_index,
            key=source_mode_radio_key,
        )
        selected_normalized_folder: str | None = None
        selected_yaml_folder_path: str | None = None
        effective_source_mode = confirmed_source_mode
        if source_mode == SOURCE_MODE_YAML_FOLDER and (
            confirmed_source_mode != SOURCE_MODE_YAML_FOLDER or not confirmed_yaml_folder_path
        ):
            try:
                picked_path = _pick_directory_with_dialog(confirmed_yaml_folder_path or str(Path.cwd()))
                accepted = _validate_and_store_yaml_folder_selection(
                    picked_path, confirmed_source_mode, confirmed_yaml_folder_path or None
                )
            except Exception as exc:
                _restore_source_selection_state(
                    confirmed_source_mode, confirmed_yaml_folder_path or None
                )
                st.session_state["yaml_folder_source_warning"] = (
                    f"フォルダ選択ダイアログを開けませんでした: {exc}"
                )
                accepted = False
            if accepted:
                st.session_state["confirmed_source_mode_key"] = SOURCE_MODE_YAML_FOLDER
            st.rerun()
        if source_mode == SOURCE_MODE_FOLDER:
            st.session_state["confirmed_source_mode_key"] = SOURCE_MODE_FOLDER
            st.session_state["source_mode_key"] = SOURCE_MODE_FOLDER
            effective_source_mode = SOURCE_MODE_FOLDER
            if not selectable_bundles:
                st.error("選択可能なフォルダ（data/normalized, out/*）が見つかりません。")
                return
            selected_normalized_folder = st.selectbox(
                "フォルダ選択（data/normalized, out/*）",
                folder_names,
                key="normalized_folder_key",
                format_func=lambda v: label_map.get(v, v),
            )
            source_urls = source_url_map.get(selected_normalized_folder, [])
            if len(source_urls) == 1:
                url = source_urls[0]
                st.markdown(f"元の法令ソース: [{_source_url_display(url)}]({url})")
            elif len(source_urls) > 1:
                st.markdown("元の法令ソース:")
                for index, url in enumerate(source_urls, start=1):
                    st.markdown(f"- [{index}. {_source_url_display(url)}]({url})")
            else:
                st.caption("元の法令ソースURL: meta.yaml に記載なし")
        if source_mode == SOURCE_MODE_YAML_FOLDER:
            selected_yaml_folder_path = confirmed_yaml_folder_path
            effective_source_mode = SOURCE_MODE_YAML_FOLDER
            st.caption(f"選択中フォルダ: {selected_yaml_folder_path}")
            if st.button("フォルダを選び直す", key="yaml_folder_source_repick_button"):
                try:
                    picked_path = _pick_directory_with_dialog(selected_yaml_folder_path)
                    accepted = _validate_and_store_yaml_folder_selection(
                        picked_path, SOURCE_MODE_YAML_FOLDER, selected_yaml_folder_path
                    )
                except Exception as exc:
                    _restore_source_selection_state(
                        SOURCE_MODE_YAML_FOLDER, selected_yaml_folder_path
                    )
                    st.session_state["yaml_folder_source_warning"] = (
                        f"フォルダ選択ダイアログを開けませんでした: {exc}"
                    )
                    accepted = False
                if accepted:
                    st.session_state["confirmed_source_mode_key"] = SOURCE_MODE_YAML_FOLDER
                st.rerun()
            if not selected_yaml_folder_path:
                effective_source_mode = SOURCE_MODE_FOLDER
                selected_normalized_folder = current_folder or (
                    folder_names[0] if folder_names else None
                )
    try:
        regdoc_ir, regdoc_profile, regdoc_meta, source_label = _load_from_selected_source(
            effective_source_mode, selected_normalized_folder, selected_yaml_folder_path
        )
    except Exception as exc:
        st.error(f"YAML抽出/パースに失敗しました: {exc}")
        return

    # 法令切替時に前法令の selected_nids を持ち越すと「存在しない nid」エラーになるため、
    # ソース署名が変わったタイミングで選択状態を初期化する。
    doc_signature = " | ".join(
        [
            effective_source_mode,
            selected_normalized_folder or "",
            selected_yaml_folder_path or "",
            str(regdoc_ir.get("doc_id") or ""),
        ]
    )
    prev_doc_signature = str(st.session_state.get("active_doc_signature", ""))
    if prev_doc_signature and prev_doc_signature != doc_signature:
        _clear_selection_state()
    st.session_state["active_doc_signature"] = doc_signature
    index = build_doc_index(regdoc_ir)
    is_egov_doc = str(regdoc_ir.get("doc_id") or "").startswith("jp_egov_")
    base_purpose = _purpose(regdoc_profile)
    original_profile_tooltip = "参照元プロファイル: 不明"
    if effective_source_mode == SOURCE_MODE_FOLDER and selected_normalized_folder:
        matched = next((b for b in selectable_bundles if b[0] == selected_normalized_folder), None)
        if matched is not None:
            original_profile_tooltip = f"参照元プロファイル: {matched[2].as_posix()}"
    elif effective_source_mode == SOURCE_MODE_YAML_FOLDER and selected_yaml_folder_path:
        _ir_path, _parser_path, profile_path, _meta_path = _single_yaml_bundle_in_folder(
            Path(selected_yaml_folder_path)
        )
        original_profile_tooltip = f"参照元プロファイル: {profile_path.as_posix()}"

    if "editable_purpose_yaml" not in st.session_state:
        st.session_state["editable_purpose_yaml"] = yaml.safe_dump(
            base_purpose, allow_unicode=True, sort_keys=False
        )
    if "applied_custom_purpose" not in st.session_state:
        st.session_state["applied_custom_purpose"] = deepcopy(base_purpose)
    pending_custom_profile_path = str(st.session_state.pop("pending_custom_profile_path", "")).strip()
    if pending_custom_profile_path:
        custom_path = Path(pending_custom_profile_path)
        if not custom_path.exists():
            st.warning(f"表示例の custom_yaml_path が見つかりません: {pending_custom_profile_path}")
        else:
            try:
                loaded_custom = yaml.safe_load(custom_path.read_text(encoding="utf-8"))
                if not isinstance(loaded_custom, dict):
                    raise ValueError("custom_yaml_path のYAMLトップレベルは辞書である必要があります。")
                st.session_state["editable_purpose_yaml"] = yaml.safe_dump(
                    loaded_custom, allow_unicode=True, sort_keys=False
                )
                st.session_state["applied_custom_purpose"] = loaded_custom
            except Exception as exc:
                st.warning(f"表示例の custom_yaml_path 読込に失敗しました: {exc}")
    pending_seed = st.session_state.pop("pending_custom_profile_seed", None)
    if pending_seed == "mock":
        seeded = _mock_purpose(base_purpose)
        st.session_state["editable_purpose_yaml"] = yaml.safe_dump(
            seeded, allow_unicode=True, sort_keys=False
        )
        st.session_state["applied_custom_purpose"] = seeded

    purpose_mode = str(st.session_state.get("purpose_mode_key", profile_options[0]))
    with st.expander(f"プロファイル：[{purpose_mode}]", expanded=True):
        st.radio(
            "プロファイル切替",
            profile_options,
            horizontal=True,
            key="purpose_mode_key",
            help=original_profile_tooltip,
        )
        c_apply1, c_apply2 = st.columns(2)
        with c_apply1:
            if st.button("オリジナルのYAML設定を以下に呼出し", help=original_profile_tooltip):
                st.session_state["editable_purpose_yaml"] = yaml.safe_dump(
                    base_purpose, allow_unicode=True, sort_keys=False
                )
        with c_apply2:
            if st.button("以下のカスタマイズYAMLを適用"):
                try:
                    loaded = yaml.safe_load(st.session_state.get("editable_purpose_yaml", ""))
                    if not isinstance(loaded, dict):
                        raise ValueError("YAMLのトップレベルは辞書である必要があります。")
                    st.session_state["applied_custom_purpose"] = loaded
                    st.session_state["editable_purpose_yaml"] = yaml.safe_dump(
                        loaded, allow_unicode=True, sort_keys=False
                    )
                    if loaded != base_purpose:
                        st.session_state["pending_purpose_mode_key"] = "カスタマイズ"
                        st.session_state["profile_apply_notice"] = (
                            "success",
                            "カスタマイズ設定を適用しました（プロファイル: カスタマイズ）。",
                        )
                        st.rerun()
                    else:
                        st.session_state["pending_purpose_mode_key"] = "オリジナル"
                        st.session_state["profile_apply_notice"] = (
                            "info",
                            "適用内容はオリジナル設定と同一です（プロファイル: オリジナル）。",
                        )
                        st.rerun()
                except Exception as exc:
                    st.error(f"YAML適用に失敗しました: {exc}")
        st.text_area(
            "YAMLエディットボックス",
            key="editable_purpose_yaml",
            height=260,
        )
        profile_apply_notice = st.session_state.pop("profile_apply_notice", None)
        if isinstance(profile_apply_notice, tuple) and len(profile_apply_notice) == 2:
            level, message = profile_apply_notice
            if level == "success":
                st.success(str(message))
            elif level == "info":
                st.info(str(message))

    purpose_mode = str(st.session_state.get("purpose_mode_key", profile_options[0]))
    current = base_purpose if purpose_mode == "オリジナル" else deepcopy(
        st.session_state.get("applied_custom_purpose", base_purpose)
    )

    dedup_mode_label = str(st.session_state.get("dedup_mode_label_key", dedup_mode_options[0]))
    egov_merge_article_p1 = bool(st.session_state.get("egov_merge_article_p1_key", True))
    display_mode_status = "共通省略" if dedup_mode_label == "共通先祖省略" else "兄弟省略"
    if is_egov_doc and egov_merge_article_p1:
        display_mode_status += "、各条第一項統合"
    with st.expander(f"表示カスタマイズ：[{display_mode_status}]", expanded=True):
        st.radio("文脈省略モード", dedup_mode_options, horizontal=True, key="dedup_mode_label_key")
        st.checkbox(
            "各条第一項の統合表示（eGovのみ）",
            key="egov_merge_article_p1_key",
            disabled=not is_egov_doc,
        )

    dedup_mode_label = str(st.session_state.get("dedup_mode_label_key", dedup_mode_options[0]))
    dedup_mode = "prefix" if dedup_mode_label == "共通先祖省略" else "exact"
    egov_merge_article_p1 = bool(st.session_state.get("egov_merge_article_p1_key", True))
    selectable_kinds = [str(v) for v in current.get("selectable_kinds", []) if isinstance(v, str)]
    candidate_visible_by_nid = build_candidate_visibility_map(index, current)
    if "selected_nids" not in st.session_state:
        st.session_state["selected_nids"] = []
    if "draft_selected_nids" not in st.session_state:
        st.session_state["draft_selected_nids"] = list(st.session_state["selected_nids"])
    pending_demo_nids_raw = st.session_state.pop("pending_demo_selection_nids", None)
    pending_demo_nids: List[str] = []
    if isinstance(pending_demo_nids_raw, list):
        pending_demo_nids = [str(nid) for nid in pending_demo_nids_raw if isinstance(nid, str)]
    if pending_demo_nids:
        resolved = [nid for nid in pending_demo_nids if nid in index.by_nid]
        if resolved:
            st.session_state["draft_selected_nids"] = resolved
            st.session_state["selected_nids"] = resolved
        else:
            st.warning("表示例の selection_nids はこのデータセットに存在しません。")

    left, right = st.columns(2)
    with left:
        st.subheader("チェック項目選択")
        _inject_nid_copy_hook()

        query = st.text_input("検索（nid/表示ラベル/本文）", "")
        rows = _all_rows(index, selectable_kinds, query, visible_by_nid=candidate_visible_by_nid)
        selectable_row_ids = [nid for nid, _, selectable, _ in rows if selectable]
        label_by_id = {nid: label for nid, label, _, _ in rows}

        st.caption("ord順の全ノードを表示中。選択可能ノードのみチェックできます。")
        draft_set = set(st.session_state.get("draft_selected_nids", []))
        _sync_checkbox_defaults(selectable_row_ids, draft_set)

        with st.form("candidate_form"):
            st.markdown(
                """
                <style>
                div[class*="st-key-candidate_"][data-testid="stElementContainer"] {
                    margin-bottom: 2px;
                }
                div[class*="st-key-candidate_"] div.row-widget.stCheckbox {
                    margin: 0 !important;
                    min-height: 0 !important;
                    padding: 0 !important;
                }
                div[class*="st-key-candidate_"] div[data-testid="stCheckbox"] {
                    margin: 0 !important;
                    padding: 0 !important;
                    min-height: 0 !important;
                }
                div[class*="st-key-candidate_"] div[data-testid="stCheckbox"] {
                    min-height: 0 !important;
                    height: auto !important;
                    margin: 0 !important;
                    padding: 0 !important;
                    line-height: 1 !important;
                }
                div[class*="st-key-candidate_"] div[data-testid="stCheckbox"] * {
                    min-height: 0 !important;
                    margin: 0 !important;
                    padding: 0 !important;
                    line-height: 1 !important;
                }
                div[class*="st-key-candidate_"] div.row-widget.stCheckbox {
                    align-items: flex-start !important;
                }
                .candidate-list .candidate-row {
                    display: flex;
                    align-items: flex-start;
                    justify-content: space-between;
                    gap: 8px;
                    line-height: 1.25;
                    margin: 0;
                    border-bottom: 1px solid #e5e7eb;
                }
                .candidate-list .candidate-row-selectable {
                    border-radius: 4px;
                    padding: 2px 6px;
                }
                .candidate-list .candidate-label {
                    color: #4b5563;
                    overflow-wrap: anywhere;
                }
                .candidate-list .candidate-icons {
                    white-space: nowrap;
                    color: #4b5563;
                    display: inline-flex;
                    gap: 6px;
                }
                .candidate-list .candidate-icon {
                    cursor: help;
                    font-size: 0.9em;
                    line-height: 1.1;
                }
                .candidate-list .candidate-icon-btn,
                .candidate-list .candidate-icon-btn:hover,
                .candidate-list .candidate-icon-btn:focus,
                .candidate-list .candidate-icon-btn:active,
                .candidate-list .candidate-icon-btn:focus-visible {
                    border: 0 !important;
                    outline: 0 !important;
                    box-shadow: none !important;
                    background: transparent !important;
                    background-color: transparent !important;
                    border-radius: 0 !important;
                    appearance: none !important;
                    -webkit-appearance: none !important;
                    padding: 0 !important;
                    margin: 0 !important;
                    min-height: 0 !important;
                    min-width: 0 !important;
                    width: auto !important;
                    height: auto !important;
                    font: inherit !important;
                    font-size: 0.9em !important;
                    color: #4b5563 !important;
                    line-height: 1.1 !important;
                    cursor: copy !important;
                    text-decoration: none !important;
                    display: inline !important;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<div class='candidate-list'>", unsafe_allow_html=True)
            with st.container(height=560, border=True):
                for row_num, (nid, label, selectable, depth) in enumerate(rows, start=1):
                    indent_px = depth * 14
                    row_bg = "#eef5ff" if row_num % 2 == 0 else "#ffffff"
                    if selectable:
                        c_check, c_text = st.columns([1, 30], vertical_alignment="top")
                        with c_check:
                            st.checkbox(
                                "",
                                key=_checkbox_key(nid),
                                label_visibility="collapsed",
                            )
                        with c_text:
                            path_tip = escape(_human_path(index, nid), quote=True)
                            nid_copy_icon = _nid_copy_icon_html(nid)
                            st.markdown(
                                (
                                    f"<div class='candidate-row candidate-row-selectable' style='margin-left:{indent_px}px;background:{row_bg};'>"
                                    f"<span class='candidate-label'>{escape(label)}</span>"
                                    "<span class='candidate-icons'>"
                                    f"<span class='candidate-icon' title='{path_tip}'>ⓘ</span>"
                                    f"{nid_copy_icon}"
                                    "</span>"
                                    "</div>"
                                ),
                                unsafe_allow_html=True,
                            )
                    else:
                        nid_copy_icon = _nid_copy_icon_html(nid)
                        st.markdown(
                            (
                                f"<div class='candidate-row' style='margin-left:{indent_px}px;background:{row_bg};'>"
                                f"<span class='candidate-label'>{escape(label)}</span>"
                                "<span class='candidate-icons'>"
                                f"{nid_copy_icon}"
                                "</span>"
                                "</div>"
                            ),
                            unsafe_allow_html=True,
                        )
            st.markdown("</div>", unsafe_allow_html=True)
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
        st.subheader("チェックシート")
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
    st.markdown("`candidate_visibility`")
    st.code(
        yaml.safe_dump({"candidate_visibility": current.get("candidate_visibility", {})}, allow_unicode=True, sort_keys=False),
        "yaml",
    )
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
