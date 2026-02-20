from __future__ import annotations

import logging
import re
from statistics import median
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from lxml import etree

from .models_ir import Node, build_root
from .nid import IROHA_ORDER, NidBuilder, extract_digits, slug_iroha
from .ord_key import assign_document_order, normalize_num_attr, num_attr_to_segments

LOGGER = logging.getLogger(__name__)

# e-Gov law-data schema reference:
# https://laws.e-gov.go.jp/docs/law-data-basic/419a603-xml-schema-for-japanese-law/


def lname(elem: etree._Element) -> str:
    tag = elem.tag
    if isinstance(tag, str) and "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def is_subitem_tag(tag: str) -> bool:
    return tag in {"Subitem1", "Subitem2", "Subitem3", "Subitem4"}


def should_skip(elem: etree._Element) -> bool:
    def is_true(val: Optional[str]) -> bool:
        if val is None:
            return False
        return val.strip().lower() in {"true", "1"}

    return is_true(elem.get("Delete")) or is_true(elem.get("Hide"))


def text_without_rt(elem: etree._Element) -> str:
    parts: List[str] = []

    def walk(n: etree._Element) -> None:
        if n.text:
            parts.append(n.text)
        for c in n:
            if lname(c) == "Rt":
                if c.tail:
                    parts.append(c.tail)
                continue
            walk(c)
            if c.tail:
                parts.append(c.tail)

    walk(elem)
    return "".join(parts)


def extract_sentence_text(
    container: etree._Element, sentence_tag: str = "Sentence"
) -> str:
    sents = container.findall(f".//{sentence_tag}")
    return "".join(text_without_rt(s).strip() for s in sents).strip()


def extract_sentence_text_in(elem: etree._Element, container_tag: str) -> str:
    container = find_first(elem, container_tag)
    if container is None:
        return ""
    sents = container.findall(".//Sentence")
    return "".join(text_without_rt(s).strip() for s in sents).strip()


def find_first(elem: etree._Element, tag: str) -> Optional[etree._Element]:
    for child in elem.iter():
        if lname(child) == tag:
            return child
    return None


def find_text(elem: etree._Element, tag: str) -> Optional[str]:
    child = find_first(elem, tag)
    if child is None:
        return None
    text = text_without_rt(child).strip()
    return text or None


NOTE_CONTAINER_TAGS = {"Note", "Remarks"}
TABLE_WRAPPER_TAGS = {"TableStruct", "Table"}
TABLE_ROW_TAGS = {"TableHeaderRow", "TableRow"}
TABLE_CELL_TAGS = {"TableHeaderColumn", "TableColumn"}
TABLE_TITLE_TAGS = ("TableStructTitle", "TableTitle")
IROHA_LEADING_CHARS = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヰヱヲン"


def _extract_note_texts_from_direct_children(elem: etree._Element) -> List[str]:
    note_texts: List[str] = []
    for child in elem:
        if lname(child) not in NOTE_CONTAINER_TAGS:
            continue
        text = text_without_rt(child).strip()
        if text:
            note_texts.append(text)
    return note_texts


def _safe_positive_int(value: Optional[str], default: int = 1) -> int:
    if value is None:
        return default
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed > 0 else default


def _normalize_border(value: Optional[str]) -> str:
    if value is None:
        return "solid"
    return "none" if value.strip().lower() == "none" else "solid"


def _parse_table_rows(table_elem: etree._Element) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for row in table_elem:
        row_tag = lname(row)
        if row_tag not in TABLE_ROW_TAGS:
            continue
        row_is_header = row_tag == "TableHeaderRow"
        cells: List[Dict[str, Any]] = []
        for cell in row:
            cell_tag = lname(cell)
            if cell_tag not in TABLE_CELL_TAGS:
                continue
            cell_text = text_without_rt(cell).strip()
            cells.append(
                {
                    "text": cell_text,
                    "rowspan": _safe_positive_int(cell.get("rowspan"), 1),
                    "colspan": _safe_positive_int(cell.get("colspan"), 1),
                    "border_top": _normalize_border(cell.get("BorderTop")),
                    "border_bottom": _normalize_border(cell.get("BorderBottom")),
                    "border_left": _normalize_border(cell.get("BorderLeft")),
                    "border_right": _normalize_border(cell.get("BorderRight")),
                    "is_header": row_is_header or cell_tag == "TableHeaderColumn",
                }
            )
        if not cells:
            row_text = text_without_rt(row).strip()
            if row_text:
                cells.append(
                    {
                        "text": row_text,
                        "rowspan": 1,
                        "colspan": 1,
                        "border_top": "solid",
                        "border_bottom": "solid",
                        "border_left": "solid",
                        "border_right": "solid",
                        "is_header": row_is_header,
                    }
                )
        rows.append(
            {
                "is_header_row": row_is_header,
                "has_header_cell": any(c["is_header"] for c in cells),
                "cells": cells,
            }
        )
    return rows


def _rebuild_cover_from_anchors(
    anchors: Dict[str, Dict[str, Any]],
    nrows: int,
) -> Tuple[Dict[Tuple[int, int], str], int]:
    cover: Dict[Tuple[int, int], str] = {}
    ncols = 0
    for anchor_id, anchor in anchors.items():
        if anchor.get("covered"):
            continue
        r0 = int(anchor["r"])
        c0 = int(anchor["c"])
        if r0 < 0 or r0 >= nrows or c0 < 0:
            continue
        rowspan = max(1, min(int(anchor["rowspan"]), nrows - r0))
        colspan = max(1, int(anchor["colspan"]))
        anchor["rowspan"] = rowspan
        anchor["colspan"] = colspan
        for rr in range(r0, r0 + rowspan):
            for cc in range(c0, c0 + colspan):
                cover[(rr, cc)] = anchor_id
                ncols = max(ncols, cc + 1)
    return cover, ncols


def _build_table_grid(
    raw_rows: List[Dict[str, Any]],
) -> Tuple[Dict[str, Dict[str, Any]], Dict[Tuple[int, int], str], int, int]:
    anchors: Dict[str, Dict[str, Any]] = {}
    cover: Dict[Tuple[int, int], str] = {}
    nrows = len(raw_rows)
    anchor_idx = 0
    for r, row in enumerate(raw_rows):
        c = 0
        for cell in row["cells"]:
            while (r, c) in cover:
                c += 1
            anchor_id = f"a{anchor_idx}"
            anchor_idx += 1
            rowspan = max(1, int(cell["rowspan"]))
            colspan = max(1, int(cell["colspan"]))
            anchors[anchor_id] = {
                "id": anchor_id,
                "r": r,
                "c": c,
                "rowspan": rowspan,
                "colspan": colspan,
                "text": cell["text"],
                "is_header": bool(cell["is_header"]),
                "border_top": cell["border_top"],
                "border_bottom": cell["border_bottom"],
                "border_left": cell["border_left"],
                "border_right": cell["border_right"],
                "span_source": "attr" if (rowspan > 1 or colspan > 1) else "none",
                "covered": False,
            }
            for rr in range(r, min(nrows, r + rowspan)):
                for cc in range(c, c + colspan):
                    cover[(rr, cc)] = anchor_id
            c += colspan
    cover, ncols = _rebuild_cover_from_anchors(anchors, nrows)
    return anchors, cover, nrows, ncols


