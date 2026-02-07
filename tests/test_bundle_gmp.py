from __future__ import annotations

from pathlib import Path

import yaml

from qai_xml2ir import cli


def write_sample_xml(path: Path) -> None:
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<Law>
  <LawNum>平成十年厚生省令第〇号</LawNum>
  <LawBody>
    <LawTitle>テスト法</LawTitle>
    <MainProvision>
      <Article Num="1">
        <ArticleTitle>第一条</ArticleTitle>
        <ArticleCaption>（目的）</ArticleCaption>
        <Paragraph Num="1">
          <ParagraphSentence>
            <Sentence>この省令はテストである。</Sentence>
          </ParagraphSentence>
          <Item Num="1">
            <ItemTitle>一</ItemTitle>
            <ItemSentence><Sentence>項目一</Sentence></ItemSentence>
          </Item>
        </Paragraph>
      </Article>
      <Article Num="2">
        <ArticleTitle>第二条</ArticleTitle>
        <Paragraph Num="1">
          <ParagraphNum>1</ParagraphNum>
          <ParagraphSentence><Sentence>第一項</Sentence></ParagraphSentence>
        </Paragraph>
        <Paragraph Num="2">
          <ParagraphNum>2</ParagraphNum>
          <ParagraphSentence><Sentence>第二項</Sentence></ParagraphSentence>
        </Paragraph>
      </Article>
    </MainProvision>
  </LawBody>
</Law>
"""
    path.write_text(xml, encoding="utf-8", newline="\n")


def test_bundle_outputs(tmp_path: Path) -> None:
    xml_path = tmp_path / "416M60000100179_20260501_507M60000100117.xml"
    write_sample_xml(xml_path)
    out_dir = tmp_path / "out"
    doc_id = "jp_test_doc"

    cli.bundle(
        input=xml_path,
        out_dir=out_dir,
        doc_id=doc_id,
        short_title="テスト",
        retrieved_at="2026-02-02",
        source_url="https://laws.e-gov.go.jp/law/416M60000100179/20260501_507M60000100117",
        emit_only="all",
    )

    ir_path = out_dir / f"{doc_id}.regdoc_ir.yaml"
    parser_profile_path = out_dir / f"{doc_id}.parser_profile.yaml"
    regdoc_profile_path = out_dir / f"{doc_id}.regdoc_profile.yaml"
    meta_path = out_dir / f"{doc_id}.meta.yaml"

    assert ir_path.exists()
    assert parser_profile_path.exists()
    assert regdoc_profile_path.exists()
    assert meta_path.exists()

    ir = yaml.safe_load(ir_path.read_text(encoding="utf-8"))
    regdoc_profile = yaml.safe_load(regdoc_profile_path.read_text(encoding="utf-8"))
    meta = yaml.safe_load(meta_path.read_text(encoding="utf-8"))

    assert ir["doc_id"] == doc_id
    assert ir["schema"] == "qai.regdoc_ir.v2"
    assert regdoc_profile["doc_id"] == doc_id
    assert meta["doc"]["id"] == doc_id
    assert meta["bundle"]["ir"]["schema"] == "qai.regdoc_ir.v2"
    assert meta["bundle"]["parser_profile"]["id"] == "jp_law_default_v1"
