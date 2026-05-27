from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Iterable

import yaml


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"IR YAML must be a mapping: {path}")
    return data


def _iter_children(node: dict[str, Any]) -> Iterable[dict[str, Any]]:
    children = node.get("children") or []
    if not isinstance(children, list):
        return []
    return (child for child in children if isinstance(child, dict))


def find_path(root: dict[str, Any], target_nid: str) -> list[dict[str, Any]] | None:
    stack: list[tuple[dict[str, Any], list[dict[str, Any]]]] = [(root, [])]
    while stack:
        node, ancestors = stack.pop()
        path = [*ancestors, node]
        if node.get("nid") == target_nid:
            return path
        for child in reversed(list(_iter_children(node))):
            stack.append((child, path))
    return None


def _inline_code(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).replace("\r\n", " ").replace("\n", " ").strip()
    if not text:
        return ""
    escaped = text.replace("`", "\\`")
    return f"`{escaped}`"


def _node_text(node: dict[str, Any], blank_text_kinds: set[str]) -> str:
    kind = str(node.get("kind") or "")
    if kind in blank_text_kinds:
        return ""
    heading = node.get("heading")
    if isinstance(heading, str) and heading.strip():
        return heading
    text = node.get("text")
    if isinstance(text, str) and text.strip():
        return text
    return ""


def render_markdown(
    *,
    ir_path: Path,
    target_nid: str,
    path: list[dict[str, Any]],
    blank_text_kinds: set[str],
) -> str:
    lines = [
        "# 深い階層サンプル抽出",
        "",
        f"- source: `{ir_path.as_posix()}`",
        f"- target_nid: `{target_nid}`",
        "- method: IR YAMLをparseし、target_nidの祖先経路を抽出",
        "",
        "| 階層 | nid | kind | kind_raw | text / heading |",
        "|---:|---|---|---|---|",
    ]
    for level, node in enumerate(path, start=1):
        lines.append(
            "| "
            + " | ".join(
                [
                    str(level),
                    _inline_code(node.get("nid")),
                    _inline_code(node.get("kind")),
                    _inline_code(node.get("kind_raw")),
                    _inline_code(_node_text(node, blank_text_kinds)),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Extract an ancestor-path review sample from RegDoc IR YAML."
    )
    parser.add_argument("--ir", required=True, type=Path, help="Path to *.regdoc_ir.yaml")
    parser.add_argument("--nid", required=True, help="Target node nid")
    parser.add_argument("--output", type=Path, help="Markdown output path. Defaults to stdout.")
    parser.add_argument(
        "--blank-text-kind",
        action="append",
        default=[],
        help="Node kind whose text/heading cell should be left blank. Can be repeated.",
    )
    args = parser.parse_args(argv)

    ir_doc = _load_yaml(args.ir)
    root = ir_doc.get("content")
    if not isinstance(root, dict):
        raise ValueError(f"IR YAML has no mapping content root: {args.ir}")
    sample_path = find_path(root, args.nid)
    if sample_path is None:
        print(f"target nid not found: {args.nid}", file=sys.stderr)
        return 1

    markdown = render_markdown(
        ir_path=args.ir,
        target_nid=args.nid,
        path=sample_path,
        blank_text_kinds=set(args.blank_text_kind or []),
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8", newline="\n")
    else:
        print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
