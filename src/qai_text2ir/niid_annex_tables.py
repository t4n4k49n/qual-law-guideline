from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Optional, Tuple

from qai_xml2ir.models_ir import Node

from .niid_visual_reviewed_tables import VISUAL_REVIEW_PARSER, VISUAL_REVIEWED_TABLES


PARSER_ID = "niid_annex_table_adapter"
TABLE_CONFIGS: Dict[str, Dict[str, Any]] = {
    "付表2": {
        "start_contains": "実験室の BSL",
        "columns": ["risk_group", "laboratory_bsl", "laboratory_purpose", "laboratory_practice_operation", "safety_equipment"],
        "source_format": "fixed_width_matrix",
    },
    "付表3": {
        "start_contains": "ＢＳＬ",
        "columns": ["criterion", "parent_criterion", "bsl1", "bsl2", "bsl3", "bsl4"],
        "fixed_width_columns": ["criterion", "bsl1", "bsl2", "bsl3", "bsl4"],
        "source_format": "fixed_width_matrix",
    },
    "付表4": {
        "start_contains": "ＡＢＳＬ",
        "columns": ["absl", "laboratory_practice", "safety_equipment", "facility_criteria"],
        "source_format": "fixed_width_matrix",
    },
    "別表7": {
        "start_contains": "省令での記載項目",
        "columns": ["category", "ordinance_item", "record_content", "pathogen_type_1", "pathogen_type_2", "pathogen_type_3"],
        "fixed_width_columns": ["ordinance_item", "record_content", "pathogen_type_1", "pathogen_type_2", "pathogen_type_3"],
        "source_format": "fixed_width_matrix",
    },
    "別表4": {
        "start_contains": "対象病原体等ＢＳＬ",
        "columns": ["section", "criterion", "type1_bsl4", "type2_bsl3", "type2_bsl2", "type3_bsl3", "type3_bsl2", "type4_bsl3", "type4_bsl2"],
        "source_format": "fixed_width_matrix",
    },
    "別表5": {
        "start_contains": "対象病原体等ＢＳＬ",
        "columns": ["section", "criterion", "type1_bsl4", "type2_bsl3", "type2_bsl2", "type3_bsl3", "type3_bsl2", "type4_bsl3", "type4_bsl2"],
        "source_format": "fixed_width_matrix",
    },
    "別表8": {
        "start_contains": "省令での記載項目",
        "columns": ["work_category", "target_person", "ordinance_item", "frequency", "remarks"],
        "source_format": "fixed_width_matrix",
    },
    "別表10": {
        "start_contains": "省令での記載項目",
        "columns": ["category", "ordinance_item", "specific_content", "regulation_reference"],
        "fixed_width_columns": ["ordinance_item", "specific_content", "regulation_reference"],
        "source_format": "fixed_width_comparison_table",
    },
}
DISPLAY_COLUMNS_BY_NUM: Dict[str, List[str]] = {
    "付表2": ["病原体等のリスク群", "実験室のBSL", "実験室の使用目的", "実験手技及び運用", "実験室の安全機器"],
    "付表3": ["criterion", "parent", "BSL1", "BSL2", "BSL3", "BSL4"],
    "付表4": ["ABSL", "実験手技", "安全機器", "設備基準"],
    "別表4": ["大項目", "小項目", "1種 BSL4", "2種 BSL3", "2種 BSL2", "3種 BSL3", "3種 BSL2", "4種 BSL3", "4種 BSL2"],
    "別表5": ["大項目", "小項目", "1種 BSL4", "2種 BSL3", "2種 BSL2", "3種 BSL3", "3種 BSL2", "4種 BSL3", "4種 BSL2"],
    "別表7": ["category", "省令での記載項目", "記帳の内容", "1種病原体等", "2種病原体等", "3種病原体等"],
    "別表8": ["業務区分", "対象者", "省令での記載項目", "回数等", "備考"],
    "別表10": ["category", "省令での記載項目", "具体的内容", "国立感染症研究所病原体等安全管理規程における該当部分"],
}
READINESS_BY_NUM: Dict[str, Dict[str, str]] = {
    "別表1": {
        "decision": "promotion_candidate_as_annex_text",
        "promotion_mode": "annex_text",
        "reason": "narrative reference text; table reconstruction is not applicable",
    },
    "付表1-1": {
        "decision": "promotion_candidate_as_annex_text",
        "promotion_mode": "annex_text",
        "reason": "risk group description text; table reconstruction is not applicable",
    },
    "付表1-2": {
        "decision": "promotion_candidate_as_numbered_annex_text",
        "promotion_mode": "annex_text_with_existing_subitems",
        "reason": "numbered assessment items are preserved as annex text/subitems; no table reconstruction needed",
    },
    "付表1-3": {
        "decision": "promotion_candidate_as_numbered_annex_text",
        "promotion_mode": "annex_text_with_existing_subitems",
        "reason": "animal experiment risk assessment items are preserved as annex text/subitems; no table reconstruction needed",
    },
    "付表2": {
        "decision": "promotion_candidate_as_visual_reviewed_table",
        "promotion_mode": "visual_reviewed_table_records",
        "reason": "PDF image visual review restored wrapped cells into reviewed table records",
    },
    "付表3": {
        "decision": "promotion_candidate_as_visual_reviewed_table",
        "promotion_mode": "visual_reviewed_table_records",
        "reason": "PDF image visual review restored BSL header, parent criteria, and footnote-bearing values",
    },
    "付表4": {
        "decision": "promotion_candidate_as_visual_reviewed_table",
        "promotion_mode": "visual_reviewed_table_records",
        "reason": "PDF image visual review restored ABSL rows and multi-line cells into reviewed records",
    },
    "別表2": {
        "decision": "promotion_candidate_as_sectioned_annex_text",
        "promotion_mode": "annex_text",
        "reason": "BSL criteria are section-style text, not a column reconstruction target",
    },
    "別表3": {
        "decision": "promotion_candidate_as_sectioned_annex_text",
        "promotion_mode": "annex_text",
        "reason": "ABSL criteria are section-style text, not a column reconstruction target",
    },
    "別表4": {
        "decision": "promotion_candidate_as_visual_reviewed_table",
        "promotion_mode": "visual_reviewed_table_records",
        "reason": "PDF text visual review restored the wide matrix into reviewed table records",
    },
    "別表5": {
        "decision": "promotion_candidate_as_visual_reviewed_table",
        "promotion_mode": "visual_reviewed_table_records",
        "reason": "PDF text visual review restored the wide matrix into reviewed table records",
    },
    "別表6": {
        "decision": "promotion_candidate_as_numbered_annex_text",
        "promotion_mode": "annex_text",
        "reason": "numbered operational requirements are preserved as annex text; not a table target",
    },
    "別表7": {
        "decision": "promotion_candidate_as_visual_reviewed_table",
        "promotion_mode": "visual_reviewed_table_records",
        "reason": "PDF image visual review restored row-spanned categories and wrapped cells into reviewed records",
    },
    "別表8": {
        "decision": "promotion_candidate_as_visual_reviewed_table",
        "promotion_mode": "visual_reviewed_table_records",
        "reason": "PDF text visual review restored the education/training matrix into reviewed table records",
    },
    "別表9": {
        "decision": "promotion_candidate_as_numbered_annex_text",
        "promotion_mode": "annex_text",
        "reason": "disaster response requirements are preserved as numbered annex text; not a table target",
    },
    "別表10": {
        "decision": "promotion_candidate_as_visual_reviewed_table",
        "promotion_mode": "visual_reviewed_table_records",
        "reason": "PDF image visual review restored row-spanned categories and comparison cells into reviewed records",
    },
}
HEADING_BY_NUM: Dict[str, str] = {
    "付表2": "病原体等のリスク群分類と、実験室のＢＳＬ分類、実験室使用目的、実験手技及び安全機器との関連性",
    "付表3": "ＢＳＬ実験室の安全設備基準",
    "付表4": "病原体等取扱動物実験施設のＡＢＳＬ分類、実験手技、安全機器及び設備基準",
    "別表4": "国立感染症研究所における施設の位置、構造及び設備の技術上の基準一覧",
    "別表5": "国立感染症研究所における特定病原体等の保管等の技術上の基準一覧",
    "別表7": "記帳事項に関する一覧（法第５６条の２３関係）",
    "別表8": "特定病原体等の取扱いに必要な教育訓練（法第５６条の２１関係）",
    "別表10": "感染症発生予防規程対照表（法第５６条の１８関係）",
}


