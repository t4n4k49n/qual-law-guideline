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


def test_eu_gmp_chapter2_sections_and_responsibility_items(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "Chapter 2: Personnel",
            "Principle",
            "The correct manufacture of medicinal products relies upon people.",
            "General",
            "2.1 The manufacturer should have an adequate number of personnel.",
            "Key Personnel",
            "2.6 The duties of the Qualified Person(s) are described in Article 51 of Directive 2001/83/EC1,",
            "and can be summarised as follows:",
            "a) for medicinal products manufactured within the European Union, a Qualified Person must",
            "ensure that each batch has been manufactured and checked in accordance with the marketing",
            "authorisation2;",
            "The persons responsible for these duties must meet the qualification requirements laid down",
            "in Article 49 3 of the same Directive.",
            "(b) in the case of medicinal products coming from third countries, a Qualified Person must ensure",
            "that each production batch has undergone tests.",
            "2.7 The head of the Production Department generally has the following responsibilities:",
            "      i.   To ensure that products are produced and stored according to the appropriate",
            "           documentation in order to obtain the required quality;",
            "     ii.   To approve the instructions relating to production operations.",
            "1",
            "    Article 55 of Directive 2001/82/EC",
        ]
    )
    input_path = tmp_path / "eu_gmp_ch2.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")
    parser_profile = load_parser_profile(path=Path("src/qai_text2ir/profiles/eu_gmp_chap2_default_v1.yaml"))

    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="eu_gmp_ch2_sample",
        parser_profile=parser_profile,
    )
    ir_dict = ir_doc.to_dict()
    verify_document(ir_dict)

    nodes = _flatten(ir_dict["content"])
    chapter = next(n for n in nodes if n["kind"] == "chapter")
    sections = [n for n in nodes if n["kind"] == "section"]
    para_27 = next(n for n in nodes if n["kind"] == "paragraph" and n.get("num") == "2.7")
    para_26 = next(n for n in nodes if n["kind"] == "paragraph" and n.get("num") == "2.6")
    item_i = next(n for n in nodes if n["kind"] == "item" and n.get("num") == "i")
    item_ii = next(n for n in nodes if n["kind"] == "item" and n.get("num") == "ii")
    item_a = next(n for n in nodes if n["kind"] == "item" and n.get("num") == "a")
    item_b = next(n for n in nodes if n["kind"] == "item" and n.get("num") == "b")
    all_text = "\n".join(n.get("text") or "" for n in nodes)

    assert chapter.get("heading") == "Personnel"
    assert [s.get("heading") for s in sections[:3]] == ["Principle", "General", "Key Personnel"]
    assert item_i["nid"].startswith(para_27["nid"])
    assert item_ii["nid"].startswith(para_27["nid"])
    assert "documentation in order to obtain the required quality" in (item_i.get("text") or "")
    assert "\n" not in (item_i.get("text") or "")
    assert item_a["nid"].startswith(para_26["nid"])
    assert item_b["nid"].startswith(para_26["nid"])
    assert "Article 55 of Directive 2001/82/EC" not in all_text
    assert "Directive 2001/83/EC1" not in (para_26.get("text") or "")
    assert "authorisation2" not in (item_a.get("text") or "")
    assert "Article 49 3" not in (para_26.get("text") or "")


