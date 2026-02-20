from __future__ import annotations

from pathlib import Path
import re

from qai_xml2ir.egov_parser import parse_egov_xml
from qai_xml2ir.models_ir import IRDocument


def write_sample_xml(path: Path) -> None:
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<Law>
  <LawNum>平成十年厚生省令第〇号</LawNum>
  <LawBody>
    <LawTitle>テスト法</LawTitle>
    <MainProvision>
      <Paragraph Num="1">
        <ParagraphSentence><Sentence>MP</Sentence></ParagraphSentence>
      </Paragraph>
      <Part Num="1">
        <PartTitle>第一編　総則</PartTitle>
        <Chapter Num="1">
          <ChapterTitle>第一章　総則</ChapterTitle>
          <Article Num="10">
            <ArticleTitle>第十条</ArticleTitle>
            <Paragraph Num="1">
              <ParagraphSentence><Sentence>編内条文</Sentence></ParagraphSentence>
            </Paragraph>
          </Article>
        </Chapter>
        <Article Num="11">
          <ArticleTitle>第十一条</ArticleTitle>
          <Paragraph Num="1">
            <ParagraphSentence><Sentence>編直下条文</Sentence></ParagraphSentence>
          </Paragraph>
        </Article>
      </Part>
      <Section Num="1">
        <SectionTitle>第一節　手続</SectionTitle>
        <Subsection Num="1">
          <SubsectionTitle>第一款　小見出し</SubsectionTitle>
          <Division Num="1">
            <DivisionTitle>第一目　細目</DivisionTitle>
            <Article Num="12">
              <ArticleTitle>第十二条</ArticleTitle>
              <Paragraph Num="1">
                <ParagraphSentence><Sentence>款目内条文</Sentence></ParagraphSentence>
              </Paragraph>
            </Article>
          </Division>
        </Subsection>
      </Section>
      <Chapter Num="9" Delete="true">
        <ChapterTitle>第九章　削除</ChapterTitle>
        <Article Num="99">
          <ArticleTitle>第九十九条</ArticleTitle>
          <Paragraph Num="1">
            <ParagraphSentence><Sentence>削除条文</Sentence></ParagraphSentence>
          </Paragraph>
        </Article>
      </Chapter>
      <Article Num="13" Hide="true">
        <ArticleTitle>第十三条</ArticleTitle>
        <Paragraph Num="1">
          <ParagraphSentence><Sentence>非表示条文</Sentence></ParagraphSentence>
        </Paragraph>
      </Article>
      <Article Num="3">
        <ArticleTitle>第三条</ArticleTitle>
        <Paragraph Num="1">
          <ParagraphSentence><Sentence>第三条本文</Sentence></ParagraphSentence>
          <Item Num="1">
            <ItemTitle>一</ItemTitle>
            <ItemSentence><Sentence>A</Sentence></ItemSentence>
          </Item>
        </Paragraph>
      </Article>
      <Article Num="3_2">
        <ArticleTitle>第三条の二</ArticleTitle>
        <Paragraph Num="1">
          <ParagraphSentence><Sentence>第3条の2本文</Sentence></ParagraphSentence>
        </Paragraph>
      </Article>
      <Article Num="3_3">
        <ArticleTitle>第三条の三</ArticleTitle>
        <Paragraph Num="1">
          <ParagraphSentence><Sentence>第三条の三本文</Sentence></ParagraphSentence>
          <Item Num="1">
            <ItemTitle>一</ItemTitle>
            <ItemSentence><Sentence>B</Sentence></ItemSentence>
          </Item>
        </Paragraph>
      </Article>
      <Article Num="1">
        <ArticleTitle>第一条</ArticleTitle>
        <ArticleCaption>（目的）</ArticleCaption>
        <Paragraph Num="1">
          <ParagraphSentence>
            <Sentence>P</Sentence>
          </ParagraphSentence>
          <TableStruct>
            <TableStructTitle>条文内表</TableStructTitle>
            <Table>
              <TableHeaderRow>
                <TableHeaderColumn><Sentence>欄1</Sentence></TableHeaderColumn>
                <TableHeaderColumn><Sentence>欄2</Sentence></TableHeaderColumn>
              </TableHeaderRow>
              <TableRow>
                <TableColumn><Sentence>A</Sentence></TableColumn>
                <TableColumn><Sentence>B</Sentence></TableColumn>
              </TableRow>
              <TableRow>
                <TableColumn><Sentence>C</Sentence></TableColumn>
                <TableColumn><Sentence>D</Sentence></TableColumn>
              </TableRow>
            </Table>
            <Remarks><Sentence>表注: 代表値</Sentence></Remarks>
          </TableStruct>
          <Remarks><Sentence>条文注: 運用上の留意</Sentence></Remarks>
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
              <Subitem2>
                <Subitem2Title>（１）</Subitem2Title>
                <Subitem2Sentence><Sentence>S2</Sentence></Subitem2Sentence>
              </Subitem2>
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
    <AppdxTable Num="1">
      <AppdxTableTitle>別表第一</AppdxTableTitle>
      <Table><TableRow><TableColumn><TableColumnSentence><Sentence>別表本文</Sentence></TableColumnSentence></TableColumn></TableRow></Table>
    </AppdxTable>
    <AppdxNote Num="1">
      <AppdxNoteTitle>別記第一</AppdxNoteTitle>
      <AppdxNoteSentence><Sentence>別記本文</Sentence></AppdxNoteSentence>
    </AppdxNote>
    <SupplProvision>
      <SupplProvisionLabel>附則</SupplProvisionLabel>
      <Paragraph Num="1">
        <ParagraphSentence><Sentence>附則段落</Sentence></ParagraphSentence>
      </Paragraph>
      <Chapter Num="1">
        <ChapterTitle>第一章　附則章</ChapterTitle>
        <Article Num="2">
          <ArticleTitle>附則第二条</ArticleTitle>
          <Paragraph Num="1">
            <ParagraphSentence><Sentence>附則章内条文</Sentence></ParagraphSentence>
          </Paragraph>
        </Article>
      </Chapter>
      <SupplProvisionAppdxTable Num="1">
        <SupplProvisionAppdxTableTitle>附則別表第一</SupplProvisionAppdxTableTitle>
        <SupplProvisionAppdxTableSentence><Sentence>附則別表本文</Sentence></SupplProvisionAppdxTableSentence>
      </SupplProvisionAppdxTable>
      <Article Num="1">
        <ArticleTitle>附則第一条</ArticleTitle>
        <Paragraph Num="1">
          <ParagraphSentence><Sentence>附則本文</Sentence></ParagraphSentence>
        </Paragraph>
      </Article>
    </SupplProvision>
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
    assert ir.schema == "qai.regdoc_ir.v4"

    nodes = flatten(ir.content)
    assert all(n.ord is None or isinstance(n.ord, int) for n in nodes)
    assert all(
        n.nid == "root" or (isinstance(n.ord, int) and n.ord > 0)
        for n in nodes
    )
    ords = [n.ord for n in nodes if n.nid != "root"]
    assert ords == list(range(1, len(ords) + 1))
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

    part_nodes = [n for n in nodes if n.kind == "part"]
    assert any(n.num == "第一編" for n in part_nodes)
    assert any(n.num == "第十条" for n in articles)
    assert any(n.num == "第十一条" for n in articles)

    subsection_nodes = [n for n in nodes if n.kind == "subsection"]
    division_nodes = [n for n in nodes if n.kind == "division"]
    assert len(subsection_nodes) >= 1
    assert len(division_nodes) >= 1
    assert any(n.num == "第十二条" for n in articles)

    art3_2 = next(n for n in articles if n.num == "第三条の二")
    assert art3_2.nid == "art3_2"
    assert all(n.nid != "art32" for n in articles)

    art3 = next(n for n in articles if n.num == "第三条")
    art3_3 = next(n for n in articles if n.num == "第三条の三")
    art3_items = [n for n in nodes if n.kind == "item" and n.nid.startswith("art3.")]
    art3_3_items = [n for n in nodes if n.kind == "item" and n.nid.startswith("art3_3.")]
    assert any(n.nid.endswith(".i1") for n in art3_items)
    assert any(n.nid.endswith(".i1") for n in art3_3_items)
    assert all(n.nid != "art3.i1_2" for n in art3_3_items)

    paragraph = next(n for n in nodes if n.kind == "paragraph" and n.text == "P2")
    item = next(n for n in nodes if n.kind == "item" and n.text == "I")
    subitem = next(n for n in nodes if n.kind == "subitem" and n.text == "S")
    subitem2 = next(n for n in nodes if n.kind == "point" and n.text == "S2")
    assert paragraph.text == "P2"
    assert item.text == "I"
    assert subitem.text == "S"
    assert subitem2.nid.endswith(".ro.pt1")
    assert "I" not in paragraph.text
    assert "S" not in paragraph.text
    assert art1.text == "P"

    top_paragraph = next(n for n in nodes if n.kind == "paragraph" and n.nid.startswith("mp.p"))
    assert top_paragraph.text == "MP"

    annex_article = next(n for n in articles if n.nid == "annex1.art1")
    assert annex_article.num == "附則第一条"

    annex_paragraph = next(n for n in nodes if n.kind == "paragraph" and n.nid == "annex1.p1")
    assert annex_paragraph.text == "附則段落"

    annex_chapter = next(n for n in nodes if n.kind == "chapter" and n.nid == "annex1.ch1")
    assert annex_chapter.num == "第一章"

    annex_chapter_article = next(n for n in articles if n.num == "附則第二条")
    assert annex_chapter_article.nid == "annex1.art2"

    appendices = [n for n in nodes if n.kind == "appendix"]
    appdx_table = next(n for n in appendices if n.nid == "appdx_table1")
    appdx_note = next(n for n in appendices if n.nid == "appdx_note1")
    annex_appdx_table = next(n for n in appendices if n.nid == "annex1.appdx_table1")
    assert appdx_table.num == "別表第一"
    assert appdx_note.num == "別記第一"
    assert annex_appdx_table.num == "附則別表第一"
    assert any(c.kind == "table" for c in appdx_table.children)

    art1_table = next(c for c in art1.children if c.kind == "table")
    assert art1_table.heading == "条文内表"
    art1_header = next(c for c in art1_table.children if c.kind == "table_header")
    assert "欄1" in (art1_header.text or "")
    art1_rows = [n for n in art1_header.children if n.kind == "table_row"]
    assert len(art1_rows) == 2
    assert any("A | B" in (n.text or "") for n in art1_rows)
    art1_table_notes = [n for n in art1_table.children if n.kind == "note"]
    assert any("表注: 代表値" in (n.text or "") for n in art1_table_notes)

    art1_notes = [n for n in art1.children if n.kind == "note"]
    assert any("条文注: 運用上の留意" in (n.text or "") for n in art1_notes)

    assert all(n.num != "第九十九条" for n in articles)
    assert all(n.num != "第十三条" for n in articles)


