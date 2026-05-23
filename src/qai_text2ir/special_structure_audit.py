from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import typer
import yaml


TABLE_CAPTION_RE = re.compile(r"^\s*Table\s+([0-9A-Za-z][\w.-]*)\s*[:：\.]\s+\S.*$", re.IGNORECASE | re.MULTILINE)
FIGURE_CAPTION_RE = re.compile(r"^\s*Figure\s+([0-9A-Za-z][\w.-]*)\s*[:：\.]\s+\S.*$", re.IGNORECASE | re.MULTILINE)
CHECKED_ITEM_RE = re.compile(r"CHECKED ITEM", re.IGNORECASE)
YES_NO_NA_RE = re.compile(r"YES\s+NO\s+N/?A\s+COMMENTS", re.IGNORECASE)
FIXED_WIDTH_RE = re.compile(r"\S.*?\s{2,}\S.*?\s{2,}\S")
CHECKBOX_OR_FORM_RE = re.compile(r"[\uE000-\uF8FF☐☑☒□■]|\.{4,}|…{2,}|_{3,}")
ORDINARY_TEXT_KINDS = {"chapter", "section", "paragraph", "item", "subitem"}
SPECIAL_COUNT_KINDS = {"table", "table_header", "table_row", "figure", "preformatted", "note"}

