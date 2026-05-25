from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

from qai_xml2ir.models_ir import Node


TABLE_SPECS = [
    {
        "table_no": "1",
        "caption_re": re.compile(r"^\s*表１\s+清浄区域の分類\s*$"),
        "end_re": re.compile(r"^\s*注\s*1）"),
        "parent_nid": "cha7.p7_1",
        "strip_re": re.compile(r"\n?\s*表１\s+清浄区域の分類.*$", flags=re.DOTALL),
        "heading": "表１ 清浄区域の分類",
    },
    {
        "table_no": "2",
        "caption_re": re.compile(r"^\s*表２\s+微生物管理に係る環境モニタリングの頻度\s*$"),
        "end_re": re.compile(r"^\s*表\s*3\s+環境微生物の許容基準"),
        "parent_nid": "cha11.p11_3",
        "strip_re": re.compile(r"\n?\s*表２\s+微生物管理に係る環境モニタリングの頻度.*$", flags=re.DOTALL),
        "heading": "表２ 微生物管理に係る環境モニタリングの頻度",
    },
    {
        "table_no": "3",
        "caption_re": re.compile(r"^\s*表\s*3\s+環境微生物の許容基準\(作業時\)\s*注）1\s*$"),
        "end_re": re.compile(r"^\s*注）1\s+"),
        "parent_nid": "cha11.p11_3",
        "remove_child_nid": "cha11.p11_3.pre1",
        "heading": "表 3 環境微生物の許容基準(作業時) 注）1",
    },
]
RECONSTRUCTED_COLUMNS_BY_TABLE = {
    "1": [
        "area",
        "cleanliness_level",
        "non_operational_0_5um",
        "non_operational_5_0um",
        "operational_0_5um",
        "operational_5_0um",
    ],
    "2": [
        "grade",
        "area_condition",
        "airborne_particles",
        "airborne_microorganisms",
        "surface_attached_equipment_walls",
        "surface_attached_gloves_garment",
    ],
    "3": [
        "grade",
        "airborne_microorganisms_cfu_m3",
        "settle_plate_cfu_plate",
        "contact_plate_cfu_24_30cm2",
        "gloves_cfu_5_fingers",
    ],
}
RECONSTRUCTED_RECORDS_BY_TABLE = {
    "1": [
        {
            "record_id": "aseptic_table1.r1",
            "raw_row_nums": [6],
            "cells": ["重要区域", "グレード A (ISO 5)", "3,520", "20", "3,520", "20"],
        },
        {
            "record_id": "aseptic_table1.r2",
            "raw_row_nums": [9],
            "cells": ["直接支援区域", "グレード B (ISO 7)", "3,520", "29", "352,000", "2,900"],
        },
        {
            "record_id": "aseptic_table1.r3",
            "raw_row_nums": [10],
            "cells": ["その他の支援区域", "グレード C (ISO 8)", "352,000", "2,900", "3,520,000", "29,000"],
        },
        {
            "record_id": "aseptic_table1.r4",
            "raw_row_nums": [11, 12, 13, 14],
            "cells": [
                "その他の支援区域",
                "グレード D",
                "3,520,000",
                "29,000",
                "作業形態による注2）",
                "作業形態による注2）",
            ],
        },
    ],
    "2": [
        {
            "record_id": "aseptic_table2.r1",
            "raw_row_nums": [4],
            "cells": ["A", "", "作業中", "作業シフトごと", "作業終了後", "作業終了後"],
        },
        {
            "record_id": "aseptic_table2.r2",
            "raw_row_nums": [5],
            "cells": ["B", "", "作業中", "作業シフトごと", "作業終了後", "作業終了後"],
        },
        {
            "record_id": "aseptic_table2.r3",
            "raw_row_nums": [6, 7, 8],
            "cells": ["C，D", "製品や容器が環境に曝露される区域", "月1回", "週2回", "週2回", "----"],
        },
        {
            "record_id": "aseptic_table2.r4",
            "raw_row_nums": [9],
            "cells": ["C，D", "その他の区域", "月1回", "週1回", "週1回", "----"],
        },
    ],
    "3": [
        {"record_id": "aseptic_table3.r1", "raw_row_nums": [4], "cells": ["A", "＜1", "＜1", "＜1", "＜1"]},
        {"record_id": "aseptic_table3.r2", "raw_row_nums": [5], "cells": ["B", "10", "5", "5", "5"]},
        {"record_id": "aseptic_table3.r3", "raw_row_nums": [6], "cells": ["C", "100", "50", "25", "----"]},
        {"record_id": "aseptic_table3.r4", "raw_row_nums": [7], "cells": ["D", "200", "100", "50", "----"]},
    ],
}
NON_DATA_ROWS_BY_TABLE = {
    "1": [
        {"raw_row_num": 1, "reason": "header_line"},
        {"raw_row_num": 2, "reason": "header_line"},
        {"raw_row_num": 3, "reason": "header_line"},
        {"raw_row_num": 4, "reason": "header_line"},
        {"raw_row_num": 5, "reason": "header_line"},
        {"raw_row_num": 7, "reason": "wrapped_area_label"},
        {"raw_row_num": 8, "reason": "wrapped_area_label"},
    ],
    "2": [
        {"raw_row_num": 1, "reason": "header_line"},
        {"raw_row_num": 2, "reason": "header_line"},
        {"raw_row_num": 3, "reason": "header_line"},
    ],
    "3": [
        {"raw_row_num": 1, "reason": "header_line"},
        {"raw_row_num": 2, "reason": "header_line"},
        {"raw_row_num": 3, "reason": "header_line"},
    ],
}


