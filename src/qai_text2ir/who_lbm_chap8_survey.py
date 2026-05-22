from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional

from qai_xml2ir.models_ir import Node


TABLE_CAPTION_PATTERNS = {
    "5": re.compile(
        r"^Table\s+5\.\s+Basic Laboratory\s+[-–—]\s+Biosafety Level 1:\s+laboratory safety survey\.?\s*$",
        re.IGNORECASE,
    ),
    "6": re.compile(
        r"^Table\s+6\.\s+Basic laboratory\s+[-–—]\s+Biosafety Level 2:\s+laboratory safety survey\.?\s*$",
        re.IGNORECASE,
    ),
    "7": re.compile(
        r"^Table\s+7\.\s+Containment laboratory\s+[-–—]\s+Biosafety Level 3:\s+laboratory safety survey\.?\s*$",
        re.IGNORECASE,
    ),
}

SECTION_HEADINGS = {
    "Laboratory",
    "Laboratory design",
    "Gas cylinders",
    "Chemicals",
    "Refrigerators/freezers/cold rooms",
    "Electrical equipment",
    "Personal protective equipment",
    "Waste management",
    "Occupational health and safety programmes available",
    "General engineering controls",
    "General practices and procedures",
    "General laboratory housekeeping",
    "Fire protection",
    "Heated constant temperature baths",
    "Biological safety cabinet (BSC)",
    "Decontamination",
    "Handling of contaminated waste",
    "Personal protection",
    "Practices",
    "Facility",
    "Hand protection",
    "Respiratory protection",
}

SCAFFOLD_EXACT = {
    "LABORATORY BIOSAFETY MANUAL",
    "8. GUIDELINES FOR LABORATORY/FACILITY CERTIFICATION",
    "Location",
    "Date",
    "Location Date",
    "Person in charge of laboratory",
    "CHECKED ITEM (ENTER DATE OF CHECK)",
    "CHECKED ITEM (ENTER DATE OF CHECK) YES NO N/A COMMENTS",
    "YES",
    "NO",
    "N/A",
    "COMMENTS",
    "Biosafety Level:",
    "Attach the appropriate",
    "Biosafety Level Survey",
    "Form",
}

SCAFFOLD_PATTERNS = [
    re.compile(r"^•\s*[0-9ivxlcdm]+\s*•$", re.IGNORECASE),
    re.compile(r"^Safety surveyor[’']s signature\b", re.IGNORECASE),
    re.compile(r"^Date survey completed\b", re.IGNORECASE),
    re.compile(r"^CHECKED ITEM \(ENTER DATE OF CHECK\).*COMMENTS\b", re.IGNORECASE),
    re.compile(r"^This form is used in conjunction\b", re.IGNORECASE),
    re.compile(r"^(?:survey form|Level 2 laboratory safety survey forms?)$", re.IGNORECASE),
    re.compile(r"^○(?:\s*○)+$"),
]

CONTROL_RE = re.compile(r"(?:\\x01|[\x00-\x08\x0b\x0c\x0e-\x1f\uE000-\uF8FF])")
DOT_LEADER_RE = re.compile(r"\s*\.{2,}\s*$")
SIDE_LABEL_RE = re.compile(r"\s*\.?\s*\b(?:Location|Date|Brand|Type|Serial no\.?)\s*:\s*", re.IGNORECASE)
TRAILING_SIDE_LABEL_RE = re.compile(r"\s+\b(?:Location|Date|Brand|Type|Serial no\.?)\s*:\s*$", re.IGNORECASE)


@dataclass
class SurveyRow:
    text: str
    start_line: int
    end_line: int
    raw_line_count: int


@dataclass
class SurveySection:
    heading: str
    line_no: int
    rows: List[SurveyRow] = field(default_factory=list)


@dataclass
class SurveyTable:
    table_no: str
    heading: str
    caption_line: int
    end_line: int
    sections: List[SurveySection] = field(default_factory=list)

    @property
    def row_count(self) -> int:
        return sum(len(section.rows) for section in self.sections)