def test_eu_gmp_chapter3_sections_and_footnote_cleanup(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "Chapter 3: Premises and Equipment",
            "Deadline for coming into operation: 1 March 2015.",
            "    \uf0b7    from 1 June 2015 onwards for any medicinal product newly introduced into shared",
            "         manufacturing facilities;",
            "a",
            "  In January 2015 the deadline for coming into operation was adapted with regard to the toxicological evaluation",
            "to align with the coming effect of the EMA guideline on setting health based exposure limits for use in risk",
            "identification in the manufacture of different medicinal products in shared facilities.",
            "ER 3 PREMISES AND EQUIPMENT",
            "PRINCIPLE",
            "Premises and equipment must be located, designed, constructed, adapted and maintained to",
            "suit the operations to be carried out.",
            "PREMISES",
            "General",
            "3.1 Premises should be situated in an environment which, when considered together with",
            "measures to protect the manufacture, presents minimal risk of causing contamination.",
            "Production Area",
            "3.6 Cross-contamination should be prevented for all products by appropriate design and",
            "operation of manufacturing facilities.",
            "      i.   the risk cannot be adequately controlled by operational and/ or technical measures,",
            "     ii.   scientific data from the toxicological evaluation does not support a controllable",
            "           risk.",
            "Further guidance can be found in Chapter 5 and in Annexes 2, 3, 4, 5 & 6.",
            "EQUIPMENT",
            "3.34 Manufacturing equipment should be designed, located and maintained to suit its",
            "intended purpose.",
        ]
    )
    input_path = tmp_path / "eu_gmp_ch3.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")
    parser_profile = load_parser_profile(path=Path("src/qai_text2ir/profiles/eu_gmp_chap3_default_v1.yaml"))

    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="eu_gmp_ch3_sample",
        parser_profile=parser_profile,
    )
    ir_dict = ir_doc.to_dict()
    verify_document(ir_dict)

    nodes = _flatten(ir_dict["content"])
    sections = [n for n in nodes if n["kind"] == "section"]
    para_36 = next(n for n in nodes if n["kind"] == "paragraph" and n.get("num") == "3.6")
    para_334 = next(n for n in nodes if n["kind"] == "paragraph" and n.get("num") == "3.34")
    item_i = next(n for n in nodes if n["kind"] == "item" and n.get("num") == "i")
    item_ii = next(n for n in nodes if n["kind"] == "item" and n.get("num") == "ii")
    deadline_bullet = next(n for n in nodes if n["kind"] == "subitem" and "1 June 2015" in (n.get("text") or ""))
    guidance_para = next(n for n in nodes if n["kind"] == "paragraph" and "Further guidance" in (n.get("text") or ""))
    all_text = "\n".join(n.get("text") or "" for n in nodes)

    assert [s.get("heading") for s in sections] == [
        "PRINCIPLE",
        "PREMISES",
        "General",
        "Production Area",
        "EQUIPMENT",
    ]
    assert para_36["nid"].startswith("cha3.sec4")
    assert item_i["nid"].startswith(para_36["nid"])
    assert item_ii["nid"].startswith(para_36["nid"])
    assert "\uf0b7" not in (deadline_bullet.get("text") or "")
    assert "manufacturing facilities" in (deadline_bullet.get("text") or "")
    assert guidance_para["nid"].startswith("cha3.sec4")
    assert "Further guidance" not in (item_ii.get("text") or "")
    assert "intended purpose" in (para_334.get("text") or "")
    assert "\n" not in (para_334.get("text") or "")
    assert "ER 3 PREMISES" not in all_text
    assert "deadline for coming into operation was adapted" not in all_text