app = typer.Typer(add_completion=False)


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _walk_nodes(root: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    stack = [root]
    while stack:
        node = stack.pop()
        yield node
        stack.extend(reversed([c for c in node.get("children") or [] if isinstance(c, dict)]))


def _guess_doc_id(doc_dir: Path) -> Optional[str]:
    matches = sorted(doc_dir.glob("*.regdoc_ir.yaml"))
    if len(matches) != 1:
        return None
    suffix = ".regdoc_ir.yaml"
    return matches[0].name[: -len(suffix)]


def _caption_key(kind: str, number: str) -> str:
    return f"{kind.lower()} {number.lower().rstrip('.')}"


def _first_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _line_range_from_spans(node: Dict[str, Any]) -> Optional[str]:
    starts: List[int] = []
    ends: List[int] = []
    for span in node.get("source_spans") or []:
        if not isinstance(span, dict):
            continue
        start = span.get("start_line") or span.get("line_start") or span.get("start")
        end = span.get("end_line") or span.get("line_end") or span.get("end") or start
        locator = span.get("locator")
        if not isinstance(start, int) and isinstance(locator, str):
            match = re.search(r"line:(\d+)", locator)
            if match:
                start = int(match.group(1))
                end = start
        if isinstance(start, int):
            starts.append(start)
        if isinstance(end, int):
            ends.append(end)
    if not starts:
        return None
    return f"{min(starts)}-{max(ends or starts)}"


def _resolve_source_path(bundle_dir: Path, manifest: Dict[str, Any]) -> Optional[Path]:
    raw = ((manifest.get("input") or {}).get("path") or "").strip()
    if not raw:
        return None
    path = Path(raw)
    candidates = [path]
    if not path.is_absolute():
        candidates.extend([Path.cwd() / path, bundle_dir / path, bundle_dir.parent / path])
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return path


def audit_source_text(text: str, *, source_path: str = "") -> Dict[str, Any]:
    table_captions: List[Dict[str, Any]] = []
    figure_captions: List[Dict[str, Any]] = []
    checklist_headers: List[Dict[str, Any]] = []
    fixed_width_blocks: List[Dict[str, Any]] = []
    current_block: List[Tuple[int, str]] = []

    def flush_block() -> None:
        nonlocal current_block
        if len(current_block) >= 2:
            fixed_width_blocks.append(
                {
                    "source_path": source_path,
                    "line_start": current_block[0][0],
                    "line_end": current_block[-1][0],
                    "sample": current_block[0][1].strip(),
                }
            )
        current_block = []

    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        table_match = TABLE_CAPTION_RE.match(line)
        figure_match = FIGURE_CAPTION_RE.match(line)
        if table_match:
            table_captions.append(
                {
                    "source_path": source_path,
                    "line": line_no,
                    "caption": stripped,
                    "key": _caption_key("table", table_match.group(1)),
                }
            )
        if figure_match:
            figure_captions.append(
                {
                    "source_path": source_path,
                    "line": line_no,
                    "caption": stripped,
                    "key": _caption_key("figure", figure_match.group(1)),
                }
            )
        if CHECKED_ITEM_RE.search(line) or YES_NO_NA_RE.search(line):
            checklist_headers.append({"source_path": source_path, "line": line_no, "text": stripped})

        if FIXED_WIDTH_RE.search(line):
            current_block.append((line_no, line))
        else:
            flush_block()
    flush_block()

    return {
        "source_path": source_path,
        "table_captions": table_captions,
        "figure_captions": figure_captions,
        "checklist_headers": checklist_headers,
        "fixed_width_blocks": fixed_width_blocks,
    }


def _node_text(node: Dict[str, Any]) -> str:
    parts = [node.get("heading"), node.get("text")]
    return "\n".join(str(part) for part in parts if part not in (None, ""))


def _has_multiline_fixed_width(text: str) -> bool:
    return sum(1 for line in text.splitlines() if FIXED_WIDTH_RE.search(line)) >= 2


def _recommended_resolution(trigger: str) -> str:
    if "possible_" in trigger or "caption" in trigger or "fixed_width" in trigger:
        return "targeted_parser"
    if "checklist" in trigger or "form" in trigger:
        return "profile_rule"
    return "targeted_parser"


def audit_ir(ir: Dict[str, Any]) -> Dict[str, Any]:
    root = ir.get("content") or {}
    nodes = list(_walk_nodes(root)) if isinstance(root, dict) else []
    counts = {kind: 0 for kind in SPECIAL_COUNT_KINDS}
    suspicious_nodes: List[Dict[str, Any]] = []
    generated_caption_keys = {"table": set(), "figure": set()}

    for node in nodes:
        kind = str(node.get("kind") or "")
        if kind in counts:
            counts[kind] += 1
        text = _node_text(node)
        for match in TABLE_CAPTION_RE.finditer(text):
            if kind == "table":
                generated_caption_keys["table"].add(_caption_key("table", match.group(1)))
        for match in FIGURE_CAPTION_RE.finditer(text):
            if kind == "figure":
                generated_caption_keys["figure"].add(_caption_key("figure", match.group(1)))

        triggers: List[str] = []
        if kind == "preformatted" and node.get("kind_raw") in {"possible_table", "possible_form"}:
            triggers.append(str(node.get("kind_raw")))
        if kind == "preformatted" and "possible_plaintext_table_not_structured" in (node.get("tags") or []):
            triggers.append("possible_plaintext_table_not_structured")
        if kind in ORDINARY_TEXT_KINDS:
            has_caption = bool(TABLE_CAPTION_RE.search(text) or FIGURE_CAPTION_RE.search(text))
            if has_caption and _has_multiline_fixed_width(text):
                triggers.append("caption_with_fixed_width_in_ordinary_text")
            if CHECKED_ITEM_RE.search(text) or YES_NO_NA_RE.search(text):
                triggers.append("checklist_header_in_ordinary_text")
            if CHECKBOX_OR_FORM_RE.search(text):
                triggers.append("form_control_in_ordinary_text")
            if _has_multiline_fixed_width(text):
                triggers.append("fixed_width_block_in_ordinary_text")
        if triggers:
            suspicious_nodes.append(
                {
                    "nid": node.get("nid"),
                    "kind": kind,
                    "kind_raw": node.get("kind_raw"),
                    "tags": node.get("tags") or [],
                    "line_range": _line_range_from_spans(node),
                    "trigger": ", ".join(sorted(set(triggers))),
                    "text_sample": _first_line(text)[:240],
                    "recommended_resolution": _recommended_resolution(" ".join(triggers)),
                }
            )

    return {
        "counts": counts,
        "generated_caption_keys": {
            "table": sorted(generated_caption_keys["table"]),
            "figure": sorted(generated_caption_keys["figure"]),
        },
        "suspicious_nodes": suspicious_nodes,
    }


def audit_bundle(bundle_dir: Path, doc_id: Optional[str] = None, *, mode: str = "normal") -> Dict[str, Any]:
    bundle_dir = Path(bundle_dir)
    resolved_doc_id = doc_id or _guess_doc_id(bundle_dir)
    if not resolved_doc_id:
        return {
            "doc_id": None,
            "bundle_dir": bundle_dir.as_posix(),
            "status": "fail",
            "errors": ["could not determine doc_id from *.regdoc_ir.yaml"],
            "unresolved_special_blocks": [],
        }

    ir_path = bundle_dir / f"{resolved_doc_id}.regdoc_ir.yaml"
    manifest_path = bundle_dir / "manifest.yaml"
    ir = _load_yaml(ir_path) if ir_path.exists() else {}
    manifest = _load_yaml(manifest_path) if manifest_path.exists() else {}
    source_path = _resolve_source_path(bundle_dir, manifest)
    source = {"source_path": str(source_path or ""), "table_captions": [], "figure_captions": [], "checklist_headers": [], "fixed_width_blocks": []}
    if source_path and source_path.exists():
        source = audit_source_text(source_path.read_text(encoding="utf-8"), source_path=source_path.as_posix())

    ir_audit = audit_ir(ir)
    counts = ir_audit["counts"]
    unresolved: List[Dict[str, Any]] = []
    unresolved.extend(
        {
            "source_path": str(source_path or ""),
            "line_range": item.get("line_range"),
            "trigger": item.get("trigger"),
            "generated_node_nid": item.get("nid"),
            "recommended_resolution": item.get("recommended_resolution"),
            "text_sample": item.get("text_sample"),
        }
        for item in ir_audit["suspicious_nodes"]
    )

    generated_tables = counts.get("table", 0)
    generated_figures = counts.get("figure", 0)
    if generated_tables == 0:
        for caption in source.get("table_captions") or []:
            unresolved.append(
                {
                    "source_path": caption.get("source_path"),
                    "line_range": str(caption.get("line")),
                    "trigger": caption.get("caption"),
                    "generated_node_nid": None,
                    "recommended_resolution": "targeted_parser",
                    "text_sample": caption.get("caption"),
                }
            )
    if generated_figures == 0:
        for caption in source.get("figure_captions") or []:
            unresolved.append(
                {
                    "source_path": caption.get("source_path"),
                    "line_range": str(caption.get("line")),
                    "trigger": caption.get("caption"),
                    "generated_node_nid": None,
                    "recommended_resolution": "targeted_parser",
                    "text_sample": caption.get("caption"),
                }
            )
    for header in source.get("checklist_headers") or []:
        if not any("checklist" in str(item.get("trigger") or "") for item in unresolved):
            unresolved.append(
                {
                    "source_path": header.get("source_path"),
                    "line_range": str(header.get("line")),
                    "trigger": f"checklist_header: {header.get('text')}",
                    "generated_node_nid": None,
                    "recommended_resolution": "profile_rule",
                    "text_sample": header.get("text"),
                }
            )

    status = "pass" if not unresolved else ("fail" if mode in {"promotion", "release"} else "warn")
    return {
        "doc_id": resolved_doc_id,
        "bundle_dir": bundle_dir.as_posix(),
        "source_path": source.get("source_path"),
        "source_tables": len(source.get("table_captions") or []),
        "source_figures": len(source.get("figure_captions") or []),
        "source_checklist_headers": len(source.get("checklist_headers") or []),
        "fixed_width_table_candidate_blocks": len(source.get("fixed_width_blocks") or []),
        "generated_counts": counts,
        "generated_tables": generated_tables,
        "generated_rows": counts.get("table_row", 0),
        "generated_figures": generated_figures,
        "suspicious_nodes": ir_audit["suspicious_nodes"],
        "unresolved_special_blocks": unresolved,
        "unresolved_count": len(unresolved),
        "status": status,
    }


def collect_run_audit(run_out_dir: Path, *, mode: str = "normal") -> Dict[str, Any]:
    doc_dirs = sorted([p for p in Path(run_out_dir).iterdir() if p.is_dir()])
    documents = [audit_bundle(p, mode=mode) for p in doc_dirs]
    return {
        "run_out_dir": Path(run_out_dir).as_posix(),
        "mode": mode,
        "document_count": len(documents),
        "documents": documents,
        "totals": {
            "source_tables": sum(int(d.get("source_tables") or 0) for d in documents),
            "source_figures": sum(int(d.get("source_figures") or 0) for d in documents),
            "generated_tables": sum(int(d.get("generated_tables") or 0) for d in documents),
            "generated_rows": sum(int(d.get("generated_rows") or 0) for d in documents),
            "generated_figures": sum(int(d.get("generated_figures") or 0) for d in documents),
            "unresolved_special_blocks": sum(int(d.get("unresolved_count") or 0) for d in documents),
        },
        "status": "fail" if any(d.get("status") == "fail" for d in documents) else ("warn" if any(d.get("status") == "warn" for d in documents) else "pass"),
    }


def _escape_md(value: Any) -> str:
    return str(value if value is not None else "").replace("|", "\\|").replace("\n", " ")


def render_markdown(summary: Dict[str, Any]) -> str:
    lines = [
        "# SPECIAL STRUCTURE AUDIT",
        "",
        f"- Run out dir: `{summary.get('run_out_dir', '')}`",
        f"- Mode: `{summary.get('mode', '')}`",
        f"- Status: `{summary.get('status', '')}`",
        "",
        "| doc_id | source_tables | source_figures | generated_tables | generated_rows | generated_figures | unresolved_special_blocks | status |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    docs = summary.get("documents") if "documents" in summary else [summary]
    for doc in docs or []:
        lines.append(
            "| {doc_id} | {source_tables} | {source_figures} | {generated_tables} | {generated_rows} | {generated_figures} | {unresolved} | {status} |".format(
                doc_id=_escape_md(doc.get("doc_id")),
                source_tables=doc.get("source_tables", 0),
                source_figures=doc.get("source_figures", 0),
                generated_tables=doc.get("generated_tables", 0),
                generated_rows=doc.get("generated_rows", 0),
                generated_figures=doc.get("generated_figures", 0),
                unresolved=doc.get("unresolved_count", 0),
                status=_escape_md(doc.get("status")),
            )
        )
    lines += ["", "## Unresolved Blocks", "", "| doc_id | source_path | line_range | trigger | generated_node_nid | recommended_resolution |", "|---|---|---:|---|---|---|"]
    count = 0
    for doc in docs or []:
        for item in doc.get("unresolved_special_blocks") or []:
            count += 1
            lines.append(
                f"| {_escape_md(doc.get('doc_id'))} | `{_escape_md(item.get('source_path'))}` | {_escape_md(item.get('line_range'))} | {_escape_md(item.get('trigger') or item.get('text_sample'))} | {_escape_md(item.get('generated_node_nid'))} | {_escape_md(item.get('recommended_resolution'))} |"
            )
    if count == 0:
        lines.append("| none |  |  |  |  |  |")
    lines.append("")
    return "\n".join(lines)


@app.command()
def main(
    run_out_dir: Optional[Path] = typer.Option(None, "--run-out-dir", exists=True, file_okay=False, dir_okay=True),
    bundle_dir: Optional[Path] = typer.Option(None, "--bundle-dir", exists=True, file_okay=False, dir_okay=True),
    doc_id: Optional[str] = typer.Option(None, "--doc-id"),
    mode: str = typer.Option("normal", "--mode", help="normal, promotion, or release"),
    out_dir: Optional[Path] = typer.Option(None, "--out-dir", file_okay=False, dir_okay=True),
    format: str = typer.Option("markdown", "--format"),
    out: Optional[Path] = typer.Option(None, "--out"),
) -> None:
    if mode not in {"normal", "promotion", "release"}:
        raise typer.BadParameter("mode must be normal, promotion, or release")
    if bool(run_out_dir) == bool(bundle_dir):
        raise typer.BadParameter("provide exactly one of --run-out-dir or --bundle-dir")

    summary = collect_run_audit(run_out_dir, mode=mode) if run_out_dir else audit_bundle(bundle_dir, doc_id, mode=mode)  # type: ignore[arg-type]
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "SPECIAL_STRUCTURE_AUDIT.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        (out_dir / "SPECIAL_STRUCTURE_AUDIT.md").write_text(
            render_markdown(summary) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    elif format == "json":
        rendered = json.dumps(summary, ensure_ascii=False, indent=2)
        (out.write_text(rendered + "\n", encoding="utf-8", newline="\n") if out else typer.echo(rendered))
    elif format == "markdown":
        rendered = render_markdown(summary)
        (out.write_text(rendered + "\n", encoding="utf-8", newline="\n") if out else typer.echo(rendered))
    else:
        raise typer.BadParameter("format must be markdown or json")

    if summary.get("status") == "fail":
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
