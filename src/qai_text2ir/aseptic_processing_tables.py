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
        "parent_nid": "cha7.sec7_1",
        "strip_re": re.compile(r"\n?\s*表１\s*清浄区域の分類.*$", flags=re.DOTALL),
        "heading": "表１ 清浄区域の分類",
    },
    {
        "table_no": "2",
        "caption_re": re.compile(r"^\s*表２\s+微生物管理に係る環境モニタリングの頻度\s*$"),
        "end_re": re.compile(r"^\s*表\s*3\s+環境微生物の許容基準"),
        "parent_nid": "cha11.sec11_3",
        "strip_re": re.compile(r"\n?\s*表２\s*微生物管理に係る環境モニタリングの頻度.*$", flags=re.DOTALL),
        "heading": "表２ 微生物管理に係る環境モニタリングの頻度",
    },
    {
        "table_no": "3",
        "caption_re": re.compile(r"^\s*表\s*3\s+環境微生物の許容基準\(作業時\)\s*注）1\s*$"),
        "end_re": re.compile(r"^\s*注）1\s+"),
        "parent_nid": "cha11.sec11_3",
        "remove_child_nid": "cha11.sec11_3.pre1",
        "heading": "表 3 環境微生物の許容基準(作業時) 注）1",
    },
]
RECONSTRUCTED_COLUMNS_BY_TABLE = {
    "1": [
        "area_group",
        "area_name",
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
RECONSTRUCTED_COLUMN_LABELS_BY_TABLE = {
    "1": [
        "名称 区分",
        "名称 区域",
        "空気の清浄度レベル注1）",
        "最大許容微粒子数（個／m3） 非作業時 ≧0.5μm",
        "最大許容微粒子数（個／m3） 非作業時 ≧5.0μm",
        "最大許容微粒子数（個／m3） 作業時 ≧0.5μm",
        "最大許容微粒子数（個／m3） 作業時 ≧5.0μm",
    ],
    "2": [
        "グレード",
        "区域",
        "空中浮遊微粒子",
        "空中微生物",
        "表面付着微生物 装置，壁など",
        "表面付着微生物 手袋，作業衣",
    ],
    "3": [
        "グレード",
        "空中微生物 浮遊菌 (CFU/m3)",
        "空中微生物 落下菌注）2 (CFU/plate)",
        "表面付着微生物 コンタクトプレート (CFU/24～30cm2)",
        "表面付着微生物 手袋 (CFU/5指)",
    ],
}
HEADER_STRUCTURE_BY_TABLE = {
    "1": {
        "spanning_headers": [
            {"label": "名称", "columns": ["area_group", "area_name"], "column_range": [0, 1]},
            {
                "label": "最大許容微粒子数（個／m3）",
                "columns": [
                    "non_operational_0_5um",
                    "non_operational_5_0um",
                    "operational_0_5um",
                    "operational_5_0um",
                ],
                "column_range": [3, 6],
            },
            {
                "label": "非作業時",
                "columns": ["non_operational_0_5um", "non_operational_5_0um"],
                "column_range": [3, 4],
            },
            {
                "label": "作業時",
                "columns": ["operational_0_5um", "operational_5_0um"],
                "column_range": [5, 6],
            },
        ],
        "leaf_labels": ["区分", "区域", "清浄度レベル注1）", "≧0.5μm", "≧5.0μm", "≧0.5μm", "≧5.0μm"],
    },
    "2": {
        "spanning_headers": [
            {
                "label": "表面付着微生物",
                "columns": ["surface_attached_equipment_walls", "surface_attached_gloves_garment"],
                "column_range": [4, 5],
            }
        ],
        "leaf_labels": ["グレード", "区域", "空中浮遊微粒子", "空中微生物", "装置，壁など", "手袋，作業衣"],
    },
    "3": {
        "spanning_headers": [
            {
                "label": "空中微生物",
                "columns": ["airborne_microorganisms_cfu_m3", "settle_plate_cfu_plate"],
                "column_range": [1, 2],
            },
            {
                "label": "表面付着微生物",
                "columns": ["contact_plate_cfu_24_30cm2", "gloves_cfu_5_fingers"],
                "column_range": [3, 4],
            },
        ],
        "leaf_labels": ["グレード", "浮遊菌", "落下菌注）2", "コンタクトプレート", "手袋"],
        "unit_labels": [None, "(CFU/m3)", "(CFU/plate)", "(CFU/24～30cm2)", "(CFU/5指)"],
    },
}
RECONSTRUCTED_RECORDS_BY_TABLE = {
    "1": [
        {
            "record_id": "aseptic_table1.r1",
            "raw_row_nums": [6],
            "cells": ["無菌操作区域", "重要区域", "グレード A (ISO 5)", "3,520", "20", "3,520", "20"],
        },
        {
            "record_id": "aseptic_table1.r2",
            "raw_row_nums": [9],
            "cells": ["無菌操作区域", "直接支援区域", "グレード B (ISO 7)", "3,520", "29", "352,000", "2,900"],
        },
        {
            "record_id": "aseptic_table1.r3",
            "raw_row_nums": [10],
            "cells": ["その他の支援区域", "", "グレード C (ISO 8)", "352,000", "2,900", "3,520,000", "29,000"],
        },
        {
            "record_id": "aseptic_table1.r4",
            "raw_row_nums": [11, 12, 13, 14],
            "cells": [
                "その他の支援区域",
                "",
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
RECORD_REVIEW_BY_TABLE = {
    "1": {
        "status": "reviewed_candidate",
        "candidate_granularity": "visual_reconstructed_table_row",
        "table_row_promotion": "promoted",
        "table_row_promotion_reason": "PDF visual review restored merged headers and four data rows",
        "note_handling": "table notes kept as note nodes; note-to-cell links deferred",
        "reviewed_records": 4,
        "deferred_raw_rows": [1, 2, 3, 4, 5, 7, 8],
    },
    "2": {
        "status": "reviewed_candidate",
        "candidate_granularity": "visual_reconstructed_table_row",
        "table_row_promotion": "promoted",
        "table_row_promotion_reason": "PDF visual review restored merged C/D condition rows",
        "note_handling": "no separate note node in source table range",
        "reviewed_records": 4,
        "deferred_raw_rows": [1, 2, 3],
    },
    "3": {
        "status": "reviewed_candidate",
        "candidate_granularity": "visual_reconstructed_table_row",
        "table_row_promotion": "promoted",
        "table_row_promotion_reason": "PDF visual review restored merged microbial header rows",
        "note_handling": "table notes kept as note nodes; note-to-cell links deferred",
        "reviewed_records": 4,
        "deferred_raw_rows": [1, 2, 3],
    },
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
    columns = RECONSTRUCTED_COLUMNS_BY_TABLE.get(table.table_no, ["raw_line"])
    column_labels = RECONSTRUCTED_COLUMN_LABELS_BY_TABLE.get(table.table_no, ["raw_line"])
    header_structure = HEADER_STRUCTURE_BY_TABLE.get(table.table_no, {})
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
            "source_format": "pdf_visual_review_plus_ragged_text",
            "column_reconstruction": "visual_reviewed",
            "column_reconstruction_status": "complete_for_reviewed_tables",
            "columns": columns,
            "column_labels": column_labels,
            "header_structure": header_structure,
            "raw_lines": table.raw_lines,
            "non_data_raw_rows": NON_DATA_ROWS_BY_TABLE.get(table.table_no, []),
            "record_review": RECORD_REVIEW_BY_TABLE.get(table.table_no, {}),
        },
    )
    header = _make_node(
        nid=f"{table_nid}.tblh",
        kind="table_header",
        kind_raw="table_header",
        num=None,
        heading=None,
        text=" | ".join(column_labels),
        source_label=source_label,
        line_idx=table.caption_idx + line_no_offset,
        role="structural",
        data={"columns": columns, "column_labels": column_labels, "header_structure": header_structure},
    )
    node.children.append(header)
    records = RECONSTRUCTED_RECORDS_BY_TABLE.get(table.table_no, [])
    for row_no, record in enumerate(records, start=1):
        raw_row_nums = list(record["raw_row_nums"])
        raw_lines = [table.raw_lines[i - 1] for i in raw_row_nums if 0 <= i - 1 < len(table.raw_lines)]
        raw_indexes = [table.raw_line_indexes[i - 1] for i in raw_row_nums if 0 <= i - 1 < len(table.raw_line_indexes)]
        line_idx = raw_indexes[0] if raw_indexes else table.caption_idx
        cells = list(record["cells"])
        header.children.append(
            _make_node(
                nid=f"{header.nid}.tblr{row_no}",
                kind="table_row",
                kind_raw="table_row",
                num=str(row_no),
                heading=None,
                text=" | ".join(cells),
                source_label=source_label,
                line_idx=line_idx + line_no_offset,
                data={
                    "record_id": record["record_id"],
                    "cells": cells,
                    "columns": columns,
                    "column_labels": column_labels,
                    "raw_row_nums": raw_row_nums,
                    "raw_lines": raw_lines,
                    "visual_review_status": "reviewed_candidate",
                    "source_basis": "PDF visual table and source text table lines",
                },
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
    return node


def _apply_column_reconstruction_prototype(table_node: Node, table_no: str) -> None:
    columns = RECONSTRUCTED_COLUMNS_BY_TABLE.get(table_no)
    records = RECONSTRUCTED_RECORDS_BY_TABLE.get(table_no, [])
    if not columns:
        return
    table_node.data["column_reconstruction"] = "prototype"
    table_node.data["column_reconstruction_status"] = "partial"
    table_node.data["reconstructed_columns"] = columns
    table_node.data["reconstructed_records"] = [
        {**record, "review_status": "reviewed_candidate", "promotion_status": "deferred"} for record in records
    ]
    table_node.data["non_data_raw_rows"] = NON_DATA_ROWS_BY_TABLE.get(table_no, [])
    table_node.data["record_review"] = RECORD_REVIEW_BY_TABLE.get(table_no, {})
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


def _source_line(node: Node) -> Optional[int]:
    for span in node.source_spans or []:
        locator = span.get("locator")
        if not isinstance(locator, str):
            continue
        match = re.search(r"line:(\d+)", locator)
        if match:
            return int(match.group(1))
    return None


def _remove_duplicate_table_notes(parent: Node, table: RawTable, *, line_no_offset: int) -> None:
    note_lines = {line_idx + line_no_offset + 1 for line_idx in table.note_line_indexes}
    if not note_lines:
        return

    def overlaps_table_note(child: Node) -> bool:
        if child.kind != "note":
            return False
        return any((_source_line(child) or -1) in note_lines for _span in child.source_spans or [None])

    parent.children = [child for child in parent.children if not overlaps_table_note(child)]


def _source_lines(node: Node) -> set[int]:
    lines: set[int] = set()
    for span in node.source_spans or []:
        locator = span.get("locator")
        if not isinstance(locator, str):
            continue
        match = re.search(r"line:(\d+)", locator)
        if match:
            lines.add(int(match.group(1)))
    return lines


def _remove_generated_table_artifacts(parent: Node, table: RawTable, spec: Dict[str, Any], *, line_no_offset: int) -> None:
    table_lines = {
        line_idx + line_no_offset + 1
        for line_idx in [table.caption_idx, *table.raw_line_indexes, *table.note_line_indexes]
    }
    strip_re = spec.get("strip_re")

    def clean(node: Node) -> None:
        if strip_re is not None and node.text:
            cleaned = strip_re.sub("", node.text).rstrip()
            if cleaned != node.text:
                node.text = cleaned or None
                node.source_spans = [
                    span
                    for span in node.source_spans
                    if _locator_line_not_in(span, table_lines)
                ]

        kept_children: List[Node] = []
        for child in node.children:
            child_lines = _source_lines(child)
            generated_table_artifact = (
                child.kind == "preformatted"
                or "possible_plaintext_table_not_structured" in child.tags
                or (child.data or {}).get("warning") == "possible_plaintext_table_not_structured"
            )
            if generated_table_artifact and child_lines and child_lines.issubset(table_lines):
                continue
            clean(child)
            kept_children.append(child)
        node.children = kept_children

    clean(parent)


def _locator_line_not_in(span: Dict[str, str], blocked_lines: set[int]) -> bool:
    locator = span.get("locator")
    if not isinstance(locator, str):
        return True
    match = re.search(r"line:(\d+)", locator)
    if not match:
        return True
    return int(match.group(1)) not in blocked_lines


def _insert_child_by_source_order(parent: Node, child: Node) -> None:
    child_line = _source_line(child)
    if child_line is None:
        parent.children.append(child)
        return
    for idx, existing in enumerate(parent.children):
        existing_line = _source_line(existing)
        if existing_line is not None and existing_line > child_line:
            parent.children.insert(idx, child)
            return
    parent.children.append(child)


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
        _remove_generated_table_artifacts(parent, table, spec, line_no_offset=line_no_offset)
        _remove_duplicate_table_notes(parent, table, line_no_offset=line_no_offset)
        table_node = _table_node(table, parent_nid=parent.nid, source_label=source_label, line_no_offset=line_no_offset)
        _insert_child_by_source_order(parent, table_node)
        applied.append({"table_no": table.table_no, "parent_nid": parent.nid, "rows": len(table.raw_lines)})
    return {"applied": bool(applied), "tables": applied}
