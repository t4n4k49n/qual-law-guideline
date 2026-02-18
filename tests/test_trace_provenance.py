from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from qai_text2ir.profile_loader import load_parser_profile_with_provenance
from qai_text2ir.text_parser import parse_text_to_ir


def _write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def test_load_profile_with_provenance_collects_extends_chain(tmp_path: Path) -> None:
    _write(
        tmp_path / "base.yaml",
        "\n".join(
            [
                "schema: qai.parser_profile.v1",
                "id: base",
                "preprocess:",
                "  drop_line_regexes:",
                "    - '^A$'",
            ]
        )
        + "\n",
    )
    _write(
        tmp_path / "child.yaml",
        "\n".join(
            [
                "schema: qai.parser_profile.v1",
                "id: child",
                "extends: base",
                "preprocess:",
                "  drop_line_regexes:",
                "    - '^B$'",
            ]
        )
        + "\n",
    )

    resolved, provenance = load_parser_profile_with_provenance(
        profile_id="child",
        profiles_dir_override=tmp_path,
    )

    assert "extends" not in resolved
    assert len(provenance) == 2
    assert provenance[0]["profile_id"] == "base"
    assert provenance[1]["profile_id"] == "child"
    assert provenance[0]["sha256"]
    assert provenance[1]["sha256"]


def test_refine_subtrees_tags_record_dispatch_and_fallback(tmp_path: Path) -> None:
    _write(
        tmp_path / "top.yaml",
        "\n".join(
            [
                "schema: qai.parser_profile.v1",
                "id: top",
                "context_root_kind: annex",
                "structural_kinds: [annex]",
                "marker_types:",
                "  - id: annex",
                "    kind: annex",
                "    kind_raw: ANNEX",
                "    match: '^ANNEX\\s+(?P<n>\\d+[A-Z]?)\\b(?:\\s+|$)'",
                "    num_group: n",
                "structure:",
                "  root:",
                "    children: [annex]",
                "  annex:",
                "    children: [note, history]",
                "  note:",
                "    children: []",
                "  history:",
                "    children: []",
                "postprocess:",
                "  refine_subtrees:",
                "    enabled: true",
                "    kind: annex",
                "    key: num",
                "    dispatch_by_num:",
                "      '15': dispatch_profile",
                "    fallback_profile_id: fallback_profile",
                "    keep_unmapped: true",
            ]
        )
        + "\n",
    )
    _write(
        tmp_path / "dispatch_profile.yaml",
        "\n".join(
            [
                "schema: qai.parser_profile.v1",
                "id: dispatch_profile",
                "context_root_kind: annex",
                "structural_kinds: [annex]",
                "marker_types:",
                "  - id: annex",
                "    kind: annex",
                "    kind_raw: ANNEX",
                "    match: '^ANNEX\\s+(?P<n>\\d+[A-Z]?)\\b(?:\\s+|$)'",
                "    num_group: n",
                "structure:",
                "  root:",
                "    children: [annex]",
                "  annex:",
                "    children: [note, history]",
                "  note:",
                "    children: []",
                "  history:",
                "    children: []",
            ]
        )
        + "\n",
    )
    _write(
        tmp_path / "fallback_profile.yaml",
        "\n".join(
            [
                "schema: qai.parser_profile.v1",
                "id: fallback_profile",
                "context_root_kind: annex",
                "structural_kinds: [annex]",
                "marker_types:",
                "  - id: annex",
                "    kind: annex",
                "    kind_raw: ANNEX",
                "    match: '^ANNEX\\s+(?P<n>\\d+[A-Z]?)\\b(?:\\s+|$)'",
                "    num_group: n",
                "structure:",
                "  root:",
                "    children: [annex]",
                "  annex:",
                "    children: [note, history]",
                "  note:",
                "    children: []",
                "  history:",
                "    children: []",
            ]
        )
        + "\n",
    )
    input_path = tmp_path / "input.txt"
    _write(
        input_path,
        "\n".join(
            [
                "ANNEX 15",
                "DISPATCH TITLE",
                "Some text",
                "ANNEX 3",
                "FALLBACK TITLE",
                "Some text",
            ]
        )
        + "\n",
    )

    profile, _ = load_parser_profile_with_provenance(
        profile_id="top",
        profiles_dir_override=tmp_path,
    )
    doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="trace_refine_tags",
        parser_profile=profile,
        profiles_dir_override=tmp_path,
    ).to_dict()

    annexes: List[Dict] = [n for n in doc["content"]["children"] if n.get("kind") == "annex"]
    ann15 = next(n for n in annexes if n.get("num") == "15")
    ann3 = next(n for n in annexes if n.get("num") == "3")

    assert "refined_by=dispatch_profile" in ann15.get("tags", [])
    assert "refine_kind=annex" in ann15.get("tags", [])
    assert "refine_key=15" in ann15.get("tags", [])

    assert "refined_by=fallback_profile" in ann3.get("tags", [])
    assert "refine_kind=annex" in ann3.get("tags", [])
    assert "refine_key=3" in ann3.get("tags", [])
