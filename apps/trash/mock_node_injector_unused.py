from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict

from qai_mock_ui.ir_model import build_doc_index


# TRASH: 旧モックUI向けのデモ行注入ロジック。
# 実法令データを汚染するため本体では使用しない。
def ensure_mock_nodes_for_demo(regdoc_ir: Dict[str, Any]) -> Dict[str, Any]:
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
                (
                    "appdx_table1.tbl1.tblh.tblr2",
                    1.0,
                    "【2行目デモ】標識の補足説明 | 【2行目デモ】大きさの補足 | 【2行目デモ】設置箇所の補足",
                ),
                (
                    "appdx_table1.tbl1.tblh.tblr3",
                    2.0,
                    "【3行目デモ】標識の補足説明 | 【3行目デモ】大きさの補足 | 【3行目デモ】設置箇所の補足",
                ),
                (
                    "appdx_table1.tbl1.tblh.tblr4",
                    3.0,
                    "【4行目デモ】標識の補足説明 | 【4行目デモ】大きさの補足 | 【4行目デモ】設置箇所の補足",
                ),
                (
                    "appdx_table1.tbl1.tblh.tblr5",
                    4.0,
                    "【5行目デモ】標識の補足説明 | 【5行目デモ】大きさの補足 | 【5行目デモ】設置箇所の補足",
                ),
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
