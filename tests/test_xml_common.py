from __future__ import annotations

from pathlib import Path

from qai_xml2ir.xml_common import parse_xml_document


def test_parse_xml_document_accepts_huge_text_node(tmp_path: Path) -> None:
    xml_path = tmp_path / "huge.xml"
    long_text = "A" * 10_000_100
    xml_path.write_text(f"<Root><Text>{long_text}</Text></Root>", encoding="utf-8")

    tree = parse_xml_document(xml_path)

    assert tree.getroot().findtext("Text") == long_text
