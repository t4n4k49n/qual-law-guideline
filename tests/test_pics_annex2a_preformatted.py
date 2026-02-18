from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir


def _flatten(node: Dict) -> List[Dict]:
    out = [node]
    for child in node.get("children", []):
        out.extend(_flatten(child))
    return out


def test_figure_block_keeps_arrow_newlines(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "ANNEX 2A",
            "MANUFACTURE OF ADVANCED THERAPY MEDICINAL",
            "PRODUCTS FOR HUMAN USE",
            "",
            "SCOPE",
            "Figure 3: Example of autologous CAR-T therapy ATMP manufacturing",
            "    Donation",
            "↓",
            "    Transduction",
            "",
            "PRINCIPLE",
            "B3.3   During the life cycle of the product where devices are incorporated.",
        ]
    )
    input_path = tmp_path / "pics_annex2a_preformatted_figure.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")

    profile = load_parser_profile(
        path=Path("src/qai_text2ir/profiles/pics_annex2a_default_v1.yaml")
    )
    ir = parse_text_to_ir(
        input_path=input_path,
        doc_id="pics_annex2a_preformatted_figure",
        parser_profile=profile,
    ).to_dict()

    nodes = _flatten(ir["content"])
    all_text = "\n".join((n.get("text") or "") for n in nodes)
    assert "\n↓\n" in all_text
