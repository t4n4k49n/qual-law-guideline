from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import typer
from qai_xml2ir.models_ir import Node

from .profile_loader import load_parser_profile
from .text_parser import parse_text_to_ir


PARSER_PROFILE = Path("src/qai_text2ir/profiles/jp_niid_pathogen_safety_management_annex_v1.yaml")
SOURCE = Path("data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt")


CLASSIFICATION_BY_NUM: Dict[str, Dict[str, Any]] = {
    "別表1": {
        "structure_type": "narrative_reference",
        "column_restoration": "not_applicable",
        "next_action": "keep_as_annex_text",
        "reason": "別表・付表の適用関係を説明する短い本文であり、表列復元対象ではない",
    },
    "付表1-1": {
        "structure_type": "narrative_reference",
        "column_restoration": "not_applicable",
        "next_action": "keep_as_annex_text",
        "reason": "リスク群分類の説明本文であり、列境界を持つ表ではない",
    },
    "付表1-2": {
        "structure_type": "numbered_assessment_items",
        "column_restoration": "not_applicable",
        "next_action": "consider_numbered_item_structure_later",
        "reason": "リスク評価項目の列挙であり、表列復元より番号付き項目化の検討が先",
    },
    "付表1-3": {
        "structure_type": "numbered_assessment_items",
        "column_restoration": "not_applicable",
        "next_action": "consider_numbered_item_structure_later",
        "reason": "動物実験リスク評価項目の列挙であり、表列復元対象ではない",
    },
    "付表2": {
        "structure_type": "fixed_width_matrix",
        "column_restoration": "candidate",
        "next_action": "table_adapter_candidate",
        "reason": "BSL分類、使用目的、実験手技、安全機器の関係を複数列で示す固定幅表",
    },
    "付表3": {
        "structure_type": "fixed_width_matrix",
        "column_restoration": "candidate",
        "next_action": "table_adapter_candidate",
        "reason": "BSL1-4の安全設備基準を横持ち列で比較する固定幅表",
    },
    "付表4": {
        "structure_type": "fixed_width_matrix",
        "column_restoration": "candidate",
        "next_action": "table_adapter_candidate",
        "reason": "ABSL1-4の実験手技・安全機器・設備基準を横持ち列で比較する固定幅表",
    },
    "別表2": {
        "structure_type": "sectioned_text",
        "column_restoration": "not_applicable",
        "next_action": "consider_section_structure_later",
        "reason": "BSLごとの文章型基準であり、列復元ではなく節構造化の検討対象",
    },
    "別表3": {
        "structure_type": "sectioned_text",
        "column_restoration": "not_applicable",
        "next_action": "consider_section_structure_later",
        "reason": "ABSLごとの文章型基準であり、列復元ではなく節構造化の検討対象",
    },
    "別表4": {
        "structure_type": "large_fixed_width_matrix",
        "column_restoration": "candidate_complex",
        "next_action": "table_adapter_candidate_after_manual_review",
        "reason": "特定病原体等区分ごとの技術基準一覧で、横長かつ複数行セルが多い",
    },
    "別表5": {
        "structure_type": "large_fixed_width_matrix",
        "column_restoration": "candidate_complex",
        "next_action": "table_adapter_candidate_after_manual_review",
        "reason": "保管等の技術基準一覧で、横長かつ注記・滅菌基準の複数行セルが多い",
    },
    "別表6": {
        "structure_type": "numbered_requirements",
        "column_restoration": "not_applicable",
        "next_action": "consider_numbered_item_structure_later",
        "reason": "運営規則作成基準の番号付き要求事項であり、表列復元対象ではない",
    },
    "別表7": {
        "structure_type": "fixed_width_matrix",
        "column_restoration": "candidate",
        "next_action": "table_adapter_candidate",
        "reason": "記帳項目、記帳内容、1-3種病原体等の要否を並べた固定幅表",
    },
    "別表8": {
        "structure_type": "fixed_width_matrix_with_embedded_items",
        "column_restoration": "candidate_complex",
        "next_action": "table_adapter_candidate_after_manual_review",
        "reason": "教育訓練対象、記載項目、回数、備考の表だが、箇条書きがセル内に混在する",
    },
    "別表9": {
        "structure_type": "numbered_requirements",
        "column_restoration": "not_applicable",
        "next_action": "consider_numbered_item_structure_later",
        "reason": "災害時対応の番号付き要求事項であり、表列復元対象ではない",
    },
    "別表10": {
        "structure_type": "fixed_width_comparison_table",
        "column_restoration": "candidate",
        "next_action": "table_adapter_candidate",
        "reason": "省令項目、具体的内容、規程該当部分を対応付ける比較表",
    },
}


@dataclass
class NiidAnnexInventoryItem:
    num: str
    heading: str
    structure_type: str
    column_restoration: str
    next_action: str
    reason: str
    line_count: int
    note_count: int
    subitem_count: int
    wide_line_count: int


def _walk(node: Node) -> Iterable[Node]:
    yield node
    for child in node.children:
        yield from _walk(child)


def _line_count(node: Node) -> int:
    parts = [part for part in [node.heading, node.text] if part]
    return len([line for line in "\n".join(parts).splitlines() if line.strip()])


def _wide_line_count(node: Node) -> int:
    parts = [part for part in [node.heading, node.text] if part]
    return len([line for line in "\n".join(parts).splitlines() if "  " in line])


def build_niid_annex_inventory(root: Node) -> List[NiidAnnexInventoryItem]:
    items: List[NiidAnnexInventoryItem] = []
    for annex in [node for node in root.children if node.kind == "annex"]:
        if annex.num not in CLASSIFICATION_BY_NUM:
            continue
        classification = CLASSIFICATION_BY_NUM[annex.num]
        descendants = list(_walk(annex))
        items.append(
            NiidAnnexInventoryItem(
                num=str(annex.num),
                heading=annex.heading or "",
                structure_type=str(classification["structure_type"]),
                column_restoration=str(classification["column_restoration"]),
                next_action=str(classification["next_action"]),
                reason=str(classification["reason"]),
                line_count=_line_count(annex),
                note_count=sum(1 for node in descendants if node.kind == "note"),
                subitem_count=sum(1 for node in descendants if node.kind == "subitem"),
                wide_line_count=_wide_line_count(annex),
            )
        )
    return items


def inventory_to_dicts(items: List[NiidAnnexInventoryItem]) -> List[Dict[str, Any]]:
    return [asdict(item) for item in items]


def render_inventory_markdown(items: List[NiidAnnexInventoryItem]) -> str:
    lines = [
        "# NIID別表・付表 table inventory",
        "",
        "| 対象 | 見出し | 形式 | 列復元 | 次アクション | 根拠 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            "| "
            + " | ".join(
                [
                    item.num,
                    item.heading,
                    item.structure_type,
                    item.column_restoration,
                    item.next_action,
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
    doc = parse_text_to_ir(input_path=input_path, doc_id="jp_niid_pathogen_safety_management_annex_inventory", parser_profile=profile)
    items = build_niid_annex_inventory(doc.content)
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
