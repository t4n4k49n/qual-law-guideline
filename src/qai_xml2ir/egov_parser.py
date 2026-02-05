from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

from lxml import etree

from .models_ir import Node, build_root
from .nid import NidBuilder, extract_digits, slug_iroha

LOGGER = logging.getLogger(__name__)

# e-Gov law-data schema reference:
# https://laws.e-gov.go.jp/docs/law-data-basic/419a603-xml-schema-for-japanese-law/


def lname(elem: etree._Element) -> str:
    tag = elem.tag
    if isinstance(tag, str) and "}" in tag:
        return tag.split("}", 1)[1]
    return tag


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


def ord_from_attr_or_index(elem: etree._Element, index: int) -> Optional[int]:
    num = elem.get("Num")
    if num:
        try:
            return int(num)
        except ValueError:
            return extract_digits(num)
    return index


def normalize_num_attr(num: Optional[str]) -> Optional[str]:
    if not num:
        return None
    normalized = num.translate(str.maketrans("０１２３４５６７８９", "0123456789"))
    cleaned = re.sub(r"[^0-9_]", "", normalized)
    return cleaned or None


def major_ord_from_num_attr(num: Optional[str]) -> Optional[int]:
    normalized = normalize_num_attr(num)
    if not normalized:
        return None
    head = normalized.split("_", 1)[0]
    if not head:
        return None
    try:
        return int(head)
    except ValueError:
        return None


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

    main = find_first(law_body, "MainProvision")
    if main is not None:
        children.extend(parse_main_provision(main, nid_builder))

    suppl_nodes = []
    for child in law_body:
        if lname(child) == "SupplProvision":
            suppl_nodes.append(
                parse_suppl_provision(child, nid_builder, len(suppl_nodes) + 1)
            )
    children.extend(suppl_nodes)

    root_node = build_root(children)

    as_of = extract_as_of_from_filename(path.name)
    return ParsedLaw(
        title=title,
        law_id=law_id,
        law_number=law_number,
        as_of=as_of,
        root=root_node,
    )


