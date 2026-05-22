from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from qai_text2ir.table_note_inventory import app, inventory_text


def test_inventory_text_detects_tables_notes_and_footnotes() -> None:
    text = "\n".join(
        [
            "Table 1 Maximum permitted total particle concentration",
            "Grade  At rest  In operation",
            "A      3520     3520",
            "Note 1: The particle limits apply to the whole cleanroom.",
            "(a) Footnote-style table note.",
        ]
    )

    result = inventory_text(text, input_label="sample.txt")

    assert result["tables_detected"] == 1
    assert result["notes_detected"] == 2
    assert result["fixed_width_candidate_rows"] == 2
    assert result["items"][0]["kind"] == "table_caption"


def test_inventory_cli_writes_json(tmp_path: Path) -> None:
    input_path = tmp_path / "sample.txt"
    out_path = tmp_path / "inventory.json"
    input_path.write_text("Table 2: Example\nA  B\nNote: Example note\n", encoding="utf-8", newline="\n")

    result = CliRunner().invoke(app, ["--input", str(input_path), "--out", str(out_path)])

    assert result.exit_code == 0
    data = json.loads(out_path.read_text(encoding="utf-8"))
    assert data["tables_detected"] == 1
    assert data["notes_detected"] == 1
