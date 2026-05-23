from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

from qai_xml2ir.models_ir import Node


PARSER_ID = "pics_annexes_bundle_specials"
ANNEX2B_CAPTION = "Table 1. Illustrative guide to manufacturing activities within the scope of Annex 2B"
ANNEX20_CAPTION = "Figure 1: Overview of a typical quality risk management process"


@dataclass(frozen=True)
class LocatedBlock:
    caption_idx: int
    end_idx: int


TABLE2B_COLUMNS = [
    "Type and source of material",
    "Example product",
    "Manufacturing step 1",
    "Manufacturing step 2",
    "Manufacturing step 3",
    "Manufacturing step 4",
]

TABLE2B_ROWS = [
    [
        "Animal or plant sources: non-transgenic",
        "Heparins, insulin, enzymes, proteins, allergen extract, immunosera",
        "Collection of plant, organ, animal material or fluid",
        "Cutting, mixing, and/or initial processing",
        "Isolation and purification",
        "Formulation, filling",
    ],
    [
        "Virus or bacteria / fermentation / cell culture",
        "Viral or bacterial vaccines; enzymes, proteins",
        "Establishment and maintenance of MCB, WCB, MVS, WVS",
        "Cell culture and/or fermentation",
        "Inactivation when applicable, isolation and purification",
        "Formulation, filling",
    ],
    [
        "Biotechnology fermentation / cell culture",
        "Recombinant products, MAb, allergens, vaccines",
        "Establishment and maintenance of MCB and WCB, MSL, WSL",
        "Cell culture and/or fermentation",
        "Isolation, purification, modification",
        "Formulation, filling",
    ],
    [
        "Animal sources: transgenic",
        "Recombinant proteins",
        "Master and working transgenic bank",
        "Collection, cutting, mixing, and/or initial processing",
        "Isolation, purification and modification",
        "Formulation, filling",
    ],
    [
        "Plant sources: transgenic",
        "Recombinant proteins, vaccines, allergens",
        "Master and working transgenic bank",
        "Growing, harvesting",
        "Initial extraction, isolation, purification, modification",
        "Formulation, filling",
    ],
    [
        "Human sources",
        "Urine derived enzymes, hormones",
        "Collection of fluid",
        "Mixing, and/or initial processing",
        "Isolation and purification",
        "Formulation, filling",
    ],
    [
        "Human sources: products from cells and tissues not classified as ATMPs",
        "Products from cells and tissues, not classified as ATMPs",
        "Donation, procurement and testing of starting tissue / cells",
        "Initial processing, isolation and purification",
        "Cell isolation, culture, purification, combination with non-cellular components",
        "Formulation, combination, filling",
    ],
]

TABLE2B_NOTES = [
    "1 In the EEA, this is Directive 2002/98/EC and its Commission Directives.",
    "2 In the EEA, this is Directive 2009/41/EC on contained use of genetically modified micro-organisms.",
    "3 See section B1 for the extent to which GMP principles apply.",
    "4 See section on 'Seed lot and cell bank system' for the extent to which GMP applies.",
    "5 In the EEA: HMPC guideline on Good Agricultural and Collection Practice - EMEA/HMPC/246816/2005 may be applied to growing, harvesting and initial processing in open fields.",
    "6 For principles of GMP apply, see explanatory text in 'Scope'.",
    "7 In the EEA, human tissues and cells must comply with Directive 2004/23/EC and implementing Directives at these stages.",
]

