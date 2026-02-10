from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import yaml

from qai_text2ir import cli
from qai_xml2ir.verify import verify_document


def _flatten(node: Dict) -> List[Dict]:
    out = [node]
    for child in node.get("children", []):
        out.extend(_flatten(child))
    return out


def test_text2ir_bundle_outputs_and_structure(tmp_path: Path) -> None:
    fixture = Path("tests/fixtures/CFR_PART11_SubpartA.txt")
    input_path = tmp_path / fixture.name
    input_path.write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")

    out_dir = tmp_path / "out"
    doc_id = "us_cfr_21_part_11_subpart_a"
    cli.bundle(
        input=input_path,
        out_dir=out_dir,
        doc_id=doc_id,
        title="21 CFR Part 11",
        short_title="CFR Part 11",
        cfr_title="21",
        cfr_part="11",
        source_url="https://www.ecfr.gov/current/title-21/part-11",
        retrieved_at="2026-02-10",
        emit_only="all",
    )

    ir_path = out_dir / f"{doc_id}.regdoc_ir.yaml"
    parser_profile_path = out_dir / f"{doc_id}.parser_profile.yaml"
    regdoc_profile_path = out_dir / f"{doc_id}.regdoc_profile.yaml"
    meta_path = out_dir / f"{doc_id}.meta.yaml"

    assert ir_path.exists()
    assert parser_profile_path.exists()
    assert regdoc_profile_path.exists()
    assert meta_path.exists()

    ir = yaml.safe_load(ir_path.read_text(encoding="utf-8"))
    parser_profile = yaml.safe_load(parser_profile_path.read_text(encoding="utf-8"))
    regdoc_profile = yaml.safe_load(regdoc_profile_path.read_text(encoding="utf-8"))
    meta = yaml.safe_load(meta_path.read_text(encoding="utf-8"))

    verify_document(ir)

    assert parser_profile["id"] == "us_cfr_default_v1"
    assert regdoc_profile["profiles"]["dq_gmp_checklist"]["context_display_policy"][0]["include_ancestors_until_kind"] == "section"
    assert meta["doc"]["identifiers"]["cfr_title"] == "21"
    assert meta["doc"]["identifiers"]["cfr_part"] == "11"
    assert meta["doc"]["sources"][0]["format"] == "txt"

    nodes = _flatten(ir["content"])
    kinds = [n["kind"] for n in nodes]
    assert "part" in kinds
    assert "subpart" in kinds
    assert "section" in kinds

    paragraph = next(n for n in nodes if n["kind"] == "paragraph")
    item = next(n for n in nodes if n["kind"] == "item")
    subitem = next(n for n in nodes if n["kind"] == "subitem")

    assert item["nid"].startswith(paragraph["nid"])
    assert subitem["nid"].startswith(item["nid"])
    assert "This part applies to records in electronic form." in subitem["text"]
    assert "Continuation text for the same clause." in subitem["text"]
    assert any(span.get("locator") == "line:4" for span in subitem["source_spans"])
    assert any(span.get("locator") == "line:5" for span in subitem["source_spans"])

