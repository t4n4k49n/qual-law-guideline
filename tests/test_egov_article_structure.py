from __future__ import annotations

from pathlib import Path

from qai_xml2ir.egov_parser import parse_egov_xml


def _flatten(node):
    nodes = [node]
    for child in node.children:
        nodes.extend(_flatten(child))
    return nodes


def _find_by_nid(root, nid: str):
    for node in _flatten(root):
        if node.nid == nid:
            return node
    return None


def _write_minimal_law(path: Path, body: str) -> None:
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Law>
  <LawNum>令和八年厚生労働省令第〇号</LawNum>
  <LawBody>
    <LawTitle>構造テスト法令</LawTitle>
    <MainProvision>
{body}
    </MainProvision>
  </LawBody>
</Law>
"""
    path.write_text(xml, encoding="utf-8", newline="\n")


def test_article_single_paragraph_num_empty_keeps_paragraph_layer(tmp_path: Path) -> None:
    body = """      <Article Num="1">
        <ArticleTitle>第一条</ArticleTitle>
        <Paragraph Num="1">
          <ParagraphNum/>
          <ParagraphSentence>
            <Sentence>薬局の構造設備の基準は、次のとおりとする。</Sentence>
          </ParagraphSentence>
          <Item Num="1">
            <ItemTitle>一</ItemTitle>
            <ItemSentence><Sentence>一号本文</Sentence></ItemSentence>
          </Item>
        </Paragraph>
      </Article>"""
    xml_path = tmp_path / "egov_min_single.xml"
    _write_minimal_law(xml_path, body)

    parsed = parse_egov_xml(xml_path)
    root = parsed.root
    nodes = _flatten(root)

    art1 = _find_by_nid(root, "art1")
    assert art1 is not None
    assert art1.kind == "article"
    assert art1.text is None

    p1 = _find_by_nid(root, "art1.p1")
    assert p1 is not None
    assert p1.kind == "paragraph"
    assert p1.text is not None

    # Item は article 直下ではなく paragraph 直下に配置されること
    i1 = _find_by_nid(root, "art1.p1.i1")
    assert i1 is not None
    assert i1.kind == "item"
    assert all(not (c.kind == "item" and c.nid == "art1.p1.i1") for c in art1.children)
    assert any(c.kind == "item" and c.nid == "art1.p1.i1" for c in p1.children)

    # fold が復活した場合に落ちるガード
    assert all(not (n.kind == "article" and (n.text or "").strip()) for n in nodes)
    for article in [n for n in nodes if n.kind == "article"]:
        assert any(c.kind == "paragraph" for c in article.children)
        assert all(c.kind not in {"item", "subitem", "point"} for c in article.children)


def test_article_with_multiple_paragraphs_keeps_all_paragraph_nodes(tmp_path: Path) -> None:
    body = """      <Article Num="2">
        <ArticleTitle>第二条</ArticleTitle>
        <Paragraph Num="1">
          <ParagraphSentence><Sentence>第一項本文</Sentence></ParagraphSentence>
          <Item Num="1">
            <ItemTitle>一</ItemTitle>
            <ItemSentence><Sentence>第一項一号本文</Sentence></ItemSentence>
          </Item>
        </Paragraph>
        <Paragraph Num="2">
          <ParagraphNum>2</ParagraphNum>
          <ParagraphSentence><Sentence>第二項本文</Sentence></ParagraphSentence>
        </Paragraph>
      </Article>"""
    xml_path = tmp_path / "egov_min_multi.xml"
    _write_minimal_law(xml_path, body)

    parsed = parse_egov_xml(xml_path)
    root = parsed.root

    art2 = _find_by_nid(root, "art2")
    assert art2 is not None
    assert art2.kind == "article"
    assert art2.text is None

    p1 = _find_by_nid(root, "art2.p1")
    p2 = _find_by_nid(root, "art2.p2")
    assert p1 is not None and p1.kind == "paragraph"
    assert p2 is not None and p2.kind == "paragraph"
    assert any(c.nid == "art2.p1" for c in art2.children)
    assert any(c.nid == "art2.p2" for c in art2.children)

    i1 = _find_by_nid(root, "art2.p1.i1")
    assert i1 is not None
    assert i1.kind == "item"
    assert all(c.kind not in {"item", "subitem", "point"} for c in art2.children)
