from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


ARTICLE_FORBIDDEN_CHILDREN = {"item", "subitem", "point"}


@dataclass
class Problem:
    file: Path
    code: str
    article_nid: str
    detail: str


def _walk_nodes(node: dict[str, Any]):
    yield node
    for child in node.get("children") or []:
        if isinstance(child, dict):
            yield from _walk_nodes(child)


def _load_ir_root(path: Path) -> dict[str, Any] | None:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(raw, dict):
        return None
    content = raw.get("content")
    if not isinstance(content, dict):
        return None
    if content.get("kind") != "document":
        return None
    return content


def _iter_yaml_paths(input_path: Path):
    if input_path.is_file():
        yield input_path
        return
    for path in sorted(input_path.rglob("*.yaml")):
        yield path


def check_file(path: Path) -> list[Problem]:
    root = _load_ir_root(path)
    if root is None:
        return []

    problems: list[Problem] = []
    for node in _walk_nodes(root):
        if node.get("kind") != "article":
            continue
        nid = str(node.get("nid") or "<unknown>")
        text = node.get("text")
        children = [c for c in (node.get("children") or []) if isinstance(c, dict)]
        child_kinds = [str(c.get("kind") or "") for c in children]

        if isinstance(text, str) and text.strip():
            problems.append(
                Problem(
                    file=path,
                    code="A",
                    article_nid=nid,
                    detail="article.text is not null/empty",
                )
            )

        forbidden = [k for k in child_kinds if k in ARTICLE_FORBIDDEN_CHILDREN]
        if forbidden:
            problems.append(
                Problem(
                    file=path,
                    code="B",
                    article_nid=nid,
                    detail=f"article has forbidden direct children: {sorted(set(forbidden))}",
                )
            )

        if "paragraph" not in child_kinds:
            problems.append(
                Problem(
                    file=path,
                    code="C",
                    article_nid=nid,
                    detail="article has no direct paragraph child",
                )
            )

    return problems


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check IR YAML structure for article/paragraph invariants. "
            "Input can be a single IR YAML file or a directory."
        )
    )
    parser.add_argument("input", type=Path, help="IR YAML file or directory")
    args = parser.parse_args()

    input_path: Path = args.input
    if not input_path.exists():
        print(f"[ERROR] path not found: {input_path}")
        return 1

    all_problems: list[Problem] = []
    scanned = 0
    for path in _iter_yaml_paths(input_path):
        scanned += 1
        all_problems.extend(check_file(path))

    if not all_problems:
        print(f"[OK] no structure problems found (scanned: {scanned} yaml files)")
        return 0

    print(f"[NG] found {len(all_problems)} problems")
    for p in all_problems:
        print(f"- file={p.file} code={p.code} article={p.article_nid}: {p.detail}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
