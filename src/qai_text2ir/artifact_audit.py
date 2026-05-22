from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import typer
import yaml

from .artifact_classifier import has_dot_leader, looks_like_form_artifact
from .glyph_sanitizer import PRIVATE_USE_RE, pua_codepoints

app = typer.Typer(add_completion=False)


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _walk_nodes(root: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    stack = [root]
    while stack:
        node = stack.pop()
        yield node
        stack.extend(reversed([c for c in node.get("children", []) if isinstance(c, dict)]))


def _walk_strings(value: Any, path: str = "$") -> Iterable[tuple[str, str]]:
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, list):
        for idx, item in enumerate(value):
            yield from _walk_strings(item, f"{path}[{idx}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from _walk_strings(item, f"{path}.{key}")


def _preview(text: str, limit: int = 120) -> str:
    return " ".join(text.split())[:limit]


def audit_ir_file(path: Path) -> Dict[str, Any]:
    payload = _load_yaml(path)
    doc_id = str(payload.get("doc_id") or path.name.removesuffix(".regdoc_ir.yaml"))
    findings: List[Dict[str, Any]] = []
    root = payload.get("content") if isinstance(payload.get("content"), dict) else {}
    node_by_path: Dict[str, Dict[str, Any]] = {}
    for node in _walk_nodes(root):
        nid = str(node.get("nid") or "")
        for key in ("heading", "text", "kind_raw"):
            if isinstance(node.get(key), str):
                node_by_path[f"{nid}.{key}"] = node

    for field_path, text in _walk_strings(payload):
        flags: List[str] = []
        cps = pua_codepoints(text)
        if cps:
            flags.append("literal_pua")
        if "\uFFFD" in text:
            flags.append("replacement_char")
        if has_dot_leader(text):
            flags.append("dot_leader")
        if looks_like_form_artifact(text):
            flags.append("form_artifact_like")
        if not flags:
            continue
        severity = "warning"
        if "literal_pua" in flags or "replacement_char" in flags:
            severity = "severe"
        elif ("dot_leader" in flags or "form_artifact_like" in flags) and (
            field_path.endswith(".text") or field_path.endswith(".heading")
        ):
            severity = "review"
        findings.append(
            {
                "doc_id": doc_id,
                "file": str(path),
                "field": field_path,
                "codepoints": cps,
                "flags": flags,
                "severity": severity,
                "preview": _preview(text),
            }
        )

    summary = {
        "doc_id": doc_id,
        "file": str(path),
        "literal_pua": sum(1 for f in findings if "literal_pua" in f["flags"]),
        "replacement_char": sum(1 for f in findings if "replacement_char" in f["flags"]),
        "dot_leader_hits": sum(1 for f in findings if "dot_leader" in f["flags"]),
        "form_artifact_like": sum(1 for f in findings if "form_artifact_like" in f["flags"]),
        "severe": sum(1 for f in findings if f["severity"] == "severe"),
        "review": sum(1 for f in findings if f["severity"] == "review"),
    }
    return {"summary": summary, "findings": findings}


def audit_paths(paths: List[Path]) -> Dict[str, Any]:
    files: List[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(path.rglob("*.regdoc_ir.yaml")))
        elif path.name.endswith(".regdoc_ir.yaml"):
            files.append(path)

    documents = [audit_ir_file(path) for path in files]
    summary = {
        "files": len(files),
        "literal_pua": sum(d["summary"]["literal_pua"] for d in documents),
        "replacement_char": sum(d["summary"]["replacement_char"] for d in documents),
        "dot_leader_hits": sum(d["summary"]["dot_leader_hits"] for d in documents),
        "form_artifact_like": sum(d["summary"]["form_artifact_like"] for d in documents),
        "severe": sum(d["summary"]["severe"] for d in documents),
        "review": sum(d["summary"]["review"] for d in documents),
    }
    return {"summary": summary, "documents": documents}


def render_markdown(result: Dict[str, Any]) -> str:
    summary = result["summary"]
    lines = [
        "# TEXT2IR ARTIFACT AUDIT",
        "",
        "## Summary",
        "",
        "| files | literal_pua | replacement_char | dot_leader_hits | form_artifact_like | severe | review |",
        "|---:|---:|---:|---:|---:|---:|---:|",
        f"| {summary['files']} | {summary['literal_pua']} | {summary['replacement_char']} | {summary['dot_leader_hits']} | {summary['form_artifact_like']} | {summary['severe']} | {summary['review']} |",
        "",
        "## Documents",
        "",
        "| doc_id | literal_pua | dot_leader_hits | form_artifact_like | severe | review | file |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for doc in result["documents"]:
        item = doc["summary"]
        lines.append(
            f"| {item['doc_id']} | {item['literal_pua']} | {item['dot_leader_hits']} | {item['form_artifact_like']} | {item['severe']} | {item['review']} | `{item['file']}` |"
        )
    lines += ["", "## Critical Nodes", "", "| doc_id | field | flags | severity | preview |", "|---|---|---|---|---|"]
    for doc in result["documents"]:
        for finding in doc["findings"]:
            if finding["severity"] != "severe":
                continue
            preview = str(finding["preview"]).replace("|", "\\|")
            lines.append(
                f"| {finding['doc_id']} | `{finding['field']}` | {','.join(finding['flags'])} | {finding['severity']} | {preview} |"
            )
    lines.append("")
    return "\n".join(lines)


@app.command()
def main(
    paths: List[Path] = typer.Argument(..., exists=True),
    json_out: Optional[Path] = typer.Option(None, "--json-out"),
    md_out: Optional[Path] = typer.Option(None, "--md-out"),
) -> None:
    result = audit_paths(paths)
    if json_out:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    if md_out:
        md_out.parent.mkdir(parents=True, exist_ok=True)
        md_out.write_text(render_markdown(result), encoding="utf-8", newline="\n")
    if not json_out and not md_out:
        typer.echo(render_markdown(result))


if __name__ == "__main__":
    app()
