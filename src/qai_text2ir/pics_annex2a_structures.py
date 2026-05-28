from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

from qai_xml2ir.models_ir import Node


TABLE1_RE = re.compile(
    r"^\s*Table\s+1\.\s+Illustrative guide to manufacturing activities within the scope of Annex 2A\s*$",
    re.IGNORECASE,
)
FIG12_RE = re.compile(
    r"^\s*Figure\s+1:\s+Example of gene therapy mRNA\s+Figure\s+2:\s+Example of in vivo viral vector gene\s*$",
    re.IGNORECASE,
)
FIG3_RE = re.compile(
    r"^\s*Figure\s+3:\s+Example of autologous CAR-T therapy ATMP manufacturing\s*$",
    re.IGNORECASE,
)
PRINCIPLE_RE = re.compile(r"^\s*PRINCIPLE\s*$")


@dataclass
class Annex2AStructures:
    table_idx: int
    table_end_idx: int
    fig12_idx: int
    fig12_end_idx: int
    fig3_idx: int
    fig3_end_idx: int


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


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


def _find_structures(lines: List[str]) -> Optional[Annex2AStructures]:
    table_idx = next((idx for idx, line in enumerate(lines) if TABLE1_RE.match(line)), None)
    fig12_idx = next((idx for idx, line in enumerate(lines) if FIG12_RE.match(line)), None)
    fig3_idx = next((idx for idx, line in enumerate(lines) if FIG3_RE.match(line)), None)
    if table_idx is None or fig12_idx is None or fig3_idx is None:
        return None
    principle_idx = next((idx for idx in range(fig3_idx + 1, len(lines)) if PRINCIPLE_RE.match(lines[idx])), len(lines))
    return Annex2AStructures(
        table_idx=table_idx,
        table_end_idx=fig12_idx,
        fig12_idx=fig12_idx,
        fig12_end_idx=fig3_idx,
        fig3_idx=fig3_idx,
        fig3_end_idx=principle_idx,
    )


TABLE_COLUMNS = [
    "Example product / product class",
    "Application of this Annex (see note 1) manufacturing step 1",
    "Application of this Annex (see note 1) manufacturing step 2",
    "Application of this Annex (see note 1) manufacturing step 3",
    "Application of this Annex (see note 1) manufacturing step 4",
]

TABLE_ROWS = [
    [
        "Gene therapy: mRNA",
        "Linear DNA template preparation",
        "In vitro cell free transcription",
        "mRNA purification",
        "Formulation, filling",
    ],
    [
        "Gene therapy: in vivo viral vectors",
        "Plasmid manufacturing",
        "Establishment of MCB, WCB2",
        "Vector manufacturing and purification",
        "Formulation, filling",
    ],
    [
        "Gene therapy: in vivo non-viral vectors (naked DNA, lipoplexes, polyplexes, etc.)",
        "Plasmid manufacturing",
        "Establishment of bacterial bank2",
        "Fermentation and purification",
        "Formulation, filling",
    ],
    [
        "Gene therapy: ex-vivo genetically modified cells",
        "Donation, procurement and testing of starting tissue / cells",
        "Plasmid manufacturing; Vector manufacturing3",
        "Ex-vivo genetic modification of cells",
        "Formulation, filling",
    ],
    [
        "Somatic cell therapy",
        "Donation, procurement and testing of starting tissue / cells",
        "Establishment of MCB, WCB or primary cell lot or cell pool2",
        "Cell isolation, culture purification, combination with non-cellular components",
        "Formulation, combination, filling",
    ],
    [
        "Tissue engineered products",
        "Donation, procurement and testing of starting tissue / cells",
        "Initial processing, isolation and purification, establish MCB, WCB, primary cell lot or cell pool2",
        "Cell isolation, culture, purification, combination with non-cellular components",
        "Formulation, combination, filling",
    ],
]

TABLE_ROW_LINE_HINTS = [
    "Gene therapy:",
    "in vivo viral",
    "in vivo non-",
    "ex-vivo",
    "Somatic cell",
    "Tissue",
]

TABLE_FOOTNOTES = [
    "1 Application of this annex applies to manufacturing steps illustrated in dark grey. Application of this annex or principles of this annex apply to steps illustrated in light grey apply depending on the requirements of national legislation.",
    "2 Refer to points 5.32 for establishment of cell banks and seed lots.",
    "3 In the case of gene therapy ex-vivo genetically modified cells, this guide applies to vector manufacturing except where otherwise authorised by national law where principles of GMP should apply.",
]


def _find_line_containing(lines: List[str], start: int, end: int, needle: str) -> int:
    lowered = needle.lower()
    for idx in range(start, min(end, len(lines))):
        if lowered in lines[idx].lower():
            return idx
    return start


def _find_footnote_line(lines: List[str], start: int, end: int, note_no: int) -> int:
    pattern = re.compile(rf"^\s*{note_no}\s+")
    for idx in range(start, min(end, len(lines))):
        if pattern.match(lines[idx]):
            return idx
    return start


