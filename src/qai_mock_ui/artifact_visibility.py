from __future__ import annotations

from typing import Any, Iterable

ARTIFACT_TAGS = {
    "form_artifact",
    "layout_artifact",
    "not_selectable",
    "sanitized_layout_artifact",
    "reference_only",
}
ARTIFACT_KIND_RAWS = {"form_artifact", "layout_artifact", "artifact"}


def _has_any(values: Iterable[str], targets: set[str]) -> bool:
    return bool({str(value) for value in values} & targets)


def is_artifact_like(
    *,
    kind: str | None,
    kind_raw: str | None = None,
    tags: Iterable[str] = (),
    visibility: dict[str, Any] | None = None,
) -> bool:
    if str(kind_raw or "") in ARTIFACT_KIND_RAWS:
        return True
    if _has_any(tags, ARTIFACT_TAGS):
        return True
    if isinstance(visibility, dict):
        if visibility.get("default_review") == "hidden":
            return True
        if visibility.get("dq_gmp_checklist") == "hidden":
            return True
    return False


def is_default_visible_node(node: Any) -> bool:
    return not is_artifact_like(
        kind=getattr(node, "kind", None),
        kind_raw=getattr(node, "kind_raw", None),
        tags=getattr(node, "tags", []) or [],
        visibility=getattr(node, "visibility", {}) or {},
    )


def is_default_visible_raw(node: dict[str, Any]) -> bool:
    return not is_artifact_like(
        kind=str(node.get("kind") or ""),
        kind_raw=str(node.get("kind_raw") or ""),
        tags=[str(tag) for tag in (node.get("tags") or [])],
        visibility=node.get("visibility") if isinstance(node.get("visibility"), dict) else {},
    )
