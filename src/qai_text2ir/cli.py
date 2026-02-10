from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import typer

from qai_xml2ir.models_meta import build_meta
from qai_xml2ir.serialize import sha256_file, write_yaml
from qai_xml2ir.verify import verify_document

from .profile_loader import load_parser_profile
from .text_parser import parse_text_to_ir

app = typer.Typer(add_completion=False)


def _build_regdoc_profile(doc_id: str) -> Dict[str, Any]:
    return {
        "schema": "qai.regdoc_profile.v1",
        "doc_id": doc_id,
        "profiles": {
            "dq_gmp_checklist": {
                "selectable_kinds": ["subitem", "item", "paragraph", "statement"],
                "grouping_policy": [
                    {"when_kind": "subitem", "group_under_kind": "item"},
                    {"when_kind": "item", "group_under_kind": "paragraph"},
                    {"when_kind": "paragraph", "group_under_kind": "section"},
                    {"when_kind": "statement", "group_under_kind": "section"},
                ],
                "context_display_policy": [
                    {
                        "when_kind": "subitem",
                        "include_ancestors_until_kind": "section",
                        "include_headings": True,
                        "include_chapeau_text": True,
                    },
                    {
                        "when_kind": "item",
                        "include_ancestors_until_kind": "section",
                        "include_headings": True,
                        "include_chapeau_text": True,
                    },
                    {
                        "when_kind": "paragraph",
                        "include_ancestors_until_kind": "section",
                        "include_headings": True,
                        "include_chapeau_text": True,
                    },
                ],
                "render_templates": {},
            }
        },
    }


def _build_text_meta(
    *,
    doc_id: str,
    title: str,
    short_title: str,
    cfr_title: Optional[str],
    cfr_part: Optional[str],
    source_url: Optional[str],
    retrieved_at: Optional[str],
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
    meta["doc"]["jurisdiction"] = "US"
    meta["doc"]["language"] = "en"
    meta["doc"]["doc_type"] = "regulation"
    meta["doc"]["identifiers"]["cfr_title"] = cfr_title
    meta["doc"]["identifiers"]["cfr_part"] = cfr_part
    meta["doc"]["sources"] = [
        {
            "url": source_url,
            "format": "txt",
            "retrieved_at": retrieved_at,
            "checksum": None,
            "label": "CFR",
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
    emit_only: str = typer.Option("all", "--emit-only"),
) -> None:
    if emit_only not in {"all", "meta", "parser_profile", "regdoc_ir", "regdoc_profile"}:
        raise typer.BadParameter(
            "--emit-only must be one of: all|meta|parser_profile|regdoc_ir|regdoc_profile"
        )

    resolved_doc_id = doc_id or input.stem
    resolved_title = title or resolved_doc_id
    resolved_short_title = short_title or resolved_title

    parser_profile = load_parser_profile()
    ir_doc = parse_text_to_ir(
        input_path=input,
        doc_id=resolved_doc_id,
        parser_profile=parser_profile,
    )
    verify_document(ir_doc.to_dict())

    regdoc_profile = _build_regdoc_profile(resolved_doc_id)

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
            parser_profile_id=parser_profile["id"],
            ir_path=ir_path.name,
            parser_profile_path=parser_profile_path.name,
            regdoc_profile_path=regdoc_profile_path.name,
            input_path=str(input),
            input_checksum=sha256_file(input),
        )
        write_yaml(meta_path, meta)


if __name__ == "__main__":
    app()

