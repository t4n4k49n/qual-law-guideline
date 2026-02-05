from __future__ import annotations

from typing import Any, Dict, List, Optional


def build_parser_profile(
    profile_id: str = "jp_law_default_v1",
    title: Optional[str] = "JP Law default markers",
) -> Dict[str, Any]:
    marker_types: List[Dict[str, Any]] = [
        {
            "id": "chapter",
            "kind": "chapter",
            "kind_raw": "章",
            "match": r"^第[一二三四五六七八九十百千]+章",
        },
        {
            "id": "section",
            "kind": "section",
            "kind_raw": "節",
            "match": r"^第[一二三四五六七八九十百千]+節",
        },
        {
            "id": "article",
            "kind": "article",
            "kind_raw": "条",
            "match": r"^第[一二三四五六七八九十百千]+条",
        },
        {
            "id": "paragraph",
            "kind": "paragraph",
            "kind_raw": "項",
            "match": r"^[0-9０-９]+",
        },
        {
            "id": "item",
            "kind": "item",
            "kind_raw": "号",
            "match": r"^[一二三四五六七八九十]+",
        },
        {
            "id": "subitem",
            "kind": "subitem",
            "kind_raw": "イロハ",
            "match": r"^[アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン]",
        },
        {
            "id": "point",
            "kind": "point",
            "kind_raw": "（1）",
            "match": r"^(\\([0-9]+\\)|（[0-9０-９]+）)",
        },
    ]

    structure = {
        "root": {"children": ["chapter", "section", "article", "annex", "appendix"]},
        "chapter": {"children": ["section", "article"]},
        "section": {"children": ["article"]},
        "article": {"children": ["paragraph", "item", "subitem", "point"]},
        "paragraph": {"children": ["item", "subitem", "point"]},
        "item": {"children": ["subitem", "point"]},
        "subitem": {"children": ["point"]},
        "point": {"children": []},
        "annex": {"children": ["article"]},
        "appendix": {"children": []},
    }

    return {
        "schema": "qai.parser_profile.v1",
        "id": profile_id,
        "title": title,
        "applies_to": {
            "family": "JP_LAW",
            "jurisdiction": "JP",
            "defaults": True,
        },
        "marker_types": marker_types,
        "structure": structure,
        "diagnostics": [],
        "warnings": {},
        "compound_prefix": {"enabled": True, "max_depth": 4},
    }


def build_regdoc_profile(doc_id: str) -> Dict[str, Any]:
    return {
        "schema": "qai.regdoc_profile.v1",
        "doc_id": doc_id,
        "profiles": {
            "dq_gmp_checklist": {
                "selectable_kinds": ["subitem", "item", "paragraph", "statement"],
                "grouping_policy": [
                    {"when_kind": "subitem", "group_under_kind": "item"},
                    {"when_kind": "item", "group_under_kind": "paragraph"},
                    {"when_kind": "paragraph", "group_under_kind": "article"},
                    {"when_kind": "statement", "group_under_kind": "article"},
                ],
                "context_display_policy": [
                    {
                        "when_kind": "subitem",
                        "include_ancestors_until_kind": "article",
                        "include_headings": True,
                        "include_chapeau_text": True,
                    },
                    {
                        "when_kind": "item",
                        "include_ancestors_until_kind": "article",
                        "include_headings": True,
                        "include_chapeau_text": True,
                    },
                    {
                        "when_kind": "paragraph",
                        "include_ancestors_until_kind": "article",
                        "include_headings": True,
                        "include_chapeau_text": True,
                    },
                ],
                "render_templates": {},
            }
        },
    }
