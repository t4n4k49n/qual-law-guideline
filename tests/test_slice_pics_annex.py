from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_slice_annex_stops_before_next_annex(tmp_path: Path) -> None:
    src = Path("tests/fixtures/pics_slice_annex_fixture.txt")
    out_path = tmp_path / "annex1.txt"

    subprocess.run(
        [
            sys.executable,
            "scripts/slice_pics_annex.py",
            "--input",
            str(src),
            "--annex-id",
            "1",
            "--output",
            str(out_path),
        ],
        check=True,
    )

    text = out_path.read_text(encoding="utf-8")
    assert "ANNEX 1" in text
    assert "Line A" in text
    assert "ANNEX 2" not in text
    assert "Line B" not in text


def test_slice_annex_does_not_stop_on_inline_reference(tmp_path: Path) -> None:
    src = Path("tests/fixtures/pics_slice_annex_fixture.txt")
    out_path = tmp_path / "annex1.txt"

    subprocess.run(
        [
            sys.executable,
            "scripts/slice_pics_annex.py",
            "--input",
            str(src),
            "--annex-id",
            "1",
            "--output",
            str(out_path),
        ],
        check=True,
    )

    text = out_path.read_text(encoding="utf-8")
    assert "references Annex 1 in sentence" in text


def test_slice_annex_supports_alphanumeric_annex_id(tmp_path: Path) -> None:
    src = Path("tests/fixtures/pics_slice_annex_2a_fixture.txt")
    out_path = tmp_path / "annex2a.txt"

    subprocess.run(
        [
            sys.executable,
            "scripts/slice_pics_annex.py",
            "--input",
            str(src),
            "--annex-id",
            "2A",
            "--output",
            str(out_path),
        ],
        check=True,
    )

    text = out_path.read_text(encoding="utf-8")
    assert "ANNEX 2A" in text
    assert "ATMP line 1" in text
    assert "ANNEX 2B" not in text
    assert "ATMP line 2" not in text
    assert "references Annex 2A in sentence" in text


def test_slice_annex_prefers_longest_block_when_heading_repeats(tmp_path: Path) -> None:
    src = tmp_path / "annex_repeat.txt"
    src.write_text(
        "\n".join(
            [
                "ANNEX 2A",
                "TOC line",
                "ANNEX 2B",
                "Other TOC line",
                "",
                "ANNEX 2A",
                "Body line 1",
                "Body line 2",
                "ANNEX 2B",
                "Next annex body",
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    out_path = tmp_path / "annex2a_body.txt"

    subprocess.run(
        [
            sys.executable,
            "scripts/slice_pics_annex.py",
            "--input",
            str(src),
            "--annex-id",
            "2A",
            "--output",
            str(out_path),
        ],
        check=True,
    )

    text = out_path.read_text(encoding="utf-8")
    assert "Body line 1" in text
    assert "Body line 2" in text
    assert "TOC line" not in text
