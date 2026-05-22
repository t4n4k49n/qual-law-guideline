from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import typer
import yaml

TABLE_CAPTION_RE = re.compile(
    r"^\s*(?:Table)\s+[\dA-Za-z][\w.-]*\s*[:：\.]?\s+\S.*$|^\s*表\s*[\d０-９一二三四五六七八九十]+[^\n]*$",
    re.IGNORECASE,
)
NOTE_RE = re.compile(r"^\s*(?:Note|Notes|NB)\s*(?:\d+)?\s*[:：\.-]\s*.+$|^\s*(?:注|注記|備考|※)\s*[:：]?\s*.+$", re.IGNORECASE)
FOOTNOTE_RE = re.compile(r"^\s*\([a-z0-9ivxlcdm]+\)\s+\S+", re.IGNORECASE)
FIXED_WIDTH_RE = re.compile(r"\S\s{2,}\S")

app = typer.Typer(add_completion=False)


def inventory_text(text: str, *, input_label: str = "") -> Dict[str, Any]:
    items: List[Dict[str, Any]] = []
    fixed_width_rows = 0
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        if TABLE_CAPTION_RE.match(stripped):
            items.append({"kind": "table_caption", "line": line_no, "text": stripped})
            continue
        if NOTE_RE.match(stripped):
            items.append({"kind": "note", "line": line_no, "text": stripped})
            continue
        if FOOTNOTE_RE.match(stripped):
            items.append({"kind": "footnote_like", "line": line_no, "text": stripped})
            continue
        if FIXED_WIDTH_RE.search(stripped):
            fixed_width_rows += 1
    return {
        "input": input_label,
        "tables_detected": sum(1 for item in items if item["kind"] == "table_caption"),
        "notes_detected": sum(1 for item in items if item["kind"] in {"note", "footnote_like"}),
        "fixed_width_candidate_rows": fixed_width_rows,
        "items": items,
    }


def render_markdown(result: Dict[str, Any]) -> str:
    lines = [
        "# TABLE / NOTE INVENTORY",
        "",
        f"- input: `{result.get('input')}`",
        f"- tables_detected: {result.get('tables_detected')}",
        f"- notes_detected: {result.get('notes_detected')}",
        f"- fixed_width_candidate_rows: {result.get('fixed_width_candidate_rows')}",
        "",
        "| kind | line | text |",
        "|---|---:|---|",
    ]
    for item in result.get("items") or []:
        text = str(item.get("text") or "").replace("|", "\\|")
        lines.append(f"| {item.get('kind')} | {item.get('line')} | {text} |")
    lines.append("")
    return "\n".join(lines)


@app.command()
def main(
    input: Path = typer.Option(..., "--input", exists=True, dir_okay=False),
    out: Optional[Path] = typer.Option(None, "--out"),
    format: str = typer.Option("json", "--format"),
) -> None:
    result = inventory_text(input.read_text(encoding="utf-8"), input_label=str(input))
    if format == "json":
        rendered = json.dumps(result, ensure_ascii=bool(out is None), indent=2)
    elif format == "yaml":
        rendered = yaml.safe_dump(result, allow_unicode=True, sort_keys=False)
    elif format == "markdown":
        rendered = render_markdown(result)
    else:
        raise typer.BadParameter("format must be json, yaml, or markdown")

    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered + "\n", encoding="utf-8", newline="\n")
    else:
        typer.echo(rendered.encode("ascii", "backslashreplace").decode("ascii"))


if __name__ == "__main__":
    app()