@dataclass
class SurveyParseResult:
    tables: List[SurveyTable]
    consumed_line_indexes: List[int]


def find_survey_table_regions(lines: List[str]) -> List[tuple[str, int, int]]:
    captions: List[tuple[str, int]] = []
    for idx, line in enumerate(lines):
        stripped = line.strip()
        for table_no, pattern in TABLE_CAPTION_PATTERNS.items():
            if pattern.match(stripped):
                captions.append((table_no, idx))
                break
    regions: List[tuple[str, int, int]] = []
    for pos, (table_no, start_idx) in enumerate(captions):
        if table_no not in {"5", "6", "7"}:
            continue
        if pos + 1 < len(captions):
            end_idx = captions[pos + 1][1]
        else:
            end_idx = _find_table7_end(lines, start_idx)
        regions.append((table_no, start_idx, end_idx))
    return regions


def parse_chap8_survey_tables(
    lines: List[str],
    *,
    line_no_offset: int = 0,
) -> SurveyParseResult:
    tables: List[SurveyTable] = []
    consumed: List[int] = []
    for table_no, start_idx, end_idx in find_survey_table_regions(lines):
        table_lines = lines[start_idx:end_idx]
        table = _parse_table(table_no, table_lines, start_idx=start_idx, line_no_offset=line_no_offset)
        tables.append(table)
        consumed.extend(range(start_idx, end_idx))
    return SurveyParseResult(tables=tables, consumed_line_indexes=consumed)


def build_table_nodes(
    *,
    tables: Iterable[SurveyTable],
    node_factory: Any,
    parent_nid: str,
    source_label: str,
) -> List[Node]:
    nodes: List[Node] = []
    for table in tables:
        table_node = node_factory.create_node(
            kind="table",
            kind_raw="table",
            num=table.table_no,
            line_no=table.caption_line,
            source_label=source_label,
            parent_nid=parent_nid,
        )
        table_node.heading = table.heading
        table_node.role = "structural"
        table_node.normativity = None
        table_node.data = {
            "table_no": table.table_no,
            "table_role": "laboratory_safety_survey",
            "parser": "who_lbm_chap8_survey",
            "row_count": table.row_count,
            "omitted_columns": ["YES", "NO", "N/A", "COMMENTS"],
            "omitted_form_controls": True,
        }
        for section in table.sections:
            section_node = node_factory.create_node(
                kind="table_header",
                kind_raw="table_header",
                num=None,
                line_no=section.line_no,
                source_label=source_label,
                parent_nid=table_node.nid,
            )
            section_node.heading = section.heading
            section_node.role = "structural"
            section_node.normativity = None
            section_node.data = {
                "header_role": "checklist_section",
                "table_no": table.table_no,
                "row_count": len(section.rows),
            }
            for row in section.rows:
                row_node = node_factory.create_node(
                    kind="table_row",
                    kind_raw="table_row",
                    num=None,
                    line_no=row.start_line,
                    source_label=source_label,
                    parent_nid=section_node.nid,
                )
                row_node.text = row.text
                row_node.role = "normative"
                row_node.normativity = "must"
                row_node.data = {
                    "row_role": "checklist_item",
                    "table_no": table.table_no,
                    "section_heading": section.heading,
                    "omitted_form_controls": True,
                    "source_line_count": row.raw_line_count,
                }
                if row.end_line != row.start_line:
                    row_node.source_spans.append(
                        {"source_label": source_label, "locator": f"line:{row.end_line}"}
                    )
                section_node.children.append(row_node)
            table_node.children.append(section_node)
        nodes.append(table_node)
    return nodes


def summarize_tables(tables: Iterable[SurveyTable]) -> Dict[str, Any]:
    return {
        table.table_no: {
            "heading": table.heading,
            "row_count": table.row_count,
            "sections": {section.heading: len(section.rows) for section in table.sections},
        }
        for table in tables
    }


