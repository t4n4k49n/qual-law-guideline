from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from qai_text2ir import cli
from qai_text2ir.goal_check import check_bundle
from qai_text2ir.special_structure_audit import app, audit_bundle, audit_source_text, collect_run_audit, render_markdown


def _bundle(run_dir: Path, doc_id: str, text: str) -> Path:
    input_path = run_dir / f"{doc_id}.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")
    out_dir = run_dir / doc_id
    cli.bundle(
        input=input_path,
        out_dir=out_dir,
        doc_id=doc_id,
        title=f"{doc_id} title",
        short_title=doc_id,
        jurisdiction="TEST",
        language="en",
        family="TEST",
        source_url=f"https://example.test/{doc_id}",
        retrieved_at="2026-05-23",
        emit_only="all",
    )
    return out_dir


def test_audit_source_text_detects_required_source_signals() -> None:
    result = audit_source_text(
        "\n".join(
            [
                "Table 1: Cleanroom limits",
                "Grade    Rest      Operation",
                "A        3520      3520",
                "Figure 2. Process flow",
                "CHECKED ITEM",
                "YES NO N/A COMMENTS",
            ]
        ),
        source_path="sample.txt",
    )

    assert result["table_captions"][0]["key"] == "table 1"
    assert result["figure_captions"][0]["key"] == "figure 2"
    assert len(result["checklist_headers"]) == 2
    assert len(result["fixed_width_blocks"]) == 1


def test_special_structure_audit_flags_table_caption_left_without_table_node(tmp_path: Path) -> None:
    run_dir = tmp_path / "run_out"
    run_dir.mkdir()
    bundle_dir = _bundle(
        run_dir,
        "who_lbm_3rd_fixture",
        "\n".join(
            [
                "1. Scope",
                "Table 1: Example table",
                "Column A  Column B  Column C",
                "Alpha     Beta      Gamma",
            ]
        ),
    )

    result = audit_bundle(bundle_dir, "who_lbm_3rd_fixture", mode="promotion")

    assert result["source_tables"] == 1
    assert result["generated_tables"] == 0
    assert result["unresolved_count"] >= 1
    assert result["status"] == "fail"


def test_goal_check_promotion_fails_on_unresolved_special_structure(tmp_path: Path) -> None:
    run_dir = tmp_path / "run_out"
    run_dir.mkdir()
    bundle_dir = _bundle(
        run_dir,
        "pics_annex1_fixture",
        "1. Scope\nTable 2: Limits\nGrade  Sample  Limit\nA      Daily   1\n",
    )

    normal = check_bundle(bundle_dir, "pics_annex1_fixture")
    promotion = check_bundle(bundle_dir, "pics_annex1_fixture", mode="promotion")

    assert normal.passed
    assert any(w.code == "special_structure_unresolved" for w in normal.warnings)
    assert not promotion.passed
    assert any(e.code == "special_structure_unresolved" for e in promotion.errors)


def test_special_structure_audit_reports_checklist_text_in_human_visible_ir(tmp_path: Path) -> None:
    run_dir = tmp_path / "run_out"
    run_dir.mkdir()
    bundle_dir = _bundle(
        run_dir,
        "who_lbm_chap8_fixture",
        "8. Checklist\nCHECKED ITEM\nYES NO N/A COMMENTS\nQualification status ....\n",
    )

    result = audit_bundle(bundle_dir, "who_lbm_chap8_fixture", mode="release")

    assert result["source_checklist_headers"] == 2
    assert result["status"] == "fail"
    assert any("checklist" in item["trigger"] for item in result["unresolved_special_blocks"])


def test_special_structure_audit_cli_writes_required_files(tmp_path: Path) -> None:
    run_dir = tmp_path / "run_out"
    report_dir = tmp_path / "report"
    run_dir.mkdir()
    _bundle(run_dir, "pics_part2_fixture", "1. Scope\nFigure 1: Flow\nStart  Step  End\nA      B     C\n")

    result = CliRunner().invoke(app, ["--run-out-dir", str(run_dir), "--mode", "normal", "--out-dir", str(report_dir)])

    assert result.exit_code == 0
    data = json.loads((report_dir / "SPECIAL_STRUCTURE_AUDIT.json").read_text(encoding="utf-8"))
    markdown = (report_dir / "SPECIAL_STRUCTURE_AUDIT.md").read_text(encoding="utf-8")
    assert data["document_count"] == 1
    assert "| doc_id | source_tables | source_figures | generated_tables |" in markdown


def test_special_structure_audit_markdown_includes_required_unresolved_columns(tmp_path: Path) -> None:
    run_dir = tmp_path / "run_out"
    run_dir.mkdir()
    _bundle(run_dir, "pics_annex2a_fixture", "1. Scope\nTable 1: Cells\nA  B  C\nD  E  F\n")

    markdown = render_markdown(collect_run_audit(run_dir, mode="promotion"))

    assert "recommended_resolution" in markdown
    assert "targeted_parser" in markdown
