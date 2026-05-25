from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urljoin

import typer
from lxml import html
from qai_xml2ir.models_ir import Node

from .html_extract import extract_mhlw_t_doc_lines


PARSER_ID = "mhlw_csv_annex_adapter"
DEFAULT_SOURCE_URL = "https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573"
DEFAULT_WEB_BASE_URL = "https://www.mhlw.go.jp/web/"


@dataclass
class CsvAnnex:
    num: str
    heading: Optional[str]
    source_format: str
    extractable_text: bool
    line_no: Optional[int]
    label: Optional[str] = None
    href: Optional[str] = None
    resolved_url: Optional[str] = None
    table_rows_found: Optional[int] = None
    deferred_reason: Optional[str] = None


def _line_span(source_label: str, line_no: int) -> Dict[str, str]:
    return {"source_label": source_label, "locator": f"line:{line_no}"}


def _find_line_no(lines: List[str], value: str) -> Optional[int]:
    for idx, line in enumerate(lines, start=1):
        if line.strip() == value:
            return idx
    return None


def _infer_quoted_heading(lines: Iterable[str], annex_num: str) -> Optional[str]:
    pattern = re.compile(re.escape(annex_num) + r"[「\"](?P<title>[^」\"]+)[」\"]")
    for line in lines:
        match = pattern.search(line)
        if match:
            return match.group("title").strip()
    return None


def _make_annex_node(annex: CsvAnnex, *, source_label: str) -> Node:
    line_no = annex.line_no or 1
    node = Node(
        nid=f"annex{annex.num.replace('別紙', '')}",
        kind="annex",
        kind_raw="別紙",
        num=annex.num,
        ord=None,
        heading=annex.heading,
        text=annex.label,
        role="structural",
        normativity=None,
        source_spans=[_line_span(source_label, line_no)],
        data={
            "parser": PARSER_ID,
            "source_format": annex.source_format,
            "extractable_text": annex.extractable_text,
            "column_reconstruction": False,
            "deferred_reason": annex.deferred_reason,
        },
    )
    if annex.href:
        node.data["href"] = annex.href
    if annex.resolved_url:
        node.data["resolved_url"] = annex.resolved_url
    if annex.table_rows_found is not None:
        node.data["table_rows_found"] = annex.table_rows_found
    return node


def _strip_annex_tail(text: Optional[str]) -> Optional[str]:
    if not text:
        return text
    cleaned = re.sub(
        r"\s+別紙1\s+画像1\s*\([^)]*\)\s+別紙2\s+カテゴリ分類表と対応例\s*$",
        "",
        text,
    ).rstrip()
    return cleaned or None


def extract_mhlw_csv_annexes_from_lines(lines: List[str]) -> List[CsvAnnex]:
    annex1_line_no = _find_line_no(lines, "別紙1")
    annex2_line_no = _find_line_no(lines, "別紙2")
    annex1_label = lines[annex1_line_no] if annex1_line_no and annex1_line_no < len(lines) else None
    annex2_heading = lines[annex2_line_no] if annex2_line_no and annex2_line_no < len(lines) else None
    annexes: List[CsvAnnex] = []
    if annex1_line_no is not None:
        annexes.append(
            CsvAnnex(
                num="別紙1",
                heading=_infer_quoted_heading(lines, "別紙1"),
                source_format="html_image_reference",
                extractable_text=False,
                line_no=annex1_line_no,
                label=annex1_label,
                deferred_reason="HTML本文には画像リンク表示のみが残るため、内容テキスト化には画像取得/OCRが必要",
            )
        )
    if annex2_line_no is not None:
        annexes.append(
            CsvAnnex(
                num="別紙2",
                heading=annex2_heading or _infer_quoted_heading(lines, "別紙2"),
                source_format="html_table_title_only",
                extractable_text=False,
                line_no=annex2_line_no,
                table_rows_found=0,
                deferred_reason="HTML本文抽出範囲には表題行のみが残り、表本体行が確認できない",
            )
        )
    return annexes


