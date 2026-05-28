from __future__ import annotations

import re
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

from qai_xml2ir.models_ir import Node


CAPTION_RE = re.compile(r"^\s*Table\s+(?P<num>[1-6])\s*[:.]\s*(?P<title>.*\S)\s*$", re.IGNORECASE)
PARA_RE = re.compile(r"^\s*\d{1,2}\.\d+\s+")
PAGE_RE = re.compile(r"^\s*PE\s+009-17\s+\(Annexes\)(?:\s|$)")
ANNEX_HEADER_RE = re.compile(r"^\s*Annex\s+1\s+Manufacture\s+of\s+sterile\s+medicinal\s+products\s*$", re.IGNORECASE)
NOTE_START_RE = re.compile(r"^\s*(?:\([a-c]\)|[a-c]\)|Note\s+\d+\s*:)", re.IGNORECASE)
GRADE_RE = re.compile(r"^\s*(?:Grade\s+)?([ABCD])\b")


@dataclass
class Annex1Table:
    table_no: str
    caption: str
    caption_idx: int
    end_idx: int
    columns: List[str]
    rows: List[Dict[str, Any]]
    notes: List[Dict[str, Any]]
    raw_lines: List[str]


VISUAL_REVIEW_SOURCE_RUN = "runs/20260528-160046554_feat-pics-annex1-table-visual-review-v1/visual_reconstruction.json"
VISUAL_REVIEW_PARSER = "pics_annex1_visual_review_v1"

_PARTICLE_HEADER_GROUPS = [
    {
        "label": "Maximum limits for total particle >= 0.5 um/m3",
        "columns": [1, 2],
        "subcolumns": ["at rest", "in operation"],
    },
    {
        "label": "Maximum limits for total particle >= 5 um/m3",
        "columns": [3, 4],
        "subcolumns": ["at rest", "in operation"],
    },
]