def _can_absorb_anchor(
    *,
    source_anchor_id: str,
    target_anchor_id: str,
    anchors: Dict[str, Dict[str, Any]],
    cover: Dict[Tuple[int, int], str],
) -> bool:
    target = anchors[target_anchor_id]
    r0 = int(target["r"])
    c0 = int(target["c"])
    for rr in range(r0, r0 + int(target["rowspan"])):
        for cc in range(c0, c0 + int(target["colspan"])):
            if cover.get((rr, cc)) != target_anchor_id:
                return False
            if cover.get((rr, cc)) == source_anchor_id:
                continue
            other = anchors.get(cover.get((rr, cc), ""))
            if other is not None and other["text"].strip():
                return False
    return True


def _infer_border_spans(
    anchors: Dict[str, Dict[str, Any]],
    cover: Dict[Tuple[int, int], str],
    nrows: int,
) -> Tuple[Dict[str, Dict[str, Any]], Dict[Tuple[int, int], str], int]:
    changed = True
    while changed:
        changed = False
        ordered_ids = sorted(
            (aid for aid, a in anchors.items() if not a.get("covered")),
            key=lambda aid: (int(anchors[aid]["r"]), int(anchors[aid]["c"])),
        )
        for anchor_id in ordered_ids:
            anchor = anchors[anchor_id]
            if anchor.get("covered"):
                continue
            if anchor["text"].strip():
                continue
            r = int(anchor["r"])
            c = int(anchor["c"])
            rowspan = int(anchor["rowspan"])
            colspan = int(anchor["colspan"])

            # implicit vertical merge from border style
            if r > 0 and anchor["border_top"] == "none":
                above_id = cover.get((r - 1, c))
                if above_id and above_id != anchor_id and not anchors[above_id].get("covered"):
                    above = anchors[above_id]
                    if above["border_bottom"] == "none" and _can_absorb_anchor(
                        source_anchor_id=above_id,
                        target_anchor_id=anchor_id,
                        anchors=anchors,
                        cover=cover,
                    ):
                        needed = (r + rowspan) - int(above["r"])
                        if needed > int(above["rowspan"]):
                            above["rowspan"] = needed
                            if above["span_source"] == "none":
                                above["span_source"] = "border"
                        anchor["covered"] = True
                        cover, _ = _rebuild_cover_from_anchors(anchors, nrows)
                        changed = True
                        continue

            # implicit horizontal merge from border style
            if c > 0 and anchor["border_left"] == "none":
                left_id = cover.get((r, c - 1))
                if left_id and left_id != anchor_id and not anchors[left_id].get("covered"):
                    left = anchors[left_id]
                    if left["border_right"] == "none" and _can_absorb_anchor(
                        source_anchor_id=left_id,
                        target_anchor_id=anchor_id,
                        anchors=anchors,
                        cover=cover,
                    ):
                        needed = (c + colspan) - int(left["c"])
                        if needed > int(left["colspan"]):
                            left["colspan"] = needed
                            if left["span_source"] == "none":
                                left["span_source"] = "border"
                        anchor["covered"] = True
                        cover, _ = _rebuild_cover_from_anchors(anchors, nrows)
                        changed = True
                        continue
    cover, ncols = _rebuild_cover_from_anchors(anchors, nrows)
    return anchors, cover, ncols


def _flatten_grid_to_rows(
    anchors: Dict[str, Dict[str, Any]],
    cover: Dict[Tuple[int, int], str],
    nrows: int,
    ncols: int,
) -> List[List[str]]:
    rows: List[List[str]] = []
    for r in range(nrows):
        row_cells: List[str] = []
        for c in range(ncols):
            anchor_id = cover.get((r, c))
            text = ""
            if anchor_id:
                text = str(anchors[anchor_id]["text"])
            row_cells.append(text)
        rows.append(row_cells)
    return rows


def _is_data_like_first_cell(cell_text: str) -> bool:
    first = cell_text.strip()
    if not first:
        return True
    patterns = (
        r"^[一二三四五六七八九十百千]+[ 　]",
        r"^[0-9０-９]+[ 　]",
        r"^(\([0-9]+\)|（[0-9０-９]+）)",
        rf"^[{IROHA_LEADING_CHARS}][ 　]",
        r"^第?[一二三四五六七八九十百千0-9０-９]+条",
        r"^法第",
    )
    if any(re.match(p, first) for p in patterns):
        return True
    return re.search(r"^.{0,8}条", first) is not None


def _avg_cell_len(cells: List[str]) -> float:
    trimmed = [c.strip() for c in cells if c.strip()]
    if not trimmed:
        return 0.0
    return sum(len(c) for c in trimmed) / len(trimmed)


def _should_promote_first_data_row_to_header(data_row_cells: List[List[str]]) -> bool:
    if len(data_row_cells) < 2:
        return False

    first_cells = data_row_cells[0]
    if len(first_cells) < 2:
        return False
    if any("。" in cell for cell in first_cells):
        return False
    if _is_data_like_first_cell(first_cells[0]):
        return False

    first_avg = _avg_cell_len(first_cells)
    if first_avg == 0.0 or first_avg > 20:
        return False

    sample_tail = data_row_cells[1:6]
    tail_avgs: List[float] = []
    for cells in sample_tail:
        avg = _avg_cell_len(cells)
        if avg > 0.0:
            tail_avgs.append(avg)
    if not tail_avgs:
        return False
    tail_median = float(median(tail_avgs))
    if tail_median <= 0.0:
        return False

    return (first_avg / tail_median) <= 0.67


