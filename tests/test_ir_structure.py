from __future__ import annotations

from pathlib import Path

from qai_xml2ir.egov_parser import parse_egov_xml
from qai_xml2ir.models_ir import IRDocument


def write_sample_xml(path: Path) -> None:
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<Law>
  <LawNum>平成十年厚生省令第〇号</LawNum>
  <LawBody>
    <LawTitle>テスト法</LawTitle>
    <MainProvision>
      <Article Num="3_2">
        <ArticleTitle>第三条の二</ArticleTitle>
        <Paragraph Num="1">
          <ParagraphSentence><Sentence>第3条の2本文</Sentence></ParagraphSentence>
        </Paragraph>
      </Article>
      <Article Num="1">
        <ArticleTitle>第一条</ArticleTitle>
        <ArticleCaption>（目的）</ArticleCaption>
        <Paragraph Num="1">
          <ParagraphSentence>
            <Sentence>P</Sentence>
          </ParagraphSentence>
        </Paragraph>
      </Article>
      <Article Num="4">
        <ArticleTitle>第四条</ArticleTitle>
        <Paragraph Num="1">
          <ParagraphNum>1</ParagraphNum>
          <ParagraphSentence><Sentence>P2</Sentence></ParagraphSentence>
          <Item Num="1">
            <ItemTitle>一</ItemTitle>
            <ItemSentence><Sentence>I</Sentence></ItemSentence>
            <Subitem1>
              <Subitem1Title>ロ</Subitem1Title>
              <Subitem1Sentence><Sentence>S</Sentence></Subitem1Sentence>
            </Subitem1>
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


def flatten(node):
    nodes = [node]
    for c in node.children:
        nodes.extend(flatten(c))
    return nodes


def test_ir_structure(tmp_path: Path) -> None:
    xml_path = tmp_path / "416M60000100179_20260501_507M60000100117.xml"
    write_sample_xml(xml_path)
    parsed = parse_egov_xml(xml_path)
    ir = IRDocument(doc_id="jp_test_doc", content=parsed.root, index={})

    nodes = flatten(ir.content)
    articles = [n for n in nodes if n.kind == "article"]
    assert len(articles) >= 2
    assert parsed.as_of == "2026-05-01"

    art1 = next(n for n in articles if n.num == "第一条")
    assert art1.heading == "（目的）"
    assert art1.text is not None
    assert all(c.kind != "paragraph" for c in art1.children)

    art2 = next(n for n in articles if n.num == "第二条")
    assert any(c.kind == "paragraph" for c in art2.children)

    subitems = [n for n in nodes if n.kind == "subitem"]
    assert any(n.nid.endswith(".ro") for n in subitems)

    art3_2 = next(n for n in articles if n.num == "第三条の二")
    assert art3_2.nid == "art3_2"
    assert all(n.nid != "art32" for n in articles)

    paragraph = next(n for n in nodes if n.kind == "paragraph" and n.text == "P2")
    item = next(n for n in nodes if n.kind == "item" and n.text == "I")
    subitem = next(n for n in nodes if n.kind == "subitem" and n.text == "S")
    assert paragraph.text == "P2"
    assert item.text == "I"
    assert subitem.text == "S"
    assert "I" not in paragraph.text
    assert "S" not in paragraph.text
    assert art1.text == "P"
