from __future__ import annotations

from lxml import etree

from qai_xml2ir.egov_parser import _extract_table_payload


def test_extract_table_payload_does_not_promote_data_row_for_headerless_table() -> None:
    xml = """\
<TableStruct>
  <Table>
    <TableRow>
      <TableColumn><Sentence>一　第一類医薬品</Sentence></TableColumn>
      <TableColumn><Sentence>第１類医薬品</Sentence></TableColumn>
    </TableRow>
    <TableRow>
      <TableColumn><Sentence>二　第二類医薬品</Sentence></TableColumn>
      <TableColumn><Sentence>第２類医薬品</Sentence></TableColumn>
    </TableRow>
    <TableRow>
      <TableColumn><Sentence>三　第三類医薬品</Sentence></TableColumn>
      <TableColumn><Sentence>第３類医薬品</Sentence></TableColumn>
    </TableRow>
  </Table>
</TableStruct>
"""
    wrapper = etree.fromstring(xml.encode("utf-8"))
    _, header_rows, data_rows, _ = _extract_table_payload(wrapper)

    assert header_rows == []
    assert len(data_rows) == 3
    assert data_rows[0] == "一　第一類医薬品 | 第１類医薬品"


def test_extract_table_payload_promotes_implicit_header_for_short_label_row() -> None:
    xml = """\
<TableStruct>
  <Table>
    <TableRow>
      <TableColumn><Sentence>医薬品</Sentence></TableColumn>
      <TableColumn><Sentence>使用数量</Sentence></TableColumn>
    </TableRow>
    <TableRow>
      <TableColumn><Sentence>次の要件に適合する第一類医薬品</Sentence></TableColumn>
      <TableColumn><Sentence>一日当たりの最大使用数量を遵守すること。</Sentence></TableColumn>
    </TableRow>
    <TableRow>
      <TableColumn><Sentence>指定第二類医薬品</Sentence></TableColumn>
      <TableColumn><Sentence>購入者へ情報提供を行い適正使用を確保すること。</Sentence></TableColumn>
    </TableRow>
  </Table>
</TableStruct>
"""
    wrapper = etree.fromstring(xml.encode("utf-8"))
    _, header_rows, data_rows, _ = _extract_table_payload(wrapper)

    assert header_rows == ["医薬品 | 使用数量"]
    assert len(data_rows) == 2
    assert data_rows[0].startswith("次の要件に適合する第一類医薬品 | ")