VISUAL_REVIEW_BY_TABLE: Dict[str, Dict[str, Any]] = {
    "1": {
        "source_pages": ["source_pages/annex1_tables_p19_20-020.png"],
        "cell_reconstruction": "visual_reviewed_cells",
        "cell_reconstruction_status": "complete",
        "header_groups": _PARTICLE_HEADER_GROUPS,
        "merged_cells": [
            {"type": "column_span", "row": "header", "columns": [1, 2], "expanded": False},
            {"type": "column_span", "row": "header", "columns": [3, 4], "expanded": False},
        ],
        "visual_features": [
            "Two-tier particle-size headers span the at-rest and in-operation subcolumns.",
            "Grade D has wrapped cell text for both in-operation limits; each wrapped cell is one logical value.",
        ],
        "row_review": [
            {"record_id": "t1.r1", "visual_row": "A", "status": "checked"},
            {"record_id": "t1.r2", "visual_row": "B", "status": "checked"},
            {"record_id": "t1.r3", "visual_row": "C", "status": "checked"},
            {"record_id": "t1.r4", "visual_row": "D", "status": "checked", "wrapped_cells": [2, 4]},
        ],
    },
    "2": {
        "source_pages": ["source_pages/annex1_tables_p21-021.png"],
        "cell_reconstruction": "visual_reviewed_cells",
        "cell_reconstruction_status": "complete",
        "merged_cells": [
            {
                "type": "column_span",
                "row": "A",
                "columns": [1, 2, 3],
                "text": "No growth",
                "expanded": True,
            }
        ],
        "visual_features": [
            "Grade A has one horizontally merged No growth cell across all three monitoring-method columns.",
        ],
        "row_review": [
            {"record_id": "t2.r1", "visual_row": "A", "status": "checked", "expanded_merged_cells": [1, 2, 3]},
            {"record_id": "t2.r2", "visual_row": "B", "status": "checked"},
            {"record_id": "t2.r3", "visual_row": "C", "status": "checked"},
            {"record_id": "t2.r4", "visual_row": "D", "status": "checked"},
        ],
    },
    "3": {
        "source_pages": ["source_pages/annex1_tables_p30_31-031.png"],
        "cell_reconstruction": "visual_reviewed_cells",
        "cell_reconstruction_status": "complete",
        "merged_cells": [
            {"type": "row_span", "column": 0, "rows": [2, 3], "text": "Grade C", "expanded": True}
        ],
        "visual_features": [
            "Grade C spans two operation rows and is expanded into two logical records.",
        ],
        "row_review": [
            {"record_id": "t3.r1", "visual_row": "Grade A/1", "status": "checked"},
            {"record_id": "t3.r2", "visual_row": "Grade C/1", "status": "checked", "rowspan_group": "Grade C"},
            {"record_id": "t3.r3", "visual_row": "Grade C/2", "status": "checked", "rowspan_group": "Grade C"},
            {"record_id": "t3.r4", "visual_row": "Grade D/1", "status": "checked"},
        ],
    },
    "4": {
        "source_pages": ["source_pages/annex1_tables_p32-032.png"],
        "cell_reconstruction": "visual_reviewed_cells",
        "cell_reconstruction_status": "complete",
        "merged_cells": [
            {"type": "row_span", "column": 0, "rows": list(range(1, 9)), "text": "Grade A", "expanded": True},
            {"type": "row_span", "column": 0, "rows": [9, 10], "text": "Grade B", "expanded": True},
            {"type": "row_span", "column": 0, "rows": [12, 13, 14, 15], "text": "Grade D", "expanded": True},
        ],
        "visual_features": [
            "Grade labels are vertically centered in merged cells; text extraction places some labels mid-group.",
            "The Grade B and Grade D first operations must be assigned from the visual row-span, not from the extracted label line.",
        ],
        "row_review": [
            *[
                {"record_id": f"t4.r{i}", "visual_row": f"Grade A/{i}", "status": "checked", "rowspan_group": "Grade A"}
                for i in range(1, 9)
            ],
            {"record_id": "t4.r9", "visual_row": "Grade B/1", "status": "checked", "rowspan_group": "Grade B"},
            {"record_id": "t4.r10", "visual_row": "Grade B/2", "status": "checked", "rowspan_group": "Grade B"},
            {"record_id": "t4.r11", "visual_row": "Grade C/1", "status": "checked"},
            *[
                {"record_id": f"t4.r{i}", "visual_row": f"Grade D/{i - 11}", "status": "checked", "rowspan_group": "Grade D"}
                for i in range(12, 16)
            ],
        ],
    },
    "5": {
        "source_pages": ["source_pages/annex1_tables_p56_59-058.png"],
        "cell_reconstruction": "visual_reviewed_cells",
        "cell_reconstruction_status": "complete",
        "header_groups": _PARTICLE_HEADER_GROUPS,
        "merged_cells": [
            {"type": "column_span", "row": "header", "columns": [1, 2], "expanded": False},
            {"type": "column_span", "row": "header", "columns": [3, 4], "expanded": False},
        ],
        "visual_features": [
            "Two-tier particle-size headers span the at-rest and in-operation subcolumns.",
            "Grade D has wrapped cell text for both in-operation limits; each wrapped cell is one logical value.",
        ],
        "row_review": [
            {"record_id": "t5.r1", "visual_row": "A", "status": "checked"},
            {"record_id": "t5.r2", "visual_row": "B", "status": "checked"},
            {"record_id": "t5.r3", "visual_row": "C", "status": "checked"},
            {"record_id": "t5.r4", "visual_row": "D", "status": "checked", "wrapped_cells": [2, 4]},
        ],
    },
    "6": {
        "source_pages": ["source_pages/annex1_tables_p60-060.png"],
        "cell_reconstruction": "visual_reviewed_cells",
        "cell_reconstruction_status": "complete",
        "merged_cells": [
            {
                "type": "column_span",
                "row": "A",
                "columns": [1, 2, 3, 4],
                "text": "No growth (c)",
                "expanded": True,
            }
        ],
        "visual_features": [
            "Grade A has one horizontally merged No growth(c) cell across all four monitoring-method columns.",
        ],
        "row_review": [
            {"record_id": "t6.r1", "visual_row": "A", "status": "checked", "expanded_merged_cells": [1, 2, 3, 4]},
            {"record_id": "t6.r2", "visual_row": "B", "status": "checked"},
            {"record_id": "t6.r3", "visual_row": "C", "status": "checked"},
            {"record_id": "t6.r4", "visual_row": "D", "status": "checked"},
        ],
    },
}


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _line_span(source_label: str, idx: int) -> Dict[str, str]:
    return {"source_label": source_label, "locator": f"line:{idx + 1}"}


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
    data: Optional[Dict[str, Any]] = None,
) -> Node:
    role = "informative" if kind == "note" else ("structural" if kind in {"table", "table_header"} else "normative")
    return Node(
        nid=nid,
        kind=kind,
        kind_raw=kind_raw,
        num=num,
        ord=None,
        heading=heading,
        text=text,
        role=role,
        normativity=None if role != "normative" else "must",
        source_spans=[_line_span(source_label, line_idx)],
        data=data or {},
    )