def _extract_table_payload(
    wrapper_elem: etree._Element,
) -> Tuple[Optional[str], List[str], List[str], List[str], Optional[Dict[str, Any]]]:
    wrapper_tag = lname(wrapper_elem)
    heading: Optional[str] = None
    if wrapper_tag != "Table":
        for title_tag in TABLE_TITLE_TAGS:
            heading = find_text(wrapper_elem, title_tag)
            if heading:
                break

    table_elem = wrapper_elem if wrapper_tag == "Table" else find_first(wrapper_elem, "Table")
    if table_elem is None:
        return heading, [], [], _extract_note_texts_from_direct_children(wrapper_elem), None

    raw_rows = _parse_table_rows(table_elem)
    anchors, cover, nrows, ncols = _build_table_grid(raw_rows)
    anchors, cover, ncols = _infer_border_spans(anchors, cover, nrows)
    flat_rows = _flatten_grid_to_rows(anchors, cover, nrows, ncols)

    explicit_header_indices = {
        idx
        for idx, row in enumerate(raw_rows)
        if row["is_header_row"] or row["has_header_cell"]
    }
    row_entries: List[Tuple[int, List[str], str]] = []
    for idx, cells in enumerate(flat_rows):
        row_text = " | ".join(cells)
        if row_text.strip():
            row_entries.append((idx, cells, row_text))

    header_rows: List[str] = []
    data_rows: List[str] = []
    header_indices_final: set[int] = set()
    if explicit_header_indices:
        for idx, _, row_text in row_entries:
            if idx in explicit_header_indices:
                header_rows.append(row_text)
                header_indices_final.add(idx)
            else:
                data_rows.append(row_text)
    else:
        data_row_cells = [cells for _, cells, _ in row_entries]
        data_rows = [row_text for _, _, row_text in row_entries]
        if data_rows and _should_promote_first_data_row_to_header(data_row_cells):
            header_rows = [data_rows[0]]
            header_indices_final = {row_entries[0][0]}
            data_rows = data_rows[1:]

    has_merge = any(
        (int(anchor["rowspan"]) > 1 or int(anchor["colspan"]) > 1)
        for anchor in anchors.values()
        if not anchor.get("covered")
    )
    table_layout: Optional[Dict[str, Any]] = None
    if has_merge:
        header_row_count = 0
        while header_row_count in header_indices_final:
            header_row_count += 1
        table_layout = {
            "nrows": nrows,
            "ncols": ncols,
            "header_row_count": header_row_count,
            "flatten": "fill",
            "cells": [
                {
                    "r": int(anchor["r"]),
                    "c": int(anchor["c"]),
                    "rowspan": int(anchor["rowspan"]),
                    "colspan": int(anchor["colspan"]),
                    "text": str(anchor["text"]),
                    "is_header": bool(anchor["is_header"]) or int(anchor["r"]) in header_indices_final,
                    "span_source": anchor["span_source"],
                }
                for anchor in sorted(
                    (a for a in anchors.values() if not a.get("covered")),
                    key=lambda a: (int(a["r"]), int(a["c"])),
                )
            ],
        }

    note_texts = _extract_note_texts_from_direct_children(wrapper_elem)
    return heading, header_rows, data_rows, note_texts, table_layout


def _append_note_node(parent: Node, nid_builder: NidBuilder, note_text: str, kind_raw: str = "note") -> None:
    note_idx = sum(1 for child in parent.children if child.kind == "note") + 1
    parent.children.append(
        Node(
            nid=nid_builder.unique(f"{parent.nid}.note{note_idx}"),
            kind="note",
            kind_raw=kind_raw,
            num=None,
            ord=None,
            heading=None,
            text=note_text,
            role="informative",
            normativity=None,
        )
    )


def _append_table_node(
    parent: Node,
    nid_builder: NidBuilder,
    heading: Optional[str],
    header_rows: List[str],
    data_rows: List[str],
    note_texts: List[str],
    table_layout: Optional[Dict[str, Any]],
) -> None:
    table_idx = sum(1 for child in parent.children if child.kind == "table") + 1
    table_node = Node(
        nid=nid_builder.unique(f"{parent.nid}.tbl{table_idx}"),
        kind="table",
        kind_raw="table",
        num=None,
        ord=None,
        heading=heading,
        text=None,
        role="structural",
        normativity=None,
    )

    header_texts = list(header_rows)
    row_texts = list(data_rows)

    header_node = Node(
        nid=nid_builder.unique(f"{table_node.nid}.tblh"),
        kind="table_header",
        kind_raw="table_header",
        num=None,
        ord=None,
        heading=None,
        text="\n".join(header_texts) if header_texts else None,
        role="structural",
        normativity=None,
    )
    table_node.children.append(header_node)

    for row_idx, row_text in enumerate(row_texts, start=1):
        header_node.children.append(
            Node(
                nid=nid_builder.unique(f"{header_node.nid}.tblr{row_idx}"),
                kind="table_row",
                kind_raw="table_row",
                num=None,
                ord=None,
                heading=None,
                text=row_text,
                role="normative",
                normativity=None,
            )
        )

    for note_text in note_texts:
        _append_note_node(table_node, nid_builder, note_text)

    if table_layout:
        table_node.data = {"table": table_layout}

    parent.children.append(table_node)


def _attach_structured_children(
    parent: Node,
    source_elem: etree._Element,
    nid_builder: NidBuilder,
    fallback_table_heading: Optional[str] = None,
) -> None:
    table_wrappers: List[etree._Element] = []
    for child in source_elem:
        child_tag = lname(child)
        if child_tag in TABLE_WRAPPER_TAGS:
            table_wrappers.append(child)
            continue
        if child_tag.endswith("Sentence"):
            for grandchild in child:
                if lname(grandchild) in TABLE_WRAPPER_TAGS:
                    table_wrappers.append(grandchild)

    for wrapper in table_wrappers:
        heading, header_rows, data_rows, note_texts, table_layout = _extract_table_payload(wrapper)
        _append_table_node(
            parent,
            nid_builder,
            heading=heading or fallback_table_heading,
            header_rows=header_rows,
            data_rows=data_rows,
            note_texts=note_texts,
            table_layout=table_layout,
        )

    for note_text in _extract_note_texts_from_direct_children(source_elem):
        _append_note_node(parent, nid_builder, note_text)


