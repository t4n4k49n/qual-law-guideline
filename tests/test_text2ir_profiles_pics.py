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


def _run_bundle(
    *,
    tmp_path: Path,
    fixture_name: str,
    profile_id: str,
    doc_id: str,
) -> Dict:
    fixture = Path("tests/fixtures") / fixture_name
    input_path = tmp_path / fixture.name
    input_path.write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")

    out_dir = tmp_path / "out"
    cli.bundle(
        input=input_path,
        out_dir=out_dir,
        doc_id=doc_id,
        title=doc_id,
        short_title=doc_id,
        parser_profile_id=profile_id,
        source_url="https://picscheme.org/",
        retrieved_at="2026-02-10",
        emit_only="all",
    )

    ir = yaml.safe_load((out_dir / f"{doc_id}.regdoc_ir.yaml").read_text(encoding="utf-8"))
    meta = yaml.safe_load((out_dir / f"{doc_id}.meta.yaml").read_text(encoding="utf-8"))
    parser_profile = yaml.safe_load((out_dir / f"{doc_id}.parser_profile.yaml").read_text(encoding="utf-8"))
    regdoc_profile = yaml.safe_load((out_dir / f"{doc_id}.regdoc_profile.yaml").read_text(encoding="utf-8"))
    return {
        "ir": ir,
        "meta": meta,
        "parser_profile": parser_profile,
        "regdoc_profile": regdoc_profile,
    }


def test_text2ir_pics_part1_profile(tmp_path: Path) -> None:
    bundled = _run_bundle(
        tmp_path=tmp_path,
        fixture_name="PICS_PE_009-17_PART-I_CHAPTER-5-9_formatted.txt",
        profile_id="pics_part1_default_v1",
        doc_id="pics_part1_ch5_9",
    )
    ir = bundled["ir"]
    verify_document(ir)

    nodes = _flatten(ir["content"])
    kinds = [n["kind"] for n in nodes]
    assert "chapter" in kinds
    assert "paragraph" in kinds
    assert "point" in kinds
    assert ir["index"]["display_name_by_nid"]
    assert bundled["parser_profile"]["id"] == "pics_part1_default_v1"
    assert bundled["regdoc_profile"]["profiles"]["dq_gmp_checklist"]["context_display_policy"][0]["include_ancestors_until_kind"] == "chapter"


def test_text2ir_pics_annex1_profile(tmp_path: Path) -> None:
    bundled = _run_bundle(
        tmp_path=tmp_path,
        fixture_name="PICS_PE_009-17_ANNEX-1.txt",
        profile_id="pics_annex1_default_v1",
        doc_id="pics_annex1",
    )
    ir = bundled["ir"]
    verify_document(ir)

    nodes = _flatten(ir["content"])
    kinds = [n["kind"] for n in nodes]
    assert "chapter" in kinds
    assert "paragraph" in kinds
    assert "item" in kinds
    assert "point" in kinds
    assert ir["index"]["display_name_by_nid"]
    assert bundled["meta"]["doc"]["jurisdiction"] == "INTL"
    assert bundled["meta"]["doc"]["language"] == "en"
    assert bundled["meta"]["doc"]["sources"][0]["label"] == "PIC/S"

