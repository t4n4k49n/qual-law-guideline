from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import typer
from lxml import html
from qai_xml2ir.models_ir import Node


PARSER_ID = "mhlw_csv_annex2_table_adapter"
ANNEX2_HEADING = "カテゴリ分類表と対応例"

MAIN_TABLE_COLUMNS = [
    "category_no",
    "category_name",
    "content",
    "content_detail",
    "development_plan",
    "system_assessment",
    "system_registry",
    "urs",
    "fs",
    "ds",
    "supplier_audit",
    "acceptance_test",
    "validation_plan_report",
    "dq",
    "iq",
    "oq",
    "pq",
    "sop",
    "document_control",
    "remarks",
]
EXCLUDED_TABLE_COLUMNS = ["excluded_item", "description"]


@dataclass
class CsvAnnex2Table:
    table_no: str
    heading: str
    table_id: Optional[str]
    columns: List[str]
    rows: List[List[str]]
    source_format: str = "mhlw_page2_html_table"


def _normalize_text(value: str) -> str:
    text = re.sub(r"\s+", " ", value).strip()
    return text.replace("\u3000", " ").strip()


def _span_int(value: Optional[str]) -> int:
    if not value:
        return 1
    try:
        return max(int(value), 1)
    except ValueError:
        return 1


def _expanded_rows(table: Any) -> List[List[str]]:
    rows: List[List[str]] = []
    rowspans: Dict[int, Tuple[str, int]] = {}
    for tr in table.xpath(".//tr"):
        cells = tr.xpath("./th|./td")
        if not cells:
            continue
        row: List[str] = []
        col_idx = 0
        for cell in cells:
            while col_idx in rowspans:
                text, remaining = rowspans[col_idx]
                row.append(text)
                if remaining > 1:
                    rowspans[col_idx] = (text, remaining - 1)
                else:
                    del rowspans[col_idx]
                col_idx += 1
            text = _normalize_text("".join(cell.itertext()))
            colspan = _span_int(cell.get("colspan"))
            rowspan = _span_int(cell.get("rowspan"))
            for _ in range(colspan):
                row.append(text)
                if rowspan > 1:
                    rowspans[col_idx] = (text, rowspan - 1)
                col_idx += 1
        while col_idx in rowspans:
            text, remaining = rowspans[col_idx]
            row.append(text)
            if remaining > 1:
                rowspans[col_idx] = (text, remaining - 1)
            else:
                del rowspans[col_idx]
            col_idx += 1
        if any(cell.strip() for cell in row):
            rows.append(row)
    return rows


def _pad_or_trim(row: List[str], size: int) -> List[str]:
    if len(row) == size:
        return row
    if len(row) < size:
        return row + [""] * (size - len(row))
    return row[:size]


def extract_mhlw_csv_annex2_tables(page2_html_path: Path) -> List[CsvAnnex2Table]:
    tree = html.fromstring(page2_html_path.read_text(encoding="utf-8"))
    html_tables = tree.xpath('//*[@id="contents"]//table')
    if len(html_tables) < 2:
        return []

    main_rows = [_pad_or_trim(row, len(MAIN_TABLE_COLUMNS)) for row in _expanded_rows(html_tables[0])]
    if main_rows and main_rows[0] == [""] * len(MAIN_TABLE_COLUMNS):
        main_rows = main_rows[1:]
    excluded_rows = [_pad_or_trim(row, len(EXCLUDED_TABLE_COLUMNS)) for row in _expanded_rows(html_tables[1])]
    if excluded_rows and excluded_rows[0] == [""] * len(EXCLUDED_TABLE_COLUMNS):
        excluded_rows = excluded_rows[1:]

    return [
        CsvAnnex2Table(
            table_no="1",
            heading="カテゴリ分類表",
            table_id=html_tables[0].get("id"),
            columns=list(MAIN_TABLE_COLUMNS),
            rows=main_rows,
        ),
        CsvAnnex2Table(
            table_no="2",
            heading="本ガイドラインの対象外",
            table_id=html_tables[1].get("id"),
            columns=list(EXCLUDED_TABLE_COLUMNS),
            rows=excluded_rows,
        ),
    ]


def annex2_tables_to_dicts(tables: List[CsvAnnex2Table]) -> List[Dict[str, Any]]:
    return [asdict(table) for table in tables]


