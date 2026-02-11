from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

import typer
import yaml

from qai_xml2ir.models_meta import build_meta
from qai_xml2ir.serialize import sha256_file, write_yaml
from qai_xml2ir.verify import verify_document

from .profile_loader import load_parser_profile
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
                "selectable_kinds": ["subitem", "item", "paragraph", "statement"],
                "grouping_policy": [
                    {"when_kind": "subitem", "group_under_kind": "item"},
                    {"when_kind": "item", "group_under_kind": "paragraph"},
                    {"when_kind": "paragraph", "group_under_kind": context_root_kind},
                    {"when_kind": "statement", "group_under_kind": context_root_kind},
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


def _build_text_meta(
    *,
    doc_id: str,
    title: str,
    short_title: str,
    cfr_title: Optional[str],
    cfr_part: Optional[str],
    source_url: Optional[str],
    retrieved_at: Optional[str],
    jurisdiction: str,
    language: str,
    source_label: str,
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
        doc_type="regulation",
        law_id=None,
        law_number=None,
        as_of=None,
        revision_id=None,
        effective_from=None,
        effective_to=None,
        revision_note=None,
        source_url=None,
        retrieved_at=None,
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
    meta["doc"]["doc_type"] = "regulation"
    meta["doc"]["identifiers"]["cfr_title"] = cfr_title
    meta["doc"]["identifiers"]["cfr_part"] = cfr_part
    meta["doc"]["sources"] = [
        {
            "url": source_url,
            "format": "txt",
            "retrieved_at": retrieved_at,
            "checksum": None,
            "label": source_label,
        }
    ]
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
    source_url: Optional[str] = typer.Option(None, "--source-url"),
    retrieved_at: Optional[str] = typer.Option(None, "--retrieved-at"),
    parser_profile_path: Optional[Path] = typer.Option(None, "--parser-profile", exists=True, dir_okay=False),
    parser_profile_id: Optional[str] = typer.Option(None, "--parser-profile-id"),
    regdoc_profile_path: Optional[Path] = typer.Option(None, "--regdoc-profile", exists=True, dir_okay=False),
    context_root_kind: Optional[str] = typer.Option(None, "--context-root-kind"),
    jurisdiction: Optional[str] = typer.Option(None, "--jurisdiction"),
    language: Optional[str] = typer.Option(None, "--language"),
    emit_only: str = typer.Option("all", "--emit-only"),
    qualitycheck: bool = typer.Option(True, "--qualitycheck/--no-qualitycheck"),
    strict: bool = typer.Option(False, "--strict"),
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
    if not isinstance(source_url, str):
        source_url = None
    if not isinstance(retrieved_at, str):
        retrieved_at = None
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

    if emit_only not in {"all", "meta", "parser_profile", "regdoc_ir", "regdoc_profile"}:
        raise typer.BadParameter(
            "--emit-only must be one of: all|meta|parser_profile|regdoc_ir|regdoc_profile"
        )

    resolved_doc_id = doc_id or input.stem
    resolved_title = title or resolved_doc_id
    resolved_short_title = short_title or resolved_title

    parser_profile = load_parser_profile(
        profile_id=parser_profile_id,
        path=parser_profile_path,
        family="US_CFR",
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
            source_url=source_url,
            retrieved_at=retrieved_at,
            jurisdiction=resolved_jurisdiction,
            language=resolved_language,
            source_label=source_label,
            parser_profile_id=parser_profile["id"],
            ir_path=ir_path.name,
            parser_profile_path=parser_profile_path.name,
            regdoc_profile_path=regdoc_profile_path.name,
            input_path=_safe_meta_input_path(input),
            input_checksum=sha256_file(input),
        )
        write_yaml(meta_path, meta)


if __name__ == "__main__":
    app()