def test_appendix_scoped_indexing(tmp_path: Path) -> None:
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<Law>
  <LawNum>令和三年法第〇号</LawNum>
  <LawBody>
    <LawTitle>別表連番テスト</LawTitle>
    <MainProvision>
      <Article Num="1">
        <ArticleTitle>第一条</ArticleTitle>
        <Paragraph Num="1">
          <ParagraphSentence><Sentence>本文</Sentence></ParagraphSentence>
        </Paragraph>
      </Article>
    </MainProvision>
    <SupplProvision>
      <SupplProvisionLabel>附則</SupplProvisionLabel>
      <Article Num="1">
        <ArticleTitle>附則第一条</ArticleTitle>
        <Paragraph Num="1">
          <ParagraphSentence><Sentence>附則本文</Sentence></ParagraphSentence>
        </Paragraph>
      </Article>
      <SupplProvisionAppdxTable Num="1">
        <SupplProvisionAppdxTableTitle>附則別表第一</SupplProvisionAppdxTableTitle>
        <SupplProvisionAppdxTableSentence><Sentence>附則別表</Sentence></SupplProvisionAppdxTableSentence>
      </SupplProvisionAppdxTable>
    </SupplProvision>
    <SupplProvision>
      <SupplProvisionLabel>附則</SupplProvisionLabel>
      <Article Num="1">
        <ArticleTitle>附則第一条</ArticleTitle>
        <Paragraph Num="1">
          <ParagraphSentence><Sentence>附則本文2</Sentence></ParagraphSentence>
        </Paragraph>
      </Article>
    </SupplProvision>
    <AppdxStyle Num="1">
      <AppdxStyleTitle>別記第一</AppdxStyleTitle>
      <AppdxStyleSentence><Sentence>別記本文</Sentence></AppdxStyleSentence>
    </AppdxStyle>
    <AppdxTable Num="2">
      <AppdxTableTitle>別表第二</AppdxTableTitle>
      <Table><TableRow><TableColumn><TableColumnSentence><Sentence>別表本文</Sentence></TableColumnSentence></TableColumn></TableRow></Table>
    </AppdxTable>
  </LawBody>
