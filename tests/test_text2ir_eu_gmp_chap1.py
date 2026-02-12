from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import yaml

from qai_text2ir import cli
from qai_text2ir.text_parser import parse_text_to_ir
from qai_xml2ir.verify import verify_document


def _flatten(node: Dict) -> List[Dict]:
    out = [node]
    for child in node.get("children", []):
        out.extend(_flatten(child))
    return out


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
    profile_path = Path("src/qai_text2ir/profiles/eu_gmp_chap1_default_v1.yaml")
    parser_profile = yaml.safe_load(profile_path.read_text(encoding="utf-8"))

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
        parser_profile_path=Path("src/qai_text2ir/profiles/eu_gmp_chap1_default_v1.yaml"),
        emit_only="all",
    )

    meta = yaml.safe_load((out_dir / f"{doc_id}.meta.yaml").read_text(encoding="utf-8"))
    assert meta["doc"]["doc_type"] == "guideline"
    assert meta["doc"]["sources"][0]["format"] == "pdf"
    assert meta["doc"]["identifiers"]["eu_volume"] == "4"
    assert "cfr_title" not in meta["doc"]["identifiers"]
    assert "cfr_part" not in meta["doc"]["identifiers"]
