from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional


def build_meta(
    *,
    doc_id: str,
    title: str,
    short_title: Optional[str],
    doc_type: str,
    law_id: Optional[str],
    law_number: Optional[str],
    as_of: Optional[str],
    revision_id: Optional[str],
    effective_from: Optional[str],
    effective_to: Optional[str],
    revision_note: Optional[str],
    source_url: Optional[str],
    retrieved_at: Optional[str],
    parser_profile_id: str,
    ir_path: str,
    parser_profile_path: str,
    regdoc_profile_path: str,
    input_path: str,
    input_checksum: Optional[str],
    tool_version: Optional[str] = None,
    notes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    return {
        "schema": "qai.regdoc_meta.v1",
        "doc": {
            "id": doc_id,
            "title": title,
            "short_title": short_title,
            "jurisdiction": "JP",
            "doc_type": doc_type,
            "language": "ja",
            "issuer": {"name": None, "kind": None},
            "identifiers": {
                "e_gov_law_id": law_id,
                "e_gov_revision_id": revision_id,
                "law_number": law_number,
                "cfr_title": None,
                "cfr_part": None,
                "eu_volume": None,
                "pics_doc_id": None,
                "who_publication_id": None,
            },
            "version": {
                "as_of": as_of,
                "effective_from": effective_from,
                "effective_to": effective_to,
                "revision_note": revision_note,
            },
            "sources": [
                {
                    "url": source_url,
                    "format": "xml",
                    "retrieved_at": retrieved_at,
                    "checksum": None,
                    "label": "e-Gov",
                }
            ]
            if source_url
            else [],
            "legal_meta": {
                "competent_authority": [],
                "legal_basis": [],
                "binding_level": None,
                "license_note": None,
            },
        },
        "bundle": {
            "ir": {"schema": "qai.regdoc_ir.v4", "path": ir_path},
            "parser_profile": {
                "schema": "qai.parser_profile.v1",
                "id": parser_profile_id,
                "path": parser_profile_path,
            },
            "regdoc_profile": {
                "schema": "qai.regdoc_profile.v1",
                "path": regdoc_profile_path,
            },
        },
        "generation": {
            "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "tool": {"name": "qai_xml2ir", "version": tool_version},
            "inputs": [{"path": input_path, "checksum": input_checksum}],
            "notes": notes or [],
        },
    }
