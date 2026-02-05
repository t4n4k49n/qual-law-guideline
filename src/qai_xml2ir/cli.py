from __future__ import annotations

import logging
from datetime import date
from pathlib import Path
from typing import Optional

import typer

from .egov_parser import collect_display_names, parse_egov_xml
from .models_ir import IRDocument
from .models_meta import build_meta
from .models_profiles import build_parser_profile, build_regdoc_profile
from .serialize import sha256_file, write_yaml

app = typer.Typer(add_completion=False)


def guess_doc_type(law_number: Optional[str]) -> str:
    if not law_number:
        return "statute"
    if "省令" in law_number:
        return "ministerial_ordinance"
    if "政令" in law_number:
        return "cabinet_order"
    if "規則" in law_number:
        return "rule"
    if "告示" in law_number:
        return "notice"
    if "法律" in law_number:
        return "statute"
    return "statute"


def build_default_doc_id(law_id: Optional[str], as_of: Optional[str], stem: str) -> str:
    if law_id and as_of:
        return f"jp_egov_{law_id}_{as_of}"
    return stem


@app.command()
def bundle(
    input: Path = typer.Option(..., "--input", exists=True, dir_okay=False),
    out_dir: Path = typer.Option(..., "--out-dir", file_okay=False),
    doc_id: Optional[str] = typer.Option(None, "--doc-id"),
    short_title: Optional[str] = typer.Option(None, "--short-title"),
    retrieved_at: Optional[str] = typer.Option(None, "--retrieved-at"),
    source_url: Optional[str] = typer.Option(None, "--source-url"),
    emit_only: str = typer.Option("all", "--emit-only"),
) -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    parsed = parse_egov_xml(input)
    doc_id = doc_id or build_default_doc_id(parsed.law_id, parsed.as_of, input.stem)

    index = {"display_name_by_nid": {}}
    collect_display_names(parsed.root, index["display_name_by_nid"])
    ir_doc = IRDocument(doc_id=doc_id, content=parsed.root, index=index)

    parser_profile = build_parser_profile()
    regdoc_profile = build_regdoc_profile(doc_id)

    stem = doc_id
    ir_path = out_dir / f"{stem}.regdoc_ir.yaml"
    parser_profile_path = out_dir / f"{stem}.parser_profile.yaml"
    regdoc_profile_path = out_dir / f"{stem}.regdoc_profile.yaml"
    meta_path = out_dir / f"{stem}.meta.yaml"

    if emit_only not in {"all", "ir"}:
        raise typer.BadParameter("--emit-only must be 'all' or 'ir'")

    if emit_only in {"all", "ir"}:
        write_yaml(ir_path, ir_doc.to_dict())

    if emit_only == "all":
        write_yaml(parser_profile_path, parser_profile)
        write_yaml(regdoc_profile_path, regdoc_profile)

        retrieved = retrieved_at or date.today().isoformat()
        input_checksum = sha256_file(input)
        meta = build_meta(
            doc_id=doc_id,
            title=parsed.title or doc_id,
            short_title=short_title,
            doc_type=guess_doc_type(parsed.law_number),
            law_id=parsed.law_id,
            law_number=parsed.law_number,
            as_of=parsed.as_of,
            effective_from=None,
            effective_to=None,
            revision_note=None,
            source_url=source_url,
            retrieved_at=retrieved,
            parser_profile_id=parser_profile["id"],
            ir_path=ir_path.name,
            parser_profile_path=parser_profile_path.name,
            regdoc_profile_path=regdoc_profile_path.name,
            input_path=str(input),
            input_checksum=input_checksum,
            tool_version=None,
            notes=[],
        )
        write_yaml(meta_path, meta)


if __name__ == "__main__":
    app()
