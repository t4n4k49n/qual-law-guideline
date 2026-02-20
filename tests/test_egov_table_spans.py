from __future__ import annotations

from lxml import etree

from qai_xml2ir.egov_parser import _extract_table_payload


def test_extract_table_payload_infers_vertical_span_from_borders_and_fills_rows() -> None:
    xml = """\
<TableStruct>
  <Table>
    <TableRow>
      <TableColumn BorderBottom="none"><Sentence>第二十二条第一項</Sentence></TableColumn>
      <TableColumn><Sentence>から第二十五条まで</Sentence></TableColumn>
      <TableColumn><Sentence>及び第二十四条</Sentence></TableColumn>
    </TableRow>
    <TableRow>
      <TableColumn BorderTop="none"><Sentence/></TableColumn>
      <TableColumn><Sentence>から第二十五条まで</Sentence></TableColumn>
      <TableColumn><Sentence>及び第二十四条</Sentence></TableColumn>
    </TableRow>
  </Table>
</TableStruct>
"""
    wrapper = etree.fromstring(xml.encode("utf-8"))
    _, header_rows, data_rows, _, table_layout = _extract_table_payload(wrapper)

    assert header_rows == []
    assert len(data_rows) == 2
    assert data_rows[1] == "第二十二条第一項 | から第二十五条まで | 及び第二十四条"
    assert table_layout is not None
    cell00 = next(c for c in table_layout["cells"] if c["r"] == 0 and c["c"] == 0)
    assert cell00["text"] == "第二十二条第一項"
    assert cell00["rowspan"] == 2
    assert cell00["colspan"] == 1
    assert cell00["span_source"] == "border"


def test_extract_table_payload_handles_explicit_rowspan_without_column_shift() -> None:
    xml = """\
<TableStruct>
  <Table>
    <TableRow>
      <TableColumn rowspan="2"><Sentence>A</Sentence></TableColumn>
      <TableColumn><Sentence>B1</Sentence></TableColumn>
      <TableColumn><Sentence>C1</Sentence></TableColumn>
    </TableRow>
    <TableRow>
      <TableColumn><Sentence>B2</Sentence></TableColumn>
      <TableColumn><Sentence>C2</Sentence></TableColumn>
    </TableRow>
  </Table>
</TableStruct>
"""
    wrapper = etree.fromstring(xml.encode("utf-8"))
    _, header_rows, data_rows, _, table_layout = _extract_table_payload(wrapper)

    assert header_rows == []
    assert len(data_rows) == 2
    assert data_rows[0] == "A | B1 | C1"
    assert data_rows[1] == "A | B2 | C2"
    assert table_layout is not None
    cell00 = next(c for c in table_layout["cells"] if c["r"] == 0 and c["c"] == 0)
    assert cell00["rowspan"] == 2
    assert cell00["span_source"] == "attr"
