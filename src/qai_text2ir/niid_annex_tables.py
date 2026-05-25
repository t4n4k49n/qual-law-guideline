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


def normalize_niid_annex_tables(root: Node, *, source_label: str) -> Dict[str, Any]:
    applied: List[Dict[str, Any]] = []
    for _parent, node in _walk(root):
        if node.kind != "annex":
            continue
        result = _normalize_annex_table(node, source_label=source_label)
        if result is not None:
            applied.append(result)
    return {"applied": bool(applied), "tables": applied}
