from __future__ import annotations

import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import typer
import yaml

from qai_xml2ir.models_meta import build_meta
from qai_xml2ir.serialize import sha256_file, write_yaml
from qai_xml2ir.verify import verify_document

from .profile_loader import load_parser_profile_with_provenance
from .text_parser import parse_text_to_ir, qualitycheck_document

app = typer.Typer(add_completion=False)


def _read_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise typer.BadParameter(f"Invalid YAML content: {path}")
    return data


def _infer_default_language(jurisdiction: Optional[str], parser_profile: Dict[str, Any]) -> str:
    explicit = parser_profile.get("language")
    if isinstance(explicit, str) and explicit.strip():
        return explicit
    applies_to = parser_profile.get("applies_to") or {}
    by_applies_to = applies_to.get("language")
    if isinstance(by_applies_to, str) and by_applies_to.strip():
        return by_applies_to
    if jurisdiction == "JP":
        return "ja"
    return "en"


def _infer_source_label(parser_profile: Dict[str, Any]) -> str:
    explicit = parser_profile.get("source_label")
    if isinstance(explicit, str) and explicit.strip():
        return explicit
    applies_to = parser_profile.get("applies_to") or {}
    family = applies_to.get("family")
    if isinstance(family, str) and family.strip():
        return family
    return "text"


def _build_regdoc_profile(doc_id: str, context_root_kind: str = "section") -> Dict[str, Any]:
    return {
        "schema": "qai.regdoc_profile.v1",
        "doc_id": doc_id,
        "profiles": {
            "dq_gmp_checklist": {
                "selectable_kinds": ["subitem", "item", "paragraph", "statement", "table_row"],
                "grouping_policy": [
                    {"when_kind": "subitem", "group_under_kind": "item"},
                    {"when_kind": "item", "group_under_kind": "paragraph"},
                    {"when_kind": "paragraph", "group_under_kind": context_root_kind},
                    {"when_kind": "statement", "group_under_kind": context_root_kind},
                    {"when_kind": "table_row", "group_under_kind": "table"},
                ],
                "context_display_policy": [
                    {
                        "when_kind": "subitem",
                        "include_ancestors_until_kind": context_root_kind,
                        "include_headings": True,
                        "include_chapeau_text": True,
                    },
                    {
                        "when_kind": "item",
                        "include_ancestors_until_kind": context_root_kind,
                        "include_headings": True,
                        "include_chapeau_text": True,
                    },
                    {
                        "when_kind": "paragraph",
                        "include_ancestors_until_kind": context_root_kind,
                        "include_headings": True,
                        "include_chapeau_text": True,
                    },
                    {
                        "when_kind": "table_row",
                        "include_ancestors_until_kind": context_root_kind,
                        "include_headings": True,
                        "include_chapeau_text": True,
                        "include_descendants": True,
                        "include_descendants_of": "ancestors",
                        "include_descendants_kinds": ["note"],
                        "include_descendants_max_depth": 3,
                    },
                ],
                "render_templates": {},
            }
        },
    }


