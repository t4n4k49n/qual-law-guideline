from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

from qai_xml2ir.models_ir import Node


CAPTION_RE = re.compile(r"^\s*表１：原薬生産に対する本ガイドラインの適用\s*$")
NEXT_CHAPTER_RE = re.compile(r"^\s*2[．.]\s+品質マネージメント\s*$")
RECONSTRUCTED_COLUMNS = [
    "production_type",
    "early_stage_1",
    "early_stage_2",
    "middle_stage",
    "late_stage",
    "final_stage",
]
RECONSTRUCTED_RECORDS = [
    {
        "record_id": "api_gmp_table1.r1",
        "raw_row_nums": [3, 4, 5],
        "cells": [
            "化学的合成による原薬",
            "原薬出発物質の製造",
            "原薬出発物質の工程への導入",
            "中間体の製造",
            "分離及び精製",
            "物理的加工処理及び包装",
        ],
    },
    {
        "record_id": "api_gmp_table1.r2",
        "raw_row_nums": [6, 7, 8],
        "cells": [
            "動物由来の原薬",
            "器官、液体又は組織の収集",
            "細断、混合、及び初期加工処理",
            "原薬出発物質の工程への導入",
            "分離及び精製",
            "物理的加工処理及び包装",
        ],
    },
    {
        "record_id": "api_gmp_table1.r3",
        "raw_row_nums": [9, 10, 11],
        "cells": [
            "植物から抽出する原薬",
            "植物の収集",
            "細断及び初期抽出",
            "原薬出発物質の工程への導入",
            "分離及び精製",
            "物理的加工処理及び包装",
        ],
    },
    {
        "record_id": "api_gmp_table1.r4",
        "raw_row_nums": [12, 13, 14],
        "cells": [
            "原薬として使用する生薬抽出物",
            "植物の収集",
            "細断及び初期抽出",
            "",
            "再抽出",
            "物理的加工処理及び包装",
        ],
    },
    {
        "record_id": "api_gmp_table1.r5",
        "raw_row_nums": [15, 16, 17],
        "cells": [
            "粉砕又は粉末化した生薬で構成する原薬",
            "植物の収集又は栽培及び収穫",
            "細断／粉砕",
            "",
            "",
            "物理的加工処理及び包装",
        ],
    },
    {
        "record_id": "api_gmp_table1.r6",
        "raw_row_nums": [18, 19, 20, 21, 22],
        "cells": [
            "バイオテクノロジー（発酵・細胞培養）を応用した原薬",
            "マスターセルバンク及びワーキングセルバンクの確立",
            "ワーキングセルバンクの維持管理",
            "細胞培養又は発酵",
            "分離及び精製",
            "物理的加工処理及び包装",
        ],
    },
    {
        "record_id": "api_gmp_table1.r7",
        "raw_row_nums": [23, 24, 25],
        "cells": [
            "クラシカル発酵を応用した原薬",
            "セルバンクの確立",
            "セルバンクの維持管理",
            "セルの発酵工程への導入",
            "分離及び精製",
            "物理的加工処理及び包装",
        ],
    },
]
RECORD_REVIEW = {
    "status": "reviewed_candidate",
    "candidate_granularity": "reconstructed_record",
    "table_row_promotion": "deferred",
    "table_row_promotion_reason": (
        "raw rows contain visual layout and multi-line cells; keep stable raw table_rows until normalized run readiness"
    ),
    "note_handling": "directional_note_kept_as_non_data_raw_row",
    "visual_information": "PDF gray-area layout not represented in text source",
    "reviewed_records": 7,
    "deferred_raw_rows": [1, 2, 26],
}


@dataclass
class ApiGmpTable1:
    caption_idx: int
    end_idx: int
    raw_lines: List[str]
    raw_line_indexes: List[int]


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


