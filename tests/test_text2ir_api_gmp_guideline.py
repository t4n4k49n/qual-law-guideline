from __future__ import annotations

from collections import Counter
from pathlib import Path

from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir, qualitycheck_document
from qai_xml2ir.verify import verify_document


SOURCE = Path("data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt")
PROFILE = Path("src/qai_text2ir/profiles/jp_pmda_api_gmp_guideline_v1.yaml")


def _flatten(node):
    yield node
    for child in node.children:
        yield from _flatten(child)


def test_api_gmp_profile_drops_notice_and_toc_duplicates() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_pmda_api_gmp_guideline_20011102",
        parser_profile=profile,
    )
    ir = ir_doc.to_dict()
    verify_document(ir)

    root_children = ir_doc.content.children
    root_chapter_nums = [node.num for node in root_children if node.kind == "chapter"]
    counts = Counter(root_chapter_nums)

    assert root_chapter_nums[:3] == ["1", "2", "3"]
    assert counts["1"] == 1
    assert counts["2"] == 1
    assert counts["19"] == 1
    assert not qualitycheck_document(ir_doc.content)


def test_api_gmp_profile_keeps_deep_sections_under_chapters() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_pmda_api_gmp_guideline_20011102",
        parser_profile=profile,
    )
    nodes = list(_flatten(ir_doc.content))
    by_num = {(node.kind, node.num): node for node in nodes}

    assert by_num[("chapter", "3")].heading == "従業員"
    assert by_num[("paragraph", "3.1")].text == "従業員の適格性"
    assert by_num[("paragraph", "3.10")].text.startswith("中間体・原薬の生産を実施し監督するため")
    assert by_num[("paragraph", "3.2")].text == "従業員の衛生"