def parse_main_provision(
    main: etree._Element, nid_builder: NidBuilder
) -> List[Node]:
    nodes: List[Node] = []
    ch_idx = 0
    sec_idx = 0
    art_idx = 0
    for child in main:
        tag = lname(child)
        if tag == "Chapter":
            ch_idx += 1
            try:
                nodes.append(parse_chapter(child, nid_builder, ch_idx))
            except Exception:
                LOGGER.exception("Failed while parsing Chapter element")
                raise
        elif tag == "Section":
            sec_idx += 1
            try:
                nodes.append(parse_section(child, nid_builder, None, sec_idx))
            except Exception:
                LOGGER.exception("Failed while parsing Section element")
                raise
        elif tag == "Article":
            art_idx += 1
            try:
                nodes.append(
                    parse_article(
                        child, nid_builder, ord_from_attr_or_index(child, art_idx)
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Article element")
                raise
        elif tag.startswith("Appdx"):
            try:
                nodes.append(parse_appendix(child, nid_builder, len(nodes) + 1))
            except Exception:
                LOGGER.exception("Failed while parsing Appendix element")
                raise
        else:
            LOGGER.warning("Skipping unknown tag under MainProvision: %s", tag)
    return nodes


def parse_chapter(
    chapter: etree._Element, nid_builder: NidBuilder, ch_ord: int
) -> Node:
    title = find_text(chapter, "ChapterTitle")
    num, heading = split_num_heading(title)
    node = Node(
        nid=nid_builder.unique(f"ch{ch_ord}"),
        kind="chapter",
        kind_raw="章",
        num=num,
        ord=ch_ord,
        heading=heading,
        text=None,
        role="structural",
        normativity=None,
    )
    sec_idx = 0
    art_idx = 0
    for child in chapter:
        tag = lname(child)
        if tag == "Section":
            sec_idx += 1
            try:
                node.children.append(parse_section(child, nid_builder, ch_ord, sec_idx))
            except Exception:
                LOGGER.exception("Failed while parsing Section in Chapter")
                raise
        elif tag == "Article":
            art_idx += 1
            try:
                node.children.append(
                    parse_article(
                        child, nid_builder, ord_from_attr_or_index(child, art_idx)
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Article in Chapter")
                raise
        elif tag.startswith("Appdx"):
            try:
                node.children.append(
                    parse_appendix(child, nid_builder, len(node.children) + 1)
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
    ch_ord: Optional[int],
    sec_ord: int,
) -> Node:
    title = find_text(section, "SectionTitle")
    num, heading = split_num_heading(title)
    prefix = f"ch{ch_ord}." if ch_ord is not None else ""
    node = Node(
        nid=nid_builder.unique(f"{prefix}sec{sec_ord}"),
        kind="section",
        kind_raw="節",
        num=num,
        ord=sec_ord,
        heading=heading,
        text=None,
        role="structural",
        normativity=None,
    )
    art_idx = 0
    for child in section:
        tag = lname(child)
        if tag == "Article":
            art_idx += 1
            try:
                node.children.append(
                    parse_article(
                        child, nid_builder, ord_from_attr_or_index(child, art_idx)
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Article in Section")
                raise
        elif tag.startswith("Appdx"):
            try:
                node.children.append(
                    parse_appendix(child, nid_builder, len(node.children) + 1)
                )
            except Exception:
                LOGGER.exception("Failed while parsing Appendix in Section")
                raise
        else:
            if tag != "SectionTitle":
                LOGGER.warning("Skipping unknown tag under Section: %s", tag)
    return node


def parse_article(
    article: etree._Element, nid_builder: NidBuilder, art_ord: Optional[int]
) -> Node:
    num = find_text(article, "ArticleTitle")
    heading = find_text(article, "ArticleCaption")
    num_attr = article.get("Num")
    normalized_num = normalize_num_attr(num_attr)
    art_ord = major_ord_from_num_attr(num_attr) or art_ord or 0

    paragraphs = [c for c in article if lname(c) == "Paragraph"]
    fold = False
    if len(paragraphs) == 1:
        p = paragraphs[0]
        p_num_text = find_text(p, "ParagraphNum")
        p_attr = p.get("Num")
        fold = (p_num_text is None or p_num_text == "") and (p_attr in (None, "", "1"))

    node = Node(
        nid=nid_builder.unique(f"art{normalized_num or art_ord}"),
        kind="article",
        kind_raw="条",
        num=num,
        ord=art_ord,
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
        for child in paragraphs[0]:
            tag = lname(child)
            if tag == "Item":
                i_idx += 1
                try:
                    node.children.append(
                        parse_item(child, nid_builder, art_ord, None, i_idx)
                    )
                except Exception:
                    LOGGER.exception("Failed while parsing Item in folded Article")
                    raise
            elif tag.startswith("Subitem"):
                try:
                    node.children.append(
                        parse_subitem(child, nid_builder, art_ord, None, None)
                    )
                except Exception:
                    LOGGER.exception("Failed while parsing Subitem in folded Article")
                    raise
    else:
        p_idx = 0
        for p in paragraphs:
            p_idx += 1
            try:
                node.children.append(parse_paragraph(p, nid_builder, art_ord, p_idx))
            except Exception:
                LOGGER.exception("Failed while parsing Paragraph")
                raise
        for child in article:
            tag = lname(child)
            if tag in {"ArticleTitle", "ArticleCaption", "Paragraph"}:
                continue
            if tag.startswith("Appdx"):
                try:
                    node.children.append(
                        parse_appendix(child, nid_builder, len(node.children) + 1)
                    )
                except Exception:
                    LOGGER.exception("Failed while parsing Appendix in Article")
                    raise
    return node


def parse_paragraph(
    paragraph: etree._Element,
    nid_builder: NidBuilder,
    art_ord: int,
    p_idx: int,
) -> Node:
    p_num_text = find_text(paragraph, "ParagraphNum")
    num = p_num_text or "1"
    p_ord = ord_from_attr_or_index(paragraph, p_idx) or p_idx
    heading = find_text(paragraph, "ParagraphCaption")
    text = extract_sentence_text_in(paragraph, "ParagraphSentence")
    node = Node(
        nid=nid_builder.unique(f"art{art_ord}.p{p_ord}"),
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
    for child in paragraph:
        tag = lname(child)
        if tag == "Item":
            i_idx += 1
            try:
                node.children.append(
                    parse_item(child, nid_builder, art_ord, p_ord, i_idx)
                )
            except Exception:
                LOGGER.exception("Failed while parsing Item in Paragraph")
                raise
        elif tag.startswith("Subitem"):
            try:
                node.children.append(
                    parse_subitem(child, nid_builder, art_ord, p_ord, None)
                )
            except Exception:
                LOGGER.exception("Failed while parsing Subitem in Paragraph")
                raise
    return node


def parse_item(
    item: etree._Element,
    nid_builder: NidBuilder,
    art_ord: int,
    p_ord: Optional[int],
    i_idx: Optional[int] = None,
) -> Node:
    num = find_text(item, "ItemTitle")
    i_ord = ord_from_attr_or_index(item, i_idx or 1) or (i_idx or 1)
    text = extract_sentence_text_in(item, "ItemSentence")
    nid_prefix = f"art{art_ord}."
    if p_ord is not None:
        nid_prefix += f"p{p_ord}."
    nid = f"{nid_prefix}i{i_ord}"
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
        if tag.startswith("Subitem"):
            s_idx += 1
            try:
                node.children.append(
                    parse_subitem(child, nid_builder, art_ord, p_ord, i_ord, s_idx)
                )
            except Exception:
                LOGGER.exception("Failed while parsing Subitem in Item")
                raise
    return node


def parse_subitem(
    elem: etree._Element,
    nid_builder: NidBuilder,
    art_ord: int,
    p_ord: Optional[int],
    i_ord: Optional[int],
    s_idx: Optional[int] = None,
) -> Node:
    tag = lname(elem)
    title = find_text(elem, f"{tag}Title")
    sentence_tag = f"{tag}Sentence"
    text = extract_sentence_text_in(elem, sentence_tag)

    kind = "subitem" if tag == "Subitem1" else "point"
    kind_raw = title or ("イロハ" if tag == "Subitem1" else tag)

    slug = slug_iroha(title) if tag == "Subitem1" else None
    ord_val = extract_digits(title) or (s_idx or 1)

    nid_prefix = f"art{art_ord}."
    if p_ord is not None:
        nid_prefix += f"p{p_ord}."
    if i_ord is not None:
        nid_prefix += f"i{i_ord}."
    if tag == "Subitem1" and slug:
        nid = f"{nid_prefix}{slug}"
    elif tag == "Subitem1":
        nid = f"{nid_prefix}s{ord_val}"
    else:
        nid = f"{nid_prefix}pt{ord_val}"

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
    return node


def parse_appendix(
    elem: etree._Element, nid_builder: NidBuilder, idx: int
) -> Node:
    title = None
    for key in ("AppdxTableTitle", "AppdxStyleTitle", "AppdxTitle"):
        title = find_text(elem, key)
        if title:
            break
    text = extract_sentence_text(elem)
    nid = nid_builder.unique(f"appendix{idx}")
    return Node(
        nid=nid,
        kind="appendix",
        kind_raw=lname(elem),
        num=title,
        ord=idx,
        heading=None,
        text=text or None,
        role="structural",
        normativity=None,
    )


def parse_suppl_provision(
    suppl: etree._Element, nid_builder: NidBuilder, idx: int
) -> Node:
    node = Node(
        nid=nid_builder.unique(f"annex{idx}"),
        kind="annex",
        kind_raw="附則",
        num=find_text(suppl, "SupplProvisionLabel"),
        ord=idx,
        heading=None,
        text=None,
        role="structural",
        normativity=None,
    )
    art_idx = 0
    for child in suppl:
        tag = lname(child)
        if tag == "Article":
            art_idx += 1
            try:
                node.children.append(
                    parse_article(
                        child, nid_builder, ord_from_attr_or_index(child, art_idx)
                    )
                )
            except Exception:
                LOGGER.exception("Failed while parsing Article in SupplProvision")
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


def extract_law_id_from_filename(name: str) -> Optional[str]:
    m = re.match(r"([0-9A-Za-z]+)_", name)
    if not m:
        return None
    return m.group(1)
