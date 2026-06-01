from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from lxml import etree

from .models_ir import Node, build_root
from .nid import NidBuilder
from .ord_key import assign_document_order
from .xml_common import flatten_text, lname, normalize_ws


ECFR_XML_USER_GUIDE = "https://www.govinfo.gov/bulkdata/ECFR/resources/ECFR-XML-User-Guide.pdf"
MARKER_RE = re.compile(r"^\((?P<num>[A-Za-z]+|[0-9]+)\)\s*")
AS_OF_RE = re.compile(r"title(?P<title>[0-9]+)_part(?P<part>[0-9A-Za-z]+)_(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})")


@dataclass
class ParsedCFR:
    title: str
    cfr_title: Optional[str]
    cfr_part: Optional[str]
    as_of: Optional[str]
    root: Node
    notes: List[str]


class _CFRNodeFactory:
    def __init__(self) -> None:
        self._nid_builder = NidBuilder()

    @staticmethod
    def _slug(value: Optional[str]) -> str:
        if not value:
            return ""
        slug = value.strip().lower().replace(".", "_")
        slug = re.sub(r"[^a-z0-9_]+", "_", slug)
        return re.sub(r"_+", "_", slug).strip("_")

    def create(
        self,
        *,
        kind: str,
        kind_raw: Optional[str],
        num: Optional[str],
        heading: Optional[str],
        text: Optional[str],
        parent_nid: str,
        locator: str,
        role: Optional[str] = None,
        normativity: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Node:
        prefix_by_kind = {
            "part": "part",
            "subpart": "subpt",
            "section": "sec",
            "paragraph": "p",
            "item": "i",
            "subitem": "si",
            "note": "note",
        }
        prefix = prefix_by_kind.get(kind, kind[:3])
        token = self._slug(num) or prefix
        if not token.startswith(prefix):
            token = f"{prefix}{token}"
        base_nid = token if parent_nid == "root" else f"{parent_nid}.{token}"
        resolved_role = role
        if resolved_role is None:
            resolved_role = "structural" if kind in {"part", "subpart", "section"} else "normative"
        resolved_normativity = normativity
        if resolved_normativity is None and resolved_role == "normative":
            resolved_normativity = "must"
        return Node(
            nid=self._nid_builder.unique(base_nid),
            kind=kind,
            kind_raw=kind_raw,
            num=num,
            ord=None,
            heading=heading,
            text=text,
            role=resolved_role,
            normativity=resolved_normativity,
            source_spans=[{"source_label": "CFR", "locator": locator}],
            data=data or {},
        )


def _metadata(elem: etree._Element) -> Dict[str, Any]:
    raw = elem.get("hierarchy_metadata")
    if not raw:
        return {}
    decoded = html.unescape(raw)
    try:
        parsed = json.loads(decoded)
    except json.JSONDecodeError:
        return {"hierarchy_metadata_raw": decoded}
    return parsed if isinstance(parsed, dict) else {}


def _head_text(elem: etree._Element) -> str:
    for child in elem:
        if lname(child) == "HEAD":
            return flatten_text(child)
    return ""


def _strip_after_dash(text: str) -> str:
    for sep in ("—", "-"):
        if sep in text:
            return normalize_ws(text.split(sep, 1)[1])
    return normalize_ws(text)


def _part_heading(elem: etree._Element) -> str:
    return _strip_after_dash(_head_text(elem))


def _subpart_heading(elem: etree._Element) -> str:
    return _strip_after_dash(_head_text(elem))


def _section_heading(elem: etree._Element) -> str:
    head = _head_text(elem)
    num = elem.get("N") or ""
    head = re.sub(r"^§\s*" + re.escape(num) + r"\s*", "", head)
    return normalize_ws(head)


def _note_text(elem: etree._Element) -> str:
    tag = lname(elem)
    if tag in {"AUTH", "SOURCE"}:
        hed = ""
        body_parts: List[str] = []
        for child in elem:
            if lname(child) == "HED":
                hed = flatten_text(child)
            else:
                text = flatten_text(child)
                if text:
                    body_parts.append(text)
        return normalize_ws(" ".join([hed, *body_parts]))
    return flatten_text(elem)


def _direct_children(elem: etree._Element, tags: set[str]) -> List[etree._Element]:
    return [child for child in elem if lname(child) in tags]


def _locator(elem: etree._Element, suffix: str = "") -> str:
    tag = lname(elem)
    n_attr = elem.get("N")
    base = f"{tag}[@N='{n_attr}']" if n_attr else tag
    return f"{base}/{suffix}" if suffix else base


def _classify_marker(raw_num: str, stack: List[Node], position: int) -> str:
    if raw_num.isdigit():
        return "item"
    lower = raw_num.lower()
    has_item_parent = any(node.kind == "item" for node in stack)
    if position > 0 and has_item_parent and re.fullmatch(r"[ivxlcdm]+", lower):
        return "subitem"
    if has_item_parent and re.fullmatch(r"[ivxlcdm]+", lower):
        return "subitem"
    return "paragraph"


def _parent_for(kind: str, stack: List[Node]) -> Node:
    if kind == "paragraph":
        for node in reversed(stack):
            if node.kind == "section":
                return node
    if kind == "item":
        for node in reversed(stack):
            if node.kind == "paragraph":
                return node
        for node in reversed(stack):
            if node.kind == "section":
                return node
    if kind == "subitem":
        for node in reversed(stack):
            if node.kind == "item":
                return node
        for node in reversed(stack):
            if node.kind == "paragraph":
                return node
    return stack[-1]


def _trim_stack_for(parent: Node, stack: List[Node]) -> List[Node]:
    idx = stack.index(parent)
    return stack[: idx + 1]


def _append_text(node: Node, text: str) -> None:
    cleaned = normalize_ws(text)
    if not cleaned:
        return
    if node.text:
        node.text = normalize_ws(f"{node.text} {cleaned}")
    else:
        node.text = cleaned


def _parse_p(elem: etree._Element, factory: _CFRNodeFactory, section: Node, stack: List[Node], index: int) -> List[Node]:
    text = flatten_text(elem)
    marker_matches: List[re.Match[str]] = []
    remainder = text
    while True:
        match = MARKER_RE.match(remainder)
        if not match:
            break
        marker_matches.append(match)
        remainder = remainder[match.end() :]

    if not marker_matches:
        _append_text(section, text)
        return [section]

    current_stack = stack
    created: Optional[Node] = None
    for pos, match in enumerate(marker_matches):
        raw_num = match.group("num")
        kind = _classify_marker(raw_num, current_stack, pos)
        parent = _parent_for(kind, current_stack)
        current_stack = _trim_stack_for(parent, current_stack)
        node = factory.create(
            kind=kind,
            kind_raw=f"({raw_num})",
            num=raw_num.lower(),
            heading=None,
            text=None,
            parent_nid=parent.nid,
            locator=f"{_locator(elem)}[{index}]",
        )
        parent.children.append(node)
        current_stack.append(node)
        created = node

    if created is not None:
        _append_text(created, remainder)
    return current_stack


def _parse_section(elem: etree._Element, factory: _CFRNodeFactory, parent: Node) -> Node:
    num = elem.get("N")
    section = factory.create(
        kind="section",
        kind_raw="§",
        num=num,
        heading=_section_heading(elem),
        text=None,
        parent_nid=parent.nid,
        locator=_locator(elem),
        data={"hierarchy_metadata": _metadata(elem)} if _metadata(elem) else None,
    )
    parent.children.append(section)

    stack = [section]
    p_index = 0
    note_index = 0
    for child in elem:
        tag = lname(child)
        if tag == "P":
            p_index += 1
            stack = _parse_p(child, factory, section, stack, p_index)
        elif tag == "CITA":
            note_index += 1
            text = _note_text(child)
            if text:
                note = factory.create(
                    kind="note",
                    kind_raw="CITA",
                    num=None,
                    heading=None,
                    text=text,
                    parent_nid=section.nid,
                    locator=f"{_locator(elem)}/CITA[{note_index}]",
                    role="informative",
                    normativity=None,
                )
                section.children.append(note)
    return section


def _parse_subpart(elem: etree._Element, factory: _CFRNodeFactory, parent: Node) -> Node:
    subpart = factory.create(
        kind="subpart",
        kind_raw="Subpart",
        num=elem.get("N"),
        heading=_subpart_heading(elem),
        text=None,
        parent_nid=parent.nid,
        locator=_locator(elem),
        data={"hierarchy_metadata": _metadata(elem)} if _metadata(elem) else None,
    )
    parent.children.append(subpart)
    for section_elem in _direct_children(elem, {"DIV8"}):
        if section_elem.get("TYPE") == "SECTION":
            _parse_section(section_elem, factory, subpart)
    return subpart


def _parse_filename(path: Path) -> Dict[str, Optional[str]]:
    match = AS_OF_RE.search(path.stem)
    if not match:
        return {"cfr_title": None, "cfr_part": None, "as_of": None}
    return {
        "cfr_title": match.group("title"),
        "cfr_part": match.group("part"),
        "as_of": match.group("date"),
    }


def parse_ecfr_xml(path: Path) -> ParsedCFR:
    tree = etree.parse(str(path))
    xml_root = tree.getroot()
    if lname(xml_root) != "DIV5" or xml_root.get("TYPE") != "PART":
        raise ValueError("eCFR parser expects a DIV5 TYPE='PART' root")

    factory = _CFRNodeFactory()
    part = factory.create(
        kind="part",
        kind_raw="PART",
        num=xml_root.get("N"),
        heading=_part_heading(xml_root),
        text=None,
        parent_nid="root",
        locator=_locator(xml_root),
        data={"hierarchy_metadata": _metadata(xml_root)} if _metadata(xml_root) else None,
    )

    note_count = 0
    for child in xml_root:
        tag = lname(child)
        if tag in {"AUTH", "SOURCE"}:
            note_count += 1
            text = _note_text(child)
            if text:
                part.children.append(
                    factory.create(
                        kind="note",
                        kind_raw=tag,
                        num=None,
                        heading=None,
                        text=text,
                        parent_nid=part.nid,
                        locator=f"{_locator(xml_root)}/{tag}[{note_count}]",
                        role="informative",
                        normativity=None,
                    )
                )
        elif tag == "DIV6" and child.get("TYPE") == "SUBPART":
            _parse_subpart(child, factory, part)

    root = build_root([part])
    assign_document_order(root)
    info = _parse_filename(path)
    cfr_title = info["cfr_title"]
    cfr_part = info["cfr_part"] or xml_root.get("N")
    title = f"{cfr_title} CFR Part {cfr_part} - {_part_heading(xml_root)}" if cfr_title and cfr_part else _head_text(xml_root)
    return ParsedCFR(
        title=title,
        cfr_title=cfr_title,
        cfr_part=cfr_part,
        as_of=info["as_of"],
        root=root,
        notes=[
            "Parsed as eCFR XML using GPO/OFR ECFR XML User Guide.",
            f"Schema reference: {ECFR_XML_USER_GUIDE}",
        ],
    )


def collect_display_names(node: Node, index: Dict[str, str]) -> None:
    label = None
    if node.kind == "part" and node.num:
        label = f"Part {node.num}"
    elif node.kind == "subpart" and node.num:
        label = f"Subpart {node.num}"
    elif node.kind == "section" and node.num:
        label = f"§ {node.num}"
    elif node.kind in {"paragraph", "item", "subitem"} and node.kind_raw:
        label = node.kind_raw
    if label and node.heading:
        label = f"{label} {node.heading}"
    if label:
        index[node.nid] = label
    for child in node.children:
        collect_display_names(child, index)
