from __future__ import annotations

from pathlib import Path

from qai_text2ir.profile_loader import load_parser_profile


def _write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def test_extends_list_merge_concat_and_uniq(tmp_path: Path) -> None:
    _write(
        tmp_path / "base.yaml",
        "\n".join(
            [
                "schema: qai.parser_profile.v1",
                "id: base",
                "preprocess:",
                "  drop_line_regexes:",
                "    - 'A'",
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
                "    - 'B'",
                "    - 'A'",
            ]
        )
        + "\n",
    )

    profile = load_parser_profile(
        profile_id="child",
        profiles_dir_override=tmp_path,
    )
    assert profile["preprocess"]["drop_line_regexes"] == ["A", "B"]


def test_extends_marker_types_merge_by_id(tmp_path: Path) -> None:
    _write(
        tmp_path / "base.yaml",
        "\n".join(
            [
                "schema: qai.parser_profile.v1",
                "id: base",
                "marker_types:",
                "  - id: annex",
                "    kind: annex",
                "    match: 'X'",
                "  - id: section",
                "    kind: section",
                "    match: 'S'",
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
                "marker_types:",
                "  - id: annex",
                "    kind: annex",
                "    match: 'Y'",
            ]
        )
        + "\n",
    )

    profile = load_parser_profile(
        profile_id="child",
        profiles_dir_override=tmp_path,
    )
    markers = profile["marker_types"]
    assert [m.get("id") for m in markers] == ["annex", "section"]
    assert markers[0]["match"] == "Y"
    assert markers[1]["match"] == "S"


def test_extends_cycle_detection(tmp_path: Path) -> None:
    _write(
        tmp_path / "A.yaml",
        "\n".join(
            [
                "schema: qai.parser_profile.v1",
                "id: A",
                "extends: B",
            ]
        )
        + "\n",
    )
    _write(
        tmp_path / "B.yaml",
        "\n".join(
            [
                "schema: qai.parser_profile.v1",
                "id: B",
                "extends: A",
            ]
        )
        + "\n",
    )

    try:
        load_parser_profile(profile_id="A", profiles_dir_override=tmp_path)
        assert False, "expected ValueError for cyclic extends"
    except ValueError as exc:
        assert "Cyclic profile extends" in str(exc)
