from __future__ import annotations

from lxml import etree

from qai_xml2ir.egov_parser import _extract_table_payload, clean_extracted_text


def test_clean_extracted_text_collapses_ascii_xml_indentation_only() -> None:
    assert clean_extracted_text("次のいずれか\n      一\u3000略名\n      二\u3000商標") == "次のいずれか 一\u3000略名 二\u3000商標"


def test_table_payload_collapses_cell_indentation() -> None:
    xml = """\
<TableStruct>
  <Table>
    <TableRow>
      <TableColumn>
        <Sentence>次のいずれか
          一　略名
          二　商標</Sentence>
      </TableColumn>
      <TableColumn><Sentence>値</Sentence></TableColumn>
    </TableRow>
  </Table>
</TableStruct>
"""
    wrapper = etree.fromstring(xml.encode("utf-8"))

    _, _, data_rows, _, _ = _extract_table_payload(wrapper)

    assert data_rows == ["次のいずれか 一\u3000略名 二\u3000商標 | 値"]
