from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from lxml import etree


WHITESPACE_RE = re.compile(r"\s+")


def lname(elem: etree._Element) -> str:
    tag = elem.tag
    if isinstance(tag, str) and "}" in tag:
        return tag.split("}", 1)[1]
    return str(tag)


def parse_xml_document(path: Path) -> etree._ElementTree:
    return etree.parse(str(path), parser=etree.XMLParser(huge_tree=True))


def normalize_ws(text: Optional[str]) -> str:
    if not text:
        return ""
    return WHITESPACE_RE.sub(" ", text).strip()


def flatten_text(elem: etree._Element) -> str:
    parts = [part for part in elem.itertext()]
    return normalize_ws("".join(parts))