</Law>
"""
    xml_path = tmp_path / "410A00000000000_20240101_000A00000000000.xml"
    xml_path.write_text(xml, encoding="utf-8", newline="\n")
    parsed = parse_egov_xml(xml_path)
    ir = IRDocument(doc_id="jp_test_doc", content=parsed.root, index={})

    nodes = flatten(ir.content)
    appendices = [n for n in nodes if n.kind == "appendix"]
    assert any(n.nid == "appdx_style1" for n in appendices)
    assert any(n.nid == "appdx_table2" for n in appendices)
    assert any(n.nid == "annex1.appdx_table1" for n in appendices)


def test_ord_article_branch_sorting(tmp_path: Path) -> None:
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<Law>
  <LawBody>
    <LawTitle>条枝番ソート</LawTitle>
    <MainProvision>
      <Article Num="29">
        <ArticleTitle>第二十九条</ArticleTitle>
        <Paragraph Num="1"><ParagraphSentence><Sentence>A</Sentence></ParagraphSentence></Paragraph>
      </Article>
      <Article Num="29_2">
        <ArticleTitle>第二十九条の二</ArticleTitle>
        <Paragraph Num="1"><ParagraphSentence><Sentence>B</Sentence></ParagraphSentence></Paragraph>
      </Article>
      <Article Num="29_2_2">
        <ArticleTitle>第二十九条の二の二</ArticleTitle>
        <Paragraph Num="1"><ParagraphSentence><Sentence>C</Sentence></ParagraphSentence></Paragraph>
      </Article>
    </MainProvision>
  </LawBody>
</Law>
"""
    xml_path = tmp_path / "300A00000000000_20240101_000A00000000000.xml"
    xml_path.write_text(xml, encoding="utf-8", newline="\n")
    parsed = parse_egov_xml(xml_path)
    articles = [n for n in flatten(parsed.root) if n.kind == "article"]
    ordered = sorted(articles, key=lambda n: n.ord or "")
    assert [n.num for n in ordered] == ["第二十九条", "第二十九条の二", "第二十九条の二の二"]


