#!/usr/bin/env python3
"""Check normalized promotion completion against main branch.

Exit 0 only when:
1) promotion_commit exists
2) promotion_commit is an ancestor of main_ref
"""

from __future__ import annotations

import argparse
import subprocess
import sys


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def fail(msg: str) -> int:
    print(f"ERROR: {msg}", file=sys.stderr)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify normalized promotion commit is reflected in main."
    )
    parser.add_argument(
        "--promotion-commit",
        required=True,
        help="Promotion commit SHA to verify.",
    )
    parser.add_argument(
        "--main-ref",
        default="origin/main",
        help="Main branch ref to verify against (default: origin/main).",
    )
    parser.add_argument(
        "--skip-fetch",
        action="store_true",
        help="Skip `git fetch origin` before verification.",
    )
    args = parser.parse_args()

    if not args.skip_fetch:
        fetch = run_git(["fetch", "origin"])
        if fetch.returncode != 0:
            return fail(f"`git fetch origin` failed: {fetch.stderr.strip()}")

    exists = run_git(["rev-parse", "--verify", f"{args.promotion_commit}^{{commit}}"])
    if exists.returncode != 0:
        return fail(
            f"promotion_commit not found: {args.promotion_commit} ({exists.stderr.strip()})"
        )

    ancestor = run_git(
        ["merge-base", "--is-ancestor", args.promotion_commit, args.main_ref]
    )
    if ancestor.returncode != 0:
        return fail(
            f"promotion_commit is NOT in {args.main_ref}: {args.promotion_commit}"
        )

    print(
        f"OK: promotion_commit exists and is merged into {args.main_ref}: {args.promotion_commit}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