def _find_caption_end(lines: List[str], caption_idx: int) -> int:
    idx = caption_idx + 1
    while idx < len(lines):
        stripped = lines[idx].strip()
        if not stripped:
            break
        if PARA_RE.match(stripped) or CAPTION_RE.match(stripped) or PAGE_RE.match(stripped):
            break
        if lines[idx].startswith(" ") or lines[idx].startswith("\t"):
            idx += 1
            continue
        break
    return idx


def _caption_text(lines: List[str], caption_idx: int) -> Tuple[str, int]:
    caption_end = _find_caption_end(lines, caption_idx)
    return _clean(" ".join(lines[i].strip() for i in range(caption_idx, caption_end))), caption_end


def _skip_noise(lines: List[str], idx: int) -> int:
    while idx < len(lines):
        stripped = lines[idx].strip()
        if not stripped or PAGE_RE.match(stripped) or ANNEX_HEADER_RE.match(stripped):
            idx += 1
            continue
        return idx
    return idx


def _collect_note_text(lines: List[str], start_idx: int, stop_idx: int) -> Tuple[str, int]:
    first = lines[start_idx].strip()
    chunks = [first]
    idx = start_idx + 1
    while idx < stop_idx:
        stripped = lines[idx].strip()
        if not stripped:
            idx += 1
            continue
        if NOTE_START_RE.match(stripped) or PARA_RE.match(stripped) or CAPTION_RE.match(stripped):
            break
        if PAGE_RE.match(stripped) or ANNEX_HEADER_RE.match(stripped):
            idx += 1
            continue
        chunks.append(stripped)
        idx += 1
    return _clean(" ".join(chunks)), idx


def _collect_notes(lines: List[str], start_idx: int, stop_idx: int) -> List[Dict[str, Any]]:
    notes: List[Dict[str, Any]] = []
    idx = start_idx
    while idx < stop_idx:
        stripped = lines[idx].strip()
        if not stripped or PAGE_RE.match(stripped) or ANNEX_HEADER_RE.match(stripped):
            idx += 1
            continue
        if PARA_RE.match(stripped) or CAPTION_RE.match(stripped):
            break
        if NOTE_START_RE.match(stripped):
            text, next_idx = _collect_note_text(lines, idx, stop_idx)
            notes.append({"line_idx": idx, "text": text})
            idx = max(next_idx, idx + 1)
            continue
        idx += 1
    return notes


def _clean_raw_lines(lines: List[str]) -> List[str]:
    return [
        line
        for line in lines
        if line.strip() and not PAGE_RE.match(line.strip()) and not ANNEX_HEADER_RE.match(line.strip())
    ]


