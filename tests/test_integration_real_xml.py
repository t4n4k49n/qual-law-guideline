from __future__ import annotations

import os
from pathlib import Path

import pytest
import yaml
from typer.testing import CliRunner

from qai_xml2ir.cli import app
from qai_xml2ir.verify import (
    assert_unique_nids,
    check_annex_article_nids,
    check_appendix_scoped_indices,
    summarize_kinds,
)


def _load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _sample_paths() -> list[Path]:
    paths = []
    for key in ("EGOV_XML_SAMPLE_1", "EGOV_XML_SAMPLE_2", "EGOV_XML_SAMPLE_3"):
        value = os.environ.get(key)
        if value:
            paths.append(Path(value))
    return paths


@pytest.mark.integration
def test_integration_real_xml(tmp_path: Path) -> None:
    xml_paths = _sample_paths()
    if not xml_paths:
        pytest.skip("No EGOV_XML_SAMPLE_* environment variables provided.")

    runner = CliRunner()
    for idx, xml_path in enumerate(xml_paths, start=1):
        if not xml_path.exists():
            pytest.skip(f"Missing sample XML: {xml_path}")

        out_dir = tmp_path / "out" / f"doc{idx}"
        doc_id = f"jp_test_doc_{idx}"
        result = runner.invoke(
            app,
            [
                "--input",
                str(xml_path),
                "--out-dir",
                str(out_dir),
                "--doc-id",
                doc_id,
                "--emit-only",
                "all",
            ],
        )
        assert result.exit_code == 0, result.output

        ir_path = out_dir / f"{doc_id}.regdoc_ir.yaml"
        parser_profile_path = out_dir / f"{doc_id}.parser_profile.yaml"
        regdoc_profile_path = out_dir / f"{doc_id}.regdoc_profile.yaml"
        meta_path = out_dir / f"{doc_id}.meta.yaml"

        assert ir_path.exists()
        assert parser_profile_path.exists()
        assert regdoc_profile_path.exists()
        assert meta_path.exists()

        ir = _load_yaml(ir_path)
        assert ir.get("schema")
        assert ir.get("doc_id")
        root = ir.get("content")
        assert root is not None

        assert_unique_nids(root)
        kinds = summarize_kinds(root)
        assert kinds.get("article", 0) >= 1

        collisions, invalid_annex = check_annex_article_nids(root)
        assert not collisions
        assert not invalid_annex

        appendix_problems = check_appendix_scoped_indices(root)
        assert not appendix_problems

        meta = _load_yaml(meta_path)
        assert meta["bundle"]["ir"]["path"] == ir_path.name
        assert meta["bundle"]["parser_profile"]["path"] == parser_profile_path.name
        assert meta["bundle"]["regdoc_profile"]["path"] == regdoc_profile_path.name