def extract_mhlw_csv_annexes_from_html(
    input_path: Path,
    *,
    source_url: str = DEFAULT_SOURCE_URL,
    web_base_url: str = DEFAULT_WEB_BASE_URL,
) -> List[CsvAnnex]:
    tree = html.fromstring(input_path.read_text(encoding="utf-8"))
    text_lines = extract_mhlw_t_doc_lines(input_path)
    annexes = {annex.num: annex for annex in extract_mhlw_csv_annexes_from_lines(text_lines)}

    image_link = tree.xpath(
        '//p[normalize-space()="別紙1"]'
        '/ancestor::div[contains(@class, "eline")][1]'
        "/following-sibling::div[1]//a[1]"
    )
    if image_link and "別紙1" in annexes:
        href = image_link[0].get("href")
        annexes["別紙1"].href = href
        annexes["別紙1"].resolved_url = urljoin(web_base_url, href) if href else None
        label = re.sub(r"\s+", " ", "".join(image_link[0].itertext())).strip()
        annexes["別紙1"].label = label or annexes["別紙1"].label

    if "別紙2" in annexes:
        table_rows = tree.xpath(
            '//p[normalize-space()="別紙2"]'
            '/ancestor::div[contains(@class, "eline")][1]'
            "/following-sibling::div//tr"
        )
        annexes["別紙2"].table_rows_found = len(table_rows)

    for annex in annexes.values():
        if annex.resolved_url is None and annex.href:
            annex.resolved_url = urljoin(source_url, annex.href)
    return list(annexes.values())


def normalize_mhlw_csv_annexes(root: Node, raw_lines: List[str], *, source_label: str) -> Dict[str, Any]:
    annexes = extract_mhlw_csv_annexes_from_lines(raw_lines)
    if not annexes:
        return {"applied": False}
    for child in root.children:
        if child.kind == "chapter" and child.num == "10":
            child.text = _strip_annex_tail(child.text)
            break
    existing = {(child.kind, child.num) for child in root.children}
    for annex in annexes:
        if ("annex", annex.num) not in existing:
            root.children.append(_make_annex_node(annex, source_label=source_label))
    return {
        "applied": True,
        "annexes": [
            {
                "num": annex.num,
                "source_format": annex.source_format,
                "extractable_text": annex.extractable_text,
            }
            for annex in annexes
        ],
    }


def annexes_to_dicts(annexes: List[CsvAnnex]) -> List[Dict[str, Any]]:
    return [asdict(annex) for annex in annexes]


def render_annex_inventory_markdown(annexes: List[CsvAnnex]) -> str:
    lines = [
        "# CSVガイドライン 別紙inventory",
        "",
        "| 別紙 | 見出し | 形式 | 抽出可否 | 補足 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for annex in annexes:
        detail = annex.deferred_reason or ""
        if annex.href:
            detail = f"{detail} href={annex.href}".strip()
        if annex.table_rows_found is not None:
            detail = f"{detail} table_rows_found={annex.table_rows_found}".strip()
        lines.append(
            "| "
            + " | ".join(
                [
                    annex.num,
                    annex.heading or "",
                    annex.source_format,
                    "可" if annex.extractable_text else "不可",
                    detail,
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


app = typer.Typer(add_completion=False)


@app.command("inventory")
def inventory_command(
    input_path: Path = typer.Option(..., "--input", exists=True, file_okay=True, dir_okay=False),
    out_json: Path = typer.Option(..., "--out-json"),
    out_md: Path = typer.Option(..., "--out-md"),
    source_url: str = typer.Option(DEFAULT_SOURCE_URL, "--source-url"),
) -> None:
    annexes = extract_mhlw_csv_annexes_from_html(input_path, source_url=source_url)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(
        json.dumps(annexes_to_dicts(annexes), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    out_md.write_text(render_annex_inventory_markdown(annexes), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    app()
