from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Tuple

import yaml


def _extract_yaml_body(chunk: str) -> str:
    lines = chunk.splitlines()
    # txtconcat は先頭にファイル名や区切り情報が入る場合があるため、
    # YAMLの開始候補(schema/doc_id/profiles/content/index)から本文を探す。
    for idx, line in enumerate(lines):
        if line.startswith(("schema:", "doc_id:", "profiles:", "content:", "index:")):
            return "\n".join(lines[idx:]).strip()
    return chunk.strip()


def _classify_chunk(raw_chunk: str) -> tuple[str | None, Dict[str, Any] | None]:
    chunk = raw_chunk.strip()
    if not chunk:
        return None, None
    hint_head = "\n".join(chunk.splitlines()[:5]).lower()
    body = _extract_yaml_body(chunk)
    if not body:
        return None, None
    meta_hint = (".meta" in hint_head) or ("qai.regdoc_meta" in body.lower())
    try:
        parsed = yaml.safe_load(body)
    except yaml.YAMLError:
        # meta は表示補助用途。metaのみ壊れている場合はスキップして継続する。
        if meta_hint:
            return "meta", None
        raise
    if not isinstance(parsed, dict):
        return None, None

    schema = str(parsed.get("schema") or "").lower()
    if ".regdoc_ir" in hint_head or "qai.regdoc_ir" in schema:
        return "regdoc_ir", parsed
    if ".regdoc_profile" in hint_head or "qai.regdoc_profile" in schema:
        return "regdoc_profile", parsed
    if ".meta" in hint_head or "qai.regdoc_meta" in schema:
        return "meta", parsed
    return None, None


def load_regdoc_ir_and_profile_from_txtconcat(path: str | Path) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    ir, profile, _ = load_regdoc_bundle_from_txtconcat(path)
    return ir, profile


def load_regdoc_bundle_from_txtconcat(
    path: str | Path,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any] | None]:
    txt_path = Path(path)
    if not txt_path.exists():
        raise FileNotFoundError(f"txtconcat が見つかりません: {txt_path}")
    raw = txt_path.read_text(encoding="utf-8")
    chunks = [c for c in raw.split("==========") if c.strip()]
    ir: Dict[str, Any] | None = None
    profile: Dict[str, Any] | None = None
    meta: Dict[str, Any] | None = None

    for chunk in chunks:
        kind, parsed = _classify_chunk(chunk)
        if kind == "regdoc_ir":
            ir = parsed
        elif kind == "regdoc_profile":
            profile = parsed
        elif kind == "meta":
            meta = parsed

    if ir is None:
        raise ValueError("txtconcat から regdoc_ir.yaml を抽出できませんでした。")
    if profile is None:
        raise ValueError("txtconcat から regdoc_profile.yaml を抽出できませんでした。")
    return ir, profile, meta
