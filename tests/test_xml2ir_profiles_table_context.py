from qai_xml2ir.models_profiles import build_parser_profile, build_regdoc_profile


def test_xml2ir_parser_profile_supports_table_and_note_structure() -> None:
    profile = build_parser_profile()
    structure = profile.get("structure") or {}

    assert structure.get("table", {}).get("children") == ["table_header", "note"]
    assert structure.get("table_header", {}).get("children") == ["table_row"]
    assert structure.get("appendix", {}).get("children") == ["table", "note"]
    assert "note" in (structure.get("paragraph", {}).get("children") or [])


def test_xml2ir_regdoc_profile_supports_table_row_and_note_descendants() -> None:
    profile = build_regdoc_profile("jp_test_doc")
    checklist = profile["profiles"]["dq_gmp_checklist"]

    assert "table_row" in checklist["selectable_kinds"]
    assert {"when_kind": "table_row", "group_under_kind": "table"} in checklist["grouping_policy"]

    table_row_policy = next(
        p for p in checklist["context_display_policy"] if p.get("when_kind") == "table_row"
    )
    assert table_row_policy["include_descendants"] is True
    assert table_row_policy["include_descendants_of"] == "ancestors"
    assert table_row_policy["include_descendants_kinds"] == ["note"]

