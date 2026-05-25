from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List

import typer

from .api_gmp_table1 import RECORD_REVIEW as API_GMP_RECORD_REVIEW
from .api_gmp_table1 import RECONSTRUCTED_COLUMNS as API_GMP_COLUMNS
from .api_gmp_table1 import RECONSTRUCTED_RECORDS as API_GMP_RECORDS
from .aseptic_processing_tables import (
    RECONSTRUCTED_COLUMNS_BY_TABLE as ASEPTIC_COLUMNS,
)
from .aseptic_processing_tables import (
    RECONSTRUCTED_RECORDS_BY_TABLE as ASEPTIC_RECORDS,
)
from .aseptic_processing_tables import (
    RECORD_REVIEW_BY_TABLE as ASEPTIC_RECORD_REVIEW,
)


@dataclass
class TableRecordReview:
    doc_no: str
    document: str
    table_nid: str
    table_heading: str
    columns: List[str]
    records: int
    review_status: str
    candidate_granularity: str
    table_row_promotion: str
    deferred_raw_rows: List[int]
    remaining_issue: str


def build_table_record_review_inventory() -> List[TableRecordReview]:
    items = [
        TableRecordReview(
            doc_no="6",
            document="原薬GMPガイドライン",
            table_nid="cha1.p1_3.tbl1",
            table_heading="表１：原薬生産に対する本ガイドラインの適用",
            columns=list(API_GMP_COLUMNS),
            records=len(API_GMP_RECORDS),
            review_status=str(API_GMP_RECORD_REVIEW["status"]),
            candidate_granularity=str(API_GMP_RECORD_REVIEW["candidate_granularity"]),
            table_row_promotion=str(API_GMP_RECORD_REVIEW["table_row_promotion"]),
            deferred_raw_rows=list(API_GMP_RECORD_REVIEW["deferred_raw_rows"]),
            remaining_issue=str(API_GMP_RECORD_REVIEW["visual_information"]),
        )
    ]
    aseptic_headings = {
        "1": "表１ 清浄区域の分類",
        "2": "表２ 微生物管理に係る環境モニタリングの頻度",
        "3": "表 3 環境微生物の許容基準(作業時) 注）1",
    }
    aseptic_nids = {
        "1": "cha7.p7_1.tbl1",
        "2": "cha11.p11_3.tbl2",
        "3": "cha11.p11_3.tbl3",
    }
    for table_no in ["1", "2", "3"]:
        review = ASEPTIC_RECORD_REVIEW[table_no]
        items.append(
            TableRecordReview(
                doc_no="7",
                document="無菌操作法指針",
                table_nid=aseptic_nids[table_no],
                table_heading=aseptic_headings[table_no],
                columns=list(ASEPTIC_COLUMNS[table_no]),
                records=len(ASEPTIC_RECORDS[table_no]),
                review_status=str(review["status"]),
                candidate_granularity=str(review["candidate_granularity"]),
                table_row_promotion=str(review["table_row_promotion"]),
                deferred_raw_rows=list(review["deferred_raw_rows"]),
                remaining_issue=str(review["table_row_promotion_reason"]),
            )
        )
    return items


def inventory_to_dicts(items: List[TableRecordReview]) -> List[Dict[str, Any]]:
    return [asdict(item) for item in items]


def render_inventory_markdown(items: List[TableRecordReview]) -> str:
    lines = [
        "# 6/7 table record review inventory",
        "",
        "| 文書 | table | records | 候補粒度 | table_row昇格 | 保留raw rows | 残課題 |",
        "| --- | --- | ---: | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            "| "
            + " | ".join(
                [
                    item.document,
                    f"`{item.table_nid}`",
                    str(item.records),
                    item.candidate_granularity,
                    item.table_row_promotion,
                    ", ".join(str(row) for row in item.deferred_raw_rows),
                    item.remaining_issue,
                ]
            )
            + " |"
        )
    lines.extend(["", "## Columns", ""])
    for item in items:
        lines.extend([f"### {item.table_nid}", "", ", ".join(f"`{column}`" for column in item.columns), ""])
    return "\n".join(lines).rstrip() + "\n"


app = typer.Typer(add_completion=False)


@app.command("inventory")
def inventory_command(
    out_json: Path = typer.Option(..., "--out-json"),
    out_md: Path = typer.Option(..., "--out-md"),
) -> None:
    items = build_table_record_review_inventory()
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(
        json.dumps(inventory_to_dicts(items), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    out_md.write_text(render_inventory_markdown(items), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    app()
