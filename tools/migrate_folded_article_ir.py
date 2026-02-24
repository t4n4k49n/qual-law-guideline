from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

FOLDED_DIRECT_KINDS = {"item", "subitem", "point"}


@dataclass
class MigrationSummary:
    articles_migrated: int = 0
    nids_rewritten: int = 0


def _walk_nodes(node: dict[str, Any]):
    yield node
    for child in node.get("children") or []:
        if isinstance(child, dict):
            yield from _walk_nodes(child)


def _assign_document_order_dict(root: dict[str, Any]) -> None:
    counter = 0
    for node in _walk_nodes(root):
        if node.get("nid") == "root":
            node["ord"] = None
            continue
        counter += 1
        node["ord"] = counter


def _insert_p1_in_nid(nid: str, article_nid: str) -> str:
    prefix = f"{article_nid}."
    if not nid.startswith(prefix):
        return nid
    remainder = nid[len(prefix) :]
    return f"{article_nid}.p1.{remainder}"


def _rewrite_subtree_nids(node: dict[str, Any], article_nid: str, summary: MigrationSummary) -> None:
    nid = node.get("nid")
    if isinstance(nid, str):
        new_nid = _insert_p1_in_nid(nid, article_nid)
        if new_nid != nid:
            node["nid"] = new_nid
            summary.nids_rewritten += 1
    for child in node.get("children") or []:
        if isinstance(child, dict):
            _rewrite_subtree_nids(child, article_nid, summary)


def _make_paragraph_node(article: dict[str, Any], moved_children: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "nid": f"{article['nid']}.p1",
        "kind": "paragraph",
        "kind_raw": "項",
        "num": "1",
        "ord": None,
        "heading": None,
        "text": article.get("text"),
        "role": article.get("role"),
        "normativity": article.get("normativity"),
        "tags": [],
        "refs": {"internal": [], "external": []},
        "source_spans": [],
        "children": moved_children,
    }


def migrate_ir(raw: dict[str, Any]) -> MigrationSummary:
    content = raw.get("content")
    if not isinstance(content, dict):
        raise ValueError("Invalid IR YAML: missing dict content")

    summary = MigrationSummary()
    for node in _walk_nodes(content):
        if node.get("kind") != "article":
            continue
        children = [c for c in (node.get("children") or []) if isinstance(c, dict)]
        child_kinds = [str(c.get("kind") or "") for c in children]
        has_paragraph = "paragraph" in child_kinds
        has_folded_children = any(k in FOLDED_DIRECT_KINDS for k in child_kinds)
        has_article_text = isinstance(node.get("text"), str) and bool(node.get("text").strip())
        needs_rescue = (not has_paragraph) and (has_article_text or has_folded_children)
        if not needs_rescue:
            continue

        article_nid = str(node.get("nid"))
        moved_children = copy.deepcopy(children)
        for child in moved_children:
            _rewrite_subtree_nids(child, article_nid, summary)

        p1 = _make_paragraph_node(node, moved_children)
        node["children"] = [p1]
        node["text"] = None
        summary.articles_migrated += 1

    _assign_document_order_dict(content)
    raw["index"] = {}
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Migrate folded article IR to article->paragraph structure. "
            "Rescue use only; prefer XML re-generation."
        )
    )
    parser.add_argument("--input", type=Path, required=True, help="Input IR YAML")
    parser.add_argument("--output", type=Path, required=True, help="Output IR YAML")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"[ERROR] input not found: {args.input}")
        return 1

    raw = yaml.safe_load(args.input.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        print("[ERROR] invalid IR YAML")
        return 1

    summary = migrate_ir(raw)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        yaml.safe_dump(raw, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
        newline="\n",
    )

    print(
        "[OK] migrated"
        f" articles={summary.articles_migrated}"
        f" nids_rewritten={summary.nids_rewritten}"
        f" output={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
