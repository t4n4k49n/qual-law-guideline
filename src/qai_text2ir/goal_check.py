from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import typer
import yaml

from qai_xml2ir.verify import verify_document


EXPECTED_IR_SCHEMA = "qai.regdoc_ir.v4"
REQUIRED_NODE_FIELDS = [
    "kind",
    "nid",
    "num",
    "heading",
    "text",
    "ord",
    "role",
    "normativity",
    "kind_raw",
    "source_spans",
    "tags",
    "children",
]
REQUIRED_CHECKLIST_KEYS = [
    "candidate_visibility",
    "selectable_kinds",
    "grouping_policy",
    "context_display_policy",
]

app = typer.Typer(add_completion=False)


@dataclass
class CheckMessage:
    code: str
    message: str
    path: str = ""

    def to_dict(self) -> Dict[str, str]:
        data = {"code": self.code, "message": self.message}
        if self.path:
            data["path"] = self.path
        return data


@dataclass
class GoalCheckResult:
    doc_id: str
    bundle_dir: str
    passed: bool
    errors: List[CheckMessage] = field(default_factory=list)
    warnings: List[CheckMessage] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "bundle_dir": self.bundle_dir,
            "passed": self.passed,
            "errors": [e.to_dict() for e in self.errors],
            "warnings": [w.to_dict() for w in self.warnings],
            "summary": self.summary,
        }


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        loaded = yaml.safe_load(f)
    return loaded or {}


