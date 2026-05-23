from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

from qai_xml2ir.models_ir import Node


CAPTION_RE = re.compile(r"^\s*Table\s+1:\s+Application of this Guide to API Manufacturing\s*$", re.IGNORECASE)
NEXT_CHAPTER_RE = re.compile(r"^\s*2\.\s+QUALITY MANAGEMENT\s*$", re.IGNORECASE)


@dataclass
class Part2Table1:
    caption_idx: int
    end_idx: int
    raw_lines: List[str]


COLUMNS = [
    "Type of Manufacturing",
    "Step 1",
    "Step 2",
    "Step 3",
    "Step 4",
    "Step 5",
]

ROWS = [
    [
        "Chemical Manufacturing",
        "Production of the API Starting Material",
        "Introduction of the API Starting Material into process",
        "Production of Intermediate(s)",
        "Isolation and purification",
        "Physical processing, and packaging",
    ],
    [
        "API derived from animal sources",
        "Collection of organ, fluid, or tissue",
        "Cutting, mixing, and/or initial processing",
        "Introduction of the API Starting Material into process",
        "Isolation and purification",
        "Physical processing, and packaging",
    ],
    [
        "API extracted from plant sources",
        "Collection of plant",
        "Cutting and initial extraction(s)",
        "Introduction of the API Starting Material into process",
        "Isolation and purification",
        "Physical processing, and packaging",
    ],
    [
        "Herbal extracts used as API",
        "Collection of plants",
        "Cutting and initial extraction",
        "",
        "Further extraction",
        "Physical processing, and packaging",
    ],
    [
        "API consisting of comminuted or powdered herbs",
        "Collection of plants and/or cultivation and harvesting",
        "Cutting/comminuting",
        "",
        "",
        "Physical processing, and packaging",
    ],
    [
        "Biotechnology: fermentation / cell culture",
        "Establishment of master cell bank and working cell bank",
        "Maintenance of working cell bank",
        "Cell culture and/or fermentation",
        "Isolation and purification",
        "Physical processing, and packaging",
    ],
    [
        "Classical Fermentation to produce an API",
        "Establishment of cell bank",
        "Maintenance of the cell bank",
        "Introduction of the cells into fermentation",
        "Isolation and purification",
        "Physical processing, and packaging",
    ],
]

ROW_LINE_HINTS = [
    "Chemical",
    "API derived",
    "API extracted",
    "Herbal extracts",
    "API consisting",
    "Biotechnology:",
    "Fermentation to",
]


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


def _find_table(lines: List[str]) -> Optional[Part2Table1]:
    caption_idx = next((idx for idx, line in enumerate(lines) if CAPTION_RE.match(line)), None)
    if caption_idx is None:
        return None
    end_idx = next((idx for idx in range(caption_idx + 1, len(lines)) if NEXT_CHAPTER_RE.match(lines[idx])), len(lines))
    return Part2Table1(caption_idx=caption_idx, end_idx=end_idx, raw_lines=lines[caption_idx:end_idx])


def _find_line_containing(lines: List[str], start: int, end: int, needle: str) -> int:
    lowered = needle.lower()
    for idx in range(start, min(end, len(lines))):
        if lowered in lines[idx].lower():
            return idx
    return start


def _table_node(table: Part2Table1, *, parent_nid: str, source_label: str, line_no_offset: int) -> Node:
    table_nid = f"{parent_nid}.tbl1"
    node = _make_node(
        nid=table_nid,
        kind="table",
        kind_raw="table",
        num="1",
        heading="Table 1: Application of this Guide to API Manufacturing",
        text=None,
        source_label=source_label,
        line_idx=table.caption_idx + line_no_offset,
        role="structural",
        data={
            "parser": "pics_part2_api_table1",
            "table_no": "1",
            "source_format": "fixed_width",
            "shading_reconstructed": False,
            "note": "Grey shading in the source PDF may not be recoverable from text layer.",
            "raw_lines": table.raw_lines,
        },
    )
    header = _make_node(
        nid=f"{table_nid}.tblh",
        kind="table_header",
        kind_raw="table_header",
        num=None,
        heading=None,
        text=" | ".join(COLUMNS),
        source_label=source_label,
        line_idx=table.caption_idx + line_no_offset,
        role="structural",
        data={"columns": COLUMNS},
    )
    node.children.append(header)
    for row_no, cells in enumerate(ROWS, start=1):
        line_idx = _find_line_containing(
            table.raw_lines,
            0,
            len(table.raw_lines),
            ROW_LINE_HINTS[row_no - 1],
        )
        row_node = _make_node(
            nid=f"{header.nid}.tblr{row_no}",
            kind="table_row",
            kind_raw="table_row",
            num=str(row_no),
            heading=None,
            text=" | ".join(cells),
            source_label=source_label,
            line_idx=table.caption_idx + line_idx + line_no_offset,
            data={"cells": cells, "manufacturing_type": cells[0]},
        )
        header.children.append(row_node)
    note_idx = _find_line_containing(table.raw_lines, 0, len(table.raw_lines), "Increasing GMP requirements")
    node.children.append(
        _make_node(
            nid=f"{table_nid}.not1",
            kind="note",
            kind_raw="note",
            num="1",
            heading=None,
            text="Increasing GMP requirements",
            source_label=source_label,
            line_idx=table.caption_idx + note_idx + line_no_offset,
            role="informative",
            data={"note_type": "table_annotation", "table_no": "1"},
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
        r"\n?\s*Table\s+1:\s+Application of this Guide to API Manufacturing.*$",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    ).rstrip()
    cleaned = re.sub(r"\n?\s*Introduction\s*$", "", cleaned, flags=re.IGNORECASE).rstrip()
    return cleaned or None


def normalize_pics_part2_table1(
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
        if node.kind in {"chapter", "section", "paragraph", "item", "subitem"} and "Table 1:" in (node.text or ""):
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
    return {"applied": True, "parent_nid": target.nid, "rows": len(ROWS)}