def _table1_node(struct: Annex2AStructures, lines: List[str], source_label: str, parent_nid: str, line_no_offset: int) -> Node:
    table_nid = f"{parent_nid}.tbl1"
    node = _make_node(
        nid=table_nid,
        kind="table",
        kind_raw="table",
        num="1",
        heading="Table 1. Illustrative guide to manufacturing activities within the scope of Annex 2A",
        text=None,
        source_label=source_label,
        line_idx=struct.table_idx + line_no_offset,
        role="structural",
        data={
            "parser": "pics_annex2a_table1",
            "table_no": "1",
            "source_format": "fixed_width_text_layer",
            "shading_reconstructed": False,
            "shading_note": "PDF shading is not reliably represented in the text layer.",
            "raw_lines": lines[struct.table_idx:struct.table_end_idx],
        },
    )
    header = _make_node(
        nid=f"{table_nid}.tblh",
        kind="table_header",
        kind_raw="table_header",
        num=None,
        heading=None,
        text=" | ".join(TABLE_COLUMNS),
        source_label=source_label,
        line_idx=struct.table_idx + line_no_offset,
        role="structural",
        data={"columns": TABLE_COLUMNS},
    )
    node.children.append(header)
    for row_no, cells in enumerate(TABLE_ROWS, start=1):
        line_idx = _find_line_containing(
            lines,
            struct.table_idx,
            struct.table_end_idx,
            TABLE_ROW_LINE_HINTS[row_no - 1],
        )
        row_node = _make_node(
            nid=f"{header.nid}.tblr{row_no}",
            kind="table_row",
            kind_raw="table_row",
            num=str(row_no),
            heading=None,
            text=" | ".join(cells),
            source_label=source_label,
            line_idx=line_idx + line_no_offset,
            data={"cells": cells, "product_class": cells[0]},
        )
        header.children.append(row_node)
    for note_no, note_text in enumerate(TABLE_FOOTNOTES, start=1):
        line_idx = _find_footnote_line(lines, struct.table_idx, struct.table_end_idx, note_no)
        node.children.append(
            _make_node(
                nid=f"{table_nid}.not{note_no}",
                kind="note",
                kind_raw="note",
                num=str(note_no),
                heading=None,
                text=note_text,
                source_label=source_label,
                line_idx=line_idx + line_no_offset,
                role="informative",
                data={"note_type": "table_note", "table_no": "1"},
            )
        )
    return node


FIGURES = {
    "1": {
        "heading": "Figure 1: Example of gene therapy mRNA ATMP manufacturing",
        "columns": [
            {
                "label": "linear DNA template path",
                "steps": [
                    "Linear DNA template preparation",
                    "Plasmid DNA construct preparation",
                    "Transfer of Plasmid DNA to starter colony (e.g. E. coli)",
                    "Purification, linearization and polishing",
                    "Storage of linear DNA template",
                    "OR",
                    "Plasmid DNA construct preparation",
                    "Polymerase Chain Reaction (PCR)",
                    "Storage of linear DNA template",
                ],
            },
            {
                "label": "ATMP manufacturing",
                "steps": [
                    "Transcription",
                    "Purification",
                    "Harvest",
                    "Formulation",
                    "Filling",
                    "Storage",
                    "Distribution for patient access",
                ],
            },
        ],
    },
    "2": {
        "heading": "Figure 2: Example of in vivo viral vector gene therapy ATMP manufacturing",
        "columns": [
            {
                "label": "plasmid manufacturing",
                "steps": [
                    "Plasmid Manufacturing",
                    "Plasmid DNA construct preparation",
                    "Transfer of Plasmid DNA to starter colony (e.g. E. coli)",
                    "Expansion",
                    "Dispensing",
                    "Storage",
                ],
            },
            {
                "label": "ATMP manufacturing",
                "steps": [
                    "Establishing MCB or WCB",
                    "Thawing",
                    "Transfection",
                    "Induction",
                    "Harvest",
                    "Purification",
                    "Formulation",
                    "Sterile Filtration",
                    "Filling",
                    "Storage",
                    "Distribution for patient access",
                ],
            },
        ],
    },
    "3": {
        "heading": "Figure 3: Example of autologous CAR-T therapy ATMP manufacturing",
        "columns": [
            {
                "label": "plasmid manufacturing",
                "steps": [
                    "Plasmid DNA construct preparation",
                    "Transfer of Plasmid DNA to starter colony (e.g. E. coli)",
                    "Expansion",
                    "Dispensing",
                    "Storage",
                ],
            },
            {
                "label": "viral vector product manufacturing",
                "steps": [
                    "Establishing MCB or WCB",
                    "Thawing",
                    "Transfection",
                    "Induction",
                    "Harvest",
                    "Purification",
                    "Sterile Filtration",
                    "Dispensing",
                    "Storage",
                ],
            },
            {
                "label": "ATMP manufacturing",
                "steps": [
                    "Donation or procurement of patient cells",
                    "Transduction",
                    "Expansion",
                    "Harvest",
                    "Formulation",
                    "Filling",
                    "Storage",
                    "Distribution for patient access",
                ],
            },
        ],
    },
}


