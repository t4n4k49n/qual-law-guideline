from __future__ import annotations

from collections import Counter
from pathlib import Path

from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir, qualitycheck_document
from qai_xml2ir.verify import verify_document


SOURCE = Path("data/human-readable/pmda/aseptic_processing_guideline/source_texts/000206144.txt")
PROFILE = Path("src/qai_text2ir/profiles/jp_pmda_aseptic_processing_guideline_v1.yaml")


def _walk(node):
    yield node
    for child in node.children:
        yield from _walk(child)


def test_aseptic_profile_drops_front_matter_and_toc_duplicates() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_pmda_aseptic_processing_guideline_trial",
        parser_profile=profile,
    )
    verify_document(ir_doc.to_dict())

    root_chapters = [node for node in ir_doc.content.children if node.kind == "chapter"]
    root_nums = [node.num for node in root_chapters]
    counts = Counter(root_nums)

    assert root_nums[:3] == ["1", "2", "3"]
    assert counts["1"] == 1
    assert counts["20"] == 1
    assert not qualitycheck_document(ir_doc.content)


def test_aseptic_profile_keeps_main_and_reference_sections_separate() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_pmda_aseptic_processing_guideline_trial",
        parser_profile=profile,
    )
    nodes = list(_walk(ir_doc.content))
    by_kind_num = {(node.kind, node.num): node for node in nodes}

    assert by_kind_num[("chapter", "3")].heading == "品質システム"
    assert by_kind_num[("paragraph", "3.1")].text.startswith("品質システム一般要求事項")
    assert by_kind_num[("chapter", "A1")].heading == "細胞培養／発酵により製造する原薬"
    assert by_kind_num[("paragraph", "A1.1")].text.startswith("一般要件")
