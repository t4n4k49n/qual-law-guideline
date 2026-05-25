from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import typer
from qai_xml2ir.models_ir import Node

from .niid_annex_tables import PARSER_ID, READINESS_BY_NUM
from .profile_loader import load_parser_profile
from .text_parser import parse_text_to_ir


PARSER_PROFILE = Path("src/qai_text2ir/profiles/jp_niid_pathogen_safety_management_annex_v1.yaml")
SOURCE = Path("data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt")


@dataclass
class NiidAnnexReadinessItem:
    num: str
    heading: str
    decision: str
    promotion_mode: str
    reason: str
    has_table: bool
    rows: Optional[int]
    cell_reconstructed_rows: Optional[int]
    cell_deferred_rows: Optional[int]


def _walk(node: Node) -> Iterable[Node]:
    yield node
    for child in node.children:
        yield from _walk(child)


def build_niid_annex_readiness_inventory(root: Node) -> List[NiidAnnexReadinessItem]:
    items: List[NiidAnnexReadinessItem] = []
    for annex in [node for node in root.children if node.kind == "annex"]:
        if annex.num not in READINESS_BY_NUM:
            continue
        table = next(
            (node for node in _walk(annex) if node.kind == "table" and node.data.get("parser") == PARSER_ID),
            None,
        )
        decision = READINESS_BY_NUM[str(annex.num)]
        rows = None
        if table and table.children:
            rows = len([row for row in table.children[0].children if row.kind == "table_row"])
        items.append(
            NiidAnnexReadinessItem(
                num=str(annex.num),
                heading=annex.heading or "",
                decision=str(decision["decision"]),
                promotion_mode=str(decision["promotion_mode"]),
                reason=str(decision["reason"]),
                has_table=table is not None,
                rows=rows,
                cell_reconstructed_rows=table.data.get("cell_reconstructed_rows") if table else None,
                cell_deferred_rows=table.data.get("cell_deferred_rows") if table else None,
            )
        )
    return items


def readiness_to_dicts(items: List[NiidAnnexReadinessItem]) -> List[Dict[str, Any]]:
    return [asdict(item) for item in items]


def render_readiness_markdown(items: List[NiidAnnexReadinessItem]) -> str:
    lines = [
        "# NIID annex readiness inventory",
        "",
        "| annex | decision | promotion mode | table | rows | cells | reason |",
        "| --- | --- | --- | --- | ---: | --- | --- |",
    ]
    for item in items:
        cell_summary = ""
        if item.cell_reconstructed_rows is not None:
            cell_summary = f"{item.cell_reconstructed_rows}/{item.rows}"
        lines.append(
            "| "
            + " | ".join(
                [
                    item.num,
                    item.decision,
                    item.promotion_mode,
                    "yes" if item.has_table else "no",
                    "" if item.rows is None else str(item.rows),
                    cell_summary,
                    item.reason,
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


app = typer.Typer(add_completion=False)


@app.command()
def main(
    input_path: Path = typer.Option(SOURCE, "--input", exists=True, file_okay=True, dir_okay=False),
    profile_path: Path = typer.Option(PARSER_PROFILE, "--profile", exists=True, file_okay=True, dir_okay=False),
    out_json: Path = typer.Option(..., "--out-json"),
    out_md: Path = typer.Option(..., "--out-md"),
) -> None:
    profile = load_parser_profile(path=profile_path)
    doc = parse_text_to_ir(input_path=input_path, doc_id="jp_niid_pathogen_safety_management_readiness", parser_profile=profile)
    items = build_niid_annex_readiness_inventory(doc.content)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(
        json.dumps(readiness_to_dicts(items), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    out_md.write_text(render_readiness_markdown(items), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    app()