def _figure_node(
    *,
    figure_no: str,
    parent_nid: str,
    line_idx: int,
    raw_lines: List[str],
    source_label: str,
    line_no_offset: int,
    parse_confidence: str,
) -> Node:
    spec = FIGURES[figure_no]
    return _make_node(
        nid=f"{parent_nid}.fig{figure_no}",
        kind="figure",
        kind_raw="figure",
        num=figure_no,
        heading=spec["heading"],
        text=None,
        source_label=source_label,
        line_idx=line_idx + line_no_offset,
        role="informative",
        data={
            "parser": "pics_annex2a_flow_figures",
            "figure_no": figure_no,
            "format": "flow_diagram_text_layer",
            "parse_confidence": parse_confidence,
            "columns": spec["columns"],
            "raw_lines": raw_lines,
        },
    )


def _figure_nodes(struct: Annex2AStructures, lines: List[str], source_label: str, parent_nid: str, line_no_offset: int) -> List[Node]:
    fig12_raw = lines[struct.fig12_idx:struct.fig12_end_idx]
    fig3_raw = lines[struct.fig3_idx:struct.fig3_end_idx]
    return [
        _figure_node(
            figure_no="1",
            parent_nid=parent_nid,
            line_idx=struct.fig12_idx,
            raw_lines=fig12_raw,
            source_label=source_label,
            line_no_offset=line_no_offset,
            parse_confidence="split_from_side_by_side_caption",
        ),
        _figure_node(
            figure_no="2",
            parent_nid=parent_nid,
            line_idx=struct.fig12_idx,
            raw_lines=fig12_raw,
            source_label=source_label,
            line_no_offset=line_no_offset,
            parse_confidence="split_from_side_by_side_caption",
        ),
        _figure_node(
            figure_no="3",
            parent_nid=parent_nid,
            line_idx=struct.fig3_idx,
            raw_lines=fig3_raw,
            source_label=source_label,
            line_no_offset=line_no_offset,
            parse_confidence="explicit_caption",
        ),
    ]


def _walk_with_parent(node: Node, parent: Optional[Node] = None) -> Iterable[Tuple[Optional[Node], Node]]:
    yield parent, node
    for child in node.children:
        yield from _walk_with_parent(child, node)


def _source_lines(node: Node) -> List[int]:
    lines: List[int] = []
    for span in node.source_spans:
        locator = span.get("locator")
        if not isinstance(locator, str):
            continue
        match = re.search(r"line:(\d+)", locator)
        if match:
            lines.append(int(match.group(1)))
    return lines


def _strip_special_text(text: Optional[str]) -> Optional[str]:
    if not text:
        return text
    pattern = re.compile(r"\n?\s*Table\s+1\.\s+Illustrative guide to manufacturing activities within the scope of Annex 2A.*$", re.IGNORECASE | re.DOTALL)
    cleaned = pattern.sub("", text).rstrip()
    cleaned = re.sub(
        r"\n?\s*Annex\s+2A\s+Manufacture\s+of\s+advanced\s+therapy\s+medicinal\s+products\s+for\s+human\s+use\s*$",
        "",
        cleaned,
        flags=re.IGNORECASE,
    ).rstrip()
    return cleaned or None


def normalize_pics_annex2a_structures(
    root: Node,
    raw_lines: List[str],
    *,
    source_label: str,
    line_no_offset: int = 0,
) -> Dict[str, Any]:
    struct = _find_structures(raw_lines)
    if struct is None:
        return {"applied": False}

    start_line = struct.table_idx + line_no_offset + 1
    end_line = struct.fig3_end_idx + line_no_offset + 1
    target_parent: Optional[Node] = None
    target_node: Optional[Node] = None
    for parent, node in _walk_with_parent(root):
        text = node.text or ""
        if "Table 1. Illustrative guide to manufacturing activities within the scope of Annex 2A" in text:
            target_parent = parent
            target_node = node
            break
    if target_node is None:
        return {"applied": False}

    insertion_parent = target_node
    insertion_parent.text = _strip_special_text(insertion_parent.text)
    insertion_parent.source_spans = [
        span
        for span in insertion_parent.source_spans
        if not any(start_line <= line <= end_line for line in _source_lines_from_span(span))
    ]
    insertion_parent.children = [
        child
        for child in insertion_parent.children
        if not any(start_line <= line <= end_line for line in _source_lines(child))
    ]
    insertion_parent.children.append(_table1_node(struct, raw_lines, source_label, insertion_parent.nid, line_no_offset))
    insertion_parent.children.extend(_figure_nodes(struct, raw_lines, source_label, insertion_parent.nid, line_no_offset))
    return {
        "applied": True,
        "parent_nid": insertion_parent.nid,
        "table_rows": len(TABLE_ROWS),
        "figures": 3,
        "removed_from_parent": target_parent.nid if target_parent else None,
    }


def _source_lines_from_span(span: Dict[str, Any]) -> List[int]:
    locator = span.get("locator")
    if not isinstance(locator, str):
        return []
    match = re.search(r"line:(\d+)", locator)
    return [int(match.group(1))] if match else []
