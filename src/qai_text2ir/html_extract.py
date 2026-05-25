from __future__ import annotations

import re
from pathlib import Path
from typing import List

from lxml import html


def _normalize_text(value: str) -> str:
    text = re.sub(r"\s+", " ", value).strip()
    text = text.replace("\u3000", " ")
    return text.strip()


def extract_mhlw_t_doc_lines(input_path: Path) -> List[str]:
    tree = html.fromstring(input_path.read_text(encoding="utf-8"))
    content = tree.xpath('//*[@id="contents"]')
    root = content[0] if content else tree
    lines: List[str] = []
    for element in root.xpath('.//*[contains(concat(" ", normalize-space(@class), " "), " eline ")]//p'):
        text = _normalize_text("".join(element.itertext()))
        if not text:
            continue
        if text == "目次":
            continue
        classes = set((element.get("class") or "").split())
        if "toc_item-others" in classes:
            continue
        lines.append(text)
    return lines


def write_lines(path: Path, lines: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