def _split_fixed_width_cells(line: str) -> List[str]:
    return [cell.strip() for cell in re.split(r"\s{2,}", line.strip()) if cell.strip()]


def _apply_cell_reconstruction_v1(table: Node, columns: List[str]) -> Dict[str, int]:
    reconstructed = 0
    deferred = 0
    for header in table.children:
        if header.kind != "table_header":
            continue
        header.data["cell_reconstruction"] = "fixed_width_cells_v1"
        header.data["columns"] = columns
        for row in header.children:
            if row.kind != "table_row":
                continue
            raw_line = str(row.data.get("raw_line") or row.text or "")
            cells = _split_fixed_width_cells(raw_line)
            if len(cells) == len(columns):
                row.data["cells"] = cells
                row.data["columns"] = columns
                row.data["cell_reconstruction"] = "fixed_width_cells_v1"
                row.data.pop("column_reconstruction_warning", None)
                reconstructed += 1
            else:
                row.data["cell_reconstruction"] = "deferred"
                row.data["column_reconstruction_warning"] = "fixed_width_cell_split_deferred"
                row.data["cell_reconstruction_deferred_reason"] = f"split_count={len(cells)} expected={len(columns)}"
                deferred += 1
    table.data["cell_reconstruction"] = "fixed_width_cells_v1"
    table.data["cell_reconstruction_status"] = "partial"
    table.data["cell_reconstructed_rows"] = reconstructed
    table.data["cell_deferred_rows"] = deferred
    return {"reconstructed": reconstructed, "deferred": deferred}


