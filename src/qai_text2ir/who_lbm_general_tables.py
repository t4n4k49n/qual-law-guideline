from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

from qai_xml2ir.models_ir import Node


PARSER_ID = "who_lbm_general_tables"


@dataclass(frozen=True)
class TableSpec:
    no: str
    caption: str
    columns: List[str]
    rows: List[List[str]]
    notes: List[str]


@dataclass(frozen=True)
class RawFixedWidthTableSpec:
    no: str
    caption: str
    columns: List[str]
    slices: List[Tuple[int, Optional[int]]]
    end_marker: str
    parent_heading: str


TABLE_SPECS: List[TableSpec] = [
    TableSpec(
        no="1",
        caption="Table 1. Classification of infective microorganisms by risk group",
        columns=["Risk group", "Individual/community risk", "Description"],
        rows=[
            [
                "Risk Group 1",
                "no or low individual and community risk",
                "A microorganism that is unlikely to cause human or animal disease.",
            ],
            [
                "Risk Group 2",
                "moderate individual risk, low community risk",
                "A pathogen that can cause human or animal disease but is unlikely to be a serious hazard to laboratory workers, the community, livestock or the environment. Laboratory exposures may cause serious infection, but effective treatment and preventive measures are available and the risk of spread of infection is limited.",
            ],
            [
                "Risk Group 3",
                "high individual risk, low community risk",
                "A pathogen that usually causes serious human or animal disease but does not ordinarily spread from one infected individual to another. Effective treatment and preventive measures are available.",
            ],
            [
                "Risk Group 4",
                "high individual and community risk",
                "A pathogen that usually causes serious human or animal disease and that can be readily transmitted from one individual to another, directly or indirectly. Effective treatment and preventive measures are not usually available.",
            ],
        ],
        notes=[],
    ),
    TableSpec(
        no="2",
        caption="Table 2. Relation of risk groups to biosafety levels, practices and equipment",
        columns=["Risk group", "Biosafety level", "Laboratory type", "Laboratory practices", "Safety equipment"],
        rows=[
            ["1", "Basic - Biosafety Level 1", "Basic teaching, research", "GMT", "None; open bench work"],
            [
                "2",
                "Basic - Biosafety Level 2",
                "Primary health services; diagnostic services, research",
                "GMT plus protective clothing, biohazard sign",
                "Open bench plus BSC for potential aerosols",
            ],
            [
                "3",
                "Containment - Biosafety Level 3",
                "Special diagnostic services, research",
                "As Level 2 plus special clothing, controlled access, directional airflow",
                "BSC and/or other primary devices for all activities",
            ],
            [
                "4",
                "Maximum containment - Biosafety Level 4",
                "Dangerous pathogen units",
                "As Level 3 plus airlock entry, shower exit, special waste disposal",
                "Class III BSC, or positive pressure suits in conjunction with Class II BSCs, double-ended autoclave (through the wall), filtered air",
            ],
        ],
        notes=["BSC, biological safety cabinet; GMT, good microbiological techniques (see Part IV of this manual)"],
    ),
    TableSpec(
        no="3",
        caption="Table 3. Summary of biosafety level requirements",
        columns=["Requirement", "Biosafety Level 1", "Biosafety Level 2", "Biosafety Level 3", "Biosafety Level 4"],
        rows=[
            ["Isolation of laboratory", "No", "No", "Yes", "Yes"],
            ["Room sealable for decontamination", "No", "No", "Yes", "Yes"],
            ["Ventilation: inward airflow", "No", "Desirable", "Yes", "Yes"],
            ["Ventilation: controlled ventilating system", "No", "Desirable", "Yes", "Yes"],
            ["Ventilation: HEPA-filtered air exhaust", "No", "No", "Yes/No", "Yes"],
            ["Double-door entry", "No", "No", "Yes", "Yes"],
            ["Airlock", "No", "No", "No", "Yes"],
            ["Airlock with shower", "No", "No", "No", "Yes"],
            ["Anteroom", "No", "No", "Yes", "-"],
            ["Anteroom with shower", "No", "No", "Yes/No", "No"],
            ["Effluent treatment", "No", "No", "Yes/No", "Yes"],
            ["Autoclave: on site", "No", "Desirable", "Yes", "Yes"],
            ["Autoclave: in laboratory room", "No", "No", "Desirable", "Yes"],
            ["Autoclave: double-ended", "No", "No", "Desirable", "Yes"],
            ["Biological safety cabinets", "No", "Desirable", "Yes", "Yes"],
            ["Personnel safety monitoring capability", "No", "No", "Desirable", "Yes"],
        ],
        notes=[
            "a Environmental and functional isolation from general traffic.",
            "b Dependent on location of exhaust (see Chapter 4).",
            "c Dependent on agent(s) used in the laboratory.",
            "d For example, window, closed-circuit television, two-way communication.",
        ],
    ),
    TableSpec(
        no="4",
        caption="Table 4. Animal facility containment levels: summary of practices and safety equipment",
        columns=["Risk group", "Containment level", "Laboratory practices and safety equipment"],
        rows=[
            ["1", "ABSL-1", "Limited access, protective clothing and gloves."],
            [
                "2",
                "ABSL-2",
                "ABSL-1 practices plus: hazard warning signs. Class I or II BSCs for activities that produce aerosols. Decontamination of waste and cages before washing.",
            ],
            ["3", "ABSL-3", "ABSL-2 practices plus: controlled access. BSCs and special protective clothing for all activities."],
            [
                "4",
                "ABSL-4",
                "ABSL-3 plus: strictly limited access. Clothing change before entering. Class III BSCs or positive pressure suits. Shower on exit. Decontamination of all wastes before removal from facility.",
            ],
        ],
        notes=["ABSL, animal facility Biosafety Level; BSCs, biological safety cabinets"],
    ),
    TableSpec(
        no="8",
        caption="Table 8. Selection of a biological safety cabinet (BSC), by type of protection needed",
        columns=["Type of protection", "BSC selection"],
        rows=[
            ["Personnel protection, microorganisms in Risk Groups 1-3", "Class I, Class II, Class III"],
            ["Personnel protection, microorganisms in Risk Group 4, glove-box laboratory", "Class III"],
            ["Personnel protection, microorganisms in Risk Group 4, suit laboratory", "Class I, Class II"],
            ["Product protection", "Class II, Class III only if laminar flow included"],
            ["Volatile radionuclide/chemical protection, minute amounts", "Class IIB1, Class IIA2 vented to the outside"],
            ["Volatile radionuclide/chemical protection", "Class I, Class IIB2, Class III"],
        ],
        notes=[],
    ),
    TableSpec(
        no="9",
        caption="Table 9. Differences between Class I, II and III biological safety cabinets (BSCs)",
        columns=["BSC", "Face velocity (m/s)", "Airflow recirculated (%)", "Airflow exhausted (%)", "Exhaust system"],
        rows=[
            ["Class I", "0.36", "0", "100", "Hard duct"],
            ["Class IIA1", "0.38-0.51", "70", "30", "Exhaust to room or thimble connection"],
            ["Class IIA2 vented to the outside", "0.51", "70", "30", "Exhaust to room or thimble connection"],
            ["Class IIB1", "0.51", "30", "70", "Hard duct"],
            ["Class IIB2", "0.51", "0", "100", "Hard duct"],
            ["Class III", "NA", "0", "100", "Hard duct"],
        ],
        notes=[
            "NA, not applicable.",
            "a All biologically contaminated ducts are under negative pressure or are surrounded by negative pressure ducts and plenums.",
        ],
    ),
    TableSpec(
        no="10",
        caption="Table 10. Biosafety equipment",
        columns=["Equipment", "Hazard corrected", "Safety features"],
        rows=[
            ["Biological safety cabinet - Class I", "Aerosol and spatter", "• Minimum inward airflow (face velocity) at work access opening. Adequate filtration of exhaust air. • Does not provide product protection"],
            ["Biological safety cabinet - Class II", "Aerosol and spatter", "• Minimum inward airflow (face velocity) at work access opening. Adequate filtration of exhaust air • Provides product protection"],
            ["Biological safety cabinet - Class III", "Aerosol and spatter", "• Maximum containment • Provides product protection if laminar flow air is included"],
            ["Negative pressure flexible-film isolator", "Aerosol and spatter", "• Maximum containment"],
            ["Spatter shield", "Spatter of chemicals", "• Forms screen between operator and work"],
            ["Pipetting aids", "Hazards from pipetting by mouth, e.g. ingestion of pathogens, inhalation of aerosols produced by mouth suction on pipette, blowing out of liquid or dripping from pipette, contamination of suction end of pipette", "• Ease of use • Controls contamination of suction end of pipette, protecting pipetting aid, user and vacuum line • Can be sterilized • Controls leakage from pipette tip"],
            ["Loop microincinerators, disposable loops", "Spatter from transfer loops", "• Shielded in open-ended glass or ceramic tube. Heated by gas or electricity • Disposable, no heating necessary"],
            ["Leakproof vessels for collection and transport of infectious materials for sterilization within a facility", "Aerosols, spillage and leakage", "• Leakproof construction with lid or cover • Durable • Autoclavable"],
            ["Sharps disposal containers", "Puncture wounds", "• Autoclavable • Robust, puncture-proof"],
            ["Transport containers between laboratories, institutions", "Release of microorganisms", "• Robust • Watertight primary and secondary containers to contain spills • Absorbent material to contain spills"],
            ["Autoclaves, manual or automatic", "Infectious material (made safe for disposal or reuse)", "• Approved design • Effective heat sterilization"],
            ["Screw-capped bottles", "Aerosols and spillage", "• Effective containment"],
            ["Vacuum line protection", "Contamination of laboratory vacuum system with aerosols and overflow fluids", "• Cartridge-type filter prevents passage of aerosols (particle size 0.45 um) • Overflow flask contains appropriate disinfectant. Rubber bulb may be used to close off vacuum automatically when storage flask is full • Entire unit autoclavable"],
        ],
        notes=[],
    ),
    TableSpec(
        no="11",
        caption="Table 11. Personal protective equipment",
        columns=["Equipment", "Hazard corrected", "Safety features"],
        rows=[
            ["Laboratory coats, gowns, coveralls", "Contamination of clothing", "• Back opening • Cover street clothing"],
            ["Plastic aprons", "Contamination of clothing", "• Waterproof"],
            ["Footwear", "Impact and splash", "• Closed-toe"],
            ["Goggles", "Impact and splash", "• Impact-resistant lenses (must be optically correct or worn over corrective eye glasses) • Side shields"],
            ["Safety spectacles", "Impact", "• Impact-resistant lenses (must be optically correct) • Side shields"],
            ["Face shields", "Impact and splash", "• Shield entire face • Easily removable in case of accident"],
            ["Respirators", "Inhalation of aerosols", "• Designs available include single-use disposable; full-face or half-face air purifying; full-face or hooded powered air purifying (PAPR); and supplied air respirators"],
            ["Gloves", "Direct contact with microorganisms", "• Disposable microbiologically approved latex, vinyl or nitrile • Hand protection"],
            ["Gloves", "Cuts", "• Mesh"],
        ],
        notes=[],
    ),
    TableSpec(
        no="12",
        caption="Table 12. Recommended dilutions of chlorine-releasing compounds",
        columns=["Dilution requirement or compound", '"Clean" conditions (a)', '"Dirty" conditions (b)'],
        rows=[
            ["Available chlorine required", "0.1% (1 g/l)", "0.5% (5 g/l)"],
            ["Sodium hypochlorite solution (5% available chlorine)", "20 ml/l", "100 ml/l"],
            ["Calcium hypochlorite (70% available chlorine)", "1.4 g/l", "7.0 g/l"],
            ["Sodium dichloroisocyanurate powder (60% available chlorine)", "1.7 g/l", "8.5 g/l"],
            ["Sodium dichloroisocyanurate tablets (1.5 g available chlorine per tablet)", "1 tablet per litre", "4 tablets per litre"],
            ["Chloramine (25% available chlorine) (c)", "20 g/l", "20 g/l"],
        ],
        notes=[
            "a After removal of bulk material.",
            "b For flooding, e.g. on blood or before removal of bulk material.",
            "c See text.",
        ],
    ),
    TableSpec(
        no="13",
        caption="Table 13. General rules for chemical incompatibilities",
        columns=["Substance category", "Incompatible substances"],
        rows=[
            ["Alkali metals, e.g. sodium, potassium, caesium and lithium", "Carbon dioxide, chlorinated hydrocarbons, water"],
            ["Halogens", "Ammonia, acetylene, hydrocarbons"],
            ["Acetic acid, hydrogen sulfide, aniline, hydrocarbons, sulfuric acid", "Oxidizing agents, e.g. chromic acid, nitric acid, peroxides, permanganates"],
        ],
        notes=[],
    ),
    TableSpec(
        no="14",
        caption="Table 14. Storage of compressed and liquefied gases",
        columns=["Container", "Storage information"],
        rows=[
            [
                "Compressed gas cylinders and liquefied gas containers (a,b)",
                "• Should be securely fixed (e.g. chained) to the wall or a solid bench so that they are not inadvertently dislodged. • Must be transported with their caps in place and supported on trolleys. • Should be stored in bulk in an appropriate facility at some distance from the laboratory. This area should be locked and appropriately identified. • Should not be placed near radiators, open flames, other heat sources, sparking electrical equipment, or in direct sunlight.",
            ],
            ["Small, single-use gas cylinders (a,b)", "• Must not be incinerated."],
        ],
        notes=[
            "a The main high-pressure valve should be turned off when the equipment is not in use and when the room is unoccupied.",
            "b Rooms where flammable gas cylinders are used and/or stored should be identified by warning notices on the doors.",
        ],
    ),
    TableSpec(
        no="15",
        caption="Table 15. Types and uses of fire extinguishers",
        columns=["Type", "Use for", "Do not use for"],
        rows=[
            ["Water", "Paper, wood, fabric", "Electrical fires, flammable liquids, burning metals"],
            ["Carbon dioxide (CO2) extinguisher gases", "Flammable liquids and gases, electrical fires", "Alkali metals, paper"],
            ["Dry powder", "Flammable liquids and gases, alkali metals, electrical fires", "Reusable equipment and instruments, as residues are very difficult to remove"],
            ["Foam", "Flammable liquids", "Electrical fires"],
        ],
        notes=[],
    ),
]


