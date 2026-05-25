from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import typer

from .mhlw_csv_annexes import DEFAULT_WEB_BASE_URL, extract_mhlw_csv_annexes_from_html


DEFAULT_PAGE1_URL = "https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573&dataType=1&pageNo=1"
DEFAULT_PAGE2_URL = "https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573&dataType=1&pageNo=2"


@dataclass
class CsvAnnexSourceRecoveryItem:
    num: str
    heading: Optional[str]
    current_source_format: str
    current_extractable_text: bool
    current_source_note: str
    source_candidate: str
    candidate_url: str
    source_status: str
    table_body_available: bool
    ocr_required: bool
    recovery_action: str
    reason: str


def _page2_has_annex2_table(page2_html_text: Optional[str]) -> bool:
    if not page2_html_text:
        return False
    if "<table" not in page2_html_text.lower():
        return False
    if "カテゴリ分類表と対応例" in page2_html_text:
        return True
    return all(token in page2_html_text for token in ("カテゴリ", "内容", "開発計画書"))


def build_mhlw_csv_annex_source_recovery(
    input_html: Path,
    *,
    page1_url: str = DEFAULT_PAGE1_URL,
    page2_url: str = DEFAULT_PAGE2_URL,
    web_base_url: str = DEFAULT_WEB_BASE_URL,
    image_http_status: Optional[int] = None,
    page2_html_text: Optional[str] = None,
) -> List[CsvAnnexSourceRecoveryItem]:
    annexes = extract_mhlw_csv_annexes_from_html(input_html, source_url=page1_url, web_base_url=web_base_url)
    by_num = {annex.num: annex for annex in annexes}
    results: List[CsvAnnexSourceRecoveryItem] = []

    annex1 = by_num.get("別紙1")
    if annex1 and annex1.resolved_url:
        image_status = "reachable_http_200" if image_http_status == 200 else "candidate_identified"
        results.append(
            CsvAnnexSourceRecoveryItem(
                num="別紙1",
                heading=annex1.heading,
                current_source_format=annex1.source_format,
                current_extractable_text=annex1.extractable_text,
                current_source_note=annex1.deferred_reason or "",
                source_candidate="mhlw_image_endpoint",
                candidate_url=annex1.resolved_url,
                source_status=image_status,
                table_body_available=False,
                ocr_required=True,
                recovery_action="download_image_then_ocr_or_manual_transcription",
                reason="local_page1_html_points_to_image_only; textual content is not available in HTML",
            )
        )

    annex2 = by_num.get("別紙2")
    if annex2:
        page2_has_table = _page2_has_annex2_table(page2_html_text)
        results.append(
            CsvAnnexSourceRecoveryItem(
                num="別紙2",
                heading=annex2.heading,
                current_source_format=annex2.source_format,
                current_extractable_text=annex2.extractable_text,
                current_source_note=annex2.deferred_reason or "",
                source_candidate="mhlw_official_page2_html",
                candidate_url=page2_url,
                source_status="official_page2_contains_table_body" if page2_has_table else "candidate_identified",
                table_body_available=page2_has_table,
                ocr_required=False,
                recovery_action="fetch_official_page2_and_parse_html_table",
                reason="local_page1_html_has_annex2_title_only; official page2 is the candidate for the table body",
            )
        )

    return results


def source_recovery_items_to_dicts(items: List[CsvAnnexSourceRecoveryItem]) -> List[Dict[str, Any]]:
    return [asdict(item) for item in items]


def render_source_recovery_markdown(items: List[CsvAnnexSourceRecoveryItem]) -> str:
    lines = [
        "# CSVガイドライン 別紙ソース回収inventory",
        "",
        "| 別紙 | 現状 | 回収候補 | 候補URL | 状態 | OCR | 次アクション |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            "| "
            + " | ".join(
                [
                    item.num,
                    item.current_source_format,
                    item.source_candidate,
                    item.candidate_url,
                    item.source_status,
                    "要" if item.ocr_required else "不要",
                    item.recovery_action,
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## 判定メモ",
            "",
        ]
    )
    for item in items:
        lines.extend(
            [
                f"### {item.num}",
                "",
                f"- 見出し: {item.heading or ''}",
                f"- 現状メモ: {item.current_source_note}",
                f"- 表本体利用可否: {'可' if item.table_body_available else '不可'}",
                f"- 根拠: `{item.reason}`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


app = typer.Typer(add_completion=False)


@app.command("inventory")
def inventory_command(
    input_path: Path = typer.Option(..., "--input", exists=True, file_okay=True, dir_okay=False),
    out_json: Path = typer.Option(..., "--out-json"),
    out_md: Path = typer.Option(..., "--out-md"),
    page2_html: Optional[Path] = typer.Option(None, "--page2-html", exists=True, file_okay=True, dir_okay=False),
    image_http_status: Optional[int] = typer.Option(None, "--image-http-status"),
) -> None:
    page2_html_text = page2_html.read_text(encoding="utf-8") if page2_html else None
    items = build_mhlw_csv_annex_source_recovery(
        input_path,
        image_http_status=image_http_status,
        page2_html_text=page2_html_text,
    )
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(
        json.dumps(source_recovery_items_to_dicts(items), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    out_md.write_text(render_source_recovery_markdown(items), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    app()