def _safe_meta_input_path(input_path: Path) -> str:
    try:
        return str(input_path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return input_path.name


def _write_yaml_no_prompt(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(
            data,
            f,
            allow_unicode=True,
            sort_keys=False,
            width=float("inf"),
        )


def _git_info() -> Tuple[Optional[str], Optional[str]]:
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except Exception:
        commit = None
    try:
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except Exception:
        branch = None
    return commit or None, branch or None


def _extract_tag_value(tags: List[str], prefix: str) -> Optional[str]:
    token = f"{prefix}="
    for tag in tags:
        if tag.startswith(token):
            return tag[len(token) :]
    return None


def _extract_refine_summary(ir_doc: Dict[str, Any]) -> Dict[str, Any]:
    root = ir_doc.get("content") or {}
    children = root.get("children") or []
    applied: List[Dict[str, str]] = []
    refine_kind: Optional[str] = None
    for node in children:
        if not isinstance(node, dict):
            continue
        tags = node.get("tags") or []
        if not isinstance(tags, list):
            continue
        used_profile_id = _extract_tag_value(tags, "refined_by")
        if not used_profile_id:
            continue
        key = str(node.get("num") or _extract_tag_value(tags, "refine_key") or "")
        node_refine_kind = _extract_tag_value(tags, "refine_kind")
        if node_refine_kind and refine_kind is None:
            refine_kind = node_refine_kind
        applied.append({"key": key, "used_profile_id": used_profile_id})
    return {"kind": refine_kind or "annex", "applied": applied}


def _build_text_meta(
    *,
    doc_id: str,
    title: str,
    short_title: str,
    cfr_title: Optional[str],
    cfr_part: Optional[str],
    doc_type: str,
    source_url: Optional[str],
    source_format: str,
    retrieved_at: Optional[str],
    jurisdiction: str,
    language: str,
    source_label: str,
    eu_volume: Optional[str],
    pics_doc_id: Optional[str],
    who_publication_id: Optional[str],
    parser_profile_id: str,
    ir_path: str,
    parser_profile_path: str,
    regdoc_profile_path: str,
    input_path: str,
    input_checksum: str,
) -> Dict[str, Any]:
    meta = build_meta(
        doc_id=doc_id,
        title=title,
        short_title=short_title,
        doc_type=doc_type,
        law_id=None,
        law_number=None,
        as_of=None,
        revision_id=None,
        effective_from=None,
        effective_to=None,
        revision_note=None,
        source_url=source_url,
        retrieved_at=retrieved_at,
        parser_profile_id=parser_profile_id,
        ir_path=ir_path,
        parser_profile_path=parser_profile_path,
        regdoc_profile_path=regdoc_profile_path,
        input_path=input_path,
        input_checksum=input_checksum,
        tool_version=None,
        notes=[],
    )
    meta["doc"]["jurisdiction"] = jurisdiction
    meta["doc"]["language"] = language
    identifiers = meta["doc"].setdefault("identifiers", {})
    if cfr_title:
        identifiers["cfr_title"] = cfr_title
    else:
        identifiers.pop("cfr_title", None)
    if cfr_part:
        identifiers["cfr_part"] = cfr_part
    else:
        identifiers.pop("cfr_part", None)
    if eu_volume:
        identifiers["eu_volume"] = eu_volume
    else:
        identifiers.pop("eu_volume", None)
    if pics_doc_id:
        identifiers["pics_doc_id"] = pics_doc_id
    else:
        identifiers.pop("pics_doc_id", None)
    if who_publication_id:
        identifiers["who_publication_id"] = who_publication_id
    else:
        identifiers.pop("who_publication_id", None)

    if source_url:
        meta["doc"]["sources"] = [
            {
                "url": source_url,
                "format": source_format,
                "retrieved_at": retrieved_at,
                "checksum": None,
                "label": source_label,
            }
        ]
    else:
        meta["doc"]["sources"] = []
    meta["generation"]["tool"]["name"] = "qai_text2ir"
    meta["generation"]["created_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return meta


@app.command()
def bundle(
    input: Path = typer.Option(..., "--input", exists=True, dir_okay=False),
    out_dir: Path = typer.Option(..., "--out-dir", file_okay=False),
    doc_id: Optional[str] = typer.Option(None, "--doc-id"),
    title: Optional[str] = typer.Option(None, "--title"),
    short_title: Optional[str] = typer.Option(None, "--short-title"),
    cfr_title: Optional[str] = typer.Option(None, "--cfr-title"),
    cfr_part: Optional[str] = typer.Option(None, "--cfr-part"),
    doc_type: str = typer.Option("regulation", "--doc-type"),
    source_url: Optional[str] = typer.Option(None, "--source-url"),
    source_format: Optional[str] = typer.Option(None, "--source-format"),
    retrieved_at: Optional[str] = typer.Option(None, "--retrieved-at"),
    eu_volume: Optional[str] = typer.Option(None, "--eu-volume"),
    pics_doc_id: Optional[str] = typer.Option(None, "--pics-doc-id"),
    who_publication_id: Optional[str] = typer.Option(None, "--who-publication-id"),
    parser_profile_path: Optional[Path] = typer.Option(None, "--parser-profile", exists=True, dir_okay=False),
    parser_profile_id: Optional[str] = typer.Option(None, "--parser-profile-id"),
    regdoc_profile_path: Optional[Path] = typer.Option(None, "--regdoc-profile", exists=True, dir_okay=False),
    context_root_kind: Optional[str] = typer.Option(None, "--context-root-kind"),
    jurisdiction: Optional[str] = typer.Option(None, "--jurisdiction"),
    language: Optional[str] = typer.Option(None, "--language"),
    family: Optional[str] = typer.Option(None, "--family"),
    emit_only: str = typer.Option("all", "--emit-only"),
    qualitycheck: bool = typer.Option(True, "--qualitycheck/--no-qualitycheck"),
    strict: bool = typer.Option(False, "--strict"),
    write_manifest: bool = typer.Option(True, "--write-manifest/--no-write-manifest"),
    overwrite_manifest: bool = typer.Option(False, "--overwrite-manifest"),
) -> None:
    if not isinstance(doc_id, str):
        doc_id = None
    if not isinstance(title, str):
        title = None
    if not isinstance(short_title, str):
        short_title = None
    if not isinstance(cfr_title, str):
        cfr_title = None
    if not isinstance(cfr_part, str):
        cfr_part = None
    if not isinstance(doc_type, str):
        doc_type = "regulation"
    if not isinstance(source_url, str):
        source_url = None
    if not isinstance(source_format, str):
        source_format = None
    if not isinstance(retrieved_at, str):
        retrieved_at = None
    if not isinstance(eu_volume, str):
        eu_volume = None
    if not isinstance(pics_doc_id, str):
        pics_doc_id = None
    if not isinstance(who_publication_id, str):
        who_publication_id = None
    if not isinstance(parser_profile_path, Path):
        parser_profile_path = None
    if not isinstance(parser_profile_id, str):
        parser_profile_id = None
    if not isinstance(regdoc_profile_path, Path):
        regdoc_profile_path = None
    if not isinstance(context_root_kind, str):
        context_root_kind = None
    if not isinstance(jurisdiction, str):
        jurisdiction = None
    if not isinstance(language, str):
        language = None
    if not isinstance(family, str):
        family = None

    if emit_only not in {"all", "meta", "parser_profile", "regdoc_ir", "regdoc_profile"}:
        raise typer.BadParameter(
            "--emit-only must be one of: all|meta|parser_profile|regdoc_ir|regdoc_profile"
        )

    resolved_doc_id = doc_id or input.stem
    resolved_title = title or resolved_doc_id
    resolved_short_title = short_title or resolved_title
    inferred_source_format = source_format
    if inferred_source_format is None:
        lowered = (source_url or "").lower()
        inferred_source_format = "pdf" if ".pdf" in lowered else "txt"

    resolved_family = family or ("WHO_LBM" if (jurisdiction or "").upper() == "WHO" else "US_CFR")
    parser_profile, profile_provenance = load_parser_profile_with_provenance(
        profile_id=parser_profile_id,
        path=parser_profile_path,
        family=resolved_family,
    )
    applies_to = parser_profile.get("applies_to") or {}
    resolved_jurisdiction = jurisdiction or applies_to.get("jurisdiction") or "US"
    resolved_language = language or _infer_default_language(resolved_jurisdiction, parser_profile)
    source_label = _infer_source_label(parser_profile)
    ir_doc = parse_text_to_ir(
        input_path=input,
        doc_id=resolved_doc_id,
        parser_profile=parser_profile,
    )
    qc_warnings: List[str] = []
    if qualitycheck:
        qc_warnings = qualitycheck_document(ir_doc.content)
        for msg in qc_warnings:
            typer.echo(f"[qualitycheck] {msg}", err=True)
        if strict and qc_warnings:
            raise typer.BadParameter(
                f"qualitycheck found {len(qc_warnings)} warning(s); re-run with --no-qualitycheck or fix input/profile."
            )
    verify_document(ir_doc.to_dict())

    if regdoc_profile_path:
        regdoc_profile = _read_yaml(regdoc_profile_path)
    else:
        resolved_context_root_kind = context_root_kind or parser_profile.get("context_root_kind") or (
            "section" if resolved_jurisdiction == "US" else "chapter"
        )
        regdoc_profile = _build_regdoc_profile(resolved_doc_id, context_root_kind=resolved_context_root_kind)

    stem = resolved_doc_id
    ir_path = out_dir / f"{stem}.regdoc_ir.yaml"
    parser_profile_path = out_dir / f"{stem}.parser_profile.yaml"
    regdoc_profile_path = out_dir / f"{stem}.regdoc_profile.yaml"
    meta_path = out_dir / f"{stem}.meta.yaml"

    if emit_only in {"all", "regdoc_ir"}:
        write_yaml(ir_path, ir_doc.to_dict())
    if emit_only in {"all", "parser_profile"}:
        write_yaml(parser_profile_path, parser_profile)
    if emit_only in {"all", "regdoc_profile"}:
        write_yaml(regdoc_profile_path, regdoc_profile)
    if emit_only in {"all", "meta"}:
        meta = _build_text_meta(
            doc_id=resolved_doc_id,
            title=resolved_title,
            short_title=resolved_short_title,
            cfr_title=cfr_title,
            cfr_part=cfr_part,
            doc_type=doc_type,
            source_url=source_url,
            source_format=inferred_source_format,
            retrieved_at=retrieved_at,
            jurisdiction=resolved_jurisdiction,
            language=resolved_language,
            source_label=source_label,
            eu_volume=eu_volume,
            pics_doc_id=pics_doc_id,
            who_publication_id=who_publication_id,
            parser_profile_id=parser_profile["id"],
            ir_path=ir_path.name,
            parser_profile_path=parser_profile_path.name,
            regdoc_profile_path=regdoc_profile_path.name,
            input_path=_safe_meta_input_path(input),
            input_checksum=sha256_file(input),
        )
        write_yaml(meta_path, meta)

    if write_manifest:
        manifest_path = out_dir / "manifest.yaml"
        if manifest_path.exists() and not overwrite_manifest:
            typer.echo(
                f"[manifest] skip existing file (use --overwrite-manifest): {manifest_path}",
                err=True,
            )
            return
        commit, branch = _git_info()
        command_argv = " ".join(shlex.quote(v) for v in sys.argv)
        parser_profile_sha = sha256_file(parser_profile_path) if parser_profile_path.exists() else None
        ir_dict = ir_doc.to_dict()
        manifest: Dict[str, Any] = {
            "schema": "qai.run_manifest.v1",
            "run_id": out_dir.name,
            "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "git": {"commit": commit, "branch": branch},
            "input": {
                "path": _safe_meta_input_path(input),
                "checksum": sha256_file(input),
            },
            "command": {"argv": command_argv},
            "outputs": {
                "doc_id": resolved_doc_id,
                "files": [
                    f"{stem}.regdoc_ir.yaml",
                    f"{stem}.parser_profile.yaml",
                    f"{stem}.regdoc_profile.yaml",
                    f"{stem}.meta.yaml",
                ],
            },
            "parser_profile": {
                "id": str(parser_profile.get("id") or ""),
                "resolved_sha256": parser_profile_sha,
                "provenance": profile_provenance,
            },
            "qualitycheck": {
                "enabled": bool(qualitycheck),
                "strict": bool(strict),
                "warnings_count": len(qc_warnings),
                "warnings": qc_warnings[:20],
            },
            "refine": _extract_refine_summary(ir_dict),
        }
        _write_yaml_no_prompt(manifest_path, manifest)


if __name__ == "__main__":
    app()