def test_ord_collision_avoidance_article_vs_paragraph(tmp_path: Path) -> None:
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<Law>
  <LawBody>
    <LawTitle>衝突回避</LawTitle>
    <MainProvision>
      <Article Num="29_2">
        <ArticleTitle>第二十九条の二</ArticleTitle>
        <Paragraph Num="1"><ParagraphSentence><Sentence>A</Sentence></ParagraphSentence></Paragraph>
        <Paragraph Num="2"><ParagraphSentence><Sentence>B</Sentence></ParagraphSentence></Paragraph>
      </Article>
      <Article Num="29_2_2">
        <ArticleTitle>第二十九条の二の二</ArticleTitle>
        <Paragraph Num="1"><ParagraphSentence><Sentence>C</Sentence></ParagraphSentence></Paragraph>
      </Article>
    </MainProvision>
  </LawBody>
</Law>
"""
    xml_path = tmp_path / "301A00000000000_20240101_000A00000000000.xml"
    xml_path.write_text(xml, encoding="utf-8", newline="\n")
    parsed = parse_egov_xml(xml_path)
    nodes = flatten(parsed.root)
    art_29_2_2 = next(n for n in nodes if n.kind == "article" and n.nid == "art29_2_2")
    p2 = next(n for n in nodes if n.kind == "paragraph" and n.nid == "art29_2.p2")
    assert art_29_2_2.ord != p2.ord


def test_ord_subitem_iroha_sorting(tmp_path: Path) -> None:
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<Law>
  <LawBody>
    <LawTitle>イロハ順</LawTitle>
    <MainProvision>
      <Article Num="1">
        <ArticleTitle>第一条</ArticleTitle>
        <Paragraph Num="1">
          <ParagraphSentence><Sentence>A</Sentence></ParagraphSentence>
          <Item Num="1">
            <ItemTitle>一</ItemTitle>
            <ItemSentence><Sentence>B</Sentence></ItemSentence>
            <Subitem1><Subitem1Title>イ</Subitem1Title><Subitem1Sentence><Sentence>I</Sentence></Subitem1Sentence></Subitem1>
            <Subitem1><Subitem1Title>ロ</Subitem1Title><Subitem1Sentence><Sentence>R</Sentence></Subitem1Sentence></Subitem1>
            <Subitem1><Subitem1Title>ハ</Subitem1Title><Subitem1Sentence><Sentence>H</Sentence></Subitem1Sentence></Subitem1>
          </Item>
        </Paragraph>
      </Article>
    </MainProvision>
  </LawBody>
</Law>
"""
    xml_path = tmp_path / "302A00000000000_20240101_000A00000000000.xml"
    xml_path.write_text(xml, encoding="utf-8", newline="\n")
    parsed = parse_egov_xml(xml_path)
    nodes = flatten(parsed.root)
    subitems = [n for n in nodes if n.kind == "subitem"]
    ordered = sorted(subitems, key=lambda n: n.ord or "")
    assert [n.num for n in ordered] == ["イ", "ロ", "ハ"]