def _next_stop_idx(lines: List[str], start_idx: int) -> int:
    idx = start_idx
    while idx < len(lines):
        stripped = lines[idx].strip()
        if idx > start_idx and CAPTION_RE.match(stripped):
            return idx
        if PARA_RE.match(stripped):
            return idx
        upper = stripped.upper()
        if upper in {
            "ASEPTIC PREPARATION AND PROCESSING",
            "ENVIRONMENTAL AND PERSONNEL MONITORING - VIABLE PARTICLE",
            "ENVIRONMENTAL AND PERSONNEL MONITORING \u2013 VIABLE PARTICLE",
            "ASEPTIC PROCESS SIMULATION (APS) (ALSO KNOWN AS MEDIA FILL)",
        }:
            return idx
        idx += 1
    return idx


def _numeric_table(table_no: str, caption: str, caption_idx: int, lines: List[str], body_start: int, stop_idx: int) -> Annex1Table:
    if table_no in {"1", "5"}:
        unit = "\u00b5m/m3" if table_no == "1" else "\u03bcm/m3"
        suffix = "(b)" if table_no == "1" else "(a)"
        columns = [
            "Grade",
            f">= 0.5 {unit} at rest",
            f">= 0.5 {unit} in operation",
            f">= 5 {unit} at rest",
            f">= 5 {unit} in operation",
        ]
        table_1_rows = [
            ["A", "3 520", "3 520", "Not specified (a)", "Not specified (a)"],
            ["B", "3 520", "352 000", "Not specified (a)", "2 930"],
            ["C", "352 000", "3 520 000", "2 930", "29 300"],
            ["D", "3 520 000", f"Not predetermined {suffix}", "29 300", f"Not predetermined {suffix}"],
        ]
        table_5_rows = [
            ["A", "3 520", "3 520", "29", "29"],
            ["B", "3 520", "352 000", "29", "2 930"],
            ["C", "352 000", "3 520 000", "2 930", "29 300"],
            ["D", "3 520 000", "Not predetermined (a)", "29 300", "Not predetermined (a)"],
        ]
        source_rows = table_1_rows if table_no == "1" else table_5_rows
    elif table_no == "2":
        columns = [
            "Grade",
            "Air sample CFU/m3",
            "Settle plates (diameter 90 mm) CFU/4 hours (a)",
            "Contact plates (diameter 55 mm) CFU/plate",
        ]
        source_rows = [
            ["A", "No growth", "No growth", "No growth"],
            ["B", "10", "5", "5"],
            ["C", "100", "50", "25"],
            ["D", "200", "100", "50"],
        ]
    else:
        columns = [
            "Grade",
            "Air sample CFU/m3",
            "Settle plates (diameter 90 mm) CFU/4 hours (a)",
            "Contact plates (diameter 55 mm) CFU/plate (b)",
            "Glove print, including 5 fingers on both hands CFU/glove",
        ]
        source_rows = [
            ["A", "No growth (c)", "No growth (c)", "No growth (c)", "No growth (c)"],
            ["B", "10", "5", "5", "5"],
            ["C", "100", "50", "25", "-"],
            ["D", "200", "100", "50", "-"],
        ]

    line_by_grade: Dict[str, int] = {}
    for idx in range(body_start, stop_idx):
        match = GRADE_RE.match(lines[idx])
        if match and match.group(1) not in line_by_grade:
            line_by_grade[match.group(1)] = idx
    rows = [
        {"line_idx": line_by_grade.get(cells[0], body_start), "cells": cells, "grade": cells[0]}
        for cells in source_rows
    ]
    notes = _collect_notes(lines, stop_idx, _next_stop_idx(lines, stop_idx))
    end_idx = _next_stop_idx(lines, stop_idx)
    return Annex1Table(
        table_no=table_no,
        caption=caption,
        caption_idx=caption_idx,
        end_idx=end_idx,
        columns=columns,
        rows=rows,
        notes=notes,
        raw_lines=_clean_raw_lines(lines[caption_idx:end_idx]),
    )


