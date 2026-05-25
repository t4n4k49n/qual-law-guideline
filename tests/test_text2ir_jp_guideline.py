from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import yaml

from qai_text2ir import cli
from qai_text2ir.html_extract import extract_mhlw_t_doc_lines
from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir
from qai_xml2ir.verify import verify_document


def _flatten(node: Dict) -> List[Dict]:
    out = [node]
    for child in node.get("children", []):
        out.extend(_flatten(child))
    return out


def test_jp_profile_normalizes_fullwidth_markers_and_hierarchy(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "１．序文",
            "１．３　適用範囲",
            "本文です。",
            "（１）　一つ目の要件",
            "①　詳細要件",
            "第９条の２ 見出し",
            "条文形式の本文です。",
            "Ａ１ 参考情報",
        ]
    )
    input_path = tmp_path / "jp_guideline.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")
    profile = load_parser_profile(family="JP_GUIDELINE")

    ir = parse_text_to_ir(input_path=input_path, doc_id="jp_guideline_sample", parser_profile=profile).to_dict()
    verify_document(ir)
    nodes = _flatten(ir["content"])

    chapter_1 = next(n for n in nodes if n["kind"] == "chapter" and n.get("num") == "1")
    paragraph_13 = next(n for n in nodes if n["kind"] == "paragraph" and n.get("num") == "1.3")
    item_1 = next(n for n in nodes if n["kind"] == "item" and n.get("num") == "1")
    subitem_1 = next(n for n in nodes if n["kind"] == "subitem" and n.get("num") == "1")
    article_like = next(n for n in nodes if n["kind"] == "paragraph" and n.get("num") == "9_2")

    assert chapter_1.get("heading") == "序文"
    assert any(n["kind"] == "chapter" and n.get("num") == "A1" for n in nodes)
    assert paragraph_13["nid"].startswith(chapter_1["nid"])
    assert item_1["nid"].startswith(paragraph_13["nid"])
    assert subitem_1["nid"].startswith(item_1["nid"])
    assert article_like.get("kind_raw") == "第９条の２"


def test_jp_profile_bundle_outputs_four_files(tmp_path: Path) -> None:
    input_path = tmp_path / "api_gmp_excerpt.txt"
    input_path.write_text(
        "\n".join(
            [
                "1.3   適用範囲",
                "本ガイドラインは、ヒト用医薬品に使用する原薬に適用する。",
                "(1) 対象範囲を定める。",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )
    out_dir = tmp_path / "bundle"
    doc_id = "jp_pmda_api_gmp_excerpt"

    cli.bundle(
        input=input_path,
        out_dir=out_dir,
        doc_id=doc_id,
        title="原薬GMPのガイドライン 抜粋",
        short_title="原薬GMPガイドライン",
        doc_type="guideline",
        source_url="https://www.pmda.go.jp/files/000156438.pdf",
        source_format="txt",
        retrieved_at="2026-05-23",
        jurisdiction="JP",
        language="ja",
        family="JP_GUIDELINE",
        emit_only="all",
    )

    for suffix in ("regdoc_ir", "parser_profile", "regdoc_profile", "meta"):
        assert (out_dir / f"{doc_id}.{suffix}.yaml").exists()
    ir = yaml.safe_load((out_dir / f"{doc_id}.regdoc_ir.yaml").read_text(encoding="utf-8"))
    verify_document(ir)


def test_extract_mhlw_t_doc_html_lines() -> None:
    lines = extract_mhlw_t_doc_lines(Path("data/human-readable/mhlw/csv_guideline/00tb6573.html"))

    assert "1．3 カテゴリ分類" in lines
    assert "3．コンピュータ化システムの開発、検証及び運用管理に関する文書の作成" in lines
    assert not any(line == "目次" for line in lines)
