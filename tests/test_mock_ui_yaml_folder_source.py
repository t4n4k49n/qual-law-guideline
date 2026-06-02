import sys
import types

import pytest


streamlit_stub = types.ModuleType("streamlit")
streamlit_components_stub = types.ModuleType("streamlit.components")
streamlit_components_v1_stub = types.ModuleType("streamlit.components.v1")
streamlit_stub.session_state = {}
streamlit_stub.components = streamlit_components_stub
streamlit_components_stub.v1 = streamlit_components_v1_stub
sys.modules.setdefault("streamlit", streamlit_stub)
sys.modules.setdefault("streamlit.components", streamlit_components_stub)
sys.modules.setdefault("streamlit.components.v1", streamlit_components_v1_stub)

from apps.mock_gmp_checklist_ui import (
    SOURCE_MODE_FOLDER,
    SOURCE_MODE_YAML_FOLDER,
    _display_preset_label,
    _display_preset_signature,
    _single_yaml_bundle_in_folder,
    _validate_and_store_yaml_folder_selection,
)


def _write_bundle(folder, prefix: str = "sample") -> None:
    for suffix in [
        ".regdoc_ir.yaml",
        ".parser_profile.yaml",
        ".regdoc_profile.yaml",
        ".meta.yaml",
    ]:
        (folder / f"{prefix}{suffix}").write_text("doc: {}\n", encoding="utf-8")


def test_single_yaml_bundle_in_folder_accepts_exactly_one_bundle(tmp_path) -> None:
    _write_bundle(tmp_path, "law_a")

    ir_path, parser_path, profile_path, meta_path = _single_yaml_bundle_in_folder(tmp_path)

    assert ir_path.name == "law_a.regdoc_ir.yaml"
    assert parser_path.name == "law_a.parser_profile.yaml"
    assert profile_path.name == "law_a.regdoc_profile.yaml"
    assert meta_path.name == "law_a.meta.yaml"


def test_single_yaml_bundle_in_folder_rejects_missing_yaml(tmp_path) -> None:
    _write_bundle(tmp_path, "law_a")
    (tmp_path / "law_a.meta.yaml").unlink()

    with pytest.raises(ValueError, match="揃っていません"):
        _single_yaml_bundle_in_folder(tmp_path)


def test_single_yaml_bundle_in_folder_rejects_multiple_sets(tmp_path) -> None:
    _write_bundle(tmp_path, "law_a")
    _write_bundle(tmp_path, "law_b")

    with pytest.raises(ValueError, match="複数"):
        _single_yaml_bundle_in_folder(tmp_path)


def test_single_yaml_bundle_in_folder_rejects_mismatched_prefix(tmp_path) -> None:
    _write_bundle(tmp_path, "law_a")
    (tmp_path / "law_a.meta.yaml").rename(tmp_path / "law_b.meta.yaml")

    with pytest.raises(ValueError, match="prefix"):
        _single_yaml_bundle_in_folder(tmp_path)


def test_validate_yaml_folder_selection_stores_only_valid_folder(tmp_path) -> None:
    streamlit_stub.session_state.clear()
    _write_bundle(tmp_path, "law_a")

    accepted = _validate_and_store_yaml_folder_selection(
        str(tmp_path), SOURCE_MODE_FOLDER, None
    )

    assert accepted is True
    assert streamlit_stub.session_state["source_mode_key"] == SOURCE_MODE_YAML_FOLDER
    assert streamlit_stub.session_state["yaml_folder_source_selected_path"] == str(tmp_path)


def test_validate_yaml_folder_selection_restores_previous_state_on_invalid_folder(tmp_path) -> None:
    streamlit_stub.session_state.clear()
    previous_path = "out/valid-yaml-folder"

    accepted = _validate_and_store_yaml_folder_selection(
        str(tmp_path), SOURCE_MODE_YAML_FOLDER, previous_path
    )

    assert accepted is False
    assert streamlit_stub.session_state["source_mode_key"] == SOURCE_MODE_YAML_FOLDER
    assert streamlit_stub.session_state["confirmed_source_mode_key"] == SOURCE_MODE_YAML_FOLDER
    assert streamlit_stub.session_state["yaml_folder_source_selected_path"] == previous_path
    assert "上手く選択されませんでした" in streamlit_stub.session_state["yaml_folder_source_warning"]


def test_validate_yaml_folder_selection_restores_folder_mode_on_cancel() -> None:
    streamlit_stub.session_state.clear()

    accepted = _validate_and_store_yaml_folder_selection(None, SOURCE_MODE_FOLDER, None)

    assert accepted is False
    assert streamlit_stub.session_state["source_mode_key"] == SOURCE_MODE_FOLDER
    assert streamlit_stub.session_state["confirmed_source_mode_key"] == SOURCE_MODE_FOLDER
    assert "yaml_folder_source_selected_path" not in streamlit_stub.session_state


def test_display_preset_signature_normalizes_selected_nids_order() -> None:
    left = _display_preset_signature(
        SOURCE_MODE_FOLDER,
        "law_a",
        None,
        "オリジナル",
        ["tblr3", "tblr1"],
    )
    right = _display_preset_signature(
        SOURCE_MODE_FOLDER,
        "law_a",
        "",
        "オリジナル",
        ["tblr1", "tblr3"],
    )

    assert left == right


def test_display_preset_signature_ignores_display_customization() -> None:
    signature = _display_preset_signature(
        SOURCE_MODE_FOLDER,
        "law_a",
        None,
        "オリジナル",
        ["tblr1"],
    )

    assert "dedup_mode_label" not in signature
    assert "egov_merge_article_p1" not in signature


def test_display_preset_label_uses_display_name_and_title() -> None:
    label = _display_preset_label(
        "example4",
        {"display_name": "表示例4", "display_title": "表の1行目と3行目"},
    )

    assert label == "表示例4：表の1行目と3行目"