def _grade_from_line(line: str) -> Tuple[Optional[str], str]:
    match = re.match(r"^\s*Grade\s+([ABCD])\s*(.*)$", line)
    if match:
        return match.group(1), match.group(2).strip()
    return None, line.strip()


def _operation_rows(table_no: str, caption: str, caption_idx: int, lines: List[str], body_start: int, stop_idx: int) -> Annex1Table:
    columns = ["Grade", "Operation"]
    rows: List[Dict[str, Any]] = []
    current_grade: Optional[str] = "A" if table_no == "4" else None
    current_op: Optional[str] = None
    current_line = body_start

    def flush() -> None:
        nonlocal current_op
        if current_grade and current_op:
            rows.append(
                {
                    "line_idx": current_line,
                    "cells": [f"Grade {current_grade}", _clean(current_op)],
                    "grade": current_grade,
                    "operations": [_clean(current_op)],
                }
            )
        current_op = None

    for idx in range(body_start, stop_idx):
        raw = lines[idx]
        stripped = raw.strip()
        if not stripped or PAGE_RE.match(stripped) or ANNEX_HEADER_RE.match(stripped):
            continue
        grade, remainder = _grade_from_line(raw)
        if grade:
            flush()
            current_grade = grade
            stripped = remainder
        bullet_match = re.match(r"^-\s+(.*)$", stripped)
        if bullet_match:
            flush()
            current_op = bullet_match.group(1)
            current_line = idx
            continue
        if current_op and (raw.startswith(" ") or raw.startswith("\t")):
            current_op = f"{current_op} {stripped}"
    flush()

    if table_no == "4" and len(rows) == 15:
        # The Grade labels are vertically centered in row-spanned cells in the PDF.
        # Text extraction places Grade B/D labels after the first operation(s).
        visual_grades = ["A"] * 8 + ["B"] * 2 + ["C"] + ["D"] * 4
        for row, visual_grade in zip(rows, visual_grades):
            row["grade"] = visual_grade
            row["cells"][0] = f"Grade {visual_grade}"

    return Annex1Table(
        table_no=table_no,
        caption=caption,
        caption_idx=caption_idx,
        end_idx=stop_idx,
        columns=columns,
        rows=rows,
        notes=[],
        raw_lines=_clean_raw_lines(lines[caption_idx:stop_idx]),
    )


def parse_pics_annex1_tables(lines: List[str]) -> List[Annex1Table]:
    tables: List[Annex1Table] = []
    for idx, line in enumerate(lines):
        match = CAPTION_RE.match(line)
        if not match:
            continue
        table_no = match.group("num")
        caption, caption_end = _caption_text(lines, idx)
        body_start = _skip_noise(lines, caption_end)
        stop_idx = body_start
        if table_no in {"1", "2", "5", "6"}:
            while stop_idx < len(lines):
                stripped = lines[stop_idx].strip()
                if NOTE_START_RE.match(stripped):
                    break
                if PARA_RE.match(stripped) or (stop_idx > body_start and CAPTION_RE.match(stripped)):
                    break
                stop_idx += 1
            tables.append(_numeric_table(table_no, caption, idx, lines, body_start, stop_idx))
        else:
            stop_idx = _next_stop_idx(lines, body_start)
            tables.append(_operation_rows(table_no, caption, idx, lines, body_start, stop_idx))
    return tables


