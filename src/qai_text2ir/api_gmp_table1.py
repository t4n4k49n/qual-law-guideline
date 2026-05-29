from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

from qai_xml2ir.models_ir import Node


CAPTION_RE = re.compile(r"^\s*表１：原薬生産に対する本ガイドラインの適用\s*$")
NEXT_CHAPTER_RE = re.compile(r"^\s*2[．.]\s+品質マネージメント\s*$")
RECONSTRUCTED_COLUMNS = [
    "production_type",
    "process_example_step_1",
    "process_example_step_2",
    "process_example_step_3",
    "process_example_step_4",
    "process_example_step_5",
]
SPANNING_PROCESS_HEADER = "形態ごとの生産工程の事例"
RECONSTRUCTED_COLUMN_LABELS = [
    "生産形態",
    f"{SPANNING_PROCESS_HEADER} STEP 1",
    f"{SPANNING_PROCESS_HEADER} STEP 2",
    f"{SPANNING_PROCESS_HEADER} STEP 3",
    f"{SPANNING_PROCESS_HEADER} STEP 4",
    f"{SPANNING_PROCESS_HEADER} STEP 5",
]
RECONSTRUCTED_STAGE_LABELS = [
    None,
    "原薬出発物質の製造",
    "原薬出発物質の工程への導入又は初期加工処理",
    "中間体の製造又は同等工程",
    "分離及び精製又は再抽出",
    "物理的加工処理及び包装",
]
RECONSTRUCTED_RECORDS = [
    {
        "record_id": "api_gmp_table1.r1",
        "raw_row_nums": [3, 4, 5],
        "guideline_applicable": [False, True, True, True, True],
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
        "guideline_applicable": [False, False, True, True, True],
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
        "guideline_applicable": [False, False, True, True, True],
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
        "guideline_applicable": [False, False, False, True, True],
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
        "guideline_applicable": [False, False, False, False, True],
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
        "guideline_applicable": [False, True, True, True, True],
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
        "guideline_applicable": [False, True, True, True, True],
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
    "candidate_granularity": "visual_reconstructed_table_row",
    "table_row_promotion": "promoted",
    "table_row_promotion_reason": "PDF visual review restored the 6-column by 7-row table structure",
    "note_handling": "directional_note_kept_on_table_data",
    "visual_information": "gray cells are represented by per-stage guideline_applicable flags",
    "reviewed_records": 7,
    "deferred_raw_rows": [],
    "visual_source": {
        "pdf": "data/human-readable/pmda/api_gmp_guideline/000156438.pdf",
        "page": 8,
        "basis": "PDF visual review of Table 1 gray cells and grid",
    },
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
            "source_format": "pdf_visual_review_plus_ragged_text",
            "column_reconstruction": "visual_reviewed",
            "column_reconstruction_status": "complete_for_table1",
            "columns": RECONSTRUCTED_COLUMNS,
            "column_labels": RECONSTRUCTED_COLUMN_LABELS,
            "header_structure": {
                "spanning_headers": [
                    {
                        "label": SPANNING_PROCESS_HEADER,
                        "columns": RECONSTRUCTED_COLUMNS[1:],
                        "column_range": [1, 5],
                    }
                ],
                "leaf_stage_labels": RECONSTRUCTED_STAGE_LABELS,
                "flattening_rule": "repeat spanning header into STEP 1..5 column labels and keep PDF leaf labels as stage_labels",
            },
            "raw_lines": table.raw_lines,
            "record_review": RECORD_REVIEW,
            "visual_notes": [
                {
                    "text": "灰色部分：本ガイドラインを適用する工程",
                    "meaning": "guideline_applicable=true",
                },
                {
                    "text": "ＧＭＰ要求事項の増大",
                    "meaning": "requirements increase from earlier to later process stages",
                    "direction": "left_to_right",
                },
            ],
            "non_data_raw_rows": [
                {"raw_row_num": 1, "reason": "header_line"},
                {"raw_row_num": 2, "reason": "visual_annotation"},
                {"raw_row_num": 26, "reason": "directional_note_without_cells"},
            ],
            "reconstructed_records": RECONSTRUCTED_RECORDS,
            "review_status": "visual_reviewed",
            "review_limitation": "cell text is normalized from PDF visual review and source text lines; it is not an automated OCR extraction",
        },
    )
    header = _make_node(
        nid=f"{table_nid}.tblh",
        kind="table_header",
        kind_raw="table_header",
        num=None,
        heading=None,
        text=" | ".join(RECONSTRUCTED_COLUMN_LABELS),
        source_label=source_label,
        line_idx=table.caption_idx + line_no_offset,
        role="structural",
        data={
            "columns": RECONSTRUCTED_COLUMNS,
            "column_labels": RECONSTRUCTED_COLUMN_LABELS,
            "stage_labels": RECONSTRUCTED_STAGE_LABELS,
            "spanning_headers": [
                {
                    "label": SPANNING_PROCESS_HEADER,
                    "columns": RECONSTRUCTED_COLUMNS[1:],
                    "column_range": [1, 5],
                }
            ],
        },
    )
    node.children.append(header)
    first_data_line_idx = table.raw_line_indexes[2] if len(table.raw_line_indexes) > 2 else table.caption_idx
    for row_no, record in enumerate(RECONSTRUCTED_RECORDS, start=1):
        raw_row_nums = list(record["raw_row_nums"])
        raw_lines = [table.raw_lines[i - 1] for i in raw_row_nums if 0 <= i - 1 < len(table.raw_lines)]
        raw_indexes = [table.raw_line_indexes[i - 1] for i in raw_row_nums if 0 <= i - 1 < len(table.raw_line_indexes)]
        line_idx = raw_indexes[0] if raw_indexes else first_data_line_idx
        guideline_applicable = list(record["guideline_applicable"])
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
                    "columns": RECONSTRUCTED_COLUMNS,
                    "column_labels": RECONSTRUCTED_COLUMN_LABELS,
                    "stage_labels": RECONSTRUCTED_STAGE_LABELS,
                    "raw_row_nums": raw_row_nums,
                    "raw_lines": raw_lines,
                    "guideline_applicable": guideline_applicable,
                    "guideline_applicable_columns": [
                        column
                        for column, applies in zip(RECONSTRUCTED_COLUMNS[1:], guideline_applicable)
                        if applies
                    ],
                    "visual_fill": [
                        "not_applicable",
                        *["gray" if applies else "white" for applies in guideline_applicable],
                    ],
                    "visual_review_status": "reviewed_candidate",
                    "source_basis": "PDF page 8 visual table and source text table lines",
                },
            )
        )
    return node


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
        if node.kind in {"chapter", "section", "paragraph", "item", "subitem"} and "表１：原薬生産に対する本ガイドラインの適用" in (
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
