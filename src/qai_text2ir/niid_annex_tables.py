from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Optional, Tuple

from qai_xml2ir.models_ir import Node


PARSER_ID = "niid_annex_table_adapter"
TABLE_CONFIGS: Dict[str, Dict[str, Any]] = {
    "付表2": {
        "start_contains": "病原体等の",
        "columns": ["risk_group", "laboratory_bsl", "laboratory_purpose", "laboratory_practice_operation", "safety_equipment"],
        "source_format": "fixed_width_matrix",
    },
    "付表3": {
        "start_contains": "ＢＳＬ",
        "columns": ["criterion", "bsl1", "bsl2", "bsl3", "bsl4"],
        "source_format": "fixed_width_matrix",
    },
    "付表4": {
        "start_contains": "ＡＢＳＬ",
        "columns": ["absl", "laboratory_practice", "safety_equipment", "facility_criteria"],
        "source_format": "fixed_width_matrix",
    },
    "別表7": {
        "start_contains": "省令での記載項目",
        "columns": ["ordinance_item", "record_content", "pathogen_type_1", "pathogen_type_2", "pathogen_type_3"],
        "source_format": "fixed_width_matrix",
    },
    "別表10": {
        "start_contains": "省令での記載項目",
        "columns": ["ordinance_item", "specific_content", "regulation_reference"],
        "source_format": "fixed_width_comparison_table",
    },
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
        "decision": "promotion_candidate_as_raw_table",
        "promotion_mode": "table_raw_rows_with_column_schema",
        "reason": "multi-line wrapped cells cannot be safely split in v1, but the full table is preserved with source spans",
    },
    "付表3": {
        "decision": "promotion_candidate_as_partial_cell_table",
        "promotion_mode": "table_rows_with_partial_cells",
        "reason": "safe fixed-width rows are cell-split; remaining note/header rows are preserved raw",
    },
    "付表4": {
        "decision": "promotion_candidate_as_partial_cell_table",
        "promotion_mode": "table_rows_with_partial_cells",
        "reason": "ABSL start rows are cell-split; wrapped continuation rows are preserved raw",
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
        "decision": "promotion_candidate_as_raw_annex_text",
        "promotion_mode": "annex_text_raw_hold",
        "reason": "complex wide matrix is fully preserved as annex text; cell reconstruction is not required for readiness",
    },
    "別表5": {
        "decision": "promotion_candidate_as_raw_annex_text",
        "promotion_mode": "annex_text_raw_hold",
        "reason": "complex wide matrix is fully preserved as annex text; cell reconstruction is not required for readiness",
    },
    "別表6": {
        "decision": "promotion_candidate_as_numbered_annex_text",
        "promotion_mode": "annex_text",
        "reason": "numbered operational requirements are preserved as annex text; not a table target",
    },
    "別表7": {
        "decision": "promotion_candidate_as_partial_cell_table",
        "promotion_mode": "table_rows_with_partial_cells",
        "reason": "safe fixed-width rows are cell-split; wrapped record rows remain raw",
    },
    "別表8": {
        "decision": "promotion_candidate_as_raw_annex_text",
        "promotion_mode": "annex_text_raw_hold",
        "reason": "embedded item table is fully preserved as annex text; cell reconstruction is not required for readiness",
    },
    "別表9": {
        "decision": "promotion_candidate_as_numbered_annex_text",
        "promotion_mode": "annex_text",
        "reason": "disaster response requirements are preserved as numbered annex text; not a table target",
    },
    "別表10": {
        "decision": "promotion_candidate_as_partial_cell_table",
        "promotion_mode": "table_rows_with_partial_cells",
        "reason": "safe comparison rows are cell-split; wrapped rows remain raw",
    },
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
    _apply_cell_reconstruction_v1(table, columns)
    return table


def _normalize_annex_table(annex: Node, *, source_label: str) -> Optional[Dict[str, Any]]:
    if annex.num not in TABLE_CONFIGS:
        return None
    config = TABLE_CONFIGS[str(annex.num)]
    lines = _content_lines(annex)
    if not lines:
        return None
    start_idx = _find_table_start(lines, str(config["start_contains"]))
    preamble = lines[:start_idx]
    table_lines = [line for line in lines[start_idx:] if not _is_page_marker(line)]
    if not table_lines:
        return None
    annex.data["original_text_before_table_adapter"] = annex.text
    annex.data["table_adapter"] = PARSER_ID
    annex.data["table_adapter_status"] = "table_node_created_raw_rows"
    annex.text = "\n\n".join(preamble) or None
    annex.children.append(
        _table_node(
            annex,
            table_lines=table_lines,
            start_idx=start_idx,
            source_label=source_label,
            columns=list(config["columns"]),
            source_format=str(config["source_format"]),
        )
    )
    return {"annex_num": annex.num, "rows": len(table_lines), "columns": list(config["columns"])}


def _apply_readiness_decision(annex: Node) -> None:
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