def _table_node(table: Annex1Table, *, parent_nid: str, source_label: str) -> Node:
    table_nid = f"{parent_nid}.tbl{table.table_no}" if parent_nid != "root" else f"tbl{table.table_no}"
    visual_review = deepcopy(VISUAL_REVIEW_BY_TABLE.get(table.table_no, {}))
    node = _make_node(
        nid=table_nid,
        kind="table",
        kind_raw="table",
        num=table.table_no,
        heading=table.caption,
        text=None,
        source_label=source_label,
        line_idx=table.caption_idx,
        data={
            "parser": "pics_annex1_tables",
            "table_no": table.table_no,
            "source_format": "fixed_width",
            "raw_lines": table.raw_lines,
            "visual_review_parser": VISUAL_REVIEW_PARSER,
            "visual_review_source_runs": [VISUAL_REVIEW_SOURCE_RUN],
            **visual_review,
        },
    )
    header = _make_node(
        nid=f"{table_nid}.tblh",
        kind="table_header",
        kind_raw="table_header",
        num=None,
        heading=None,
        text=" | ".join(table.columns),
        source_label=source_label,
        line_idx=table.caption_idx,
        data={"columns": table.columns},
    )
    node.children.append(header)
    row_review = visual_review.get("row_review") or []
    for row_no, row in enumerate(table.rows, start=1):
        cells = row["cells"]
        visual_row = deepcopy(row_review[row_no - 1]) if row_no <= len(row_review) else {}
        row_node = _make_node(
            nid=f"{header.nid}.tblr{row_no}",
            kind="table_row",
            kind_raw="table_row",
            num=str(row_no),
            heading=None,
            text=" | ".join(cells),
            source_label=source_label,
            line_idx=int(row.get("line_idx", table.caption_idx)),
            data={
                "cells": cells,
                "grade": row.get("grade"),
                "visual_review_parser": VISUAL_REVIEW_PARSER,
                "visual_review_source_run": VISUAL_REVIEW_SOURCE_RUN,
                "cell_reconstruction": visual_review.get("cell_reconstruction", "visual_reviewed_cells"),
                "cell_reconstruction_status": visual_review.get("cell_reconstruction_status", "complete"),
                **visual_row,
                **({"operations": row["operations"]} if row.get("operations") else {}),
            },
        )
        header.children.append(row_node)
    for note_no, note in enumerate(table.notes, start=1):
        note_node = _make_node(
            nid=f"{table_nid}.not{note_no}",
            kind="note",
            kind_raw="note",
            num=str(note_no),
            heading=None,
            text=note["text"],
            source_label=source_label,
            line_idx=int(note.get("line_idx", table.caption_idx)),
            data={"note_type": "table_note", "table_no": table.table_no},
        )
        node.children.append(note_node)
    return node


def _walk_with_parent(node: Node, parent: Optional[Node] = None) -> Iterable[Tuple[Optional[Node], Node]]:
    yield parent, node
    for child in node.children:
        yield from _walk_with_parent(child, node)


def _source_lines(node: Node) -> List[int]:
    out: List[int] = []
    for span in node.source_spans:
        locator = span.get("locator")
        if not isinstance(locator, str):
            continue
        match = re.search(r"line:(\d+)", locator)
        if match:
            out.append(int(match.group(1)))
    return out


def _source_lines_from_span(span: Dict[str, Any]) -> List[int]:
    locator = span.get("locator")
    if not isinstance(locator, str):
        return []
    match = re.search(r"line:(\d+)", locator)
    return [int(match.group(1))] if match else []


def _strip_embedded_table_text(text: Optional[str], table_no: str) -> Optional[str]:
    if not text:
        return text
    pattern = re.compile(rf"\n\s*Table\s+{re.escape(table_no)}\s*[:.].*$", re.IGNORECASE | re.DOTALL)
    cleaned = pattern.sub("", text).rstrip()
    return cleaned or None


def _strip_table_residue(text: Optional[str]) -> Optional[str]:
    if not text:
        return text
    kept: List[str] = []
    residue_re = re.compile(
        r"^\s*(?:"
        r"Maximum limits\b|at rest\b|Grade\b|[ABCD]\b|D$|No growth\b|CFU\s*/|"
        r"\([a-c]\)|[a-c]\)|Note\s+\d+\s*:|predetermined\b|\d[\d\s]{2,}"
        r")",
        re.IGNORECASE,
    )
    for line in text.splitlines():
        if kept and residue_re.match(line):
            break
        kept.append(line)
    cleaned = "\n".join(kept).rstrip()
    return cleaned or None


