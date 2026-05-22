from __future__ import annotations

from pathlib import Path
from copy import deepcopy

import yaml

from qai_text2ir import cli
from qai_text2ir.goal_check import check_bundle, render_markdown


def _make_bundle(tmp_path: Path, doc_id: str = "goal_check_sample") -> Path:
    input_path = tmp_path / "sample.txt"
    input_path.write_text(
        "\n".join(
            [
                "1. Scope",
                "1.1 This clause is used for goal check testing.",
                "1.2 This second clause keeps ordering deterministic.",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )
    out_dir = tmp_path / "bundle"
    cli.bundle(
        input=input_path,
        out_dir=out_dir,
        doc_id=doc_id,
        title="Goal Check Sample",
        short_title="Goal Check",
        jurisdiction="TEST",
        language="en",
        family="TEST",
        source_url="https://example.test/goal-check",
        retrieved_at="2026-05-22",
        emit_only="all",
    )
    return out_dir


def test_goal_check_passes_for_complete_text2ir_bundle(tmp_path: Path) -> None:
    doc_id = "goal_check_sample"
    out_dir = _make_bundle(tmp_path, doc_id)

    result = check_bundle(out_dir, doc_id)

    assert result.passed
    assert result.summary["schema"] == "qai.regdoc_ir.v4"
    assert result.summary["files"]["ir"]["exists"] is True
    assert result.summary["verify_document"] == "pass"
    assert result.summary["source_spans"]["coverage"] > 0
    assert result.summary["dq_gmp_checklist"]["has_table_row_selectable"] is True
    assert result.summary["dq_gmp_checklist"]["has_descendant_policy"] is True
    assert result.summary["parser_profile"]["has_markers"] is True
    assert "PASS" in render_markdown(result)


def test_text2ir_bundle_writes_explicit_family_to_meta(tmp_path: Path) -> None:
    doc_id = "goal_check_family"
    out_dir = _make_bundle(tmp_path, doc_id)
    meta = yaml.safe_load((out_dir / f"{doc_id}.meta.yaml").read_text(encoding="utf-8"))

    assert meta["doc"]["family"] == "TEST"


def test_text2ir_bundle_uses_profile_family_when_family_is_omitted(tmp_path: Path) -> None:
    input_path = tmp_path / "sample.txt"
    input_path.write_text("1. Scope\n1.1 Text.", encoding="utf-8", newline="\n")
    out_dir = tmp_path / "bundle"

    cli.bundle(
        input=input_path,
        out_dir=out_dir,
        doc_id="goal_check_profile_family",
        title="Goal Check Profile Family",
        short_title="Goal Check",
        jurisdiction="TEST",
        language="en",
        parser_profile_id="markdown_table_test_v1",
        source_url="https://example.test/profile-family",
        retrieved_at="2026-05-22",
        emit_only="all",
    )

    meta = yaml.safe_load((out_dir / "goal_check_profile_family.meta.yaml").read_text(encoding="utf-8"))
    assert meta["doc"]["family"] == "TEST"


def test_goal_check_detects_wrong_schema(tmp_path: Path) -> None:
    doc_id = "goal_check_bad_schema"
    out_dir = _make_bundle(tmp_path, doc_id)
    ir_path = out_dir / f"{doc_id}.regdoc_ir.yaml"
    ir = yaml.safe_load(ir_path.read_text(encoding="utf-8"))
    ir["schema"] = "qai.regdoc_ir.v3"
    ir_path.write_text(yaml.safe_dump(ir, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")

    result = check_bundle(out_dir, doc_id)

    assert not result.passed
    assert any(error.code == "unexpected_ir_schema" for error in result.errors)


def test_goal_check_detects_duplicate_nid_and_ord(tmp_path: Path) -> None:
    doc_id = "goal_check_duplicate"
    out_dir = _make_bundle(tmp_path, doc_id)
    ir_path = out_dir / f"{doc_id}.regdoc_ir.yaml"
    ir = yaml.safe_load(ir_path.read_text(encoding="utf-8"))
    children = ir["content"]["children"]
    first = children[0]
    second = deepcopy(first)
    children.append(second)
    second["nid"] = first["nid"]
    second["ord"] = first["ord"]
    ir_path.write_text(yaml.safe_dump(ir, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")

    result = check_bundle(out_dir, doc_id)

    assert not result.passed
    assert any(error.code == "verify_document_failed" for error in result.errors)


def test_goal_check_detects_missing_dq_gmp_checklist_keys(tmp_path: Path) -> None:
    doc_id = "goal_check_bad_profile"
    out_dir = _make_bundle(tmp_path, doc_id)
    profile_path = out_dir / f"{doc_id}.regdoc_profile.yaml"
    profile = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
    profile["profiles"]["dq_gmp_checklist"].pop("candidate_visibility")
    profile_path.write_text(yaml.safe_dump(profile, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")

    result = check_bundle(out_dir, doc_id)

    assert not result.passed
    assert any(error.code == "dq_gmp_checklist_missing_keys" for error in result.errors)


def test_goal_check_warns_when_source_spans_are_missing(tmp_path: Path) -> None:
    doc_id = "goal_check_missing_spans"
    out_dir = _make_bundle(tmp_path, doc_id)
    ir_path = out_dir / f"{doc_id}.regdoc_ir.yaml"
    ir = yaml.safe_load(ir_path.read_text(encoding="utf-8"))
    first = ir["content"]["children"][0]
    first["source_spans"] = []
    ir_path.write_text(yaml.safe_dump(ir, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")

    result = check_bundle(out_dir, doc_id)

    assert result.passed
    assert any(warning.code == "missing_source_spans" for warning in result.warnings)


def test_goal_check_promotion_mode_requires_meta_family(tmp_path: Path) -> None:
    doc_id = "goal_check_missing_family"
    out_dir = _make_bundle(tmp_path, doc_id)
    meta_path = out_dir / f"{doc_id}.meta.yaml"
    meta = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
    meta["doc"].pop("family", None)
    meta_path.write_text(yaml.safe_dump(meta, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")

    normal_result = check_bundle(out_dir, doc_id)
    promotion_result = check_bundle(out_dir, doc_id, mode="promotion")

    assert normal_result.passed
    assert any(warning.code == "meta_family_missing" for warning in normal_result.warnings)
    assert not promotion_result.passed
    assert any(error.code == "meta_family_missing" for error in promotion_result.errors)


def test_goal_check_promotion_fails_on_literal_private_use_glyph(tmp_path: Path) -> None:
    doc_id = "goal_check_pua"
    out_dir = _make_bundle(tmp_path, doc_id)
    ir_path = out_dir / f"{doc_id}.regdoc_ir.yaml"
    ir = yaml.safe_load(ir_path.read_text(encoding="utf-8"))
    ir["content"]["children"][0]["text"] = "Leaked glyph \uec1e"
    ir_path.write_text(yaml.safe_dump(ir, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")

    result = check_bundle(out_dir, doc_id, mode="promotion")

    assert not result.passed
    assert any(error.code == "literal_private_use_glyph" for error in result.errors)


def test_goal_check_promotion_fails_on_visible_form_artifact(tmp_path: Path) -> None:
    doc_id = "goal_check_form"
    out_dir = _make_bundle(tmp_path, doc_id)
    ir_path = out_dir / f"{doc_id}.regdoc_ir.yaml"
    ir = yaml.safe_load(ir_path.read_text(encoding="utf-8"))
    ir["content"]["children"][0]["text"] = "Information on sign current ............. [ ] [ ] [ ] YES NO N/A COMMENTS"
    ir_path.write_text(yaml.safe_dump(ir, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")

    result = check_bundle(out_dir, doc_id, mode="promotion")

    assert not result.passed
    assert any(error.code == "severe_form_artifact_visible" for error in result.errors)
