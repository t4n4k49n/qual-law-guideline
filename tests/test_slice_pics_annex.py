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