def test_ord_absolute_order_with_parallel_num(tmp_path: Path) -> None:
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<Law>
  <LawBody>
    <LawTitle>並列表現順序</LawTitle>
    <MainProvision>
      <Article Num="15_1">
        <ArticleTitle>第十五条の一</ArticleTitle>
        <Paragraph Num="1"><ParagraphSentence><Sentence>A</Sentence></ParagraphSentence></Paragraph>
      </Article>
      <Article Num="15:16">
        <ArticleTitle>第十五条及び第十六条</ArticleTitle>
        <Paragraph Num="1"><ParagraphSentence><Sentence>B</Sentence></ParagraphSentence></Paragraph>
      </Article>
      <Article Num="15_2">
        <ArticleTitle>第十五条の二</ArticleTitle>
        <Paragraph Num="1"><ParagraphSentence><Sentence>C</Sentence></ParagraphSentence></Paragraph>
      </Article>
      <Article Num="20">
        <ArticleTitle>第二十条</ArticleTitle>
        <Paragraph Num="1">
          <ParagraphSentence><Sentence>D</Sentence></ParagraphSentence>
          <Item Num="1:2">
            <ItemTitle>一及び二</ItemTitle>
            <ItemSentence><Sentence>E</Sentence></ItemSentence>
          </Item>
          <Item Num="3">
            <ItemTitle>三</ItemTitle>
            <ItemSentence><Sentence>F</Sentence></ItemSentence>
          </Item>
        </Paragraph>
      </Article>
    </MainProvision>
  </LawBody>
</Law>
"""
    xml_path = tmp_path / "304A00000000000_20240101_000A00000000000.xml"
    xml_path.write_text(xml, encoding="utf-8", newline="\n")

    parsed = parse_egov_xml(xml_path)
    nodes = flatten(parsed.root)

    a_15_1 = next(n for n in nodes if n.kind == "article" and n.num == "第十五条の一")
    a_1516 = next(n for n in nodes if n.kind == "article" and n.num == "第十五条及び第十六条")
    a_15_2 = next(n for n in nodes if n.kind == "article" and n.num == "第十五条の二")
    assert a_15_1.ord < a_1516.ord < a_15_2.ord

    item_12 = next(n for n in nodes if n.kind == "item" and n.num == "一及び二")
    item_3 = next(n for n in nodes if n.kind == "item" and n.num == "三")
    assert item_12.ord < item_3.ord


def test_article_nid_no_collision_between_colon_and_plain_num(tmp_path: Path) -> None:
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<Law>
  <LawBody>
    <LawTitle>コロンNum衝突回避</LawTitle>
    <MainProvision>
      <Article Num="15:16">
        <ArticleTitle>第十五条及び第十六条</ArticleTitle>
        <Paragraph Num="1"><ParagraphSentence><Sentence>A</Sentence></ParagraphSentence></Paragraph>
      </Article>
      <Article Num="1516">
        <ArticleTitle>第千五百十六条</ArticleTitle>
        <Paragraph Num="1"><ParagraphSentence><Sentence>B</Sentence></ParagraphSentence></Paragraph>
      </Article>
    </MainProvision>
  </LawBody>
</Law>
"""
    xml_path = tmp_path / "305A00000000000_20240101_000A00000000000.xml"
    xml_path.write_text(xml, encoding="utf-8", newline="\n")

    parsed = parse_egov_xml(xml_path)
    articles = [n for n in flatten(parsed.root) if n.kind == "article"]
    nids = {n.nid for n in articles}

    assert "art15__16" in nids
    assert "art1516" in nids
    assert "art15__16_2" not in nids
    assert "art1516_2" not in nids