def _walk_nodes(root: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    stack = [root]
    while stack:
        node = stack.pop()
        yield node
        children = node.get("children") or []
        stack.extend(reversed([c for c in children if isinstance(c, dict)]))


def _count_kinds(root: Dict[str, Any]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for node in _walk_nodes(root):
        kind = str(node.get("kind") or "")
        if kind:
            counts[kind] = counts.get(kind, 0) + 1
    return dict(sorted(counts.items()))


def _required_paths(bundle_dir: Path, doc_id: str) -> Dict[str, Path]:
    return {
        "ir": bundle_dir / f"{doc_id}.regdoc_ir.yaml",
        "parser_profile": bundle_dir / f"{doc_id}.parser_profile.yaml",
        "regdoc_profile": bundle_dir / f"{doc_id}.regdoc_profile.yaml",
        "meta": bundle_dir / f"{doc_id}.meta.yaml",
        "manifest": bundle_dir / "manifest.yaml",
    }


def check_bundle(bundle_dir: Path, doc_id: str) -> GoalCheckResult:
    bundle_dir = Path(bundle_dir)
    paths = _required_paths(bundle_dir, doc_id)
    errors: List[CheckMessage] = []
    warnings: List[CheckMessage] = []
    summary: Dict[str, Any] = {
        "files": {},
        "schema": None,
        "node_count": 0,
        "kind_counts": {},
        "source_spans": {},
        "verify_document": "not_run",
        "dq_gmp_checklist": {},
        "manifest": {},
    }

    for key in ("ir", "parser_profile", "regdoc_profile", "meta"):
        exists = paths[key].exists()
        summary["files"][key] = {"path": paths[key].name, "exists": exists}
        if not exists:
            errors.append(CheckMessage("missing_required_file", f"missing {paths[key].name}", paths[key].name))

    manifest_exists = paths["manifest"].exists()
    summary["files"]["manifest"] = {"path": paths["manifest"].name, "exists": manifest_exists}
    if not manifest_exists:
        warnings.append(CheckMessage("missing_manifest", "manifest.yaml is missing", "manifest.yaml"))

    if errors:
        return GoalCheckResult(
            doc_id=doc_id,
            bundle_dir=str(bundle_dir),
            passed=False,
            errors=errors,
            warnings=warnings,
            summary=summary,
        )

    ir = _load_yaml(paths["ir"])
    parser_profile = _load_yaml(paths["parser_profile"])
    regdoc_profile = _load_yaml(paths["regdoc_profile"])
    meta = _load_yaml(paths["meta"])
    manifest = _load_yaml(paths["manifest"]) if manifest_exists else {}

    schema = ir.get("schema")
    summary["schema"] = schema
    if schema != EXPECTED_IR_SCHEMA:
        errors.append(CheckMessage("unexpected_ir_schema", f"expected {EXPECTED_IR_SCHEMA}, got {schema!r}", paths["ir"].name))

    root = ir.get("content")
    if not isinstance(root, dict):
        errors.append(CheckMessage("missing_ir_content", "regdoc_ir content is missing or invalid", paths["ir"].name))
        nodes: List[Dict[str, Any]] = []
    else:
        nodes = list(_walk_nodes(root))
        summary["node_count"] = len(nodes)
        summary["kind_counts"] = _count_kinds(root)
        try:
            verify_document(ir)
            summary["verify_document"] = "pass"
        except AssertionError as exc:
            summary["verify_document"] = "fail"
            errors.append(CheckMessage("verify_document_failed", str(exc), paths["ir"].name))

    missing_fields: Dict[str, List[str]] = {}
    source_nodes = 0
    source_total = 0
    table_payload_nodes = 0
    for node in nodes:
        nid = str(node.get("nid") or "")
        if nid != "root":
            missing = [field for field in REQUIRED_NODE_FIELDS if field not in node]
            if missing:
                missing_fields[nid or "<unknown>"] = missing
            spans = node.get("source_spans") or []
            if spans:
                source_nodes += 1
                source_total += len(spans)
            elif node.get("kind") not in {"document"}:
                warnings.append(CheckMessage("missing_source_spans", f"node has no source_spans: {nid}", nid))
        if node.get("kind") in {"table", "table_header", "table_row"} and node.get("data"):
            table_payload_nodes += 1
        if node.get("kind") in {"table", "table_header", "table_row"} and "data" not in node:
            warnings.append(CheckMessage("table_data_missing", "table node has no data payload", nid))

    if missing_fields:
        for nid, fields in sorted(missing_fields.items())[:20]:
            errors.append(CheckMessage("missing_node_fields", f"missing fields: {', '.join(fields)}", nid))
        if len(missing_fields) > 20:
            errors.append(CheckMessage("missing_node_fields_truncated", f"{len(missing_fields) - 20} more nodes missing required fields"))

    non_root_count = max(len(nodes) - 1, 0)
    coverage = (source_nodes / non_root_count) if non_root_count else 1.0
    summary["source_spans"] = {
        "nodes_with_source_spans": source_nodes,
        "non_root_nodes": non_root_count,
        "coverage": round(coverage, 6),
        "total_spans": source_total,
    }
    summary["table_payload_nodes"] = table_payload_nodes

    doc_meta = meta.get("doc") or {}
    bundle_meta = meta.get("bundle") or {}
    generation_meta = meta.get("generation") or {}
    for field_name in ("id", "title", "jurisdiction", "language"):
        if not doc_meta.get(field_name):
            warnings.append(CheckMessage("meta_field_missing", f"meta.doc.{field_name} is missing", paths["meta"].name))
    if "family" not in doc_meta:
        warnings.append(CheckMessage("meta_family_missing", "meta.doc.family is missing; older meta may omit it", paths["meta"].name))
    if not doc_meta.get("sources"):
        warnings.append(CheckMessage("meta_sources_missing", "meta.doc.sources is missing or empty", paths["meta"].name))
    if not bundle_meta:
        errors.append(CheckMessage("meta_bundle_missing", "meta.bundle is missing", paths["meta"].name))
    if not generation_meta:
        warnings.append(CheckMessage("meta_generation_missing", "meta.generation is missing", paths["meta"].name))
    elif not generation_meta.get("inputs"):
        warnings.append(CheckMessage("meta_generation_inputs_missing", "meta.generation.inputs is missing or empty", paths["meta"].name))

    summary["parser_profile"] = {
        "id": parser_profile.get("id"),
        "schema": parser_profile.get("schema"),
        "extends": parser_profile.get("extends"),
        "has_markers": bool(parser_profile.get("markers")),
        "has_refine_subtrees": bool(((parser_profile.get("postprocess") or {}).get("refine_subtrees") or {})),
    }
    if not parser_profile.get("id"):
        errors.append(CheckMessage("parser_profile_id_missing", "parser_profile.id is missing", paths["parser_profile"].name))

    checklist = ((regdoc_profile.get("profiles") or {}).get("dq_gmp_checklist") or {})
    missing_checklist = [key for key in REQUIRED_CHECKLIST_KEYS if key not in checklist]
    if missing_checklist:
        errors.append(
            CheckMessage(
                "dq_gmp_checklist_missing_keys",
                f"missing keys: {', '.join(missing_checklist)}",
                paths["regdoc_profile"].name,
            )
        )
    selectable = checklist.get("selectable_kinds") or []
    context_policy = checklist.get("context_display_policy") or []
    summary["dq_gmp_checklist"] = {
        "has_candidate_visibility": "candidate_visibility" in checklist,
        "selectable_kinds": selectable,
        "has_table_row_selectable": "table_row" in selectable,
        "context_display_policy_count": len(context_policy) if isinstance(context_policy, list) else 0,
        "has_descendant_policy": any(bool(p.get("include_descendants")) for p in context_policy if isinstance(p, dict)),
        "has_ancestor_policy": any("include_ancestors_until_kind" in p for p in context_policy if isinstance(p, dict)),
    }
    if "table_row" not in selectable:
        warnings.append(CheckMessage("table_row_not_selectable", "dq_gmp_checklist.selectable_kinds does not include table_row", paths["regdoc_profile"].name))
    if not summary["dq_gmp_checklist"]["has_descendant_policy"]:
        warnings.append(CheckMessage("descendant_policy_missing", "context_display_policy has no include_descendants rule", paths["regdoc_profile"].name))

    if manifest:
        summary["manifest"] = {
            "schema": manifest.get("schema"),
            "has_input": bool(manifest.get("input")),
            "has_command": bool(manifest.get("command")),
            "has_outputs": bool(manifest.get("outputs")),
            "has_profile_provenance": bool(((manifest.get("parser_profile") or {}).get("provenance"))),
            "qualitycheck": manifest.get("qualitycheck") or {},
            "refine": manifest.get("refine") or {},
        }
        if not summary["manifest"]["has_profile_provenance"]:
            warnings.append(CheckMessage("manifest_profile_provenance_missing", "manifest parser_profile.provenance is missing", paths["manifest"].name))

    return GoalCheckResult(
        doc_id=doc_id,
        bundle_dir=str(bundle_dir),
        passed=not errors,
        errors=errors,
        warnings=warnings,
        summary=summary,
    )


def render_markdown(result: GoalCheckResult) -> str:
    status = "PASS" if result.passed else "FAIL"
    lines = [
        f"# GOAL CHECK: {result.doc_id}",
        "",
        f"Status: **{status}**",
        "",
        "## Summary",
        "",
        f"- Bundle dir: `{result.bundle_dir}`",
        f"- Schema: `{result.summary.get('schema')}`",
        f"- Nodes: {result.summary.get('node_count')}",
        f"- Verify: {result.summary.get('verify_document')}",
        f"- Source span coverage: {result.summary.get('source_spans', {}).get('coverage')}",
        "",
        "## Files",
        "",
        "| File | Exists |",
        "|---|---|",
    ]
    for info in (result.summary.get("files") or {}).values():
        lines.append(f"| `{info.get('path')}` | {info.get('exists')} |")
    lines += ["", "## Kind Counts", "", "| Kind | Count |", "|---|---:|"]
    for kind, count in (result.summary.get("kind_counts") or {}).items():
        lines.append(f"| {kind} | {count} |")
    checklist = result.summary.get("dq_gmp_checklist") or {}
    lines += [
        "",
        "## dq_gmp_checklist",
        "",
        f"- selectable_kinds: `{checklist.get('selectable_kinds')}`",
        f"- table_row selectable: {checklist.get('has_table_row_selectable')}",
        f"- ancestor policy: {checklist.get('has_ancestor_policy')}",
        f"- descendant policy: {checklist.get('has_descendant_policy')}",
        "",
        "## Errors",
        "",
    ]
    if result.errors:
        for error in result.errors:
            lines.append(f"- `{error.code}` {error.path}: {error.message}".strip())
    else:
        lines.append("- none")
    lines += ["", "## Warnings", ""]
    if result.warnings:
        for warning in result.warnings:
            lines.append(f"- `{warning.code}` {warning.path}: {warning.message}".strip())
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


@app.command()
def main(
    bundle_dir: Path = typer.Option(..., "--bundle-dir", exists=True, file_okay=False, dir_okay=True),
    doc_id: str = typer.Option(..., "--doc-id"),
    format: str = typer.Option("markdown", "--format"),
    out: Optional[Path] = typer.Option(None, "--out"),
) -> None:
    result = check_bundle(bundle_dir=bundle_dir, doc_id=doc_id)
    if format == "json":
        rendered = json.dumps(result.to_dict(), ensure_ascii=False, indent=2)
    elif format == "yaml":
        rendered = yaml.safe_dump(result.to_dict(), sort_keys=False, allow_unicode=True)
    elif format == "markdown":
        rendered = render_markdown(result)
    else:
        raise typer.BadParameter("format must be markdown, json, or yaml")

    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        typer.echo(rendered)
    if not result.passed:
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