FIGURE20_STEPS = [
    "Initiate Quality Risk Management Process",
    "Risk Assessment",
    "Risk Identification",
    "Risk Analysis",
    "Risk Evaluation",
    "Risk Control",
    "Risk Reduction",
    "Risk Acceptance",
    "Output / Result of the Quality Risk Management Process",
    "Risk Review",
    "Review Events",
    "Risk Communication",
    "Risk Management tools",
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


def _find_line(lines: List[str], pattern: re.Pattern[str], start: int = 0) -> Optional[int]:
    for idx in range(start, len(lines)):
        if pattern.match(lines[idx]):
            return idx
    return None


def _find_annex2b_table(lines: List[str]) -> Optional[LocatedBlock]:
    caption_idx = _find_line(lines, re.compile(r"^\s*Table\s+1\.\s+Illustrative guide to manufacturing activities within the scope of Annex 2B\s*$", re.IGNORECASE))
    if caption_idx is None:
        return None
    principle_idx = _find_line(lines, re.compile(r"^\s*PRINCIPLE\s*$"), start=caption_idx + 1)
    return LocatedBlock(caption_idx=caption_idx, end_idx=principle_idx or min(len(lines), caption_idx + 180))


def _find_annex20_figure(lines: List[str]) -> Optional[LocatedBlock]:
    caption_idx = _find_line(lines, re.compile(r"^\s*Figure\s+1:\s+Overview of a typical quality risk management process\s*$", re.IGNORECASE))
    if caption_idx is None:
        return None
    decision_idx = _find_line(lines, re.compile(r"^\s*16\.\s+Decision nodes\b", re.IGNORECASE), start=caption_idx + 1)
    return LocatedBlock(caption_idx=caption_idx, end_idx=decision_idx or min(len(lines), caption_idx + 80))


def _normalized(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().lower()


def _find_target_node(root: Node, caption: str) -> Optional[Node]:
    token = _normalized(caption)
    for _parent, node in _walk_with_parent(root):
        if node.kind in {"annex", "section", "paragraph", "item", "subitem"}:
            text = _normalized(" ".join(v for v in [node.heading, node.text] if v))
            if token in text:
                return node
    return None


def _find_annex(root: Node, annex_num: str) -> Optional[Node]:
    for _parent, node in _walk_with_parent(root):
        if node.kind == "annex" and str(node.num or "").upper() == annex_num.upper():
            return node
    return None


def _strip_known_blocks(text: Optional[str]) -> Optional[str]:
    if not text:
        return text
    cleaned = re.sub(
        r"\s*Table\s+1\.\s+Illustrative guide to manufacturing activities within the scope of Annex 2B.*?(?=PRINCIPLE\b|$)",
        " ",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    annex2b_row_patterns = [
        r"^\s*Animal or\s+Heparins, insulin,.*$",
        r"^\s*Virus or\s+Viral or bacterial.*$",
        r"^\s*Biotechnology Recombinant.*$",
        r"^\s*Animal\s+Recombinant\s+Master and.*$",
        r"^\s*Plant sources:\s+Recombinant.*$",
    ]
    for pattern in annex2b_row_patterns:
        cleaned = re.sub(pattern, " ", cleaned, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(
        r"^\s*Human\s+Products from\s+Donation,.*?(?=PRINCIPLE\b|$)",
        " ",
        cleaned,
        flags=re.IGNORECASE | re.DOTALL,
    )
    cleaned = re.sub(
        r"\s*5\s+In the EEA: HMPC guideline on Good Agricultural and Collection Practice.*?7\s+In the EEA, human tissues and cells must comply with Directive 2004/23/EC and implementing Directives\s+at these stages\.",
        " ",
        cleaned,
        flags=re.IGNORECASE | re.DOTALL,
    )
    cleaned = re.sub(
        r"\s*Figure\s+1:\s+Overview of a typical quality risk management process.*?(?=16\.\s+Decision nodes\b|$)",
        " ",
        cleaned,
        flags=re.IGNORECASE | re.DOTALL,
    )
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    return cleaned or None


def _remove_spans_in_range(node: Node, start_line: int, end_line: int) -> None:
    node.source_spans = [
        span
        for span in node.source_spans
        if not any(start_line <= line <= end_line for line in _source_lines_from_span(span))
    ]


def _find_line_containing(lines: List[str], start: int, end: int, needle: str) -> int:
    lowered = needle.lower()
    for idx in range(start, min(end, len(lines))):
        if lowered in lines[idx].lower():
            return idx
    return start


def _annex2b_table_node(block: LocatedBlock, lines: List[str], *, parent_nid: str, source_label: str, line_no_offset: int) -> Node:
    table_nid = f"{parent_nid}.tbl1_annex2b"
    table = _make_node(
        nid=table_nid,
        kind="table",
        kind_raw="table",
        num="1",
        heading=ANNEX2B_CAPTION,
        text=None,
        source_label=source_label,
        line_idx=block.caption_idx + line_no_offset,
        role="structural",
        data={
            "parser": PARSER_ID,
            "annex": "2B",
            "table_no": "1",
            "source_format": "fixed_width_text_layer",
            "shading_reconstructed": False,
            "shading_note": "The source text layer does not preserve grey shading reliably.",
            "raw_lines": lines[block.caption_idx:block.end_idx],
        },
    )
    header = _make_node(
        nid=f"{table_nid}.tblh",
        kind="table_header",
        kind_raw="table_header",
        num=None,
        heading=None,
        text=" | ".join(TABLE2B_COLUMNS),
        source_label=source_label,
        line_idx=block.caption_idx + line_no_offset,
        role="structural",
        data={"columns": TABLE2B_COLUMNS},
    )
    table.children.append(header)
    for row_no, cells in enumerate(TABLE2B_ROWS, start=1):
        line_idx = _find_line_containing(lines, block.caption_idx, block.end_idx, cells[0].split(":")[0])
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
                    "parser": PARSER_ID,
                    "annex": "2B",
                    "cells": cells,
                    "row_key": cells[0],
                    "raw_lines": lines[block.caption_idx:block.end_idx],
                },
            )
        )
    for note_no, note in enumerate(TABLE2B_NOTES, start=1):
        line_idx = _find_line_containing(lines, block.caption_idx, block.end_idx, f"{note_no} ")
        table.children.append(
            _make_node(
                nid=f"{table_nid}.not{note_no}",
                kind="note",
                kind_raw="note",
                num=str(note_no),
                heading=None,
                text=note,
                source_label=source_label,
                line_idx=line_idx + line_no_offset,
                role="informative",
                data={"parser": PARSER_ID, "annex": "2B", "note_type": "table_note", "table_no": "1"},
            )
        )
    return table


def _annex20_figure_node(block: LocatedBlock, lines: List[str], *, parent_nid: str, source_label: str, line_no_offset: int) -> Node:
    return _make_node(
        nid=f"{parent_nid}.fig1_qrm",
        kind="figure",
        kind_raw="figure",
        num="1",
        heading=ANNEX20_CAPTION,
        text=None,
        source_label=source_label,
        line_idx=block.caption_idx + line_no_offset,
        role="informative",
        data={
            "parser": PARSER_ID,
            "annex": "20",
            "figure_no": "1",
            "format": "quality_risk_management_process_diagram",
            "steps": FIGURE20_STEPS,
            "raw_lines": lines[block.caption_idx:block.end_idx],
        },
    )


def normalize_pics_annexes_bundle_specials(
    root: Node,
    raw_lines: List[str],
    *,
    source_label: str,
    line_no_offset: int = 0,
) -> Dict[str, Any]:
    applied_tables = 0
    applied_figures = 0

    for _parent, node in _walk_with_parent(root):
        if node.kind in {"annex", "section", "paragraph", "item", "subitem"}:
            node.text = _strip_known_blocks(node.text)

    table_block = _find_annex2b_table(raw_lines)
    if table_block is not None:
        target = _find_target_node(root, ANNEX2B_CAPTION) or _find_annex(root, "2B")
        if target is not None:
            _remove_spans_in_range(target, table_block.caption_idx + 1, table_block.end_idx)
            target.children.append(
                _annex2b_table_node(
                    table_block,
                    raw_lines,
                    parent_nid=target.nid,
                    source_label=source_label,
                    line_no_offset=line_no_offset,
                )
            )
            applied_tables += 1

    figure_block = _find_annex20_figure(raw_lines)
    if figure_block is not None:
        target = _find_target_node(root, ANNEX20_CAPTION) or _find_annex(root, "20")
        if target is not None:
            _remove_spans_in_range(target, figure_block.caption_idx + 1, figure_block.end_idx)
            target.children.append(
                _annex20_figure_node(
                    figure_block,
                    raw_lines,
                    parent_nid=target.nid,
                    source_label=source_label,
                    line_no_offset=line_no_offset,
                )
            )
            applied_figures += 1

    return {"applied": bool(applied_tables or applied_figures), "tables": applied_tables, "figures": applied_figures}
