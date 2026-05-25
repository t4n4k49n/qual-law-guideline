from __future__ import annotations

from collections import Counter
from pathlib import Path

from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir, qualitycheck_document
from qai_xml2ir.verify import verify_document


SOURCE = Path("data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt")
PROFILE = Path("src/qai_text2ir/profiles/jp_niid_pathogen_safety_management_v1.yaml")


def _walk(node):
    yield node
    for child in node.children:
        yield from _walk(child)


def test_niid_profile_drops_front_matter_toc_and_annexes_for_body_phase() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_niid_pathogen_safety_management_trial",
        parser_profile=profile,
    )
    verify_document(ir_doc.to_dict())

    root_chapters = [node for node in ir_doc.content.children if node.kind == "chapter"]
    root_nums = [node.num for node in root_chapters]
    counts = Counter(root_nums)
    headings_and_text = [str(part) for node in _walk(ir_doc.content) for part in (node.heading, node.text) if part]

    assert root_nums == ["1", "2", "3", "4", "5", "6"]
    assert all(counts[num] == 1 for num in root_nums)
    assert not any(part.strip() == "別表１" for part in headings_and_text)
    assert not qualitycheck_document(ir_doc.content)


def test_niid_profile_parses_articles_paragraphs_and_numbered_items() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_niid_pathogen_safety_management_trial",
        parser_profile=profile,
    )
    nodes = list(_walk(ir_doc.content))
    chapter_1 = next(node for node in nodes if node.kind == "chapter" and node.num == "1")
    article_1 = next(node for node in chapter_1.children if node.kind == "paragraph" and node.num == "1")
    article_2 = next(node for node in chapter_1.children if node.kind == "paragraph" and node.num == "2")
    article_9_2 = next(node for node in nodes if node.kind == "paragraph" and node.num == "9_2")
    article_1_para_2 = next(node for node in article_1.children if node.kind == "item" and node.num == "2")
    article_2_item_1 = next(node for node in article_2.children if node.kind == "subitem" and node.num == "1")

    assert chapter_1.heading == "総     則"
    assert article_1.text.startswith("国立感染症研究所病原体等安全管理規程")
    assert article_9_2.text.startswith("ポリオウイルス取扱施設運営委員会")
    assert article_1_para_2.text.startswith("安全管理規程は、感染症法に基づく")
    assert article_2_item_1.text.startswith("「病原体等」とは")
