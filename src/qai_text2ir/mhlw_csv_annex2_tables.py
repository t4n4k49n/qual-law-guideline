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
SEMANTIC_VALUE_COLUMNS = MAIN_TABLE_COLUMNS[4:19]
SEMANTIC_VALUE_LEGEND = {
    "◎": {
        "status": "required",
        "meaning": "必須",
    },
    "○": {
        "status": "conditional_required",
        "meaning": "システムアセスメントの結果による(基本的には必要)",
    },
    "△": {
        "status": "conditional_omittable",
        "meaning": "システムアセスメントの結果による(基本的には省略)",
    },
    "―": {
        "status": "omittable",
        "meaning": "省略可能",
    },
}
FOOTNOTE_RE = re.compile(r"^([◎○△―])(\d*)$")


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
    return [_table_to_dict(table) for table in tables]


def _semantic_value(raw_value: str) -> Dict[str, Any]:
    raw = raw_value.strip()
    if not raw:
        return {
            "raw": raw_value,
            "symbol": "",
            "status": "blank",
            "meaning": "",
            "footnote_refs": [],
            "semantic_warning": "blank_semantic_value",
        }
    match = FOOTNOTE_RE.match(raw)
    if not match:
        return {
            "raw": raw_value,
            "symbol": "",
            "status": "unparsed",
            "meaning": "",
            "footnote_refs": [],
            "semantic_warning": "unparsed_semantic_value",
        }
    symbol, refs = match.groups()
    legend = SEMANTIC_VALUE_LEGEND[symbol]
    return {
        "raw": raw_value,
        "symbol": symbol,
        "status": legend["status"],
        "meaning": legend["meaning"],
        "footnote_refs": list(refs),
    }


def _row_values(row: List[str]) -> Dict[str, Dict[str, Any]]:
    by_column = dict(zip(MAIN_TABLE_COLUMNS, row))
    return {column: _semantic_value(by_column.get(column, "")) for column in SEMANTIC_VALUE_COLUMNS}


def _record_from_rows(category_no: str, rows: List[Tuple[int, List[str]]]) -> Dict[str, Any]:
    first_row = rows[0][1]
    first = dict(zip(MAIN_TABLE_COLUMNS, first_row))
    record_id = f"csv_annex2.category{category_no}"
    variants = []
    footnote_refs = set()
    warnings = []
    for row_no, row in rows:
        values = _row_values(row)
        for value in values.values():
            footnote_refs.update(value.get("footnote_refs") or [])
            if value.get("semantic_warning"):
                warnings.append({"raw_row_num": row_no, "warning": value["semantic_warning"]})
        by_column = dict(zip(MAIN_TABLE_COLUMNS, row))
        variants.append(
            {
                "raw_row_num": row_no,
                "content_detail": by_column.get("content_detail", ""),
                "semantic_values": values,
                "remarks": by_column.get("remarks", ""),
            }
        )
    record: Dict[str, Any] = {
        "record_id": record_id,
        "raw_row_nums": [row_no for row_no, _ in rows],
        "category_no": category_no,
        "category_name": first.get("category_name", ""),
        "content": first.get("content", ""),
        "variants": variants,
        "footnote_refs": sorted(footnote_refs),
        "review_status": "reviewed_candidate",
        "promotion_status": "deferred",
    }
    if warnings:
        record["semantic_warnings"] = warnings
    if not record["category_name"]:
        record["semantic_warnings"] = record.get("semantic_warnings", []) + [
            {"raw_row_num": rows[0][0], "warning": "blank_category_name_preserved"}
        ]
    return record


def build_main_table_semantic_records(table: CsvAnnex2Table) -> List[Dict[str, Any]]:
    if table.table_no != "1":
        return []
    grouped: Dict[str, List[Tuple[int, List[str]]]] = {}
    order: List[str] = []
    for row_no, row in enumerate(table.rows, start=1):
        category_no = row[0].strip() if row else ""
        if not category_no.isdigit():
            continue
        if category_no not in grouped:
            grouped[category_no] = []
            order.append(category_no)
        grouped[category_no].append((row_no, row))
    return [_record_from_rows(category_no, grouped[category_no]) for category_no in order]


def build_excluded_table_semantic_records(table: CsvAnnex2Table) -> List[Dict[str, Any]]:
    if table.table_no != "2":
        return []
    records = []
    for row_no, row in enumerate(table.rows, start=1):
        by_column = dict(zip(EXCLUDED_TABLE_COLUMNS, row))
        records.append(
            {
                "record_id": f"csv_annex2.excluded.r{row_no}",
                "raw_row_nums": [row_no],
                "excluded_item": by_column.get("excluded_item", ""),
                "description": by_column.get("description", ""),
                "review_status": "reviewed_candidate",
                "promotion_status": "deferred",
            }
        )
    return records


def _semantic_records_for_table(table: CsvAnnex2Table) -> List[Dict[str, Any]]:
    if table.table_no == "1":
        return build_main_table_semantic_records(table)
    if table.table_no == "2":
        return build_excluded_table_semantic_records(table)
    return []


def _table_to_dict(table: CsvAnnex2Table) -> Dict[str, Any]:
    data = asdict(table)
    data["semantic_records"] = _semantic_records_for_table(table)
    return data


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
    lines.extend(["## Semantic records", ""])
    for table in tables:
        records = _semantic_records_for_table(table)
        lines.extend([f"### 表{table.table_no}", "", f"- semantic records: {len(records)}"])
        if table.table_no == "1":
            lines.append("- semantic value columns: " + ", ".join(f"`{column}`" for column in SEMANTIC_VALUE_COLUMNS))
        lines.append("")
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
    semantic_records = _semantic_records_for_table(table)
    record_ids_by_raw_row: Dict[int, str] = {}
    for record in semantic_records:
        for raw_row_num in record["raw_row_nums"]:
            record_ids_by_raw_row[raw_row_num] = record["record_id"]
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
            "semantic_reconstruction": "csv_annex2_semantic_records_v1",
            "semantic_reconstruction_status": "reviewed_candidate",
            "semantic_value_legend": SEMANTIC_VALUE_LEGEND if table.table_no == "1" else {},
            "semantic_value_columns": SEMANTIC_VALUE_COLUMNS if table.table_no == "1" else [],
            "semantic_records": semantic_records,
            "semantic_record_count": len(semantic_records),
            "record_review": {
                "status": "reviewed_candidate",
                "candidate_granularity": "semantic_record",
                "table_row_promotion": "deferred",
                "table_row_promotion_reason": "HTML table rows are preserved; semantic records need normalized run review before replacing table_row candidates",
                "reviewed_records": len(semantic_records),
            },
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
        row_data = {
            "cells": row,
            "columns": table.columns,
            "column_reconstruction": "html_table_cells",
        }
        if row_no in record_ids_by_raw_row:
            row_data["semantic_record_id"] = record_ids_by_raw_row[row_no]
        else:
            row_data["semantic_reconstruction_warning"] = "non_data_row_not_semantic_record"
        header.children.append(
            _make_node(
                nid=f"{header.nid}.tblr{row_no}",
                kind="table_row",
                kind_raw="table_row",
                num=str(row_no),
                heading=None,
                text=" | ".join(row),
                source_span=row_span,
                data=row_data,
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