def test_eu_gmp_chapter4_to_9_profile_preparation_samples(tmp_path: Path) -> None:
    parser_profile = load_parser_profile(path=Path("src/qai_text2ir/profiles/eu_gmp_chap4_9_default_v1.yaml"))
    samples = {
        "chap4": [
            "Chapter 4: Documentation",
            "Table of Contents",
            "Principle",
            "Required GMP Documentation",
            "Procedures and records",
            "Principle",
            "Good documentation constitutes an essential part of the quality assurance system.",
            "Required GMP Documentation",
            "Required GMP documentation (by type):",
            "Specifications Describe in detail the requirements with which the products or",
            "materials used or obtained during manufacture have to conform.",
            "Specifications for starting and packaging materials",
            "4.14 Specifications for starting and primary or printed packaging materials should include or",
            "provide reference to, if applicable:",
            "     a) A description of the materials, including:",
            "              - The designated name and the internal code reference;",
            "Note: Where a validated process is continuously monitored and controlled, then automatically",
            "generated reports may be limited to compliance summaries.",
        ],
        "chap5": [
            "CHAPTER 5 PRODUCTION",
            "Chapter 5: Production",
            "Status of the document: Revisiona.",
            "a",
            "  In January 2015 the deadline for coming into operation was adapted with regard to the toxicological evaluation",
            "to align with the coming effect of the EMA guideline on setting health based exposure limits for use in risk",
            "identification in the manufacture of different medicinal products in shared facilities. Furthermore, correction of",
            "the reference in footnote 2 took place.",
            "Principle",
            "Production operations must follow clearly defined procedures.",
            "General",
            "5.1 Production should be performed and supervised by competent people.",
            "Prevention of cross-contamination in production",
            "5.20 A Quality Risk Management process should be used to assess and control the risks.",
            "Starting materials",
            "5.35 Manufacturers of finished products are responsible for any testing of starting materials.",
            "Product shortage due to manufacturing constraints",
            "5.71 The manufacturer should report restrictions in supply in accordance with its legal obligations4.",
            "4",
            "    Articles 23a and 81 of Directive 2001/83/EC",
        ],
        "chap7": [
            "Chapter 7",
            "Outsourced Activities",
            "Principle",
            "Any activity covered by the GMP Guide that is outsourced should be controlled.",
            "Note: This Chapter deals with the responsibilities of manufacturers towards the",
            "Competent Authorities of the Member States.",
            "General",
            "7.1 There should be a written Contract covering the outsourced activities.",
            "The Contract Giver",
            "7.4 The pharmaceutical quality system of the Contract Giver should include control.",
        ],
        "chap9": [
            "CHAPTER 9 SELF INSPECTION",
            "Principle",
            "Self inspections should be conducted in order to monitor implementation.",
            "9.1 Personnel matters should be examined at intervals.",
            "59",
        ],
    }

    parsed = {}
    for name, lines in samples.items():
        input_path = tmp_path / f"{name}.txt"
        input_path.write_text("\n".join(lines), encoding="utf-8", newline="\n")
        ir_doc = parse_text_to_ir(
            input_path=input_path,
            doc_id=f"eu_gmp_{name}_sample",
            parser_profile=parser_profile,
        )
        ir_dict = ir_doc.to_dict()
        verify_document(ir_dict)
        parsed[name] = _flatten(ir_dict["content"])

    chap4_sections = [n.get("heading") for n in parsed["chap4"] if n["kind"] == "section"]
    chap4_text = "\n".join(n.get("text") or "" for n in parsed["chap4"])
    chap4_note = next(n for n in parsed["chap4"] if n["kind"] == "note")
    chap4_bullet = next(n for n in parsed["chap4"] if n["kind"] == "subitem")

    assert chap4_sections.count("Principle") == 1
    assert "Required GMP Documentation" in chap4_sections
    assert "Specifications for starting and packaging materials" in chap4_sections
    assert "Table of Contents" not in chap4_text
    assert "validated process" in (chap4_note.get("text") or "")
    assert "designated name" in (chap4_bullet.get("text") or "")

    chap5_chapters = [n for n in parsed["chap5"] if n["kind"] == "chapter"]
    chap5_sections = [n.get("heading") for n in parsed["chap5"] if n["kind"] == "section"]
    chap5_text = "\n".join(n.get("text") or "" for n in parsed["chap5"])

    assert len(chap5_chapters) == 1
    assert chap5_chapters[0].get("heading") == "Production"
    assert "Prevention of cross-contamination in production" in chap5_sections
    assert "Product shortage due to manufacturing constraints" in chap5_sections
    assert "footnote 2 took place" not in chap5_text
    assert "legal obligations4" not in chap5_text
    assert "Articles 23a" not in chap5_text

    chap7_chapter = next(n for n in parsed["chap7"] if n["kind"] == "chapter")
    chap7_note = next(n for n in parsed["chap7"] if n["kind"] == "note")
    chap7_sections = [n.get("heading") for n in parsed["chap7"] if n["kind"] == "section"]

    assert chap7_chapter.get("heading") == "Outsourced Activities"
    assert "This Chapter deals" in (chap7_note.get("text") or "")
    assert "The Contract Giver" in chap7_sections

    chap9_chapter = next(n for n in parsed["chap9"] if n["kind"] == "chapter")
    chap9_text = "\n".join(n.get("text") or "" for n in parsed["chap9"])

    assert chap9_chapter.get("heading") == "SELF INSPECTION"
    assert "Self inspections should be conducted" in chap9_text
    assert all("\n" not in (n.get("text") or "") for n in parsed["chap9"])
    assert "59" not in chap9_text