def render_annex2_table_inventory_markdown(tables: List[CsvAnnex2Table]) -> str:
    lines = [
        "# CSVガイドライン 別紙2 table inventory",
        "",
        "| 表 | 見出し | HTML table id | 列数 | 行数 | 形式 |",
        "| --- | --- | --- | ---: | ---: | --- |",
    ]
    for table in tables:
        lines.append(
            "| "
            + " | ".join(
                [
                    table.table_no,
                    table.heading,
                    table.table_id or "",
                    str(len(table.columns)),
                    str(len(table.rows)),
                    table.source_format,
                ]
            )
            + " |"
        )
    lines.extend(["", "## Columns", ""])
    for table in tables:
        lines.extend([f"### 表{table.table_no}", "", ", ".join(f"`{column}`" for column in table.columns), ""])
    return "\n".join(lines).rstrip() + "\n"


def _line_span(source_label: str, locator: str) -> Dict[str, str]:
    return {"source_label": source_label, "locator": locator}


def _make_node(
    *,
    nid: str,
    kind: str,
    kind_raw: Optional[str],
    num: Optional[str],
    heading: Optional[str],
    text: Optional[str],
    source_span: Dict[str, Any],
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
        source_spans=[source_span],
        data=data or {},
    )


def _table_node(annex: Node, table: CsvAnnex2Table, *, source_label: str) -> Node:
    table_nid = f"{annex.nid}.tbl{table.table_no}"
    span = _line_span(source_label, f"html_table:{table.table_id or table.table_no}")
    node = _make_node(
        nid=table_nid,
        kind="table",
        kind_raw="table",
        num=table.table_no,
        heading=table.heading,
        text=None,
        source_span=span,
        role="structural",
        data={
            "parser": PARSER_ID,
            "annex_num": annex.num,
            "source_format": table.source_format,
            "html_table_id": table.table_id,
            "column_reconstruction": "html_table_cells_with_column_schema",
            "column_reconstruction_status": "partial",
            "reconstructed_columns": table.columns,
            "row_count": len(table.rows),
        },
    )
    header = _make_node(
        nid=f"{table_nid}.tblh",
        kind="table_header",
        kind_raw="table_header",
        num=None,
        heading=None,
        text=" | ".join(table.columns),
        source_span=span,
        role="structural",
        data={"columns": table.columns},
    )
    node.children.append(header)
    for row_no, row in enumerate(table.rows, start=1):
        row_span = _line_span(source_label, f"html_table:{table.table_id or table.table_no}:row:{row_no}")
        header.children.append(
            _make_node(
                nid=f"{header.nid}.tblr{row_no}",
                kind="table_row",
                kind_raw="table_row",
                num=str(row_no),
                heading=None,
                text=" | ".join(row),
                source_span=row_span,
                data={
                    "cells": row,
                    "columns": table.columns,
                    "column_reconstruction": "html_table_cells",
                },
            )
        )
    return node


def normalize_mhlw_csv_annex2_tables(
    annex: Node,
    *,
    page2_html_path: Path,
    source_label: str,
) -> Dict[str, Any]:
    tables = extract_mhlw_csv_annex2_tables(page2_html_path)
    if not tables:
        return {"applied": False}
    annex.data["annex2_table_adapter"] = PARSER_ID
    annex.data["annex2_table_source_path"] = page2_html_path.as_posix()
    annex.data["source_format"] = "html_page1_placeholder_and_page2_tables"
    annex.data["extractable_text"] = True
    annex.data["table_rows_found"] = sum(len(table.rows) for table in tables)
    annex.data["column_reconstruction"] = "html_table_cells_with_column_schema"
    annex.data["column_reconstruction_status"] = "partial"
    annex.children = [child for child in annex.children if child.data.get("parser") != PARSER_ID]
    for table in tables:
        annex.children.append(_table_node(annex, table, source_label=source_label))
    return {
        "applied": True,
        "tables": [
            {"table_no": table.table_no, "heading": table.heading, "rows": len(table.rows), "columns": table.columns}
            for table in tables
        ],
    }


app = typer.Typer(add_completion=False)


@app.command("inventory")
def inventory_command(
    input_path: Path = typer.Option(..., "--input", exists=True, file_okay=True, dir_okay=False),
    out_json: Path = typer.Option(..., "--out-json"),
    out_md: Path = typer.Option(..., "--out-md"),
) -> None:
    tables = extract_mhlw_csv_annex2_tables(input_path)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(
        json.dumps(annex2_tables_to_dicts(tables), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    out_md.write_text(render_annex2_table_inventory_markdown(tables), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    app()