@dataclass
class RawTable:
    table_no: str
    caption_idx: int
    end_idx: int
    raw_lines: List[str]
    raw_line_indexes: List[int]
    note_lines: List[str]
    note_line_indexes: List[int]
    heading: str


def _line_span(source_label: str, line_idx: int) -> Dict[str, str]:
    return {"source_label": source_label, "locator": f"line:{line_idx + 1}"}


def _make_node(
    *,
    nid: str,
    kind: str,
    kind_raw: Optional[str],
    num: Optional[str],
    heading: Optional[str],
    text: Optional[str],
    source_label: str,
    line_idx: int,
    role: Optional[str] = None,
    data: Optional[Dict[str, Any]] = None,
) -> Node:
    resolved_role = role or ("structural" if kind in {"table", "table_header"} else "normative")
    return Node(
        nid=nid,
        kind=kind,
        kind_raw=kind_raw,
        num=num,
        ord=None,
        heading=heading,
        text=text,
        role=resolved_role,
        normativity="must" if resolved_role == "normative" else None,
        source_spans=[_line_span(source_label, line_idx)],
        data=data or {},
    )


def _find_table(lines: List[str], spec: Dict[str, Any]) -> Optional[RawTable]:
    caption_re = spec["caption_re"]
    end_re = spec["end_re"]
    caption_idx = next((idx for idx, line in enumerate(lines) if caption_re.match(line)), None)
    if caption_idx is None:
        return None
    end_idx = next((idx for idx in range(caption_idx + 1, len(lines)) if end_re.match(lines[idx])), len(lines))
    raw_lines: List[str] = []
    raw_line_indexes: List[int] = []
    for idx in range(caption_idx + 1, end_idx):
        line = lines[idx].strip()
        if not line:
            continue
        raw_lines.append(line)
        raw_line_indexes.append(idx)

    note_lines: List[str] = []
    note_line_indexes: List[int] = []
    if str(spec["table_no"]) in {"1", "3"}:
        for idx in range(end_idx, min(end_idx + 4, len(lines))):
            line = lines[idx].strip()
            if not line:
                break
            if line.startswith("注"):
                note_lines.append(line)
                note_line_indexes.append(idx)
    return RawTable(
        table_no=str(spec["table_no"]),
        caption_idx=caption_idx,
        end_idx=end_idx,
        raw_lines=raw_lines,
        raw_line_indexes=raw_line_indexes,
        note_lines=note_lines,
        note_line_indexes=note_line_indexes,
        heading=str(spec["heading"]),
    )


