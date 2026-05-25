from __future__ import annotations

from pathlib import Path

from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir, qualitycheck_document
from qai_xml2ir.verify import verify_document


SOURCE = Path("data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt")
PROFILE = Path("src/qai_text2ir/profiles/jp_niid_pathogen_safety_management_annex_v1.yaml")


def _walk(node):
    yield node
    for child in node.children:
        yield from _walk(child)


def test_niid_annex_profile_keeps_all_betsuhyo_and_fuhyo_markers() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_niid_pathogen_safety_management_annex_trial",
        parser_profile=profile,
    )
    verify_document(ir_doc.to_dict())

    annexes = [node for node in ir_doc.content.children if node.kind == "annex"]
    annex_nums = [node.num for node in annexes]

    assert annex_nums == [
        "別表1",
        "付表1-1",
        "付表1-2",
        "付表1-3",
        "付表2",
        "付表3",
        "付表4",
        "別表2",
        "別表3",
        "別表4",
        "別表5",
        "別表6",
        "別表7",
        "別表8",
        "別表9",
        "別表10",
    ]
    assert not qualitycheck_document(ir_doc.content)


def test_niid_annex_profile_preserves_annex_text_without_body_chapters() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_niid_pathogen_safety_management_annex_trial",
        parser_profile=profile,
    )
    nodes = list(_walk(ir_doc.content))
    annex_by_num = {node.num: node for node in ir_doc.content.children if node.kind == "annex"}
    all_text = "\n".join(str(part) for node in nodes for part in (node.heading, node.text) if part)

    assert [node.kind for node in ir_doc.content.children] == ["annex"] * 16
    assert "第１章" not in all_text
    assert annex_by_num["別表1"].heading.startswith("病原体等の取扱いにおいては")
    assert "における該当部分" in all_text
    assert "特定病原体等の取扱いに必要な教育訓練" in all_text