def _with_line_offset(table: Annex1Table, line_no_offset: int) -> Annex1Table:
    if line_no_offset == 0:
        return table
    return Annex1Table(
        table_no=table.table_no,
        caption=table.caption,
        caption_idx=table.caption_idx + line_no_offset,
        end_idx=table.end_idx + line_no_offset,
        columns=table.columns,
        rows=[
            {
                **row,
                "line_idx": int(row.get("line_idx", table.caption_idx)) + line_no_offset,
            }
            for row in table.rows
        ],
        notes=[
            {
                **note,
                "line_idx": int(note.get("line_idx", table.caption_idx)) + line_no_offset,
            }
            for note in table.notes
        ],
        raw_lines=table.raw_lines,
    )


def _replace_preformatted(root: Node, table: Annex1Table, source_label: str) -> bool:
    for parent, node in list(_walk_with_parent(root)):
        if parent is None or node.kind != "preformatted":
            continue
        heading = node.heading or ""
        if not re.match(rf"^\s*Table\s+{re.escape(table.table_no)}\s*[:.]", heading, flags=re.IGNORECASE):
            continue
        replacement = _table_node(table, parent_nid=parent.nid, source_label=source_label)
        parent.text = _strip_table_residue(parent.text)
        parent.source_spans = [
            span
            for span in parent.source_spans
            if not any(table.caption_idx + 1 <= line <= table.end_idx for line in _source_lines_from_span(span))
        ]
        children = parent.children
        target_idx = children.index(node)
        children[target_idx] = replacement
        parent.children = [
            child
            for pos, child in enumerate(children)
            if pos <= target_idx
            or child.kind != "note"
            or not any(table.caption_idx + 1 <= line <= table.end_idx for line in _source_lines(child))
        ]
        return True
    return False


def _insert_after_embedded(root: Node, table: Annex1Table, source_label: str) -> bool:
    caption_re = re.compile(rf"Table\s+{re.escape(table.table_no)}\s*[:.]", re.IGNORECASE)
    for parent, node in list(_walk_with_parent(root)):
        if parent is None or node.kind not in {"chapter", "section", "paragraph", "item", "subitem"}:
            continue
        if not caption_re.search(node.text or ""):
            continue
        node.text = _strip_embedded_table_text(node.text, table.table_no)
        replacement_parent = parent
        replacement = _table_node(table, parent_nid=replacement_parent.nid, source_label=source_label)
        children = replacement_parent.children
        children.insert(children.index(node) + 1, replacement)
        return True
    return False


def _insert_by_source_line(root: Node, table: Annex1Table, source_label: str) -> None:
    best_parent = root
    best_line = -1
    for _parent, node in _walk_with_parent(root):
        if node.kind not in {"annex", "section", "paragraph"}:
            continue
        lines = [line for line in _source_lines(node) if line <= table.caption_idx + 1]
        if lines and max(lines) > best_line:
            best_parent = node
            best_line = max(lines)
    best_parent.children.append(_table_node(table, parent_nid=best_parent.nid, source_label=source_label))


def normalize_pics_annex1_tables(
    root: Node,
    raw_lines: List[str],
    *,
    source_label: str,
    line_no_offset: int = 0,
) -> List[Dict[str, Any]]:
    tables = [_with_line_offset(table, line_no_offset) for table in parse_pics_annex1_tables(raw_lines)]
    applied: List[Dict[str, Any]] = []
    for table in tables:
        inserted = _replace_preformatted(root, table, source_label)
        if not inserted:
            inserted = _insert_after_embedded(root, table, source_label)
        if not inserted:
            _insert_by_source_line(root, table, source_label)
        applied.append(
            {
                "table_no": table.table_no,
                "caption": table.caption,
                "rows": len(table.rows),
                "notes": len(table.notes),
            }
        )
    return applied
