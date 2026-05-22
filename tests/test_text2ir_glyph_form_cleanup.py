from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from qai_text2ir.glyph_sanitizer import contains_private_use, normalize_marker_glyph, pua_codepoints
from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir


def _flatten(node: Dict) -> List[Dict]:
    out = [node]
    for child in node.get("children", []):
        out.extend(_flatten(child))
    return out


def test_pua_marker_is_normalized_for_marker_matching() -> None:
    assert normalize_marker_glyph("\uf0b7 Procedure") == "• Procedure"
    assert pua_codepoints("\uf0b7 \uec1e") == ["U+EC1E", "U+F0B7"]
    assert contains_private_use("\uec1e")


def test_who_lbm_form_artifact_is_separated_and_sanitized(tmp_path: Path) -> None:
    input_path = tmp_path / "who_form.txt"
    input_path.write_text(
        "\n".join(
            [
                "8. Laboratory biosecurity and risk assessment",
                "5. Laboratory biosafety concepts: The manual emphasizes current biosafety practice. Table 5. Basic Laboratory - Biosafety Level 1: laboratory safety survey",
                "CHECKED ITEM (ENTER DATE OF CHECK)       YES       NO       N/A       COMMENTS",
                "Information on sign accurate and current .............................................. \uec1e \uec1e \uec1e",
                "Sign legible and not defaced ............. \uec1e \uec1e \uec1e",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )
    profile = load_parser_profile(path=Path("src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml"))

    ir = parse_text_to_ir(input_path=input_path, doc_id="who_form", parser_profile=profile).to_dict()
    nodes = _flatten(ir["content"])
    all_text = "\n".join(str(n.get("text") or "") for n in nodes)

    assert "\uec1e" not in all_text
    assert "................................" not in all_text
    assert "The manual emphasizes current biosafety practice." in all_text
    artifact_nodes = [n for n in nodes if n.get("kind_raw") == "form_artifact"]
    assert artifact_nodes
    assert all("not_selectable" in (n.get("tags") or []) for n in artifact_nodes)
    assert any("Information on sign accurate and current" in (n.get("text") or "") for n in artifact_nodes)


def test_pics_private_use_bullet_does_not_leak_to_yaml(tmp_path: Path) -> None:
    input_path = tmp_path / "pics_bullet.txt"
    input_path.write_text(
        "\n".join(
            [
                "ANNEX 2A",
                "SCOPE",
                "\uf0b7 The manufacturer should maintain contamination controls.",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )
    profile = load_parser_profile(path=Path("src/qai_text2ir/profiles/pics_annex2a_default_v1.yaml"))

    ir = parse_text_to_ir(input_path=input_path, doc_id="pics_bullet", parser_profile=profile).to_dict()
    rendered_values = "\n".join(str(n.get("text") or "") + str(n.get("kind_raw") or "") for n in _flatten(ir["content"]))

    assert "\uf0b7" not in rendered_values
    assert "contamination controls" in rendered_values
