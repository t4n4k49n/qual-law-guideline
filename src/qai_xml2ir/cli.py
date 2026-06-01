from __future__ import annotations

import json
import logging
from importlib.metadata import PackageNotFoundError, version as pkg_version
from datetime import date
from pathlib import Path
from typing import List, Optional, Sequence
import tomllib

import typer
import yaml

from .egov_parser import collect_display_names as collect_egov_display_names
from .egov_parser import parse_egov_xml
from .ecfr_parser import collect_display_names as collect_ecfr_display_names
from .ecfr_parser import parse_ecfr_xml
from .models_ir import IRDocument
from .models_meta import build_meta
from .models_profiles import build_ecfr_parser_profile, build_parser_profile, build_regdoc_profile
from .nid_migration import (
    build_existing_nids,
    build_report,
    load_nids_file,
    migrate_nids,
    render_output_data,
)
from .serialize import sha256_file, write_yaml
from .verify import (
    assert_unique_nids,
    check_article_paragraph_structure,
    check_annex_article_nids,
    check_appendix_scoped_indices,
    check_ord_format_and_order,
)

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


def _normalize_as_of_for_doc_id(as_of: Optional[str]) -> Optional[str]:
    if not as_of:
        return None
    return as_of.replace('-', '')


def build_default_doc_id(
    law_id: Optional[str],
    as_of: Optional[str],
    revision_id: Optional[str],
    stem: str,
) -> str:
    if law_id and as_of and revision_id:
        as_of_raw = _normalize_as_of_for_doc_id(as_of)
        return f"jp_egov_{law_id}_{as_of_raw}_{revision_id}"
    if law_id and as_of:
        as_of_raw = _normalize_as_of_for_doc_id(as_of)
        return f"jp_egov_{law_id}_{as_of_raw}"
    return stem


def build_default_cfr_doc_id(cfr_title: Optional[str], cfr_part: Optional[str], as_of: Optional[str], stem: str) -> str:
    if cfr_title and cfr_part and as_of:
        return f"us_cfr_title{cfr_title}_part{cfr_part}_{as_of.replace('-', '')}"
    if cfr_title and cfr_part:
        return f"us_cfr_title{cfr_title}_part{cfr_part}"
    return stem


def _resolve_tool_version() -> Optional[str]:
    try:
        return pkg_version("qai-xml2ir")
    except PackageNotFoundError:
        pyproject = Path(__file__).resolve().parents[2] / "pyproject.toml"
        if not pyproject.exists():
            return None
        try:
            parsed = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError):
            return None
        project = parsed.get("project", {})
        value = project.get("version")
        if isinstance(value, str) and value.strip():
            return value.strip()
        return None


@app.command()
def bundle(
    input: Path = typer.Option(..., "--input", exists=True, dir_okay=False),
    out_dir: Path = typer.Option(..., "--out-dir", file_okay=False),
    doc_id: Optional[str] = typer.Option(None, "--doc-id"),
    short_title: Optional[str] = typer.Option(None, "--short-title"),
    retrieved_at: Optional[str] = typer.Option(None, "--retrieved-at"),
    source_url: Optional[str] = typer.Option(None, "--source-url"),
    xml_family: str = typer.Option("egov", "--xml-family", help="XML family: egov or ecfr"),
    emit_only: str = typer.Option("all", "--emit-only"),
) -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    if xml_family not in {"egov", "ecfr"}:
        raise typer.BadParameter("--xml-family must be 'egov' or 'ecfr'")

    index = {"display_name_by_nid": {}}
    if xml_family == "ecfr":
        parsed = parse_ecfr_xml(input)
        doc_id = doc_id or build_default_cfr_doc_id(parsed.cfr_title, parsed.cfr_part, parsed.as_of, input.stem)
        collect_ecfr_display_names(parsed.root, index["display_name_by_nid"])
        parser_profile = build_ecfr_parser_profile()
        meta_kwargs = {
            "title": parsed.title or doc_id,
            "doc_type": "regulation",
            "law_id": None,
            "law_number": None,
            "as_of": parsed.as_of,
            "revision_id": None,
            "jurisdiction": "US",
            "language": "en",
            "source_label": "eCFR",
            "cfr_title": parsed.cfr_title,
            "cfr_part": parsed.cfr_part,
            "notes": parsed.notes,
        }
    else:
        parsed = parse_egov_xml(input)
        doc_id = doc_id or build_default_doc_id(parsed.law_id, parsed.as_of, parsed.revision_id, input.stem)
        collect_egov_display_names(parsed.root, index["display_name_by_nid"])
        parser_profile = build_parser_profile()
        meta_kwargs = {
            "title": parsed.title or doc_id,
            "doc_type": guess_doc_type(parsed.law_number),
            "law_id": parsed.law_id,
            "law_number": parsed.law_number,
            "as_of": parsed.as_of,
            "revision_id": parsed.revision_id,
            "jurisdiction": "JP",
            "language": "ja",
            "source_label": "e-Gov",
            "cfr_title": None,
            "cfr_part": None,
            "notes": [],
        }

    ir_doc = IRDocument(doc_id=doc_id, content=parsed.root, index=index)
    _run_verify_or_fail(ir_doc.content)

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
            title=meta_kwargs["title"],
            short_title=short_title,
            doc_type=meta_kwargs["doc_type"],
            law_id=meta_kwargs["law_id"],
            law_number=meta_kwargs["law_number"],
            as_of=meta_kwargs["as_of"],
            revision_id=meta_kwargs["revision_id"],
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
            tool_version=_resolve_tool_version(),
            notes=meta_kwargs["notes"],
            jurisdiction=meta_kwargs["jurisdiction"],
            language=meta_kwargs["language"],
            source_label=meta_kwargs["source_label"],
            cfr_title=meta_kwargs["cfr_title"],
            cfr_part=meta_kwargs["cfr_part"],
        )
        write_yaml(meta_path, meta)


