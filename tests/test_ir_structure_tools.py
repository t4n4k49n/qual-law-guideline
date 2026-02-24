from __future__ import annotations

from pathlib import Path

import yaml

from tools.check_ir_structure import check_file
from tools.migrate_folded_article_ir import migrate_ir


def _write_yaml(path: Path, payload: dict) -> None:
    path.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
        newline="\n",
    )


def test_check_ir_structure_detects_folded_article(tmp_path: Path) -> None:
    folded = {
        "schema": "qai.regdoc_ir.v4",
        "doc_id": "jp_test",
        "content": {
            "nid": "root",
            "kind": "document",
            "children": [
                {
                    "nid": "art1",
                    "kind": "article",
                    "text": "第一項本文",
                    "children": [
                        {
                            "nid": "art1.i1",
                            "kind": "item",
                            "text": "一号本文",
                            "children": [],
                        }
                    ],
                }
            ],
        },
    }
    path = tmp_path / "folded.regdoc_ir.yaml"
    _write_yaml(path, folded)

    problems = check_file(path)
    codes = {p.code for p in problems}
    assert {"A", "B", "C"}.issubset(codes)


def test_check_ir_structure_passes_unfolded_article(tmp_path: Path) -> None:
    unfolded = {
        "schema": "qai.regdoc_ir.v4",
        "doc_id": "jp_test",
        "content": {
            "nid": "root",
            "kind": "document",
            "children": [
                {
                    "nid": "art1",
                    "kind": "article",
                    "text": None,
                    "children": [
                        {
                            "nid": "art1.p1",
                            "kind": "paragraph",
                            "text": "第一項本文",
                            "children": [
                                {
                                    "nid": "art1.p1.i1",
                                    "kind": "item",
                                    "text": "一号本文",
                                    "children": [],
                                }
                            ],
                        }
                    ],
                }
            ],
        },
    }
    path = tmp_path / "unfolded.regdoc_ir.yaml"
    _write_yaml(path, unfolded)

    problems = check_file(path)
    assert not problems


def test_migrate_folded_article_ir_rewrites_to_p1() -> None:
    raw = {
        "schema": "qai.regdoc_ir.v4",
        "doc_id": "jp_test",
        "content": {
            "nid": "root",
            "kind": "document",
            "children": [
                {
                    "nid": "art2",
                    "kind": "article",
                    "text": "第一項本文",
                    "children": [
                        {
                            "nid": "art2.i1",
                            "kind": "item",
                            "text": "一号本文",
                            "children": [
                                {
                                    "nid": "art2.i1.ro",
                                    "kind": "subitem",
                                    "text": "ロ本文",
                                    "children": [],
                                }
                            ],
                        }
                    ],
                }
            ],
        },
        "index": {"display_name_by_nid": {"art2.i1": "一"}},
    }

    summary = migrate_ir(raw)
    assert summary.articles_migrated == 1

    art2 = raw["content"]["children"][0]
    assert art2["text"] is None
    assert len(art2["children"]) == 1
    assert art2["children"][0]["nid"] == "art2.p1"
    assert art2["children"][0]["kind"] == "paragraph"
    item = art2["children"][0]["children"][0]
    assert item["nid"] == "art2.p1.i1"
    subitem = item["children"][0]
    assert subitem["nid"] == "art2.p1.i1.ro"
    assert raw["index"] == {}
