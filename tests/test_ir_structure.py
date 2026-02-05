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
            <Subitem1>
              <Subitem1Title>ロ</Subitem1Title>
              <Subitem1Sentence><Sentence>ロの内容</Sentence></Subitem1Sentence>
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

    art1 = next(n for n in articles if n.num == "第一条")
    assert art1.heading == "（目的）"
    assert art1.text is not None
    assert all(c.kind != "paragraph" for c in art1.children)

    art2 = next(n for n in articles if n.num == "第二条")
    assert any(c.kind == "paragraph" for c in art2.children)

    subitems = [n for n in nodes if n.kind == "subitem"]
    assert any(n.nid.endswith(".ro") for n in subitems)