def _run_verify_or_fail(root) -> None:
    assert_unique_nids(root)
    collisions, invalid_annex = check_annex_article_nids(root)
    appendix_problems = check_appendix_scoped_indices(root)
    ord_problems = check_ord_format_and_order(root)
    article_paragraph_problems = check_article_paragraph_structure(root)

    errors = []
    if collisions:
        errors.append(f"annex nid collisions: {collisions}")
    if invalid_annex:
        errors.append(f"invalid annex article nids: {invalid_annex}")
    if appendix_problems:
        errors.append(f"appendix index problems: {appendix_problems}")
    if ord_problems:
        errors.append(f"ord problems: {ord_problems}")
    if article_paragraph_problems:
        errors.append(f"article/paragraph structure problems: {article_paragraph_problems}")

    if errors:
        raise typer.BadParameter("verify failed: " + " | ".join(errors))


def _discover_inputs(paths: Sequence[Path]) -> List[Path]:
    supported = {".yaml", ".yml", ".json", ".txt", ".md"}
    collected: List[Path] = []
    for p in paths:
        if p.is_file():
            collected.append(p)
            continue
        if p.is_dir():
            for child in sorted(p.rglob("*")):
                if child.is_file() and child.suffix.lower() in supported:
                    collected.append(child)
            continue
        raise typer.BadParameter(f"入力パスが存在しません: {p}")
    # 順序維持 dedup
    unique: List[Path] = []
    seen = set()
    for c in collected:
        key = str(c.resolve())
        if key in seen:
            continue
        seen.add(key)
        unique.append(c)
    return unique


def _default_out_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}.migrated{input_path.suffix}")


def _default_report_path(out_path: Path) -> Path:
    return out_path.with_name(f"{out_path.stem}.report.yaml")


@app.command("migrate-checksheet-nids")
def migrate_checksheet_nids(
    input: List[Path] = typer.Option(..., "--input", exists=True),
    ir: Path = typer.Option(..., "--ir", exists=True, dir_okay=False),
    out: Optional[Path] = typer.Option(None, "--out"),
    report: Optional[Path] = typer.Option(None, "--report"),
    out_dir: Optional[Path] = typer.Option(None, "--out-dir"),
    dedup: bool = typer.Option(True, "--dedup/--no-dedup"),
    on_unresolved: str = typer.Option("error", "--on-unresolved"),
    purpose: Optional[str] = typer.Option(None, "--purpose"),
) -> None:
    if on_unresolved not in {"error", "warn", "ignore"}:
        raise typer.BadParameter("--on-unresolved must be error|warn|ignore")

    inputs = _discover_inputs(input)
    if not inputs:
        raise typer.BadParameter("入力ファイルが見つかりません")

    if len(inputs) > 1 and out is not None:
        raise typer.BadParameter("--out は単一入力時のみ指定可能です")
    if len(inputs) > 1 and report is not None:
        raise typer.BadParameter("--report は単一入力時のみ指定可能です")

    ir_data = yaml.safe_load(ir.read_text(encoding="utf-8"))
    existing_nids, _kind_by_nid = build_existing_nids(ir_data)

    total_files = 0
    total_unresolved = 0
    summary_rows: List[str] = []

    for src in inputs:
        loaded = load_nids_file(src)
        result = migrate_nids(loaded.nids, existing_nids, dedup=dedup)
        total_files += 1
        total_unresolved += result.unresolved_count

        if out_dir is not None:
            target_out = out_dir / src.name
        elif out is not None and len(inputs) == 1:
            target_out = out
        else:
            target_out = _default_out_path(src)
        target_out.parent.mkdir(parents=True, exist_ok=True)

        rendered = render_output_data(loaded, result.resolved_nids)
        target_out.write_text(rendered, encoding="utf-8", newline="\n")

        if out_dir is not None:
            target_report = out_dir / f"{src.stem}.migrated.report.yaml"
        elif report is not None and len(inputs) == 1:
            target_report = report
        else:
            target_report = _default_report_path(target_out)
        target_report.parent.mkdir(parents=True, exist_ok=True)

        report_data = build_report(
            input_path=src,
            ir_path=ir,
            result=result,
            purpose=purpose,
        )
        target_report.write_text(
            yaml.safe_dump(report_data, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
            newline="\n",
        )

        if result.unresolved_count and on_unresolved == "warn":
            typer.secho(
                f"[WARN] unresolved nids in {src}: {result.unresolved_count}",
                fg=typer.colors.YELLOW,
                err=True,
            )

        summary_rows.append(
            json.dumps(
                {
                    "input": str(src),
                    "out": str(target_out),
                    "report": str(target_report),
                    "changed": result.changed_count,
                    "unchanged": result.unchanged_count,
                    "unresolved": result.unresolved_count,
                },
                ensure_ascii=False,
            )
        )

    for row in summary_rows:
        typer.echo(row, err=True)
    typer.echo(
        f"migrate-checksheet-nids summary: files={total_files}, unresolved_total={total_unresolved}, on_unresolved={on_unresolved}",
        err=True,
    )

    if total_unresolved and on_unresolved == "error":
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
