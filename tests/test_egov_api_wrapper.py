from __future__ import annotations

from pathlib import Path

from qai_xml2ir.cli import guess_doc_type
from qai_xml2ir.egov_parser import parse_egov_xml


def test_parse_egov_api_wrapper_uses_lawfulltext_law_metadata(tmp_path: Path) -> None:
    xml_path = tmp_path / "416M60000100179_20260501_507M60000100117.xml"
    xml_path.write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<DataRoot>
  <Result><Code>0</Code><Message/></Result>
  <ApplData>
    <LawId>416M60000100179</LawId>
    <LawNum/>
    <LawFullText>
      <Law Lang="ja">
        <LawNum>平成十六年厚生労働省令第百七十九号</LawNum>
        <LawBody>
          <LawTitle>医薬品及び医薬部外品の製造管理及び品質管理の基準に関する省令</LawTitle>
          <MainProvision>
            <Article Num="1">
              <ArticleTitle>第一条</ArticleTitle>
              <Paragraph Num="1">
                <ParagraphSentence><Sentence>本文</Sentence></ParagraphSentence>
              </Paragraph>
            </Article>
          </MainProvision>
        </LawBody>
      </Law>
    </LawFullText>
  </ApplData>
</DataRoot>
""",
        encoding="utf-8",
        newline="\n",
    )

    parsed = parse_egov_xml(xml_path)

    assert parsed.law_id == "416M60000100179"
    assert parsed.law_number == "平成十六年厚生労働省令第百七十九号"
    assert parsed.title == "医薬品及び医薬部外品の製造管理及び品質管理の基準に関する省令"
    assert guess_doc_type(parsed.law_number) == "ministerial_ordinance"