def _table_node(table: RawTable, *, parent_nid: str, source_label: str, line_no_offset: int) -> Node:
    table_nid = f"{parent_nid}.tbl{table.table_no}"
    node = _make_node(
        nid=table_nid,
        kind="table",
        kind_raw="table",
        num=table.table_no,
        heading=table.heading,
        text=None,
        source_label=source_label,
        line_idx=table.caption_idx + line_no_offset,
        role="structural",
        data={
            "parser": "aseptic_processing_table_adapter",
            "table_no": table.table_no,
            "source_format": "ragged_fixed_width_text",
            "column_reconstruction": False,
            "raw_lines": table.raw_lines,
        },
    )
    header = _make_node(
        nid=f"{table_nid}.tblh",
        kind="table_header",
        kind_raw="table_header",
        num=None,
        heading=None,
        text="raw_line",
        source_label=source_label,
        line_idx=table.caption_idx + line_no_offset,
        role="structural",
        data={"columns": ["raw_line"]},
    )
    node.children.append(header)
    for row_no, (line, line_idx) in enumerate(zip(table.raw_lines, table.raw_line_indexes), start=1):
        header.children.append(
            _make_node(
                nid=f"{header.nid}.tblr{row_no}",
                kind="table_row",
                kind_raw="table_row",
                num=str(row_no),
                heading=None,
                text=line,
                source_label=source_label,
                line_idx=line_idx + line_no_offset,
                data={"cells": [line], "raw_line": line},
            )
        )
    for note_no, (line, line_idx) in enumerate(zip(table.note_lines, table.note_line_indexes), start=1):
        node.children.append(
            _make_node(
                nid=f"{table_nid}.not{note_no}",
                kind="note",
                kind_raw="note",
                num=str(note_no),
                heading=None,
                text=line,
                source_label=source_label,
                line_idx=line_idx + line_no_offset,
                role="informative",
                data={"note_type": "table_note", "table_no": table.table_no},
            )
        )
    _apply_column_reconstruction_prototype(node, table.table_no)
    return node


def _apply_column_reconstruction_prototype(table_node: Node, table_no: str) -> None:
    columns = RECONSTRUCTED_COLUMNS_BY_TABLE.get(table_no)
    records = RECONSTRUCTED_RECORDS_BY_TABLE.get(table_no, [])
    if not columns:
        return
    table_node.data["column_reconstruction"] = "prototype"
    table_node.data["column_reconstruction_status"] = "partial"
    table_node.data["reconstructed_columns"] = columns
    table_node.data["reconstructed_records"] = records
    table_node.data["non_data_raw_rows"] = NON_DATA_ROWS_BY_TABLE.get(table_no, [])
    row_to_record = {
        row_no: record["record_id"]
        for record in records
        for row_no in record["raw_row_nums"]
    }
    for header in table_node.children:
        if header.kind != "table_header":
            continue
        header.data["reconstructed_columns"] = columns
        for row in header.children:
            if row.kind != "table_row":
                continue
            row_no = int(row.num or 0)
            if row_no in row_to_record:
                row.data["column_reconstruction_record_id"] = row_to_record[row_no]
            else:
                row.data["column_reconstruction_warning"] = "non_data_row_not_cell_reconstructed"


def _walk_with_parent(node: Node, parent: Optional[Node] = None) -> Iterable[Tuple[Optional[Node], Node]]:
    yield parent, node
    for child in node.children:
        yield from _walk_with_parent(child, node)


def _node_by_nid(root: Node, nid: str) -> Optional[Node]:
    for _parent, node in _walk_with_parent(root):
        if node.nid == nid:
            return node
    return None


def _remove_child(parent: Node, child_nid: str) -> None:
    parent.children = [child for child in parent.children if child.nid != child_nid]


def normalize_aseptic_processing_tables(
    root: Node,
    raw_lines: List[str],
    *,
    source_label: str,
    line_no_offset: int = 0,
) -> Dict[str, Any]:
    applied: List[Dict[str, Any]] = []
    for spec in TABLE_SPECS:
        table = _find_table(raw_lines, spec)
        if table is None:
            continue
        parent = _node_by_nid(root, str(spec["parent_nid"]))
        if parent is None:
            continue
        strip_re = spec.get("strip_re")
        if strip_re is not None and parent.text:
            parent.text = strip_re.sub("", parent.text).rstrip() or None
        remove_child_nid = spec.get("remove_child_nid")
        if isinstance(remove_child_nid, str):
            _remove_child(parent, remove_child_nid)
        parent.children.append(_table_node(table, parent_nid=parent.nid, source_label=source_label, line_no_offset=line_no_offset))
        applied.append({"table_no": table.table_no, "parent_nid": parent.nid, "rows": len(table.raw_lines)})
    return {"applied": bool(applied), "tables": applied}