FIGURE_CAPTIONS: Dict[str, str] = {
    "1": "Figure 1. Biohazard warning sign for laboratory doors",
    "2": "Figure 2. A typical Biosafety Level 1 laboratory",
    "3": "Figure 3. A typical Biosafety Level 2 laboratory",
    "4": "Figure 4. A typical Biosafety Level 3 laboratory",
    "5": "Figure 5. Suggested format for medical contact card",
    "6": "Figure 6. Schematic diagram of a Class I biological safety cabinet.",
    "7": "Figure 7. Schematic representation of a Class IIA1 biological safety cabinet.",
    "8": "Figure 8. Schematic diagram of a Class IIB1 biological safety cabinet.",
    "9": "Figure 9. Schematic representation of a Class III biological safety cabinet (glove box).",
    "10": "Figure 10. Gravity displacement autoclave",
    "11": "Figure 11. Examples of triple packaging systems",
    "12": "Figure 12. International radiation hazard symbol",
}


RAW_FIXED_WIDTH_TABLE_SPECS: List[RawFixedWidthTableSpec] = [
    RawFixedWidthTableSpec(
        no="A4-1",
        caption="Table A4-1. Equipment and operations that may create hazards",
        columns=["Equipment", "Hazard", "How to eliminate or reduce the hazard"],
        slices=[(0, 17), (17, 44), (44, None)],
        end_marker="In addition to microbiological hazards",
        parent_heading="Equipment safety",
    ),
    RawFixedWidthTableSpec(
        no="A4-2",
        caption="Table A4-2. Common causes of equipment-related accidents",
        columns=["Accident", "Accident cause", "Reducing or eliminating the hazard"],
        slices=[(0, 26), (26, 57), (57, None)],
        end_marker="ANNEX 5",
        parent_heading="Equipment safety",
    ),
    RawFixedWidthTableSpec(
        no="A5-1",
        caption="Table A5-1. Chemicals: hazards and precautions",
        columns=[
            "Chemical",
            "Physical properties",
            "Health hazards",
            "Fire hazards",
            "Safety precautions",
            "Incompatible chemicals / other hazards",
        ],
        slices=[(0, 24), (24, 50), (50, 76), (76, 98), (98, 125), (125, None)],
        end_marker="INDEX",
        parent_heading="Chemicals: hazards and precautions",
    ),
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
    resolved_role = role or ("structural" if kind in {"table", "table_header", "figure"} else "normative")
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


def _normalized_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().lower()


def _find_caption_idx(raw_lines: List[str], caption: str) -> Optional[int]:
    wanted = _normalized_text(caption)
    for idx, line in enumerate(raw_lines):
        joined = _normalized_text(line)
        if joined == wanted or joined.startswith(wanted):
            return idx
        if idx + 1 < len(raw_lines) and _normalized_text(f"{line} {raw_lines[idx + 1]}") == wanted:
            return idx
    return None


def _raw_block(raw_lines: List[str], caption_idx: int, max_lines: int = 90) -> List[str]:
    out: List[str] = []
    blank_run = 0
    for line in raw_lines[caption_idx : min(len(raw_lines), caption_idx + max_lines)]:
        if line.strip():
            blank_run = 0
        else:
            blank_run += 1
        out.append(line)
        if blank_run >= 3 and len(out) > 5:
            break
    return out


def _raw_table_block(raw_lines: List[str], caption_idx: int, caption: str, end_marker: str) -> List[Tuple[int, str]]:
    block: List[Tuple[int, str]] = []
    caption_token = _normalized_text(caption)
    for idx in range(caption_idx + 1, len(raw_lines)):
        line = raw_lines[idx]
        if end_marker in line:
            break
        stripped = line.strip()
        if not stripped:
            continue
        if _normalized_text(stripped) == caption_token:
            continue
        if stripped.startswith("• ") and stripped.endswith("•"):
            continue
        if stripped in {"LABORATORY BIOSAFETY MANUAL", "ANNEX 4. EQUIPMENT SAFETY", "ANNEX 5. CHEMICALS: HAZARDS AND PRECAUTIONS"}:
            continue
        if stripped == "\f":
            continue
        if re.fullmatch(r"•\s*\d+\s*•", stripped):
            continue
        if stripped.startswith("CHEMICAL") or stripped.startswith("EQUIPMENT") or stripped.startswith("ACCIDENT"):
            continue
        block.append((idx, line.rstrip()))
    return block


def _split_by_slices(line: str, slices: List[Tuple[int, Optional[int]]]) -> List[str]:
    return [line[start:end].strip() if end is not None else line[start:].strip() for start, end in slices]


def _table_node(spec: TableSpec, *, parent_nid: str, source_label: str, caption_idx: int, raw_lines: List[str]) -> Node:
    table_nid = f"{parent_nid}.tbl{spec.no}"
    table = _make_node(
        nid=table_nid,
        kind="table",
        kind_raw="table",
        num=spec.no,
        heading=spec.caption,
        text=None,
        source_label=source_label,
        line_idx=caption_idx,
        role="structural",
        data={
            "parser": PARSER_ID,
            "table_no": spec.no,
            "source_format": "fixed_width_or_captioned_block",
            "raw_lines": _raw_block(raw_lines, caption_idx),
        },
    )
    header = _make_node(
        nid=f"{table_nid}.tblh",
        kind="table_header",
        kind_raw="table_header",
        num=None,
        heading=None,
        text=" | ".join(spec.columns),
        source_label=source_label,
        line_idx=caption_idx,
        role="structural",
        data={"columns": spec.columns},
    )
    table.children.append(header)
    for row_no, cells in enumerate(spec.rows, start=1):
        header.children.append(
            _make_node(
                nid=f"{header.nid}.tblr{row_no}",
                kind="table_row",
                kind_raw="table_row",
                num=str(row_no),
                heading=None,
                text=" | ".join(cells),
                source_label=source_label,
                line_idx=caption_idx,
                data={
                    "parser": PARSER_ID,
                    "cells": cells,
                    "row_key": cells[0],
                    "raw_lines": _raw_block(raw_lines, caption_idx, max_lines=12),
                },
            )
        )
    for note_no, note in enumerate(spec.notes, start=1):
        table.children.append(
            _make_node(
                nid=f"{table_nid}.not{note_no}",
                kind="note",
                kind_raw="note",
                num=str(note_no),
                heading=None,
                text=note,
                source_label=source_label,
                line_idx=caption_idx,
                role="informative",
                data={"parser": PARSER_ID, "note_type": "table_note", "table_no": spec.no},
            )
        )
    return table


def _raw_fixed_width_table_node(
    spec: RawFixedWidthTableSpec,
    *,
    parent_nid: str,
    source_label: str,
    caption_idx: int,
    raw_lines: List[str],
) -> Node:
    block = _raw_table_block(raw_lines, caption_idx, spec.caption, spec.end_marker)
    table_nid = f"{parent_nid}.tbl{spec.no.lower().replace('-', '_')}"
    table = _make_node(
        nid=table_nid,
        kind="table",
        kind_raw="table",
        num=spec.no,
        heading=spec.caption,
        text=None,
        source_label=source_label,
        line_idx=caption_idx,
        role="structural",
        data={
            "parser": PARSER_ID,
            "table_no": spec.no,
            "source_format": "fixed_width_line_preserving_table",
            "cell_reconstruction": "fixed_width_slices_v1",
            "reconstruction_note": "Each visual source line is preserved as a table_row; blank cells represent visual rowspans/continuations.",
            "raw_lines": [line for _idx, line in block],
        },
    )
    header = _make_node(
        nid=f"{table_nid}.tblh",
        kind="table_header",
        kind_raw="table_header",
        num=None,
        heading=None,
        text=" | ".join(spec.columns),
        source_label=source_label,
        line_idx=caption_idx,
        role="structural",
        data={"columns": spec.columns},
    )
    table.children.append(header)
    for row_no, (line_idx, line) in enumerate(block, start=1):
        cells = _split_by_slices(line, spec.slices)
        header.children.append(
            _make_node(
                nid=f"{header.nid}.tblr{row_no}",
                kind="table_row",
                kind_raw="table_row",
                num=str(row_no),
                heading=None,
                text=" | ".join(cells),
                source_label=source_label,
                line_idx=line_idx,
                data={
                    "parser": PARSER_ID,
                    "cells": cells,
                    "raw_line": line,
                    "visual_row_reconstruction": "fixed_width_line_preserving",
                },
            )
        )
    return table


def _figure_node(no: str, caption: str, *, parent_nid: str, source_label: str, caption_idx: int, raw_lines: List[str]) -> Node:
    return _make_node(
        nid=f"{parent_nid}.fig{no}",
        kind="figure",
        kind_raw="figure",
        num=no,
        heading=caption,
        text=None,
        source_label=source_label,
        line_idx=caption_idx,
        role="informative",
        data={
            "parser": PARSER_ID,
            "figure_no": no,
            "caption": caption,
            "raw_lines": _raw_block(raw_lines, caption_idx, max_lines=18),
        },
    )


def _caption_token(caption: str) -> str:
    return _normalized_text(caption).rstrip(".")


def _find_target_node(root: Node, caption: str) -> Optional[Node]:
    token = _caption_token(caption)
    for _parent, node in _walk_with_parent(root):
        if node.kind in {"chapter", "annex", "part", "section", "item", "subitem", "preamble"}:
            haystack = _normalized_text(" ".join(v for v in [node.heading, node.text] if v))
            if token in haystack:
                return node
    return None


def _find_nearest_structural_node(root: Node, caption_idx: int) -> Node:
    best = root
    best_line = -1
    for _parent, node in _walk_with_parent(root):
        if node.kind not in {"chapter", "annex", "part", "section", "preamble"}:
            continue
        for span in node.source_spans:
            locator = span.get("locator")
            if not isinstance(locator, str):
                continue
            match = re.search(r"line:(\d+)", locator)
            if not match:
                continue
            line_no = int(match.group(1)) - 1
            if best_line <= line_no <= caption_idx:
                best = node
                best_line = line_no
    return best


def _find_by_heading(root: Node, heading: str) -> Optional[Node]:
    wanted = _normalized_text(heading)
    for _parent, node in _walk_with_parent(root):
        if node.kind not in {"chapter", "annex", "part", "section", "preamble"}:
            continue
        if _normalized_text(str(node.heading or "")) == wanted:
            return node
    return None


STRIP_PATTERNS: List[Tuple[re.Pattern[str], str]] = [
    (re.compile(r"\s*Table 1\. Classification of infective microorganisms by risk group.*?(?=Laboratory facilities are designated)", re.IGNORECASE | re.DOTALL), " "),
    (re.compile(r"\n?\s{0,2}1\s+Basic\s+.*?BSC, biological safety cabinet; GMT, good microbiological techniques \(see Part IV of this manual\)", re.IGNORECASE | re.DOTALL), ""),
    (re.compile(r"\s*Table 3\. Summary of biosafety level requirements.*?(?=Thus, the assignment of a biosafety level)", re.IGNORECASE | re.DOTALL), " "),
    (re.compile(r"\s*Table 4\. Animal facility containment levels: summary of practices and safety\s+equipment.*?(?=Animal facilities, like laboratories)", re.IGNORECASE | re.DOTALL), " "),
    (re.compile(r"\s*Table 8\. Selection of a biological safety cabinet \(BSC\), by type of protection needed.*?(?=air whisks aerosol particles)", re.IGNORECASE | re.DOTALL), " "),
    (re.compile(r"\s*Table 9\. Differences between Class I, II and III biological safety cabinets \(BSCs\).*?(?=Class III biological safety cabinet)", re.IGNORECASE | re.DOTALL), " "),
    (re.compile(r"\s*Table 10\. Biosafety equipment.*?(?=Pipetting aids\s+A pipetting aid)", re.IGNORECASE | re.DOTALL), " "),
    (re.compile(r"\s*Table 11\. Personal protective equipment.*?(?=manufactured with special frames)", re.IGNORECASE | re.DOTALL), " "),
    (re.compile(r"\s*Table 12\. Recommended dilutions of chlorine-releasing compounds.*?(?=Chlorine \(sodium hypochlorite\))", re.IGNORECASE | re.DOTALL), " "),
    (re.compile(r"\s*Table 13\. General rules for chemical incompatibilities.*?(?=Some solvent vapours are toxic)", re.IGNORECASE | re.DOTALL), " "),
    (re.compile(r"\s*Table 14\. Storage of compressed and liquefied gases.*?(?=For further information see references)", re.IGNORECASE | re.DOTALL), " "),
    (re.compile(r"\s*Table 15\. Types and uses of fire extinguishers.*?(?=For further information see reference)", re.IGNORECASE | re.DOTALL), " "),
    (re.compile(r"\s*Table A4-1\. Equipment and operations that may create hazards.*?(?=In addition to microbiological hazards)", re.IGNORECASE | re.DOTALL), " "),
    (re.compile(r"\s*Table A4-2\. Common causes of equipment-related accidents.*?(?=ANNEX 5|$)", re.IGNORECASE | re.DOTALL), " "),
    (re.compile(r"\s*Table A5-1\. Chemicals: hazards and precautions.*?(?=INDEX)", re.IGNORECASE | re.DOTALL), " "),
]

FIGURE_STRIP_PATTERNS = [
    re.compile(
        r"\s*Figure\s+1\. Biohazard warning sign for laboratory doors.*?Responsible Investigator named above\.",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(r"\s*Figure\s+1\. Biohazard warning sign for laboratory doors.*?(?=Personal protection)", re.IGNORECASE | re.DOTALL),
    re.compile(r"\s*Figure\s+2\. A typical Biosafety Level 1 laboratory.*?(?=Training)", re.IGNORECASE | re.DOTALL),
    re.compile(r"\s*Figure\s+3\. A typical Biosafety Level 2 laboratory.*?(?=Essential biosafety equipment)", re.IGNORECASE | re.DOTALL),
    re.compile(r"\s*Figure\s+4\. A typical Biosafety Level 3 laboratory.*?(?=a picture of the card holder)", re.IGNORECASE | re.DOTALL),
    re.compile(r"\s*Figure\s+5\. Suggested format for medical contact card", re.IGNORECASE | re.DOTALL),
    re.compile(r"\s*Figure\s+6\. Schematic diagram of a Class I biological safety cabinet\..*?(?=and then to the outside)", re.IGNORECASE | re.DOTALL),
    re.compile(r"\s*Figure\s+7\. Schematic representation of a Class IIA1 biological safety cabinet\..*?(?=fuel costs because)", re.IGNORECASE | re.DOTALL),
    re.compile(r"\s*Figure\s+8\. Schematic diagram of a Class IIB1 biological safety cabinet\..*?(?=Table 9\.)", re.IGNORECASE | re.DOTALL),
    re.compile(r"\s*Figure\s+9\. Schematic representation of a Class III biological safety cabinet \(glove box\)\..*?(?=is maintained between)", re.IGNORECASE | re.DOTALL),
    re.compile(
        r"Figure\s+10 shows the general construction of a gravity\s*displacement autoclave\..*?Figure\s+10\. Gravity displacement autoclave",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"\n\s*pressure\s+safety\s+combined pressure\s+safety\s+cotton wool.*?non-return valve\s*",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(r"\s*Figure\s+10\. Gravity displacement autoclave", re.IGNORECASE | re.DOTALL),
    re.compile(r"\s*Figure\s+11\. Examples of triple packaging systems.*?(?=\d+\. Clean and disinfect)", re.IGNORECASE | re.DOTALL),
    re.compile(r"\s*Figure\s+12\. International radiation\s+hazard symbol", re.IGNORECASE | re.DOTALL),
]


def _strip_known_blocks(text: Optional[str]) -> Optional[str]:
    if not text:
        return text
    cleaned = text
    for pattern, replacement in STRIP_PATTERNS:
        cleaned = pattern.sub(replacement, cleaned)
    for pattern in FIGURE_STRIP_PATTERNS:
        cleaned = pattern.sub(" ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    return cleaned or None


def _normalize_prose_continuation_whitespace(text: Optional[str]) -> Optional[str]:
    if not text:
        return text
    paragraphs = re.split(r"\n{2,}", text.strip())
    cleaned_paragraphs = []
    for paragraph in paragraphs:
        cleaned = re.sub(r"\s*\n\s*", " ", paragraph.strip())
        cleaned = re.sub(r" {2,}", " ", cleaned).strip()
        if cleaned:
            cleaned_paragraphs.append(cleaned)
    return "\n\n".join(cleaned_paragraphs) or None


def _remove_matching_preformatted(root: Node, captions: Iterable[str]) -> int:
    tokens = {_caption_token(caption) for caption in captions}
    removed = 0
    for _parent, node in list(_walk_with_parent(root)):
        if not node.children:
            continue
        kept = []
        for child in node.children:
            if child.kind == "preformatted":
                heading = _normalized_text(child.heading or "")
                if any(token in heading for token in tokens):
                    removed += 1
                    continue
            kept.append(child)
        node.children = kept
    return removed


def normalize_who_lbm_general_tables(
    root: Node,
    raw_lines: List[str],
    *,
    source_label: str,
    line_no_offset: int = 0,
) -> Dict[str, Any]:
    applied_tables = 0
    applied_figures = 0
    captions = [spec.caption for spec in TABLE_SPECS] + [spec.caption for spec in RAW_FIXED_WIDTH_TABLE_SPECS] + list(FIGURE_CAPTIONS.values())

    _remove_matching_preformatted(root, captions)
    for _parent, node in _walk_with_parent(root):
        if node.kind in {"chapter", "annex", "part", "section", "item", "subitem", "preamble"}:
            node.text = _normalize_prose_continuation_whitespace(_strip_known_blocks(node.text))

    for spec in TABLE_SPECS:
        caption_idx = _find_caption_idx(raw_lines, spec.caption)
        if caption_idx is None:
            continue
        target = _find_target_node(root, spec.caption) or _find_nearest_structural_node(root, caption_idx)
        target.children.append(
            _table_node(
                spec,
                parent_nid=target.nid,
                source_label=source_label,
                caption_idx=caption_idx + line_no_offset,
                raw_lines=raw_lines,
            )
        )
        applied_tables += 1

    for spec in RAW_FIXED_WIDTH_TABLE_SPECS:
        caption_idx = _find_caption_idx(raw_lines, spec.caption)
        if caption_idx is None:
            continue
        target = _find_by_heading(root, spec.parent_heading) or _find_nearest_structural_node(root, caption_idx)
        target.children.append(
            _raw_fixed_width_table_node(
                spec,
                parent_nid=target.nid,
                source_label=source_label,
                caption_idx=caption_idx + line_no_offset,
                raw_lines=raw_lines,
            )
        )
        applied_tables += 1

    for no, caption in FIGURE_CAPTIONS.items():
        caption_idx = _find_caption_idx(raw_lines, caption)
        if caption_idx is None:
            continue
        target = _find_target_node(root, caption) or _find_nearest_structural_node(root, caption_idx)
        target.children.append(
            _figure_node(
                no,
                caption,
                parent_nid=target.nid,
                source_label=source_label,
                caption_idx=caption_idx + line_no_offset,
                raw_lines=raw_lines,
            )
        )
        applied_figures += 1

    return {
        "applied": bool(applied_tables or applied_figures),
        "tables": applied_tables,
        "figures": applied_figures,
    }
