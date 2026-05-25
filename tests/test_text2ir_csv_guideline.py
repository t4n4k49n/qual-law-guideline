from __future__ import annotations

from collections import Counter
from pathlib import Path

from qai_text2ir.html_extract import extract_mhlw_t_doc_lines
from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir, qualitycheck_document
from qai_xml2ir.verify import verify_document


SOURCE_HTML = Path("data/human-readable/mhlw/csv_guideline/00tb6573.html")
PROFILE = Path("src/qai_text2ir/profiles/jp_mhlw_csv_guideline_v1.yaml")


def _walk(node):
    yield node
    for child in node.children:
        yield from _walk(child)


def test_csv_html_extraction_keeps_body_and_drops_toc() -> None:
    lines = extract_mhlw_t_doc_lines(SOURCE_HTML)

    assert "1．総則" in lines
    assert "1．3 カテゴリ分類" in lines
    assert "3．コンピュータ化システムの開発、検証及び運用管理に関する文書の作成" in lines
    assert not any(line == "目次" for line in lines)


def test_csv_profile_drops_notice_front_matter_and_title_duplicates(tmp_path: Path) -> None:
    input_path = tmp_path / "00tb6573.extracted.txt"
    input_path.write_text("\n".join(extract_mhlw_t_doc_lines(SOURCE_HTML)) + "\n", encoding="utf-8", newline="\n")
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="jp_mhlw_csv_guideline_trial",
        parser_profile=profile,
    )
    verify_document(ir_doc.to_dict())

    root_chapters = [node for node in ir_doc.content.children if node.kind == "chapter"]
    root_nums = [node.num for node in root_chapters]
    counts = Counter(root_nums)

    assert root_nums[:3] == ["1", "2", "3"]
    assert root_nums[-1] == "10"
    assert counts["1"] == 1
    assert counts["10"] == 1
    assert not qualitycheck_document(ir_doc.content)


def test_csv_profile_preserves_expected_nested_items(tmp_path: Path) -> None:
    input_path = tmp_path / "00tb6573.extracted.txt"
    input_path.write_text("\n".join(extract_mhlw_t_doc_lines(SOURCE_HTML)) + "\n", encoding="utf-8", newline="\n")
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="jp_mhlw_csv_guideline_trial",
        parser_profile=profile,
    )
    nodes = list(_walk(ir_doc.content))
    by_kind_num = {(node.kind, node.num): node for node in nodes}

    assert by_kind_num[("chapter", "1")].heading == "総則"
    assert by_kind_num[("paragraph", "1.3")].text.startswith("カテゴリ分類")
    assert by_kind_num[("chapter", "3")].heading == "コンピュータ化システムの開発、検証及び運用管理に関する文書の作成"
    assert any(node.kind == "item" and node.num == "7" for node in nodes)
    assert any(node.kind == "subitem" and node.num == "1" for node in nodes)


def test_csv_annex_adapter_separates_visible_annex_placeholders(tmp_path: Path) -> None:
    input_path = tmp_path / "00tb6573.extracted.txt"
    input_path.write_text("\n".join(extract_mhlw_t_doc_lines(SOURCE_HTML)) + "\n", encoding="utf-8", newline="\n")
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="jp_mhlw_csv_guideline_trial",
        parser_profile=profile,
    )
    nodes = list(_walk(ir_doc.content))
    by_nid = {node.nid: node for node in nodes}
    annexes = [node for node in ir_doc.content.children if node.kind == "annex"]

    assert "postprocess=mhlw_csv_annexes" in ir_doc.content.tags
    assert [annex.num for annex in annexes] == ["別紙1", "別紙2"]
    assert annexes[0].heading == "コンピュータ化システムのライフサイクルモデル"
    assert annexes[0].text == "画像1 (36KB)"
    assert annexes[0].data["source_format"] == "html_image_reference"
    assert annexes[0].data["extractable_text"] is False
    assert annexes[1].heading == "カテゴリ分類表と対応例"
    assert annexes[1].data["source_format"] == "html_table_title_only"
    assert annexes[1].data["table_rows_found"] == 0
    assert "別紙1" not in (by_nid["cha10"].text or "")
    assert not qualitycheck_document(ir_doc.content)