def _apply_visual_reviewed_records(table: Node, annex_num: str, source_span: Dict[str, Any]) -> bool:
    reviewed = VISUAL_REVIEWED_TABLES.get(annex_num)
    if not reviewed:
        return False
    columns = list(reviewed["columns"])
    records = list(reviewed["records"])
    original_headers = table.children
    table.data["raw_table_audit"] = {
        "source_format": table.data.get("source_format"),
        "raw_lines": table.data.get("raw_lines", []),
        "fixed_width_cell_reconstructed_rows": table.data.get("cell_reconstructed_rows", 0),
        "fixed_width_cell_deferred_rows": table.data.get("cell_deferred_rows", 0),
    }
    table.data["table_adapter"] = PARSER_ID
    table.data["visual_review_parser"] = VISUAL_REVIEW_PARSER
    table.data["column_reconstruction"] = "visual_reviewed_cells"
    table.data["column_reconstruction_status"] = "complete"
    table.data["cell_reconstruction"] = "visual_reviewed_cells"
    table.data["cell_reconstruction_status"] = "complete"
    table.data["cell_reconstructed_rows"] = len(records)
    table.data["cell_deferred_rows"] = 0
    table.data["reconstructed_columns"] = columns
    table.data["visual_review_source_runs"] = [
        "runs/20260526-100829653_feat-niid-visual-table-review-v1/visual_reconstruction.json",
        "runs/20260526-112428711_feat-niid-visual-table-review-v2/visual_reconstruction.json",
    ]
    header = _make_node(
        nid=f"{table.nid}.tblh_visual",
        kind="table_header",
        kind_raw="table_header",
        num=None,
        heading=None,
        text=" | ".join(DISPLAY_COLUMNS_BY_NUM.get(annex_num, columns)),
        source_span=source_span,
        role="structural",
        data={
            "columns": columns,
            "display_columns": DISPLAY_COLUMNS_BY_NUM.get(annex_num, columns),
            "reconstructed_columns": columns,
            "cell_reconstruction": "visual_reviewed_cells",
            "supersedes_headers": [child.nid for child in original_headers],
        },
    )
    for row_no, record in enumerate(records, start=1):
        normalized_record = dict(record)
        if "section" in columns and "section" not in normalized_record:
            normalized_record["section"] = str(record.get("category", ""))
        cells = [str(normalized_record.get(column, "")) for column in columns]
        header.children.append(
            _make_node(
                nid=f"{header.nid}.tblr{row_no}",
                kind="table_row",
                kind_raw="table_row",
                num=str(row_no),
                heading=None,
                text=" | ".join(cells),
                source_span=source_span,
                data={
                    "cells": cells,
                    "columns": columns,
                    "record": {column: normalized_record.get(column, "") for column in columns},
                    "cell_reconstruction": "visual_reviewed_cells",
                    "visual_reviewed": True,
                },
            )
        )
    for note_no, note in enumerate(reviewed.get("notes", []), start=1):
        table.children.append(
            _make_node(
                nid=f"{table.nid}.note{note_no}",
                kind="note",
                kind_raw="note",
                num=str(note_no),
                heading=str(note.get("mark", "")),
                text=str(note.get("text", "")),
                source_span=source_span,
                role="informative",
                data={"visual_reviewed": True},
            )
        )
    table.children = [header, *[child for child in table.children if child.kind == "note"]]
    return True


