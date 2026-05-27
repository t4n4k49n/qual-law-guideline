from __future__ import annotations

from pathlib import Path

import yaml

from tools.extract_ir_sample import find_path, main, render_markdown


def _sample_ir() -> dict:
    return {
        "schema": "qai.regdoc_ir.v4",
        "doc_id": "sample",
        "content": {
            "nid": "root",
            "kind": "document",
            "children": [
                {
                    "nid": "cha1",
                    "kind": "chapter",
                    "kind_raw": "Chapter",
                    "heading": "Pharmaceutical Quality System",
                    "children": [
                        {
                            "nid": "cha1.p1_8",
                            "kind": "paragraph",
                            "kind_raw": "1.8",
                            "text": "Paragraph text",
                            "children": [
                                {
                                    "nid": "cha1.p1_8.iiii",
                                    "kind": "item",
                                    "kind_raw": "(iii)",
                                    "text": "All necessary facilities for GMP are provided including:",
                                    "children": [
                                        {
                                            "nid": "cha1.p1_8.iiii.si3",
                                            "kind": "subitem",
                                            "kind_raw": "•",
                                            "text": "Suitable equipment and services;",
                                            "children": [],
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ],
        },
        "index": {},
    }


def test_find_path_returns_ancestor_chain() -> None:
    path = find_path(_sample_ir()["content"], "cha1.p1_8.iiii.si3")

    assert path is not None
    assert [node["nid"] for node in path] == [
        "root",
        "cha1",
        "cha1.p1_8",
        "cha1.p1_8.iiii",
        "cha1.p1_8.iiii.si3",
    ]


def test_render_markdown_preserves_review_table_shape() -> None:
    path = find_path(_sample_ir()["content"], "cha1.p1_8.iiii.si3")
    assert path is not None

    markdown = render_markdown(
        ir_path=Path("sample.regdoc_ir.yaml"),
        target_nid="cha1.p1_8.iiii.si3",
        path=path,
        blank_text_kinds={"paragraph"},
    )

    assert "| 階層 | nid | kind | kind_raw | text / heading |" in markdown
    assert "| 3 | `cha1.p1_8` | `paragraph` | `1.8` |  |" in markdown
    assert "| 4 | `cha1.p1_8.iiii` | `item` | `(iii)` | `All necessary facilities for GMP are provided including:` |" in markdown
    assert "| 5 | `cha1.p1_8.iiii.si3` | `subitem` | `•` | `Suitable equipment and services;` |" in markdown


def test_main_writes_markdown_output(tmp_path: Path) -> None:
    ir_path = tmp_path / "sample.regdoc_ir.yaml"
    output_path = tmp_path / "SAMPLE_EXTRACT.md"
    ir_path.write_text(yaml.safe_dump(_sample_ir(), allow_unicode=True, sort_keys=False), encoding="utf-8")

    exit_code = main(
        [
            "--ir",
            str(ir_path),
            "--nid",
            "cha1.p1_8.iiii.si3",
            "--output",
            str(output_path),
            "--blank-text-kind",
            "paragraph",
        ]
    )

    assert exit_code == 0
    assert output_path.read_text(encoding="utf-8").startswith("# 深い階層サンプル抽出")