def _find_table7_end(lines: List[str], start_idx: int) -> int:
    for idx in range(start_idx + 1, len(lines)):
        if re.match(r"^PART\s+II\b", lines[idx].strip(), flags=re.IGNORECASE):
            return idx
    return len(lines)


def _parse_table(table_no: str, lines: List[str], *, start_idx: int, line_no_offset: int) -> SurveyTable:
    heading = lines[0].strip().rstrip(".") if table_no == "5" else lines[0].strip()
    table = SurveyTable(
        table_no=table_no,
        heading=heading,
        caption_line=start_idx + 1 + line_no_offset,
        end_line=start_idx + len(lines) + line_no_offset,
    )
    current_section: Optional[SurveySection] = None
    row_parts: List[str] = []
    row_start: Optional[int] = None
    row_last: Optional[int] = None

    def flush_row() -> None:
        nonlocal row_parts, row_start, row_last, current_section
        if not row_parts:
            return
        text = _clean_row_text(" ".join(row_parts))
        if text and current_section is not None:
            current_section.rows.append(
                SurveyRow(
                    text=text,
                    start_line=row_start or start_idx + 1 + line_no_offset,
                    end_line=row_last or row_start or start_idx + 1 + line_no_offset,
                    raw_line_count=len(row_parts),
                )
            )
        row_parts = []
        row_start = None
        row_last = None

    for rel_idx, raw_line in enumerate(lines[1:], start=1):
        line_no = start_idx + rel_idx + 1 + line_no_offset
        stripped = raw_line.strip()
        if _is_ignored_line(stripped):
            continue
        section = _section_heading(stripped)
        if section:
            flush_row()
            current_section = SurveySection(heading=section, line_no=line_no)
            table.sections.append(current_section)
            continue
        if current_section is None:
            continue
        has_terminator = _has_row_terminator(stripped)
        piece = _clean_row_piece(stripped)
        if piece:
            if row_start is None:
                row_start = line_no
            row_last = line_no
            row_parts.append(piece)
        if has_terminator:
            flush_row()
    flush_row()
    return table


def _is_ignored_line(stripped: str) -> bool:
    if not stripped:
        return True
    if stripped in SCAFFOLD_EXACT:
        return True
    if stripped in {"Brand:", "Type:", "Serial no.:"}:
        return True
    return any(pattern.match(stripped) for pattern in SCAFFOLD_PATTERNS)


def _section_heading(stripped: str) -> Optional[str]:
    left_segment = re.split(r"\s{2,}", stripped, maxsplit=1)[0].strip()
    if left_segment in SECTION_HEADINGS:
        return left_segment
    candidate = TRAILING_SIDE_LABEL_RE.sub("", stripped).strip()
    candidate = SIDE_LABEL_RE.sub(" ", candidate).strip()
    candidate = re.sub(r"\s+", " ", candidate)
    return candidate if candidate in SECTION_HEADINGS else None


def _has_row_terminator(stripped: str) -> bool:
    return bool(CONTROL_RE.search(stripped))


def _clean_row_piece(stripped: str) -> str:
    text = stripped.strip()
    text = re.sub(r"^•\s*", "", text)
    text = SIDE_LABEL_RE.sub(" ", text)
    text = CONTROL_RE.sub(" ", text)
    text = DOT_LEADER_RE.sub("", text)
    text = re.sub(r"\.{2,}", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _clean_row_text(text: str) -> str:
    cleaned = _clean_row_piece(text)
    cleaned = cleaned.replace("appropriate . disinfectant", "appropriate disinfectant")
    cleaned = cleaned.replace("needlesyringe", "needle-syringe")
    cleaned = re.sub(r"\s+([,.;:)])", r"\1", cleaned)
    cleaned = re.sub(r"([(])\s+", r"\1", cleaned)
    return cleaned.strip()