def split_num_heading(title: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    if not title:
        return None, None
    if "　" in title:
        left, right = title.split("　", 1)
        return left.strip() or None, right.strip() or None
    if " " in title:
        left, right = title.split(" ", 1)
        return left.strip() or None, right.strip() or None
    return title.strip(), None


def detect_definition(text: Optional[str]) -> bool:
    if not text:
        return False
    return "とは" in text and ("いう" in text or "において" in text)


def local_segments_from_num_attr_or_index(
    elem: etree._Element, index: int
) -> List[int]:
    segs = num_attr_to_segments(elem.get("Num"))
    if segs:
        return segs
    return [index]


def local_segments_from_title_or_index(title: Optional[str], index: int) -> List[int]:
    digit = extract_digits(title)
    if digit is not None:
        return [digit]
    return [index]


def local_segments_from_subitem1_title(
    title: Optional[str], index: int
) -> List[int]:
    if not title:
        return [index]
    stripped = title.strip()
    if not stripped:
        return [index]
    base = IROHA_ORDER.get(stripped[0])
    if base is None:
        return local_segments_from_title_or_index(stripped, index)
    extra_digits = [
        int(raw.translate(str.maketrans("０１２３４５６７８９", "0123456789")))
        for raw in re.findall(r"[0-9０-９]+", stripped[1:])
    ]
    return [base, *extra_digits]


def build_display_name(node: Node) -> Optional[str]:
    parts: List[str] = []
    if node.num:
        parts.append(node.num)
    if node.heading:
        parts.append(node.heading)
    if not parts:
        return None
    return " ".join(parts).strip()


def collect_display_names(node: Node, index: dict) -> None:
    name = build_display_name(node)
    if name:
        index[node.nid] = name
    for child in node.children:
        collect_display_names(child, index)


@dataclass
class ParsedLaw:
    title: str
    law_id: Optional[str]
    law_number: Optional[str]
    as_of: Optional[str]
    revision_id: Optional[str]
    root: Node


def parse_egov_xml(path: Path) -> ParsedLaw:
    tree = etree.parse(str(path))
    root = tree.getroot()
    law_body = find_first(root, "LawBody")
    if law_body is None:
        law_body = root

    title = find_text(law_body, "LawTitle") or ""
    law_number = find_text(root, "LawNum") or find_text(law_body, "LawNum")
    law_id = find_text(root, "LawId") or extract_law_id_from_filename(path.name)

    nid_builder = NidBuilder()
    children: List[Node] = []

    suppl_idx = 0
    body_appdx_idx = 0
    top_idx = 0
    for child in law_body:
        tag = lname(child)
        if tag == "MainProvision":
            top_idx += 1
            children.extend(
                parse_main_provision(
                    child,
                    nid_builder,
                    parent_ord=None,
                )
            )
        elif tag == "SupplProvision":
            top_idx += 1
            suppl_idx += 1
            children.append(
                parse_suppl_provision(
                    child,
                    nid_builder,
                    local_segments=[suppl_idx],
                    parent_ord=None,
                )
            )
        elif tag.startswith("Appdx"):
            if should_skip(child):
                LOGGER.info("Skipping deleted/hidden %s under LawBody", tag)
                continue
            top_idx += 1
            body_appdx_idx += 1
            children.append(
                parse_appendix(
                    child,
                    nid_builder,
                    local_segments=[body_appdx_idx],
                    parent_ord=None,
                )
            )
        else:
            continue

    root_node = build_root(children)
    assign_document_order(root_node)

    as_of = extract_as_of_from_filename(path.name)
    revision_id = extract_revision_id_from_filename(path.name)
    return ParsedLaw(
        title=title,
        law_id=law_id,
        law_number=law_number,
        as_of=as_of,
        revision_id=revision_id,
        root=root_node,
    )


def parse_main_provision(
    main: etree._Element, nid_builder: NidBuilder, parent_ord: Optional[int]
) -> List[Node]:
    nodes: List[Node] = []
    ch_idx = 0
    sec_idx = 0
    art_idx = 0
    appdx_idx = 0
    appdx_idx = 0
    part_idx = 0
    p_idx = 0
    appdx_idx = 0
    for child in main:
        tag = lname(child)
        if tag in {"Part", "Chapter", "Section", "Article"} and should_skip(child):
            LOGGER.info("Skipping deleted/hidden %s under MainProvision", tag)
            continue
        if tag == "Chapter":
            ch_idx += 1
            try:
                nodes.append(
                    parse_chapter(
                        child,
                        nid_builder,
                        local_segments=local_segments_from_num_attr_or_index(child, ch_idx),
                        parent_ord=parent_ord,
                        scope_prefix="",
                        article_scope_prefix="",
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Chapter element")
                raise
        elif tag == "Part":
            part_idx += 1
            try:
                nodes.append(
                    parse_part(
                        child,
                        nid_builder,
                        local_segments=local_segments_from_num_attr_or_index(child, part_idx),
                        parent_ord=parent_ord,
                        parent_nid=None,
                        article_scope_prefix="",
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Part element")
                raise
        elif tag == "Section":
            sec_idx += 1
            try:
                nodes.append(
                    parse_section(
                        child,
                        nid_builder,
                        None,
                        local_segments=local_segments_from_num_attr_or_index(child, sec_idx),
                        parent_ord=parent_ord,
                        article_scope_prefix="",
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Section element")
                raise
        elif tag == "Article":
            art_idx += 1
            try:
                nodes.append(
                    parse_article(
                        child,
                        nid_builder,
                        local_segments=local_segments_from_num_attr_or_index(child, art_idx),
                        parent_ord=parent_ord,
                        scope_prefix="",
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Article element")
                raise
        elif tag == "Paragraph":
            p_idx += 1
            try:
                nodes.append(
                    parse_top_paragraph(
                        child,
                        nid_builder,
                        local_segments=local_segments_from_num_attr_or_index(child, p_idx),
                        parent_ord=parent_ord,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing top-level Paragraph")
                raise
        elif tag.startswith("Appdx"):
            try:
                if should_skip(child):
                    LOGGER.info("Skipping deleted/hidden %s under MainProvision", tag)
                    continue
                appdx_idx += 1
                nodes.append(
                    parse_appendix(
                        child,
                        nid_builder,
                        local_segments=local_segments_from_num_attr_or_index(child, appdx_idx),
                        parent_ord=parent_ord,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Appendix element")
                raise
        else:
            LOGGER.warning("Skipping unknown tag under MainProvision: %s", tag)
    return nodes


def parse_chapter(
    chapter: etree._Element,
    nid_builder: NidBuilder,
    local_segments: List[int],
    parent_ord: Optional[int],
    scope_prefix: str,
    article_scope_prefix: str = "",
) -> Node:
    title = find_text(chapter, "ChapterTitle")
    num, heading = split_num_heading(title)
    chapter_key = local_segments[0] if local_segments else 1
    chapter_nid = nid_builder.unique(f"{scope_prefix}ch{chapter_key}")
    ord_val = None
    node = Node(
        nid=chapter_nid,
        kind="chapter",
        kind_raw="章",
        num=num,
        ord=ord_val,
        heading=heading,
        text=None,
        role="structural",
        normativity=None,
    )
    sec_idx = 0
    art_idx = 0
    appdx_idx = 0
    for child in chapter:
        tag = lname(child)
        if tag in {"Section", "Article"} and should_skip(child):
            LOGGER.info("Skipping deleted/hidden %s under Chapter", tag)
            continue
        if tag == "Section":
            sec_idx += 1
            try:
                node.children.append(
                    parse_section(
                        child,
                        nid_builder,
                        chapter_nid,
                        local_segments=local_segments_from_num_attr_or_index(child, sec_idx),
                        parent_ord=node.ord,
                        article_scope_prefix=article_scope_prefix,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Section in Chapter")
                raise
        elif tag == "Article":
            art_idx += 1
            try:
                node.children.append(
                    parse_article(
                        child,
                        nid_builder,
                        local_segments=local_segments_from_num_attr_or_index(child, art_idx),
                        parent_ord=node.ord,
                        scope_prefix=article_scope_prefix,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Article in Chapter")
                raise
        elif tag.startswith("Appdx"):
            try:
                if should_skip(child):
                    LOGGER.info("Skipping deleted/hidden %s under Chapter", tag)
                    continue
                appdx_idx += 1
                node.children.append(
                    parse_appendix(
                        child,
                        nid_builder,
                        local_segments=local_segments_from_num_attr_or_index(child, appdx_idx),
                        parent_ord=node.ord,
                        scope_prefix=article_scope_prefix,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Appendix in Chapter")
                raise
        else:
            if tag != "ChapterTitle":
                LOGGER.warning("Skipping unknown tag under Chapter: %s", tag)
    return node


def parse_section(
    section: etree._Element,
    nid_builder: NidBuilder,
    parent_nid: Optional[str],
    local_segments: List[int],
    parent_ord: Optional[int],
    article_scope_prefix: str = "",
) -> Node:
    title = find_text(section, "SectionTitle")
    num, heading = split_num_heading(title)
    prefix = f"{parent_nid}." if parent_nid else ""
    sec_key = local_segments[0] if local_segments else 1
    ord_val = None
    node = Node(
        nid=nid_builder.unique(f"{prefix}sec{sec_key}"),
        kind="section",
        kind_raw="節",
        num=num,
        ord=ord_val,
        heading=heading,
        text=None,
        role="structural",
        normativity=None,
    )
    art_idx = 0
    appdx_idx = 0
    for child in section:
        tag = lname(child)
        if tag in {"Subsection", "Division", "Article"} and should_skip(child):
            LOGGER.info("Skipping deleted/hidden %s under Section", tag)
            continue
        if tag == "Article":
            art_idx += 1
            try:
                node.children.append(
                    parse_article(
                        child,
                        nid_builder,
                        local_segments=local_segments_from_num_attr_or_index(child, art_idx),
                        parent_ord=node.ord,
                        scope_prefix=article_scope_prefix,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Article in Section")
                raise
        elif tag == "Subsection":
            try:
                node.children.append(
                    parse_subsection(
                        child,
                        nid_builder,
                        node.nid,
                        local_segments=local_segments_from_num_attr_or_index(
                            child, len(node.children) + 1
                        ),
                        parent_ord=node.ord,
                        article_scope_prefix=article_scope_prefix,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Subsection in Section")
                raise
        elif tag == "Division":
            try:
                node.children.append(
                    parse_division(
                        child,
                        nid_builder,
                        node.nid,
                        local_segments=local_segments_from_num_attr_or_index(
                            child, len(node.children) + 1
                        ),
                        parent_ord=node.ord,
                        article_scope_prefix=article_scope_prefix,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Division in Section")
                raise
        elif tag.startswith("Appdx"):
            try:
                if should_skip(child):
                    LOGGER.info("Skipping deleted/hidden %s under Section", tag)
                    continue
                appdx_idx += 1
                node.children.append(
                    parse_appendix(
                        child,
                        nid_builder,
                        local_segments=local_segments_from_num_attr_or_index(child, appdx_idx),
                        parent_ord=node.ord,
                        scope_prefix=article_scope_prefix,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Appendix in Section")
                raise
        else:
            if tag != "SectionTitle":
                LOGGER.warning("Skipping unknown tag under Section: %s", tag)
    return node


def parse_article(
    article: etree._Element,
    nid_builder: NidBuilder,
    local_segments: List[int],
    parent_ord: Optional[int],
    scope_prefix: str = "",
) -> Node:
    num = find_text(article, "ArticleTitle")
    heading = find_text(article, "ArticleCaption")
    num_attr = article.get("Num")
    normalized_num = normalize_num_attr(num_attr)
    ord_val = None

    paragraphs = [c for c in article if lname(c) == "Paragraph"]
    fold = False
    if len(paragraphs) == 1:
        p = paragraphs[0]
        p_num_text = find_text(p, "ParagraphNum")
        p_attr = p.get("Num")
        fold = (p_num_text is None or p_num_text == "") and (p_attr in (None, "", "1"))

    article_key = normalized_num or str(local_segments[0])
    article_nid = nid_builder.unique(f"{scope_prefix}art{article_key}")
    node = Node(
        nid=article_nid,
        kind="article",
        kind_raw="条",
        num=num,
        ord=ord_val,
        heading=heading,
        text=None,
        role="normative",
        normativity="must",
    )

    if fold and paragraphs:
        text = extract_sentence_text_in(paragraphs[0], "ParagraphSentence")
        node.text = text or None
        if detect_definition(text):
            node.role = "definition"
        i_idx = 0
        s_idx = 0
        for child in paragraphs[0]:
            tag = lname(child)
            if tag == "Item":
                i_idx += 1
                try:
                    node.children.append(
                        parse_item(
                            child,
                            nid_builder,
                            article_nid,
                            local_segments=local_segments_from_num_attr_or_index(child, i_idx),
                            parent_ord=node.ord,
                        )
                    )
                except Exception:
                    LOGGER.exception("Failed while parsing Item in folded Article")
                    raise
            elif is_subitem_tag(tag):
                s_idx += 1
                try:
                    node.children.append(
                        parse_subitem(
                            child,
                            nid_builder,
                            article_nid,
                            local_segments=local_segments_from_subitem1_title(
                                find_text(child, "Subitem1Title"),
                                s_idx,
                            )
                            if lname(child) == "Subitem1"
                            else local_segments_from_title_or_index(
                                find_text(child, f"{lname(child)}Title"), s_idx
                            ),
                            parent_ord=node.ord,
                        )
                    )
                except Exception:
                    LOGGER.exception("Failed while parsing Subitem in folded Article")
                    raise
        _attach_structured_children(node, paragraphs[0], nid_builder)
    else:
        p_idx = 0
        appdx_idx = 0
        for p in paragraphs:
            p_idx += 1
            try:
                node.children.append(
                    parse_paragraph(
                        p,
                        nid_builder,
                        article_nid,
                        local_segments=local_segments_from_num_attr_or_index(p, p_idx),
                        parent_ord=node.ord,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Paragraph")
                raise
        for child in article:
            tag = lname(child)
            if tag in {"ArticleTitle", "ArticleCaption", "Paragraph"}:
                continue
            if tag.startswith("Appdx"):
                try:
                    if should_skip(child):
                        LOGGER.info("Skipping deleted/hidden %s under Article", tag)
                        continue
                    appdx_idx += 1
                    node.children.append(
                        parse_appendix(
                            child,
                            nid_builder,
                            local_segments=local_segments_from_num_attr_or_index(
                                child, appdx_idx
                            ),
                            parent_ord=node.ord,
                            scope_prefix=scope_prefix,
                        )
                    )
                except Exception:
                    LOGGER.exception("Failed while parsing Appendix in Article")
                    raise
        _attach_structured_children(node, article, nid_builder)
    return node


def parse_part(
    part: etree._Element,
    nid_builder: NidBuilder,
    local_segments: List[int],
    parent_ord: Optional[int],
    parent_nid: Optional[str],
    article_scope_prefix: str = "",
) -> Node:
    title = find_text(part, "PartTitle")
    num, heading = split_num_heading(title)
    part_key = local_segments[0] if local_segments else 1
    ord_val = None
    prefix = f"{parent_nid}." if parent_nid else ""
    node = Node(
        nid=nid_builder.unique(f"{prefix}part{part_key}"),
        kind="part",
        kind_raw="編",
        num=num,
        ord=ord_val,
        heading=heading,
        text=None,
        role="structural",
        normativity=None,
    )
    ch_idx = 0
    art_idx = 0
    appdx_idx = 0
    for child in part:
        tag = lname(child)
        if tag in {"Chapter", "Article"} and should_skip(child):
            LOGGER.info("Skipping deleted/hidden %s under Part", tag)
            continue
        if tag == "Chapter":
            ch_idx += 1
            try:
                node.children.append(
                    parse_chapter(
                        child,
                        nid_builder,
                        local_segments=local_segments_from_num_attr_or_index(child, ch_idx),
                        parent_ord=node.ord,
                        scope_prefix=f"{node.nid}.",
                        article_scope_prefix=article_scope_prefix,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Chapter in Part")
                raise
        elif tag == "Article":
            art_idx += 1
            try:
                node.children.append(
                    parse_article(
                        child,
                        nid_builder,
                        local_segments=local_segments_from_num_attr_or_index(child, art_idx),
                        parent_ord=node.ord,
                        scope_prefix=article_scope_prefix,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Article in Part")
                raise
        elif tag.startswith("Appdx"):
            try:
                if should_skip(child):
                    LOGGER.info("Skipping deleted/hidden %s under Part", tag)
                    continue
                appdx_idx += 1
                node.children.append(
                    parse_appendix(
                        child,
                        nid_builder,
                        local_segments=local_segments_from_num_attr_or_index(child, appdx_idx),
                        parent_ord=node.ord,
                        scope_prefix=article_scope_prefix,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Appendix in Part")
                raise
    return node


def parse_subsection(
    subsection: etree._Element,
    nid_builder: NidBuilder,
    parent_nid: str,
    local_segments: List[int],
    parent_ord: Optional[int],
    article_scope_prefix: str = "",
) -> Node:
    title = find_text(subsection, "SubsectionTitle")
    num, heading = split_num_heading(title)
    subsec_key = local_segments[0] if local_segments else 1
    ord_val = None
    node = Node(
        nid=nid_builder.unique(f"{parent_nid}.subsec{subsec_key}"),
        kind="subsection",
        kind_raw="款",
        num=num,
        ord=ord_val,
        heading=heading,
        text=None,
        role="structural",
        normativity=None,
    )
    art_idx = 0
    appdx_idx = 0
    for child in subsection:
        tag = lname(child)
        if tag in {"Division", "Article"} and should_skip(child):
            LOGGER.info("Skipping deleted/hidden %s under Subsection", tag)
            continue
        if tag == "Division":
            try:
                node.children.append(
                    parse_division(
                        child,
                        nid_builder,
                        node.nid,
                        local_segments=local_segments_from_num_attr_or_index(
                            child, len(node.children) + 1
                        ),
                        parent_ord=node.ord,
                        article_scope_prefix=article_scope_prefix,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Division in Subsection")
                raise
        elif tag == "Article":
            art_idx += 1
            try:
                node.children.append(
                    parse_article(
                        child,
                        nid_builder,
                        local_segments=local_segments_from_num_attr_or_index(child, art_idx),
                        parent_ord=node.ord,
                        scope_prefix=article_scope_prefix,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Article in Subsection")
                raise
        elif tag.startswith("Appdx"):
            try:
                if should_skip(child):
                    LOGGER.info("Skipping deleted/hidden %s under Subsection", tag)
                    continue
                appdx_idx += 1
                node.children.append(
                    parse_appendix(
                        child,
                        nid_builder,
                        local_segments=local_segments_from_num_attr_or_index(child, appdx_idx),
                        parent_ord=node.ord,
                        scope_prefix=article_scope_prefix,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Appendix in Subsection")
                raise
    return node


def parse_division(
    division: etree._Element,
    nid_builder: NidBuilder,
    parent_nid: str,
    local_segments: List[int],
    parent_ord: Optional[int],
    article_scope_prefix: str = "",
) -> Node:
    title = find_text(division, "DivisionTitle")
    num, heading = split_num_heading(title)
    div_key = local_segments[0] if local_segments else 1
    ord_val = None
    node = Node(
        nid=nid_builder.unique(f"{parent_nid}.div{div_key}"),
        kind="division",
        kind_raw="目",
        num=num,
        ord=ord_val,
        heading=heading,
        text=None,
        role="structural",
        normativity=None,
    )
    art_idx = 0
    appdx_idx = 0
    for child in division:
        tag = lname(child)
        if tag == "Article" and should_skip(child):
            LOGGER.info("Skipping deleted/hidden %s under Division", tag)
            continue
        if tag == "Article":
            art_idx += 1
            try:
                node.children.append(
                    parse_article(
                        child,
                        nid_builder,
                        local_segments=local_segments_from_num_attr_or_index(child, art_idx),
                        parent_ord=node.ord,
                        scope_prefix=article_scope_prefix,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Article in Division")
                raise
        elif tag.startswith("Appdx"):
            try:
                if should_skip(child):
                    LOGGER.info("Skipping deleted/hidden %s under Division", tag)
                    continue
                appdx_idx += 1
                node.children.append(
                    parse_appendix(
                        child,
                        nid_builder,
                        local_segments=local_segments_from_num_attr_or_index(child, appdx_idx),
                        parent_ord=node.ord,
                        scope_prefix=article_scope_prefix,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Appendix in Division")
                raise
    return node


def parse_top_paragraph(
    paragraph: etree._Element,
    nid_builder: NidBuilder,
    local_segments: List[int],
    parent_ord: Optional[int],
    scope_prefix: str = "mp",
) -> Node:
    p_num_text = find_text(paragraph, "ParagraphNum")
    num = p_num_text or "1"
    p_key = local_segments[0] if local_segments else 1
    p_ord = None
    heading = find_text(paragraph, "ParagraphCaption")
    text = extract_sentence_text_in(paragraph, "ParagraphSentence")
    node = Node(
        nid=nid_builder.unique(f"{scope_prefix}.p{p_key}"),
        kind="paragraph",
        kind_raw="項",
        num=num,
        ord=p_ord,
        heading=heading,
        text=text or None,
        role="normative",
        normativity="must",
    )
    if detect_definition(text):
        node.role = "definition"
    i_idx = 0
    s_idx = 0
    for child in paragraph:
        tag = lname(child)
        if tag == "Item":
            i_idx += 1
            try:
                node.children.append(
                    parse_item(
                        child,
                        nid_builder,
                        node.nid,
                        local_segments=local_segments_from_num_attr_or_index(child, i_idx),
                        parent_ord=node.ord,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Item in top-level Paragraph")
                raise
        elif is_subitem_tag(tag):
            s_idx += 1
            title = find_text(child, f"{tag}Title")
            if tag == "Subitem1":
                local_sub_segs = local_segments_from_subitem1_title(title, s_idx)
            else:
                local_sub_segs = (
                    num_attr_to_segments(child.get("Num"))
                    or local_segments_from_title_or_index(title, s_idx)
                )
            try:
                node.children.append(
                    parse_subitem(
                        child,
                        nid_builder,
                        node.nid,
                        local_segments=local_sub_segs,
                        parent_ord=node.ord,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Subitem in top-level Paragraph")
                raise
    _attach_structured_children(node, paragraph, nid_builder)
    return node


def parse_paragraph(
    paragraph: etree._Element,
    nid_builder: NidBuilder,
    article_nid: str,
    local_segments: List[int],
    parent_ord: Optional[int],
) -> Node:
    p_num_text = find_text(paragraph, "ParagraphNum")
    num = p_num_text or "1"
    p_key = local_segments[0] if local_segments else 1
    p_ord = None
    heading = find_text(paragraph, "ParagraphCaption")
    text = extract_sentence_text_in(paragraph, "ParagraphSentence")
    node = Node(
        nid=nid_builder.unique(f"{article_nid}.p{p_key}"),
        kind="paragraph",
        kind_raw="項",
        num=num,
        ord=p_ord,
        heading=heading,
        text=text or None,
        role="normative",
        normativity="must",
    )
    if detect_definition(text):
        node.role = "definition"
    i_idx = 0
    s_idx = 0
    for child in paragraph:
        tag = lname(child)
        if tag == "Item":
            i_idx += 1
            try:
                node.children.append(
                    parse_item(
                        child,
                        nid_builder,
                        node.nid,
                        local_segments=local_segments_from_num_attr_or_index(child, i_idx),
                        parent_ord=node.ord,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Item in Paragraph")
                raise
        elif is_subitem_tag(tag):
            s_idx += 1
            title = find_text(child, f"{tag}Title")
            if tag == "Subitem1":
                local_sub_segs = local_segments_from_subitem1_title(title, s_idx)
            else:
                local_sub_segs = (
                    num_attr_to_segments(child.get("Num"))
                    or local_segments_from_title_or_index(title, s_idx)
                )
            try:
                node.children.append(
                    parse_subitem(
                        child,
                        nid_builder,
                        node.nid,
                        local_segments=local_sub_segs,
                        parent_ord=node.ord,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Subitem in Paragraph")
                raise
    _attach_structured_children(node, paragraph, nid_builder)
    return node


def parse_item(
    item: etree._Element,
    nid_builder: NidBuilder,
    parent_nid: str,
    local_segments: List[int],
    parent_ord: Optional[int],
) -> Node:
    num = find_text(item, "ItemTitle")
    i_key = local_segments[0] if local_segments else 1
    i_ord = None
    text = extract_sentence_text_in(item, "ItemSentence")
    nid = f"{parent_nid}.i{i_key}"
    node = Node(
        nid=nid_builder.unique(nid),
        kind="item",
        kind_raw="号",
        num=num,
        ord=i_ord,
        heading=None,
        text=text or None,
        role="normative",
        normativity="must",
    )
    if detect_definition(text):
        node.role = "definition"
    s_idx = 0
    for child in item:
        tag = lname(child)
        if is_subitem_tag(tag):
            s_idx += 1
            title = find_text(child, f"{tag}Title")
            if tag == "Subitem1":
                local_sub_segs = local_segments_from_subitem1_title(title, s_idx)
            else:
                local_sub_segs = (
                    num_attr_to_segments(child.get("Num"))
                    or local_segments_from_title_or_index(title, s_idx)
                )
            try:
                node.children.append(
                    parse_subitem(
                        child,
                        nid_builder,
                        node.nid,
                        local_segments=local_sub_segs,
                        parent_ord=node.ord,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Subitem in Item")
                raise
    _attach_structured_children(node, item, nid_builder)
    return node


def parse_subitem(
    elem: etree._Element,
    nid_builder: NidBuilder,
    parent_nid: str,
    local_segments: List[int],
    parent_ord: Optional[int],
) -> Node:
    tag = lname(elem)
    title = find_text(elem, f"{tag}Title")
    sentence_tag = f"{tag}Sentence"
    text = extract_sentence_text_in(elem, sentence_tag)

    kind = "subitem" if tag == "Subitem1" else "point"
    kind_raw = title or ("イロハ" if tag == "Subitem1" else tag)

    slug = slug_iroha(title) if tag == "Subitem1" else None
    ord_val = None
    seg_key = local_segments[0] if local_segments else 1

    if tag == "Subitem1" and slug:
        nid = f"{parent_nid}.{slug}"
    elif tag == "Subitem1":
        nid = f"{parent_nid}.s{seg_key}"
    else:
        nid = f"{parent_nid}.pt{seg_key}"

    node = Node(
        nid=nid_builder.unique(nid),
        kind=kind,
        kind_raw=kind_raw,
        num=title,
        ord=ord_val,
        heading=None,
        text=text or None,
        role="normative",
        normativity="must",
    )
    if detect_definition(text):
        node.role = "definition"
    sub_idx = 0
    for child in elem:
        child_tag = lname(child)
        if is_subitem_tag(child_tag):
            sub_idx += 1
            child_title = find_text(child, f"{child_tag}Title")
            if child_tag == "Subitem1":
                local_sub_segs = local_segments_from_subitem1_title(child_title, sub_idx)
            else:
                local_sub_segs = (
                    num_attr_to_segments(child.get("Num"))
                    or local_segments_from_title_or_index(child_title, sub_idx)
                )
            try:
                node.children.append(
                    parse_subitem(
                        child,
                        nid_builder,
                        node.nid,
                        local_segments=local_sub_segs,
                        parent_ord=node.ord,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing nested Subitem")
                raise
    _attach_structured_children(node, elem, nid_builder)
    return node


def parse_appendix(
    elem: etree._Element,
    nid_builder: NidBuilder,
    local_segments: List[int],
    parent_ord: Optional[int],
    scope_prefix: str = "",
) -> Node:
    return parse_appdx(
        elem,
        nid_builder,
        scope_prefix=scope_prefix,
        local_segments=local_segments,
        parent_ord=parent_ord,
    )


def appendix_kind_key(tag: str) -> str:
    base_tag = tag.replace("SupplProvision", "", 1)
    mapping = {
        "AppdxTable": "appdx_table",
        "AppdxNote": "appdx_note",
        "AppdxStyle": "appdx_style",
        "Appdx": "appdx",
        "AppdxFig": "appdx_fig",
        "AppdxFormat": "appdx_format",
    }
    return mapping.get(base_tag, "appdx")


def parse_appdx(
    elem: etree._Element,
    nid_builder: NidBuilder,
    scope_prefix: str,
    local_segments: List[int],
    parent_ord: Optional[int],
) -> Node:
    tag = lname(elem)
    base_tag = tag.replace("SupplProvision", "", 1)
    key = appendix_kind_key(tag)
    title_keys = {
        "AppdxTable": ["SupplProvisionAppdxTableTitle", "AppdxTableTitle"],
        "AppdxNote": ["SupplProvisionAppdxNoteTitle", "AppdxNoteTitle"],
        "AppdxStyle": ["SupplProvisionAppdxStyleTitle", "AppdxStyleTitle"],
        "AppdxFig": ["SupplProvisionAppdxFigTitle", "AppdxFigTitle"],
        "AppdxFormat": ["SupplProvisionAppdxFormatTitle", "AppdxFormatTitle"],
        "Appdx": [
            "SupplProvisionAppdxTitle",
            "AppdxTitle",
            "ArithFormulaTitle",
            "ArithFormulaNum",
        ],
    }
    title = None
    for title_key in title_keys.get(base_tag, []):
        title = find_text(elem, title_key)
        if title:
            break
    if title is None and base_tag == "Appdx":
        title = find_text(elem, "ArithFormulaNum")
    ord_val = None
    normalized_num = normalize_num_attr(elem.get("Num"))
    suffix = normalized_num or "_".join(str(seg) for seg in local_segments)
    prefix = f"{scope_prefix}" if scope_prefix else ""
    nid = nid_builder.unique(f"{prefix}{key}{suffix}")
    text = text_without_rt(elem).strip() or None
    node = Node(
        nid=nid,
        kind="appendix",
        kind_raw=tag,
        num=title,
        ord=ord_val,
        heading=None,
        text=text or None,
        role="structural",
        normativity=None,
    )
    _attach_structured_children(
        node,
        elem,
        nid_builder,
        fallback_table_heading=title if base_tag == "AppdxTable" else None,
    )
    return node


def parse_suppl_provision(
    suppl: etree._Element,
    nid_builder: NidBuilder,
    local_segments: List[int],
    parent_ord: Optional[int],
) -> Node:
    annex_key = local_segments[0] if local_segments else 1
    ord_val = None
    node = Node(
        nid=nid_builder.unique(f"annex{annex_key}"),
        kind="annex",
        kind_raw="附則",
        num=find_text(suppl, "SupplProvisionLabel"),
        ord=ord_val,
        heading=None,
        text=None,
        role="structural",
        normativity=None,
    )
    art_idx = 0
    ch_idx = 0
    p_idx = 0
    appdx_idx = 0
    for child in suppl:
        tag = lname(child)
        if tag in {"Chapter", "Paragraph", "Article"} and should_skip(child):
            LOGGER.info("Skipping deleted/hidden %s in SupplProvision", tag)
            continue
        if tag == "Chapter":
            ch_idx += 1
            try:
                node.children.append(
                    parse_chapter(
                        child,
                        nid_builder,
                        local_segments=local_segments_from_num_attr_or_index(child, ch_idx),
                        parent_ord=node.ord,
                        scope_prefix=f"{node.nid}.",
                        article_scope_prefix=f"{node.nid}.",
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Chapter in SupplProvision")
                raise
        elif tag == "Paragraph":
            p_idx += 1
            try:
                node.children.append(
                    parse_top_paragraph(
                        child,
                        nid_builder,
                        local_segments=local_segments_from_num_attr_or_index(child, p_idx),
                        parent_ord=node.ord,
                        scope_prefix=node.nid,
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Paragraph in SupplProvision")
                raise
        elif tag == "Article":
            art_idx += 1
            try:
                node.children.append(
                    parse_article(
                        child,
                        nid_builder,
                        local_segments=local_segments_from_num_attr_or_index(child, art_idx),
                        parent_ord=node.ord,
                        scope_prefix=f"{node.nid}.",
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Article in SupplProvision")
                raise
        elif tag.startswith("SupplProvisionAppdx"):
            try:
                if should_skip(child):
                    LOGGER.info("Skipping deleted/hidden %s in SupplProvision", tag)
                    continue
                appdx_idx += 1
                node.children.append(
                    parse_appendix(
                        child,
                        nid_builder,
                        local_segments=local_segments_from_num_attr_or_index(child, appdx_idx),
                        parent_ord=node.ord,
                        scope_prefix=f"{node.nid}.",
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Appendix in SupplProvision")
                raise
    return node


def extract_as_of_from_filename(name: str) -> Optional[str]:
    m = re.search(r"_(\d{8})_", name)
    if not m:
        m = re.search(r"(\d{8})", name)
        if not m:
            return None
    raw = m.group(1)
    return f"{raw[0:4]}-{raw[4:6]}-{raw[6:8]}"




def extract_revision_id_from_filename(name: str) -> Optional[str]:
    m = re.search(r"_(\d{8})_([0-9A-Za-z]+)", name)
    if not m:
        return None
    return m.group(2)


def extract_law_id_from_filename(name: str) -> Optional[str]:
    m = re.match(r"([0-9A-Za-z]+)_", name)
    if not m:
        return None
    return m.group(1)