def _find_table(lines: List[str]) -> Optional[ApiGmpTable1]:
    caption_idx = next((idx for idx, line in enumerate(lines) if CAPTION_RE.match(line)), None)
    if caption_idx is None:
        return None
    end_idx = next((idx for idx in range(caption_idx + 1, len(lines)) if NEXT_CHAPTER_RE.match(lines[idx])), len(lines))
    raw_lines: List[str] = []
    raw_line_indexes: List[int] = []
    for idx in range(caption_idx + 1, end_idx):
        line = lines[idx].strip()
        if not line:
            continue
        raw_lines.append(line)
        raw_line_indexes.append(idx)
    return ApiGmpTable1(caption_idx=caption_idx, end_idx=end_idx, raw_lines=raw_lines, raw_line_indexes=raw_line_indexes)


def _table_node(table: ApiGmpTable1, *, parent_nid: str, source_label: str, line_no_offset: int) -> Node:
    table_nid = f"{parent_nid}.tbl1"
    node = _make_node(
        nid=table_nid,
        kind="table",
        kind_raw="table",
        num="1",
        heading="表１：原薬生産に対する本ガイドラインの適用",
        text=None,
        source_label=source_label,
        line_idx=table.caption_idx + line_no_offset,
        role="structural",
        data={
            "parser": "api_gmp_table1_adapter",
            "table_no": "1",
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
    _apply_column_reconstruction_prototype(node)
    return node


def _apply_column_reconstruction_prototype(table_node: Node) -> None:
    table_node.data["column_reconstruction"] = "prototype"
    table_node.data["column_reconstruction_status"] = "partial"
    table_node.data["reconstructed_columns"] = RECONSTRUCTED_COLUMNS
    table_node.data["reconstructed_records"] = [
        {**record, "review_status": "reviewed_candidate", "promotion_status": "deferred"} for record in RECONSTRUCTED_RECORDS
    ]
    table_node.data["record_review"] = RECORD_REVIEW
    table_node.data["non_data_raw_rows"] = [
        {"raw_row_num": 1, "reason": "header_line"},
        {"raw_row_num": 2, "reason": "visual_annotation"},
        {"raw_row_num": 26, "reason": "directional_note_without_cells"},
    ]
    row_to_record = {
        row_no: record["record_id"]
        for record in RECONSTRUCTED_RECORDS
        for row_no in record["raw_row_nums"]
    }
    for header in table_node.children:
        if header.kind != "table_header":
            continue
        header.data["reconstructed_columns"] = RECONSTRUCTED_COLUMNS
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


def _source_lines_from_span(span: Dict[str, Any]) -> List[int]:
    locator = span.get("locator")
    if not isinstance(locator, str):
        return []
    match = re.search(r"line:(\d+)", locator)
    return [int(match.group(1))] if match else []


def _strip_table_text(text: Optional[str]) -> Optional[str]:
    if not text:
        return text
    cleaned = re.sub(
        r"\n?\s*表１：原薬生産に対する本ガイドラインの適用.*$",
        "",
        text,
        flags=re.DOTALL,
    ).rstrip()
    return cleaned or None


def normalize_api_gmp_table1(
    root: Node,
    raw_lines: List[str],
    *,
    source_label: str,
    line_no_offset: int = 0,
) -> Dict[str, Any]:
    table = _find_table(raw_lines)
    if table is None:
        return {"applied": False}

    target: Optional[Node] = None
    for _parent, node in _walk_with_parent(root):
        if node.kind in {"chapter", "paragraph", "item", "subitem"} and "表１：原薬生産に対する本ガイドラインの適用" in (
            node.text or ""
        ):
            target = node
            break
    if target is None:
        return {"applied": False}

    start_line = table.caption_idx + line_no_offset + 1
    end_line = table.end_idx + line_no_offset
    target.text = _strip_table_text(target.text)
    target.source_spans = [
        span
        for span in target.source_spans
        if not any(start_line <= line <= end_line for line in _source_lines_from_span(span))
    ]
    target.children.append(_table_node(table, parent_nid=target.nid, source_label=source_label, line_no_offset=line_no_offset))
    return {"applied": True, "parent_nid": target.nid, "rows": len(table.raw_lines)}
