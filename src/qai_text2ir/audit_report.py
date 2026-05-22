from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import typer
import yaml

from .goal_check import check_bundle

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


def _kind_counts(root: Dict[str, Any]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for node in _walk_nodes(root):
        kind = str(node.get("kind") or "")
        if kind:
            counts[kind] = counts.get(kind, 0) + 1
    return dict(sorted(counts.items()))


def _count_possible_tables(root: Dict[str, Any]) -> int:
    count = 0
    for node in _walk_nodes(root):
        if node.get("kind") != "preformatted":
            continue
        if node.get("kind_raw") == "possible_table" or "possible_plaintext_table_not_structured" in (node.get("tags") or []):
            count += 1
    return count


def _remaining_gap(*, counts: Dict[str, int], possible_tables: int, normal_goal: str, promotion_goal: str) -> str:
    if normal_goal != "pass" or promotion_goal != "pass":
        return "goal_check"
    if counts.get("table_row", 0) == 0 and possible_tables > 0:
        return "table_rows_pending"
    return "none"


def _guess_doc_id(doc_dir: Path) -> Optional[str]:
    matches = sorted(doc_dir.glob("*.regdoc_ir.yaml"))
    if len(matches) != 1:
        return None
    suffix = ".regdoc_ir.yaml"
    name = matches[0].name
    return name[: -len(suffix)] if name.endswith(suffix) else None


def collect_bundle_summary(doc_dir: Path) -> Dict[str, Any]:
    doc_id = _guess_doc_id(doc_dir)
    if not doc_id:
        return {
            "doc_dir": doc_dir.as_posix(),
            "doc_id": None,
            "goal_check": "fail",
            "errors": ["could not determine doc_id from *.regdoc_ir.yaml"],
        }

    ir_path = doc_dir / f"{doc_id}.regdoc_ir.yaml"
    parser_path = doc_dir / f"{doc_id}.parser_profile.yaml"
    meta_path = doc_dir / f"{doc_id}.meta.yaml"
    manifest_path = doc_dir / "manifest.yaml"
    ir = _load_yaml(ir_path) if ir_path.exists() else {}
    root = ir.get("content") or {}
    counts = _kind_counts(root) if isinstance(root, dict) else {}
    node_count = sum(counts.values())
    source_nodes = 0
    source_total = 0
    for node in _walk_nodes(root) if isinstance(root, dict) else []:
        spans = node.get("source_spans") or []
        if node.get("nid") != "root" and spans:
            source_nodes += 1
            source_total += len(spans)
    non_root = max(node_count - 1, 0)
    coverage = round(source_nodes / non_root, 6) if non_root else 1.0

    parser_profile = _load_yaml(parser_path) if parser_path.exists() else {}
    meta = _load_yaml(meta_path) if meta_path.exists() else {}
    manifest = _load_yaml(manifest_path) if manifest_path.exists() else {}
    goal = check_bundle(doc_dir, doc_id)
    promotion_goal = check_bundle(doc_dir, doc_id, mode="promotion")
    provenance = ((manifest.get("parser_profile") or {}).get("provenance") or [])
    refine = manifest.get("refine") or {}
    qualitycheck = manifest.get("qualitycheck") or {}
    doc_meta = meta.get("doc") or {}
    possible_tables = _count_possible_tables(root) if isinstance(root, dict) else 0
    normal_goal_status = "pass" if goal.passed else "fail"
    promotion_goal_status = "pass" if promotion_goal.passed else "fail"

    return {
        "doc_dir": doc_dir.as_posix(),
        "doc_id": doc_id,
        "input_path": ((manifest.get("input") or {}).get("path") or ""),
        "parser_profile": parser_profile.get("id"),
        "parser_profile_path": ((manifest.get("parser_profile") or {}).get("path") or ""),
        "schema": ir.get("schema"),
        "four_files": all(
            (doc_dir / f"{doc_id}.{suffix}").exists()
            for suffix in ["regdoc_ir.yaml", "parser_profile.yaml", "regdoc_profile.yaml", "meta.yaml"]
        ),
        "manifest": manifest_path.exists(),
        "strict": qualitycheck.get("strict"),
        "qualitycheck_warnings": qualitycheck.get("warnings_count"),
        "goal_check": normal_goal_status,
        "promotion_goal_check": promotion_goal_status,
        "goal_errors": [e.to_dict() for e in goal.errors],
        "goal_warnings": [w.to_dict() for w in goal.warnings],
        "promotion_goal_errors": [e.to_dict() for e in promotion_goal.errors],
        "promotion_goal_warnings": [w.to_dict() for w in promotion_goal.warnings],
        "node_count": node_count,
        "kind_counts": counts,
        "source_spans": {
            "nodes_with_source_spans": source_nodes,
            "non_root_nodes": non_root,
            "coverage": coverage,
            "total_spans": source_total,
        },
        "table_counts": {
            "table": counts.get("table", 0),
            "table_header": counts.get("table_header", 0),
            "table_row": counts.get("table_row", 0),
            "note": counts.get("note", 0),
            "preformatted": counts.get("preformatted", 0),
            "possible_table": possible_tables,
        },
        "meta_family": doc_meta.get("family"),
        "profile_provenance_count": len(provenance),
        "refine_applied_count": len(refine.get("applied") or []),
        "title": (doc_meta.get("title") or ""),
        "remaining_gap": _remaining_gap(
            counts=counts,
            possible_tables=possible_tables,
            normal_goal=normal_goal_status,
            promotion_goal=promotion_goal_status,
        ),
    }


def collect_run_summary(run_out_dir: Path) -> Dict[str, Any]:
    doc_dirs = sorted([p for p in Path(run_out_dir).iterdir() if p.is_dir()])
    documents = [collect_bundle_summary(p) for p in doc_dirs]
    return {
        "run_out_dir": Path(run_out_dir).as_posix(),
        "document_count": len(documents),
        "documents": documents,
        "totals": {
            "goal_pass": sum(1 for d in documents if d.get("goal_check") == "pass"),
            "goal_fail": sum(1 for d in documents if d.get("goal_check") == "fail"),
            "nodes": sum(int(d.get("node_count") or 0) for d in documents),
            "tables": sum(int((d.get("table_counts") or {}).get("table") or 0) for d in documents),
            "table_rows": sum(int((d.get("table_counts") or {}).get("table_row") or 0) for d in documents),
            "notes": sum(int((d.get("table_counts") or {}).get("note") or 0) for d in documents),
            "possible_tables": sum(int((d.get("table_counts") or {}).get("possible_table") or 0) for d in documents),
        },
    }


def render_markdown(summary: Dict[str, Any]) -> str:
    lines = [
        "# TEXT2IR AUDIT REPORT",
        "",
        f"- Run out dir: `{summary.get('run_out_dir')}`",
        f"- Documents: {summary.get('document_count')}",
        f"- GOAL pass: {summary.get('totals', {}).get('goal_pass')}",
        f"- GOAL fail: {summary.get('totals', {}).get('goal_fail')}",
        "",
        "## Documents",
        "",
        "| doc_id | goal | promotion | schema | family | 4files | manifest | strict | warnings | nodes | source coverage | table | row | note | possible_table | profile | refine | remaining_gap |",
        "|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|",
    ]
    for doc in summary.get("documents") or []:
        table_counts = doc.get("table_counts") or {}
        source = doc.get("source_spans") or {}
        lines.append(
            "| {doc_id} | {goal} | {promotion} | {schema} | {family} | {four} | {manifest} | {strict} | {warnings} | {nodes} | {coverage} | {table} | {row} | {note} | {possible} | {profile} | {refine} | {gap} |".format(
                doc_id=doc.get("doc_id"),
                goal=doc.get("goal_check"),
                promotion=doc.get("promotion_goal_check"),
                schema=doc.get("schema"),
                family=doc.get("meta_family"),
                four=doc.get("four_files"),
                manifest=doc.get("manifest"),
                strict=doc.get("strict"),
                warnings=doc.get("qualitycheck_warnings"),
                nodes=doc.get("node_count"),
                coverage=source.get("coverage"),
                table=table_counts.get("table"),
                row=table_counts.get("table_row"),
                note=table_counts.get("note"),
                possible=table_counts.get("possible_table"),
                profile=doc.get("parser_profile"),
                refine=doc.get("refine_applied_count"),
                gap=doc.get("remaining_gap"),
            )
        )
    lines += ["", "## GOAL Issues", ""]
    issue_count = 0
    for doc in summary.get("documents") or []:
        for error in doc.get("goal_errors") or []:
            issue_count += 1
            lines.append(f"- `{doc.get('doc_id')}` error `{error.get('code')}`: {error.get('message')}")
        for warning in doc.get("goal_warnings") or []:
            issue_count += 1
            lines.append(f"- `{doc.get('doc_id')}` warning `{warning.get('code')}`: {warning.get('message')}")
    if issue_count == 0:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


@app.command()
def main(
    run_out_dir: Path = typer.Option(..., "--run-out-dir", exists=True, file_okay=False, dir_okay=True),
    format: str = typer.Option("markdown", "--format"),
    out: Optional[Path] = typer.Option(None, "--out"),
) -> None:
    summary = collect_run_summary(run_out_dir)
    if format == "json":
        rendered = json.dumps(summary, ensure_ascii=False, indent=2)
    elif format == "yaml":
        rendered = yaml.safe_dump(summary, sort_keys=False, allow_unicode=True)
    elif format == "markdown":
        rendered = render_markdown(summary)
    else:
        raise typer.BadParameter("format must be markdown, json, or yaml")
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        typer.echo(rendered)


if __name__ == "__main__":
    app()
