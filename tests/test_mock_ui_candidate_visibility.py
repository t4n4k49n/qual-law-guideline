from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml

from qai_mock_ui.candidate_visibility import build_candidate_visibility_map
from qai_mock_ui.ir_model import build_doc_index

BASE_DIR = Path(
    "data/normalized/jp_egov_336M50000100002_20260501_507M60000100117"
)
IR_PATH = BASE_DIR / "jp_egov_336M50000100002_20260501_507M60000100117.regdoc_ir.yaml"
PROFILE_PATH = BASE_DIR / "jp_egov_336M50000100002_20260501_507M60000100117.regdoc_profile.yaml"


def _load_fixture() -> tuple[Dict[str, Any], Dict[str, Any]]:
    regdoc_ir = yaml.safe_load(IR_PATH.read_text(encoding="utf-8"))
    regdoc_profile = yaml.safe_load(PROFILE_PATH.read_text(encoding="utf-8"))
    if not isinstance(regdoc_ir, dict) or not isinstance(regdoc_profile, dict):
        raise ValueError("fixture load failed")
    return regdoc_ir, regdoc_profile


def test_candidate_visibility_deny_under_annex_hides_annex_subtree() -> None:
    regdoc_ir, regdoc_profile = _load_fixture()
    index = build_doc_index(regdoc_ir)
    purpose = regdoc_profile["profiles"]["dq_gmp_checklist"]
    purpose["candidate_visibility"] = {
        "deny_rules": [
            {"under_kind": "annex"},
            {"kind": "annex"},
        ]
    }

    visible = build_candidate_visibility_map(index, purpose)
    assert visible["art1.p1"] is True
    assert visible["annex1"] is False
    assert visible["annex1.p1"] is False


def test_candidate_visibility_allow_then_deny_uses_deny_precedence() -> None:
    regdoc_ir, regdoc_profile = _load_fixture()
    index = build_doc_index(regdoc_ir)
    purpose = regdoc_profile["profiles"]["dq_gmp_checklist"]
    purpose["candidate_visibility"] = {
        "allow_rules": [{"kind_in": ["paragraph"]}],
        "deny_rules": [{"under_kind": "annex"}],
    }

    visible = build_candidate_visibility_map(index, purpose)
    assert visible["art1.p1"] is True
    assert visible["art1.p1.i1"] is False
    assert visible["annex1.p1"] is False


def test_candidate_visibility_hides_reference_artifacts_even_if_kind_is_allowed() -> None:
    regdoc_ir, regdoc_profile = _load_fixture()
    first_child = regdoc_ir["content"]["children"][0]
    first_child.setdefault("children", []).append(
        {
            "nid": "art1.p1.art1",
            "kind": "preformatted",
            "kind_raw": "form_artifact",
            "num": None,
            "ord": 1.5,
            "heading": None,
            "text": "Reference form artifact: hidden by default.",
            "role": "informative",
            "normativity": None,
            "tags": ["form_artifact", "not_selectable"],
            "refs": {"internal": [], "external": []},
            "source_spans": [{"source_id": "fixture", "start_line": 1, "end_line": 3}],
            "visibility": {
                "default_review": "hidden",
                "dq_gmp_checklist": "hidden",
                "search_default": "hidden",
            },
            "children": [],
        }
    )

    index = build_doc_index(regdoc_ir)
    purpose = regdoc_profile["profiles"]["dq_gmp_checklist"]
    purpose["candidate_visibility"] = {"allow_rules": [{"kind_in": ["paragraph", "preformatted"]}]}

    visible = build_candidate_visibility_map(index, purpose)
    assert visible["art1.p1"] is True
    assert visible["art1.p1.art1"] is False
