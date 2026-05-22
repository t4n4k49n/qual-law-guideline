from __future__ import annotations

from pathlib import Path

from qai_text2ir import cli
from qai_text2ir.audit_report import collect_run_summary, render_markdown


def _bundle(run_dir: Path, doc_id: str, text: str) -> None:
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
        retrieved_at="2026-05-22",
        emit_only="all",
    )


def test_audit_report_collects_multiple_bundles(tmp_path: Path) -> None:
    run_dir = tmp_path / "run_out"
    run_dir.mkdir()
    _bundle(run_dir, "doc_a", "1. Scope\n1.1 First requirement.")
    _bundle(run_dir, "doc_b", "1. Scope\n1.1 Second requirement.\n1.2 Third requirement.")

    summary = collect_run_summary(run_dir)

    assert summary["document_count"] == 2
    assert summary["totals"]["goal_pass"] == 2
    assert summary["totals"]["goal_fail"] == 0
    assert summary["totals"]["nodes"] > 0
    assert {doc["doc_id"] for doc in summary["documents"]} == {"doc_a", "doc_b"}
    assert all(doc["four_files"] for doc in summary["documents"])
    assert all(doc["manifest"] for doc in summary["documents"])
    assert all(doc["source_spans"]["coverage"] > 0 for doc in summary["documents"])
    assert all(doc["meta_family"] == "TEST" for doc in summary["documents"])
    assert all(doc["promotion_goal_check"] == "pass" for doc in summary["documents"])
    assert all(doc["remaining_gap"] == "none" for doc in summary["documents"])


def test_audit_report_renders_markdown(tmp_path: Path) -> None:
    run_dir = tmp_path / "run_out"
    run_dir.mkdir()
    _bundle(run_dir, "doc_a", "1. Scope\n1.1 First requirement.")

    markdown = render_markdown(collect_run_summary(run_dir))

    assert "# TEXT2IR AUDIT REPORT" in markdown
    assert "| doc_a | pass | pass |" in markdown
