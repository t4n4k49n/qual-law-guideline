from __future__ import annotations

from pathlib import Path
import re
from typing import Dict, List

import yaml

from qai_text2ir import cli
from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir, qualitycheck_document
from qai_xml2ir.verify import verify_document


def _flatten(node: Dict) -> List[Dict]:
    out = [node]
    for child in node.get("children", []):
        out.extend(_flatten(child))
    return out


def _load_profile(path: str) -> Dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def test_eu_gmp_chapter_heading_merge_and_hierarchy(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "Chapter 1",
            "Pharmaceutical Quality System",
            "1.1 Principle",
            "This chapter should describe the quality system.",
            "1.4 Product quality review",
            "(i) The review should include at least",
            "(ii) Deviations and non-conformances",
            "• CAPA actions",
        ]
    )
    input_path = tmp_path / "eu_gmp_ch1.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")
    parser_profile = _load_profile("src/qai_text2ir/profiles/eu_gmp_chap1_default_v1.yaml")

    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="eu_gmp_ch1_sample",
        parser_profile=parser_profile,
    ).to_dict()
    verify_document(ir_doc)

    nodes = _flatten(ir_doc["content"])
    chapter = next(n for n in nodes if n["kind"] == "chapter" and n.get("num") == "1")
    paragraph_14 = next(n for n in nodes if n["kind"] == "paragraph" and n.get("num") == "1.4")
    item_ii = next(n for n in nodes if n["kind"] == "item" and n.get("num") == "ii")
    bullet = next(n for n in nodes if n["kind"] == "subitem" and n.get("kind_raw") == "•")

    assert chapter.get("heading") == "Pharmaceutical Quality System"
    assert item_ii["nid"].startswith(paragraph_14["nid"])
    assert bullet["nid"].startswith(item_ii["nid"])


def test_bundle_meta_doc_type_source_format_and_identifiers(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "Chapter 1",
            "Pharmaceutical Quality System",
            "1.1 Principle",
            "Text body.",
        ]
    )
    input_path = tmp_path / "eu_gmp_ch1_meta.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")
    out_dir = tmp_path / "out"
    doc_id = "eu_gmp_meta_sample"

    cli.bundle(
        input=input_path,
        out_dir=out_dir,
        doc_id=doc_id,
        title="EU GMP Chapter 1",
        short_title="EU GMP Ch1",
        doc_type="guideline",
        source_url="https://example.org/chapter1.pdf",
        retrieved_at="2026-02-12",
        eu_volume="4",
        parser_profile_path=Path("src/qai_text2ir/profiles/eu_gmp_chap1_default_v2.yaml"),
        emit_only="all",
    )

    meta = yaml.safe_load((out_dir / f"{doc_id}.meta.yaml").read_text(encoding="utf-8"))
    assert meta["doc"]["doc_type"] == "guideline"
    assert meta["doc"]["sources"][0]["format"] == "pdf"
    assert meta["doc"]["identifiers"]["eu_volume"] == "4"
    assert "cfr_title" not in meta["doc"]["identifiers"]
    assert "cfr_part" not in meta["doc"]["identifiers"]


def test_drop_page_numbers_and_fix_hyphen_wrap(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "Chapter 1",
            "Pharmaceutical Quality System",
            "Pharmaceutical Quality System1",
            "1.4 Product quality review",
            "(xiv) This should ensure that process, procedural or system-",
            " based errors or problems have not been overlooked.",
            "Commission Européenne, B-1049 Bruxelles / Europese Commissie, B-1049 Brussel - Belgium Telephone: (32-2) 299 11 11.",
            "   3",
        ]
    )
    input_path = tmp_path / "eu_gmp_drop_page_and_hyphen.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")
    parser_profile = _load_profile("src/qai_text2ir/profiles/eu_gmp_chap1_default_v2.yaml")

    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="eu_gmp_drop_page_and_hyphen",
        parser_profile=parser_profile,
    )
    ir_dict = ir_doc.to_dict()
    verify_document(ir_dict)

    nodes = _flatten(ir_dict["content"])
    item_xiv = next(n for n in nodes if n["kind"] == "item" and n.get("num") == "xiv")
    text_xiv = item_xiv.get("text") or ""
    assert "system-based" in text_xiv
    assert "system- based" not in text_xiv
    assert "Commission" not in "\n".join((n.get("text") or "") for n in nodes)
    assert "Pharmaceutical Quality System1" not in "\n".join((n.get("text") or "") for n in nodes)
    for node in nodes:
        for field in ("heading", "text"):
            value = node.get(field) or ""
            for line in value.splitlines():
                assert not re.fullmatch(r"\s*\d{1,3}\s*", line)
    warnings = qualitycheck_document(ir_doc.content)
    assert not any("unresolved hyphen-space pattern remains" in w for w in warnings)
    assert not any("page-number-only line remains" in w for w in warnings)


def test_parse_item_roman_rparen_and_dedent_back_to_paragraph(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "Chapter 1",
            "Pharmaceutical Quality System",
            "1.13 The principles of quality risk management are that:",
            "    i) The evaluation of the risk to quality is based on scientific knowledge,",
            "       experience with the process and ultimately links to the protection of the patient",
            "    ii) The level of effort, formality and documentation of the quality risk",
            "        management process is commensurate with the level of risk",
            "Examples of the processes and applications of quality risk management can be found.",
            "8",
        ]
    )
    input_path = tmp_path / "eu_gmp_item_rparen_dedent.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")
    parser_profile = _load_profile("src/qai_text2ir/profiles/eu_gmp_chap1_default_v2.yaml")

    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="eu_gmp_item_rparen_dedent",
        parser_profile=parser_profile,
    )
    ir_dict = ir_doc.to_dict()
    verify_document(ir_dict)

    nodes = _flatten(ir_dict["content"])
    paragraph_113 = next(n for n in nodes if n["kind"] == "paragraph" and n.get("num") == "1.13")
    item_i = next(n for n in nodes if n["kind"] == "item" and n.get("num") == "i")
    item_ii = next(n for n in nodes if n["kind"] == "item" and n.get("num") == "ii")

    assert item_i["nid"].startswith(paragraph_113["nid"])
    assert item_ii["nid"].startswith(paragraph_113["nid"])
    assert "Examples of the processes and applications of quality risk management can be found." in (
        paragraph_113.get("text") or ""
    )
    assert "Examples of the processes and applications of quality risk management can be found." not in (
        item_ii.get("text") or ""
    )
    assert " 8 " not in f" {paragraph_113.get('text') or ''} "


def test_preformatted_block_still_repairs_hyphen_wrap(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "Chapter 1",
            "Pharmaceutical Quality System",
            "1.4 Product quality review",
            "(xiv) process, procedural or system-",
            "            based errors are reviewed.",
        ]
    )
    input_path = tmp_path / "eu_gmp_preformatted_hyphen.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")
    parser_profile = _load_profile("src/qai_text2ir/profiles/eu_gmp_chap1_default_v2.yaml")

    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="eu_gmp_preformatted_hyphen",
        parser_profile=parser_profile,
    )
    nodes = _flatten(ir_doc.to_dict()["content"])
    item_xiv = next(n for n in nodes if n["kind"] == "item" and n.get("num") == "xiv")
    text_xiv = item_xiv.get("text") or ""

    assert "system-based" in text_xiv
    assert "system-            based" not in text_xiv


def test_profile_loader_defaults_to_eu_gmp_v2() -> None:
    profile = load_parser_profile(family="EU_GMP")
    assert profile["id"] == "eu_gmp_chap1_default_v2"
