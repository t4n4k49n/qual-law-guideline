from __future__ import annotations

from pathlib import Path

import yaml

from qai_mock_ui.candidate_visibility import build_candidate_visibility_map
from qai_mock_ui.ir_model import build_doc_index
from qai_text2ir import cli
from qai_text2ir.candidate_visibility_profiles import (
    apply_candidate_visibility_profile,
    load_candidate_visibility_profile,
)


PROFILE_IDS = [
    "jp_pmda_api_gmp_guideline_visibility_v1",
    "jp_pmda_aseptic_processing_guideline_visibility_v1",
    "jp_niid_pathogen_safety_management_visibility_v1",
    "jp_mhlw_csv_guideline_visibility_v1",
]


def _node(nid: str, kind: str, children: list[dict] | None = None) -> dict:
    return {
        "nid": nid,
        "kind": kind,
        "num": None,
        "ord": 1,
        "heading": None,
        "text": None,
        "children": children or [],
    }


def _visibility_for(profile_id: str) -> dict[str, bool]:
    regdoc_profile = cli._build_regdoc_profile("candidate_visibility_sample", context_root_kind="chapter")
    profile = load_candidate_visibility_profile(profile_id=profile_id)
    regdoc_profile = apply_candidate_visibility_profile(regdoc_profile, profile)
    purpose = regdoc_profile["profiles"]["dq_gmp_checklist"]
    regdoc_ir = {
        "content": _node(
            "root",
            "document",
            [
                _node("cha1", "chapter", [_node("cha1.p1_1", "paragraph"), _node("cha1.p1_3", "paragraph")]),
                _node("cha1.p1_3.tbl1", "table", [_node("cha1.p1_3.tbl1.tblh1", "table_header", [_node("cha1.p1_3.tbl1.tblh1.tblr1", "table_row")])]),
                _node("cha2", "chapter", [_node("cha2.p2_1", "paragraph")]),
                _node("cha3", "chapter", [_node("cha3.p3_1", "paragraph")]),
                _node("cha5", "chapter", [_node("cha5.p40", "paragraph")]),
                _node("cha6", "chapter", [_node("cha6.p42", "paragraph")]),
                _node("cha10", "chapter", [_node("cha10.p10_1", "paragraph")]),
                _node("cha20", "chapter", [_node("cha20.p20_1", "paragraph")]),
            ],
        )
    }
    return build_candidate_visibility_map(build_doc_index(regdoc_ir), purpose)


def test_candidate_visibility_profiles_are_loadable() -> None:
    for profile_id in PROFILE_IDS:
        profile = load_candidate_visibility_profile(profile_id=profile_id)
        assert profile["id"] == profile_id
        assert profile["candidate_visibility"]["deny_rules"]


def test_api_gmp_visibility_hides_terms_and_table1() -> None:
    visible = _visibility_for("jp_pmda_api_gmp_guideline_visibility_v1")

    assert visible["cha3"] is True
    assert visible["cha20"] is False
    assert visible["cha20.p20_1"] is False
    assert visible["cha1.p1_3.tbl1"] is False
    assert visible["cha1.p1_3.tbl1.tblh1.tblr1"] is False


def test_aseptic_visibility_hides_intro_and_terms() -> None:
    visible = _visibility_for("jp_pmda_aseptic_processing_guideline_visibility_v1")

    assert visible["cha1"] is False
    assert visible["cha2.p2_1"] is False
    assert visible["cha3.p3_1"] is True


def test_niid_visibility_hides_target_out_chapters() -> None:
    visible = _visibility_for("jp_niid_pathogen_safety_management_visibility_v1")

    assert visible["cha1.p1_1"] is False
    assert visible["cha5.p40"] is False
    assert visible["cha6.p42"] is False
    assert visible["cha3.p3_1"] is True


def test_csv_visibility_hides_target_out_sections_and_terms() -> None:
    visible = _visibility_for("jp_mhlw_csv_guideline_visibility_v1")

    assert visible["cha1.p1_1"] is False
    assert visible["cha1.p1_3"] is True
    assert visible["cha10.p10_1"] is False


def test_text2ir_bundle_can_apply_candidate_visibility_profile(tmp_path: Path) -> None:
    input_path = tmp_path / "csv_excerpt.txt"
    input_path.write_text(
        "\n".join(["1．総則", "1．1 目的", "本文", "1．3 カテゴリ分類", "本文"]) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    out_dir = tmp_path / "bundle"

    cli.bundle(
        input=input_path,
        out_dir=out_dir,
        doc_id="jp_mhlw_csv_guideline_excerpt",
        title="CSVガイドライン抜粋",
        short_title="CSVガイドライン",
        doc_type="guideline",
        source_format="txt",
        retrieved_at="2026-05-23",
        jurisdiction="JP",
        language="ja",
        family="JP_GUIDELINE",
        parser_profile_id="jp_mhlw_csv_guideline_v1",
        candidate_visibility_profile_id="jp_mhlw_csv_guideline_visibility_v1",
        emit_only="all",
    )

    regdoc_profile = yaml.safe_load((out_dir / "jp_mhlw_csv_guideline_excerpt.regdoc_profile.yaml").read_text(encoding="utf-8"))
    visibility = regdoc_profile["profiles"]["dq_gmp_checklist"]["candidate_visibility"]
    assert {"nid_prefix": "cha1.p1_1", "reason": "1.1は対象外OK範囲として候補表示から除外する"} in visibility["deny_rules"]