def _line_span(source_label: str, fallback_line_no: int) -> Dict[str, str]:
    return {"source_label": source_label, "locator": f"line:{fallback_line_no}"}


def _make_node(
    *,
    nid: str,
    kind: str,
    kind_raw: Optional[str],
    num: Optional[str],
    heading: Optional[str],
    text: Optional[str],
    source_span: Dict[str, Any],
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
        source_spans=[source_span],
        data=data or {},
    )


def _walk(node: Node, parent: Optional[Node] = None) -> Iterable[Tuple[Optional[Node], Node]]:
    yield parent, node
    for child in node.children:
        yield from _walk(child, node)


def _content_lines(annex: Node) -> List[str]:
    return [line.rstrip() for line in (annex.text or "").splitlines() if line.strip()]


def _is_page_marker(line: str) -> bool:
    return bool(re.fullmatch(r"\s*-+\s*\d+\s*-+\s*", line))


def _find_table_start(lines: List[str], needle: str) -> int:
    for idx, line in enumerate(lines):
        if needle in line:
            return idx
    return 0


def _span_for_line(annex: Node, line_idx: int, source_label: str) -> Dict[str, Any]:
    if line_idx < len(annex.source_spans):
        return dict(annex.source_spans[line_idx])
    return _line_span(source_label, 1)


def _node_source_line(node: Node) -> int:
    for span in node.source_spans or []:
        locator = str(span.get("locator") or "")
        match = re.search(r"line:(\d+)", locator)
        if match:
            return int(match.group(1))
    return 10**9


def _is_orphan_marker_note(node: Node) -> bool:
    if node.kind != "note":
        return False
    return (node.text or "").strip() in {"•", "・", "○"}


def _table_node(
    annex: Node,
    *,
    table_lines: List[str],
    start_idx: int,
    source_label: str,
    columns: List[str],
    source_format: str,
) -> Node:
    table_nid = f"{annex.nid}.tbl1"
    first_span = _span_for_line(annex, start_idx, source_label)
    table = _make_node(
        nid=table_nid,
        kind="table",
        kind_raw="table",
        num="1",
        heading=annex.heading,
        text=None,
        source_span=first_span,
        role="structural",
        data={
            "parser": PARSER_ID,
            "annex_num": annex.num,
            "source_format": source_format,
            "column_reconstruction": "raw_rows_with_column_schema",
            "column_reconstruction_status": "partial",
            "reconstructed_columns": columns,
            "raw_lines": table_lines,
        },
    )
    header = _make_node(
        nid=f"{table_nid}.tblh",
        kind="table_header",
        kind_raw="table_header",
        num=None,
        heading=None,
        text="raw_line",
        source_span=first_span,
        role="structural",
        data={"columns": ["raw_line"], "reconstructed_columns": columns},
    )
    table.children.append(header)
    for row_no, line in enumerate(table_lines, start=1):
        line_idx = start_idx + row_no - 1
        header.children.append(
            _make_node(
                nid=f"{header.nid}.tblr{row_no}",
                kind="table_row",
                kind_raw="table_row",
                num=str(row_no),
                heading=None,
                text=line.strip(),
                source_span=_span_for_line(annex, line_idx, source_label),
                data={
                    "cells": [line.strip()],
                    "raw_line": line.strip(),
                    "column_reconstruction_warning": "raw_row_only_cell_reconstruction_pending",
                },
            )
        )
    _apply_cell_reconstruction_v1(table, list(TABLE_CONFIGS[str(annex.num)].get("fixed_width_columns", columns)))
    _apply_visual_reviewed_records(table, str(annex.num), first_span)
    return table


