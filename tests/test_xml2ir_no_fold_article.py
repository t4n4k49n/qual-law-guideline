from __future__ import annotations

from qai_xml2ir.models_profiles import build_parser_profile
from qai_xml2ir.verify import check_article_paragraph_structure


def test_check_article_paragraph_structure_detects_all_violations() -> None:
    root = {
        "nid": "root",
        "kind": "document",
        "children": [
            {
                "nid": "art1",
                "kind": "article",
                "text": "bad article text",
                "children": [
                    {"nid": "art1.i1", "kind": "item", "children": []},
                ],
            },
            {
                "nid": "art2",
                "kind": "article",
                "text": None,
                "children": [],
            },
        ],
    }
    problems = check_article_paragraph_structure(root)
    assert any("article.text must be empty: nid=art1" in p for p in problems)
    assert any("article has forbidden direct children" in p and "art1" in p for p in problems)
    assert any("article must have paragraph child: nid=art1" in p for p in problems)
    assert any("article must have paragraph child: nid=art2" in p for p in problems)


def test_parser_profile_structure_disallows_article_direct_item() -> None:
    profile = build_parser_profile()
    structure = profile["structure"]
    root_children = structure["root"]["children"]
    article_children = structure["article"]["children"]

    assert "paragraph" in root_children
    assert "appendix" in root_children
    assert "paragraph" in article_children
    assert "appendix" in article_children
    assert "item" not in article_children
    assert "subitem" not in article_children
    assert "point" not in article_children

    for kind in ("part", "chapter", "section", "subsection", "division"):
        assert "appendix" in structure[kind]["children"]
