from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Tuple

import pytest
import yaml

from qai_mock_ui.ir_model import build_doc_index
from qai_mock_ui.render import render_selected_nodes, render_text_preview

BASE_DIR = Path(
    "data/normalized/jp_egov_336M50000100002_20260501_507M60000100117"
)
IR_PATH = BASE_DIR / "jp_egov_336M50000100002_20260501_507M60000100117.regdoc_ir.yaml"
PROFILE_PATH = BASE_DIR / "jp_egov_336M50000100002_20260501_507M60000100117.regdoc_profile.yaml"


def _find_raw_node(node: Dict[str, Any], nid: str) -> Dict[str, Any] | None:
    if node.get("nid") == nid:
        return node
    for child in node.get("children") or []:
        found = _find_raw_node(child, nid)
        if found is not None:
            return found
    return None


def _load_fixture() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    regdoc_ir = yaml.safe_load(IR_PATH.read_text(encoding="utf-8"))
    regdoc_profile = yaml.safe_load(PROFILE_PATH.read_text(encoding="utf-8"))
    if not isinstance(regdoc_ir, dict) or not isinstance(regdoc_profile, dict):
        raise ValueError("fixture load failed")
    return regdoc_ir, regdoc_profile


def _apply_mock_nodes(regdoc_ir: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(regdoc_ir)
    root = data["content"]
    row1 = _find_raw_node(root, "appdx_table1.tbl1.tblh.tblr1")
    table = _find_raw_node(root, "appdx_table1.tbl1")
    header = _find_raw_node(root, "appdx_table1.tbl1.tblh")
    assert row1 and table and header

    table_children = table.setdefault("children", [])
    table_children.append(
        {
            "nid": "appdx_table1.tbl1.note1",
            "kind": "note",
            "kind_raw": "note",
            "num": None,
            "ord": row1["ord"] + 2,
            "heading": None,
            "text": "※ 表の注記（デモ用）",
            "role": "informative",
            "normativity": None,
            "tags": [],
            "refs": [],
            "source_spans": [],
            "children": [],
        }
    )
    header_children = header.setdefault("children", [])
    header_children.append(
        {
            "nid": "appdx_table1.tbl1.tblh.tblr2",
            "kind": "table_row",
            "kind_raw": "table_row",
            "num": None,
            "ord": row1["ord"] + 1,
            "heading": None,
            "text": "【2行目デモ】標識の補足説明 | 【2行目デモ】大きさの補足 | 【2行目デモ】設置箇所の補足",
            "role": "normative",
            "normativity": None,
            "tags": [],
            "refs": [],
            "source_spans": [],
            "children": [],
        }
    )
    data.setdefault("index", {}).setdefault("display_name_by_nid", {})[
        "appdx_table1.tbl1.tblh.tblr2"
    ] = "2行目"
    data.setdefault("index", {}).setdefault("display_name_by_nid", {})[
        "appdx_table1.tbl1.note1"
    ] = "注記"
    return data


def _mock_purpose(regdoc_profile: Dict[str, Any]) -> Dict[str, Any]:
    purpose = deepcopy(regdoc_profile["profiles"]["dq_gmp_checklist"])
    for rule in purpose["context_display_policy"]:
        if rule.get("when_kind") == "subitem":
            rule["include_chapeau_text"] = False
        if rule.get("when_kind") == "table_row":
            rule["include_ancestors_until_kind"] = "table"
    return purpose


def _pick_existing_nid(index, *candidates: str) -> str:
    for nid in candidates:
        if nid in index.by_nid:
            return nid
    raise AssertionError(f"none of candidate nids exists: {candidates}")


def test_requirement1_subitem_preview_only_heading_and_item() -> None:
    regdoc_ir, regdoc_profile = _load_fixture()
    index = build_doc_index(_apply_mock_nodes(regdoc_ir))
    purpose = _mock_purpose(regdoc_profile)
    ro_nid = _pick_existing_nid(index, "art12.p1.i2.ro", "art12.i2.ro")
    blocks = render_selected_nodes(index, purpose, [ro_nid])
    text = render_text_preview(blocks)
    expected = (
        "（一般区分の医薬部外品製造業者等の製造所の構造設備）\n"
        "ロ　常時居住する場所及び不潔な場所から明確に区別されていること。"
    )
    assert text == expected


def test_requirement2_sibling_context_is_omitted_for_second_item() -> None:
    regdoc_ir, regdoc_profile = _load_fixture()
    index = build_doc_index(_apply_mock_nodes(regdoc_ir))
    purpose = _mock_purpose(regdoc_profile)
    ro_nid = _pick_existing_nid(index, "art12.p1.i2.ro", "art12.i2.ro")
    ha_nid = _pick_existing_nid(index, "art12.p1.i2.ha", "art12.i2.ha")
    blocks = render_selected_nodes(index, purpose, [ro_nid, ha_nid])
    text = render_text_preview(blocks)
    assert text.count("（一般区分の医薬部外品製造業者等の製造所の構造設備）") == 1
    assert "ロ　常時居住する場所及び不潔な場所から明確に区別されていること。" in text
    assert "ハ　作業を行うのに支障のない面積を有すること。" in text


def test_requirement3_table_row_includes_title_header_note_and_row() -> None:
    regdoc_ir, regdoc_profile = _load_fixture()
    index = build_doc_index(_apply_mock_nodes(regdoc_ir))
    purpose = _mock_purpose(regdoc_profile)
    blocks = render_selected_nodes(index, purpose, ["appdx_table1.tbl1.tblh.tblr1"])
    text = render_text_preview(blocks)
    assert "別表" in text
    assert "標識 | 大きさ | 標識を付ける箇所" in text
    assert "※ 表の注記（デモ用）" in text
    assert "| 産業標準化法（昭和二十四年法律第百八十五号）" in text


def test_requirement4_second_table_row_omits_repeated_header_block() -> None:
    regdoc_ir, regdoc_profile = _load_fixture()
    index = build_doc_index(_apply_mock_nodes(regdoc_ir))
    purpose = _mock_purpose(regdoc_profile)
    blocks = render_selected_nodes(
        index, purpose, ["appdx_table1.tbl1.tblh.tblr1", "appdx_table1.tbl1.tblh.tblr2"]
    )
    text = render_text_preview(blocks)
    assert text.count("別表") == 1
    assert blocks[1].header_omitted is True
    assert text.count("※ 表の注記（デモ用）") == 1
    assert "【2行目デモ】標識の補足説明" in text


def test_first_selected_item_keeps_context_in_both_dedup_modes() -> None:
    regdoc_ir, regdoc_profile = _load_fixture()
    index = build_doc_index(_apply_mock_nodes(regdoc_ir))
    purpose = _mock_purpose(regdoc_profile)
    selected = [
        _pick_existing_nid(index, "art12.p1.i2.ro", "art12.i2.ro"),
        _pick_existing_nid(index, "art12.p1.i2.ha", "art12.i2.ha"),
    ]

    blocks_exact = render_selected_nodes(index, purpose, selected, header_dedup_mode="exact")
    blocks_prefix = render_selected_nodes(index, purpose, selected, header_dedup_mode="prefix")

    assert blocks_exact[0].header_omitted is False
    assert blocks_prefix[0].header_omitted is False
    assert "（一般区分の医薬部外品製造業者等の製造所の構造設備）" in blocks_exact[0].header_lines
    assert "（一般区分の医薬部外品製造業者等の製造所の構造設備）" in blocks_prefix[0].header_lines


def test_article_line_head_is_separated_from_heading_text() -> None:
    regdoc_ir, regdoc_profile = _load_fixture()
    index = build_doc_index(_apply_mock_nodes(regdoc_ir))
    purpose = _mock_purpose(regdoc_profile)
    blocks = render_selected_nodes(index, purpose, ["art1.p1"])

    assert blocks
    headers = blocks[0].header_lines
    assert "（薬局の構造設備）" in headers
    assert "第一条" in headers
    assert "第一条 （薬局の構造設備）" not in headers


def test_egov_merge_off_keeps_article_and_paragraph1_separated() -> None:
    regdoc_ir, regdoc_profile = _load_fixture()
    index = build_doc_index(_apply_mock_nodes(regdoc_ir))
    purpose = _mock_purpose(regdoc_profile)

    blocks = render_selected_nodes(
        index,
        purpose,
        ["art1.p1"],
        render_options={"egov_merge_article_p1": False},
    )
    assert blocks
    assert "第一条" in blocks[0].header_lines
    assert any(line.startswith("1　") for line in blocks[0].item_lines)
    assert not any(line.startswith("第一条　") for line in blocks[0].item_lines)


def test_egov_merge_on_merges_article_and_paragraph1() -> None:
    regdoc_ir, regdoc_profile = _load_fixture()
    index = build_doc_index(_apply_mock_nodes(regdoc_ir))
    purpose = _mock_purpose(regdoc_profile)

    blocks = render_selected_nodes(
        index,
        purpose,
        ["art1.p1"],
        render_options={"egov_merge_article_p1": True},
    )
    assert blocks
    assert not any(line == "第一条" for line in blocks[0].header_lines)
    assert any(line.startswith("第一条　薬局の構造設備の基準は、次のとおりとする。") for line in blocks[0].item_lines)


def test_egov_merge_is_consistent_between_selected_and_ancestor_rendering() -> None:
    regdoc_ir, regdoc_profile = _load_fixture()
    index = build_doc_index(_apply_mock_nodes(regdoc_ir))
    purpose = _mock_purpose(regdoc_profile)

    # item 選択時に p1 をヘッダへ補う（UIモックと同じ前提）
    for rule in purpose["context_display_policy"]:
        if rule.get("when_kind") in {"item", "subitem", "statement"}:
            rule["force_article_p1_text"] = True

    p1_blocks = render_selected_nodes(
        index,
        purpose,
        ["art1.p1"],
        render_options={"egov_merge_article_p1": True},
    )
    item_blocks = render_selected_nodes(
        index,
        purpose,
        ["art1.p1.i2"],
        render_options={"egov_merge_article_p1": True},
    )

    assert p1_blocks and item_blocks
    merged_line = "第一条　薬局の構造設備の基準は、次のとおりとする。"
    assert merged_line in p1_blocks[0].item_lines
    assert merged_line in item_blocks[0].header_lines
    assert "第一条" not in item_blocks[0].header_lines


def test_prefix_dedup_uses_merged_context_chain() -> None:
    regdoc_ir, regdoc_profile = _load_fixture()
    index = build_doc_index(_apply_mock_nodes(regdoc_ir))
    purpose = _mock_purpose(regdoc_profile)
    for rule in purpose["context_display_policy"]:
        if rule.get("when_kind") in {"item", "subitem", "statement"}:
            rule["force_article_p1_text"] = True

    blocks = render_selected_nodes(
        index,
        purpose,
        ["art1.p1", "art1.p1.i2"],
        header_dedup_mode="prefix",
        render_options={"egov_merge_article_p1": True},
    )
    assert len(blocks) == 2
    # 先行 block の item に出た統合コンテキストは次 block で prefix 省略される
    assert blocks[1].header_lines == []
    assert blocks[1].header_omitted is True


def test_force_article_p1_text_precedence_against_egov_merge_option() -> None:
    regdoc_ir, regdoc_profile = _load_fixture()
    index = build_doc_index(_apply_mock_nodes(regdoc_ir))
    purpose = _mock_purpose(regdoc_profile)
    for rule in purpose["context_display_policy"]:
        if rule.get("when_kind") in {"item", "subitem", "statement"}:
            rule["force_article_p1_text"] = True

    off_blocks = render_selected_nodes(
        index,
        purpose,
        ["art1.p1.i2"],
        render_options={"egov_merge_article_p1": False},
    )
    on_blocks = render_selected_nodes(
        index,
        purpose,
        ["art1.p1.i2"],
        render_options={"egov_merge_article_p1": True},
    )

    assert off_blocks and on_blocks
    assert "1　薬局の構造設備の基準は、次のとおりとする。" in off_blocks[0].header_lines
    assert "第一条　薬局の構造設備の基準は、次のとおりとする。" not in off_blocks[0].header_lines

    assert "第一条　薬局の構造設備の基準は、次のとおりとする。" in on_blocks[0].header_lines
    assert "1　薬局の構造設備の基準は、次のとおりとする。" not in on_blocks[0].header_lines


def test_missing_nid_raises_by_default_with_p1_suggestion() -> None:
    regdoc_ir, regdoc_profile = _load_fixture()
    index = build_doc_index(_apply_mock_nodes(regdoc_ir))
    purpose = _mock_purpose(regdoc_profile)
    assert "art1.p1.i2" in index.by_nid
    assert "art1.i2" not in index.by_nid

    with pytest.raises(ValueError) as exc:
        render_selected_nodes(index, purpose, ["art1.i2"])
    msg = str(exc.value)
    assert "art1.i2" in msg
    assert "art1.p1.i2" in msg


def test_missing_nid_warn_mode_continues_with_existing_nodes(capsys: pytest.CaptureFixture[str]) -> None:
    regdoc_ir, regdoc_profile = _load_fixture()
    index = build_doc_index(_apply_mock_nodes(regdoc_ir))
    purpose = _mock_purpose(regdoc_profile)
    assert "art1.p1.i3" in index.by_nid

    blocks = render_selected_nodes(
        index,
        purpose,
        ["art1.i2", "art1.p1.i3"],
        on_missing_nids="warn",
    )
    captured = capsys.readouterr()
    assert "art1.i2" in captured.err
    assert len(blocks) == 1
    assert blocks[0].nid == "art1.p1.i3"


def test_render_templates_default_enables_egov_merge_without_render_options() -> None:
    regdoc_ir, regdoc_profile = _load_fixture()
    index = build_doc_index(_apply_mock_nodes(regdoc_ir))
    purpose = _mock_purpose(regdoc_profile)
    purpose.setdefault("render_templates", {})["egov_merge_article_p1"] = True

    blocks = render_selected_nodes(index, purpose, ["art1.p1"])
    assert blocks
    assert any(line.startswith("第一条　薬局の構造設備の基準は、次のとおりとする。") for line in blocks[0].item_lines)