def _normalize_annex_table(annex: Node, *, source_label: str) -> Optional[Dict[str, Any]]:
    if annex.num not in TABLE_CONFIGS:
        return None
    if annex.num in HEADING_BY_NUM:
        annex.heading = HEADING_BY_NUM[str(annex.num)]
    config = TABLE_CONFIGS[str(annex.num)]
    lines = _content_lines(annex)
    if not lines:
        return None
    start_idx = _find_table_start(lines, str(config["start_contains"]))
    preamble = lines[:start_idx]
    if preamble and annex.heading and str(annex.heading).endswith(preamble[0].strip()):
        preamble = preamble[1:]
    table_lines = [line for line in lines[start_idx:] if not _is_page_marker(line)]
    if not table_lines:
        return None
    annex.data["original_text_before_table_adapter"] = annex.text
    annex.data["table_adapter"] = PARSER_ID
    annex.data["table_adapter_status"] = "table_node_created_raw_rows"
    annex.text = "\n\n".join(preamble) or None
    table_node = _table_node(
        annex,
        table_lines=table_lines,
        start_idx=start_idx,
        source_label=source_label,
        columns=list(config["columns"]),
        source_format=str(config["source_format"]),
    )
    if annex.num in {"別表4", "別表5"} and table_node.data.get("visual_review_parser"):
        annex.text = None
    retained_children = [
        child
        for child in annex.children
        if child.kind in {"note", "history"} and not _is_orphan_marker_note(child)
    ]
    annex.children = sorted([*retained_children, table_node], key=_node_source_line)
    return {"annex_num": annex.num, "rows": len(table_lines), "columns": list(config["columns"])}


def _apply_readiness_decision(annex: Node) -> None:
    if (
        annex.num == "別表1"
        and annex.heading
        and annex.heading.startswith("病原体等の取扱いにおいては")
    ):
        heading_text = annex.heading.rstrip()
        body_text = (annex.text or "").lstrip()
        annex.heading = None
        annex.text = f"{heading_text}{body_text}" if body_text else heading_text
    if annex.num in HEADING_BY_NUM:
        annex.heading = HEADING_BY_NUM[str(annex.num)]
    if annex.num not in READINESS_BY_NUM:
        return
    decision = READINESS_BY_NUM[str(annex.num)]
    annex.data["normalization_readiness"] = {
        **decision,
        "status": "ready_for_readiness_review",
    }
    for child in annex.children:
        if child.kind == "table" and child.data.get("parser") == PARSER_ID:
            child.data["normalization_readiness"] = {
                **decision,
                "status": "ready_for_readiness_review",
            }
    if decision.get("promotion_mode") == "annex_text_raw_hold":
        annex.children = [child for child in annex.children if child.kind in {"note", "history"}]


def normalize_niid_annex_tables(root: Node, *, source_label: str) -> Dict[str, Any]:
    applied: List[Dict[str, Any]] = []
    for _parent, node in _walk(root):
        if node.kind != "annex":
            continue
        result = _normalize_annex_table(node, source_label=source_label)
        if result is not None:
            applied.append(result)
        _apply_readiness_decision(node)
    return {"applied": bool(applied), "tables": applied}
